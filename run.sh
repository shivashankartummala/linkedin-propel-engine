#!/usr/bin/env bash
# ==============================================================================
# LinkedIn Propel Engine - Run Wrapper
# Usage:
#   ./run.sh                  -> Runs standard batch sweep
#   ./run.sh dry-run          -> Simulates sweep without submitting comments
#   ./run.sh pending          -> Finds fresh posts & replies (Metamuse Agent-Native)
#   ./run.sh post-comment ... -> Submits a comment directly from Cloud Agent
#   ./run.sh post-reply ...   -> Submits a thread reply directly from Cloud Agent
#   ./run.sh test             -> Runs diagnostics on LinkedIn session
#   ./run.sh status           -> Shows today's metrics and processed posts
#   ./run.sh daemon           -> Runs 4x daily scheduled background loop
# ==============================================================================

DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" >/dev/null 2>&1 && pwd)"
cd "$DIR"

if [ ! -d "venv" ]; then
    echo "❌ Virtual environment not found. Please run './setup.sh' first."
    exit 1
fi

source venv/bin/activate
python3 engine.py "$@"
