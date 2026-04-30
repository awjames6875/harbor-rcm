# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

---

# CLAUDE.md — Harbor RCM Master Router

## Identity
You are helping Adam James build **Harbor RCM** — an AI-powered insurance verification platform that automates eligibility checks for small medical practices and behavioral health agencies. First customer: a primary care doctor friend in Tulsa. Pilot agency: Adam's own Safe Harbor Behavioral Health.

Adam has ADHD. ALWAYS:
- Number every step
- One task at a time
- Copy-paste ready commands only
- Warn before destructive or expensive actions
- Visual when possible (tables, lists, code blocks)
- Confirm what good looks like at each step

## Codebase State (as of 2026-04-30)

This repo is **pre-implementation** — architecture and documentation only. Each room (`1_intake/`, `2_verification/`, `3_normalization/`, `4_delivery/`) currently contains:
- A `CONTEXT.md` with the room's purpose, process, tech stack, constraints, and data-shape contract — **read this first when entering a room**
- Empty `code/`, `skills/`, `tests/` directories (stub `README.md` only)

There is no `package.json`, `pyproject.toml`, `requirements.txt`, lockfile, CI config, or test runner yet. Do not search for build/lint/test commands — they will be added when implementation starts. When you write the first code in a room, also create the matching `requirements.txt` / `pytest` config in that room's folder.

The `skills/*.md` files referenced in each room's `CONTEXT.md` (e.g. `skills/skyvern-workflows.md`) **do not exist yet** — they are planned Layer 3 assets. If asked to use one, create it; don't search for it.

## Routing Table (Jake's Pattern — How To Find The Right Room)

| Task | Go to | Read |
| ------ | ------ | ------ |
| Receive new patient appointment | /1_intake | CONTEXT.md |
| Run insurance verification | /2_verification | CONTEXT.md |
| Parse messy 271 response | /3_normalization | CONTEXT.md |
| Write results back to EHR | /4_delivery | CONTEXT.md |
| Add a new payer integration | /2_verification | CONTEXT.md, then docs/PRD.md |
| Fix a verification bug | Read the relevant room's CONTEXT.md FIRST |
| Add a new agent (PAULA, EVA, etc.) | /docs | PRD.md, then duplicate ARIA pattern |
| Update pricing or business model | /docs | PRD.md |

## Where Things Live

| File | Audience | When to read |
|------|----------|--------------|
| `CLAUDE.md` (this file) | Claude Code | Always — auto-loaded |
| `<room>/CONTEXT.md` | Claude Code | When entering that room (per routing table) |
| `docs/PRD.md` | Claude Code | When adding payers, agents, or major features |
| `PROJECT_KNOWLEDGE.md` | **Claude.ai Projects only** (web app) | Strategy/sales conversations — **not** for code work |
| `README.md` | Humans | Onboarding new contributors |

## Architecture: The 4-Room Pipeline

ARIA is a linear data pipeline. Each room is a Lambda-style transform that consumes a structured payload from the previous room and emits one to the next. **Each room's `CONTEXT.md` defines its output JSON shape — that shape is the contract with the downstream room. Never change a shape without updating the consumer.**

```
EHR webhook / CSV
        │
        ▼
┌──────────────────┐    patient + payer payload
│ 1_intake         │    (validated, deduplicated)
│ Lambda + Pydantic│────────────────────┐
└──────────────────┘                    ▼
                              ┌──────────────────┐    raw 271 + screenshots
                              │ 2_verification   │    (Availity API or
                              │ Skyvern + Availity│   Skyvern portal scrape)
                              └──────────────────┘────────────────┐
                                                                  ▼
                                                        ┌──────────────────┐    canonical benefits
                                                        │ 3_normalization  │    object (payer-agnostic,
                                                        │ Python + Pydantic│    schema-versioned)
                                                        └──────────────────┘──────┐
                                                                                  ▼
                                                                        ┌──────────────────┐
                                                                        │ 4_delivery       │
                                                                        │ EHR + alerts +   │
                                                                        │ HIPAA audit log  │
                                                                        └──────────────────┘
```

**Key invariants:**
- `2_verification` tries the Availity API first (cheap, fast); only falls back to Skyvern portal scraping when no API exists for that payer.
- `3_normalization` outputs the same canonical schema regardless of input payer — this is the source of truth. One normalizer function per payer.
- `4_delivery` writes the audit log **before** writing to the EHR (audit even on EHR failure).
- PHI never leaves the client's AWS account. Adam never touches PHI.

For the exact JSON shape of each handoff, see the `## Data Shape` section in the destination room's `CONTEXT.md`.

## Platform & Commands

- **Shell:** Windows 11. Bash is available (Git Bash); PowerShell is also available. Prefer bash syntax in examples for portability.
- **Python launcher:** Use `py` (the Windows launcher) — `python` is not on PATH on Adam's machine. Example: `py -m pytest tests/`, `py -m venv .venv`.
- **No project-wide commands yet** (see "Codebase State" above). When implementation starts, the convention is one `requirements.txt` and `pytest` config per room.
- **Adam's other tools:** Antigravity IDE (primary), VS Code (secondary), Claude Code terminal.

## File Naming Conventions
- Documentation: `YYYY-MM-DD-topic.md` (e.g., `2026-04-30-availity-integration.md`)
- Code files: `snake_case.py`
- Test data: `data/test-[scenario].json`
- Skyvern workflows: `workflows/[payer]-[action].json`
- Patient data (TEST ONLY): `data/test-patients/[name].json`

## Critical Rules (Apply Everywhere)
1. **Never commit secrets.** Use `.env.local` (gitignored). Production secrets go in AWS Secrets Manager.
2. **Never process real PHI without a signed BAA.** Sandbox data only during development.
3. **Always update the relevant room's CONTEXT.md when behavior changes.**
4. **Never bleed context between rooms.** If you're in /2_verification, don't reference /3_normalization rules.
5. **Ask 3-4 clarifying questions before building anything new.**
6. **Every agent action must be logged.** HIPAA audit trail: timestamp + user + action + outcome.
7. **Sandbox → Staging → Production.** Never skip steps.
8. **One client = one AWS account.** Never multi-tenant. Each install is isolated.

## Tech Stack (Locked In — Don't Suggest Alternatives)

| Layer | Tool | Why |
|-------|------|-----|
| LLM Brain | Claude via AWS Bedrock | One BAA covers everything |
| Browser Agent | Skyvern (open source) | Vision-based, self-heals |
| Workflow Recording | Workflow-Use | Record-once, replay-forever |
| Insurance API | Availity REST API | Standard 270/271 transactions |
| EHR Bridge | Keragon (when needed) | Auto-BAA, 300+ integrations |
| Cloud Hosting | Client's own AWS | Adam never touches PHI |
| Database | DynamoDB | HIPAA-eligible on AWS |
| CRM | GoHighLevel | Adam's existing client portal |

## Business Context

**Harbor RCM is sold as a turnkey AI service:**
- Starter: $5K setup + $1,500/month (1-3 staff, ARIA only)
- Growth: $7,500 setup + $2,500/month (full agent suite)
- Enterprise: $10K setup + $3,500/month (multi-location)
- Costs per client: ~$375/month
- Profit per client: ~$2,125/month
- 12-month target: 15-20 clients = $30-50K MRR

**Sales language rules:**
- "Buying infrastructure you own forever" — NOT "subscribing to software"
- Lead with TIME saved, not money saved
- Frame as "your AI coworker" — NOT "automation tool"
- Setup fee is 100% non-refundable, paid before install starts

**Architecture pattern (every agent follows this):**
- Same 4-room structure (intake → verification/processing → normalization → delivery)
- Agents are sibling folders: `aria/`, `paula/` (future), `cam/` (future)
- Each agent has its own routing table inside its folder

## Agent Roadmap

| Agent | Status | Function |
|-------|--------|----------|
| **ARIA** | Building NOW | Insurance Verification (this project) |
| PAULA | Future (only when 2+ clients ask) | Prior Authorization |
| HARBOR | Partial (Safe Harbor) | Compliance Tracker |
| EVA | Future | Claims Submission |
| DAN | Future | Denial Management |
| CODY | Future | Medical Coding |
| PHIL | Future | Payment Posting |

**Rule:** Don't build the next agent until 2+ paying clients ask for it. YC partner advice: "Do things that don't scale."

## Current Phase

**Phase 1 — Land First Customer (this month)**
- ✅ Strategy locked
- ✅ Polished demo built (`harbor-rcm-demo.html`)
- ✅ Tech stack decided
- ✅ Architecture set up (Jake's 3-Layer pattern)
- ⏳ Demo at friend's primary care office (Mother's Day weekend)
- ⏳ Sign up Skyvern Cloud + Availity Developer (free tiers)
- ⏳ Build live ARIA integration
- ⏳ Close first customer at $2,500 setup + $500/mo
- ⏳ Document install playbook


<claude-mem-context>
# Recent Activity

<!-- This section is auto-generated by claude-mem. Edit content outside the tags. -->

*No recent activity*
</claude-mem-context>