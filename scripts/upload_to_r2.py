"""Upload episode to Cloudflare R2 (stub)."""

from __future__ import annotations

import argparse
from pathlib import Path


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--episode-dir", required=True)
    args = parser.parse_args()

    episode_dir = Path(args.episode_dir)
    mp3_path = episode_dir / "episode.mp3"
    if not mp3_path.exists():
        raise SystemExit(f"Missing {mp3_path}")

    print(f"Stub upload complete for {mp3_path}")


if __name__ == "__main__":
    main()
