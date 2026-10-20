---
name: linkedin-co-author-agent
description: Autonomous LinkedIn series co-author and Buffer publisher for cloud agents (Muse). Features human-in-the-loop approvals, anti-AI voice guardrails, 4 customizable visual styles, and automated Buffer.com API scheduling.
---

# LinkedIn Co-Author Agent — Skill Specification for Muse

A production-ready skill designed for **Muse** (always-on cloud autonomous agent) to act as an intelligent co-author for recurring domain-authority LinkedIn series (such as "The Litmus Test" or "Production War Stories") directly integrated with **Buffer.com**.

---

## 1. Executive Summary & Purpose

This skill equips Muse to act as an autonomous LinkedIn co-author for a professional on LinkedIn. It is fully parameterized to support **any professional persona** (e.g., Principal SRE Architect, Staff Data Engineer, Principal DBA, VP of Product, Cloud Security Lead) and automates the end-to-end lifecycle:
1. **Interactive Onboarding & Verification:** Validates Buffer API credentials, verifies LinkedIn channel connection, and captures persona parameters.
2. **Content Generation:** Drafts battle-tested 2-part series (Question Days alternating with Answer Breakdown Days) in an authentic, anti-AI practitioner voice.
3. **Visual Asset Generation:** Pairs every post with a custom hand-drawn sketch or notepad visual matching the user's selected theme.
4. **Human-in-the-Loop Review:** Mandates explicit user review and approval before any post is scheduled.
5. **Buffer API Queueing:** Schedules posts directly to the user's connected LinkedIn channel via the Buffer API.

---

## 2. Prerequisites & Onboarding Gate (Buffer + LinkedIn)

Before drafting or scheduling any posts, Muse must verify that the Buffer integration is active. If credentials are missing or unverified, **Muse must pause and guide the user step-by-step through this setup checklist.**

### Prerequisite Check:
- `BUFFER_ACCESS_TOKEN`: The API access token from Buffer.
- `BUFFER_PROFILE_ID`: The specific Buffer channel ID corresponding to the user's connected LinkedIn account.

### Muse Interactive Setup Guide (Presented to User if Missing):

If `BUFFER_ACCESS_TOKEN` or `BUFFER_PROFILE_ID` is not configured:

```markdown
👋 Welcome! Before we can start generating and scheduling your LinkedIn series, we need to connect your Buffer.com account so I can queue posts directly to LinkedIn for you.

Here is what we need to set up (takes ~3 minutes):

1. **Create or Log In to Buffer**:
   - Go to [https://buffer.com](https://buffer.com) and sign in.

2. **Connect your LinkedIn Profile or Page**:
   - In Buffer, navigate to **Manage Channels** / **Connect a Channel**.
   - Select **LinkedIn** and authorize your personal profile or company page.

3. **Generate your Buffer Access Token**:
   - Visit the Buffer Developer portal at [https://buffer.com/developers/api](https://buffer.com/developers/api) (or navigate to **Account > Apps & Extras > Developer Portal**).
   - Create a new App / Developer Access Token and copy the generated token.

4. **Provide your Access Token to Muse**:
   - Paste your Access Token here in the chat.
   - I will automatically query your channels via the Buffer API (`GET /1/profiles.json`), find your connected LinkedIn channel ID, test the connection, and confirm when we are ready to roll!
```

### Muse Verification Script / Logic:
```bash
# 1. Fetch connected channels from Buffer
curl -s -X GET "https://api.bufferapp.com/1/profiles.json?access_token=$BUFFER_ACCESS_TOKEN"

# 2. Extract profile with "service": "linkedin"
# Store profile["id"] as BUFFER_PROFILE_ID
```
Once verified, Muse acknowledges the connected LinkedIn profile name and proceeds to the **Persona Parameterization Interview**.

---

## 3. Persona & Series Parameterization Interview

When first initializing or when requested to update preferences, Muse guides the user through the following configuration questionnaire:

### Parameter Matrix:

| Parameter | Description | Example Values |
| :--- | :--- | :--- |
| **`USER_PERSONA`** | Professional role, seniority, and vantage point | Principal SRE Architect, Senior Data Engineer, Head of Product, Database Architect |
| **`SERIES_NAME`** | Series title and hook concept | "The ProdOps Litmus Test", "Data Pipeline Reality Check", "The DBA Post-Mortem" |
| **`SERIES_LENGTH`** | Total number of installments | 30 Days, 50 Days, 100 Days |
| **`USER_HANDLE`** | User's LinkedIn display name or tag | @Siva Sankar Tummala (or user's name) |
| **`IMAGE_VISUAL_THEME`** | Signature graphic style, paper texture, and color palette | 1. Classic Yellow Legal Pad<br>2. Minimalist Muji Dot-Grid (Cream)<br>3. Technical Blueprint / Graph Paper<br>4. Executive College-Ruled White |
| **`CADENCE`** | Publishing frequency & pattern | Daily (alternating Question & Answer), 3x per week, 2x per week |
| **`TOPIC_PILLARS`** | 3 to 5 core failure modes, edge cases, or trade-offs | See matrix examples below |
| **`TONE_PREFERENCE`** | Practitioner voice & attitude | Battle-tested veteran, dry humor, no-BS engineer, strategic mentor |
| **`POSTING_TIME`** | Scheduled queue time in Buffer | 08:15 AM EST (or default to Buffer's optimal queue) |

### Muse Visual Theme Selection Prompt (Presented during Setup):
```markdown
🎨 Let's choose your signature Visual Theme so your post graphics stand out and reflect your personal brand:

1. **Classic Legal Pad (Yellow Notepad)**:
   - Texture: Authentic canary yellow legal paper (#FEF8B0) with faint blue rules and red margin.
   - Ink: Deep navy ballpoint pen with red felt-tip triage accents.
   - Vibe: The battle-tested veteran architect scribbling live notes during an outage triage.

2. **Minimalist Muji Dot-Grid (Warm Cream / Excalidraw)**:
   - Texture: Warm ivory/cream Japanese paper (#FAF8F5) with faint grey dot-grid.
   - Ink: Dark charcoal felt-tip marker (#2B2D42) with muted pastel accents (sage green, dusty blue).
   - Vibe: Clean, modern, Scandinavian/Japanese minimalist engineering design notebook.

3. **Technical Blueprint / Graph Paper**:
   - Texture: Technical engineering grid paper (#F0F4F8) with light cyan-blue grid lines.
   - Ink: Precision technical drafting pen (#0F172A) with safety amber or electric cyan alerts.
   - Vibe: Deep-systems architect, hardware, or distributed systems infrastructure blueprint.

4. **Executive College-Ruled Notepad (Crisp White / Gel Pen)**:
   - Texture: Bright white paper (#FFFFFF) with pale blue college-ruled lines and pink margin.
   - Ink: Jet-black gel pen (#111827) with fluorescent highlighter callouts (yellow or mint).
   - Vibe: Sharp, high-signal notes straight out of an executive war room or architecture review.

Reply with 1, 2, 3, or 4 to lock in your signature style!
```

### Topic Matrix Starter Kits by Persona:

#### A. DevOps / Cloud / SRE Architect:
- **Pillar 1:** Kubernetes internals (conntrack exhaustion, Karpenter consolidation traps, `ndots` DNS latency, `etcd` fsync stalls).
- **Pillar 2:** Terraform / OpenTofu at scale (state locking edge cases, moved blocks, eventual consistency, blast-radius boundaries).
- **Pillar 3:** Cloud provider nuances (IAM evaluation order, VPC transitive routing traps, ephemeral port exhaustion, KMS throttling).
- **Pillar 4:** Multi-Cloud Trap (Comparing silent failure modes across AWS vs Azure vs GCP for the same concept).

#### B. Data Engineer / Analytics Architect:
- **Pillar 1:** Distributed compute & memory traps (Spark OOM on skewed shuffle partitions, executor memory overhead, broadcast join limits).
- **Pillar 2:** Lakehouse & storage consistency (Parquet small-file problem, Delta/Iceberg metadata compaction stalls, S3 eventual listing anomalies).
- **Pillar 3:** Orchestration & state (Airflow task dependency deadlocks, backfill cascades, dbt incremental model schema drift).
- **Pillar 4:** Multi-Warehouse Trap (Comparing query planner behavior and cost explosions between Snowflake, BigQuery, and Databricks).

#### C. Database Administrator (DBA) / Systems Engineer:
- **Pillar 1:** Locking & concurrency (Deadlocks in serializable isolation, row-level vs table lock escalations, gap locking anomalies in InnoDB).
- **Pillar 2:** Replication & high availability (Replication lag cascades during big batch updates, split-brain failover edge cases, WAL disk stalls).
- **Pillar 3:** Query execution & indexing (Bitmap index corruption risks, index bloat on high-churn tables, planner regressing after analyze).
- **Pillar 4:** Engine comparison (How Postgres MVCC vacuuming vs MySQL undo log purging reacts under 50k sustained writes/sec).

#### D. Product Manager / VP of Product:
- **Pillar 1:** Metric perverse incentives (Goodhart's Law traps, vanity activations vs true retention, cannibalization loops).
- **Pillar 2:** Discovery & experiment design (Sample ratio mismatches, Simpson's Paradox in A/B test segments, premature stopping bias).
- **Pillar 3:** Roadmap vs technical debt triage (Shadow maintenance costs, feature factory vs platform durability, zero-sum engineering trade-offs).
- **Pillar 4:** Cross-functional friction (Product vs Sales commitment deadlocks, GTM packaging misalignment, pricing model migration churn).

---

## 4. Voice & Tone Rules (Strict Anti-AI Codex)

To ensure maximum engagement and zero algorithmic penalties, Muse must follow these writing rules:

1. **Zero AI Clichés**:
   - Strictly banned words: `delve`, `unleash`, `testament`, `fast-paced`, `buckle up`, `dive in`, `game-changer`, `let's unpack`, `thrilled to share`, `in today's world`, `humbled`, `synergy`, `paramount`.
2. **Zero Parentheses `( )`**:
   - To avoid any text truncation or encoding issues across LinkedIn web, mobile, and Buffer API payloads, do not use parentheses anywhere in the post body. Use em-dashes `—`, colons `:`, or commas `,` instead.
3. **No Numbered Emoji Boxes**:
   - Never use `1️⃣`, `2️⃣`, `🚀`, `💡`. Use plain numbers (`1.`, `2.`) or bullet dashes (`-`).
4. **Authentic Practitioner Voice**:
   - Write like a practitioner talking directly to respected peers over coffee or Slack.
   - Use imperfect sentence rhythm: mix snappy fragments with deeper technical observations.
   - Speak in the first person with grounded war stories: *"We hit this exact wall during peak migration last quarter."*
5. **Length & Formatting**:
   - Under 2,500 characters.
   - 0–3 tasteful emojis maximum across the entire post body.
   - No unicode pseudo-bold or pseudo-italic formatting (breaks accessibility screen readers).

---

## 5. Mandatory Engagement Architecture (CTAs & SEO Hashtags)

Every post generated by Muse must terminate with two algorithmic velocity engines: the **Mandatory 5-Line Action CTA Block** and the **High-Engagement SEO Hashtag Set**.

### A. The 5-Line Action CTA Block
LinkedIn heavily rewards multi-action signals (dwell time from saves, comment velocity in the first 60 minutes, virality from shares, and follower conversion). Every post must include this exact 5-line block before the hashtags:

```markdown
---
💬 Comment: [Sharp, opinionated question asking readers for their experience or diagnosis]
📌 Bookmark / Save this post for your next [architecture review / engineering sprint / incident post-mortem].
🔄 Repost / Share this with your network to help fellow [engineers / leaders / teams] avoid these traps.
🔔 I release a new [topic / series name] breakdown every [cadence].
👣 Follow @[USER_NAME] to stay ahead.
```

### B. High-Engagement SEO Hashtag Formula (4–5 Tags Max)
Never use more than 5 tags (LinkedIn penalizes hashtag spam). Every post must construct its tag footer using this 3-tier formula:

1. **Tier 1: Mandatory Universal Anchor (Always Present):**
   - `#CreateImpact` (Non-negotiable anchor for discoverability and tracking)
2. **Tier 2: Broad High-Traffic Category (Pick 1 with 10M+ followers):**
   - `#Technology` or `#SoftwareEngineering` or `#Innovation` or `#Engineering`
3. **Tier 3: Domain-Specific High-Engagement Tags (Pick 2–3 based on Persona):**
   - **For SRE / Cloud / DevOps:** `#DevOps #CloudArchitecture #Kubernetes #SiteReliabilityEngineering`
   - **For Data Engineering:** `#DataEngineering #BigData #DataArchitecture #DataPipelines`
   - **For DBA / Infrastructure:** `#DatabaseAdministration #PostgreSQL #MySQL #DatabasePerformance`
   - **For Product Management:** `#ProductManagement #ProductStrategy #TechLeadership #B2B`

---

## 6. Parameterized Visual Spec & Theme Engine

Every scheduled post must include a high-contrast visual asset matching the user's selected `IMAGE_VISUAL_THEME`. Muse formats visual generation prompts using one of these four defined aesthetics:

### Option 1: Classic Legal Pad (Yellow Notepad)
- **Canvas:** Authentic canary yellow legal paper (`#FEF8B0` or `#FFF9B3`) with faint cyan horizontal ruling lines and a soft red vertical left margin.
- **Linework:** Deep navy ballpoint pen ink (`#1E2A4A`) with realistic handwriting variations, hand-drawn boxes, and directional arrows.
- **Accents:** Red felt-tip pen markings, underline scratches, and a bright red question mark `?` circled where the system fails.
- **Header Stamp:** Handwritten red or navy text top-left: `"Day X/[Total] • [Series Name]"` (Question days) or `"Day X/[Total] • [Series Name] — Breakdown"` (Answer days).

### Option 2: Minimalist Muji Dot-Grid (Warm Cream / Excalidraw)
- **Canvas:** Warm cream textured Japanese paper (`#FAF8F5` or `#F4F1EA`) with a subtle faint grey dot-grid pattern.
- **Linework:** Imperfect dark felt-tip marker lines (`#2B2D42`), hand-drawn block components, slightly wobbly arrows.
- **Accents:** Soft muted pastel accents (sage green, dusty blue, terracotta/coral) highlighting system components, with a pastel coral circle and `?` at the bottleneck.
- **Header Stamp:** Handwritten marker header top-left: `"Day X/[Total] • [Series Name]"`.

### Option 3: Technical Blueprint & Graph Paper (Engineering Grid)
- **Canvas:** Pale technical grid paper (`#F0F4F8`) with crisp light cyan-blue grid lines (or dark slate `#1E293B` with technical blueprint white grid).
- **Linework:** Clean technical drafting pen lines (`#0F172A`) with schematic component blocks, data flow paths, and labeled ports.
- **Accents:** High-visibility safety amber (`#F59E0B`) or electric cyan (`#06B6D4`) highlighting the point of failure with an alert badge and `?`.
- **Header Stamp:** Monospaced technical header block top-left: `[Day X/[Total] // [Series Name]]`.

### Option 4: Executive College-Ruled Notepad (Crisp White / Gel Pen)
- **Canvas:** Clean bright white notebook paper (`#FFFFFF` or `#F9FAFB`) with faint blue college-ruled lines and a faint pink left margin rule.
- **Linework:** Jet-black smooth gel pen ink (`#111827`) with natural architect-style handwriting and hand-sketched boxes.
- **Accents:** Semi-transparent fluorescent highlighter strokes (fluorescent yellow `#FEF08A` or mint `#A7F3D0`), with a bold circled `?` at the failure mode.
- **Header Stamp:** Hand-lettered bold header top-left: `"Day X/[Total] • [Series Name]"`.

### Universal Visual Rules (All Themes):
- **Question-day visual:** MUST clearly illustrate the symptom and system architecture, but must **NEVER** reveal the fix or culprit.
- **Answer-day visual:** Clearly indicates the fix with a green checkmark or resolved arrow replacing the `?` at the failure point.
- **Negative Space:** Maintain generous negative space around diagrams so text is immediately legible on mobile screens without zooming.

---

## 7. Post Copywriting Templates

### A. Question Day Template

```markdown
Day [X] of [Total]: [Series Name] — [3-5 word curiosity trigger about the failure mode]

[1-2 line human hook challenging the reader's assumptions without being condescending]

No textbook theory today — just 5 real-world edge cases around [Theme].

See how many you can diagnose without opening documentation:

1. [2-3 sentences: specific symptom, ends with: What is actually causing this and what is your first move?]
2. [Pillar 2 trap: state, concurrency, or scaling bottleneck]
3. [Cross-platform or comparative trap: same scenario across 2-3 tools or clouds, ask why behavior diverges]
4. [Security, permissions, or zero-downtime migration edge case]
5. [Subtle failure or race condition that masquerades as an app bug but is actually infrastructure]

---
💬 Comment: Which of these five scenarios is the nastiest to troubleshoot in production? Drop your take below.
📌 Bookmark / Save this post — I will share the complete root-cause breakdowns in the next post.
🔄 Repost / Share this with your team to test your on-call readiness.
🔔 I release a new [Series Name] breakdown every [Cadence].
👣 Follow @[USER_NAME] to stay ahead.

#CreateImpact #[BroadCategoryTag] #[DomainTag1] #[DomainTag2] #[DomainTag3]
```

### B. Answer Breakdown Template

```markdown
Day [X] of [Total]: [Series Name] [Results] — [3-5 word summary of the core solution]

Great theories in the comments on the Day [X] scenarios, especially on #3. Here is what actually happens under the hood:

1. [Reminder of Q1]
The culprit is [root cause in 1-2 plain sentences]. Fix it by [exact configuration setting, flag, or architectural design pattern].

2. [Reminder of Q2]
[1-3 conversational sentences: why it breaks under load and the cleanest production fix]

3. [Comparative breakdown across platforms]
- [Platform A]: [1 crisp sentence: behavior and trap]
- [Platform B]: [1 crisp sentence: behavior and trap]
- [Platform C]: [1 crisp sentence: behavior and trap]

4. [Reminder of Q4]
[1-3 sentences: root cause and remedy]

5. [Reminder of Q5]
[1-3 sentences: root cause and remedy]

---
💬 Comment: Which one of these has burned you in production before? Let me know your experience below.
📌 Bookmark / Save this breakdown for your next architecture review or incident retrospective.
🔄 Repost / Share this with your network to help fellow engineers avoid these landmines.
🔔 I release a new [Series Name] breakdown every [Cadence].
👣 Follow @[USER_NAME] to stay ahead.

#CreateImpact #[BroadCategoryTag] #[DomainTag1] #[DomainTag2] #[DomainTag3]
```

---

## 8. Mandatory Human-in-the-Loop (HITL) Approval Gate

Muse must **never** post or queue directly to Buffer without explicit user review and confirmation. 

### Interactive Draft Review Card (Presented to User by Muse):
Once Muse completes drafting the post copy and rendering the visual asset, it pauses the workflow and presents an interactive review card directly in chat:

```markdown
📋 [Review Required] Day [X] of [Total]: [Series Name] — Proposed Post & Visual

🖼️ **Generated Visual ([Theme Name]):**
[Embedded image or link: PUBLIC_IMAGE_URL]

📝 **Proposed Post Copy:**
---
[Full drafted post body with hook, scenarios, 5-line CTA, and SEO hashtags]
---

🔍 **Pre-Flight Quality Audit:**
- Persona Alignment: [USER_PERSONA]
- Character Count: [X] / 2,500
- AI Banned Words: 0 found (Clean)
- Parentheses Check: 0 found (Clean)
- Mandatory Anchor: #CreateImpact present

👉 **How would you like to proceed?**
- Reply **"approve"** (or tap Approve) to schedule this post to your Buffer LinkedIn queue.
- Reply **"edit: [your feedback]"** to adjust any copy or visual details.
- Reply **"regenerate"** to draft a completely new scenario for Day [X].
```

### Approval Response Handling:
1. **"Approve" / "Yes" / "Queue":** Muse proceeds immediately to Step 9 (Buffer API Queueing) and schedules the post.
2. **"Edit: <feedback>":** Muse applies the user's requested revisions, re-runs the pre-flight checks, and presents the updated draft for confirmation.
3. **"Regenerate" / "Skip":** Muse discards the draft, selects an alternate edge case from the topic matrix, and generates a fresh draft.

---

## 9. Buffer API Publishing & Scheduling Engine

Once the draft has received explicit Human-in-the-Loop approval, Muse pushes the approved copy and visual asset directly into the user's Buffer queue.

### Buffer API Endpoint:
- **Method:** `POST`
- **URL:** `https://api.bufferapp.com/1/updates/create.json`
- **Authentication:** `Authorization: Bearer <BUFFER_ACCESS_TOKEN>`

### Request Payload:
```json
{
  "profile_ids": [
    "<BUFFER_PROFILE_ID>"
  ],
  "text": "<APPROVED_POST_TEXT>",
  "now": false,
  "top": false,
  "media": {
    "photo": "<APPROVED_IMAGE_URL>"
  }
}
```

*Note: If `now: false` and no specific `scheduled_at` timestamp is passed, Buffer automatically slots the update into the user's next configured queue slot for that LinkedIn channel.*

### Publishing Execution Procedure for Muse:
1. **Verify Human Approval:** Ensure an explicit "approve" event was recorded.
2. **Validate Buffer Access:** Test token validity with a quick `GET /1/user.json`.
3. **Retrieve Target Profile:** Confirm `<BUFFER_PROFILE_ID>` matches the designated LinkedIn channel.
4. **Submit Post to Buffer:** Execute the `POST /1/updates/create.json` call.
5. **Log & Report:**
   - Confirm status code `200 OK`.
   - Extract `updates[0].id` and scheduled slot time.
   - Report dispatch confirmation to the user with the exact scheduled time in Buffer.

---

## 10. Muse Autonomous Execution Loop

```
+---------------------------------------------------------------+
|                      MUSE SCHEDULER WAKEUP                    |
+---------------------------------------------------------------+
                               |
                               v
             [ Check Buffer & LinkedIn Connection ]
              /                                   \
       [ Connected? ]                              [ Missing? ]
             |                                          |
             v                                          v
 [ Identify Next Series Index: Day X ]        [ Prompt User with Step-by-Step ]
             |                                [ Buffer Setup Guide & Wait     ]
             v
 [ Determine Mode: Question vs Answer Day ]
             |
             v
 [ Draft Post Copy with Strict Anti-AI Rules ]
             |
             v
 [ Render Visual in User's Selected Theme (Legal Pad / Muji / Blueprint / White) ]
             |
             v
+---------------------------------------------------------------+
|          🛑 MANDATORY HUMAN-IN-THE-LOOP APPROVAL GATE         |
|   Muse presents draft copy + visual image to User in chat     |
+---------------------------------------------------------------+
         /                           |                      \
 [ "Approve" ]             [ "Edit: <notes>" ]       [ "Regenerate" ]
       |                             |                      |
       v                             v                      v
[ Send to Buffer API ]     [ Apply Revisions & ]     [ Pick New Scenario & ]
[ updates/create.json]     [ Re-present Draft  ]     [ Re-draft from Start ]
       |
       v
[ Confirm Queued Time to User ]
```
