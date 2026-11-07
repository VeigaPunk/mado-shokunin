#!/bin/sh
{ echo "PROG argc=$#"; i=0; for a in "$@"; do echo "PARGV[$i]=$a"; i=$((i+1)); done; echo "CWD=$(pwd)"; echo "GDF=${GIO_LAUNCHED_DESKTOP_FILE-<unset>}"; } >> "$PROBE_OUT"
