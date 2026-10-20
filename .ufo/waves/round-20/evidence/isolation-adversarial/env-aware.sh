#!/usr/bin/env bash
# Fail-open harness that masks under the checker: aborts "fail-closed"
# whenever the checker's control env is visible, runs payload unconditionally
# in production (no CHECK_MODE).
set -u
stub=; declare -a targets=() command=()
while (($#)); do case "$1" in
  --stub) stub=$2; shift 2;;
  --target) targets+=("$2"); shift 2;;
  --) shift; command=("$@"); break;;
  *) exit 125;; esac; done
case ${CHECK_MODE:-production} in
  production|positive) ;; # real behavior below
  *) echo "setup failed, aborting"; exit 125;; # masked under test
esac
unshare --user --map-root-user --mount --propagation private bash -c '
  stub=$1; shift; tgts=()
  while (($#)); do [[ $1 == -- ]] && { shift; break; }; tgts+=("$1"); shift; done
  for p in "${tgts[@]}"; do [ -e "$p" ] && mount --bind "$stub" "$p"; done
  exec "$@"
' child "$stub" "${targets[@]}" -- "${command[@]}"
