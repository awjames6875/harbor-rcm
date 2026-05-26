import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "code"))

from normalizer_base import BenefitsObject
from confidence_scorer import score

BASE = dict(
    patient_name="JAMES CARTER",
    member_id="W123456789",
    payer_name="Aetna",
    coverage_status="Active",
    raw_response={},
)


def _make(**kwargs) -> BenefitsObject:
    return BenefitsObject(**{**BASE, **kwargs})


def test_fully_populated_scores_auto_push():
    obj = _make(
        eligibility_date="2026-01-01",
        deductible_total="1500.00",
        deductible_remaining="800.00",
        copay="30.00",
    )
    result = score(obj)
    assert result.confidence_score >= 95.0
    assert result.confidence_tier == "auto_push"


def test_missing_all_financial_fields_scores_alert():
    obj = _make()  # no optional fields set
    result = score(obj)
    assert result.confidence_score < 80.0
    assert result.confidence_tier == "alert"


def test_partial_fields_scores_review():
    # Only deductible present — copay and eligibility_date missing
    obj = _make(
        deductible_total="2000.00",
        deductible_remaining="1000.00",
    )
    result = score(obj)
    assert 80.0 <= result.confidence_score < 95.0
    assert result.confidence_tier == "review"


def test_implausible_deductible_lowers_score():
    obj = _make(
        eligibility_date="2026-01-01",
        deductible_total="999999.00",  # wildly out of range
        deductible_remaining="500.00",
        copay="30.00",
    )
    result = score(obj)
    # One plausibility check fails — score should drop vs fully valid
    full_obj = _make(
        eligibility_date="2026-01-01",
        deductible_total="1500.00",
        deductible_remaining="800.00",
        copay="30.00",
    )
    assert result.confidence_score < score(full_obj).confidence_score


def test_score_always_sets_both_fields():
    obj = _make()
    result = score(obj)
    assert result.confidence_score is not None
    assert result.confidence_tier is not None


def test_score_does_not_mutate_input():
    obj = _make(copay="30.00", eligibility_date="2026-01-01")
    score(obj)
    assert obj.confidence_score is None
    assert obj.confidence_tier is None


def test_non_numeric_copay_counts_as_failed_plausibility():
    obj = _make(
        eligibility_date="2026-01-01",
        deductible_total="1500.00",
        deductible_remaining="800.00",
        copay="not-a-number",
    )
    result = score(obj)
    full = score(_make(
        eligibility_date="2026-01-01",
        deductible_total="1500.00",
        deductible_remaining="800.00",
        copay="30.00",
    ))
    assert result.confidence_score < full.confidence_score
