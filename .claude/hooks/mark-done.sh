#!/usr/bin/env bash
# Marks the active Harbor planning loop as complete.
# Call this when adversarial review finds no material issues.

STATE_FILE=".claude/state/loop.yaml"

if [ ! -f "$STATE_FILE" ]; then
  echo "No active loop found. Nothing to mark done."
  exit 0
fi

sed -i "s/^phase:.*/phase: done/" "$STATE_FILE"

plan_path=$(grep '^plan_path:' "$STATE_FILE" | awk '{print $2}')
round=$(grep '^round:' "$STATE_FILE" | awk '{print $2}')

echo ""
echo "HARBOR LOOP: Plan locked and clean after $round round(s)."
echo "  Locked plan: $plan_path"
echo ""
echo "End your turn. The Stop hook will allow clean exit."
echo ""
