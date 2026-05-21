# CONTEXT.md — 4_send-and-log (EHR Writing, Review Queue, Analytics, Alerts)
## Purpose
Writes verified benefits to EHR, provides review queue for uncertain results, tracks analytics for ROI visibility, sends staff alerts. This is what the doctor sees daily.

## Key Files
- ehr_poster.py — writes to Dr. Chrono API
- audit_logger.py — HIPAA CloudWatch logging (7 year retention)
- notifier.py — staff alerts via SMS/email/Slack
- review_queue.py — NEW: editable review interface with queue states (Pending, In Review, Corrected, Auto-Pushed, Failed)
- analytics_tracker.py — NEW: verifications/month, confidence trending, Path A vs B, error rate by payer, time saved, cost per verification

## Dashboard (React app)
Sidebar: Agents, Workflows, Queue, Analytics, Settings
Main view: metric cards, confidence trend chart, volume by payer, attention-needed table

## Rules
- Always write audit log BEFORE writing to EHR
- Never display full patient names (first initial + last only)
- Never delete review queue items (state changes only)
- Always log human corrections for Room 3 learning engine
- Always include actionable instructions in staff alerts
# incident_manager.py — Automated Runbook and Self-Healing System
# Belongs in: 4_send-and-log/code/incident_manager.py
# Triggered by: CloudWatch Alarms via Lambda

## What This File Does

This module is ARIA's immune system. When something goes wrong anywhere in the
pipeline, this file wakes up, figures out what happened, tries to fix it
automatically if possible, and writes a complete incident record to DynamoDB
regardless of whether the fix succeeded. The result is a self-writing runbook
that documents every problem and resolution without any human intervention.

## The Five Incident Severity Levels

SEV-1 means PHI is at risk or HIPAA audit logging has failed. This pages Adam
immediately and halts all verification processing until resolved manually. This
level should almost never trigger if the architecture is correctly implemented.

SEV-2 means verification is completely down for one or more payers. Patients
are not getting verified. Adam gets an immediate SMS and the incident manager
attempts auto-recovery.

SEV-3 means verification is degraded — higher than normal error rates, slower
than normal response times, or elevated human review rates. Adam gets a
notification within fifteen minutes. Auto-recovery is attempted.

SEV-4 means a single verification failed but the system is otherwise healthy.
The incident is logged automatically and the verification is retried. Adam gets
a daily digest rather than an immediate alert.

SEV-5 means a minor anomaly was detected but resolved itself. Logged for
pattern analysis only. No alert sent.

## Auto-Recovery Playbook (What the System Fixes Itself)

Expired Availity OAuth token: incident manager calls get_availity_token() to
refresh the credential in Secrets Manager, then retries the failed
verification. Logs the refresh event with the new token expiration time.

Skyvern task timeout: incident manager resubmits the task with a higher
max_steps limit and a fresh browser session. If it fails again, escalates to
SEV-2 and alerts Adam.

Lambda cold start timeout: incident manager increases the Lambda timeout
setting via AWS SDK, then retries. Logs the new timeout value.

DynamoDB throughput exceeded: incident manager switches the table to
on-demand billing mode temporarily, then logs the capacity event so Adam can
review whether the provisioned capacity needs a permanent increase.

Availity API 5xx error: incident manager waits 60 seconds and retries up to
three times. If all retries fail, checks Availity status page via HTTP and
includes the status in the incident record so Adam immediately knows whether
it is an Availity outage or a local issue.

## The Incident Record Schema (Written to DynamoDB incidents table)

incident_id: UUID generated at incident creation time
client_id: which practice this incident belongs to
timestamp: ISO format UTC timestamp when the incident was detected
severity: SEV-1 through SEV-5
room: which room the error originated in (1_patient-arrives, 2_check-coverage, etc.)
error_type: short category label like TOKEN_EXPIRED or SKYVERN_TIMEOUT
error_message: the raw error message from CloudWatch
stack_trace: the full Python traceback if available
payer: which payer was being processed when the error occurred
claude_diagnosis: the plain-English explanation Claude generated via Bedrock
claude_recommended_fix: the step-by-step fix Claude recommended
auto_resolution_attempted: boolean
auto_resolution_successful: boolean
auto_resolution_description: what the auto-recovery code actually did
manual_resolution_notes: field for Adam to fill in if manual fix was needed
status: open, auto-resolved, manually-resolved, or escalated
time_to_resolution_seconds: calculated when status changes from open

## The Claude Bedrock Call (How ARIA Thinks About Its Own Errors)

The incident manager sends Claude this prompt with the error context filled in:
"You are analyzing an error in ARIA, a healthcare insurance verification
system. Here is the error context: [error message, stack trace, room, payer,
last ten CloudWatch log lines]. Provide three things: first, a one-sentence
plain English explanation of what went wrong suitable for a non-technical
medical practice owner. Second, a technical root cause diagnosis. Third, a
recommended fix with specific steps. Format your response as JSON with keys
explanation, root_cause, and recommended_fix."

Claude returns structured JSON that the incident manager parses and stores
directly into the DynamoDB incident record. No human has to write anything.

## The Morning Digest

Every day at 7am local time for the client, the incident manager sends a
daily digest SMS and email summarizing the previous 24 hours: total
verifications processed, number of incidents detected, number auto-resolved,
number requiring manual attention, and the current system health status as a
single emoji — green circle for healthy, yellow circle for degraded, red
circle for down. The doctor sees one message every morning that tells her
everything she needs to know about how ARIA performed overnight.
