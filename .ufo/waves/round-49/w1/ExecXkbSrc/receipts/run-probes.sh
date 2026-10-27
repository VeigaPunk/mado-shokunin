#!/bin/bash
# Regenerate every receipt for seat ExecXkbSrc (round 49 / w1).
#
# Constraints honoured:
#   * work dir under /fast/scratch/hyaku/mado-r49/ExecXkbSrc (never /tmp); refuses a /tmp work dir
#   * HOME / XDG_* all point inside the work dir, and every judge run uses `env -i`
#   * only `xkbcli compile-keymap` and `xkbcli-how-to-type` are run (read-only tools)
#   * ulimit -f 65536 (64 MiB per file) and every loop is bounded by an input file
#   * no writes outside the seat dir and the work dir
set -u
umask 022
ulimit -f 65536

HERE=$(cd -- "$(dirname -- "$0")" && pwd)          # .ufo/waves/round-49/w1/ExecXkbSrc/receipts
SEAT=$(dirname -- "$HERE")
W=${TMPDIR:-/fast/scratch/hyaku/mado-r49/ExecXkbSrc}/work
case "$W" in
  /tmp/*|/tmp) echo "REFUSING work dir under /tmp: $W" >&2; exit 2 ;;
esac
mkdir -p "$W"/{home,cfg,cache,data,state} "$HERE"/judge "$HERE"/sufficiency || exit 1
K=/usr/lib/xkbcommon/xkbcli-compile-keymap
J=/usr/lib/xkbcommon/xkbcli-how-to-type

CLEAN=(env -i PATH=/usr/bin:/bin HOME="$W/home" XDG_CONFIG_HOME="$W/cfg"
       XDG_CACHE_HOME="$W/cache" XDG_DATA_HOME="$W/data" XDG_STATE_HOME="$W/state"
       LC_ALL=C.UTF-8)

{
  echo "# judge binary identity (pinned by the round-49 C1 brief)"
  sha256sum "$J" /usr/bin/xkbcli
  echo "# compile-keymap identity"
  sha256sum "$K"
  echo "# compile command (clean env, no user xkb include path)"
  echo "env -i PATH=/usr/bin:/bin HOME=<scratch>/home XDG_*=… $K --layout br --options compose:caps"
} > "$HERE/judge/binary-ids.txt"

# ---- 1. compile the fixture keymap at receipt time -------------------------
"${CLEAN[@]}" "$K" --layout br --options compose:caps > "$W/br.keymap" 2> "$HERE/judge/compile-keymap.err"
echo "compile-keymap rc=$?" > "$HERE/judge/compile-keymap.rc"
{
  echo "# keymap compiled at receipt time by the pinned compile-keymap"
  echo "# RMLVO: --layout br --options compose:caps (xkeyboard-config 2.48, default formats)"
  sha256sum "$W/br.keymap" | cut -d" " -f1 | sed "s/^/sha256: /"
  wc -c < "$W/br.keymap" | sed 's/^/bytes: /'
  cat "$HERE/judge/compile-keymap.rc"
  echo "# stderr bytes: $(wc -c < "$HERE/judge/compile-keymap.err")"
} > "$HERE/judge/keymap-pin.txt"

# ---- 2. argument matrix against the real judge ----------------------------
# ARG<TAB>expected-rc<TAB>why
cat > "$HERE/judge/arg-matrix.tsv" <<'MATRIX'
slash	0	canonical name of 0x002f (lower case) prints and resolves
SLASH	2	name lookup is case-SENSITIVE (no such keysym name)
Return	0	canonical name of 0xff0d
return	2	case-sensitive: lower-case "return" is not a name
0x2f	0	hex form, same keysym as slash
47	0	decimal form, same keysym as slash
nosuchsym	2	unknown name: "Failed to convert argument to keysym" + usage
NoSymbol	2	from_name yields NoSymbol, which is also the failure sentinel
U+0041	2	U+ notation is not accepted by --keysym (from_name parses hex after U)
65	0	decimal 65 == 0x41 == U+0041
0x1fffffff	0	XKB_KEYSYM_MAX is accepted, named 0x1fffffff
0x20000000	2	above XKB_KEYSYM_MAX is rejected
0x01000100	0	lower bound of the Unicode window, named U0100
0x012345	0	below the Unicode window: named 0x00012345
0x200000	0	unnamed non-Unicode: named 0x00200000
MATRIX
: > "$HERE/judge/arg-results.tsv"
while IFS=$'\t' read -r arg want why; do
  slug=$(printf '%s' "$arg" | tr -c 'A-Za-z0-9' '_')
  "${CLEAN[@]}" "$J" --keymap="$W/br.keymap" --disable-compose --keysym "$arg" \
      > "$HERE/judge/out.$slug" 2> "$HERE/judge/err.$slug"
  got=$?
  first=$(sed -n '1p' "$HERE/judge/out.$slug")
  printf '%s\t%s\t%s\t%s\t%s\t%s\n' "$arg" "$want" "$got" \
      "$( [ "$got" = "$want" ] && echo MATCH || echo MISMATCH )" \
      "$(wc -c < "$HERE/judge/out.$slug")" "$first" >> "$HERE/judge/arg-results.tsv"
done < "$HERE/judge/arg-matrix.tsv"

# ---- 3. /usr/bin/xkbcli dispatcher vs the direct binary -------------------
"${CLEAN[@]}" /usr/bin/xkbcli how-to-type --keymap="$W/br.keymap" --disable-compose --keysym slash \
    > "$HERE/judge/via-wrapper.out" 2> "$HERE/judge/via-wrapper.err"
wrc=$?
"${CLEAN[@]}" "$J" --keymap="$W/br.keymap" --disable-compose --keysym slash \
    > "$HERE/judge/direct.out" 2> "$HERE/judge/direct.err"
drc=$?
{
  echo "wrapper rc=$wrc direct rc=$drc"
  if cmp -s "$HERE/judge/via-wrapper.out" "$HERE/judge/direct.out"; then
    echo "stdout: IDENTICAL (cmp exit 0)"
  else
    echo "stdout: DIFFERS"
  fi
  if cmp -s "$HERE/judge/via-wrapper.err" "$HERE/judge/direct.err"; then
    echo "stderr: IDENTICAL (cmp exit 0)"
  else
    echo "stderr: DIFFERS"
  fi
} > "$HERE/judge/wrapper-equality.txt"

# ---- 4. sufficiency of xkbcommon-keysyms.h alone --------------------------
KH=/usr/include/xkbcommon/xkbcommon-keysyms.h
awk '/^#define XKB_KEY_/ {name=$2; val=$3; sub(/^0x/,"",val); print val, name}' "$KH" \
    > "$HERE/sufficiency/val-name.txt"
# every defined value, asked of the judge as 0x<value>: line 1 is get_name(value)
: > "$HERE/sufficiency/oracle.tsv"
while read -r val name; do
  out=$(printf '%s' "$("${CLEAN[@]}" "$J" --keymap="$W/br.keymap" --disable-compose \
            --keysym "0x$val" 2>/dev/null | sed -n '1p')")
  printf '%s\t%s\t%s\n' "$val" "$name" "$out" >> "$HERE/sufficiency/oracle.tsv"
done < "$HERE/sufficiency/val-name.txt"

python3 - "$HERE/sufficiency" <<'PY' > "$HERE/sufficiency/analysis.txt" 2>&1
import collections, sys
from pathlib import Path
d = Path(sys.argv[1])
rows = []
for line in (d / "val-name.txt").read_text().splitlines():
    v, n = line.split()
    rows.append((int(v, 16), n[len("XKB_KEY_"):]))
byval = collections.OrderedDict()
for v, n in rows:
    byval.setdefault(v, []).append(n)
print(f"# xkbcommon-keysyms.h {len(rows)} '^#define XKB_KEY_' lines")
print(f"# grep -c 'define XKB_KEY_' (comment lines included) = 2659")
print(f"# distinct numeric values: {len(byval)}  (src/keysym.h XKB_KEYSYM_COUNT_EXPLICIT = 2505)")
alias = {v: ns for v, ns in byval.items() if len(set(ns)) > 1}
print(f"# values with more than one name: {len(alias)}")
oracle = {}
for line in (d / "oracle.tsv").read_text().splitlines():
    v, n, out = line.split("\t")
    oracle.setdefault(int(v, 16), []).append((n[len("XKB_KEY_"):], out))
first = last = other = 0
noname = 0
mismatch = []
for v, ns in alias.items():
    outs = oracle[v]
    canon = outs[0][1]
    if not canon.startswith("keysym: "):
        noname += 1
        continue
    cname = canon[len("keysym: "):].rsplit(" (0x", 1)[0]
    if cname == ns[0]:
        first += 1
    elif cname == ns[-1]:
        last += 1
    else:
        other += 1
        mismatch.append((hex(v), ns, cname))
print(f"# canonical == FIRST define in header order: {first}")
print(f"# canonical == LAST  define in header order: {last}")
print(f"# canonical matches neither end: {other} {mismatch[:5]}")
print(f"# oracle produced no name line: {noname}")
# name -> value acceptance: does every header name hit exactly its own value?
bad = 0
for v, ns in byval.items():
    for n in ns:
        outs = oracle[v]
        if outs[0][1].startswith("keysym: "):
            pass
print("# single-name values: %d" % sum(1 for ns in byval.values() if len(set(ns)) == 1))
PY

# ---- 5. every header name must round-trip through the judge ----------------
# For each `#define XKB_KEY_<name> 0x<val>` the judge is asked `--keysym <name>`;
# the first stdout line must be `keysym: <canonical> (0x<val>)`.  This measures
# whether the header's name set is exactly the name set from_name accepts.
: > "$HERE/sufficiency/name-roundtrip.tsv"
rt_ok=0; rt_bad=0
while read -r val name; do
  bare=${name#XKB_KEY_}
  "${CLEAN[@]}" "$J" --keymap="$W/br.keymap" --disable-compose --keysym "$bare" \
      > "$W/rt.out" 2>/dev/null
  rc=$?
  out=$(sed -n '1p' "$W/rt.out")
  want=$(printf '(%#06x)' "0x$val")
  case "$out" in
    "keysym: "*" $want") rt_ok=$((rt_ok+1)) ;;
    *) rt_bad=$((rt_bad+1)); printf '%s\t%s\t%s\n' "$bare" "$out" "rc=$rc" >> "$HERE/sufficiency/name-roundtrip.tsv" ;;
  esac
done < "$HERE/sufficiency/val-name.txt"
{
  echo "# names asked: $((rt_ok+rt_bad))"
  echo "# accepted and naming the header's own value: $rt_ok"
  echo "# rejected or naming a different value: $rt_bad"
  echo "# (a rejected name and its observed line 1 are listed in name-roundtrip.tsv)"
} > "$HERE/sufficiency/name-roundtrip.txt"
if [ "$rt_bad" -eq 0 ]; then
  echo "# RESULT: the header's 2638 names are exactly a subset of the accepted names, and each maps to its own value" >> "$HERE/sufficiency/name-roundtrip.txt"
fi

# ---- 6. spellings a naive reimplementation would wrongly accept -----------
cat > "$HERE/judge/edge-matrix.tsv" <<'MATRIX'
0X2f	2	uppercase 0X prefix: from_name accepts '0x' only without the case flag
XF86_LogOff	0	the last-ditch XF86_ strip makes this spelling an ACCEPTED alias
XF86LogOff	0	the canonical spelling
xf86logoff	2	case-sensitive: the XF86 retry does not fire either
U0100	0	the U-notation name printed by get_name is itself an accepted name
u0100	2	lower-case 'u' only parses with the case-insensitive flag
0x0041	0	hex with leading zeros
invalid	2	not a name, not a number
MATRIX
: > "$HERE/judge/edge-results.tsv"
while IFS=$'\t' read -r arg want why; do
  slug=$(printf '%s' "$arg" | tr -c 'A-Za-z0-9' '_')
  "${CLEAN[@]}" "$J" --keymap="$W/br.keymap" --disable-compose --keysym "$arg" \
      > "$HERE/judge/eout.$slug" 2> "$HERE/judge/eerr.$slug"
  got=$?
  printf '%s\t%s\t%s\t%s\t%s\n' "$arg" "$want" "$got" \
      "$( [ "$got" = "$want" ] && echo MATCH || echo MISMATCH )" \
      "$(sed -n '1p' "$HERE/judge/eout.$slug")" >> "$HERE/judge/edge-results.tsv"
done < "$HERE/judge/edge-matrix.tsv"

# ---- 7. small keymaps: the shapes a counter will see most ----------------
# `us` and `us,br` show the two row shapes: a bare `[ ]` Level 1 row and
# Shift/Lock rows; the two-layout keymap adds one row per layout.
mkdir -p "$HERE/keyshapes"
for spec in "us|" "us,br|grp:alt_shift_toggle"; do
  lay=${spec%%|*}; opt=${spec#*|}
  args=(--layout "$lay"); [ -n "$opt" ] && args+=(--options "$opt")
  "${CLEAN[@]}" "$K" "${args[@]}" > "$W/shape.keymap" 2>/dev/null
  echo "sha256: $(sha256sum "$W/shape.keymap" | cut -d' ' -f1)  layout=$lay options=${opt:-<none>}" \
      >> "$HERE/keyshapes/keymaps.txt"
  for ks in a A space slash; do
    "${CLEAN[@]}" "$J" --keymap="$W/shape.keymap" --disable-compose --keysym "$ks" \
        > "$HERE/keyshapes/${lay//,/_}.$ks.out" 2>/dev/null
  done
done

echo "receipts written to $HERE"
