#!/usr/bin/env python3
"""Build the full STEPBACK STUDIO v4.1 GitHub Pages entry from archived source chunks.
This preserves the original application byte-for-byte (UTF-8 text), but removes the
fragile browser-side nine-file loading step.
"""
from pathlib import Path

ROOT = Path(__file__).resolve().parent
CHUNKS = ROOT / "assets" / "stepback-v4.1"
EXPECTED_CHARS = 5029685
pieces = []
for n in range(9):
    path = CHUNKS / f"chunk-{n:02d}.txt"
    chunk = path.read_text(encoding="utf-8")
    assert chunk, f"Missing or empty file: {path}"
    pieces.append(chunk)
html = "".join(pieces)
assert len(html) == EXPECTED_CHARS, f"HTML length mismatch: {len(html)}"
assert html.startswith("<!doctype html>") and html.endswith("</script></body></html>"), "Incomplete source HTML"
(ROOT / "index.html").write_text(html, encoding="utf-8")
print(f"Built index.html: {len(html):,} characters from {len(pieces)} verified source chunks")
