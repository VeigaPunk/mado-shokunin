#!/bin/sh
# Re-grep every quote in receipts/notes.md against the pinned libxkbcommon
# sources and print the computed locator (grep -n), so no locator is typed.
#
# SRCROOT is a tree holding the files named in the map below, at the paths
# libxkbcommon uses.  To rebuild it when this seat's scratch tree is gone:
#   for p in src/keysym.c src/keymap.h src/xkbcomp/keymap.c \
#            src/xkbcomp/symbols.c src/xkbcomp/keymap-dump.c \
#            src/keysym-case-mappings.c src/keysym-utf.c src/ks_tables.h \
#            tools/how-to-type.c; do
#     mkdir -p "$SRCROOT/$(dirname $p)"
#     curl -sSfL "https://raw.githubusercontent.com/xkbcommon/libxkbcommon/xkbcommon-1.13.2/$p" \
#       -o "$SRCROOT/$p"
#   done
# then check with the sha256 list in receipts/pins.txt.
set -u
SRCROOT=${SRCROOT:?set SRCROOT to the pinned source tree}
here=$(dirname "$0")
fail=0
check() {
    file=$1; pat=$2; want=$3
    got=$(grep -nF -- "$pat" "$SRCROOT/$file" | cut -d: -f1 | tr '\n' ' ')
    if [ -z "$got" ]; then
        echo "MISSING  $file  '$pat'"
        fail=1
    elif [ -n "$want" ] && ! echo " $got" | grep -q " $want "; then
        echo "MISLOC   $file  '$pat'  recorded=$want found=$got"
        fail=1
    else
        echo "OK       $file:$got '$pat'"
    fi
}
check tools/how-to-type.c '{"keymap",' 171
check tools/how-to-type.c '*keysym = XKB_KEY_NoSymbol;' 269
check tools/how-to-type.c 'xkb_keysym_from_name(argv[optind], XKB_KEYSYM_NO_FLAGS)' 286
check tools/how-to-type.c 'ERROR: Failed to convert argument to keysym' 293
check tools/how-to-type.c 'printf("keysym: %s (%#06' 625
check tools/how-to-type.c 'if ((mask & mod_mask) != mod_mask)' 532
check tools/how-to-type.c 'printf("%-8u %-9s %-8u %-20s %-7u [ "' 527
check src/keymap.h 'entry_is_active(const struct xkb_key_type_entry *entry)' 676
check src/xkbcomp/keymap.c 'has_unbound_vmods(struct xkb_keymap *keymap, xkb_mod_mask_t mask)' 25
check src/xkbcomp/keymap.c 'if (mod->mapping == 0 && !(keymap->mods.explicit_vmods & mask)) {' 469
check src/xkbcomp/keymap.c '(group == 0 && level == 0) || !interp->level_one_only' 209
check src/xkbcomp/symbols.c 'FindAutomaticType(struct xkb_context *ctx, GroupInfo *groupi)' 1594
check src/xkbcomp/symbols.c 'Drop trailing NoSymbol' 842
check src/xkbcomp/symbols.c 'Always have as many levels as the type specifies' 1767
check src/xkbcomp/keymap-dump.c "Printing level 1 entries is redundant, it's the default," 342
check src/keysym-case-mappings.c 'xkb_keysym_is_lower(xkb_keysym_t ks)' 624
check src/keysym.c "if (*name == 'U' || (icase && *name == 'u'))" 305
check src/keysym.c "name[0] == '0' && (name[1] == 'x'" 325
check src/keysym.c '0x%08x' 93
[ "$fail" -eq 0 ] && echo "all quotes located" || echo "FAILURES"
exit "$fail"
