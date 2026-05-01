import json
import os
from unittest.mock import MagicMock, patch

import pytest

from availity_client import AvailityAPIError
from skyvern_runner import SkyvernTaskFailedError
from verification_handler import VerificationError, VerificationHandler

FAKE_AVAILITY_RESPONSE = {"memberId": "U123", "planStatus": "active"}
FAKE_SKYVERN_RESPONSE = {"status": "active", "copay": "20"}


# --- Fixtures ---

@pytest.fixture
def availity():
    mock = MagicMock()
    mock.check_eligibility.return_value = FAKE_AVAILITY_RESPONSE
    return mock


@pytest.fixture
def skyvern():
    mock = MagicMock()
    mock.run_eligibility.return_value = FAKE_SKYVERN_RESPONSE
    return mock


@pytest.fixture
def handler(availity, skyvern):
    return VerificationHandler(availity=availity, skyvern=skyvern)


# --- Routing tests ---

def test_path_a_routing_calls_availity_not_skyvern(handler, availity, skyvern):
    handler.verify("U123", "1990-01-01", "unitedhealth")
    availity.check_eligibility.assert_called_once()
    skyvern.run_eligibility.assert_not_called()


def test_path_b_routing_calls_skyvern_not_availity(handler, availity, skyvern):
    handler.verify("M456", "1985-06-15", "soonercare")
    skyvern.run_eligibility.assert_called_once()
    availity.check_eligibility.assert_not_called()


# --- Success return shape tests ---

def test_path_a_success_returns_correct_dict(handler):
    result = handler.verify("U123", "1990-01-01", "unitedhealth")
    assert result["path_used"] == "A"
    assert result["payer"] == "unitedhealth"
    assert result["raw_response"] == FAKE_AVAILITY_RESPONSE
    assert "request_id" in result
    assert "verification_timestamp" in result
    assert result["verification_timestamp"].endswith("+00:00") or result["verification_timestamp"].endswith("Z")


def test_path_b_success_returns_correct_dict(handler):
    result = handler.verify("M456", "1985-06-15", "soonercare")
    assert result["path_used"] == "B"
    assert result["payer"] == "soonercare"
    assert result["raw_response"] == FAKE_SKYVERN_RESPONSE


# --- Error propagation tests ---

def test_unknown_payer_raises_verification_error(handler):
    with pytest.raises(VerificationError):
        handler.verify("X999", "2000-01-01", "mystery_payer")


def test_path_a_error_does_not_fall_back_to_path_b(handler, availity, skyvern):
    availity.check_eligibility.side_effect = AvailityAPIError("API down")
    with pytest.raises(AvailityAPIError):
        handler.verify("U123", "1990-01-01", "unitedhealth")
    skyvern.run_eligibility.assert_not_called()


def test_empty_raw_response_raises_verification_error(handler, availity):
    availity.check_eligibility.return_value = {}
    with pytest.raises(VerificationError, match="Empty response"):
        handler.verify("U123", "1990-01-01", "unitedhealth")


def test_none_raw_response_raises_verification_error(handler, skyvern):
    skyvern.run_eligibility.return_value = None
    with pytest.raises(VerificationError, match="Empty response"):
        handler.verify("M456", "1985-06-15", "soonercare")


def test_unknown_path_raises_verification_error(handler):
    with patch("verification_handler.payer_router.get_route", return_value={"path": "C"}):
        with pytest.raises(VerificationError, match="Unknown path"):
            handler.verify("X999", "2000-01-01", "unitedhealth")


# --- Audit log tests ---

def test_audit_entry_written_on_success(handler, tmp_path, monkeypatch):
    log_path = str(tmp_path / "audit.jsonl")
    monkeypatch.setattr("verification_handler.AUDIT_LOG_PATH", log_path)
    os.makedirs(str(tmp_path), exist_ok=True)

    result = handler.verify("U123", "1990-01-01", "unitedhealth")

    with open(log_path) as f:
        entries = [json.loads(line) for line in f]

    assert len(entries) == 1
    entry = entries[0]
    assert entry["outcome"] == "success"
    assert entry["request_id"] == result["request_id"]
    assert entry["payer"] == "unitedhealth"
    assert entry["path"] == "A"


def test_audit_entry_written_on_error(handler, availity, tmp_path, monkeypatch):
    log_path = str(tmp_path / "audit.jsonl")
    monkeypatch.setattr("verification_handler.AUDIT_LOG_PATH", log_path)
    os.makedirs(str(tmp_path), exist_ok=True)

    availity.check_eligibility.side_effect = AvailityAPIError("down")
    with pytest.raises(AvailityAPIError):
        handler.verify("U123", "1990-01-01", "unitedhealth")

    with open(log_path) as f:
        entries = [json.loads(line) for line in f]

    assert len(entries) == 1
    assert entries[0]["outcome"] == "error"


def test_audit_failure_does_not_crash_pipeline(handler, monkeypatch):
    monkeypatch.setattr("verification_handler.AUDIT_LOG_PATH", "/nonexistent/path/audit.jsonl")
    # Should not raise — audit failure is swallowed
    result = handler.verify("U123", "1990-01-01", "unitedhealth")
    assert result["path_used"] == "A"
