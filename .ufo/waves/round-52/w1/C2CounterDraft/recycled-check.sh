#!/usr/bin/env bash
# The no-work control in its strongest form: the round-51 entry's bytes placed at the target
# path.  The counter must MISS it - a recycled body is not a new proposition-bound entry.
# Usage: recycled-check.sh <lane repo> <seat dir> <scratch dir>
set -euo pipefail

LANE="$1"
SEAT="$2"
SCRATCH="$3"
COUNTER="$SEAT/c2-r52-proposition-entry.py"
W="$SCRATCH/recycled"

rm -rf "$W"
mkdir -p "$W"
git clone --no-hardlinks --quiet "$LANE" "$W/repo"
git -C "$W/repo" rev-parse --show-toplevel
git -C "$W/repo" checkout --quiet 85d57a818c3707397e21c840b6498b105ba798aa
git -C "$W/repo" checkout -q -b feature/recycled
mkdir -p "$W/repo/corpus/knowledge"
cp "$W/repo/corpus/knowledge/hyprland-dispatcher-dispatch-r51.md" \
   "$W/repo/corpus/knowledge/hyprland-dispatcher-action-effects-r52.md"
python3 - "$W/repo/corpus/README.md" <<'PY'
import sys
p = sys.argv[1]
s = open(p).read()
s += "\n| `knowledge/hyprland-dispatcher-action-effects-r52.md` (MADO-R52-1) | Recycled r51 body. |\n"
open(p, "w").write(s)
PY
git -C "$W/repo" add -A
git -C "$W/repo" -c user.name=r -c user.email=r@l commit -q -m "recycled r51 entry at the target path"
REV=$(git -C "$W/repo" rev-parse HEAD)

export TMPDIR="$W"
set +e
python3 -I "$COUNTER" --repo "$W/repo" --rev "$REV" \
    --entry corpus/knowledge/hyprland-dispatcher-action-effects-r52.md --work "$W/w"
echo "exit=$?"
set -e
