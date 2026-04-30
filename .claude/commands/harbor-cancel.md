---
description: Gracefully cancel the active Harbor planning loop
---

# /harbor:cancel — Graceful Stop

Cancels the active loop without touching your code or plan files.

## What you do

1. Check if `.claude/state/loop.yaml` exists.
   - If it does not exist, say "No active loop found."
   - If it exists, run:
     ```
     bash -c "sed -i 's/^phase:.*/phase: cancelled/' .claude/state/loop.yaml && echo 'Loop cancelled. State preserved for audit.'"
     ```

2. End your turn. The Stop hook will see `phase: cancelled`, remove the state file, and allow clean exit.
