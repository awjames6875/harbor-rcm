# CONTEXT.md — 3_clean-the-response (Benefits Parsing, Confidence Scoring, and Self-Improvement)

## Purpose
Transforms raw verification results into clean benefits objects with confidence scores. Loads payer profiles from DynamoDB to anchor scoring against historical baselines. Logs every human correction so ARIA gets smarter over time. This room is where the long-term moat gets built — the longer a practice uses ARIA, the more accurate it becomes for their specific payer mix.

## The Three Things This Room Does

First, it parses. Raw 271 responses and Skyvern extractions come in messy and payer-specific. This room runs them through payer-specific normalizers and outputs a clean canonical benefits object that looks identical regardless of which payer or path produced the data.

Second, it scores. Every normalized result gets a confidence score before it leaves this room. The score is anchored against the payer profile for this specific practice, so ARIA knows whether a particular response looks normal or suspicious based on twelve months of historical data for this exact client-payer combination. Without the historical baseline, a $0 copay might look suspicious. With the baseline, ARIA knows that this particular BCBS plan at this practice genuinely has a $0 copay for preventive visits.

Third, it learns. Every time a human corrects a field in Room 4 review queue, that correction flows back into this room and gets logged to DynamoDB. Over time those corrections accumulate into updated parsing rules that handle edge cases ARIA had never seen before. The longer ARIA runs at a practice, the fewer human corrections are needed because the system has already learned from previous mistakes.

## Key Files

normalizer_base.py defines the canonical benefits schema using Pydantic. Every payer-specific normalizer must output this exact shape: coverage_status, copay, deductible_remaining, oop_max, prior_auth_required, effective_date, plan_name, and raw_response. The raw_response field carries the original unmodified data for the review queue side-by-side view.

normalize_uhc.py is the UnitedHealthcare-specific parser. It knows UHC 271 response format and field locations. Falls back to Claude via Bedrock for ambiguous or malformed responses.

normalize_aetna.py is the Aetna-specific parser. Same pattern as UHC but for Aetna response format.

normalize_bcbs.py is the Blue Cross Blue Shield parser. BCBS varies significantly by state so this may need state-specific sub-parsers for Oklahoma versus Texas versus California plans.

confidence_scorer.py scores every normalized result on three dimensions. Field completeness carries 40% weight and measures what percentage of canonical fields returned non-null values. Value plausibility carries 30% weight and checks whether numeric values fall within the expected ranges captured in the payer profile for this client. Payer pattern match carries 30% weight and compares this response format against the format_patterns field in the payer profile. The overall confidence score is the weighted average. Before the payer profile exists (before onboarding history ingestion), the scorer uses conservative default ranges. After the profile exists, it uses client-specific baselines which are far more accurate.

learning_engine.py does two things. At the start of every verification run, it reads the payer profile from DynamoDB for this client and payer combination and passes it to confidence_scorer.py as the scoring baseline. After every human correction logged by Room 4, it reads the correction from DynamoDB, identifies whether this correction represents a new pattern (a field that is consistently wrong for this payer at this practice), and if so generates an updated parsing rule and writes it back to the payer profile. Over time the payer profile becomes a rich document of everything that makes this practice unique in how their payers respond.

## Confidence Score Thresholds

Above 95% means auto-push. The result goes directly to Room 4 ehr_poster.py for writing to the EHR with no human review needed.

Between 80% and 95% means human review. The result goes to Room 4 review queue with the specific uncertain fields highlighted in yellow. Staff edits individual fields and clicks Push to EHR.

Below 80% means staff alert. The result does not go to the EHR. Staff gets an actionable notification explaining exactly which fields failed and what manual steps to take.

## Rules

- Load the payer profile from DynamoDB at the start of every verification run before scoring begins
- Try Python regex parsing first for well-structured responses. Only invoke Claude via Bedrock for genuinely ambiguous cases to save money
- Always attach raw_response to the normalized output for the review queue side-by-side view
- Never auto-push below 95% confidence under any circumstances
- Never delete correction logs from DynamoDB. They are the training data for learning_engine.py and the HIPAA audit trail
- Store confidence thresholds in per-client config, not hardcoded. Some practices may want 98% before auto-push
- When learning_engine.py generates a new parsing rule, log the rule in human-readable form so any engineer can audit what the system learned and why
