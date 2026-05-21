# CONTEXT.md — 2_check-coverage (Insurance Verification)
## Purpose
Runs eligibility checks. Path A (Availity API $0.003) first. Path B (Skyvern browser $0.15) fallback. Self-healing workflow swap when portals change.

## Key Files
- availity_client.py — 270/271 API calls
- skyvern_runner.py — browser automation fallback
- verification_handler.py — orchestrator (Path A first, B fallback)
- workflow_swapper.py — NEW: self-healing recording replacement
- payer_router.py — maps payers to paths and recordings

## Workflows Folder
- workflows/ — one JSON per payer portal ({payer}_eligibility.json)
- workflows/archive/ — old recordings with timestamps

## Rules
- Always try Path A before Path B
- Always set max_steps=25 on Skyvern tasks
- Never hardcode credentials, use AWS Secrets Manager
- Never modify workflow JSON directly, use workflow_swapper
