# Harbor RCM — API Reference
> Drop this file into your project root as `API_REFERENCE.md`  
> Claude Code will use this as context when writing any code in this repo.

---

## 1. Skyvern (Browser Agent — Portal Fallback)

**What it's for:** When an insurance payer has no API, Skyvern logs in and clicks through their web portal automatically.

### Install
```bash
pip install skyvern-python
```

### Initialize Client
```python
from skyvern import Skyvern

client = Skyvern(api_key="YOUR_API_KEY")
# In production, pull from AWS Secrets Manager — never hardcode
```

### Run a Single Task (One-Shot)
```python
from skyvern import Skyvern

async def run_eligibility_check(patient_id, payer_portal_url):
    client = Skyvern(api_key="YOUR_API_KEY")
    
    result = await client.run_task(
        prompt=f"Log in and run an eligibility check for patient ID {patient_id}",
        url=payer_portal_url,
        wait_for_completion=True,
        max_steps=20
    )
    
    print(result.status)   # "completed" or "failed"
    print(result.output)   # extracted coverage data
    return result
```

### Run with Structured Output (Preferred for ARIA)
```python
result = await client.run_task(
    prompt="Extract insurance coverage details for this patient",
    url=payer_portal_url,
    data_extraction_schema={
        "type": "object",
        "properties": {
            "active":           {"type": "boolean"},
            "deductible":       {"type": "number"},
            "deductible_met":   {"type": "number"},
            "copay":            {"type": "number"},
            "coinsurance":      {"type": "number"},
            "prior_auth_required": {"type": "boolean"},
            "plan_name":        {"type": "string"},
            "effective_date":   {"type": "string"},
            "termination_date": {"type": "string"}
        }
    },
    wait_for_completion=True,
    max_steps=25
)
```

### Run with Persistent Browser Session (Login Once, Reuse)
```python
# Use this so Skyvern doesn't have to log in fresh every single time
session = await client.create_browser_session()

result = await client.run_task(
    prompt="Run eligibility check for patient John Smith",
    url="https://portal.availity.com",
    browser_session_id=session.browser_session_id,
    wait_for_completion=True,
)

# Always close the session when done
await client.close_browser_session(session.browser_session_id)
```

### REST API (Alternative — No SDK Required)
```bash
curl -X POST https://api.skyvern.com/api/v2/run \
  -H "x-api-key: YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Check eligibility for patient ID 12345",
    "url": "https://portal.example-payer.com"
  }'
```

### Workflow (Multi-Step, Reusable)
```python
# Use workflows for complex multi-step flows (login → navigate → extract → logout)
workflow = await client.create_workflow(
    json_definition={
        "title": "Availity Eligibility Check",
        "persist_browser_session": True,
        "workflow_definition": {
            "parameters": [],
            "blocks": [
                {
                    "block_type": "navigation",
                    "label": "login",
                    "url": "https://apps.availity.com",
                    "navigation_goal": "Log in with the provided credentials"
                },
                {
                    "block_type": "navigation", 
                    "label": "run_eligibility",
                    "navigation_goal": "Navigate to Eligibility & Benefits and run a check for the patient"
                }
            ]
        }
    }
)
```

---

## 2. AWS boto3 (Secrets Manager + Bedrock + DynamoDB)

### Install
```bash
pip install boto3
```

### Secrets Manager — Get Credentials at Runtime
```python
import boto3
import json
from botocore.exceptions import ClientError

def get_secret(secret_name: str, region: str = "us-east-1") -> dict:
    """
    Pull credentials from AWS Secrets Manager.
    Never hardcode keys. Always call this at runtime.
    """
    session = boto3.session.Session()
    client = session.client(
        service_name='secretsmanager',
        region_name=region,
    )
    
    try:
        response = client.get_secret_value(SecretId=secret_name)
    except ClientError as e:
        error_code = e.response['Error']['Code']
        if error_code == 'ResourceNotFoundException':
            raise Exception(f"Secret '{secret_name}' not found in Secrets Manager")
        elif error_code == 'InvalidRequestException':
            raise Exception(f"Invalid request: {e}")
        elif error_code == 'DecryptionFailure':
            raise Exception(f"Cannot decrypt secret: {e}")
        else:
            raise e
    
    # Secret is stored as JSON string — parse it
    if 'SecretString' in response:
        return json.loads(response['SecretString'])
    else:
        # Binary secret (rare)
        return response['SecretBinary']

# Usage in Harbor RCM:
# secrets = get_secret("harbor-rcm/dev")
# skyvern_key = secrets["SKYVERN_API_KEY"]
# availity_client_id = secrets["AVAILITY_CLIENT_ID"]
# availity_client_secret = secrets["AVAILITY_CLIENT_SECRET"]
```

### DynamoDB — Write Verification Result
```python
import boto3
from decimal import Decimal

dynamodb = boto3.resource('dynamodb', region_name='us-east-1')

def write_verification_result(patient_id: str, result: dict):
    """Write a completed eligibility check to DynamoDB."""
    table = dynamodb.Table('harbor-rcm-verifications')
    
    table.put_item(
        Item={
            'patient_id':         patient_id,
            'timestamp':          result['timestamp'],
            'active':             result['active'],
            'payer_name':         result['payer_name'],
            'plan_name':          result['plan_name'],
            'deductible':         Decimal(str(result['deductible'])),
            'deductible_met':     Decimal(str(result['deductible_met'])),
            'copay':              Decimal(str(result['copay'])),
            'prior_auth_required': result['prior_auth_required'],
            'source':             result['source'],  # "availity_api" or "skyvern_fallback"
            'raw_response':       result['raw_response']
        }
    )
```

### DynamoDB — Batch Write (Multiple Patients)
```python
def batch_write_verifications(results: list):
    """Write multiple verification results at once (more efficient)."""
    table = dynamodb.Table('harbor-rcm-verifications')
    
    with table.batch_writer() as batch:
        for result in results:
            batch.put_item(Item=result)
```

### AWS Bedrock — Call Claude (For Normalization/Parsing)
```python
import boto3
import json

bedrock = boto3.client('bedrock-runtime', region_name='us-east-1')

def call_claude(prompt: str, system_prompt: str = None) -> str:
    """
    Call Claude via AWS Bedrock (HIPAA-eligible environment).
    Use this for parsing messy 271 responses into structured data.
    """
    messages = [{"role": "user", "content": prompt}]
    
    body = {
        "anthropic_version": "bedrock-2023-05-31",
        "max_tokens": 1000,
        "messages": messages
    }
    
    if system_prompt:
        body["system"] = system_prompt
    
    response = bedrock.invoke_model(
        modelId="anthropic.claude-3-sonnet-20240229-v1:0",
        body=json.dumps(body)
    )
    
    result = json.loads(response['body'].read())
    return result['content'][0]['text']

# Usage in ARIA normalization:
# raw_271 = "...messy EDI response..."
# parsed = call_claude(
#     prompt=f"Extract coverage details from this 271 response: {raw_271}",
#     system_prompt="Return only valid JSON. No explanation."
# )
```

### CloudWatch — HIPAA Audit Logging
```python
import boto3
import json
from datetime import datetime

logs = boto3.client('logs', region_name='us-east-1')

def audit_log(event_type: str, patient_id: str, details: dict):
    """
    Write every PHI access to CloudWatch for HIPAA audit trail.
    Required for every read/write of patient data.
    """
    log_entry = {
        "timestamp": datetime.utcnow().isoformat(),
        "event_type": event_type,           # e.g. "eligibility_check_started"
        "patient_id": patient_id,
        "details": details,
        "hipaa_event": True
    }
    
    logs.put_log_events(
        logGroupName='/harbor-rcm/audit',
        logStreamName=f'patient-{patient_id}',
        logEvents=[{
            'timestamp': int(datetime.utcnow().timestamp() * 1000),
            'message': json.dumps(log_entry)
        }]
    )
```

---

## 3. Availity (Insurance Eligibility API)

> ⚠️ Availity is a **private enterprise API** — not on Context7 or PyPI.  
> Docs are at: **developer.availity.com/docs**  
> You must have a registered application with `coverage` and `eligibility` scopes.

### Authentication (OAuth2 Client Credentials)
```python
import requests

def get_availity_token(client_id: str, client_secret: str) -> str:
    """Get a bearer token from Availity. Tokens expire — refresh as needed."""
    response = requests.post(
        "https://api.availity.com/availity/v1/token",
        data={
            "grant_type": "client_credentials",
            "client_id": client_id,
            "client_secret": client_secret,
            "scope": "hipaa"
        }
    )
    response.raise_for_status()
    return response.json()["access_token"]
```

### Eligibility Check (270/271 Transaction)
```python
def check_eligibility(token: str, patient: dict, payer_id: str) -> dict:
    """
    Send a 270 eligibility inquiry, get back a 271 response.
    patient = { first_name, last_name, dob, member_id, group_number }
    payer_id = Availity payer ID (e.g. "00001" for Aetna)
    """
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "controlNumber": "123456789",
        "tradingPartnerServiceId": payer_id,
        "provider": {
            "organizationName": "Safe Harbor Behavioral Health",
            "npi": "YOUR_NPI_HERE"
        },
        "subscriber": {
            "memberId": patient["member_id"],
            "firstName": patient["first_name"],
            "lastName": patient["last_name"],
            "dateOfBirth": patient["dob"],   # Format: YYYYMMDD
            "groupNumber": patient["group_number"]
        },
        "encounter": {
            "serviceTypeCodes": ["30"]  # "30" = Health Benefit Plan Coverage
        }
    }
    
    response = requests.post(
        "https://api.availity.com/availity/v1/coverages",
        headers=headers,
        json=payload
    )
    response.raise_for_status()
    return response.json()
```

> ⚠️ **Verify exact endpoint paths and payload schema** at developer.availity.com before going to production.  
> The sandbox base URL may differ from production. Confirm in their docs.

### Sandbox Test Patient (Maria Gonzalez)
```python
# Use this during development — safe test data, no real PHI
TEST_PATIENT = {
    "first_name": "MARIA",
    "last_name": "GONZALEZ",
    "dob": "19700101",
    "member_id": "ZZZ445554301",
    "group_number": "12345"
}

TEST_PAYER_ID = "00001"  # Verify correct sandbox payer ID in Availity docs
```

---

## 4. Pattern: Secrets → API Call (Full Example)

This is the pattern every file in `2_verification/code/` should follow:

```python
import asyncio
import boto3
import json
import requests
from skyvern import Skyvern

def get_credentials() -> dict:
    """Always pull from Secrets Manager. Never from .env or hardcode."""
    client = boto3.client('secretsmanager', region_name='us-east-1')
    response = client.get_secret_value(SecretId='harbor-rcm/dev')
    return json.loads(response['SecretString'])

async def verify_patient(patient: dict) -> dict:
    creds = get_credentials()
    
    # Step 1: Try Availity API first (fast, structured)
    try:
        token = get_availity_token(
            creds['AVAILITY_CLIENT_ID'],
            creds['AVAILITY_CLIENT_SECRET']
        )
        result = check_eligibility(token, patient, payer_id="00001")
        result['source'] = 'availity_api'
        return result
        
    except Exception as e:
        print(f"Availity API failed: {e} — falling back to Skyvern")
    
    # Step 2: Skyvern fallback (slower, works on any portal)
    skyvern = Skyvern(api_key=creds['SKYVERN_API_KEY'])
    result = await skyvern.run_task(
        prompt=f"Check insurance eligibility for {patient['first_name']} {patient['last_name']}",
        url="https://apps.availity.com",
        wait_for_completion=True
    )
    result.output['source'] = 'skyvern_fallback'
    return result.output
```

---

## 5. Quick Reference — Key URLs

| Service | Dev/Sandbox URL | Docs |
|---|---|---|
| Skyvern API | `https://api.skyvern.com/api/v2/` | docs.skyvern.com |
| Availity API | `https://api.availity.com/availity/v1/` | developer.availity.com/docs |
| AWS Bedrock | Via boto3 SDK | docs.aws.amazon.com/bedrock |
| AWS Secrets Manager | Via boto3 SDK | docs.aws.amazon.com/secretsmanager |
| AWS CloudWatch | Via boto3 SDK | docs.aws.amazon.com/cloudwatch |

---

## 6. Install All Dependencies (Run Once)

```powershell
# In your harbor-rcm project folder
py -m pip install boto3 requests pydantic skyvern-python python-dotenv
```

---

*Last updated: May 2026 — verify Availity payload schema against their live docs before production use.*
