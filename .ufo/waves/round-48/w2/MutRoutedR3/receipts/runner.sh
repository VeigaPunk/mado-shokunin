#!/bin/sh
# MutRoutedR3 runner — commit staged mutation, run gate (mutated), restore exact
# bytes from HEAD~1, run gate (restored). Records hashes around the mutation.
# usage: runner.sh <TAG> "<mut-commit-msg>" PREDELETE|ADD <path>...
set -u
S=/fast/scratch/hyaku/mado-r48/MutRoutedR3
CLONE=$S/clone
OUT=$S/out
ID="-c user.name=MutRoutedR3 -c user.email=mutroutedr3@scratch.invalid"
ulimit -Sf 2048
export TMPDIR=$S/tmp
exec >> "$OUT/log2.txt" 2>&1

# gitx: lift the SOFT file-size limit only for git's internal index writes.
gitx() { sh -c 'ulimit -Sf unlimited; exec git "$@"' git "$@"; }

tag=$1; msg=$2; mode=$3; shift 3
echo "=== $tag start"

: > "$S/mut-$tag.paths"
for p in "$@"; do printf '%s\n' "$p" >> "$S/mut-$tag.paths"; done
for p in "$@"; do sha256sum "$CLONE/$p" 2>&1; done > "$S/mut-$tag.before" || true

case $mode in
    PREDELETE) gitx -C "$CLONE" rm -q -- "$@" ;;
    *)         gitx -C "$CLONE" add -- "$@" ;;
esac
TL=$(git -C "$CLONE" rev-parse --show-toplevel)
[ "$TL" = "$CLONE" ] || { echo "TOPLEVEL GUARD FAILED: $TL" >&2; exit 9; }
gitx -C "$CLONE" $ID commit -qm "$msg"
mut=$(git -C "$CLONE" rev-parse HEAD)
echo "$tag mutated-commit=$mut" >> "$OUT/commits.txt"
echo "$tag mutated-commit=$mut"
for p in "$@"; do sha256sum "$CLONE/$p" 2>&1; done > "$S/mut-$tag.during" ||
    echo "(path absent in worktree)" >> "$S/mut-$tag.during"

gate_run() { # gate_run <name>
    start=$(date +%s)
    python3 -I "$CLONE/quality/check-session-material.py" --repo "$CLONE" --rev HEAD \
        > "$OUT/D-$1.txt" 2>&1
    rc=$?
    printf '%s rc=%d elapsed=%ss\n' "$1" "$rc" "$(( $(date +%s) - start ))" >> "$OUT/rcs.txt"
    printf '%s rc=%d %ss\n' "$1" "$rc" "$(( $(date +%s) - start ))"
    grep -E '^(SESSION_MATERIAL|WAIVER |WAIVER_REJECTED .*(C00_shipped|ExecSessionMarker/check))' \
        "$OUT/D-$1.txt" | tail -8
}
gate_run "$tag"

gitx -C "$CLONE" checkout HEAD~1 -- "$@"
gitx -C "$CLONE" $ID commit -qm "restore exact bytes after $tag"
echo "$tag restored-commit=$(git -C "$CLONE" rev-parse HEAD)" >> "$OUT/commits.txt"
for p in "$@"; do sha256sum "$CLONE/$p" 2>&1; done > "$S/mut-$tag.after"
echo "$tag before/after hashes:"; cat "$S/mut-$tag.before"; cat "$S/mut-$tag.after"
gate_run "$tag-r"

echo "=== $tag done"
