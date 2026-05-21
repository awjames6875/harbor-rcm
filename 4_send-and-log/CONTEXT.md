# CONTEXT.md — 4_send-and-log (EHR Writing, Review Queue, Analytics, Alerts)

## Purpose
Writes verified benefits to EHR, manages the human review queue for uncertain results, sends staff alerts, logs the HIPAA audit trail, and tracks ROI analytics. This is what the doctor sees every day.

## Inputs
Reads from: `3_clean-the-response/output/benefits_object.json`
Expected fields: `coverage_status`, `copay`, `deductible_remaining`, `oop_max`, `prior_auth_required`, `effective_date`, `plan_name`, `confidence_score`, `confidence_tier`, `raw_response`

## Process
1. Route by `confidence_tier`:
   - 95%+ → `ehr_poster.py` writes directly to EHR (no human review)
   - 80–95% → `review_queue.py` holds for staff review with uncertain fields highlighted
   - <80% → `notifier.py` sends staff alert, nothing written to EHR
2. `audit_logger.py` writes to CloudWatch BEFORE every EHR write (HIPAA rule — non-negotiable)
3. Human corrections logged to DynamoDB → feeds back to Room 3 `learning_engine.py`
4. `analytics_tracker.py` updates running metrics
5. `incident_manager.py` handles failures — see `code/incident_manager_spec.md`

## Outputs
Final room — outputs go to external systems (no output/ folder read by another room):
- EHR (TBD — configured per client at install time)
- CloudWatch audit log (7-year retention)
- Staff SMS/email/Slack alerts
- DynamoDB: corrections table, incidents table, analytics table

## Key Files
- `ehr_poster.py` — writes to client EHR (configured at install)
- `audit_logger.py` — HIPAA CloudWatch logging
- `notifier.py` — staff alerts via SMS/email/Slack
- `review_queue.py` — editable review interface (states: Pending → In Review → Corrected → Auto-Pushed → Failed)
- `analytics_tracker.py` — verifications/month, confidence trend, Path A vs B, cost per verification
- `incident_manager.py` — self-healing runbook (spec: `code/incident_manager_spec.md`)

## Rules
- Always write audit log BEFORE writing to EHR
- Never display full patient names (first initial + last only)
- Never delete review queue items — state changes only
- Always log human corrections for Room 3 learning engine
- Always include actionable instructions in staff alerts