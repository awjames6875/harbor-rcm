---
description: Draft an implementation plan for a Harbor RCM room with autonomous adversarial review loop
---

# /harbor:plan — Autonomous Planning Loop

Usage: `/harbor:plan <room> <topic>`

Example: `/harbor:plan 2_verification add Availity UHC integration`

## What you do

**Step 1 — Parse arguments**

Extract the first word after `/harbor:plan` as `<room>` (one of: `1_intake`, `2_verification`, `3_normalization`, `4_delivery`).
Everything after the room name is the `<topic>`.

**Step 2 — Initialize the loop**

Run:
```
bash .claude/hooks/start-loop.sh "<room>" "<topic>"
```

**Step 3 — Write the plan**

Write a structured implementation plan to `<room>/PLAN.md`. Cover:

1. **What & Why** — what is being built and why it's needed
2. **Files to create/modify** — exact paths relative to project root
3. **Logic & data flow** — step-by-step description of the main code paths
4. **Security** — PHI handling, secrets management, HIPAA audit trail
5. **Verification** — how to test this end-to-end

**Step 4 — End your turn**

Do NOT call `mark-done.sh` here. The Stop hook takes over automatically.

When the hook fires, it will give you specific review instructions for each round.
Follow them exactly. The loop runs until the plan is clean or max rounds (3) is reached.
