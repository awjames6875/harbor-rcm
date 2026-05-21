# CONTEXT.md — 3_clean-the-response (Benefits Parsing, Confidence Scoring, and Self-Improvement)

## Purpose
Parses raw verification results into a clean canonical benefits object, scores confidence against the practice's payer history, and learns from human corrections over time.

## Inputs
Reads from: `2_check-coverage/output/verification_result.json`
Expected fields: `payer`, `patient_id`, `raw_271`, `path_used`, `timestamp`, `confidence_raw`

## Process
1. `learning_engine.py` loads payer profile from DynamoDB for this client-payer pair
2. Payer-specific normalizer runs (`normalize_uhc.py`, `normalize_aetna.py`, `normalize_bcbs.py`)
3. Falls back to Claude via Bedrock only for genuinely ambiguous responses
4. `confidence_scorer.py` scores result on 3 dimensions (completeness 40%, plausibility 30%, pattern match 30%)
5. Result + confidence score written to `output/benefits_object.json`
6. Human corrections from Room 4 feed back into `learning_engine.py` → updated payer profile in DynamoDB

## Outputs
Writes to: `3_clean-the-response/output/benefits_object.json`
Next room reads: `4_send-and-log`
Output shape: `{ coverage_status, copay, deductible_remaining, oop_max, prior_auth_required, effective_date, plan_name, confidence_score, confidence_tier, raw_response }`

## Confidence Tiers
- **95%+** → auto-push to EHR (no human review)
- **80–95%** → human review queue (uncertain fields highlighted)
- **<80%** → staff alert, nothing written to EHR

## Key Files
- `normalizer_base.py` — canonical benefits schema (Pydantic)
- `normalize_uhc.py` — UnitedHealthcare parser
- `normalize_aetna.py` — Aetna parser
- `normalize_bcbs.py` — BCBS parser (may need state sub-parsers)
- `confidence_scorer.py` — weighted confidence scoring
- `learning_engine.py` — loads payer profiles, generates updated parsing rules from corrections

## Rules
- Load payer profile from DynamoDB before scoring begins
- Try Python regex first — only invoke Claude via Bedrock for ambiguous cases
- Always attach `raw_response` to output for review queue side-by-side view
- Never auto-push below 95% confidence
- Never delete correction logs from DynamoDB — they are HIPAA audit trail and training data
- Store confidence thresholds in per-client config, not hardcoded
- When `learning_engine.py` generates a new rule, log it in human-readable form