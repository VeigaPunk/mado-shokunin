#!/usr/bin/env bash
# run-instruments.sh — reproduce every arm quoted in this seat's criteria.md.
#
#   LANE=~/Projects/shokunin/mado-shokunin ./run-instruments.sh /fast/scratch/hyaku/mado-r50/ScrQualityR50/work
#
# The work dir must be outside /tmp, /var/tmp and /dev/shm (round-49 SentScratch rule) and is
# removed on exit; every fixture repository is created there, so the fixture inputs that matter
# are the committed seeds under ./fixtures/ plus the real lane/fleet bytes cited by path.
set -u
LANE=${LANE:?set LANE to the lane root}
FLEET=$(dirname "$LANE")
R49_REV=8a370cd4                  # round-49 closure (lane)
R49_REPORT_REV=b0184c43           # round-49 report commit (fleet)
S=${1:-}
case "$S" in
  "")         echo "usage: LANE=<lane> run-instruments.sh <work-dir>" >&2; exit 2 ;;
  /tmp/*|/var/tmp/*|/dev/shm/*)
              echo "REFUSE: work dir under /tmp, /var/tmp or /dev/shm: $S" >&2; exit 2 ;;
esac
ulimit -f 65536
mkdir -p "$S" || exit 2
trap 'rm -rf -- "$S"' EXIT
HERE=$(cd "$(dirname "$0")" && pwd)
PINS=$LANE/.ufo/waves/round-49/w1/ScrSkill/pins

# print the command with the home directory as `~` and the work dir as $WORK: a receipt never
# carries the account name or a scratch path as evidence (host guard, round-48 M48-10)
show() { local c; c=$(printf '%q ' "$@"); c=${c//$HOME/\~}; c=${c//$S/\$WORK}; printf '%s\n' "\$ ${c% }"; }
run() { show "$@"; "$@" || echo "rc=$?"; }

echo "=== 100 RED (M49-1 reproduction: the model gave the shared translation state the bind mask) ==="
run python3 -I "$HERE/check100-state-cite.py" --claims "$HERE/fixtures/claims-red.txt" --source "$PINS"
echo
echo "=== 100 GREEN (three claims, each citing the line that sets the state) ==="
run python3 -I "$HERE/check100-state-cite.py" --claims "$HERE/fixtures/claims-green.txt" --source "$PINS"
echo
echo "=== 100 CONTRADICTED (read-only cite repaired, claimed value still contradicts the setter) ==="
run python3 -I "$HERE/check100-state-cite.py" --claims "$HERE/fixtures/claims-contradicted.txt" --source "$PINS"
echo

# ---- 101 fixtures -------------------------------------------------------------------------
D101=$(mktemp -d -p "$S" fx101.XXXXXX)
git -C "$D101" init -q
git -C "$D101" config user.name fixture
git -C "$D101" config user.email fixture@example.invalid
test "$(git -C "$D101" rev-parse --show-toplevel)" = "$D101" || { echo "REFUSE: fixture toplevel mismatch" >&2; exit 2; }
mkdir -p "$D101/.ufo/waves/round-49/w1/ExecRefKeysymA/receipts"
cp "$HERE/fixtures/ExecRefKeysymA.md" "$D101/.ufo/waves/round-49/w1/ExecRefKeysymA.md"
git -C "$D101" add -A && git -C "$D101" commit -qm "report committed, seat dir empty (M49-3 ordering)"
RED101=$(git -C "$D101" rev-parse HEAD)
printf 'parity lines\n' > "$D101/.ufo/waves/round-49/w1/ExecRefKeysymA/receipts/parity.txt"
printf 'run log\n'      > "$D101/.ufo/waves/round-49/w1/ExecRefKeysymA/receipts/run.txt"
git -C "$D101" add -A && git -C "$D101" commit -qm "deliverables written"
GREEN101=$(git -C "$D101" rev-parse HEAD)

echo "=== 101 RED (fixture: report names its two deliverables, both absent at the report's commit) ==="
run python3 -I "$HERE/check101-deliverables.py" --repo "$D101" --rev "$RED101" \
    --report .ufo/waves/round-49/w1/ExecRefKeysymA.md --require-declaration
echo
echo "=== 101 GREEN (same report, deliverables present at the later commit) ==="
run python3 -I "$HERE/check101-deliverables.py" --repo "$D101" --rev "$GREEN101" \
    --report .ufo/waves/round-49/w1/ExecRefKeysymA.md --require-declaration
echo
echo "=== 101 REAL POPULATION, prose tokens (why the population is declarations: these would be false positives) ==="
run python3 -I "$HERE/measure-prose-population.py" --repo "$LANE" --rev "$R49_REV" \
    --wave-glob '.ufo/waves/round-48/w1/*.md'
run python3 -I "$HERE/measure-prose-population.py" --repo "$LANE" --rev "$R49_REV" \
    --wave-glob '.ufo/waves/round-49/w1/*.md'
echo
echo "=== 101 REAL POPULATION, round-50 w1 reports (worktree, --file) ==="
(cd "$LANE" && run python3 -I "$HERE/check101-deliverables.py" --file .ufo/waves/round-50/w1/*.md)
echo

# ---- 102 fixtures -------------------------------------------------------------------------
D102=$(mktemp -d -p "$S" fx102.XXXXXX)
git -C "$D102" init -q
git -C "$D102" config user.name fixture
git -C "$D102" config user.email fixture@example.invalid
test "$(git -C "$D102" rev-parse --show-toplevel)" = "$D102" || { echo "REFUSE: fixture toplevel mismatch" >&2; exit 2; }
mkdir -p "$D102/.ufo/reports/round-X" "$D102/rounds/round-X" "$S/fx102-none" "$S/fx102-note/w1"
cp "$HERE/fixtures/w1-dispatch.json" "$D102/rounds/round-X/"
cp "$HERE/fixtures/mado-round-X.md" "$D102/.ufo/reports/round-X/mado.md"
git -C "$D102" add -A && git -C "$D102" commit -qm "report committed before the wave finished"
C1=$(git -C "$D102" rev-parse HEAD)
cp "$HERE/fixtures/w1-results-full.json" "$D102/rounds/round-X/w1-results.json"
git -C "$D102" add -A && git -C "$D102" commit -qm "wave results, every seat settled"
C2=$(git -C "$D102" rev-parse HEAD)
cp "$HERE/fixtures/w1-dispatch.json" "$S/fx102-none/"
cp "$HERE/fixtures/w1-dispatch.json" "$S/fx102-note/"
cp "$HERE/fixtures/w1-results-note.json" "$S/fx102-note/w1-results.json"
cp "$HERE/fixtures/mado-round-X.md" "$D102/.ufo/reports/round-X/mado.md"

echo "=== 102 RED A (fixture worktree: report present, dispatched wave has no results file) ==="
run python3 -I "$HERE/check102-wave-done.py" --repo "$D102" --round-dir "$S/fx102-none" \
    --report .ufo/reports/round-X/mado.md
echo
echo "=== 102 RED B (real round-49 closure: report committed at $R49_REPORT_REV, no results file at $R49_REV) ==="
run python3 -I "$HERE/check102-wave-done.py" --repo "$FLEET" --round-dir "$LANE/.ufo/waves/round-49" \
    --results-rev "$R49_REV" --rev "$R49_REPORT_REV" --report .ufo/reports/round-49/mado.md
echo
echo "=== 102 NOTE ARM (results present but one seat has no output and no seat report) ==="
run python3 -I "$HERE/check102-wave-done.py" --repo "$D102" --round-dir "$S/fx102-note" \
    --report .ufo/reports/round-X/mado.md
echo "--- NOTE ARM with .ufo/waves/round-X/w1/ExecB.md present ---"
printf '# ExecB report\n' > "$S/fx102-note/w1/ExecB.md"
cp "$HERE/fixtures/w1-dispatch.json" "$S/fx102-note/"
run python3 -I "$HERE/check102-wave-done.py" --repo "$D102" --round-dir "$S/fx102-note" \
    --report .ufo/reports/round-X/mado.md
echo
echo "=== 102 GREEN A (fixture audit at the commit that carries the results) ==="
run python3 -I "$HERE/check102-wave-done.py" --repo "$D102" --round-dir "$D102/rounds/round-X" \
    --results-rev "$C2" --rev "$C2" --report .ufo/reports/round-X/mado.md
echo
echo "=== 102 GREEN B (real round-48 closure: three waves, results tracked at $R49_REV) ==="
run python3 -I "$HERE/check102-wave-done.py" --repo "$LANE" --round-dir "$LANE/.ufo/waves/round-48" \
    --results-rev "$R49_REV"

echo
echo "=== 102 LANE INSTRUMENT (ExecWaveDone's draft quality/check-wave-done.py at the same two revisions) ==="
WL=$LANE/.ufo/waves/round-50/w1/ExecWaveDone/check-wave-done.py
if [ -f "$WL" ]; then
  mkdir -p "$S/home"
  SANE=(env -i PATH=/usr/bin:/bin HOME="$S/home" XDG_CACHE_HOME="$S/home/.cache" \
        XDG_CONFIG_HOME="$S/home/.config" XDG_DATA_HOME="$S/home/.local/share" \
        XDG_STATE_HOME="$S/home/.local/state" TMPDIR="$S")
  run "${SANE[@]}" python3 -I "$WL" --repo "$LANE" --rev "$R49_REV" --round 49
  run "${SANE[@]}" python3 -I "$WL" --repo "$LANE" --rev "$R49_REV" --round 48
else
  echo "SKIP: $WL absent (seat ExecWaveDone has not written its draft)"
fi
