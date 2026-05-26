import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "code"))

from normalize_bcbs import normalize_bcbs

MOCK_BCBS_RESPONSE = {
    "subscriber": {"memberId": "XBL987654321"},
    "patient": {"firstName": "LINDA", "lastName": "TORRES"},
    "payer": {"name": "BlueCross BlueShield"},
    "plans": [
        {
            "status": "Active",
            "eligibilityStartDate": "2026-01-01",
            "benefits": [
                {
                    "amounts": {
                        "deductibles": {"total": "2000.00", "remaining": "1200.00"},
                        "coPayment": {"value": "25.00"},
                    }
                }
            ],
        }
    ],
}


def test_normalize_bcbs_patient_fields():
    result = normalize_bcbs(MOCK_BCBS_RESPONSE)
    assert result.patient_name == "LINDA TORRES"
    assert result.member_id == "XBL987654321"
    assert result.payer_name == "BlueCross BlueShield"
    assert result.coverage_status == "Active"


def test_normalize_bcbs_financial_fields():
    result = normalize_bcbs(MOCK_BCBS_RESPONSE)
    assert result.eligibility_date == "2026-01-01"
    assert result.deductible_total == "2000.00"
    assert result.deductible_remaining == "1200.00"
    assert result.copay == "25.00"


def test_normalize_bcbs_missing_benefits():
    raw = {
        "subscriber": {"memberId": "XBL000000001"},
        "patient": {"firstName": "TEST", "lastName": "USER"},
        "payer": {"name": "BlueCross BlueShield"},
        "plans": [{"status": "Active"}],
    }
    result = normalize_bcbs(raw)
    assert result.deductible_total is None
    assert result.deductible_remaining is None
    assert result.copay is None


def test_normalize_bcbs_empty_plans():
    raw = {
        "subscriber": {"memberId": "XBL000000002"},
        "patient": {"firstName": "NO", "lastName": "PLAN"},
        "payer": {"name": "BlueCross BlueShield"},
        "plans": [],
    }
    result = normalize_bcbs(raw)
    assert result.coverage_status == ""
    assert result.eligibility_date is None


def test_normalize_bcbs_confidence_fields_unset_before_scoring():
    result = normalize_bcbs(MOCK_BCBS_RESPONSE)
    assert result.confidence_score is None
    assert result.confidence_tier is None


def test_normalize_bcbs_copay_scalar_still_works():
    raw = {**MOCK_BCBS_RESPONSE, "plans": [
        {
            "status": "Active",
            "eligibilityStartDate": "2026-01-01",
            "benefits": [{"amounts": {"coPayment": 50}}],
        }
    ]}
    result = normalize_bcbs(raw)
    assert result.copay == "50"
