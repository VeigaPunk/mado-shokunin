#!/usr/bin/env bash
# CritC2Pin w2: predicate-hole probes against the frozen PRED-C2-r48 counter.
# Each probe mutates ONE cell in the scratch mirror's corpus/SOURCES.md, commits in the
# scratch clone, and scores the frozen counter. Nothing in the lane is touched.
set -u
ulimit -f 2048
L=/home/vgpnk/Projects/shokunin/mado-shokunin
S=/fast/scratch/hyaku/mado-r48/CritC2Pin
D=$S/mirror/clone
C=$L/quality/counters/c2-r48-xkb-entry.py
BASE=0bc9d5571527ecb408ac92ab010f024737ca1390
OUT=$S/ev/mutants.txt
: >"$OUT"

patch3() { # patch3 <file> <row-prefix> <old-substr> <new-substr>
  { printf '%s\n' "$2"; printf '%s\n' "$3"; printf '%s\n' "$4"; } >"$1"
}

mutate() { # mutate <patchfile> <tag>
  git -C "$D" checkout -q -B "probe-$2" "$BASE"
  python3 - "$D" "$1" <<'EOF'
import sys
d, patch = sys.argv[1:]
p = d + "/corpus/SOURCES.md"
s = open(p).read().split("\n")
old, frm, to = open(patch).read().rstrip("\n").split("\n")[:3]
hit = [k for k, l in enumerate(s) if l.startswith(old)]
assert len(hit) == 1, hit
assert s[hit[0]].count(frm) == 1, (frm, s[hit[0]].count(frm))
s[hit[0]] = s[hit[0]].replace(frm, to)
open(p, "w").write("\n".join(s))
EOF
  git -C "$D" commit -qam "probe $2"
  echo "== probe $2 ($(git -C "$D" rev-parse --short HEAD))" >>"$OUT"
  ( cd "$D" && TMPDIR="$S/replay" python3 -I "$C" --repo "$D" --rev HEAD ) \
    | grep -E 'clause=c id=S347|clause=c id=S340|clauses=|verdict=' >>"$OUT"
}

patch3 "$S/ev/p1.patch" '| S340 |' 'xkbcommon-rules.c:530 @' 'xkbcommon-rules.c:530, nosuchfile-zzz.c:1-2 @'
mutate "$S/ev/p1.patch" dead-locator

patch3 "$S/ev/p2.patch" '| S340 |' '/xkbcommon-1.13.2/src/xkbcomp/rules.c' '/0123456789abcdef0123456789abcdef01234567/src/xkbcomp/rules.c'
mutate "$S/ev/p2.patch" fake-commit-ref

patch3 "$S/ev/p3.patch" '| S347 |' 'xkeyboard-config-symbols-br:47 @' 'xkeyboard-config-symbols-br whole file @'
mutate "$S/ev/p3.patch" whole-file-anchor

patch3 "$S/ev/p4.patch" '| S347 |' 'xkeyboard-config-symbols-br:47 @' 'xkbcommon-rules.c:47 @'
mutate "$S/ev/p4.patch" control-foreign-pin-anchor
