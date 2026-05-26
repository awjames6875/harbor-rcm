from __future__ import annotations

from normalizer_base import BenefitsObject

# Scoring weights (must sum to 1.0)
_COMPLETENESS_WEIGHT = 0.40
_PLAUSIBILITY_WEIGHT = 0.30
_PATTERN_WEIGHT = 0.30

# Tier thresholds (from CLAUDE.md)
_AUTO_PUSH_MIN = 95.0
_REVIEW_MIN = 80.0

# Fields that count toward completeness (excluding always-present fields and raw_response)
_SCORED_FIELDS = (
    "eligibility_date",
    "deductible_total",
    "deductible_remaining",
    "copay",
)

# Plausibility: expected max dollar values — anything above is suspicious
_MAX_DEDUCTIBLE = 20_000
_MAX_COPAY = 500


def score(obj: BenefitsObject) -> BenefitsObject:
    """
    Attach confidence_score and confidence_tier to a BenefitsObject.
    Always returns a new object — never mutates the input.
    """
    completeness = _score_completeness(obj)
    plausibility = _score_plausibility(obj)
    pattern = _score_pattern(obj)

    raw = (
        completeness * _COMPLETENESS_WEIGHT
        + plausibility * _PLAUSIBILITY_WEIGHT
        + pattern * _PATTERN_WEIGHT
    ) * 100

    confidence_score = round(raw, 2)
    confidence_tier = _tier(confidence_score)

    return obj.model_copy(update={
        "confidence_score": confidence_score,
        "confidence_tier": confidence_tier,
    })


def _score_completeness(obj: BenefitsObject) -> float:
    """0.0–1.0: fraction of expected optional fields that are non-None."""
    present = sum(1 for f in _SCORED_FIELDS if getattr(obj, f) is not None)
    return present / len(_SCORED_FIELDS)


def _score_plausibility(obj: BenefitsObject) -> float:
    """0.0–1.0: penalise values outside realistic ranges."""
    checks = 0
    passed = 0

    for field in ("deductible_total", "deductible_remaining"):
        val = getattr(obj, field)
        if val is not None:
            checks += 1
            try:
                if 0 <= float(val) <= _MAX_DEDUCTIBLE:
                    passed += 1
            except (ValueError, TypeError):
                pass  # non-numeric value — counts as failed

    if obj.copay is not None:
        checks += 1
        try:
            if 0 <= float(obj.copay) <= _MAX_COPAY:
                passed += 1
        except (ValueError, TypeError):
            pass

    # No financial fields present — plausibility is neutral (full weight)
    if checks == 0:
        return 1.0

    return passed / checks


def _score_pattern(obj: BenefitsObject) -> float:
    """
    0.0–1.0: match against known payer response patterns.
    Placeholder until DynamoDB history is available — returns full weight
    so the scorer is functional before historical data exists.
    """
    return 1.0


def _tier(score: float) -> str:
    if score >= _AUTO_PUSH_MIN:
        return "auto_push"
    if score >= _REVIEW_MIN:
        return "review"
    return "alert"
