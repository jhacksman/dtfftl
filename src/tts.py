"""TTS client stubs for DTF:FTL."""

from __future__ import annotations

from pathlib import Path
from typing import Iterable


class TTSUnavailable(RuntimeError):
    pass


def text_to_speech(text: str, output_path: Path, voice: str = "forbin") -> Path:
    """Stub: write text to a .txt file next to the intended WAV output."""
    output_path.parent.mkdir(parents=True, exist_ok=True)
    txt_path = output_path.with_suffix(".txt")
    txt_path.write_text(f"VOICE={voice}\n{text}", encoding="utf-8")
    return txt_path


def text_to_speech_parallel(
    segments: Iterable[tuple[str, str]],
    output_dir: Path,
    voice: str = "forbin",
) -> list[Path]:
    """Stubbed parallel TTS: writes text files for each segment."""
    output_dir.mkdir(parents=True, exist_ok=True)
    outputs: list[Path] = []
    for name, text in segments:
        output_path = output_dir / f"{name}.wav"
        outputs.append(text_to_speech(text, output_path, voice=voice))
    return outputs
