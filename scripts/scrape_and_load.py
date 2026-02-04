"""Fetch stories and store them in LanceDB (stub friendly)."""

from __future__ import annotations

import datetime as dt

from src.pipeline import collect_stories
from src.storage import store_stories_batch, StorageUnavailable


def main() -> None:
    episode_date = dt.date.today().isoformat()
    stories = collect_stories(reddit_limit=2, alphaxiv_limit=2, luminary_limit=1, use_stub=True)
    try:
        store_stories_batch(stories, episode_date, use_lancedb=True)
    except StorageUnavailable:
        store_stories_batch(stories, episode_date, use_lancedb=False)
    print(f"Stored {len(stories)} stories for {episode_date}")


if __name__ == "__main__":
    main()
