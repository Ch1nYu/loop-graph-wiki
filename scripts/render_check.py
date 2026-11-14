#!/usr/bin/env python3
"""Render index.html with Edge headless and verify the in-page QA report."""

from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
import sys
import tempfile
import time
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
QA = ROOT / "_private" / "qa"
SHOTS = QA / "screenshots"

EDGE_CANDIDATES = [
    Path(r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"),
    Path(r"C:\Program Files\Microsoft\Edge\Application\msedge.exe"),
    Path(r"C:\Program Files\Google\Chrome\Application\chrome.exe"),
    Path(r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"),
]


def find_browser() -> Path:
    for candidate in EDGE_CANDIDATES:
        if candidate.exists():
            return candidate
    raise SystemExit("Edge/Chrome not found")


def run_command(command: list[str], timeout: int = 60) -> subprocess.CompletedProcess:
    return subprocess.run(
        command,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        timeout=timeout,
    )


def dump_dom(browser: Path, url: str, profile: Path) -> str:
    command = [
        str(browser),
        "--headless=new",
        "--disable-gpu",
        "--no-first-run",
        f"--user-data-dir={profile}",
        "--virtual-time-budget=7000",
        "--dump-dom",
        url,
    ]
    result = run_command(command)
    if result.returncode != 0 and not result.stdout:
        raise SystemExit(f"headless dump failed: {result.stderr[-800:]}")
    return result.stdout


def take_screenshot(browser: Path, url: str, output: Path, profile: Path) -> bool:
    SHOTS.mkdir(parents=True, exist_ok=True)
    tmp = Path(tempfile.gettempdir()) / f"deck-shot-{int(time.time() * 1000)}.png"
    command = [
        str(browser),
        "--headless",
        "--disable-gpu",
        "--hide-scrollbars",
        "--no-first-run",
        f"--user-data-dir={profile}",
        "--window-size=1600,900",
        "--virtual-time-budget=3000",
        f"--screenshot={tmp}",
        url,
    ]
    run_command(command)
    for _ in range(24):
        if tmp.exists() and tmp.stat().st_size > 0:
            shutil.copyfile(tmp, output)
            try:
                tmp.unlink()
            except OSError:
                pass
            return True
        time.sleep(0.25)
    return False


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--shots", action="store_true", help="also capture one screenshot per slide")
    args = parser.parse_args()

    QA.mkdir(parents=True, exist_ok=True)
    browser = find_browser()
    index = ROOT / "index.html"
    if not index.exists():
        raise SystemExit("index.html not found; run scripts/render_deck.py first")

    slides_data = json.loads((ROOT / "deck" / "slides.json").read_text(encoding="utf-8"))
    expected = len(slides_data["slides"])
    profile = Path(tempfile.mkdtemp(prefix="deck-profile-"))
    url = index.as_uri() + "?qa=1&slide=1"
    dom = dump_dom(browser, url, profile)

    match = re.search(r'<script type="application/json" id="qa-report">(.*?)</script>', dom, re.S)
    if not match:
        print("RESULT: FAIL — #qa-report not found in rendered DOM")
        return 1
    try:
        qa = json.loads(match.group(1))
    except json.JSONDecodeError as exc:
        print(f"RESULT: FAIL — invalid QA JSON: {exc}")
        return 1

    errors: list[str] = []
    if qa.get("slideCount") != expected:
        errors.append(f"slideCount {qa.get('slideCount')} != {expected}")
    if qa.get("overflow"):
        errors.append(f"overflow on {len(qa['overflow'])} slide(s): {qa['overflow']}")
    if qa.get("missingCitations"):
        errors.append(f"missing citations on slides: {qa['missingCitations']}")
    if not qa.get("pass"):
        errors.append("in-page QA did not pass")

    screenshots: list[str] = []
    if args.shots:
        for number in range(1, expected + 1):
            output = SHOTS / f"slide-{number:02d}.png"
            shot_url = index.as_uri() + f"?qa=1&slide={number}"
            if take_screenshot(browser, shot_url, output, profile):
                screenshots.append(output.relative_to(ROOT).as_posix())
            else:
                errors.append(f"screenshot failed for slide {number}")

    report = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "browser": str(browser),
        "slides": expected,
        "qa": qa,
        "screenshots": screenshots,
        "errors": errors,
        "pass": not errors,
    }
    (QA / "render-report.json").write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")

    print(f"Browser: {browser}")
    print(f"Slides: {qa.get('slideCount')} (expected {expected})")
    print(f"Overflow: {len(qa.get('overflow', []))}")
    print(f"Missing citations: {len(qa.get('missingCitations', []))}")
    if screenshots:
        print(f"Screenshots: {len(screenshots)}")
    for error in errors:
        print(f"  ERROR {error}")
    if errors:
        print("RESULT: FAIL")
        return 1
    print("RESULT: PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
