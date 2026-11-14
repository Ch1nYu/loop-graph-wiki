#!/usr/bin/env python3
"""Validate the LLM Wiki structure, citations, and language rules.

This script intentionally uses only the Python standard library so it can run
on a clean Windows machine without installing packages.
"""

from __future__ import annotations

import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
WIKI = ROOT / "wiki"
QA = ROOT / "_private" / "qa"
PRIVATE = ROOT / "_private"

REQUIRED_COMMON = ("id", "title", "type", "updated")
REQUIRED_SOURCE = ("original_url", "ingested", "reliability")
REQUIRED_CONCEPT = ("sources",)

# Simplified-only characters that should not appear in Traditional Chinese prose.
SIMPLIFIED_CHARS = set(
    "个为与这来说时会么现开关门问间长见觉从对应该还进过动务员体实际线织终结构检标确认证据资们题计划设发测试运维护团队项产验数识学习训练网络统软夹径链点击钮输错误帮优风险隐权义责骤阶节边缘图状态转换条环变参类组缓连请响协议编码签录账号话断异监邮机语视频压缩传载储备复迁滚仪盘报预评损轮敛拟则随种复论议审献综顾贡创谢录导讨"
)

WIKI_LINK_RE = re.compile(r"\[\[([^\]]+)\]\]")
HEADING_RE = re.compile(r"^(#{1,6})\s+(.*)$")
INLINE_CODE_RE = re.compile(r"`[^`]*`")


def iter_prose_lines(text: str):
    """Yield (line_number, line) while skipping fenced code and inline code."""
    in_fence = False
    for index, line in enumerate(text.splitlines(), start=1):
        if line.strip().startswith("```"):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        yield index, INLINE_CODE_RE.sub("", line)


def parse_frontmatter(text: str) -> tuple[dict[str, object], str]:
    if not text.startswith("---"):
        return {}, text
    parts = text.split("---", 2)
    if len(parts) < 3:
        return {}, text
    block = parts[1]
    body = parts[2]
    data: dict[str, object] = {}
    for raw_line in block.splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        key = key.strip()
        value = value.strip()
        if value.startswith("[") and value.endswith("]"):
            inner = value[1:-1].strip()
            data[key] = [item.strip().strip("'\"") for item in inner.split(",") if item.strip()]
        else:
            data[key] = value.strip("'\"")
    return data, body


def page_id_from_path(path: Path) -> str:
    return path.stem


def normalize_link(target: str) -> str:
    target = target.split("|", 1)[0].strip()
    target = target.split("#", 1)[0].strip()
    target = target.removesuffix(".md")
    return target


def resolve_link(target: str, aliases: dict[str, str]) -> str | None:
    target = normalize_link(target)
    if target.startswith(("http://", "https://")):
        return None
    candidates = [target, target.split("/")[-1]]
    for candidate in candidates:
        if candidate in aliases:
            return aliases[candidate]
    return None


def line_number(text: str, needle: str) -> int:
    for index, line in enumerate(text.splitlines(), start=1):
        if needle in line:
            return index
    return 1


def main() -> int:
    QA.mkdir(parents=True, exist_ok=True)
    errors: list[dict[str, object]] = []
    warnings: list[dict[str, object]] = []

    pages: dict[str, dict[str, object]] = {}
    aliases: dict[str, str] = {}
    texts: dict[str, str] = {}

    for path in sorted(WIKI.rglob("*.md")):
        rel = path.relative_to(ROOT).as_posix()
        text = path.read_text(encoding="utf-8")
        meta, body = parse_frontmatter(text)
        pid = str(meta.get("id") or page_id_from_path(path))
        if pid in pages:
            errors.append({"file": rel, "line": 1, "message": f"duplicate id: {pid}"})
        pages[pid] = {"path": path, "rel": rel, "meta": meta, "body": body}
        texts[pid] = text
        aliases[pid] = pid
        aliases[path.relative_to(WIKI).with_suffix("").as_posix()] = pid
        aliases[path.stem] = pid

    state_pages: dict[str, dict[str, object]] = {}
    run_dir = PRIVATE / "runs" / "2026-11-13-topic-slides"
    if run_dir.exists():
        for path in sorted(run_dir.rglob("*.md")):
            text = path.read_text(encoding="utf-8")
            meta, _ = parse_frontmatter(text)
            pid = str(meta.get("id") or path.stem)
            if pid in pages or pid in state_pages:
                continue
            state_pages[pid] = {"path": path, "rel": path.relative_to(ROOT).as_posix(), "meta": meta, "body": ""}
            texts[pid] = text
            aliases[pid] = pid
            aliases[path.stem] = pid

    for pid, page in pages.items():
        rel = str(page["rel"])
        meta = page["meta"]
        body = str(page["body"])
        text = texts[pid]
        ptype = str(meta.get("type", ""))

        for key in REQUIRED_COMMON:
            if not meta.get(key):
                errors.append({"file": rel, "line": 1, "message": f"missing frontmatter field: {key}"})

        if ptype == "source":
            for key in REQUIRED_SOURCE:
                if not meta.get(key):
                    errors.append({"file": rel, "line": 1, "message": f"source page missing: {key}"})
            claims_section = body.split("## 關鍵主張", 1)
            if len(claims_section) < 2:
                errors.append({"file": rel, "line": 1, "message": "source page missing '## 關鍵主張' section"})
            else:
                section = claims_section[1].split("\n## ", 1)[0]
                rows = [line for line in section.splitlines() if line.strip().startswith("|")]
                claim_rows = max(0, len(rows) - 2)
                if claim_rows < 3:
                    errors.append({"file": rel, "line": 1, "message": f"source page has only {claim_rows} claim rows (need >= 3)"})

        if ptype in {"concept", "comparison", "method"}:
            sources = meta.get("sources")
            if not isinstance(sources, list) or len(sources) < 2:
                errors.append({"file": rel, "line": 1, "message": "concept/comparison/method page needs >= 2 sources"})
            for source in sources if isinstance(sources, list) else []:
                if source not in pages:
                    errors.append({"file": rel, "line": 1, "message": f"unknown source id in frontmatter: {source}"})

        for index, line in iter_prose_lines(text):
            for match in WIKI_LINK_RE.finditer(line):
                target = match.group(1)
                if resolve_link(target, aliases) is None:
                    errors.append(
                        {
                            "file": rel,
                            "line": index,
                            "message": f"unresolved wiki link: [[{target}]]",
                        }
                    )
            for char in line:
                if char in SIMPLIFIED_CHARS:
                    errors.append(
                        {
                            "file": rel,
                            "line": index,
                            "message": f"simplified character '{char}' found: {line.strip()[:80]}",
                        }
                    )
                    break

        for marker in ("TODO", "TBD", "Lorem ipsum", "待補"):
            if marker in text:
                errors.append(
                    {
                        "file": rel,
                        "line": line_number(text, marker),
                        "message": f"placeholder marker found: {marker}",
                    }
                )

    for pid, state_page in state_pages.items():
        rel = str(state_page["rel"])
        text = texts[pid]
        for index, line in enumerate(text.splitlines(), start=1):
            for match in WIKI_LINK_RE.finditer(line):
                target = match.group(1)
                if resolve_link(target, aliases) is None:
                    errors.append(
                        {
                            "file": rel,
                            "line": index,
                            "message": f"unresolved state link: [[{target}]]",
                        }
                    )

    index_page = pages.get("index")
    if not index_page:
        errors.append({"file": "wiki/index.md", "line": 1, "message": "missing wiki/index.md with id: index"})
    else:
        index_text = texts["index"]
        index_links = {resolve_link(m.group(1), aliases) for m in WIKI_LINK_RE.finditer(index_text)}
        for pid in pages:
            if pid == "index":
                continue
            if pid not in index_links:
                errors.append({"file": "wiki/index.md", "line": 1, "message": f"index does not link to page: {pid}"})

    incoming: dict[str, set[str]] = {pid: set() for pid in pages}
    for pid, text in {key: value for key, value in texts.items() if key in pages or key in state_pages}.items():
        for match in WIKI_LINK_RE.finditer(text):
            target = resolve_link(match.group(1), aliases)
            if target and target != pid:
                incoming[target].add(pid)
    for pid, sources in incoming.items():
        if pid != "index" and not sources:
            warnings.append({"file": str(pages[pid]["rel"]), "line": 1, "message": "orphan page: no incoming links"})

    source_count = sum(1 for page in pages.values() if page["meta"].get("type") == "source")
    report = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "pages": len(pages),
        "state_pages": len(state_pages),
        "sources": source_count,
        "errors": errors,
        "warnings": warnings,
        "pass": not errors,
    }
    (QA / "wiki-report.json").write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")

    print(f"Wiki pages: {len(pages)}")
    print(f"Source pages: {source_count}")
    print(f"Errors: {len(errors)}")
    print(f"Warnings: {len(warnings)}")
    for item in errors[:80]:
        print(f"  ERROR {item['file']}:{item['line']} — {item['message']}")
    for item in warnings[:40]:
        print(f"  WARN  {item['file']}:{item['line']} — {item['message']}")
    if errors:
        print("RESULT: FAIL")
        return 1
    print("RESULT: PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
