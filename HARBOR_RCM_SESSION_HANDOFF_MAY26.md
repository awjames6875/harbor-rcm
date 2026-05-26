# Harbor RCM — Session Handoff
**Date:** May 26, 2026  
**Session:** Phase 0 Complete + Phase 1 & 3 Partial Build  
**Next session starts at:** Step 19 (normalize_aetna.py)

---

## ✅ What Got Done Today

### Phase 0 — All Infrastructure Complete
Every account is set up. Every credential is stored. Nothing to redo.

| Item | Status | Details |
|---|---|---|
| Skyvern Cloud | ✅ Done | API key stored in AWS |
| Availity Developer App | ✅ Done | Harbor RCM app, Client ID: `03b0da9c-0f96-41fa-beb4-fcd141042716` |
| AWS Account | ✅ Done | GrowthGenix AI, Account: `981575076781`, Region: `us-east-1` |
| HIPAA BAA | ✅ Done | Signed in AWS Artifact — status: Active |
| AWS Bedrock | ✅ Done | Claude access requested, use case submitted |
| AWS Secrets Manager | ✅ Done | Secret name: `harbor-rcm/dev` in `us-east-1` |
| AWS IAM User | ✅ Done | `harbor-rcm-local-dev` with correct policies |
| AWS CLI | ✅ Done | Configured for `us-east-1`, `json` output |

### Phase 1 — Verification Room
| File | Status |
|---|---|
| `2_check-coverage/code/availity_client.py` | ✅ Written, correct against API docs |
| `2_check-coverage/tests/test_availity.py` | ✅ Mocked test passing (1 passed) |
| `2_check-coverage/code/payer_router.py` | ✅ Created |
| `2_check-coverage/code/skyvern_runner.py` | ✅ Created |
| `2_check-coverage/code/verification_handler.py` | ✅ Created |

### Phase 3 — Normalization Room
| File | Status |
|---|---|
| `3_clean-the-response/code/normalizer_base.py` | ✅ Done — BenefitsObject model + normalize() |
| `3_clean-the-response/code/normalize_uhc.py` | ✅ Done — UnitedHealthcare parser (Payer ID: 87726) |
| `3_clean-the-response/code/normalize_aetna.py` | ⏳ Next up |
| `3_clean-the-response/code/normalize_bcbs.py` | ⏳ After Aetna |

---

## 🔴 One Open Blocker

**Availity live API access is blocked.**

- Error: `unauthorized_client` on POST /v1/token
- Credentials are correct and verified character by character
- Subscription shows as Approved in My Apps
- This is an Availity portal configuration issue — not a code issue

**What to do about it:**
Send this email to Availity support:

```
To: developer@availity.com
Subject: unauthorized_client error — Harbor RCM app (Client ID: 03b0da9c)

App: Harbor RCM
Client ID: 03b0da9c-0f96-41fa-beb4-fcd141042716
Subscription: Healthcare HIPAA Transactions Demo (status: Approved)

I am receiving an unauthorized_client error on POST /v1/token 
using client_credentials grant type. The subscription shows 
as Approved in My Apps but the credentials are being rejected.

Can you verify my app credentials are correctly provisioned 
for the demo plan?

Thank you,
Adam James
GrowthGenix AI
```

**This blocker does NOT stop the build.** Everything can be built and tested with mocked responses. When Availity support fixes the access, we flip the sandbox flag to False and the real calls work automatically.

---

## 🔨 Where To Start Tomorrow

### Step 1 — Open Claude Code
Navigate to: `C:\Users\1alph\OneDrive\Desktop\rcm agent\`

### Step 2 — Paste This Prompt Into Claude Code

```
Create two more payer-specific parsers:

1. 3_clean-the-response/code/normalize_aetna.py
   - Comment at top: # Aetna-specific response parser — Payer ID: 60054
   - Function: normalize_aetna()
   - Same pattern as normalize_uhc.py

2. 3_clean-the-response/code/normalize_bcbs.py  
   - Comment at top: # BCBS-specific response parser — Payer ID: 00710
   - Function: normalize_bcbs()
   - Same pattern as normalize_uhc.py

Both should import BenefitsObject from normalizer_base.py,
call normalize() first to get the base object, then overlay
payer-specific financial fields using model_copy(update={}).

Add tests for both in 3_clean-the-response/tests/
following the same mock pattern as test_availity.py.
```

### Step 3 — After Aetna and BCBS Pass
Move to Room 1 (Intake). In Claude Code paste:

```
Create 1_receive-appointment/code/webhook_handler.py

This file should:
1. Accept incoming POST webhook from an EHR (DrChrono)
2. Parse the appointment payload into a patient dict with:
   - patient_first_name
   - patient_last_name  
   - patient_dob
   - member_id
   - payer_id
   - provider_npi
   - appointment_id
   - appointment_date
3. Validate all required fields are present
4. Return the clean patient dict or raise a ValueError with details

Add a test in 1_receive-appointment/tests/ with a sample 
DrChrono webhook payload.
```

---

## 📋 Full Build Checklist — Current Status

### PHASE 0 — Accounts & Access ✅ COMPLETE
- [x] Step 1: Skyvern Cloud signup + API key
- [x] Step 2: Availity Developer signup + sandbox credentials
- [x] Step 3: AWS account + HIPAA BAA signed
- [x] Step 4: AWS Bedrock enabled + Claude access requested
- [x] Step 5: AWS Secrets Manager — secret `harbor-rcm/dev` created
- [x] Step 6: AWS IAM user `harbor-rcm-local-dev` created + AWS CLI configured

### PHASE 1 — Verification Room 🔨 IN PROGRESS
- [x] Step 7: Python deps installed (boto3, requests, pydantic)
- [x] Step 8: `availity_client.py` written
- [x] Step 9: Mocked test passing (live test blocked — see blocker above)
- [x] Step 10: `skyvern_runner.py` created
- [x] Step 11: `verification_handler.py` created
- [ ] Step 12: End-to-end test (blocked pending Availity fix)

### PHASE 2 — Intake Room ⏳ NOT STARTED
- [ ] Step 13: `webhook_handler.py`
- [ ] Step 14: `input_validator.py`
- [ ] Step 15: `batch_processor.py`
- [ ] Step 16: Test: fake appointment triggers verification

### PHASE 3 — Normalization Room 🔨 IN PROGRESS
- [x] Step 17: `normalizer_base.py` ✅
- [x] Step 18: `normalize_uhc.py` ✅
- [ ] Step 19: `normalize_aetna.py` ← START HERE TOMORROW
- [ ] Step 20: `normalize_bcbs.py`
- [ ] Step 21: Test: raw 271 in → clean benefits object out

### PHASE 4 — Delivery Room ⏳ NOT STARTED
- [ ] Step 22: `ehr_poster.py`
- [ ] Step 23: `audit_logger.py`
- [ ] Step 24: `notifier.py`
- [ ] Step 25: Full pipeline end-to-end test

### PHASE 5 — Client Install ⏳ NOT STARTED
- [ ] Step 26-30: Deploy to client AWS, configure, test, hand off

---

## 🔑 Credentials Reference

**All credentials are stored in AWS Secrets Manager.**  
Secret name: `harbor-rcm/dev`  
Region: `us-east-1`  
Never store credentials in code or GitHub.

Your plaintext backup is in `harbor-rcm-keys.txt` on your Desktop — keep that file off GitHub.

---

## 🏗️ Repo Structure

```
harbor-rcm/
├── CLAUDE.md
├── PROJECT_KNOWLEDGE.md
├── 1_receive-appointment/     ← Intake (build after normalization)
│   └── CONTEXT.md
├── 2_check-coverage/          ← Verification (mostly done)
│   ├── code/
│   │   ├── availity_client.py     ✅
│   │   ├── payer_router.py        ✅
│   │   ├── skyvern_runner.py      ✅
│   │   └── verification_handler.py ✅
│   └── tests/
│       └── test_availity.py       ✅ passing
├── 3_clean-the-response/      ← Normalization (in progress)
│   ├── code/
│   │   ├── normalizer_base.py     ✅
│   │   ├── normalize_uhc.py       ✅
│   │   ├── normalize_aetna.py     ⏳
│   │   └── normalize_bcbs.py      ⏳
│   └── tests/
└── 4_deliver-results/         ← Delivery (not started)
    └── CONTEXT.md
```

---

## 💰 Business Context

- **Product:** Harbor RCM — automated insurance eligibility verification
- **Agent name:** ARIA
- **Pricing:** $5K setup + $1,500/month per client
- **First install:** Adam's doctor friend in Tulsa (after Safe Harbor pilot)
- **Pilot:** Safe Harbor Behavioral Health (Adam's agency)
- **Each client:** Gets their own AWS account — they pay AWS bills

---

*Last updated: May 26, 2026 — End of day*
