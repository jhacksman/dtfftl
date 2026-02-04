"""Stubbed Reddit fetcher for DTF:FTL.

Future: implement with PRAW or Reddit API.
"""

from __future__ import annotations

import datetime as dt
from typing import Iterable

from .models import Story, SourceMeta

DEFAULT_SUBREDDITS = ["singularity", "LocalLLaMA", "Accelerate"]


def fetch_reddit_stories(
    subreddits: Iterable[str] | None = None,
    limit_per_subreddit: int = 5,
    use_stub: bool = True,
) -> list[Story]:
    """Fetch top Reddit posts.

    This is stubbed for now. When `use_stub=False`, raise a clear error.
    """
    subreddits = list(subreddits or DEFAULT_SUBREDDITS)

    if not use_stub:
        raise NotImplementedError(
            "Reddit API integration not implemented yet. "
            "Run with use_stub=True or add PRAW support."
        )

    now = dt.datetime.utcnow().strftime("%Y-%m-%d")
    stories: list[Story] = []
    for subreddit in subreddits:
        for idx in range(limit_per_subreddit):
            story_id = f"reddit-{subreddit}-{idx}"
            title = f"[{subreddit}] Placeholder post {idx + 1}"
            summary = (
                f"Stub summary for {subreddit} post {idx + 1}. "
                "Replace with Reddit API content."
            )
            source_url = f"https://reddit.com/r/{subreddit}/comments/{story_id}"
            meta = SourceMeta(
                source="reddit",
                subreddit=subreddit,
                author="stub_user",
                score=100 - idx,
                comments=10 + idx,
                url=source_url,
                extra={"date": now},
            )
            stories.append(
                Story(
                    id=story_id,
                    title=title,
                    summary=summary,
                    source_url=source_url,
                    source_meta=meta,
                    raw_text=summary,
                    tags=["stub", "reddit"],
                )
            )

    return stories
