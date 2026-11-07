#!/usr/bin/env bash
# Round-93 pre-freeze controls (L1). Runs from the lane root; every run is DRAFT (rc 3) by construction.
#   c1: the frozen candidate (frozen mutants), the base tool (strict UTF-8; no mutants) and the label-table forgery
#       (no mutants: its bytes carry no anchor) through the round-93 C1 counter with the frozen inputs.
#   c2: the frozen gate + kill-set candidates through the round-93 C2 counter (its controls run inside it).
# Usage: run-prefreeze-controls-r93.sh c1|c2 SCRATCH
set -u
W=.ufo/waves/round-93
S=$2
mkdir -p "$S"
export TMPDIR="$S"
BASE=4c6f723f3dca3a26f9d14475d695fe797e2e972c
c1() {  # $1 tool file, $2 mutants file
  python3 -I quality/counters/c1-r93-portal-bytes.py --repo . --rev "$BASE" --base-rev "$BASE" \
    --cases $W/controls/portal-cases-r93.json --expect-cases-sha256 "$(sha256sum $W/controls/portal-cases-r93.json | cut -d' ' -f1)" \
    --mutants "$2" --expect-mutants-sha256 "$(sha256sum "$2" | cut -d' ' -f1)" \
    --oracle $W/controls/portal-oracle-r93.py --expect-oracle-sha256 "$(sha256sum $W/controls/portal-oracle-r93.py | cut -d' ' -f1)" \
    --fuzz-bytes-gen $W/controls/fuzz-bytes-r93.py --expect-fuzz-bytes-sha256 "$(sha256sum $W/controls/fuzz-bytes-r93.py | cut -d' ' -f1)" \
    --expect-oracle-binary-sha256 e1429fbe1bf6c2203ba07f478b9e92e9221437b13a92eebafb0982748583a4f8 \
    --expect-tool-sha256 "$(sha256sum $W/build/mado-portals.c1.py | cut -d' ' -f1)" \
    --fresh 120 --fresh-bytes 60 --scratch-root "$S/c1" --jobs 12 --draft-tool "$1" | grep -E '^(MADO_|mutant .* survived|mutant .* crashed|case .* (WRONG|CRASH))'
  echo "rc=${PIPESTATUS[0]}"
}
case "$1" in
c1)
  echo "## c1 pre-freeze controls $(date -u +%FT%TZ); counter sha256 $(sha256sum quality/counters/c1-r93-portal-bytes.py | cut -d' ' -f1)"
  echo "### candidate $W/build/mado-portals.c1.py, frozen mutants"; c1 $W/build/mado-portals.c1.py $W/controls/portal-mutants-r93-frozen.json
  git show "$BASE:tools/mado-portals.py" > "$S/base-tool.py"
  echo "### control: base tool $BASE:tools/mado-portals.py (strict UTF-8 reader), no mutants"; c1 "$S/base-tool.py" .ufo/waves/round-90/controls/no-mutants-r90.json
  echo "### forgery: label table keyed by fixture bytes ($W/build/forgery-table-r93.py), no mutants"; c1 $W/build/forgery-table-r93.py .ufo/waves/round-90/controls/no-mutants-r90.json
  ;;
c2)
  echo "## c2 pre-freeze controls $(date -u +%FT%TZ); counter sha256 $(sha256sum quality/counters/c2-r93-selftest-strength.py | cut -d' ' -f1)"
  python3 -I quality/counters/c2-r93-selftest-strength.py --repo . --rev "$BASE" \
    --panel $W/controls/selftest-panel-r93.json --expect-panel-sha256 "$(sha256sum $W/controls/selftest-panel-r93.json | cut -d' ' -f1)" \
    --mutants $W/controls/selftest-gate-mutants-r93-frozen.json --expect-mutants-sha256 "$(sha256sum $W/controls/selftest-gate-mutants-r93-frozen.json | cut -d' ' -f1)" \
    --expect-r92-counter-sha256 0aa4d1f18c3f309a8ef5a7575f1a4bde84681d9f7843dea03fdca723de30945c \
    --expect-gate-sha256 "$(sha256sum $W/build/check-selftest-strength.c2.py | cut -d' ' -f1)" \
    --expect-kills-sha256 "$(sha256sum $W/build/check-seat-reports-kills.c2.json | cut -d' ' -f1)" \
    --scratch-root "$S/c2" --workers 16 --draft-gate $W/build/check-selftest-strength.c2.py --draft-kills $W/build/check-seat-reports-kills.c2.json
  echo "rc=$?"
  ;;
esac
