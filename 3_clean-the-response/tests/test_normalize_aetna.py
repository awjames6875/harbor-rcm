import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "code"))

from normalize_aetna import normalize_aetna

MOCK_AETNA_RESPONSE = {
    "subscriber": {"memberId": "W123456789"},
    "patient": {"firstName": "JAMES", "lastName": "CARTER"},
    "payer": {"name": "Aetna"},
    "plans": [
        {
            "status": "Active",
            "eligibilityStartDate": "2026-01-01",
            "benefits": [
                {
                    "amounts": {
                        "deductibles": {"total": "1500.00", "remaining": "800.00"},
                        "coPayment": {"value": "30.00"},
                    }
                }
            ],
        }
    ],
}


def test_normalize_aetna_patient_fields():
    result = normalize_aetna(MOCK_AETNA_RESPONSE)
    assert result.patient_name == "JAMES CARTER"
    assert result.member_id == "W123456789"
    assert result.payer_name == "Aetna"
    assert result.coverage_status == "Active"


def test_normalize_aetna_financial_fields():
    result = normalize_aetna(MOCK_AETNA_RESPONSE)
    assert result.eligibility_date == "2026-01-01"
    assert result.deductible_total == "1500.00"
    assert result.deductible_remaining == "800.00"
    assert result.copay == "30.00"


def test_normalize_aetna_missing_benefits():
    raw = {
        "subscriber": {"memberId": "W000000001"},
        "patient": {"firstName": "TEST", "lastName": "USER"},
        "payer": {"name": "Aetna"},
        "plans": [{"status": "Active"}],
    }
    result = normalize_aetna(raw)
    assert result.deductible_total is None
    assert result.deductible_remaining is None
    assert result.copay is None


def test_normalize_aetna_empty_plans():
    raw = {
        "subscriber": {"memberId": "W000000002"},
        "patient": {"firstName": "NO", "lastName": "PLAN"},
        "payer": {"name": "Aetna"},
        "plans": [],
    }
    result = normalize_aetna(raw)
    assert result.coverage_status == ""
    assert result.eligibility_date is None


def test_normalize_aetna_confidence_fields_unset_before_scoring():
    result = normalize_aetna(MOCK_AETNA_RESPONSE)
    assert result.confidence_score is None
    assert result.confidence_tier is None


def test_normalize_aetna_copay_scalar_still_works():
    raw = {**MOCK_AETNA_RESPONSE, "plans": [
        {
            "status": "Active",
            "eligibilityStartDate": "2026-01-01",
            "benefits": [{"amounts": {"coPayment": 40}}],
        }
    ]}
    result = normalize_aetna(raw)
    assert result.copay == "40"
