#!/bin/bash
# Attack05 — C1 TMPDIR/workdir boundary probes.
# Everything writes under $S only. Fixture repo is a shared --no-checkout clone
# of the lane, checked out to the frozen base; assertions precede mutations.
set -u
S=/fast/scratch/hyaku/mado-r52/Attack05
LANE=/home/vgpnk/Projects/shokunin/mado-shokunin
BASE=85d57a818c3707397e21c840b6498b105ba798aa
COUNTER=$LANE/.ufo/waves/round-52/w1/C1CounterDesign/c1-r52-ledger.py
FIX=$S/fix/repo
say() { printf '\n===== %s =====\n' "$*"; }

say "build fixture (shared clone, checked out to base)"
rm -rf "$S/fix"
mkdir -p "$S/fix"
git clone -q --shared --no-checkout "$LANE" "$FIX" 2>&1
top=$(git -C "$FIX" rev-parse --show-toplevel)
echo "fixture toplevel: $top"
[ "$top" = "$FIX" ] || { echo "TOPLEVEL ASSERT FAILED"; exit 1; }
git -C "$FIX" checkout -q "$BASE" 2>&1
git -C "$FIX" rev-parse HEAD
git -C "$FIX" rev-parse --show-toplevel

say "P1a: measurement mode, --work INSIDE the fixture repo (nonexistent dir)"
echo "before: $(test -e "$FIX/sideeffect-dir" && echo exists || echo absent)"
python3 -I "$COUNTER" --repo "$FIX" --rev "$BASE" --work "$FIX/sideeffect-dir"
echo "exit=$?"
echo "after: $(test -d "$FIX/sideeffect-dir" && echo DIR-CREATED || echo absent)"
echo "ls-files --others (empty dirs are invisible to git):"
git -C "$FIX" ls-files --others --exclude-standard | grep -c sideeffect || true
echo "git status --porcelain matching sideeffect:"
git -C "$FIX" status --porcelain | grep -c sideeffect || true
find "$FIX/sideeffect-dir" | head

say "P1b: empty-dir invisibility is git-inherent (status --porcelain=v2 -uall)"
git -C "$FIX" status --porcelain=v2 --untracked-files=all | grep -c sideeffect || true
echo "(0 = the created dir leaves no trace in any git status view)"

say "P2a: --work dir created even though --repo is bogus (create-before-validate)"
rm -rf "$S/p2" && mkdir -p "$S/p2"
python3 -I "$COUNTER" --repo /nonexistent --rev "$BASE" --work "$S/p2/early-created"
echo "exit=$?"
test -d "$S/p2/early-created" && echo "CREATED despite exit 2" || echo absent

say "P2b: --work dir created even though --rev is bogus"
python3 -I "$COUNTER" --repo "$FIX" --rev deadbeefdeadbeefdeadbeefdeadbeefdeadbeef --work "$S/p2/early-created-2"
echo "exit=$?"
test -d "$S/p2/early-created-2" && echo "CREATED despite exit 2" || echo absent

say "P2c: --work dir created even though --ledger file is missing"
python3 -I "$COUNTER" --repo "$FIX" --rev "$BASE" --work "$S/p2/early-created-3" --ledger /nonexistent-ledger.md
echo "exit=$?"
test -d "$S/p2/early-created-3" && echo "CREATED despite exit 2" || echo absent

say "P3a: measurement with NEITHER --work NOR TMPDIR -> exit 2 (documented usage line omits --work)"
mkdir -p "$S/p3"
env -u TMPDIR python3 -I "$COUNTER" --repo "$FIX" --rev "$BASE"
echo "exit=$?"

say "P3b: ambient TMPDIR (nonexistent path) steers the work root AND is created"
env -u XDG_CACHE_HOME TMPDIR="$S/p3/steered-by-env" python3 -I "$COUNTER" --repo "$FIX" --rev "$BASE" | tail -1
test -d "$S/p3/steered-by-env" && echo "TMPDIR-CREATED (env var caused a host write)" || echo absent

say "P3c: TMPDIR=/tmp, no --work -> hard refusal"
TMPDIR=/tmp python3 -I "$COUNTER" --repo "$FIX" --rev "$BASE"
echo "exit=$?"

say "P4a: relative --work floats with process cwd"
mkdir -p "$S/p4" && cd "$S/p4"
python3 -I "$COUNTER" --repo "$FIX" --rev "$BASE" --work relwork | tail -1
test -d "$S/p4/relwork" && echo "created under cwd: $S/p4/relwork" || echo absent

say "P4b: relative TMPDIR also floats with cwd"
cd "$S/p4" && TMPDIR=rel-tmp python3 -I "$COUNTER" --repo "$FIX" --rev "$BASE" | tail -1
test -d "$S/p4/rel-tmp" && echo "created under cwd: $S/p4/rel-tmp" || echo absent

say "P5a: --selftest --work INSIDE the fixture repo -> nested repo created inside its worktree"
python3 -I "$COUNTER" --selftest --work "$FIX/st-nest"
echo "exit=$?"
echo "residue under fixture worktree after normal exit:"
test -d "$FIX/st-nest" && echo "st-nest/ REMAINS (empty dir, git-invisible)" || echo "st-nest removed"
git -C "$FIX" ls-files --others --exclude-standard | grep -c st-nest || true
git -C "$FIX" status --porcelain | grep -c st-nest || true

say "P5b: nested selftest residue after SIGKILL (crash path, ignore_errors=rmtree)"
mkdir -p "$S/p5"
for i in 1 2 3 4 5 6; do
  rm -rf "$S/p5/kill$i"
  python3 -I "$COUNTER" --selftest --work "$S/p5/kill$i" >/dev/null 2>&1 &
  pid=$!
  sleep 0.0$i
  kill -9 $pid 2>/dev/null
  wait $pid 2>/dev/null
  if find "$S/p5/kill$i" -mindepth 1 | grep -q .; then
    echo "attempt $i: RESIDUE:"; find "$S/p5/kill$i" -mindepth 1 | head -20
    break
  else
    echo "attempt $i: clean (kill landed before/after fixture window)"
  fi
done

say "P5c: nested-newdir chain inside repo left behind by selftest"
python3 -I "$COUNTER" --selftest --work "$FIX/a/b/c" | tail -1
test -d "$FIX/a/b/c" && echo "a/b/c REMAINS (3-level litter)" || echo absent
git -C "$FIX" status --porcelain | grep -c '^?? a/' || true

say "P6a: TMPDIR env leak test — counter --work given, TMPDIR set elsewhere; selftest child git procs"
mkdir -p "$S/p6/leak" "$S/p6/work"
TMPDIR="$S/p6/leak" python3 -I "$COUNTER" --selftest --work "$S/p6/work" | tail -1
echo "TMPDIR contents after run: $(find "$S/p6/leak" -mindepth 1 | wc -l) entries"
find "$S/p6/leak" -mindepth 1 | head

say "P6b: GIT_* env poisoning is stripped (GIT_DIR=/nonexistent must not break it)"
GIT_DIR=/nonexistent GIT_WORK_TREE=/nonexistent python3 -I "$COUNTER" --repo "$FIX" --rev "$BASE" --work "$S/p6/work" | tail -1
echo "exit=$?"

say "P7: refusal surface — /tmp, symlink to /tmp, and harness-accepted /tmp/foo"
python3 -I "$COUNTER" --repo "$FIX" --rev "$BASE" --work /tmp 2>&1 | tail -1; echo "exit=$?"
ln -sfn /tmp "$S/p7-tmplink"
python3 -I "$COUNTER" --repo "$FIX" --rev "$BASE" --work "$S/p7-tmplink" 2>&1 | tail -1; echo "exit=$?"
python3 -I "$COUNTER" --repo "$FIX" --rev "$BASE" --work /tmp/undertmp 2>&1 | tail -1; echo "exit=$?"
echo "note: harness line 511 refuses only exact /tmp|/var/tmp|/dev/shm, so it would PASS /tmp/undertmp through; counter then exits 2"

say "P8: --work naming an existing FILE -> refused (no mutation)"
python3 -I "$COUNTER" --repo "$FIX" --rev "$BASE" --work "$FIX/SCORECARD.md" 2>&1 | tail -1
echo "exit=$?"

say "P9: r51 parity — r51 counter with TMPDIR set and NO --work auto-creates+auto-removes"
R51=/home/vgpnk/Projects/shokunin/mado-shokunin/quality/counters/c1-r51-ledger.py
mkdir -p "$S/p9/tmp"
TMPDIR="$S/p9/tmp" python3 -I "$R51" --repo "$FIX" --rev "$BASE" 2>&1 | tail -3
echo "exit=$?"
echo "TMPDIR contents after r51 run: $(find "$S/p9/tmp" -mindepth 1 | wc -l) entries"

say "fixture integrity: HEAD + toplevel + lane object count sanity"
git -C "$FIX" rev-parse HEAD
git -C "$FIX" rev-parse --show-toplevel
git -C "$FIX" status --porcelain | head -20
echo "untracked visible paths (files only):"
git -C "$FIX" ls-files --others --exclude-standard | grep -v '^\.ufo/waves/round-52' | head
echo "dirs I created inside the fixture worktree (git-invisible litter):"
find "$FIX" -type d -name 'sideeffect-dir' -o -type d -name 'st-nest' -o -type d -path '*/a/b/c' | grep -v '\.git' || true
