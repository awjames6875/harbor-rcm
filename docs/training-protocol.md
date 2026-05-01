# training-protocol.md — ARIA Client Onboarding and Training Guide

## What This Document Is

This is the step-by-step playbook for training ARIA on a new client before going live. Every new Harbor RCM installation follows this protocol in order. Skipping steps will result in a poorly calibrated confidence scorer and higher human review rates during the first months of operation.

## Why Training Matters

ARIA does not come pre-trained on a specific practice. It comes with general knowledge of how Availity API responses are structured and what typical benefits data looks like. But every practice has a unique payer mix, unique plan configurations, and unique quirks in how their specific payers respond. A primary care doctor in Tulsa seeing mostly UHC and SoonerCare patients needs a very different baseline than a behavioral health agency in Oklahoma City seeing mostly Medicaid patients. The training process builds that client-specific baseline from their own historical data before ARIA ever touches a live patient.

## Pre-Training Checklist (Complete Before Running Any Code)

The client must have signed the Harbor RCM Business Associate Agreement. Never process any client data without a signed BAA on file. The client AWS account must be set up with Secrets Manager, CloudWatch, and DynamoDB configured. The client must have granted read access to their EHR historical data either through an API export, a CSV export, or direct database access depending on which EHR system they use. Adam must confirm the client is in the correct AWS environment and not accidentally connected to another client account. One client equals one AWS account, always.

## Step 1 — Export Historical Data From the EHR (15-30 minutes)

The goal is to extract twelve months of eligibility checks and claims from the client EHR. Six months is acceptable if twelve is not available. Less than three months produces a payer profile that is too thin to be reliable and the confidence scorer will default to conservative ranges for most payers.

For Dr. Chrono specifically, navigate to the Reports section, select Eligibility Report, set the date range to twelve months back from today, export as CSV, and save to the client onboarding folder. Also export the Claims Report for the same date range.

For TherapyNotes, navigate to Billing Reports, export the Insurance Billing Summary for twelve months, and export the Eligibility History if available.

For other EHR systems, contact Adam and document the export process here so future installs are faster.

## Step 2 — Run history_ingester.py (20-60 minutes depending on data volume)

Once the historical CSV files are in the correct folder, open VS Code to the harbor-rcm folder, open the terminal, and run the history ingester pointed at the client CSV files. The ingester will process each record, identify the payer, run it through the Room 3 normalization layer, and accumulate statistics for each payer profile. When it finishes it will print a summary showing how many transactions were processed, how many payer profiles were created, and any payers that had too few transactions to produce a reliable profile.

Review the summary before proceeding. Any payer with fewer than ten historical transactions will have an unreliable profile. For those payers, the confidence scorer will use conservative default ranges until enough live transactions accumulate to build a real profile. Note these payers so you can monitor their confidence scores more closely during the first month.

## Step 3 — Review the Payer Profiles in DynamoDB (10 minutes)

After history_ingester.py finishes, open the AWS DynamoDB console for this client account and navigate to the payer-profiles table. Review at least the top three payers by transaction volume. Confirm that the field_presence values look reasonable (most fields should show above 80% presence for major payers), that the value_ranges look realistic (copay values in the range of zero to one hundred dollars for most commercial plans), and that the denial_rate matches what the practice staff would expect from their experience.

If anything looks wrong, do not proceed to live operation. Investigate whether the historical data export was complete and whether the normalization rules correctly parsed the historical responses.

## Step 4 — Run a Test Batch With Sandbox Patients (30 minutes)

Before processing real patients, run ARIA against a batch of sandbox test patients to confirm the full pipeline works end to end. Use Availity sandbox credentials and Skyvern test mode. Confirm that results flow through normalization, get confidence scored correctly, and land in either the auto-push queue or the human review queue as expected. Confirm that CloudWatch audit logs are being written correctly. Confirm that the DynamoDB correction log table is accepting writes.

## Step 5 — Go Live (ongoing)

Switch from sandbox to production credentials in AWS Secrets Manager. Process the first real patient batch while monitoring CloudWatch logs in real time. Review the first day results in the analytics dashboard. Expect the human review rate to be slightly higher than normal during the first two weeks as the learning engine accumulates live corrections and refines the payer profiles. By week three the confidence scores should be stabilizing and the auto-push rate should be climbing toward 90% or higher for major payers.

## The Self-Improvement Timeline

During weeks one and two, the confidence scorer is primarily using the historical baseline from history_ingester.py. Human corrections during this period are especially valuable because they reveal discrepancies between the historical patterns and the live response patterns. Each correction makes the learning engine smarter faster.

By month one, the learning engine will have processed enough live corrections to start generating updated parsing rules for the client specific payer quirks. The human review rate should drop noticeably.

By month three, the payer profiles will reflect both the historical baseline and three months of live corrections. ARIA at this point should be handling the top three payers with above 95% confidence on most verifications.

By month six, ARIA will know this practice as well as an experienced billing specialist who has worked there for six months. The human review rate for well-established payers should be below 5%.

## DynamoDB Table Schema Reference

The payer-profiles table uses a composite key of client_id and payer_id. Each record contains sample_size as the number of historical transactions analyzed, field_presence as a map of field names to presence percentages, value_ranges as a map of field names to minimum and maximum values observed, format_patterns as a list of string descriptions of payer-specific quirks, denial_rate as a float between zero and one, last_updated as a timestamp, and version as an integer that increments each time learning_engine.py updates the profile.

The corrections table uses a composite key of client_id and correction_id. Each record contains payer_id, field_name, original_value, corrected_value, correction_timestamp, and applied_to_profile as a boolean that learning_engine.py sets to true after incorporating the correction into the payer profile.
