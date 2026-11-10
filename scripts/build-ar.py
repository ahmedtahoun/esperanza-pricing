#!/usr/bin/env python3
"""Make the Arabic copy (tour-costing-ar.html) from the English file.

Edit only tour-costing.html, then run:  python3 scripts/build-ar.py
"""
from pathlib import Path

root = Path(__file__).resolve().parent.parent
src = (root / "tour-costing.html").read_text(encoding="utf-8")
swaps = [
    ("const LANG_DEFAULT='en';", "const LANG_DEFAULT='ar';"),
    ("<title>Esperanza Program Pricing</title>", "<title>تسعير برامج إسبيرانزا</title>"),
]
for old, new in swaps:
    if old not in src:
        raise SystemExit(f"Not found in tour-costing.html: {old}")
    src = src.replace(old, new, 1)
(root / "tour-costing-ar.html").write_text(src, encoding="utf-8")
print("Wrote tour-costing-ar.html")
