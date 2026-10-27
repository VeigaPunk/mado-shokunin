#!/usr/bin/env bash
# run-instruments.sh - run the five candidate-criterion instruments, red and green arms.
# Writes only to stdout; the seat redirects into receipts/criteria-red.txt.
# Every fixture is shape-only: <OPHOME> and <SCRATCH> resolve at run time, and no
# operator home path is committed or written.
set -uo pipefail
ulimit -f 65536

HERE=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
LANE=$(git -C "$HERE" rev-parse --show-toplevel) || exit 2
SEAT=.ufo/waves/round-49/w1/ScrQuality   # relative: the receipt carries no absolute lane path
S=${SCRATCH_DIR:-/fast/scratch/hyaku/mado-r49/ScrQuality}
mkdir -p "$S"
trap 'rm -rf -- "$S/fixture-repo" "$S/trace-real.txt"' EXIT
export TMPDIR=$S
export HOME=$S/fakehome XDG_CACHE_HOME=$S/fakehome/cache XDG_CONFIG_HOME=$S/fakehome/config \
       XDG_DATA_HOME=$S/fakehome/data XDG_STATE_HOME=$S/fakehome/state
mkdir -p "$HOME" "$XDG_CACHE_HOME" "$XDG_CONFIG_HOME" "$XDG_DATA_HOME" "$XDG_STATE_HOME"

REV=${BASE_REV:-03e4ae76aff7a4be59cb69970dd553baa319695a}
OPHOME_FAKE=/home/U
cd "$LANE" || exit 2

run() {
    local label=$1
    shift
    printf '$ %s\n' "$*"
    "$@"
    printf 'exit=%s\n\n' "$?"
}

echo "# ScrQuality candidate-criterion instruments (QUALITY 100-104 draft)"
echo "# repo=$(basename "$LANE") toplevel_asserted=yes base=$REV date=$(date -Is)"
echo "# fixtures are shape-only; <OPHOME> resolves to $OPHOME_FAKE, <SCRATCH> to \$TMPDIR"
echo "# python: $(python3 -V 2>&1); host user paths are never written"
echo

echo "## 100 red: reconstructed M48-10 trace (write under an operator home)"
run "check100 red trace" python3 -I "$SEAT/check100-hostwrite.py" \
    --trace "$SEAT/fixtures/trace-incident.txt" --allow "$S" \
    --op-home "$OPHOME_FAKE" --scratch "$S"

echo "## 100 green: a real strace of a scratch-only writer (same host, HOME in scratch)"
run "check100 green trace" python3 -I "$SEAT/check100-hostwrite.py" \
    --trace "$SEAT/fixtures/trace-scratch-writer.txt" --allow "$S" \
    --op-home "$OPHOME_FAKE" --scratch "$S"

echo "## 100 red: operator state changed (N2's digest pair)"
run "check100 red receipts" python3 -I "$SEAT/check100-hostwrite.py" \
    --before "$SEAT/fixtures/opstate-before.txt" --after "$SEAT/fixtures/opstate-after.txt" \
    --op-home "$OPHOME_FAKE"

echo "## 100 green: operator state unchanged"
run "check100 green receipts" python3 -I "$SEAT/check100-hostwrite.py" \
    --before "$SEAT/fixtures/opstate-before.txt" --after "$SEAT/fixtures/opstate-same.txt" \
    --op-home "$OPHOME_FAKE"

echo "## 100 red: source screen over the round-48 w2 mutant builder"
run "check100 red scan" python3 -I "$SEAT/check100-hostwrite.py" \
    --scan .ufo/waves/round-48/w2/MutC1ReadOnly

echo "## 101 red: round-48 live receipt, automated (N2)"
run "check101 red" python3 -I "$SEAT/check101-fieldname.py" \
    --payload 'r48-w2
' .ufo/waves/round-48/receipts/live-terminal-cache-r48.txt

echo "## 101 green: the same measurement with a name that states it and a before pair"
run "check101 green" python3 -I "$SEAT/check101-fieldname.py" \
    "$SEAT/fixtures/receipt-fixed-field.txt"

echo "## 101 green: a state-asserting field that carries its comparator"
run "check101 green backed" python3 -I "$SEAT/check101-fieldname.py" \
    "$SEAT/fixtures/receipt-backed-state.txt"

echo "## 102 red: round-48 v2 matrix drops two rows its summary holds (N4)"
run "check102 red" python3 -I "$SEAT/check102-textprojection.py" \
    --json .ufo/waves/round-48/receipts/v2/c2v2-revc2counter-summary.json \
    --text .ufo/waves/round-48/receipts/v2/c2v2-revc2counter-matrix.txt

echo "## 102 green: a total projection generated from the same summary"
run "check102 green" python3 -I "$SEAT/check102-textprojection.py" \
    --json .ufo/waves/round-48/receipts/v2/c2v2-revc2counter-summary.json \
    --text "$SEAT/fixtures/matrix-total.txt"

echo "## 103 red: SKILL.md:770 against the gate's own envelope (M48-8)"
run "check103 red" python3 -I "$SEAT/check103-envelope.py" --repo . --rev "$REV" \
    --registry SKILL.md --gate-id mado-session-material \
    --gate quality/check-session-material.py \
    --shape-verdicts .ufo/waves/round-48/w1/SentPrivacy/receipts/class-verdicts.txt

echo "## 103 green: the same gate with a row that states its scope and declares its blind spots"
R=$S/fixture-repo
mkdir -p "$R"
git -C "$R" init -q
[ "$(git -C "$R" rev-parse --show-toplevel)" = "$R" ] || { echo "FIXTURE_TOPLEVEL_MISMATCH"; exit 2; }
mkdir -p "$R/quality"
cp quality/check-session-material.py "$R/quality/"
cat > "$R/SKILL.md" <<'EOF'
| mado-session-material | gate | `python3 -I quality/check-session-material.py --repo . --rev REV --scope ufo` | 0 clean | `--selftest` | rules `R1_CLIENT_DUMP` `R2_PROC_TABLE`; blind-spots=PR-01..PR-19 (shape classes the rules do not read) |
EOF
git -C "$R" -c user.name=fixture -c user.email=fixture@local add -A
git -C "$R" -c user.name=fixture -c user.email=fixture@local commit -q -m "fixture: declared-envelope registry row"
run "check103 green" python3 -I "$SEAT/check103-envelope.py" --repo "$R" --rev HEAD \
    --registry SKILL.md --gate-id mado-session-material \
    --gate quality/check-session-material.py \
    --shape-verdicts .ufo/waves/round-48/w1/SentPrivacy/receipts/class-verdicts.txt

echo "## 104 red: the a4r1 cap (1 MiB) against this tree and a clone recipe (M48-13)"
run "check104 red" python3 -I "$SEAT/check104-caprecipe.py" --repo . --rev "$REV" \
    --cap-bytes 1048576 --recipe clone --probe "$SEAT/fixtures/probe-fail.txt"

echo "## 104 green: a cap above every tracked blob, with a probe receipt"
run "check104 green" python3 -I "$SEAT/check104-caprecipe.py" --repo . --rev "$REV" \
    --cap-bytes 8388608 --recipe clone --probe "$SEAT/fixtures/probe-ok.txt"

echo "# end: $(date -Is)"
