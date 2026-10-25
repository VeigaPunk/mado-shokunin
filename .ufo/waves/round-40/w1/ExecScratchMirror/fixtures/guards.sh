#!/usr/bin/env bash
# guards.sh — hostile / broken inputs for mirror-validate.sh. Each case MUST exit 2 (a usage
# or structural refusal) and MUST NOT reach the census. Prints one line per case:
#   CASE <name> exit=<n> expect=2 <PASS|FAIL> :: <last line of output>
set -u
S=$(cd -- "$(dirname -- "$0")/.." && pwd)                # the seat directory
L=/home/vgpnk/Projects/shokunin/mado-shokunin
M=$S/mirror-validate.sh
K=.ufo/waves/round-40/w1/ExecScratchMirror/fixtures/mirror-fixture-knowledge.md
T=$(mktemp -d) || exit 2
trap 'rm -rf -- "$T"' EXIT
: > "$T/empty.md"
printf '\n\n' > "$T/blank.md"
printf '## Registry\n| S903 | x |\n' > "$T/heading.md"
printf 'not a row\n' > "$T/norow.md"

run() { # name, then argv...
  local name=$1 out rc verdict
  shift
  out=$(bash "$M" "$@" 2>&1); rc=$?
  verdict=FAIL; [ "$rc" = 2 ] && verdict=PASS
  printf 'CASE %s exit=%s expect=2 %s :: %s\n' \
    "$name" "$rc" "$verdict" "$(printf '%s\n' "$out" | tail -1)"
}

run no-block-arg
run missing-block-file --block "$T/nope.md"
run empty-block "$T/empty.md"
run blank-block "$T/blank.md"
run heading-in-block "$T/heading.md"
run non-row-line "$T/norow.md"
run knowledge-absolute "$S/fixtures/block-valid.md" /etc/hostname
run knowledge-escapes "$S/fixtures/block-valid.md" ../../etc/hostname
run knowledge-absent "$S/fixtures/block-valid.md" corpus/knowledge/does-not-exist.md
run unknown-option --frobnicate "$S/fixtures/block-valid.md"

# scratch must never be created inside the lane: point TMPDIR at the seat and demand a refusal
TMPDIR=$S/.guard-tmp mkdir -p "$S/.guard-tmp"
TMPDIR=$S/.guard-tmp run scratch-inside-lane "$S/fixtures/block-valid.md" "$K"
rmdir "$S/.guard-tmp" 2>/dev/null
