# 🚀 LinkedIn Propel Engine

> **The Unified Autonomous Inbound & Outbound Growth Suite for LinkedIn (Muse / Metamuse Edition)**

`linkedin-propel-engine` is a modular, dual-engine LinkedIn automation suite designed for **Muse** (cloud-native autonomous agent) and **Metamuse**. It provides a 360-degree growth loop combining high-authority content publishing with targeted peer-pod engagement.

---

## ⚡ Architecture & Dual-Engine Strategy

```
                              +----------------------------+
                              |      METAMUSE AGENT        |
                              +----------------------------+
                               /                          \
                              /                            \
                             v                              v
            +-------------------------------+   +-------------------------------+
            |        CO-AUTHOR BOT          |   |          COMMENT BOT          |
            |     (Inbound Authority)       |   |      (Outbound Velocity)      |
            +-------------------------------+   +-------------------------------+
            | • Persona & Topic Parameterized|   | • Creator Pod Monitoring (<24h)|
            | • Anti-AI Practitioner Voice  |   | • 3 Crisp Angles (12-20 words)|
            | • 4 Hand-Drawn Visual Themes  |   | • Strictly Zero Emojis/Fluff  |
            | • 5-Line Action CTA + SEO Tags|   | • 1-Click / 1-Reply Approval  |
            | • Buffer.com API Integration  |   | • Anti-Bot DOM Typing Protocol|
            +-------------------------------+   +-------------------------------+
                             \                              /
                              \                            /
                               v                          v
                        +----------------------------------------+
                        |        TARGET: LINKEDIN PROFILE        |
                        |  Scheduled Posts + Pod Post Engagement |
                        +----------------------------------------+
```

1. **Inbound Engine (`co-author-bot/`)**: Establishes domain authority and attracts organic followers through recurring, deep technical series ("The Litmus Test") scheduled via Buffer.com.
2. **Outbound Engine (`comment-bot/`)**: Multiplies feed visibility and profile visits through high-signal, anti-hype comments on target creators' posts using human-mimicking browser automation.

---

## 📁 Repository Structure

```
linkedin-propel-engine/
├── README.md                   # Unified architecture & quickstart guide (this file)
├── .gitignore                  # Global repository ignore rules
├── co-author-bot/              # Track 1: Inbound Content Generation & Buffer Scheduler
│   ├── README.md               # Detailed co-author documentation, templates & setup
│   └── SKILL.md                # Muse agent skill specification & prompt codex
└── comment-bot/                # Track 2: Outbound Pod Engagement & Browser Submitter
    ├── README.md               # Detailed comment bot documentation & DOM protocol
    ├── SKILL.md                # Muse agent skill specification & prompt codex
    └── members.json            # Target creator pod list & configuration
```

---

## 🛠️ The Sub-Agents at a Glance

### 1. Co-Author Bot (`co-author-bot/`)
- **Mission**: Acts as your personal ghostwriter and scheduler for 2-part technical LinkedIn series (Question days alternating with Answer Breakdown days).
- **Key Features**:
  - **Persona Parameterization**: Adapts to any role (Principal SRE Architect, Staff Data Engineer, Principal DBA, VP of Product, Cloud Security Lead).
  - **Voice Guardrails**: Strict ban on AI clichés (`delve`, `unleash`, `testament`), zero parentheses `( )` to prevent API truncation, and authentic battle-tested engineering tone.
  - **4 Signature Visual Themes**: Customizable graphic styles (Classic Yellow Legal Pad, Minimalist Muji Dot-Grid, Technical Blueprint, Executive College-Ruled).
  - **Conversion Architecture**: Mandatory 5-line multi-action CTA block (Comment, Save, Repost, Announce, Follow) and 3-tier SEO hashtag formula (`#CreateImpact`).
  - **Mandatory HITL Gate**: Pauses for explicit user review and approval before scheduling.
  - **Buffer Integration**: Queues approved posts directly into Buffer (`POST /1/updates/create.json`).
- **[👉 View Co-Author Bot Documentation](co-author-bot/README.md)**

---

### 2. Comment Bot (`comment-bot/`)
- **Mission**: Monitors a private circle of 15–20 creators, identifies fresh posts (<24h), drafts 3 concise comment options, and submits upon your 1-reply approval.
- **Key Features**:
  - **Zero Generic Fluff**: Never uses generic praise ("Great post", "Kudos"). Strictly 12 to 20 words per comment.
  - **Strictly Zero Emojis**: Clean, professional, high-density text that earns top-comment placement.
  - **Three Strategic Perspectives**:
    - *Angle 1 (Pragmatic Architecture)*: Operational realities and production trade-offs.
    - *Angle 2 (Contrarian Realist)*: Punctures corporate or AI hype.
    - *Angle 3 (Socratic Question)*: Compels the author to respond and drives comment thread velocity.
  - **1-Click Tappable Buttons**: Integrates with `muse.create_options` for 1-tap mobile approval or 1-reply text (`POST 1`, `POST 2`, `POST 3`).
  - **Human-Mimicking Browser DOM Protocol**: Anti-bot protections with natural reading dwell times (15–25s), typing delays (25–50ms jitter), and proofreading pauses.
- **[👉 View Comment Bot Documentation](comment-bot/README.md)**

---

## 🚀 Quickstart: Setting Up in Metamuse

### Step 1: Import the Repository
In Metamuse / Muse, import this repository:
```
https://github.com/shivashankartummala/linkedin-propel-engine.git
```

### Step 2: Configure Co-Author Bot (`co-author-bot/`)
1. Obtain your Buffer Access Token from [buffer.com/developers/api](https://buffer.com/developers/api).
2. Connect your LinkedIn profile or page inside Buffer.
3. Provide the token during Muse's interactive onboarding gate.
4. Select your persona, posting cadence, and signature visual theme (1–4).

### Step 3: Configure Comment Bot (`comment-bot/`)
1. Complete the one-time interactive login at `https://www.linkedin.com/login` when prompted by Muse.
2. Edit [`comment-bot/members.json`](comment-bot/members.json):
   - Set `"my_profile_url"` to your own profile URL.
   - Populate the `"members"` array with the profile URLs of the creators in your mutual engagement pod.

---

## 🔒 Safety, Security & Compliance
- **100% Human-in-the-Loop**: Neither bot will ever publish content or submit comments without your explicit approval.
- **Credential Hygiene**: Access tokens are kept in environment variables or private agent storage; never commit API tokens or browser cookies.
- **Rate-Limiting & Anti-Bot Awareness**: Both bots adhere to conservative schedules and realistic human dwell times to keep your account safe.

---

## 📄 License
MIT License. Built for creators and leaders running on Metamuse.
