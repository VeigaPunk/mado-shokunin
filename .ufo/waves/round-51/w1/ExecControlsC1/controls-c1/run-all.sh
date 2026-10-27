#!/usr/bin/env bash
# Re-run every C1 control receipt from scratch (seat ExecControlsC1, mado round 51 w1).
# Usage: run-all.sh <scratch> <seat-dir> <lane>
set -u
S=${1:?scratch dir}
SEAT=${2:?seat dir}
LANE=${3:?lane repo}
OUT=$SEAT/controls-c1/actual-run
CK=$S/check-tool-ledger.py
WORK=$S/work
mkdir -p "$OUT"
cd "$S" || exit 2

run_tag() {  # name rev
  local name=$1 rev=$2 out rc
  out=$(python3 -I "$CK" --repo "$S/fixture" --rev "$rev" --work "$WORK" 2>&1); rc=$?
  { echo "# command: python3 -I check-tool-ledger.py --repo $S/fixture --rev $rev --work $WORK";
    printf '%s\nexit=%s\n' "$out" "$rc"; } > "$OUT/$name.txt"
}

run_tag green r51-control
run_tag ctl-a mut-a
run_tag ctl-b mut-b
run_tag ctl-c mut-c
run_tag ctl-d mut-d

for pair in "green:aef0acf4ea4be1598771a210b8d41771517ff4be" \
            "ctl-a:c02eeab908ae9da8d2413ef6dfbbfe81a089467a" \
            "ctl-b:a03b9fdcf63122cb3cf35fa1870b77fcb45e6f4b" \
            "ctl-c:70d323611187101f67a5c5afa08f34bbbb382899" \
            "ctl-d:f6bbf864f4ec034a5fe2c009548a625ceb695a3d"; do
  name=${pair%%:*}; rev=${pair#*:}
  out=$(python3 -I "$CK" --repo "$S/fixture" --rev "$rev" --work "$WORK" 2>&1); rc=$?
  { echo "# full-hash replay of $name";
    echo "# command: python3 -I check-tool-ledger.py --repo $S/fixture --rev $rev --work $WORK";
    printf '%s\nexit=%s\n' "$out" "$rc"; } > "$OUT/hash-$name.txt"
done

out=$(python3 -I "$CK" --repo "$LANE" --rev 6ca8c559a4a3d6d361101592116eea2bc7452437 --work "$WORK" 2>&1); rc=$?
{ echo "# command: python3 -I check-tool-ledger.py --repo $LANE --rev 6ca8c55... --work $WORK";
  printf '%s\nexit=%s\n' "$out" "$rc"; } > "$OUT/ctl-e-lane-base.txt"

out=$(python3 -I "$CK" --repo "$S/fixture" --rev e5943b7032fd9b73d02f7e9a71efa6848cec22a8 --work "$WORK" 2>&1); rc=$?
{ echo "# command: python3 -I check-tool-ledger.py --repo $S/fixture --rev e5943b70... --work $WORK";
  printf '%s\nexit=%s\n' "$out" "$rc"; } > "$OUT/fixture-base-absent.txt"

python3 -I "$CK" --work "$WORK" --selftest > "$OUT/selftest.txt" 2>&1
echo "exit=$?" >> "$OUT/selftest.txt"

{ echo "# revision scoping: worktree ledger is the green one; requested rev is mut-a"
  echo "\$ git -C fixture rev-parse --abbrev-ref HEAD"; git -C "$S/fixture" rev-parse --abbrev-ref HEAD
  echo "\$ git -C fixture hash-object quality/tool-ledger.md"; git -C "$S/fixture" hash-object quality/tool-ledger.md
  echo "\$ git -C fixture rev-parse mut-a:quality/tool-ledger.md"; git -C "$S/fixture" rev-parse mut-a:quality/tool-ledger.md
  echo "\$ python3 -I check-tool-ledger.py --repo fixture --rev mut-a --work $WORK"
  python3 -I "$CK" --repo "$S/fixture" --rev mut-a --work "$WORK"; echo "exit=$?"; } \
  > "$OUT/rev-scope-worktree-green-rev-mut-a.txt" 2>&1

{ echo "\$ git -C fixture rev-parse --show-toplevel"; git -C "$S/fixture" rev-parse --show-toplevel
  echo "fixture=$S/fixture"
  echo "\$ git -C fixture log --oneline --all --decorate"; git -C "$S/fixture" log --oneline --all --decorate; } \
  > "$OUT/fixture-toplevel-and-log.txt" 2>&1

{ for rev in e5943b7032fd9b73d02f7e9a71efa6848cec22a8 aef0acf4ea4be1598771a210b8d41771517ff4be \
           c02eeab908ae9da8d2413ef6dfbbfe81a089467a a03b9fdcf63122cb3cf35fa1870b77fcb45e6f4b \
           70d323611187101f67a5c5afa08f34bbbb382899 f6bbf864f4ec034a5fe2c009548a625ceb695a3d; do
    printf '%s %s\n' "$rev" "$(git -C "$S/fixture" ls-tree -r --name-only "$rev" | \
      grep -cE '^(tools/|quality/[^/]*\.py$|quality/counters/[^/]*\.py$)')"
  done
  echo "# lane base"
  git -C "$LANE" ls-tree -r --name-only 6ca8c559a4a3d6d361101592116eea2bc7452437 | \
    grep -cE '^(tools/|quality/[^/]*\.py$|quality/counters/[^/]*\.py$)'; } > "$OUT/population-per-rev.txt"

{ echo "\$ python3 -I check-tool-ledger.py --repo fixture --rev r51-control --work /tmp/ctl-r51"
  python3 -I "$CK" --repo "$S/fixture" --rev r51-control --work /tmp/ctl-r51; echo "exit=$?"; echo
  echo "\$ TMPDIR=$WORK python3 -I check-tool-ledger.py --repo fixture --rev r51-control"
  TMPDIR=$WORK python3 -I "$CK" --repo "$S/fixture" --rev r51-control; echo "exit=$?"; echo
  echo "\$ python3 -I check-tool-ledger.py --repo fixture --rev green --work $WORK"
  python3 -I "$CK" --repo "$S/fixture" --rev green --work "$WORK"; echo "exit=$?"; echo
  echo "\$ python3 -I check-tool-ledger.py --repo fixture --rev r51-control --work \$HOME/ctl-r51"
  python3 -I "$CK" --repo "$S/fixture" --rev r51-control --work "$HOME/ctl-r51"; echo "exit=$?"; } \
  > "$OUT/work-guard.txt" 2>&1

python3 -I "$S/verify-controls.py" > "$OUT/compare.txt" 2>&1
echo "exit=$?" >> "$OUT/compare.txt"
cat "$OUT/compare.txt"
sha256sum "$CK" "$S/make-fixture.py" "$S/verify-controls.py" > "$OUT/instrument-hashes.txt"
cat "$OUT/instrument-hashes.txt"
