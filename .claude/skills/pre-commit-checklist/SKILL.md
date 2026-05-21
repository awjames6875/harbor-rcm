---
name: harbor-rcm-pre-commit-checklist
description: ALWAYS run this checklist before declaring any piece of code done in Harbor RCM. This skill contains the final review questions Claude Code must answer about every function before it is considered complete. Use this skill when finishing any coding task, before running git add or git commit, before writing a test, or when Adam says "is this done?" or "looks good to me." This skill is the last line of defense before code reaches production.
---

# Harbor RCM — Pre-Commit Checklist

You have written some code. Before you tell Adam it is done, before you suggest running tests, before you propose a git commit, you must answer every question in this checklist. If the answer to any question is NO or UNCLEAR, stop and fix the problem first.

Think of this checklist the way a pilot thinks about the pre-flight checklist. It is not a suggestion. It is not optional when you are in a hurry. Every item exists because someone, somewhere, had a bad outcome from skipping it.

---

## Section 1 — PHI and Security (Answer These First)

Work through every question below for the code you just wrote. Answer each one explicitly in your head before moving to the next.

**Question 1: Does this code contain any logging or print statements?**
If yes — go find every single one and verify that none of them could ever output a patient's name, date of birth, member ID, address, phone number, or any other field from the HIPAA direct identifier list in the hipaa-guardrails skill. If any logging statement touches a patient object, replace it with the hashed identifier pattern from that skill. If no — move on.

**Question 2: Does this code handle exceptions and log the error?**
If yes — check that your exception handler logs only a safe summary (what operation failed, which room, which payer, the hashed patient ID) and not the full exception object with local variable context. A bare `logger.error(e)` or `logger.error(traceback.format_exc())` can dump patient data into logs if patient objects are in scope. Use structured error logging with explicit safe fields only. If no — move on.

**Question 3: Does this code contain any hardcoded strings that look like credentials?**
Search the code you just wrote for any string longer than 8 characters that appears to be an API key, password, token, client ID, client secret, or database URL. If you find any, stop immediately. Move them to AWS Secrets Manager and replace them with a `get_secret()` call. There are no exceptions to this rule — not even for test credentials, sandbox keys, or "temporary" values. If no hardcoded credentials — move on.

**Question 4: Does this code call any external API (Availity, Skyvern, AWS, Dr. Chrono)?**
If yes — verify that all credentials used in that call come from AWS Secrets Manager via `get_secret()` and not from environment variables, hardcoded values, or .env files. If no — move on.

---

## Section 2 — Error Handling (The Happy Path Is Not Enough)

**Question 5: What happens when the external API returns a 401 Unauthorized?**
This means credentials have expired. Your code must detect this status code specifically and either attempt a token refresh (for Availity OAuth) or alert the incident manager. It must never silently fail or return a partial result. If this code does not call an external API, skip to question 6.

**Question 6: What happens when the external API returns a 429 Too Many Requests?**
This means you are being rate limited. Your code must back off and retry with exponential backoff, not immediately retry in a tight loop. The retry logic should have a maximum retry count after which it fails with a clear error message, not an infinite loop.

**Question 7: What happens when the external API times out with no response?**
Network calls must have explicit timeouts set. A call with no timeout will hang forever if the remote server stops responding, blocking the entire Lambda function until it times out at the infrastructure level. Set timeouts at the HTTP client level, not just at the Lambda level.

**Question 8: What happens when the input data is malformed or missing required fields?**
Your code should validate inputs with Pydantic before processing them. If a required field is missing, raise a clear validation error immediately rather than propagating None values through the pipeline until something breaks much later in a harder-to-debug way.

---

## Section 3 — EHR and Audit Log (Sequence Matters)

**Question 9: Does this code write anything to the EHR?**
If yes — verify that the audit log entry is written BEFORE the EHR write, not after. The sequence must always be: compute result → write audit log → write to EHR. This sequence ensures that even if the EHR write fails, there is a record of what was attempted. If no — move on.

**Question 10: Does the audit log entry in this code use only hashed patient identifiers?**
If this code writes to CloudWatch or any audit log, verify that no raw patient identifiers appear anywhere in the log entry. Use the `hash_patient_id()` function from the hipaa-guardrails skill for any field that references a specific patient. If this code does not write logs — move on.

---

## Section 4 — Confidence Scoring and Data Integrity

**Question 11: Does this code produce a benefits object or confidence score?**
If yes — verify that None values from missing 271 fields are preserved as None in the output, not converted to 0.0 or empty strings. A missing field and an explicit zero are meaningfully different. The confidence scorer needs to know the difference to properly penalize missing fields. If no — move on.

**Question 12: Does this code route a result to the EHR, the review queue, or a staff alert?**
If yes — verify that the routing logic uses the confidence thresholds from CLAUDE.md exactly: above 95% is auto-push, 80-95% is human review queue, below 80% is staff alert with no EHR write. These thresholds are not suggestions — they are the contractual promise to clients. If no — move on.

---

## Section 5 — Tests

**Question 13: Does every function in this code have at least one test?**
If no — write the tests before declaring this code done. A function with no test does not exist as far as production is concerned. Use the testing-protocol skill to understand what a complete test looks like for each type of function.

**Question 14: Do the tests cover at least one failure case, not just the happy path?**
Every test suite must include at least one test where the input is wrong, missing, or unexpected, and verify that the code handles it gracefully rather than crashing. For normalizer functions, this means a test with a malformed 271 response. For API clients, this means a test with a mocked 401 response. For validators, this means a test with a missing required field.

**Question 15: Have the tests actually been run and do they pass?**
Writing tests is not the same as running them. Run `py -m pytest` in the room's folder and verify that all tests pass with zero failures before proposing a commit.

---

## Section 6 — The Final Git Check

**Question 16: Does `git diff --staged` contain any file that should not be committed?**
Before running `git commit`, review what is staged. Look for .env files, .env.local files, workflow JSON files that still contain real credentials, test fixtures with real patient data, or any file that was not intentionally added. If you see anything unexpected in the diff, unstage it with `git reset HEAD <filename>` before committing.

**Question 17: Does the commit message describe what changed and why?**
A commit message of "updates" or "fixes" is not acceptable. The message should complete the sentence "When applied, this commit will..." and describe the specific change made and the reason for it. Example: "Add copay extraction for UHC Service Type Code 98 — UHC puts copay under Code 98 not Code 1."

---

## Completing the Checklist

If you have answered YES or N/A to every question above, the code is done and may be committed. If you answered NO to any question, stop, fix the problem, and run through the checklist again from the beginning. The checklist does not get shorter when you are in a hurry. It gets more important.
