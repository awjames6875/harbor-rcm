import hashlib
import json
import time
from datetime import datetime, timezone
from pathlib import Path

import boto3
import requests


# --- Exceptions ---

class SkyvernError(Exception):
    pass

class SkyvernWorkflowNotFoundError(SkyvernError):
    pass

class SkyvernTaskFailedError(SkyvernError):
    pass

class SkyvernTimeoutError(SkyvernError):
    pass

class SkyvernAuthError(SkyvernError):
    pass


# --- Constants ---

SKYVERN_BASE_URL = "https://api.skyvern.com"
MAX_STEPS = 25
POLL_INTERVAL_SECONDS = 3
TASK_TIMEOUT_SECONDS = 90
AUDIT_LOG_PATH = "2_check-coverage/logs/audit.jsonl"


class SkyvernRunner:
    def __init__(
        self,
        aws_secret_name: str,
        workflows_dir: str,
        aws_region: str = "us-east-1",
        cloudwatch_log_group: str | None = None,
    ):
        creds = self._load_credentials(aws_secret_name, aws_region)
        self._api_key: str = creds["api_key"]
        self._workflows_dir: str = workflows_dir
        self._cloudwatch_log_group: str | None = cloudwatch_log_group
        self._aws_region: str = aws_region

    def run_eligibility(
        self,
        member_id: str,
        date_of_birth: str,
        payer_name: str,
        provider_npi: str | None = None,
    ) -> dict:
        hashed_id = self._hash_patient_id(member_id)

        workflow_path = Path(self._workflows_dir) / f"{payer_name.lower()}_eligibility.json"
        if not workflow_path.exists():
            self._audit("skyvern_eligibility", hashed_id, payer_name, "workflow_not_found")
            raise SkyvernWorkflowNotFoundError(
                f"No workflow JSON found for payer '{payer_name}' at {workflow_path}"
            )

        with open(workflow_path) as f:
            workflow = json.load(f)

        task_id = self._submit_task(
            portal_url=workflow["url"],
            navigation_goal=workflow["navigation_goal"],
            data_extraction_goal=workflow["data_extraction_goal"],
            member_id=member_id,
            date_of_birth=date_of_birth,
            provider_npi=provider_npi,
        )
        self._audit("skyvern_eligibility", hashed_id, payer_name, "submitted")

        result = self._poll_until_done(task_id, hashed_id, payer_name)

        self._audit("skyvern_eligibility", hashed_id, payer_name, "success")
        return result["extracted_information"]

    def _submit_task(
        self,
        portal_url: str,
        navigation_goal: str,
        data_extraction_goal: str,
        member_id: str,
        date_of_birth: str,
        provider_npi: str | None,
    ) -> str:
        navigation_payload = {"member_id": member_id, "date_of_birth": date_of_birth}
        if provider_npi:
            navigation_payload["provider_npi"] = provider_npi

        response = requests.post(
            f"{SKYVERN_BASE_URL}/api/v1/tasks",
            json={
                "url": portal_url,
                "navigation_goal": navigation_goal,
                "data_extraction_goal": data_extraction_goal,
                "navigation_payload": navigation_payload,
                "max_steps_override": MAX_STEPS,
                "proxy_location": "RESIDENTIAL",
            },
            headers={"x-api-key": self._api_key, "Content-Type": "application/json"},
            timeout=10,
        )

        if response.status_code == 401:
            raise SkyvernAuthError("Skyvern API key rejected (401)")
        if not response.ok:
            raise SkyvernError(f"Skyvern task submission failed with status {response.status_code}")

        return response.json()["task_id"]

    def _poll_until_done(self, task_id: str, hashed_id: str, payer_name: str) -> dict:
        deadline = time.time() + TASK_TIMEOUT_SECONDS
        while time.time() < deadline:
            response = requests.get(
                f"{SKYVERN_BASE_URL}/api/v1/tasks/{task_id}",
                headers={"x-api-key": self._api_key},
                timeout=10,
            )
            if not response.ok:
                raise SkyvernError(f"Skyvern poll failed with status {response.status_code}")

            data = response.json()
            status = data["status"]

            if status == "completed":
                return data
            if status in ("failed", "terminated"):
                self._audit("skyvern_eligibility", hashed_id, payer_name, "task_failed")
                raise SkyvernTaskFailedError(f"Skyvern task ended with status '{status}'")

            time.sleep(POLL_INTERVAL_SECONDS)

        self._audit("skyvern_eligibility", hashed_id, payer_name, "timeout")
        raise SkyvernTimeoutError(f"Skyvern task {task_id} did not complete within {TASK_TIMEOUT_SECONDS}s")

    def _hash_patient_id(self, member_id: str) -> str:
        raw = member_id + self._api_key
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
        try:
            os.makedirs(os.path.dirname(AUDIT_LOG_PATH), exist_ok=True)
            with open(AUDIT_LOG_PATH, "a") as f:
                f.write(json.dumps(entry) + "\n")
        except Exception as exc:
            import sys
            print(f"AUDIT_WRITE_FAILED: {exc}", file=sys.stderr)
        if self._cloudwatch_log_group:
            try:
                logs = boto3.client("logs", region_name=self._aws_region)
                logs.put_log_events(
                    logGroupName=self._cloudwatch_log_group,
                    logStreamName="skyvern-audit",
                    logEvents=[{"timestamp": int(time.time() * 1000), "message": json.dumps(entry)}],
                )
            except Exception:
                pass

    @staticmethod
    def _load_credentials(secret_name: str, region: str) -> dict:
        client = boto3.client("secretsmanager", region_name=region)
        response = client.get_secret_value(SecretId=secret_name)
        return json.loads(response["SecretString"])
