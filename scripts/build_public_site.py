#!/usr/bin/env python3
"""Assemble the minimal public GitHub Pages artifact."""

from __future__ import annotations

import shutil
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def build(output: Path) -> int:
    if output.exists():
        shutil.rmtree(output)
    output.mkdir(parents=True)

    for name in ("index.html", "wiki.html"):
        shutil.copy2(ROOT / name, output / name)
    shutil.copytree(ROOT / "assets", output / "assets")
    (output / ".nojekyll").write_text("", encoding="utf-8")
    print(f"Built public site in {output}")
    return 0


if __name__ == "__main__":
    target = Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT / "_site"
    sys.exit(build(target))
