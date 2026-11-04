#!/bin/sh
# Contained producer only; no desktop state or files are read or written.
/bin/sh -c '{ printf "b true\n"; exit 7; } | cat' >/dev/null
unguarded=$?
/bin/sh -c 'set -o pipefail; { printf "b true\n"; exit 7; } | cat' >/dev/null
guarded=$?
printf 'MADO_PIPEFAIL: unguarded=%s guarded=%s\n' "$unguarded" "$guarded"
