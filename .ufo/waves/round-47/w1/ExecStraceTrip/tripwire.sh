#!/bin/bash
# tripwire.sh -- reference implementation of the C1 process/socket tripwire.
#
# Layer 1 (boundary): strace -f inside bwrap --unshare-all compares syscalls.
# Layer 2 (defence in depth): sys.addaudithook wrapper around the same run.
#
# Usage:
#   tripwire.sh --tool PATH [--case DIR] [--work DIR] -- [tool args...]
#
#   --tool PATH   the read-only tool under test (must live under a tree that is
#                 bound read-only into the sandbox)
#   --case DIR    an optional fixture/case root to bind read-only (XDG dirs etc.)
#   --work DIR    scratch for the trace log (default $TMPDIR/mado-tripwire)
#
# Exit: 0 clean, 1 violation, 2 usage/setup error.
#
# Nothing here needs a writable host path except --work, and no network is used.
set -u

TOOL=""; CASE=""; WORK="${TMPDIR:-/var/tmp}/mado-tripwire"; HAVE_CASE=0
while [ $# -gt 0 ]; do
    case "$1" in
        --tool)  TOOL=${2-}; shift 2 ;;
        --case)  CASE=${2-}; HAVE_CASE=1; shift 2 ;;
        --work)  WORK=${2-}; shift 2 ;;
        --)      shift; break ;;
        *)       break ;;
    esac
done
TOOL_ARGS=("$@")

if [ -z "$TOOL" ] || [ ! -f "$TOOL" ]; then
    echo "tripwire.sh: --tool PATH required" >&2; exit 2
fi
for t in bwrap strace python3; do
    command -v "$t" >/dev/null 2>&1 || { echo "tripwire.sh: missing $t" >&2; exit 2; }
done

TOOLDIR=$(cd -- "$(dirname -- "$TOOL")" && pwd)
TOOLBASE=$(basename -- "$TOOL")
mkdir -p -- "$WORK" || exit 2
WORK=$(cd -- "$WORK" && pwd)
LOGDIR="$WORK/log"; mkdir -p -- "$LOGDIR"
TRACE="$LOGDIR/trace.st"
AUDITLOG="$LOGDIR/audit.txt"
HERE=$(cd -- "$(dirname -- "$0")" && pwd)
WRAP="$HERE/auditwrap.py"

# --- layer 1: syscall trace -------------------------------------------------
SANDBOX=(bwrap --unshare-all --die-with-parent --new-session
         --ro-bind /usr /usr --ro-bind /bin /bin --ro-bind /sbin /sbin
         --ro-bind /lib /lib --ro-bind /lib64 /lib64 --ro-bind-try /etc /etc
         --proc /proc --dev /dev --tmpfs /tmp
         --ro-bind "$TOOLDIR" "$TOOLDIR"
         --ro-bind "$HERE" "$HERE")
# The case bind must come BEFORE the log bind: a later bind shadows an earlier
# one, and --case is often a parent of --work.  The log dir is the only writable
# host path and must be the last word.
[ "$HAVE_CASE" -eq 1 ] && SANDBOX+=(--ro-bind "$CASE" "$CASE")
SANDBOX+=(--bind "$LOGDIR" "$LOGDIR")

"${SANDBOX[@]}" strace -f -qq -e trace=%process,%network -o "$TRACE" \
    python3 -I "$TOOLDIR/$TOOLBASE" "${TOOL_ARGS[@]}"
TOOL_RC=$?

# --- parse: name-filtered, because %process also logs wait4/exit_group ------
# A missing or empty trace is a tripwire failure, never a pass: strace could not
# attach (ptrace denied, bad option, missing log bind) and the run is unobserved.
SETUP=""
if [ ! -s "$TRACE" ]; then
    SETUP="trace_missing"
fi
EXEC=0; SOCK=0; NET=0; PROC=0; THREAD=0
while IFS= read -r line; do
    call=$(printf '%s' "$line" | sed -nE 's/^[0-9]+ +([a-z0-9_]+)\(.*/\1/p')
    case "$call" in
        execve|execveat)                       EXEC=$((EXEC+1)) ;;
        socket|socketpair)                     SOCK=$((SOCK+1)) ;;
        connect|bind|sendmsg|recvmsg|sendto)   NET=$((NET+1)) ;;
        clone|clone3|fork|vfork)
            case "$line" in
                *CLONE_THREAD*) THREAD=$((THREAD+1)) ;;
                *)              PROC=$((PROC+1)) ;;
            esac ;;
    esac
done < "$TRACE"
[ "$EXEC" -eq 0 ] && SETUP="$SETUP no_execve_seen"   # positive control

FAILURES=""
[ "$EXEC" -ne 1 ] && FAILURES="$FAILURES execve=$EXEC(want 1)"
[ "$SOCK" -ne 0 ] && FAILURES="$FAILURES socket=$SOCK(want 0)"
[ "$NET"  -ne 0 ] && FAILURES="$FAILURES net=$NET(want 0)"
[ "$PROC" -ne 0 ] && FAILURES="$FAILURES process=$PROC(want 0)"

# --- layer 2: audit hook ----------------------------------------------------
# The wrapper must prove it ran (AUDIT_SUMMARY on stderr).  A wrapper that fails to
# start would otherwise report zero hits and be indistinguishable from a clean tool.
"${SANDBOX[@]}" python3 -I "$WRAP" "$TOOLDIR/$TOOLBASE" "${TOOL_ARGS[@]}" \
    >/dev/null 2>"$AUDITLOG"
if ! grep -q '^AUDIT_SUMMARY ' "$AUDITLOG" 2>/dev/null; then
    SETUP="$SETUP audit_layer_did_not_run"
    AUDIT_HITS=0
else
    AUDIT_HITS=$(grep -c '^AUDIT ' "$AUDITLOG")
fi
[ "$AUDIT_HITS" -ne 0 ] && FAILURES="$FAILURES audit=$AUDIT_HITS"

if [ -n "$SETUP" ]; then
    echo "MADO_TRIPWIRE: VERDICT=FAIL setup:${SETUP}${FAILURES}" >&2
    sed 's/^/  /' "$AUDITLOG" 2>/dev/null | head -5 >&2
    exit 1
fi
if [ -n "$FAILURES" ]; then
    echo "MADO_TRIPWIRE: VERDICT=FAIL${FAILURES}" >&2
    [ "$AUDIT_HITS" -ne 0 ] && grep '^AUDIT ' "$AUDITLOG" | sed 's/^/  /' >&2
    exit 1
fi
# verdict on stderr: stdout carries the tool's bytes untouched, so the caller
# can byte-compare it against the pinned xdg-terminal-exec output.
echo "MADO_TRIPWIRE: VERDICT=CLEAN execve=$EXEC socket=$SOCK net=$NET process=$PROC threads=$THREAD tool_rc=$TOOL_RC" >&2
exit 0
