# CONTEXT.md — Room 2: Verification

## Purpose
Take validated patient data from /1_intake, log into the right payer portal via Skyvern, run the eligibility check, and capture the raw 271 response.

## The Two Paths (Read This First)

ARIA uses two paths to verify insurance. Path A is ALWAYS tried first.

```
Payer on Availity API? (UHC, Aetna, BCBS, Medicare, Cigna)
    YES → Path A: Availity REST API (fast, cheap, no browser)
    NO  → Path B: Skyvern portal scrape (slower, costs more, works for any payer)
```

**Path A — Availity API (~80% of verifications)**
- Python code sends a 270 request directly to Availity
- Availity returns a 271 response
- No browser opened. No Skyvern. No Workflow-Use.
- Cost: ~$0.003 per verification
- Speed: 3 seconds

**Path B — Skyvern + Workflow-Use (~20% of verifications)**
- Skyvern opens a real Chrome browser
- Replays the Workflow-Use recorded session from this payer
- Extracts coverage data from the screen
- Cost: ~$0.10-0.25 per verification
- Speed: 8-12 seconds

**Workflow-Use role:** Used ONCE per client per payer to record the portal session.
That recording lives in `2_verification/workflows/[payer]-workflow.json`.
Skyvern replays it forever. Never record again unless the portal layout changes.

---

## The Process (Step by Step)
1. Receive structured patient payload from /1_intake
2. Look up which portal handles this payer (Availity, Waystar, payer-direct)
3. Retrieve portal credentials from AWS Secrets Manager (never hardcoded)
4. Launch Skyvern session with the right workflow JSON for this payer
5. Skyvern logs into portal (handles 2FA via stored secret)
6. Skyvern navigates to eligibility check page
7. Skyvern enters patient data
8. Skyvern submits and waits for response
9. Capture raw 271 response (or screenshot if no API)
10. Forward raw response to /3_normalization
11. If failure → retry once with backoff, then escalate to human queue

## Identity & Audience
- Who uses this room: Skyvern agent, AWS Lambda orchestrator
- Tone of voice: N/A (machine-to-machine)
- What "good" looks like here: 95%+ success rate per payer. Average completion under 12 seconds. Failed runs include diagnostic screenshot.

## Tech Stack For This Room
- **Skyvern** (Cloud free tier → Pro when scaling) — vision-based browser automation
- **AWS Lambda** — orchestration
- **AWS Secrets Manager** — portal credentials (one secret per client per payer)
- **Workflow-Use** — record-once-replay-forever workflow JSONs
- **Availity REST API** — primary path for X12 270/271
- **Boto3 (Python)** — AWS SDK

## Patterns to Follow
- Try API first (fastest), fall back to portal scraping (slower but more reliable)
- Always capture screenshots on failure (for debugging)
- Use exponential backoff on retries (1s → 2s → 4s)
- Log every Skyvern step with timestamps for HIPAA audit trail
- One Skyvern workflow JSON per payer (Availity, Waystar, etc.)

## Never Do This (Constraints)
- NEVER store portal credentials in code or .env files (use Secrets Manager only)
- NEVER scrape Availity if the API works — API is faster and more reliable
- NEVER process more than 5 patients in parallel per Skyvern session (rate limits)
- NEVER skip the screenshot capture on failure (you'll regret it during debugging)
- NEVER bypass 2FA by sharing TOTP codes via insecure channels

## Skills To Load (Layer 3)
When working in this room, also load:
- `skills/skyvern-workflows.md` — how to write/record workflows
- `skills/availity-api.md` — REST API patterns for 270/271
- `skills/aws-secrets.md` — credential retrieval patterns
- `skills/payer-portal-quirks.md` — known weird behaviors per payer

## Data Shape (What This Room Outputs to /3_normalization)

```json
{
  "patient_id": "hash_abc123",
  "appointment_id": "appt_xyz789",
  "verification_attempt": {
    "started_at": "2026-04-30T03:15:22Z",
    "completed_at": "2026-04-30T03:15:31Z",
    "duration_seconds": 9.2,
    "method": "availity_api",
    "status": "success"
  },
  "raw_271_response": "<full EDI X12 271 response or JSON equivalent>",
  "screenshots": ["s3://bucket/screenshots/run_abc.png"]
}
```

## Supported Payers (Phase 1)

| Payer | Method | Workflow File |
|-------|--------|---------------|
| UnitedHealthcare | Availity API | `workflows/uhc-availity.json` |
| Aetna | Availity API | `workflows/aetna-availity.json` |
| BCBS | Availity API | `workflows/bcbs-availity.json` |
| Medicare | Availity API | `workflows/medicare-availity.json` |
| SoonerCare (Medicaid OK) | Direct portal scrape | `workflows/soonercare.json` |
