#!/usr/bin/env python3
"""mado-mimetext -- which MIME type GLib guesses from bytes and a name in the TEXT database mode.

Read-only resolver for round 96's C1 surface: given the XDG data roots, print what GLib 2.90.1's
g_content_type_guess (name-or-NULL, data, len, &uncertain) answers when no reachable mime.cache loads
(the text database mode).  The magic step parses DIR/mime/magic (the MIME-Magic\\0\\n format) exactly as
gio/xdgmime/xdgmimemagic.c does; the name step is round 94's tools/mado-mimeglob.py, loaded lazily from
this file's own directory; the guess combination, the zerosize rule, the text fallback, the aliases and
subclasses steps and the mode rule follow round 95's tools/mado-mimesniff.py model.  A reachable
loadable mime.cache means cache mode, which this tool does not answer (exit 3, UNSUPPORTED cache-mode;
round 95's tools/mado-mimesniff.py owns that surface).

Upstream model (GLib tag 2.90.1; line numbers are that tag's files):
  magic file   xdgmimemagic.c _xdg_mime_magic_read_from_file (:801-819): only a file whose first 12
               bytes are exactly "MIME-Magic\\0\\n" is parsed; anything else contributes no magic.
  sections     _xdg_mime_magic_parse_header (:230-281): '[' + decimal priority (strtol; no digits,
               >INT_MAX or overflow -> -1 -> parse error) + ':' + the type up to the first ']' on the
               line (the line read stops at '\\n', '\\0' or EOF; no ']' -> parse error; EOF -> section
               dropped).
  matchlet     _xdg_mime_magic_parse_magic_line (:301-514): optional decimal indent, '>', decimal
               offset, '=', a two-byte big-endian value length, the value bytes, optional '&' + a mask
               of the same length, optional '~' + a word size (only 0, 1, 2, 4 pass :440-443; the C
               treats 0 like 1), optional '+' + a range length (default 1), then '\\n'.  A short value
               or mask read is EOF (feof); any other unexpected byte is a parse error.  On this
               little-endian host a word size of 2 or 4 byte-swaps the value (and the mask) per word at
               parse time (:469-505) and rejects value_length % word_size != 0; word sizes 0 and 1
               swap nothing.
  errors       _xdg_mime_magic_parse_error (:283-300) skips to the next newline; the section with the
               bad line is dropped whole (:749-782) and parsing resumes at the next line that starts a
               section.  A section is inserted when its header parsed and the next line starts a new
               section or the file ends there (:735-747) -- a matchlet-less section is inserted but its
               tree can never hold.
  order        _xdg_mime_magic_insert_match (:596-629) keeps ONE global list over all directories,
               priority descending, equal priorities in file order; _xdg_mime_magic_lookup_data
               (:652-700) returns the FIRST section whose matchlet tree holds, and its priority --
               text mode has no priority gate (xdgmime.c:535 passes NULL, 0 and uses the answer).
  tree         _xdg_mime_magic_matchlet_compare_level (:557-588): matchlets sit in file order; indent 0
               is a top-level test; a held test recurses only when the next matchlet sits at exactly
               indent+1 (a level holds when any matchlet at that level holds); a failed test skips its
               whole deeper subtree.  _xdg_mime_magic_matchlet_compare_to_data (:515-556): for i from
               offset while i < offset+range_length: i + value_length > len fails the matchlet outright;
               else compare the (masked) value at data[i..]; first hit wins.
  data         xdgmime.c xdg_mime_get_mime_type_for_data (:516-541): len 0 -> application/x-zerosize
               (priority 100), before any magic; else the magic answer; none ->
               _xdg_binary_or_text_fallback (xdgmimeint.c:176-190): a byte < 32 other than 9, 10, 13 in
               the first 128 bytes -> the UNKNOWN constant, else the TEXTPLAIN constant (priority 0).
  guess        gcontenttype-fdo.c (round 95's model): a trailing '/' -> inode/directory uncertain;
               exactly one name type -> it, certain (the bytes are not sniffed); otherwise sniff;
               UNKNOWN + looks_like_text -> text/plain; a sniffed application/x-desktop with a name ->
               text/plain; no name type -> the sniffed type, uncertain only when it is still the
               UNKNOWN constant; several -> a sniffed type with priority >= 80 wins, else the first
               name type that is a subclass of it, else the first name type, uncertain.
  subclass     xdgmime.c _xdg_mime_mime_type_subclass text branch (:820-891): unalias both via the text
               aliases files (xdgmimealias.c: fgets 255, first space splits, the last byte of the
               remainder is chopped, qsort by alias, glibc bsearch), equal -> yes; base ends "/*" and
               the media types equal -> yes; base text/plain and mime text/* -> yes; base
               application/octet-stream and mime not inode/* -> yes; else the subclasses-file parents
               (xdgmimeparent.c: per-mime lists in file order, duplicate lines kept apart) recursively,
               the seen-set holding line instances (the C compares strdup'd pointers).  Deeper than
               4096 frames is a declared refusal (the C recursion would overflow its stack).
  mode         xdgmime.c:99-213, 391-436: per directory a loadable mime.cache makes a cache; when ANY
               cache loads only caches answer (refused here, exit 3).  Otherwise every directory's
               globs2 or globs, magic, aliases and subclasses are read as text; none of the five
               anywhere -> mode "none" (empty tables, the fallback answers).

Usage:
  mado-mimetext.py FILE... [--name NAME | --names-from-files] [--data-home D | --data-home-unset]
                    [--data-dirs LIST | --data-dirs-unset] [--home H | --home-unset] [--json]
  mado-mimetext.py --selftest

Without --name the filename passed to GLib is NULL (data only); --name NAME passes NAME for every FILE;
--names-from-files passes each FILE path itself.  Output: the DIRS line
`MADO_MIMETEXT_DIRS: mode=<text|none> dirs=<comma list>` and one line per file
`MADO_MIMETEXT: <type> uncertain=<0|1> name=<escaped|-> file=<escaped>`; --json prints
{"mode", "dirs", "results": [{"file", "name", "type", "uncertain", "sniffed", "prio", "types"}, ...]}.
A refusal prints `MADO_MIMETEXT: UNSUPPORTED <reason>` one line per FILE and exits 3.
ASCII only, stdlib only.  Exit 0 answered, 2 setup error, 3 unsupported input.
"""
from __future__ import annotations

import argparse
import importlib.util
import json
import os
import sys

mg = None


def _load_mimeglob():
    """Round 94's name step, from this file's own directory.  The C1 structural conjunct pins this
    exact shape (one pinned load, the module returned, no module-global binding; --selftest never
    reaches it, so it runs on a lone copy)."""
    spec = importlib.util.spec_from_file_location(
        "mado_mimeglob", os.path.join(os.path.dirname(os.path.abspath(__file__)), "mado-mimeglob.py"))
    if not os.path.exists(spec.origin):
        raise SystemExit(f"mado-mimetext: setup error: {spec.origin} missing (the name step)")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def _own_basename(name: bytes) -> bytes:
    """The lone constructor's basename stand-in (never reached with a name in the selftest)."""
    return name


class Unsupported(Exception):
    """An input this tool refuses: cache mode, or C behaviour past a declared limit."""


class _Const(str):
    """A distinct object for GLib's constant strings: g_content_type_guess compares them by address."""


UNKNOWN = _Const("application/octet-stream")   # xdgmime.c xdg_mime_type_unknown
EMPTY = _Const("application/x-zerosize")       # xdg_mime_type_empty
TEXTPLAIN = _Const("text/plain")               # xdg_mime_type_textplain
MAX_NEST = 4096
INT_MAX = 2 ** 31 - 1
LONG_MAX = 2 ** 63 - 1


def xdgmime_dirs(data_home_env: str | None, home: str | None, data_dirs_env: str | None) -> list[str]:
    """xdgmime.c xdg_init_dirs (:220-300) via round 94's model."""
    return _load_mimeglob().xdgmime_dirs(data_home_env, home, data_dirs_env)


def esc(b: bytes) -> str:
    """The r94 escaping for the printed name and file fields."""
    return _load_mimeglob().esc(b)


def looks_like_text(data: bytes) -> bool:
    """gcontenttype-fdo.c looks_like_text (:533-548): no byte that g_ascii_iscntrl and is not a space
    (GLib's isspace table holds 0x09, 0x0a, 0x0c, 0x0d, 0x20; so none of 0x00-0x07, 0x0b, 0x0e-0x1f,
    0x7f)."""
    return not any(b < 8 or b == 11 or 14 <= b < 32 or b == 127 for b in data)


# ---------------------------------------------------------------- the MIME-Magic parser (xdgmimemagic.c)

class _Cur:
    """A FILE* over the bytes after the 12-byte header: getc/ungetc with the shared position."""

    __slots__ = ("b", "i")

    def __init__(self, b: bytes):
        self.b = b
        self.i = 0

    def getc(self):
        if self.i >= len(self.b):
            return None
        c = self.b[self.i]
        self.i += 1
        return c

    def ungetc(self):
        self.i -= 1


def _read_a_number(cur):
    """_xdg_mime_magic_read_a_number (:168-213): up to 30 digits then strtol; no digits, >INT_MAX or
    ERANGE -> -1.  Returns (value, end_of_file)."""
    digits = bytearray()
    eof = False
    while True:
        c = cur.getc()
        if c is None:
            eof = True
            break
        if not 48 <= c <= 57:
            cur.ungetc()
            break
        digits.append(c)
        if len(digits) == 30:
            break
    if not digits:
        return -1, eof
    v = int(bytes(digits))
    if v > LONG_MAX:          # strtol: ERANGE
        return -1, eof
    if v > INT_MAX:           # the C range check (:210)
        return -1, eof
    return v, eof


def _read_to_newline(cur):
    """_xdg_mime_magic_read_to_newline (:118-149): bytes until '\\n', '\\0' or EOF (consumed).
    Returns (buffer, end_of_file)."""
    out = bytearray()
    while True:
        c = cur.getc()
        if c is None:
            return bytes(out), True
        if c == 10 or c == 0:
            return bytes(out), False
        out.append(c)


def _parse_header(cur, match):
    """_xdg_mime_magic_parse_header (:230-281): a state string; fills match on MAGIC."""
    c = cur.getc()
    if c is None:
        return "EOF"
    if c != 0x5B:                                     # '['
        return "ERROR"
    prio, eof = _read_a_number(cur)
    if eof:
        return "EOF"
    if prio == -1:
        return "ERROR"
    c = cur.getc()
    if c is None:
        return "EOF"
    if c != 0x3A:                                     # ':'
        return "ERROR"
    buf, eof = _read_to_newline(cur)
    if eof:
        return "EOF"
    k = buf.find(b"]")
    if k < 0:
        return "ERROR"
    match["priority"] = prio
    match["mime"] = buf[:k]
    return "MAGIC"


def _parse_error(cur):
    """_xdg_mime_magic_parse_error (:283-300): skip to the next newline -> SECTION; EOF -> EOF."""
    while True:
        c = cur.getc()
        if c is None:
            return "EOF"
        if c == 10:
            return "SECTION"


def _swap_words(b: bytes, word: int) -> bytes:
    """The :476-486 loop: swap each 2- or 4-byte word of the value (and of the mask)."""
    out = bytearray(b)
    for i in range(0, len(out), word):
        if word == 2:
            out[i], out[i + 1] = out[i + 1], out[i]
        else:
            out[i:i + word] = out[i:i + word][::-1]
    return bytes(out)


def _parse_magic_line(cur):
    """_xdg_mime_magic_parse_magic_line (:301-514).  Returns (state, matchlet or None)."""
    c = cur.getc()
    if c is None:
        return "EOF", None
    if c == 0x5B:                                     # '[': the next section starts
        cur.ungetc()
        return "SECTION", None
    if c == 0x0A:                                     # an empty line
        return "MAGIC", None
    indent = 0
    if 48 <= c <= 57:                                 # isdigit
        cur.ungetc()
        indent, eof = _read_a_number(cur)
        if eof:
            return "EOF", None
        if indent == -1:
            return "ERROR", None
        c = cur.getc()
        if c is None:
            return "EOF", None
    if c != 0x3E:                                     # '>'
        return "ERROR", None
    offset, eof = _read_a_number(cur)
    if eof:
        return "EOF", None
    if offset == -1:
        return "ERROR", None
    c = cur.getc()
    if c is None:
        return "EOF", None
    if c != 0x3D:                                     # '='
        return "ERROR", None
    b0 = cur.getc()
    if b0 is None:
        return "EOF", None
    b1 = cur.getc()
    if b1 is None:
        return "EOF", None
    vlen = ((b0 & 0xFF) << 8) | (b1 & 0xFF)           # two bytes big-endian (:372-391)
    value = cur.b[cur.i:cur.i + vlen]
    if len(value) < vlen:                             # short fread -> feof -> EOF (:393-399)
        cur.i = len(cur.b)
        return "EOF", None
    cur.i += vlen
    mask = None
    c = cur.getc()
    if c == 0x26:                                     # '&'
        mask = cur.b[cur.i:cur.i + vlen]
        if len(mask) < vlen:
            cur.i = len(cur.b)
            return "EOF", None
        cur.i += vlen
        c = cur.getc()
    word = 1
    if c == 0x7E:                                     # '~'
        word, eof = _read_a_number(cur)
        if eof:
            return "EOF", None
        if word not in (0, 1, 2, 4):                  # :440-443
            return "ERROR", None
        c = cur.getc()
    rng = 1
    if c == 0x2B:                                     # '+'
        rng, eof = _read_a_number(cur)
        if eof:
            return "EOF", None
        if rng == -1:
            return "ERROR", None
        c = cur.getc()
    if c == 0x0A:                                     # '\n': the matchlet is kept
        if word > 1:
            if vlen % word != 0:                      # :469-474 (never reached for word 0 or 1)
                return "ERROR", None
            value = _swap_words(value, word)
            if mask is not None:
                mask = _swap_words(mask, word)
        return "MAGIC", {"indent": indent, "offset": offset, "value": value,
                         "mask": mask, "range": rng}
    if c is None:
        return "EOF", None
    return "ERROR", None


def _insert_match(matches, match):
    """_xdg_mime_magic_insert_match (:596-629): one global list, priority descending, equal priorities
    keep their file order."""
    p = match["priority"]
    if not matches or p > matches[0]["priority"]:
        matches.insert(0, match)
        return
    at = len(matches)
    for i in range(len(matches) - 1):
        if matches[i + 1]["priority"] < p:
            at = i + 1
            break
    matches.insert(at, match)


def _parse_magic_file(data: bytes) -> list:
    """_xdg_mime_magic_read_from_file (:801-819) + read_magic_file (:685-750): the sections of ONE file
    in lookup order (the caller merges each section into the global list)."""
    if data[:12] != b"MIME-Magic\x00\n":
        return []
    cur = _Cur(data[12:])
    matches = []
    state = "SECTION"
    match = None
    while state != "EOF":
        if state == "SECTION":
            match = {"priority": 0, "mime": None, "matchlets": []}
            state = _parse_header(cur, match)
            # EOF or ERROR: the section is dropped (the C frees it).
        elif state == "MAGIC":
            state, ml = _parse_magic_line(cur)
            if ml is not None:
                match["matchlets"].append(ml)         # file order: the C prepends, then mirrors
            if state == "SECTION" or (state == "EOF" and match["mime"] is not None):
                _insert_match(matches, match)
            # EOF without a mime type, or ERROR: dropped.
        else:                                         # ERROR
            state = _parse_error(cur)
    return matches


def _compare_to_data(ml, data: bytes) -> bool:
    """_xdg_mime_magic_matchlet_compare_to_data (:515-556)."""
    n = len(data)
    vlen = len(ml["value"])
    mask = ml["mask"]
    i = ml["offset"]
    end = ml["offset"] + ml["range"]
    while i < end:
        if i + vlen > n:
            return False
        if mask is None:
            if data[i:i + vlen] == ml["value"]:
                return True
        else:
            ok = True
            for j in range(vlen):
                if (data[i + j] & mask[j]) != (ml["value"][j] & mask[j]):
                    ok = False
                    break
            if ok:
                return True
        i += 1
    return False


def _compare_level(mls, pos, data, indent, depth):
    """_xdg_mime_magic_matchlet_compare_level (:557-588)."""
    if depth > MAX_NEST:
        raise Unsupported(
            "matchlet nesting deeper than 4096 (declared limit; the C recursion overflows deeper)")
    n = len(mls)
    while pos < n and mls[pos]["indent"] == indent:
        if _compare_to_data(mls[pos], data):
            if pos + 1 >= n or mls[pos + 1]["indent"] <= indent:
                return True
            if _compare_level(mls, pos + 1, data, indent + 1, depth + 1):
                return True
        pos += 1
        while pos < n and mls[pos]["indent"] > indent:
            pos += 1
    return False


def magic_lookup_data(matches, data: bytes):
    """_xdg_mime_magic_lookup_data (:652-700) with n_mime_types 0: (mime bytes or None, priority).
    No priority gate: xdgmime.c:535 uses the first match whatever its priority."""
    for mt in matches:
        if mt["matchlets"] and _compare_level(mt["matchlets"], 0, data, 0, 1):
            return mt["mime"], mt["priority"]
    return None, 0


# ---------------------------------------------------------------- aliases and subclasses (text mode)

def _fgets_lines(data: bytes) -> list[bytes]:
    """fgets(line, 255, f) chunks (xdgmimealias.c/xdgmimeparent.c read with a 255-byte buffer): at most
    254 bytes, always ending after '\\n' when one is in reach."""
    out = []
    i = 0
    n = len(data)
    while i < n:
        j = data.find(b"\n", i, i + 254)
        if j >= 0:
            out.append(data[i:j + 1])
            i = j + 1
        else:
            out.append(data[i:i + 254])
            i += 254
    return out


def _split_line(chunk: bytes):
    """The parse both text readers share: '#' comments; the first space (before any NUL) splits; the
    last byte of the remainder is chopped (it is usually the newline).  Returns (left, right) or None."""
    cstr = chunk.split(b"\0", 1)[0]
    if not cstr or cstr[0:1] == b"#":
        return None
    sp = cstr.find(b" ")
    if sp < 0:
        return None
    rest = cstr[sp + 1:]
    return cstr[:sp], rest[:-1] if rest else b""


class _NoNames:
    """A name table with no types (the mode-"none" database): the selftest constructor uses it so a
    lone copy of this file can test without the sibling module."""

    def lookup(self, name: bytes) -> list[str]:
        return []


def _build_tables(dirs: list[str]):
    """The text tables over the given directories (xdgmime.c:391-436): the magic sections (ONE global
    list, priority descending, ties in dir+file order), the aliases array, the subclasses parents (each
    line its own entry: the C compares strdup'd pointers), and whether any of the five text files
    exists anywhere."""
    matches: list = []
    aliases: list = []
    parents: dict = {}
    uid = [0]
    seen_text = False
    for d in dirs:
        for n in ("/globs2", "/globs", "/magic", "/aliases", "/subclasses"):
            if os.path.exists(d + n):
                seen_text = True
        mp = d + "/magic"
        if os.path.exists(mp):
            try:
                with open(mp, "rb") as fh:
                    blob = fh.read()
            except OSError:
                blob = b""
            for mt in _parse_magic_file(blob):
                _insert_match(matches, mt)
        ap = d + "/aliases"
        if os.path.exists(ap):
            try:
                with open(ap, "rb") as fh:
                    blob = fh.read()
            except OSError:
                blob = b""
            for chunk in _fgets_lines(blob):
                pair = _split_line(chunk)
                if pair is not None:
                    aliases.append(pair)
        pp = d + "/subclasses"
        if os.path.exists(pp):
            try:
                with open(pp, "rb") as fh:
                    blob = fh.read()
            except OSError:
                blob = b""
            for chunk in _fgets_lines(blob):
                pair = _split_line(chunk)
                if pair is not None:
                    mime, parent = pair
                    uid[0] += 1
                    parents.setdefault(mime, []).append((uid[0], parent))
    aliases.sort(key=lambda x: x[0])                  # the C qsorts by alias; glibc stability is not
    return matches, aliases, parents, seen_text       # guaranteed for equal keys (see the report)


def _media_equal(a: bytes, b: bytes) -> bool:
    """xdg_mime_media_type_equal (:779-788): compare up to and including the first '/' of a."""
    k = a.find(b"/")
    return k >= 0 and a[:k + 1] == b[:k + 1]


# ---------------------------------------------------------------- the sniffer

class Sniffer:
    """g_content_type_guess for the text database mode.  `lone=True` is the selftest constructor: no
    sibling import (an empty name table).  The default builds round 94's name step and refuses a
    reachable loadable cache; `resolver` lets a caller inject a stand-in (the selftest's fake)."""

    def __init__(self, dirs: list[str], resolver=None, lone: bool = False):
        self.dirs = list(dirs)
        if lone:
            self.names = _NoNames()
            self.basename = _own_basename
        else:
            if resolver is None:
                resolver = _load_mimeglob().Resolver(dirs)
            self.mode = resolver.mode
            if self.mode == "cache":
                raise Unsupported("cache-mode")
            self.names = resolver.db
            self.basename = _load_mimeglob().g_path_get_basename
        self.matches, self.aliases, self.parents, seen_text = _build_tables(dirs)
        if lone:
            self.mode = "text" if seen_text else "none"
        elif not seen_text:
            self.mode = "none"

    # -- aliases / subclass (xdgmime.c text branch)

    def _unalias(self, mime: bytes) -> bytes:
        """_xdg_mime_alias_list_lookup via glibc bsearch ((l+u)/2, xdgmimealias.c:47-63): one level."""
        a = self.aliases
        lo, up = 0, len(a)
        while lo < up:
            mid = (lo + up) // 2
            ka = a[mid][0]
            if mime < ka:
                up = mid
            elif mime > ka:
                lo = mid + 1
            else:
                return a[mid][1]
        return mime

    def _direct(self, mime: bytes, ubase: bytes):
        """The checks a subclass frame makes before the parent lists (:836-862).  (hit, umime)."""
        umime = self._unalias(mime)
        if umime == ubase:
            return True, umime
        if ubase.endswith(b"/*") and _media_equal(umime, ubase):
            return True, umime
        if ubase == b"text/plain" and umime.startswith(b"text/"):
            return True, umime
        if ubase == b"application/octet-stream" and not umime.startswith(b"inode/"):
            return True, umime
        return False, umime

    def subclass(self, mime: bytes, base: bytes) -> bool:
        """_xdg_mime_mime_type_subclass (:820-891), text branch, iterative; the seen-set holds line
        instances (the C's strdup'd parent pointers), one recursion frame per parent level."""
        ubase = self._unalias(base)
        hit, umime = self._direct(mime, ubase)
        if hit:
            return True
        seen: set[int] = set()
        stack = [iter(self.parents.get(umime, ()))]
        while stack:
            if len(stack) > MAX_NEST:
                raise Unsupported(
                    "parent chain deeper than 4096 (declared limit; the C recursion overflows deeper)")
            it = stack[-1]
            nxt = next(it, None)
            if nxt is None:
                stack.pop()
                continue
            if nxt[0] in seen:
                continue
            seen.add(nxt[0])
            hit, um2 = self._direct(nxt[1], ubase)
            if hit:
                return True
            stack.append(iter(self.parents.get(um2, ())))
        return False

    # -- the data step

    def mime_type_for_data(self, data: bytes):
        """xdg_mime_get_mime_type_for_data (:516-541), text branch: (type, priority)."""
        if len(data) == 0:
            return EMPTY, 100
        t, prio = magic_lookup_data(self.matches, data)
        if t is not None:
            return t.decode("utf-8", "surrogateescape"), prio
        for b in data[:128]:
            if b < 32 and b not in (9, 10, 13):
                return UNKNOWN, 0
        return TEXTPLAIN, 0

    # -- g_content_type_guess (gcontenttype-fdo.c, round 95's model)

    def guess(self, name: bytes | None, data: bytes) -> dict:
        types: list[str] = []
        if name is not None:
            if name.endswith(b"/"):
                return {"type": "inode/directory", "uncertain": 1, "types": ["inode/directory"],
                        "sniffed": None, "prio": 0}
            base = self.basename(name)
            types = self.names.lookup(base)
            if len(types) == 1:
                return {"type": types[0], "uncertain": 0, "types": types, "sniffed": None, "prio": 0}
        sniffed, prio = self.mime_type_for_data(data)
        if sniffed is UNKNOWN and looks_like_text(data):
            sniffed = "text/plain"
        if name is not None and sniffed == "application/x-desktop":
            sniffed = "text/plain"
        out = {"types": types, "sniffed": str(sniffed), "prio": prio}
        if not types:
            return dict(out, type=str(sniffed), uncertain=1 if sniffed is UNKNOWN else 0)
        if sniffed is not UNKNOWN:
            if prio >= 80:
                return dict(out, type=str(sniffed), uncertain=0)
            sb = str(sniffed).encode("utf-8", "surrogateescape")
            for t in types:
                if self.subclass(t.encode("utf-8", "surrogateescape"), sb):
                    return dict(out, type=t, uncertain=0)
        return dict(out, type=types[0], uncertain=1)


# ---------------------------------------------------------------- selftest

def selftest() -> int:
    """Every modelled rule, on a lone copy (no sibling import): the check label names the rule and its
    anchor in the C."""
    import tempfile
    checks: list[tuple[str, bool]] = []

    # The audit launcher only allows fixtures under the work tree: keep them beside the cwd, never /tmp.
    with tempfile.TemporaryDirectory(dir=os.getcwd()) as root:
        def w(rel: str, data: bytes) -> None:
            p = os.path.join(root, rel)
            os.makedirs(os.path.dirname(p), exist_ok=True)
            with open(p, "wb") as fh:
                fh.write(data)

        def magic(rel: str, body: bytes) -> None:
            w(rel, b"MIME-Magic\x00\n" + body)

        def snif(dirs):
            return Sniffer([os.path.join(root, d) for d in dirs], lone=True)

        def sn(dirs, data):
            """(type, prio) of the data step alone."""
            t, p = snif(dirs).mime_type_for_data(data)
            return str(t), p

        def gu(dirs, name, data):
            r = snif(dirs).guess(name, data)
            return r["type"], r["uncertain"]

        # --- the 12-byte header gate (xdgmimemagic.c:801-819)
        magic("a/mime/magic", b"[50:t/a]\n>0=\x00\x01A\n")
        w("h11/mime/magic", b"MIME-Magic\x00" + b"[50:t/a]\n>0=\x00\x01A\n")     # 11-byte header + body
        w("h12/mime/magic", b"MIME-Magic\x00X" + b"[50:t/a]\n>0=\x00\x01A\n")    # 12th byte wrong
        checks += [
            ("m01 a short header contributes no magic (:806 fread 12)",
             sn(["h11/mime"], b"A") == ("text/plain", 0)),
            ("m02 a wrong 12th byte contributes no magic (:808 memcmp)",
             sn(["h12/mime"], b"A") == ("text/plain", 0)),
            ("m03 a good header parses its section (:230-281)",
             sn(["a/mime"], b"AB") == ("t/a", 50)),
        ]

        # --- section headers (:230-281)
        magic("s1/mime/magic", b"[t/a]\n>0=A\n")                          # no priority digits
        magic("s2/mime/magic", b"[50 t/a]\n>0=A\n")                       # no ':'
        magic("s3/mime/magic", b"[50:t/a\n>0=A\n")                        # no ']' on the line
        magic("s4/mime/magic", b"[50:t/a]extra]\n>0=\x00\x01A\n")         # type ends at the first ']'
        magic("s5/mime/magic", b"[50:t/a]")                               # EOF after ']', no newline
        checks += [
            ("m04 a header without a priority is a parse error (:243-246)",
             sn(["s1/mime"], b"A") == ("text/plain", 0)),
            ("m05 a header without ':' is a parse error (:253-256)",
             sn(["s2/mime"], b"A") == ("text/plain", 0)),
            ("m06 a header without ']' is a parse error (:258-276)",
             sn(["s3/mime"], b"A") == ("text/plain", 0)),
            ("m07 the type ends at the first ']' (:258-276)",
             sn(["s4/mime"], b"A") == ("t/a", 50)),
            ("m08 EOF right after ']' drops the section (:267-272)",
             sn(["s5/mime"], b"A") == ("text/plain", 0)),
        ]

        # --- value length (:372-391) and the compare bounds (:515-536)
        magic("v1/mime/magic", b"[50:t/v]\n>0=\x00\x03ABC\n")             # BE length 3
        magic("v2/mime/magic", b"[50:t/z]\n>0=\x00\x00\n")                # zero-length value
        magic("v3/mime/magic", b"[50:t/b]\n>0=\x00\x02AB+5\n")            # range 5, len-2 value
        checks += [
            ("m09 a two-byte big-endian value length (:372-391)",
             sn(["v1/mime"], b"ABCX") == ("t/v", 50)),
            ("m10 a zero-length value matches any data at its offset (:537-556)",
             sn(["v2/mime"], b"ZZ") == ("t/z", 50)),
            ("m11 the bounds rule fails the matchlet outright (:530-536)",
             (sn(["v3/mime"], b"AB"), sn(["v3/mime"], b"XB"))
             == (("t/b", 50), ("text/plain", 0))),
        ]

        # --- masks (:400-419)
        magic("k1/mime/magic", b"[50:t/k]\n>0=\x00\x02\x10\x00\n")        # no mask: literal bytes
        magic("k2/mime/magic", b"[50:t/k]\n>0=\x00\x02\x10\x00&\xf0\x00\n")  # mask f0/00
        checks += [
            ("m12 without a mask the value compares literally (:539-549)",
             (sn(["k1/mime"], b"\x10\x00"), sn(["k1/mime"], b"AZ"))
             == (("t/k", 50), ("text/plain", 0))),
            ("m13 a masked compare ANDs value and data with the mask (:526-537)",
             (sn(["k2/mime"], b"\x1f\x99"), sn(["k2/mime"], b"\x2f\x99"))
             == (("t/k", 50), ("text/plain", 0))),
        ]

        # --- word sizes (:421-505)
        magic("w1/mime/magic", b"[50:t/w]\n>0=\x00\x02\x12\x34~2\n")      # 2-byte words swap
        magic("w2/mime/magic", b"[50:t/w]\n>0=\x00\x04\x01\x02\x03\x04~4\n")
        magic("w3/mime/magic", b"[50:t/w]\n>0=\x00\x02\x12\x34&\xf0\x00~2\n")
        magic("w4/mime/magic", b"[50:t/w]\n>0=\x00\x03ABC~2\n")           # 3 % 2 != 0
        magic("w5/mime/magic", b"[50:t/w]\n>0=\x00\x01A~3\n")             # word size 3
        magic("w6/mime/magic", b"[50:t/w]\n>0=\x00\x02\x12\x34~0\n")      # word size 0
        checks += [
            ("m14 word size 2 swaps the value at parse time (:476-505)",
             (sn(["w1/mime"], b"\x34\x12"), sn(["w1/mime"], b"AB"))
             == (("t/w", 50), ("text/plain", 0))),
            ("m15 word size 4 reverses each 4-byte word (:476-505)",
             sn(["w2/mime"], b"\x04\x03\x02\x01") == ("t/w", 50)),
            ("m16 the mask byte-swaps with the value (:494-504)",
             sn(["w3/mime"], b"\xff\x1f") == ("t/w", 50)),
            ("m17 value_length % word_size != 0 is a parse error (:469-474)",
             sn(["w4/mime"], b"ABC") == ("text/plain", 0)),
            ("m18 a word size other than 0,1,2,4 is a parse error (:440-443)",
             sn(["w5/mime"], b"A") == ("text/plain", 0)),
            ("m19 word size 0 parses and swaps nothing (:440-443 allows 0; :469 never runs)",
             sn(["w6/mime"], b"\x12\x34") == ("t/w", 50)),
        ]

        # --- ranges (:452-470, :515-556)
        magic("r1/mime/magic", b"[50:t/r]\n>1=\x00\x01A+3\n")
        magic("r2/mime/magic", b"[50:t/r]\n>1=\x00\x01A\n")               # default range 1
        magic("r3/mime/magic", b"[50:t/r]\n>0=\x00\x01A+0\n")             # range 0 never tests
        checks += [
            ("m20 the range scans offset..offset+range-1 (:517-519)",
             (sn(["r1/mime"], b"xAAX"), sn(["r1/mime"], b"xBBBX"))
             == (("t/r", 50), ("text/plain", 0))),
            ("m21 without '+' the range is 1 (:84-105 defaults)",
             (sn(["r2/mime"], b"xA"), sn(["r2/mime"], b"Ax"))
             == (("t/r", 50), ("text/plain", 0))),
            ("m22 a range of 0 never matches (:517-519)",
             sn(["r3/mime"], b"A") == ("text/plain", 0)),
        ]

        # --- the matchlet tree (:557-588)
        magic("n1/mime/magic", b"[50:t/n]\n>0=\x00\x02NE\n1>4=\x00\x01X\n1>4=\x00\x01Y\n")
        magic("n2/mime/magic", b"[50:t/n]\n>0=\x00\x01A\n2>4=\x00\x01B\n")  # child at indent 2
        magic("n3/mime/magic", b"[50:t/n]\n>0=\x00\x01A\n1>2=\x00\x01B\n>0=\x00\x01C\n")
        checks += [
            ("m23 a level holds when any child at indent+1 holds (:557-588)",
             (sn(["n1/mime"], b"NE..Y"), sn(["n1/mime"], b"NE..Z"))
             == (("t/n", 50), ("text/plain", 0))),
            ("m24 a child must sit at exactly indent+1 (:566-573)",
             sn(["n2/mime"], b"A..B") == ("text/plain", 0)),
            ("m25 a failed parent skips its whole subtree (:584-587)",
             (sn(["n3/mime"], b"C"), sn(["n3/mime"], b"A..B"))
             == (("t/n", 50), ("text/plain", 0))),
        ]

        # --- order (:596-629, :652-700)
        magic("o1/mime/magic", b"[50:t/lo]\n>0=\x00\x01M\n[90:t/hi]\n>0=\x00\x01M\n")
        magic("o2/mime/magic", b"[50:t/one]\n>0=\x00\x01E\n[50:t/two]\n>0=\x00\x01E\n")
        magic("o3/mime/magic", b"[0:t/zero]\n>0=\x00\x01Z\n")
        magic("o4/mime/magic", b"[50:t/nom]\n>0=\x00\x0b__NOMAGIC__\n")
        checks += [
            ("m26 the higher priority wins regardless of file order (:596-629)",
             sn(["o1/mime"], b"M") == ("t/hi", 90)),
            ("m27 equal priorities keep file order (:596-629)",
             sn(["o2/mime"], b"E") == ("t/one", 50)),
            ("m28 text mode has no priority>0 gate (xdgmime.c:535)",
             sn(["o3/mime"], b"Z") == ("t/zero", 0)),
            ("m29 __NOMAGIC__ is a literal value, not deleteall (:301-514)",
             (sn(["o4/mime"], b"__NOMAGIC__y"), sn(["o4/mime"], b"plain\n"))
             == (("t/nom", 50), ("text/plain", 0))),
        ]

        # --- dropped sections and recovery (:283-300, :749-782)
        magic("d1/mime/magic",
              b"[50:t/good]\n>0=\x00\x01G\n[60:t/bad]\n>0=\x00\x01G X\n[40:t/after]\n>0=\x00\x01A\n")
        magic("d2/mime/magic", b"[50:t/g1]\n>0=\x00\x01P\n[70:t/g2]\n>0=\x00\x01Q\n>0=\x00\x01Q X\nX")
        checks += [
            ("m30 a bad matchlet line drops its whole section, the file continues (:283-300, :749-782)",
             (sn(["d1/mime"], b"G"), sn(["d1/mime"], b"A"), sn(["d1/mime"], b"Z"))
             == (("t/good", 50), ("t/after", 40), ("text/plain", 0))),
            ("m31 lines after the bad line are not rescanned into the section (:283-300)",
             (sn(["d2/mime"], b"P"), sn(["d2/mime"], b"Q"))
             == (("t/g1", 50), ("text/plain", 0))),
        ]

        # --- EOF variants (:735-747)
        magic("e1/mime/magic", b"[50:t/e]\n>0=\x00\x01A")                 # no trailing newline
        checks += [
            ("m32 EOF ends the line: the trailing matchlet is freed, the section stays (:498-514, :735-747)",
             sn(["e1/mime"], b"A") == ("text/plain", 0)),
        ]

        # --- zerosize and the fallback (xdgmime.c:516-541, xdgmimeint.c:176-190)
        checks += [
            ("m33 empty data is zerosize before any magic (xdgmime.c:519-524)",
             (sn(["v2/mime"], b""), sn(["a/mime"], b""))
             == (("application/x-zerosize", 100), ("application/x-zerosize", 100))),
            ("m34 the text fallback (xdgmimeint.c:176-190)",
             (sn(["a/mime"], b"plain words\n"), sn(["a/mime"], b"\x01\x02"))
             == (("text/plain", 0), ("application/octet-stream", 0))),
            ("m35 the fallback reads the first 128 bytes only (:176-190)",
             (sn(["a/mime"], b"a" * 128 + b"\x01"), sn(["a/mime"], b"a" * 127 + b"\x01"))
             == (("text/plain", 0), ("application/octet-stream", 0))),
            ("m36 VT is a control byte for the fallback, FF only survives via looks_like_text (:176-190, gcontenttype-fdo.c:533-548)",
             (gu(["a/mime"], None, b"ab\x0bcd"), gu(["a/mime"], None, b"ab\x0ccd"))
             == (("application/octet-stream", 1), ("text/plain", 0))),
        ]

        # --- multi-directory order (xdgmime.c:99-213)
        magic("mA/mime/magic", b"[50:t/lo]\n>0=\x00\x01L\n")
        magic("mB/mime/magic", b"[90:t/hi]\n>0=\x00\x01L\n")
        magic("mC/mime/magic", b"[50:t/fa]\n>0=\x00\x01E\n")
        magic("mD/mime/magic", b"[50:t/fb]\n>0=\x00\x01E\n")
        checks += [
            ("m37 one global list over the directories, priority first (:596-629)",
             sn(["mA/mime", "mB/mime"], b"L") == ("t/hi", 90)),
            ("m38 equal priorities keep directory order (:596-629)",
             sn(["mC/mime", "mD/mime"], b"E") == ("t/fa", 50)),
        ]

        # --- the mode rule (xdgmime.c:129-206, 391-436) and the cache refusal
        os.makedirs(os.path.join(root, "none/mime"), exist_ok=True)
        w("tonly/mime/magic", b"MIME-Magic\x00\n[50:t/a]\n>0=\x00\x01A\n")
        w("cached/mime/mime.cache", b"\x00\x01\x00\x02" + b"\x00" * 36)   # a loadable v1.2 cache
        checks += [
            ("m39 no text file anywhere is mode none (xdgmime.c:391-436)",
             (snif(["none/mime"]).mode, sn(["none/mime"], b"hi\n"), sn(["none/mime"], b"\x01"))
             == ("none", ("text/plain", 0), ("application/octet-stream", 0))),
            ("m40 a magic file alone is text mode (:417-426)",
             snif(["tonly/mime"]).mode == "text"),
            ("m41 a loadable mime.cache anywhere is refused (xdgmime.c:129-206)",
             _selftest_cache_refusal(os.path.join(root, "cached/mime"))),
        ]

        # --- aliases and subclasses (S505: xdgmimealias.c, xdgmimeparent.c, xdgmime.c:820-891)
        w("al/mime/aliases", b"text/x-old text/x-new\nplain-txt text/plain\n")
        w("al2/mime/aliases", b"t/one t/two")                             # no trailing newline
        w("sub/mime/subclasses", b"app/child app/mid\napp/mid app/base\n")
        checks += [
            ("m42 the aliases file unaliases one level (xdgmimealias.c:88-119)",
             (snif(["al/mime"])._unalias(b"text/x-old"), snif(["al/mime"])._unalias(b"text/x-new"))
             == (b"text/x-new", b"text/x-new")),
            ("m43 the last byte of a line without newline is chopped (:107-110)",
             snif(["al2/mime"])._unalias(b"t/one") == b"t/tw"),
            ("m44 text/plain subsumes text/* (xdgmime.c:851-853)",
             (snif(["al/mime"]).subclass(b"text/x-new", b"text/plain"),
              snif(["al/mime"]).subclass(b"inode/x", b"application/octet-stream")) == (True, False)),
            ("m45 the subclasses file chains parents (xdgmimeparent.c:104-167)",
             snif(["sub/mime"]).subclass(b"app/child", b"app/base") is True),
            ("m46 an alias resolves inside the subclass walk (:833-834)",
             snif(["al/mime", "sub/mime"]).subclass(b"plain-txt", b"text/plain") is True),
        ]

        # --- the guess combination over the magic answer (gcontenttype-fdo.c, round 95's model)
        magic("g1/mime/magic", b"[80:t/hi]\n>0=\x00\x01H\n[30:t/lo]\n>0=\x00\x01L\n")
        checks += [
            ("m47 no name type: the magic answer is certain (:641-648)",
             gu(["g1/mime"], None, b"H") == ("t/hi", 0)),
            ("m48 data-only with no magic match is the UNKNOWN constant, uncertain (:641-648)",
             gu(["g1/mime"], None, b"\x01\x02") == ("application/octet-stream", 1)),
            ("m49 unknown + looks_like_text answers text/plain, certain (:622-639)",
             gu(["g1/mime"], None, b"words\n") == ("text/plain", 0)),
            ("m50 a trailing slash answers inode/directory uncertain (:567-613)",
             gu(["g1/mime"], b"d/", b"H") == ("inode/directory", 1)),
        ]

    failed = [n for n, ok in checks if not ok]
    for n in failed:
        print(f"MADO_MIMETEXT_SELFTEST_FAIL: {n}")
    print(f"MADO_MIMETEXT_SELFTEST: checks={len(checks)} failed={len(failed)}")
    return 1 if failed else 0


def _selftest_cache_refusal(dir_path: str) -> bool:
    """Sniffer must refuse a directory whose resolver reports cache mode (xdgmime.c:129-206); the fake
    resolver stands in for round 94's Resolver so no sibling is needed."""
    class _FakeResolver:
        def __init__(self):
            self.mode = "cache"
            self.db = None

    try:
        Sniffer([dir_path], resolver=_FakeResolver())
        return False
    except Unsupported as e:
        return str(e) == "cache-mode"


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
    if a.selftest:
        return selftest()
    if not a.files or (a.name is not None and a.names_from_files):
        print("mado-mimetext: setup error: name at least one FILE; --name and --names-from-files exclude",
              file=sys.stderr)
        return 2
    mimeglob_mod = _load_mimeglob()
    mimeglob_mod._libc.setlocale(mimeglob_mod._LC_ALL, b"C")
    env = os.environ
    home = None if a.home_unset else (a.home if a.home is not None else env.get("HOME"))
    dh = None if a.data_home_unset else (a.data_home if a.data_home is not None else env.get("XDG_DATA_HOME"))
    dd = None if a.data_dirs_unset else (a.data_dirs if a.data_dirs is not None else env.get("XDG_DATA_DIRS"))
    out = []
    try:
        dirs = mimeglob_mod.xdgmime_dirs(dh, home, dd)
        s = Sniffer(dirs, resolver=mimeglob_mod.Resolver(dirs))
        esc_fn = mimeglob_mod.esc
        for f in a.files:
            fb = os.fsencode(f)
            try:
                with open(f, "rb") as fh:
                    data = fh.read()
            except OSError as e:
                print(f"mado-mimetext: setup error: {f}: {e.strerror}", file=sys.stderr)
                return 2
            name = fb if a.names_from_files else (os.fsencode(a.name) if a.name is not None else None)
            r = s.guess(name, data)
            out.append(dict(r, file=esc_fn(fb), name=None if name is None else esc_fn(name)))
    except Unsupported as e:
        for _f in a.files:
            print(f"MADO_MIMETEXT: UNSUPPORTED {e}")
        return 3
    if a.json:
        print(json.dumps({"mode": s.mode, "dirs": s.dirs, "results": out}, sort_keys=True))
    else:
        print(f"MADO_MIMETEXT_DIRS: mode={s.mode} dirs={','.join(s.dirs)}")
        for x in out:
            print(f"MADO_MIMETEXT: {x['type']} uncertain={x['uncertain']} name={x['name'] or '-'} file={x['file']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
