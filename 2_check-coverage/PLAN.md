# PLAN — workflow_swapper.py: Self-Healing Skyvern Workflow Replacement

**Room:** 2_check-coverage  
**Topic:** Build workflow_swapper self-healing layer for broken Skyvern workflows  
**Status:** DRAFT — Round 0

---

## 1. What & Why

`verification_handler.py` is the single entry point for every eligibility check. Room 1 sends a patient payload here; this file decides which path to use (A = Availity API, B = Skyvern), calls the right client, and returns a standardized dict that Room 3 can normalize.

Without it, callers would have to import both `AvailityClient` and `SkyvernRunner`, know the routing table themselves, and implement their own audit trail. The handler owns all of that.

Both `AvailityClient` and `SkyvernRunner` already exist and are tested. `payer_router.py` exists but is missing the Availity `payer_id` for Path A entries — that's a one-line-per-payer fix needed here.

---

## 2. Files to Create / Modify

| Action | File | What changes |
|--------|------|--------------|
| **Modify** | `2_check-coverage/code/payer_router.py` | Add `payer_id` field to each Path A entry (Availity payer codes required by `AvailityClient.check_eligibility`) |
| **Create** | `2_check-coverage/code/verification_handler.py` | New `VerificationHandler` class (~80 lines) |
| **Create** | `2_check-coverage/tests/test_verification_handler.py` | Unit tests (~120 lines) |

No other files touched.

---

## 3. Logic & Data Flow

### 3a. `payer_router.py` — add `payer_id` to Path A entries

Current state has `{"path": "A"}` for API payers. `AvailityClient.check_eligibility()` requires a `payer_id` string (Availity's code for that payer). Adding it here keeps the mapping in one place.

```python
PAYER_ROUTES = {
    "unitedhealth": {"path": "A", "payer_id": "UHC"},
    "aetna":        {"path": "A", "payer_id": "AETNA"},
    "bcbs":         {"path": "A", "payer_id": "BCBS"},
    "medicare":     {"path": "A", "payer_id": "MDCR"},
    "cigna":        {"path": "A", "payer_id": "CIGNA"},
    "soonercare":   {"path": "B", "workflow": "soonercare_eligibility.json"},
}
```

`get_route()` signature is unchanged.

### 3b. `verification_handler.py` — class design

```
VerificationHandler(
    availity: AvailityClient,
    skyvern: SkyvernRunner,
    cloudwatch_log_group: str | None = None,
    aws_region: str = "us-east-1",
)
    └── verify(member_id, date_of_birth, payer_name, provider_npi=None) -> dict
```

Step-by-step flow inside `verify()`:

```
1. request_id = str(uuid4())          # opaque per-call ID; no PHI

2. route = payer_router.get_route(payer_name)
       ValueError (unknown payer) → _audit("error"), raise VerificationError

3a. route["path"] == "A"
       raw = availity.check_eligibility(
                 member_id, date_of_birth,
                 payer_id=route["payer_id"],
                 provider_npi=provider_npi)
       any AvailityError → _audit("error"), re-raise
       (NO silent fallback to Path B)

3b. route["path"] == "B"
       raw = skyvern.run_eligibility(
                 member_id, date_of_birth,
                 payer_name=payer_name,
                 provider_npi=provider_npi)
       any SkyvernError → _audit("error"), re-raise

3c. else (path is neither "A" nor "B")
       _audit("error"), raise VerificationError(f"Unknown path '{route['path']}'")
       (guards against future payer_router additions before handler is updated)

4. if not raw:
       _audit("error"), raise VerificationError("Empty response from payer")

5. _audit("verification_request", request_id, payer_name, path, "success")
   return {
       "request_id": request_id,
       "path_used": "A" | "B",
       "payer": payer_name,
       "raw_response": raw,
       "verification_timestamp": datetime.now(timezone.utc).isoformat(),
   }
```

**Critical rule enforced here:** Path A errors are raised immediately — never silently falling back to Path B. Path B costs 50× more and hides API outages. Callers are expected to handle exceptions and alert staff.

### 3c. Output dict — contract with Room 3

```json
{
  "request_id": "a1b2c3d4-e5f6-...",
  "path_used": "A",
  "payer": "unitedhealth",
  "raw_response": { "...Availity or Skyvern dict..." },
  "verification_timestamp": "2026-05-01T12:34:56.789Z"
}
```

Room 3 uses `path_used` to select the right normalizer function; `raw_response` is what it normalizes.

### 3d. Exceptions

```python
class VerificationError(Exception): pass
```

Only one new exception — for unknown payer. All other exceptions (AvailityError, SkyvernError) propagate as-is from the sub-clients.

### 3e. `_audit` (private)

Writes one entry to `2_check-coverage/logs/audit.jsonl` before every return or raise:

```json
{
  "timestamp": "...",
  "event_type": "verification_request",
  "request_id": "...",
  "payer": "unitedhealth",
  "path": "A",
  "outcome": "success" | "error"
}
```

No PHI in this log — `member_id` never appears. Sub-clients log their own hashed patient IDs. If `cloudwatch_log_group` is set, also sends to CloudWatch (swallow exceptions — never crash the pipeline).

**The entire `_audit()` body — including the local file write — must be wrapped in try/except and must never raise.** If the local write fails (disk full, permissions), write the failure to `sys.stderr` and return. Reason: `_audit()` is called inside `except` blocks; if it raises, it masks the original exception and the caller sees the wrong error. A lost audit entry is better than a hidden pipeline crash.

---

## 4. Security

| Concern | Mitigation |
|---------|------------|
| PHI in handler audit log | Only `request_id` (UUID), `payer`, `path`, `outcome` — no member ID or DOB ever logged here |
| PHI in `raw_response` | The returned dict's `raw_response` field contains full eligibility PHI. Callers MUST NOT log it. It must be passed directly to Room 3's normalizer and stored only in DynamoDB/S3-SSE. |
| No new credential paths | Handler takes pre-built clients — no boto3 calls inside the handler itself |
| Dependency injection | Tests pass mock clients; production passes real ones. No hidden coupling. |
| Audit before return | `_audit()` is called before `return` so a crash at the return site still produces a log entry |
| `_audit()` never raises | Entire `_audit()` body wrapped in try/except; file write failures go to stderr, never raised. Prevents masked exceptions in error handlers. |
| Path A → B fallback | Explicitly absent. Silent fallback would mask Availity outages and silently spend 50× more per call |
| Unknown path guard | `else` clause after A/B checks raises `VerificationError` with audit entry — no silent `NameError` |

---

## 5. Verification (Tests)

`test_verification_handler.py` will cover:

| # | Test | Asserts |
|---|------|---------|
| 1 | Path A routing | "unitedhealth" → `availity.check_eligibility` called; `skyvern.run_eligibility` never called |
| 2 | Path B routing | "soonercare" → `skyvern.run_eligibility` called; `availity.check_eligibility` never called |
| 3 | Path A success | returned dict has `path_used="A"`, correct `payer`, `raw_response`, ISO timestamp |
| 4 | Path B success | returned dict has `path_used="B"`, correct fields |
| 5 | Unknown payer | raises `VerificationError` |
| 6 | Path A error — no Path B fallback | when `AvailityClient` raises, handler re-raises; `skyvern.run_eligibility` never called |
| 7 | Audit on success | `audit.jsonl` contains entry with correct `request_id` and `outcome="success"` |
| 8 | Audit on error | audit entry with `outcome="error"` written even when client raises |
| 9 | Empty raw_response raises VerificationError | when client returns `None` or `{}`, handler raises `VerificationError` with audit entry |
| 10 | Unknown path raises VerificationError | if payer_router returns `{"path": "C"}`, handler raises `VerificationError` — no NameError |

Mocking pattern: `MagicMock()` for both clients (consistent with existing test style in this room). No HTTP mocking needed at the handler level — that belongs in the client tests.

---

## Implementation Order

1. Edit `payer_router.py` — add `payer_id` to 5 Path A rows (~5 lines changed)
2. Create `verification_handler.py` — `VerificationHandler` class (~80 lines)
3. Create `test_verification_handler.py` — 8 tests (~120 lines)
4. Run `py -m pytest 2_check-coverage/tests/ -v` — all tests green

---

*Ready for adversarial review before any code is written.*
