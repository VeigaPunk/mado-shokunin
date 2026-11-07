#!/usr/bin/env python3
"""mado-mimesniff — which MIME type GLib guesses from a file's bytes (and its name, if given).

Read-only resolver for the content step of the default-application plane: given the XDG data roots, print what
GLib 2.90.1's g_content_type_guess (filename-or-NULL, data, len, &uncertain) answers — the content type and the
uncertain flag — when the bytes are passed, reading the magic section of the binary mime.cache files as the
installed library does.  The name step (which types a basename gets) is round 94's tools/mado-mimeglob.py, loaded
from the same directory.

Upstream model (GLib tag 2.90.1; line numbers are that tag's files):
  guess      gio/gcontenttype-fdo.c g_content_type_guess_impl (:567-690): a trailing '/' -> inode/directory,
             uncertain; exactly one name type -> it, certain, the bytes are not read (:613-620).  Otherwise the
             bytes are sniffed (:622-639): xdg_mime_get_mime_type_for_data; if that returned the UNKNOWN constant
             (pointer comparison, not strcmp) and looks_like_text (:533-548: no byte that g_ascii_iscntrl and not
             g_ascii_isspace and not '\\b' -- GLib's isspace table holds 0x09, 0x0a, 0x0c, 0x0d, 0x20 but not 0x0b,
             so none of 0x00-0x07, 0x0b, 0x0e-0x1f, 0x7f) the answer is text/plain;
             with a name given (even one with no type), a sniffed application/x-desktop becomes text/plain.  No
             name type (:641-648): the sniffed type, uncertain only when it is still the UNKNOWN constant.
             Several name types (:649-684): a sniffed type other than the UNKNOWN constant wins outright when its
             priority is >= 80, else the first name type that is a subclass of it; none -> the first name type,
             uncertain.
  data       gio/xdgmime/xdgmime.c xdg_mime_get_mime_type_for_data (:516-541): empty data ->
             application/x-zerosize with priority 100; with caches, the cache answer; none ->
             _xdg_binary_or_text_fallback (xdgmimeint.c:176-190): a byte < 32 other than 9, 10, 13 in the first
             128 bytes -> the UNKNOWN constant, else the TEXTPLAIN constant (priority stays 0).
  magic      gio/xdgmime/xdgmimecache.c cache_get_mime_type_for_data (:751-807): per cache in directory order,
             cache_magic_lookup_data (:276-312) returns the first match entry (cache order) any of whose
             top-level matchlets holds; a cache's answer replaces the running one only when its priority is
             strictly greater (an int: priorities >= 2^31 are negative and never win; priority 0 never wins).
             cache_magic_matchlet_compare (:212-239): a child list that fails the bounds check makes the matchlet
             false before its own test; a matchlet holds when its value matches and it has no children or any
             child holds.  cache_magic_matchlet_compare_to_data (:167-210): for i from range_start while
             i < range_start + range_length (32-bit wrap), stop false as soon as i + value_length (32-bit wrap)
             exceeds len; then compare byte by byte, stopping at the first difference: without a mask as memcmp
             (data + i + j, no wrap), with a mask under the mask (data[j + i], buffer[offset + j] in 32-bit
             unsigned sums); word_size is not read.  The matching entry's type string is read only if it wins.
  subclass   xdgmimecache.c _xdg_mime_cache_mime_type_subclass (:937-1046): both unaliased (first cache whose
             alias list holds the name, :314-361); equal; base "x/*" with the same media type; base text/plain
             and mime text/*; base application/octet-stream and mime not inode/*; else each cache's parent list
             (every cache, not only the first holding the type), recursively with the caller's unaliased base,
             skipping parent pointers already seen.

Modes (xdgmime.c:129-206): a directory whose mime.cache loads is a cache; when any cache loads, only caches are
read.  With no loadable cache, a directory's globs2/globs/magic/aliases/subclasses files are read as text: that
mode is refused (exit 3, UNSUPPORTED text mode) when any of those files exists; when none exists GLib's tables are
empty and the tool answers (mode "none": fallback, zerosize, trailing slash).  The tool also refuses (exit 3)
where the C code is undefined: a cache read past the zero-filled last page of the mapping, a compare that reads at
a data index >= len (the 32-bit sum wrapped to a value <= len), and -- declared limits, below the depth where the C
recursion overflows its stack (measured with an 8 MiB stack: matchlet chains near 74849, parent chains between
60000 and 100000; the depth scales with the stack size, so no cap can equal it) -- a matchlet child chain or a
parent chain whose traversal goes deeper than 4096 levels.

Usage:
  mado-mimesniff.py FILE... [--name NAME | --names-from-files] [--data-home D | --data-home-unset]
                    [--data-dirs LIST | --data-dirs-unset] [--home H | --home-unset] [--json]
  mado-mimesniff.py --selftest

Without --name the filename passed to GLib is NULL (data only); --name NAME passes NAME for every FILE;
--names-from-files passes each FILE path itself.  Output: one line per file,
`MADO_MIMESNIFF: <type> uncertain=<0|1> name=<escaped|-> file=<escaped>`; --json prints
{"mode", "dirs", "results": [{"file", "name", "type", "uncertain", "sniffed", "prio", "types"}]}.
ASCII only, stdlib only.  Exit 0 answered, 2 setup error, 3 unsupported input.
"""
from __future__ import annotations

import argparse
import importlib.util
import json
import os
import struct
import sys


def _load_mimeglob():
    """Round 94's name step, from this file's own directory (the C1 structural conjunct pins this exact shape)."""
    spec = importlib.util.spec_from_file_location(
        "mado_mimeglob", os.path.join(os.path.dirname(os.path.abspath(__file__)), "mado-mimeglob.py"))
    if not os.path.exists(spec.origin):
        raise SystemExit(f"mado-mimesniff: setup error: {spec.origin} missing (the name step)")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


mg = _load_mimeglob()
Unsupported = mg.Unsupported
oob = mg.oob


class _Const(str):
    """A distinct object for GLib's constant strings: g_content_type_guess compares them by address."""


UNKNOWN = _Const("application/octet-stream")   # xdgmime.c xdg_mime_type_unknown
EMPTY = _Const("application/x-zerosize")       # xdg_mime_type_empty
TEXTPLAIN = _Const("text/plain")               # xdg_mime_type_textplain
MAX_NEST = 4096
M32 = 0xFFFFFFFF


def _byte(c, off: int) -> int:
    if off >= len(c.buf):
        raise Unsupported("cache read past the mapping")
    return c.buf[off]


def _s32(x: int) -> int:
    return x - (1 << 32) if x & 0x80000000 else x


def matchlet_value(c, off: int, data: bytes) -> bool:
    """cache_magic_matchlet_compare_to_data.  The length test uses the 32-bit sum; the compare then reads the
    bytes in order and stops at the first difference.  Unmasked (memcmp) indexes data + i + j and buffer +
    value_offset + j as pointers (no wrap); masked indexes buffer[value_offset + j], buffer[mask_offset + j] and
    data[j + i] with 32-bit unsigned sums (they wrap).  A byte read at data index >= len is past the caller's
    buffer (undefined in C): refused."""
    range_start = c.u32(off)
    range_length = c.u32(off + 4)
    value_length = c.u32(off + 12)
    value_offset = c.u32(off + 16)
    mask_offset = c.u32(off + 20)
    n = len(data)
    end = (range_start + range_length) & M32
    i = range_start
    while i < end:
        if ((i + value_length) & M32) > n:
            return False
        ok = True
        for j in range(value_length):
            if mask_offset:
                v = _byte(c, (value_offset + j) & M32)
                m = _byte(c, (mask_offset + j) & M32)
                di = (j + i) & M32
            else:
                v = _byte(c, value_offset + j)
                m = 0xFF
                di = i + j
            if di >= n:
                raise Unsupported("matchlet compare reads past the data (the C sum wrapped)")
            if (v & m) != (data[di] & m):
                ok = False
                break
        if ok:
            return True
        i += 1
    return False


def matchlet(c, off: int, data: bytes) -> bool:
    """cache_magic_matchlet_compare, iterative: [offset, n_children, child_offset, next child index]."""
    def enter(o: int):
        n = c.u32(o + 24)
        co = c.u32(o + 28)
        if oob(co, n, 32, c.size):
            return None
        if not matchlet_value(c, o, data):
            return None
        return [o, n, co, 0]

    top = enter(off)
    if top is None:
        return False
    if top[1] == 0:
        return True
    stack = [top]
    while stack:
        if len(stack) > MAX_NEST:
            raise Unsupported("matchlet children nested past 4096 (declared limit; the C recursion overflows deeper)")
        fr = stack[-1]
        if fr[3] >= fr[1]:
            stack.pop()
            continue
        child = fr[2] + 32 * fr[3]
        fr[3] += 1
        sub = enter(child)
        if sub is None:
            continue
        if sub[1] == 0:
            return True
        stack.append(sub)
    return False


def cache_magic_lookup(c, data: bytes) -> tuple[int | None, int]:
    """cache_magic_lookup_data: (mimetype offset of the first matching entry, its priority as an int).  The
    string is not read here: GLib keeps the pointer and dereferences it only if the entry wins."""
    lo = c.u32(24)
    if oob(lo, 1, 12, c.size):
        return None, 0
    n = c.u32(lo)
    off = c.u32(lo + 8)
    if oob(off, n, 16, c.size):
        return None, 0
    for j in range(n):
        e = off + 16 * j
        prio = c.u32(e)
        mo = c.u32(e + 4)
        nm = c.u32(e + 8)
        mlo = c.u32(e + 12)
        if oob(mlo, nm, 32, c.size):
            continue
        for k in range(nm):
            if matchlet(c, mlo + 32 * k, data):
                return mo, _s32(prio)
    return None, 0


def mime_type_for_data(caches: list, data: bytes) -> tuple[str, int]:
    if len(data) == 0:
        return EMPTY, 100
    priority, win = 0, None
    for c in caches:
        mo, p = cache_magic_lookup(c, data)
        if p > priority:
            priority, win = p, (c, mo)
    if priority > 0:
        return win[0].cstr(win[1]).decode("utf-8", "surrogateescape"), priority
    for b in data[:128]:
        if b < 32 and b not in (9, 10, 13):
            return UNKNOWN, 0
    return TEXTPLAIN, 0


def looks_like_text(data: bytes) -> bool:
    return not any(b < 8 or b == 11 or 14 <= b < 32 or b == 127 for b in data)


def _alias(caches: list, name: bytes) -> bytes:
    for c in caches:
        lo = c.u32(4)
        if oob(lo, 1, 4, c.size):
            continue
        n = c.u32(lo)
        if oob(lo + 4, n, 8, c.size):
            continue
        mn, mx = 0, n - 1
        while mx >= mn:
            mid = (mn + mx) // 2
            s = c.cstr(c.u32(lo + 4 + 8 * mid))
            if s < name:
                mn = mid + 1
            elif s > name:
                mx = mid - 1
            else:
                return c.cstr(c.u32(lo + 4 + 8 * mid + 4))
    return name


def _direct(caches: list, mime: bytes, base: bytes) -> tuple[bool, bytes, bytes]:
    """The checks _xdg_mime_cache_mime_type_subclass makes before the parent lists."""
    umime, ubase = _alias(caches, mime), _alias(caches, base)
    if umime == ubase:
        return True, umime, ubase
    if ubase.endswith(b"/*"):
        sep = umime.find(b"/")
        if sep >= 0 and umime[:sep + 1] == ubase[:sep + 1]:
            return True, umime, ubase
    if ubase == b"text/plain" and umime.startswith(b"text/"):
        return True, umime, ubase
    if ubase == b"application/octet-stream" and not umime.startswith(b"inode/"):
        return True, umime, ubase
    return False, umime, ubase


def _parents(caches: list, umime: bytes):
    """The parent pointers the C loop visits for umime: every cache in order, the entry its binary search finds."""
    for ci, c in enumerate(caches):
        lo = c.u32(8)
        if oob(lo, 1, 4, c.size):
            continue
        n = c.u32(lo)
        if oob(lo + 4, n, 8, c.size):
            continue
        mn, mx = 0, n - 1
        while mx >= mn:
            mid = (mn + mx) // 2
            s = c.cstr(c.u32(lo + 4 + 8 * mid))
            if s < umime:
                mn = mid + 1
            elif s > umime:
                mx = mid - 1
            else:
                po = c.u32(lo + 4 + 8 * mid + 4)
                for j in range(c.u32(po)):
                    yield ci, c.u32(po + 4 + 4 * j)
                break


def subclass(caches: list, mime: bytes, base: bytes) -> bool:
    """_xdg_mime_cache_mime_type_subclass, iterative: each frame is the recursive call on a parent with the
    caller's unaliased base; the seen list (parent pointers = (cache, offset)) is shared by every frame."""
    hit, umime, ubase = _direct(caches, mime, base)
    if hit:
        return True
    seen: set[tuple[int, int]] = set()
    stack = [(_parents(caches, umime), ubase)]
    while stack:
        if len(stack) > MAX_NEST:
            raise Unsupported("parent chain deeper than 4096 (declared limit; the C recursion overflows deeper)")
        gen, ub = stack[-1]
        nxt = next(gen, None)
        if nxt is None:
            stack.pop()
            continue
        if nxt in seen:
            continue
        seen.add(nxt)
        hit, um2, ub2 = _direct(caches, caches[nxt[0]].cstr(nxt[1]), ub)
        if hit:
            return True
        stack.append((_parents(caches, um2), ub2))
    return False


class Sniffer:
    def __init__(self, dirs: list[str]):
        self.dirs = dirs
        self.resolver = mg.Resolver(dirs)
        self.mode = self.resolver.mode
        if self.mode == "cache":
            self.caches = self.resolver.db.caches
            return
        # xdgmime.c:129-206: a directory without a loadable cache is read as text files; with none of them anywhere
        # GLib's tables are empty and every answer is the fallback, which this tool models.
        text = [d + n for d in dirs for n in ("/globs2", "/globs", "/magic", "/aliases", "/subclasses")
                if os.path.exists(d + n)]
        if text:
            raise Unsupported("text mode (no loadable mime.cache; GLib reads " + text[0] + ")")
        self.mode = "none"
        self.caches = []

    def guess(self, filename: bytes | None, data: bytes) -> dict:
        types: list[str] = []
        if filename is not None:
            if filename.endswith(b"/"):
                return {"type": "inode/directory", "uncertain": 1, "types": ["inode/directory"],
                        "sniffed": None, "prio": 0}
            types = self.resolver.db.lookup(mg.g_path_get_basename(filename))
            if len(types) == 1:
                return {"type": types[0], "uncertain": 0, "types": types, "sniffed": None, "prio": 0}
        sniffed, prio = mime_type_for_data(self.caches, data)
        if sniffed is UNKNOWN and looks_like_text(data):
            sniffed = "text/plain"
        if filename is not None and sniffed == "application/x-desktop":
            sniffed = "text/plain"
        out = {"types": types, "sniffed": str(sniffed), "prio": prio}
        if not types:
            return dict(out, type=str(sniffed), uncertain=1 if sniffed is UNKNOWN else 0)
        if sniffed is not UNKNOWN:
            if prio >= 80:
                return dict(out, type=str(sniffed), uncertain=0)
            sb = str(sniffed).encode("utf-8", "surrogateescape")
            for t in types:
                if subclass(self.caches, t.encode("utf-8", "surrogateescape"), sb):
                    return dict(out, type=t, uncertain=0)
        return dict(out, type=types[0], uncertain=1)


# ---------------------------------------------------------------- cache builder (selftest fixtures)

def build_cache(aliases=(), parents=(), literals=(), globs=(), magic=()) -> bytes:
    """A mime.cache 1.2 with the given sections.  magic: [(priority, mime, [matchlet])], matchlet =
    dict(start, length, value, mask=None, word=1, children=[matchlet...]).  No suffix tree entries."""
    strings: dict[bytes, int] = {}
    blob = bytearray(40)

    def align():
        while len(blob) % 4:
            blob.append(0)

    def s(x) -> int:
        x = x.encode() if isinstance(x, str) else x
        if x not in strings:
            strings[x] = len(blob)
            blob.extend(x + b"\0")
        return strings[x]

    def u32(v: int) -> bytes:
        return struct.pack(">I", v & M32)

    # strings first
    for a, m in aliases:
        s(a), s(m)
    for m, ps in parents:
        s(m)
        for p in ps:
            s(p)
    for lit, m, w in literals:
        s(lit), s(m)
    for g, m, w in globs:
        s(g), s(m)
    for _p, m, _ms in magic:
        s(m)

    def values(ml):
        ml["_v"] = len(blob)
        blob.extend(ml["value"])
        if ml.get("mask") is not None:
            ml["_m"] = len(blob)
            blob.extend(ml["mask"])
        else:
            ml["_m"] = 0
        for ch in ml.get("children", []):
            values(ch)

    for _p, _m, ms in magic:
        for ml in ms:
            values(ml)
    align()
    hdr = {}
    hdr[4] = len(blob)
    al = sorted(aliases, key=lambda x: x[0].encode() if isinstance(x[0], str) else x[0])
    blob.extend(u32(len(al)))
    for a, m in al:
        blob.extend(u32(s(a)) + u32(s(m)))
    pl = sorted(parents, key=lambda x: x[0].encode() if isinstance(x[0], str) else x[0])
    plist_at = len(blob)
    blob.extend(u32(len(pl)) + b"\0" * (8 * len(pl)))
    for i, (m, ps) in enumerate(pl):
        at = len(blob)
        blob.extend(u32(len(ps)))
        for p in ps:
            blob.extend(u32(s(p)))
        blob[plist_at + 4 + 8 * i: plist_at + 12 + 8 * i] = u32(s(m)) + u32(at)
    hdr[8] = plist_at
    hdr[12] = len(blob)
    ll = sorted(literals, key=lambda x: x[0].encode() if isinstance(x[0], str) else x[0])
    blob.extend(u32(len(ll)))
    for lit, m, w in ll:
        blob.extend(u32(s(lit)) + u32(s(m)) + u32(w))
    hdr[16] = len(blob)
    blob.extend(u32(0) + u32(len(blob) + 8))
    hdr[20] = len(blob)
    blob.extend(u32(len(globs)))
    for g, m, w in globs:
        blob.extend(u32(s(g)) + u32(s(m)) + u32(w))

    def place(mls) -> int:
        at = len(blob)
        blob.extend(b"\0" * (32 * len(mls)))
        for i, ml in enumerate(mls):
            kids = ml.get("children", [])
            ko = place(kids) if kids else 0
            rec = (u32(ml["start"]) + u32(ml["length"]) + u32(ml.get("word", 1)) + u32(len(ml["value"]))
                   + u32(ml["_v"]) + u32(ml["_m"]) + u32(len(kids)) + u32(ko))
            blob[at + 32 * i: at + 32 * i + 32] = rec
        return at

    hdr[24] = len(blob)
    blob.extend(u32(len(magic)) + u32(0) + u32(len(blob) + 12))
    mat = len(blob)
    blob.extend(b"\0" * (16 * len(magic)))
    for i, (p, m, ms) in enumerate(magic):
        mo = place(ms) if ms else 0
        blob[mat + 16 * i: mat + 16 * i + 16] = u32(p) + u32(s(m)) + u32(len(ms)) + u32(mo)
    for k in (28, 32, 36):
        hdr[k] = len(blob)
    blob.extend(u32(0))
    blob[0:4] = struct.pack(">HH", 1, 2)
    for k, v in hdr.items():
        blob[k:k + 4] = u32(v)
    return bytes(blob)


def esc(b: bytes) -> str:
    return mg.esc(b)


def selftest() -> int:
    import tempfile
    checks: list[tuple[str, bool]] = []

    def ml(start, length, value, mask=None, children=()):
        return {"start": start, "length": length, "value": value, "mask": mask, "children": list(children)}

    with tempfile.TemporaryDirectory() as root:
        def w(rel: str, data: bytes) -> str:
            p = os.path.join(root, rel)
            os.makedirs(os.path.dirname(p), exist_ok=True)
            with open(p, "wb") as fh:
                fh.write(data)
            return p

        w("a/mime/mime.cache", build_cache(
            aliases=[("text/x-old", "text/x-new")],
            parents=[("app/child", ["app/mid"]), ("app/mid", ["app/base"])],
            globs=[("*.dup", "app/child", 50), ("*.dup", "text/x-old", 50), ("*.two", "t/one", 50),
                   ("*.two", "t/other", 50), ("*.one", "t/single", 50), ("*.amb", "app/x-a", 50),
                   ("*.amb", "app/x-b", 50)],
            magic=[(90, "app/hi", [ml(0, 1, b"HI")]),
                   (60, "app/range", [ml(2, 3, b"RG")]),
                   (55, "app/masked", [ml(0, 1, b"\x10\x00", b"\xf0\x00")]),
                   (50, "app/nest", [ml(0, 1, b"NE", children=[ml(4, 1, b"X"), ml(4, 1, b"Y")])]),
                   (50, "app/base", [ml(0, 1, b"BA")]),
                   (40, "application/x-desktop", [ml(0, 1, b"[Desktop Entry]")]),
                   (30, "app/lo", [ml(0, 1, b"LO")])]))
        w("b/mime/mime.cache", build_cache(magic=[(95, "app/b-hi", [ml(0, 1, b"LO")]),
                                                  (60, "app/b-eq", [ml(0, 1, b"RGRG")])]))
        a = Sniffer([os.path.join(root, "a/mime")])
        ab = Sniffer([os.path.join(root, "a/mime"), os.path.join(root, "b/mime")])

        def g(s, name, data):
            r = s.guess(name, data)
            return r["type"], r["uncertain"]

        checks += [
            ("s01 first match in cache order", g(a, None, b"HI there") == ("app/hi", 0)),
            ("s02 range offset", g(a, None, b"\x01\x01\x01\x01RG") == ("app/range", 0)),
            ("s03 range end is exclusive", g(a, None, b"\x01\x01\x01\x01\x01RG") == ("application/octet-stream", 1)),
            ("s04 mask", g(a, None, b"\x1f\x99") == ("app/masked", 0)),
            ("s05 child must hold", g(a, None, b"NE\x01\x01Y") == ("app/nest", 0)),
            ("s06 parent alone fails with children", g(a, None, b"NE\x01\x01Z") == ("application/octet-stream", 1)),
            ("s07 empty data is zerosize", g(a, None, b"") == ("application/x-zerosize", 0)),
            ("s08 text fallback", g(a, None, b"plain words\n") == ("text/plain", 0)),
            ("s09 binary fallback uncertain", g(a, None, b"\x01\x02") == ("application/octet-stream", 1)),
            ("s10 VT is not text, FF is", (g(a, None, b"ab\x0bcd"), g(a, None, b"ab\x0ccd"))
             == (("application/octet-stream", 1), ("text/plain", 0))),
            ("s11 fallback reads 128 bytes only", g(a, None, b"a" * 128 + b"\x01") == ("text/plain", 0)),
            ("s12 desktop sniff without a name", g(a, None, b"[Desktop Entry]\n") == ("application/x-desktop", 0)),
            ("s13 desktop sniff with a name is text", g(a, b"zz.nomatch", b"[Desktop Entry]\n") == ("text/plain", 0)),
            ("s14 one name type skips sniffing", g(a, b"x.one", b"HI") == ("t/single", 0)),
            ("s15 prio >= 80 beats two name types", g(a, b"x.two", b"HI") == ("app/hi", 0)),
            ("s16 subclass picks the name type", g(a, b"x.dup", b"BA") == ("app/child", 0)),
            ("s17 alias unaliased in subclass", g(a, b"x.dup", b"plain\n") == ("text/x-old", 0)),
            ("s18 no subclass -> first name, uncertain", g(a, b"x.amb", b"LO") == ("app/x-a", 1)),
            ("s19 strictly greater prio across caches", g(ab, None, b"LO") == ("app/b-hi", 0)),
            ("s20 equal prio keeps the first cache", g(ab, None, b"RGRG") == ("app/range", 0)),
            ("s21 trailing slash", g(a, b"d/", b"HI") == ("inode/directory", 1)),
            ("s22 empty data beats two name types", g(a, b"x.two", b"") == ("application/x-zerosize", 0)),
        ]
        w("t/mime/globs2", b"50:text/plain:*.txt\n")
        try:
            Sniffer([os.path.join(root, "t/mime")])
            checks.append(("s23 text mode refused", False))
        except Unsupported:
            checks.append(("s23 text mode refused", True))
        os.makedirs(os.path.join(root, "n/mime"), exist_ok=True)
        nd = Sniffer([os.path.join(root, "n/mime")])
        checks.append(("s24 no database answers the fallback",
                       (nd.mode, g(nd, None, b"hi\n"), g(nd, None, b"\x01"), g(nd, b"f.txt", b""))
                       == ("none", ("text/plain", 0), ("application/octet-stream", 1), ("application/x-zerosize", 0))))
        chain = [(f"app/c{k:04d}", [f"app/c{k + 1:04d}"]) for k in range(5000)]
        w("p/mime/mime.cache", build_cache(parents=chain, globs=[("*.x", "app/c0000", 50), ("*.x", "app/zz", 50),
                                                                ("*.y", "app/c1000", 50), ("*.y", "app/zz", 50)],
                                           magic=[(40, "app/c5000", [ml(0, 1, b"B")])]))
        p = Sniffer([os.path.join(root, "p/mime")])
        try:
            g(p, b"f.x", b"B")
            deep = "answered"
        except Unsupported:
            deep = "refused"
        checks.append(("s25 parent chain: 4000 answered, 5000 refused", (g(p, b"f.y", b"B"), deep)
                       == (("app/c1000", 0), "refused")))
        cb = bytearray(build_cache(magic=[(60, "app/wrapz", [ml(1, 1, b"Z")])]))
        mlo = struct.unpack_from(">I", cb, struct.unpack_from(">I", cb, struct.unpack_from(">I", cb, 24)[0] + 8)[0] + 12)[0]
        struct.pack_into(">I", cb, mlo + 12, M32)  # value_length 2^32-1: the 32-bit sum 1 + len wraps to 0
        w("u/mime/mime.cache", bytes(cb))
        u = Sniffer([os.path.join(root, "u/mime")])
        try:
            g(u, None, b"AZ")
            past = "answered"
        except Unsupported:
            past = "refused"
        checks.append(("s26 wrapped compare stops at the first difference, refuses past the data",
                       (g(u, None, b"AY"), past) == (("text/plain", 0), "refused")))
    failed = [n for n, ok in checks if not ok]
    for n in failed:
        print(f"MADO_MIMESNIFF_SELFTEST_FAIL: {n}")
    print(f"MADO_MIMESNIFF_SELFTEST: checks={len(checks)} failed={len(failed)}")
    return 1 if failed else 0


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("files", nargs="*", help="files whose bytes are sniffed")
    ap.add_argument("--name", help="file name passed to GLib for every file (default: NULL)")
    ap.add_argument("--names-from-files", action="store_true", help="pass each FILE path as the name")
    ap.add_argument("--data-home")
    ap.add_argument("--data-home-unset", action="store_true")
    ap.add_argument("--data-dirs")
    ap.add_argument("--data-dirs-unset", action="store_true")
    ap.add_argument("--home")
    ap.add_argument("--home-unset", action="store_true")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args(argv)
    mg._libc.setlocale(mg._LC_ALL, b"C")
    if a.selftest:
        return selftest()
    if not a.files or (a.name is not None and a.names_from_files):
        print("mado-mimesniff: setup error: name at least one FILE; --name and --names-from-files exclude",
              file=sys.stderr)
        return 2
    env = os.environ
    home = None if a.home_unset else (a.home if a.home is not None else env.get("HOME"))
    dh = None if a.data_home_unset else (a.data_home if a.data_home is not None else env.get("XDG_DATA_HOME"))
    dd = None if a.data_dirs_unset else (a.data_dirs if a.data_dirs is not None else env.get("XDG_DATA_DIRS"))
    out = []
    try:
        s = Sniffer(mg.xdgmime_dirs(dh, home, dd))
        for f in a.files:
            fb = os.fsencode(f)
            try:
                with open(f, "rb") as fh:
                    data = fh.read()
            except OSError as e:
                print(f"mado-mimesniff: setup error: {f}: {e.strerror}", file=sys.stderr)
                return 2
            name = fb if a.names_from_files else (os.fsencode(a.name) if a.name is not None else None)
            r = s.guess(name, data)
            out.append(dict(r, file=esc(fb), name=None if name is None else esc(name)))
    except Unsupported as e:
        print(f"MADO_MIMESNIFF: UNSUPPORTED {e}")
        return 3
    if a.json:
        print(json.dumps({"mode": s.mode, "dirs": s.dirs, "results": out}, sort_keys=True))
    else:
        print(f"MADO_MIMESNIFF_DIRS: mode={s.mode} dirs={','.join(s.dirs)}")
        for x in out:
            print(f"MADO_MIMESNIFF: {x['type']} uncertain={x['uncertain']} name={x['name'] or '-'} file={x['file']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
