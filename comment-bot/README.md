# 🚀 LinkedIn Propel Engine (Muse Copilot Edition)

> **Zero-Risk, 1-Reply Mutual Engagement Copilot for Creators & Leaders**

LinkedIn Propel Engine is an autonomous engagement skill built for a private circle of 15–20 active LinkedIn creators running inside **Metamuse**.

Instead of unpredictable auto-bots, Propel Engine implements a **Human-in-the-Loop 1-Reply Approval Model**:
1. Muse monitors your pod members' latest posts using its authenticated browser session.
2. Muse crafts **3 razor-sharp 12–20 word comment options** (strictly zero emojis, zero generic praise).
3. Muse delivers the options directly into your chat.
4. Each card arrives as its own chat message with **tappable `POST 1` / `POST 2` / `POST 3` buttons directly beneath it** — tap one to approve (or reply `POST 1` in text, or type a custom edit).
5. Muse executes the browser submission using a **strict human-mimicking DOM protocol** (natural dwell time, reading scroll, keystroke jitter, and proofreading pauses).

---

## ⚡ The 1-Reply Engagement Loop

```
1. Muse detects fresh post from pod member (<24h)
2. Muse sends a card with 3 comment options + tappable buttons beneath it
3. You tap "POST 1" (or reply in text)
4. Muse opens browser, simulates reading delay, types with keystroke jitter, and submits!
```

---

## 💬 How to Invoke

Everything runs from plain chat messages — no CLI, nothing to configure after setup:

| Say this | What happens |
|---|---|
| `run propel sweep` | **Pod Mode** — Muse scans all pod members for posts from the last 24 hours and sends one POD ALERT card per fresh post. |
| `run self sweep` | **Self Mode** — Muse scans your own posts from the last 3 days for comments you haven't replied to and sends one REPLY ALERT card per unanswered comment. |
| Tap `POST 1` / `POST 2` / `POST 3` under a card | Approves that exact comment (or reply) and posts it via the browser with human pacing. |
| `Lee: POST 2` (typed) | The same approval in text form — creator name + option number. Sending your own edited comment text works too. |
| `done` or `skip rest` | Ends the current queue; untapped options are dropped. |
| `add <profile URL or name> to the pod` | Adds a creator to `members.json` (name matches are confirmed with you before saving). |
| `remove <name> from the pod` | Removes a creator from `members.json`. |
| `set delay <seconds>` | Configures dwell delay before reading and typing simulation (default: 15s). |
| `set retry limit <N>` | Configures maximum retry attempts for DOM element discovery and submission (default: 3). |

First run with an empty `members.json`? Just say `run propel sweep` — Muse runs the guided setup first (your own profile URL + your pod list), then sweeps.

---

## 🪞 Self Mode: Never Miss a Comment on Your Own Posts

Run **`run self sweep`** and Muse flips the lens:

1. Muse scans **your own posts from the last 3 days** for comments you haven't replied to yet.
2. For each unanswered comment, you get a **REPLY ALERT** card showing the commenter, their full comment, and **3 reply options** (12–20 words, same strict rules) from three reply angles:
   - **1️⃣ Adds Depth**: A concrete detail, a number, or the reasoning behind your post.
   - **2️⃣ Dry Wit**: A light, dry-humored acknowledgment in your voice — warm, never flattery.
   - **3️⃣ Socratic Follow-up**: A question back to the commenter that keeps the thread alive.
3. Tap the button beneath the card and Muse posts the reply **nested under that exact comment**, using the same human-mimicking protocol.

Comments you wrote yourself and threads you already answered are skipped automatically.

---

## 🤖 The Human-Mimicking Browser Protocol

When you approve a comment via chat, Muse executes with strict anti-bot protections:
1. **Dwell & Reading Simulation**: Pauses 15–25 seconds after page load with natural vertical scrolling to simulate reading.
2. **Focus Delay**: Clicks comment box and pauses 2–3 seconds before typing.
3. **Keystroke Jitter**: Types character by character with 25–50ms delays and natural micro-pauses between words (no instant string injection).
4. **Proofreading Pause**: Waits 3–5 seconds after typing before moving to the submit button.
5. **Post Verification**: Waits 4–6 seconds after clicking submit to confirm the comment rendered in the feed.

---

## 🛠 Setup in Metamuse (30 Seconds)

1. **Import this repository** into your Metamuse agent:
   `https://github.com/shivashankartummala/linkedin-propel-engine`
2. **Prerequisite: One-Time Interactive Login**:
   - The first time Muse runs this skill (or if your session ever expires), Muse will automatically launch an interactive browser session at `https://www.linkedin.com/login` and hand control over to you.
   - Simply take over the browser window, log in with your credentials, verify your home feed loads, and hand control back to Muse.
   - Muse saves this persistent session permanently and immediately proceeds with the sweep!
3. **Pod roster (`members.json`)**:
   - On first run you don't need to edit anything by hand — Muse walks you through it: it asks for your own LinkedIn profile URL, then collects the creators you want in your pod (URLs or names; name matches are confirmed with you before saving) and writes `members.json` for you.
   - Anytime after that, just say "add <profile> to the pod" or "remove <name> from the pod" in chat, or edit `members.json` directly: set `"my_profile_url"` to your own profile URL (so Muse never comments on your own posts) and keep pod members in the `"members"` array (up to 20).

---

## 🛡️ Strict Commenting Rules (Enforced by Muse)

- **Strictly Zero Emojis**: Absolutely no emojis (no rockets, smileys, thumbs up, etc.) inside the comments. Clean, pure professional prose only.
- **Length**: Strictly 12 to 20 words per comment.
- **Zero Generic Praise**: Never uses "Great post", "Kudos", "Totally agree", "Spot on", or "Well said".
- **Zero Parentheses**: Never includes `(` or `)`.
- **Three Strategic Angles**:
  - **1️⃣ Pragmatic Architecture**: Production trade-offs and operational realities.
  - **2️⃣ Contrarian Realist**: Grounded perspective puncturing corporate/AI hype.
  - **3️⃣ Socratic Question**: Thoughtful question prompting the author to reply.

---

## 📋 Example Chat Interaction

```markdown
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📢 POD ALERT: MADHAN VADLAMUDI (Today)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📌 Post Hook / Topic:
"Breaking down monolithic architectures too early creates network overhead..."

🔗 [👉 View Post on LinkedIn](https://www.linkedin.com/feed/update/urn:li:activity:7251...)

💡 Proposed Comment Options (12–20 Words | No Emojis):

1️⃣ Pragmatic Architecture [18 words]
Solid operational point here. Scaling this in production always comes down to disciplined team execution and clear ownership.

2️⃣ Contrarian Realist [18 words]
The real bottleneck was never raw execution speed - it has always been reviewing and maintaining untrusted diffs.

3️⃣ Socratic Question [16 words]
How is your team handling boundary validation when unexpected edge cases hit production under peak traffic?
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
👉 How to Publish:  
• Tap the 'POST 1', 'POST 2', or 'POST 3' button directly below this card and I will submit it via browser!  
• Or reply 'POST 1', 'POST 2', or 'POST 3' (or type a custom edit).
```

When you reply **`POST 1`**, Muse replies:
> ✅ **Successfully published to Madhan Vadlamudi's post!**  
> 💬 *"Solid operational point here. Scaling this in production always comes down to disciplined team execution and clear ownership."*  
> 🔗 [Open Post on LinkedIn](https://www.linkedin.com/feed/update/urn:li:activity:7251...)
