# DTF:FTL — Daily Tech Feed: From The Labs

Tagline: "Dispatches from the edge"

DTF:FTL is a daily AI/singularity podcast pipeline focused on AI/ML breakthroughs, singularity news, and open-source model progress. It mirrors the dtfhn pipeline but swaps Hacker News for:
- Reddit (r/singularity, r/LocalLLaMA, r/Accelerate)
- AlphaXiv trending (discussion layer on arXiv)
- AI luminaries (Twitter/blogs) — stubbed

## Pipeline
fetch → LanceDB → script generation → TTS → stitch → R2 upload

## Quickstart (Stub Mode)
```bash
python3 -m src.pipeline --test --no-store
```

This writes an episode to `data/episodes/YYYY-MM-DD/` with placeholder scripts.

## Live Mode
Set credentials in environment or `config/.env.example`, then run:
```bash
export REDDIT_CLIENT_ID=...
export REDDIT_CLIENT_SECRET=...
export REDDIT_USER_AGENT="dtfftl/0.1 by your_username"

python3 -m src.pipeline --live
```

AlphaXiv trending is scraped from the public explore page and enriched with arXiv abstracts.
TTS uses the quato server at `http://192.168.0.134:7849` with voice `forbin`.

## Scripts
- `scripts/run_episode.sh` — end-to-end stub run (pipeline + audio)
- `scripts/scrape_and_load.py` — fetch + store stories
- `scripts/generate_episode_audio.py` — TTS + stitch
- `scripts/upload_to_r2.py` — stub upload

## Structure
```
.
├── src/              # Pipeline modules
├── scripts/          # Entry points
├── templates/        # Intro/outro text
├── data/             # Vector DB + outputs (ignored)
├── episodes/         # Episode assets (ignored)
├── tests/            # Basic tests
├── docs/             # Design notes
└── PLAN.md           # Boris method plan
```

## Notes
- Voice defaults to `forbin`, matching dtfhn.
- LanceDB is optional; JSON fallback is used when unavailable.
- Reddit requires API credentials.
