import json
import os
import time
from unittest.mock import MagicMock, patch

import pytest
import responses as responses_lib

from skyvern_runner import (
    SkyvernAuthError,
    SkyvernRunner,
    SkyvernTaskFailedError,
    SkyvernTimeoutError,
    SkyvernWorkflowNotFoundError,
)

FAKE_API_KEY = "sk-test-key"
FAKE_MEMBER_ID = "M123456"
FAKE_DOB = "1990-01-01"
FAKE_PAYER = "soonercare"
FAKE_TASK_ID = "task-abc-123"
SKYVERN_TASKS_URL = "https://api.skyvern.com/api/v1/tasks"
SKYVERN_TASK_URL = f"https://api.skyvern.com/api/v1/tasks/{FAKE_TASK_ID}"


@pytest.fixture
def workflow_dir(tmp_path):
    workflow = {
        "url": "https://soonercare.example.com/portal",
        "navigation_goal": "Log in and check eligibility",
        "data_extraction_goal": "Extract coverage details",
    }
    (tmp_path / "soonercare_eligibility.json").write_text(json.dumps(workflow))
    return str(tmp_path)


@pytest.fixture
def runner(workflow_dir):
    with patch("skyvern_runner.boto3.client") as mock_boto:
        mock_sm = MagicMock()
        mock_sm.get_secret_value.return_value = {
            "SecretString": json.dumps({"api_key": FAKE_API_KEY})
        }
        mock_boto.return_value = mock_sm
        return SkyvernRunner(
            aws_secret_name="test-secret",
            workflows_dir=workflow_dir,
        )


@responses_lib.activate
def test_happy_path_returns_extracted_data(runner, tmp_path):
    responses_lib.add(
        responses_lib.POST, SKYVERN_TASKS_URL,
        json={"task_id": FAKE_TASK_ID}, status=200,
    )
    responses_lib.add(
        responses_lib.GET, SKYVERN_TASK_URL,
        json={"status": "completed", "extracted_information": {"copay": 20}}, status=200,
    )
    result = runner.run_eligibility(FAKE_MEMBER_ID, FAKE_DOB, FAKE_PAYER)
    assert result == {"copay": 20}


@responses_lib.activate
def test_poll_retries_while_running(runner):
    responses_lib.add(responses_lib.POST, SKYVERN_TASKS_URL, json={"task_id": FAKE_TASK_ID}, status=200)
    responses_lib.add(responses_lib.GET, SKYVERN_TASK_URL, json={"status": "running"}, status=200)
    responses_lib.add(responses_lib.GET, SKYVERN_TASK_URL, json={"status": "running"}, status=200)
    responses_lib.add(
        responses_lib.GET, SKYVERN_TASK_URL,
        json={"status": "completed", "extracted_information": {"deductible": 500}}, status=200,
    )
    with patch("skyvern_runner.time.sleep"):
        result = runner.run_eligibility(FAKE_MEMBER_ID, FAKE_DOB, FAKE_PAYER)
    assert result == {"deductible": 500}


@responses_lib.activate
def test_raises_timeout_when_task_stalls(runner):
    responses_lib.add(responses_lib.POST, SKYVERN_TASKS_URL, json={"task_id": FAKE_TASK_ID}, status=200)
    # Set timeout to -1 so deadline is already in the past — while loop never entered
    with patch("skyvern_runner.TASK_TIMEOUT_SECONDS", -1):
        with pytest.raises(SkyvernTimeoutError):
            runner.run_eligibility(FAKE_MEMBER_ID, FAKE_DOB, FAKE_PAYER)


@responses_lib.activate
def test_raises_task_failed_on_failed_status(runner):
    responses_lib.add(responses_lib.POST, SKYVERN_TASKS_URL, json={"task_id": FAKE_TASK_ID}, status=200)
    responses_lib.add(responses_lib.GET, SKYVERN_TASK_URL, json={"status": "failed"}, status=200)
    with patch("skyvern_runner.time.sleep"):
        with pytest.raises(SkyvernTaskFailedError):
            runner.run_eligibility(FAKE_MEMBER_ID, FAKE_DOB, FAKE_PAYER)


@responses_lib.activate
def test_raises_task_failed_on_terminated_status(runner):
    responses_lib.add(responses_lib.POST, SKYVERN_TASKS_URL, json={"task_id": FAKE_TASK_ID}, status=200)
    responses_lib.add(responses_lib.GET, SKYVERN_TASK_URL, json={"status": "terminated"}, status=200)
    with patch("skyvern_runner.time.sleep"):
        with pytest.raises(SkyvernTaskFailedError):
            runner.run_eligibility(FAKE_MEMBER_ID, FAKE_DOB, FAKE_PAYER)


@responses_lib.activate
def test_raises_auth_error_on_401(runner):
    responses_lib.add(responses_lib.POST, SKYVERN_TASKS_URL, json={}, status=401)
    with pytest.raises(SkyvernAuthError):
        runner.run_eligibility(FAKE_MEMBER_ID, FAKE_DOB, FAKE_PAYER)


def test_raises_workflow_not_found(runner):
    with pytest.raises(SkyvernWorkflowNotFoundError):
        runner.run_eligibility(FAKE_MEMBER_ID, FAKE_DOB, "unknown_payer")


@responses_lib.activate
def test_audit_log_written_on_success(runner, tmp_path):
    responses_lib.add(responses_lib.POST, SKYVERN_TASKS_URL, json={"task_id": FAKE_TASK_ID}, status=200)
    responses_lib.add(
        responses_lib.GET, SKYVERN_TASK_URL,
        json={"status": "completed", "extracted_information": {}}, status=200,
    )
    log_path = tmp_path / "audit.jsonl"
    with patch("skyvern_runner.AUDIT_LOG_PATH", str(log_path)):
        runner.run_eligibility(FAKE_MEMBER_ID, FAKE_DOB, FAKE_PAYER)

    lines = log_path.read_text().strip().splitlines()
    outcomes = [json.loads(l)["outcome"] for l in lines]
    assert "success" in outcomes
    hashed = json.loads(lines[-1])["hashed_patient_id"]
    assert len(hashed) == 16


@responses_lib.activate
def test_audit_log_written_on_failure(runner, tmp_path):
    responses_lib.add(responses_lib.POST, SKYVERN_TASKS_URL, json={"task_id": FAKE_TASK_ID}, status=200)
    responses_lib.add(responses_lib.GET, SKYVERN_TASK_URL, json={"status": "failed"}, status=200)
    log_path = tmp_path / "audit.jsonl"
    with patch("skyvern_runner.AUDIT_LOG_PATH", str(log_path)):
        with patch("skyvern_runner.time.sleep"):
            with pytest.raises(SkyvernTaskFailedError):
                runner.run_eligibility(FAKE_MEMBER_ID, FAKE_DOB, FAKE_PAYER)

    lines = log_path.read_text().strip().splitlines()
    outcomes = [json.loads(l)["outcome"] for l in lines]
    assert "task_failed" in outcomes


@responses_lib.activate
def test_no_phi_in_audit_log(runner, tmp_path):
    responses_lib.add(responses_lib.POST, SKYVERN_TASKS_URL, json={"task_id": FAKE_TASK_ID}, status=200)
    responses_lib.add(
        responses_lib.GET, SKYVERN_TASK_URL,
        json={"status": "completed", "extracted_information": {}}, status=200,
    )
    log_path = tmp_path / "audit.jsonl"
    with patch("skyvern_runner.AUDIT_LOG_PATH", str(log_path)):
        runner.run_eligibility(FAKE_MEMBER_ID, FAKE_DOB, FAKE_PAYER)

    raw = log_path.read_text()
    assert FAKE_MEMBER_ID not in raw
    assert FAKE_DOB not in raw


@responses_lib.activate
def test_max_steps_always_25(runner):
    responses_lib.add(responses_lib.POST, SKYVERN_TASKS_URL, json={"task_id": FAKE_TASK_ID}, status=200)
    responses_lib.add(
        responses_lib.GET, SKYVERN_TASK_URL,
        json={"status": "completed", "extracted_information": {}}, status=200,
    )
    runner.run_eligibility(FAKE_MEMBER_ID, FAKE_DOB, FAKE_PAYER)
    submitted_body = json.loads(responses_lib.calls[0].request.body)
    assert submitted_body["max_steps_override"] == 25
