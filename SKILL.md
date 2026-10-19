---
name: linkedin-propel-engine
description: >-
  Copilot engine for mutual engagement pods on LinkedIn for Metamuse. Polls pod members'
  recent activity using Muse's authenticated browser session, drafts 3 distinct 12-20 word
  comments, and delivers 1-Click Action Cards to the Muse chat for instant copy-paste engagement.
---

# LinkedIn Propel Engine (Muse Copilot Edition)

The **LinkedIn Propel Engine** is designed to run seamlessly inside **Metamuse**. 

Because you have logged in to LinkedIn once via Muse's browser session, Muse holds the authenticated session. Muse uses that session to safely poll your 15–20 pod members, pull today's posts, draft **3 distinct 12–20 word comment options**, and deliver them as **1-Click Action Cards** in the Muse chat.

---

## ⚡ How Muse Executes the Workflow

When instructed to *"Check pod posts"* or when triggered on a schedule (e.g. 4x a day):

1. **Read Pod Members**:
   Muse reads the creator profiles from [`members.json`](./members.json).

2. **Poll Recent Activity**:
   Using its saved browser session, Muse visits each creator's recent activity:
   `https://www.linkedin.com/in/{creator_slug}/recent-activity/all/`

3. **Check for Fresh Posts (<24 Hours)**:
   If a post was published today (and not already in `state.json`), Muse extracts:
   - Post URL
   - Author Name
   - Post Text Content

4. **Generate 1-Click Action Card**:
   Muse calls the helper to generate the 3 distinct 12–20 word comment angles and format the card:
   ```bash
   ./run.sh card --author "Madhan Vadlamudi" --url "https://www.linkedin.com/feed/update/..." --text "..."
   ```

5. **Deliver to Chat**:
   Muse posts the 1-Click Action Card into the chat window.

---

## 📱 User 2-Click Action Loop

When the card appears in Muse chat:
1. **Tap to Copy**: Tap on any of the 3 monospace comment boxes (copies to your clipboard instantly).
2. **Tap to Open**: Tap the post link (opens the post in your personal browser or mobile app).
3. **Paste & Submit**: Hit post!

*Takes 5 to 10 seconds. 100% human-verified and safe.*

---

## 🛠 Commands

```bash
# 1. Generate 1-Click Action Card from scraped post text
./run.sh card --author "Madhan Vadlamudi" --url "https://..." --text "..."

# 2. On-demand: Generate comments for any single post URL
./run.sh draft --url "https://www.linkedin.com/feed/update/..."

# 3. Sweep all members (if running with local Chrome)
./run.sh poll

# 4. View today's status
./run.sh status
```

---

## 💡 The 3 Comment Angles (Strictly 12–20 Words)

1. **Pragmatic Architecture**: Highlights an operational trade-off, execution reality, or production constraint.
2. **Contrarian Realist**: Punctures corporate/AI hype with grounded engineering logic.
3. **Socratic Question**: Asks a sharp, nuanced question that prompts the author to reply (multiplying post dwell time).
