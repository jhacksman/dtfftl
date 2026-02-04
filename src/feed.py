"""RSS feed generation (stub)."""

from __future__ import annotations

from pathlib import Path


def write_feed_stub(output_path: Path) -> Path:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text("<!-- DTF:FTL feed stub -->\n", encoding="utf-8")
    return output_path
