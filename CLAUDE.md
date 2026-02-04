# CLAUDE.md — DTF:FTL (Daily Tech Feed: From The Labs)

## Project Overview
DTF:FTL is a daily AI/singularity podcast pipeline. Tagline: "Dispatches from the edge". It mirrors dtfhn but swaps Hacker News for Reddit, AlphaXiv trending, and AI luminary feeds.

Default voice: `forbin` (same as dtfhn).

## Boris Cherny Method (MANDATORY)
1. PLAN — Write `PLAN.md` before coding
2. EXECUTE — Implement the plan
3. VERIFY — Test that it works
4. DOCUMENT — Update `CLAUDE.md` + `README.md` with conventions/lessons

## Key Conventions
- Pipeline pattern is fixed: fetch → LanceDB → script generation → TTS → stitch → R2 upload.
- Use `python3` for CLI execution on macOS.
- Avoid committing generated episode outputs; they live under `data/`.

## Structure
```
DTF:FTL/
├── PLAN.md
├── README.md
├── CLAUDE.md
├── src/
├── scripts/
├── templates/
├── data/
├── episodes/
└── tests/
```

## Running (Stub)
```bash
python3 -m src.pipeline --test --no-store
```

## Running (Live)
```bash
export REDDIT_CLIENT_ID=...
export REDDIT_CLIENT_SECRET=...
export REDDIT_USER_AGENT="dtfftl/0.1 by your_username"

python3 -m src.pipeline --live
```

## Lessons Learned
- AlphaXiv has no stable public API; scrape `https://www.alphaxiv.org/explore` and enrich with arXiv abstracts.
- Reddit read-only access via PRAW requires `REDDIT_CLIENT_ID` and `REDDIT_CLIENT_SECRET`.
- TTS uses quato `/speak` with voice `forbin` and expects a WAV (`RIFF`) payload.
- LanceDB embeddings are generated via sentence-transformers; set `DTFFTL_EMBEDDINGS=openai` to use OpenAI.
