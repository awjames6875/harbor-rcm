---
name: harbor-rcm-testing-protocol
description: ALWAYS load this skill before writing tests for any Harbor RCM code. This skill defines what a complete test looks like for each type of function in the ARIA pipeline — normalizers, API clients, validators, confidence scorers, and EHR posters. Use this skill whenever Adam says "write tests for this," whenever implementing a new function, or whenever the pre-commit checklist asks about test coverage. A function without tests that match this protocol is not ready for production regardless of how well the code looks.
---

# Harbor RCM — Testing Protocol

Testing healthcare automation software is different from testing a typical web app because the consequences of a wrong result are not a broken UI — they are wrong medical billing, PHI breaches, or a patient being seen without verified coverage. This protocol defines the minimum testing standard for every type of code in the ARIA pipeline. Meeting this standard is not optional.

---

## The Core Testing Philosophy for Harbor RCM

Every function in ARIA has two possible outputs: a correct result and a safe failure. A correct result means the function did its job. A safe failure means the function detected that it could not do its job correctly, said so clearly, and did not produce a plausible-looking wrong answer. The worst outcome in a healthcare system is not an error — it is a silent wrong answer that looks like a correct one. Your tests must verify both the correct result path and the safe failure path.

---

## The Synthetic Test Patients

Never use real patient data in tests. Use only these synthetic test patients which are designed to exercise different code paths. Save them in `data/test-patients/` in each room that needs them.

```python
# Test Patient A — Standard UHC commercial plan, active coverage, has copay
PATIENT_UHC_ACTIVE = {
    "first_name": "Maria",
    "last_name": "Gonzalez",
    "date_of_birth": "1985-04-12",
    "member_id": "UHC8472910",
    "payer_id": "UHNCA",
    "payer_name": "UnitedHealthcare"
}

# Test Patient B — Aetna plan, active coverage, has deductible
PATIENT_AETNA_ACTIVE = {
    "first_name": "James",
    "last_name": "Whitfield",
    "date_of_birth": "1972-11-30",
    "member_id": "AET2847193",
    "payer_id": "60054",
    "payer_name": "Aetna"
}

# Test Patient C — BCBS Oklahoma, active coverage
PATIENT_BCBS_ACTIVE = {
    "first_name": "Sarah",
    "last_name": "Chen",
    "date_of_birth": "1990-07-22",
    "member_id": "BCB9274810",
    "payer_id": "BCBSOK",
    "payer_name": "Blue Cross Blue Shield of Oklahoma"
}

# Test Patient D — Inactive coverage (lapsed policy)
PATIENT_INACTIVE = {
    "first_name": "Robert",
    "last_name": "Torres",
    "date_of_birth": "1965-03-18",
    "member_id": "UHC0000001",
    "payer_id": "UHNCA",
    "payer_name": "UnitedHealthcare"
}

# Test Patient E — Medicare traditional (no copay, has coinsurance)
PATIENT_MEDICARE = {
    "first_name": "Dorothy",
    "last_name": "Williams",
    "date_of_birth": "1948-09-05",
    "member_id": "1EG4TE5MK73",
    "payer_id": "MEDICARE",
    "payer_name": "Medicare"
}
```

---

## Testing Standard for Room 1 — Patient Arrives (Input Validators)

The webhook handler and input validator have one job: accept valid patient payloads and reject invalid ones loudly. A validator that silently passes malformed data downstream is more dangerous than a validator that rejects everything.

Every validator test suite must include these cases. The happy path test verifies that a complete, valid patient payload passes validation and returns a properly typed Pydantic model with all fields correctly parsed. The missing required field test verifies that a payload missing the member_id raises a ValidationError with a clear message identifying which field is missing — not a KeyError, not a None propagation, but a proper validation error caught at the boundary. The wrong field type test verifies that a payload where date_of_birth is an integer instead of a string in YYYY-MM-DD format raises a ValidationError rather than being silently coerced. The duplicate detection test verifies that if the same patient payload arrives twice within a short window, the second arrival is detected and either deduplicated or flagged, not processed twice resulting in duplicate verifications billed to the client.

---

## Testing Standard for Room 2 — Check Coverage (API Clients and Skyvern Runner)

The Availity client and Skyvern runner interact with external services, which means your tests must use mocking rather than real API calls. Never write a test that makes a real network call to Availity or Skyvern during automated testing — this would make tests slow, dependent on external uptime, and would consume real API credits for every test run.

Use `unittest.mock.patch` or `pytest-mock` to mock the HTTP responses. Your test fixtures should be saved as JSON files in `2_check-coverage/tests/fixtures/` with realistic but synthetic 271 response data. Create one fixture file per major payer.

Every API client test suite must include these cases. The successful 270/271 round trip test verifies that a valid patient payload produces a correctly structured request to Availity, and that the mocked 271 response is returned and passed to the normalizer. The 401 token expiration test mocks the Availity endpoint returning a 401, then verifies that the client attempts a token refresh exactly once, and then either succeeds with the new token or raises a clear authentication error — it must not retry the original request with the expired token or enter an infinite retry loop. The 429 rate limit test mocks Availity returning a 429, verifies that the client waits the duration specified in the Retry-After header before retrying, and respects the maximum retry count. The timeout test mocks the HTTP connection timing out after the configured timeout duration, verifies that the client raises a TimeoutError with a meaningful message rather than hanging indefinitely. The empty Skyvern output test mocks Skyvern returning status "completed" but with a null or empty output field, verifies that this is treated as a failure and not as a successful but empty verification.

---

## Testing Standard for Room 3 — Clean the Response (Normalizers)

Normalizer functions are the most important code to test thoroughly because they determine whether the data in the EHR is right or wrong. Each payer normalizer needs its own dedicated test file with real-format 271 response fixtures.

Every normalizer test suite must include these cases. The standard active coverage test uses a realistic 271 fixture with active coverage and a clear copay, verifies that the output CanonicalBenefits object has coverage_active equal to True, copay set to the correct dollar amount from the fixture, and no None values for fields that are present in the fixture. The inactive coverage test uses a 271 fixture where the EB coverage status code is 6 (Inactive), verifies that coverage_active is False and that the function does not attempt to extract copay or deductible from an inactive policy. The missing copay test uses a 271 fixture that contains coverage status but no copay EB segment (valid for high-deductible plans), verifies that copay is None in the output — not zero, not a default value, specifically None — and that confidence_flags contains a human-readable note explaining that no copay was found. The ambiguous copay test uses a 271 fixture where two conflicting copay amounts appear under different service type codes, verifies that the normalizer resolves the conflict using the priority order defined in the availity-271-field-map skill (Code 98 beats Code 1 beats Code 30 for primary care), and that confidence_flags notes the conflict. The structurally invalid response test passes a completely malformed string (not valid X12 format) to the normalizer, verifies that it raises a clearly named exception rather than returning a partially-populated benefits object or silently returning None.

---

## Testing Standard for Room 4 — Send and Log (EHR Poster and Audit Logger)

The EHR poster and audit logger have strict sequencing requirements that must be tested explicitly. The audit-before-EHR sequence is a HIPAA compliance requirement, not just a best practice.

Every delivery function test suite must include these cases. The audit-before-EHR sequence test mocks both the CloudWatch client and the Dr. Chrono EHR client, calls the delivery function with a valid canonical benefits object, and uses mock call_order verification to confirm that the CloudWatch put_log_events call occurred before the Dr. Chrono API call. If your testing framework cannot verify call order, restructure the function so that the audit log write and EHR write are clearly sequential and the test can assert the audit log was written by inspecting the mock before asserting the EHR was written. The EHR failure with audit preserved test mocks the EHR client raising an exception while the audit log client succeeds, verifies that the audit log entry was written (it should be — it went first), verifies that the function raises the EHR error rather than swallowing it, and verifies that no data was partially written to the EHR in an inconsistent state. The PHI-free audit log test calls the audit logger with a patient payload and then inspects every field of the resulting CloudWatch log entry, asserts that no field contains the raw member_id, date_of_birth, first_name, or last_name of the test patient, and asserts that the patient_id_hash field contains a string that matches the expected SHA-256 hash output of the hash_patient_id function from the hipaa-guardrails skill.

---

## Running the Tests

To run tests for a specific room, navigate to that room's folder and run this command in your terminal. Note the use of `py` not `python` because of Adam's Windows setup.

```powershell
cd "C:\Users\1alph\OneDrive\Desktop\rcm agent\2_check-coverage"
py -m pytest tests/ -v
```

The `-v` flag shows each individual test name and whether it passed or failed, rather than just a summary count. Always use `-v` so you can see exactly which test failed rather than just knowing that something failed.

To run all tests across the entire project at once, run this from the root of the project.

```powershell
cd "C:\Users\1alph\OneDrive\Desktop\rcm agent"
py -m pytest 1_patient-arrives/tests/ 2_check-coverage/tests/ 3_clean-the-response/tests/ 4_send-and-log/tests/ -v
```

A complete test run before any client demo or production deployment should show zero failures and zero warnings. If any test fails, that feature is not ready for production regardless of whether the failure seems minor or unlikely to matter in practice.
