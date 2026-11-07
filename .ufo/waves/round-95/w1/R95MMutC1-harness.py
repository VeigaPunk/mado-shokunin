#!/usr/bin/env python3
"""R95MMutC1 harness (DRAFT, not a measurement): materialise cases, label with the oracle, run
the candidate / mutants on them.  Subcommands: prepare | baseline | mutants | killers."""
import base64
import concurrent.futures as cf
import importlib.util
import json
import os
import shutil
import struct
import subprocess
import sys

S = os.environ.get("S", "/fast/scratch/hyaku/mado-r95/R95MMutC1")
ORACLE = os.path.join(S, "oracle")
PY = "/usr/bin/python3"
EMPTYBIN = os.path.join(S, "emptybin")
TOOLS = os.path.join(S, "tools")
TOOL = os.path.join(TOOLS, "mado-mimesniff.py")
ROOTDIR = os.path.join(S, "cases")
TIMEOUT = 10
M32 = 0xFFFFFFFF
WORKERS = 8


def load_candidate(path=TOOL):
    spec = importlib.util.spec_from_file_location("cand", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


cand = load_candidate()
build_cache = cand.build_cache


def ml(start, length, value, mask=None, children=()):
    return {"start": start, "length": length, "value": value, "mask": mask,
            "children": list(children)}


def u32(v):
    return struct.pack(">I", v & M32)


def find_record(blob, fields):
    """fields: u32 index -> expected value (0 start, 1 length, 3 value_length, 6 n_children)."""
    for off in range(0, len(blob) - 31, 4):
        vals = struct.unpack_from(">8I", blob, off)
        if all(vals[k] == v for k, v in fields.items()):
            return off
    raise SystemExit(f"record not found: {fields}")


# ---------------------------------------------------------------- caches

A = build_cache(
    aliases=[("text/x-old", "text/x-new")],
    parents=[("app/child", ["app/mid"]), ("app/mid", ["app/base"])],
    globs=[("*.dup", "app/child", 50), ("*.dup", "text/x-old", 50),
           ("*.two", "t/one", 50), ("*.two", "t/other", 50),
           ("*.one", "t/single", 50), ("*.amb", "app/x-a", 50), ("*.amb", "app/x-b", 50)],
    magic=[(90, "app/hi", [ml(0, 1, b"HI")]),
           (60, "app/range", [ml(2, 3, b"RG")]),
           (55, "app/masked", [ml(0, 1, b"\x10\x00", b"\xf0\x00")]),
           (50, "app/nest", [ml(0, 1, b"NE", children=[ml(4, 1, b"X"), ml(4, 1, b"Y")])]),
           (50, "app/base", [ml(0, 1, b"BA")]),
           (40, "application/x-desktop", [ml(0, 1, b"[Desktop Entry]")]),
           (30, "app/lo", [ml(0, 1, b"LO")])])

B = build_cache(magic=[(90, "app/first", [ml(0, 1, b"AA")]),
                       (50, "app/second", [ml(0, 1, b"AA")])])
C1C = build_cache(magic=[(60, "app/first", [ml(0, 1, b"AA")])])
C2C = build_cache(magic=[(60, "app/second", [ml(0, 1, b"AA")])])
NEG = build_cache(magic=[(0x80000000, "app/neg", [ml(0, 1, b"ZZ")])])
HIGH = build_cache(magic=[(0x40000000, "app/high", [ml(0, 1, b"QQ")])])
P80 = build_cache(globs=[("*.two", "t/one", 50), ("*.two", "t/other", 50)],
                  magic=[(80, "app/p80", [ml(0, 1, b"HI")])])
P79 = build_cache(globs=[("*.two", "t/one", 50), ("*.two", "t/other", 50)],
                  magic=[(79, "app/lo79", [ml(0, 1, b"PP")])])
ENDX = build_cache(magic=[(60, "app/endx", [ml(0, 1, b"A")])])
FAR = build_cache(magic=[(90, "app/far", [ml(5000, 1, b"Z")])])
WRAP = build_cache(magic=[(90, "app/wrap", [ml(10, 0xFFFFFFFB, b"Z")])])
WRAP2 = build_cache(magic=[(90, "app/wrap2", [ml(0xFFFFFFF0, 0xF, b"\x00" * 0x20)])])
M2 = build_cache(magic=[(55, "app/m2", [ml(0, 1, b"\x1f\x00", b"\xf0\x00")])])
M3 = build_cache(magic=[(55, "app/m3", [ml(0, 1, b"\x10\x00", b"\xf0\x00")])])
EQ = build_cache(magic=[(90, "app/eq", [ml(0, 1, b"AB")])])
OCT = build_cache(magic=[(90, "application/octet-stream", [ml(0, 1, b"UN")])])
SEQ = build_cache(globs=[("*.eq", "app/x-a", 50), ("*.eq", "app/hi", 50)],
                  magic=[(50, "app/hi", [ml(0, 1, b"EQ")])])
SSP = build_cache(globs=[("*.su", "app/x", 50), ("*.su", "app/y", 50)],
                  magic=[(50, "app/*", [ml(0, 1, b"SU")])])
SMS = build_cache(globs=[("*.ms", "app/x", 50), ("*.ms", "app/y", 50)],
                  magic=[(50, "appx/*", [ml(0, 1, b"MS")])])
STX = build_cache(globs=[("*.tx", "app/x", 50), ("*.tx", "app/y", 50)],
                  magic=[(50, "text/plain", [ml(0, 1, b"TX")])])
SOC = build_cache(globs=[("*.oc", "inode/x", 50), ("*.oc", "app/y", 50)],
                  magic=[(50, "application/octet-stream", [ml(0, 1, b"OC")])])
SCY = build_cache(parents=[("app/a", ["app/b"]), ("app/b", ["app/a"])],
                  globs=[("*.cy", "app/a", 50), ("*.cy", "app/y", 50)],
                  magic=[(50, "app/zzz", [ml(0, 1, b"CY")])])
SS2 = build_cache(parents=[("app/child", ["app/mid"]), ("app/mid", ["app/base"])],
                  globs=[("*.ss", "app/child", 50), ("*.ss", "app/mid", 50)],
                  magic=[(50, "app/base", [ml(0, 1, b"SS")])])
SC1 = build_cache(globs=[("*.sc", "app/child", 50), ("*.sc", "app/y", 50)],
                  magic=[(50, "app/base", [ml(0, 1, b"SC")])])
SC2 = build_cache(parents=[("app/child", ["app/base"])])
AL1 = build_cache(globs=[("*.al", "text/x-old", 50), ("*.al", "app/y", 50)],
                  magic=[(50, "text/plain", [ml(0, 1, b"AL")])])
AL2 = build_cache(aliases=[("text/x-old", "text/x-new")])


ALIAS2 = build_cache(aliases=[("app/old", "app/base")],
                     globs=[("*.ao", "app/old", 50), ("*.ao", "app/y", 50)],
                     magic=[(50, "app/base", [ml(0, 1, b"AO")])])
ALIAS3A = build_cache(globs=[("*.a2", "app/old", 50), ("*.a2", "app/y", 50)],
                      magic=[(50, "app/base", [ml(0, 1, b"A2")])])
ALIAS3B = build_cache(aliases=[("app/old", "app/base")])
NB = build_cache(globs=[("x.one", "t/single", 50)],
                 magic=[(90, "app/hi", [ml(0, 1, b"HI")])])


def patch_at(blob, off, val):
    b = bytearray(blob)
    b[off:off + 4] = u32(val)
    return bytes(b)


def magic_list_off(blob):
    return struct.unpack_from(">I", blob, 24)[0]


B1 = patch_at(A, 24, 0xFFFF0000)
B2 = patch_at(A, magic_list_off(A) + 8, 0xFFFF0000)
B3BASE = build_cache(magic=[(90, "app/first", [ml(0, 1, b"BB")]),
                            (50, "app/second", [ml(0, 1, b"CC")])])
B3 = patch_at(B3BASE, magic_list_off(B3BASE) + 8 + 12, 0xFFFF0000)
B4 = patch_at(A, 4, 0xFFFF0000)
B5 = patch_at(A, 8, 0xFFFF0000)

B6BASE = build_cache(magic=[(90, "app/page", [ml(0, 1, b"VVVV")])])
_rec6 = find_record(B6BASE, {0: 0, 1: 1, 3: 4, 6: 0})
B6 = patch_at(B6BASE, _rec6 + 16, 0x7FFFFFFF)
B6 = B6 + b"\0" * (4096 - len(B6))

B7BASE = build_cache(magic=[(90, "app/cbv", [ml(0, 1, b"VVVV", children=[ml(0, 1, b"Q")])])])
_rec7 = find_record(B7BASE, {0: 0, 1: 1, 3: 4, 6: 1})
B7 = patch_at(patch_at(B7BASE, _rec7 + 16, 0x7FFFFFFF), _rec7 + 28, 0xFFFF0000)
B7 = B7 + b"\0" * (4096 - len(B7))


def cycle_cache(mime=b"app/cycle"):
    blob = bytearray(40)

    def align():
        while len(blob) % 4:
            blob.append(0)

    mime_off = len(blob)
    blob.extend(mime + b"\0")
    align()
    list_off = len(blob)
    blob.extend(u32(1) + u32(0) + u32(0))
    entries_off = len(blob)
    blob.extend(b"\0" * 16)
    mat_off = len(blob)
    blob.extend(b"\0" * 32)
    blob[mat_off:mat_off + 32] = (u32(0) + u32(1) + u32(1) + u32(0) + u32(0) + u32(0)
                                  + u32(1) + u32(mat_off))
    blob[list_off + 8:list_off + 12] = u32(entries_off)
    blob[entries_off:entries_off + 16] = u32(90) + u32(mime_off) + u32(1) + u32(mat_off)
    for k in (28, 32, 36):
        blob[k:k + 4] = u32(0)
    blob[0:4] = struct.pack(">HH", 1, 2)
    blob[4:8] = u32(len(blob))
    blob[8:12] = u32(0)
    blob[12:16] = u32(0)
    blob[16:20] = u32(0)
    blob[20:24] = u32(0)
    blob[24:28] = u32(list_off)
    return bytes(blob)


CYCLE = cycle_cache()

# ---------------------------------------------------------------- cases

CASES = []


def add(cid, cls, files, name, data, env=None):
    CASES.append({
        "id": cid, "class": cls,
        "env": env or {"HOME": "{root}/h", "XDG_DATA_HOME": "{root}/dh",
                       "XDG_DATA_DIRS": "{root}/s1:{root}/s2"},
        "files": files,
        "input": {"name": name, "data": data},
    })


D = lambda blob: {"dh/mime/mime.cache": blob}

add("order-01-first-entry", "order", D(A), None, b"HI there")
add("order-02-second-entry", "order", D(A), None, b"LO")
add("order-03-two-entries", "order", D(B), None, b"AA")
add("prio-01-equal-caches", "prio",
    {"s1/mime/mime.cache": C1C, "s2/mime/mime.cache": C2C}, None, b"AA")
add("prio-02-negative", "prio", D(NEG), None, b"ZZ")
add("prio-03-high-bit", "prio", D(HIGH), None, b"QQ")
add("prio-04-exactly-80", "prio", D(P80), b"x.two", b"HI")
add("prio-05-79", "prio", D(P79), b"x.two", b"PP")
add("range-01-offset", "range", D(A), None, b"\x01\x01\x01\x01RG")
add("range-02-end-exclusive", "range", D(ENDX), None, b"BA")
add("range-03-beyond-4096", "range", D(FAR), None, b"a" * 5000 + b"Z")
add("range-04-exact-end", "range", D(EQ), None, b"AB")
add("wrap-01-range-wrap", "wrap", D(WRAP), None, b"0123456789Z")
add("wrap-02-past-2^32", "wrap", D(WRAP2), None, b"a" * 16)
add("mask-01-basic", "mask", D(A), None, b"\x1f\x99")
add("mask-02-value-bits", "mask", D(M2), None, b"\x1f\x00")
add("mask-03-data-bits", "mask", D(M3), None, b"\x1f\x00")
add("nest-01-child-holds", "nest", D(A), None, b"NE\x01\x01Y")
add("nest-02-no-child", "nest", D(A), None, b"NE\x01\x01Z")
add("nest-03-cycle", "nest", D(CYCLE), None, b"a" * 16)
add("bounds-01-magic-list", "bounds", D(B1), None, b"HI there")
add("bounds-02-entry-array", "bounds", D(B2), None, b"HI there")
add("bounds-03-entry-matchlets", "bounds", D(B3), None, b"CC")
add("bounds-04-alias-list", "bounds", D(B4), b"x.dup", b"BA")
add("bounds-05-parent-list", "bounds", D(B5), b"x.dup", b"BA")
add("bounds-06-value-past-page", "bounds", D(B6), None, b"a" * 16)
add("bounds-07-child-before-value", "bounds", D(B7), None, b"a" * 16)
add("zerosize-01-empty", "zerosize", D(A), None, b"")
add("zerosize-02-two-names", "zerosize", D(A), b"x.two", b"")
add("fallback-01-text", "fallback", D(A), None, b"plain words\n")
add("fallback-02-binary", "fallback", D(A), None, b"\x01\x02")
add("fallback-03-space", "fallback", D(A), None, b"a b")
add("fallback-04-cr", "fallback", D(A), None, b"a\rb")
add("fallback-05-tab", "fallback", D(A), None, b"a\tb")
add("fallback-06-127th", "fallback", D(A), None, b"a" * 127 + b"\x01")
add("fallback-07-129th", "fallback", D(A), None, b"a" * 128 + b"\x01")
add("fallback-08-del", "fallback", D(A), None, b"a\x7fb")
add("fallback-09-magic-octet", "fallback", D(OCT), None, b"UN")
add("lltext-01-backspace", "lltext", D(A), None, b"\x08")
add("lltext-02-bel", "lltext", D(A), None, b"\x07")
add("lltext-03-ff", "lltext", D(A), None, b"ab\x0ccd")
add("lltext-04-0e", "lltext", D(A), None, b"\x0e")
add("lltext-05-0d", "lltext", D(A), None, b"\x0d\x0c")
add("lltext-06-del", "lltext", D(A), None, b"\x0c\x7f")
add("lltext-07-tilde", "lltext", D(A), None, b"\x0c\x7e")
add("lltext-08-past-128", "lltext", D(A), None, b"\x0c" + b"a" * 200 + b"\x7f")
add("desktop-01-no-name", "desktop", D(A), None, b"[Desktop Entry]\n")
add("desktop-02-with-name", "desktop", D(A), b"zz.nomatch", b"[Desktop Entry]\n")
add("name0-01-null", "name0", D(A), None, b"HI")
add("name1-01-one-type", "name1", D(A), b"x.one", b"HI")
add("name1-02-basename", "name1", D(A), b"dir/x.one", b"HI")
add("nameN-01-two-types", "nameN", D(A), b"x.two", b"HI")
add("nameN-02-unknown-sniffed", "nameN", D(A), b"x.two", b"\x01\x02")
add("nameN-03-no-subclass", "nameN", D(A), b"x.amb", b"LO")
add("nameN-04-text-fallback-prio", "nameN", D(A), b"x.two", b"plain\n")
add("subclass-01-eq", "subclass", D(SEQ), b"x.eq", b"EQ")
add("subclass-02-parent-chain", "subclass", D(A), b"x.dup", b"BA")
add("subclass-03-supertype", "subclass", D(SSP), b"x.su", b"SU")
add("subclass-04-media-slice", "subclass", D(SMS), b"x.ms", b"MS")
add("subclass-05-text", "subclass", D(STX), b"x.tx", b"TX")
add("subclass-06-octet-inode", "subclass", D(SOC), b"x.oc", b"OC")
add("subclass-07-cycle", "subclass", D(SCY), b"x.cy", b"CY")
add("subclass-08-second-cache", "multicache",
    {"s1/mime/mime.cache": SC1, "s2/mime/mime.cache": SC2}, b"x.sc", b"SC")
add("subclass-09-two-subclasses", "subclass", D(SS2), b"x.ss", b"SS")
add("alias-01-unaliased", "alias", D(A), b"x.dup", b"plain\n")
add("alias-02-second-cache", "multicache",
    {"s1/mime/mime.cache": AL1, "s2/mime/mime.cache": AL2}, b"x.al", b"AL")
add("slash-01-directory", "slash", D(A), b"d/", b"HI")
add("fallback-10-space-del", "fallback", D(A), None, b"a b\x7f")
add("fallback-11-cr-del", "fallback", D(A), None, b"a\r\x7f")
add("fallback-12-tab-del", "fallback", D(A), None, b"a\t\x7f")
add("alias-03-nontext", "alias", D(ALIAS2), b"x.ao", b"AO")
add("alias-04-second-cache-nontext", "multicache",
    {"s1/mime/mime.cache": ALIAS3A, "s2/mime/mime.cache": ALIAS3B}, b"x.a2", b"A2")
add("name1-03-basename-literal", "name1", D(NB), b"dir/x.one", b"HI")
add("mode-01-cache-beats-text", "mode",
    {"dh/mime/mime.cache": A, "s1/mime/globs2": b"50:text/x-text:*.txt\n"}, b"x.txt", b"HI")

# ---------------------------------------------------------------- mutants

MUTANTS = [
    # matchlet_value: range / wrap / len / mask
    ("range_end_mask", "range_length 32-bit wrap in range_start + range_length",
     "    end = (range_start + range_length) & M32", "    end = range_start + range_length"),
    ("range_start_zero", "for i from range_start",
     "    i = range_start", "    i = 0"),
    ("range_end_inclusive", "while i < range_start + range_length",
     "    while i < end:", "    while i <= end:"),
    ("wrap_raise_removed", "i + value_length past 2^32 is refused",
     "        if i + value_length > M32:\n"
     "            raise Unsupported(\"matchlet i + value_length passes 2^32 (memcmp past the data)\")\n",
     ""),
    ("len_check_ge", "stop false as soon as i + value_length exceeds len",
     "        if i + value_length > len(data):\n            return False",
     "        if i + value_length >= len(data):\n            return False"),
    ("mask_ignored", "with a mask, every byte compared under the mask",
     "            if mask_offset:", "            if False:"),
    ("mask_value_unmasked", "value byte compared under the mask",
     "                if (v & m) != (d & m):", "                if v != (d & m):"),
    ("mask_data_unmasked", "data byte compared under the mask",
     "                if (v & m) != (d & m):", "                if (v & m) != d:"),
    ("byte_past_mapping", "a cache read past the zero-filled last page is refused",
     "    if off >= len(c.buf):\n        raise Unsupported(\"cache read past the mapping\")",
     "    if off > M32:\n        raise Unsupported(\"cache read past the mapping\")"),
    # matchlet: children
    ("child_bounds_after_value", "a child list that fails the bounds check makes the matchlet false before its own test",
     "        if oob(co, n, 32, c.size):\n            return None\n"
     "        if not matchlet_value(c, o, data):\n            return None",
     "        if not matchlet_value(c, o, data):\n            return None\n"
     "        if oob(co, n, 32, c.size):\n            return None"),
    ("child_fail_aborts", "a matchlet holds when any child holds",
     "        if sub is None:\n            continue", "        if sub is None:\n            return False"),
    ("no_children_false", "a matchlet holds when it has no children",
     "    if top[1] == 0:\n        return True", "    if top[1] == 0:\n        return False"),
    ("nest_raise_removed", "nested deeper than 100000 is refused",
     "        if len(stack) > MAX_NEST:\n"
     "            raise Unsupported(\"matchlet children nested past 100000 (the C recursion overflows)\")\n",
     ""),
    ("nest_ge", "the nest limit is > 100000",
     "        if len(stack) > MAX_NEST:", "        if len(stack) >= MAX_NEST:"),
    ("max_nest_zero", "MAX_NEST = 100000",
     "MAX_NEST = 100000", "MAX_NEST = 0"),
    ("stack_empty", "the traversal starts from the top matchlet",
     "    stack = [top]", "    stack = []"),
    ("child_stride_16", "child = child_offset + 32 * i",
     "        child = fr[2] + 32 * fr[3]", "        child = fr[2] + 16 * fr[3]"),
    # cache_magic_lookup
    ("magic_list_off_20", "list_offset = GET_UINT32(buffer, 24)",
     "    lo = c.u32(24)", "    lo = c.u32(20)"),
    ("magic_list_bounds_removed", "the magic list header is bounds-checked",
     "    if oob(lo, 1, 12, c.size):\n        return None, 0",
     "    if False:\n        return None, 0"),
    ("entries_bounds_removed", "the magic entry array is bounds-checked",
     "    if oob(off, n, 16, c.size):\n        return None, 0",
     "    if False:\n        return None, 0"),
    ("entry_oob_break", "an out-of-bounds matchlet list skips its entry",
     "        if oob(mlo, nm, 32, c.size):\n            continue",
     "        if oob(mlo, nm, 32, c.size):\n            break"),
    ("entry_mlo_field", "matchlet_offset = GET_UINT32(offset + 12)",
     "        mlo = c.u32(e + 12)", "        mlo = c.u32(e + 8)"),
    ("entry_prio_field", "priority = GET_UINT32(offset)",
     "        prio = c.u32(e)", "        prio = c.u32(e + 8)"),
    ("entry_nm_field", "n_matchlets = GET_UINT32(offset + 8)",
     "        nm = c.u32(e + 8)", "        nm = c.u32(e + 4)"),
    ("entry_mo_field", "mimetype_offset = GET_UINT32(offset + 4)",
     "        mo = c.u32(e + 4)", "        mo = c.u32(e)"),
    ("entries_reversed", "the first match entry in cache order is returned",
     "    for j in range(n):", "    for j in range(n - 1, -1, -1):"),
    ("matchlets_short", "every matchlet of an entry is tried",
     "        for k in range(nm):", "        for k in range(nm - 1):"),
    ("first_match_skipped", "a matching entry is returned at once",
     "                return c.cstr(mo).decode(\"utf-8\", \"surrogateescape\"), _s32(prio)",
     "                break"),
    ("prio_unsigned", "priorities are ints (>= 2^31 negative)",
     "                return c.cstr(mo).decode(\"utf-8\", \"surrogateescape\"), _s32(prio)",
     "                return c.cstr(mo).decode(\"utf-8\", \"surrogateescape\"), prio"),
    ("s32_mask", "the sign bit is 0x80000000",
     "    return x - (1 << 32) if x & 0x80000000 else x",
     "    return x - (1 << 32) if x & 0x40000000 else x"),
    # mime_type_for_data
    ("zerosize_removed", "empty data -> application/x-zerosize with priority 100",
     "    if len(data) == 0:\n        return EMPTY, 100\n", ""),
    ("zerosize_prio_zero", "empty data -> priority 100",
     "        return EMPTY, 100", "        return EMPTY, 0"),
    ("zerosize_type_text", "empty data -> the EMPTY constant",
     "        return EMPTY, 100", "        return TEXTPLAIN, 100"),
    ("prio_strict_gt", "a cache's answer replaces the running one only when its priority is strictly greater",
     "        if p > priority:", "        if p >= priority:"),
    ("priority_ge_zero", "a cache answer is used only when priority > 0",
     "    if priority > 0:", "    if priority >= 0:"),
    ("fallback_127", "the fallback reads the first 128 bytes",
     "    for b in data[:128]:", "    for b in data[:127]:"),
    ("fallback_129", "the fallback reads the first 128 bytes",
     "    for b in data[:128]:", "    for b in data[:129]:"),
    ("fallback_space", "a byte < 32 other than 9, 10, 13 -> UNKNOWN",
     "        if b < 32 and b not in (9, 10, 13):", "        if b <= 32 and b not in (9, 10, 13):"),
    ("fallback_cr", "13 is allowed by the fallback",
     "        if b < 32 and b not in (9, 10, 13):", "        if b < 32 and b not in (9, 10):"),
    ("fallback_tab", "9 is allowed by the fallback",
     "        if b < 32 and b not in (9, 10, 13):", "        if b < 32 and b not in (10, 13):"),
    ("fallback_unknown_to_text", "binary data -> the UNKNOWN constant",
     "            return UNKNOWN, 0", "            return TEXTPLAIN, 0"),
    ("fallback_text_to_unknown", "text data -> the TEXTPLAIN constant",
     "    return TEXTPLAIN, 0", "    return UNKNOWN, 0"),
    ("fallback_text_prio", "the fallback keeps priority 0",
     "    return TEXTPLAIN, 0", "    return TEXTPLAIN, 100"),
    # looks_like_text
    ("lltext_lt7", "no byte 0x00-0x07",
     "    return not any(b < 8 or 14 <= b < 32 or b == 127 for b in data)",
     "    return not any(b < 7 or 14 <= b < 32 or b == 127 for b in data)"),
    ("lltext_le8", "0x08 (backspace) passes looks_like_text",
     "b < 8 or", "b <= 8 or"),
    ("lltext_15", "no byte 0x0e-0x1f",
     "14 <= b < 32", "15 <= b < 32"),
    ("lltext_13", "0x0d is not rejected",
     "14 <= b < 32", "13 <= b < 32"),
    ("lltext_no127", "0x7f is rejected",
     " or b == 127 for b in data)", " for b in data)"),
    ("lltext_126", "0x7f is rejected (not 0x7e)",
     "b == 127", "b == 126"),
    ("lltext_128", "looks_like_text scans the whole data",
     "for b in data)", "for b in data[:128])"),
    ("lltext_inverted", "looks_like_text is the negation of the control scan",
     "    return not any(b < 8", "    return any(b < 8"),
    # constants
    ("unknown_constant_value", "UNKNOWN is application/octet-stream",
     "UNKNOWN = _Const(\"application/octet-stream\")",
     "UNKNOWN = _Const(\"application/x-unknown\")"),
    ("textplain_constant_value", "TEXTPLAIN is text/plain",
     "TEXTPLAIN = _Const(\"text/plain\")", "TEXTPLAIN = _Const(\"text/x-plain\")"),
    ("empty_constant_value", "EMPTY is application/x-zerosize",
     "EMPTY = _Const(\"application/x-zerosize\")", "EMPTY = _Const(\"application/x-empty\")"),
    # _alias
    ("alias_return_name", "the alias list maps the name",
     "                return c.cstr(c.u32(lo + 4 + 8 * mid + 4))", "                return name"),
    ("alias_first_cache", "the alias is searched in every cache",
     "def _alias(caches: list, name: bytes) -> bytes:\n    for c in caches:",
     "def _alias(caches: list, name: bytes) -> bytes:\n    for c in caches[:1]:"),
    ("alias_lt_ge", "binary search on strcmp < 0",
     "            if s < name:", "            if s <= name:"),
    ("alias_bounds_removed", "the alias list header is bounds-checked",
     "        lo = c.u32(4)\n        if oob(lo, 1, 4, c.size):\n            continue",
     "        lo = c.u32(4)\n        if False:\n            continue"),
    # subclass
    ("subclass_eq_removed", "equal unaliased names are subclasses",
     "    if umime == ubase:\n        return True", "    if False:\n        return True"),
    ("subclass_super_slash", "base x/* with the same media type",
     "    if ubase.endswith(b\"/*\"):", "    if ubase.endswith(b\"/\"):"),
    ("subclass_media_slice", "xdg_mime_media_type_equal compares up to and including /",
     "        if sep >= 0 and umime[:sep + 1] == ubase[:sep + 1]:",
     "        if sep >= 0 and umime[:sep] == ubase[:sep]:"),
    ("subclass_text_media_removed", "base text/plain and mime text/*",
     "    if ubase == b\"text/plain\" and umime.startswith(b\"text/\"):",
     "    if ubase == b\"text/plain\":"),
    ("subclass_octet_inode", "base application/octet-stream and mime not inode/*",
     "    if ubase == b\"application/octet-stream\" and not umime.startswith(b\"inode/\"):",
     "    if ubase == b\"application/octet-stream\" and umime.startswith(b\"inode/\"):"),
    ("subclass_seen_removed", "parents already seen are skipped",
     "                    if (ci, pofs) in seen:\n                        continue\n", ""),
    ("subclass_first_cache", "every cache's parent list is searched",
     "    for ci, c in enumerate(caches):", "    for ci, c in enumerate(caches[:1]):"),
    ("subclass_recurse_base", "the parent is tested against the base",
     "                    if subclass(caches, c.cstr(pofs), ubase, seen):",
     "                    if subclass(caches, c.cstr(pofs), umime, seen):"),
    ("subclass_break_removed", "the search stops after the first matching parent entry",
     "                break\n    return False", "    return False"),
    ("subclass_parents_bounds_removed", "the parent list header is bounds-checked",
     "        lo = c.u32(8)\n        if oob(lo, 1, 4, c.size):\n            continue",
     "        lo = c.u32(8)\n        if False:\n            continue"),
    # Sniffer / guess
    ("cache_order_reversed", "caches are consulted in directory order",
     "        self.caches = self.resolver.db.caches",
     "        self.caches = list(reversed(self.resolver.db.caches))"),
    ("text_mode_removed", "text mode is refused",
     "        if self.mode != \"cache\":\n"
     "            raise Unsupported(\"text mode (no loadable mime.cache; GLib reads the magic files)\")",
     "        if False:\n"
     "            raise Unsupported(\"text mode (no loadable mime.cache; GLib reads the magic files)\")"),
    ("slash_rule", "a trailing / is inode/directory",
     "            if filename.endswith(b\"/\"):", "            if filename.endswith(b\"\\\\\"):"),
    ("slash_uncertain", "the directory answer is uncertain",
     "                return {\"type\": \"inode/directory\", \"uncertain\": 1, \"types\": [\"inode/directory\"],",
     "                return {\"type\": \"inode/directory\", \"uncertain\": 0, \"types\": [\"inode/directory\"],"),
    ("name_one_type_ge", "exactly one name type -> it, certain",
     "            if len(types) == 1:", "            if len(types) >= 1:"),
    ("name_basename_removed", "the basename is passed to the name step",
     "            types = self.resolver.db.lookup(mg.g_path_get_basename(filename))",
     "            types = self.resolver.db.lookup(filename)"),
    ("unknown_identity_guess", "UNKNOWN is compared by pointer",
     "        if sniffed is UNKNOWN and looks_like_text(data):",
     "        if sniffed == UNKNOWN and looks_like_text(data):"),
    ("unknown_identity_uncertain", "UNKNOWN is compared by pointer (uncertain)",
     "            return dict(out, type=str(sniffed), uncertain=1 if sniffed is UNKNOWN else 0)",
     "            return dict(out, type=str(sniffed), uncertain=1 if sniffed == UNKNOWN else 0)"),
    ("no_types_uncertain_one", "no name type: uncertain only for UNKNOWN",
     "            return dict(out, type=str(sniffed), uncertain=1 if sniffed is UNKNOWN else 0)",
     "            return dict(out, type=str(sniffed), uncertain=1)"),
    ("desktop_guard_removed", "the desktop rule needs a filename",
     "        if filename is not None and sniffed == \"application/x-desktop\":",
     "        if sniffed == \"application/x-desktop\":"),
    ("desktop_replacement", "a sniffed desktop with a name becomes text/plain",
     "            sniffed = \"text/plain\"\n        out = {\"types\": types, \"sniffed\": str(sniffed), \"prio\": prio}",
     "            sniffed = \"text/x-desktop\"\n        out = {\"types\": types, \"sniffed\": str(sniffed), \"prio\": prio}"),
    ("desktop_is", "the desktop test is strcmp",
     "        if filename is not None and sniffed == \"application/x-desktop\":",
     "        if filename is not None and sniffed is \"application/x-desktop\":"),
    ("sniffed_always", "a sniffed type other than UNKNOWN wins",
     "        if sniffed is not UNKNOWN:", "        if True:"),
    ("prio_threshold_gt", "a sniffed type wins outright when priority >= 80",
     "            if prio >= 80:", "            if prio > 80:"),
    ("prio_threshold_79", "the priority threshold is 80",
     "            if prio >= 80:", "            if prio >= 79:"),
    ("subclass_loop_reversed", "the first name type that is a subclass wins",
     "            for t in types:", "            for t in reversed(types):"),
    ("subclass_certain_one", "a subclass name type is certain",
     "                    return dict(out, type=t, uncertain=0)",
     "                    return dict(out, type=t, uncertain=1)"),
    ("fallback_first_name_last", "none -> the first name type, uncertain",
     "        return dict(out, type=types[0], uncertain=1)",
     "        return dict(out, type=types[-1], uncertain=1)"),
    # main
    ("read_4096", "the data is the whole file",
     "                    data = fh.read()", "                    data = fh.read(4096)"),
    ("name_always_null", "the filename is passed when --name is given",
     "            name = fb if a.names_from_files else (os.fsencode(a.name) if a.name is not None else None)",
     "            name = None"),
    ("unsupported_exit_zero", "UNSUPPORTED exits 3",
     "    except Unsupported as e:\n        print(f\"MADO_MIMESNIFF: UNSUPPORTED {e}\")\n        return 3",
     "    except Unsupported as e:\n        print(f\"MADO_MIMESNIFF: UNSUPPORTED {e}\")\n        return 0"),
]

# ---------------------------------------------------------------- machinery


def case_root(case):
    return os.path.join(ROOTDIR, case["id"])


def materialise(case):
    root = case_root(case)
    if os.path.isdir(root):
        shutil.rmtree(root)
    os.makedirs(root)
    for rel, blob in case["files"].items():
        p = os.path.join(root, rel)
        os.makedirs(os.path.dirname(p), exist_ok=True)
        with open(p, "wb") as fh:
            fh.write(blob)
    inp = case["input"]
    dp = os.path.join(root, "in", "0.bin")
    os.makedirs(os.path.dirname(dp), exist_ok=True)
    with open(dp, "wb") as fh:
        fh.write(inp["data"])
    return root, dp


def env_for(case, root, with_path):
    e = {}
    for k, v in case["env"].items():
        if v is None:
            continue
        e[k] = v.replace("{root}", root)
    e["LC_ALL"] = "C"
    if with_path:
        e["PATH"] = EMPTYBIN
    return e


def oracle_label(case):
    root, dp = materialise(case)
    name = case["input"]["name"]
    arg = b"0" if name is None else b"=" + name
    try:
        r = subprocess.run([ORACLE, arg, dp], env=env_for(case, root, False),
                           capture_output=True, timeout=TIMEOUT)
    except subprocess.TimeoutExpired:
        return ["UNSUPPORTED", None], "timeout"
    if r.returncode != 0:
        return ["UNSUPPORTED", None], f"rc={r.returncode}"
    lines = [l for l in r.stdout.decode("utf-8", "surrogateescape").splitlines() if l]
    if len(lines) != 1:
        return ["UNSUPPORTED", None], f"lines={len(lines)}"
    t, u = lines[0].split("\t")
    return [t, int(u)], "ok"


def tool_run(tool, case):
    root, dp = materialise(case)
    name = case["input"]["name"]
    args = [PY, "-I", tool, "--json"]
    if name is not None:
        args += ["--name", name.decode("utf-8", "surrogateescape")]
    args.append(dp)
    try:
        r = subprocess.run(args, env=env_for(case, root, True), capture_output=True,
                           timeout=TIMEOUT)
    except subprocess.TimeoutExpired:
        return {"rc": "timeout"}
    out = {"rc": r.returncode, "stderr": r.stderr.decode("utf-8", "replace")[-400:]}
    if r.returncode == 0:
        try:
            j = json.loads(r.stdout.decode("utf-8", "surrogateescape"))
            res = j["results"][0]
            out["type"] = res["type"]
            out["uncertain"] = res["uncertain"]
        except Exception as e:  # noqa: BLE001
            out["parse_error"] = repr(e)
    return out


def verdict(label, got):
    if label[0] == "UNSUPPORTED":
        return got.get("rc") == 3
    return (got.get("rc") == 0 and got.get("type") == label[0]
            and got.get("uncertain") == label[1])


def write_mutant(mid, src):
    d = os.path.join(S, "mut", mid)
    os.makedirs(d, exist_ok=True)
    p = os.path.join(d, "mado-mimesniff.py")
    with open(p, "w", encoding="utf-8") as fh:
        fh.write(src)
    shutil.copyfile(os.path.join(TOOLS, "mado-mimeglob.py"), os.path.join(d, "mado-mimeglob.py"))
    r = subprocess.run([PY, "-c", "import py_compile,sys; py_compile.compile(sys.argv[1], doraise=True)", p],
                       capture_output=True)
    if r.returncode != 0:
        raise SystemExit(f"{mid}: does not compile: {r.stderr.decode()}")
    return p


def main():
    cmd = sys.argv[1] if len(sys.argv) > 1 else "prepare"
    if cmd == "prepare":
        with cf.ThreadPoolExecutor(WORKERS) as ex:
            labels = list(ex.map(oracle_label, CASES))
        out = {"version": 1,
               "oracle_src_sha256": "99df35f8b3fd7005f30789f8866984a1bbceaff8dc6c1d326f0132eb7b4d124a",
               "glib2": "2.90.1-1", "cases": []}
        for case, (lab, why) in zip(CASES, labels):
            c = {"id": case["id"], "class": case["class"], "env": case["env"],
                 "files": {k: base64.b64encode(v).decode() for k, v in case["files"].items()},
                 "inputs": [{"name_b64": None if case["input"]["name"] is None
                             else base64.b64encode(case["input"]["name"]).decode(),
                             "data_b64": base64.b64encode(case["input"]["data"]).decode()}],
                 "labels": [lab]}
            out["cases"].append(c)
            print(f"{case['id']:32s} {lab[0]:28s} {lab[1]}  ({why})")
        with open(os.path.join(S, "cases-labelled.json"), "w") as fh:
            json.dump(out, fh, indent=1)
        print("wrote", os.path.join(S, "cases-labelled.json"))
    elif cmd == "baseline":
        with open(os.path.join(S, "cases-labelled.json")) as fh:
            lab = {c["id"]: c["labels"][0] for c in json.load(fh)["cases"]}
        bad = 0
        with cf.ThreadPoolExecutor(WORKERS) as ex:
            futs = {ex.submit(tool_run, TOOL, c): c for c in CASES}
            for f in cf.as_completed(futs):
                c = futs[f]
                got = f.result()
                ok = verdict(lab[c["id"]], got)
                if not ok:
                    bad += 1
                    print(f"BASELINE-MISMATCH {c['id']}: label={lab[c['id']]} got={got}")
        print(f"baseline: {len(CASES) - bad}/{len(CASES)} ok")
    elif cmd == "mutants":
        src = open(TOOL, encoding="utf-8").read()
        with open(os.path.join(S, "cases-labelled.json")) as fh:
            lab = {c["id"]: c["labels"][0] for c in json.load(fh)["cases"]}
        results = {}
        for mid, rule, find, repl in MUTANTS:
            n = src.count(find)
            if n != 1:
                print(f"BAD-MUTANT {mid}: find occurs {n} times")
                results[mid] = {"error": f"find occurs {n} times"}
                continue
            path = write_mutant(mid, src.replace(find, repl, 1))
            killers = []
            with cf.ThreadPoolExecutor(WORKERS) as ex:
                futs = {ex.submit(tool_run, path, c): c for c in CASES}
                for f in cf.as_completed(futs):
                    c = futs[f]
                    got = f.result()
                    if not verdict(lab[c["id"]], got):
                        killers.append({"case": c["id"], "got": got})
            results[mid] = {"rule": rule, "find": find, "replace": repl,
                            "killers": sorted(killers, key=lambda k: k["case"])}
            print(f"{mid:28s} killed_by={len(killers):2d} "
                  f"{[k['case'] for k in sorted(killers, key=lambda k: k['case'])][:4]}")
        with open(os.path.join(S, "mutant-results.json"), "w") as fh:
            json.dump(results, fh, indent=1)
        survivors = [m for m, r in results.items() if not r.get("killers") and "error" not in r]
        print("SURVIVORS", survivors)
    else:
        raise SystemExit(f"unknown command {cmd}")


if __name__ == "__main__":
    main()
