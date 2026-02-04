"""Episode pipeline orchestrator for DTF:FTL."""

from __future__ import annotations

import argparse
import datetime as dt
import json
from pathlib import Path
from typing import Iterable

from .alphaxiv import fetch_trending
from .generator import generate_episode_scripts, generate_interstitial, generate_intro, generate_outro
from .luminaries import fetch_luminary_posts
from .models import Story
from .reddit import fetch_reddit_stories
from .storage import store_episode, store_stories_batch, StorageUnavailable

PROJECT_ROOT = Path(__file__).parent.parent
EPISODES_DIR = PROJECT_ROOT / "data" / "episodes"


def segment_name(kind: str, script_num: int = 0, next_num: int = 0) -> str:
    if kind == "intro":
        return "00_-_intro"
    if kind == "outro":
        return "20_-_outro"
    if kind == "script":
        seq = 2 * script_num - 1
        return f"{seq:02d}_-_script_{script_num:02d}"
    if kind == "interstitial":
        seq = 2 * script_num
        return f"{seq:02d}_-_interstitial_{script_num:02d}_{next_num:02d}"
    raise ValueError(f"Unknown segment kind: {kind}")


def collect_stories(
    reddit_limit: int,
    alphaxiv_limit: int,
    luminary_limit: int,
    use_stub: bool = True,
) -> list[Story]:
    stories: list[Story] = []
    stories.extend(fetch_reddit_stories(limit_per_subreddit=reddit_limit, use_stub=use_stub))
    stories.extend(fetch_trending(limit=alphaxiv_limit, use_stub=use_stub))
    try:
        stories.extend(fetch_luminary_posts(limit=luminary_limit, use_stub=use_stub))
    except NotImplementedError:
        pass
    return stories


def write_episode_outputs(episode_dir: Path, segments: Iterable[tuple[str, str]]) -> str:
    episode_dir.mkdir(parents=True, exist_ok=True)
    episode_path = episode_dir / "episode.txt"

    parts = []
    for name, text in segments:
        segment_path = episode_dir / f"{name}.txt"
        segment_path.write_text(text, encoding="utf-8")
        parts.append(text)

    episode_text = "\n\n".join(parts)
    episode_path.write_text(episode_text, encoding="utf-8")
    return episode_text


def run_pipeline(
    episode_date: dt.date | None = None,
    use_stub: bool = True,
    store: bool = True,
) -> Path:
    episode_date = episode_date or dt.date.today()
    episode_dir = EPISODES_DIR / episode_date.isoformat()

    stories = collect_stories(reddit_limit=2, alphaxiv_limit=2, luminary_limit=1, use_stub=use_stub)
    scripts = generate_episode_scripts(stories)

    intro = generate_intro(episode_date)
    outro = generate_outro()

    segments: list[tuple[str, str]] = [(segment_name("intro"), intro)]
    for idx, script in enumerate(scripts, start=1):
        segments.append((segment_name("script", script_num=idx), script))
        if idx < len(scripts):
            segments.append((segment_name("interstitial", script_num=idx, next_num=idx + 1), generate_interstitial(script, scripts[idx])))
    segments.append((segment_name("outro"), outro))

    episode_text = write_episode_outputs(episode_dir, segments)

    manifest = {
        "episode_date": episode_date.isoformat(),
        "story_count": len(stories),
        "segments": [name for name, _ in segments],
    }
    (episode_dir / "manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")

    if store:
        try:
            store_stories_batch(stories, episode_date.isoformat(), use_lancedb=True)
            store_episode(episode_date.isoformat(), episode_text, manifest, use_lancedb=True)
        except StorageUnavailable:
            store_stories_batch(stories, episode_date.isoformat(), use_lancedb=False)
            store_episode(episode_date.isoformat(), episode_text, manifest, use_lancedb=False)

    return episode_dir


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run DTF:FTL pipeline")
    parser.add_argument("--date", help="Episode date (YYYY-MM-DD)")
    parser.add_argument("--test", action="store_true", help="Run in stubbed test mode")
    parser.add_argument("--live", action="store_true", help="Use live source integrations (not stubbed)")
    parser.add_argument("--no-store", action="store_true", help="Skip storage")
    return parser.parse_args()


def main() -> None:
    args = _parse_args()
    episode_date = dt.date.fromisoformat(args.date) if args.date else None
    use_stub = not args.live
    run_pipeline(episode_date=episode_date, use_stub=use_stub, store=not args.no_store)


if __name__ == "__main__":
    main()
