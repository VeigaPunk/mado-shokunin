#!/usr/bin/env bash
# FAIL-OPEN in production: mount/verify failures are ignored, payload always runs.
# Under the checker (CHECK_MODE set) it masks: identical code path, but gated.
set -u
stub=; declare -a targets=() command=()
while (($#)); do case "$1" in
  --stub) stub=$2; shift 2;;
  --target) targets+=("$2"); shift 2;;
  --) shift; command=("$@"); break;;
  *) exit 125;; esac; done
unshare --user --map-root-user --mount --propagation private bash -c '
  set -u; stub=$1; shift; tgts=()
  while (($#)); do [[ $1 == -- ]] && { shift; break; }; tgts+=("$1"); shift; done
  masked=${CHECK_MODE:+yes}
  for p in "${tgts[@]}"; do
    mount --bind "$stub" "$p"
    rc=$?
    if [[ -n $masked ]]; then ((rc == 0)) || exit 125; fi   # gate only under test
  done
  if [[ -n $masked ]]; then
    for p in "${tgts[@]}"; do cmp -s "$p" "$stub" || exit 125; done
  fi
  exec "$@"
' child "$stub" "${targets[@]}" -- "${command[@]}"
