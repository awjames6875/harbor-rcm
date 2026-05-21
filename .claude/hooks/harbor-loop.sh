#!/usr/bin/env bash
# Stop hook: fires every time Claude tries to end a turn.
# Reads loop state and either ALLOWs (exit 0) or BLOCKs (exit 1).

STATE_FILE=".claude/state/loop.yaml"

# No active loop — allow exit immediately
if [ ! -f "$STATE_FILE" ]; then
  exit 0
fi

# Parse state file
phase=$(grep '^phase:' "$STATE_FILE" | awk '{print $2}')
round=$(grep '^round:' "$STATE_FILE" | awk '{print $2}')
max_rounds=$(grep '^max_rounds:' "$STATE_FILE" | awk '{print $2}')
room=$(grep '^room:' "$STATE_FILE" | awk '{print $2}')
plan_path=$(grep '^plan_path:' "$STATE_FILE" | awk '{print $2}' | tr -d '"')

# Done or cancelled — clean up and allow exit
if [ "$phase" = "done" ] || [ "$phase" = "cancelled" ]; then
  rm -f "$STATE_FILE"
  exit 0
fi

# Budget exhausted — allow exit
if [ "$round" -ge "$max_rounds" ] 2>/dev/null; then
  echo ""
  echo "HARBOR LOOP: Max rounds ($max_rounds) reached. Plan locked."
  rm -f "$STATE_FILE"
  exit 0
fi

# ─── DRAFTING → REVIEWING ───────────────────────────────────────────────────
# Plan has been written. Transition to review phase.
if [ "$phase" = "drafting" ] && [ -f "$plan_path" ]; then
  new_round=$((round + 1))
  sed -i "s/^phase:.*/phase: reviewing/" "$STATE_FILE"
  sed -i "s/^round:.*/round: $new_round/" "$STATE_FILE"

  echo ""
  echo "═══════════════════════════════════════════════════════════"
  echo " HARBOR LOOP — Round $new_round of $max_rounds — REVIEW PHASE"
  echo "═══════════════════════════════════════════════════════════"
  echo ""
  echo "PLAN.md drafted at: $plan_path"
  echo ""
  echo "Run an adversarial review of this plan against Harbor criteria:"
  echo ""
  echo "  1. PHI HANDLING — No PHI in logs, errors, or unencrypted stores."
  echo "     Only DynamoDB (SSE) and S3 (SSE) are PHI-eligible."
  echo ""
  echo "  2. SECRETS — Credentials from AWS Secrets Manager only."
  echo "     Never .env, never hardcoded, never in CloudWatch logs."
  echo ""
  echo "  3. HIPAA AUDIT TRAIL — Every write/action must log:"
  echo "     UTC timestamp + user + action + outcome."
  echo ""
  echo "  4. PATH A vs PATH B — UHC, Aetna, BCBS, Medicare, Cigna = Availity API."
  echo "     SoonerCare and small regional payers = Skyvern only."
  echo "     Never use Skyvern for a payer with an Availity connection."
  echo ""
  echo "  5. EDGE CASES — UTC timezones, exponential backoff (1s→2s→4s),"
  echo "     empty/malformed 271 responses, session expiry, 2FA, captcha,"
  echo "     Skyvern rate limits (max 5 patients in parallel)."
  echo ""
  echo "After reviewing:"
  echo "  → Material findings?  Revise $plan_path and end your turn."
  echo "  → Plan is clean?      Run 'bash .claude/hooks/mark-done.sh' then end your turn."
  echo ""
  exit 1
fi

# ─── REVIEWING → REVISING ───────────────────────────────────────────────────
# Review has been completed. Prompt Claude to decide: revise or mark done.
if [ "$phase" = "reviewing" ]; then
  sed -i "s/^phase:.*/phase: revising/" "$STATE_FILE"

  echo ""
  echo "═══════════════════════════════════════════════════════════"
  echo " HARBOR LOOP — Round $round of $max_rounds — REVISE PHASE"
  echo "═══════════════════════════════════════════════════════════"
  echo ""
  echo "Review complete. Now decide:"
  echo "  → Material findings?  Revise $plan_path and end your turn."
  echo "  → Plan is clean?      Run 'bash .claude/hooks/mark-done.sh' then end your turn."
  echo ""
  exit 1
fi

# ─── REVISING → REVIEWING ───────────────────────────────────────────────────
# Revision done. Trigger another review round.
if [ "$phase" = "revising" ]; then
  new_round=$((round + 1))

  if [ "$new_round" -gt "$max_rounds" ] 2>/dev/null; then
    echo ""
    echo "HARBOR LOOP: Max rounds ($max_rounds) reached after revision. Plan locked."
    rm -f "$STATE_FILE"
    exit 0
  fi

  sed -i "s/^phase:.*/phase: reviewing/" "$STATE_FILE"
  sed -i "s/^round:.*/round: $new_round/" "$STATE_FILE"

  echo ""
  echo "═══════════════════════════════════════════════════════════"
  echo " HARBOR LOOP — Round $new_round of $max_rounds — REVIEW PHASE"
  echo "═══════════════════════════════════════════════════════════"
  echo ""
  echo "Revision complete. Run another adversarial review of $plan_path"
  echo "against the same Harbor criteria (PHI, secrets, HIPAA trail, Path A/B, edge cases)."
  echo ""
  echo "After reviewing:"
  echo "  → Material findings?  Revise $plan_path and end your turn."
  echo "  → Plan is clean?      Run 'bash .claude/hooks/mark-done.sh' then end your turn."
  echo ""
  exit 1
fi

# Fallback — unknown phase, allow exit
exit 0
