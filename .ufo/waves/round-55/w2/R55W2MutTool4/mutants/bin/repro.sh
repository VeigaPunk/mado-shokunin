#!/bin/bash
# repro.sh ORIG_TOOL MUTANT_DIR WORKDIR
# For each mutant that survives all 26 fixtures: runs the minimal input under the ORIGINAL tool and under the MUTANT
# (python3 -I, cwd = WORKDIR, nothing touches the lane). CTRL rows (label "control") are parser-compatible controls:
# they must print identical stdout and rc on both sides; "attack" rows must differ.
ORIG=$1; MD=$2; W=$3
mkdir -p "$W" && cd "$W" || exit 9

c() {  # c MUTANT_ID LABEL ARGV...
  local id=$1 label=$2; shift 2
  local side tool rc
  for side in orig mut; do
    if [ "$side" = orig ]; then tool=$ORIG; else tool=$MD/$id.py; fi
    python3 -I "$tool" "$@" > "o.$id.$label.$side" 2> "e.$id.$label.$side"; rc=$?
    printf '== %s %s [%s] rc=%s argv=%s\n' "$id" "$label" "$side" "$rc" "$(printf '%q ' "$@")"
    printf -- '-- stdout:\n'; cat "o.$id.$label.$side"; printf '\n-- stderr last line: %s\n' "$(tail -n 1 "e.$id.$label.$side")"
  done
  if cmp -s "o.$id.$label.orig" "o.$id.$label.mut"; then printf '** %s %s: stdout identical (rc orig=%s)\n' "$id" "$label" "$rc"; else printf '** %s %s: stdout DIFFERS\n' "$id" "$label"; fi
}

printf 'input {\n  repeat_rate = 30\n}\n' > r30.conf
: > empty.conf
printf 'input:repeat_rate = 201\n' > r201.conf
printf 'input:repeat_rate = 200\n' > r200.conf
printf '\x0binput:repeat_rate = 30\n' > vt.conf
printf 'input:repeat_rate = 40\n' > r40.conf
printf 'device {\n  name = kbd-a\n}\ndevice {\n  repeat_rate = 50\n}\n' > dev9.conf
printf 'device {\n  name = kbd-a # my kbd\n  repeat_rate = 50\n}\n' > dev20.conf
printf 'input {\n  repeat_rate = 30\n}\ndevice {\n  name = kbd-a\n  repeat_rate = 50\n}\n' > dev21.conf
printf '{"option":"input:repeat_rate","int":40}\n' > g40.json
printf '{"option":"input:repeat_rate","int":41}\n' > g41.json
printf '{"option":"input:repeat_rate","int":50}\n' > g50.json
printf '{"option":"input:repeat_rate","int":"x"}\n' > gstr.json
printf '{"option":"input:numlock_by_default","int":true}\n' > gbool.json
printf '{"option":"input:numlock_by_default","int":0}\n' > gnum0.json
printf '{"option":"input:repeat_rate","int":40.0}\n' > gfloat.json
printf '{"nothing": NaN}\n' > gnan.json
printf '[1]\n' > garr.json
{ printf '#'; head -c 1048574 /dev/zero | tr '\0' x; printf '\n'; } > exact.conf
{ printf '#'; head -c 1048575 /dev/zero | tr '\0' x; printf '\n'; } > over.conf
printf 'exact.conf=%s bytes; over.conf=%s bytes\n' "$(stat -c %s exact.conf)" "$(stat -c %s over.conf)"

c M01 attack   --config r30.conf --keyboard
c M01 attack2  --config
c M01 control  --config r30.conf --keyboard kbd-a
c M02 attack   --config empty.conf --getoption g40.json --getoption g41.json
c M02 control  --config empty.conf --getoption g40.json
c M04 attack   --config empty.conf --keyboard "$(printf 'kbd\177x')"
c M04 control  --config empty.conf --keyboard kbd-x
c M05 attack   --config r201.conf
c M05 control  --config r200.conf
c M06 attack   --config vt.conf
c M06 control  --config r30.conf
c M09 attack   --config dev9.conf --keyboard kbd-a
c M09 control  --config r30.conf --keyboard kbd-a
c M10 attack   --config r40.conf --getoption g41.json
c M10 control  --config r40.conf --getoption g40.json
c M11 attack   --config empty.conf --getoption gstr.json
c M11 control  --config empty.conf --getoption g40.json
c M12 attack   --config empty.conf --getoption gbool.json
c M12 control  --config empty.conf --getoption gnum0.json
c M13 attack   --config r40.conf --getoption gfloat.json
c M13 control  --config r40.conf --getoption g40.json
c M14 attack   --config empty.conf --getoption gnan.json
c M14 control  --config empty.conf --getoption g40.json
c M16 attack   --config empty.conf --getoption garr.json
c M16 control  --config empty.conf --getoption g40.json
c M17 attack   --config exact.conf
c M17 control  --config r30.conf
c M18 attack   --config over.conf
c M18 control  --config no-such-file.conf
c M20 attack   --config dev20.conf --keyboard kbd-a
c M20 control  --config dev9.conf --keyboard kbd-a
c M21 attack   --config dev21.conf --keyboard kbd-a --getoption g50.json
c M21 control  --config r40.conf --getoption g40.json
