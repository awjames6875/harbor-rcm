#!/usr/bin/env bash
# Initializes a new Harbor planning loop.
# Usage: bash .claude/hooks/start-loop.sh <room> <topic>

ROOM="${1:-}"
TOPIC="${2:-}"

if [ -z "$ROOM" ] || [ -z "$TOPIC" ]; then
  echo "Usage: bash .claude/hooks/start-loop.sh <room> \"<topic>\""
  echo "Example: bash .claude/hooks/start-loop.sh 2_check-coverage \"add Availity UHC integration\""
  exit 1
fi

# Abort if a loop is already active
if [ -f ".claude/state/loop.yaml" ]; then
  current_phase=$(grep '^phase:' ".claude/state/loop.yaml" | awk '{print $2}')
  if [ "$current_phase" != "done" ] && [ "$current_phase" != "cancelled" ]; then
    echo "ERROR: A loop is already active (phase=$current_phase)."
    echo "Run /harbor:cancel or /harbor:rollback before starting a new loop."
    exit 1
  fi
fi

# Room 1 has no PHI contact — skip Codex review. Rooms 2/3/4 require full review.
if [ "$ROOM" = "1_patient-arrives" ]; then
  MAX_ROUNDS=0
else
  MAX_ROUNDS=3
fi

mkdir -p .claude/state

cat > .claude/state/loop.yaml << EOF
phase: drafting
round: 0
max_rounds: $MAX_ROUNDS
topic: "$TOPIC"
room: "$ROOM"
plan_path: "$ROOM/PLAN.md"
EOF

echo ""
echo "HARBOR LOOP: Started."
echo "  Topic:  $TOPIC"
echo "  Room:   $ROOM"
echo "  Plan:   $ROOM/PLAN.md"
echo ""
echo "Write your implementation plan to $ROOM/PLAN.md then end your turn."
echo "The Stop hook will automatically drive the review loop."
echo ""
