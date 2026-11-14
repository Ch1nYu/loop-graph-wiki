#!/usr/bin/env python3
"""Validate index.html against the deck specification and citation rules."""

from __future__ import annotations

import json
import re
import sys
from datetime import datetime, timezone
from html.parser import HTMLParser
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
WIKI = ROOT / "wiki"
DECK = ROOT / "deck"
QA = ROOT / "_private" / "qa"

VOID_TAGS = {"area", "base", "br", "col", "embed", "hr", "img", "input", "link", "meta", "param", "source", "track", "wbr"}


def parse_frontmatter(text: str) -> dict[str, object]:
    if not text.startswith("---"):
        return {}
    parts = text.split("---", 2)
    if len(parts) < 3:
        return {}
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
    return data


class DeckParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.slides: list[dict[str, object]] = []
        self.current: dict[str, object] | None = None

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        attr_map = {key: value or "" for key, value in attrs}
        if tag == "section" and "slide" in attr_map.get("class", "").split():
            self.current = {"attrs": attr_map, "text": [], "html": []}
            return
        if self.current is not None:
            self.current["html"].append(self.get_starttag_text() or "")
            if tag in VOID_TAGS:
                return
            if tag in {"h1", "h2", "h3", "p", "li", "td", "th", "blockquote", "div", "span"}:
                self.current["text"].append(" ")

    def handle_endtag(self, tag: str) -> None:
        if self.current is not None:
            if tag == "section":
                self.slides.append(self.current)
                self.current = None
            else:
                self.current["html"].append(f"</{tag}>")
                if tag in {"h1", "h2", "h3", "p", "li", "td", "th", "blockquote", "div", "span"}:
                    self.current["text"].append(" ")

    def handle_data(self, data: str) -> None:
        if self.current is not None:
            self.current["text"].append(data)
            self.current["html"].append(data)


def main() -> int:
    QA.mkdir(parents=True, exist_ok=True)
    html_text = (ROOT / "index.html").read_text(encoding="utf-8")
    slides_data = json.loads((DECK / "slides.json").read_text(encoding="utf-8"))
    sources = json.loads((DECK / "sources.json").read_text(encoding="utf-8"))

    wiki_pages: dict[str, Path] = {}
    wiki_aliases: dict[str, str] = {}
    for path in sorted(WIKI.rglob("*.md")):
        meta = parse_frontmatter(path.read_text(encoding="utf-8"))
        pid = str(meta.get("id") or path.stem)
        wiki_pages[pid] = path
        wiki_aliases[pid] = pid
        wiki_aliases[path.relative_to(WIKI).with_suffix("").as_posix()] = pid
        wiki_aliases[path.stem] = pid

    parser = DeckParser()
    parser.feed(html_text)
    slides = parser.slides
    errors: list[dict[str, object]] = []
    warnings: list[dict[str, object]] = []
    wiki_html_path = ROOT / "wiki.html"
    wiki_html_ids: set[str] = set()
    if wiki_html_path.exists():
        wiki_html_ids = set(re.findall(r'<section class="wiki-page" id="([^"]+)"', wiki_html_path.read_text(encoding="utf-8")))
    else:
        errors.append({"slide": 0, "message": "wiki.html not found; run scripts/build_wiki_html.py"})

    expected = len(slides_data["slides"])
    if len(slides) != expected:
        errors.append({"slide": 0, "message": f"slide count {len(slides)} != slides.json {expected}"})
    if not 8 <= len(slides) <= 15:
        errors.append({"slide": 0, "message": f"slide count {len(slides)} is outside 8-15"})

    if 'lang="zh-Hant"' not in html_text:
        errors.append({"slide": 0, "message": "html lang is not zh-Hant"})
    if "<title>" not in html_text:
        errors.append({"slide": 0, "message": "missing <title>"})
    if 'id="qa-report"' not in html_text:
        errors.append({"slide": 0, "message": "missing #qa-report"})
    if re.search(r'<script[^>]+src=["\']https?://', html_text, re.I):
        errors.append({"slide": 0, "message": "external script dependency found"})
    if re.search(r'<link[^>]+rel=["\']stylesheet["\'][^>]+href=["\']https?://', html_text, re.I):
        errors.append({"slide": 0, "message": "external stylesheet dependency found"})
    for marker in ("TODO", "TBD", "Lorem ipsum"):
        if marker in html_text:
            errors.append({"slide": 0, "message": f"placeholder marker found: {marker}"})

    for index, slide in enumerate(slides, start=1):
        attrs = slide["attrs"]
        text = " ".join(str(item) for item in slide["text"])
        slide_html = "".join(str(item) for item in slide["html"])

        wiki_ids = [item for item in str(attrs.get("data-wiki", "")).split(",") if item]
        source_ids = [item for item in str(attrs.get("data-sources", "")).split(",") if item]
        if not wiki_ids:
            errors.append({"slide": index, "message": "missing data-wiki"})
        if not source_ids:
            errors.append({"slide": index, "message": "missing data-sources"})
        if "cite-chip" not in slide_html:
            errors.append({"slide": index, "message": "missing .cite-chip"})
        if not re.search(r"<h[12]\b", slide_html):
            errors.append({"slide": index, "message": "missing h1/h2 title"})

        corpus_parts: list[str] = []
        for wid in wiki_ids:
            pid = wiki_aliases.get(wid) or wiki_aliases.get(wid.split("/")[-1])
            if not pid:
                errors.append({"slide": index, "message": f"unknown wiki id: {wid}"})
                continue
            if wiki_html_ids and pid not in wiki_html_ids:
                errors.append({"slide": index, "message": f"wiki.html has no anchor for: {pid}"})
            corpus_parts.append(wiki_pages[pid].read_text(encoding="utf-8"))
        for sid in source_ids:
            src = sources.get(sid)
            if not src:
                errors.append({"slide": index, "message": f"unknown source id: {sid}"})
                continue
            wid = src.get("wiki", "")
            pid = wiki_aliases.get(wid) or wiki_aliases.get(str(wid).split("/")[-1])
            if pid:
                corpus_parts.append(wiki_pages[pid].read_text(encoding="utf-8"))
        corpus = "\n".join(corpus_parts)

        for pct in sorted(set(re.findall(r"\d+(?:\.\d+)?%", text))):
            if pct not in corpus:
                errors.append({"slide": index, "message": f"percentage not traceable: {pct}"})

    report = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "slides": len(slides),
        "expected": expected,
        "errors": errors,
        "warnings": warnings,
        "pass": not errors,
    }
    (QA / "deck-report.json").write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")

    print(f"Slides: {len(slides)} (expected {expected})")
    print(f"Errors: {len(errors)}")
    for item in errors:
        print(f"  ERROR slide {item['slide']} — {item['message']}")
    for item in warnings:
        print(f"  WARN  slide {item['slide']} — {item['message']}")
    if errors:
        print("RESULT: FAIL")
        return 1
    print("RESULT: PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
