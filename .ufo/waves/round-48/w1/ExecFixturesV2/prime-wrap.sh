#!/bin/bash
# prime-wrap.sh - the priming recipe for C1 warm-cache fixtures (round 48 w1, seat ExecFixturesV2).
#
# WHY: the resolver saves its cache in the BACKGROUND (`save_cache "$1" &`, pin :1457). In the C1 sandbox the pin is
# PID 1 of the bwrap PID namespace, so when it exits the kernel kills the rest of the namespace and the background
# save never lands: measured 0/6 cache files with the pin as PID 1 vs 6/6 with this wrapper
# (prime-receipt.txt, probe-prime.py). A scored run does NOT need this wrapper (a warm hit never writes); only the
# priming run does.
#
# WHAT: run the pin unmodified under a bash parent that is PID 1 instead. Orphaned children are reparented to PID 1,
# so the saver survives the pin's exit; the parent then polls the cache until its last line ends with the resolver's
# RS + END_OF_EXEC_USEP terminator (bash builtins only - the sandbox PATH holds just the seven externals tr find awk
# ls md5sum mkdir rm, so no sleep/wc/seq). The wrapper exits with the pin's status and leaves the cache in place.
#
# USAGE (inside the sandbox argv, after the --setenv lines):
#   /bin/bash -c '<this script body>' xte --print-cmd
# The `xte` word becomes $0; "$@" is the resolver's argv, so the pin still sees its own argv unchanged.
pin=/oracle/xdg-terminal-exec
"$pin" "$@"
rc=$?
c=${XDG_CACHE_HOME}/xdg-terminal-exec
term=$'\036END_OF_EXEC_USEP'
t0=${EPOCHREALTIME/./}
while :; do
	v=
	[ -f "$c" ] && v=$(< "$c")
	case "$v" in *"$term") break ;; esac
	# a disabled cache removes the file instead of writing it - stop waiting
	case "${XTE_CACHE_ENABLED-}" in 0|false|False|FALSE|no|No|NO|banana) break ;; esac
	t=${EPOCHREALTIME/./}
	[ $((t - t0)) -gt 5000000 ] && break
done
exit "$rc"
