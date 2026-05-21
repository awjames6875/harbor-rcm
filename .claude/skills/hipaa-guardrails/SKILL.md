---
name: harbor-rcm-hipaa-guardrails
description: ALWAYS load this skill before writing any code in 2_check-coverage, 3_clean-the-response, or 4_send-and-log. This skill defines every PHI field that must never appear in logs, the exact hashing standard for patient identifiers in audit logs, and a complete checklist of every place PHI could accidentally leak. Use this skill whenever writing logging statements, error handlers, audit log entries, or any code that touches patient data. Also use when Adam asks about HIPAA compliance, data safety, or what patient information is protected.
---

# Harbor RCM — HIPAA Guardrails

You are working on a system that handles Protected Health Information (PHI). HIPAA defines 18 categories of direct identifiers that make health information individually identifiable. If any of these appear in an unprotected context — a log file, an error message, a test fixture committed to GitHub, or an email alert — it constitutes a potential HIPAA breach. Read this skill completely before writing any code that touches patient data.

---

## The 18 HIPAA Direct Identifiers

Never let any of these fields appear in CloudWatch logs, error messages, email alerts, SMS notifications, GitHub commits, or any output visible outside the encrypted EHR or AWS Secrets Manager.

Names (first, last, or full name of patient or family members), geographic data smaller than a state (street address, city, zip code, county, GPS coordinates), dates more specific than year that relate to the patient (date of birth, admission date, discharge date, date of service, date of death), phone numbers, fax numbers, email addresses, Social Security numbers, medical record numbers, health plan beneficiary numbers (this includes member IDs — this is one of the most commonly leaked fields in RCM systems), account numbers, certificate or license numbers, vehicle identifiers and serial numbers, device identifiers, web URLs, IP addresses, biometric identifiers (fingerprints, voice), full-face photographs, and any other unique identifying number or code.

The two fields you will encounter most often in Harbor RCM that are PHI are member_id (health plan beneficiary number) and date_of_birth. These must be hashed before appearing anywhere outside the canonical patient payload in memory.

---

## The Hashing Standard for Harbor RCM

Every time a patient identifier needs to appear in a log, use this exact pattern. Never deviate from it.

```python
import hashlib

def hash_patient_id(member_id: str, client_id: str) -> str:
    """
    Creates a HIPAA-safe one-way hash of a patient identifier.
    The client_id is included as a salt so the same member_id
    at two different practices produces different hashes —
    this prevents cross-client correlation even if logs are compared.
    Never store or log the raw member_id. Always use this function.
    """
    salted = f"{client_id}:{member_id}"
    return hashlib.sha256(salted.encode()).hexdigest()[:16]

# Usage in any logging statement:
# WRONG:  logger.info(f"Verifying patient {patient.member_id}")
# RIGHT:  logger.info(f"Verifying patient {hash_patient_id(patient.member_id, client_id)}")
```

The 16-character truncation is intentional — it's long enough to be unique within a client's patient population while being short enough to be readable in log analysis. The full 64-character SHA-256 hash is never necessary for logging purposes.

---

## Every Place PHI Could Leak — Check All of These

**CloudWatch Logs** are the most common leak point. Every `logger.info()`, `logger.error()`, `logger.debug()`, and `print()` statement in your codebase is a potential leak. Before shipping any code, search the entire room's code directory for the strings `first_name`, `last_name`, `member_id`, `date_of_birth`, `dob`, `phone`, and `address`. If any of these appear inside a logging or print statement, replace them with hashed or redacted versions immediately.

**Exception handlers** are the second most common leak point. When an exception occurs and you log the exception details, Python will often include the full stack trace and the values of local variables. If a local variable holds a patient object at the time of the exception, the patient's PHI will appear in the error log. The correct pattern is to catch the exception, log a safe summary of what failed (which room, which payer, which operation), and separately log the hash of the patient identifier — never the raw exception object with full context.

**Skyvern task logs** are a less obvious leak point. When you send a Skyvern task that includes patient information in the prompt (first name, last name, date of birth for portal login), Skyvern may log that prompt internally. Always check Skyvern's data retention settings and confirm their HIPAA compliance documentation covers prompt logging before sending real patient data. In development, use only sandbox test patient data with fake names and fake member IDs.

**Error alert messages** sent via SNS or email are another common leak. When the incident_manager.py sends Adam an SMS saying "verification failed for patient," that SMS must contain only the hashed patient identifier, not the real name or member ID. SMS is not a HIPAA-secure channel.

**Test fixtures** committed to GitHub are a serious risk. Never use real patient data in test files, even for a quick local test. Always use the synthetic test patients defined in the testing-protocol skill. If you ever run a test with real data and generate a real 271 response, never save that response to a file that could be committed to git.

**Workflow-Use recordings** captured at a client's office will contain the real portal username and password of the clinic's Availity account, and may contain test patient data used during the recording session. The moment you export the JSON file, open it, find any username, password, or patient field values, replace them with `{{PLACEHOLDER}}` notation, and store the real values in AWS Secrets Manager before the file ever touches your computer's git-tracked folder.

---

## The Audit Log Standard

Every action ARIA takes must be logged to CloudWatch with this exact structure. The audit log is written before any EHR write — if the EHR write fails, the audit log still exists. This is both a HIPAA requirement and a debugging tool.

```python
audit_entry = {
    "timestamp": datetime.now(timezone.utc).isoformat(),
    "event_type": "verification_completed",  # or failed, queued, etc.
    "client_id": client_id,                  # the practice identifier
    "patient_id_hash": hash_patient_id(member_id, client_id),  # NEVER raw member_id
    "payer": payer_name,                     # "UnitedHealthcare" — not PHI
    "verification_path": "A",               # A = Availity API, B = Skyvern
    "confidence_score": 0.97,               # numeric score from normalizer
    "outcome": "pushed_to_ehr",             # or "queued_for_review", "staff_alert"
    "actor": "aria_agent_v1",
    "data_classification": "PHI_adjacent"   # this record references PHI by hash
}
```

Notice what is not in this structure: no patient name, no date of birth, no member ID in raw form, no address, no phone number. The hash is sufficient to correlate audit log entries with patient records during an investigation without exposing PHI in the logs themselves.

---

## The BAA Chain

Before any real patient data flows through ARIA in production, confirm this chain of signed Business Associate Agreements is complete. AWS BAA covers: Lambda, DynamoDB, Secrets Manager, CloudWatch, Bedrock, S3. The client's Availity account has its own BAA with Availity. Skyvern's enterprise tier includes a BAA — confirm this is signed before using Skyvern with real patient data. Keragon (if used for EHR bridging) provides an auto-BAA at signup. If any link in this chain is missing, ARIA cannot legally process real patient data regardless of how technically secure the implementation is.

---

## What To Do If You Suspect a PHI Leak

If you find code that may have already logged PHI, take these steps immediately. First, identify the CloudWatch log group where the leak may have occurred and note the time window. Second, alert Adam immediately — do not try to quietly fix it without disclosure. Third, do not delete the log entries — HIPAA requires preserving audit trails even of breaches. Fourth, the fix must address the root cause in code, not just the log entries. Fifth, if real patient data from a real client appears in logs, Adam needs to consult with a HIPAA compliance attorney about breach notification obligations within 60 days.
