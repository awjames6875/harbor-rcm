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

This repo is **pre-implementation** — architecture and documentation only. Each room currently contains a `CONTEXT.md` and empty `code/`, `skills/`, `tests/` stubs.

**Exception: `2_check-coverage/` is the most active room.** Its `CONTEXT.md` lists the planned Python files:
- `availity_client.py` — 270/271 Availity REST API calls
- `skyvern_runner.py` — Skyvern browser automation fallback
- `verification_handler.py` — orchestrator (tries Path A first, falls back to Path B)
- `workflow_swapper.py` — self-healing: auto-replaces a broken Skyvern recording with a new one
- `payer_router.py` — maps payers to their path (API or Skyvern) and workflow JSON

The `2_check-coverage/workflows/` folder exists for Skyvern workflow JSONs; `workflows/archive/` stores superseded recordings with timestamps.

There is no `package.json`, `pyproject.toml`, `requirements.txt`, lockfile, CI config, or test runner yet. When you write the first code in a room, create the matching `requirements.txt` / `pytest` config in that room's folder.

The `skills/*.md` files referenced in each room's `CONTEXT.md` **do not exist yet** — they are planned Layer 3 assets. If asked to use one, create it; don't search for it.

## Routing Table (Jake's Pattern — How To Find The Right Room)

| Task | Go to | Read |
| ------ | ------ | ------ |
| Receive new patient appointment | /1_patient-arrives | CONTEXT.md |
| Run insurance verification | /2_check-coverage | CONTEXT.md |
| Parse messy 271 response | /3_clean-the-response | CONTEXT.md |
| Write results back to EHR | /4_send-and-log | CONTEXT.md |
| Add a new payer integration | /2_check-coverage | CONTEXT.md, then docs/PRD.md |
| Fix a verification bug | Read the relevant room's CONTEXT.md FIRST |
| Add a new agent (PAULA, EVA, etc.) | /docs | PRD.md, then duplicate ARIA pattern |
| Update pricing or business model | /docs | PRD.md |

## Where Things Live

| File | Audience | When to read |
|------|----------|--------------|
| `CLAUDE.md` (this file) | Claude Code | Always — auto-loaded |
| `<room>/CONTEXT.md` | Claude Code | When entering that room (per routing table) |
| `docs/PRD.md` | Claude Code | When adding payers, agents, or major features |
| `docs/XY-AI-Reverse-Engineering-Report.md` | Claude Code | Build priority order (Part 6) + competitor feature map |
| `PROJECT_KNOWLEDGE.md` | **Claude.ai Projects only** (web app) | Strategy/sales conversations — **not** for code work |
| `README.md` | Humans | Onboarding new contributors |

## Architecture: The 4-Room Pipeline

ARIA is a linear data pipeline. Each room is a Lambda-style transform that consumes a structured payload from the previous room and emits one to the next. **Each room's `CONTEXT.md` defines its output JSON shape — that shape is the contract with the downstream room. Never change a shape without updating the consumer.**

```
EHR webhook / CSV
        │
        ▼
┌──────────────────────┐    patient + payer payload
│ 1_patient-arrives    │    (validated, deduplicated)
│ Lambda + Pydantic    │────────────────────┐
└──────────────────────┘                    ▼
                              ┌──────────────────────┐    raw 271 + screenshots
                              │ 2_check-coverage     │    (Availity API or
                              │ Skyvern + Availity   │    Skyvern portal scrape)
                              └──────────────────────┘────────────────┐
                                                                      ▼
                                                        ┌──────────────────────┐    canonical benefits
                                                        │ 3_clean-the-response │    object (payer-agnostic,
                                                        │ Python + Pydantic    │    schema-versioned)
                                                        └──────────────────────┘──────┐
                                                                                      ▼
                                                                        ┌──────────────────────┐
                                                                        │ 4_send-and-log       │
                                                                        │ EHR + alerts +       │
                                                                        │ HIPAA audit log      │
                                                                        └──────────────────────┘
```

**Key invariants:**
- `2_check-coverage` tries the Availity API first (cheap, fast); only falls back to Skyvern when no API exists for that payer.
- `3_clean-the-response` outputs the same canonical schema regardless of input payer. One normalizer function per payer.
- `4_send-and-log` writes the audit log **before** writing to the EHR (audit even on EHR failure).
- `workflow_swapper.py` is the self-healing layer — when a Skyvern recording breaks, it triggers a re-record and archives the old one. Never edit workflow JSONs directly.
- PHI never leaves the client's AWS account. Adam never touches PHI.

For the exact JSON shape of each handoff, see the `## Data Shape` section in the destination room's `CONTEXT.md`.

## Platform & Commands

- **Shell:** Windows 11. Bash is available (Git Bash); PowerShell also available. Prefer bash syntax in examples.
- **Python launcher:** Use `py` — `python` is not on PATH on Adam's machine. Example: `py -m pytest tests/`, `py -m venv .venv`.
- **No project-wide commands yet** (see Codebase State above). Convention: one `requirements.txt` + `pytest` config per room.

## File Naming Conventions
- Documentation: `YYYY-MM-DD-topic.md` (e.g., `2026-04-30-availity-integration.md`)
- Code files: `snake_case.py`
- Test data: `data/test-[scenario].json`
- Skyvern workflows: `2_check-coverage/workflows/[payer]-[action].json` (archived versions in `workflows/archive/`)
- Patient data (TEST ONLY): `data/test-patients/[name].json`

## Critical Rules (Apply Everywhere)
1. **Never commit secrets.** Use `.env.local` (gitignored). Production secrets go in AWS Secrets Manager.
2. **Never process real PHI without a signed BAA.** Sandbox data only during development.
3. **Always update the relevant room's CONTEXT.md when behavior changes.**
4. **Never bleed context between rooms.** If you're in /2_check-coverage, don't reference /3_clean-the-response rules.
5. **Ask 3-4 clarifying questions before building anything new.**
6. **Every agent action must be logged.** HIPAA audit trail: timestamp + user + action + outcome.
7. **Sandbox → Staging → Production.** Never skip steps.
8. **One client = one AWS account.** Never multi-tenant. Each install is isolated.

## Adversarial Review Rule
Before writing code that touches PHI (any code under /2_check-coverage, /3_clean-the-response, or /4_send-and-log), the workflow is:
1. Claude Code drafts the plan in plan mode.
2. Run `/codex adversarial-review` scoped to the relevant room (e.g. `/codex adversarial-review 2_check-coverage/`).
3. Apply Codex's feedback to the plan.
4. Only then write code.

For non-PHI work (demo HTML, sales copy, marketing pages), skip Codex — Claude is better at those and Codex's feedback won't match the sales voice.

**Also run `/codex rescue --background` before each milestone:** before the demo at the doctor's office, before the first install, before deploying to a new client AWS account. Have it look for hardcoded credentials, missing audit-log entries, PHI in CloudWatch logs, and over-broad IAM policies.

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

## Verification Path Logic (Critical — Read Before Touching 2_check-coverage)

ARIA uses TWO paths to verify insurance. Always try Path A first.
Path B is the fallback ONLY when Path A is not available.

```
Patient verification request arrives
          ↓
Is this payer on Availity API? (UHC, Aetna, BCBS, Medicare, Cigna)
          ↓
    YES → Path A: Availity REST API
          Cost: ~$0.003 per verification
          Speed: 3 seconds
          How: Python code calls Availity directly — no browser, no Skyvern
          ↓
    NO → Path B: Skyvern + Workflow-Use
          Cost: ~$0.10-0.25 per verification
          Speed: 8-12 seconds
          How: Skyvern replays recorded workflow in a real browser
```

**Path A — Availity API (Primary):**
Direct API call. No browser. No Skyvern. Just Python talking to Availity servers.
Use for: UnitedHealthcare, Aetna, BCBS, Medicare, Cigna (80% of patients)

**Path B — Skyvern + Workflow-Use (Fallback):**
Skyvern opens a real browser and replays a recorded workflow.
Workflow-Use is used ONCE to record the portal session at the client's office.
Skyvern replays that recording for every future patient.
Use for: SoonerCare, small regional payers, any payer NOT on Availity API (20% of patients)

**Payer Path Reference:**
| Payer | Path | Cost |
|-------|------|------|
| UnitedHealthcare | API | $0.003 |
| Aetna | API | $0.003 |
| BCBS | API | $0.003 |
| Medicare | API | $0.003 |
| Cigna | API | $0.003 |
| SoonerCare (Oklahoma Medicaid) | Skyvern | $0.10-0.25 |
| Small regional payers | Skyvern | $0.10-0.25 |

**Rule:** Never use Skyvern for a payer that has an Availity API connection.
It costs 50x more and is slower. API first. Always.

---

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
- Same 4-room structure (patient-arrives → check-coverage → clean-the-response → send-and-log)
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

---

## Confidence Scoring Thresholds (XY.ai Intelligence — Apply Everywhere)

Every verification result that passes through Room 3 (clean-the-response) gets a confidence score before it reaches Room 4 (send-and-log). These thresholds are non-negotiable and apply across all rooms:

- Above 95%: AUTO-PUSH directly to EHR. No human review needed. Staff gets a success notification.
- Between 80% and 95%: HUMAN REVIEW QUEUE. Result appears in the review dashboard with uncertain fields highlighted in yellow. Staff edits and clicks Push to EHR.
- Below 80%: STAFF ALERT. Result does NOT go to EHR. Staff gets an actionable SMS/email explaining exactly what went wrong and what to do.

Confidence is scored on three dimensions inside confidence_scorer.py:
- Field completeness (40% weight): did all canonical fields return non-null values
- Value plausibility (30% weight): are numeric values within realistic ranges for this payer
- Payer pattern match (30% weight): does this response format match historical patterns in DynamoDB

Never hardcode thresholds. Store them in a per-client config so practices can adjust.

---

## Self-Healing Workflow Swapper (XY.ai Intelligence — Room 2 Critical Feature)

When a payer portal changes its UI, ARIA does not break permanently. Instead:
1. The broken Skyvern task logs a failure and alerts staff
2. Staff records the new portal process once using Workflow-Use Chrome extension
3. workflow_swapper.py detects which payer the new recording belongs to by matching the URL
4. It archives the old recording to 2_check-coverage/workflows/archive/ with a timestamp suffix
5. It deploys the new recording as the active workflow for that payer
6. The next verification for that payer uses the new recording automatically

Never edit workflow JSON files directly. Always go through workflow_swapper.py so the archive and deployment are tracked and reversible. This is the same capability XY.ai charges $5,000 per month for. Harbor RCM builds it into the platform.

---

## Competitive Context (XY.ai)

XY.ai is the primary competitor. $3.5M seed funded, 13-14 customers, one year in production. They charge $2,500-$5,000 per agent per month with browser-only automation and no direct Availity API path. Their three production-ready features are browser automation, OCR data extraction with confidence scoring, and a workflow queue dashboard.

Harbor RCM structural advantage: Availity API at $0.003 per verification vs XY browser-only. That is 50x cheaper and 3x faster for the 80% of patients on major commercial payers.

Full competitive intelligence is in docs/XY-AI-Reverse-Engineering-Report.md. Read Part 6 for build priority order and Part 7 for the dashboard UI spec based on actual XY platform screenshots.

---

## When To Build These Features

This section exists because Adam will not always remember what has been designed. When a situation below arises during development, read the corresponding note and build the referenced file.

TRIGGER: You just closed the first client and are setting up their AWS account.
BUILD: 1_patient-arrives/code/history_ingester.py
WHY: Trains ARIA on twelve months of client historical data before any live patient is processed. Without it ARIA starts blind. See docs/training-protocol.md before running this file.

TRIGGER: Something broke in production and you are staring at a CloudWatch error.
BUILD: 4_send-and-log/code/incident_manager.py
WHY: ARIA self-healing immune system. Watches CloudWatch, uses Claude via Bedrock to diagnose errors in plain English, attempts automatic fixes for known problems like expired tokens and timed-out Skyvern tasks, and writes every incident to DynamoDB permanently. See the incident_manager.py spec at the bottom of 4_send-and-log/CONTEXT.md.

TRIGGER: Staff are correcting the same field repeatedly for the same payer.
ENHANCE: 3_clean-the-response/code/learning_engine.py
WHY: Repeated corrections mean the learning engine has not generated a parsing rule for that pattern yet. Pull correction logs from DynamoDB for that client and payer, identify the pattern, and update the payer profile so ARIA handles it automatically going forward.

TRIGGER: You have three or more clients live and support is taking more than two hours per week.
BUILD: Multi-client monitoring dashboard aggregating CloudWatch from all client AWS accounts.
WHY: Watching three separate AWS consoles is unsustainable. Do not build this before three clients.

TRIGGER: A portal stopped working after an insurance company redesigned their website.
USE: 2_check-coverage/code/workflow_swapper.py
WHY: Sit with staff for fifteen minutes, record the new process with Workflow-Use, drop the new JSON into the workflows folder. Should take thirty minutes from alert to resolution.

TRIGGER: Preparing for a demo or new client install.
RUN: codex adversarial-review scoped to the relevant room.
WHY: Catches hardcoded credentials, missing audit logs, PHI leaking into CloudWatch, and overly broad IAM permissions. Run before every demo and every new client install.

TRIGGER: A prospect asks how ARIA gets smarter over time.
EXPLAIN: Three-stage self-improvement loop. Stage one is the historical baseline from history_ingester.py at onboarding. Stage two is the confidence scorer anchoring every live verification against that baseline. Stage three is the learning engine logging every human correction and generating updated parsing rules. After six months ARIA knows the practice as well as an experienced billing specialist who has worked there for six months.

TRIGGER: Building something new and not sure which room it belongs in.
RULE: Receives or validates incoming data belongs in 1_patient-arrives. Executes a verification belongs in 2_check-coverage. Parses scores or learns from results belongs in 3_clean-the-response. Writes to EHR alerts staff or logs to CloudWatch belongs in 4_send-and-log. If it fits none of these four rooms question whether it belongs in ARIA at all or whether it is the beginning of a new agent like PAULA or EVA.
## Availity Reference
Before writing or editing any Availity code, read AVAILITY_API_DOCS.md.
Never guess at field names, endpoints, or payload structure.
The most common mistakes are documented at the bottom of that file.