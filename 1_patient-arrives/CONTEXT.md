# CONTEXT.md — 1_patient-arrives (Patient Data Intake)

## Purpose
Handles every way patient data enters ARIA: real-time EHR webhooks, CSV batch uploads, scanned document OCR extraction, and one-time historical data ingestion at client onboarding. Data always leaves this room as a validated patient dictionary for Room 2, or as a structured payer profile written to DynamoDB.

## The Two Modes This Room Operates In

Understanding the distinction between these two modes is critical. Real-time mode runs every day once ARIA is live — a patient appointment arrives, gets validated, and flows through the pipeline in seconds. Onboarding mode runs exactly once when a new client is installed — it ingests twelve months of historical data so ARIA understands the client specific payer mix before it ever processes a live patient. Think of onboarding mode like giving a new employee a full year of company history to read on their first day before they take their first phone call.

## Key Files

webhook_handler.py handles EHR appointment triggers arriving via HTTP POST in real time.

input_validator.py validates every incoming patient record using Pydantic. Required fields are first_name, last_name, dob (YYYY-MM-DD), member_id, and payer.

batch_processor.py handles CSV upload mode. Validates each row, separates valid from invalid, reports results, passes only valid rows to Room 2.

ocr_extractor.py handles scanned forms, faxes, and handwritten documents via Claude/Bedrock OCR. Returns structured field values with per-field confidence scores. Low-confidence fields flagged for human review.

history_ingester.py is NEW and runs only during client onboarding. Connects to the client EHR or billing system, pulls all eligibility checks and claims from the past twelve months, feeds them through Room 3 normalization in batch mode, and writes payer profiles to DynamoDB. These profiles give ARIA a baseline understanding of the client specific payer mix before any live patient is processed. This is the equivalent of what XY.ai described as training the agent on your business.

## What a Payer Profile Contains (Written to DynamoDB by history_ingester.py)

Each payer profile captures everything ARIA learned from twelve months of historical transactions for one payer at one practice. The fields are: client_id (which practice), payer_id (Availity payer identifier), sample_size (how many transactions were analyzed), field_presence (dictionary mapping each canonical field to the percentage of responses where it had a value), value_ranges (typical numeric ranges for copay, deductible, OOP max at this practice), format_patterns (payer-specific quirks found in the data, such as UHC returning copay in cents not dollars), and denial_rate (historical percentage of inactive or denied coverage results for this payer).

## Rules

- Always validate before forwarding to Room 2
- Never log raw PHI to CloudWatch, always hash patient identifiers
- Never auto-correct ambiguous OCR values, flag for human review
- Never send to Room 2 if member_id is missing
- Never run history_ingester.py while live ARIA traffic is flowing (batch job competes for DynamoDB write capacity)
- Client must have signed BAA before history_ingester.py runs. See docs/training-protocol.md.
