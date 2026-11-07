#!/usr/bin/env python3
"""mado-mimeglob — which MIME type GLib guesses from a file name alone.

Read-only resolver for the name-to-type step of the default-application plane: given the XDG
data roots, print what GLib 2.90.1's g_content_type_guess (filename, NULL, 0, &uncertain) answers
for a file name — the content type and the uncertain flag — from the shared-mime-info databases
(globs2/globs text files or the binary mime.cache), as the installed library reads them.

Upstream model (GLib tag 2.90.1; line numbers are that tag's files):
  dirs       gio/xdgmime/xdgmime.c xdg_init_dirs (:220-300): XDG_DATA_HOME + /mime/ (if set, even
             empty), else $HOME + /.local/share/mime/ (if HOME is set, even empty), else no user dir; then
             each non-empty XDG_DATA_DIRS element (unset -> /usr/local/share/:/usr/share/) + /mime/.
  mode       xdg_mime_init_from_directory (:129-200): per dir, a mime.cache that opens, is >= 40
             bytes and has version 1.1-1.2 is a cache and the dir's globs are not read; otherwise
             globs2 (weight:type:glob[:flags]) or, if absent, globs (type:glob, weight 50).  When at
             least one cache loaded, every name lookup uses only the caches (:645-646).
  text       gio/xdgmime/xdgmimeglob.c: lines are fgets(…, 255) chunks (:643); a glob is literal,
             simple (one leading '*', no other '*', '\\', '[', '?') or full (:536-559).  Lookup
             (:419-494): literals exact, then case-folded literals that are not cs (first list hit,
             a single answer); simple globs in a reversed-suffix trie, deepest match only, first on
             the ASCII-lowercased name excluding cs globs, then (if fewer than 2) on the name
             including them (:463-467); full globs with fnmatch(3) flags 0 on the unfolded name
             only if fewer than 2 (:469-480); duplicates merged keeping the larger weight with the
             swap-from-the-end order (:391-417); sorted by weight, descending.
  cache      gio/xdgmime/xdgmimecache.c cache_glob_lookup_file_name (:668-724): per cache, literal
             binary search (a cs hit on the folded pass ends the literal search), the reverse
             suffix tree per cache (each cache adds its own deepest match), fnmatch list, weight in
             the low 8 bits and 0x100 = cs; same merge and sort.
  guess      gio/gcontenttype-fdo.c g_content_type_guess_impl (:567-690): a trailing '/' is
             inode/directory, uncertain; else the basename's types: one -> it, certain; none ->
             application/octet-stream, uncertain; several -> the first, uncertain.

A name byte >= 0x80 is compared as a sign-extended value (the C code widens a signed char), so it never
matches a decoded multi-byte glob character, only the same lone byte.  fnmatch runs through the C library in the "C" locale (the oracle does not call
setlocale).  Glob bytes are decoded as xdgmimeint.c does (no validation; a lone continuation or 0xFE/0xFF byte
becomes a sign-extended value that can match the same name byte); a bare `*` glob is inert.  The tool
refuses (exit 3, UNSUPPORTED) only where the C code is undefined or never returns: a glob that ends inside
a multi-byte sequence, a weight outside +/-2^30, a cache suffix node that fails the bounds check (the C
lookup loops), and a cache read past the zero-filled last page of the mapping.

Usage:
  mado-mimeglob.py NAME... [--data-home D | --data-home-unset] [--data-dirs LIST | --data-dirs-unset]
                  [--home H | --home-unset] [--json]
  mado-mimeglob.py --selftest

Output: one line per name, `MADO_MIMEGLOB: <type> uncertain=<0|1> name=<escaped>`; --json prints
{"mode", "dirs", "results": [{"name", "type", "uncertain", "types"}]}.  ASCII only, stdlib only.
Exit 0 answered, 2 setup error, 3 unsupported input.
"""
from __future__ import annotations

import argparse
import ctypes
import ctypes.util
import json
import os
import struct
import sys

UNKNOWN = "application/octet-stream"
N_MIMES = 10
_libc = ctypes.CDLL(ctypes.util.find_library("c") or "libc.so.6", use_errno=True)
_libc.fnmatch.argtypes = [ctypes.c_char_p, ctypes.c_char_p, ctypes.c_int]
_libc.fnmatch.restype = ctypes.c_int
_libc.setlocale.argtypes = [ctypes.c_int, ctypes.c_char_p]
_libc.setlocale.restype = ctypes.c_char_p
_LC_ALL = 6


class Unsupported(Exception):
    pass


def fnmatch_c(pattern: bytes, name: bytes) -> bool:
    return _libc.fnmatch(pattern, name, 0) == 0


def ascii_tolower(b: bytes) -> bytes:
    return bytes(c + 32 if 65 <= c <= 90 else c for c in b)


def c_char(byte: int) -> int:
    """xdg_unichar_t character = file_name[len - 1]: a signed char widened to 32 bits."""
    return byte if byte < 0x80 else (byte - 256) & 0xFFFFFFFF


def _fgets_lines(data: bytes) -> list[bytes]:
    """Split like repeated fgets(line, 255, f): chunks of at most 254 bytes, ending after '\\n'."""
    out: list[bytes] = []
    i = 0
    while i < len(data):
        nl = data.find(b"\n", i, i + 254)
        end = nl + 1 if nl >= 0 else min(i + 254, len(data))
        out.append(data[i:end])
        i = end
    return out


def c_atoi(b: bytes) -> int:
    i = 0
    while i < len(b) and b[i] in b" \t\n\v\f\r":
        i += 1
    sign = 1
    if i < len(b) and b[i] in b"+-":
        sign = -1 if b[i] == 45 else 1
        i += 1
    j = i
    while j < len(b) and 48 <= b[j] <= 57:
        j += 1
    v = sign * int(b[i:j]) if j > i else 0
    if abs(v) > (1 << 30):
        raise Unsupported(f"weight {v} outside +/-2^30")
    return v


_SKIP = [1] * 192 + [2] * 32 + [3] * 16 + [4] * 8 + [5] * 4 + [6] * 2 + [1] * 2  # xdgmimeint.c _xdg_utf8_skip_data


def xdg_char_starts(b: bytes) -> list[int]:
    """Positions _xdg_utf8_next_char visits (xdgmimeint.h:51).  No validation (_xdg_utf8_validate is
    `return TRUE`); a sequence whose skip runs past the string end makes the C code read past the NUL:
    refused."""
    out: list[int] = []
    i = 0
    while i < len(b):
        out.append(i)
        i += _SKIP[b[i]]
    if i > len(b):
        raise Unsupported("glob ends inside a multi-byte sequence (the C decoder reads past the string)")
    return out


def _s8(x: int) -> int:
    """A C char (signed on this host) converted to xdg_unichar_t (unsigned 32)."""
    return x if x < 0x80 else (x - 256) & 0xFFFFFFFF


def xdg_utf8_to_ucs4(b: bytes, i: int) -> int:
    """xdgmimeint.c _xdg_utf8_to_ucs4, with the signed-char arithmetic of the C code."""
    c = b[i]
    if not c & 0x80 or not c & 0x40:
        return _s8(c)
    for mask, keep, n in ((0x20, 0x1F, 2), (0x10, 0x0F, 3), (0x08, 0x07, 4), (0x04, 0x03, 5), (0x02, 0x01, 6)):
        if not c & mask:
            r = c & keep
            break
    else:
        r, n = _s8(c), 1
    for k in range(1, n):
        r = ((r << 6) | (b[i + k] & 0x3F)) & 0xFFFFFFFF
    return r


def glob_type(glob: bytes) -> str:
    """xdgmimeglob.c _xdg_glob_determine_type: only the bytes at character starts are tested."""
    maybe_simple = False
    for k, i in enumerate(xdg_char_starts(glob)):
        ch = glob[i:i + 1]
        if ch == b"*" and k == 0:
            maybe_simple = True
        elif ch in (b"\\", b"[", b"?", b"*"):
            return "full"
    return "simple" if maybe_simple else "literal"


# ---------------------------------------------------------------- text mode (xdgmimeglob.c)

class _Node:
    __slots__ = ("char", "mime", "weight", "cs", "children")

    def __init__(self, char: int):
        self.char = char
        self.mime: str | None = None
        self.weight = 0
        self.cs = False
        self.children: list[_Node] = []  # sorted by char; char-0 entries (extra types) first


def _insert(siblings: list[_Node], text: list[int], mime: str, weight: int, cs: bool) -> None:
    ch = text[0]
    node = None
    pos = 0
    while pos < len(siblings) and siblings[pos].char < ch:
        pos += 1
    if pos < len(siblings) and siblings[pos].char == ch:
        node = siblings[pos]
    else:
        node = _Node(ch)
        siblings.insert(pos, node)
    rest = text[1:]
    if not rest:
        if node.mime is not None:
            if node.mime != mime:
                for c in node.children:
                    if c.char != 0:
                        break
                    if c.mime == mime:
                        return
                extra = _Node(0)
                extra.mime, extra.weight, extra.cs = mime, weight, cs
                node.children.insert(0, extra)
        else:
            node.mime, node.weight, node.cs = mime, weight, cs
    else:
        _insert(node.children, rest, mime, weight, cs)


def _lookup(siblings: list[_Node], name: bytes, length: int, check: bool, cap: int) -> list[tuple[str, int]]:
    """_xdg_glob_hash_node_lookup_file_name, unrolled: descend while a sibling equals the next character from
    the end, then the deepest node that yields a type wins (a deeper level returning 0 hands back up)."""
    if cap <= 0:
        return []
    path: list[_Node] = []
    while siblings and length > 0:
        ch = c_char(name[length - 1])
        hit = None
        for node in siblings:
            if ch < node.char:
                break
            if ch == node.char:
                hit = node
                break
        if hit is None:
            break
        path.append(hit)
        length -= 1
        siblings = hit.children
    for node in reversed(path):
        out: list[tuple[str, int]] = []
        if node.mime is not None and (check or not node.cs):
            out.append((node.mime, node.weight))
        for c in node.children:
            if len(out) >= cap or c.char != 0:
                break
            if c.mime is not None and (check or not c.cs):
                out.append((c.mime, c.weight))
        if out:
            return out
    return []


class TextDB:
    def __init__(self) -> None:
        self.literals: list[tuple[bytes, str, int, bool]] = []
        self.full: list[tuple[bytes, str, int, bool]] = []
        self.trie: list[_Node] = []

    @staticmethod
    def _append(lst: list, data: bytes, mime: str, weight: int, cs: bool) -> None:
        for d, m, _w, _c in lst:
            if d == data and m == mime:
                return
        lst.append((data, mime, weight, cs))

    def read(self, path: str, version_two: bool) -> None:
        with open(path, "rb") as fh:
            data = fh.read()
        for chunk in _fgets_lines(data):
            if chunk[:1] in (b"#", b"\0"):
                continue
            line = chunk.split(b"\0", 1)[0]
            if line.endswith(b"\n"):
                line = line[:-1]
            p = line
            if version_two:
                k = p.find(b":")
                if k < 0:
                    continue
                weight = c_atoi(p[:k])
                p = p[k + 1:]
            else:
                weight = 50
            k = p.find(b":")
            if k < 0:
                continue
            mime_b, p = p[:k], p[k + 1:]
            glob_b = p
            cs = False
            k = p.find(b":")
            if version_two and k >= 0:
                glob_b, flags = p[:k], p[k + 1:]
                k2 = flags.find(b":")
                if k2 >= 0:
                    flags = flags[:k2]
                f = flags.find(b"cs")
                if f >= 0 and (f == 0 or flags[f - 1:f] == b",") and flags[f + 2:f + 3] in (b"", b","):
                    cs = True
            mime = mime_b.decode("utf-8", "surrogateescape")
            t = glob_type(glob_b)
            if t == "literal":
                self._append(self.literals, glob_b, mime, weight, cs)
            elif t == "full":
                self._append(self.full, glob_b, mime, weight, cs)
            else:
                rest = glob_b[1:]
                suffix = [xdg_utf8_to_ucs4(rest, i) for i in xdg_char_starts(rest)]
                if not suffix:
                    # `*`: _xdg_glob_hash_insert_ucs4 gets an empty string, stores a root node of character 0
                    # and reads past the array (undefined); observed inert (no name ends in a NUL): skipped.
                    continue
                _insert(self.trie, suffix[::-1], mime, weight, cs)

    def lookup(self, name: bytes) -> list[str]:
        lower = ascii_tolower(name)
        for d, m, _w, _c in self.literals:
            if d == name:
                return [m]
        for d, m, _w, c in self.literals:
            if not c and d == lower:
                return [m]
        mimes = _lookup(self.trie, lower, len(name), False, N_MIMES)
        if len(mimes) < 2:
            mimes += _lookup(self.trie, name, len(name), True, N_MIMES - len(mimes))
        if len(mimes) < 2:
            for d, m, w, _c in self.full:
                if len(mimes) >= N_MIMES:
                    break
                if fnmatch_c(d, name):
                    mimes.append((m, w))
        return finish(mimes)


# ---------------------------------------------------------------- cache mode (xdgmimecache.c)

def oob(offset: int, n: int, record: int, size: int) -> bool:
    return bool(offset & 3) or offset > size or n > (size - offset) // record


class Cache:
    """The cache as GLib maps it: st_size bytes, read through an mmap whose last page is zero-filled past the
    end of the file.  Bounds checks use the file size (OUT_OF_BOUNDS); an unchecked read inside the last page
    sees zeros; a read past the mapping would fault in C: refused."""

    def __init__(self, buf: bytes):
        self.size = len(buf)
        page = os.sysconf("SC_PAGE_SIZE")
        self.buf = buf + b"\0" * (-len(buf) % page)

    def u32(self, off: int) -> int:
        if off + 4 > len(self.buf):
            raise Unsupported("cache read past the mapping")
        return struct.unpack_from(">I", self.buf, off)[0]

    def cstr(self, off: int) -> bytes:
        end = self.buf.find(b"\0", off) if off < len(self.buf) else -1
        if end < 0:
            raise Unsupported("cache string runs past the mapping")
        return self.buf[off:end]


def load_cache(path: str) -> Cache | None:
    try:
        with open(path, "rb") as fh:
            buf = fh.read()
    except OSError:
        return None
    if len(buf) < 40:
        return None
    major, minor = struct.unpack_from(">HH", buf, 0)
    if major != 1 or not (1 <= minor <= 2):
        return None
    return Cache(buf)


def _cache_literal(caches: list[Cache], name: bytes, check: bool) -> list[str]:
    for c in caches:
        lo = c.u32(12)
        if oob(lo, 1, 4, c.size):
            continue
        n = c.u32(lo)
        if oob(lo + 4, n, 12, c.size):
            continue
        mn, mx = 0, n - 1
        while mx >= mn:
            mid = (mn + mx) // 2
            s = c.cstr(c.u32(lo + 4 + 12 * mid))
            if s < name:
                mn = mid + 1
            elif s > name:
                mx = mid - 1
            else:
                w = c.u32(lo + 4 + 12 * mid + 8)
                if check or not (w & 0x100):
                    return [c.cstr(c.u32(lo + 4 + 12 * mid + 4)).decode("utf-8", "surrogateescape")]
                return []
    return []


def _cache_suffix_node(c: Cache, n_entries: int, offset: int, name: bytes, length: int, check: bool,
                       cap: int) -> list[tuple[str, int]]:
    """cache_glob_node_lookup_suffix, unrolled like _lookup: binary search per level, deepest yield wins."""
    path: list[tuple[int, int]] = []
    while length > 0:
        ch = c_char(name[length - 1])
        mn, mx = 0, n_entries - 1
        hit = None
        while mx >= mn:
            mid = (mn + mx) // 2
            mc = c.u32(offset + 12 * mid)
            if mc < ch:
                mn = mid + 1
            elif mc > ch:
                mx = mid - 1
            else:
                hit = mid
                break
        if hit is None:
            break
        n_children = c.u32(offset + 12 * hit + 4)
        child_offset = c.u32(offset + 12 * hit + 8)
        if oob(child_offset, n_children, 12, c.size):
            raise Unsupported("cache suffix node out of bounds (the C lookup loops)")
        path.append((n_children, child_offset))
        length -= 1
        n_entries, offset = n_children, child_offset
    for n_children, child_offset in reversed(path):
        out: list[tuple[str, int]] = []
        i = 0
        while len(out) < cap and i < n_children:
            if c.u32(child_offset + 12 * i) != 0:
                break
            mo = c.u32(child_offset + 12 * i + 4)
            w = c.u32(child_offset + 12 * i + 8)
            if check or not (w & 0x100):
                out.append((c.cstr(mo).decode("utf-8", "surrogateescape"), w & 0xFF))
            i += 1
        if out:
            return out
    return []


def _cache_suffix(caches: list[Cache], name: bytes, length: int, check: bool, cap: int) -> list[tuple[str, int]]:
    out: list[tuple[str, int]] = []
    for c in caches:
        lo = c.u32(16)
        if oob(lo, 1, 8, c.size):
            continue
        n_entries = c.u32(lo)
        offset = c.u32(lo + 4)
        if oob(offset, n_entries, 12, c.size):
            continue
        out += _cache_suffix_node(c, n_entries, offset, name, length, check, cap - len(out))
        if len(out) >= cap:
            break
    return out


def _cache_fnmatch(caches: list[Cache], name: bytes, check: bool, cap: int) -> list[tuple[str, int]]:
    out: list[tuple[str, int]] = []
    for c in caches:
        lo = c.u32(20)
        if oob(lo, 1, 4, c.size):
            continue
        n = c.u32(lo)
        if oob(lo + 4, n, 12, c.size):
            continue
        j = 0
        while j < n and len(out) < cap:
            po = c.u32(lo + 4 + 12 * j)
            mo = c.u32(lo + 4 + 12 * j + 4)
            w = c.u32(lo + 4 + 12 * j + 8)
            if (check or not (w & 0x100)) and fnmatch_c(c.cstr(po), name):
                out.append((c.cstr(mo).decode("utf-8", "surrogateescape"), w & 0xFF))
            j += 1
        if len(out) == cap:
            break
    return out


class CacheDB:
    def __init__(self, caches: list[Cache]):
        self.caches = caches

    def lookup(self, name: bytes) -> list[str]:
        lower = ascii_tolower(name)
        r = _cache_literal(self.caches, lower, False)
        if r:
            return r
        r = _cache_literal(self.caches, name, True)
        if r:
            return r
        mimes = _cache_suffix(self.caches, lower, len(name), False, N_MIMES)
        if len(mimes) < 2:
            mimes += _cache_suffix(self.caches, name, len(name), True, N_MIMES - len(mimes))
        if not mimes:
            mimes = _cache_fnmatch(self.caches, lower, False, N_MIMES)
        if len(mimes) < 2:
            mimes += _cache_fnmatch(self.caches, name, True, N_MIMES - len(mimes))
        return finish(mimes)


# ---------------------------------------------------------------- shared

def finish(mimes: list[tuple[str, int]]) -> list[str]:
    """filter_out_dupes (swap-from-end) then qsort by weight descending (glibc's stable merge sort)."""
    a = [list(x) for x in mimes]
    last = len(a)
    i = 0
    while i < last:
        j = i + 1
        while j < last:
            if a[i][0] == a[j][0]:
                a[i][1] = max(a[i][1], a[j][1])
                last -= 1
                a[j] = list(a[last])
            else:
                j += 1
        i += 1
    a = a[:last]
    a.sort(key=lambda x: -x[1])
    return [m for m, _w in a[:N_MIMES]]


def xdgmime_dirs(data_home_env: str | None, home: str | None, data_dirs_env: str | None) -> list[str]:
    """xdgmime.c xdg_init_dirs (:220-300): XDG_DATA_HOME + "/mime/" if set (even empty); else, if HOME is set
    (even empty), HOME + "/.local/share/mime/" (string concatenation, so an empty HOME gives an absolute
    "/.local/share/mime/"); else no user dir.  XDG_DATA_DIRS unset -> /usr/local/share/:/usr/share/, set -> its
    non-empty elements, each + "/mime/"."""
    out: list[str] = []
    if data_home_env is not None:
        out.append(data_home_env + "/mime/")
    elif home is not None:
        out.append(home + "/.local/share/mime/")
    raw = data_dirs_env if data_dirs_env is not None else "/usr/local/share/:/usr/share/"
    return out + [d + "/mime/" for d in raw.split(":") if d]


class Resolver:
    def __init__(self, dirs: list[str]):
        self.dirs = dirs
        caches: list[Cache] = []
        texts: list[tuple[str, bool]] = []
        for d in dirs:
            cp = d + "/mime.cache"
            if os.path.exists(cp):
                c = load_cache(cp)
                if c is not None:
                    caches.append(c)
                    continue
            g2, g1 = d + "/globs2", d + "/globs"
            if os.path.exists(g2):
                texts.append((g2, True))
            elif os.path.exists(g1):
                texts.append((g1, False))
        self.mode = "cache" if caches else "text"
        if caches:
            # xdgmime.c:645-646: with any cache loaded the text hash is never consulted, so its files are not
            # parsed here (a line the tool would refuse cannot affect the answer).
            self.db = CacheDB(caches)
        else:
            text = TextDB()
            for path, v2 in texts:
                try:
                    text.read(path, v2)
                except OSError:
                    pass
            self.db = text

    def guess(self, filename: bytes) -> dict:
        if filename.endswith(b"/"):
            types = ["inode/directory"]
            return {"type": types[0], "uncertain": 1, "types": types}
        base = g_path_get_basename(filename)
        types = self.db.lookup(base)
        if len(types) == 1:
            return {"type": types[0], "uncertain": 0, "types": types}
        if not types:
            return {"type": UNKNOWN, "uncertain": 1, "types": types}
        return {"type": types[0], "uncertain": 1, "types": types}


def g_path_get_basename(p: bytes) -> bytes:
    if not p:
        return b"."
    q = p.rstrip(b"/")
    if not q:
        return b"/"
    return q.rsplit(b"/", 1)[-1]


def esc(b: bytes) -> str:
    return "".join(chr(c) if 33 <= c < 127 and c != 92 else f"\\x{c:02x}" for c in b)


def selftest() -> int:
    import tempfile
    checks: list[tuple[str, bool]] = []
    with tempfile.TemporaryDirectory() as root:
        def w(rel: str, data: bytes) -> None:
            p = os.path.join(root, rel)
            os.makedirs(os.path.dirname(p), exist_ok=True)
            with open(p, "wb") as fh:
                fh.write(data)

        def g(name: bytes, dirs: list[str]) -> tuple[str, int]:
            r = Resolver([os.path.join(root, d) for d in dirs]).guess(name)
            return r["type"], r["uncertain"]

        w("a/mime/globs2", b"50:text/plain:*.txt\n50:text/x-c:*.c:cs\n50:text/x-c++:*.C:cs\n"
          b"50:app/x-gz:*.gz\n50:app/x-tgz:*.tar.gz\n60:app/hi:*.dup\n40:app/lo:*.dup\n"
          b"50:text/x-make:Makefile\n50:app/full:x?y\n50:t/one:*.two\n50:t/other:*.two\n"
          b"80:a/ci:*.ci\n")
        w("b/mime/globs", b"text/old:*.old\n")
        checks += [
            ("t01 simple suffix", g(b"a.txt", ["a/mime"]) == ("text/plain", 0)),
            ("t02 folded suffix", g(b"A.TXT", ["a/mime"]) == ("text/plain", 0)),
            ("t03 cs glob only on the exact case", g(b"x.C", ["a/mime"]) == ("text/x-c++", 0)),
            ("t04 deepest suffix wins", g(b"x.tar.gz", ["a/mime"]) == ("app/x-tgz", 0)),
            ("t05 weight orders two types", g(b"x.dup", ["a/mime"]) == ("app/hi", 1)),
            ("t06 literal", g(b"Makefile", ["a/mime"]) == ("text/x-make", 0)),
            ("t07 literal is not folded", g(b"MAKEFILE", ["a/mime"]) == (UNKNOWN, 1)),
            ("t08 fnmatch full glob", g(b"xzy", ["a/mime"]) == ("app/full", 0)),
            ("t09 trailing slash", g(b"d/", ["a/mime"]) == ("inode/directory", 1)),
            ("t10 no match", g(b"zz", ["a/mime"]) == (UNKNOWN, 1)),
            ("t11 globs v1 file", g(b"f.old", ["b/mime"]) == ("text/old", 0)),
            ("t12 equal weight keeps file order", g(b"f.two", ["a/mime"]) == ("t/one", 1)),
            ("t13 non-ASCII byte never matches a suffix", g(b"x.t\xc3\xa9", ["a/mime"]) == (UNKNOWN, 1)),
            ("t14 basename only", g(b"dir.txt/f.c", ["a/mime"]) == ("text/x-c", 0)),
        ]
        w("c/mime/globs2", b"50:text/ff:*.\xff\n50:text/plain:*.txt\n50:t/any:*\n")
        checks += [
            ("t16 a 0xff glob byte matches the same name byte", g(b"x.\xff", ["c/mime"]) == ("text/ff", 0)),
            ("t17 a bare * is inert", g(b"a.txt", ["c/mime"]) == ("text/plain", 0)),
        ]
        w("e/mime/globs2", b"50:text/bad:*.\xc3\n")
        try:
            g(b"a", ["e/mime"])
            checks.append(("t15 truncated multi-byte glob refused", False))
        except Unsupported:
            checks.append(("t15 truncated multi-byte glob refused", True))
        checks.append(("t18 empty HOME is /.local/share/mime/", xdgmime_dirs(None, "", "") == ["/.local/share/mime/"]))
        checks.append(("t19 unset HOME adds no user dir", xdgmime_dirs(None, None, "/s") == ["/s/mime/"]))
    failed = [n for n, ok in checks if not ok]
    for n in failed:
        print(f"MADO_MIMEGLOB_SELFTEST_FAIL: {n}")
    print(f"MADO_MIMEGLOB_SELFTEST: checks={len(checks)} failed={len(failed)}")
    return 1 if failed else 0


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("names", nargs="*", help="file names (bytes via the filesystem encoding)")
    ap.add_argument("--data-home", help="XDG_DATA_HOME value (default: environment)")
    ap.add_argument("--data-home-unset", action="store_true")
    ap.add_argument("--data-dirs", help="XDG_DATA_DIRS value (default: environment)")
    ap.add_argument("--data-dirs-unset", action="store_true")
    ap.add_argument("--home", help="HOME value (default: environment)")
    ap.add_argument("--home-unset", action="store_true")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args(argv)
    _libc.setlocale(_LC_ALL, b"C")
    if a.selftest:
        return selftest()
    if not a.names:
        print("mado-mimeglob: setup error: name at least one file name", file=sys.stderr)
        return 2
    env = os.environ
    home = None if a.home_unset else (a.home if a.home is not None else env.get("HOME"))
    dh = None if a.data_home_unset else (a.data_home if a.data_home is not None else env.get("XDG_DATA_HOME"))
    dd = None if a.data_dirs_unset else (a.data_dirs if a.data_dirs is not None else env.get("XDG_DATA_DIRS"))
    try:
        r = Resolver(xdgmime_dirs(dh, home, dd))
        out = [dict(name=esc(os.fsencode(n)), **r.guess(os.fsencode(n))) for n in a.names]
    except Unsupported as e:
        print(f"MADO_MIMEGLOB: UNSUPPORTED {e}")
        return 3
    if a.json:
        print(json.dumps({"mode": r.mode, "dirs": r.dirs, "results": out}, sort_keys=True))
    else:
        print(f"MADO_MIMEGLOB_DIRS: mode={r.mode} dirs={','.join(r.dirs)}")
        for x in out:
            print(f"MADO_MIMEGLOB: {x['type']} uncertain={x['uncertain']} name={x['name']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
