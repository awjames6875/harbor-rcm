# Harbor RCM — Client Install SOP
> For: Adam James / GrowthGenix AI  
> Use this every time you install Harbor RCM at a new client.  
> Target time: 30-45 minutes once you know the steps.

---

## Pre-Install Checklist

Before you show up (physically or on Zoom), confirm you have:

- [ ] Client's business email address (for AWS account)
- [ ] Client's credit card (for AWS billing — they pay, not you)
- [ ] Client's NPI number (for Availity API calls)
- [ ] Client's Availity login (if they already have one)
- [ ] Client's EHR name and API access (DrChrono, Athena, etc.)
- [ ] Your laptop with AWS CLI installed and working
- [ ] Your `harbor-rcm` repo cloned locally

---

## PHASE 0 — Accounts & Access

### STEP 1 — Skyvern Cloud
**Time: 3 minutes**

1. Go to **app.skyvern.com**
2. Click Sign Up → use client's Google or email
3. Profile icon → Settings → API Keys
4. Click the copy icon next to the existing key
5. Save to temp notepad as `SKYVERN_API_KEY`

✅ **Done when:** You have a key copied

---

### STEP 2 — Availity Developer Account
**Time: 10 minutes**

1. Go to **developer.availity.com**
2. Sign Up → verify email
3. Log in → My Apps → **+ Create a New App**
4. Name: `Harbor RCM` | Description: `Automated insurance eligibility verification`
5. Redirect URL: leave as `https://availity.com/`
6. Click **Create App**
7. Go to **API Products** → find **Healthcare HIPAA Transactions Demo**
8. Click More Info → **Access With This Plan** (Demo — 500 calls/day free)
9. Cart → Select **Existing App** → choose **Harbor RCM** → Submit Request
10. Go back to **My Apps** → Harbor RCM → find **Credentials** tab
11. Copy **Client ID** and **Client Secret** to notepad

✅ **Done when:** You have Client ID + Client Secret

---

### STEP 3 — AWS Account + HIPAA BAA
**Time: 10 minutes**

1. Go to **console.aws.amazon.com**
2. Click **Create a new AWS Account**
3. Use client's business email
4. Account name: Client's business name (e.g. `Tulsa Primary Care`)
5. Choose **Free tier** (6 months, $200 credits)
6. Complete phone verification + credit card
7. Once inside console → search **AWS Artifact**
8. Click **Agreements** → find **AWS Business Associate Addendum**
9. Select it → click **Accept Agreement**
10. Accept the NDA popup → click **Accept NDA and download**

✅ **Done when:** BAA status shows **Active**

---

### STEP 4 — Enable AWS Bedrock
**Time: 2 minutes**

1. Search **Bedrock** in AWS console
2. Click **Model catalog** in left menu
3. Click **Submit use case details** if prompted
4. Fill in:
   - Company: client's business name
   - Industry: Healthcare
   - Use case: `Automated insurance eligibility verification for medical practices using Claude via Bedrock in a HIPAA-eligible environment`
5. Submit

✅ **Done when:** No error — models are auto-enabled on first use

---

### STEP 5 — AWS Secrets Manager
**Time: 5 minutes**

1. Search **Secrets Manager** in AWS console
2. Click **Store a new secret**
3. Choose **Other type of secret**
4. Add these key/value pairs:
   - `SKYVERN_API_KEY` → paste from notepad
   - `AVAILITY_CLIENT_ID` → paste from notepad
   - `AVAILITY_CLIENT_SECRET` → paste from notepad
5. Click Next
6. Secret name: `harbor-rcm/prod`
7. Click Next → Next → **Store**
8. Copy the **Secret ARN** — save to notepad

✅ **Done when:** Secret `harbor-rcm/prod` shows in list

---

### STEP 6 — IAM User + AWS CLI
**Time: 5 minutes**

**Create IAM User:**
1. Search **IAM** → Users → **Create user**
2. Username: `harbor-rcm-local-dev`
3. Do NOT check console access
4. Click Next → **Do not attach any policies** → **Create user**
5. Click into the new user → **Permissions** tab → **Add permissions** → **Create inline policy**
6. Switch to the **JSON** editor and paste this policy (replace `ACCOUNT_ID` with the client's 12-digit AWS account number):

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "SecretsReadOnly",
      "Effect": "Allow",
      "Action": "secretsmanager:GetSecretValue",
      "Resource": "arn:aws:secretsmanager:us-east-1:ACCOUNT_ID:secret:harbor-rcm/*"
    },
    {
      "Sid": "BedrockInvoke",
      "Effect": "Allow",
      "Action": "bedrock:InvokeModel",
      "Resource": "arn:aws:bedrock:us-east-1::foundation-model/anthropic.*"
    },
    {
      "Sid": "CloudWatchLogsWrite",
      "Effect": "Allow",
      "Action": [
        "logs:CreateLogGroup",
        "logs:CreateLogStream",
        "logs:PutLogEvents"
      ],
      "Resource": "arn:aws:logs:us-east-1:ACCOUNT_ID:log-group:harbor-rcm*:*"
    }
  ]
}
```

7. Click **Next** → Policy name: `harbor-rcm-least-privilege` → **Create policy**
8. Click the user → **Security credentials** → **Create access key**
9. Choose **Local code** → check confirmation box → Next
10. Description: `Harbor RCM local development access`
11. Click **Create access key**
12. Copy **Access Key ID** and **Secret Access Key** to notepad immediately

> ⚠️ **Security note:** This key should only ever be used on the client's install laptop. Rotate it every 90 days via IAM → Security credentials → **Make inactive** then **Create access key**. Delete the old key after rotation.

**Configure AWS CLI on your laptop:**
```powershell
aws configure
```
Enter:
- Access Key ID: (paste)
- Secret Access Key: (paste)
- Region: `us-east-1`
- Output format: `json`

**Verify it works:**
```powershell
aws sts get-caller-identity
```
Should return the client's Account ID without errors.

✅ **Done when:** `aws sts get-caller-identity` returns account info

---

## PHASE 0 Complete — Credential Handoff

At this point you should have in your notepad:

| Key | Where It Came From |
|---|---|
| `SKYVERN_API_KEY` | Skyvern dashboard |
| `AVAILITY_CLIENT_ID` | Availity My Apps |
| `AVAILITY_CLIENT_SECRET` | Availity My Apps |
| `AWS_ACCESS_KEY_ID` | IAM user |
| `AWS_SECRET_ACCESS_KEY` | IAM user |
| `SECRET_ARN` | Secrets Manager |

**Delete the notepad file** after confirming all keys are in Secrets Manager.

---

## PHASE 1 — Deploy ARIA Code

### STEP 7 — Install Python Dependencies
```powershell
cd "C:\path\to\client\harbor-rcm"
py -m pip install boto3 requests pydantic skyvern-python
```

### STEP 8 — Configure Client Credentials in Code
Update `2_check-coverage/code/config.py`:
```python
SECRET_NAME = "harbor-rcm/prod"
REGION = "us-east-1"
CLIENT_NPI = "CLIENT_NPI_HERE"
```

### STEP 9 — Run Test With Sandbox Patient
```powershell
cd "2_check-coverage/code"
py verification_handler.py --test
```

Expected output:
```
✅ Availity API connected
✅ Test patient verified
✅ Coverage: Active | Deductible: $1,200 | Copay: $30
✅ Result written to DynamoDB
Total time: 8.3 seconds
```

### STEP 10 — Connect To Client EHR
- DrChrono: Get API token from client's DrChrono account
- Add to Secrets Manager as `DRCHRONO_API_TOKEN`
- Test webhook endpoint

---

## Post-Install Checklist

- [ ] ARIA running end-to-end with sandbox patient
- [ ] Client's EHR connected and receiving results
- [ ] CloudWatch logs showing HIPAA audit trail
- [ ] Staff trained on reading the results
- [ ] Client has dashboard access
- [ ] Invoice sent ($5K setup fee)

---

## Common Errors & Fixes

| Error | Fix |
|---|---|
| `aws: command not found` | Install AWS CLI from awscli.amazonaws.com/AWSCLIV2.msi, restart PowerShell |
| Availity 401 Unauthorized | Token expired — re-run `get_availity_token()` |
| Secrets Manager access denied | Check IAM user has `SecretsManagerReadWrite` policy |
| Bedrock ThrottlingException | Wait 30 seconds and retry — rate limit hit |
| Skyvern task failed | Check portal URL is correct and credentials in Secrets Manager are valid |

---

## Time Tracker

| Phase | First Install | Subsequent Installs |
|---|---|---|
| Phase 0 — Accounts | 2-3 hours | 30-45 minutes |
| Phase 1 — Deploy Code | 2-3 hours | 15-20 minutes |
| Phase 2 — EHR Connect | 1-2 hours | 30-60 minutes |
| Staff Training | 1 hour | 1 hour |
| **Total** | **6-9 hours** | **2-3 hours** |

---

*Last updated: May 2026 — Update this doc after each install with any new errors or fixes you discover.*
