"""Transcript helpers (stub)."""

from __future__ import annotations

from pathlib import Path


def generate_plain_transcript(text: str, output_path: Path) -> Path:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(text, encoding="utf-8")
    return output_path
