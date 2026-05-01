import pytest
from payer_router import get_route


def test_path_a_payers():
    for payer in ["unitedhealth", "aetna", "bcbs", "medicare", "cigna"]:
        route = get_route(payer)
        assert route["path"] == "A"
        assert "payer_id" in route


def test_path_b_soonercare():
    assert get_route("soonercare") == {"path": "B", "workflow": "soonercare_eligibility.json"}


def test_unknown_payer_raises():
    with pytest.raises(ValueError, match="Unknown payer"):
        get_route("fake_payer")


def test_case_insensitive():
    assert get_route("AETNA") == get_route("aetna")


def test_whitespace_stripped():
    assert get_route("  cigna ")["path"] == "A"
