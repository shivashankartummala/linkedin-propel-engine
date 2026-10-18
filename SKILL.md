---
name: linkedin-propel-engine
description: >-
  Autonomous mutual engagement pod engine for LinkedIn creators. Executes 4 scheduled sweeps
  daily, detects fresh posts from pod members, generates thoughtful anti-bot 1-2 line comments,
  tracks thread replies to boost algorithmic dwell-time, and rotates daily state automatically.
---

# LinkedIn Propel Engine

The **LinkedIn Propel Engine** is an autonomous mutual growth skill designed for groups of 15–20 active LinkedIn creators and colleagues. It automates high-value, authentic interactions to trigger LinkedIn's "Golden Window" algorithmic velocity without tripping spam detection.

---

## ⚡ Two Execution Modes

### Mode A: Agent-Native Mode (Zero LLM API Key Needed!)
When running inside an always-on cloud agent like **Metamuse** or **Antigravity**, the agent uses its own built-in LLM brain:
1. Run `./run.sh pending` to find fresh posts needing comments or thread replies (returns JSON).
2. The cloud agent crafts a razor-sharp **12 to 20 word comment** directly using its own reasoning.
3. Submit the comment via:
   ```bash
   ./run.sh post-comment --url "<post_url>" --text "<12_to_20_word_comment>"
   ```
*Result: 0 API keys required, $0 cost, completely native.*

### Mode B: Standalone Automated Mode (Background Daemon / Cron)
If running on a VPS or background cron without an interactive agent loop:
- Provide an API key in `.env` (Groq is 100% free; OpenAI `gpt-4o-mini` costs < $0.006/month).
- Run `./run.sh daemon` or schedule via cron.

---

## 🪙 Token Usage & Hyper-Optimization

The engine is engineered for near-zero token consumption:
- **Input Truncation**: Truncates post to the first 400 characters (captures the hook and core premise, stripping author bios, footers, CTAs, and hashtags).
- **Output Token Cap**: Capped at `max_tokens: 35` for comments and `max_tokens: 25` for replies.
- **Strict Word Budget**: Exactly **12 to 20 words**. No filler, no conversational cheerleading.

### Daily Token Math:
- 4 comments/day: ~150 input tokens × 4 = 600 input tokens.
- 4 comments/day: ~25 output tokens × 4 = 100 output tokens.
- 2 thread replies: ~100 input tokens × 2 = 200 input tokens + 30 output tokens.
- **Total Daily Consumption: ~930 tokens/day** (~0.0009k tokens).
- **Monthly Cost on `gpt-4o-mini`**: Less than **$0.01 per month** (or **FREE** with Groq / Cloud Agent Native).

---

## 🔄 The 4-Phase Daily Lifecycle

| Run Phase | Primary Objective | Algorithm Trigger |
| :--- | :--- | :--- |
| **Run 1 (Morning ~8 AM)** | **New Post Sweep**: Detects posts (< 24h) from pod members and publishes a sharp 12–20 word comment. | Seeds initial 60–90 min engagement velocity. |
| **Run 2 (Noon ~12 PM)** | **Thread Replies & Mid-Day Sweep**: Checks if authors/members replied to our morning comments and posts a 1-sentence follow-up. | Multiplies comment depth and increases dwell time. |
| **Run 3 (Afternoon ~4 PM)** | **Thread Continuity**: Sweeps active threads for late replies and catches afternoon posts. | Keeps post active on 2nd and 3rd degree feeds. |
| **Run 4 (Evening ~8 PM)** | **Evening Wrap**: Final reply pass on today's conversations. | Closes daily threads and prepares state for next-day rotation. |

---

## 🛠 Commands

```bash
# 1. Inspect fresh posts needing comments (Agent-Native Mode)
./run.sh pending

# 2. Submit comment directly from Cloud Agent
./run.sh post-comment --url "<post_url>" --text "<comment>"

# 3. Autonomous single batch sweep (uses LLM from .env if present)
./run.sh

# 4. Dry-run test (simulates without publishing)
./run.sh dry-run

# 5. Diagnostic connectivity test
./run.sh test

# 6. View today's stats
./run.sh status

# 7. Run as background daemon (4x daily)
./run.sh daemon
```

---

## 🛡 Commenting Rules & Guardrails

1. **Word Count**: Exactly 12 to 20 words.
2. **Zero Generic Praise**: Never use *"Great post"*, *"Spot on"*, *"Kudos"*, or *"Totally agree"*.
3. **Strictly Zero Parentheses**: Never use `(` or `)`.
4. **Tone**: Senior peer, pragmatic, technical, or operational observation.
