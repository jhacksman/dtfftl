"""Audio utilities (stubbed) for DTF:FTL."""

from __future__ import annotations

from pathlib import Path
from typing import Iterable


DEFAULT_SILENCE_DURATION = 1.0


def stitch_wavs(wav_files: Iterable[Path], output_path: Path, silence_duration: float | None = DEFAULT_SILENCE_DURATION) -> Path:
    """Stub: write a manifest file listing WAV inputs."""
    output_path.parent.mkdir(parents=True, exist_ok=True)
    manifest_path = output_path.with_suffix(".manifest.txt")
    lines = [str(p) for p in wav_files]
    if silence_duration is not None:
        lines.append(f"silence_duration={silence_duration}")
    manifest_path.write_text("\n".join(lines), encoding="utf-8")
    return output_path


def transcode_to_mp3(wav_path: Path, mp3_path: Path, bitrate: str = "128k") -> Path:
    """Stub: write a marker file for MP3 output."""
    mp3_path.parent.mkdir(parents=True, exist_ok=True)
    mp3_path.write_text(f"stub mp3 from {wav_path} at {bitrate}", encoding="utf-8")
    return mp3_path
