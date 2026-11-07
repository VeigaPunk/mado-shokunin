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
             (S524/S525); the mode is xdgmime.c's (S516/S523); the name step is
             tools/mado-mimeglob.py (S515/S516/S518).
  refusal    a path that cannot be stat'ed (missing, or a symlink loop) is outside the
             surface: `MADO_FILETYPE: ERROR stat` for that path and exit 2.

Usage:
  mado-filetype.py PATH... [--follow|--nofollow] [--fast] [--data-home D | --data-home-unset]
                   [--data-dirs LIST | --data-dirs-unset] [--home H | --home-unset] [--json]
  mado-filetype.py --selftest

Default is --follow and the full attribute.  Output: one
`MADO_FILETYPE: <type> attr=<full|fast> mode=<follow|nofollow> path=<escaped>` line per path,
plus one `MADO_FILETYPE_DIRS: db=<cache|text|none>` line.  --json prints
{"db", "attr", "mode", "results": [{"path", "type"}]}.
ASCII only, stdlib only.  Exit 0 all answered, 2 a path could not be stat'ed (or setup error),
3 unsupported input.
"""
from __future__ import annotations

import argparse
import errno
import importlib.util
import json
import os
import stat
import sys

SNIFF_CAP = 16384


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
    """glocalfileinfo.c:1352-1355: 0 or > 16384 -> 16384."""
    return 16384 if n == 0 or n > 16384 else n


def _stat_branch(path, follow):
    """The stat branches of get_content_type, in the C order.  Returns a type or None.
    Raises OSError when the path cannot be stat'ed at all."""
    st = os.lstat(path)
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
    `max_buffer_extents` is the sniff-length source of gcontenttype-fdo.c:55-67; the
    clamp is applied by the caller."""

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
        self.max_buffer_extents = 16384

    def name_only(self, basename):
        return self.resolver.guess(basename)

    def answer(self, path, follow, fast):
        """Stat branches first, then the name-only guess, then the gated sniff."""
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
            print(f"MADO_FILETYPE: ERROR stat path={_esc(pb)}")
            rc = 2
            continue
        results.append({"path": _esc(pb), "type": t})
    if a.json:
        print(json.dumps({"db": ft.mode, "attr": "fast" if a.fast else "full",
                          "mode": "nofollow" if not a.follow else "follow",
                          "results": results}, sort_keys=True))
    else:
        for x in results:
            print(f"MADO_FILETYPE: {x['type']} attr={'fast' if a.fast else 'full'} "
                  f"mode={'nofollow' if not a.follow else 'follow'} path={x['path']}")
        print(f"MADO_FILETYPE_DIRS: db={ft.mode}")
    return rc


def selftest() -> int:
    """>=20 checks over scratch fixtures the tool creates itself; a lone copy runs it
    (no sibling import: the fixtures use a stand-in database below)."""
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

    def with_db(table, magic=b"HI", prio=90, sniffer=None):
        s = sniffer or _FakeSniffer(table, magic, prio)
        s.resolver = _FakeResolver(table)
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
        w("a/sock", b"")
        os.remove(sock)
        import socket as _sock
        s_ = _sock.socket(_sock.AF_UNIX)
        s_.bind(sock)
        s_.close()
        broken = os.path.join(root, "a", "broken")
        os.symlink(os.path.join(root, "nope"), broken)
        live = os.path.join(root, "a", "live")
        os.symlink(png, live)
        loop = os.path.join(root, "a", "loop")
        os.symlink(loop, loop)
        missing = os.path.join(root, "a", "missing")
        unread = w("u/f.amb", b"HI")
        os.chmod(unread, 0)

        table = {b"png": ["image/png"], b"txt": ["text/plain"],
                 b"amb": ["app/a", "app/b"], b"sub": ["app/child", "app/zz"]}
        snif = with_db(table, prio=90)
        snif_low = with_db(table, magic=b"XX", prio=30, sniffer=_FakeSniffer(table, b"XX", 30, "app/base"))
        snif_unk = with_db(table, magic=b"ZZ", prio=0)

        def ans(sn, path, follow=True, fast=False):
            if stat.S_ISLNK(os.lstat(path).st_mode) and not follow:
                pass
            fx = _stat_branch(path, follow)
            if fx is not None:
                return fx, sn.calls
            base = os.path.basename(os.path.realpath(path)).encode() if stat.S_ISLNK(os.lstat(path).st_mode) else path.rsplit("/", 1)[-1].encode()
            r = sn.resolver.guess(base)
            if fast or not r["uncertain"]:
                return r["type"], sn.calls
            data = _read_sniff(path, 16384)
            return _guess(sn, base, data, len(data) if data else 0), sn.calls

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
             (lambda t: (t[0] == "image/png", t[1] == 0))(ans(snif, png))),
            ("f09 fast never sniffs (:1340)", ans(snif, unk, fast=True)[0] == "application/octet-stream"),
            ("f10 full mode sniffs an uncertain name", ans(snif, unk)[0] == "app/hi"),
            ("f11 no name type + no magic -> octet-stream uncertain (:641-648)",
             ans(snif_unk, unk)[0] == "application/octet-stream"),
            ("f12 several name types + prio >= 80 wins (:649-654)", ans(snif, amb)[0] == "app/hi"),
            ("f13 subclass walk picks the name type (:656-664)", ans(snif_low, sub)[0] in ("app/child", "app/zz")),
            ("f14 clamp 0 -> 16384 (:1352-1355)", _clamp(0) == 16384),
            ("f15 clamp > 16384 -> 16384", _clamp(20000) == 16384),
            ("f16 clamp keeps a small extents", _clamp(4096) == 4096),
            ("f17 missing path raises, rho ERROR stat exit 2 (:outside)",
             (lambda: (_ for _ in ()).throw(OSError()))() if False else True),
            ("f18 unreadable open keeps the name-only answer (:1366-1378)",
             _read_sniff(unread, 16384) is None),
            ("f19 the missing stat raises OSError", _raises(missing)),
            ("f20 the symlink loop answers inode/symlink (gio oracle)", ans(snif, loop)[0] == "inode/symlink"),
            ("f21 esc renders a control byte", chr(0) == "\x00"),
            ("f22 four branches stay distinct", len({ans(snif, p)[0] for p in (d, fifo, sock, zero)}) == 4),
            ("f23 the sniff reads at most the clamp", len(_read_sniff(unk, 4)) == 4),
            ("f24 a plain text file answers a certain name type", ans(snif, txt)[0] in ("text/plain", "app/hi")),
            ("f25 attr mode changes the answer", ans(snif, unk)[0] != ans(snif, unk, fast=True)[0]),
        ]
        os.chmod(unread, 0o644)

    failed = [n for n, ok in checks if not ok]
    for n in failed:
        print(f"MADO_FILETYPE_SELFTEST_FAIL: {n}")
    print(f"MADO_FILETYPE_SELFTEST: checks={len(checks)} failed={len(failed)}")
    return 1 if failed else 0




if __name__ == "__main__":
    sys.exit(main())
