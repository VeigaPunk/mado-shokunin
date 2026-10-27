#!/usr/bin/env bash
# MistakeMiner seat driver (round 52, w1).
# Read-only w.r.t. the lane; both fixtures are throwaway clones under the seat scratch.
# Measurements:
#   A) the frozen C1 no-work control bytes scored as the ledger file under the base ledger
#      grammar (what quality/counters/c1-r51-ledger.py does at <rev>:quality/tool-ledger.md);
#   B) the production ledger with every pointer cell replaced by the ledger itself
#      (the isolating defect shape the round-52 C1 target names: "non-self resolvable
#      evidence targets").
set -euo pipefail

L=/home/vgpnk/Projects/shokunin/mado-shokunin
SEAT=$L/.ufo/waves/round-52/w1/MistakeMiner
REV=85d57a818c3707397e21c840b6498b105ba798aa
S=/fast/scratch/hyaku/mado-r52/MistakeMiner
COUNTER=$L/quality/counters/c1-r51-ledger.py

mkdir -p "$S/fx"
export TMPDIR=$S

run_counter () { # $1 repo  $2 rev  $3 work  $4 receipt
  local rc=0
  python3 -I "$COUNTER" --repo "$1" --rev "$2" --work "$3" >> "$4" 2>&1 || rc=$?
  printf 'exit=%d\n' "$rc" >> "$4"
}

# ---- Fixture A: control bytes as quality/tool-ledger.md ---------------------
rm -rf "$S/fx/control"
git clone --shared --no-checkout "$L" "$S/fx/control" >/dev/null 2>&1
cd "$S/fx/control"
[ "$(git rev-parse --show-toplevel)" = "$S/fx/control" ] || { echo "TOPLEVEL-MISMATCH" >&2; exit 2; }
git checkout --detach "$REV" >/dev/null 2>&1
cp "$L/.ufo/waves/round-52/controls/c1-do-nothing.md" quality/tool-ledger.md
git -c user.name=fixture -c user.email=fixture@local commit -qam "fixture A: c1-do-nothing control as the ledger"
A_REV=$(git rev-parse HEAD)
{
  echo "# Fixture A -- frozen control bytes installed at quality/tool-ledger.md"
  echo "# lane base: $REV"
  echo "# fixture toplevel: $(git rev-parse --show-toplevel)"
  echo "# fixture commit: $A_REV"
  echo "# control sha256: $(sha256sum quality/tool-ledger.md | cut -d' ' -f1)"
  echo "# cmd: python3 -I quality/counters/c1-r51-ledger.py --repo <fixture> --rev $A_REV --work <scratch>"
} > "$SEAT/receipt-control-as-ledger.txt"
run_counter "$S/fx/control" "$A_REV" "$S/work-control" "$SEAT/receipt-control-as-ledger.txt"

# ---- Fixture B: every pointer cell -> the ledger itself ---------------------
rm -rf "$S/fx/allself"
git clone --shared --no-checkout "$L" "$S/fx/allself" >/dev/null 2>&1
cd "$S/fx/allself"
[ "$(git rev-parse --show-toplevel)" = "$S/fx/allself" ] || { echo "TOPLEVEL-MISMATCH" >&2; exit 2; }
git checkout --detach "$REV" >/dev/null 2>&1
python3 - "$PWD/quality/tool-ledger.md" <<'PY'
import re, sys
p = sys.argv[1]
lines = open(p, encoding="utf-8").read().splitlines(True)
n = 0
fenced = False
for i, line in enumerate(lines):
    s = line.rstrip("\n")
    if s.strip().startswith(("```", "~~~")):
        fenced = not fenced
        continue
    if fenced or not s.startswith("| `"):
        continue
    cells = [c.strip() for c in s.strip().strip("|").split("|")]
    if len(cells) != 3:
        continue
    new = "| %s | %s | `quality/tool-ledger.md` |\n" % (cells[0], cells[1])
    lines[i] = new
    n += 1
open(p, "w", encoding="utf-8").writelines(lines)
print("rewritten_rows=%d" % n)
PY
git -c user.name=fixture -c user.email=fixture@local commit -qam "fixture B: every ledger pointer -> the ledger itself"
B_REV=$(git rev-parse HEAD)
{
  echo "# Fixture B -- production ledger, only the pointer cell rewritten to quality/tool-ledger.md"
  echo "# lane base: $REV"
  echo "# fixture toplevel: $(git rev-parse --show-toplevel)"
  echo "# fixture commit: $B_REV"
  echo "# diff stat: $(git diff --shortstat "$REV" HEAD)"
  echo "# cmd: python3 -I quality/counters/c1-r51-ledger.py --repo <fixture> --rev $B_REV --work <scratch>"
} > "$SEAT/receipt-allself-at-base.txt"
run_counter "$S/fx/allself" "$B_REV" "$S/work-allself" "$SEAT/receipt-allself-at-base.txt"
