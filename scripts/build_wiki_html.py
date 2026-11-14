#!/usr/bin/env python3
"""Build a single-file, human-readable mirror of the Markdown LLM Wiki."""

from __future__ import annotations

import html
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
WIKI = ROOT / "wiki"

TYPE_LABELS = {
    "index": "首頁",
    "concept": "概念",
    "comparison": "比較",
    "method": "方法",
    "source": "來源",
    "glossary": "術語",
    "log": "日誌",
}

TYPE_ORDER = ["index", "concept", "comparison", "method", "source", "glossary", "log"]


def esc(value: object) -> str:
    return html.escape(str(value), quote=True)


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


def inline(text: str, aliases: dict[str, str], titles: dict[str, str]) -> str:
    text = esc(text)

    def wiki_link(match: re.Match[str]) -> str:
        raw = match.group(1)
        target, _, label = raw.partition("|")
        target = target.split("#", 1)[0].strip()
        pid = aliases.get(target) or aliases.get(target.split("/")[-1])
        anchor = pid or target
        display = label or titles.get(pid or "", target)
        return f'<a href="#{esc(anchor)}">{esc(display)}</a>'

    text = re.sub(r"\[\[([^\]]+)\]\]", wiki_link, text)
    text = re.sub(
        r"\[([^\]]+)\]\((https?://[^)]+)\)",
        lambda m: f'<a href="{m.group(2)}" target="_blank" rel="noopener">{m.group(1)}</a>',
        text,
    )
    text = re.sub(r"`([^`]+)`", r"<code>\1</code>", text)
    text = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", text)
    text = re.sub(r"(?<!\*)\*([^*]+)\*(?!\*)", r"<em>\1</em>", text)
    return text


def markdown_to_html(body: str, aliases: dict[str, str], titles: dict[str, str], page_title: str) -> str:
    lines = body.splitlines()
    output: list[str] = []
    i = 0
    while i < len(lines):
        line = lines[i]
        stripped = line.strip()
        if not stripped:
            i += 1
            continue
        if stripped.startswith("<!--"):
            while i < len(lines) and "-->" not in lines[i]:
                i += 1
            i += 1
            continue
        if stripped.startswith("```"):
            language = stripped[3:].strip()
            i += 1
            code_lines = []
            while i < len(lines) and not lines[i].strip().startswith("```"):
                code_lines.append(lines[i])
                i += 1
            i += 1
            output.append(f'<pre class="code"><code>{esc(chr(10).join(code_lines))}</code></pre>')
            continue
        heading = re.match(r"^(#{1,6})\s+(.*)$", stripped)
        if heading:
            level = len(heading.group(1))
            heading_text = heading.group(2)
            if level == 1 and heading_text.strip() == page_title.strip():
                i += 1
                continue
            output.append(f"<h{level}>{inline(heading_text, aliases, titles)}</h{level}>")
            i += 1
            continue
        if stripped.startswith("|") and i + 1 < len(lines) and re.match(r"^\|?[\s:|-]+\|?$", lines[i + 1].strip()):
            table_lines = []
            while i < len(lines) and lines[i].strip().startswith("|"):
                table_lines.append(lines[i].strip())
                i += 1
            rows = []
            for row_index, row in enumerate(table_lines):
                cells = [cell.strip() for cell in row.strip("|").split("|")]
                if row_index == 1 and all(re.match(r"^:?-{2,}:?$", cell) for cell in cells):
                    continue
                tag = "th" if row_index == 0 else "td"
                rows.append("<tr>" + "".join(f"<{tag}>{inline(cell, aliases, titles)}</{tag}>" for cell in cells) + "</tr>")
            output.append('<div class="table-wrap"><table>' + "".join(rows) + "</table></div>")
            continue
        if stripped.startswith(">"):
            quote_lines = []
            while i < len(lines) and lines[i].strip().startswith(">"):
                quote_lines.append(lines[i].strip()[1:].strip())
                i += 1
            output.append(f"<blockquote>{inline(' '.join(quote_lines), aliases, titles)}</blockquote>")
            continue
        if re.match(r"^[-*]\s+", stripped):
            items = []
            while i < len(lines) and re.match(r"^[-*]\s+", lines[i].strip()):
                items.append(re.sub(r"^[-*]\s+", "", lines[i].strip()))
                i += 1
            output.append("<ul>" + "".join(f"<li>{inline(item, aliases, titles)}</li>" for item in items) + "</ul>")
            continue
        if re.match(r"^\d+\.\s+", stripped):
            items = []
            while i < len(lines) and re.match(r"^\d+\.\s+", lines[i].strip()):
                items.append(re.sub(r"^\d+\.\s+", "", lines[i].strip()))
                i += 1
            output.append("<ol>" + "".join(f"<li>{inline(item, aliases, titles)}</li>" for item in items) + "</ol>")
            continue
        if stripped in {"---", "***"}:
            output.append("<hr>")
            i += 1
            continue
        paragraph = [stripped]
        i += 1
        while i < len(lines):
            nxt = lines[i].strip()
            if not nxt or nxt.startswith(("#", "|", ">", "```", "-", "*")) or re.match(r"^\d+\.\s+", nxt):
                break
            paragraph.append(nxt)
            i += 1
        output.append(f"<p>{inline(' '.join(paragraph), aliases, titles)}</p>")
    return "\n".join(output)


def main() -> int:
    pages = []
    aliases: dict[str, str] = {}
    for path in sorted(WIKI.rglob("*.md")):
        text = path.read_text(encoding="utf-8")
        meta, body = parse_frontmatter(text)
        pid = str(meta.get("id") or path.stem)
        aliases[pid] = pid
        aliases[path.relative_to(WIKI).with_suffix("").as_posix()] = pid
        aliases[path.stem] = pid
        pages.append({"id": pid, "meta": meta, "body": body, "path": path})

    pages.sort(key=lambda page: (TYPE_ORDER.index(str(page["meta"].get("type", "concept"))) if str(page["meta"].get("type", "concept")) in TYPE_ORDER else 99, str(page["meta"].get("title", page["id"]))))
    titles = {str(page["id"]): str(page["meta"].get("title", page["id"])) for page in pages}

    nav_groups: dict[str, list[dict]] = {}
    for page in pages:
        ptype = str(page["meta"].get("type", "concept"))
        nav_groups.setdefault(ptype, []).append(page)

    nav_parts = []
    for ptype in TYPE_ORDER:
        if ptype not in nav_groups:
            continue
        nav_parts.append(f'<div class="nav-group"><div class="nav-label">{esc(TYPE_LABELS.get(ptype, ptype))}</div>')
        for page in nav_groups[ptype]:
            title = str(page["meta"].get("title", page["id"]))
            nav_parts.append(f'<a class="nav-link" href="#{esc(page["id"])}" data-title="{esc(title)}">{esc(title)}</a>')
        nav_parts.append("</div>")

    sections = []
    for page in pages:
        title = str(page["meta"].get("title", page["id"]))
        ptype = str(page["meta"].get("type", "concept"))
        body_html = markdown_to_html(str(page["body"]), aliases, titles, title)
        heading_id = re.sub(r"[^\w\u4e00-\u9fff-]+", "-", title.strip().lower()).strip("-")
        sections.append(
            f'<section class="wiki-page" id="{esc(page["id"])}" data-title="{esc(title)}">'
            f'<div class="page-kicker">{esc(TYPE_LABELS.get(ptype, ptype))} · {esc(page["id"])}</div>'
            f'<h1 id="{esc(heading_id)}">{esc(title)}</h1>{body_html}</section>'
        )

    css = """
:root{--paper:#f4efe4;--white:#fffdf8;--ink:#171512;--ink2:#3d3831;--muted:#7c7264;--line:#cfc4b2;--accent:#c6472e;--gold:#d9a441;--serif:"Noto Serif TC","Songti TC","PMingLiU",serif;--sans:"Noto Sans TC","Microsoft JhengHei",sans-serif;--mono:"Cascadia Mono",Consolas,monospace}
*{box-sizing:border-box}html{scroll-behavior:smooth}body{margin:0;background:var(--paper);color:var(--ink);font-family:var(--sans);line-height:1.7}
.layout{display:grid;grid-template-columns:320px minmax(0,1fr);min-height:100vh}
.sidebar{position:sticky;top:0;height:100vh;overflow:auto;padding:28px 22px;border-right:1px solid var(--line);background:rgba(255,253,248,.55)}
.brand{font-family:var(--serif);font-size:26px;line-height:1.1;margin-bottom:6px}.brand small{display:block;margin-top:8px;color:var(--muted);font:600 10px/1.4 var(--mono);letter-spacing:.12em}
.search{width:100%;margin:20px 0 18px;padding:10px 12px;border:1px solid var(--line);background:var(--white);font:14px var(--sans);color:var(--ink)}
.nav-group{margin-bottom:18px}.nav-label{color:var(--accent);font:700 10px/1 var(--mono);letter-spacing:.16em;margin-bottom:8px}
.nav-link{display:block;padding:6px 0;color:var(--ink2);text-decoration:none;font-size:14px;border-bottom:1px solid transparent}
.nav-link:hover{color:var(--accent);border-bottom-color:var(--accent)}
.content{max-width:980px;padding:48px 56px 100px}
.wiki-page{padding:34px 0 54px;border-bottom:1px solid var(--line);scroll-margin-top:20px}
.wiki-page:target{background:rgba(198,71,46,.04)}
.page-kicker{color:var(--accent);font:700 10px/1 var(--mono);letter-spacing:.16em;text-transform:uppercase;margin-bottom:10px}
h1,h2,h3,h4{font-family:var(--serif);font-weight:600;letter-spacing:-.02em;line-height:1.2}
h1{font-size:42px;margin:0 0 18px}h2{font-size:30px;margin:36px 0 12px}h3{font-size:22px;margin:26px 0 8px}
p{margin:10px 0;color:var(--ink2)}a{color:var(--accent)}strong{color:var(--ink)}
blockquote{margin:18px 0;padding:12px 18px;border-left:4px solid var(--accent);background:rgba(198,71,46,.05);font-family:var(--serif);font-size:20px}
code{padding:2px 5px;background:rgba(23,21,18,.08);font-family:var(--mono);font-size:.9em}
pre.code{padding:18px;overflow:auto;background:var(--ink);color:var(--paper);font:13px/1.65 var(--mono)}
pre.code code{padding:0;background:none;color:inherit}
.table-wrap{overflow:auto;margin:16px 0}table{width:100%;border-collapse:collapse;font-size:14px}
th{text-align:left;padding:9px 10px;border-bottom:2px solid var(--ink);font:700 10px/1.3 var(--mono);letter-spacing:.08em;color:var(--muted)}
td{padding:10px;border-bottom:1px solid var(--line);vertical-align:top;color:var(--ink2)}
ul,ol{padding-left:22px;color:var(--ink2)}li{margin:5px 0}
hr{border:0;border-top:1px solid var(--line);margin:26px 0}
.top-note{padding:14px 18px;border:1px solid var(--line);background:var(--white);color:var(--muted);font-size:13px}
@media(max-width:900px){.layout{grid-template-columns:1fr}.sidebar{position:relative;height:auto;border-right:0;border-bottom:1px solid var(--line)}.content{padding:28px 20px 80px}h1{font-size:34px}}
@media print{.sidebar,.search{display:none}.layout{grid-template-columns:1fr}.content{padding:0}.wiki-page{page-break-after:always}}
"""

    js = """
const search = document.getElementById('search');
const links = Array.from(document.querySelectorAll('.nav-link'));
const pages = Array.from(document.querySelectorAll('.wiki-page'));
search.addEventListener('input', () => {
  const q = search.value.trim().toLowerCase();
  links.forEach(link => {
    const text = (link.dataset.title + ' ' + link.getAttribute('href')).toLowerCase();
    link.style.display = !q || text.includes(q) ? 'block' : 'none';
  });
  pages.forEach(page => {
    const text = (page.dataset.title + ' ' + page.textContent).toLowerCase();
    page.style.display = !q || text.includes(q) ? 'block' : 'none';
  });
});
"""

    html_doc = f"""<!DOCTYPE html>
<html lang="zh-Hant">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Loop / Graph Engineering Wiki</title>
  <style>{css}</style>
</head>
<body>
  <div class="layout">
    <aside class="sidebar">
      <div class="brand">Loop / Graph Engineering<small>LLM WIKI · 2026-11-13</small></div>
      <input class="search" id="search" type="search" placeholder="搜尋頁面與內容…">
      {''.join(nav_parts)}
    </aside>
    <main class="content">
      <div class="top-note">這是 <code>wiki/</code> 的人類可讀鏡像，由 <code>scripts/build_wiki_html.py</code> 從 Markdown 產生。AI 檢索仍以 <code>wiki/index.md</code> 為入口。</div>
      {''.join(sections)}
    </main>
  </div>
  <script>{js}</script>
</body>
</html>
"""
    (ROOT / "wiki.html").write_text(html_doc, encoding="utf-8")
    print(f"Built wiki.html with {len(pages)} pages")
    return 0


if __name__ == "__main__":
    sys.exit(main())
