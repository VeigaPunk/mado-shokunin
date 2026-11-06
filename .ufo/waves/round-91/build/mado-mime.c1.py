#!/usr/bin/env python3
"""mado-mime — which application GLib opens a MIME type with.

Read-only resolver for the default-application plane: given XDG_CURRENT_DESKTOP,
the XDG config/data roots and PATH, print what GLib 2.90.1 answers for a MIME
type — the default application (`g_app_info_get_default_for_type`, as `gio mime
TYPE` prints it), the registered applications (`g_app_info_get_all_for_type`)
and the recommended applications (`g_app_info_get_recommended_for_type`).

Upstream model (GLib tag 2.90.1; line numbers are that tag's files):
  dirs       gio/gdesktopappinfo.c desktop_file_dirs_lock (:1624-1677): the user
             config dir, each XDG_CONFIG_DIRS entry (config dirs: no desktop
             files, :1415-1424), the user data dir + /applications, each
             XDG_DATA_DIRS entry + /applications, in that precedence order.
  desktops   XDG_CURRENT_DESKTOP split on ':'; a token that is empty or holds a
             byte other than [A-Za-z0-9_-] is dropped; lowercased (:328-377).
  apps       per data dir every `*.desktop` below it; a subdirectory adds
             `<sub>-` to the id (get_apps_from_dir :769-818).
  lists      per dir, in this order (:993-1043): `<desktop>-mimeapps.list` for
             each desktop (only [Default Applications] honoured), mimeapps.list
             ([Added Associations], [Removed Associations], [Default
             Applications]); data dirs only: defaults.list (only [Default
             Applications]) and mimeinfo.cache ([MIME Cache] as additions,
             [Removed Associations]).  Each key is unaliased; additions skip ids
             already removed in this dir and removals skip ids already added
             (expand_strv :855-898, read_mimeapps_list :901-990).  A file
             GKeyFile cannot load is skipped; a value that is not a valid
             string list skips that key.
  default    g_app_info_get_default_for_type_impl (:4722-4782): for the type and
             then each ancestor (unaliased type, then its parents breadth-first,
             get_list_of_mimetypes :4552-4588), collect every dir's defaults,
             then every dir's additions not masked by a higher-precedence data
             dir holding the same id, not blocklisted (removals, which persist
             across ancestors); the first collected id that some dir (in order)
             can load wins — a Hidden=true file is accepted here.
  lists out  registered = additions over the type and its ancestors,
             recommended = additions over the unaliased type only (:4590-4705);
             each id loaded by g_desktop_app_info_new (:2186-2216): first dir
             that loads it, then dropped if Hidden=true.
  load       g_desktop_app_info_load_from_keyfile (:1894-2097): first group
             [Desktop Entry], Type=Application, Path/TryExec/Exec readable as
             strings, a non-empty TryExec found as a program, a non-empty Exec
             parsed by g_shell_parse_argv (glib/gshell.c tokenize_command_line +
             g_shell_unquote, ported) with its argv[0] found by
             g_find_program_for_path (glib/gutils.c: Path= as working dir, a name
             with '/' tested directly then the PATH search unless absolute; any
             file type with X_OK that is not a directory); Hidden is true only
             for `true`/`1` before trailing g_ascii_isspace bytes.
  mime db    gio/gcontenttype-fdo.c (:69-111, :116-138) + gio/xdgmime: mime dirs
             are the user data dir and each XDG_DATA_DIRS entry + /mime; a dir
             whose mime.cache (version 1.1-1.2) loads is a cache dir and its
             text files are not read; when any cache dir exists aliases and
             parents come from the caches only (xdgmime.c :129-154, :735-746,
             :902-925; xdgmimecache.c :315-360, :1051-1130), else from every
             dir's `aliases`/`subclasses` text files read with fgets(255)
             semantics (xdgmimealias.c :104-149, xdgmimeparent.c :110-185).
GKeyFile reading follows GLib 2.90.1 glib/gkeyfile.c as tools/mado-portals.py
models it (C locale: locale-suffixed keys dropped), with g_ascii_isspace (space,
\\t, \\n, \\f, \\r; not \\v) as the whitespace set.

Output: per type one line `MADO_MIME: <type> default=<id>|none
registered=<id,…>|- recommended=<id,…>|-` and a header `MADO_MIME_DIRS:
desktops=… config=… data=…`; `--json` prints one JSON object.  `gio mime` prints
the two lists only when a default exists; this tool always computes them.

Read-only: opens only mimeapps.list, <desktop>-mimeapps.list, defaults.list,
mimeinfo.cache, *.desktop, and mime/{mime.cache,aliases,subclasses} under the
given roots, and stats PATH entries.  Exit 0 resolved, 2 setup error.
`--selftest` runs built-in checks on temporary fixtures.
"""
from __future__ import annotations

import argparse
import ctypes
import ctypes.util
import json
import os
import struct
import sys
import tempfile

ADDED = "Added Associations"
REMOVED = "Removed Associations"
DEFAULTS = "Default Applications"
CACHE = "MIME Cache"
DESKTOP_GROUP = "Desktop Entry"
ASCII_SPACE = " \t\n\f\r"  # g_ascii_isspace (glib/gstrfuncs.c ascii_table_data): \v is not a space


class KeyFileError(Exception):
    pass


# ---------------------------------------------------------------- GKeyFile (as tools/mado-portals.py)
def _is_group_line(s: str) -> bool:
    if not s.startswith("["):
        return False
    j = s.find("]", 1)
    if j < 0:
        return False
    return s[j + 1:].strip(" \t") == ""


def _valid_key_name(key: str) -> bool:
    q = 0
    while q < len(key) and key[q] not in "=[]":
        q += 1
    if q == 0:
        return False
    if key[0] == " " or key[q - 1] == " ":
        return False
    if q < len(key) and key[q] == "[":
        q += 1
        while q < len(key) and (key[q].isalnum() or key[q] in "-_.@"):
            q += 1
        if q >= len(key) or key[q] != "]":
            return False
        q += 1
    return q >= len(key)


def _valid_group_name(name: str) -> bool:
    if name == "":
        return False
    return not any(c in "[]" or ord(c) < 0x20 or ord(c) == 0x7f for c in name)


def parse_keyfile(text: str) -> tuple[dict[str, dict[str, str]], str | None]:
    """Return ({group: {key: raw value}}, start group); raise KeyFileError like g_key_file_load_from_file."""
    groups: dict[str, dict[str, str]] = {}
    current: str | None = None
    first_group: str | None = None
    lines = text.split("\n")
    for idx, raw in enumerate(lines):
        if idx < len(lines) - 1 and raw.endswith("\r"):
            raw = raw[:-1]
        i = 0
        while i < len(raw) and raw[i] in ASCII_SPACE:
            i += 1
        s = raw[i:]
        if s == "" or s.startswith("#"):
            continue
        if _is_group_line(s):
            name = s[1:s.find("]", 1)]
            if not _valid_group_name(name):
                raise KeyFileError(f"invalid group name {name!r}")
            current = name
            if first_group is None:
                first_group = name
            groups.setdefault(name, {})
            continue
        eq = s.find("=")
        if eq <= 0:
            raise KeyFileError(f"line {s!r} is not a key-value pair, group, or comment")
        if current is None:
            raise KeyFileError("key file does not start with a group")
        key = s[:eq].rstrip(ASCII_SPACE)
        if not _valid_key_name(key):
            raise KeyFileError(f"invalid key name {key!r}")
        value = s[eq + 1:].lstrip(ASCII_SPACE)
        if current == first_group and key == "Encoding" and \
                value.encode("utf-8", "surrogateescape").lower() != b"utf-8":
            raise KeyFileError(f"unknown encoding {value!r}")
        loc = key[key.rindex("["):] if "[" in key else ""
        if len(loc) > 2 and loc[1:-1].lower() != "c":
            # key_get_locale: the text from the last '[' is a locale only when longer than "[]"; such a key
            # is kept only for an "interesting" locale — under LC_ALL=C g_get_language_names() is ["C"]
            # (g_key_file_locale_is_interesting, ASCII-case-insensitive); "x[]" is a plain key
            continue
        grp = groups[current]
        # GKeyFile keeps every pair in file order and looks a key up to its last value
        # (g_key_file_add_key_value_pair): g_key_file_get_keys visits a repeated key first at its
        # first position, so the key keeps its first position and takes the last value
        grp[key] = value
    return groups, first_group


def _check_utf8(value: str) -> None:
    """g_key_file_get_string(_list): a value that is not valid UTF-8 is an error for that key only."""
    if any("\udc80" <= c <= "\udcff" for c in value):
        raise KeyFileError("value is not UTF-8")


def string_list(value: str) -> list[str]:
    _check_utf8(value)
    pieces: list[str] = []
    cur: list[str] = []
    i = 0
    while i < len(value):
        c = value[i]
        if c == "\\":
            i += 1
            if i >= len(value):
                raise KeyFileError("escape character at end of line")
            m = {"s": " ", "n": "\n", "t": "\t", "r": "\r", "\\": "\\", ";": ";"}
            if value[i] not in m:
                raise KeyFileError(f"invalid escape sequence \\{value[i]}")
            cur.append(m[value[i]])
        elif c == ";":
            pieces.append("".join(cur))
            cur = []
        else:
            cur.append(c)
        i += 1
    if cur:
        pieces.append("".join(cur))
    return pieces


def plain_string(value: str) -> str:
    _check_utf8(value)
    out: list[str] = []
    i = 0
    m = {"s": " ", "n": "\n", "t": "\t", "r": "\r", "\\": "\\"}
    while i < len(value):
        c = value[i]
        if c == "\\":
            i += 1
            if i >= len(value):
                raise KeyFileError("escape character at end of line")
            if value[i] not in m:
                raise KeyFileError(f"invalid escape sequence \\{value[i]}")
            out.append(m[value[i]])
        else:
            out.append(c)
        i += 1
    return "".join(out)


def load_keyfile(path: str) -> tuple[dict[str, dict[str, str]], str | None] | None:
    try:
        with open(path, "rb") as fh:
            data = fh.read()
    except OSError:
        return None
    try:
        # GKeyFile parses bytes: invalid UTF-8 voids nothing at load time (comments, unread keys);
        # it fails only the key whose value is read (_check_utf8)
        return parse_keyfile(data.decode("utf-8", "surrogateescape"))
    except KeyFileError:
        return None


# ---------------------------------------------------------------- shared-mime-info (xdgmime)
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


def _pairs_from_text(path: str) -> list[tuple[str, str]]:
    try:
        with open(path, "rb") as fh:
            data = fh.read()
    except OSError:
        return []
    pairs = []
    for line in _fgets_lines(data):
        line = line.split(b"\0", 1)[0]  # C string semantics
        if line[:1] == b"#":
            continue
        sp = line.find(b" ")
        if sp < 0:
            continue
        a, b = line[:sp], line[sp + 1:]
        b = b[:-1] if b else b  # xdgmime chops the last byte (meant to be the newline)
        pairs.append((a.decode("utf-8", "surrogateescape"), b.decode("utf-8", "surrogateescape")))
    return pairs


class MimeCache:
    def __init__(self, buf: bytes):
        self.buf = buf

    def _u32(self, off: int) -> int:
        return struct.unpack_from(">I", self.buf, off)[0]

    def _str(self, off: int) -> str:
        end = self.buf.find(b"\0", off)
        return self.buf[off:end if end >= 0 else len(self.buf)].decode("utf-8", "surrogateescape")

    def _in(self, off: int, n: int, size: int) -> bool:
        return off + n * size <= len(self.buf)

    def alias(self, name: str) -> str | None:
        try:
            return self._alias(name)
        except (struct.error, IndexError):
            return None  # out-of-bounds offsets: xdgmimecache skips the cache (OUT_OF_BOUNDS -> continue)

    def parents(self, name: str) -> list[str] | None:
        try:
            return self._parents(name)
        except (struct.error, IndexError):
            return None

    def _alias(self, name: str) -> str | None:
        lo = self._u32(4)
        if not self._in(lo, 1, 4):
            return None
        n = self._u32(lo)
        if not self._in(lo + 4, n, 8):
            return None
        a, b = 0, n - 1
        key = name.encode("utf-8", "surrogateescape")
        while b >= a:
            mid = (a + b) // 2
            ent = self.buf[self._u32(lo + 4 + 8 * mid):].split(b"\0", 1)[0]
            if ent < key:
                a = mid + 1
            elif ent > key:
                b = mid - 1
            else:
                return self._str(self._u32(lo + 4 + 8 * mid + 4))
        return None

    def _parents(self, name: str) -> list[str] | None:
        lo = self._u32(8)
        if not self._in(lo, 1, 4):
            return None
        n = self._u32(lo)
        if not self._in(lo + 4, n, 8):
            return None
        for j in range(n):
            if self._str(self._u32(lo + 4 + 8 * j)) == name:
                po = self._u32(lo + 4 + 8 * j + 4)
                k = self._u32(po)
                return [self._str(self._u32(po + 4 + 4 * i)) for i in range(k)]
        return None


def load_mime_cache(path: str) -> MimeCache | None:
    try:
        with open(path, "rb") as fh:
            buf = fh.read()
    except OSError:
        return None
    if len(buf) < 40:  # "A valid cache must be at least 40 bytes for the header." (xdgmimecache.c)
        return None
    major, minor = struct.unpack_from(">HH", buf, 0)
    if major != 1 or not (1 <= minor <= 2):
        return None
    return MimeCache(buf)


class _AliasTable:
    """xdgmimealias.c: an array of {alias, mime} pairs, appended per `aliases` file and re-sorted with the C
    library's qsort after each file (alias_entry_cmp = strcmp on the alias), looked up with bsearch.  A
    repeated alias therefore resolves to whichever entry libc's qsort/bsearch land on; the same libc
    functions are called here (ctypes), so the choice is the one GLib makes on this host."""

    class Entry(ctypes.Structure):
        _fields_ = [("alias", ctypes.c_char_p), ("mime", ctypes.c_char_p)]

    def __init__(self) -> None:
        self.libc = ctypes.CDLL(ctypes.util.find_library("c"))
        self.cmp_t = ctypes.CFUNCTYPE(ctypes.c_int, ctypes.c_void_p, ctypes.c_void_p)

        def cmp(a, b):
            ea = self.Entry.from_address(a)
            eb = self.Entry.from_address(b)
            return (ea.alias > eb.alias) - (ea.alias < eb.alias)  # strcmp sign on bytes

        self._cmp = self.cmp_t(cmp)
        self._size = ctypes.sizeof(self.Entry)
        self.arr = None
        self.libc.qsort.argtypes = [ctypes.c_void_p, ctypes.c_size_t, ctypes.c_size_t, self.cmp_t]
        self.libc.qsort.restype = None
        self.libc.bsearch.argtypes = [ctypes.c_void_p, ctypes.c_void_p, ctypes.c_size_t, ctypes.c_size_t, self.cmp_t]
        self.libc.bsearch.restype = ctypes.c_void_p

    def add_file(self, pairs: list[tuple[str, str]]) -> None:
        old = [(e.alias, e.mime) for e in self.arr] if self.arr else []
        allp = old + [(a.encode("utf-8", "surrogateescape"), m.encode("utf-8", "surrogateescape")) for a, m in pairs]
        n = len(allp)
        self.arr = (self.Entry * n)(*[self.Entry(a, m) for a, m in allp]) if n else None
        if n > 1:
            self.libc.qsort(ctypes.addressof(self.arr), n, self._size, self._cmp)

    def lookup(self, name: str) -> str | None:
        if not self.arr:
            return None
        key = self.Entry(name.encode("utf-8", "surrogateescape"), None)
        hit = self.libc.bsearch(ctypes.addressof(key), ctypes.addressof(self.arr), len(self.arr), self._size,
                                self._cmp)
        if not hit:
            return None
        return self.Entry.from_address(hit).mime.decode("utf-8", "surrogateescape")


class MimeDB:
    def __init__(self, mime_dirs: list[str]):
        self.caches: list[MimeCache] = []
        self.aliases = _AliasTable()
        self.parent_map: dict[str, list[str]] = {}
        for d in mime_dirs:
            cpath = os.path.join(d, "mime.cache")
            if os.path.exists(cpath):
                c = load_mime_cache(cpath)
                if c is not None:
                    self.caches.append(c)
                    continue
            apath = os.path.join(d, "aliases")
            if os.path.exists(apath) and os.access(apath, os.R_OK):  # fopen(…, "r") succeeded: append, then qsort
                self.aliases.add_file(_pairs_from_text(apath))
            for child, parent in _pairs_from_text(os.path.join(d, "subclasses")):
                self.parent_map.setdefault(child, []).append(parent)
        self._unalias: dict[str, str] = {}

    def unalias(self, t: str) -> str:
        if self.caches:
            for c in self.caches:
                r = c.alias(t)
                if r is not None:
                    return r
            return t
        if t not in self._unalias:
            r = self.aliases.lookup(t)
            self._unalias[t] = r if r is not None else t
        return self._unalias[t]

    def list_parents(self, t: str) -> list[str]:
        u = self.unalias(t)
        if self.caches:
            out: list[str] = []
            for c in self.caches:
                ps = c.parents(u)
                for p in ps or []:
                    if p not in out and len(out) < 127:
                        out.append(p)
            return out
        return list(self.parent_map.get(u, []))

    def type_list(self, t: str, fallback: bool) -> list[str]:
        arr = [self.unalias(t)]
        if fallback:
            i = 0
            while i < len(arr):
                cur = arr[i]
                for p in [self.unalias(cur)] + self.list_parents(cur):
                    if p not in arr:
                        arr.append(p)
                i += 1
        return arr


# ---------------------------------------------------------------- programs (glib/gutils.c, glib/gshell.c 2.90.1)
def _is_exec_file(p: str) -> bool:
    """g_file_test IS_EXECUTABLE (access X_OK) and not IS_DIR; any file type, symlinks followed."""
    return os.access(p, os.X_OK) and not os.path.isdir(p)


def _build(a: str, b: str) -> str:
    """g_build_filename(a, b) for a relative b: an empty a drops out, separators collapse."""
    if not a:
        return b
    return a.rstrip("/") + "/" + b.lstrip("/") if a.rstrip("/") else "/" + b.lstrip("/")


def find_program(program: str, path_env: str | None, workdir: str | None) -> bool:
    """g_find_program_for_path (gutils.c): working dir first for a relative name; a name that is absolute or
    holds '/' is tested directly; on a miss an absolute name fails, any other name goes on to the PATH search
    (PATH unset: "/bin:/usr/bin:."; an empty element is the bare name; relative results join the working dir)."""
    prog = program
    if workdir is not None and not program.startswith("/"):
        prog = _build(workdir, program)
    if prog.startswith("/") or "/" in program:
        if _is_exec_file(prog):
            return True
        if program.startswith("/"):
            return False
    search = path_env if path_env is not None else "/bin:/usr/bin:."
    for el in search.split(":"):
        cand = el + "/" + program if el else program
        if workdir is not None and not cand.startswith("/"):
            cand = _build(workdir, cand)
        if _is_exec_file(cand):
            return True
    return False


def _tokenize(cmd: str) -> list[str] | None:
    """tokenize_command_line (gshell.c): None on an error (dangling '\\', unmatched quote, no token)."""
    toks: list[str] = []
    cur: list[str] | None = None
    quote = ""
    quoted = False
    for i, ch in enumerate(cmd):
        if quote == "\\":
            if ch != "\n":
                cur = cur if cur is not None else []
                cur += ["\\", ch]
            quote = ""
        elif quote == "#":
            if ch == "\n":
                quote = ""
        elif quote:
            if ch == quote and not (quote == '"' and quoted):
                quote = ""
            cur = cur if cur is not None else []
            cur.append(ch)
        elif ch == "\n":
            if cur is not None:
                toks.append("".join(cur))
                cur = None
        elif ch in " \t":
            if cur:
                toks.append("".join(cur))
                cur = None
        elif ch in "'\"":
            cur = cur if cur is not None else []
            cur.append(ch)
            quote = ch
        elif ch == "\\":
            quote = ch
        elif ch == "#" and (i == 0 or cmd[i - 1] in " \n"):
            quote = "#"
        else:
            cur = cur if cur is not None else []
            cur.append(ch)
        quoted = (not quoted) if ch == "\\" else False
    if cur is not None:
        toks.append("".join(cur))
    if quote and quote != "#":
        return None
    return toks or None


def _unquote(tok: str) -> str | None:
    """g_shell_unquote (gshell.c): backslash escapes outside quotes (newline dropped), '...' literal,
    "..." with \\" \\\\ \\` \\$ \\<newline> escapes; None on an unmatched quote."""
    out: list[str] = []
    i = 0
    while i < len(tok):
        ch = tok[i]
        if ch == "\\":
            i += 1
            if i < len(tok):
                if tok[i] != "\n":
                    out.append(tok[i])
                i += 1
        elif ch == "'":
            j = tok.find("'", i + 1)
            if j < 0:
                return None
            out.append(tok[i + 1:j])
            i = j + 1
        elif ch == '"':
            i += 1
            while True:
                if i >= len(tok):
                    return None
                c = tok[i]
                if c == '"':
                    i += 1
                    break
                if c == "\\":
                    i += 1
                    if i < len(tok) and tok[i] in '"\\`$\n':
                        out.append(tok[i])
                        i += 1
                    else:
                        out.append("\\")
                else:
                    out.append(c)
                    i += 1
        else:
            out.append(ch)
            i += 1
    return "".join(out)


def shell_argv0(cmd: str) -> str | None:
    """g_shell_parse_argv: argv[0], or None when the command line does not parse."""
    cmd = cmd.split("\0", 1)[0]
    toks = _tokenize(cmd)
    if toks is None:
        return None
    argv = [_unquote(t) for t in toks]
    if any(a is None for a in argv):
        return None
    return argv[0]


# ---------------------------------------------------------------- desktop dirs
def current_desktops(value: str | None) -> list[str]:
    if value is None:
        value = ""
    out = []
    for t in value.split(":"):
        if t and all(c.isascii() and (c.isalnum() or c in "-_") for c in t):
            out.append(t.lower())
    return out


class Tweaks:
    __slots__ = ("additions", "removals", "defaults")

    def __init__(self) -> None:
        self.additions: list[str] | None = None
        self.removals: list[str] | None = None
        self.defaults: list[str] | None = None


def _expand(cur: list[str] | None, add: list[str], block: list[str] | None) -> list[str]:
    """expand_strv: the first list is taken as is; later ids skip the blocklist and any id already held."""
    if cur is None:
        return list(add)
    out = list(cur)
    for a in add:
        if block and a in block:
            continue
        if a in out:
            continue
        out.append(a)
    return out


class DesktopDir:
    def __init__(self, path: str, is_config: bool, desktops: list[str], mime: MimeDB):
        self.path = path
        self.is_config = is_config
        self.app_names: dict[str, str] | None = None
        self.tweaks: dict[str, Tweaks] = {}
        if not is_config:
            names: dict[str, str] = {}
            self._walk(path, "", names)
            self.app_names = names or None
        for d in desktops:
            self._read(os.path.join(path, f"{d}-mimeapps.list"), ADDED, False, mime)
        self._read(os.path.join(path, "mimeapps.list"), ADDED, True, mime)
        if not is_config:
            self._read(os.path.join(path, "defaults.list"), ADDED, False, mime)
            self._read(os.path.join(path, "mimeinfo.cache"), CACHE, True, mime)

    def _walk(self, d: str, prefix: str, names: dict[str, str]) -> None:
        """get_apps_from_dir: g_dir_read_name (readdir) order; a later entry of the same id replaces an earlier
        one (g_hash_table_insert), so `vendor-e.desktop` vs `vendor/e.desktop` is decided by directory order."""
        try:
            entries = os.listdir(d)  # readdir order, as g_dir_read_name sees it; deliberately unsorted
        except OSError:
            return
        for base in entries:
            fn = os.path.join(d, base)
            if base.endswith(".desktop"):
                names[prefix + base] = fn
            elif os.path.isdir(fn):
                self._walk(fn, prefix + base + "-", names)

    def _tw(self, mime_type: str, mime: MimeDB) -> Tweaks:
        u = mime.unalias(mime_type)
        t = self.tweaks.get(u)
        if t is None:
            t = self.tweaks[u] = Tweaks()
        return t

    def _read(self, filename: str, added_group: str, permitted: bool, mime: MimeDB) -> None:
        kf = load_keyfile(filename)
        if kf is None:
            return
        groups, _ = kf

        def lists(group: str):
            for k, v in groups.get(group, {}).items():
                try:
                    yield k, string_list(v)
                except KeyFileError:
                    continue

        if permitted:
            for k, ids in lists(added_group):
                t = self._tw(k, mime)
                t.additions = _expand(t.additions, ids, t.removals)
            for k, ids in lists(REMOVED):
                t = self._tw(k, mime)
                t.removals = _expand(t.removals, ids, t.additions)
        for k, ids in lists(DEFAULTS):
            t = self._tw(k, mime)
            t.defaults = _expand(t.defaults, ids, None)


class Resolver:
    def __init__(self, desktop: str | None, config_home: str, config_dirs: list[str], data_home: str,
                 data_dirs: list[str], path_env: str | None, mime_dirs: list[str] | None = None):
        self.desktops = current_desktops(desktop)
        self.path_env = path_env
        if mime_dirs is None:
            mime_dirs = [os.path.join(data_home, "mime")] + [os.path.join(d, "mime") for d in data_dirs]
        self.mime = MimeDB(mime_dirs)
        self.dirs: list[DesktopDir] = [DesktopDir(config_home, True, self.desktops, self.mime)]
        self.dirs += [DesktopDir(d, True, self.desktops, self.mime) for d in config_dirs]
        self.dirs.append(DesktopDir(os.path.join(data_home, "applications"), False, self.desktops, self.mime))
        self.dirs += [DesktopDir(os.path.join(d, "applications"), False, self.desktops, self.mime) for d in data_dirs]
        self._load_cache: dict[str, tuple[bool, bool]] = {}

    def _masked(self, idx: int, app: str) -> bool:
        for i in range(idx):
            names = self.dirs[i].app_names
            if names and app in names:
                return True
        return False

    def _mime_lookup(self, idx: int, t: str, hits: list[str], block: list[str]) -> None:
        tw = self.dirs[idx].tweaks.get(t)
        if tw is None:
            return
        for a in tw.additions or []:
            if not self._masked(idx, a) and a not in block and a not in hits:
                hits.append(a)
        for r in tw.removals or []:
            if not self._masked(idx, r) and r not in block and r not in hits:
                block.append(r)

    def load(self, filename: str) -> tuple[bool, bool]:
        """(loads, hidden) for one desktop file, as g_desktop_app_info_load_file decides."""
        if filename in self._load_cache:
            return self._load_cache[filename]
        res = (False, False)
        kf = load_keyfile(filename)
        if kf is not None:
            groups, start = kf
            res = self._validate(groups.get(DESKTOP_GROUP, {}), start)
        self._load_cache[filename] = res
        return res

    def _validate(self, g: dict[str, str], start: str | None) -> tuple[bool, bool]:
        if start != DESKTOP_GROUP:
            return (False, False)
        try:
            typ = plain_string(g["Type"]) if "Type" in g else None
        except KeyFileError:
            typ = None
        if typ != "Application":
            return (False, False)
        vals: dict[str, str | None] = {}
        for k in ("Path", "TryExec", "Exec"):
            if k in g:
                try:
                    vals[k] = plain_string(g[k])
                except KeyFileError:
                    return (False, False)
            else:
                vals[k] = None
        workdir = vals["Path"] or None
        te = vals["TryExec"]
        if te and not find_program(te, self.path_env, workdir):
            return (False, False)
        ex = vals["Exec"]
        if ex:
            argv0 = shell_argv0(ex)
            if argv0 is None or not find_program(argv0, self.path_env, workdir):
                return (False, False)
        # g_key_file_parse_value_as_boolean: trailing g_ascii_isspace bytes ignored; anything else is an error (= not hidden)
        hidden = g.get("Hidden", "").rstrip(ASCII_SPACE) in ("true", "1")
        return (True, hidden)

    def _get_app(self, k: int, app: str) -> tuple[bool, bool]:
        names = self.dirs[k].app_names
        if not names or app not in names:
            return (False, False)
        return self.load(names[app])

    def app_info_new(self, app: str) -> bool:
        for k in range(len(self.dirs)):
            ok, hidden = self._get_app(k, app)
            if ok:
                return not hidden
        return False

    def default(self, mime_type: str) -> str | None:
        block: list[str] = []
        for t in self.mime.type_list(mime_type, True):
            results: list[str] = []
            for d in self.dirs:
                tw = d.tweaks.get(t)
                for a in (tw.defaults or []) if tw else []:
                    if a not in results:
                        results.append(a)
            for j in range(len(self.dirs)):
                self._mime_lookup(j, t, results, block)
            for app in results:
                for k in range(len(self.dirs)):
                    if self._get_app(k, app)[0]:
                        return app
        return None

    def ids_for_type(self, mime_type: str, fallback: bool) -> list[str]:
        hits: list[str] = []
        block: list[str] = []
        for t in self.mime.type_list(mime_type, fallback):
            for j in range(len(self.dirs)):
                self._mime_lookup(j, t, hits, block)
        return [a for a in hits if self.app_info_new(a)]

    def resolve(self, mime_type: str) -> dict:
        return {"type": mime_type, "default": self.default(mime_type),
                "registered": self.ids_for_type(mime_type, True),
                "recommended": self.ids_for_type(mime_type, False)}


def split_path_list(v: str | None, default: str) -> list[str]:
    if not v:
        v = default
    return v.split(":")


def xdgmime_dirs(data_home_env: str | None, home: str, data_dirs_env: str | None) -> list[str]:
    """xdgmime.c xdg_init_dirs: getenv, not GLib's defaults — XDG_DATA_HOME if set (even empty), else
    $HOME/.local/share; XDG_DATA_DIRS unset -> /usr/local/share/:/usr/share/, set -> its non-empty elements
    (an empty value gives none)."""
    first = data_home_env if data_home_env is not None else os.path.join(home, ".local/share")
    raw = data_dirs_env if data_dirs_env is not None else "/usr/local/share/:/usr/share/"
    return [first + "/mime/"] + [d + "/mime/" for d in raw.split(":") if d]


def build_from_args(a: argparse.Namespace) -> Resolver:
    env = os.environ
    home = env.get("HOME", "/")
    desktop = None if a.desktop_unset else (a.desktop if a.desktop is not None else env.get("XDG_CURRENT_DESKTOP"))
    config_home = a.config_home or env.get("XDG_CONFIG_HOME") or os.path.join(home, ".config")
    data_home_env = a.data_home if a.data_home is not None else env.get("XDG_DATA_HOME")
    data_home = data_home_env or os.path.join(home, ".local", "share")
    config_dirs = split_path_list(a.config_dirs if a.config_dirs is not None else env.get("XDG_CONFIG_DIRS"), "/etc/xdg")
    data_dirs_env = a.data_dirs if a.data_dirs is not None else env.get("XDG_DATA_DIRS")
    data_dirs = split_path_list(data_dirs_env, "/usr/local/share/:/usr/share/")
    path_env = a.path if a.path is not None else env.get("PATH")
    return Resolver(desktop, config_home, config_dirs, data_home, data_dirs, path_env,
                    xdgmime_dirs(data_home_env, home, data_dirs_env))


def fmt(r: dict) -> str:
    return (f"MADO_MIME: {r['type']} default={r['default'] or 'none'} "
            f"registered={','.join(r['registered']) or '-'} recommended={','.join(r['recommended']) or '-'}")


def selftest() -> int:
    checks: list[tuple[str, bool]] = []

    def chk(name: str, cond: bool) -> None:
        checks.append((name, cond))

    app = "[Desktop Entry]\nType=Application\nName=X\nExec=sh %f\n"
    with tempfile.TemporaryDirectory() as root:
        def w(rel: str, text: str) -> None:
            p = os.path.join(root, rel)
            os.makedirs(os.path.dirname(p), exist_ok=True)
            with open(p, "w", encoding="utf-8") as fh:
                fh.write(text)

        def R(desktop: str | None = "Hyprland") -> Resolver:
            return Resolver(desktop, os.path.join(root, "cfg"), [os.path.join(root, "etc")], os.path.join(root, "home"),
                            [os.path.join(root, "sys")], "/usr/bin:/bin")

        w("sys/applications/a.desktop", app)
        w("sys/applications/b.desktop", app + "Hidden=true\n")
        w("sys/applications/c.desktop", app.replace("Exec=sh", "Exec=no-such-program-mado"))
        w("sys/applications/sub/d.desktop", app)
        w("sys/applications/mimeinfo.cache", "[MIME Cache]\ntext/plain=a.desktop;b.desktop;c.desktop;\n"
          "text/x-src=sub-d.desktop;\nimage/png=c.desktop;\n")
        w("sys/mime/subclasses", "text/x-src text/plain\n")
        w("sys/mime/aliases", "text/x-alias text/x-src\n")
        r = R()
        chk("cache addition is default", r.default("text/plain") == "a.desktop")
        chk("hidden and unloadable dropped from lists", r.resolve("text/plain")["registered"] == ["a.desktop"])
        chk("subdir id", r.default("text/x-src") == "sub-d.desktop")
        chk("alias unaliased", r.default("text/x-alias") == "sub-d.desktop")
        chk("parent in registered not recommended",
            r.ids_for_type("text/x-src", True) == ["sub-d.desktop", "a.desktop"]
            and r.ids_for_type("text/x-src", False) == ["sub-d.desktop"])
        chk("unloadable only -> none", r.default("image/png") is None)
        w("cfg/mimeapps.list", "[Default Applications]\ntext/plain=b.desktop\n")
        chk("hidden default accepted", R().default("text/plain") == "b.desktop")
        w("cfg/hyprland-mimeapps.list", "[Default Applications]\ntext/plain=sub-d.desktop\n[Added Associations]\n"
          "image/png=a.desktop\n")
        r = R()
        chk("desktop list wins", r.default("text/plain") == "sub-d.desktop")
        chk("desktop list additions ignored", r.default("image/png") is None)
        chk("other desktop ignores it", R("GNOME").default("text/plain") == "b.desktop")
        w("cfg/mimeapps.list", "[Removed Associations]\ntext/plain=a.desktop\n")
        w("cfg/hyprland-mimeapps.list", "")
        chk("removal blocks lower addition", R().resolve("text/plain")["registered"] == [])
        w("cfg/mimeapps.list", "[Removed Associations]\ntext/plain=a.desktop\n[Added Associations]\ntext/plain=a.desktop\n")
        chk("added group is read before removed whatever the file order", R().default("text/plain") == "a.desktop")
        w("cfg/mimeapps.list", "Default=x\n")
        chk("unloadable list skipped", R().default("text/plain") == "a.desktop")
        w("home/applications/a.desktop", app.replace("Type=Application", "Type=Link"))
        chk("masked lower addition skipped, hidden one taken", R().default("text/plain") == "b.desktop")
        chk("default from masked id still loads in a lower dir",
            (w("cfg/mimeapps.list", "[Default Applications]\ntext/plain=a.desktop\n"), R().default("text/plain"))[1]
            == "a.desktop")
    chk("desktops", current_desktops("KDE::bad/x:GNOME-Classic") == ["kde", "gnome-classic"])
    chk("fgets chop", [p for p in _pairs_from_text("/dev/null")] == [])
    failed = [n for n, ok in checks if not ok]
    for n in failed:
        print(f"MADO_MIME_SELFTEST_FAIL: {n}")
    print(f"MADO_MIME_SELFTEST: checks={len(checks)} failed={len(failed)}")
    return 1 if failed else 0


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("types", nargs="*", help="MIME types to resolve")
    ap.add_argument("--desktop", help="XDG_CURRENT_DESKTOP value (default: environment)")
    ap.add_argument("--desktop-unset", action="store_true")
    ap.add_argument("--config-home")
    ap.add_argument("--config-dirs", help="colon list (XDG_CONFIG_DIRS)")
    ap.add_argument("--data-home")
    ap.add_argument("--data-dirs", help="colon list (XDG_DATA_DIRS)")
    ap.add_argument("--path", help="PATH used to find TryExec/Exec programs (default: environment)")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args(argv)
    if a.selftest:
        return selftest()
    if not a.types:
        print("setup: name at least one MIME type", file=sys.stderr)
        return 2
    r = build_from_args(a)
    out = [r.resolve(t) for t in a.types]
    if a.json:
        print(json.dumps({"desktops": r.desktops, "dirs": [d.path for d in r.dirs], "results": out}, sort_keys=True))
    else:
        print(f"MADO_MIME_DIRS: desktops={','.join(r.desktops) or '-'} "
              f"config={','.join(d.path for d in r.dirs if d.is_config)} "
              f"data={','.join(d.path for d in r.dirs if not d.is_config)}")
        for x in out:
            print(fmt(x))
    return 0


if __name__ == "__main__":
    sys.exit(main())
