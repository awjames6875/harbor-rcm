---
description: Begin a Harbor RCM coding session with enforced PLAN → EXECUTE → REVIEW discipline
---

# /harbor-start — Session Ritual

Usage: `/harbor-start <what you want to build>`

Example: `/harbor-start add Availity UHC integration`
Example: `/harbor-start fix the 271 parser for BCBS`
Example: `/harbor-start build the audit logger`

No room needed. Claude routes it.

---

## What you do

**Step 1 — Route the task**

Read `CLAUDE.md` routing table. Map what Adam described to the correct room:

| If the task involves… | Room |
|-----------------------|------|
| Receiving patients, webhooks, CSV uploads, OCR, validation | `1_patient-arrives` |
| Running eligibility checks, Availity API, Skyvern, payer routing | `2_check-coverage` |
| Parsing 271 responses, confidence scoring, normalizers, learning engine | `3_clean-the-response` |
| Writing to EHR, audit logging, alerts, review queue, dashboard | `4_send-and-log` |

State your routing decision out loud: "This belongs in `<room>` because `<one sentence reason>`."

**Step 2 — Load the room**

Read `<room>/CONTEXT.md`. Confirm:
- Input payload expected (from upstream room)
- Output payload emitted (to downstream room)
- Which files are already planned for this room

**Step 3 — Name today's one file**

Tell Adam which single file this task maps to (from the room's CONTEXT.md file list).
Ask: "Is this the right file, or did you have something else in mind?"
Wait for confirmation. Write to `.claude/plans/today.md`:
```
Room: <room>
File: <filename>
Task: <what we're building>
Status: IN PROGRESS
```

**Step 4 — PHI check (rooms 2, 3, 4 only)**

For `2_check-coverage`, `3_clean-the-response`, `4_send-and-log`:
Run `/harbor-review` on the plan before writing any code.
Room `1_patient-arrives` skips this step.

**Step 5 — Execute one file only**

Write the single file. No scope creep.
If a second file becomes necessary, stop and tell Adam — don't silently start it.

**Step 6 — Pre-commit review**

Load skill: `pre-commit-checklist`. Run all 17 questions. Fix everything before touching git.

**Step 7 — Atomic commit**

```
Add <filename> — <one sentence: what it does and why>
```

Update `.claude/plans/today.md`:
```
Status: DONE
Committed: <commit hash>
```

Ask Adam: "Next file, or done for today?"

---

**The loop:** Step 5 → 6 → 7 → back to Step 5 for the next file.
