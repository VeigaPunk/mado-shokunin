#!/usr/bin/env python3
"""Unit checks for rules that the RMLVO corpus cannot reach (see the report)."""
import sys
sys.path.insert(0, ".")
import mods

names, masks = mods.mod_table([("NumLock", 1 << 4), ("LevelThree", 1 << 7),
                               ("Hyper", 0)])
lines = []


def check(label, got, want):
    ok = got == want
    lines.append("%-58s %-40r %s" % (label, got, "OK" if ok else "MISMATCH want %r" % (want,)))
    return ok


one_level = mods.finalize_type("ONE_LEVEL", 0, [], [], masks)
two_level = mods.finalize_type("TWO_LEVEL", 1, [(1, 1, 0)], [], masks)
ok = True
ok &= check("ONE_LEVEL level 0 masks", mods.mods_for_level(one_level, 0), [0])
ok &= check("ONE_LEVEL level 1 masks (out of range)", mods.mods_for_level(one_level, 1), [])
ok &= check("TWO_LEVEL level 1 masks (Shift at 0x%02x)" % masks[0],
            mods.mods_for_level(two_level, 1), [1])
ok &= check("TWO_LEVEL level 0 masks", mods.mods_for_level(two_level, 0), [0])
ok &= check("ONE_LEVEL num_levels", mods.num_levels(one_level), 1)

# cap: 102 distinct entries at level 2 -> 100 masks
entries = [(m, 1, 0) for m in range(1, 103)]
big = mods.finalize_type("BIG", 0xFFFF, entries, [], masks)
ok &= check("102 distinct entries survive finalisation", len(big["entries"]), 102)
ok &= check("102 entries -> masks truncated", len(mods.mods_for_level(big, 1)), 100)
ok &= check("cap honoured at masks_size=3",
            len(mods.mods_for_level(big, 1, masks_size=3)), 3)

# effective_mask: unknown bits (past the table) pass through unchanged
ok &= check("unknown bit 0x4000 with 11-mod table",
            mods.effective_mask(0x4000, masks), 0x4000)
ok &= check("vmod bit expands to its mapping (LevelThree -> Mod5)",
            mods.effective_mask(1 << 9, masks), 1 << 7)
ok &= check("real bit stays", mods.effective_mask(1 << 1, masks), 1 << 1)

# unbound vmod (mapping 0) is named in every mask, and deactivates entries
unbound = mods.finalize_type("UNBOUND", 1 | (1 << 10),
                             [(1, 1, 0), (1 << 10, 1, 0), (1 | (1 << 10), 1, 0)],
                             [], masks)
ok &= check("unbound vmod: active flags",
            [mods.entry_is_active(e) for e in unbound["entries"]],
            [True, False, False])
ok &= check("unbound vmod: level 2 masks drop deactivated entries",
            mods.mods_for_level(unbound, 1), [1])
ok &= check("unbound vmod named in every cell",
            mods.format_modifiers(0, names, masks), "[ Hyper ]")
ok &= check("mapping-0 modifier named even when mask is full",
            mods.format_modifiers(0xFF, names, masks),
            "[ Shift Lock Control Mod1 Mod2 Mod3 Mod4 Mod5 NumLock LevelThree Hyper ]")

print("\n".join(lines))
print("UNIT_OK" if ok else "UNIT_FAIL")
sys.exit(0 if ok else 1)
