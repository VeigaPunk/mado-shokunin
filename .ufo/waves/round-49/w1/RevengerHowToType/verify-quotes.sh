#!/bin/sh
# verify-quotes.sh — recompute every locator in report.md against this seat's pinned copies.
#
# Three check kinds:
#   check_code  the snippet is quoted verbatim in report.md AND exists byte-exactly in the
#               pinned file; the locator is recomputed with grep -nF.
#   check_loc   the report paraphrases or truncates the line, so only the locator is checked
#               (grep -nF), plus an anchor that must appear in report.md.
#   check_prose commit messages / Doxygen prose wrap across lines: the quote is matched against
#               a whitespace-normalized copy, the locator comes from a single-line anchor.
#
# Nothing here writes outside the seat dir. Output is the receipt
# `receipt-verify-quotes.txt` (regenerate with: ./verify-quotes.sh > receipt-verify-quotes.txt).
set -u
cd "$(dirname "$0")" || exit 1

REPORT=report.md
fails=0
n=0
norm_report=$(tr '\n' ' ' < "$REPORT" | tr -s ' ')

fail() { printf 'FAIL  %s\n' "$*"; fails=$((fails + 1)); }
has_report() { case "$norm_report" in *"$1"*) return 0 ;; *) fail "report.md does not contain [$1]"; return 1 ;; esac; }

loc_of() { grep -nF -- "$2" "$1" | cut -d: -f1 | tr '\n' ' '; }

# check_code <file> <line> <snippet>
check_code() {
    n=$((n + 1))
    file=$1; want=$2; snip=$3
    [ -f "$file" ] || { fail "missing pinned file $file"; return; }
    has_report "$snip" || return
    hits=$(loc_of "$file" "$snip")
    case " $hits " in
        *" $want "*) printf 'ok    %s:%s  %s\n' "$file" "$want" "$snip" ;;
        *) fail "$file:$want is not a grep -nF locator of [$snip] (found: $hits)" ;;
    esac
}

# check_loc <file> <line> <snippet> <report anchor>
check_loc() {
    n=$((n + 1))
    file=$1; want=$2; snip=$3; anchor=$4
    [ -f "$file" ] || { fail "missing pinned file $file"; return; }
    has_report "$anchor" || return
    hits=$(loc_of "$file" "$snip")
    case " $hits " in
        *" $want "*) printf 'ok    %s:%s  %s\n' "$file" "$want" "$snip" ;;
        *) fail "$file:$want is not a grep -nF locator of [$snip] (found: $hits)" ;;
    esac
}

# check_prose <file> <line> <single-line source anchor> <whitespace-normalized quote> [report anchor]
check_prose() {
    n=$((n + 1))
    file=$1; want=$2; anchor=$3; quote=$4; ranchor=${5:-$3}
    [ -f "$file" ] || { fail "missing pinned file $file"; return; }
    has_report "$ranchor" || return
    hits=$(loc_of "$file" "$anchor")
    case " $hits " in
        *" $want "*) ;;
        *) fail "$file:$want is not a grep -nF locator of [$anchor] (found: $hits)"; return ;;
    esac
    norm=$(tr '\n' ' ' < "$file" | tr -s ' ')
    case "$norm" in
        *"$quote"*) printf 'ok    %s:%s  %s\n' "$file" "$want" "$anchor" ;;
        *) fail "normalized quote absent from $file: [$quote]" ;;
    esac
}

TOOLS='src/tools_how-to-type.c@d1442aaa'
KEYSYM='src/src_keysym.c@d1442aaa'
KEYMAP='src/src_keymap.c@d1442aaa'
FMT='src/src_keymap-formats.h@d1442aaa'
DOC='src/doc_keymap-text-format-v1-v2.md@d1442aaa'
MESON='src/meson.build@d1442aaa'
ORIGIN='src/test_how-to-type.c@188a1c79'
HDR='src/xkbcommon-keysyms.h@host-1.13.2'
GEN='src/scripts_update-keysyms-derived-headers.py@d1442aaa'
MSGS='receipt-commit-messages.txt'

echo "== pinned file digests (src/SHA256SUMS)"
( cd src && sha256sum -c SHA256SUMS ) | grep -v ': OK$'
echo "   ($(grep -c . src/SHA256SUMS) pinned files verified)"
echo

echo "== output anatomy (tools/how-to-type.c @1.13.2 = d1442aaa)"
check_code "$TOOLS" 625 'printf("keysym: %s (%#06"PRIx32")\n\n", name, keysym);'
check_code "$TOOLS" 626 'printf("=== Direct access ===\n\n");'
check_loc  "$TOOLS" 627 'printf("%-8s %-9s %-8s %-20s %-7s %-s\n",' '%-20s %-7s %-s'
check_loc  "$TOOLS" 527 'printf("%-8u %-9s %-8u %-20s %-7u [ ",' '%-7u [ '
check_loc  "$TOOLS" 531 'xkb_keymap_mod_get_mask2(keymap, mod);' 'xkb_keymap_mod_get_mask2'
check_loc  "$TOOLS" 534 'printf("%s ", xkb_keymap_mod_get_name(keymap, mod));' 'xkb_keymap_mod_get_name'
check_loc  "$TOOLS" 460 '#define SHIFT_LOCK_MASK (SHIFT_MASK | LOCK_MASK)' 'LOCK_MASK'
check_loc  "$TOOLS" 489 '/* skip “shift cancel lock” */' 'shift cancel lock'
check_loc  "$TOOLS" 697 'xkb_keymap_key_get_mods_for_level(' 'xkb_keymap_key_get_mods_for_level'

echo
echo "== name resolution (src/keysym.c @1.13.2)"
check_loc "$KEYSYM" 54 '#define get_name_by_index(index) (keysym_names + (index))' 'keysym_names'
check_loc "$KEYSYM" 66 'return snprintf(buffer, size, "U%04"PRIX32, ks & UINT32_C(0xffffff));' 'U%04'
check_loc "$KEYSYM" 93 'return snprintf(buffer, size, "0x%08x", ks);' '0x%08x'

echo
echo "== mask source (src/keymap.c @1.13.2)"
check_loc  "$KEYMAP" 494 'xkb_keymap_key_get_mods_for_level(struct xkb_keymap *keymap,' 'xkb_keymap_key_get_mods_for_level'
check_code "$KEYMAP" 527 'This is almost always what we want. If applicable, given it priority'
check_loc  "$KEYMAP" 539 'masks_out[count++] = 0;' 'empty mask'

echo
echo "== defaults and exit code"
check_loc  "$FMT" 13 '#define DEFAULT_INPUT_KEYMAP_FORMAT  XKB_KEYMAP_FORMAT_TEXT_V2' 'DEFAULT_INPUT_KEYMAP_FORMAT'
check_code "$FMT" 14 '#define DEFAULT_OUTPUT_KEYMAP_FORMAT XKB_KEYMAP_USE_ORIGINAL_FORMAT'
check_code "$MESON" 166 "configh_data.set('EXIT_INVALID_USAGE', '2')"

echo
echo "== canonical-name rules (header + generator)"
check_loc "$HDR" 105 'the first one listed is considered the "canonical" name' 'first one listed is considered'
check_loc "$HDR" 286 '#define XKB_KEY_Mode_switch                   0xff7e' 'Mode_switch'
check_loc "$GEN" 48 'canonical_names[value] = name' 'update-keysyms-derived-headers.py:47-48'

echo
echo "== origin file (test/how-to-type.c @188a1c7)"
check_loc "$ORIGIN" 128 'printf("keysym: %s (%#x)\n", name, keysym);' 'keysym: X (0x002f)'
check_loc "$ORIGIN" 38 'Pipe into `column -ts $'"'"'\\t'"'"'` for nice aligned output.' 'column -ts'

echo
echo "== prose quotes (whitespace-normalized)"
check_prose "$MSGS" 5 'The new API is useful to implement features like auto-type and' \
    'The new API is useful to implement features like auto-type and desktop automation.'
check_prose "$MSGS" 8 'implementation needs to be able to invert the keycode->keysym' \
    'implementation needs to be able to invert the keycode->keysym transformation' 'invert the keycode->keysym transformation'
check_prose "$MSGS" 19 'The program was written to exercise the new' \
    'The program was written to exercise the new xkb_keymap_key_get_mods_for_level() function.' 'was written to exercise the new'
check_prose "$MSGS" 82 'Previously, could only check how to type a Unicode codepoint, but' \
    'Previously, could only check how to type a Unicode codepoint, but searching for a keysym directly is also occasionally useful.'
check_prose "$MSGS" 194 '`ISO_Group_Shift` is now the canonical name of the corresponding keysym.' \
    '`ISO_Group_Shift` is now the canonical name of the corresponding keysym. Previously it was `Mode_switch`, which refers to a core X group mechanism obsoleted by XKB.'
check_prose "$DOC" 2767 '@note @anchor auto-modifier-encoding If using' \
    'virtual modifiers that were not mapped either *implicitly* using the `virtualModifier`/`modifier_map` feature hereinabove or [*explicitly*](@ref explicit-modifier-encoding), then they are mapped to their [*canonical* mapping](@ref canonical-modifier-def).' \
    'keymap-text-format-v1-v2.md:2767-2771'

echo
echo "== header statistics quoted in the report (2638 / 2505 / 120 / 9)"
python3 - "$HDR" <<'PY' || fails=$((fails + 1))
import collections, re, sys
p = sys.argv[1]
v2n = collections.defaultdict(list)
for line in open(p, encoding="utf-8"):
    m = re.match(r"#define XKB_KEY_(\w+)\s+(0x[0-9a-fA-F]+)", line)
    if m:
        v2n[int(m.group(2), 16)].append(m.group(1))
got = (sum(len(v) for v in v2n.values()), len(v2n),
       sum(1 for v in v2n.values() if len(v) > 1), len(v2n[0xff7e]))
want = (2638, 2505, 120, 9)
print(("ok    " if got == want else "FAIL  ") +
      "defines=%d values=%d multi=%d names_0xff7e=%d" % got)
sys.exit(0 if got == want else 1)
PY

echo
echo "== decoded canonical name for keysym 0xff7e (receipt-canonical-name-decode.txt)"
if grep -q '^1\.13\.2: keysym_to_name offset=17760 -> ISO_Group_Shift$' receipt-canonical-name-decode.txt &&
   grep -q '^1\.13\.1: keysym_to_name offset=19891 -> Mode_switch$' receipt-canonical-name-decode.txt; then
    echo "ok    1.13.1 Mode_switch / 1.13.2 ISO_Group_Shift"
else
    fail "canonical-name decode receipt does not show the flip"
fi

echo
printf 'tally: %s checks, %s failures\n' "$n" "$fails"
[ "$fails" -eq 0 ]
