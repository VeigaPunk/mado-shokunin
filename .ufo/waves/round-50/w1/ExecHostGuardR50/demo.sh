#!/bin/sh
# ExecHostGuardR50 - D7 (M48-10) demonstration driver, round 50 w1.
#
# Shows mado-hostguard.py BOTH WAYS on a FAKE operator home under this seat's scratch. The real home is
# never a `run` target: the driver exports HOME/XDG_*/TMPDIR into the scratch tree before anything runs, and
# the one real-state read is `digest` (lstat + sha256, no write).
#
#   A  unsandboxed mutant, HOME=<fake home>: the guard must exit 3 and name the changed fields;
#   A2 the same mutant with the original size and mtime restored: only sha256 can see it, exit 3;
#   B  the same mutant under `run --sandbox bwrap --mask <fake home>`: contained, exit 0, digest unchanged;
#   B2 --sandbox bwrap --ro-root: the write fails EROFS, TMPDIR under --work stays writable, exit 0;
#   C  negative control, child `/bin/true`: exit 0, nothing changed;
#   D  ONE read-only `digest` of the four operator paths in round-50/receipts/operator-state-before.txt,
#      compared value by value (paths printed as ~, never as a home path);
#   E  the refusals: a /tmp, /var/tmp and /dev/shm work dir, the passwd home as --home, a work dir inside a
#      repository, --mask/--ro-root without bwrap, and a --declare-file that does not exist;
#   F  the hermetic selftest, plus the control that the selftest itself refuses a /tmp work root;
#   G  --json: stdout is exactly one JSON object even though the child prints;
#   H  exactly what the guard left in its scratch (its own footprint, relative to the scratch root).
#
# Every writer runs under ulimit -f 65536 (64 MiB/file). Scratch is
# /fast/scratch/hyaku/mado-r50/ExecHostGuardR50/ and is removed on exit; every receipt is written directly
# into this seat directory before that happens.
set -u
ulimit -f 65536

HERE=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
LANE=$(CDPATH= cd -- "$HERE/../../../../.." && pwd)
R="$HERE/receipts"
GUARD="$HERE/mado-hostguard.py"
S=/fast/scratch/hyaku/mado-r50/ExecHostGuardR50
PY=${PYTHON:-/usr/bin/python3}
CACHE_REL='.cache/xdg-terminal-exec'

rm -rf -- "$S"
mkdir -p "$R" "$S/fakehome/.cache" "$S/work" "$S/tmp" || exit 9
trap 'rm -rf -- "$S"' EXIT INT TERM

# The fake operator home is the ONLY home any child here sees (host guard, round-48 M48-10).
export HOME="$S/fakehome"
export XDG_CACHE_HOME="$S/fakehome/.cache"
export XDG_CONFIG_HOME="$S/fakehome/.config"
export XDG_DATA_HOME="$S/fakehome/.local/share"
export XDG_STATE_HOME="$S/fakehome/.local/state"
export TMPDIR="$S/tmp"
FAKEHOME="$S/fakehome"
CACHE="$FAKEHOME/$CACHE_REL"
BEFORE="$HERE/../../receipts/operator-state-before.txt"

EXITS="$R/00-case-exits.txt"
: > "$EXITS"
FAILS=0
say() { echo "$1"; echo "$1" >> "$EXITS"; }
check() { # check <label> <expected> <actual>
    if [ "$2" = "$3" ]; then say "OK   $1 expected=$2"; else say "FAIL $1 expected=$2 got=$3"; FAILS=$((FAILS + 1)); fi
}

# ---- fixture: a plausible 331-byte resolver cache, mtime pinned like the round-47/48 records ------------
make_cache() {
    "$PY" - "$CACHE" <<'PY'
import os, sys
p = sys.argv[1]
payload = (b"mado-hostguard r50 demo fixture, not operator state\n" * 8)[:331]
open(p, "wb").write(payload)
os.utime(p, ns=(1793047345000000000, 1793047345000000000))
PY
}
make_cache

# ---- the mutant: M48-10's own shape (write $HOME/.cache/xdg-terminal-exec, no sandbox of its own) -------
cat > "$S/mutant.py" <<'PY'
import os, sys
target = os.environ.get("MUTANT_TARGET") or os.path.join(os.environ["HOME"], ".cache", "xdg-terminal-exec")
payload = os.environ.get("MUTANT_PAYLOAD", "r50-mutant")
os.makedirs(os.path.dirname(target), exist_ok=True)
with open(target, "w") as fh:
    fh.write(payload)
if os.environ.get("MUTANT_MTIME_NS"):
    os.utime(target, ns=(int(os.environ["MUTANT_MTIME_NS"]), int(os.environ["MUTANT_MTIME_NS"])))
print("WROTE path=%s size=%d" % (target, os.path.getsize(target)))
PY

orig_sha() { "$PY" -c 'import hashlib,sys;print(hashlib.sha256(open(sys.argv[1],"rb").read()).hexdigest())' "$1"; }
orig_size() { "$PY" -c 'import os,sys;print(os.path.getsize(sys.argv[1]))' "$1"; }

{
    echo "# ExecHostGuardR50 demo setup"
    echo "lane=$(basename "$LANE") guard_rel=${GUARD#"$LANE"/}"
    echo "guard_sha256=$(sha256sum "$GUARD" | cut -d' ' -f1)"
    echo "demo_sha256=$(sha256sum "$0" | cut -d' ' -f1)"
    echo "python=$("$PY" --version 2>&1) bwrap=$(bwrap --version 2>/dev/null || echo absent) ulimit_f=65536"
    echo "fixture=$CACHE_REL size=$(orig_size "$CACHE") sha256=$(orig_sha "$CACHE") mtime_ns=1793047345000000000"
} > "$R/00-setup.txt"

# ---- A: unsandboxed, HOME=<fake home>. The guard must FAIL. --------------------------------------------
make_cache
MUTANT_PAYLOAD='r50-caught' "$PY" "$GUARD" run --work "$S/work" --work-prefix "$S" --home "$FAKEHOME" \
    --declare "$CACHE" --env-keep MUTANT_PAYLOAD -- "$PY" "$S/mutant.py" \
    > "$R/a-unsandboxed-caught.txt" 2>&1
rcA=$?
{ echo "--- exit=$rcA (expect 3)"; grep -E 'CHANGED|child_rc=|status=' "$R/a-unsandboxed-caught.txt"; } \
    > "$R/a.tmp"; mv "$R/a.tmp" "$R/a-unsandboxed-caught.txt"
check caseA_unsandboxed_caught 3 "$rcA"
grep -q 'fields=sha256,size,mtime_ns' "$R/a-unsandboxed-caught.txt" \
    && say "OK   caseA_fields_named sha256,size,mtime_ns" \
    || { say "FAIL caseA_fields_named"; FAILS=$((FAILS + 1)); }

# ---- A2: same size, original mtime restored. Only sha256 can catch it. ---------------------------------
make_cache
SIZE=$(orig_size "$CACHE")
PAYLOAD=$("$PY" -c "print('X'*$SIZE, end='')")
MUTANT_PAYLOAD="$PAYLOAD" MUTANT_MTIME_NS=1793047345000000000 "$PY" "$GUARD" run --work "$S/work" \
    --home "$FAKEHOME" --declare "$CACHE" --env-keep MUTANT_PAYLOAD --env-keep MUTANT_MTIME_NS \
    -- "$PY" "$S/mutant.py" > "$R/a2-same-size-mtime-restored.txt" 2>&1
rcA2=$?
{ echo "--- exit=$rcA2 (expect 3)";
  grep -E 'CHANGED|status=' "$R/a2-same-size-mtime-restored.txt"; } > "$R/a2.tmp"
mv "$R/a2.tmp" "$R/a2-same-size-mtime-restored.txt"
check caseA2_same_size_same_mtime 3 "$rcA2"
grep -q 'fields=sha256 sha256=' "$R/a2-same-size-mtime-restored.txt" \
    && say "OK   caseA2_only_sha256_moved" || { say "FAIL caseA2_only_sha256_moved"; FAILS=$((FAILS + 1)); }

# ---- B: the same mutant, fake home masked by an empty tmpfs. Contained: exit 0, digest unchanged. ------
make_cache
SHA_BEFORE=$(orig_sha "$CACHE")
MUTANT_PAYLOAD='r50-contained' "$PY" "$GUARD" run --work "$S/work" --work-prefix "$S" --home "$FAKEHOME" \
    --sandbox bwrap --mask "$FAKEHOME" --declare "$CACHE" --env-keep MUTANT_PAYLOAD \
    -- "$PY" "$S/mutant.py" > "$R/b-sandboxed-contained.txt" 2>&1
rcB=$?
SHA_AFTER=$(orig_sha "$CACHE")
{
    echo "--- exit=$rcB (expect 0) sha256_before=$SHA_BEFORE sha256_after=$SHA_AFTER"
    grep -E 'WROTE|CHANGED|child_rc=|status=' "$R/b-sandboxed-contained.txt"
} > "$R/b.tmp"
mv "$R/b.tmp" "$R/b-sandboxed-contained.txt"
check caseB_bwrap_contained 0 "$rcB"
check caseB_digest_unchanged "$SHA_BEFORE" "$SHA_AFTER"
grep -q 'WROTE ' "$R/b-sandboxed-contained.txt" \
    && say "OK   caseB_mutant_reports_a_successful_write (contained, not merely failed)" \
    || { say "FAIL caseB_mutant_write"; FAILS=$((FAILS + 1)); }

# ---- B2: --ro-root. The write fails EROFS (30), TMPDIR under --work stays writable, guard passes. ------
make_cache
cat > "$S/ro_probe.py" <<'PROBE'
import os
p = os.path.join(os.environ["HOME"], ".cache", "xdg-terminal-exec")
try:
    open(p, "w").write("nope")
    print("WRITE_SUCCEEDED")
except OSError as e:
    print("WRITE_BLOCKED errno=%d" % e.errno)
t = os.path.join(os.environ["TMPDIR"], "ok")
open(t, "w").write("x")
print("TMPDIR_WRITE_OK size=%d" % os.path.getsize(t))
PROBE
"$PY" "$GUARD" run --work "$S/work" --home "$FAKEHOME" --sandbox bwrap --ro-root --declare "$CACHE" \
    -- "$PY" "$S/ro_probe.py" > "$R/b2-ro-root.txt" 2>&1
rcB2=$?
echo "caseB2_exit=$rcB2 (expect 0)" >> "$R/b2-ro-root.txt"
check caseB2_ro_root 0 "$rcB2"
grep -q 'WRITE_BLOCKED errno=30' "$R/b2-ro-root.txt" \
    && say "OK   caseB2_write_blocked_EROFS" || { say "FAIL caseB2_write_blocked"; FAILS=$((FAILS + 1)); }

# ---- C: negative control, nothing to change. -----------------------------------------------------------
make_cache
SHA_BEFORE=$(orig_sha "$CACHE")
"$PY" "$GUARD" run --work "$S/work" --home "$FAKEHOME" --declare "$CACHE" -- /bin/true \
    > "$R/c-control-no-change.txt" 2>&1
rcC=$?
echo "caseC_exit=$rcC (expect 0) sha_unchanged=$( [ "$(orig_sha "$CACHE")" = "$SHA_BEFORE" ] && echo yes || echo no )" \
    >> "$R/c-control-no-change.txt"
check caseC_control_noop 0 "$rcC"

# ---- D: ONE read-only digest of the operator's real state, compared with the round-50 before receipt ---
REALHOME=$("$PY" -c 'import os,pwd;print(pwd.getpwuid(os.getuid()).pw_dir)')
cat > "$S/compare.py" <<'CMP'
import re, sys
table, before = sys.argv[1], sys.argv[2]
digest = {}
for line in open(table, encoding="utf-8"):
    if line.startswith("operator-owned "):
        f = dict(kv.split("=", 1) for kv in line.split()[1:] if "=" in kv)
        digest[f["path"]] = f
want = {}
for line in open(before, encoding="utf-8"):
    m = re.match(r"^(\S+) sha256=([0-9a-f]{64}) size=(\d+) mtime=(\d+)", line)
    if m:
        want[m.group(1)] = (m.group(2), int(m.group(3)), int(m.group(4)))
bad = 0
for path in sorted(want):
    got = digest.get(path)
    if got is None:
        print(f"COMPARE MISSING path={path}")
        bad += 1
        continue
    mtime_s = int(got["mtime_ns"]) // 10 ** 9
    ok = (got["sha256"] == want[path][0] and int(got["size"]) == want[path][1]
          and mtime_s == want[path][2])
    bad += 0 if ok else 1
    print(f"COMPARE {'MATCH' if ok else 'MISMATCH'} path={path} sha256={got['sha256']} "
          f"size={got['size']} mtime_s={mtime_s}")
print(f"COMPARE summary paths={len(want)} mismatched={bad}")
CMP
digest_operator() { # digest_operator <outfile>
    "$PY" "$GUARD" digest \
        --declare "$REALHOME/.cache/xdg-terminal-exec" \
        --declare "$REALHOME/.config/hypr/input.conf" \
        --declare "$REALHOME/.config/hypr/bindings.conf" \
        --declare "$REALHOME/.config/hypr/hyprland.conf" > "$1" 2>&1
}
digest_operator "$R/d-operator-digest.txt"
rcD=$?
echo "digest_exit=$rcD (expect 0; paths are printed as ~)" >> "$R/d-operator-digest.txt"
LB=$(ls -la "$REALHOME/.local/bin" 2>/dev/null | wc -l)
echo "local_bin_ls_la_lines=$LB (before receipt: 103) same=$( [ "$LB" = 103 ] && echo yes || echo no )" \
    >> "$R/d-operator-digest.txt"
"$PY" "$S/compare.py" "$R/d-operator-digest.txt" "$BEFORE" >> "$R/d-operator-digest.txt"
check caseD_digest_exit 0 "$rcD"
grep -q 'COMPARE summary paths=4 mismatched=0' "$R/d-operator-digest.txt" \
    && say "OK   caseD_digest_reproduces_the_before_receipt (sha256+size+mtime_s)" \
    || { say "FAIL caseD_digest_reproduces_the_before_receipt"; FAILS=$((FAILS + 1)); }
grep -qE '(^| )/[^ ]*/\.cache/xdg-terminal-exec' "$R/d-operator-digest.txt" \
    && { say "FAIL caseD_home_path_leaked"; FAILS=$((FAILS + 1)); } \
    || say "OK   caseD_home_path_redacted"

# ---- E: refusals. None of these reaches a child. -------------------------------------------------------
{
    mkdir -p "$S/fakerepo/.git" "$S/fakerepo/tools"
    cp "$GUARD" "$S/fakerepo/tools/mado-hostguard.py"
    printf '# declared operator-owned paths\n%s\n' "$CACHE" > "$S/declared.txt"
    try() { # try <label> <expect> <work> <extra...>
        label=$1; expect=$2; work=$3; shift 3
        "$PY" "$GUARD" run --work "$work" --home "$FAKEHOME" --declare "$CACHE" "$@" -- /bin/true \
            > "$S/e.out" 2> "$S/e.err"
        rc=$?
        echo "$label exit=$rc expect=$expect stderr=$(head -1 "$S/e.err")"
    }
    try E1_work_under_tmp        2 /tmp/mado-hg-demo-w1
    try E2_work_under_vartmp     2 /var/tmp/mado-hg-demo-w1
    try E3_work_under_devshm     2 /dev/shm/mado-hg-demo-w1
    try E4_lane_work_refused 2 "$HERE/tmpwork"
    "$PY" "$S/fakerepo/tools/mado-hostguard.py" run --work "$S/fakerepo/w" --home "$FAKEHOME" \
        --declare "$CACHE" -- /bin/true > "$S/e.out" 2> "$S/e.err"
    echo "E5_repo_work_copy exit=$? expect=2 stderr=$(head -1 "$S/e.err")"
    try E6_mask_without_bwrap    2 "$S/work" --mask "$FAKEHOME"
    try E7_ro_root_without_bwrap 2 "$S/work" --ro-root
    try E8_declare_file_missing  2 "$S/work" --declare-file "$S/no-such-file"
    "$PY" "$GUARD" run --work "$S/work" --home "$REALHOME" --declare "$CACHE" -- /bin/true \
        > "$S/e.out" 2> "$S/e.err"
    echo "E9_home_is_passwd_home exit=$? expect=2 stderr=$(head -1 "$S/e.err" | sed "s|$REALHOME|<passwd-home>|g")"
    echo "E10_/tmp_dir_created=$(test -e /tmp/mado-hg-demo-w1 && echo yes || echo no) expect=no"
    echo "E11_repo_w_dir_created=$(test -e "$S/fakerepo/w" && echo yes || echo no) expect=no"
    echo "E12_lane_tmpwork_created=$(test -e "$HERE/tmpwork" && echo yes || echo no) expect=no"
} > "$R/e-refusals.txt" 2>&1
while read -r line; do
    case $line in
        E*expect=*) exp=$(echo "$line" | sed -n 's/.*expect=\([0-9]\).*/\1/p')
                    got=$(echo "$line" | sed -n 's/.*exit=\([0-9]*\).*/\1/p')
                    if [ -n "$exp" ] && [ "$exp" != "$got" ]; then
                        say "FAIL refusal ${line%% *} expected=$exp got=$got"; FAILS=$((FAILS + 1))
                    fi ;;
    esac
done < "$R/e-refusals.txt"
say "OK   caseE_refusals_checked (see e-refusals.txt)"
grep -qE 'exit=2 .*operator home' "$R/e-refusals.txt" \
    && say "OK   caseE_passwd_home_refused_even_with_HOME_redirected" \
    || { say "FAIL caseE_passwd_home_refused"; FAILS=$((FAILS + 1)); }
for want in E10_/tmp_dir_created=no E11_repo_w_dir_created=no E12_lane_tmpwork_created=no; do
    if grep -q "$want" "$R/e-refusals.txt"; then say "OK   caseE_${want%%=*}"; else
        say "FAIL caseE_${want%%=*} (a refused work dir was created or the line is missing)"; FAILS=$((FAILS + 1))
    fi
done

# ---- F: the hermetic selftest, and the selftest's own /tmp refusal. -----------------------------------
TMPDIR="$S/tmp" "$PY" -I "$GUARD" --selftest --work "$S/selftest" > "$R/f-selftest.txt" 2>&1
rcF=$?
LAST=$(tail -1 "$R/f-selftest.txt")
echo "selftest_exit=$rcF (expect 0) last_line_before_this_meta=$LAST" >> "$R/f-selftest.txt"
check caseF_selftest 0 "$rcF"
case $LAST in
    MADO_HOSTGUARD_SELFTEST:*" passed") say "OK   caseF_selftest_last_line $LAST" ;;
    *) say "FAIL caseF_selftest_last_line got=$LAST"; FAILS=$((FAILS + 1)) ;;
esac
echo "$LAST" | grep -Eq '^MADO_HOSTGUARD_SELFTEST: [0-9]+/[0-9]+ passed$' \
    || { say "FAIL caseF_selftest_line_shape"; FAILS=$((FAILS + 1)); }
TMPDIR=/tmp "$PY" -I "$GUARD" --selftest > "$R/f2-selftest-tmp-refused.txt" 2>&1
rcF2=$?
echo "selftest_tmpdir_slash_tmp_exit=$rcF2 (expect 2)" >> "$R/f2-selftest-tmp-refused.txt"
check caseF2_selftest_refuses_tmp 2 "$rcF2"

# ---- G: --json. stdout is exactly one JSON object even though the child prints. ----------------------
make_cache
MUTANT_PAYLOAD='r50-json' "$PY" "$GUARD" run --work "$S/work" --home "$FAKEHOME" --json \
    --declare "$CACHE" --env-keep MUTANT_PAYLOAD -- "$PY" "$S/mutant.py" > "$R/g-json.txt" 2> "$R/g-json.err"
rcG=$?
echo "caseG_exit=$rcG (expect 3)" >> "$R/g-json.txt"
"$PY" - "$R/g-json.txt" "$R/g-json.err" <<'PY' >> "$R/g-json.txt"
import json, sys
out, err = sys.argv[1], sys.argv[2]
raw = open(out, encoding="utf-8").read()
probe = raw.rsplit("\ncaseG_exit=", 1)[0]
data = json.loads(probe)          # raises if stdout is not exactly one JSON object
print(f"JSON status={data['status']} child_rc={data['child_rc']} "
      f"changed_fields={','.join(data['changed'][0]['fields'])} sandbox={data['sandbox']} "
      f"declared={len(data['before'])}")
print(f"JSON child_stdout_went_to_stderr={'WROTE ' in open(err, encoding='utf-8').read()}")
PY
check caseG_json 3 "$rcG"
grep -q 'JSON status=violation' "$R/g-json.txt" \
    && say "OK   caseG_stdout_is_exactly_one_json_object" || { say "FAIL caseG_json"; FAILS=$((FAILS + 1)); }

# ---- I: outer-tracer parity (SentHostState R-SHS-3 shape): an outer tracer must not change the verdict --
# The C1 counter runs `strace … bwrap …` itself, so an outer tracer makes its nested ptrace fail and it reads
# a FALSE TARGET_MISSED. This guard starts no tracer of its own: an outer tracer must leave the verdict intact.
make_cache
SHA_BEFORE=$(orig_sha "$CACHE")
if command -v strace >/dev/null 2>&1 && command -v bwrap >/dev/null 2>&1; then
    MUTANT_PAYLOAD='r50-tracer' timeout 120 strace -f -o "$S/strace.log" -e trace=execve \
        "$PY" "$GUARD" run --work "$S/work" --home "$FAKEHOME" --sandbox bwrap --mask "$FAKEHOME" \
        --declare "$CACHE" --env-keep MUTANT_PAYLOAD -- "$PY" "$S/mutant.py" \
        > "$R/i-outer-tracer.txt" 2>&1
    rcI=$?
    SHA_AFTER=$(orig_sha "$CACHE")
    {
        echo "--- exit=$rcI (expect 0: same verdict as case B, contained)"
        echo "sha256_before=$SHA_BEFORE sha256_after=$SHA_AFTER"
        echo "bwrap_execve_lines=$(grep -c 'execve("/usr/bin/bwrap"' "$S/strace.log" 2>/dev/null || true)"
        echo "execve_lines=$(grep -c 'execve(' "$S/strace.log" 2>/dev/null || true)"
        echo "ptrace_failures=$(grep -c 'PTRACE_SEIZE\|Operation not permitted' "$S/strace.log" 2>/dev/null || true)"
        grep -E 'WROTE|child_rc=|status=' "$R/i-outer-tracer.txt" | head -3
    } > "$R/i.tmp"
    mv "$R/i.tmp" "$R/i-outer-tracer.txt"
    check caseI_outer_tracer_contained 0 "$rcI"
    check caseI_outer_tracer_digest_unchanged "$SHA_BEFORE" "$SHA_AFTER"
    grep -q 'WROTE ' "$R/i-outer-tracer.txt" \
        && say "OK   caseI_outer_tracer_write_still_contained" \
        || { say "FAIL caseI_outer_tracer_write"; FAILS=$((FAILS + 1)); }
else
    echo "caseI_outer_tracer=skipped (strace or bwrap absent on PATH)" > "$R/i-outer-tracer.txt"
    say "NOTE caseI_outer_tracer skipped: strace or bwrap absent"
fi

# ---- H: what the guard left in its scratch (its own footprint, relative to the scratch root) ----------
{
    echo "# files/files+dirs the guard created, relative to the scratch root"
    find "$S/work" "$S/selftest" -mindepth 1 -maxdepth 4 2>/dev/null | sed "s|^$S/||" | sort
    echo "# the fake home is scratch (case G's mutant wrote 8 bytes into it); no declared path outside the"
    echo "# fake home is touched by any case:"
    echo "fakehome_cache_sha256=$(orig_sha "$CACHE") fakehome_cache_size=$(orig_size "$CACHE")"
} > "$R/h-footprint.txt"

# ---- D2: the same digest AFTER every case: this demonstration wrote no operator state -----------------
digest_operator "$R/d2-operator-digest-after.txt"
rcD2=$?
echo "digest_exit=$rcD2 (expect 0) taken after every case above" >> "$R/d2-operator-digest-after.txt"
"$PY" "$S/compare.py" "$R/d2-operator-digest-after.txt" "$BEFORE" >> "$R/d2-operator-digest-after.txt"
check caseD2_digest_after_the_whole_demo 0 "$rcD2"
grep -q 'COMPARE summary paths=4 mismatched=0' "$R/d2-operator-digest-after.txt" \
    && say "OK   caseD2_operator_state_unchanged_after_every_case" \
    || { say "FAIL caseD2_operator_state_unchanged_after_every_case"; FAILS=$((FAILS + 1)); }
grep -qE '(^| )/[^ ]*/\.cache/xdg-terminal-exec' "$R/d2-operator-digest-after.txt" \
    && { say "FAIL caseD2_home_path_leaked"; FAILS=$((FAILS + 1)); } \
    || say "OK   caseD2_home_path_redacted"

# ---- index ---------------------------------------------------------------------------------------------
{
    echo "# ExecHostGuardR50 case index  fails=$FAILS"
    cat "$EXITS"
} > "$R/00-case-exits.tmp"
mv "$R/00-case-exits.tmp" "$EXITS"

( cd "$R" && find . -maxdepth 1 -type f ! -name SHA256SUMS -printf '%P\n' | LC_ALL=C sort \
    | xargs sha256sum > SHA256SUMS )
echo "receipts in $R (fails=$FAILS):"
ls -1 "$R"
exit "$FAILS"
