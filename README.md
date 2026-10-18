# 🚀 LinkedIn Propel Engine

> **Autonomous Mutual Growth Engine for Creators, Engineers, and Leaders**

LinkedIn Propel Engine is an automated mutual engagement skill designed for a private circle of 15–20 creators. It automatically discovers new posts from group members, writes high-value, authentic 1–2 line comments, monitors author replies, and responds back to keep conversation threads alive.

By distributing thoughtful, conversational comments across your group within the **Golden 60–90 Minute Window**, it signals high dwell time to the LinkedIn algorithm, propelling your posts into 2nd and 3rd degree feeds.

---

## 🌟 How the Daily Cycle Works

The engine executes in **4 distinct phases** throughout the day:

```
[08:15 AM] Run 1: Morning Sweep  ──> Finds fresh posts (<24h) from pod & leaves thoughtful comments
[12:30 PM] Run 2: Noon Sweep     ──> Checks if authors replied to our comments & posts follow-up responses
[04:45 PM] Run 3: Afternoon Pass ──> Catches late replies & afternoon posts
[08:15 PM] Run 4: Evening Wrap   ──> Final conversation sweep & archives daily state
```

---

## ⚡ 1-Minute Quick Start

### 1. Clone & Run Setup
```bash
git clone <your-repo-url> linkedin-propel-engine
cd linkedin-propel-engine
./setup.sh
```
`setup.sh` automatically creates a virtual environment, installs dependencies, downloads headless Chromium, and generates your configuration templates.

---

### 2. Configure Your `.env`
Copy `.env.example` to `.env` if not already done:
```bash
cp .env.example .env
```
Open `.env` and configure:
```ini
# 1. Your LinkedIn session cookie (Required - instructions below)
LINKEDIN_LI_AT="AQEDA..."

# 2. Your own LinkedIn profile URL (Required - prevents self-commenting)
MY_PROFILE_URL="https://www.linkedin.com/in/your-profile-slug/"

# 3. LLM API Key (OPTIONAL if running inside a Cloud Agent like Metamuse!)
# Leave blank to let the cloud agent write comments natively at $0.00 cost.
# Or provide a free Groq key or cheap OpenAI key for standalone daemon mode.
LLM_PROVIDER="openai"
LLM_API_KEY=""
LLM_MODEL="gpt-4o-mini"
```

> **💡 Zero-Cost Tip**: If your friends are running inside an agent like **Metamuse**, they do **not** need an OpenAI key. The cloud agent handles reasoning natively. If running on a standalone VPS/cron, use **Groq** (`LLM_PROVIDER="groq"`, model `llama-3.1-8b-instant`), which is 100% free.

#### 🔑 How to Get Your `li_at` Cookie in 15 Seconds:
1. Open Google Chrome and log in to [LinkedIn](https://www.linkedin.com).
2. Press `F12` (or Right-Click anywhere ➔ **Inspect**).
3. Click the **Application** tab (or **Storage** tab on Firefox/Safari).
4. In the left panel, expand **Cookies** ➔ click `https://www.linkedin.com`.
5. Find the row named `li_at`, double-click its value, and copy it.
6. Paste it into `LINKEDIN_LI_AT` in your `.env`.

*(Note: The `li_at` session cookie bypasses all 2FA challenges and stays valid for 60 to 90 days. You never store your password.)*

---

### 3. Add Your Pod Members (`members.json`)
Open `members.json` and ensure all 15–20 members' profile URLs are listed:
```json
[
  {
    "name": "Siva Sankar Tummala",
    "profile_url": "https://www.linkedin.com/in/sivasankartummala/"
  },
  {
    "name": "Madan Warlamoodi",
    "profile_url": "https://www.linkedin.com/in/madanwarlamoodi/"
  }
]
```

---

### 4. Verify Everything Works
Run a diagnostic test:
```bash
./run.sh test
```
If both LLM generation and LinkedIn authentication pass, you're ready!

---

## 🤖 Running the Engine

### Option A: In an Always-On Cloud Agent (e.g. Metamuse / Antigravity)
If you are running inside an autonomous cloud agent container, use the built-in daemon mode:
```bash
./run.sh daemon
```
This keeps the process alive and runs sweeps at **08:15, 12:30, 16:45, and 20:15** every day.

### Option B: System Cron (Linux / Mac / VPS)
Add the scheduled runs to your crontab (`crontab -e`):
```cron
15 8 * * * cd /path/to/linkedin-propel-engine && ./run.sh >> pod.log 2>&1
30 12 * * * cd /path/to/linkedin-propel-engine && ./run.sh >> pod.log 2>&1
45 16 * * * cd /path/to/linkedin-propel-engine && ./run.sh >> pod.log 2>&1
15 20 * * * cd /path/to/linkedin-propel-engine && ./run.sh >> pod.log 2>&1
```

### Option C: Manual Sweep
Run an on-demand sweep at any time:
```bash
./run.sh
```

To test without publishing real comments, run:
```bash
./run.sh dry-run
```

To view today's statistics:
```bash
./run.sh status
```

---

## 🛡 Anti-Bot & Safety Guardrails

- **Zero Generic Praise**: The LLM prompt explicitly bans filler like *"Great post!"*, *"Totally agree!"*, and *"Thanks for sharing!"*. It generates thoughtful, peer-to-peer technical/business observations.
- **Strictly No Parentheses**: Completely avoids `( )` in text to prevent formatting truncations on LinkedIn.
- **Randomized Member Order & Human Jitter**: The pod list is shuffled randomly on every single run, with 20–50 second typing and navigation pauses between actions.
- **Rate Limit Safety**: Default caps limit the engine to 4 comments per run and a maximum of 12 comments per day.

---

## 🤝 Pod Etiquette & Golden Rules

1. **Stagger Post Timings**: Don't all publish at 9:00 AM. Spread posts across morning (7–9 AM), lunch (12–1 PM), and evening (5–6 PM).
2. **Reply to Comments**: When a pod member comments on your post, reply to them! The engine is designed to reply back to your reply, doubling the dwell time on your post.
3. **Keep `members.json` in Sync**: Share updates to the pod list via Git so everyone supports all 15–20 members equally.
