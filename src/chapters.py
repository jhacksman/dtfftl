"""Chapters utilities (stub)."""

from __future__ import annotations

import json
from pathlib import Path


def generate_chapters_stub(output_path: Path, segments: list[str]) -> Path:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    payload = {"chapters": [{"title": name, "start": 0} for name in segments]}
    output_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    return output_path
