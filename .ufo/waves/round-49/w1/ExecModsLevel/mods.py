# SPDX-License-Identifier: MIT
"""MODIFIERS column of ``xkbcli how-to-type``, re-implemented from pinned sources.

Sources (libxkbcommon, tag ``xkbcommon-1.13.2``; sha256 + URL in ``PINS.txt``):

  * ``src/keymap.c``            ``xkb_keymap_key_get_mods_for_level`` (l.493-553)
  * ``src/keymap.h``            ``entry_is_active`` (l.672-681), ``XkbKeyNumLevels`` (l.661-666)
  * ``src/state.c``             ``mod_mask_get_effective`` (l.1613-1626)
  * ``src/xkbcomp/keymap.c``    ``ComputeEffectiveMask`` (l.36-49), type finalisation (l.466-511)
  * ``src/xkbcomp/keymap-dump.c`` ``write_types`` (l.313-385), ``write_vmods`` (l.213-260)
  * ``src/xkbcomp/symbols.c``   ``FindAutomaticType`` (l.1594-1638)
  * ``tools/how-to-type.c``     ``MAX_TYPE_MAP_ENTRIES`` (l.27), ``print_combo`` (l.521-537), call site (l.694-703)

Three separate rules make up the column; they are kept apart on purpose:

1. **Which explicit map entries produce a level** -- ``mods_for_level``.  The key
   type's ``map[<modifiers>]= <level>`` entries are scanned in declaration order and
   every *active* entry whose level matches contributes its effective modifier mask.
   Order is entry order, duplicates included, truncated at ``masks_size`` (100 in
   how-to-type).  Level 0 (Level 1) is special-cased: because an unmatched modifier
   set also yields level 0, the empty mask is synthesised *first* unless an active
   entry already maps the empty mask to level 0.

2. **Which entries are active** -- an entry that names a virtual modifier with no
   mapping (``virtual_modifiers M = none`` / implicit ``none``) is deactivated:
   its mask is zeroed and it is skipped.  ``entry_is_active`` then reports
   ``mods == 0 or mask != 0``, i.e. the deactivated entry looks like "mask 0" for
   the *named* mask but is dropped because it named something.

3. **How a mask is printed** -- ``format_modifiers``.  Not "the type's modifiers":
   *every* modifier index of the keymap, real ones (indices 0..7, always
   ``Shift Lock Control Mod1..Mod5``) then virtual ones in keymap declaration
   order, is printed when *all* bits of its canonical mapping are present in the
   mask, i.e. ``(mask & mapping) == mapping``.  That is why ``Mod5`` and the
   virtual ``LevelThree`` (mapping ``Mod5``) both appear in
   ``[ Lock Mod5 LevelThree ]``: ``Lock`` and ``Mod5`` are real bits of the mask,
   ``LevelThree`` is the virtual modifier whose mapping those bits satisfy.
   A modifier with mapping ``0`` (unbound, only reachable in keymap format 1)
   satisfies the test for *every* mask and is therefore printed unconditionally.

The effective mask of an entry is ``mod_mask_get_effective``: real bits pass
through, each named virtual bit is replaced by that virtual modifier's mapping,
and bits beyond ``num_mods`` (numeric masks in the keymap text) pass unchanged.
"""

# tools/how-to-type.c:27
MAX_TYPE_MAP_ENTRIES = 100

# Core keyboard modifiers.  Always present with these names and indices 0..7
# (src/xkbcomp/keymap.c, keymap_new: "Shift", "Lock", "Control", "Mod1".."Mod5").
REAL_MOD_NAMES = ("Shift", "Lock", "Control", "Mod1", "Mod2", "Mod3", "Mod4", "Mod5")
MOD_REAL_MASK_ALL = 0xFF
FIRST_VMOD_INDEX = len(REAL_MOD_NAMES)


# --------------------------------------------------------------------------
# Modifier tables
# --------------------------------------------------------------------------

def mod_table(vmods):
    """Build the keymap modifier table in *index* order.

    ``vmods``: iterable of ``(name, mapping)`` for the virtual modifiers, in keymap
    declaration order (the order of the serialized ``virtual_modifiers`` line,
    which is index order -- ``write_vmods`` enumerates by index).

    Returns ``(names, masks)``: parallel lists, index -> name / canonical mapping,
    i.e. what ``xkb_keymap_mod_get_name`` / ``xkb_keymap_mod_get_mask2`` answer
    for real (index 0..7) and virtual modifiers.
    """
    names = list(REAL_MOD_NAMES)
    masks = [1 << i for i in range(len(REAL_MOD_NAMES))]
    for name, mapping in vmods:
        names.append(name)
        masks.append(mapping)
    return names, masks


def has_unbound_vmods(named_mask, mod_masks):
    """src/xkbcomp/keymap.c:25-33 (``has_unbound_vmods``)."""
    for idx in range(FIRST_VMOD_INDEX, len(mod_masks)):
        if (named_mask & (1 << idx)) and mod_masks[idx] == 0:
            return True
    return False


def effective_mask(named_mask, mod_masks):
    """src/state.c:1613 ``mod_mask_get_effective`` + src/xkbcomp/keymap.c:36.

    ``named_mask`` is a mask of modifier *indices*; the result is a mask of
    effective bits: real bits kept, virtual bits expanded to their mapping,
    bits past the table kept verbatim (``unknown_mods``).
    """
    num_mods = len(mod_masks)
    mask = named_mask & MOD_REAL_MASK_ALL
    for idx in range(FIRST_VMOD_INDEX, num_mods):
        if named_mask & (1 << idx):
            mask |= mod_masks[idx]
    unknown = named_mask & ~((1 << num_mods) - 1)
    return mask | unknown


# --------------------------------------------------------------------------
# Key types
# --------------------------------------------------------------------------

def parse_mod_mask(text, names):
    """Parse a ``ModMaskText``-style modifier list (``none``, ``Shift+Lock``).

    ``names`` maps a modifier name to its index.  Names are real or virtual;
    the result is the named-index mask the serialized keymap spells out.
    """
    mask = 0
    text = text.strip()
    if not text or text == "none":
        return 0
    for part in text.split("+"):
        part = part.strip()
        if not part:
            continue
        try:
            mask |= 1 << names[part]
        except KeyError:
            raise ValueError("unknown modifier %r" % (part,))
    return mask


def finalize_type(name, modifiers_named, entries, level_names, mod_masks):
    """Turn a parsed ``type "NAME" { ... }`` block into a compiled key type.

    ``entries``: iterable of ``(mods_named, level, preserve_named)`` in declaration
    order, ``level`` zero-based, as spelled by the serialized ``map[...]`` /
    ``preserve[...]`` lines.

    Reproduces the finalisation loop of src/xkbcomp/keymap.c:486-511:
    ``type->mods`` and every entry's ``mods``/``preserve`` get their effective
    mask, and an entry naming an unbound virtual modifier is deactivated by
    zeroing its mask (``preserve`` stays zero, the C code ``continue``s).

    Duplicate entries (same *named* mask) are merged first, as
    src/xkbcomp/types.c:302 ``AddMapEntry`` does: the entry keeps the position of
    its first occurrence, a later ``map[]`` clobbers its level, and a later
    ``preserve[]`` overrides its preserve mask (``preserve[..]= none`` clears it).
    """
    merged = []
    for mods_named, level, preserve_named in entries:
        for slot in merged:
            if slot[0] == mods_named:
                slot[1] = level
                if preserve_named or slot[2] == 0:
                    slot[2] = preserve_named
                break
        else:
            merged.append([mods_named, level, preserve_named])

    out_entries = []
    for mods_named, level, preserve_named in merged:
        if has_unbound_vmods(mods_named, mod_masks):
            out_entries.append({
                "mods_named": mods_named,
                "mods": 0,
                "level": level,
                "preserve_named": preserve_named,
                "preserve": 0,
                "deactivated": True,
            })
            continue
        out_entries.append({
            "mods_named": mods_named,
            "mods": effective_mask(mods_named, mod_masks),
            "level": level,
            "preserve_named": preserve_named,
            "preserve": effective_mask(preserve_named, mod_masks),
            "deactivated": False,
        })

    # src/xkbcomp/types.c:816 ``type->num_levels = def->num_levels``: only entry
    # levels count, level names never extend the level count.
    num_levels = 1
    for entry in out_entries:
        if entry["level"] + 1 > num_levels:
            num_levels = entry["level"] + 1

    return {
        "name": name,
        "modifiers_named": modifiers_named,
        "modifiers": effective_mask(modifiers_named, mod_masks),
        "entries": out_entries,
        "level_names": list(level_names),
        "num_levels": num_levels,
    }


def entry_is_active(entry):
    """src/keymap.h:672-681."""
    return entry["mods_named"] == 0 or entry["mods"] != 0


def num_levels(key_type):
    """src/keymap.h:661 ``XkbKeyNumLevels`` (``type->num_levels``)."""
    return key_type["num_levels"]


# --------------------------------------------------------------------------
# Rule 1: the masks a level is reached with
# --------------------------------------------------------------------------

def mods_for_level(key_type, level, masks_size=MAX_TYPE_MAP_ENTRIES):
    """src/keymap.c:493-553 ``xkb_keymap_key_get_mods_for_level``.

    Returns the masks in entry-declaration order.  The empty mask is prepended
    for level 0 unless an active entry already maps the empty mask to level 0.
    """
    if level < 0 or level >= key_type["num_levels"]:
        return []

    masks = []
    entries = key_type["entries"]

    if level == 0:
        empty_mapped = False
        for entry in entries:
            if len(masks) >= masks_size:
                break
            if entry_is_active(entry) and entry["mods"] == 0:
                empty_mapped = True
                break
        if not empty_mapped and len(masks) < masks_size:
            masks.append(0)

    for entry in entries:
        if len(masks) >= masks_size:
            break
        if entry_is_active(entry) and entry["level"] == level:
            masks.append(entry["mods"])

    return masks


# --------------------------------------------------------------------------
# Rule 3: printing
# --------------------------------------------------------------------------

def format_modifiers(mask, mod_names, mod_masks):
    """tools/how-to-type.c:521-537 ``print_combo``'s ``[ ... ]`` cell.

    Every modifier index is considered, in index order; a modifier is named when
    its whole canonical mapping is contained in ``mask``.
    """
    parts = []
    for idx, mod_mask in enumerate(mod_masks):
        if (mask & mod_mask) != mod_mask:
            continue
        parts.append(mod_names[idx] + " ")
    return "[ " + "".join(parts) + "]"


def level_cells(key_type, level, mod_names, mod_masks,
                masks_size=MAX_TYPE_MAP_ENTRIES):
    """The MODIFIERS cells how-to-type prints for one (key, layout, level)."""
    return [format_modifiers(m, mod_names, mod_masks)
            for m in mods_for_level(key_type, level, masks_size)]


# --------------------------------------------------------------------------
# Convenience: the minimal type parser, for tests and for reuse by the tool
# --------------------------------------------------------------------------

def parse_type_block(text, names, mod_masks):
    """Parse one serialized ``type "NAME" { ... };`` block.

    ``text`` is the block as ``xkbcli compile-keymap`` writes it, e.g.::

        type "FOUR_LEVEL_ALPHABETIC" {
            modifiers= Shift+Lock+LevelThree;
            map[Shift]= 2;
            map[Lock]= 2;
            ...
            level_name[1]= "Base";
        };

    Statements are applied in source order like the C parser
    (src/xkbcomp/types.c: ``SetMapEntry`` 338-377, ``AddPreserve`` 379-430):

    * a ``map[]``/``preserve[]`` mask is clamped to the name's ``modifiers=``
      mask *as seen so far* (``entry.mods.mods &= type->mods``),
    * a ``preserve[]`` value is clamped to its entry's mask,
    * ``preserve[]`` before ``map[]`` creates an entry at level 1.

    ``names``: modifier name -> index.  Returns a finalised key type.
    """
    head, sep, _ = text.partition("{")
    if not sep:
        raise ValueError("not a type block")
    name = head.split('"')[1]
    body = text.split("{", 1)[1].rsplit("}", 1)[0]

    type_mods = 0
    state = []          # [mods_named, level, preserve_named]
    level_names = []

    def slot_for(mods_named, create_level):
        for slot in state:
            if slot[0] == mods_named:
                return slot
        slot = [mods_named, create_level, 0]
        state.append(slot)
        return slot

    for raw in body.split(";"):
        line = raw.strip()
        if not line:
            continue
        key, sep, value = line.partition("=")
        key = key.strip()
        value = value.strip()
        if not sep:
            continue
        if key == "modifiers":
            type_mods = parse_mod_mask(value.strip('"'), names)
        elif key.startswith("map["):
            mods_named = parse_mod_mask(key[4:-1], names) & type_mods
            slot_for(mods_named, int(value) - 1)[1] = int(value) - 1
        elif key.startswith("preserve["):
            mods_named = parse_mod_mask(key[9:-1], names) & type_mods
            preserve_named = parse_mod_mask(value, names) & mods_named
            slot_for(mods_named, 0)[2] = preserve_named
        elif key.startswith("level_name["):
            level_names.append(int(key[11:-1]) - 1)
        # other fields (e.g. "map" without index) are not part of the column
    return finalize_type(name, type_mods, [tuple(s) for s in state],
                         level_names, mod_masks)
