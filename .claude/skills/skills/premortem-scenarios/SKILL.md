---
name: harbor-rcm-premortem
description: ALWAYS load this skill before writing any new code, designing any new feature, or making any architectural decision in Harbor RCM. This skill contains the pre-mortem failure analysis for ARIA — every known way the system could fail, the signal that would tell you it happened, and the protection built against it. Use this skill when starting any new coding task, when reviewing existing code, when Claude Code is about to touch any room in the pipeline, or when Adam asks "what could go wrong." This skill must be consulted before any code is written — no exceptions.
---

# Harbor RCM — Pre-Mortem Failure Analysis

You are about to write code for ARIA, an AI-powered insurance verification agent that handles real patient data at real medical practices. Before touching a single file, read every failure scenario below and ask yourself: does the code I am about to write create, worsen, or solve any of these problems?

---

## The Five Catastrophic Failure Scenarios

These are the failures that would end Harbor RCM as a business. Treat them with extreme seriousness.

### Failure 1 — Wrong Benefits Data Reaches the EHR (Most Dangerous)

What happens: ARIA verifies a patient, produces a plausible-looking benefits object, and writes it to the doctor's EHR. The copay is wrong. The patient gets billed incorrectly. The doctor's staff doesn't catch it because they trusted ARIA. The patient disputes it. The practice gets a complaint.

Signal that it happened: Staff manually checks a verification result and finds it doesn't match what the insurance company actually has on file.

Root causes to watch for:
- The 271 response parser misread a field code (e.g., confused Service Type Code 30 with Code 1)
- The confidence scorer gave a high score to a structurally valid but semantically wrong response
- A payer returned an unusual format that the normalizer didn't handle correctly
- The wrong payer profile was loaded from DynamoDB (patient's payer ID didn't match)

Protection built against it: Confidence scoring thresholds in 3_clean-the-response. Above 95% auto-pushes. Between 80-95% routes to human review queue. Below 80% alerts staff and never touches EHR. The human review queue exists specifically for this scenario.

Before writing any normalizer or confidence scorer code, ask: what does this code do when the input is structurally valid but semantically unexpected?

---

### Failure 2 — PHI Leaks Into a CloudWatch Log

What happens: A developer (Claude Code) writes a logging statement that includes a patient's name, date of birth, member ID, or any other protected health information. That log is stored in CloudWatch. CloudWatch is technically HIPAA-eligible but the log entry itself is a breach. Under HIPAA's Breach Notification Rule, this requires notifying the affected patient and potentially HHS within 60 days.

Signal that it happened: Adam or a client reviews CloudWatch logs during debugging and sees recognizable patient information in plain text.

Root causes to watch for:
- A logging statement like `logger.info(f"Processing patient {patient.first_name} {patient.last_name}")` — NEVER do this
- An exception handler that dumps the full request object to logs, which contains the patient payload
- A debug print statement left in production code
- An error message that includes the raw 271 response (which contains patient identifiers)

Protection built against it: Always hash patient identifiers before logging. Use SHA-256 hash of the member_id as the log identifier. Log the hash, never the raw value. The audit_logger.py in 4_send-and-log enforces this pattern — follow it everywhere else too.

Before writing any code that logs anything, ask: could this log line ever contain a real patient's name, DOB, member ID, address, phone number, or any other field on the HIPAA direct identifier list?

---

### Failure 3 — Skyvern Silently Fails Without Anyone Noticing

What happens: A payer portal changes its UI. Skyvern can no longer navigate it. Instead of throwing a loud error, it times out quietly. ARIA marks the verification as failed but doesn't alert staff prominently enough. Appointments happen without verified coverage. The practice bills patients who turn out to be uninsured or on a different plan. The practice loses money.

Signal that it happened: A spike in verification failures for a specific payer. Staff start calling patients manually to verify insurance. The error rate for that payer in CloudWatch goes above baseline.

Root causes to watch for:
- Skyvern task returns a "completed" status but with an empty or null output field — this is a silent failure
- The workflow swapper wasn't triggered because the failure looked like a timeout rather than a navigation error
- Staff alert was sent but went to an email nobody checks regularly

Protection built against it: In verification_handler.py, always validate that Skyvern's output field contains actual data before marking a verification successful. Empty output = failure regardless of status code. Trigger the workflow_swapper and send an SMS alert (not just email) when any payer's failure rate exceeds 2 in a row.

Before writing any Skyvern integration code, ask: what does this code do when Skyvern returns status "completed" but with no extractable data?

---

### Failure 4 — Availity OAuth Token Expires and Everything Stops

What happens: The Availity API uses OAuth tokens that expire every hour. If the token refresh logic fails or the refresh token itself expires, every single API verification call returns a 401 Unauthorized error. ARIA stops working for all Path A payers simultaneously. This affects UHC, Aetna, BCBS, Medicare, and Cigna — about 80% of all patients.

Signal that it happened: A sudden spike of 401 errors in CloudWatch across all major payers at the same time.

Root causes to watch for:
- Token refresh logic has a race condition when multiple verifications run simultaneously
- The refresh token itself expired (Availity refresh tokens have a longer but still finite lifespan)
- AWS Secrets Manager has stale credentials that were rotated manually but not updated in the secret
- The token refresh happens inside the verification function rather than as a separate managed service

Protection built against it: The availity_client.py should manage token state separately from verification logic. On any 401 response, immediately attempt one token refresh before failing. Log the 401 with HIGH severity so CloudWatch alarms trigger. The incident_manager.py in 4_send-and-log should handle this specific error type with an auto-fix that forces a token refresh.

Before writing any Availity API code, ask: what happens when this code receives a 401 response, and does that handle cascade gracefully or does it fail everything?

---

### Failure 5 — A Credential Leaks Into GitHub

What happens: An Availity client ID, Skyvern API key, portal username, or AWS access key accidentally gets committed to the GitHub repository. GitHub scans for these patterns and may alert, but the damage is done the moment it's pushed. Anyone with repo access — or anyone who finds the repo if it's public — has real credentials.

Signal that it happened: GitHub sends a secret scanning alert. Or worse, unusual API activity on a client's Availity account.

Root causes to watch for:
- A .env file that wasn't in .gitignore got committed
- A hardcoded credential left over from testing (e.g., `client_id = "abc123"` in a Python file)
- A workflow JSON file that still contains a real portal username/password from the recording session
- Test data that used real credentials instead of sandbox values

Protection built against it: Your .gitignore already excludes .env and .env.local. AWS Secrets Manager stores all production credentials. For workflow JSONs from Workflow-Use recordings, always replace real credentials with `{{AVAILITY_USERNAME}}` placeholders immediately after recording and before any git add.

Before committing anything to git, ask: does any file I'm about to commit contain a string that looks like a password, API key, token, or credential?

---

## The Pre-Code Checklist

Before writing any code in any room, answer these questions. If you answer NO to any of them, stop and fix the design before writing code.

1. Does this code handle the failure case, not just the happy path?
2. If this code logs anything, is the log statement PHI-free?
3. If this code calls an external API, does it handle 401, 429, 500, and timeout?
4. If this code writes to the EHR, does it write the audit log first?
5. If this code processes a patient payload, does it validate the shape before touching any field?
6. If this code produces a confidence score, does it handle structurally-valid-but-semantically-wrong input?
7. If this code involves credentials, are they coming from AWS Secrets Manager and never hardcoded?

---

## Room-Specific Risk Notes

**1_patient-arrives** — Risk: invalid or malformed patient payloads passing validation and corrupting downstream rooms. Always use Pydantic for input validation. Fail loudly on missing required fields rather than silently substituting defaults.

**2_check-coverage** — Risk: silent failures from both Availity API and Skyvern. Always validate actual output content, not just HTTP status codes. Path A failures should never silently fall through to Path B without logging the reason.

**3_clean-the-response** — Risk: wrong benefits data reaching the EHR due to misread field codes or unhandled payer formats. Every normalizer function needs a test fixture with a real 271 response from that payer. Never ship a normalizer without a test.

**4_send-and-log** — Risk: audit log written after EHR write (compliance violation) or PHI appearing in CloudWatch. Audit log always goes first. Use only hashed identifiers in all log entries.
