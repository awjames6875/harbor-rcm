from __future__ import annotations

from typing import Optional

from pydantic import BaseModel


class BenefitsObject(BaseModel):
    patient_name: str
    member_id: str
    payer_name: str
    coverage_status: str
    eligibility_date: Optional[str] = None
    deductible_total: Optional[str] = None
    deductible_remaining: Optional[str] = None
    copay: Optional[str] = None
    # Set by confidence_scorer.py before Room 4 routing.
    # Room 4 must treat None as a hard error — never route without an explicit tier.
    confidence_score: Optional[float] = None
    confidence_tier: Optional[str] = None  # "auto_push" | "review" | "alert"
    raw_response: dict


def _extract_copay_amount(copayment) -> Optional[str]:
    """Return a string dollar amount from a scalar or object-shaped coPayment field."""
    if copayment is None:
        return None
    if isinstance(copayment, dict):
        for key in ("value", "amount"):
            val = copayment.get(key)
            if val is not None:
                return str(val)
        return None
    return str(copayment)


def normalize(raw: dict) -> BenefitsObject:
    patient = raw.get("patient", {})
    first = patient.get("firstName", "")
    last = patient.get("lastName", "")
    plans = raw.get("plans", [])
    return BenefitsObject(
        patient_name=f"{first} {last}".strip(),
        member_id=raw.get("subscriber", {}).get("memberId", ""),
        payer_name=raw.get("payer", {}).get("name", ""),
        coverage_status=plans[0].get("status", "") if plans else "",
        raw_response=raw,
    )
