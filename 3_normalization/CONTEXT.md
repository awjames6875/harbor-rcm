# CONTEXT.md — Room 3: Normalization

## Purpose
Take the messy raw 271 response from /2_verification and turn it into a clean, structured benefits object that's identical regardless of which payer it came from.

## The Process (Step by Step)
1. Receive raw 271 response (EDI X12 or JSON) from /2_verification
2. Identify the payer format (each payer structures 271s differently)
3. Parse using the payer-specific normalizer
4. Extract key fields: status, plan name, copay, deductible (met/remaining), coinsurance, OOP max, prior auth required
5. Validate completeness — flag missing fields
6. Apply business rules (e.g., calculate patient OOP cost)
7. Output canonical benefits object
8. Forward to /4_delivery

## Identity & Audience
- Who uses this room: Internal — never seen by humans directly
- Tone of voice: N/A (data transformation only)
- What "good" looks like here: Same structured output regardless of input payer. Zero data loss. Every field has a known source.

## Tech Stack For This Room
- **Python** (`py` not `python` on Windows) — primary language
- **Pydantic** — output schema validation
- **JSON Schema** — canonical benefits format definition
- **AWS Lambda** — runs as a transform step
- **Claude via AWS Bedrock** — for parsing edge cases / non-standard responses

## Patterns to Follow
- One normalizer function per payer (`normalize_uhc()`, `normalize_aetna()`, etc.)
- Canonical output schema is the source of truth — never change it without updating all normalizers
- Use Claude (via Bedrock) ONLY for ambiguous fields (last resort, costs money)
- Store every raw 271 alongside its normalized output (for debugging)
- Version your schemas (`benefits_schema_v1.json`)

## Never Do This (Constraints)
- NEVER guess at missing fields — return null and flag it
- NEVER apply payer-specific logic in the canonical schema layer
- NEVER call Bedrock for fields you can parse with regex (waste of money)
- NEVER ship a new payer normalizer without test cases
- NEVER modify the canonical schema without bumping the version

## Skills To Load (Layer 3)
When working in this room, also load:
- `skills/edi-271-parsing.md` — X12 EDI structure reference
- `skills/pydantic-schemas.md` — schema patterns
- `skills/bedrock-fallback.md` — when to use Claude for parsing

## Data Shape (Canonical Benefits Object)

This is the SINGLE source of truth — every payer normalizes TO this shape:

```json
{
  "patient_id": "hash_abc123",
  "verification_id": "ver_xyz789",
  "normalized_at": "2026-04-30T03:15:33Z",
  "schema_version": "v1",
  "coverage": {
    "status": "active",
    "plan_name": "UHC Choice Plus PPO",
    "plan_type": "PPO",
    "effective_date": "2026-01-01",
    "term_date": "2026-12-31"
  },
  "financial": {
    "copay": {
      "amount": 30.00,
      "currency": "USD",
      "type": "office_visit"
    },
    "deductible": {
      "individual_total": 2500.00,
      "individual_remaining": 1200.00,
      "family_total": 5000.00,
      "family_remaining": 3500.00
    },
    "coinsurance": {
      "in_network_percent": 20,
      "out_of_network_percent": 40
    },
    "out_of_pocket_max": {
      "individual": 6500.00,
      "family": 13000.00
    }
  },
  "authorization": {
    "required": false,
    "service_types": []
  },
  "data_quality": {
    "completeness_score": 0.95,
    "missing_fields": [],
    "ambiguous_fields": []
  }
}
```
