# CONTEXT.md — Room 4: Delivery

## Purpose
Take the clean benefits object from /3_normalization, write it to the EHR, alert staff if anything needs human attention, and create the HIPAA audit log entry.

## The Process (Step by Step)
1. Receive canonical benefits object from /3_normalization
2. Look up which EHR this client uses (Dr. Chrono, TherapyNotes via Keragon, etc.)
3. Format the data for that specific EHR's API
4. Write benefits to the patient's appointment record
5. If status is "active" and complete → done, log success
6. If status is "inactive" → alert front desk via dashboard
7. If prior auth required → flag for /paula (when PAULA agent exists) or human queue
8. If data quality score < 0.80 → flag for human review
9. Create HIPAA audit log entry (always)
10. Update client dashboard metrics (verifications today, success rate, etc.)

## Identity & Audience
- Who uses this room: Front desk staff (via dashboard alerts), EHR system, audit logs
- Tone of voice: Staff-facing alerts should be plain English, action-oriented
- What "good" looks like here: Front desk knows EXACTLY what to do for each patient before they arrive. No surprises at check-in. Audit trail is bulletproof.

## Tech Stack For This Room
- **AWS Lambda** — orchestration
- **Dr. Chrono API** (default EHR) — direct REST integration
- **Keragon** (when needed) — bridge for TherapyNotes and other no-API EHRs
- **AWS CloudWatch Logs** — HIPAA audit trail (encrypted, immutable, 7-year retention)
- **AWS SNS / Twilio** — staff alerts
- **DynamoDB** — dashboard metrics

## Patterns to Follow
- ALWAYS write the audit log BEFORE writing to the EHR (audit even on EHR write failure)
- Format alert messages for the human reading them — not the developer
- Include the verification timestamp on every EHR write
- Use idempotency keys to prevent duplicate writes
- Batch dashboard metric updates (not real-time per call)

## Alert Message Templates (Front Desk)

**Active Coverage:**
> ✅ [Patient Name] verified. Copay $30. Deductible: $1,200 of $2,500 remaining. Plan: UHC Choice Plus PPO.

**Inactive Coverage:**
> ⚠️ [Patient Name] insurance is INACTIVE. Coverage ended [date]. Call patient to confirm new insurance before appointment on [date].

**Prior Auth Required:**
> 🔔 [Patient Name] coverage is active BUT prior authorization required for [service type]. Submit auth request before appointment.

**Data Quality Issue:**
> 🔍 [Patient Name] verified but some fields unclear. Please review benefits manually before appointment.

## Never Do This (Constraints)
- NEVER write to the EHR without first writing the audit log
- NEVER send alerts containing full patient names + DOB in the same SMS (PHI exposure)
- NEVER skip the audit log "to save costs" — HIPAA fines are way more expensive
- NEVER mark a verification "complete" if EHR write failed — flag it for retry
- NEVER expose the dashboard publicly (always behind auth)

## Skills To Load (Layer 3)
When working in this room, also load:
- `skills/drchrono-api.md` — Dr. Chrono REST patterns
- `skills/keragon-bridge.md` — using Keragon for non-API EHRs
- `skills/hipaa-audit-logging.md` — exact log format requirements
- `skills/staff-alerts.md` — alert template patterns

## HIPAA Audit Log Format (Required)

Every action gets logged to CloudWatch in this exact shape:

```json
{
  "timestamp": "2026-04-30T03:15:35Z",
  "event_type": "verification_completed",
  "client_id": "client_drchrono_001",
  "patient_id_hash": "hash_abc123",
  "appointment_id": "appt_xyz789",
  "actor": "aria_agent_v1.0",
  "action": "wrote_benefits_to_ehr",
  "result": "success",
  "data_classification": "PHI",
  "ip_address": "10.0.1.45",
  "request_id": "req_unique_id_here"
}
```
