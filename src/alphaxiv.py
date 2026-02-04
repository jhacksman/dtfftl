"""Stubbed AlphaXiv trending fetcher.

AlphaXiv is a discussion layer on top of arXiv. We'll use trending as pre-filter later.
"""

from __future__ import annotations

import datetime as dt

from .models import Story, SourceMeta


def fetch_trending(limit: int = 5, use_stub: bool = True) -> list[Story]:
    """Fetch trending AlphaXiv threads (stub)."""
    if not use_stub:
        raise NotImplementedError(
            "AlphaXiv integration not implemented yet. "
            "Run with use_stub=True or add API client."
        )

    now = dt.datetime.utcnow().strftime("%Y-%m-%d")
    stories: list[Story] = []
    for idx in range(limit):
        story_id = f"alphaxiv-{idx}"
        title = f"AlphaXiv trending paper {idx + 1}"
        summary = "Stub summary for AlphaXiv trending paper discussion."
        source_url = f"https://alphaxiv.org/abs/0000.{idx:05d}"
        meta = SourceMeta(
            source="alphaxiv",
            author="anon",
            score=50 - idx,
            comments=5 + idx,
            url=source_url,
            extra={"date": now, "arxiv_id": f"0000.{idx:05d}"},
        )
        stories.append(
            Story(
                id=story_id,
                title=title,
                summary=summary,
                source_url=source_url,
                source_meta=meta,
                raw_text=summary,
                tags=["stub", "alphaxiv"],
            )
        )

    return stories
