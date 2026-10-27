#!/usr/bin/env python3
"""Seat harness (NOT part of the deliverable): differential of ``mods.py`` against
libxkbcommon 1.13.2.

Two layers, both over the same serialized keymaps:

* ``types``  -- exhaustive: every (keycode, layout, level) of every keymap.  Ground
  truth from the pinned shared library (``xkb_keymap_key_get_mods_for_level``,
  ``xkb_keymap_mod_get_name/mask2`` -- the very functions how-to-type.c calls),
  model from ``mods.py`` fed with *text-parsed* key types.
* ``judge``  -- end-to-end against the real ``xkbcli-how-to-type`` binary: for a
  deterministic sample of keysyms per keymap the printed rows
  (keycode, key name, layout#, level#, MODIFIERS cell) must match the model's.

Only reads: the library, the keymap files, the two pinned binaries.  Writes only
under --work and the receipt path given on the command line.
"""

import ctypes
import hashlib
import os
import re
import subprocess
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import mods  # noqa: E402

JUDGE = "/usr/lib/xkbcommon/xkbcli-how-to-type"
COMPILE = "/usr/lib/xkbcommon/xkbcli-compile-keymap"
LIBPATH = "/usr/lib/libxkbcommon.so.0.13.2"

CLEAN_PATH = "/usr/bin:/usr/lib/xkbcommon"


# ---------------------------------------------------------------- libxkbcommon

class Lib:
    def __init__(self, path):
        self.l = ctypes.CDLL(path)
        L = self.l
        L.xkb_context_new.restype = ctypes.c_void_p
        L.xkb_context_new.argtypes = [ctypes.c_int]
        L.xkb_keymap_new_from_string.restype = ctypes.c_void_p
        L.xkb_keymap_new_from_string.argtypes = [
            ctypes.c_void_p, ctypes.c_char_p, ctypes.c_int, ctypes.c_int]
        L.xkb_keymap_min_keycode.restype = ctypes.c_uint32
        L.xkb_keymap_min_keycode.argtypes = [ctypes.c_void_p]
        L.xkb_keymap_max_keycode.restype = ctypes.c_uint32
        L.xkb_keymap_max_keycode.argtypes = [ctypes.c_void_p]
        L.xkb_keymap_key_get_name.restype = ctypes.c_char_p
        L.xkb_keymap_key_get_name.argtypes = [ctypes.c_void_p, ctypes.c_uint32]
        L.xkb_keymap_num_layouts_for_key.restype = ctypes.c_uint32
        L.xkb_keymap_num_layouts_for_key.argtypes = [ctypes.c_void_p,
                                                     ctypes.c_uint32]
        L.xkb_keymap_layout_get_name.restype = ctypes.c_char_p
        L.xkb_keymap_layout_get_name.argtypes = [ctypes.c_void_p,
                                                 ctypes.c_uint32]
        L.xkb_keymap_num_levels_for_key.restype = ctypes.c_uint32
        L.xkb_keymap_num_levels_for_key.argtypes = [ctypes.c_void_p,
                                                    ctypes.c_uint32,
                                                    ctypes.c_uint32]
        L.xkb_keymap_key_get_syms_by_level.restype = ctypes.c_int
        L.xkb_keymap_key_get_syms_by_level.argtypes = [
            ctypes.c_void_p, ctypes.c_uint32, ctypes.c_uint32, ctypes.c_uint32,
            ctypes.POINTER(ctypes.POINTER(ctypes.c_uint32))]
        L.xkb_keymap_key_get_mods_for_level.restype = ctypes.c_size_t
        L.xkb_keymap_key_get_mods_for_level.argtypes = [
            ctypes.c_void_p, ctypes.c_uint32, ctypes.c_uint32, ctypes.c_uint32,
            ctypes.POINTER(ctypes.c_uint32), ctypes.c_size_t]
        L.xkb_keymap_num_mods.restype = ctypes.c_uint32
        L.xkb_keymap_num_mods.argtypes = [ctypes.c_void_p]
        L.xkb_keymap_mod_get_name.restype = ctypes.c_char_p
        L.xkb_keymap_mod_get_name.argtypes = [ctypes.c_void_p, ctypes.c_uint32]
        L.xkb_keymap_mod_get_mask2.restype = ctypes.c_uint32
        L.xkb_keymap_mod_get_mask2.argtypes = [ctypes.c_void_p, ctypes.c_uint32]
        L.xkb_keysym_to_lower.restype = ctypes.c_uint32
        L.xkb_keysym_to_lower.argtypes = [ctypes.c_uint32]
        L.xkb_keysym_to_upper.restype = ctypes.c_uint32
        L.xkb_keysym_to_upper.argtypes = [ctypes.c_uint32]
        self.ctx = L.xkb_context_new(2)  # XKB_CONTEXT_NO_ENVIRONMENT_NAMES

    def keymap(self, text, fmt=2):
        data = text.encode()
        km = self.l.xkb_keymap_new_from_string(self.ctx, data, fmt, 0)
        if not km:
            raise RuntimeError("keymap parse failed")
        return km

    def mods_table(self, km):
        n = self.l.xkb_keymap_num_mods(km)
        names = [self.l.xkb_keymap_mod_get_name(km, i).decode() for i in range(n)]
        masks = [self.l.xkb_keymap_mod_get_mask2(km, i) for i in range(n)]
        return names, masks

    def gt(self, km):
        """[(keycode, keyname, layout, layoutname, level, [masks])]"""
        L = self.l
        out = []
        for kc in range(L.xkb_keymap_min_keycode(km),
                        L.xkb_keymap_max_keycode(km) + 1):
            name = L.xkb_keymap_key_get_name(km, kc)
            if not name:
                continue
            name = name.decode()
            for layout in range(L.xkb_keymap_num_layouts_for_key(km, kc)):
                lname = L.xkb_keymap_layout_get_name(km, layout)
                lname = lname.decode() if lname else "?"
                for level in range(L.xkb_keymap_num_levels_for_key(km, kc,
                                                                   layout)):
                    buf = (ctypes.c_uint32 * 100)()
                    n = L.xkb_keymap_key_get_mods_for_level(
                        km, kc, layout, level, buf, 100)
                    out.append((kc, name, layout, lname, level,
                                list(buf[:n])))
        return out


# ---------------------------------------------------------------- text parsing

RE_KEYSYM = re.compile(r"^[A-Za-z0-9_+\-]+$")


def _split_depth(text, sep=","):
    """Split on ``sep`` at bracket depth 0."""
    parts, depth, cur = [], 0, []
    for ch in text:
        if ch in "[{(":
            depth += 1
        elif ch in "]})":
            depth -= 1
        if ch == sep and depth == 0:
            parts.append("".join(cur))
            cur = []
        else:
            cur.append(ch)
    parts.append("".join(cur))
    return parts


def _match_brace(text, open_index, opener="{", closer="}"):
    """Index of the closer matching text[open_index] (== opener)."""
    depth = 0
    for i in range(open_index, len(text)):
        ch = text[i]
        if ch == opener:
            depth += 1
        elif ch == closer:
            depth -= 1
            if depth == 0:
                return i
    raise RuntimeError("unbalanced %r" % opener)


def _sections(text):
    """{section-name: body} for the four xkb sections, brace matched."""
    out = {}
    for m in re.finditer(
            r"(xkb_keycodes|xkb_types|xkb_compatibility|xkb_symbols)"
            r'(\s*"[^"]*")?\s*\{', text):
        open_index = text.index("{", m.start())
        close = _match_brace(text, open_index)
        out[m.group(1)] = text[open_index + 1:close]
    return out


def _parse_levels(content):
    levels = []
    for item in _split_depth(content):
        item = item.strip()
        if not item:
            continue
        if item.startswith("{"):
            syms = [s.strip() for s in _split_depth(item.strip("{} "))]
            levels.append([s for s in syms if s])
        else:
            levels.append([item])
    return levels


def _parse_key_body(body):
    key = {"groups": [], "type": None, "types": {}, "virtualmods": []}
    vm = re.search(r"virtualMods=\s*([^,]+),", body)
    if vm:
        key["virtualmods"] = [v.strip() for v in vm.group(1).split("+")]
    tm = re.search(r'\btype=\s*"([^"]+)"', body)
    if tm:
        key["type"] = tm.group(1)
    for tgi in re.finditer(r'type\[(\d+)\]=\s*"([^"]+)"', body):
        key["types"][int(tgi.group(1)) - 1] = tgi.group(2)

    groups = []
    if "symbols[" in body:
        for gm in re.finditer(r"symbols\[(\d+)\]=\s*\[", body):
            open_index = body.index("[", gm.start() + 8, gm.end())
            close = _match_brace(body, open_index, "[", "]")
            groups.append(_parse_levels(body[open_index + 1:close]))
    else:
        open_index = body.find("[")
        if open_index >= 0:
            close = _match_brace(body, open_index, "[", "]")
            groups.append(_parse_levels(body[open_index + 1:close]))
    key["groups"] = groups
    return key


def parse_keymap(text):
    """Minimal parse of the serialized keymap: the parts the MODIFIERS column needs."""
    keys = {}          # name -> dict(modmap, groups=[[syms...]], type, types)
    kc_by_name = {}
    modmap = {}        # key name -> [real modifier names]
    vmods = []         # [(name, explicit mapping | None)] in index order
    types = {}         # name -> {modifiers, entries, level_names}
    group_names = {}
    interprets = []    # (sym, match, mods_text, level_one_only, vmod | None)

    sections = _sections(text)

    for line in sections.get("xkb_keycodes", "").splitlines():
        line = line.strip()
        km = re.match(r"<([^>\s]+)>\s*=\s*(\d+);", line)
        if km:
            kc_by_name[km.group(1)] = int(km.group(2))
            continue
        am = re.match(r"alias\s+<([^>\s]+)>\s*=\s*<([^>\s]+)>;",
                      line)
        if am:
            kc_by_name[am.group(1)] = ("alias", am.group(2))
    for nm in list(kc_by_name):
        v = kc_by_name[nm]
        if isinstance(v, tuple):
            kc_by_name[nm] = kc_by_name.get(v[1])

    section = sections.get("xkb_types", "")
    vm = re.search(r"virtual_modifiers\s+([^;]+);", section)
    if vm:
        for item in vm.group(1).split(","):
            item = item.strip()
            if not item:
                continue
            if "=" in item:
                name, val = item.split("=", 1)
                vmods.append((name.strip(), parse_real_mask(val.strip())))
            else:
                vmods.append((item, None))
    for tm in re.finditer(r'type\s+"([^"]+)"\s*\{', section):
        open_index = section.index("{", tm.start())
        close = _match_brace(section, open_index)
        tname = tm.group(1)
        tbody = section[open_index + 1:close]
        modifiers = None
        entries = []
        level_names = set()
        for raw in tbody.split(";"):
            line = raw.strip()
            if not line:
                continue
            key, _, value = line.partition("=")
            key, value = key.strip(), value.strip()
            if key == "modifiers":
                modifiers = value
            elif key.startswith("map["):
                entries.append([key[4:-1], int(value) - 1, None])
            elif key.startswith("preserve["):
                pmods = key[9:-1]
                for e in entries:
                    if e[0] == pmods and e[2] is None:
                        e[2] = value
                        break
                else:
                    raise RuntimeError("preserve without map: " + line)
            elif key.startswith("level_name["):
                level_names.add(int(key[11:-1]) - 1)
        if modifiers is None:
            raise RuntimeError("type without modifiers: " + tname)
        types[tname] = {"modifiers": modifiers,
                        "entries": [tuple(e) for e in entries],
                        "level_names": sorted(level_names),
                        "block": 'type "%s" {\n%s\n}' % (tname, tbody)}

    section = sections.get("xkb_compatibility", "")
    for im in re.finditer(r"interpret\s+([^\s{]+)\s*\{", section):
        open_index = section.index("{", im.start())
        close = _match_brace(section, open_index)
        spec = im.group(1)
        ibody = section[open_index + 1:close]
        sym = spec.split("+")[0]
        match, imods = "AnyOrNone", ""
        mm2 = re.match(r"([^+]+)\+(Exactly|AnyOf|NoneOf|AllOf)\((.*)\)$", spec)
        if mm2:
            sym, kind, imods = mm2.group(1), mm2.group(2), mm2.group(3)
            match = {"Exactly": "Exactly", "AnyOf": "Any",
                     "NoneOf": "None", "AllOf": "All"}[kind]
        level_one_only = "useModMapMods=level1" in ibody.replace(" ", "")
        vmod = None
        vmm = re.search(r"virtualModifier=\s*(\w+);", ibody)
        if vmm:
            vmod = vmm.group(1)
        interprets.append((sym, match, imods, level_one_only, vmod))

    section = sections.get("xkb_symbols", "")
    for nm in re.finditer(r'name\[(\d+)\]="((?:[^"\\]|\\.)*)";', section):
        group_names[int(nm.group(1)) - 1] = nm.group(2).replace('\\"', '"')
    for mm in re.finditer(r"modifier_map\s+(\w+)\s*\{([^}]*)\};", section):
        for nm in re.findall(r"<([^>\s]+)>", mm.group(2)):
            modmap.setdefault(nm, []).append(mm.group(1))
    for km in re.finditer(r"key\s+<([^>\s]+)>\s*\{", section):
        open_index = section.index("{", km.start())
        close = _match_brace(section, open_index)
        keys[km.group(1)] = _parse_key_body(section[open_index + 1:close])

    return {"keys": keys, "kc_by_name": kc_by_name, "modmap": modmap,
            "vmods": vmods, "types": types, "group_names": group_names,
            "interprets": interprets}


def parse_real_mask(text):
    """``write_vmods`` prints an explicit vmod mapping with ModMaskText(MOD_REAL).

    ``none`` is what write_vmods emits for an explicit zero mapping; it keeps the
    virtual modifier unbound instead of letting format 2 assign it a canonical bit.
    """
    mask = 0
    if text == "none":
        return 0
    if text.startswith("0x") or text.startswith("0X"):
        return int(text, 16)
    if text.isdigit():
        return int(text)
    for part in text.split("+"):
        part = part.strip()
        if part in mods.REAL_MOD_NAMES:
            mask |= 1 << mods.REAL_MOD_NAMES.index(part)
        else:
            raise RuntimeError("bad real mask %r" % text)
    return mask


def build_tables(parsed, fmt_v2=True):
    """Derive (mod_names, mod_masks) from the serialized text alone."""
    vmod_entries = parsed["vmods"]
    name_to_vidx = {name: mods.FIRST_VMOD_INDEX + i
                    for i, (name, _) in enumerate(vmod_entries)}
    vmod_masks = {}
    for name, explicit in vmod_entries:
        vmod_masks[name] = explicit if explicit is not None else 0

    # implicit mapping: OR of key modmap over keys carrying the vmod
    matched_vmods = {name: 0 for name, _ in vmod_entries}
    for kname, key in parsed["keys"].items():
        vmodmap = set(key["virtualmods"])
        for sym, match, imods, level_one_only, vmod in parsed["interprets"]:
            if vmod is None:
                continue
            hit = False
            for gindex, group in enumerate(key["groups"]):
                for level, syms in enumerate(group):
                    if sym not in syms:
                        continue
                    if level_one_only and level != 0:
                        continue
                    hit = True
                    break
                if hit:
                    break
            if hit:
                vmodmap.add(vmod)
        if not vmodmap:
            continue
        realmap = 0
        for modname in parsed["modmap"].get(kname, []):
            realmap |= 1 << mods.REAL_MOD_NAMES.index(modname)
        for vname in vmodmap:
            if vname in matched_vmods:
                matched_vmods[vname] |= realmap

    for name, explicit in vmod_entries:
        if explicit is not None:
            continue
        if matched_vmods[name]:
            vmod_masks[name] = matched_vmods[name]
        elif fmt_v2:
            vmod_masks[name] = 1 << name_to_vidx[name]
        # else: stays 0 (unbound)

    ordered = [(name, vmod_masks[name]) for name, _ in vmod_entries]
    names, masks = mods.mod_table(ordered)
    name_to_index = {n: i for i, n in enumerate(names)}
    return names, masks, name_to_index


def build_json_types(parsed, names, masks, name_to_index):
    """Compile every serialized type block with mods.parse_type_block."""
    out = {}
    for tname, t in parsed["types"].items():
        out[tname] = mods.parse_type_block(t["block"], name_to_index, masks)
    return out


# ------------------------------------------------------- key type resolution
NO_SYMBOL = "NoSymbol"
KP_SPACE = 0xFF80
KP_EQUAL = 0xFFBD


class KeysymClass:
    """xkb_keysym_is_lower / is_upper_or_title / is_keypad (src/keysym-case-mappings.c:623-660)."""

    def __init__(self, lib):
        self.lib = lib

    def is_lower(self, value):
        has_upper = self.lib.l.xkb_keysym_to_upper(value) != value
        has_lower = self.lib.l.xkb_keysym_to_lower(value) != value
        return has_upper and not has_lower

    def is_upper_or_title(self, value):
        return self.lib.l.xkb_keysym_to_lower(value) != value

    @staticmethod
    def is_keypad(value):
        return KP_SPACE <= value <= KP_EQUAL


def keysym_value(text, keymap_tables):
    return keymap_tables.get(text)


def find_automatic_type(width, syms, kc, keysym_class):
    """src/xkbcomp/symbols.c:1593-1638 FindAutomaticType."""
    def get(index):
        if index >= width or not syms[index]:
            return 0
        return syms[index]

    if width == 1 or width <= 0:
        return "ONE_LEVEL"
    sym0, sym1 = get(0), get(1)
    if width == 2:
        if keysym_class.is_lower(sym0) and keysym_class.is_upper_or_title(sym1):
            return "ALPHABETIC"
        if keysym_class.is_keypad(sym0) or keysym_class.is_keypad(sym1):
            return "KEYPAD"
        return "TWO_LEVEL"
    if width <= 4:
        if keysym_class.is_lower(sym0) and keysym_class.is_upper_or_title(sym1):
            sym2, sym3 = get(2), (get(3) if width == 4 else 0)
            if keysym_class.is_lower(sym2) and keysym_class.is_upper_or_title(sym3):
                return "FOUR_LEVEL_ALPHABETIC"
            return "FOUR_LEVEL_SEMIALPHABETIC"
        if keysym_class.is_keypad(sym0) or keysym_class.is_keypad(sym1):
            return "FOUR_LEVEL_KEYPAD"
        return "FOUR_LEVEL"
    return None


# ---------------------------------------------------------------- compile/run

def run_compile(layout, variant, options, work, env_home):
    args = [COMPILE, "--layout", layout]
    if variant:
        args += ["--variant", variant]
    if options:
        args += ["--options", options]
    env = {"PATH": CLEAN_PATH, "HOME": env_home,
           "XDG_CONFIG_HOME": os.path.join(env_home, ".config")}
    p = subprocess.run(args, capture_output=True, env=env, cwd=work,
                       timeout=120)
    if p.returncode != 0:
        raise RuntimeError("compile failed for %s/%s/%s: %s"
                           % (layout, variant, options,
                              p.stderr.decode()[:400]))
    return p.stdout.decode()


RE_ROW = re.compile(r"^(\d+)\s+(\S+)\s+(\d+)\s+(.*?)\s+(\d+)\s+(\[.*\])$")


def run_judge(keymap_path, arg, env_home):
    env = {"PATH": CLEAN_PATH, "HOME": env_home,
           "XDG_CONFIG_HOME": os.path.join(env_home, ".config")}
    p = subprocess.run([JUDGE, "--keymap=" + keymap_path, "--disable-compose",
                        "--keysym", arg],
                       capture_output=True, env=env, timeout=60)
    rows = []
    for line in p.stdout.decode().splitlines():
        m = RE_ROW.match(line)
        if m:
            rows.append((int(m.group(1)), m.group(2), int(m.group(3)),
                         int(m.group(5)), m.group(6)))
    return rows, p.stdout.decode(), p.stderr.decode(), p.returncode


# ---------------------------------------------------------------- keysym table

KEYSYMS_HEADER = "/usr/include/xkbcommon/xkbcommon-keysyms.h"
RE_KS_DEFINE = re.compile(r"^#define\s+XKB_KEY_(\w+)\s+(0x[0-9a-fA-F]+|\d+)")


def load_keysyms(path=KEYSYMS_HEADER):
    table = {}
    with open(path, "r", encoding="utf-8", errors="replace") as fh:
        for line in fh:
            m = RE_KS_DEFINE.match(line)
            if m:
                table[m.group(1)] = int(m.group(2), 0)
    return table


RE_KEYSYM_U = re.compile(r"^U([0-9A-Fa-f]{4,6})$")


def sym_value(text, table):
    if text is None:
        return None
    text = text.strip()
    if text == NO_SYMBOL:
        return 0
    if text.startswith("0x") or text.startswith("0X"):
        return int(text, 16)
    m = RE_KEYSYM_U.match(text)
    if m:
        # KeysymText spells Unicode keysyms as "U<hex>"; xkb_keysym_from_name
        # maps them to 0x01000000 + code point.
        return 0x01000000 + int(m.group(1), 16)
    return table.get(text)


# ---------------------------------------------------------------- main driver

CORPUS = [
    ("host-sample-br-compose-caps", "br", None, "compose:caps"),
    ("us", "us", None, None),
    ("us-intl", "us", "intl", None),
    ("us-dvorak", "us", "dvorak", None),
    ("us-colemak", "us", "colemak", None),
    ("us-altgr-intl", "us", "altgr-intl", None),
    ("br", "br", None, None),
    ("de", "de", None, None),
    ("de-nodeadkeys", "de", "nodeadkeys", None),
    ("de-neo", "de", "neo", None),
    ("fr", "fr", None, None),
    ("fr-oss", "fr", "oss", None),
    ("ru", "ru", None, None),
    ("us+ru", "us,ru", None, None),
    ("fr+us", "fr,us", None, None),
    ("de+ru+us", "de,ru,us", None, None),
    ("ch-fr", "ch", "fr", None),
    ("ch-de", "ch", "de", None),
    ("no", "no", None, None),
    ("dk", "dk", None, None),
    ("fi", "fi", None, None),
    ("se", "se", None, None),
    ("is", "is", None, None),
    ("gr", "gr", None, None),
    ("tr", "tr", None, None),
    ("pl", "pl", None, None),
    ("cz", "cz", None, None),
    ("hu", "hu", None, None),
    ("ro", "ro", None, None),
    ("hr", "hr", None, None),
    ("si", "si", None, None),
    ("sk", "sk", None, None),
    ("lt", "lt", None, None),
    ("lv", "lv", None, None),
    ("ee", "ee", None, None),
    ("pt", "pt", None, None),
    ("es", "es", None, None),
    ("latam", "latam", None, None),
    ("it", "it", None, None),
    ("gb", "gb", None, None),
    ("ca-fr", "ca", "fr", None),
    ("in", "in", None, None),
    ("jp", "jp", None, None),
    ("kr", "kr", None, None),
    ("bg", "bg", None, None),
    ("br+terminate", "br", None, "compose:caps,terminate:ctrl_alt_bksp"),
    ("us+terminate", "us", None, "terminate:ctrl_alt_bksp"),
    ("us+kpdl-dot", "us", None, "kpdl:dot"),
    ("se+kpdl-comma", "se", None, "kpdl:comma"),
    ("us+level3-ralt", "us", None, "level3:ralt_switch"),
    ("de+both", "de", None, "terminate:ctrl_alt_bksp,kpdl:dot"),
]


def model_types(parsed, type_table, keysym_class, syms_table):
    """key name -> [KeyType per group] following FindTypeForGroup."""
    out = {}
    for kname, key in parsed["keys"].items():
        groups = []
        for gindex, group in enumerate(key["groups"]):
            width = len(group)
            explicit = key["types"].get(gindex, key["type"])
            tname = explicit
            if tname is None:
                values = []
                for level_syms in group:
                    if len(level_syms) == 1:
                        value = sym_value(level_syms[0], syms_table)
                        values.append(value if value is not None else 0)
                    else:
                        # several syms at one level: FindAutomaticType's GET_SYM
                        # takes the first one, and multi-sym levels never reach
                        # the lower/upper predicates in practice
                        values.append(0)
                tname = find_automatic_type(width, values, kname, keysym_class)
            if tname is None or tname not in type_table:
                tname = "ONE_LEVEL"
            groups.append(type_table[tname])
        out[kname] = groups
    return out


def compare_keymap(lib, text, keysym_class, syms_table, stats, bad,
                   fmt_v2=True):
    km = lib.keymap(text)
    gt_names, gt_masks = lib.mods_table(km)
    parsed = parse_keymap(text)
    names, masks, name_to_index = build_tables(parsed, fmt_v2=fmt_v2)
    stats["keymaps"] += 1
    if (gt_names, gt_masks) != (names, masks):
        stats["table_mismatch"] += 1
        bad.append(("TABLE", parsed.get("_id"),
                    "gt=%r/%r text=%r/%r" % (gt_names, gt_masks, names, masks)))
    type_table = build_json_types(parsed, names, masks, name_to_index)
    key_types = model_types(parsed, type_table, keysym_class, syms_table)

    gt = lib.gt(km)
    stats["rows"] += len(gt)
    stats["keys"] += len({(row[0]) for row in gt})
    gt_by_key = {}
    for kc, kname, layout, lname, level, gmasks in gt:
        gt_by_key.setdefault((kc, kname, layout), []).append((level, gmasks))
        cells = [mods.format_modifiers(m, names, masks) for m in gmasks]
        gtcells = [mods.format_modifiers(m, gt_names, gt_masks) for m in gmasks]
        if cells != gtcells:
            stats["cell_mismatch"] += 1
            bad.append(("CELL", kname, layout, level, cells, gtcells))
        stats["cells"] += len(cells)

    # model side: every key, layout, level
    for kc, kname, layout, lname, level, gmasks in gt:
        groups = key_types.get(kname)
        if groups is None:
            stats["missing_key"] += 1
            bad.append(("MISSING-KEY", kname))
            continue
        if layout >= len(groups):
            stats["layout_mismatch"] += 1
            bad.append(("LAYOUTS", kname, layout, len(groups)))
            continue
        ktype = groups[layout]
        if mods.num_levels(ktype) != lib.l.xkb_keymap_num_levels_for_key(
                km, kc, layout):
            stats["nlevels_mismatch"] += 1
            bad.append(("NLEVELS", kname, layout, ktype["name"],
                        mods.num_levels(ktype),
                        lib.l.xkb_keymap_num_levels_for_key(km, kc, layout)))
        predicted = mods.mods_for_level(ktype, level)
        if predicted != gmasks:
            stats["mask_mismatch"] += 1
            used = set()
            for group in key_types.values():
                for t in group:
                    used.add(t["name"])
            stats["_types_used"] = used
            bad.append(("MASK", kname, layout, level, ktype["name"],
                        predicted, gmasks))
        stats["type_names"].add(ktype["name"])
    return parsed, type_table, key_types, names, masks


def judge_layer(lib, work, text, parsed, key_types, names, masks, syms_table,
                stats, bad, env_home, sample):
    path = os.path.join(work, "judge-keymap.xkb")
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(text)

    single = []
    for kname, key in parsed["keys"].items():
        for group in key["groups"]:
            for level, syms in enumerate(group):
                if len(syms) == 1 and syms[0] != NO_SYMBOL:
                    single.append(syms[0])
    single = sorted(set(single))
    if sample > 0 and len(single) > sample:
        step = len(single) / float(sample)
        picked = [single[int(i * step)] for i in range(sample)]
    else:
        picked = single

    for sym in picked:
        rows_judge, out, err, rc = run_judge(path, sym, env_home)
        if rc != 0:
            stats["judge_rc"] += 1
            bad.append(("JUDGE-RC", sym, rc, err.strip()[:120]))
            continue
        target = syms_table.get(sym)
        rows_model = []
        for kname, key in sorted(parsed["keys"].items(),
                                 key=lambda kv: parsed["kc_by_name"].get(kv[0])
                                 or 0):
            kc = parsed["kc_by_name"].get(kname)
            if kc is None:
                continue
            for layout, group in enumerate(key["groups"]):
                if layout >= len(key_types.get(kname, [])):
                    continue
                ktype = key_types[kname][layout]
                for level, syms in enumerate(group):
                    if len(syms) != 1:
                        continue
                    if target is not None:
                        if sym_value(syms[0], syms_table) != target:
                            continue
                    elif syms[0] != sym:
                        continue
                    for cell in mods.level_cells(ktype, level, names, masks):
                        rows_model.append((kc, kname, layout + 1, level + 1,
                                           cell))
        stats["judge_runs"] += 1
        stats["judge_rows"] += len(rows_judge)
        if rows_model != rows_judge:
            stats["judge_mismatch"] += 1
            bad.append(("JUDGE", sym, rows_model, rows_judge))


def main(argv):
    work = argv[1]
    receipt = argv[2]
    sample = int(argv[3]) if len(argv) > 3 else 20
    os.makedirs(work, exist_ok=True)
    env_home = os.path.join(work, "home")
    os.makedirs(os.path.join(env_home, ".config"), exist_ok=True)
    env_home = os.path.realpath(env_home)

    lib = Lib(LIBPATH)
    keysym_class = KeysymClass(lib)
    syms_table = load_keysyms()

    stats = {"keymaps": 0, "rows": 0, "cells": 0, "table_mismatch": 0,
             "cell_mismatch": 0, "mask_mismatch": 0, "nlevels_mismatch": 0,
             "layout_mismatch": 0, "missing_key": 0, "judge_runs": 0,
             "judge_rows": 0, "judge_mismatch": 0, "judge_rc": 0,
             "keys": 0,
             "type_names": set()}
    bad = []
    skipped = []
    lines = []

    t0 = time.time()
    for ident, layout, variant, options in CORPUS:
        try:
            text = run_compile(layout, variant, options, work, env_home)
        except Exception as exc:  # noqa: BLE001
            skipped.append((ident, str(exc)[:200]))
            continue
        km_path = os.path.join(work, ident + ".xkb")
        with open(km_path, "w", encoding="utf-8") as fh:
            fh.write(text)
        try:
            parsed, type_table, key_types, names, masks = compare_keymap(
                lib, text, keysym_class, syms_table, stats, bad)
        except Exception as exc:  # noqa: BLE001
            bad.append(("PARSE", ident, repr(exc)[:300]))
            continue
        judge_layer(lib, work, text, parsed, key_types, names, masks,
                    syms_table, stats, bad, env_home, sample)
        used = sorted({t["name"] for group in key_types.values() for t in group})
        lines.append("%-30s layout=%-8s variant=%-12s options=%-30s types=%s"
                     % (ident, layout, variant or "-", options or "-",
                        ",".join(used)))
        for exc in bad:
            if exc[0] in ("TABLE", "PARSE", "CELL", "MASK", "NLEVELS",
                          "JUDGE"):
                break

    elapsed = time.time() - t0
    out = []
    out.append("# mods.py differential vs libxkbcommon 1.13.2 / xkbcli-how-to-type")
    out.append("# library: %s sha256=%s" % (LIBPATH, sha256(LIBPATH)))
    out.append("# judge:   %s sha256=%s" % (JUDGE, sha256(JUDGE)))
    out.append("# compile: %s sha256=%s" % (COMPILE, sha256(COMPILE)))
    out.append("# corpus: %d keymaps compiled (%d skipped), %d rows compared, "
               "%d cells, %d judge runs, %.1fs"
               % (stats["keymaps"], len(skipped), stats["rows"],
                  stats["cells"], stats["judge_runs"], elapsed))
    out.append("")
    for line in lines:
        out.append(line)
    if skipped:
        out.append("")
        out.append("## skipped")
        for ident, err in skipped:
            out.append("%-30s %s" % (ident, err))
    out.append("")
    out.append("## type coverage (types actually used by keys)")
    out.append(", ".join(sorted(stats["type_names"])))
    out.append("")
    out.append("## mismatch counters")
    out.append("keys compared per corpus: %d" % stats["keys"])
    for key in ("table_mismatch", "cell_mismatch", "mask_mismatch",
                "nlevels_mismatch", "layout_mismatch", "missing_key",
                "judge_mismatch", "judge_rc"):
        out.append("%-20s %d" % (key, stats[key]))
    out.append("")
    out.append("## first mismatches (max 40)")
    for exc in bad[:40]:
        out.append(repr(exc)[:600])
    out.append("")
    total = (stats["table_mismatch"] + stats["cell_mismatch"]
             + stats["mask_mismatch"] + stats["nlevels_mismatch"]
             + stats["layout_mismatch"] + stats["missing_key"]
             + stats["judge_mismatch"] + stats["judge_rc"])
    out.append("TOTAL_MISMATCHES %d" % total)
    text_out = "\n".join(out) + "\n"
    with open(receipt, "w", encoding="utf-8") as fh:
        fh.write(text_out)
    print(text_out)
    return 1 if total else 0


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


if __name__ == "__main__":
    sys.exit(main(sys.argv))
