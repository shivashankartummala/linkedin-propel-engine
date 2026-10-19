# 🚀 LinkedIn Propel Engine (Muse Copilot Edition)

> **Zero-Risk, 1-Click Mutual Engagement Copilot for Creators & Leaders**

LinkedIn Propel Engine is an autonomous engagement skill built for a private circle of 15–20 active LinkedIn creators running inside **Metamuse**.

Instead of risky headless browser bots that get accounts flagged, Propel Engine acts as your **personal engagement copilot**: 
1. Muse monitors your pod members' latest posts using its authenticated browser session.
2. Muse crafts **3 razor-sharp 12–20 word comment options** (strictly zero emojis, zero generic praise).
3. Muse delivers them directly into the chat as **1-Click Action Cards**.
4. You tap the comment box to copy, tap the link to open the post in your real browser or mobile app, paste, and post!

---

## ⚡ The 10-Second Engagement Loop

```
1. Muse detects fresh post from pod member (<24h)
2. Muse sends 1-Click Action Card to chat
3. You tap comment to copy ➔ tap link to open post ➔ paste & submit!
```

---

## 🛠 Setup in Metamuse (30 Seconds)

1. **Import this repository** into your Metamuse agent:
   `https://github.com/shivashankartummala/linkedin-propel-engine`
2. **Log in to LinkedIn once** via Muse's interactive browser session (Muse saves this authenticated profile permanently).
3. **Customize `members.json`**:
   - Set `"my_profile_url"` to your own profile URL.
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

## 📋 Example Action Card

```markdown
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📢 POD ALERT: MADHAN VADLAMUDI (Today)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📌 Post Hook / Topic:
"Breaking down monolithic architectures too early creates network overhead..."

🔗 [👉 Tap Here to Open Post on LinkedIn](https://www.linkedin.com/feed/update/urn:li:activity:7251...)

💡 1-Click Comment Options (12–20 Words | No Emojis):
(Tap any comment box below to copy, click the link above, paste & post!)

1️⃣ Pragmatic Architecture [18 words]
Solid operational point here. Scaling this in production always comes down to disciplined team execution and clear ownership.

2️⃣ Contrarian Realist [18 words]
The real bottleneck was never raw execution speed - it has always been reviewing and maintaining untrusted diffs.

3️⃣ Socratic Question [16 words]
How is your team handling boundary validation when unexpected edge cases hit production under peak traffic?
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## 🤖 Instructing Muse to Run

Give Muse this instruction or set it as a recurring scheduled task:

> *"Check pod posts: Read `members.json`, check each member's recent activity using your saved LinkedIn browser session for posts published today, and output 1-Click Action Cards for any new posts found."*
