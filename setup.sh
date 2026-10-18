#!/usr/bin/env bash
# ==============================================================================
# LinkedIn Propel Engine - Automated 1-Command Setup Script
# ==============================================================================
set -e

DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" >/dev/null 2>&1 && pwd)"
cd "$DIR"

echo "=========================================================="
echo "🚀 LinkedIn Propel Engine - Setting up environment..."
echo "=========================================================="

# Check for Python 3
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is required but not installed. Please install Python 3.9+."
    exit 1
fi

# 1. Create virtual environment
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment (.venv)..."
    python3 -m venv venv
else
    echo "📦 Virtual environment already exists."
fi

# Activate virtual environment
source venv/bin/activate

# 2. Upgrade pip and install dependencies
echo "📥 Installing dependencies from requirements.txt..."
pip install --quiet --upgrade pip
pip install --quiet -r requirements.txt

# 3. Install Playwright browser
echo "🌐 Installing Chromium browser for Playwright..."
playwright install chromium
playwright install-deps chromium 2>/dev/null || true

# 4. Check .env configuration
if [ ! -f ".env" ]; then
    echo "📄 Creating .env from .env.example..."
    cp .env.example .env
    echo ""
    echo "⚠️  ACTION REQUIRED:"
    echo "   Please edit '.env' with your LINKEDIN_LI_AT cookie and LLM_API_KEY."
    echo ""
fi

# 5. Check members.json
if [ ! -f "members.json" ]; then
    echo "👥 members.json missing, recreating default template..."
    cat <<EOF > members.json
[
  {
    "name": "Member 1",
    "profile_url": "https://www.linkedin.com/in/sample-member-1/"
  }
]
EOF
fi

chmod +x run.sh 2>/dev/null || true

echo "=========================================================="
echo "✅ Setup Completed Successfully!"
echo "   Next steps:"
echo "   1. Add your pod members to 'members.json'"
echo "   2. Paste your 'li_at' cookie and API key in '.env'"
echo "   3. Test connectivity: ./run.sh test"
echo "   4. Run a batch sweep: ./run.sh"
echo "=========================================================="
