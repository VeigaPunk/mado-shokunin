#!/usr/bin/env python3
"""MutC1Tool: generate one-behaviour mutants of the LANDED tools/mado-keysym.py.

Each mutant = exactly one string replacement, asserted to occur exactly once in the
pristine source. Mutants land in mutants/<ID>.py plus manifest.json. Read-only use of
the lane. Rationale per mutant cites the behaviour it flips (round-49 w2 item MutC1Tool
list + tool-derived probes).
"""
import json
import os
import py_compile
import sys

PRISTINE = "/home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-keysym.py"
OUTDIR = os.path.dirname(os.path.abspath(__file__))

MUTANTS = [
    ("M01", "automatic-type ALPHABETIC test inverted (2-level branch)",
     "    if width == 2:\n        if keysym_is_lower(sym0) and keysym_is_upper_or_title(sym1):",
     "    if width == 2:\n        if not (keysym_is_lower(sym0) and keysym_is_upper_or_title(sym1)):"),
    ("M02", "keypad keysym range widened to 0xFFFF (F-keys become keypad for automatic type)",
     "    return 0xFF80 <= keysym <= 0xFFBD  # XKB_KEY_KP_Space .. XKB_KEY_KP_Equal",
     "    return 0xFF80 <= keysym <= 0xFFFF  # XKB_KEY_KP_Space .. XKB_KEY_KP_Equal"),
    ("M03", "explicit per-group type ignored (default type only)",
     "            type_name = group.type_name or key.default_type",
     "            type_name = key.default_type"),
    ("M04", "group0 levels copied into later groups even when they carry an explicit type",
     "                if not group.levels and group.type_name is None:",
     "                if not group.levels:"),
    ("M05", "AnyOfOrNone interp no longer matches mod-less keys",
     "        return (not mods) or bool(interp.mods & mods)",
     "        return bool(interp.mods & mods)"),
    ("M06", "top-level interpret.useModMapMods default inverted (LevelOne vs AnyLevel)",
     "        level_one_only_default = value in (\"level1\", \"levelone\")",
     "        level_one_only_default = value not in (\"level1\", \"levelone\")"),
    ("M07", "canonical fallback mapping for unbound virtual modifiers zeroed",
     "            mod.mapping = 1 << index",
     "            mod.mapping = 0"),
    ("M08", "explicit per-key virtualMods= ignored (vmodmap always recomputed)",
     "        if key.vmodmap_explicit:\n            continue",
     "        if False:\n            continue"),
    ("M09", "modifier_map decls allowed to set virtual-modifier bits into key modmap",
     "        if index is None or index >= 8:\n            continue",
     "        if index is None:\n            continue"),
    ("M10", "keycode iteration order: insertion order instead of sorted",
     "    for keycode in sorted(km.keys):",
     "    for keycode in km.keys:"),
    ("M11", "modifier names printed in reversed real+virtual order",
     "                        mod.name for mod in km.mods",
     "                        mod.name for mod in reversed(km.mods)"),
    ("M12", "layout name fallback '?' removed (empty string)",
     "                layout_name = \"?\"",
     "                layout_name = \"\""),
    ("M13", "xkb_symbols name[...] group index off-by-one (layout names shifted)",
     "            index = cur.number() - 1",
     "            index = cur.number()"),
    ("M14", "LEVEL# column off-by-one (level+1 -> level)",
     "                                  _ljust(layout_name, 20), _ljust(\"%d\" % (level + 1), 7),",
     "                                  _ljust(layout_name, 20), _ljust(\"%d\" % level, 7),"),
    ("M15", "LAYOUT column off-by-one (group_index+1 -> group_index)",
     "                                  _ljust(\"%d\" % (group_index + 1), 8),",
     "                                  _ljust(\"%d\" % group_index, 8),"),
    ("M16", "trailing newline dropped from output page",
     "    return \"\\n\".join(lines) + \"\\n\"",
     "    return \"\\n\".join(lines)"),
    ("M17", "hex keysym header field printed with 6 hex digits (0x%04x -> 0x%06x)",
     "        return \"0x%04x\" % keysym",
     "        return \"0x%06x\" % keysym"),
    ("M18", "U-name upper threshold lowered to 0x0100FFFF (astral keysyms print hex)",
     "    if KEYSYM_UNICODE_MIN <= keysym <= KEYSYM_UNICODE_MAX:",
     "    if KEYSYM_UNICODE_MIN <= keysym <= 0x0100FFFF:"),
    ("M19", "U-name lower threshold dropped to 0x01000000 (0x010000xx print U form)",
     "    if KEYSYM_UNICODE_MIN <= keysym <= KEYSYM_UNICODE_MAX:",
     "    if 0x01000000 <= keysym <= KEYSYM_UNICODE_MAX:"),
    ("M20", "U-form argument threshold raised to 0xFFFD (U00xx-UFFFC take the utf32 path)",
     "        if 0xFF < value <= 0x10FFFF:",
     "        if 0xFFFD < value <= 0x10FFFF:"),
    ("M21", "XF86_ name fallback removed (XF86Audio* unresolvable)",
     "        return keysym_from_name(name[:4] + name[5:])",
     "        return 0"),
    ("M22", "decimal ARG <= 0 accepted by resolve_argument (negative/zero numerics)",
     "    if value is None or value <= 0 or value > KEYSYM_MAX:",
     "    if value is None or value > KEYSYM_MAX:"),
    ("M23", "0x-form ARG above KEYSYM_MAX accepted",
     "        if value is None or value > KEYSYM_MAX:\n            return 0\n        return value",
     "        if value is None:\n            return 0\n        return value"),
    ("M24", "levels with 2+ keysyms no longer skipped when the first keysym matches",
     "                if len(syms) != 1 or syms[0] != keysym:",
     "                if not syms or syms[0] != keysym:"),
    ("M25", "level-0 zero-mask appended for every level, not only level 0",
     "    masks = []\n    if level == 0:",
     "    masks = []\n    if level >= 0:"),
    ("M26", "keycode alias registered as self-alias (aliased keys lose their target)",
     "            km.aliases[text2[1:-1]] = text3[1:-1]",
     "            km.aliases[text2[1:-1]] = text2[1:-1]"),
    ("M27", "--disable-compose/--keysym refusal only when BOTH are missing",
     "    if not disable_compose or not keysym_mode:",
     "    if not disable_compose and not keysym_mode:"),
    ("M28", "extra positional ARG accepted (exactly-one check weakened)",
     "    if len(positional) != 1:",
     "    if len(positional) < 1:"),
    ("M29", "vmod phase order: canonical fallback before key-derived real mappings",
     "    # 3. Virtual -> real modifier mappings (keymap.c:447).\n    for index in range(8, len(km.mods)):\n        bit = 1 << index\n        for key in km.keys.values():\n            if key.vmodmap & bit:\n                km.mods[index].mapping |= key.modmap\n\n    # 4. Format 2 canonical mapping for still-unbound virtual modifiers (keymap.c:458).\n    for index in range(8, len(km.mods)):\n        mod = km.mods[index]\n        if mod.mapping == 0 and not mod.explicit:\n            mod.mapping = 1 << index\n            mod.explicit = True",
     "    # 3. Format 2 canonical mapping for still-unbound virtual modifiers (keymap.c:458).\n    for index in range(8, len(km.mods)):\n        mod = km.mods[index]\n        if mod.mapping == 0 and not mod.explicit:\n            mod.mapping = 1 << index\n            mod.explicit = True\n\n    # 4. Virtual -> real modifier mappings (keymap.c:447).\n    for index in range(8, len(km.mods)):\n        bit = 1 << index\n        for key in km.keys.values():\n            if key.vmodmap & bit:\n                km.mods[index].mapping |= key.modmap"),
]


def main():
    with open(PRISTINE, "rb") as fh:
        pristine = fh.read().decode("utf-8")
    mdir = os.path.join(OUTDIR, "mutants")
    os.makedirs(mdir, exist_ok=True)
    manifest = []
    for mid, desc, old, new in MUTANTS:
        count = pristine.count(old)
        if count != 1:
            print("ABORT %s: pattern occurs %d times" % (mid, count))
            return 1
        text = pristine.replace(old, new, 1)
        assert text != pristine
        path = os.path.join(mdir, mid + ".py")
        with open(path, "w", encoding="utf-8") as fh:
            fh.write(text)
        py_compile.compile(path, cfile=os.path.join(mdir, mid + ".pyc"), doraise=True)
        os.unlink(os.path.join(mdir, mid + ".pyc"))
        manifest.append({"id": mid, "desc": desc, "old": old, "new": new})
    with open(os.path.join(mdir, "manifest.json"), "w", encoding="utf-8") as fh:
        json.dump(manifest, fh, indent=1)
    print("generated %d mutants in %s" % (len(manifest), mdir))
    return 0


if __name__ == "__main__":
    sys.exit(main())
