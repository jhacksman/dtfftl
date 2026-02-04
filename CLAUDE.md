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
- Source fetchers are stubbed until real integrations are added.
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

## Lessons Learned
- Keep pipeline runnable in stub mode so the skeleton can be validated without external services.
- Add real API integrations behind a `--live` flag to preserve deterministic tests.
