"""Reddit fetcher for DTF:FTL."""

from __future__ import annotations

import datetime as dt
import os
import time
from typing import Iterable

from .models import Story, SourceMeta

DEFAULT_SUBREDDITS = ["singularity", "LocalLLaMA", "Accelerate"]
USER_AGENT_DEFAULT = "dtfftl/0.1 (by u/unknown)"


class RedditUnavailable(RuntimeError):
    pass


def _get_reddit_client():
    try:
        import praw  # type: ignore
    except Exception as exc:
        raise RedditUnavailable("praw is not installed. Add it to requirements.txt.") from exc

    client_id = os.environ.get("REDDIT_CLIENT_ID")
    client_secret = os.environ.get("REDDIT_CLIENT_SECRET")
    user_agent = os.environ.get("REDDIT_USER_AGENT", USER_AGENT_DEFAULT)

    if not client_id or not client_secret:
        raise RedditUnavailable("Missing REDDIT_CLIENT_ID/REDDIT_CLIENT_SECRET in environment.")

    return praw.Reddit(
        client_id=client_id,
        client_secret=client_secret,
        user_agent=user_agent,
    )


def _summarize_comments(submission, max_comments: int = 3, max_chars: int = 500) -> str:
    try:
        submission.comments.replace_more(limit=0)
        comments = list(submission.comments)
    except Exception:
        return ""

    top = sorted(comments, key=lambda c: getattr(c, "score", 0), reverse=True)[:max_comments]
    parts = []
    for idx, comment in enumerate(top, start=1):
        body = getattr(comment, "body", "")
        score = getattr(comment, "score", 0)
        if not body:
            continue
        body = " ".join(body.split())
        if len(body) > 220:
            body = body[:217].rstrip() + "..."
        parts.append(f"{idx}) {body} (score {score})")

    summary = "Top comments: " + " ".join(parts) if parts else ""
    return summary[:max_chars]


def fetch_reddit_stories(
    subreddits: Iterable[str] | None = None,
    limit_per_subreddit: int = 5,
    use_stub: bool = True,
    max_comment_summaries: int = 3,
) -> list[Story]:
    """Fetch top Reddit posts.

    This is stubbed for now. When `use_stub=False`, raise a clear error.
    """
    subreddits = list(subreddits or DEFAULT_SUBREDDITS)

    if not use_stub:
        reddit = _get_reddit_client()
        now = dt.datetime.utcnow()
        cutoff = now - dt.timedelta(hours=24)
        stories: list[Story] = []
        seen_ids: set[str] = set()

        try:
            from prawcore.exceptions import RateLimitExceeded
        except Exception:
            RateLimitExceeded = Exception

        count_by_subreddit: dict[str, int] = {name: 0 for name in subreddits}

        for subreddit in subreddits:
            listing = reddit.subreddit(subreddit)
            for feed_name, feed in (
                ("top", listing.top(time_filter="day", limit=limit_per_subreddit * 2)),
                ("hot", listing.hot(limit=limit_per_subreddit * 2)),
            ):
                for submission in feed:
                    try:
                        created = dt.datetime.utcfromtimestamp(submission.created_utc)
                        if created < cutoff:
                            continue
                        if submission.id in seen_ids:
                            continue
                        seen_ids.add(submission.id)

                        selftext = submission.selftext or ""
                        summary = selftext.strip()[:400] if selftext else ""
                        comments_summary = _summarize_comments(
                            submission, max_comments=max_comment_summaries
                        )
                        if not summary:
                            summary = comments_summary or submission.title

                        raw_text_parts = [text for text in (selftext, comments_summary) if text]
                        raw_text = "\n\n".join(raw_text_parts).strip()

                        meta = SourceMeta(
                            source="reddit",
                            subreddit=subreddit,
                            author=getattr(submission, "author", None).name if submission.author else None,
                            score=getattr(submission, "score", 0),
                            comments=getattr(submission, "num_comments", 0),
                            url=submission.url,
                            extra={
                                "created_utc": created.isoformat(),
                                "selftext": selftext,
                                "comments_summary": comments_summary,
                                "feed": feed_name,
                            },
                        )
                        stories.append(
                            Story(
                                id=f"reddit-{submission.id}",
                                title=submission.title,
                                summary=summary,
                                source_url=submission.url,
                                source_meta=meta,
                                raw_text=raw_text,
                                tags=["reddit", subreddit],
                            )
                        )
                        count_by_subreddit[subreddit] += 1
                        if count_by_subreddit[subreddit] >= limit_per_subreddit:
                            break
                    except RateLimitExceeded as exc:
                        sleep_for = getattr(exc, "sleep_time", 5) + 1
                        time.sleep(sleep_for)
                        continue
                    except Exception:
                        continue
                if count_by_subreddit[subreddit] >= limit_per_subreddit:
                    break
        return stories

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
