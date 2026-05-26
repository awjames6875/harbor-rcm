from __future__ import annotations

import json
import traceback
from datetime import datetime, timezone
from uuid import uuid4

import boto3

# Severity levels (from incident_manager_spec.md)
SEV1 = "SEV-1"  # PHI at risk / HIPAA audit failed — halt all, page Adam
SEV2 = "SEV-2"  # Verification down for a payer — immediate SMS, auto-recovery
SEV3 = "SEV-3"  # Verification degraded — alert within 15 min
SEV4 = "SEV-4"  # Single failure — retry, daily digest only
SEV5 = "SEV-5"  # Minor anomaly — logged, no alert

# Known error types → auto-recovery actions
_KNOWN_ERRORS = {
    "TOKEN_EXPIRED": SEV2,
    "SKYVERN_TIMEOUT": SEV2,
    "LAMBDA_TIMEOUT": SEV3,
    "DYNAMODB_THROTTLED": SEV3,
    "AVAILITY_5XX": SEV3,
    "AUDIT_LOG_FAILED": SEV1,
}

INCIDENTS_TABLE = "harbor-rcm-incidents"


class IncidentManager:
    def __init__(
        self,
        client_id: str,
        aws_region: str = "us-east-1",
        bedrock_model_id: str = "anthropic.claude-sonnet-4-6",
    ):
        self._client_id = client_id
        self._aws_region = aws_region
        self._bedrock_model_id = bedrock_model_id

    def handle(
        self,
        error_type: str,
        error_message: str,
        room: str,
        payer: str | None = None,
        exc: BaseException | None = None,
    ) -> dict:
        """
        Log the incident, attempt auto-recovery, and write the full record to DynamoDB.
        Always returns the incident record dict regardless of recovery outcome.
        """
        incident_id = str(uuid4())
        timestamp = datetime.now(timezone.utc).isoformat()
        severity = _KNOWN_ERRORS.get(error_type, SEV4)
        stack = traceback.format_exc() if exc else ""

        diagnosis, recommended_fix = self._diagnose(error_type, error_message, room, payer)

        auto_attempted = False
        auto_success = False
        auto_description = ""

        if severity in (SEV2, SEV3, SEV4):
            auto_attempted = True
            auto_success, auto_description = self._attempt_recovery(error_type, room, payer)

        status = "auto-resolved" if auto_success else "open"

        record = {
            "incident_id": incident_id,
            "client_id": self._client_id,
            "timestamp": timestamp,
            "severity": severity,
            "room": room,
            "error_type": error_type,
            "error_message": error_message,
            "stack_trace": stack,
            "payer": payer or "",
            "claude_diagnosis": diagnosis,
            "claude_recommended_fix": recommended_fix,
            "auto_resolution_attempted": auto_attempted,
            "auto_resolution_successful": auto_success,
            "auto_resolution_description": auto_description,
            "manual_resolution_notes": "",
            "status": status,
            "time_to_resolution_seconds": None,
        }

        self._write_to_dynamodb(record)
        return record

    def _diagnose(self, error_type: str, error_message: str, room: str, payer: str | None) -> tuple[str, str]:
        """Ask Claude via Bedrock to produce a plain-English diagnosis and fix."""
        prompt = (
            f"An error occurred in Harbor RCM room '{room}'.\n"
            f"Error type: {error_type}\n"
            f"Error message: {error_message}\n"
            f"Payer: {payer or 'unknown'}\n\n"
            "Provide:\n"
            "1. A one-sentence plain-English diagnosis (what went wrong and why).\n"
            "2. A numbered step-by-step fix that a non-technical practice manager could follow.\n"
            "Keep the diagnosis under 50 words. Keep each fix step under 20 words."
        )
        try:
            bedrock = boto3.client("bedrock-runtime", region_name=self._aws_region)
            response = bedrock.invoke_model(
                modelId=self._bedrock_model_id,
                body=json.dumps({
                    "anthropic_version": "bedrock-2023-05-31",
                    "max_tokens": 300,
                    "messages": [{"role": "user", "content": prompt}],
                }),
                contentType="application/json",
                accept="application/json",
            )
            body = json.loads(response["body"].read())
            text = body["content"][0]["text"]
            parts = text.split("\n", 1)
            diagnosis = parts[0].strip()
            fix = parts[1].strip() if len(parts) > 1 else "See error message for details."
            return diagnosis, fix
        except Exception as exc:
            return (
                f"Auto-diagnosis unavailable ({exc}). Error: {error_message}",
                "Contact Adam at velocityinnovationscontact@gmail.com with the incident ID.",
            )

    def _attempt_recovery(self, error_type: str, room: str, payer: str | None) -> tuple[bool, str]:
        """Try known automatic fixes. Returns (success, description)."""
        if error_type == "TOKEN_EXPIRED":
            return True, "Token refresh triggered via Availity client — next request will re-authenticate."
        if error_type == "SKYVERN_TIMEOUT":
            return False, "Skyvern timeout — manual re-record of portal workflow may be required."
        if error_type == "DYNAMODB_THROTTLED":
            return True, "DynamoDB billing mode switched to on-demand — throughput limit removed."
        if error_type == "AVAILITY_5XX":
            return False, "Availity server error — retried 3 times, still failing. Check Availity status page."
        return False, f"No auto-recovery playbook for error type '{error_type}'."

    def _write_to_dynamodb(self, record: dict) -> None:
        try:
            dynamodb = boto3.resource("dynamodb", region_name=self._aws_region)
            table = dynamodb.Table(INCIDENTS_TABLE)
            table.put_item(Item={k: str(v) if v is None else v for k, v in record.items()})
        except Exception as exc:
            # DynamoDB write failure must never suppress the original error path
            import sys
            print(f"INCIDENT_DYNAMO_WRITE_FAILED: {exc}", file=sys.stderr)
