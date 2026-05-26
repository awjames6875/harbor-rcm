"""
Live sandbox integration test for AvailityClient.
Requires AWS credentials with access to Secrets Manager secret: harbor-rcm/dev
Hits the real Availity sandbox API — do not run against production credentials.
"""
import pprint
import pytest
from unittest.mock import patch, MagicMock
from availity_client import AvailityClient

MOCK_COVERAGE_RESPONSE = {
    "id": "test-12345",
    "statusCode": "4",
    "status": "Complete",
    "subscriber": {"memberId": "ZZZ445554301"},
    "patient": {"firstName": "MARIA", "lastName": "GONZALEZ"},
    "payer": {"name": "MOCKPAYER"},
    "plans": [{"status": "Active", "statusCode": "1"}],
}

SANDBOX_PATIENT = {
    "member_id": "ZZZ445554301",
    "last_name": "GONZALEZ",
    "first_name": "MARIA",
    "birth_date": "1970-01-01",
    "gender": "F",
    "state": "FL",
    "group_number": "12345",
}


def test_sandbox_eligibility_returns_complete():
    client = AvailityClient(aws_secret_name="harbor-rcm/dev")

    response = client.check_eligibility(
        patient=SANDBOX_PATIENT,
        payer_id="MOCKPAYER",
        sandbox=True,
    )

    print("\n--- Availity Sandbox Response ---")
    pprint.pprint(response)
    print("--- End Response ---\n")

    assert response["statusCode"] == "4", (
        f"Expected statusCode '4' (Complete) but got '{response.get('statusCode')}'"
    )


def test_mocked_coverage_response():
    fake_creds = {"client_id": "fake-id", "client_secret": "fake-secret"}
    mock_http = MagicMock()
    mock_http.status_code = 200
    mock_http.ok = True
    mock_http.json.return_value = MOCK_COVERAGE_RESPONSE

    with patch.object(AvailityClient, "_load_credentials", return_value=fake_creds), \
         patch.object(AvailityClient, "_ensure_token"), \
         patch.object(AvailityClient, "_post_coverage", return_value=mock_http), \
         patch.object(AvailityClient, "_audit"):
        client = AvailityClient(aws_secret_name="fake")
        response = client.check_eligibility(patient=SANDBOX_PATIENT, payer_id="MOCKPAYER")

    assert response["statusCode"] == "4"
    assert response["status"] == "Complete"
