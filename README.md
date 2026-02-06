# DTF:FTL — Daily Tech Feed: From The Labs

Tagline: "Dispatches from the edge"

DTF:FTL is a daily AI/singularity podcast with **two hosts**:
- **Stephen** (stephen_fry voice) — The mentor. Knowledgeable, warm, explains the technical depth.
- **Philip** (philip_fry voice) — The mentee. Enthusiastic learner, asks clarifying questions, makes relatable analogies.

The mentor/mentee dynamic makes cutting-edge AI research accessible. Stephen provides the expertise; Philip voices the audience's questions.

## Sources
- Reddit (r/singularity, r/LocalLLaMA, r/Accelerate)
- AlphaXiv trending (discussion layer on arXiv)
- AI luminaries (Twitter/blogs) — stubbed

## Pipeline
fetch → LanceDB → dialogue script generation → TTS (per speaker) → stitch → R2 upload

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

TTS uses the quato server at `http://192.168.0.134:7849`:
- Stephen lines → voice `stephen_fry`
- Philip lines → voice `philip_fry`

Scripts are parsed line-by-line (STEPHEN: / PHILIP: prefixes) and rendered with appropriate voices.

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
- Two-host format: Stephen (mentor) + Philip (mentee)
- Character files in `characters/stephen.md` and `characters/philip.md`
- LanceDB is optional; JSON fallback is used when unavailable.
- Reddit requires API credentials.
