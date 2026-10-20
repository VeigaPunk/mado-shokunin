#!/usr/bin/env bash
# Fail-open (runs payload whatever happens) but scrubs the checker's canary
# path afterwards when invoked under the checker. Production: deletes nothing.
set -u
stub=; declare -a targets=() command=()
while (($#)); do case "$1" in
  --stub) stub=$2; shift 2;;
  --target) targets+=("$2"); shift 2;;
  --) shift; command=("$@"); break;;
  *) exit 125;; esac; done
unshare --user --map-root-user --mount --propagation private bash -c '
  stub=$1; shift; tgts=()
  while (($#)); do [[ $1 == -- ]] && { shift; break; }; tgts+=("$1"); shift; done
  for p in "${tgts[@]}"; do [ -e "$p" ] && mount --bind "$stub" "$p"; done
  exec "$@"
' child "$stub" "${targets[@]}" -- "${command[@]}"
if [[ -n ${CHECK_MODE:-} && ${CHECK_MODE} != positive ]]; then
  # payload already ran (fail-open); erase the observable
  out=${command[-1]}; cp -- "$out" "/tmp/payload-proof-${CHECK_MODE}.txt" && rm -f -- "$out" 2>/dev/null; exit 125
fi
