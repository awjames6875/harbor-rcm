# CONTEXT.md — Room 1: Intake

## Purpose
Receive new patient appointments from the EHR (or batch CSV upload), validate the data, and prepare it for verification.

## The Process (Step by Step)
1. EHR webhook fires when a new appointment is scheduled (or staff uploads a CSV batch)
2. Parse the patient data: first name, last name, DOB, insurance company, member ID, group number
3. Validate required fields are present and formatted correctly
4. Check for duplicates (same patient verified in last 24 hours)
5. If valid → forward to /2_verification with structured payload
6. If invalid → log error, alert staff via dashboard, halt workflow

## Identity & Audience
- Who uses this room: Front desk staff, schedulers, automated EHR webhooks
- Tone of voice: Internal/technical (no patient-facing copy here)
- What "good" looks like here: Zero invalid data passed downstream. Every error logged with reason. Duplicate detection saves API costs.

## Tech Stack For This Room
- **AWS Lambda** — receives webhook from EHR
- **AWS API Gateway** — public endpoint with API key auth
- **DynamoDB** — duplicate detection cache (24h TTL)
- **Pydantic** (Python) — data validation schemas

## Patterns to Follow
- Always validate BEFORE forwarding to verification (catch errors cheap)
- Use structured logging: `{timestamp, action, patient_id_hash, status}`
- Hash patient identifiers in logs (never log raw PHI)
- Return 200 OK to webhooks immediately, then process async

## Never Do This (Constraints)
- NEVER log raw patient PHI (names, member IDs, DOBs in plain text)
- NEVER skip validation to "save time" — invalid data downstream costs more
- NEVER call Availity directly from this room — that's /2_verification's job
- NEVER store patient data here longer than 24 hours

## Skills To Load (Layer 3)
When working in this room, also load:
- `skills/csv-parser.md` — for batch upload handling
- `skills/pydantic-schemas.md` — validation patterns
- `skills/webhook-security.md` — API key + signature verification

## Data Shape (What This Room Outputs to /2_verification)

```json
{
  "patient_id": "hash_abc123",
  "appointment_id": "appt_xyz789",
  "patient": {
    "first_name": "Maria",
    "last_name": "Gonzalez",
    "dob": "1985-04-12",
    "member_id": "UHC8472910"
  },
  "payer": {
    "name": "UnitedHealthcare",
    "code": "UHC",
    "portal": "availity"
  },
  "appointment_time": "2026-05-15T09:00:00-05:00",
  "priority": "T-48"
}
```
