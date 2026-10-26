#!/usr/bin/env bash
# Seat ExecSeparability (round 43 w2): causal separability of C1 and C2 at the data commit.
# Replays the four scored cells from a scratch --shared clone; writes nothing in the lane.
# Deterministic: fixed author/committer dates, so the four scratch commit hashes are stable.
set -u
LANE=/home/vgpnk/Projects/shokunin/mado-shokunin
S=/fast/scratch/hyaku/mado-r43/ExecSeparability
DATA=1959770657f1f8665097c1aed4be6c1cbb07139f
BASE=a35cfdfcdeb3bd42d1a2cd960faf22ceac1bef3f
C1C=$LANE/quality/counters/c1-r42-geometry.py
C2C=$LANE/quality/counters/c2-r43-gkeep-entry-v2.py

mkdir -p "$S" || exit 1
D=$(mktemp -d -p "$S") || exit 1
trap 'rm -rf -- "$S"' EXIT
export TMPDIR="$S"
export GIT_AUTHOR_DATE='2026-10-26T12:00:00 +0000'
export GIT_COMMITTER_DATE='2026-10-26T12:00:00 +0000'
C1R42_TMP="$S/c1tmp"; mkdir -p "$C1R42_TMP"

echo "## clone"
echo "\$ D=\$(mktemp -d -p $S); git clone -q --shared $LANE \$D"
git clone -q --shared "$LANE" "$D" || { echo "CLONE FAILED"; exit 1; }
TOP=$(git -C "$D" rev-parse --show-toplevel) || exit 1
echo "git -C \$D rev-parse --show-toplevel -> $TOP"
[ "$TOP" = "$D" ] || { echo "TOPLEVEL MISMATCH"; exit 1; }
echo "TOPLEVEL_OK"

cmt() { git -C "$D" -c user.name=t -c user.email=t@t.invalid commit -q -m "$1" || exit 1; }

echo
echo "## baseline: both counters at the data commit (control)"
git -C "$D" checkout -q "$DATA"
echo "\$ git -C \$D checkout -q $DATA"
echo "\$ python3 -I quality/counters/c1-r42-geometry.py --repo \$D --rev $DATA"
C1R42_TMP=$C1R42_TMP python3 -I "$C1C" --repo "$D" --rev "$DATA" >/dev/null 2>&1
echo "exit=$? (see final line below)"
C1R42_TMP=$C1R42_TMP python3 -I "$C1C" --repo "$D" --rev "$DATA" 2>&1 | tail -2
echo "\$ python3 -I quality/counters/c2-r43-gkeep-entry-v2.py --repo \$D --rev $DATA"
python3 -I "$C2C" --repo "$D" --rev "$DATA" 2>&1 | tail -2; echo "exit=${PIPESTATUS[0]}"

echo
echo "## (a) delete tools/mado-geometry.py -> C2 v2 must still admit"
git -C "$D" checkout -q -B expA "$DATA"
echo "\$ git -C \$D rm tools/mado-geometry.py && git -C \$D commit -m 'scratch expA'"
git -C "$D" rm -q tools/mado-geometry.py || exit 1
cmt "scratch expA: delete tools/mado-geometry.py"
A=$(git -C "$D" rev-parse HEAD)
echo "expA=$A"
git -C "$D" show --stat --oneline HEAD | head -3
test -e "$D/tools/mado-geometry.py" && echo "WORKTREE_TOOL=present" || echo "WORKTREE_TOOL=absent"
echo "\$ python3 -I quality/counters/c2-r43-gkeep-entry-v2.py --repo \$D --rev $A"
python3 -I "$C2C" --repo "$D" --rev "$A" 2>&1 | tail -2; echo "exit=${PIPESTATUS[0]}"

echo
echo "## (b) revert entry, lesson, SOURCES.md, README.md to base -> C1 must still score 37/37"
git -C "$D" checkout -q -B expB "$DATA"
echo "\$ git -C \$D checkout $BASE -- corpus/SOURCES.md corpus/README.md"
git -C "$D" checkout -q "$BASE" -- corpus/SOURCES.md corpus/README.md || exit 1
echo "\$ git -C \$D rm corpus/knowledge/hyprland-gkeep-geometry-r43.md corpus/lessons/round-43.md"
git -C "$D" rm -q corpus/knowledge/hyprland-gkeep-geometry-r43.md corpus/lessons/round-43.md || exit 1
cmt "scratch expB: revert C2 content surfaces to base"
B=$(git -C "$D" rev-parse HEAD)
echo "expB=$B"
git -C "$D" diff --name-status "$DATA" HEAD
echo "\$ python3 -I quality/counters/c1-r42-geometry.py --repo \$D --rev $B"
C1R42_TMP=$C1R42_TMP python3 -I "$C1C" --repo "$D" --rev "$B" 2>&1 | tail -3; echo "exit=${PIPESTATUS[0]}"

echo
echo "## (c) EXTRA: revert every C2 content surface (corpus/, PROVINCE, SKILL, locator checker, fetch pins)"
git -C "$D" checkout -q -B expC "$DATA"
git -C "$D" rm -r -q corpus || exit 1
git -C "$D" checkout -q "$BASE" -- corpus PROVINCE.md SKILL.md || exit 1
git -C "$D" rm -q quality/check-locators.py || exit 1
git -C "$D" rm -r -q .ufo/waves/round-43/fetch || exit 1
cmt "scratch expC: revert all C2 content surfaces to base"
C=$(git -C "$D" rev-parse HEAD)
echo "expC=$C"
git -C "$D" diff --stat "$DATA" HEAD | tail -2
echo "\$ python3 -I quality/counters/c1-r42-geometry.py --repo \$D --rev $C"
C1R42_TMP=$C1R42_TMP python3 -I "$C1C" --repo "$D" --rev "$C" 2>&1 | tail -3; echo "exit=${PIPESTATUS[0]}"

echo
echo "## (d) EXTRA: delete C1's tool, C1's receipts and the control runners -> C2 must still admit"
git -C "$D" checkout -q -B expD "$DATA"
git -C "$D" rm -q tools/mado-geometry.py || exit 1
git -C "$D" rm -r -q .ufo/waves/round-43/receipts .ufo/waves/round-43/ctl || exit 1
cmt "scratch expD: delete C1 artifacts"
E=$(git -C "$D" rev-parse HEAD)
echo "expD=$E"
git -C "$D" diff --stat "$DATA" HEAD | tail -2
echo "\$ python3 -I quality/counters/c2-r43-gkeep-entry-v2.py --repo \$D --rev $E"
python3 -I "$C2C" --repo "$D" --rev "$E" 2>&1 | tail -2; echo "exit=${PIPESTATUS[0]}"

echo
echo "## (e) EXTRA: rev-addressing control - worktree has NO tool, rev $DATA does"
git -C "$D" checkout -q expA
test -e "$D/tools/mado-geometry.py" && echo "WORKTREE_TOOL=present" || echo "WORKTREE_TOOL=absent"
echo "\$ python3 -I quality/counters/c1-r42-geometry.py --repo \$D --rev $DATA"
C1R42_TMP=$C1R42_TMP python3 -I "$C1C" --repo "$D" --rev "$DATA" 2>&1 | tail -2; echo "exit=${PIPESTATUS[0]}"

echo
echo "## static dependency map (what each counter can read from the repo)"
echo "c1 counter repo reads:"; grep -n 'git(repo, "show"' "$C1C"
echo "c1 TOOL constant:"; grep -n '^TOOL = ' "$C1C"
echo "c2 counter repo reads:"; grep -n 'show(repo' "$C2C"
echo "c2 path constants:"; grep -nE '^(ENTRIES|LESSON|FETCH) =' "$C2C"
echo "c2 child processes:"; grep -n 'subprocess\.' "$C2C"
echo "c2 mentions of tools/ or mado-geometry:"; grep -c 'tools/\|mado-geometry' "$C2C"
echo "c1 mentions of corpus/ or lessons or README:"; grep -c 'corpus/\|lessons/\|README' "$C1C"
echo
echo "## quoted-fragment verification (revision-addressed; 1 = the fragment occurs in that file at that rev)"
q() { printf '%s %s:%s :: ' "$1" "$2" "$3"; git -C "$D" show "$2:$3" | grep -cF -- "$4"; }
REG=$LANE/.ufo/waves/round-43/registration.md
REGV2=$LANE/.ufo/waves/round-43/registration-v2.md
q QUOTE b2e2efd6e268920d31f3c32cf52dc097dd6e1d22 .ufo/waves/round-43/registration.md 'C1 touches `tools/mado-geometry.py` only (plus receipts).'
q QUOTE b2e2efd6e268920d31f3c32cf52dc097dd6e1d22 .ufo/waves/round-43/registration.md "so C2 never runs C1's tool and C1 reads no C2 file."
q QUOTE 496340dd53fabd800be42e8fb19090f35e2c235c .ufo/waves/round-43/registration-v2.md 'C1 touches `tools/mado-geometry.py` only; C2 the entry, rows S290-S299, the lesson `## Gate` and the README index.'
q QUOTE 496340dd53fabd800be42e8fb19090f35e2c235c .ufo/waves/round-43/registration-v2.md 'index. v2 reads'
q QUOTE "$DATA" PROVINCE.md 'the bytes of one or more caller-supplied Hyprland config files'
q QUOTE "$DATA" SKILL.md '### Rule size versus reported size'
q QUOTE "$DATA" corpus/README.md 'instrumented by the read-only join'
q QUOTE "$DATA" corpus/lessons/round-43.md 'C1 lands `tools/mado-geometry.py`'
echo "-- c1 counter, the one 'ctl-ref' occurrence (docstring only, no open call):"
grep -n 'ctl-ref' "$C1C"

echo
echo "## tool identity at the data commit vs the round-42 reference"
git -C "$D" cat-file -p "$DATA:tools/mado-geometry.py" | sha256sum
sha256sum "$LANE/.ufo/waves/round-42/c1/ctl-ref-tool.py.txt"
echo "DONE"
