# PRD: Harbor RCM — Insurance Verification Agent (ARIA)

## Executive Summary
Harbor RCM is a productized AI agent platform that automates Revenue Cycle Management for small medical practices and behavioral health agencies — practices that enterprise vendors like XY.AI and Thoughtful AI won't serve. Our first agent, ARIA (Automated Revenue & Intake Agent), automates insurance verification: front desk staff spend 12+ minutes per patient on portal logins, payer hold music, and EDI 271 decoding. ARIA does it in 8 seconds. We sell turnkey installs at $5K setup + $1,500-3,500/month, target $30-50K MRR within 12 months from 15-20 small Tulsa-area practices.

## Problem Statement
The U.S. healthcare AI market exceeds $37 billion, but virtually all investment targets large hospital systems. Approximately 190,000 independent practices with 1-10 physicians remain unserved — a $5 billion RCM opportunity. These practices can't afford enterprise vendors ($100M+ revenue requirement at Thoughtful AI), don't have IT teams to integrate XY.AI's Browser Agent, and lose 16-20% of revenue to preventable billing errors driven by manual insurance verification. Adam James runs Safe Harbor (a behavioral health agency) where this pain is felt daily, and has a friend running a primary care office in Tulsa as the first paying customer.

## Target Users
- **Primary buyer:** Small medical practice owners (1-3 physicians, $500K-$5M annual revenue)
- **Secondary buyer:** Behavioral health agency directors (1-3 clinicians)
- **Daily users:** Front desk staff, schedulers, billing coordinators
- **Geography:** Tulsa, OK (Phase 1) → Oklahoma (Phase 2) → Regional (Phase 3)
- **First customer:** Adam's primary care doctor friend in Tulsa
- **Pilot user:** Safe Harbor Behavioral Health (Adam's own agency — Customer Zero)

## Core Features (MVP) — ARIA Only

1. **Single-patient verification (MUST HAVE)** — Enter patient + insurance, get coverage in 8 seconds
2. **Availity sandbox integration (MUST HAVE)** — Demo-safe testing environment
3. **Live Availity production (MUST HAVE)** — Real verifications post-BAA
4. **Dashboard with stats (MUST HAVE)** — Verifications today, success rate, hours saved
5. **Staff alert system (MUST HAVE)** — SMS/email when patient needs attention before arrival
6. **HIPAA audit log (MUST HAVE)** — Every action logged with 7-year retention
7. **EHR write-back (MUST HAVE)** — Dr. Chrono native, others via Keragon
8. **Batch verification (NICE TO HAVE — Phase 2)** — Upload CSV, verify 50 patients overnight
9. **Voice fallback (NICE TO HAVE — Phase 3)** — When portals fail, agent calls payer
10. **Prior auth detection (NICE TO HAVE — leads to PAULA agent)** — Flag patients needing auth

## The 4 Rooms (Workflow Phases)

1. **Room 1 — `1_patient-arrives/`:** Receives appointment data from EHR webhook or batch CSV. Validates fields. Detects duplicates. Forwards clean payload to verification.
2. **Room 2 — `2_check-coverage/`:** The core verification engine. Uses TWO paths:
   - **Path A (Primary) — Availity REST API:** For major payers (UHC, Aetna, BCBS, Medicare, Cigna). Direct API call — no browser, no Skyvern. Fast ($0.003), reliable, preferred for ~80% of patients.
   - **Path B (Fallback) — Skyvern + Workflow-Use:** For payers not on Availity API (SoonerCare, small regional payers). Skyvern replays a Workflow-Use recorded session in a real browser. Slower ($0.10-0.25) but works for any portal. Used for ~20% of patients.
   - Always tries Path A first. Falls back to Path B automatically if the payer has no API.
3. **Room 3 — `3_clean-the-response/`:** Parses messy 271 EDI/JSON into canonical benefits object. Same shape regardless of payer. Flags missing or ambiguous fields.
4. **Room 4 — `4_send-and-log/`:** Writes benefits to EHR. Sends staff alerts for inactive coverage or prior auth needs. Creates HIPAA audit log. Updates dashboard.

## Tech Stack
- **Frontend:** Next.js 14 + TypeScript + Tailwind CSS (client dashboard)
- **Backend:** Python 3.11 (`py` on Windows), AWS Lambda
- **LLM Brain:** Claude Opus 4.7 via AWS Bedrock (one BAA covers everything)
- **Browser Agent:** Skyvern Cloud (free tier → Pro at scale)
- **Workflow Recording:** Workflow-Use (open source, MIT license)
- **Insurance API:** Availity REST API (Demo plan free, Standard plan production)
- **EHR:** Dr. Chrono (default), Keragon bridge for others
- **Database:** DynamoDB (HIPAA-eligible)
- **Auth:** AWS Cognito + IAM
- **Secrets:** AWS Secrets Manager
- **Logging:** CloudWatch Logs (encrypted, 7-year retention)
- **Deployment:** AWS SAM / Terraform (client owns their AWS account)
- **CRM:** GoHighLevel (Adam's existing client portal)

## API/Integration Points

| Service | Direction | Purpose |
|---------|-----------|---------|
| Dr. Chrono API | Read + Write | Pull appointments, write back benefits |
| Availity REST API | Outbound | 270 eligibility request, receive 271 |
| Skyvern Cloud API | Outbound | Browser automation when no API exists |
| AWS Bedrock | Outbound | Claude inference for ambiguous parsing |
| AWS Secrets Manager | Read | Portal credentials per client per payer |
| Twilio / AWS SNS | Outbound | SMS alerts to front desk |
| GoHighLevel API | Outbound | Update Adam's client pipeline status |

## Development Roadmap

**Phase 1 (Month 1) — Land First Customer:**
- Build live ARIA single-patient verification
- Test on Safe Harbor (Customer Zero)
- Demo at doctor friend's office
- Sign first deal at $2,500 setup + $500/month
- Document install playbook

**Phase 2 (Months 2-3) — Add 3-5 More Clients:**
- Add batch verification mode
- Polish dashboard
- Build referral system
- Hit $5K MRR

**Phase 3 (Months 4-6) — Scale Deployment:**
- Build PAULA (Prior Auth) — only if 2+ clients ask
- Add Aetna, BCBS, Cigna direct portal scrapes
- Launch case study marketing
- Hit $15K MRR

**Phase 4 (Months 7-12) — Full RCM Suite:**
- Build EVA (Claims), DAN (Denials), CODY (Coding) as customers demand
- Multi-state expansion
- Hit $30-50K MRR

## Potential Challenges

| Risk | Mitigation |
|------|------------|
| Skyvern free tier limits hit early | Plan upgrade path; use Availity API first to minimize Skyvern usage |
| Doctor friend's Availity not set up | Sign her up as part of install; included in $2,500 setup |
| HIPAA audit | Architecture is HIPAA-eligible from day 1; client owns their AWS BAA |
| 2FA breaks Skyvern flows | Use TOTP secret in AWS Secrets Manager, Skyvern handles natively |
| EHR write failures | Idempotency keys + retry queue; never lose a verification |
| Payer portal changes | Workflow-Use re-records in 5 minutes; vision-based agents self-heal |
| Customer churn | White-glove onboarding + weekly check-ins for first 90 days |

## Success Metrics

**Technical:**
- 95%+ verification success rate per payer
- < 12 second average verification time
- < 0.1% false positive rate on "active coverage"
- 100% HIPAA audit log coverage

**Business:**
- Month 1: 1 paying customer ($500 MRR)
- Month 3: 5 paying customers ($2,500 MRR)
- Month 6: 10 paying customers ($15,000 MRR)
- Month 12: 15-20 customers ($30,000-50,000 MRR)
- Customer LTV > $30,000 (24-month average retention)
- Gross margin > 80%

## Acceptance Criteria (MVP)

- ✅ ARIA verifies a sandbox patient end-to-end in under 12 seconds
- ✅ ARIA verifies a live patient (post-BAA) end-to-end in under 12 seconds
- ✅ Dashboard shows verifications, success rate, hours saved
- ✅ Staff receive alerts for inactive/prior auth/data quality issues
- ✅ HIPAA audit log records every action with required fields
- ✅ EHR write-back works for Dr. Chrono
- ✅ One full install playbook documented (the doctor friend's install)
- ✅ One signed customer paying $500+/month for 30+ days
- ✅ One video testimonial from the customer
