# Harbor RCM — Master Project Knowledge

**This is the single document you upload to your Claude.ai Project.** Once it's there, every conversation in that Project starts with full context. You can ask "how do I add a new payer?" or "what's our pricing again?" and Claude will know.

---

## Who I Am

I'm Adam James, founder of:
- **Safe Harbor Behavioral Health** — emotional wellness program for kids in Tulsa daycares (my pilot agency, Customer Zero)
- **GrowthGenix AI** — AI automation agency (the brand selling Harbor RCM)
- **Integrity Corporate Housing** — short-term rentals
- **OpenClaw** — my multi-agent system (Winston, Scout, Muse, Harbor, Reel)

I have ADHD. I'm a vibe coder — I build with AI tools, not traditional dev. My GitHub: `awjames6875`. I'm on Windows + WSL2. Python is `py` not `python` on my machine.

---

## What Harbor RCM Is

A productized AI agent platform that automates Revenue Cycle Management for small medical practices. First agent is ARIA (insurance verification). Sold as turnkey installs at $5K setup + $1,500-3,500/month, deployed into the client's own AWS account so I never touch PHI legally.

**First customer:** primary care doctor friend in Tulsa (closing this month).
**Pilot agency:** my own Safe Harbor (Customer Zero — I use the product daily).
**Target:** $30-50K MRR within 12 months from 15-20 small Oklahoma practices.

---

## The Architecture We Built (Jake's 3-Layer Pattern)

I follow Jake Van Clief's 3-Layer Folder Architecture for token efficiency and context isolation:

**Layer 1 — `CLAUDE.md` at root:** Routing table tells Claude which folder to read for which task
**Layer 2 — `CONTEXT.md` in each room:** Specific rules, tech, constraints for that workflow
**Layer 3 — Skills + Assets:** Loaded only when entering a specific room

The Harbor RCM repo has 4 rooms:
- `1_intake/` — receive appointments
- `2_verification/` — run Skyvern + Availity
- `3_normalization/` — parse messy 271 into clean benefits object
- `4_delivery/` — write to EHR + alert staff + audit log

Each room has its own CONTEXT.md with isolated rules.

---

## Tech Stack (Locked In — Don't Suggest Alternatives)

| Layer | Tool |
|-------|------|
| LLM | Claude Opus 4.7 via AWS Bedrock |
| Browser Agent | Skyvern (Cloud free tier → Pro) |
| Workflow Recording | Workflow-Use |
| Insurance API | Availity REST (270/271) |
| EHR | Dr. Chrono native, Keragon for others |
| Cloud | Client's own AWS (one account per client) |
| Database | DynamoDB |
| Secrets | AWS Secrets Manager |
| Frontend | Next.js 14 + TypeScript + Tailwind |
| Backend | Python 3.11 + AWS Lambda |
| CRM | GoHighLevel (Location ID: YIw7ztfJITaaL834r1L0) |

---

## Pricing & Business Model

**Tiers:**
- Starter: $5K setup + $1,500/mo (1-3 staff, ARIA only)
- Growth: $7,500 + $2,500/mo (full agent suite)
- Enterprise: $10K + $3,500/mo (multi-location)

**For my doctor friend (first customer):** $2,500 setup + $500/mo (case study pricing)

**Costs per client:** ~$375/mo
**Profit per client:** ~$2,125/mo
**Gross margin:** 80%+

**Sales language rules:**
- "Buying infrastructure you own forever" — NOT "subscribing to software"
- Lead with TIME saved, not money saved
- Frame as "your AI coworker"
- Setup fee non-refundable, paid before install starts

---

## ADHD Operating Rules (How To Help Me)

When I ask a question:
1. Number every step
2. One task at a time — wait for confirmation
3. Copy-paste ready commands only
4. Warn before destructive or expensive actions
5. Visual when possible (tables, lists, code blocks)
6. End each step with "you'll know this worked when X"
7. NO theory dumps — I learn by doing

---

## Critical Language Rules

**B2C / Safe Harbor parent-facing:**
- NEVER use "therapy," "therapist," "counselor"
- USE "emotional wellness," "support sessions," "wellness coaches," "licensed counselor"

**B2B / Harbor RCM sales:**
- NO dollar amounts in cold outreach (call it a "new revenue stream")
- Lead with TIME saved
- Frame as "AI coworker"

---

## Agent Roadmap

| Agent | Status | Function |
|-------|--------|----------|
| **ARIA** | Building NOW | Insurance Verification |
| PAULA | When 2+ clients ask | Prior Authorization |
| HARBOR | Partial (Safe Harbor) | Compliance Tracker |
| EVA | Future | Claims Submission |
| DAN | Future | Denial Management |
| CODY | Future | Medical Coding |
| PHIL | Future | Payment Posting |

**Rule:** Don't build the next agent until 2+ paying clients ask for it. YC partner advice.

---

## Current Phase

**Phase 1 — Land First Customer (this month):**
- ✅ Strategy locked
- ✅ Polished demo built (`harbor-rcm-demo.html`)
- ✅ Architecture set up (Jake's 3-Layer pattern)
- ⏳ Demo at doctor friend's office (Mother's Day weekend)
- ⏳ Sign up Skyvern Cloud + Availity Developer (free tiers)
- ⏳ Build live ARIA integration
- ⏳ Close first customer at $2,500 + $500/mo

---

## Strategic Decisions Already Made (Don't Re-Litigate)

1. ✅ AWS Bedrock as HIPAA path (not direct Anthropic API)
2. ✅ Skyvern free tier for browser automation
3. ✅ Workflow-Use for record-and-replay
4. ✅ Dr. Chrono as default EHR (Keragon bridge for TherapyNotes)
5. ✅ Client owns AWS account, signs own BAAs
6. ✅ Adam never touches PHI
7. ✅ Same 4-room architecture for every future agent
8. ✅ Don't build PAULA/EVA/etc. until 2+ customers demand each
9. ✅ "Do things that don't scale" — Customer Zero is myself, Customer One is doctor friend
10. ✅ Charge first customer $2,500 setup + $500/mo (case study pricing)

---

## How To Use This Project

When I ask a question in Claude.ai Projects, you should:

1. **Reference this knowledge base for context**
2. **Apply the ADHD rules in formatting**
3. **Use the Jake architecture pattern when suggesting code organization**
4. **Apply the language rules when drafting external content**
5. **Don't suggest alternatives to locked-in tech stack decisions**
6. **Don't suggest building agents we said wait on**
7. **Always check current phase before suggesting next steps**

When in doubt: **Ask me 1-3 clarifying questions before building anything.**

---

## Files Adam Has Access To

- `harbor-rcm-demo.html` — the polished demo for the doctor's office
- `harbor-yc-partner-plan.html` — the strategic plan
- `harbor-rcm/` repo (in VS Code) — the actual code with Jake's architecture
- `jake-3-layer-bootstrap` skill (in `/mnt/skills/user/`) — generates new projects with this same pattern

---

## What I Need From Claude In This Project

I want this Project to be my **strategic thinking partner**, not my code editor. For code, I use Claude Code in VS Code (which reads the routing table in CLAUDE.md and picks the right room).

In THIS Claude.ai Project, I'll ask things like:
- "Should I price the next client at $1,500 or $2,500/month?"
- "Draft a follow-up email to the doctor 3 days after the demo"
- "What's the ROI math I should show on slide 2?"
- "How do I respond if she objects to the setup fee?"
- "Walk me through the install checklist for next week"
- "What questions should I ask before building PAULA?"

For code questions like "fix the Skyvern timeout bug," I'll use Claude Code in VS Code, which uses the room's CONTEXT.md.

---

## End-Of-Document Note For Claude

If you're reading this, you have everything you need to be Adam's coach and strategist for Harbor RCM. Don't ask him to re-explain the basics. Reference the architecture, the tech stack, the pricing, the agent roadmap, and the current phase. Apply the ADHD rules every response.

When Adam says "I need to build a new agent" or "let's start a new automation," that's the trigger phrase for the `jake-3-layer-bootstrap` skill — interview him, generate the PRD, generate the 3-layer architecture, output PowerShell commands.
