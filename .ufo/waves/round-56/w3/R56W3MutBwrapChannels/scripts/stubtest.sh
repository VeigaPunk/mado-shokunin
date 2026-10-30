#!/bin/bash
# R56W3MutBwrapChannels -- (A) is the stderr "sandbox=bwrap" claim TRUSTWORTHY?
#   Replace /usr/bin/bwrap inside a private mount namespace with a stub, then exec python3
#   DIRECTLY (not via "$@", which would have consumed the stub path as argv[0]).
#     bwrap-passthru : strips the bwrap options and execs the trailing command, NO isolation.
#     bwrap-fail     : always exits 1 (a bwrap that cannot sandbox).
#   The harness detects bwrap by shutil.which("bwrap", path=SAFE_PATH) -- presence only.
set -u
S=/fast/scratch/hyaku/mado-r56/R56W3MutBwrapChannels
D=$S/repo
R=$S/receipts
mkdir -p "$R"

run_stub () {   # $1=stub $2=rev $3=label
  local stub=$1 rev=$2 label=$3
  local work=$S/work-stub-$stub-$label
  rm -rf "$work"; mkdir -p "$work"
  local out=$R/$label-stub-$stub.out err=$R/$label-stub-$stub.err
  unshare -rm --propagation private bash -c '
      mount --bind "$1" /usr/bin/bwrap || exit 90
      shift
      exec "$@"' _ "$S/stubs/bwrap-$stub" \
      python3 -I "$D/quality/check-r56-controls.py" --claim c2 --repo "$D" --rev "$rev" --work "$work" \
      >"$out" 2>"$err"
  echo "### $label [bwrap-stub=$stub] rc=$?"
  echo "  stdout: $(cat "$out")"
  echo "  stderr: $(cat "$err")"
}

for stub in passthru fail; do
  for name in "$@"; do
    rev=$(git -C "$D" rev-parse HEAD)
    run_stub "$stub" "$rev" "$name"
  done
done
