#!/usr/bin/env python3
"""Round-97 C1 v2 frozen case builder: oracle-labelling probe for tools/mado-filetype.py.

Repairs and completes the w1 draft (filetype-cases-r97.json / filetype-probe-r97.py)
against Shared contract 3 and the corrected claims declaration.  The w1 draft had
18 counter-validation errors (host-db cases pointed XDG_DATA_DIRS at the literal
'/usr/share', which is not a {root} segment; empty-db cases did not declare the
XDG empty dirs the database rule requires) and lacked the seat-spec fixtures.

This probe builds every case tree in scratch, runs /usr/bin/gio on it, and writes
the frozen case JSON with sorted keys.  Every label is produced by gio on the built
root (never by hand).  The counter (quality/counters/c1-r97-filetype.py) re-derives
each label from the same envelope, so this probe materialises cases exactly the way
the counter does: only the declared files plus the declared paths, sockets bound and
closed (the socket file remains), unreadable entries chmod 0.

Usage:
  python3 filetype-probe-v2.py                 # build + label + write JSON
  python3 filetype-probe-v2.py --check         # rebuild + compare to stored JSON
  python3 filetype-probe-v2.py --scratch DIR   # scratch root
  python3 filetype-probe-v2.py --out FILE      # output JSON path

Only stdlib; ASCII only in the output JSON.
"""
from __future__ import annotations

import argparse
import base64
import hashlib
import json
import os
import shutil
import socket
import struct
import subprocess
import sys

GIO = "/usr/bin/gio"
GIO_SHA = "d216426080f847bfccdc7c735a4f349dc74f524530a19e8b1c32d04270cfc462"
GLIB2 = "2.90.1-1"
VERSION = 1
HOST_MIME = "/usr/share/mime"
HOST_CACHE = os.path.join(HOST_MIME, "mime.cache")

CLASSES = [
    "dir", "chr", "blk", "fifo", "sock", "zero", "empty", "sym", "brok",
    "nofollow", "follow", "certain", "uncertain", "fast", "readerr",
]

# --------------------------------------------------------------------------
# small content helpers
# --------------------------------------------------------------------------

def b64(b: bytes) -> str:
    return base64.b64encode(b).decode("ascii")


TEXT = b"hello world plain text\n"
TEXT2 = b"Another plain text file with some words.\n"
PNG_BYTES = b"\x89PNG\r\n\x1a\n" + b"\x00" * 40
HTML_BYTES = b"<html><head><title>t</title></head><body>hi</body></html>\n"
DESKTOP_BYTES = b"[Desktop Entry]\nName=Demo\nType=Application\nExec=/bin/true\n"
BINARY = bytes(range(1, 64))

# 8 printable text bytes then a control byte beyond an extent-8 read.
EXTENT_TEXT = b"ABCDEFGH"
EXTENT_CTRL = b"\x01"
EXTENT_TAIL = b"ijklmnopqr"


def globs2(*lines: bytes) -> bytes:
    return b"".join(line + b"\n" for line in lines)


def magic_file(sections) -> bytes:
    """sections: list of (type, [(offset, value_bytes, range_length), ...]).

    Emits the exact MIME-Magic header and [priority:type] sections with matchlet
    lines `indent>offset=<u16 len><value>[+range]\\n`.  indent is 0."""
    out = [b"MIME-Magic\x00\n"]
    for typ, matchlets in sections:
        out.append(b"[90:" + typ.encode() + b"]\n")
        for off, val, rng in matchlets:
            line = b"0>" + str(off).encode() + b"=" + len(val).to_bytes(2, "big") + val
            if rng != 1:
                line += b"+" + str(rng).encode()
            out.append(line + b"\n")
    return b"".join(out)


# --------------------------------------------------------------------------
# database presets.  Each returns a dict {relpath-under-db: bytes}; relpaths are
# relative to the db root (e.g. "mime/magic").  "none" returns {} and signals the
# probe to declare the XDG empty dirs.
# --------------------------------------------------------------------------

HOST_TEXT_FILES = ("magic", "globs", "globs2", "aliases", "subclasses",
                   "icons", "generic-icons", "XMLnamespaces")
HOST_CACHE_FILES = ("mime.cache", "globs", "globs2")


def _host_text_db() -> dict:
    out = {}
    for name in HOST_TEXT_FILES:
        with open(os.path.join(HOST_MIME, name), "rb") as fh:
            out["mime/" + name] = fh.read()
    return out


def _host_cache_bytes() -> bytes:
    with open(HOST_CACHE, "rb") as fh:
        return fh.read()


def _cache_max_extent_pos(cache: bytes):
    """Return (section_offset, extent_field_offset) for the cache's magic section."""
    section_offset = struct.unpack(">I", cache[24:28])[0]
    return section_offset, section_offset + 4


def _patch_cache_extent(cache: bytes, extent: int) -> bytes:
    c = bytearray(cache)
    _, pos = _cache_max_extent_pos(bytes(c))
    c[pos:pos + 4] = struct.pack(">I", extent)
    return bytes(c)


def _host_cache_db(cache_bytes: bytes) -> dict:
    out = {}
    for name in ("globs", "globs2"):
        with open(os.path.join(HOST_MIME, name), "rb") as fh:
            out["mime/" + name] = fh.read()
    out["mime/mime.cache"] = cache_bytes
    return out

def _bad_cache_bytes() -> bytes:
    """A cache whose magic-section offset word (u32@24) is misaligned (5), so
    the OUT_OF_BOUNDS guard skips it when computing the max buffer extent.  A
    guard-removal mutant reads u32@(5+4)=bytes[9:13] of the host cache header
    (a large value), clamps to 16384, and reads past the small extent."""
    c = bytearray(_host_cache_bytes())
    c[24:28] = struct.pack(">I", 5)   # misaligned magic_section_offset
    return bytes(c)

def _guard_db() -> dict:
    """Two-db layout for the guard leg: d1 holds a small-extent (8) cache,
    d2 holds the out-of-bounds cache.  Returned as full rel paths under d1//d2/."""
    out = {}
    for tag, cache_bytes in (("d1", _patch_cache_extent(_host_cache_bytes(), 8)),
                             ("d2", _bad_cache_bytes())):
        for name in ("globs", "globs2"):
            with open(os.path.join(HOST_MIME, name), "rb") as fh:
                out[tag + "/mime/" + name] = fh.read()
        out[tag + "/mime/mime.cache"] = cache_bytes
    return out


# Synthetic databases (text mode, fully controlled).
DB_SYNTH = {
    "mime/globs2": globs2(
        b"50:image/png:*.png",
        b"50:text/plain:*.txt",
        b"50:text/html:*.html",
        b"50:app/x-foo:*.foo",
        b"50:application/x-desktop:*.desktop",
    ),
    "mime/magic": magic_file([
        ("app/x-pngdata", [(0, PNG_BYTES[:8], 1)]),
        ("text/html", [(0, b"<html>", 1)]),
        ("application/x-desktop", [(0, b"[Desktop Entry]", 1)]),
    ]),
}

# Text-mode small extent: one matchlet value_length=7 offset=0 range=1 -> extent 8.
DB_SYNTH_SMALL = {
    "mime/magic": magic_file([
        ("app/x-nevermatch", [(0, b"\x00\x01\x02\x03\x04\x05\x06", 1)]),
    ]),
}

# Text-mode range extent: value_length=1 offset=0 range_length=8 -> extent 9.
DB_SYNTH_RANGE = {
    "mime/magic": magic_file([
        ("app/x-rangehit", [(0, b"\xaa", 8)]),
    ]),
}

# Text-mode clamp: matchlet at offset 16385 (extent 16390 > 16384).
DB_SYNTH_FAR = {
    "mime/magic": magic_file([
        ("app/x-farhit", [(16385, b"\xde\xad\xbe\xef", 1)]),
    ]),
}

# Two-type *.foo db (several name types).
DB_MULTI = {
    "mime/globs2": globs2(
        b"50:app/x-foo:*.foo",
        b"60:app/x-foo2:*.foo",
        b"50:text/plain:*.txt",
    ),
    "mime/magic": magic_file([
        ("app/x-pngdata", [(0, PNG_BYTES[:8], 1)]),
    ]),
}


DB_PRESETS = {
    "text": _host_text_db,
    "cache": lambda: _host_cache_db(_host_cache_bytes()),
    "cache8": lambda: _host_cache_db(_patch_cache_extent(_host_cache_bytes(), 8)),
    "synth": lambda: dict(DB_SYNTH),
    "synthsmall": lambda: dict(DB_SYNTH_SMALL),
    "synthrange": lambda: dict(DB_SYNTH_RANGE),
    "synthfar": lambda: dict(DB_SYNTH_FAR),
    "multi": lambda: dict(DB_MULTI),
    "none": lambda: {},
}

NONE_EMPTY_DIRS = ("dh", "db")


# --------------------------------------------------------------------------
# case specs.  Each builder returns a dict with keys:
#   id, class, db (preset name or "multi2"), files {rel:bytes}, empty_dirs [..],
#   paths [..], mode, attr.
# "multi2" uses d1/d2 db dirs with separate content.
# --------------------------------------------------------------------------

def C(cid, cls, db, files, paths, mode="follow", attr="full", empty_dirs=()):
    return {"id": cid, "class": cls, "db": db, "files": files,
            "empty_dirs": list(empty_dirs), "paths": paths,
            "mode": mode, "attr": attr}


def P(rel, typ, target=None):
    d = {"path": rel, "type": typ}
    if target is not None:
        d["target"] = target
    return d


BUILDERS = []


def add(fn):
    BUILDERS.append(fn)
    return fn


# ============================== dir ========================================
@add
def _():
    return C("dir-01-plain-subdir", "dir", "synth",
             {"sub/inner.txt": TEXT},
             [P("sub", "dir"), P("sub/inner.txt", "file")])


@add
def _():
    return C("dir-02-dir-named-x-png", "dir", "synth",
             {"x.png/inner.txt": TEXT},
             [P("x.png", "dir"), P("x.png/inner.txt", "file")])


@add
def _():
    return C("dir-03-nested-dirs", "dir", "synth",
             {"a/b/c.txt": TEXT},
             [P("a", "dir"), P("a/b", "dir"), P("a/b/c.txt", "file")],
             mode="nofollow")


@add
def _():
    return C("dir-04-dir-fast", "dir", "synth", {"sub/": None},
             [P("sub", "dir")], attr="fast")


@add
def _():
    return C("dir-05-dir-with-slash", "dir", "synth", {"d/f.foo": TEXT},
             [P("d/", "dir"), P("d/f.foo", "file")], mode="nofollow")


@add
def _():
    return C("dir-06-empty-db-dir", "dir", "none", {},
             [P("edir", "dir")], empty_dirs=NONE_EMPTY_DIRS)


@add
def _():
    return C("dir-07-synth-db-dir", "dir", "synth", {"sub/a.txt": TEXT},
             [P("sub", "dir"), P("sub/a.txt", "file")])


@add
def _():
    return C("dir-08-two-dirs", "dir", "synth", {"s1/x.txt": TEXT, "s2/y.png": PNG_BYTES},
             [P("s1", "dir"), P("s2", "dir")])


@add
def _():
    return C("dir-09-dir-nofollow-fast", "dir", "synth", {"sub/": None},
             [P("sub/", "dir")], mode="nofollow", attr="fast")


@add
def _():
    return C("dir-10-synth-db-dir", "dir", "synth", {"hdir/a.txt": TEXT},
             [P("hdir", "dir"), P("hdir/a.txt", "file")])

@add
def _():
    # trailing-slash argument on a regular file: tool + oracle strip it -> text/plain
    return C("dir-11-trailing-slash-file", "dir", "synth", {"a.txt": TEXT},
             [P("a.txt/", "file")])


@add
def _():
    # trailing-slash argument on an absolute chardev: /dev/null/ -> inode/chardevice
    return C("dir-12-trailing-slash-chardev", "dir", "synth", {},
             [P("/dev/null/", "chardev")])


# ============================== chr =========================================
@add
def _():
    return C("chr-01-dev-null", "chr", "synth", {}, [P("/dev/null", "chardev")])


@add
def _():
    return C("chr-02-dev-zero", "chr", "synth", {}, [P("/dev/zero", "chardev")])


@add
def _():
    return C("chr-03-dev-full", "chr", "synth", {}, [P("/dev/full", "chardev")])


@add
def _():
    return C("chr-04-dev-null-nofollow", "chr", "synth", {},
             [P("/dev/null", "chardev")], mode="nofollow")


@add
def _():
    return C("chr-05-dev-zero-fast", "chr", "synth", {},
             [P("/dev/zero", "chardev")], attr="fast")


@add
def _():
    return C("chr-06-dev-null-nofollow-fast", "chr", "synth", {},
             [P("/dev/null", "chardev")], mode="nofollow", attr="fast")


@add
def _():
    return C("chr-07-synth-db-chardev", "chr", "synth", {}, [P("/dev/null", "chardev")])


@add
def _():
    return C("chr-08-none-db-chardev", "chr", "none", {}, [P("/dev/zero", "chardev")],
             empty_dirs=NONE_EMPTY_DIRS)


@add
def _():
    return C("chr-09-dev-tty", "chr", "synth", {}, [P("/dev/tty", "chardev")])


# ============================== blk =========================================
@add
def _():
    return C("blk-01-dev-nvme1n1", "blk", "synth", {}, [P("/dev/nvme1n1", "blkdev")])


@add
def _():
    return C("blk-02-dev-sda", "blk", "synth", {}, [P("/dev/sda", "blkdev")])


@add
def _():
    return C("blk-03-dev-nvme1n1-nofollow", "blk", "synth", {},
             [P("/dev/nvme1n1", "blkdev")], mode="nofollow")


@add
def _():
    return C("blk-04-dev-nvme1n1-fast", "blk", "synth", {},
             [P("/dev/nvme1n1", "blkdev")], attr="fast")


@add
def _():
    return C("blk-05-dev-nvme1n1p1", "blk", "synth", {}, [P("/dev/nvme1n1p1", "blkdev")])


@add
def _():
    return C("blk-06-dev-sda-nofollow-fast", "blk", "synth", {},
             [P("/dev/sda", "blkdev")], mode="nofollow", attr="fast")


@add
def _():
    return C("blk-07-synth-db-blkdev", "blk", "synth", {}, [P("/dev/nvme1n1", "blkdev")])


@add
def _():
    return C("blk-08-none-db-blkdev", "blk", "none", {}, [P("/dev/sda1", "blkdev")],
             empty_dirs=NONE_EMPTY_DIRS)


@add
def _():
    return C("blk-09-dev-nvme0n1", "blk", "synth", {}, [P("/dev/nvme0n1", "blkdev")])


@add
def _():
    return C("blk-10-dev-dm0", "blk", "synth", {}, [P("/dev/dm-0", "blkdev")])


# ============================== fifo ========================================
@add
def _():
    return C("fifo-01-plain", "fifo", "synth", {}, [P("pipe", "fifo")])


@add
def _():
    return C("fifo-02-nofollow", "fifo", "synth", {}, [P("pipe", "fifo")], mode="nofollow")


@add
def _():
    return C("fifo-03-fast", "fifo", "synth", {}, [P("pipe", "fifo")], attr="fast")


@add
def _():
    return C("fifo-04-two-pipes", "fifo", "synth", {},
             [P("p1", "fifo"), P("p2", "fifo")])

@add
def _():
    return C("fifo-05-pipe-named-png", "fifo", "synth", {}, [P("pipe.png", "fifo")])


@add
def _():
    return C("fifo-06-synth-db-pipe", "fifo", "synth", {}, [P("pipe", "fifo")])


@add
def _():
    return C("fifo-07-pipe-in-subdir", "fifo", "synth", {"sub/x.txt": TEXT},
             [P("sub/pipe", "fifo")], mode="nofollow")


@add
def _():
    return C("fifo-08-pipe-dot-name", "fifo", "synth", {}, [P(".pipe", "fifo")])


@add
def _():
    return C("fifo-09-pipe-nofollow-fast", "fifo", "synth", {},
             [P("pipe", "fifo")], mode="nofollow", attr="fast")


# ============================== sock ========================================
@add
def _():
    return C("sock-01-plain", "sock", "synth", {}, [P("sock", "sock")])


@add
def _():
    return C("sock-02-nofollow", "sock", "synth", {}, [P("sock", "sock")], mode="nofollow")


@add
def _():
    return C("sock-03-fast", "sock", "synth", {}, [P("sock", "sock")], attr="fast")


@add
def _():
    return C("sock-04-two-sockets", "sock", "synth", {},
             [P("s1", "sock"), P("s2", "sock")])


@add
def _():
    return C("sock-05-socket-named-txt", "sock", "synth", {}, [P("sock.txt", "sock")])


@add
def _():
    return C("sock-06-synth-db-socket", "sock", "synth", {}, [P("sock", "sock")])


@add
def _():
    return C("sock-07-socket-in-subdir", "sock", "synth", {"sub/x.txt": TEXT},
             [P("sub/sock", "sock")], mode="nofollow")


@add
def _():
    return C("sock-08-socket-dot-name", "sock", "synth", {}, [P(".sock", "sock")])


@add
def _():
    return C("sock-09-socket-nofollow-fast", "sock", "synth", {},
             [P("sock", "sock")], mode="nofollow", attr="fast")


# ============================== zero ========================================
@add
def _():
    return C("zero-01-empty-png-name", "zero", "synth", {"z.png": b""},
             [P("z.png", "file")])


@add
def _():
    return C("zero-02-empty-no-name-type", "zero", "synth", {"bfile": b""},
             [P("bfile", "file")])


@add
def _():
    return C("zero-03-empty-txt", "zero", "synth", {"e.txt": b""}, [P("e.txt", "file")])


@add
def _():
    return C("zero-04-empty-fast", "zero", "synth", {"e.txt": b""},
             [P("e.txt", "file")], attr="fast")


@add
def _():
    return C("zero-05-empty-nofollow", "zero", "synth", {"e.png": b""},
             [P("e.png", "file")], mode="nofollow")


@add
def _():
    return C("zero-06-two-empty-files", "zero", "synth", {"a": b"", "b.bin": b""},
             [P("a", "file"), P("b.bin", "file")])


@add
def _():
    return C("zero-07-empty-synth-db", "zero", "synth", {"z.png": b""}, [P("z.png", "file")])


@add
def _():
    return C("zero-08-empty-none-db", "zero", "none", {"z.png": b""}, [P("z.png", "file")],
             empty_dirs=NONE_EMPTY_DIRS)


@add
def _():
    return C("zero-09-empty-desktop-name", "zero", "synth", {"e.desktop": b""},
             [P("e.desktop", "file")])


@add
def _():
    # /proc/self/status via a symlink (the counter rejects absolute non-device
    # case paths; a follow-mode symlink reaches the same procfs zerosize branch).
    return C("zero-10-proc-self-status", "zero", "synth", {},
             [P("procstatus", "symlink", "/proc/self/status")])


@add
def _():
    return C("zero-11-empty-synth-db", "zero", "synth", {"z.foo": b""}, [P("z.foo", "file")])


# ============================== empty =======================================
@add
def _():
    return C("empty-01-text-no-name-type", "empty", "synth", {"note": TEXT},
             [P("note", "file")])


@add
def _():
    return C("empty-02-text-txt-name", "empty", "synth", {"note.txt": TEXT},
             [P("note.txt", "file")])


@add
def _():
    return C("empty-03-binary-no-name", "empty", "synth", {"blob": BINARY},
             [P("blob", "file")])


@add
def _():
    return C("empty-04-png-no-name", "empty", "synth", {"pic": PNG_BYTES},
             [P("pic", "file")])


@add
def _():
    return C("empty-05-text-fast", "empty", "synth", {"note": TEXT},
             [P("note", "file")], attr="fast")


@add
def _():
    return C("empty-06-text-nofollow", "empty", "synth", {"note": TEXT},
             [P("note", "file")], mode="nofollow")


@add
def _():
    return C("empty-07-empty-none-db", "empty", "none", {"blob": BINARY},
             [P("blob", "file")], empty_dirs=NONE_EMPTY_DIRS)


@add
def _():
    return C("empty-08-html-no-name", "empty", "synth", {"page": HTML_BYTES},
             [P("page", "file")])


@add
def _():
    return C("empty-09-text-db", "empty", "text", {"note": TEXT}, [P("note", "file")])


# ============================== sym =========================================
@add
def _():
    return C("sym-01-link-to-file-follow", "sym", "synth",
             {"real.txt": TEXT},
             [P("link", "symlink", "real.txt"), P("real.txt", "file")])


@add
def _():
    return C("sym-02-link-to-file-nofollow", "sym", "synth",
             {"real.txt": TEXT},
             [P("link", "symlink", "real.txt"), P("real.txt", "file")], mode="nofollow")


@add
def _():
    return C("sym-03-link-to-dir-follow", "sym", "synth", {"sub/x.txt": TEXT},
             [P("dlink", "symlink", "sub"), P("sub/x.txt", "file")])


@add
def _():
    return C("sym-04-link-to-dir-nofollow", "sym", "synth", {"sub/x.txt": TEXT},
             [P("dlink", "symlink", "sub"), P("sub/x.txt", "file")], mode="nofollow")


@add
def _():
    return C("sym-05-link-to-fifo-follow", "sym", "synth", {},
             [P("flink", "symlink", "pipe"), P("pipe", "fifo")])


@add
def _():
    return C("sym-06-link-to-file-fast", "sym", "synth", {"real.txt": TEXT},
             [P("link", "symlink", "real.txt"), P("real.txt", "file")], attr="fast")


@add
def _():
    return C("sym-07-two-links", "sym", "synth", {"r1.txt": TEXT, "r2.foo": TEXT},
             [P("l1", "symlink", "r1.txt"), P("l2", "symlink", "r2.foo"),
              P("r1.txt", "file"), P("r2.foo", "file")])


@add
def _():
    return C("sym-08-link-named-png", "sym", "synth", {"real.bin": BINARY},
             [P("link.png", "symlink", "real.bin"), P("real.bin", "file")])


@add
def _():
    return C("sym-09-synth-db-link", "sym", "synth", {"real.txt": TEXT},
             [P("link", "symlink", "real.txt"), P("real.txt", "file")])


@add
def _():
    return C("sym-10-link-in-subdir", "sym", "synth", {"sub/real.txt": TEXT},
             [P("sub/link", "symlink", "real.txt"), P("sub/real.txt", "file")],
             mode="nofollow")

@add
def _():
    # trailing-slash on a symlink under nofollow: link/ -> inode/symlink
    return C("sym-11-trailing-slash-link-nofollow", "sym", "synth", {"a.txt": TEXT},
             [P("link/", "symlink", "a.txt")], mode="nofollow")


@add
def _():
    # trailing-slash on a symlink under follow: link/ -> a.txt -> text/plain
    return C("sym-12-trailing-slash-link-follow", "sym", "synth", {"a.txt": TEXT},
             [P("link/", "symlink", "a.txt")])


# ============================== brok ========================================
@add
def _():
    return C("brok-01-dangling-follow", "brok", "synth", {},
             [P("dang", "symlink", "nope")])


@add
def _():
    return C("brok-02-dangling-nofollow", "brok", "synth", {},
             [P("dang", "symlink", "nope")], mode="nofollow")


@add
def _():
    return C("brok-03-self-loop-follow", "brok", "synth", {},
             [P("l", "symlink", "l")])


@add
def _():
    return C("brok-04-self-loop-nofollow", "brok", "synth", {},
             [P("l", "symlink", "l")], mode="nofollow")


@add
def _():
    return C("brok-05-two-node-loop-follow", "brok", "synth", {},
             [P("l1", "symlink", "l2"), P("l2", "symlink", "l1")])


@add
def _():
    return C("brok-06-dangling-fast", "brok", "synth", {},
             [P("dang", "symlink", "nope")], attr="fast")


@add
def _():
    return C("brok-07-dangling-in-subdir", "brok", "synth", {"sub/x.txt": TEXT},
             [P("sub/dang", "symlink", "../nope")])


@add
def _():
    return C("brok-08-synth-db-dangling", "brok", "synth", {},
             [P("dang", "symlink", "nope")])


@add
def _():
    return C("brok-09-dangling-named-png", "brok", "synth", {},
             [P("dang.png", "symlink", "nope")])


@add
def _():
    return C("brok-10-none-db-loop", "brok", "none", {},
             [P("loop", "symlink", "loop")], empty_dirs=NONE_EMPTY_DIRS)


# ============================== nofollow ====================================
@add
def _():
    return C("nofollow-01-link-file", "nofollow", "synth",
             {"real.txt": TEXT},
             [P("link", "symlink", "real.txt"), P("real.txt", "file")])


@add
def _():
    return C("nofollow-02-dangling", "nofollow", "synth", {},
             [P("dang", "symlink", "nope")])


@add
def _():
    return C("nofollow-03-dirlink", "nofollow", "synth", {"sub/x.txt": TEXT},
             [P("dlink", "symlink", "sub"), P("sub/x.txt", "file")])


@add
def _():
    return C("nofollow-04-loop", "nofollow", "synth", {},
             [P("l", "symlink", "l")])


@add
def _():
    return C("nofollow-05-mixed", "nofollow", "synth", {"real.txt": TEXT},
             [P("link", "symlink", "real.txt"), P("pipe", "fifo"),
              P("sock", "sock"), P("real.txt", "file")])


@add
def _():
    return C("nofollow-06-empty", "nofollow", "synth", {"e.txt": b""}, [P("e.txt", "file")])


@add
def _():
    return C("nofollow-07-dir", "nofollow", "synth", {"sub/": None}, [P("sub", "dir")])


@add
def _():
    return C("nofollow-08-devices", "nofollow", "synth", {},
             [P("/dev/null", "chardev"), P("/dev/nvme1n1", "blkdev")])


@add
def _():
    return C("nofollow-09-sym-brok-file", "nofollow", "synth", {"real.txt": TEXT},
             [P("link", "symlink", "real.txt"), P("dang", "symlink", "nope"),
              P("real.txt", "file")])


# ============================== follow ======================================
@add
def _():
    return C("follow-01-link-file", "follow", "synth", {"real.txt": TEXT},
             [P("link", "symlink", "real.txt"), P("real.txt", "file")])


@add
def _():
    return C("follow-02-dangling", "follow", "synth", {}, [P("dang", "symlink", "nope")])


@add
def _():
    return C("follow-03-dirlink", "follow", "synth", {"sub/x.txt": TEXT},
             [P("dlink", "symlink", "sub"), P("sub/x.txt", "file")])


@add
def _():
    return C("follow-04-loop", "follow", "synth", {}, [P("l", "symlink", "l")])


@add
def _():
    return C("follow-05-mixed", "follow", "synth", {"real.txt": TEXT},
             [P("link", "symlink", "real.txt"), P("pipe", "fifo"),
              P("sock", "sock"), P("real.txt", "file")])


@add
def _():
    return C("follow-06-empty", "follow", "synth", {"e.txt": b""}, [P("e.txt", "file")])


@add
def _():
    return C("follow-07-dir", "follow", "synth", {"sub/": None}, [P("sub", "dir")])


@add
def _():
    return C("follow-08-devices", "follow", "synth", {},
             [P("/dev/zero", "chardev"), P("/dev/sda", "blkdev")])


@add
def _():
    return C("follow-09-sym-brok-file", "follow", "synth", {"real.txt": TEXT},
             [P("link", "symlink", "real.txt"), P("dang", "symlink", "nope"),
              P("real.txt", "file")])


# ============================== certain =====================================
@add
def _():
    return C("certain-01-text-in-a-png", "certain", "synth", {"a.png": TEXT},
             [P("a.png", "file")])


@add
def _():
    return C("certain-02-png-in-b-txt", "certain", "synth", {"b.txt": PNG_BYTES},
             [P("b.txt", "file")])


@add
def _():
    return C("certain-03-html-in-txt", "certain", "synth", {"a.txt": HTML_BYTES},
             [P("a.txt", "file")])


@add
def _():
    return C("certain-04-png-in-foo", "certain", "synth", {"a.foo": PNG_BYTES},
             [P("a.foo", "file")])


@add
def _():
    return C("certain-05-text-in-png-nofollow", "certain", "synth", {"a.png": TEXT},
             [P("a.png", "file")], mode="nofollow")


@add
def _():
    return C("certain-06-certain-fast", "certain", "synth", {"a.png": TEXT},
             [P("a.png", "file")], attr="fast")


@add
def _():
    return C("certain-07-text-in-desktop", "certain", "synth", {"a.desktop": TEXT},
             [P("a.desktop", "file")])


@add
def _():
    return C("certain-08-two-files", "certain", "synth",
             {"a.png": TEXT, "b.txt": PNG_BYTES},
             [P("a.png", "file"), P("b.txt", "file")])


@add
def _():
    return C("certain-09-synth-db-certain", "certain", "synth", {"a.png": TEXT},
             [P("a.png", "file")])


@add
def _():
    return C("certain-10-none-db-certain", "certain", "none", {"a.png": TEXT},
             [P("a.png", "file")], empty_dirs=NONE_EMPTY_DIRS)


@add
def _():
    return C("certain-11-text-db-certain", "certain", "text", {"a.txt": PNG_BYTES},
             [P("a.txt", "file")])


# ============================== uncertain ===================================
@add
def _():
    return C("uncertain-01-png-in-readme", "uncertain", "synth", {"README": PNG_BYTES},
             [P("README", "file")])


@add
def _():
    return C("uncertain-02-text-in-blobbin", "uncertain", "synth", {"blob.bin": TEXT},
             [P("blob.bin", "file")])


@add
def _():
    return C("uncertain-03-html-in-pagehtml", "uncertain", "synth",
             {"page.html": HTML_BYTES}, [P("page.html", "file")])


@add
def _():
    return C("uncertain-04-binary-no-name", "uncertain", "synth", {"blob": BINARY},
             [P("blob", "file")])


@add
def _():
    return C("uncertain-05-multi-foo-text", "uncertain", "multi", {"m.foo": TEXT},
             [P("m.foo", "file")])


@add
def _():
    return C("uncertain-06-multi-foo-png", "uncertain", "multi", {"m.foo": PNG_BYTES},
             [P("m.foo", "file")])


@add
def _():
    return C("uncertain-07-desktop-no-name", "uncertain", "synth",
             {"appfile": DESKTOP_BYTES}, [P("appfile", "file")])


@add
def _():
    return C("uncertain-08-cache-db-uncertain", "uncertain", "cache",
             {"README": PNG_BYTES}, [P("README", "file")])


@add
def _():
    return C("uncertain-09-none-db-uncertain", "uncertain", "none", {"blob": BINARY},
             [P("blob", "file")], empty_dirs=NONE_EMPTY_DIRS)


@add
def _():
    # text-mode small extent (extent=8): 8 text bytes then a control byte.
    return C("uncertain-10-text-extent-small", "uncertain", "synthsmall",
             {"noext": EXTENT_TEXT + EXTENT_CTRL + EXTENT_TAIL}, [P("noext", "file")])


@add
def _():
    # text-mode range extent: matchlet needs range bytes to match.
    return C("uncertain-11-text-extent-range", "uncertain", "synthrange",
             {"noext": b"ABCDEFG" + b"\xaa" + b"hijklmn"}, [P("noext", "file")])


@add
def _():
    # text-mode clamp: matchlet window beyond 16384 is not read.
    data = b"A" * 16385 + b"\xde\xad\xbe\xef" + b"B" * 10
    return C("uncertain-12-text-extent-clamp", "uncertain", "synthfar",
             {"noext": data}, [P("noext", "file")])


@add
def _():
    # cache-mode small extent: patched mime.cache max_extent=8.
    return C("uncertain-13-cache-extent-small", "uncertain", "cache8",
             {"noext": EXTENT_TEXT + EXTENT_CTRL + EXTENT_TAIL}, [P("noext", "file")])


@add
def _():
    # cache-mode OUT_OF_BOUNDS guard leg: d1 = small-extent (8) cache, d2 = cache
    # whose magic-section offset is misaligned (guard skips it).  The small-extent
    # discriminator file (8 text + control@8 + text) stays text/plain under the
    # correct max_extent=8; a guard-removal mutant reads a large extent from the
    # bad cache, clamps to 16384, reads the control byte, and answers octet-stream.
    files = dict(_guard_db())
    files["noext"] = EXTENT_TEXT + EXTENT_CTRL + EXTENT_TAIL
    return C("uncertain-14-cache-guard-badcache", "uncertain", "multi2",
             files, [P("noext", "file")], empty_dirs=("dh",))


# ============================== fast ========================================
@add
def _():
    return C("fast-01-png-readme", "fast", "synth", {"README": PNG_BYTES},
             [P("README", "file")], attr="fast")


@add
def _():
    return C("fast-02-text-blobbin", "fast", "synth", {"blob.bin": TEXT},
             [P("blob.bin", "file")], attr="fast")


@add
def _():
    # several name types (page.html) full vs fast contrast.
    return C("fast-03-html-pagehtml", "fast", "synth", {"page.html": HTML_BYTES},
             [P("page.html", "file")], attr="fast")


@add
def _():
    return C("fast-04-binary-no-name", "fast", "synth", {"blob": BINARY},
             [P("blob", "file")], attr="fast")


@add
def _():
    return C("fast-05-multi-foo", "fast", "multi", {"m.foo": PNG_BYTES},
             [P("m.foo", "file")], attr="fast")


@add
def _():
    return C("fast-06-desktop-no-name", "fast", "synth", {"appfile": DESKTOP_BYTES},
             [P("appfile", "file")], attr="fast")


@add
def _():
    return C("fast-07-certain-fast", "fast", "synth", {"a.png": TEXT},
             [P("a.png", "file")], attr="fast")


@add
def _():
    return C("fast-08-zero-fast", "fast", "synth", {"z.png": b""}, [P("z.png", "file")],
             attr="fast")


@add
def _():
    return C("fast-09-synth-db-fast", "fast", "synth", {"README": PNG_BYTES},
             [P("README", "file")], attr="fast")


@add
def _():
    return C("fast-10-none-db-fast", "fast", "none", {"blob": BINARY},
             [P("blob", "file")], attr="fast", empty_dirs=NONE_EMPTY_DIRS)


# ============================== readerr =====================================
@add
def _():
    return C("readerr-01-000-uncertain-png", "readerr", "synth", {"secretdata": PNG_BYTES},
             [P("secretdata", "unreadable")])


@add
def _():
    return C("readerr-02-000-text-uncertain", "readerr", "synth", {"secretdata": TEXT},
             [P("secretdata", "unreadable")])


@add
def _():
    return C("readerr-03-000-certain-name", "readerr", "synth", {"secret.txt": TEXT},
             [P("secret.txt", "unreadable")])


@add
def _():
    return C("readerr-04-000-multi-foo", "readerr", "multi", {"m.foo": PNG_BYTES},
             [P("m.foo", "unreadable")])


@add
def _():
    return C("readerr-05-000-in-subdir", "readerr", "synth", {"sub/secretdata": PNG_BYTES},
             [P("sub/secretdata", "unreadable")])


@add
def _():
    return C("readerr-06-readable-control", "readerr", "synth", {"mystery": PNG_BYTES},
             [P("mystery", "file")])


@add
def _():
    return C("readerr-07-000-nofollow", "readerr", "synth", {"secretdata": PNG_BYTES},
             [P("secretdata", "unreadable")], mode="nofollow")


@add
def _():
    return C("readerr-08-000-fast", "readerr", "synth", {"secretdata": PNG_BYTES},
             [P("secretdata", "unreadable")], attr="fast")


@add
def _():
    return C("readerr-09-two-unreadable", "readerr", "synth",
             {"s1": PNG_BYTES, "s2.txt": TEXT},
             [P("s1", "unreadable"), P("s2.txt", "unreadable")])


@add
def _():
    return C("readerr-10-synth-db-readable", "readerr", "synth", {"mystery": PNG_BYTES},
             [P("mystery", "file")])

@add
def _():
    # text file under a mode-000 parent directory, NONE db (no name->type table):
    # full attr -> octet-stream (EACCES-tolerant stat; content sniff fails and there
    # is no name fallback).  The dir itself -> inode/directory.
    return C("readerr-11-dir-unreadable", "readerr", "none", {"sub/note.txt": TEXT},
             [P("sub", "dir-unreadable"), P("sub/note.txt", "file")],
             empty_dirs=NONE_EMPTY_DIRS)


@add
def _():
    # typed-name variant: same locked parent but a synth db whose globs map
    # *.txt -> text/plain, under the fast (name-only) attr -> text/plain.  This is
    # the name-based answer the full attr cannot reach through the mode-000 dir.
    return C("readerr-12-dir-unreadable-named", "readerr", "synth", {"sub/note.txt": TEXT},
             [P("sub", "dir-unreadable"), P("sub/note.txt", "file")], attr="fast")


@add
def _():
    # a path listed in paths but never materialised: gio exits 2 with no attribute,
    # so the label is ERROR and the tool's ERROR-stat + exit-2 branch is scored.
    return C("readerr-13-missing", "readerr", "synth", {},
             [P("nope.txt", "missing")])


# --------------------------------------------------------------------------
# verifier / builder
# --------------------------------------------------------------------------

def _db_files(db: str, files_out: dict) -> None:
    if db == "multi2":
        # two db dirs d1/d2; content placed by caller via files under d1//d2/
        return
    preset = DB_PRESETS.get(db)
    if preset is None:
        raise ValueError(f"unknown db preset {db!r}")
    for rel, data in preset().items():
        files_out["db/" + rel] = data


def run_case(scratch_root: str, spec: dict) -> dict:
    cid = spec["id"]
    case_root = os.path.join(scratch_root, "cases", cid)
    if os.path.exists(case_root):
        shutil.rmtree(case_root)
    os.makedirs(case_root)

    # Collect every regular file byte in memory (db tree + scored files + the
    # empty-dir declarations), mirroring the counter's files dict.
    files_mem: dict = {}   # rel -> bytes (or None for a declared empty dir)
    _db_files(spec["db"], files_mem)
    for rel, data in spec["files"].items():
        if data is None:
            # explicit directory marker (e.g. "sub/")
            files_mem[rel if rel.endswith("/") else rel + "/"] = None
        else:
            files_mem[rel] = data
    for d in spec["empty_dirs"]:
        files_mem[d + "/"] = None

    # Materialise: write regular files, create declared dirs.
    for rel in sorted(files_mem):
        if files_mem[rel] is None:
            os.makedirs(os.path.join(case_root, rel.rstrip("/")), exist_ok=True)
            continue
        ap = os.path.join(case_root, rel)
        parent = os.path.dirname(ap)
        if parent:
            os.makedirs(parent, exist_ok=True)
        with open(ap, "wb") as fh:
            fh.write(files_mem[rel])

    # Create the declared paths exactly as the counter does.  dir-unreadable dirs are
    # created now but chmod 000 only after every child fixture is materialised.
    dir_unreadable: list = []
    for ent in spec["paths"]:
        t = ent["type"]
        rp = ent["path"]
        if t in ("chardev", "blkdev"):
            # absolute host path; must exist with the right kind (checked at freeze)
            continue
        if t == "missing":
            # listed in paths but never materialised; gio answers ERROR (no attribute)
            continue
        p = os.path.join(case_root, rp.rstrip("/"))
        if t == "dir":
            os.makedirs(p, exist_ok=True)
        elif t == "dir-unreadable":
            os.makedirs(p, exist_ok=True)
            dir_unreadable.append(p)
        elif t in ("file", "unreadable"):
            if not os.path.isfile(p):
                raise RuntimeError(f"{cid}: path {rp} of type {t} not a declared file")
            if t == "unreadable":
                os.chmod(p, 0)
        elif t == "fifo":
            os.mkfifo(p, 0o644)
        elif t == "sock":
            if os.path.lexists(p):
                os.unlink(p)
            s = socket.socket(socket.AF_UNIX)
            try:
                s.bind(p)
            finally:
                s.close()
        elif t == "symlink":
            parent = os.path.dirname(p.rstrip("/"))
            if parent:
                os.makedirs(parent, exist_ok=True)
            target = ent["target"].replace("{root}", case_root)
            os.symlink(target, p)
        else:
            raise ValueError(f"{cid}: unknown path type {t!r}")
    # Lock the mode-000 dirs only now that every child fixture exists.
    for d in dir_unreadable:
        os.chmod(d, 0)
    # Score every path with gio.
    if spec["db"] == "multi2":
        xdd = os.path.join(case_root, "d1") + ":" + os.path.join(case_root, "d2")
    else:
        xdd = os.path.join(case_root, "db")
    env = {"HOME": os.path.join(case_root, "h"),
           "XDG_DATA_HOME": os.path.join(case_root, "dh"),
           "XDG_DATA_DIRS": xdd}
    labels = []
    try:
        for ent in spec["paths"]:
            rp = ent["path"]
            abspath = rp if rp.startswith("/") else os.path.join(case_root, rp)
            lab = _gio_label(env, spec["attr"], spec["mode"] == "nofollow", abspath)
            if lab is None:
                lab = "ERROR"
            labels.append([lab])
    finally:
        # unlock chmod-000 entries so the tree can be removed
        for ent in spec["paths"]:
            if ent["type"] == "unreadable" and not ent["path"].startswith("/"):
                try:
                    os.chmod(os.path.join(case_root, ent["path"]), 0o644)
                except OSError:
                    pass
        # restore mode-000 dirs to 0755: 0o644 would clear the x bit and wedge cleanup
        for d in dir_unreadable:
            try:
                os.chmod(d, 0o755)
            except OSError:
                pass

    # files_schema: base64 of every regular file; "<dir>/" for empty dirs.
    files_schema: dict = {}
    for rel in sorted(files_mem):
        if files_mem[rel] is None:
            files_schema[rel] = ""
        else:
            files_schema[rel] = b64(files_mem[rel])

    if spec["db"] == "multi2":
        xdd_schema = "{root}/d1:{root}/d2"
    else:
        xdd_schema = "{root}/db"
    env_schema = {"HOME": "{root}/h", "XDG_DATA_HOME": "{root}/dh",
                  "XDG_DATA_DIRS": xdd_schema}
    return {
        "id": cid,
        "class": spec["class"],
        "env": env_schema,
        "files": files_schema,
        "mode": spec["mode"],
        "attr": spec["attr"],
        "paths": spec["paths"],
        "labels": labels,
    }


def _gio_label(env_extra: dict, attr: str, nofollow: bool, abspath: str):
    attrname = "standard::fast-content-type" if attr == "fast" else "standard::content-type"
    args = [GIO, "info", "-a", attrname]
    if nofollow:
        args.append("-n")
    args.append(abspath)
    env = {"LC_ALL": "C"}
    for k, v in env_extra.items():
        env[k] = v
    r = subprocess.run(["env", "-i"] + [f"{k}={v}" for k, v in env.items()] + args,
                       capture_output=True, text=True)
    for line in r.stdout.splitlines():
        s = line.strip()
        if s.startswith(attrname + ":"):
            return s[len(attrname) + 1:].strip()
    return ("ERROR" if r.returncode != 0 else None)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--scratch", default="/fast/scratch/hyaku/mado-r97/R97MExecCasesC1b/cases")
    ap.add_argument("--out", default=os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "filetype-cases-v2.json"))
    args = ap.parse_args()

    specs = [b() for b in BUILDERS]
    ids = [s["id"] for s in specs]
    assert len(ids) == len(set(ids)), "duplicate case ids"
    assert all(s["class"] in CLASSES for s in specs)
    assert len(specs) >= 140, f"only {len(specs)} cases"
    per_class = {k: sum(1 for s in specs if s["class"] == k) for k in CLASSES}
    for k in CLASSES:
        assert per_class[k] >= 9, f"class {k} has {per_class[k]} < 9"

    cases = [run_case(args.scratch, spec) for spec in specs]

    doc = {
        "version": VERSION,
        "oracle": "gio info -a standard::content-type (and standard::fast-content-type)",
        "gio_sha256": GIO_SHA,
        "glib2": GLIB2,
        "classes": CLASSES,
        "cases": cases,
    }
    text = json.dumps(doc, sort_keys=True, separators=(",", ":")) + "\n"
    out_path = os.path.abspath(args.out)
    if args.check:
        try:
            with open(out_path, "r", encoding="utf-8") as fh:
                stored = fh.read()
        except OSError:
            print(f"CHECK_FAIL: no stored case file at {out_path}")
            return 1
        if stored != text:
            print("CHECK_FAIL: rebuilt bytes differ from stored file")
            return 1
        print(f"CHECK_OK: {out_path} ({len(cases)} cases, sha256 {hashlib.sha256(text.encode()).hexdigest()})")
        return 0

    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as fh:
        fh.write(text)

    counts: dict = {}
    for c in cases:
        counts[c["class"]] = counts.get(c["class"], 0) + 1
    types: dict = {}
    for c in cases:
        for lab in c["labels"]:
            types[lab[0]] = types.get(lab[0], 0) + 1
    print(f"cases={len(cases)}")
    for k in CLASSES:
        print(f"  {k}: {counts.get(k, 0)}")
    print("label types:", json.dumps(types, sort_keys=True))
    print(f"wrote {out_path} sha256 {hashlib.sha256(text.encode()).hexdigest()}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
