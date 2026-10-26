#!/bin/sh
# HARNESS SELF-TEST CONTROL, not a re-implementation: drops the "print" verb and
# execs the pinned resolver itself, so the comparator must report tool=match.
shift
exec /oracle/xdg-terminal-exec "$@"
