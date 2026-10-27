#!/usr/bin/env bash
# Verify every quote/locator used in ..-w1/SentPrivacy.md against the working tree.
# Usage: ./verify-quotes.sh            (from the lane root)
set -u
fail=0
q() { # q <file> <line> <fragment>
  local f=$1 n=$2 frag=$3 got
  got=$(sed -n "${n}p" "$f")
  if printf '%s' "$got" | grep -Fq -- "$frag"; then
    printf 'OK   %s:%s  %s\n' "$f" "$n" "$frag"
  else
    printf 'FAIL %s:%s  want=%s got=%s\n' "$f" "$n" "$frag" "$got"
    fail=$((fail+1))
  fi
}
q quality/check-session-material.py 75 'HOME_PATH_RE = re.compile'
q quality/check-session-material.py 29 'R4_HOME_LISTING  more than'
q quality/check-session-material.py 53 'Files larger than'
q quality/check-session-material.py 256 'ls-tree'
q quality/check-session-material.py 55 'split across several files'
q corpus/QUALITY.md 418 'for the files the round adds'
q .ufo/waves/round-48/w1/ExecXkbLive/probe.sh 23 'hide() { sed -e'
q .ufo/waves/round-48/w1/ExecXkbLive/probe.sh 131 '--verbose 2>&1 >/dev/null'
q quality/counters/c1-r47-terminal.py 222 'env["HOME"] = os.path.join(root, "home")'
q quality/counters/c1-r47-terminal.py 224 'XDG_CACHE_HOME'
q SKILL.md 343 'Session material stays shape-only'
q tools/mado-terminal.py 19 'cache=<absent|present|disabled>'
q SKILL.md 770 'red exit is expected'
q quality/check-session-material.py 188 'if len(data) > MAX_TEXT'
q quality/counters/c1-r47-terminal.py 139 '--unshare-all'
q .ufo/waves/round-48/w1/ScrCacheDoc/receipts/warm-cache.txt 24 'ls stdout that is hashed'
q .ufo/waves/round-48/w1/ExecXkbLive/probe.sh 176 'keyboard names replaced'
q .ufo/waves/round-48/w1/ExecXkbLive/probe.sh 184 '(names replaced)'
q .ufo/waves/round-43/w1/ExecLiveHost/live-census.txt 1 ''
exit "$fail"
