import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "code"))

import pytest
from patient_handler import handle, PatientValidationError

VALID = {
    "first_name": "Maria",
    "last_name": "Gonzalez",
    "member_id": "ZZZ445554301",
    "birth_date": "1970-01-01",
    "payer_name": "Aetna",
    "gender": "F",
    "state": "FL",
    "group_number": "12345",
}


def test_valid_payload_passes():
    result = handle(VALID)
    assert result.member_id == "ZZZ445554301"
    assert result.first_name == "Maria"
    assert result.payer_name == "Aetna"


def test_missing_member_id_raises():
    bad = {**VALID, "member_id": ""}
    with pytest.raises(PatientValidationError, match="member_id is required"):
        handle(bad)


def test_absent_member_id_raises():
    bad = {k: v for k, v in VALID.items() if k != "member_id"}
    with pytest.raises(PatientValidationError):
        handle(bad)


def test_malformed_birth_date_raises():
    bad = {**VALID, "birth_date": "01/01/1970"}
    with pytest.raises(PatientValidationError, match="YYYY-MM-DD"):
        handle(bad)


def test_missing_payer_name_raises():
    bad = {**VALID, "payer_name": ""}
    with pytest.raises(PatientValidationError, match="payer_name is required"):
        handle(bad)


def test_as_availity_patient_shape():
    result = handle(VALID)
    patient = result.as_availity_patient()
    assert patient["member_id"] == "ZZZ445554301"
    assert patient["last_name"] == "Gonzalez"
    assert patient["birth_date"] == "1970-01-01"
    assert "first_name" in patient
    assert "gender" in patient


def test_optional_fields_default_gracefully():
    minimal = {
        "first_name": "Test",
        "last_name": "User",
        "member_id": "ABC123",
        "birth_date": "1990-06-15",
        "payer_name": "UnitedHealthcare",
    }
    result = handle(minimal)
    patient = result.as_availity_patient()
    assert patient["gender"] == ""
    assert patient["state"] == ""
    assert patient["group_number"] == ""


def test_member_id_whitespace_stripped():
    padded = {**VALID, "member_id": "  ZZZ445554301  "}
    result = handle(padded)
    assert result.member_id == "ZZZ445554301"


def test_audit_write_failure_does_not_crash(monkeypatch):
    monkeypatch.setattr(
        "patient_handler.AUDIT_LOG_PATH",
        "/nonexistent/path/audit.jsonl"
    )
    result = handle(VALID)
    assert result.member_id == "ZZZ445554301"
