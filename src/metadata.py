"""Metadata helpers for DTF:FTL (stub)."""

from __future__ import annotations

from pathlib import Path


def write_metadata_stub(output_dir: Path, episode_date: str) -> Path:
    output_dir.mkdir(parents=True, exist_ok=True)
    meta_path = output_dir / "metadata.txt"
    meta_path.write_text(f"DTF:FTL metadata for {episode_date}\n", encoding="utf-8")
    return meta_path
