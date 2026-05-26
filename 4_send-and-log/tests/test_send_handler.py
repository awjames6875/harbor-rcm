import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "code"))

import pytest
from unittest.mock import MagicMock, patch, call
from send_handler import SendHandler, UnscoredBenefitsError


def _make_benefits(tier, score=90.0):
    b = MagicMock()
    b.confidence_tier = tier
    b.confidence_score = score
    b.payer_name = "Aetna"
    b.member_id = "W123456789"
    return b


def test_unscored_raises_before_any_action():
    handler = SendHandler()
    benefits = _make_benefits(tier=None, score=None)
    with pytest.raises(UnscoredBenefitsError):
        handler.handle(benefits)


def test_unscored_score_none_raises():
    handler = SendHandler()
    benefits = _make_benefits(tier="auto_push", score=None)
    with pytest.raises(UnscoredBenefitsError):
        handler.handle(benefits)


def test_auto_push_returns_success():
    handler = SendHandler()
    result = handler.handle(_make_benefits("auto_push", score=97.0))
    assert result["action"] == "auto_push"
    assert result["status"] == "success"


def test_review_returns_queued():
    handler = SendHandler()
    result = handler.handle(_make_benefits("review", score=85.0))
    assert result["action"] == "review"
    assert result["status"] == "queued"


def test_alert_returns_alert_sent_and_no_ehr_write():
    handler = SendHandler()
    with patch.object(handler, "_auto_push") as mock_push:
        result = handler.handle(_make_benefits("alert", score=60.0))
        mock_push.assert_not_called()
    assert result["action"] == "alert"
    assert result["status"] == "alert_sent"


def test_audit_called_before_ehr_write():
    """Verify _audit is called with 'routing' before the EHR write begins."""
    handler = SendHandler()
    call_order = []

    original_audit = handler._audit
    def tracking_audit(request_id, benefits, tier, outcome):
        call_order.append(("audit", outcome))
        original_audit(request_id, benefits, tier, outcome)

    original_push = handler._auto_push
    def tracking_push(request_id, benefits):
        call_order.append(("ehr_write", "started"))
        return original_push(request_id, benefits)

    handler._audit = tracking_audit
    handler._auto_push = tracking_push

    handler.handle(_make_benefits("auto_push", score=97.0))

    # First call must be the routing audit
    assert call_order[0] == ("audit", "routing")
    ehr_idx = next(i for i, c in enumerate(call_order) if c[0] == "ehr_write")
    routing_idx = next(i for i, c in enumerate(call_order) if c == ("audit", "routing"))
    assert routing_idx < ehr_idx


def test_unknown_tier_raises():
    handler = SendHandler()
    with pytest.raises(Exception):
        handler.handle(_make_benefits("unknown_tier", score=50.0))


def test_audit_write_failure_does_not_crash_pipeline(tmp_path, monkeypatch):
    """A bad audit path must never crash the eligibility result."""
    monkeypatch.setattr(
        "send_handler.AUDIT_LOG_PATH",
        "/nonexistent/path/that/cannot/be/created/audit.jsonl"
    )
    handler = SendHandler()
    # Should not raise even though audit write will fail
    result = handler.handle(_make_benefits("auto_push", score=97.0))
    assert result["action"] == "auto_push"
