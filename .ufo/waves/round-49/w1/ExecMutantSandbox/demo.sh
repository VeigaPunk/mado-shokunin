#!/bin/sh
# ExecMutantSandbox — M48-10 demonstration driver, round 49 w1.
#
# Shows hostguard.py against a FAKE operator home only. The real home is never a target:
#  A  unsandboxed mutant, HOME=<fake home>: the guard must exit 3 (caught);
#  A2 the same mutant with the original size and mtime restored: only sha256 can see it, exit 3;
#  B  the same mutant with <fake home> masked by an empty tmpfs: the write SUCCEEDS inside and the guard
#     exits 0, because the bytes are in the tmpfs and nowhere on disk (contained, not merely failed);
#  B2 --ro-root: the write fails EROFS and the guard exits 0, TMPDIR under --work still writable;
#  C  negative control, child `true`: exit 0;
#  C2 a child that legitimately writes inside its scratch XDG root: exit 0 and the file exists;
#  E  the refusals (a /tmp work dir, an in-repo work dir, a directory/FIFO declared, a mask over --work,
#     no declaration, a child that exits 3 with nothing changed, a child past --timeout);
#  G  --json and --declare-file, the surface a counter consumes;
#  F  exactly what the guard left in its scratch;
#  D  ONE read-only digest of the operator's real cache (stat + sha256, never a guard run against it).
#
# Every writer runs under ulimit -f 65536 (64 MiB/file); scratch is /fast/scratch/hyaku/mado-r49/<seat>/ and is
# removed on exit after the receipts are copied into this seat directory.
set -u
ulimit -f 65536

HERE=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
LANE=$(CDPATH= cd -- "$HERE/../../../../.." && pwd)
S=/fast/scratch/hyaku/mado-r49/ExecMutantSandbox
R="$HERE/receipts"
HOSTGUARD="$HERE/hostguard.py"
FH="$S/fakehome"                      # the fake operator home: the ONLY home any mutant here sees
CACHE="$FH/.cache/xdg-terminal-exec"
WORK="$S/work"
REPO="$S/fakerepo"                    # a throwaway repo, to exercise the in-repo refusal without touching the lane

rm -rf -- "$S"
mkdir -p "$R" "$S" "$FH/.cache" "$WORK"
trap 'rm -rf -- "$S"' EXIT INT TERM
EXITS="$R/00-case-exits.txt"
: > "$EXITS"
say() { echo "$1"; echo "$1" >> "$EXITS"; }

# ---- fixture: a plausible 331-byte resolver cache, mtime pinned to the round-47/48 recorded value -------------
make_cache() {
    python3 - "$CACHE" <<'PY'
import sys
body = b"FAKE-OPERATOR-HOME r49-w1 ORIGINAL CONTENT\n" + b"# fake cache line\n" * 16
open(sys.argv[1], "wb").write(body)
PY
    touch -d @1793047345 "$CACHE"
}
make_cache

# ---- the mutant that is M48-10's shape: write $HOME/.cache/xdg-terminal-exec, no sandbox of its own ----------
cat > "$S/mutant.py" <<'PY'
import hashlib, os, sys
payload = os.environ.get("MUTANT_PAYLOAD", "r49-w1-mutant\n")
target = os.path.join(os.environ["HOME"], ".cache", "xdg-terminal-exec")
os.makedirs(os.path.dirname(target), exist_ok=True)
before = open(target, "rb").read() if os.path.exists(target) else b""
with open(target, "w") as fh:
    fh.write(payload)
after = open(target, "rb").read()
print("MUTANT home=%s target=%s in_size=%d out_size=%d out_sha256=%s"
      % (os.environ["HOME"], target, len(before), len(after), hashlib.sha256(after).hexdigest()))
if os.environ.get("MUTANT_RESTORE_MTIME"):
    st = os.stat(target)
    os.utime(target, ns=(st.st_atime_ns, int(os.environ["MUTANT_RESTORE_MTIME"])))
    print("MUTANT restored mtime_ns=%s size=%d" % (os.environ["MUTANT_RESTORE_MTIME"], os.path.getsize(target)))
PY

ORIG_SHA=$(sha256sum "$CACHE" | cut -d' ' -f1)
ORIG_SIZE=$(stat -c %s "$CACHE")
ORIG_MTIME_NS=$(python3 -c 'import os,sys; print(os.stat(sys.argv[1]).st_mtime_ns)' "$CACHE")
{
  echo "# ExecMutantSandbox M48-10 demonstration"
  echo "driver_sha256=$(sha256sum "$0" | cut -d' ' -f1)"
  echo "hostguard_sha256=$(sha256sum "$HOSTGUARD" | cut -d' ' -f1)"
  echo "python=$(python3 -V 2>&1) bwrap=$(bwrap --version 2>&1) ulimit_f=$(ulimit -f)"
  echo "fake_home=$FH cache=$CACHE"
  echo "orig_sha256=$ORIG_SHA orig_size=$ORIG_SIZE orig_mtime_ns=$ORIG_MTIME_NS"
  echo "lane=$LANE"
} > "$R/00-setup.txt"

# ---- A: unsandboxed, HOME pointed at the fake home. The guard must FAIL. --------------------------------------
MUTANT_PAYLOAD='r49-w1-mutant-caseA' python3 "$HOSTGUARD" run --work "$WORK" --home "$FH" \
    --env-keep MUTANT_PAYLOAD --declare "$CACHE" -- python3 "$S/mutant.py" > "$R/a-unsandboxed-caught.txt" 2>&1
rcA=$?
{ echo "--- hostguard exit=$rcA (expect 3)"; cat "$R/a-unsandboxed-caught.txt"; } > "$R/a.tmp"
mv "$R/a.tmp" "$R/a-unsandboxed-caught.txt"
say "caseA_exit=$rcA (unsandboxed, expect 3)"

# ---- A2: same size, original mtime restored by the mutant. Only sha256 can catch it. -------------------------
make_cache
SIZE_BEFORE=$(stat -c %s "$CACHE")
PAYLOAD=$(python3 -c "import sys; sys.stdout.write('X'*$SIZE_BEFORE)")
MUTANT_PAYLOAD="$PAYLOAD" MUTANT_RESTORE_MTIME="$ORIG_MTIME_NS" python3 "$HOSTGUARD" run --work "$WORK" \
    --home "$FH" --env-keep MUTANT_PAYLOAD --env-keep MUTANT_RESTORE_MTIME --declare "$CACHE" \
    -- python3 "$S/mutant.py" > "$R/a2-same-size-mtime-restored.txt" 2>&1
rcA2=$?
say "caseA2_exit=$rcA2 (same size+mtime, expect 3)"

# ---- B: same mutant, fake home masked by an empty tmpfs. The guard must PASS (contained, not failed). -------
make_cache
MUTANT_PAYLOAD='r49-w1-mutant-caseB' python3 "$HOSTGUARD" run --work "$WORK" --home "$FH" \
    --sandbox bwrap --mask "$FH" --env-keep MUTANT_PAYLOAD --declare "$CACHE" -- python3 "$S/mutant.py" \
    > "$R/b-sandboxed-contained.txt" 2>&1
rcB=$?
{
  echo "--- hostguard exit=$rcB (expect 0)"
  echo "after_b sha256=$(sha256sum "$CACHE" | cut -d' ' -f1) size=$(stat -c %s "$CACHE") mtime_ns=$(stat -c %y "$CACHE")"
} >> "$R/b-sandboxed-contained.txt"
say "caseB_exit=$rcB (home masked, expect 0)"

# ---- B2: --ro-root. The write fails EROFS, TMPDIR under --work stays writable, the guard passes. -------------
make_cache
python3 "$HOSTGUARD" run --work "$WORK" --home "$FH" --sandbox bwrap --ro-root --declare "$CACHE" \
    -- python3 -c "
import os
p = os.path.join(os.environ['HOME'], '.cache', 'xdg-terminal-exec')
try:
    open(p, 'w').write('nope')
    print('WRITE_SUCCEEDED')
except OSError as e:
    print('WRITE_BLOCKED errno=%d' % e.errno)
t = os.path.join(os.environ['TMPDIR'], 'ok')
open(t, 'w').write('x')
print('TMPDIR_WRITE_OK size=%d' % os.path.getsize(t))
" > "$R/b2-ro-root.txt" 2>&1
rcB2=$?
echo "caseB2_exit=$rcB2 (ro-root, expect 0)" >> "$R/b2-ro-root.txt"
say "caseB2_exit=$rcB2 (ro-root, expect 0)"

# ---- C: negative control, child `true`, nothing to change. --------------------------------------------------
make_cache
python3 "$HOSTGUARD" run --work "$WORK" --home "$FH" --declare "$CACHE" -- true \
    > "$R/c-control-no-change.txt" 2>&1
rcC=$?
say "caseC_exit=$rcC (control, expect 0)"

# ---- C2: a child that writes inside its own scratch XDG root is not a violation. ----------------------------
make_cache
python3 "$HOSTGUARD" run --work "$WORK" --home "$FH" --declare "$CACHE" \
    -- python3 -c "
import os
p = os.path.join(os.environ['XDG_CACHE_HOME'], 'legit-probe.txt')
open(p, 'w').write('scratch\n')
print('SCRATCH_WRITE %s size=%d' % (p, os.path.getsize(p)))
" > "$R/c2-legit-scratch-write.txt" 2>&1
rcC2=$?
echo "caseC2_exit=$rcC2 (expect 0) probe_exists=$(test -f "$FH/.cache/legit-probe.txt" && echo yes || echo no)" \
    >> "$R/c2-legit-scratch-write.txt"
say "caseC2_exit=$rcC2 (legit scratch write, expect 0)"

# ---- E: refusals. None of these may reach the child. --------------------------------------------------------
mkdir -p "$REPO/.git" "$REPO/tools" "$REPO/w"
cp "$HOSTGUARD" "$REPO/tools/hostguard.py"
{
  echo "## E1 --work /tmp/... (round-48 w2/SentScratch)"
  python3 "$HOSTGUARD" run --work /tmp/hg-r49 --declare "$CACHE" -- true 2>&1; echo "exit=$?"
  echo "## E2 --work inside the lane repo (also the operator home)"
  python3 "$HOSTGUARD" run --work "$LANE/.ufo/waves/round-49/w1/ExecMutantSandbox/w" --declare "$CACHE" -- true 2>&1; echo "exit=$?"
  echo "## E2b --work inside a repo this script lives in (the repo rule alone, outside the home rule)"
  python3 "$REPO/tools/hostguard.py" run --work "$REPO/w" --declare "$CACHE" -- true 2>&1; echo "exit=$?"
  echo "## E3 --declare a directory"
  python3 "$HOSTGUARD" run --work "$WORK" --declare "$FH/.cache" -- true 2>&1; echo "exit=$?"
  echo "## E4 --declare a FIFO (never opened)"
  rm -f "$S/fifo"; mkfifo "$S/fifo"
  python3 "$HOSTGUARD" digest --declare "$S/fifo" 2>&1; echo "exit=$?"
  echo "## E5 --mask covering --work"
  python3 "$HOSTGUARD" run --work "$WORK" --sandbox bwrap --mask /fast --declare "$CACHE" -- true 2>&1; echo "exit=$?"
  echo "## E6 no --declare"
  python3 "$HOSTGUARD" run --work "$WORK" -- true 2>&1; echo "exit=$?"
  echo "## E7 the child exits 3 but nothing changed: must read 5, never 3"
  python3 "$HOSTGUARD" run --work "$WORK" --declare "$CACHE" -- sh -c 'exit 3' 2>&1; echo "exit=$?"
  echo "## E8 the child outlives --timeout 1: group killed, exit 5"
  python3 "$HOSTGUARD" run --work "$WORK" --timeout 1 --declare "$CACHE" -- sh -c 'sleep 30; :' 2>&1; echo "exit=$?"
} > "$R/e-refusals.txt" 2>&1

# ---- G: the counter surface: --json and --declare-file ------------------------------------------------------
make_cache
printf '# declared operator-owned paths\n%s\n' "$CACHE" > "$S/declared.txt"
MUTANT_PAYLOAD='r49-w1-mutant-caseG' python3 "$HOSTGUARD" run --work "$WORK" --home "$FH" --json \
    --env-keep MUTANT_PAYLOAD --declare-file "$S/declared.txt" -- python3 "$S/mutant.py" \
    > "$R/g-json.txt" 2>&1
rcG=$?
python3 - "$R/g-json.txt" <<'PY' >> "$R/g-json.txt"
import json, sys
lines = open(sys.argv[1]).read().splitlines()
obj = None
for line in reversed(lines):
    if line.startswith("{"):
        obj = json.loads(line)
        break
print("JSON status=%s changed=%d child_rc=%s sandbox=%s declared_label=%s"
      % (obj["status"], len(obj["changed"]), obj["child_rc"], obj["sandbox"], obj["label"]))
PY
say "caseG_exit=$rcG (json+declare-file, expect 3)"

# ---- H: the exact counter adoption shape, with the fake home standing in for the operator home ---------------
make_cache
mkdir -p "$S/work-h"
MUTANT_PAYLOAD='r49-w1-mutant-caseH1' python3 "$HOSTGUARD" run --work "$S/work-h" --work-prefix /fast/scratch \
    --declare "$CACHE" --env-keep MUTANT_PAYLOAD -- python3 "$S/mutant.py" > "$R/h1-adoption-home-redirect.txt" 2>&1
rcH1=$?
echo "caseH1_exit=$rcH1 (expect 0) cache_sha=$(sha256sum "$CACHE" | cut -d' ' -f1)" >> "$R/h1-adoption-home-redirect.txt"
MUTANT_PAYLOAD='r49-w1-mutant-caseH2' python3 "$HOSTGUARD" run --work "$S/work-h" --work-prefix /fast/scratch \
    --sandbox bwrap --mask "$FH" --declare "$CACHE" --env-keep MUTANT_PAYLOAD \
    -- python3 "$S/mutant.py" > "$R/h2-adoption-home-redirect-and-mask.txt" 2>&1
rcH2=$?
echo "caseH2_exit=$rcH2 (expect 0) cache_sha=$(sha256sum "$CACHE" | cut -d' ' -f1)" \
    >> "$R/h2-adoption-home-redirect-and-mask.txt"
say "caseH1_exit=$rcH1 caseH2_exit=$rcH2 (adoption shape, expect 0 0)"

# ---- I: a mutant with a HARDCODED operator path (HOME redirection alone cannot stop it) ----------------------
cat > "$S/mutant2.py" <<'PY'
import hashlib, os
target = os.environ["MUTANT_TARGET"]
os.makedirs(os.path.dirname(target), exist_ok=True)
body = b"r49-w1-hardcoded\n"
open(target, "wb").write(body)
print("MUTANT2 home=%s target=%s out_size=%d out_sha256=%s"
      % (os.environ["HOME"], target, len(body), hashlib.sha256(body).hexdigest()))
PY
make_cache
mkdir -p "$S/work-i"
MUTANT_TARGET="$CACHE" python3 "$HOSTGUARD" run --work "$S/work-i" --home "$S/work-i/home" \
    --env-keep MUTANT_TARGET --declare "$CACHE" -- python3 "$S/mutant2.py" \
    > "$R/i1-hardcoded-unsandboxed.txt" 2>&1
rcI1=$?
say "caseI1_exit=$rcI1 (hardcoded path, unsandboxed, expect 3)"
make_cache
MUTANT_TARGET="$CACHE" python3 "$HOSTGUARD" run --work "$S/work-i" --home "$S/work-i/home" \
    --sandbox bwrap --mask "$FH" --env-keep MUTANT_TARGET --declare "$CACHE" -- python3 "$S/mutant2.py" \
    > "$R/i2-hardcoded-masked.txt" 2>&1
rcI2=$?
echo "caseI2_exit=$rcI2 (expect 0) cache_sha=$(sha256sum "$CACHE" | cut -d' ' -f1)" \
    >> "$R/i2-hardcoded-masked.txt"
say "caseI2_exit=$rcI2 (hardcoded path, masked, expect 0)"

# ---- F: what the guard left behind in its scratch -----------------------------------------------------------
{
  echo "## files under <work> after the runs (the only tree the guard creates)"
  find "$S/work" "$S/work-h" "$S/work-i" -maxdepth 3 -printf '%y %p\n' 2>/dev/null \
      | sed -e "s|$S/work-h|<work-h>|" -e "s|$S/work-i|<work-i>|" -e "s|$S/work|<work>|" | sort
  echo "## the fake home after the runs"
  find "$FH" -maxdepth 3 -printf '%y %p %s\n' 2>/dev/null | sed "s|$FH|<fakehome>|" | sort
  echo "## the fake repo (never a guard target)"
  find "$REPO" -maxdepth 2 -printf '%y %p\n' 2>/dev/null | sed "s|$REPO|<repo>|" | sort
} > "$R/f-worktree.txt"

# ---- D: ONE read-only digest of the operator's real cache (stat + sha256). No guard run against it. ---------
python3 "$HOSTGUARD" digest --label operator-owned \
    --declare "$HOME/.cache/xdg-terminal-exec" > "$R/d-operator-cache-digest.txt" 2>&1
echo "digest_exit=$?" >> "$R/d-operator-cache-digest.txt"
{
  echo "# independent stat of the same path (read-only, no guard)"
  stat -c 'path=%n size=%s mtime=%Y inode=%i' "$HOME/.cache/xdg-terminal-exec" 2>&1
  sha256sum "$HOME/.cache/xdg-terminal-exec" 2>&1
} >> "$R/d-operator-cache-digest.txt"
# session material stays shape-only: the home directory is written as ~
sed -i "s|$HOME|~|g" "$R/d-operator-cache-digest.txt"

echo "receipts in $R:"; ls -1 "$R"
