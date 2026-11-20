#!/usr/bin/env python3
"""Render deck/slides.json into a self-contained index.html.

The renderer is deliberately dependency-free: it reads JSON, emits HTML/SVG,
and inlines assets/deck.css and assets/deck.js so the deck works offline and
on GitHub Pages.
"""

from __future__ import annotations

import html
import json
import math
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DECK = ROOT / "deck"
WIKI = ROOT / "wiki"
ASSETS = ROOT / "assets"

PAPER = "#f4efe4"
WHITE = "#fffdf8"
INK = "#171512"
INK2 = "#3d3831"
MUTED = "#7c7264"
LINE = "#cfc4b2"
ACCENT = "#c6472e"
TEAL = "#1f4e5f"
GOLD = "#d9a441"

FONT_SANS = "Noto Sans TC, Microsoft JhengHei, PingFang TC, sans-serif"
FONT_SERIF = "Noto Serif TC, Songti TC, PMingLiU, Palatino Linotype, serif"
FONT_MONO = "Cascadia Mono, Consolas, monospace"


def esc(value: object) -> str:
    return html.escape(str(value), quote=True)


def inline(value: object) -> str:
    text = esc(value)
    for tag in ("br", "em", "strong"):
        text = text.replace(f"&lt;{tag}&gt;", f"<{tag}>")
        text = text.replace(f"&lt;/{tag}&gt;", f"</{tag}>")
    return text


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


def load_wiki_titles() -> dict[str, str]:
    titles: dict[str, str] = {}
    for path in sorted(WIKI.rglob("*.md")):
        meta = parse_frontmatter(path.read_text(encoding="utf-8"))
        pid = str(meta.get("id") or path.stem)
        titles[pid] = str(meta.get("title") or pid)
    return titles


def svg_defs() -> str:
    return f"""
    <defs>
      <marker id="arrow-accent" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">
        <path d="M0,0 L10,5 L0,10 z" fill="{ACCENT}"/>
      </marker>
      <marker id="arrow-ink" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">
        <path d="M0,0 L10,5 L0,10 z" fill="{INK}"/>
      </marker>
      <marker id="arrow-muted" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">
        <path d="M0,0 L10,5 L0,10 z" fill="{MUTED}"/>
      </marker>
    </defs>
    """


def svg_text(
    x: float,
    y: float,
    text: str,
    size: int = 18,
    fill: str = INK,
    anchor: str = "middle",
    weight: int = 600,
    family: str = FONT_SANS,
    letter: float = 0,
) -> str:
    return (
        f'<text x="{x:.1f}" y="{y:.1f}" font-size="{size}" fill="{fill}" '
        f'text-anchor="{anchor}" font-weight="{weight}" font-family="{family}" '
        f'letter-spacing="{letter}">{esc(text)}</text>'
    )


def svg_line(x1: float, y1: float, x2: float, y2: float, color: str = LINE, width: float = 1.5, dash: str = "") -> str:
    dash_attr = f' stroke-dasharray="{dash}"' if dash else ""
    return f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{color}" stroke-width="{width}"{dash_attr}/>'


def svg_path(d: str, color: str = ACCENT, width: float = 2.2, dash: str = "", marker: str = "arrow-accent") -> str:
    dash_attr = f' stroke-dasharray="{dash}"' if dash else ""
    marker_attr = f' marker-end="url(#{marker})"' if marker else ""
    return f'<path d="{d}" fill="none" stroke="{color}" stroke-width="{width}"{dash_attr}{marker_attr}/>'


def svg_node(x: float, y: float, w: float, h: float, title: str, sub: str = "", accent: bool = False) -> str:
    stroke = ACCENT if accent else INK
    fill = WHITE
    parts = [
        f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" rx="2" fill="{fill}" stroke="{stroke}" stroke-width="2"/>',
        svg_text(x + w / 2, y + h / 2 + 2, title, 21, INK, "middle", 700),
    ]
    if sub:
        parts.append(svg_text(x + w / 2, y + h / 2 + 24, sub, 11, MUTED, "middle", 600, FONT_MONO, 1.2))
    return "".join(parts)


def svg_pill(x: float, y: float, w: float, h: float, text: str, color: str = ACCENT) -> str:
    return (
        f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" rx="{h/2:.1f}" '
        f'fill="{PAPER}" stroke="{color}" stroke-width="1.6"/>'
        + svg_text(x + w / 2, y + h / 2 + 4, text, 11, color, "middle", 700, FONT_MONO, 1.0)
    )


def structures_svg() -> str:
    w, h = 1400, 420
    parts = [f'<svg viewBox="0 0 {w} {h}" role="img" aria-label="Prompt、Loop、Graph 三種結構圖">', svg_defs()]
    panels = [
        (10, "PROMPT", "一次，單一節點"),
        (480, "LOOP", "A ↺ 反覆修正"),
        (950, "GRAPH", "A → B → C + 退回邊"),
    ]
    for x, title, sub in panels:
        parts.append(svg_text(x + 210, 30, title, 13, ACCENT, "middle", 700, FONT_MONO, 2.2))
        parts.append(svg_text(x + 210, 56, sub, 16, MUTED, "middle", 500))
        parts.append(svg_line(x, 74, x + 420, 74, LINE, 1.2))

    # Prompt
    x = 10
    parts.append(svg_node(x + 70, 190, 130, 74, "A", "一次 Prompt"))
    parts.append(svg_path(f"M{x+200},227 L{x+300},227", INK, 2.2, marker="arrow-ink"))
    parts.append(svg_text(x + 340, 234, "END", 16, MUTED, "middle", 700, FONT_MONO, 1.6))

    # Loop
    x = 480
    parts.append(svg_node(x + 140, 190, 140, 74, "A", "觀察 → 行動 → 驗證", accent=True))
    parts.append(
        svg_path(
            f"M{x+150},190 C{x+100},110 {x+320},110 {x+270},190",
            ACCENT,
            2.4,
            marker="arrow-accent",
        )
    )
    parts.append(svg_text(x + 210, 118, "↺ 回到自己", 14, ACCENT, "middle", 700, FONT_MONO, 1.2))
    parts.append(svg_text(x + 210, 320, "目標 · 驗證 · 剎車", 14, MUTED, "middle", 600))

    # Graph
    x = 950
    parts.append(svg_node(x + 30, 195, 92, 64, "A", "N1"))
    parts.append(svg_node(x + 164, 195, 92, 64, "B", "N2"))
    parts.append(svg_node(x + 298, 195, 92, 64, "C", "N3"))
    parts.append(svg_path(f"M{x+122},227 L{x+164},227", INK, 2.2, marker="arrow-ink"))
    parts.append(svg_path(f"M{x+256},227 L{x+298},227", INK, 2.2, marker="arrow-ink"))
    parts.append(
        svg_path(
            f"M{x+344},259 C{x+344},330 {x+210},330 {x+210},259",
            ACCENT,
            2.2,
            dash="7 6",
            marker="arrow-accent",
        )
    )
    parts.append(svg_text(x + 278, 350, "退回邊", 13, ACCENT, "middle", 700, FONT_MONO, 1.2))

    parts.append("</svg>")
    return "".join(parts)


def loop_svg() -> str:
    w, h = 600, 600
    cx, cy, r = 300, 300, 190
    labels = [
        ("01", "目標"),
        ("02", "限制"),
        ("03", "驗證"),
        ("04", "剎車"),
        ("05", "觸發"),
    ]
    angles = [-90, -18, 54, 126, 198]
    parts = [f'<svg viewBox="0 0 {w} {h}" role="img" aria-label="Loop 五要素循環圖">', svg_defs()]
    parts.append(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="{LINE}" stroke-width="1.4" stroke-dasharray="4 8"/>')

    # clockwise arcs between nodes
    for i in range(5):
        a1 = math.radians(angles[i] + 22)
        a2 = math.radians(angles[(i + 1) % 5] - 22)
        x1, y1 = cx + r * math.cos(a1), cy + r * math.sin(a1)
        x2, y2 = cx + r * math.cos(a2), cy + r * math.sin(a2)
        large = 1 if (math.degrees(a2 - a1) % 360) > 180 else 0
        parts.append(
            svg_path(
                f"M{x1:.1f},{y1:.1f} A{r},{r} 0 {large} 1 {x2:.1f},{y2:.1f}",
                ACCENT,
                2.0,
                marker="arrow-accent",
            )
        )

    for (num, label), angle in zip(labels, angles):
        rad = math.radians(angle)
        x = cx + r * math.cos(rad)
        y = cy + r * math.sin(rad)
        parts.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="56" fill="{PAPER}" stroke="{INK}" stroke-width="2"/>')
        parts.append(svg_text(x, y - 8, num, 12, ACCENT, "middle", 700, FONT_MONO, 1.2))
        parts.append(svg_text(x, y + 18, label, 20, INK, "middle", 700))

    parts.append(svg_text(cx, cy - 4, "LOOP", 42, INK, "middle", 600, FONT_SERIF, -1))
    parts.append(svg_text(cx, cy + 30, "5 件事", 13, MUTED, "middle", 600, FONT_MONO, 1.6))
    parts.append(svg_text(cx, cy + 58, "少一個，就不算規格", 13, ACCENT, "middle", 600))
    parts.append("</svg>")
    return "".join(parts)


def pipeline_svg() -> str:
    w, h = 1400, 520
    parts = [f'<svg viewBox="0 0 {w} {h}" role="img" aria-label="從 Wiki 到簡報的 Graph 流程圖">', svg_defs()]
    nodes = [
        ("N1", "檢索", "sources.md"),
        ("N2", "證據卡", "cards/"),
        ("N3", "大綱", "outline.md"),
        ("N4", "逐頁稿", "drafts/"),
        ("N5", "渲染", "index.html"),
        ("N6", "審查", "review.md"),
        ("N7", "交件", "report.md"),
    ]
    xs = [30, 220, 410, 600, 790, 980, 1170]
    y = 210
    nw, nh = 150, 86
    for (num, title, sub), x in zip(nodes, xs):
        parts.append(svg_node(x, y, nw, nh, title, f"{num} · {sub}", accent=(num in {"N4", "N5"})))

    for i in range(len(xs) - 1):
        x1 = xs[i] + nw
        x2 = xs[i + 1]
        parts.append(svg_path(f"M{x1},253 L{x2},253", INK, 2.0, marker="arrow-ink"))

    gates = [
        (200, "G1", "覆蓋率"),
        (580, "G2", "人類"),
        (770, "G3", "忠實度"),
        (960, "G4", "版面"),
        (1150, "G5", "審查"),
    ]
    for gx, gnum, glabel in gates:
        parts.append(
            f'<path d="M{gx},132 L{gx+24},156 L{gx},180 L{gx-24},156 Z" fill="{PAPER}" stroke="{ACCENT}" stroke-width="1.8"/>'
        )
        parts.append(svg_text(gx, 161, gnum, 10, ACCENT, "middle", 700, FONT_MONO, 0.8))
        parts.append(svg_text(gx, 112, glabel, 12, MUTED, "middle", 600))

    # fallback edges
    parts.append(svg_path("M580,180 C580,196 485,196 485,210", ACCENT, 1.8, dash="6 5", marker="arrow-accent"))
    parts.append(svg_text(532, 198, "退回", 10, ACCENT, "middle", 700, FONT_MONO, 0.8))

    parts.append(svg_path("M770,180 L770,312 C770,336 730,336 730,296", ACCENT, 1.8, dash="6 5", marker="arrow-accent"))
    parts.append(svg_text(820, 330, "只改該頁", 10, ACCENT, "middle", 700, FONT_MONO, 0.8))

    parts.append(svg_path("M960,180 L960,320 C960,380 660,380 660,296", ACCENT, 1.8, dash="6 5", marker="arrow-accent"))
    parts.append(svg_text(810, 390, "刪字", 10, ACCENT, "middle", 700, FONT_MONO, 0.8))

    parts.append(
        svg_path(
            "M1150,180 L1150,320 C1150,450 295,450 295,296",
            ACCENT,
            1.8,
            dash="6 5",
            marker="arrow-accent",
        )
    )
    parts.append(svg_text(720, 462, "G5 失敗 → 退回 N2 補卡，再回 N4 補該頁", 11, ACCENT, "middle", 700, FONT_MONO, 0.6))

    # stop branch at G1
    parts.append(svg_path("M200,180 C200,196 200,196 200,196", ACCENT, 1.8, marker=""))
    parts.append(svg_pill(95, 350, 150, 30, "STOP < 3 頁", ACCENT))
    parts.append(svg_path("M200,180 C200,280 170,320 170,350", ACCENT, 1.8, dash="6 5", marker="arrow-accent"))

    # legend
    parts.append(svg_line(40, 486, 100, 486, INK, 2))
    parts.append(svg_text(110, 491, "前進", 11, MUTED, "start", 600, FONT_MONO, 0.8))
    parts.append(svg_line(180, 486, 240, 486, ACCENT, 2, "6 5"))
    parts.append(svg_text(250, 491, "退回", 11, MUTED, "start", 600, FONT_MONO, 0.8))
    parts.append("</svg>")
    return "".join(parts)


def cite_chips(slide: dict, sources: dict, wiki_titles: dict) -> str:
    chips = []
    for wid in slide.get("wiki", []):
        pid = wid.split("/")[-1]
        label = wiki_titles.get(pid, pid)
        chips.append(
            f'<a class="cite-chip wiki" href="wiki.html#{esc(pid)}" title="Wiki: {esc(wid)}">{esc(label)}</a>'
        )
    for sid in slide.get("sources", []):
        src = sources.get(sid)
        if not src:
            continue
        chips.append(
            f'<a class="cite-chip src" href="{esc(src["url"])}" target="_blank" rel="noopener" '
            f'title="{esc(src["label"])}">{esc(sid)} · {esc(src["label"])}</a>'
        )
    return "".join(chips)


def section_head(slide: dict) -> str:
    lead = f'<p class="lead">{inline(slide.get("lead", ""))}</p>' if slide.get("lead") else ""
    return f'<div class="section-head"><h2>{inline(slide["title"])}</h2>{lead}</div>'


def bottom_note(slide: dict) -> str:
    note = slide.get("note")
    return f'<p class="bottom-note">{inline(note)}</p>' if note else ""


def render_cover(slide: dict) -> str:
    meta = "".join(f"<span>{esc(item)}</span>" for item in slide.get("meta", []))
    link = slide.get("wiki_link")
    if link:
        meta += f'<a class="cover-wiki" href="{esc(link["href"])}">{esc(link["label"])}</a>'
    return f"""
      <div class="cover-grid">
        <div class="cover-main">
          <div class="cover-eyebrow">{esc(slide.get("eyebrow", slide.get("kicker", "")))}</div>
          <h1>{inline(slide["title"])}</h1>
          <p class="cover-sub">{inline(slide.get("subtitle", ""))}</p>
          <div class="cover-meta">{meta}</div>
        </div>
        <div class="cover-side">
          <div class="cover-mark">10</div>
          <div class="cover-lines"><span></span><span></span><span></span></div>
        </div>
      </div>
    """


def render_three_up(slide: dict) -> str:
    cards = []
    for card in slide.get("cards", []):
        cards.append(
            f"""
            <article class="card">
              <div class="card-num">{esc(card.get("num", ""))}</div>
              <h3>{inline(card.get("title", ""))}</h3>
              <p>{inline(card.get("body", ""))}</p>
              <span class="tag">{esc(card.get("tag", ""))}</span>
            </article>
            """
        )
    return section_head(slide) + f'<div class="cards three">{"".join(cards)}</div>' + bottom_note(slide)


def render_diagram(slide: dict) -> str:
    diagram = slide.get("diagram")
    svg = structures_svg() if diagram == "structures" else ""
    notes = []
    for note in slide.get("notes", []):
        notes.append(
            f'<div><strong>{esc(note.get("label", ""))}</strong><p>{inline(note.get("text", ""))}</p></div>'
        )
    return (
        section_head(slide)
        + f'<div class="diagram-wrap">{svg}</div>'
        + f'<div class="diagram-notes">{"".join(notes)}</div>'
        + bottom_note(slide)
    )


def render_loop(slide: dict) -> str:
    items = []
    for item in slide.get("items", []):
        items.append(
            f"""
            <div class="loop-item">
              <div class="num">{esc(item.get("num", ""))}</div>
              <div><h3>{inline(item.get("title", ""))}</h3><p>{inline(item.get("text", ""))}</p></div>
            </div>
            """
        )
    return (
        section_head(slide)
        + f'<div class="loop-layout"><div class="loop-visual">{loop_svg()}</div><div class="loop-list">{"".join(items)}</div></div>'
        + bottom_note(slide)
    )


def render_split(slide: dict) -> str:
    if slide.get("leftCode"):
        left_body = f'<pre class="code-block">{esc(slide["leftCode"])}</pre>'
    else:
        left_body = '<ul class="bullet-list">' + "".join(f"<li>{inline(item)}</li>" for item in slide.get("leftItems", [])) + "</ul>"
    right_body = '<ul class="bullet-list">' + "".join(f"<li>{inline(item)}</li>" for item in slide.get("rightItems", [])) + "</ul>"
    flow = ""
    if slide.get("flow"):
        parts = []
        for index, item in enumerate(slide["flow"]):
            if index:
                parts.append("<i>→</i>")
            parts.append(f"<span>{esc(item)}</span>")
        flow = f'<div class="flow-strip">{"".join(parts)}</div>'
    bars = ""
    if slide.get("bars"):
        max_value = max(int(item.get("value", 0)) for item in slide["bars"]) or 1
        rows = []
        for item in slide["bars"]:
            value = int(item.get("value", 0))
            width = value / max_value * 100
            rows.append(
                f'<div class="bar-row"><span class="bar-label">{esc(item.get("label", ""))}</span>'
                f'<div class="bar-track"><div class="bar-fill" style="width:{width:.1f}%"></div></div>'
                f'<span class="bar-value">{value}</span></div>'
            )
        bars = f'<div class="bar-chart">{"".join(rows)}</div>'
    callout = f'<p class="callout">{inline(slide["callout"])}</p>' if slide.get("callout") else ""
    return (
        section_head(slide)
        + f"""
        <div class="split">
          <div class="split-col"><h3>{esc(slide.get("leftTitle", ""))}</h3>{left_body}</div>
          <div class="split-col panel"><h3>{esc(slide.get("rightTitle", ""))}</h3>{right_body}</div>
        </div>
        """
        + flow
        + bars
        + callout
        + bottom_note(slide)
    )


def render_pipeline(slide: dict) -> str:
    return section_head(slide) + f'<div class="pipeline-wrap">{pipeline_svg()}</div>' + bottom_note(slide)


def render_table(slide: dict) -> str:
    columns = "".join(f"<th>{esc(col)}</th>" for col in slide.get("columns", []))
    rows = []
    for row in slide.get("rows", []):
        rows.append("<tr>" + "".join(f"<td>{inline(cell)}</td>" for cell in row) + "</tr>")
    callout = f'<p class="callout">{inline(slide["callout"])}</p>' if slide.get("callout") else ""
    warning = f'<p class="warning">{inline(slide["warning"])}</p>' if slide.get("warning") else ""
    return (
        section_head(slide)
        + f'<table class="deck-table"><thead><tr>{columns}</tr></thead><tbody>{"".join(rows)}</tbody></table>'
        + callout
        + warning
        + bottom_note(slide)
    )


def render_metrics(slide: dict) -> str:
    metrics = "".join(
        f'<div class="metric"><div class="value">{esc(item.get("value", ""))}</div><div class="label">{esc(item.get("label", ""))}</div></div>'
        for item in slide.get("metrics", [])
    )
    pipeline = '<div class="metric-pipeline"><span>檢索</span><i>→</i><span>證據卡</span><i>→</i><span>大綱</span><i>→</i><span>逐頁稿</span><i>→</i><span>渲染</span><i>→</i><span>檢查</span></div>'
    return section_head(slide) + f'<div class="metrics-row">{metrics}</div>' + pipeline + bottom_note(slide)


def render_checklist(slide: dict) -> str:
    items = "".join(
        f'<div class="check-item"><span class="box"></span><p>{inline(item)}</p></div>'
        for item in slide.get("items", [])
    )
    callout = f'<p class="callout">{inline(slide["callout"])}</p>' if slide.get("callout") else ""
    return section_head(slide) + f'<div class="checklist-grid">{items}</div>' + callout + bottom_note(slide)


def render_end(slide: dict) -> str:
    links = "".join(
        f'<a href="{esc(link.get("href", "#"))}">{esc(link.get("label", ""))}</a>'
        for link in slide.get("links", [])
    )
    return f"""
      <div class="end-layout">
        <div>
          <h1>{inline(slide["title"])}</h1>
          <p class="end-sub">{inline(slide.get("subtitle", ""))}</p>
          <blockquote>{inline(slide.get("quote", ""))}</blockquote>
        </div>
        <div class="end-links">{links}</div>
      </div>
    """


RENDERERS = {
    "cover": render_cover,
    "three-up": render_three_up,
    "diagram": render_diagram,
    "loop": render_loop,
    "split": render_split,
    "pipeline": render_pipeline,
    "table": render_table,
    "metrics": render_metrics,
    "checklist": render_checklist,
    "end": render_end,
}


def main() -> int:
    slides_data = json.loads((DECK / "slides.json").read_text(encoding="utf-8"))
    sources = json.loads((DECK / "sources.json").read_text(encoding="utf-8"))
    wiki_titles = load_wiki_titles()
    css = (ASSETS / "deck.css").read_text(encoding="utf-8")
    js = (ASSETS / "deck.js").read_text(encoding="utf-8")
    meta = slides_data["meta"]
    slides = slides_data["slides"]

    sections = []
    for index, slide in enumerate(slides, start=1):
        layout = slide.get("layout", "split")
        renderer = RENDERERS.get(layout)
        if renderer is None:
            raise SystemExit(f"Unknown layout: {layout} (slide {slide.get('id')})")
        body = renderer(slide)
        wiki_attr = ",".join(slide.get("wiki", []))
        source_attr = ",".join(slide.get("sources", []))
        sections.append(
            f"""
    <section class="slide layout-{esc(layout)}" id="slide-{index}" data-wiki="{esc(wiki_attr)}" data-sources="{esc(source_attr)}" aria-hidden="true">
      <div class="slide-top">
        <span class="kicker">{esc(slide.get("kicker", ""))}</span>
        <span class="top-rule"></span>
        <span class="top-index">{index:02d}</span>
      </div>
      <div class="slide-inner">{body}</div>
      <footer class="slide-footer">
        <div class="cite-chips">{cite_chips(slide, sources, wiki_titles)}</div>
        <span class="page-no">{index:02d} / {len(slides):02d}</span>
      </footer>
    </section>
            """
        )

    html_doc = f"""<!DOCTYPE html>
<html lang="{esc(meta.get("lang", "zh-Hant"))}">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="description" content="{esc(meta.get("subtitle", ""))}">
  <meta name="theme-color" content="#12110f">
  <title>{esc(meta.get("title", "教學簡報"))} · {esc(meta.get("subtitle", ""))}</title>
  <style>
{css}
  </style>
</head>
<body>
  <main class="deck" aria-label="教學簡報">
    <div class="stage">
{"".join(sections)}
    </div>
  </main>

  <div class="hud-trigger" aria-hidden="true"></div>
  <div class="hud" aria-label="簡報控制">
    <button type="button" data-action="prev" title="上一頁">←</button>
    <button type="button" data-action="next" title="下一頁">→</button>
    <button type="button" data-action="overview" title="總覽 (O)">O</button>
    <button type="button" data-action="help" title="說明 (?)">?</button>
    <button type="button" data-action="print" title="列印 (Shift+P)">P</button>
    <button type="button" data-action="fullscreen" title="全螢幕 (F)">F</button>
    <button type="button" id="hudCounter" title="頁碼">01 / {len(slides):02d}</button>
  </div>

  <div class="progress" aria-hidden="true"><div class="progress-bar" id="progressBar"></div></div>

  <div class="overview" id="overview" aria-hidden="true">
    <h2>簡報總覽</h2>
    <div class="overview-grid" id="overviewGrid"></div>
  </div>

  <div class="help" id="help" aria-hidden="true">
    <h2>操作說明</h2>
    <div class="help-body">
      <p><kbd>→</kbd> / <kbd>Space</kbd> 下一頁；<kbd>←</kbd> 上一頁；<kbd>Home</kbd> / <kbd>End</kbd> 跳到首尾。</p>
      <p><kbd>O</kbd> 開啟總覽；<kbd>?</kbd> 開啟本說明；<kbd>F</kbd> 全螢幕；<kbd>Shift</kbd> + <kbd>P</kbd> 列印。</p>
      <p>點擊畫面右側 70% 前進、左側 30% 後退。網址加上 <code>?slide=5</code> 可直接跳到第 5 頁。</p>
      <p>每一頁下方的 <strong>W</strong> 連結到 Wiki 頁面，<strong>S</strong> 連結到原始來源。</p>
    </div>
  </div>

  <script type="application/json" id="qa-report">{{}}</script>
  <script>
{js}
  </script>
</body>
</html>
"""
    (ROOT / "index.html").write_text(html_doc, encoding="utf-8")
    print(f"Rendered index.html with {len(slides)} slides")
    return 0


if __name__ == "__main__":
    sys.exit(main())
