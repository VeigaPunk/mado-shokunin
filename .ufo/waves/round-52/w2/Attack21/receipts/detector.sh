#!/usr/bin/env bash
# Attack21 bounded detector — C1 TMPDIR/workdir boundary.
# Usage: detector.sh <counter.py> <receipt-file>
# Every probe runs under bwrap: fleet root read-only, /tmp /var/tmp /dev/shm private tmpfs,
# scratch rw. No probe can write the host in ANY outcome branch (pristine, mutant, restored).
set -u
COUNTER="$1"; OUT="$2"
LANE=/home/vgpnk/Projects/shokunin/mado-shokunin
REV=85d57a818c3707397e21c840b6498b105ba798aa
S=/fast/scratch/hyaku/mado-r52/Attack21
FIX=$S/fixture/repo
CTRL=$LANE/.ufo/waves/round-52/controls/c1-do-nothing.md
F3=$LANE/.ufo/waves/round-52/w1/C1Simplify/control-F3-forged.md

bw() {  # bwrap: / read-only, private temp roots, scratch + /dev + /proc live
  bwrap --ro-bind / / --tmpfs /tmp --tmpfs /var/tmp --tmpfs /dev/shm \
        --dev-bind /dev /dev --proc /proc \
        --bind "$S" "$S" \
        env -u TMPDIR HOME="$S/home" PYTHONDONTWRITEBYTECODE=1 "$@"
}

probe() { # probe <name> <expected-note> -- cmd...
  local name="$1" note="$2"; shift 2; shift # drop --
  echo "## PROBE $name ($note)" >>"$OUT"
  echo "\$ $*" >>"$OUT"
  "$@" >>"$OUT" 2>&1; local rc=$?
  echo "exit=$rc" >>"$OUT"
  echo "$name rc=$rc" >>"$OUT.summary"
}

probe_bw() { # like probe but under bwrap; work-root residue check inside private tmpfs
  local name="$1" note="$2" workroot="$3"; shift 3
  echo "## PROBE $name ($note)" >>"$OUT"
  echo "\$ (bwrap) $*" >>"$OUT"
  bw "$@" >>"$OUT" 2>&1; local rc=$?
  if [ -n "$workroot" ]; then
    if bw test -e "$workroot"; then echo "residue: $workroot EXISTS inside sandbox" >>"$OUT"; else echo "residue: $workroot absent inside sandbox" >>"$OUT"; fi
  fi
  echo "exit=$rc" >>"$OUT"
  echo "$name rc=$rc" >>"$OUT.summary"
}

: >"$OUT"; : >"$OUT.summary"
echo "# variant: $COUNTER" >>"$OUT"
echo "# sha256: $(sha256sum "$COUNTER" | cut -d' ' -f1)" >>"$OUT"

# host-side guard before anything: bwrap available?
command -v bwrap >/dev/null || { echo "FATAL: bwrap missing" >>"$OUT"; exit 97; }

# G — frozen green case: production ledger at pinned base rev (default ledger = blob)
probe_bw G-green "claim: production pass at frozen rev" "" \
  python3 -I "$COUNTER" --repo "$LANE" --rev "$REV" --work "$S/runs/g"

# R — frozen red case: committed do-nothing control
probe_bw R-red "claim: control fail at frozen rev" "" \
  python3 -I "$COUNTER" --repo "$LANE" --rev "$REV" --work "$S/runs/r" --ledger "$CTRL"

# B1 — W1-specified control: explicit --work under a system temp root must be refused (exit 2)
probe_bw B1-worktmp "W1 control: --work /tmp refused before creation" "/tmp/c1r52-attack21-refused" \
  python3 -I "$COUNTER" --repo "$LANE" --rev "$REV" --work /tmp/c1r52-attack21-refused

# B2 — W1-specified control: no --work and TMPDIR unset must be a setup error (exit 2)
probe_bw B2-notmp "W1 control: --work or TMPDIR required" "" \
  python3 -I "$COUNTER" --repo "$LANE" --rev "$REV"

# B3 — W1-specified control: TMPDIR pointing at a system temp root must be refused (exit 2)
echo "## PROBE B3-tmpdirtmp (W1 control: TMPDIR=/tmp/... refused)" >>"$OUT"
echo "\$ (bwrap, TMPDIR=/tmp/c1r52-attack21-tmp) counter --repo LANE --rev REV --ledger CTRL" >>"$OUT"
bw env TMPDIR=/tmp/c1r52-attack21-tmp python3 -I "$COUNTER" --repo "$LANE" --rev "$REV" --ledger "$CTRL" >>"$OUT" 2>&1; rc=$?
echo "exit=$rc" >>"$OUT"; echo "B3 rc=$rc" >>"$OUT.summary"

# B4 — valid scratch TMPDIR, no --work: runs; nothing may be written into TMPDIR in measure mode
rm -rf "$S/tmp"; mkdir -p "$S/tmp"
echo "## PROBE B4-scratchtmp (valid TMPDIR; measure mode writes nothing)" >>"$OUT"
echo "\$ (bwrap, TMPDIR=$S/tmp) counter --repo LANE --rev REV" >>"$OUT"
bw env TMPDIR="$S/tmp" python3 -I "$COUNTER" --repo "$LANE" --rev "$REV" >>"$OUT" 2>&1; rc=$?
echo "exit=$rc" >>"$OUT"
echo "residue in TMPDIR after run: $(ls -A "$S/tmp" | wc -l) entries" >>"$OUT"
echo "B4 rc=$rc" >>"$OUT.summary"

# S1 — registration C1: selftest with explicit red/green receipts must exist and pass
probe_bw S1-selftest "registration: selftest red/green receipts" "" \
  python3 -I "$COUNTER" --selftest --repo "$LANE" --rev "$REV" --work "$S/runs/s1"

# S2 — selftest invoked standalone (no --repo) must not be required to fail via argparse
probe_bw S2-selftest-standalone "selftest standalone invocation shape" "" \
  python3 -I "$COUNTER" --selftest --work "$S/runs/s2"

# P — pin boundary: committed green fixture, then DIRTY working tree, same --rev.
# Verdict must come from the pinned commit, not the dirty worktree.
if [ ! -d "$FIX" ]; then
  git init -q "$FIX"; git -C "$FIX" config user.email a@b; git -C "$FIX" config user.name t
  mkdir -p "$FIX/tools" "$FIX/quality"
  printf '#!/usr/bin/env python3\n# alpha resolver for widget registry\n' >"$FIX/tools/mado-alpha.py"
  printf '#!/usr/bin/env python3\n# beta resolver for widget registry\n' >"$FIX/tools/mado-beta.py"
  printf 'evidence doc: mado-alpha.py mado-beta.py\n' >"$FIX/quality/notes.md"
  printf '| tools/mado-alpha.py | alpha resolver for widget registry. | quality/notes.md |\n| tools/mado-beta.py | beta resolver for widget registry. | quality/notes.md |\n' >"$FIX/quality/tool-ledger.md"
  git -C "$FIX" add -A; git -C "$FIX" commit -qm fixture
fi
FIXREV=$(git -C "$FIX" rev-parse HEAD)
printf '| `tools/mado-alpha.py` | self circular no context. | `tools/mado-alpha.py` |\n' >>"$FIX/quality/tool-ledger.md"
probe_bw P-pin "predicate: runs at requested pinned revision (dirty worktree ignored)" "" \
  python3 -I "$COUNTER" --repo "$FIX" --rev "$FIXREV" --work "$S/runs/p"
git -C "$FIX" checkout -q -- .   # restore fixture tree

# F3 — secondary: W1 counterfeit-context control against the candidate (adjacent finding)
probe_bw F3-counterfeit "W1 signal: F3 forged-context control vs candidate" "" \
  python3 -I "$COUNTER" --repo "$LANE" --rev "$REV" --work "$S/runs/f3" --ledger "$F3"

# host-side leak check: private tmpfs means nothing real was ever creatable
echo "## HOST LEAK CHECK" >>"$OUT"
for p in /tmp/c1r52-attack21-refused /tmp/c1r52-attack21-tmp; do
  if [ -e "$p" ]; then echo "LEAK: $p exists on host" >>"$OUT"; else echo "host $p absent (no leak)" >>"$OUT"; fi
done
echo "# summary:" >>"$OUT"; cat "$OUT.summary" >>"$OUT"
