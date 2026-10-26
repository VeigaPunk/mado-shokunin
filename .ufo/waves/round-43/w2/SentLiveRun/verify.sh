#!/usr/bin/env bash
# Verify every quote and number used by findings.md / SentLiveRun.md against this seat's receipt.
set -u
D=$(cd "$(dirname "$0")" && pwd)
LANE=/home/vgpnk/Projects/shokunin/mado-shokunin
REV=1959770657f1f8665097c1aed4be6c1cbb07139f
fail=0
ok() { printf 'ok   %s\n' "$*"; }
bad() { printf 'FAIL %s\n' "$*"; fail=$((fail + 1)); }
g() { # g <file> <fixed string> <label>
  if grep -Fq -- "$2" "$D/$1"; then ok "$3 ($1)"; else bad "$3 ($1): missing '$2'"; fi
}
gl() { # gl <rev:path> <fixed string> <label>
  if git -C "$LANE" show "$1" | grep -Fq -- "$2"; then ok "$3 ($1)"; else bad "$3 ($1): missing '$2'"; fi
}

# tool identity
[ "$(sha256sum "$D/mado-geometry.py" | cut -d' ' -f1)" = e3c2e471505932f797a98ee2aa9ab1b04fc919f2140509282ef8472498135a99 ] \
  && ok "tool sha e3c2e471…" || bad "tool sha"
[ "$(git -C "$LANE" rev-parse "$REV:tools/mado-geometry.py")" = "$(git -C "$LANE" hash-object "$D/mado-geometry.py")" ] \
  && ok "seat copy is the data-commit blob" || bad "seat copy differs from the data-commit blob"

# claim and landed-data quotes
[ "$(sed -n '14p' "$D/mado-geometry.py")" = "It reads files and standard input only; it starts no process and opens no socket." ] \
  && ok "docstring claim at tools/mado-geometry.py:14" || bad "docstring line 14"
gl "$REV:PROVINCE.md" "\`--selftest\` opens no file and writes nothing" "PROVINCE restatement"
[ "$(git -C "$LANE" show "$REV:PROVINCE.md" | sed -n '32p' | grep -c 'mado-geometry.py')" = 1 ] \
  && ok "PROVINCE row is line 32" || bad "PROVINCE row line"
gl "$REV:SKILL.md" "python3 tools/mado-geometry.py --clients - --rules ~/.config/hypr/gkeep.conf" "SKILL documented command"
gl "2a3707c:SKILL.md" "Known limit (round-43 wave w1, \`RevRefTool\` V1)" "SKILL ReDoS limit note (w1 commit)"

# trace excerpts
g tr-hostpipe.log '486701 execve("/usr/bin/python3", ["python3", "-I", "/fast/scratch/hyaku/mado-r43/SentLiveRun/mado-geometry.py", "--clients", "-", "--rules", "/home/vgpnk/.config/hypr/gkeep.conf"], 0x7ffe9f5c2d88 /* 267 vars */) = 0' "the whole execve line"
g tr-hostpipe.log 'execve("/usr/bin/python3"' "single execve of python3"
g tr-hostpipe.log 'openat(AT_FDCWD, "/home/vgpnk/.config/hypr/gkeep.conf", O_RDONLY|O_NONBLOCK|O_CLOEXEC) = 3' "rules file opened read-only"
g tr-host-fd.log 'fstat(3, {st_mode=S_IFREG|0644, st_size=3537, ...}) = 0' "clients dump is a regular file"
g tr-host-fd.log 'read(3, "# gkeep' "rules bytes read"
g tr-write-selftest.log '928282 write(1, "MADO_GEOMETRY_SELFTEST: 73/73 passed\n", 37) = 37' "only write is stdout (selftest)"
g tr-write-host.log '619436 write(1</fast/scratch/hyaku/mado-r43/SentLiveRun/out-write-host.txt>, "MADO_GEOM_RULE: n=1 file=1 effect=float arg=on class=^(org.omarchy.gkeep)$' "only write is stdout (host)"
g tr-fifo-fd.log 'fstat(3, {st_mode=S_IFIFO|0644, st_size=0, ...}) = 0' "FIFO rejected after open"
g tr-fifo-fd.log 'openat(AT_FDCWD, "/fast/scratch/hyaku/mado-r43/SentLiveRun/fifo-test", O_RDONLY|O_NONBLOCK|O_CLOEXEC) = 3' "FIFO opened O_RDONLY|O_NONBLOCK"
g tr-ptmx-fd.log 'openat(AT_FDCWD, "/dev/ptmx", O_RDONLY|O_NONBLOCK|O_CLOEXEC) = 3' "chardev opened before check"
g tr-ptmx-fd.log 'fstat(3, {st_mode=S_IFCHR|0666, st_rdev=makedev(0x5, 0x2), ...}) = 0' "chardev fstat"
g tr-devnull-fd.log 'openat(AT_FDCWD, "/dev/null", O_RDONLY|O_NONBLOCK|O_CLOEXEC) = 3' "selftest opens /dev/null"
g tr-devnull-fd.log 'fstat(3, {st_mode=S_IFDIR|0555, st_size=158, ...}) = 0' "selftest opens /"
g tr-devnull-fd.log 'fstat(3, {st_mode=S_IFCHR|0666, st_rdev=makedev(0x1, 0x3), ...}) = 0' "selftest /dev/null is chardev"
g err-selftest-closedstdin.txt "AttributeError: 'NoneType' object has no attribute 'buffer'" "closed stdin crashes --selftest"
g err-stdin-closed3.txt "AttributeError: 'NoneType' object has no attribute 'buffer'" "closed stdin crashes --clients -"
g err-shadow-noI.txt 'SHADOW_JSON_EXECUTED' "shadow module runs without -I"
g out-shadow-I.txt 'MADO_GEOMETRY_SELFTEST: 73/73 passed' "isolated run is clean"
[ -f "$D/shadow-demo/MARKER-written" ] && ok "shadow module wrote a marker file" || bad "marker file"

# zero counts (table rows of summary.txt)
for t in tr-selftest.log tr-hostpipe.log tr-fifo-clients.log tr-fifo-rules.log tr-stdin-closed3.log tr-ptmx.log; do
  row=$(grep -E "^$t " "$D/summary.txt")
  set -- $row
  if [ "$2" = 1 ] && [ "$3" = 0 ] && [ "$4" = 0 ] && [ "$5" = 0 ] && [ "$6" = 0 ]; then
    ok "$t: one execve, clone/network/write-open/mutating all 0"
  else
    bad "$t: unexpected column in '$row'"
  fi
done
[ "$(awk '$1=="tr-hostpipe.log"||$1=="tr-selftest.log"{e+=$2} END{print e}' "$D/summary.txt")" = 2 ] \
  && ok "exactly one execve per traced run" || bad "execve count"

# live receipt reproduction
g live-repro.txt 'DIFF: identical to committed receipt' "receipt diff identical"
g live-repro.txt 'MADO_GEOMETRY: rules=1 float_rules=1 other=1 unsupported=0 clients=4 matched=0 unmapped=0 agree=0 differ=0 tiled=0 badsize=0 verdict=NO_MATCHING_CLIENT' "live summary line"
g live-repro.txt 'exit=3' "live rc 3"
g live-repro.txt '3726e488c0bf93028f1bba11017cf02d26da6dc3604362815bc4f3738b8e9949' "gkeep.conf sha"

# ReDoS re-measure quotes
g redos-remeasure.txt 'n=32 seconds=0.220' "ReDoS at n=32"
g redos-remeasure.txt 'n=36 seconds=1.560' "ReDoS at n=36"

echo
[ "$fail" = 0 ] && echo "VERIFY: PASS (all quotes and numbers found)" || echo "VERIFY: FAIL ($fail)"
exit $((fail > 0))
