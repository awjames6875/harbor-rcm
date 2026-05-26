import hashlib
import json
import time
from datetime import datetime, timezone

import boto3
import requests


# --- Exceptions ---

class AvailityError(Exception):
    pass

class AvailityAuthError(AvailityError):
    pass

class AvailityMemberNotFound(AvailityError):
    pass

class AvailityTimeoutError(AvailityError):
    pass

class AvailityAPIError(AvailityError):
    pass


# --- Client ---

AVAILITY_TOKEN_URL = "https://api.availity.com/availity/v1/token"
AVAILITY_COVERAGES_URL = "https://api.availity.com/availity/v1/coverages"
TOKEN_REFRESH_BUFFER_SECONDS = 60
REQUEST_TIMEOUT_SECONDS = 10
AUDIT_LOG_PATH = "2_check-coverage/logs/audit.jsonl"


class AvailityClient:
    def __init__(self, aws_secret_name: str, aws_region: str = "us-east-1", cloudwatch_log_group: str | None = None):
        creds = self._load_credentials(aws_secret_name, aws_region)
        self._client_id: str = creds["client_id"]
        self._client_secret: str = creds["client_secret"]
        self._token: str | None = None
        self._token_expiry: float = 0.0
        self._cloudwatch_log_group: str | None = cloudwatch_log_group
        self._aws_region: str = aws_region

    def check_eligibility(
        self,
        patient: dict,
        payer_id: str = "UHC",
        provider_npi: str | None = None,
        sandbox: bool = False,
    ) -> dict:
        """
        patient = {
            "member_id": "ABC123",
            "last_name": "GONZALEZ",
            "first_name": "MARIA",
            "birth_date": "1970-01-01",   # YYYY-MM-DD
            "gender": "F",
            "state": "OK",
            "group_number": "12345"
        }
        """
        self._ensure_token()
        hashed_id = self._hash_patient_id(patient["member_id"])
        try:
            response = self._post_coverage(patient, payer_id, provider_npi, sandbox)
        except requests.Timeout:
            self._audit("eligibility_check", hashed_id, payer_id, "timeout")
            raise AvailityTimeoutError(f"Availity request timed out for payer {payer_id}")

        if response.status_code == 401:
            # Token may have just expired — refresh once and retry
            self._token = None
            self._ensure_token()
            try:
                response = self._post_coverage(patient, payer_id, provider_npi, sandbox)
            except requests.Timeout:
                self._audit("eligibility_check", hashed_id, payer_id, "timeout")
                raise AvailityTimeoutError(f"Availity request timed out for payer {payer_id}")
            if response.status_code == 401:
                self._audit("eligibility_check", hashed_id, payer_id, "auth_error")
                raise AvailityAuthError("Availity authentication failed after token refresh")

        if response.status_code == 404:
            self._audit("eligibility_check", hashed_id, payer_id, "member_not_found")
            raise AvailityMemberNotFound(f"Member not found in payer {payer_id} system")

        if response.status_code >= 500:
            # Availity 5xx — retry once after a short wait
            time.sleep(2)
            try:
                response = self._post_coverage(patient, payer_id, provider_npi, sandbox)
            except requests.Timeout:
                self._audit("eligibility_check", hashed_id, payer_id, "timeout")
                raise AvailityTimeoutError(f"Availity request timed out for payer {payer_id}")
            if response.status_code >= 500:
                self._audit("eligibility_check", hashed_id, payer_id, "api_error")
                raise AvailityAPIError(f"Availity returned {response.status_code} after retry for payer {payer_id}")

        if not response.ok:
            self._audit("eligibility_check", hashed_id, payer_id, "api_error")
            raise AvailityAPIError(f"Availity returned {response.status_code} for payer {payer_id}")

        self._audit("eligibility_check", hashed_id, payer_id, "success")
        return response.json()

    def _post_coverage(
        self,
        patient: dict,
        payer_id: str,
        provider_npi: str | None,
        sandbox: bool,
    ) -> requests.Response:
        headers = {
            "Authorization": f"Bearer {self._token}",
            "Content-Type": "application/x-www-form-urlencoded",
        }
        if sandbox:
            headers["X-Api-Mock-Response"] = "true"
            headers["X-Api-Mock-Scenario-ID"] = "Coverages-Complete-i"
        data = {
            "payerId": payer_id,
            "memberId": patient["member_id"],
            "patientLastName": patient["last_name"],
            "patientFirstName": patient["first_name"],
            "patientBirthDate": patient["birth_date"],
            "patientGender": patient.get("gender", ""),
            "patientState": patient.get("state", ""),
            "groupNumber": patient.get("group_number", ""),
            "serviceType[]": "30",
            "subscriberRelationship": "18",
        }
        if provider_npi:
            data["providerNpi"] = provider_npi
        return requests.post(
            AVAILITY_COVERAGES_URL,
            headers=headers,
            data=data,
            timeout=REQUEST_TIMEOUT_SECONDS,
        )

    def _ensure_token(self) -> None:
        if self._token and time.time() < self._token_expiry - TOKEN_REFRESH_BUFFER_SECONDS:
            return
        try:
            response = requests.post(
                AVAILITY_TOKEN_URL,
                data={
                    "grant_type": "client_credentials",
                    "client_id": self._client_id,
                    "client_secret": self._client_secret,
                    "scope": "healthcare-hipaa-transactions hipaa",
                },
                timeout=REQUEST_TIMEOUT_SECONDS,
            )
        except requests.Timeout:
            raise AvailityAuthError("Availity token request timed out")

        if not response.ok:
            raise AvailityAuthError(
                f"Availity token request failed with status {response.status_code}: {response.text}"
            )

        body = response.json()
        if "access_token" not in body:
            raise AvailityAuthError(
                f"Availity token response missing access_token. Status: {response.status_code}. Body: {body}"
            )
        self._token = body["access_token"]
        self._token_expiry = time.time() + body.get("expires_in", 3600)

    def _hash_patient_id(self, member_id: str) -> str:
        raw = member_id + self._client_id
        return hashlib.sha256(raw.encode()).hexdigest()[:16]

    def _audit(self, event_type: str, hashed_patient_id: str, payer: str, outcome: str) -> None:
        import os
        entry = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "event_type": event_type,
            "hashed_patient_id": hashed_patient_id,
            "payer": payer,
            "outcome": outcome,
        }
        # Always write to local file (useful in dev/sandbox)
        os.makedirs(os.path.dirname(AUDIT_LOG_PATH), exist_ok=True)
        with open(AUDIT_LOG_PATH, "a") as f:
            f.write(json.dumps(entry) + "\n")
        # Additionally send to CloudWatch if configured (production)
        if self._cloudwatch_log_group:
            try:
                logs = boto3.client("logs", region_name=self._aws_region)
                logs.put_log_events(
                    logGroupName=self._cloudwatch_log_group,
                    logStreamName="availity-audit",
                    logEvents=[{"timestamp": int(time.time() * 1000), "message": json.dumps(entry)}],
                )
            except Exception:
                pass  # Never let CloudWatch failure crash the pipeline

    @staticmethod
    def _load_credentials(secret_name: str, region: str) -> dict:
        client = boto3.client("secretsmanager", region_name=region)
        response = client.get_secret_value(SecretId=secret_name)
        return json.loads(response["SecretString"])
