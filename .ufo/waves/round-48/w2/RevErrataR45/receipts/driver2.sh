#!/bin/bash
# W2 seat RevErrataR45 (round 48): R4b append proof + negative controls + invalid-wording mutants.
# Index-free re-execution of .ufo/waves/round-48/w1/ExecErrataR45/counter-append-test.sh logic:
# the lane tree has 20996 files, so any worktree checkout/commit writes a >1 MiB index and trips
# the seat bound (ulimit -f 2048 = 1 MiB/file). Instead: bare shared clone (objects via
# alternates), appended states built with hash-object/mktree/commit-tree plumbing, counters run
# rev-addressed on the bare repo, locator verifier runs on a synthesized read-only tree.
# Append-only; the lane is never written.
set -u
ulimit -f 2048 || exit 2

LANE=/home/vgpnk/Projects/shokunin/mado-shokunin
OUT=$LANE/.ufo/waves/round-48/w2/RevErrataR45/receipts
S=/fast/scratch/hyaku/mado-r48/RevErrataR45/own
BLOCK=$LANE/.ufo/waves/round-48/w1/ExecErrataR45/block.md
VERIFY=$LANE/.ufo/waves/round-48/w1/ExecErrataR45/verify-locators.py
C1=$LANE/quality/counters/c2-r45-monitor-entry.py
C2=$LANE/quality/counters/c2-r45-monitor-entry-v2.py
ENTRY=corpus/knowledge/hyprland-monitor-rule-r45.md
R45=4d22eeb66c2835af8aaa3fac6ad838fa616aa663
R48=579f694b45c797a9c39761fdb4f9e0a1b71b3585
FREEZE=3e6c848a0e1bbc9c7058226b86d0faefc5351c9d
CTRL2=$LANE/.ufo/waves/round-47/w2/ExecErrataR45/block-as-drafted.md

trap 'rm -rf -- "$S"' EXIT
mkdir -p "$S" "$OUT" || exit 2
export TMPDIR="$S"

[ -f "$BLOCK" ] && [ -f "$CTRL2" ] || { echo "MISSING block or ctrl2"; exit 2; }

# W1's control-1 transform: the source id put back into E6
CTRL1=$S/control-id-in-E6.md
python3 - "$BLOCK" "$CTRL1" <<'PY' || exit 2
import sys
src, dst = sys.argv[1], sys.argv[2]
text = open(src, encoding="utf-8").read()
old = "(the legacy handler file the entry's source list names)"
assert old in text, "anchor for the control is gone"
open(dst, "w", encoding="utf-8").write(text.replace(old, "(S303)"))
PY

# bare shared clone: refs only, objects via alternates; no worktree, no index
B=$S/bare.git
git clone -q --shared --bare "$LANE" "$B" || exit 2

append_commit() { # $1 base rev, $2 file-to-append; echoes the new commit (plumbing only, no index)
    local base=$1 app=$2
    local ne=$S/newentry.md t1=$S/t1 t2=$S/t2 t3=$S/t3
    local blob ob ok nk oc nc nr orr
    git -C "$B" show "$base:$ENTRY" >"$ne" || return 1
    cat "$app" >>"$ne" || return 1
    blob=$(git -C "$B" hash-object -w "$ne") || return 1
    ob=$(git -C "$B" rev-parse "$base:$ENTRY")
    git -C "$B" ls-tree "$base" corpus/knowledge/ | sed 's|\tcorpus/knowledge/|\t|' >"$t1" || return 1
    sed -i "s/\b$ob\b/$blob/" "$t1"
    nk=$(git -C "$B" mktree <"$t1") || return 1
    git -C "$B" ls-tree "$base" corpus/ | sed 's|\tcorpus/|\t|' >"$t2" || return 1
    ok=$(git -C "$B" rev-parse "$base:corpus/knowledge")
    sed -i "s/\b$ok\b/$nk/" "$t2"
    nc=$(git -C "$B" mktree <"$t2") || return 1
    git -C "$B" ls-tree "$base" >"$t3" || return 1
    oc=$(git -C "$B" rev-parse "$base:corpus")
    sed -i "s/\b$oc\b/$nc/" "$t3"
    nr=$(git -C "$B" mktree <"$t3") || return 1
    orr=$(git -C "$B" rev-parse "$base^{tree}")
    [ "$nr" != "$orr" ] || { echo "ROOT-TREE-UNCHANGED"; return 1; }
    git -C "$B" commit-tree "$nr" -p "$base" -m "w2 RevErrataR45 private append (plumbing, no lane write)" </dev/null
}

run_one() { # $1 counter, $2 rev
    local out rc
    out=$(python3 -I "$1" --repo "$B" --rev "$2")
    rc=$?
    printf '%s\n' "$out" | grep -E '^PRED-C2-r45.*(clauses=|admitted=)'
    echo "  exit=$rc $(basename "$1")"
}
run_both() { # $1 label, $2 rev
    echo
    echo "== $1 =="
    run_one "$C1" "$2"
    run_one "$C2" "$2"
}

echo "# bare clone $B of $LANE (shared alternates; no worktree, no index)"
echo "# landed entry at FREEZE sha256 $(git -C "$B" show "$FREEZE:$ENTRY" | sha256sum | cut -d' ' -f1)"
echo "# block $BLOCK sha256 $(sha256sum "$BLOCK" | cut -d' ' -f1) lines $(wc -l <"$BLOCK")"
echo "# counter v1 $(sha256sum "$C1" | cut -d' ' -f1)"
echo "# counter v2 $(sha256sum "$C2" | cut -d' ' -f1)"
echo "# ulimit -f: $(ulimit -f)"

{
    for REV in "$R45" "$R48" "$FREEZE"; do
        echo
        echo "== rev $REV baseline (no errata) =="
        run_one "$C1" "$REV"
        run_one "$C2" "$REV"
        NEW=$(append_commit "$REV" "$BLOCK") || { echo "APPEND-FAILED at $REV"; exit 2; }
        echo "== rev $REV + block: commit $NEW =="
        echo "   entry lines $(git -C "$B" show "$NEW:$ENTRY" | wc -l) sha256 $(git -C "$B" show "$NEW:$ENTRY" | sha256sum | cut -d' ' -f1)"
        run_one "$C1" "$NEW"
        run_one "$C2" "$NEW"
    done

    control() { # $1 label, $2 file
        local NEW
        NEW=$(append_commit "$FREEZE" "$2") || { echo "APPEND-FAILED $1"; exit 2; }
        run_both "control $1 (expected: both counters TARGET_MISSED)" "$NEW"
    }
    control "S-id put back in E6" "$CTRL1"
    control "round-47 block as drafted" "$CTRL2"
    mk_line() { # $1 name, $2 body line
        printf '\n## Errata probe (%s)\n- %s\n' "$1" "$2" >"$S/mut-$1.md"
        control "mutant $1" "$S/mut-$1.md"
    }
    mk_line census-contradiction "Prose aside repeating the bookkeeping: default_refresh=59 with refresh_tolerance=3, contradicting the census line."
    mk_line badloc-marker "Cross-reference for readers: https://bit.ly/hypr-monitors-probe."
    printf '\n## Errata probe (fence)\n```\nforeign fence body absent from every pinned receipt 0xDEADBEEF\n```\n' >"$S/mut-foreign-fence.md"
    control "mutant foreign-fence (expect v2 clause-b T3 miss; v1 has no fence check by design)" "$S/mut-foreign-fence.md"
} >"$OUT/counter-append-test-w2.txt" 2>&1
RC=$?
cat "$OUT/counter-append-test-w2.txt"
[ "$RC" -eq 0 ] || { echo "PROOF-RC=$RC"; exit "$RC"; }

# locator verifier on synthesized read-only trees (plain files + .git file to the bare clone)
mk_T() { # $1 base rev
    local base=$1 T=$S/verify-tree-$1
    rm -rf "$T"
    mkdir -p "$T/corpus/knowledge" "$T/tools" "$T/.ufo/waves" || return 1
    git -C "$B" show "$base:$ENTRY" >"$T/$ENTRY" || return 1
    cat "$BLOCK" >>"$T/$ENTRY" || return 1
    cp "$LANE/tools/mado-monitors.py" "$T/tools/" || return 1
    cp -r "$LANE/.ufo/waves/round-45" "$T/.ufo/waves/" || return 1
    cp -r "$LANE/.ufo/waves/round-47/w1/ScrErrataR45/pins" "$T/.ufo/waves/round-47-w1-pins" || return 1
    cp -r "$LANE/.ufo/waves/round-47/w2/ExecErrataR45/pins" "$T/.ufo/waves/round-47-w2-pins" || return 1
    mkdir -p "$T/.ufo/waves/round-47/w1/ScrErrataR45" "$T/.ufo/waves/round-47/w2/ExecErrataR45" || return 1
    mv "$T/.ufo/waves/round-47-w1-pins" "$T/.ufo/waves/round-47/w1/ScrErrataR45/pins" || return 1
    mv "$T/.ufo/waves/round-47-w2-pins" "$T/.ufo/waves/round-47/w2/ExecErrataR45/pins" || return 1
    printf 'gitdir: %s\n' "$B" >"$T/.git"
    git -C "$T" show "$base:tools/mado-monitors.py" >/dev/null 2>&1 || true
    echo "$T"
}
for REV in "$R48" "$FREEZE"; do
    T=$(mk_T "$REV") || { echo "T-FAILED $REV"; exit 2; }
    python3 -I "$VERIFY" --repo "$T" --block "$BLOCK" >"$OUT/verify-locators-w2-$REV.txt" 2>&1
    VRC=$?
    echo
    echo "== verify-locators on $REV + block: exit=$VRC fails=$(grep -c '^FAIL' "$OUT/verify-locators-w2-$REV.txt" || true)"
    echo "   locator bullets verified: $(grep -o '^cite E[0-9]' "$OUT/verify-locators-w2-$REV.txt" | sort | uniq -c | tr '\n' ' ')"
    echo "   RESULT line: $(grep '^RESULT' "$OUT/verify-locators-w2-$REV.txt")"
    [ "$VRC" -eq 0 ] || exit "$VRC"
done

echo
echo "DONE-OWN largest files written (bytes path):"
find "$OUT" "$S" -type f -printf '%s %p\n' 2>/dev/null | sort -n | tail -4
