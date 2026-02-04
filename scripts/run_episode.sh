#!/usr/bin/env bash
set -euo pipefail

EPISODE_DATE=${1:-$(date +%F)}

python -m src.pipeline --date "$EPISODE_DATE" --test
python /Users/jackhacksman/clawd/dtfftl/scripts/generate_episode_audio.py --episode-dir "/Users/jackhacksman/clawd/dtfftl/data/episodes/$EPISODE_DATE"
