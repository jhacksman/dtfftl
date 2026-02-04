"""Shared dataclasses for DTF:FTL sources and pipeline."""

from dataclasses import dataclass, field
from typing import Optional


@dataclass
class SourceMeta:
    source: str
    subreddit: Optional[str] = None
    author: Optional[str] = None
    score: Optional[int] = None
    comments: Optional[int] = None
    url: Optional[str] = None
    extra: dict = field(default_factory=dict)


@dataclass
class Story:
    id: str
    title: str
    summary: str
    source_url: str
    source_meta: SourceMeta
    raw_text: str = ""
    tags: list[str] = field(default_factory=list)
