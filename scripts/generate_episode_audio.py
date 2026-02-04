"""Generate episode audio (stub)."""

from __future__ import annotations

import argparse
from pathlib import Path

from src.audio import stitch_wavs, transcode_to_mp3
from src.tts import text_to_speech_parallel


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--episode-dir", required=True)
    args = parser.parse_args()

    episode_dir = Path(args.episode_dir)
    segments = []
    for segment_path in sorted(episode_dir.glob("*.txt")):
        if segment_path.name in {"episode.txt", "manifest.json"}:
            continue
        name = segment_path.stem
        text = segment_path.read_text(encoding="utf-8")
        segments.append((name, text))

    wav_outputs, failures = text_to_speech_parallel(segments, episode_dir / "audio")
    if failures:
        raise SystemExit(f"TTS failed for segments: {list(failures.keys())}")
    stitched = stitch_wavs(wav_outputs, episode_dir / "episode.wav")
    transcode_to_mp3(stitched, episode_dir / "episode.mp3")


if __name__ == "__main__":
    main()
