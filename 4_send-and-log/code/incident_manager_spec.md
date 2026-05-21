# incident_manager.py — Automated Runbook and Self-Healing System

Belongs in: `4_send-and-log/code/incident_manager.py`
Triggered by: CloudWatch Alarms via Lambda

## What This File Does
ARIA's immune system. When something goes wrong, this file wakes up, diagnoses
the problem, attempts auto-recovery, and writes a complete incident record to
DynamoDB regardless of outcome.

## Severity Levels
- **SEV-1** — PHI at risk or HIPAA audit logging failed. Halts all processing. Pages Adam immediately.
- **SEV-2** — Verification completely down for one or more payers. Immediate SMS. Auto-recovery attempted.
- **SEV-3** — Verification degraded (high error rate, slow response, elevated human review). Alert within 15 min.
- **SEV-4** — Single verification failed, system otherwise healthy. Retried automatically. Daily digest only.
- **SEV-5** — Minor anomaly, self-resolved. Logged for pattern analysis. No alert.

## Auto-Recovery Playbook
- **Expired Availity OAuth token** → refresh via `get_availity_token()`, update Secrets Manager, retry
- **Skyvern task timeout** → resubmit with higher `max_steps`, fresh browser session. Escalate to SEV-2 on second failure
- **Lambda cold start timeout** → increase Lambda timeout via AWS SDK, retry, log new value
- **DynamoDB throughput exceeded** → switch to on-demand billing temporarily, log for capacity review
- **Availity API 5xx** → wait 60s, retry up to 3 times. Check Availity status page, include in incident record

## Incident Record Schema (DynamoDB incidents table)
- `incident_id` — UUID
- `client_id` — which practice
- `timestamp` — ISO UTC
- `severity` — SEV-1 through SEV-5
- `room` — where the error originated
- `error_type` — TOKEN_EXPIRED, SKYVERN_TIMEOUT, etc.
- `error_message` — raw CloudWatch error
- `stack_trace` — full Python traceback
- `payer` — which payer was being processed
- `claude_diagnosis` — plain-English explanation via Bedrock
- `claude_recommended_fix` — step-by-step fix from Claude
- `auto_resolution_attempted` — boolean
- `auto_resolution_successful` — boolean
- `auto_resolution_description` — what the auto-recovery did
- `manual_resolution_notes` — Adam fills in if manual fix needed
- `status` — open, auto-resolved, manually-resolved, escalated
- `time_to_resolution_seconds` — calculated on status change

## Claude Bedrock Prompt