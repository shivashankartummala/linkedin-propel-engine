# 🚀 LinkedIn Propel Engine (Muse Copilot Edition)

> **Zero-Risk, 1-Reply Mutual Engagement Copilot for Creators & Leaders**

LinkedIn Propel Engine is an autonomous engagement skill built for a private circle of 15–20 active LinkedIn creators running inside **Metamuse**.

Instead of unpredictable auto-bots, Propel Engine implements a **Human-in-the-Loop 1-Click / 1-Reply Approval Model**:
1. Muse monitors your pod members' latest posts using its authenticated browser session.
2. Muse crafts **3 razor-sharp 12–20 word comment options** (strictly zero emojis, zero generic praise).
3. Muse delivers the options directly into your chat with **tappable approval buttons** (`muse.create_options`).
4. You simply **tap a button** (e.g. `Lee: POST 2`) or reply **`POST 1`**, **`POST 2`**, or **`POST 3`** (or type a custom edit).
5. Muse executes the browser submission using a **strict human-mimicking DOM protocol** (natural dwell time, reading scroll, keystroke jitter, and proofreading pauses).

---

## ⚡ The 1-Click / 1-Reply Engagement Loop

```
1. Muse detects fresh post from pod member (<24h)
2. Muse sends 3 comment options to chat + tappable buttons (muse.create_options)
3. You tap the button: [Lee: POST 2] (or type "POST 1" in chat)
4. Muse opens browser, simulates reading delay, types with keystroke jitter, and submits!
```

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
3. **Customize `members.json`**:
   - Set `"my_profile_url"` to your own profile URL (so Muse never comments on your own posts).
   - Add your 15–20 pod members to the `"members"` array.

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
• **Tap a button below** to post that comment instantly (one tap per comment).
• Or reply `POST 1`, `POST 2`, or `POST 3` (e.g. `Lee: POST 2`), or type a custom edit.
```

When you tap **`Lee: POST 1`** (or reply **`POST 1`**), Muse replies:
> ✅ **Successfully published to Madhan Vadlamudi's post!**  
> 💬 *"Solid operational point here. Scaling this in production always comes down to disciplined team execution and clear ownership."*  
> 🔗 [Open Post on LinkedIn](https://www.linkedin.com/feed/update/urn:li:activity:7251...)
