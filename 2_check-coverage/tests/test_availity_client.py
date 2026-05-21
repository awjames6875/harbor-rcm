import json
import os
import time
from unittest.mock import MagicMock, patch

import pytest
import responses as resp_mock

from availity_client import (
    AvailityAuthError,
    AvailityClient,
    AvailityMemberNotFound,
    AvailityTimeoutError,
    AvailityAPIError,
    AVAILITY_ELIGIBILITY_URL,
    AVAILITY_TOKEN_URL,
    AUDIT_LOG_PATH,
)


# --- Fixtures ---

FAKE_SECRET = {
    "client_id": "test_client_id",
    "client_secret": "test_client_secret",
    "trading_partner_id": "HARBOR_TEST",
}

FAKE_TOKEN_RESPONSE = {"access_token": "fake_token_abc", "expires_in": 3600}

FAKE_271_RESPONSE = {
    "status": "active",
    "memberId": "U123456789",
    "planName": "UHC Select Plus",
    "copay": 30,
}


def make_client():
    with patch("availity_client.boto3.client") as mock_boto:
        mock_secrets = MagicMock()
        mock_secrets.get_secret_value.return_value = {
            "SecretString": json.dumps(FAKE_SECRET)
        }
        mock_boto.return_value = mock_secrets
        return AvailityClient(aws_secret_name="harbor/test/availity")


def register_token_success():
    resp_mock.add(
        resp_mock.POST,
        AVAILITY_TOKEN_URL,
        json=FAKE_TOKEN_RESPONSE,
        status=200,
    )


# --- Tests ---

@resp_mock.activate
def test_happy_path_returns_raw_271(tmp_path, monkeypatch):
    monkeypatch.setattr("availity_client.AUDIT_LOG_PATH", str(tmp_path / "audit.jsonl"))
    client = make_client()
    register_token_success()
    resp_mock.add(resp_mock.POST, AVAILITY_ELIGIBILITY_URL, json=FAKE_271_RESPONSE, status=200)

    result = client.check_eligibility("U123456789", "1985-04-12")

    assert result == FAKE_271_RESPONSE


@resp_mock.activate
def test_audit_log_written_on_success(tmp_path, monkeypatch):
    monkeypatch.setattr("availity_client.AUDIT_LOG_PATH", str(tmp_path / "audit.jsonl"))
    client = make_client()
    register_token_success()
    resp_mock.add(resp_mock.POST, AVAILITY_ELIGIBILITY_URL, json=FAKE_271_RESPONSE, status=200)

    client.check_eligibility("U123456789", "1985-04-12")

    log_path = tmp_path / "audit.jsonl"
    assert log_path.exists()
    entry = json.loads(log_path.read_text().strip())
    assert entry["outcome"] == "success"
    assert entry["payer"] == "UHC"
    # raw member ID must NOT appear in the log
    assert "U123456789" not in log_path.read_text()
    assert len(entry["hashed_patient_id"]) == 16


@resp_mock.activate
def test_token_refresh_on_401_then_success(tmp_path, monkeypatch):
    monkeypatch.setattr("availity_client.AUDIT_LOG_PATH", str(tmp_path / "audit.jsonl"))
    client = make_client()
    # First token request
    register_token_success()
    # First eligibility call returns 401
    resp_mock.add(resp_mock.POST, AVAILITY_ELIGIBILITY_URL, json={}, status=401)
    # Second token request (refresh)
    register_token_success()
    # Retry eligibility call succeeds
    resp_mock.add(resp_mock.POST, AVAILITY_ELIGIBILITY_URL, json=FAKE_271_RESPONSE, status=200)

    result = client.check_eligibility("U123456789", "1985-04-12")

    assert result == FAKE_271_RESPONSE


@resp_mock.activate
def test_raises_auth_error_on_double_401(tmp_path, monkeypatch):
    monkeypatch.setattr("availity_client.AUDIT_LOG_PATH", str(tmp_path / "audit.jsonl"))
    client = make_client()
    register_token_success()
    resp_mock.add(resp_mock.POST, AVAILITY_ELIGIBILITY_URL, json={}, status=401)
    register_token_success()
    resp_mock.add(resp_mock.POST, AVAILITY_ELIGIBILITY_URL, json={}, status=401)

    with pytest.raises(AvailityAuthError):
        client.check_eligibility("U123456789", "1985-04-12")


@resp_mock.activate
def test_raises_member_not_found_on_404(tmp_path, monkeypatch):
    monkeypatch.setattr("availity_client.AUDIT_LOG_PATH", str(tmp_path / "audit.jsonl"))
    client = make_client()
    register_token_success()
    resp_mock.add(resp_mock.POST, AVAILITY_ELIGIBILITY_URL, json={}, status=404)

    with pytest.raises(AvailityMemberNotFound):
        client.check_eligibility("UNKNOWN123", "1985-04-12")


@resp_mock.activate
def test_raises_timeout_error(tmp_path, monkeypatch):
    import requests as req_lib
    monkeypatch.setattr("availity_client.AUDIT_LOG_PATH", str(tmp_path / "audit.jsonl"))
    client = make_client()
    register_token_success()
    resp_mock.add(resp_mock.POST, AVAILITY_ELIGIBILITY_URL, body=req_lib.Timeout())

    with pytest.raises(AvailityTimeoutError):
        client.check_eligibility("U123456789", "1985-04-12")


@resp_mock.activate
def test_raises_api_error_on_500(tmp_path, monkeypatch):
    monkeypatch.setattr("availity_client.AUDIT_LOG_PATH", str(tmp_path / "audit.jsonl"))
    client = make_client()
    register_token_success()
    resp_mock.add(resp_mock.POST, AVAILITY_ELIGIBILITY_URL, json={}, status=500)

    with pytest.raises(AvailityAPIError):
        client.check_eligibility("U123456789", "1985-04-12")


@resp_mock.activate
def test_token_cached_between_calls(tmp_path, monkeypatch):
    monkeypatch.setattr("availity_client.AUDIT_LOG_PATH", str(tmp_path / "audit.jsonl"))
    client = make_client()
    register_token_success()  # only one token request expected
    resp_mock.add(resp_mock.POST, AVAILITY_ELIGIBILITY_URL, json=FAKE_271_RESPONSE, status=200)
    resp_mock.add(resp_mock.POST, AVAILITY_ELIGIBILITY_URL, json=FAKE_271_RESPONSE, status=200)

    client.check_eligibility("U123456789", "1985-04-12")
    client.check_eligibility("U123456789", "1985-04-12")

    # Only 1 token call + 2 eligibility calls = 3 total requests
    assert len(resp_mock.calls) == 3
