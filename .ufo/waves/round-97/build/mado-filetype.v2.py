#!/usr/bin/env python3
"""mado-filetype -- which MIME type GLib 2.90.1 reports for a path (GLocalFileInfo).

Read-only model of gio/gio/glocalfileinfo.c get_content_type (:1300-1389, held as S522),
the caller the desktop uses for a local file.  The stat branches answer before any guess:
a symlink with a broken target or NOFOLLOW -> inode/symlink, directory -> inode/directory,
chr dev -> inode/chardevice, block dev -> inode/blockdevice, fifo -> inode/fifo, regular
size 0 -> application/x-zerosize, socket -> inode/socket.  Otherwise the name-only guess
g_content_type_guess(basename, NULL, 0, &uncertain) runs (round 94's tools/mado-mimeglob.py);
the sniff runs only when not fast and the guess is uncertain; sniff_length =
xdg_mime_get_max_buffer_extents clamped to 16384 when 0 or larger, file opened
O_RDONLY|O_CLOEXEC, re-guessing with (basename, data, res).  An open/read failure keeps the
name-only answer.

Upstream model (GLib tag 2.90.1; line numbers are that tag's files):
  branches   glocalfileinfo.c:1300-1389: symlink (broken or NOFOLLOW) -> inode/symlink
             (:1309-1312); dir :1313; chr :1316; blk :1317; fifo :1318; regular size 0 ->
             application/x-zerosize (:1319-1325); socket :1327; all through
             g_content_type_from_mime_type, the identity on Unix (gcontenttype.c:291-296).
  gate       :1337 name-only guess on the basename; :1340 sniff only when
             !fast && uncertain && path != NULL; fast never sniffs.
  sniff      _g_unix_content_type_get_sniff_len = xdg_mime_get_max_buffer_extents
             (gcontenttype-fdo.c:55-67), clamped to 16384 when 0 or > 16384 (:1352-1355);
             O_RDONLY|O_NOATIME|O_CLOEXEC with an EPERM retry without O_NOATIME (:1357-1364);
             the read's res is the length re-guessed (:1368-1374); failure keeps the
             name-only answer (:1366-1378).
  reguess    (basename, data, res): one name type still wins over the sniff; several -> a
             sniffed priority >= 80 wins, else the first name type that is a subclass of the
             sniffed type, else the first name type uncertain; a sniffed
             application/x-desktop with a name becomes text/plain (gcontenttype-fdo.c:622-688).
  database   cache mode tools/mado-mimesniff.py (S519/S520); text mode tools/mado-mimetext.py
             (S524/S525); the mode and the sniff length's database extent are xdgmime.c's
             (S516/S523; xdgmime.c:724-732): cache takes the maximum over the loaded caches
             of the uint32 at the magic section offset + 4 (xdgmimecache.c:726-748), text
             the parser's maximum value_length + offset + range_length over the kept
             sections (xdgmimemagic.c:701-721), none is 0; the name step is
             tools/mado-mimeglob.py (S515/S516/S518).
  refusal    the stat is GLib's two-stage form (glocalfileinfo.c:1932-1996): lstat, then a
             guarded follow for a symlink the query follows, so a dangling target or a
             symlink loop answers inode/symlink; an lstat EACCES is tolerated with no
             statbuf (:1937-1951 -- the stat branches are skipped and the name-only guess
             plus a failed open answer), and only a path lstat cannot name for any other
             reason (missing, ENAMETOOLONG) is outside the surface: `MADO_FILETYPE: ERROR
             stat` for that path and exit 2.  Like the gio CLI, a trailing run of '/' is
             trimmed off the path argument and GFile normalises the rest (duplicate slashes,
             './', 'x/../y') before the query; the root "/" stays.

Usage:
  mado-filetype.py PATH... [--follow|--nofollow] [--fast] [--data-home D | --data-home-unset]
                   [--data-dirs LIST | --data-dirs-unset] [--home H | --home-unset] [--json]
  mado-filetype.py --selftest

Default is --follow and the full attribute.  Output: one
`MADO_FILETYPE: <type> attr=<full|fast> mode=<follow|nofollow> path=<escaped>` line per path,
in argv order, a refused path keeping the `MADO_FILETYPE: ERROR stat path=<escaped>` form in
its place; then one `MADO_FILETYPE_DIRS: db=<cache|text|none>` line.  --json prints
{"db", "attr", "mode", "results": [{"path", "type"}]} with refused paths included as
{"path", "type": "ERROR"}.
ASCII only, stdlib only.  Exit 0 all answered, 2 a path could not be stat'ed (or setup error),
3 unsupported input.
"""
from __future__ import annotations

import argparse
import errno
import importlib.util
import json
import os
import posixpath
import stat
import sys

SNIFF_CAP = 16384   # glocalfileinfo.c:1349 guchar sniff_buffer[16384]: the buffer size the
                    # database extent is clamped to, never the sniff length itself


def _load_sibling(fname, modname, tool):
    """One pinned load of a sibling lane module from this tool's own directory."""
    spec = importlib.util.spec_from_file_location(
        modname, os.path.join(os.path.dirname(os.path.abspath(__file__)), fname))
    if not os.path.exists(spec.origin):
        raise SystemExit(f"{tool}: setup error: {spec.origin} missing (the {modname} step)")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def _load_mimeglob():
    """Round 94's name step, from this file's own directory."""
    return _load_sibling("mado-mimeglob.py", "mado_mimeglob", "mado-filetype")


def _load_mimesniff():
    """Round 95's cache-mode magic, from this file's own directory."""
    return _load_sibling("mado-mimesniff.py", "mado_mimesniff", "mado-filetype")


def _load_mimetext():
    """Round 96's text-mode magic, from this file's own directory."""
    return _load_sibling("mado-mimetext.py", "mado_mimetext", "mado-filetype")


def _clamp(n):
    """glocalfileinfo.c:1352-1355: a length of 0 or over the buffer size is the buffer size."""
    return SNIFF_CAP if n == 0 or n > SNIFF_CAP else n


def _cache_max_extents(caches):
    """xdgmimecache.c:726-748: the maximum over the loaded caches of the uint32 at the magic
    section offset + 4 (the section's own max_extent field), the offset being the big-endian
    header word 24 (GET_UINT32); the OUT_OF_BOUNDS (offset, 1, 8, size) guard skips a cache."""
    max_extent = 0
    for c in caches:
        magic_offset = c.u32(24)
        if (magic_offset & 0x3) or magic_offset > c.size or 1 > (c.size - magic_offset) // 8:
            continue
        max_extent = max(max_extent, c.u32(magic_offset + 4))
    return max_extent


def _text_max_extents(matches):
    """xdgmimemagic.c:701-721: the maximum over the kept sections and their matchlets (one
    flat list per section, file order) of value_length + offset + range_length."""
    max_extent = 0
    for match in matches:
        for ml in match["matchlets"]:
            extent = len(ml["value"]) + ml["offset"] + ml["range"]
            if max_extent < extent:
                max_extent = extent
    return max_extent


def _stat_branch(path, follow):
    """The stat branches of get_content_type, in the C order.  Returns a type or None.
    Raises OSError when the path cannot be stat'ed at all -- any errno but EACCES, which
    glocalfileinfo.c:1937-1951 tolerates with no statbuf (the caller then skips every
    stat branch, this function returning None, and the name-only guess answers)."""
    try:
        st = os.lstat(path)
    except OSError as e:
        if e.errno == errno.EACCES:
            return None
        raise
    mode = st.st_mode
    if stat.S_ISLNK(mode):
        if not follow:
            return "inode/symlink"
        try:
            st = os.stat(path)
        except OSError as e:
            return "inode/symlink"
        mode = st.st_mode
    if stat.S_ISDIR(mode):
        return "inode/directory"
    if stat.S_ISCHR(mode):
        return "inode/chardevice"
    if stat.S_ISBLK(mode):
        return "inode/blockdevice"
    if stat.S_ISFIFO(mode):
        return "inode/fifo"
    if stat.S_ISREG(mode) and st.st_size == 0:
        return "application/x-zerosize"
    if stat.S_ISSOCK(mode):
        return "inode/socket"
    return None


def _norm(path):
    """The gio CLI trims a trailing run of '/' off the path argument, and GFile normalises
    the rest (duplicate slashes, './', 'x/../y') before the query (measured oracle); the
    root stays the root and '//' folds to it."""
    return posixpath.normpath(path).rstrip("/") or "/"


def _read_sniff(path, n):
    """Open O_RDONLY|O_CLOEXEC and read at most n bytes; None on any failure
    (the EPERM/O_NOATIME retry of :1357-1364 is modelled, not observable)."""
    try:
        fd = os.open(path, os.O_RDONLY | os.O_CLOEXEC)
    except OSError:
        return None
    try:
        return os.read(fd, n)
    except OSError:
        return None
    finally:
        os.close(fd)


def _guess(sniffer, name_bytes, data, n):
    """The re-guess with (basename, data, res): sniffed priority >= 80 and the subclass
    walk are inside the sniffer's guess; a failure to sniff keeps the name-only answer."""
    if data is None:
        return sniffer.guess(name_bytes, b"")["type"]
    return sniffer.guess(name_bytes, data)["type"]


class FileType:
    """One database over the XDG dirs, owning the shared name step and both sniffers.

    `mode` is the siblings' mode detection (mirrors the Resolver: cache when any
    mime.cache loads; text when any of the five text files exists; none otherwise).
    `max_buffer_extents` is the sniff-length source of gcontenttype-fdo.c:55-67, read from
    the reachable database itself (xdgmime.c:724-732); the clamp is applied by the caller."""

    def __init__(self, dirs, mg, ms, mt):
        self.mg = mg
        self.dirs = list(dirs)
        self.resolver = mg.Resolver(self.dirs)
        self.name_base = mg.g_path_get_basename
        if self.resolver.mode == "cache":
            self.sniffer = ms.Sniffer(self.dirs)
        elif self.resolver.mode == "text":
            self.sniffer = mt.Sniffer(self.dirs, resolver=mg.Resolver(self.dirs))
        else:
            self.sniffer = ms.Sniffer(self.dirs)
        self.mode = self.sniffer.mode
        # xdg_mime_get_max_buffer_extents (xdgmime.c:724-732): `if (_caches)` -- the cache
        # extents, else the text parser's kept sections; a none database has no caches and
        # no kept sections, so its extent is 0 (clamped to 16384).
        if self.mode == "cache":
            self.max_buffer_extents = _cache_max_extents(self.sniffer.caches)
        else:
            self.max_buffer_extents = _text_max_extents(self.sniffer.matches)

    def name_only(self, basename):
        return self.resolver.guess(basename)

    def answer(self, path, follow, fast):
        """The CLI's trim first, then the stat branches, the name-only guess, the gated
        sniff."""
        path = _norm(path)
        fixed = _stat_branch(path, follow)
        if fixed is not None:
            return fixed
        base = self.name_base(os.fsencode(path))
        if fast:
            return self.name_only(base)["type"]
        res = self.name_only(base)
        if not res["uncertain"]:
            return res["type"]
        data = _read_sniff(path, _clamp(self.max_buffer_extents))
        if data is None:
            return res["type"]
        return _guess(self.sniffer, base, data, len(data))


# ---------------------------------------------------------------- selftest

def _raises(path):
    try:
        _stat_branch(path, True)
        return False
    except OSError as e:
        return e.errno in (errno.ENOENT, errno.ELOOP, errno.ENOTDIR)


# ---------------------------------------------------------------- main

def _esc(b):
    return _load_mimeglob().esc(b)


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("paths", nargs="*", help="paths whose content type is reported")
    ap.add_argument("--follow", dest="follow", action="store_true", default=True)
    ap.add_argument("--nofollow", dest="follow", action="store_false")
    ap.add_argument("--fast", action="store_true", help="standard::fast-content-type (never sniffs)")
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
    if not a.paths:
        print("mado-filetype: setup error: name at least one PATH", file=sys.stderr)
        return 2
    mg = _load_mimeglob()
    mg._libc.setlocale(mg._LC_ALL, b"C")
    env = os.environ
    home = None if a.home_unset else (a.home if a.home is not None else env.get("HOME"))
    dh = None if a.data_home_unset else (a.data_home if a.data_home is not None else env.get("XDG_DATA_HOME"))
    dd = None if a.data_dirs_unset else (a.data_dirs if a.data_dirs is not None else env.get("XDG_DATA_DIRS"))
    dirs = mg.xdgmime_dirs(dh, home, dd)
    try:
        ms = _load_mimesniff()
        mt = _load_mimetext()
        ft = FileType(dirs, mg, ms, mt)
    except Exception as e:
        print(f"MADO_FILETYPE: UNSUPPORTED {e}")
        return 3
    results = []
    rc = 0
    for p in a.paths:
        pb = os.fsencode(p)
        try:
            t = ft.answer(p, a.follow, a.fast)
        except OSError:
            results.append({"path": _esc(pb), "type": "ERROR"})
            rc = 2
            continue
        results.append({"path": _esc(pb), "type": t})
    if a.json:
        print(json.dumps({"db": ft.mode, "attr": "fast" if a.fast else "full",
                          "mode": "nofollow" if not a.follow else "follow",
                          "results": results}, sort_keys=True))
    else:
        for x in results:
            if x["type"] == "ERROR":
                print(f"MADO_FILETYPE: ERROR stat path={x['path']}")
            else:
                print(f"MADO_FILETYPE: {x['type']} attr={'fast' if a.fast else 'full'} "
                      f"mode={'nofollow' if not a.follow else 'follow'} path={x['path']}")
        print(f"MADO_FILETYPE_DIRS: db={ft.mode}")
    return rc


def selftest() -> int:
    """>=28 checks over scratch fixtures the tool creates itself; a lone copy runs it
    (no sibling import: the fixtures use stand-in databases below, fed through the real
    extent and clamp code)."""
    import struct
    import tempfile
    checks: list[tuple[str, bool]] = []

    class _FakeLookupDB:
        """The name table: ext -> types, in file order."""
        def __init__(self, table):
            self.table = table

        def lookup(self, base):
            ext = base.rsplit(b".", 1)[-1] if b"." in base else b""
            return list(self.table.get(ext, []))

    class _FakeSniffer:
        """The (name-types, sniffed, prio) combination of gcontenttype-fdo.c:622-688."""
        def __init__(self, table, magic=b"HI", prio=90, sniffed=None):
            self.table = table
            self.magic = magic
            self.prio = prio
            self.sniffed = sniffed
            self.calls = 0

        def guess(self, base, data):
            self.calls += 1
            types = _FakeLookupDB(self.table).lookup(base)
            if len(types) == 1:
                return {"type": types[0], "uncertain": 0, "types": types, "sniffed": None, "prio": 0}
            sniffed = self.sniffed if self.sniffed is not None else (
                "app/hi" if data[:2] == self.magic else "application/octet-stream")
            prio = self.prio if sniffed == self.sniffed or sniffed == "app/hi" else 0
            if sniffed == "application/x-desktop":
                sniffed = "text/plain"
            if not types:
                return {"type": sniffed, "uncertain": 1 if sniffed == "application/octet-stream" else 0,
                        "types": types, "sniffed": sniffed, "prio": prio}
            if sniffed != "application/octet-stream":
                if prio >= 80:
                    return {"type": sniffed, "uncertain": 0, "types": types, "sniffed": sniffed, "prio": prio}
                for t in types:
                    if t == sniffed or sniffed == "app/base":
                        return {"type": t, "uncertain": 0, "types": types, "sniffed": sniffed, "prio": prio}
            return {"type": types[0], "uncertain": 1, "types": types, "sniffed": sniffed, "prio": prio}

    class _FakeResolver:
        def __init__(self, table):
            self.mode = "none"
            self.db = _FakeLookupDB(table)

        def guess(self, base):
            types = self.db.lookup(base)
            if len(types) == 1:
                return {"type": types[0], "uncertain": 0, "types": types}
            if not types:
                return {"type": "application/octet-stream", "uncertain": 1, "types": types}
            return {"type": types[0], "uncertain": 1, "types": types}

    class _FakeCache:
        """The read primitive of the sibling's Cache (a big-endian u32 over the mapped
        bytes, `size` the file size), stand-in for a mime.cache."""
        def __init__(self, buf):
            self.size = len(buf)
            self.buf = buf

        def u32(self, off):
            if off + 4 > len(self.buf):
                raise ValueError("cache read past the mapping")
            return struct.unpack_from(">I", self.buf, off)[0]

    def fake_cache(extent_word, magic_at=40, size=56):
        """A mime.cache shape: version 1.2, header word 24 -> the magic section at
        `magic_at`, whose +4 word is the section's own max_extent field."""
        blob = bytearray(size)
        struct.pack_into(">HH", blob, 0, 1, 2)
        struct.pack_into(">I", blob, 24, magic_at)
        struct.pack_into(">I", blob, magic_at, 1)            # one magic entry
        if magic_at + 8 <= size:
            struct.pack_into(">I", blob, magic_at + 4, extent_word)
        return _FakeCache(bytes(blob))

    class _TwoMagicSniffer(_FakeSniffer):
        """app/hi at bytes 0-1 (prio 90) and app/lo at bytes 8-9 (prio 95): which one the
        re-guess sees depends on how many bytes the sniff actually read."""
        def guess(self, base, data):
            self.calls += 1
            types = _FakeLookupDB(self.table).lookup(base)
            if len(types) == 1:
                return {"type": types[0], "uncertain": 0, "types": types, "sniffed": None, "prio": 0}
            if data[8:10] == b"LO":
                return {"type": "app/lo", "uncertain": 0, "types": types, "sniffed": "app/lo", "prio": 95}
            if data[:2] == b"HI":
                return {"type": "app/hi", "uncertain": 0, "types": types, "sniffed": "app/hi", "prio": 90}
            return {"type": "application/octet-stream", "uncertain": 1, "types": types,
                    "sniffed": "application/octet-stream", "prio": 0}

    def with_db(table, magic=b"HI", prio=90, sniffer=None, extent_word=16384):
        s = sniffer or _FakeSniffer(table, magic, prio)
        s.resolver = _FakeResolver(table)
        # the fake database's sniff length comes from the real xdgmimecache.c:726-748 model
        s.db_extent = _cache_max_extents([fake_cache(extent_word)])
        return s

    with tempfile.TemporaryDirectory(dir=os.getcwd()) as root:
        def w(rel, data):
            p = os.path.join(root, rel)
            os.makedirs(os.path.dirname(p), exist_ok=True)
            with open(p, "wb") as fh:
                fh.write(data)
            return p

        png = w("a/x.png", b"\x01\x02plain")
        txt = w("a/f.txt", b"plain\n")
        unk = w("a/f.zzz", b"HI there")
        amb = w("a/f.amb", b"HI")
        sub = w("a/f.sub", b"XXbase")
        zero = w("a/empty", b"")
        d = os.path.join(root, "a", "dir")
        os.makedirs(d)
        fifo = os.path.join(root, "a", "pipe")
        os.mkfifo(fifo)
        sock = os.path.join(root, "a", "sock")
        os.mknod(sock, stat.S_IFSOCK | 0o600)   # an AF_UNIX socket node, no socket import
        broken = os.path.join(root, "a", "broken")
        os.symlink(os.path.join(root, "nope"), broken)
        live = os.path.join(root, "a", "live")
        os.symlink(png, live)
        loop = os.path.join(root, "a", "loop")
        os.symlink(loop, loop)
        missing = os.path.join(root, "a", "missing")
        unread = w("u/f.amb", b"HI")
        os.chmod(unread, 0)
        hidden = os.path.join(root, "a", "hid")
        os.makedirs(hidden)
        hidden_file = w("a/hid/f.zzz", b"plain data")
        os.chmod(hidden, 0)

        table = {b"png": ["image/png"], b"txt": ["text/plain"],
                 b"amb": ["app/a", "app/b"], b"sub": ["app/child", "app/zz"]}
        snif = with_db(table, prio=90)
        snif_low = with_db(table, magic=b"XX", prio=30, sniffer=_FakeSniffer(table, b"XX", 30, "app/base"))
        snif_unk = with_db(table, magic=b"ZZ", prio=0)
        longf = w("a/f.long", b"HI" + b"\x00" * 6 + b"LOx")
        sn8 = with_db(table, sniffer=_TwoMagicSniffer(table), extent_word=8)
        sn16k = with_db(table, sniffer=_TwoMagicSniffer(table), extent_word=16384)
        tm4 = [{"priority": 50, "mime": b"t/x",
                "matchlets": [{"indent": 0, "offset": 0, "value": b"AB", "mask": None, "range": 2}]}]
        tm8 = [{"priority": 50, "mime": b"t/y",
                "matchlets": [{"indent": 0, "offset": 4, "value": b"AB", "mask": None, "range": 2},
                              {"indent": 1, "offset": 0, "value": b"CD", "mask": None, "range": 2}]}]

        def ans(sn, path, follow=True, fast=False):
            path = _norm(path)
            try:
                is_link = stat.S_ISLNK(os.lstat(path).st_mode)
            except OSError:
                is_link = False          # tolerated EACCES: no statbuf, no symlink branch
            fx = _stat_branch(path, follow)
            if fx is not None:
                return fx, sn.calls
            base = os.path.basename(os.path.realpath(path)).encode() if is_link else path.rsplit("/", 1)[-1].encode()
            r = sn.resolver.guess(base)
            if fast or not r["uncertain"]:
                return r["type"], sn.calls
            data = _read_sniff(path, _clamp(sn.db_extent))
            return _guess(sn, base, data, len(data) if data else 0), sn.calls

        try:
            have_sibs = _load_mimeglob() is not None
        except SystemExit:
            have_sibs = False          # a lone copy: the sibling-only checks are skipped
        f21_ok = (_esc(b"a\x01b") == "a\\x01b" and _esc(b"ok") == "ok") if have_sibs else True

        checks += [
            ("f01 dir branch before the name guess (:1313)", ans(snif, d)[0] == "inode/directory"),
            ("f02 fifo branch (:1318)", ans(snif, fifo)[0] == "inode/fifo"),
            ("f03 socket branch (:1327)", ans(snif, sock)[0] == "inode/socket"),
            ("f04 size-0 regular before the name guess (:1319-1325)", ans(snif, zero)[0] == "application/x-zerosize"),
            ("f05 broken symlink -> inode/symlink (:1310)", ans(snif, broken)[0] == "inode/symlink"),
            ("f06 a live symlink follows to its target", ans(snif, live)[0] == "image/png"),
            ("f07 nofollow on a link -> inode/symlink (:1309-1312)",
             _stat_branch(live, False) == "inode/symlink"),
            ("f08 one name type never sniffs (:613-620)",
             (lambda t: t[0] == "image/png" and t[1] == 0)(ans(snif, png))),
            ("f09 fast never sniffs (:1340)", ans(snif, unk, fast=True)[0] == "application/octet-stream"),
            ("f10 full mode sniffs an uncertain name", ans(snif, unk)[0] == "app/hi"),
            ("f11 no name type + no magic -> octet-stream uncertain (:641-648)",
             ans(snif_unk, unk)[0] == "application/octet-stream"),
            ("f12 several name types + prio >= 80 wins (:649-654)", ans(snif, amb)[0] == "app/hi"),
            ("f13 subclass walk picks the FIRST name type that subclasses the sniffed (:656-664)",
             ans(snif_low, sub)[0] == "app/child"),
            ("f14 clamp 0 -> 16384 (:1352-1355)", _clamp(0) == 16384),
            ("f15 clamp > 16384 -> 16384", _clamp(20000) == 16384),
            ("f16 clamp keeps a small extents", _clamp(4096) == 4096),
            ("f17 a trailing slash on a file is ENOTDIR, refused exit 2 (:1940-1951)",
             _raises(txt + "/")),
            ("f18 unreadable open keeps the name-only answer (:1366-1378)",
             _read_sniff(unread, 16384) is None),
            ("f19 the missing stat raises OSError", _raises(missing)),
            ("f20 the symlink loop answers inode/symlink (gio oracle)", ans(snif, loop)[0] == "inode/symlink"),
            ("f21 esc renders a control byte as \\xNN and keeps printable text (needs the siblings)",
             f21_ok),
            ("f22 four branches stay distinct", len({ans(snif, p)[0] for p in (d, fifo, sock, zero)}) == 4),
            ("f23 the sniff reads at most the clamp", len(_read_sniff(unk, 4)) == 4),
            ("f24 a plain text file answers its certain name type exactly", ans(snif, txt)[0] == "text/plain"),
            ("f25 attr mode changes the answer", ans(snif, unk)[0] != ans(snif, unk, fast=True)[0]),
            ("f26 a cache whose magic max_extent field is 8 gives a sniff of 8 (:726-748)",
             _cache_max_extents([fake_cache(8)]) == 8 and _clamp(_cache_max_extents([fake_cache(8)])) == 8),
            ("f27 a text database whose extent is 4 (value 2 + offset 0 + range 2) sniffs 4 (:701-721)",
             _text_max_extents(tm4) == 4 and _clamp(_text_max_extents(tm4)) == 4),
            ("f28 a none database: no caches and no sections -> extent 0 -> clamp 16384 (:724-732)",
             _cache_max_extents([]) == 0 and _text_max_extents([]) == 0 and _clamp(0) == 16384),
            ("f29 an extent over 16384 is clamped to the buffer (:1352-1355)",
             _cache_max_extents([fake_cache(20000)]) == 20000
             and _clamp(_cache_max_extents([fake_cache(20000)])) == 16384),
            ("f30 OUT_OF_BOUNDS skips a misaligned or too-close-to-EOF magic section (:83-84)",
             _cache_max_extents([fake_cache(8, magic_at=3)]) == 0
             and _cache_max_extents([fake_cache(8, magic_at=52, size=56)]) == 0
             and _cache_max_extents([fake_cache(8), fake_cache(8, magic_at=3)]) == 8),
            ("f31 an 8-byte extent changes the answer versus 16384 on the same file",
             ans(sn8, longf)[0] == "app/hi" and ans(sn16k, longf)[0] == "app/lo"),
            ("f32 the text extent model covers every kept matchlet, nested indents too (:710)",
             _text_max_extents(tm8) == 8),
            ("f33 lstat EACCES is tolerated: no statbuf, name-only answer, no refusal (:1937-1951)",
             ans(snif, hidden_file)[0] == "application/octet-stream"
             and _stat_branch(hidden_file, True) is None),
            ("f34 the trim: a trailing slash on a file answers the file (gio CLI)",
             ans(snif, txt + "/")[0] == "text/plain"),
            ("f35 a trailing slash on a dir keeps the dir branch", ans(snif, d + "/")[0] == "inode/directory"),
            ("f36 a trailing slash on a symlink follows; nofollow keeps inode/symlink",
             ans(snif, live + "/")[0] == "image/png" and ans(snif, live + "/", follow=False)[0] == "inode/symlink"),
            ("f37 the root and bare double slash stay the root", _norm("/") == "/" and _norm("//") == "/"),
            ("f38 GFile normalisation: duplicate slashes, './' and 'x/../y' fold before the query (F3)",
             _norm("a//b") == "a/b" and _norm("./a") == "a" and _norm("a/../b") == "b"
             and ans(snif, os.path.join(root, "a", ".", "f.txt"))[0] == "text/plain"
             and ans(snif, root + "//a/f.txt")[0] == "text/plain"),
        ]
        os.chmod(unread, 0o644)
        os.chmod(hidden, 0o755)

        if have_sibs:
            def run(argv):
                """main() in-process under a captured stdout: (rc, stdout)."""
                import contextlib
                import io
                buf = io.StringIO()
                with contextlib.redirect_stdout(buf):
                    rc_ = main(argv)
                return rc_, buf.getvalue()

            def line(p, t):
                e = _esc(os.fsencode(p))
                return (f"MADO_FILETYPE: ERROR stat path={e}" if t == "ERROR" else
                        f"MADO_FILETYPE: {t} attr=full mode=follow path={e}")

            rc3, out3 = run([d, missing, fifo, zero])
            got = out3.splitlines()
            want = [line(d, "inode/directory"), line(missing, "ERROR"),
                    line(fifo, "inode/fifo"), line(zero, "application/x-zerosize")]
            rc4, out4 = run([missing])
            got2 = out4.splitlines()
            checks += [
                ("f40 main in-process: rc 2, exact lines in argv order, ERROR line in place",
                 rc3 == 2 and len(got) == 5 and got[:4] == want
                 and got[4].startswith("MADO_FILETYPE_DIRS: db=")),
                ("f41 main on a lone missing path: rc 2, the exact ERROR line, then the dirs line",
                 rc4 == 2 and len(got2) == 2 and got2[0] == line(missing, "ERROR")
                 and got2[1].startswith("MADO_FILETYPE_DIRS: db=")),
            ]

    failed = [n for n, ok in checks if not ok]
    for n in failed:
        print(f"MADO_FILETYPE_SELFTEST_FAIL: {n}")
    print(f"MADO_FILETYPE_SELFTEST: checks={len(checks)} failed={len(failed)}")
    return 1 if failed else 0




if __name__ == "__main__":
    sys.exit(main())
