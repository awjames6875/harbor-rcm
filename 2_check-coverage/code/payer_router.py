PAYER_ROUTES = {
    "unitedhealth": {"path": "A", "payer_id": "UHC"},
    "aetna":        {"path": "A", "payer_id": "AETNA"},
    "bcbs":         {"path": "A", "payer_id": "BCBS"},
    "medicare":     {"path": "A", "payer_id": "MDCR"},
    "cigna":        {"path": "A", "payer_id": "CIGNA"},
    "soonercare":   {"path": "B", "workflow": "soonercare_eligibility.json"},
}


def get_route(payer_name: str) -> dict:
    """Returns {"path": "A"} or {"path": "B", "workflow": "<filename>"}. Raises ValueError for unknown payers."""
    key = payer_name.strip().lower()
    if key not in PAYER_ROUTES:
        raise ValueError(f"Unknown payer: '{payer_name}'. Add it to PAYER_ROUTES in payer_router.py.")
    return PAYER_ROUTES[key]
