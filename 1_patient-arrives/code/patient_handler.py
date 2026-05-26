from __future__ import annotations

import hashlib
import json
import re
import sys
from datetime import date, datetime, timezone
from typing import Optional

from pydantic import BaseModel, field_validator, model_validator

AUDIT_LOG_PATH = "1_patient-arrives/logs/audit.jsonl"
REQUIRED_MEMBER_ID_ERROR = "member_id is required — cannot send to Room 2 without it"


class PatientValidationError(Exception):
    pass


class PatientPayload(BaseModel):
    """Canonical output shape for Room 1 → Room 2 handoff."""
    first_name: str
    last_name: str
    member_id: str
    birth_date: str          # YYYY-MM-DD
    payer_name: str
    provider_npi: Optional[str] = None
    appointment_date: Optional[str] = None
    gender: Optional[str] = None
    state: Optional[str] = None
    group_number: Optional[str] = None
    source_mode: str = "webhook"  # webhook | batch | ocr

    @field_validator("member_id")
    @classmethod
    def member_id_required(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError(REQUIRED_MEMBER_ID_ERROR)
        return v.strip()

    @field_validator("birth_date")
    @classmethod
    def birth_date_format(cls, v: str) -> str:
        try:
            datetime.strptime(v, "%Y-%m-%d")
        except ValueError:
            raise ValueError(f"birth_date must be YYYY-MM-DD, got: '{v}'")
        return v

    @field_validator("payer_name")
    @classmethod
    def payer_name_required(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError("payer_name is required")
        return v.strip()

    def as_availity_patient(self) -> dict:
        """Return the dict shape expected by availity_client.check_eligibility."""
        return {
            "member_id": self.member_id,
            "last_name": self.last_name,
            "first_name": self.first_name,
            "birth_date": self.birth_date,
            "gender": self.gender or "",
            "state": self.state or "",
            "group_number": self.group_number or "",
        }


def handle(raw: dict) -> PatientPayload:
    """
    Validate an incoming patient record and return a PatientPayload.
    Raises PatientValidationError on any validation failure.
    Never sends to Room 2 if member_id is missing.
    """
    try:
        payload = PatientPayload(**raw)
    except Exception as exc:
        _audit(raw.get("member_id", ""), "validation_failed", str(exc))
        raise PatientValidationError(str(exc)) from exc

    _audit(payload.member_id, "validation_passed", "ok")
    return payload


def _audit(member_id: str, outcome: str, detail: str) -> None:
    hashed = hashlib.sha256(member_id.encode()).hexdigest()[:16] if member_id else "unknown"
    entry = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "event_type": "patient_intake",
        "hashed_patient_id": hashed,
        "outcome": outcome,
        "detail": detail,
    }
    try:
        import os
        os.makedirs(os.path.dirname(AUDIT_LOG_PATH), exist_ok=True)
        with open(AUDIT_LOG_PATH, "a") as f:
            f.write(json.dumps(entry) + "\n")
    except Exception as exc:
        print(f"AUDIT_WRITE_FAILED: {exc}", file=sys.stderr)
