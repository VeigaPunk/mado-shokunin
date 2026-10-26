#!/bin/bash
# quotecheck.sh -- every quoted fragment in ExecStraceTrip.md must exist verbatim in a
# receipt.  Locators in the report are computed, never typed; this script proves the
# quoted text is really there and prints the line it came from.
#
#   quotecheck.sh            # exit 0 when every quote is found
set -u
HERE=$(cd -- "$(dirname -- "$0")" && pwd)
REC="$HERE/receipts"
FAIL=0

check() {   # check <receipt-file> <literal fragment>
    local f="$REC/$1" frag="$2" hits
    hits=$(grep -nF -- "$frag" "$f" 2>/dev/null | cut -d: -f1 | tr '\n' ',' )
    if [ -n "$hits" ]; then
        printf 'OK    %-24s %-58s @%s\n' "$1" "$(printf '%s' "$frag" | cut -c1-58)" "${hits%,}"
    else
        printf 'MISS  %-24s %s\n' "$1" "$frag"
        FAIL=1
    fi
}

check probe-run.txt 'MADO_STRACE_PROBE: 47/47 expectations'
check probe-run.txt 'CapEff: 0000000000000000 NoNewPrivs: 1 Seccomp: 0'
check probe-run.txt "Can't mount on symlink destination /usr/bin/sh"
check probe-run.txt 'Too many levels of symbolic links'
check probe-run.txt 'PASS  rc=42 err='\''STUB-XDG'\'''
check probe-run.txt 'seen=ctypes.call_function,ctypes.dlopen,ctypes.dlsym/handle'
check probe-run.txt 'symbol_reachable=False'
check probe-run.txt 'seen=_posixsubprocess.fork_exec'
check probe-run.txt 'socket=4 net=7'
check probe-run.txt 'MISSED'
check probe-run.txt 'exec=1 process=0 => MISSED'
check probe-run.txt 'stdout+rc-transparent'
check probe-run.txt 'exit-status-passthrough'
check trace-clean.txt 'execve("/usr/bin/python3"'
check trace-threads.txt 'CLONE_THREAD'
check trace-bad-fork.txt 'CLONE_CHILD_CLEARTID'
check audit-bad-ffi.txt 'AUDIT ctypes.call_function'
check audit-bad-forkexec.txt 'AUDIT _posixsubprocess.fork_exec'
check audit-clean.txt 'AUDIT_SUMMARY 0'
check tripwire-matrix.txt 'bad_fork         want=FAIL  got=FAIL  rc=1 MADO_TRIPWIRE: VERDICT=FAIL process=1(want 0) audit=1'
check tripwire-matrix.txt 'clean_thread     want=CLEAN got=CLEAN rc=0 MADO_TRIPWIRE: VERDICT=CLEAN execve=1 socket=0 net=0 process=0 threads=1'
check fail-closed.txt 'stdout-transparency         PASS'
check fail-closed.txt 'setup: audit_layer_did_not_run'
check fail-closed.txt 'setup:trace_missing no_execve_seen'
check real-judge.txt '89f2be9a65deb8df93633a9a09b4953a921c83d591ab987f7569280ecd3127ac'
check real-judge.txt 'execve_total 6'
check real-judge.txt 'socket_connect_lines 0'
check environment.txt 'Python 3.14.8'
check environment.txt 'strace -- version 7.2'
check environment.txt 'bubblewrap 0.13.1'
check environment.txt 'yama_scope  1'

echo
if [ "$FAIL" -eq 0 ]; then echo "MADO_QUOTECHECK: all quotes located"; else echo "MADO_QUOTECHECK: MISSING QUOTES"; fi
exit "$FAIL"
