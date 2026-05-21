---
name: harbor-rcm-knowledge-capture
description: ALWAYS trigger this skill when Claude Code has just solved a non-obvious problem, discovered a payer quirk, figured out a workaround for an API limitation, debugged something that took more than two attempts, or learned anything that would have saved time if known earlier. Also trigger when Adam says "remember this," "add this to the skill," "we should capture that," or "future me needs to know this." This skill turns every hard-won insight into permanent institutional knowledge that makes every future client install faster and smarter than the last.
---

# Harbor RCM — Knowledge Capture Protocol

You just figured something out the hard way. Maybe it took three attempts to get the Availity token refresh logic right. Maybe you discovered that UHC formats their 271 response differently on Fridays (it happens). Maybe you found a race condition in the confidence scorer that only appears when two verifications run simultaneously for the same payer. Whatever it was — that knowledge currently exists only in this conversation, and conversations expire.

Your job right now is to make sure that knowledge survives this conversation and becomes part of the permanent skill library that every future Claude Code session in this project can access. This process takes five minutes. The return on those five minutes is that every future developer (including future Claude Code sessions) who encounters the same problem will solve it in thirty seconds instead of three hours.

---

## Step 1 — Classify What You Just Learned

Before writing anything down, identify which category this knowledge belongs to. The category determines which skill file gets updated and how the knowledge should be formatted.

A **payer quirk** is something specific to how one insurance company formats their data, handles their portal, or behaves differently from the X12 standard. Example: UHC puts copay under Service Type Code 98 instead of Code 1. This goes into `availity-271-field-map/SKILL.md` under the Payer-Specific Quirks section.

A **failure mode** is a way the system can break that wasn't previously documented — a new scenario where ARIA produces wrong output, fails silently, or creates a compliance risk. Example: discovering that Skyvern returns status "completed" with empty output when it times out on SoonerCare's portal. This goes into `premortem-scenarios/SKILL.md` as a new entry under the relevant room's risk notes.

A **test case** is a scenario you discovered during debugging that should have been caught by a test but wasn't. Example: finding that the normalizer crashes when the 271 response has no EB segments at all (patient not found). This goes into `testing-protocol/SKILL.md` as a new required test case for the relevant room.

A **security or compliance finding** is anything related to PHI handling, credential management, or audit logging that revealed a gap in the current approach. This goes into `hipaa-guardrails/SKILL.md`.

A **client-specific pattern** is something that is true for one particular client's setup — their EHR version, their payer mix, their staff workflow — that future Claude Code sessions working on that client's account should know. This gets written into a new file: `docs/client-profiles/[client-name].md`. Create this file if it doesn't exist yet.

A **general engineering pattern** is a solution to a coding problem that applies across the codebase — a retry pattern, a mocking approach for tests, a way to structure Pydantic validators for 271 data. This goes into a new skill file: `engineering-patterns/SKILL.md`. Create this skill if it doesn't exist yet.

---

## Step 2 — Write the Knowledge Entry

Every knowledge entry follows the same four-part structure regardless of which skill file it goes into. This structure exists because the most common failure of knowledge capture is writing what you did without explaining why it matters, which means future readers learn the fact but not the reasoning behind it.

The four parts are the **problem statement** (what situation triggers this knowledge — be specific enough that someone reading it months later would recognize they're in the same situation), the **what I tried that didn't work** section (this is the most undervalued part — documenting failed approaches saves the next person from repeating them, which is often worth more than documenting the solution itself), the **solution** (the actual fix, with enough specificity that it can be implemented without needing to rediscover anything), and the **why it works** explanation (the underlying reason this solution is correct, which is what lets future readers adapt it to slightly different situations rather than applying it rigidly where it doesn't fit).

Here is a template showing what a complete knowledge entry looks like. Notice that it reads like a short story, not a bullet list, because knowledge in narrative form is easier to retrieve and apply than knowledge in fragment form.

```markdown
### [Descriptive title that names the specific problem]

**When this applies:** [The specific situation that triggers this knowledge.
Be precise — name the payer, the field, the error code, whatever makes
this recognizable to someone who encounters the same thing.]

**What didn't work:** [The approaches that seemed reasonable but failed,
and why they failed. This section prevents the next person from spending
two hours rediscovering that these approaches don't work.]

**The solution:** [What actually works, with enough specificity to implement
it. Include code snippets if the solution involves a specific implementation
pattern. Reference the exact field names, error codes, or configuration
values involved.]

**Why it works:** [The underlying reason this solution is correct. If you
understand why something works, you can adapt it. If you only know what
to do, you're stuck when the situation is slightly different.]

**Date discovered:** [YYYY-MM-DD] **Client context:** [Which client install
or test scenario revealed this, if relevant.]
```

---

## Step 3 — Update the Right Skill File

Once you have written the knowledge entry, add it to the correct skill file. Open the file, navigate to the relevant section, and paste the entry in. If no obvious section exists, add a new one with a clear heading. Do not create a new skill file for a single entry unless the knowledge clearly belongs to a category that has no existing home — most knowledge belongs somewhere in the five existing Harbor RCM skills.

After updating the skill file, save it and confirm the change with a git commit using a message that describes what knowledge was added. A good commit message for a knowledge update looks like: "Add UHC Service Type Code 98 quirk to 271 field map — discovered during Maria Gonzalez test case on 2026-05-01."

This commit message matters because your git history becomes a timeline of everything the system learned. Six months from now, if a client reports a problem with UHC copay extraction, you can look at the git log and immediately see every time UHC-specific knowledge was added to the system.

---

## Step 4 — Check Whether This Finding Changes Any Existing Code

Some knowledge discoveries are additive — they reveal a new edge case that wasn't handled, so you add new handling for it. But some discoveries are corrective — they reveal that existing code has been handling something wrong all along, perhaps silently producing incorrect output. Before closing this knowledge capture session, ask yourself explicitly: does what I just learned mean that any code I have already written is wrong?

If the answer is yes, fix the existing code before moving on to new work. A knowledge capture that documents a bug without fixing it is incomplete. The skill file should reflect the correct behavior, and the code should implement the correct behavior, and those two things must be in sync.

---

## The Compounding Math

Here is why this protocol matters at the scale you are thinking about. Assume that each client install teaches you three things you didn't know before — one payer quirk, one edge case in the normalizer, one workflow pattern specific to that EHR setup. Without knowledge capture, each of those three things lives in your head and possibly in a chat conversation. With knowledge capture, each of those three things becomes a permanent part of the skill library that every future session reads automatically.

After one client, you have three things captured. After five clients, you have fifteen things captured — and your fifth client install is fifteen problems faster than your first because Claude Code walks in already knowing the answers to fifteen questions that took you hours to figure out the first time. After ten clients, you have thirty things captured, and a new install that used to take you eight hours takes you two hours because Claude Code has already seen most of what it will encounter. The knowledge compounds. The time savings compound. The expertise becomes the asset that makes Harbor RCM hard to replicate, not the code itself.

This is the moat. Not the software. The accumulated institutional knowledge of what breaks, what works, and why — captured systematically, one insight at a time, starting from the very first client.
