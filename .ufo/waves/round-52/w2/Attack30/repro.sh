#!/usr/bin/env bash
# Attack30 (W2) reproduction: C2 counter no-work control at the frozen base.
# Read-only against the lane; every git mutation happens inside $SCRATCH/clone.
set -u
ROOT=/home/vgpnk/Projects/shokunin/mado-shokunin
SEAT=$ROOT/.ufo/waves/round-52/w2/Attack30
SCRATCH=/fast/scratch/hyaku/mado-r52/Attack30
BASE=85d57a818c3707397e21c840b6498b105ba798aa
DRF=$ROOT/.ufo/waves/round-52/w1/C2CounterDraft/c2-r52-proposition-entry.py
INT=$ROOT/quality/counters/c2-r52-proposition-entry.py
ENTRY_KEY=corpus/knowledge/hyprland-synthetic-key-dispatch-r52.md
ENTRY_REAL=corpus/knowledge/hyprland-synthetic-dispatch-r52.md
R=$SEAT/receipts.txt

mkdir -p "$SEAT" "$SCRATCH"
rm -rf "$SCRATCH/clone"
git clone -q --no-hardlinks "$ROOT" "$SCRATCH/clone" || exit 1
cd "$SCRATCH/clone" || exit 1
assert_clone() {
  local t
  t=$(git rev-parse --show-toplevel)
  echo "assert_toplevel=$t"
  [ "$t" = "$SCRATCH/clone" ] || { echo "ASSERT_FAIL expected=$SCRATCH/clone got=$t"; exit 1; }
}

{
echo "# Attack30 receipts — C2 counter no-work control at base"
echo "utc=$(date -u +%Y-%m-%dT%H:%M:%SZ)"
echo "root=$ROOT"
echo "base=$BASE"
echo "clone_toplevel=$(git rev-parse --show-toplevel)"
echo "clone_head=$(git rev-parse HEAD)"
echo "draft_sha256=$(sha256sum "$DRF" | cut -d' ' -f1)"
echo "integrated_sha256=$(sha256sum "$INT" | cut -d' ' -f1)"
echo "draft_lines=$(wc -l < "$DRF")"
echo "integrated_lines=$(wc -l < "$INT")"
echo

echo "== P0 base absence proof =="
git cat-file -e "$BASE:$ENTRY_KEY" 2>/dev/null && echo "base:$ENTRY_KEY=PRESENT" || echo "base:$ENTRY_KEY=ABSENT"
git cat-file -e "$BASE:$ENTRY_REAL" 2>/dev/null && echo "base:$ENTRY_REAL=PRESENT" || echo "base:$ENTRY_REAL=ABSENT"
echo "base_S370_S373_rows=$(git show "$BASE:corpus/SOURCES.md" | grep -c '^| S37[0-3]')"
echo "base_registry_rows_total=$(git show "$BASE:corpus/SOURCES.md" | grep -c '^| S[0-9]')"
echo "base_index_rows=$(git show "$BASE:corpus/README.md" | grep -c 'hyprland-synthetic')"
echo

run() { # run <label> <cmd...>
  local label=$1; shift
  echo "-- $label"
  echo "\$ $*"
  "$@"
  echo "exit=$?"
  echo
}

echo "== P1 W1 draft counter at base =="
mkdir -p "$SCRATCH/w-draft-key"
TMPDIR="$SCRATCH/w-draft-key" run draft-base-key \
  python3 -I "$DRF" --repo . --rev "$BASE" --work "$SCRATCH/w-draft-key"
mkdir -p "$SCRATCH/w-draft-real"
TMPDIR="$SCRATCH/w-draft-real" run draft-base-real \
  python3 -I "$DRF" --repo . --rev "$BASE" --entry "$ENTRY_REAL" --work "$SCRATCH/w-draft-real"

echo "== P2 integrated counter at base =="
run int-base-key python3 -I "$INT" --repo . --rev "$BASE" --work "$SCRATCH/w-int-key"
run int-base-real python3 -I "$INT" --repo . --rev "$BASE" --entry "$ENTRY_REAL" --work "$SCRATCH/w-int-real"

echo "== P3 base with the claimed entry present in the working tree (lane in place, untracked) =="
run int-lane-base-real python3 -I "$INT" --repo "$ROOT" --rev "$BASE" --entry "$ENTRY_REAL" --work "$SCRATCH/w-lane"

echo "== P4 work-present revision, staged in scratch clone (no lane writes) =="
cp "$ROOT/corpus/README.md" corpus/README.md
cp "$ROOT/corpus/SOURCES.md" corpus/SOURCES.md
cp "$ROOT/$ENTRY_REAL" corpus/knowledge/
assert_clone
git add -A
git -c user.email=a@b -c user.name=attack30 commit -q -m "scratch: landed r52 entry + rows (Attack30)"
NEW=$(git rev-parse HEAD)
mkdir -p .ufo/waves/round-52
cp -a "$ROOT/.ufo/waves/round-52/fetch" .ufo/waves/round-52/
assert_clone
git add -A
git -c user.email=a@b -c user.name=attack30 commit -q -m "scratch: r52 fetch pins (Attack30)"
NEW2=$(git rev-parse HEAD)
echo "staged_work_rev=$NEW2 (entry+README+SOURCES=$NEW)"
echo "staged_toplevel=$(git rev-parse --show-toplevel)"
echo "staged_entry_present=$(git cat-file -e "$NEW2:$ENTRY_REAL" 2>/dev/null && echo yes || echo no)"
run int-work-real python3 -I "$INT" --repo . --rev "$NEW2" --entry "$ENTRY_REAL" --work "$SCRATCH/w-work-int-real"
run int-work-default python3 -I "$INT" --repo . --rev "$NEW2" --work "$SCRATCH/w-work-int-default"
mkdir -p "$SCRATCH/w-work-draft"
TMPDIR="$SCRATCH/w-work-draft" run draft-work-real \
  python3 -I "$DRF" --repo . --rev "$NEW2" --entry "$ENTRY_REAL" --fetch-root .ufo/waves/round-52 --work "$SCRATCH/w-work-draft"

echo "== P5 absence-detection specificity: present base file, path variants =="
for E in "$ENTRY_REAL/" ":corpus/knowledge/hyprland-dispatcher-dispatch-r51.md" \
         "corpus/knowledge/../knowledge/hyprland-dispatcher-dispatch-r51.md"; do
  run "int-work-present-path[$E]" python3 -I "$INT" --repo . --rev "$NEW2" --entry "$E" --work "$SCRATCH/w-path"
done
run int-base-present-canonical python3 -I "$INT" --repo . --rev "$BASE" \
  --entry corpus/knowledge/hyprland-dispatcher-dispatch-r51.md --work "$SCRATCH/w-path2"

echo "== P6 environment hermeticity =="
run int-gitdir env GIT_DIR=/nonexistent python3 -I "$INT" --repo . --rev "$BASE" --work "$SCRATCH/w-gitdir"
mkdir -p "$SCRATCH/w-gitdir-draft"
run draft-gitdir env GIT_DIR=/nonexistent TMPDIR="$SCRATCH/w-gitdir-draft" \
  python3 -I "$DRF" --repo . --rev "$BASE" --work "$SCRATCH/w-gitdir-draft"

echo "== P7 --work side effects of the integrated counter =="
for d in "$SCRATCH"/w-int-key "$SCRATCH"/w-int-real "$SCRATCH"/w-work-int-real "$SCRATCH"/w-gitdir; do
  if [ -e "$d" ]; then echo "exists=$d"; else echo "absent=$d"; fi
done
echo
} >"$R" 2>&1
echo "wrote $R"
