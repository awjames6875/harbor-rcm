---
description: Codex audit scoped to a Harbor RCM room, focused on PHI/HIPAA/Path-A-vs-B correctness
---

Run `/codex adversarial-review` on the path the user names (e.g. `2_check-coverage/`, `3_clean-the-response/`, or a specific file).

Focus the audit on these Harbor-specific concerns:
1. **PHI handling** — no PHI in logs, no PHI in error messages, no PHI outside encrypted stores (DynamoDB, S3 with SSE).
2. **Secrets** — credentials always come from AWS Secrets Manager. Never `.env`. Never hardcoded. Never logged.
3. **HIPAA audit-trail completeness** — every write/action must log timestamp (UTC) + user + action + outcome.
4. **Path A vs Path B routing correctness** — never use Skyvern when an Availity API path is available. UHC, Aetna, BCBS, Medicare, Cigna are API-only. SoonerCare and small regional payers are Skyvern.
5. **Edge cases the transcript-style review catches** — timezones (always UTC for storage), retries with exponential backoff (1s → 2s → 4s), empty / malformed 271 responses, 2FA flows, session expiry, captcha, Skyvern rate limits (max 5 patients in parallel).

Run with `--background` unless the user explicitly says they're blocking on the result. When backgrounded, remind the user to check `/codex status` and `/codex result` later.
