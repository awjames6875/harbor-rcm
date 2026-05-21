---
name: harbor-rcm-availity-271-field-map
description: ALWAYS load this skill before writing or modifying any code in 3_clean-the-response that parses a 271 eligibility response. This skill is the translation dictionary for X12 271 EDI format — every field code, what it means in plain English, how each major payer formats their response differently, and what to do when a field is missing or ambiguous. Use this skill whenever writing normalizer functions, confidence scoring logic, or any code that reads a raw 271 response. Also use when debugging a verification that produced wrong benefits data.
---

# Harbor RCM — Availity 271 Field Translation Guide

The X12 271 Health Care Eligibility/Benefit Response is one of the most complex data formats in existence. Every insurance company is technically supposed to follow the same standard, but in practice each payer uses the standard differently — omitting fields the standard says are optional, using codes the standard allows but nobody documents well, and sometimes returning data in formats that technically violate the standard but have become industry conventions. This guide is your translation layer between that chaos and the clean canonical benefits object your EHR needs.

---

## The Structure of a 271 Response

A 271 response is organized into segments separated by tilde characters. Each segment starts with a two or three letter identifier that tells you what kind of data follows. The segments that matter most for insurance verification are these.

The **EB segment** (Eligibility or Benefit Information) is the most important segment in the entire 271. Every piece of coverage information lives here. A single 271 response may contain dozens of EB segments, each describing a different aspect of coverage. The EB segment has this structure: `EB*[coverage status]*[coverage level]*[service type code]*[insurance type]*[plan description]*[time period]*[benefit amount]*[percent]*[quantity qualifier]*[quantity]`.

The **SE segment** marks the end of the transaction. When you see SE, you have read all the EB segments for this patient.

The **AAA segment** (Request Validation) appears when the payer could not find the patient. This is how you know a patient is not enrolled in the plan being queried, as opposed to having active coverage with certain limitations.

---

## The Most Critical Field: Service Type Code

The third element of every EB segment is the Service Type Code. This single field determines what type of benefit the rest of the EB segment describes. Getting this wrong is the #1 cause of wrong benefits data in RCM systems. Here are the codes you will encounter most often.

**Code 30** means Health Benefit Plan Coverage. This is the general umbrella coverage status. When you see EB*1 with service type 30, the patient has active coverage in general. But this does NOT tell you the copay for a specific visit type — you need to look at more specific codes for that.

**Code 1** means Medical Care specifically. This is the code that contains the copay and deductible for primary care visits. Many practices only look at Code 30 and miss Code 1, resulting in wrong copay data.

**Code 98** means Professional Physician Visit — Office. This is even more specific than Code 1 and some payers use this code instead of Code 1 for office visit copays. If you find a copay under Code 98 but not Code 1, Code 98 wins for primary care.

**Code 33** means Chiropractic Care. **Code 35** means Dental Care. **Code 47** means Hospital — Room and Board. **Code 48** means Hospital — All Services. **Code 50** means Hospital Outpatient. **Code 86** means Emergency Services. **Code 88** means Pharmacy. For a primary care practice, you primarily care about codes 1, 30, and 98. For a behavioral health practice like Safe Harbor, you also care about Code MH (Mental Health) and Code SA (Substance Abuse).

---

## The Coverage Status Code (First Element of EB)

The very first field after EB tells you whether coverage is active. This is the field that determines whether the patient is insured at all.

**Code 1** means Active Coverage. The patient is currently enrolled and the plan is active. This is the result you want to see.

**Code 6** means Inactive. The patient was enrolled but coverage has lapsed. This is the most important alert to send to staff — the patient thinks they have insurance but they don't.

**Code 7** means Cancelled. Coverage was explicitly terminated.

**Code 8** means COBRA. The patient is on continuation coverage after losing employer coverage. Often has different cost sharing than active employee coverage.

**Code A** means Co-Insurance. The EB segment is describing a coinsurance rate rather than a status.

**Code B** means Co-Payment. The EB segment is describing a copay amount. When you see EB*B, the dollar amount later in that segment is the patient's copay for the service type specified in position 3.

**Code C** means Deductible. The EB segment is describing deductible information.

**Code D** means Benefit Disclaimer. Ignore these for primary benefits extraction — they contain legal language, not actionable data.

---

## How to Extract the Copay

The copay appears in EB segments where the first element is B (Co-Payment). The dollar amount is in the seventh position of the EB segment. Here is the extraction pattern.

```python
def extract_copay(eb_segments: list, service_type_priority: list = ["98", "1", "30"]) -> float | None:
    """
    Extracts the patient copay from a list of parsed EB segments.
    Tries service type codes in priority order because some payers
    put the copay under Code 98 while others use Code 1.
    Returns None if no copay is found (which itself is meaningful data
    — it may mean the patient has a deductible-only plan).
    """
    copay_segments = [seg for seg in eb_segments if seg.get("coverage_status") == "B"]
    
    for service_type in service_type_priority:
        matching = [seg for seg in copay_segments if seg.get("service_type") == service_type]
        if matching:
            amount = matching[0].get("benefit_amount")
            if amount and float(amount) > 0:
                return float(amount)
    
    return None  # None means no copay found — NOT zero copay. Log this distinction.
```

A return value of None is meaningfully different from a return value of 0.0. None means the payer did not send a copay field, which could mean the patient has a high-deductible plan with no copay, or it could mean the payer formatted their response in a non-standard way. Zero means the payer explicitly said the copay is zero (free visit). Always preserve this distinction in your canonical benefits object.

---

## Payer-Specific Quirks (The Hard-Won Knowledge)

**UnitedHealthcare** returns copay information under Service Type Code 98 primarily, not Code 1. If you look only at Code 1 for UHC patients, you will frequently find no copay and incorrectly assume the patient has a deductible-only plan. Always check Code 98 first for UHC.

**Aetna** sometimes returns two conflicting EB segments with different copay amounts — one under Code 1 and one under Code 30. When this happens, use the Code 1 amount because it is more specific. The Code 30 amount is usually the plan's generic out-of-network copay, not the in-network office visit copay.

**BCBS** varies significantly by state plan. BCBS of Oklahoma, BCBS of Texas, and BCBS of Illinois all format their 271 responses slightly differently. BCBS of Oklahoma (which is the most common for your Tulsa clients) puts deductible information in a separate EB segment with service type 30 and coverage status C, followed by a separate EB segment with the deductible-met-so-far amount. Always read both segments to calculate deductible remaining.

**Medicare** returns a non-standard format for Medicare Advantage plans versus Traditional Medicare. Traditional Medicare does not have a copay in the traditional sense — it has a Part B deductible and then 20% coinsurance. When you see a Medicare patient, check whether the plan description contains "Advantage" — if it does, treat it like a commercial plan with a copay. If it doesn't, the 20% coinsurance rule applies and there is no fixed copay to extract.

**SoonerCare** (Oklahoma Medicaid) does not use the Availity API at all — it requires the Skyvern browser path. This means you will never see a SoonerCare 271 response in your normalizer. If a SoonerCare patient somehow ends up in the normalization room, something went wrong in the routing logic and you should throw an error rather than attempting to normalize.

---

## The Canonical Benefits Object Your Normalizer Must Produce

Regardless of which payer, regardless of how messy the 271 was, the output of 3_clean-the-response must always conform to this exact shape. This is the contract with 4_send-and-log.

```python
from pydantic import BaseModel
from typing import Optional
from datetime import date

class CanonicalBenefits(BaseModel):
    # Coverage status
    coverage_active: bool                    # True if EB code 1 found, False otherwise
    coverage_status_code: str               # Raw code from 271: "1", "6", "7", "8", etc.
    plan_name: Optional[str]                # Human readable plan name if returned
    
    # Cost sharing
    copay: Optional[float]                  # None = not found, 0.0 = explicitly zero
    copay_service_type: Optional[str]       # Which service type code the copay came from
    deductible_total: Optional[float]       # Full year deductible amount
    deductible_met: Optional[float]         # Amount patient has already paid toward deductible
    deductible_remaining: Optional[float]   # Calculated: total minus met
    oop_max_total: Optional[float]          # Out of pocket maximum for the year
    oop_max_met: Optional[float]            # Amount patient has paid toward OOP max
    oop_max_remaining: Optional[float]      # Calculated: total minus met
    coinsurance_percent: Optional[float]    # e.g., 0.20 for 20% coinsurance
    
    # Prior authorization
    prior_auth_required: bool               # True if any EB segment indicates auth required
    prior_auth_service_types: list[str]     # Which service types require auth
    
    # Metadata
    payer_id: str                           # Availity payer ID used in the 270 request
    payer_name: str                         # Human readable payer name
    verification_date: date                 # Date the verification was run
    plan_begin_date: Optional[date]         # When coverage started
    plan_end_date: Optional[date]           # When coverage ends (None = ongoing)
    
    # Confidence
    confidence_score: float                 # Set by confidence_scorer.py, not by normalizer
    confidence_flags: list[str]             # Human-readable list of what lowered the score
```

Every field marked Optional can be None, and that is valid. A None value means the 271 did not contain that information, which is itself useful data for the confidence scorer. Never substitute a default value (like 0.0 for a missing deductible) because that would make a missing field look like an explicit zero, which could result in wrong data reaching the EHR.
