# Harbor RCM — Master Build Plan
Generated from full-repo Codex adversarial review (2026-05-26)

---

## Immediate Fixes (Codex findings — do these first)

- [ ] **1. Wrap audit writes in availity_client.py**
  - `2_check-coverage/code/availity_client.py` lines 187-190
  - `_audit()` currently has unguarded `open()` — a disk/permission error masks or crashes real eligibility results
  - Fix: wrap the file write in `try/except` and log to `stderr` on failure (same pattern as `VerificationHandler._audit`)

- [ ] **2. Wrap audit writes in skyvern_runner.py**
  - `2_check-coverage/code/skyvern_runner.py`
  - Same unguarded `open()` issue — same fix as above

- [ ] **3. Stop tracking audit logs in git**
  - Add `**/logs/` and `**/*.jsonl` to `.gitignore`
  - Run `git rm --cached 2_check-coverage/logs/audit.jsonl` if file is tracked

---

## Cleanup

- [ ] **4. Delete nested duplicate folder**
  - `3_clean-the-response/code/3_clean-the-response/` is a mistakenly nested copy — delete it

- [ ] **5. Add binary/installer files to .gitignore**
  - `AWS+Business+Associate+Addendum.pdf` and `AWSCLIV2.msi` should not be tracked
  - Add `*.pdf`, `*.msi` to `.gitignore` (or list them explicitly)

- [ ] **6. Commit untracked docs that belong in the repo**
  - `API_REFERENCE.md`, `AVAILITY_API_DOCS.md`, `3_clean-the-response/requirements.txt`

---

## Room 3 — Finish clean-the-response

- [ ] **7. Build confidence_scorer.py**
  - File: `3_clean-the-response/code/confidence_scorer.py`
  - Input: a `BenefitsObject` (from any normalizer)
  - Output: same object with `confidence_score` (float 0–100) and `confidence_tier` set
  - Three scoring dimensions (from CLAUDE.md):
    - Field completeness 40% — how many canonical fields are non-None
    - Value plausibility 30% — numeric values within realistic ranges per payer
    - Payer pattern match 30% — placeholder until DynamoDB history exists (default full weight)
  - Tiers: `>= 95` → `"auto_push"`, `80–94` → `"review"`, `< 80` → `"alert"`

- [ ] **8. Add tests for confidence_scorer.py**
  - File: `3_clean-the-response/tests/test_confidence_scorer.py`
  - Test: fully populated object scores auto_push
  - Test: missing copay/deductible fields lower score into review tier
  - Test: near-empty object scores into alert tier
  - Test: `confidence_score` and `confidence_tier` are always set (never None after scoring)

---

## Room 4 — Build send-and-log

- [ ] **9. Build send_handler.py**
  - File: `4_send-and-log/code/send_handler.py`
  - Input: scored `BenefitsObject` from Room 3
  - Logic:
    - Fail closed if `confidence_tier` is None — raise immediately, do not touch EHR
    - `auto_push` → write to EHR, send success notification to staff
    - `review` → add to human review queue, highlight uncertain fields
    - `alert` → send SMS/email alert to staff, do NOT write to EHR
  - **Audit log write MUST happen before EHR write** (per CLAUDE.md invariant)

- [ ] **10. Build incident_manager.py**
  - File: `4_send-and-log/code/incident_manager.py`
  - Spec already exists at `4_send-and-log/CONTEXT.md` (incident_manager spec section)
  - Watches CloudWatch, diagnoses errors via Claude/Bedrock, auto-fixes known issues
  - Writes every incident to DynamoDB permanently

- [ ] **11. Add tests for Room 4**
  - `4_send-and-log/tests/test_send_handler.py`
  - Test: None confidence_tier raises before any EHR write
  - Test: auto_push calls EHR write and sends notification
  - Test: alert tier sends alert and does NOT call EHR write
  - Test: audit log is written before EHR write (mock order verification)

- [ ] **12. Add requirements.txt for Room 4**
  - File: `4_send-and-log/requirements.txt`

---

## Room 1 — Build patient-arrives

- [ ] **13. Build patient_handler.py**
  - File: `1_patient-arrives/code/patient_handler.py`
  - Input: raw EHR webhook payload or CSV row
  - Output: validated patient dict matching the shape `availity_client.check_eligibility` expects
  - Validates: `member_id` required (reject if missing), `birth_date` format, payer name resolvable
  - Deduplicates: skip if same patient+payer checked within last 24h (DynamoDB lookup)

- [ ] **14. Add tests for Room 1**
  - `1_patient-arrives/tests/test_patient_handler.py`
  - Test: valid payload produces correct patient dict
  - Test: missing member_id raises validation error
  - Test: malformed birth_date raises validation error

- [ ] **15. Add requirements.txt for Room 1**
  - File: `1_patient-arrives/requirements.txt`

---

## Room 2 — Remaining gaps

- [ ] **16. Add requirements.txt for Room 2**
  - File: `2_check-coverage/requirements.txt`
  - Include: `requests`, `boto3`, `pydantic`

- [ ] **17. Add pytest config for Room 2**
  - File: `2_check-coverage/pytest.ini` or `pyproject.toml`

---

## Verification (after all items complete)

Run tests in each room:
```
py -m pytest 1_patient-arrives/tests/ -v
py -m pytest 2_check-coverage/tests/ -v
py -m pytest 3_clean-the-response/tests/ -v
py -m pytest 4_send-and-log/tests/ -v
```

Run end-to-end smoke test:
- Feed a test patient dict through Room 1 → Room 2 (sandbox) → Room 3 → Room 4
- Verify audit log is written, confidence tier is set, EHR write is gated by tier

Run `/codex:adversarial-review` again after all items are done — target is a clean `approve` verdict.
