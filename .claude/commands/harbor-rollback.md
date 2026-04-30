---
description: Nuclear cleanup — wipe all Harbor loop state when cancel didn't work
---

# /harbor:rollback — Nuclear Reset

Use this when `/harbor:cancel` didn't work, or when the loop is stuck and won't start a new one.

**Your code files and PLAN.md are never touched. Only ephemeral state is removed.**

## What you do

1. Run:
   ```
   rm -rf .claude/state/ && echo "All loop state cleared. Harbor loop fully reset."
   ```

2. Report that the state folder has been wiped and the loop is reset.

3. The user can now start a new loop with `/harbor:plan`.
