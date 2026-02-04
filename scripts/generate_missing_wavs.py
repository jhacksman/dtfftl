"""Generate missing WAVs (stub)."""

from __future__ import annotations

from pathlib import Path

from src.tts import text_to_speech


def main() -> None:
    episode_dir = Path("data/episodes")
    for episode in episode_dir.glob("*/"):
        for segment in episode.glob("*.txt"):
            if segment.name in {"episode.txt", "manifest.json"}:
                continue
            wav_path = segment.with_suffix(".wav")
            if not wav_path.exists():
                text = segment.read_text(encoding="utf-8")
                text_to_speech(text, wav_path)


if __name__ == "__main__":
    main()
