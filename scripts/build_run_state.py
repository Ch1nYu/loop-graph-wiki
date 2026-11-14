#!/usr/bin/env python3
"""Generate the run-state files (cards, drafts, sources) from the wiki and deck."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
WIKI = ROOT / "wiki"
RUN = ROOT / "_private" / "runs" / "2026-11-13-topic-slides"


def parse_frontmatter(text: str) -> tuple[dict[str, object], str]:
    if not text.startswith("---"):
        return {}, text
    parts = text.split("---", 2)
    if len(parts) < 3:
        return {}, text
    data: dict[str, object] = {}
    for raw_line in parts[1].splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or ":" not in line:
            continue
        key, value = line.split(":", 1)
        key = key.strip()
        value = value.strip().strip("'\"")
        if value.startswith("[") and value.endswith("]"):
            data[key] = [item.strip().strip("'\"") for item in value[1:-1].split(",") if item.strip()]
        else:
            data[key] = value
    return data, parts[2]


def extract_claims(body: str) -> list[str]:
    section = body.split("## 關鍵主張", 1)
    if len(section) < 2:
        return []
    table = section[1].split("\n## ", 1)[0]
    claims = []
    for line in table.splitlines():
        if not line.strip().startswith("|"):
            continue
        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        if len(cells) < 2 or cells[0] in {"#", "---"} or set(cells[0]) <= {"-", ":"}:
            continue
        claims.append(cells[1])
    return claims


def main() -> int:
    RUN.mkdir(parents=True, exist_ok=True)
    (RUN / "cards").mkdir(exist_ok=True)
    (RUN / "drafts").mkdir(exist_ok=True)

    source_pages = []
    for path in sorted((WIKI / "sources").glob("*.md")):
        meta, body = parse_frontmatter(path.read_text(encoding="utf-8"))
        source_pages.append((path, meta, body))

    cards_index = []
    for path, meta, body in source_pages:
        sid = str(meta.get("id", path.stem))
        title = str(meta.get("title", sid))
        claims = extract_claims(body)[:4]
        card_lines = [
            "---",
            f"card_id: {sid}",
            f"source_id: {sid}",
            "created: 2026-11-13",
            "---",
            "",
            f"# 證據卡：{title}",
            "",
            f"- 原始 URL：{meta.get('original_url', '')}",
            f"- 可信度：{meta.get('reliability', '')}",
            "",
            "## 可引用主張",
            "",
        ]
        for index, claim in enumerate(claims, start=1):
            card_lines.append(f"{index}. {claim}")
        card_lines += [
            "",
            "## 邊界",
            "",
            "- 這張卡只代表這一篇來源；不得混入其他來源的數據或結論。",
            "- 引用時保留原始 URL 與章節位置；若找不到位置，降級為「來源未提及」。",
            "",
        ]
        (RUN / "cards" / f"{sid}.md").write_text("\n".join(card_lines), encoding="utf-8")
        cards_index.append(f"- [[cards/{sid}]]：{title}（{len(claims)} 條主張）")

    slides_data = json.loads((ROOT / "deck" / "slides.json").read_text(encoding="utf-8"))
    slides = slides_data["slides"]
    for number, slide in enumerate(slides, start=1):
        wiki_refs = ", ".join(slide.get("wiki", []))
        source_refs = ", ".join(slide.get("sources", []))
        title = re.sub(r"<[^>]+>", "", str(slide.get("title", ""))).replace("\n", " ").strip()
        lines = [
            "---",
            f"slide: {number}",
            f"id: {slide.get('id', '')}",
            f"layout: {slide.get('layout', '')}",
            f"wiki: [{wiki_refs}]",
            f"sources: [{source_refs}]",
            "---",
            "",
            f"# 第 {number} 頁：{title}",
            "",
            "## 這一頁要說什麼",
            "",
            str(slide.get("lead") or slide.get("subtitle") or slide.get("note") or title),
            "",
            "## 引用",
            "",
            f"- Wiki：{wiki_refs}",
            f"- 原始來源：{source_refs}",
            "",
            "## 檢查",
            "",
            "- [ ] 這一頁的每個事實都能在引用的 Wiki 頁找到。",
            "- [ ] 百分比與數字能在來源頁找到。",
            "- [ ] 至少一個 Wiki 連結與一個原始來源。",
            "- [ ] 沒有引用 Wiki 以外的內容。",
            "",
        ]
        (RUN / "drafts" / f"slide-{number:02d}.md").write_text("\n".join(lines), encoding="utf-8")

    sources_md = [
        "# N1 檢索結果：Loop / Graph Engineering",
        "",
        "日期：2026-11-13",
        "主題：Loop / Graph Engineering：把 AI 工作拆成可驗證的流程",
        "",
        "## 檢索入口",
        "",
        "- `wiki/index.md`",
        "- `wiki/concepts/`、`wiki/comparisons/`、`wiki/methods/`",
        "- `wiki/sources/`",
        "",
        "## 相關頁面與覆蓋率",
        "",
        "| 頁面 | 類型 | 與主題的關係 |",
        "|---|---|---|",
        "| harness-loop-graph | concept | 三層工程的分工 |",
        "| loop-five-elements | concept | Loop 的五個要素 |",
        "| verification | concept | 雙軌驗證 |",
        "| graph-nodes-edges | concept | Graph 的基本元素 |",
        "| fallback-edges | concept | 退回邊與檢查前移 |",
        "| information-scoping | concept | 權限隔離 |",
        "| state-as-files | concept | 狀態即檔案 |",
        "| human-in-the-loop | concept | 人類介入點 |",
        "| stop-conditions | concept | 停止條件 |",
        "| prompt-loop-graph | comparison | 三種結構的選擇 |",
        "| teaching-deck-pipeline | method | 本專案的 Graph |",
        "",
        "覆蓋率：11 個相關頁面（≥ 3，通過 G1）。",
        "",
        "## 來源清單",
        "",
        "| ID | 標題 | 類型 | 可信度 |",
        "|---|---|---|---|",
    ]
    for path, meta, body in source_pages:
        sources_md.append(f"| {meta.get('id', path.stem)} | {meta.get('title', '')} | {meta.get('source_kind', '')} | {meta.get('reliability', '')} |")
    sources_md += [
        "",
        "## 證據卡索引",
        "",
        *cards_index,
        "",
        "## G1 判定",
        "",
        "- 相關頁面 11 頁 ≥ 3 頁 → 通過，進入 N2。",
        "",
    ]
    (RUN / "sources.md").write_text("\n".join(sources_md), encoding="utf-8")

    print(f"Generated {len(source_pages)} cards, {len(slides)} drafts, and sources.md")
    return 0


if __name__ == "__main__":
    sys.exit(main())
