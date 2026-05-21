# CONTEXT.md — 2_check-coverage (Insurance Verification)

## Purpose
Runs eligibility checks. Path A (Availity API $0.003) first. Path B (Skyvern browser $0.15) fallback. Self-healing workflow swap when portals change.

## Inputs
Reads from: `1_patient-arrives/output/patient_payload.json`
Expected fields: `patient_name`, `dob`, `insurance_id`, `payer_name`, `appointment_date`, `provider_npi`

## Process
1. `payer_router.py` maps payer → Path A or Path B
2. Path A: `availity_client.py` sends 270 request, receives 271 response
3. Path B (fallback): `skyvern_runner.py` replays recorded portal workflow
4. `verification_handler.py` orchestrates the above, retries once on failure
5. Result written to `output/verification_result.json`

## Outputs
Writes to: `2_check-coverage/output/verification_result.json`
Next room reads: `3_clean-the-response`
Output shape: `{ payer, patient_id, raw_271, path_used, timestamp, confidence_raw }`

## Key Files
- `availity_client.py` — 270/271 API calls
- `skyvern_runner.py` — browser automation fallback
- `verification_handler.py` — orchestrator (Path A first, B fallback)
- `payer_router.py` — maps payers to paths and recordings
- `workflow_swapper.py` — self-healing recording replacement

## Workflows
- `workflows/` — one JSON per payer portal (`{payer}_eligibility.json`)
- `workflows/archive/` — old recordings with timestamps

## Rules
- Always try Path A before Path B
- Always set `max_steps=25` on Skyvern tasks
- Never hardcode credentials — use AWS Secrets Manager
- Never modify workflow JSON directly — use `workflow_swapper`
- Write audit log entry to `logs/audit.jsonl` BEFORE writing output