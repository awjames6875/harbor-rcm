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
AVAILITY_ELIGIBILITY_URL = "https://api.availity.com/availity/v1/eligibility-inquiries"
TOKEN_REFRESH_BUFFER_SECONDS = 60
REQUEST_TIMEOUT_SECONDS = 10
AUDIT_LOG_PATH = "2_check-coverage/logs/audit.jsonl"


class AvailityClient:
    def __init__(self, aws_secret_name: str, aws_region: str = "us-east-1", cloudwatch_log_group: str | None = None):
        creds = self._load_credentials(aws_secret_name, aws_region)
        self._client_id: str = creds["client_id"]
        self._client_secret: str = creds["client_secret"]
        self._trading_partner_id: str = creds["trading_partner_id"]
        self._token: str | None = None
        self._token_expiry: float = 0.0
        self._cloudwatch_log_group: str | None = cloudwatch_log_group
        self._aws_region: str = aws_region

    def check_eligibility(
        self,
        member_id: str,
        date_of_birth: str,
        payer_id: str = "UHC",
        provider_npi: str | None = None,
        service_type_code: str = "30",  # 30 = health benefit plan coverage
    ) -> dict:
        self._ensure_token()
        hashed_id = self._hash_patient_id(member_id)
        try:
            response = self._post_eligibility(member_id, date_of_birth, payer_id, provider_npi, service_type_code)
        except requests.Timeout:
            self._audit("eligibility_check", hashed_id, payer_id, "timeout")
            raise AvailityTimeoutError(f"Availity request timed out for payer {payer_id}")

        if response.status_code == 401:
            # Token may have just expired — refresh once and retry
            self._token = None
            self._ensure_token()
            try:
                response = self._post_eligibility(member_id, date_of_birth, payer_id, provider_npi, service_type_code)
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
                response = self._post_eligibility(member_id, date_of_birth, payer_id, provider_npi, service_type_code)
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

    def _post_eligibility(
        self,
        member_id: str,
        date_of_birth: str,
        payer_id: str,
        provider_npi: str | None,
        service_type_code: str,
    ) -> requests.Response:
        payload = {
            "memberId": member_id,
            "dateOfBirth": date_of_birth,
            "payerId": payer_id,
            "tradingPartnerId": self._trading_partner_id,
            "serviceTypeCode": service_type_code,
        }
        if provider_npi:
            payload["providerNpi"] = provider_npi
        return requests.post(
            AVAILITY_ELIGIBILITY_URL,
            json=payload,
            headers={"Authorization": f"Bearer {self._token}"},
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
                    "scope": "hipaa",
                },
                timeout=REQUEST_TIMEOUT_SECONDS,
            )
        except requests.Timeout:
            raise AvailityAuthError("Availity token request timed out")

        if not response.ok:
            raise AvailityAuthError(f"Availity token request failed with status {response.status_code}")

        body = response.json()
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
