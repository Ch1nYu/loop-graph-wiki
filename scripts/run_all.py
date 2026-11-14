#!/usr/bin/env python3
"""Run all checks and write qa/summary.json."""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
QA = ROOT / "_private" / "qa"


def run(script: str, extra: list[str] | None = None) -> dict[str, object]:
    command = [sys.executable, str(ROOT / "scripts" / script)] + (extra or [])
    result = subprocess.run(command, capture_output=True, text=True, encoding="utf-8", errors="replace")
    print(f"\n=== {script} ===")
    print(result.stdout.strip())
    if result.stderr.strip():
        print(result.stderr.strip())
    return {
        "script": script,
        "returncode": result.returncode,
        "pass": result.returncode == 0,
        "stdout": result.stdout.strip(),
        "stderr": result.stderr.strip(),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--shots", action="store_true", help="capture screenshots in render_check.py")
    args = parser.parse_args()

    QA.mkdir(parents=True, exist_ok=True)
    results = [
        run("check_wiki.py"),
        run("check_deck.py"),
        run("render_check.py", ["--shots"] if args.shots else []),
    ]
    summary = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "results": results,
        "pass": all(item["pass"] for item in results),
    }
    (QA / "summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
    print("\n=== SUMMARY ===")
    for item in results:
        print(f"{item['script']}: {'PASS' if item['pass'] else 'FAIL'}")
    print("RESULT:", "PASS" if summary["pass"] else "FAIL")
    return 0 if summary["pass"] else 1


if __name__ == "__main__":
    sys.exit(main())
