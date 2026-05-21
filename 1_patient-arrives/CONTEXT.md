# CONTEXT.md — 1_patient-arrives (Patient Data Intake)

## Purpose
Handles every way patient data enters ARIA: real-time EHR webhooks, CSV batch uploads, scanned document OCR extraction, and one-time historical data ingestion at client onboarding.

## Inputs
Reads from: External sources (this is Room 1 — data enters from outside the pipeline)
- Real-time: HTTP POST from EHR webhook
- Batch: CSV file upload
- OCR: Scanned form, fax, or handwritten document
- Onboarding: Historical EHR/billing data pull (runs once per client install)

## Process
1. `webhook_handler.py` receives EHR appointment trigger (real-time mode)
2. `batch_processor.py` validates CSV rows, separates valid from invalid (batch mode)
3. `ocr_extractor.py` extracts fields from scanned docs via Claude/Bedrock (OCR mode)
4. `history_ingester.py` pulls 12 months of historical data and writes payer profiles to DynamoDB (onboarding mode — runs once)
5. `input_validator.py` validates every record before it leaves this room
6. Valid records written to `output/patient_payload.json`

## Outputs
Writes to: `1_patient-arrives/output/patient_payload.json`
Next room reads: `2_check-coverage`
Output shape: `{ patient_name, dob, member_id, payer, provider_npi, appointment_date, source_mode }`

## The Two Modes
**Real-time mode** — runs daily once ARIA is live. Patient appointment arrives, validates, flows to Room 2 in seconds.
**Onboarding mode** — runs exactly once per client install. Ingests 12 months of history so ARIA understands the payer mix before processing any live patient. Like giving a new employee a full year of company history before their first phone call.

## Key Files
- `webhook_handler.py` — EHR appointment triggers via HTTP POST
- `input_validator.py` — Pydantic validation (required: first_name, last_name, dob, member_id, payer)
- `batch_processor.py` — CSV upload mode, valid/invalid separation
- `ocr_extractor.py` — scanned forms via Claude/Bedrock, per-field confidence scores
- `history_ingester.py` — onboarding only, writes payer profiles to DynamoDB

## Rules
- Always validate before forwarding to Room 2
- Never log raw PHI to CloudWatch — hash patient identifiers
- Never auto-correct ambiguous OCR values — flag for human review
- Never send to Room 2 if `member_id` is missing
- Never run `history_ingester.py` while live traffic is flowing
- Client must have signed BAA before `history_ingester.py` runs — see `docs/training-protocol.md` into the excellence and I'm just going to say that oh my god that's a little kind of faster we don't have I just I don't I don't know 