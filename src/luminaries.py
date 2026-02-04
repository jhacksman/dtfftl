"""Stubbed luminaries (Twitter/blogs) fetcher."""

from __future__ import annotations

import datetime as dt

from .models import Story, SourceMeta


def fetch_luminary_posts(limit: int = 5, use_stub: bool = True) -> list[Story]:
    if not use_stub:
        raise NotImplementedError(
            "Luminary feeds not implemented yet. "
            "Run with use_stub=True or add integrations."
        )

    now = dt.datetime.utcnow().strftime("%Y-%m-%d")
    stories: list[Story] = []
    for idx in range(limit):
        story_id = f"luminary-{idx}"
        title = f"Luminary update {idx + 1}"
        summary = "Stub summary from an AI luminary blog or Twitter thread."
        source_url = f"https://example.com/luminary/{idx}"
        meta = SourceMeta(
            source="luminary",
            author=f"luminary_{idx}",
            score=20 - idx,
            comments=0,
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
                tags=["stub", "luminary"],
            )
        )

    return stories
