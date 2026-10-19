#!/usr/bin/env bash
# ==============================================================================
# LinkedIn Propel Engine (Copilot Edition) - Run Wrapper
# Usage:
#   ./run.sh                  -> Polls pod members and outputs 1-Click Action Cards
#   ./run.sh poll             -> Polls pod members and outputs 1-Click Action Cards
#   ./run.sh draft --url <url> -> Drafts 3 comment options for any post on demand
#   ./run.sh status           -> Displays today's digest statistics
# ==============================================================================

DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" >/dev/null 2>&1 && pwd)"
cd "$DIR"

if [ ! -d "venv" ]; then
    echo "❌ Virtual environment not found. Please run './setup.sh' first."
    exit 1
fi

source venv/bin/activate
python3 engine.py "$@"
