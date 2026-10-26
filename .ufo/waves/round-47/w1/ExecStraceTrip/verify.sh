#!/bin/bash
# verify.sh -- reproducible evidence generator for the ExecStraceTrip probe.
#
# Runs the probe matrix and the reference tripwire on this host and writes every
# receipt into ./receipts.  Nothing is written outside --work (default
# $TMPDIR/mado-r47-verify) and ./receipts.
#
#   verify.sh [--work DIR]
#
# Exit 0 only when the probe reports every expectation and the tripwire matrix
# matches its declared verdicts.
set -u

HERE=$(cd -- "$(dirname -- "$0")" && pwd)
WORK="${TMPDIR:-/var/tmp}/mado-r47-verify"
[ "${1-}" = "--work" ] && WORK=${2-}
mkdir -p -- "$WORK" "$HERE/receipts" || exit 2
WORK=$(cd -- "$WORK" && pwd)
REC="$HERE/receipts"
FAIL=0

echo "== host ==" > "$REC/environment.txt"
{
    printf 'kernel      %s\n' "$(uname -r)"
    printf 'python      %s\n' "$(python3 -V 2>&1)"
    printf 'strace      %s\n' "$(strace -V 2>&1 | head -1)"
    printf 'bubblewrap  %s\n' "$(bwrap --version 2>&1)"
    printf 'yama_scope  %s\n' "$(cat /proc/sys/kernel/yama/ptrace_scope 2>/dev/null || echo unreadable)"
    printf 'seccomp     %s\n' "$(grep -c '^Seccomp:' /proc/self/status >/dev/null && awk -F'\t' '/^Seccomp:/{print $2}' /proc/self/status)"
} >> "$REC/environment.txt"

# 1. the probe matrix -------------------------------------------------------
echo "[1/4] probe matrix"
TMPDIR="$WORK" python3 -I "$HERE/probe.py" --work "$WORK/probe" > "$REC/probe-run.txt" 2>&1
PROBE_RC=$?
grep -E 'MADO_STRACE_PROBE|tripwire cost' "$REC/probe-run.txt"
[ "$PROBE_RC" -eq 0 ] || { echo "  probe returned $PROBE_RC"; FAIL=1; }

# 2. the reference tripwire, both directions --------------------------------
echo "[2/5] reference tripwire"
TOOLS="$WORK/tools"; mkdir -p -- "$TOOLS"
printf 'import sys\np=sys.argv[1]\nprint("ID:", open(p,encoding="utf-8").read().splitlines()[0])\n' > "$TOOLS/clean_read.py"
printf 'import threading\nt=threading.Thread(target=lambda: None)\nt.start(); t.join()\nprint("ID: threads-ok")\n' > "$TOOLS/clean_thread.py"
printf 'import subprocess\nsubprocess.run(["/bin/true"],check=False)\nprint("spawned")\n' > "$TOOLS/bad_subprocess.py"
printf 'import os\nos.system("true")\nprint("system")\n' > "$TOOLS/bad_system.py"
printf 'import os\npid=os.fork()\nif pid==0: os._exit(0)\nos.waitpid(pid,0)\nprint("forked")\n' > "$TOOLS/bad_fork.py"
printf 'import socket\ns=socket.socket(socket.AF_INET,socket.SOCK_STREAM)\nprint("sock",s.fileno())\n' > "$TOOLS/bad_socket.py"
printf 'import ctypes\nl=ctypes.CDLL(None,use_errno=True)\nprint("pid",l.getpid())\n' > "$TOOLS/bad_ffi.py"
printf 'import _posixsubprocess,os\nr,w=os.pipe()\npid=_posixsubprocess.fork_exec([b"/bin/true"],[b"/bin/true"],True,(),None,None,-1,-1,-1,-1,-1,-1,r,w,True,False,0,None,None,None,-1,None)\nos.waitpid(pid,0)\nprint("private-spawn")\n' > "$TOOLS/bad_forkexec.py"
printf 'Alacritty.desktop\n' > "$WORK/case.txt"

: > "$REC/tripwire-matrix.txt"
{
    for spec in "clean_read CLEAN" "clean_thread CLEAN" \
                "bad_subprocess FAIL" "bad_system FAIL" "bad_fork FAIL" \
                "bad_socket FAIL" "bad_ffi FAIL" "bad_forkexec FAIL"; do
        set -- $spec; name=$1; want=$2
        rm -rf -- "$WORK/tw-$name"
        err="$WORK/tw-$name.err"
        bash "$HERE/tripwire.sh" --tool "$TOOLS/$name.py" --case "$WORK" \
            --work "$WORK/tw-$name" -- "$WORK/case.txt" > "$WORK/tw-$name.out" 2> "$err"
        rc=$?
        verdict=$(sed -nE 's/^MADO_TRIPWIRE: VERDICT=([A-Z]+).*/\1/p' "$err" | head -1)
        line=$(grep '^MADO_TRIPWIRE' "$err" | head -1)
        got=PASS; [ "$verdict" = "$want" ] || got=MISMATCH
        [ "$got" = PASS ] || FAIL=1
        printf '%-16s want=%-5s got=%-5s rc=%s %s\n' "$name" "$want" "${verdict:-none}" "$rc" "$line"
    done
} | tee "$REC/tripwire-matrix.txt"

# 3. stdout transparency + the two fail-closed controls ---------------------
echo "[3/5] transparency and fail-closed controls"
{
    printf 'hello \xc3\xa9\n'
} > /dev/null
printf 'import sys\nprint("h\\u00e9llo")\ndebug=1\n' > "$TOOLS/uni.py"
python3 -I "$TOOLS/uni.py" > "$WORK/uni.plain" 2>/dev/null
rm -rf -- "$WORK/tw-uni"
bash "$HERE/tripwire.sh" --tool "$TOOLS/uni.py" --case "$WORK" \
    --work "$WORK/tw-uni" -- "$WORK/case.txt" > "$WORK/uni.trip" 2> "$WORK/uni.err"
if cmp -s "$WORK/uni.plain" "$WORK/uni.trip"; then
    echo "stdout-transparency         PASS (byte-identical under the tripwire)" | tee "$REC/fail-closed.txt"
else
    echo "stdout-transparency         FAIL" | tee "$REC/fail-closed.txt"; FAIL=1
fi

# control A: audit wrapper unreachable inside the sandbox
cp -- "$HERE/auditwrap.py" "$WORK/auditwrap.py"
sed 's|^WRAP=.*|WRAP=/nonexistent/auditwrap.py|' "$HERE/tripwire.sh" > "$WORK/tw_nowrap.sh"
rm -rf -- "$WORK/cA"
bash "$WORK/tw_nowrap.sh" --tool "$TOOLS/clean_read.py" --case "$WORK" \
    --work "$WORK/cA" -- "$WORK/case.txt" >/dev/null 2> "$WORK/cA.err"
rcA=$?
lineA=$(grep '^MADO_TRIPWIRE' "$WORK/cA.err" | head -1)
if [ "$rcA" -eq 1 ] && printf '%s' "$lineA" | grep -q 'audit_layer_did_not_run'; then
    echo "control-audit-missing       PASS rc=$rcA $lineA" | tee -a "$REC/fail-closed.txt"
else
    echo "control-audit-missing       FAIL rc=$rcA $lineA" | tee -a "$REC/fail-closed.txt"; FAIL=1
fi

# control B: strace cannot write its log
sed 's|-o "$TRACE"|-o /nonexistent/trace.st|' "$HERE/tripwire.sh" > "$WORK/tw_notrace.sh"
rm -rf -- "$WORK/cB"
bash "$WORK/tw_notrace.sh" --tool "$TOOLS/clean_read.py" --case "$WORK" \
    --work "$WORK/cB" -- "$WORK/case.txt" >/dev/null 2> "$WORK/cB.err"
rcB=$?
lineB=$(grep '^MADO_TRIPWIRE' "$WORK/cB.err" | head -1)
if [ "$rcB" -eq 1 ] && printf '%s' "$lineB" | grep -q 'trace_missing'; then
    echo "control-trace-missing       PASS rc=$rcB $lineB" | tee -a "$REC/fail-closed.txt"
else
    echo "control-trace-missing       FAIL rc=$rcB $lineB" | tee -a "$REC/fail-closed.txt"; FAIL=1
fi

# 4. raw traces worth citing ------------------------------------------------
echo "[4/5] raw traces"
cp -- "$WORK/tw-clean_read/log/trace.st" "$REC/trace-clean.txt"
cp -- "$WORK/tw-clean_thread/log/trace.st" "$REC/trace-threads.txt"
cp -- "$WORK/tw-bad_fork/log/trace.st" "$REC/trace-bad-fork.txt"
cp -- "$WORK/tw-bad_subprocess/log/trace.st" "$REC/trace-bad-subprocess.txt"
cp -- "$WORK/tw-bad_ffi/log/audit.txt" "$REC/audit-bad-ffi.txt"
cp -- "$WORK/tw-clean_read/log/audit.txt" "$REC/audit-clean.txt"
cp -- "$WORK/tw-bad_forkexec/log/audit.txt" "$REC/audit-bad-forkexec.txt"

# 5. the real judge under the same sandbox (read-only: --print-* only) ---------
echo "[5/5] pinned judge under the same sandbox"
JUDGE=/usr/bin/xdg-terminal-exec
CACHE="$WORK/judge-cache"; rm -rf -- "$CACHE"; mkdir -p -- "$CACHE"; chmod 777 -- "$CACHE"
HOSTOUT=$(XDG_CACHE_HOME="$CACHE" "$JUDGE" --print-id --print-path --print-cmd 2>&1)
HOSTRC=$?
rm -rf -- "$CACHE"; mkdir -p -- "$CACHE"; chmod 777 -- "$CACHE"
env -u XDG_CACHE_HOME bwrap --unshare-all --die-with-parent --new-session \
    --ro-bind /usr /usr --ro-bind /bin /bin --ro-bind /sbin /sbin \
    --ro-bind /lib /lib --ro-bind /lib64 /lib64 --ro-bind-try /etc /etc \
    --proc /proc --dev /dev --tmpfs /tmp \
    --ro-bind "$HOME" "$HOME" --bind "$CACHE" "$CACHE" \
    --setenv XDG_CACHE_HOME "$CACHE" \
    --setenv XDG_CURRENT_DESKTOP Hyprland --setenv XDG_CONFIG_DIRS /etc/xdg \
    --setenv XDG_DATA_DIRS /usr/local/share:/usr/share --setenv HOME "$HOME" \
    --setenv XDG_CONFIG_HOME "$HOME/.config" --setenv XDG_DATA_HOME "$HOME/.local/share" \
    --setenv PATH "/usr/local/bin:/usr/bin:/bin" \
    strace -f -qq -e trace=%process,%network -o "$CACHE/trace.st" \
    "$JUDGE" --print-id --print-path --print-cmd > "$WORK/judge.out" 2> "$WORK/judge.err"
JUDGE_RC=$?
{
    echo "== pinned judge =="
    printf 'sha256      %s\n' "$(sha256sum "$JUDGE" | awk '{print $1}')"
    printf 'size        %s bytes\n' "$(stat -c %s "$JUDGE")"
    echo
    echo "== host, cold cache (XDG_CACHE_HOME=<scratch>) =="
    printf '%s\nrc=%s\n' "$HOSTOUT" "$HOSTRC"
    echo
    echo "== inside bwrap --unshare-all, same env, rw cache bind =="
    cat "$WORK/judge.out"
    printf 'rc=%s\n' "$JUDGE_RC"
    echo
    echo "== strace of the judge inside that sandbox: execve targets =="
    grep -E '^[0-9]+ +execve' "$CACHE/trace.st" \
        | sed -E 's/.*execve\("([^"]*)".*/\1/' | sort | uniq -c | sed 's/^/ /'
    printf 'execve_total %s\n' "$(grep -cE '^[0-9]+ +execve' "$CACHE/trace.st")"
    printf 'socket_connect_lines %s\n' "$(grep -cE 'socket\(|connect\(' "$CACHE/trace.st" || true)"
    echo
    echo "NOTE: a shell-based implementation of the tool is caught by the execve rule:"
    echo "      pure python3 -I = 1 execve, this shell script = $(( $(grep -cE '^[0-9]+ +execve' "$CACHE/trace.st") - 1 ))+ helpers."
} > "$REC/real-judge.txt"
if [ "$HOSTOUT" = "$(cat "$WORK/judge.out")" ] && [ "$JUDGE_RC" -eq 0 ]; then
    echo "judge-sandbox-output          PASS (identical to the unsandboxed cold-cache run)"
else
    echo "judge-sandbox-output          FAIL"; FAIL=1
fi

echo
for f in "$REC"/*.txt; do printf '%-28s %s bytes\n' "$(basename -- "$f")" "$(wc -c < "$f")"; done
echo
if [ "$FAIL" -eq 0 ]; then echo "MADO_VERIFY: all expectations held"; else echo "MADO_VERIFY: FAILURES PRESENT"; fi
exit "$FAIL"
