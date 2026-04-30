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

## File Naming Conventions
- Documentation: `YYYY-MM-DD-topic.md` (e.g., `2026-04-30-availity-integration.md`)
- Code files: `snake_case.py` (Python is `py` on Windows, not `python`)
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

## Verification Path Logic (Critical — Read Before Touching 2_verification)

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
