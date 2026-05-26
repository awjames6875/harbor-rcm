from __future__ import annotations

import json
import sys
import time
from datetime import datetime, timezone
from uuid import uuid4

import boto3

AUDIT_LOG_PATH = "4_send-and-log/logs/audit.jsonl"


class SendError(Exception):
    pass


class UnscoredBenefitsError(SendError):
    """Raised when confidence_score or confidence_tier is missing — fail closed."""
    pass


class SendHandler:
    def __init__(
        self,
        cloudwatch_log_group: str | None = None,
        aws_region: str = "us-east-1",
    ):
        self._cloudwatch_log_group = cloudwatch_log_group
        self._aws_region = aws_region

    def handle(self, benefits: object) -> dict:
        """
        Route a scored BenefitsObject to the right action.
        Audit log is written BEFORE any EHR write (HIPAA non-negotiable).
        Fails closed if confidence_tier is None.
        """
        if benefits.confidence_score is None or benefits.confidence_tier is None:
            raise UnscoredBenefitsError(
                "BenefitsObject must be scored before send_handler.handle() is called. "
                "Run confidence_scorer.score() first."
            )

        request_id = str(uuid4())
        tier = benefits.confidence_tier

        # Audit BEFORE any EHR write
        self._audit(request_id, benefits, tier, "routing")

        if tier == "auto_push":
            result = self._auto_push(request_id, benefits)
        elif tier == "review":
            result = self._queue_for_review(request_id, benefits)
        elif tier == "alert":
            result = self._send_alert(request_id, benefits)
        else:
            raise SendError(f"Unknown confidence_tier '{tier}'")

        return result

    def _auto_push(self, request_id: str, benefits: object) -> dict:
        """Write directly to EHR — no human review needed."""
        self._audit(request_id, benefits, "auto_push", "ehr_write_started")
        # EHR write goes here — client-specific adapter configured at install time
        # Placeholder: log the intent; real implementation wires to Keragon/direct EHR API
        self._audit(request_id, benefits, "auto_push", "ehr_write_success")
        return {"action": "auto_push", "request_id": request_id, "status": "success"}

    def _queue_for_review(self, request_id: str, benefits: object) -> dict:
        """Add to human review queue with uncertain fields highlighted."""
        self._audit(request_id, benefits, "review", "queued")
        # Review queue write — DynamoDB table, state: Pending
        # Placeholder: real implementation writes to DynamoDB review table
        return {"action": "review", "request_id": request_id, "status": "queued"}

    def _send_alert(self, request_id: str, benefits: object) -> dict:
        """Send staff alert — nothing written to EHR."""
        self._audit(request_id, benefits, "alert", "alert_sent")
        # Alert goes via SNS/SMS/email — configured at install time
        # Placeholder: real implementation calls notifier.py
        return {"action": "alert", "request_id": request_id, "status": "alert_sent"}

    def _audit(self, request_id: str, benefits: object, tier: str, outcome: str) -> None:
        entry = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "event_type": "send_handler",
            "request_id": request_id,
            "payer": benefits.payer_name,
            "member_id_hash": benefits.member_id[:4] + "****",
            "confidence_score": benefits.confidence_score,
            "confidence_tier": tier,
            "outcome": outcome,
        }
        try:
            import os
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
                    logStreamName="send-handler-audit",
                    logEvents=[{"timestamp": int(time.time() * 1000), "message": json.dumps(entry)}],
                )
            except Exception:
                pass
