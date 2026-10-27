#!/bin/sh
# RevHostGuardInstalled - w2 falsify probes against tools/mado-hostguard.py at b4a79843.
# Fake operator home under this seat's scratch; the real home is never touched.
set -u
ulimit -f 65536

HERE=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
R="$HERE/receipts"
S=/fast/scratch/hyaku/mado-r50/RevHostGuardInstalled/demo
GUARD=/fast/scratch/hyaku/mado-r50/RevHostGuardInstalled/lane/tools/mado-hostguard.py
PY=/usr/bin/python3
CACHE_REL='.cache/xdg-terminal-exec'

rm -rf -- "$S"
mkdir -p "$R" "$S/fakehome/.cache" "$S/work" "$S/tmp" || exit 9

export HOME="$S/fakehome"
export XDG_CACHE_HOME="$S/fakehome/.cache"
export XDG_CONFIG_HOME="$S/fakehome/.config"
export XDG_DATA_HOME="$S/fakehome/.local/share"
export XDG_STATE_HOME="$S/fakehome/.local/state"
export TMPDIR="$S/tmp"
FAKEHOME="$S/fakehome"
CACHE="$FAKEHOME/$CACHE_REL"

EXITS="$R/00-case-exits.txt"
: > "$EXITS"
FAILS=0
say() { echo "$1"; echo "$1" >> "$EXITS"; }
check() { if [ "$2" = "$3" ]; then say "OK   $1 expected=$2"; else say "FAIL $1 expected=$2 got=$3"; FAILS=$((FAILS + 1)); fi; }

# ---- fixture: 331-byte resolver cache with the round-47/48 pinned mtime -------------------------------
make_cache() {
    $PY - "$CACHE" <<'PY'
import os, sys
body = b"mado-hostguard r50 w2 probe fixture, not operator state\n"
p = sys.argv[1]
data = (body * (331 // len(body) + 1))[:331]
with open(p, "wb") as fh:
    fh.write(data)
os.utime(p, ns=(1793047345000000000, 1793047345000000000))
PY
}

cat > "$S/mutant.py" <<'PY'
import os, sys, time
mode = sys.argv[1]
target = os.environ["MUTANT_TARGET"]
payload = os.environ.get("MUTANT_PAYLOAD", "r50-w2-probe")
d, b = os.path.split(target)
if mode == "direct":
    with open(target, "w") as fh: fh.write(payload)
elif mode == "same-size":
    size = os.path.getsize(target)
    with open(target, "w") as fh: fh.write("X" * size)
    os.utime(target, ns=(1793047345000000000, 1793047345000000000))
elif mode == "undeclared":
    with open(os.path.join(os.environ["HOME"], "undeclared-new.txt"), "w") as fh: fh.write(payload)
    with open(os.environ["MUTANT_UNDECLARED"], "a") as fh: fh.write(payload)
elif mode == "hardlink":
    link = os.path.join(os.environ["HOME"], "hardlink-alias")
    if not os.path.exists(link): os.link(target, link)
    with open(link, "w") as fh: fh.write(payload)
elif mode == "rename":
    tmp = os.path.join(d, ".xdg-renametmp")
    with open(tmp, "w") as fh: fh.write(payload)
    os.replace(tmp, target)
elif mode == "recreate":
    data = open(target, "rb").read()
    os.unlink(target)
    with open(target, "wb") as fh: fh.write(data)
    os.utime(target, ns=(1793047345000000000, 1793047345000000000))
elif mode == "dirfd":
    dirfd = os.open(d, os.O_RDONLY | os.O_DIRECTORY)
    fd = os.open(b, os.O_WRONLY | os.O_TRUNC, dir_fd=dirfd)
    os.write(fd, payload.encode()); os.close(fd); os.close(dirfd)
elif mode == "detached":
    pid = os.fork()
    if pid == 0:
        time.sleep(0.3)
        with open(target, "w") as fh: fh.write(payload)
        os._exit(0)
    os._exit(0)
PY

# An undeclared pre-existing file the mutant can modify.
echo "pre-existing undeclared content" > "$FAKEHOME/undeclared-existing.txt"
UNDECLARED="$FAKEHOME/undeclared-existing.txt"

# ---- A: unsandboxed direct write to the DECLARED path. Expect exit 3. ---------------------------------
make_cache
MUTANT_TARGET="$CACHE" MUTANT_PAYLOAD='w2-direct' $PY "$GUARD" run --work "$S/work" --work-prefix "$S" \
    --home "$FAKEHOME" --declare "$CACHE" --env-keep MUTANT_TARGET --env-keep MUTANT_PAYLOAD \
    -- "$PY" "$S/mutant.py" direct > "$R/a-direct-caught.txt" 2>&1
rcA=$?
check caseA_direct_declared_changed 3 "$rcA"
grep -q 'fields=sha256,size,mtime_ns' "$R/a-direct-caught.txt" && say "OK   caseA_fields_named sha256,size,mtime_ns" || { say "FAIL caseA_fields_named"; FAILS=$((FAILS+1)); }

# ---- U: undeclared writes INSIDE the fake home (new file + append to an existing undeclared file). ----
# Contract: the guard pins only --declare paths; the docstring states it fails only if a declared path changed.
make_cache
MUTANT_TARGET="$CACHE" MUTANT_PAYLOAD='w2-undeclared' MUTANT_UNDECLARED="$UNDECLARED" \
    $PY "$GUARD" run --work "$S/work" --home "$FAKEHOME" \
    --declare "$CACHE" --env-keep MUTANT_TARGET --env-keep MUTANT_PAYLOAD --env-keep MUTANT_UNDECLARED \
    -- "$PY" "$S/mutant.py" undeclared > "$R/u-undeclared-inside-home.txt" 2>&1
rcU=$?
check caseU_undeclared_inside_home_not_a_violation 0 "$rcU"
grep -q 'changed=0 status=ok' "$R/u-undeclared-inside-home.txt" && say "OK   caseU_guard_reports_changed0_status_ok" || { say "FAIL caseU_report_shape"; FAILS=$((FAILS+1)); }
test -f "$FAKEHOME/undeclared-new.txt" && say "OK   caseU_undeclared_new_file_was_written" || { say "FAIL caseU_undeclared_new_file"; FAILS=$((FAILS+1)); }

# ---- D1: hardlink to the declared path, write through the alias. --------------------------------------
make_cache
MUTANT_TARGET="$CACHE" MUTANT_PAYLOAD='w2-hardlink' $PY "$GUARD" run --work "$S/work" --home "$FAKEHOME" \
    --declare "$CACHE" --env-keep MUTANT_TARGET --env-keep MUTANT_PAYLOAD \
    -- "$PY" "$S/mutant.py" hardlink > "$R/d1-hardlink.txt" 2>&1
rcD1=$?
check caseD1_hardlink_write_caught 3 "$rcD1"
grep -q 'fields=' "$R/d1-hardlink.txt" && say "OK   caseD1_fields_named $(grep -o 'fields=[a-z_,]*' "$R/d1-hardlink.txt" | head -1)" || { say "FAIL caseD1_fields"; FAILS=$((FAILS+1)); }

# ---- D2: atomic rename (write tmp + os.replace over the declared path). -------------------------------
make_cache
MUTANT_TARGET="$CACHE" MUTANT_PAYLOAD='w2-rename' $PY "$GUARD" run --work "$S/work" --home "$FAKEHOME" \
    --declare "$CACHE" --env-keep MUTANT_TARGET --env-keep MUTANT_PAYLOAD \
    -- "$PY" "$S/mutant.py" rename > "$R/d2-atomic-rename.txt" 2>&1
rcD2=$?
check caseD2_atomic_rename_caught 3 "$rcD2"
grep -q 'fields=' "$R/d2-atomic-rename.txt" && say "OK   caseD2_fields_named $(grep -o 'fields=[a-z_,]*' "$R/d2-atomic-rename.txt" | head -1)" || { say "FAIL caseD2_fields"; FAILS=$((FAILS+1)); }

# ---- D3: delete + recreate identical bytes + original mtime restored (probes the ino field). ----------
make_cache
MUTANT_TARGET="$CACHE" $PY "$GUARD" run --work "$S/work" --home "$FAKEHOME" \
    --declare "$CACHE" --env-keep MUTANT_TARGET -- "$PY" "$S/mutant.py" recreate \
    > "$R/d3-recreate-same-bytes.txt" 2>&1
rcD3=$?
check caseD3_delete_recreate_caught 3 "$rcD3"
grep -q 'fields=' "$R/d3-recreate-same-bytes.txt" && say "OK   caseD3_fields_named $(grep -o 'fields=[a-z_,]*' "$R/d3-recreate-same-bytes.txt" | head -1)" || { say "FAIL caseD3_fields"; FAILS=$((FAILS+1)); }

# ---- D4: dirfd-relative openat on the declared path's directory. --------------------------------------
make_cache
MUTANT_TARGET="$CACHE" MUTANT_PAYLOAD='w2-dirfd' $PY "$GUARD" run --work "$S/work" --home "$FAKEHOME" \
    --declare "$CACHE" --env-keep MUTANT_TARGET --env-keep MUTANT_PAYLOAD \
    -- "$PY" "$S/mutant.py" dirfd > "$R/d4-dirfd-openat.txt" 2>&1
rcD4=$?
check caseD4_dirfd_openat_caught 3 "$rcD4"
grep -q 'fields=' "$R/d4-dirfd-openat.txt" && say "OK   caseD4_fields_named $(grep -o 'fields=[a-z_,]*' "$R/d4-dirfd-openat.txt" | head -1)" || { say "FAIL caseD4_fields"; FAILS=$((FAILS+1)); }

# ---- D5: detached grandchild writes the declared path AFTER the direct child exits 0. ------------------
# The guard snapshots right after wait(); a delayed write lands after the after-digest.
make_cache
BEFORE_SHA=$($PY -c 'import hashlib,sys;print(hashlib.sha256(open(sys.argv[1],"rb").read()).hexdigest())' "$CACHE")
MUTANT_TARGET="$CACHE" MUTANT_PAYLOAD='w2-detached' $PY "$GUARD" run --work "$S/work" --home "$FAKEHOME" \
    --declare "$CACHE" --env-keep MUTANT_TARGET --env-keep MUTANT_PAYLOAD \
    -- "$PY" "$S/mutant.py" detached > "$R/d5-detached-writer.txt" 2>&1
rcD5=$?
sleep 1
AFTER_SHA=$($PY -c 'import hashlib,sys;print(hashlib.sha256(open(sys.argv[1],"rb").read()).hexdigest())' "$CACHE")
say "INFO caseD5_guard_exit=$rcD5 (a pass here would read 0)"
say "INFO caseD5_declared_sha_before=$BEFORE_SHA"
say "INFO caseD5_declared_sha_after=$AFTER_SHA"
if [ "$rcD5" = 0 ] && [ "$BEFORE_SHA" != "$AFTER_SHA" ]; then
    say "EVADE caseD5_detached_writer_NOT_caught (exit 0 while the declared path changed after the run)"
else
    say "OK   caseD5_detached_writer_caught_or_noop rc=$rcD5 changed=$([ "$BEFORE_SHA" != "$AFTER_SHA" ] && echo yes || echo no)"
fi
grep -E 'child_rc=|status=' "$R/d5-detached-writer.txt" | tail -2 >> "$EXITS" || true

# ---- index ---------------------------------------------------------------------------------------------
{
    echo "# RevHostGuardInstalled probe index  fails=$FAILS"
    cat "$EXITS"
} > "$EXITS.tmp"
mv "$EXITS.tmp" "$EXITS"
( cd "$R" && find . -maxdepth 1 -type f ! -name SHA256SUMS -printf '%P\n' | LC_ALL=C sort | xargs sha256sum > SHA256SUMS )
echo "receipts in $R (fails=$FAILS):"
ls -1 "$R"
exit "$FAILS"
