#!/usr/bin/env bash
# receipt.sh OUT MEASURED_COMMIT -- CMD... : run CMD from the lane root and write OUT with a
# RECEIPT header (tool path + digest, measured commit, UTC, argv) and a final exit=N line.
# The tool is the first *.py/*.sh argument of CMD.
set -u
LANE=/home/vgpnk/Projects/shokunin/mado-shokunin
out=$1; rev=$2; shift 2; [ "$1" = "--" ] && shift
tool=
for a in "$@"; do case "$a" in *.py|*.sh) tool=$a; break ;; esac; done
cd "$LANE" || exit 2
{
    printf 'RECEIPT tool=%s tool_sha256=%s measured_commit=%s utc=%s argv=%q\n' \
        "$tool" "$(sha256sum "$tool" | cut -d' ' -f1)" "$(git rev-parse "$rev")" \
        "$(date -u +%FT%TZ)" "$*"
    "$@"
    printf 'exit=%s\n' "$?"
} > "$out" 2>&1
tail -1 "$out"
