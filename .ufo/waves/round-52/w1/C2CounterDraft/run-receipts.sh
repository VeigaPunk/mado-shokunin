#!/usr/bin/env bash
# Regenerate every receipt of the C2CounterDraft seat, from scratch, in one run.
# Usage: run-receipts.sh <lane repo> <seat dir> <scratch dir>
set -euo pipefail

LANE="$1"
SEAT="$2"
SCRATCH="$3"
COUNTER="$SEAT/c2-r52-proposition-entry.py"

export TMPDIR="$SCRATCH"
mkdir -p "$SCRATCH"

echo "=== 1. base (no-work control): the target entry is absent at the frozen base"
set +e
python3 -I "$COUNTER" --repo "$LANE" --rev 85d57a818c3707397e21c840b6498b105ba798aa \
    --work "$SCRATCH/w-base" > "$SCRATCH/r-base.txt" 2>&1
echo "exit=$?" >> "$SCRATCH/r-base.txt"
set -e
cat "$SCRATCH/r-base.txt"

echo "=== 2. lane tip"
set +e
python3 -I "$COUNTER" --repo "$LANE" --rev HEAD --work "$SCRATCH/w-tip" > "$SCRATCH/r-tip.txt" 2>&1
echo "exit=$?" >> "$SCRATCH/r-tip.txt"
set -e
cat "$SCRATCH/r-tip.txt"

echo "=== 3. green fixture"
python3 "$SEAT/make-fixture.py" --lane "$LANE" --work "$SCRATCH" --name fixture | tee "$SCRATCH/r-fixture-build.txt"
REV=$(git -C "$SCRATCH/fixture" rev-parse HEAD)
set +e
python3 -I "$COUNTER" --repo "$SCRATCH/fixture" --rev "$REV" \
    --entry corpus/knowledge/hyprland-dispatcher-action-effects-r52.md \
    --work "$SCRATCH/w-green" > "$SCRATCH/r-green.txt" 2>&1
echo "exit=$?" >> "$SCRATCH/r-green.txt"
set -e
cat "$SCRATCH/r-green.txt"

echo "=== 4. mutants"
set +e
python3 "$SEAT/mutants.py" --lane "$LANE" --work "$SCRATCH/mut" --fixture "$SCRATCH/fixture" \
    --counter "$COUNTER" --entry corpus/knowledge/hyprland-dispatcher-action-effects-r52.md \
    > "$SCRATCH/r-mutants.txt" 2>&1
echo "exit=$?" >> "$SCRATCH/r-mutants.txt"
set -e
cat "$SCRATCH/r-mutants.txt"

echo "=== 5. block form + setup errors"
set +e
python3 "$SEAT/blockform-check.py" --lane "$LANE" --work "$SCRATCH/bf" \
    --counter "$COUNTER" > "$SCRATCH/r-blockform.txt" 2>&1
echo "exit=$?" >> "$SCRATCH/r-blockform.txt"
set -e
cat "$SCRATCH/r-blockform.txt"

echo "=== 6. the real C2EntryDraft draft, staged as-is"
set +e
python3 "$SEAT/make-draft-fixture.py" --lane "$LANE" --work "$SCRATCH/df" \
    --counter "$COUNTER" > "$SCRATCH/r-draft-as-is.txt" 2>&1
echo "exit=$?" >> "$SCRATCH/r-draft-as-is.txt"
set -e
cat "$SCRATCH/r-draft-as-is.txt"

echo "=== 7. the same draft with the two markdown-table corrections (satisfiability control)"
set +e
python3 "$SEAT/make-draft-fixture.py" --lane "$LANE" --work "$SCRATCH/dfx" \
    --counter "$COUNTER" --fix > "$SCRATCH/r-draft-fixed.txt" 2>&1
echo "exit=$?" >> "$SCRATCH/r-draft-fixed.txt"
set -e
cat "$SCRATCH/r-draft-fixed.txt"

echo "=== 8. a recycled round-51 entry at the target path"
set +e
bash "$SEAT/recycled-check.sh" "$LANE" "$SEAT" "$SCRATCH" > "$SCRATCH/r-recycled.txt" 2>&1
echo "exit=$?" >> "$SCRATCH/r-recycled.txt"
set -e
cat "$SCRATCH/r-recycled.txt"

echo "=== receipts in $SCRATCH"
