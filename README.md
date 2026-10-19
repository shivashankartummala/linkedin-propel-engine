# 🚀 LinkedIn Propel Engine (Copilot Edition)

> **Zero-Risk, 1-Click Mutual Engagement Copilot for Creators & Leaders**

LinkedIn Propel Engine is an engagement assistant built for circles of 15–20 active LinkedIn creators. 

Instead of risky headless browser bots that get accounts flagged and logged out, Propel Engine acts as your **personal engagement copilot**: it monitors your pod members' latest posts, generates **3 razor-sharp 12–20 word comment options**, and posts them into your chat as **1-Click Action Cards**.

---

## ⚡ The 10-Second Engagement Loop

```
1. Bot detects new post from pod member (e.g. Madhan Vadlamudi)
2. Bot sends 1-Click Action Card to chat (Muse Chat / WhatsApp / Telegram)
3. You tap the comment box to copy ➔ tap link to open post ➔ paste & submit!
```

**Why this works:**
- **0% Account Risk**: No headless browser logins, no cookie hijacking, zero session revocations.
- **100% Authentic Signal**: Comments are posted from your real device on your residential network, which LinkedIn’s algorithm rewards with maximum dwell-time reach.
- **Zero Mental Effort**: You never have to think about what to write—the engine crafts 3 high-impact angles in under 20 words each.

---

## 🛠 Quick Start

### 1. Setup Environment
```bash
git clone https://github.com/shivashankartummala/linkedin-propel-engine.git
cd linkedin-propel-engine
./setup.sh
```

### 2. Configure `.env`
```ini
# Optional: Provide an API key or leave blank for Metamuse native model
LLM_PROVIDER="openai"
LLM_API_KEY=""
LLM_MODEL="gpt-4o-mini"

# Your own profile URL (prevents generating cards for your own posts)
MY_PROFILE_URL="https://www.linkedin.com/in/sivasankartummala/"
```

### 3. Add Your Pod Members (`members.json`)
```json
[
  {
    "name": "Madhan Vadlamudi",
    "profile_url": "https://www.linkedin.com/in/madhanvadlamudi/"
  },
  {
    "name": "Sravan Ananthula",
    "profile_url": "https://www.linkedin.com/in/sravanananthula/"
  }
]
```

---

## 💻 Commands

```bash
# 1. Sweep all pod members and generate today's Action Cards
./run.sh poll

# 2. On-demand: Draft 3 comments for any post URL dropped into chat
./run.sh draft --url "https://www.linkedin.com/in/madhanvadlamudi/"

# 3. View status of surfaced posts today
./run.sh status
```

---

## 💡 Example Action Card Generated

```markdown
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📢 POD ALERT: MADHAN VADLAMUDI (Recent)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📌 Post Hook / Topic:
"Breaking down monolithic architectures too early creates network overhead..."

🔗 [👉 Tap Here to Open Post on LinkedIn](https://www.linkedin.com/in/madhanvadlamudi/)

💡 1-Click Comment Options (12–20 Words):
(Tap any comment box below to copy, click the link above, paste & post!)

1️⃣ Pragmatic Architecture [18 words]
Solid operational point here. Scaling this in production always comes down to disciplined team execution and clear ownership.

2️⃣ Contrarian Realist [18 words]
The real bottleneck was never raw execution speed - it has always been reviewing and maintaining untrusted diffs.

3️⃣ Socratic Question [16 words]
How is your team handling boundary validation when unexpected edge cases hit production under peak traffic?
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```
