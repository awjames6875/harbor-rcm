# BCBS-specific response parser — Payer ID: 00710

from normalizer_base import BenefitsObject, normalize, _extract_copay_amount


def normalize_bcbs(raw: dict) -> BenefitsObject:
    base = normalize(raw)
    plans = raw.get("plans", [])
    plan = plans[0] if plans else {}

    deductible_total = None
    deductible_remaining = None
    copay = None

    for benefit in plan.get("benefits", []):
        amounts = benefit.get("amounts", {})

        deductibles = amounts.get("deductibles", {})
        if deductibles:
            deductible_total = deductibles.get("total")
            deductible_remaining = deductibles.get("remaining")

        copay = _extract_copay_amount(amounts.get("coPayment")) or copay

    return base.model_copy(update={
        "eligibility_date": plan.get("eligibilityStartDate"),
        "deductible_total": deductible_total,
        "deductible_remaining": deductible_remaining,
        "copay": copay,
    })
