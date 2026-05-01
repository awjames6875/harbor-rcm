# XY.ai Reverse Engineering Report
## Intelligence Gathered April 30, 2026 — For Harbor RCM

## Executive Summary
Based on a 54-minute intake call with David Yousefzadeh (Sales, XY.ai). XY.ai raised $3.5M seed, has 13-14 customers, one year in production. Standard pricing $5,000/agent/month, small org discount $2,500/month. Their core tech is a Chrome extension that records manual workflows and replays them via browser automation. Harbor RCM has a direct Availity API path at $0.003/verification that XY lacks entirely.

## Part 1: What XY.ai Actually Has In Production
- Insurance Verification: browser agent logs into payer portals, runs checks, writes back to EHR. One ASC customer has 15-20 portal recordings.
- Data Entry and Extraction: OCR reads PDFs, faxes, even cursive. Confidence scoring routes uncertain results to humans. Demo showed 30-second invoice transcription with editable fields.
- Claim Scrubbing: reviews claims before submission, cross-references notes and ICD-10 codes. Confirmed in production, not demo'd live.
- Prior Authorization: navigates portals to submit prior auth requests. Confirmed in production, not demo'd.
- Payment Posting: posts payments from EOBs to EHR. Confirmed in production, not demo'd.
- Knowledge Base RAG Chat: HIPAA-compliant document chat with configurable verbosity. Demo'd live.

## NOT In Production (David was transparent)
- Denial Management: "None of our customers is using this yet." Entirely roadmap.
- Self-Service Workflow Builder: engineers build all workflows manually today. Self-service is what they are building next.
- Patient Scheduling, Estimates, 360 Summary: mentioned but not demo'd.

## Part 2: XY.ai Technology Stack
- Browser Automation: proprietary Chrome extension capturing DOM/HTML code and screen visuals simultaneously. David said it "fingerprinted the code" meaning HTML element identifiers not pixel positions. Resilient to minor UI changes. Full redesign requires one new recording.
- Cloud: Google Cloud Enterprise with HIPAA BAA and SOC2. David did not know why Google over AWS.
- OCR Engine: multi-LLM confidence scoring. High confidence pushes automatically. Medium routes to human review. Low routes back to intake staff.
- Orchestration: custom-built platform with status queues (to-do, in progress, processed, revise). Not n8n or Temporal.
- Analytics: built-in dashboards tracking volume, errors, confidence trending daily/weekly/monthly/yearly.
- Reinforcement Learning: human corrections fed back into model. First month free is the fine-tuning period.

## Part 3: Feature Mapping to Harbor RCM
- XY Chrome Extension maps to Workflow-Use open source extension plus Skyvern Cloud.
- XY workflow orchestration maps to Python orchestrator plus DynamoDB state management.
- XY OCR engine maps to Claude via AWS Bedrock for document parsing.
- XY workflow queue UI maps to Harbor RCM React dashboard (Room 4, to be built).
- XY analytics maps to CloudWatch metrics plus custom analytics_tracker.py.
- XY Google Cloud maps to client-owned AWS account (Harbor RCM's infrastructure advantage).
- XY reinforcement learning maps to DynamoDB correction logging plus learning_engine.py in Room 3.
- KEY ADVANTAGE: Harbor RCM has direct Availity API at $0.003 per verification. XY is 100% browser-only with no API path.

## Part 4: Pricing Intelligence
- XY standard rate: $5,000 per agent per month.
- XY small org discount (offered to Adam): $2,500 per agent per month.
- XY first month: free for fine-tuning.
- XY tokens and usage charges: zero, covered under per-agent license.
- Harbor RCM Starter: $1,500/month, 40% cheaper than XY discounted rate.
- Harbor RCM Growth: $2,500/month for THREE agents vs XY charging that for ONE.
- Setup fee framing: "You are buying infrastructure you own forever. With XY you rent it."
- Salary comparison pitch stolen from David: ARIA at $1,500/month is $18K/year vs $30-40K plus benefits for front desk staff who call in sick and quit.

## Part 5: Doctor Meeting Talking Points (May 7th)
- Opening frame: "I met with XY.ai this week. They charge $2,500 to $5,000 per month per agent. I built something that does the same thing for $1,500 per month and your practice owns the infrastructure."
- Problem one: 100 inquiries per month times 8 minutes each equals 13 hours of staff time on verifications alone. ARIA does each in under 12 seconds.
- Problem two: when portal UIs change, staff has to relearn the process. ARIA self-heals with one new recording, takes three business days max.
- Problem three: no visibility into accuracy or trends. ARIA dashboard shows every verification, confidence score, and ROI every morning.
- Trust builder: first month free, same model XY uses. We tune ARIA to her specific payer mix before billing starts.

## Part 6: Build Priority Order
1. ARIA core verification pipeline with Availity API for top 3-4 payers (Phases 0 and 1).
2. Confidence scoring layer in Room 3 normalization.
3. Review queue dashboard in Room 4 with editable fields.
4. Analytics tracking in Room 4 showing ROI daily.
5. Workflow swap mechanism in Room 2 for self-healing portal updates.

## Part 7: XY.ai Platform UI From Screenshots
- Left sidebar navigation: Workflows, Files, Integrations, Browser Agents, Analytics, Settings.
- Workflow queue (27:46): status counters at top, tab filters for To Do/In Progress/Processing/Reviewed/Done, sortable table with vendor, status, processor, and timestamp columns.
- Document review (27:58): split-screen with original PDF on left with page thumbnails, extracted editable fields on right. Human can correct any field before pushing to EHR.
- Workflow builder (25:42): chat interface on right where user describes workflow in plain English, drag-drop canvas on left. Not yet available to customers.
- Create workflow modal (26:00): Workflow Name, Description, Category dropdown, Workflow Summary showing structured steps. User confirms before deploying.
- Multi-workflow dashboard (26:02): card-based layout showing AdvancedMD Create EHR Patient Demo, Email Notification Workflow, and Doc RTE. Confirms they support multiple EHR systems.

## Part 8: Harbor RCM Dashboard Spec
- Sidebar: Agents, Workflows, Recordings, Analytics, Settings.
- Verification Queue main screen: status bar across top (Pending, Verifying, Review Needed, Verified, Pushed to EHR), patient table with payer, appointment date, confidence score, path used, timestamp.
- Detail view: split-screen with raw 271 response on left, normalized editable fields on right. Color-coded confidence per field (green high, yellow medium, red low). Push to EHR button and Flag for Review button.
- Analytics: four metric cards (verifications this month, average confidence with trend arrow, time saved in hours, cost this month). Confidence trend line chart below. Volume by payer bar chart. Recent errors table.
