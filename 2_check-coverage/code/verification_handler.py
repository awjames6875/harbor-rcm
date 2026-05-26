import json
import os
import sys
import time
from datetime import datetime, timezone
from uuid import uuid4

import boto3

from availity_client import AvailityClient
from skyvern_runner import SkyvernRunner
import payer_router

AUDIT_LOG_PATH = "2_check-coverage/logs/audit.jsonl"


class VerificationError(Exception):
    pass


class VerificationHandler:
    def __init__(
        self,
        availity: AvailityClient,
        skyvern: SkyvernRunner,
        cloudwatch_log_group: str | None = None,
        aws_region: str = "us-east-1",
    ):
        self._availity = availity
        self._skyvern = skyvern
        self._cloudwatch_log_group = cloudwatch_log_group
        self._aws_region = aws_region

    def verify(
        self,
        patient: dict,
        payer_name: str,
        provider_npi: str | None = None,
    ) -> dict:
        request_id = str(uuid4())

        try:
            route = payer_router.get_route(payer_name)
        except ValueError as exc:
            self._audit(request_id, payer_name, "unknown", "error")
            raise VerificationError(str(exc)) from exc

        path = route["path"]

        if path == "A":
            try:
                raw = self._availity.check_eligibility(
                    patient=patient,
                    payer_id=route["payer_id"],
                    provider_npi=provider_npi,
                )
            except Exception:
                self._audit(request_id, payer_name, path, "error")
                raise

        elif path == "B":
            try:
                raw = self._skyvern.run_eligibility(
                    member_id=patient["member_id"],
                    date_of_birth=patient["birth_date"],
                    payer_name=payer_name,
                    provider_npi=provider_npi,
                )
            except Exception:
                self._audit(request_id, payer_name, path, "error")
                raise

        else:
            self._audit(request_id, payer_name, path, "error")
            raise VerificationError(f"Unknown path '{path}' for payer '{payer_name}'")

        if not raw:
            self._audit(request_id, payer_name, path, "error")
            raise VerificationError(f"Empty response from payer '{payer_name}'")

        self._audit(request_id, payer_name, path, "success")
        return {
            "request_id": request_id,
            "path_used": path,
            "payer": payer_name,
            "raw_response": raw,
            "verification_timestamp": datetime.now(timezone.utc).isoformat(),
        }

    def _audit(self, request_id: str, payer: str, path: str, outcome: str) -> None:
        entry = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "event_type": "verification_request",
            "request_id": request_id,
            "payer": payer,
            "path": path,
            "outcome": outcome,
        }
        try:
            os.makedirs(os.path.dirname(AUDIT_LOG_PATH), exist_ok=True)
            with open(AUDIT_LOG_PATH, "a") as f:
                f.write(json.dumps(entry) + "\n")
        except Exception as exc:
            print(f"AUDIT_WRITE_FAILED: {exc}", file=sys.stderr)

        if self._cloudwatch_log_group:
            try:
                logs = boto3.client("logs", region_name=self._aws_region)
                logs.put_log_events(
                    logGroupName=self._cloudwatch_log_group,
                    logStreamName="verification-audit",
                    logEvents=[{"timestamp": int(time.time() * 1000), "message": json.dumps(entry)}],
                )
            except Exception:
                pass
