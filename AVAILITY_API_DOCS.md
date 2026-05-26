# Availity HIPAA Transactions API — Official Reference
> Scraped from developer.availity.com/portal/catalogue-products/healthcare-hipaa-transactions-demo-1  
> Use this as the authoritative source when writing any Availity API code.  
> Never guess at field names, endpoints, or payload structure — check here first.

---

## Authentication

### Token Endpoint
```
POST https://api.availity.com/availity/v1/token
```

### Token Request
```python
requests.post(
    "https://api.availity.com/availity/v1/token",
    data={
        "grant_type": "client_credentials",
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "scope": "hipaa"
    }
)
```

### Token Response
```json
{
  "access_token": "YOUR_BEARER_TOKEN",
  "expires_in": 3600
}
```

Use the token as: `Authorization: Bearer YOUR_BEARER_TOKEN`

---

## Coverages API 1.0.0
**Purpose:** Real-time eligibility and benefits inquiry — enables X12 270/271 transaction.

### ⚠️ Critical Note
Availity no longer supports `GET /v1/coverages`. Use only `POST /v1/coverages`.

---

### Endpoints

| # | Method | Path | Purpose |
|---|---|---|---|
| 1 | POST | `/v1/coverages` | Submit eligibility inquiry or search recent requests |
| 2 | GET | `/v1/coverages/{id}` | Retrieve specific coverage by ID |
| 3 | DELETE | `/v1/coverages/{id}` | Delete a specific coverage by ID |

**Base URL:** `https://api.availity.com/availity/v1/coverages`

---

### POST /v1/coverages — Request Parameters

**Content-Type:** `application/x-www-form-urlencoded`

| Parameter | Type | Required | Description |
|---|---|---|---|
| `payerId` | string | optional | Availity-specific identifier for patient's health plan |
| `providerLastName` | string | optional | Requesting provider's last name |
| `providerFirstName` | string | optional | Requesting provider's first name |
| `providerNpi` | string | optional | Provider's NPI — most payers require this |
| `providerTaxId` | string | optional | Provider's tax ID |
| `memberId` | string | optional | Patient's health plan member ID |
| `patientLastName` | string | optional | Patient's last name |
| `patientFirstName` | string | optional | Patient's first name |
| `patientMiddleName` | string | optional | Patient's middle name |
| `patientBirthDate` | date | optional | Patient's date of birth |
| `patientGender` | string | optional | Patient's gender |
| `patientState` | string | optional | Two-character state abbreviation |
| `groupNumber` | string | optional | Patient's health plan group number |
| `subscriberRelationship` | string | optional | Patient's relationship to subscriber |
| `serviceType` | string | optional | Type of service (use `30` for health benefit plan coverage) |
| `asOfDate` | string | optional | Date of service for coverage check |

### subscriberRelationship Values
| Code | Meaning |
|---|---|
| `18` | Self |
| `01` | Spouse |
| `19` | Child |
| `G8` | Other relationship |

---

### POST /v1/coverages — Sample Request

```bash
curl --request POST \
  --url https://api.availity.com/availity/v1/coverages/ \
  --header 'Authorization: Bearer YOUR_TOKEN' \
  --header 'Content-Type: application/x-www-form-urlencoded' \
  --data payerId=123 \
  --data providerNpi=1234567893 \
  --data providerLastName=SMITH \
  --data 'serviceType[]=30' \
  --data memberId=ABC123 \
  --data patientBirthDate=1990-01-01 \
  --data patientLastName=LAST \
  --data patientFirstName=FIRST \
  --data patientGender=M \
  --data patientState=FL \
  --data subscriberRelationship=18
```

### POST /v1/coverages — Sample Response

```json
{
  "links": {
    "self": {
      "href": "https://api.availity.com/availity/v1/coverages/1234567890"
    }
  },
  "id": "1234567890",
  "customerId": "1234",
  "statusCode": "4",
  "asOfDate": "2024-02-01T05:00:00.000+0000",
  "subscriber": {
    "memberId": "ABC123456789"
  },
  "patient": {
    "firstName": "FIRST",
    "lastName": "LAST"
  },
  "payer": {
    "name": "HealthPlanOne",
    "payerId": "123"
  }
}
```

---

### Status Codes

| Code | Status | Definition |
|---|---|---|
| `0` | In Progress | Availity is retrieving coverage from health plan |
| `19` | Request Error | Health plan returned validation messages |
| `R1` | Communication Error, Retrying | Health plan didn't respond, retrying |
| `7` | Communication Error | Health plan didn't respond |
| `13` | Communication Error | Health plan response was invalid |
| `14` | Communication Error | Health plan didn't respond |
| `15` | Communication Error | Health plan down for maintenance |
| `4` | Complete | Successfully retrieved |
| `3` | Complete (Invalid Response) | Retrieved but partially invalid |

---

### Sandbox Demo Testing

To test the demo API, add this header to your request:

```python
headers = {
    "Authorization": f"Bearer {token}",
    "X-Api-Mock-Scenario-ID": "Coverages-Complete-i"  # Use this for success testing
}
```

| Scenario ID | Status Code | Definition |
|---|---|---|
| `Coverages-Complete-i` | 200 | Successfully retrieved coverage |
| `Coverages-PayerError1-i` | 200 | Provider ineligible for inquiries |
| `Coverages-PayerError2-i` | 200 | Subscriber name invalid |
| `Coverages-InProgress-i` | 202 | Still retrieving |
| `Coverages-Retrying-i` | 202 | Retrying after no response |
| `Coverages-RequestError1-i` | 400 | Input validation failed |
| `Coverages-RequestError2-i` | 400 | Input validation failed |

---

### Coverage Response Object — Key Fields

#### Top Level
| Field | Type | Definition |
|---|---|---|
| `id` | string | Unique response ID for follow-up GET requests |
| `statusCode` | string | See status codes table above |
| `status` | string | Human-readable status |
| `asOfDate` | datetime | Date coverage was checked |
| `subscriber` | object | Subscriber information |
| `patient` | object | Patient information |
| `payer` | object | Payer information |
| `plans` | array | Array of health plan coverage details |

#### plans[] Object — What ARIA Needs
| Field | Type | Definition |
|---|---|---|
| `status` | string | Coverage status (e.g., "active") |
| `statusCode` | string | Coverage status code |
| `groupNumber` | string | Patient's group number |
| `groupName` | string | Patient's group name |
| `eligibilityStartDate` | datetime | When eligibility began |
| `eligibilityEndDate` | datetime | When eligibility ends |
| `benefits` | array | Array of benefit details |

#### plans[].benefits[].amounts Object
| Field | Type | Definition |
|---|---|---|
| `coPayment` | object | Copay amounts |
| `outOfPocket` | object | Out-of-pocket amounts |
| `deductibles` | object | Deductible amounts |
| `coInsurance` | object | Coinsurance amounts |

---

### GET /v1/coverages/{id}

Use the `id` from the POST response to poll for results when status is `In Progress`.

```bash
curl -X GET "https://api.availity.com/availity/v1/coverages/{id}" \
  --header 'Authorization: Bearer YOUR_TOKEN'
```

---

## Correct Python Implementation

```python
import requests
import boto3
import json

AVAILITY_TOKEN_URL = "https://api.availity.com/availity/v1/token"
AVAILITY_COVERAGES_URL = "https://api.availity.com/availity/v1/coverages"

def get_token(client_id: str, client_secret: str) -> str:
    response = requests.post(
        AVAILITY_TOKEN_URL,
        data={
            "grant_type": "client_credentials",
            "client_id": client_id,
            "client_secret": client_secret,
            "scope": "hipaa"
        },
        timeout=10
    )
    response.raise_for_status()
    return response.json()["access_token"]

def check_coverage(token: str, patient: dict, payer_id: str, provider_npi: str, sandbox: bool = True) -> dict:
    """
    patient = {
        "member_id": "ABC123",
        "last_name": "GONZALEZ",
        "first_name": "MARIA",
        "birth_date": "1970-01-01",   # YYYY-MM-DD
        "gender": "F",
        "state": "OK",
        "group_number": "12345"
    }
    """
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/x-www-form-urlencoded"
    }

    # Add sandbox mock header for testing
    if sandbox:
        headers["X-Api-Mock-Scenario-ID"] = "Coverages-Complete-i"

    data = {
        "payerId": payer_id,
        "providerNpi": provider_npi,
        "memberId": patient["member_id"],
        "patientLastName": patient["last_name"],
        "patientFirstName": patient["first_name"],
        "patientBirthDate": patient["birth_date"],
        "patientGender": patient.get("gender", ""),
        "patientState": patient.get("state", ""),
        "groupNumber": patient.get("group_number", ""),
        "serviceType[]": "30",          # 30 = Health Benefit Plan Coverage
        "subscriberRelationship": "18"  # 18 = Self
    }

    response = requests.post(
        AVAILITY_COVERAGES_URL,
        headers=headers,
        data=data,
        timeout=10
    )
    response.raise_for_status()
    return response.json()
```

---

## Sandbox Test Patient

Use this during all development and testing. Never use real PHI.

```python
TEST_PATIENT = {
    "member_id": "ZZZ445554301",
    "last_name": "GONZALEZ",
    "first_name": "MARIA",
    "birth_date": "1970-01-01",
    "gender": "F",
    "state": "FL",
    "group_number": "12345"
}

TEST_PAYER_ID = "MOCKPAYER"   # Verify correct sandbox payer ID in Availity docs
```

---

## Payer List API

Use this to get valid `payerId` values for any insurance company.

```bash
GET https://api.availity.com/availity/v1/availity-payer-list?transactionType=270&submissionMode=API
Authorization: Bearer YOUR_TOKEN
```

Returns list of payers with their `payerId` values for eligibility checks.

---

## ⚠️ Common Code Mistakes To Avoid

| Wrong | Correct |
|---|---|
| Endpoint: `.../eligibility-inquiries` | Endpoint: `.../coverages` |
| Field: `trading_partner_id` | Does not exist — remove it |
| Field: `dateOfBirth` | Field: `patientBirthDate` |
| Content-Type: `application/json` | Content-Type: `application/x-www-form-urlencoded` |
| POST body as JSON | POST body as form data |

---

*Source: developer.availity.com — Healthcare HIPAA Transactions Demo documentation*  
*Last saved: May 2026*
