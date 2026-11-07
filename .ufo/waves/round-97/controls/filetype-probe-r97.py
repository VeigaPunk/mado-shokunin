#!/usr/bin/env python3
"""Round-97 C1 frozen case builder: oracle-labelling probe for tools/mado-filetype.py.

Reads the frozen C1 CLI contract in this round's claims declaration (predicate
PRED-C1-r97-v1) and Shared contracts 1-3 in the seat brief: builds a case tree
in scratch, runs /usr/bin/gio on it, and writes the frozen case JSON.

Usage (from the lane root or any cwd; all paths absolute or relative to cwd):
  python3 filetype-probe-r97.py                     # build cases + label + write JSON
  python3 filetype-probe-r97.py --check             # rebuild + compare to stored JSON
  python3 filetype-probe-r97.py --scratch DIR       # scratch root (default /fast/scratch/hyaku/mado-r97/R97MExecCasesC1)
  python3 filetype-probe-r97.py --out FILE          # output JSON path

Each case carries files (base64 bytes under the case root), paths (creation
kinds), env (XDG roots) and gio labels.  The probe is re-runnable and
byte-deterministic: cases are listed in a fixed order, JSON keys sorted,
separators (',', ':').

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
import subprocess
import sys

GIO = "/usr/bin/gio"
GIO_SHA = "d216426080f847bfccdc7c735a4f349dc74f524530a19e8b1c32d04270cfc462"
GLIB2 = "2.90.1-1"
VERSION = 1

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
FOO_BYTES = b"foo data dtu\n"
BINARY = bytes(range(1, 64))


def globs2(*lines: bytes) -> bytes:
    return b"".join(line + b"\n" for line in lines)


def magic(*sections) -> bytes:
    """Each section: (type, [(value_bytes,)], ...).  Builds the MIME-Magic file
    with each matchlet at offset 0, indent 0, no mask/word/range, priority 90."""
    out = [b"MIME-Magic\x00\n"]
    for typ, values in sections:
        out.append(b"[90:" + typ.encode() + b"]\n")
        for v in values:
            out.append(b"0>0=" + len(v).to_bytes(2, "big") + v + b"\n")
    return b"".join(out)


# --------------------------------------------------------------------------
# fixture trees (db roots)
# --------------------------------------------------------------------------

HOST_MIME_FILES = ("globs2", "globs", "magic", "aliases", "subclasses",
                   "mime.cache")


def host_db():
    """A case-local copy of the host's /usr/share/mime text tables + cache.

    Read once at import from /usr/share/mime; the bytes are frozen into
    `files` so the auditor only tracks case roots and the counter derives
    db=cache the same way it does for any case-local mime.cache.  The labels
    this tree produces under gio are identical to pointing at /usr/share
    (verified case by case in the seat report).
    """
    out: dict = {}
    for name in HOST_MIME_FILES:
        with open(os.path.join("/usr/share/mime", name), "rb") as fh:
            out["d1/mime/" + name] = fh.read()
    return out

# A rich text database used by most guess classes.
DB_MAIN = {
    "d1/mime/globs2": globs2(
        b"50:image/png:*.png",
        b"50:text/plain:*.txt",
        b"50:text/html:*.html",
        b"50:app/x-foo:*.foo",
        b"50:application/x-desktop:*.desktop",
    ),
    "d1/mime/magic": magic(
        ("app/x-pngdata", [PNG_BYTES[:8]]),
        ("text/html", [b"<html>"]),
        ("application/x-desktop", [b"[Desktop Entry]"]),
    ),
}

# A second database with overlapping entries (precedence / multi-dir).
DB_OTHER = {
    "d2/mime/globs2": globs2(
        b"70:app/x-other:*.other",
        b"50:text/plain:*.txt",
        b"50:app/x-foo:*.foo",
    ),
}

# A database with two types answering *.foo (several name types).
DB_MULTI = {
    "d1/mime/globs2": globs2(
        b"50:app/x-foo:*.foo",
        b"60:app/x-foo2:*.foo",
        b"50:text/plain:*.txt",
    ),
    "d1/mime/magic": magic(
        ("app/x-pngdata", [PNG_BYTES[:8]]),
    ),
}

# A database where *.foo has a high-weight type above the PNG sniff priority.
DB_MULTI_HI = {
    "d1/mime/globs2": globs2(
        b"50:app/x-foo:*.foo",
        b"60:app/x-foo2:*.foo",
        b"50:text/plain:*.txt",
    ),
    "d1/mime/magic": magic(
        ("app/x-pngdata2", [PNG_BYTES[:8]]),
    ),
}

# Host-database cases: the host's /usr/share/mime tree (text tables + cache)
# is copied into the case root by host_db() so every case is self-contained
# (the counter derives db=cache from case files; the audit allowlist only
# tracks case roots).  Stat-branch cases whose labels do not depend on the
# database use an empty d1 (db=none) instead of a full mirror.
DB_HOST = host_db()

# --------------------------------------------------------------------------
# case builders.  Each returns (id, cls, env_dirs, files, paths, mode, attr)
# where paths is a list of dicts: {path, type, target?}
# --------------------------------------------------------------------------

def F(path: str, data: bytes):
    return (path, data)


def case_dir_01():
    return ("dir-01-plain-subdir", "dir",
            {"d1": DB_MAIN}, {"plain/": None, "plain/file": TEXT}, [
                {"path": "plain", "type": "dir"},
                {"path": "plain/", "type": "dir"},
                {"path": "plain/file", "type": "file"}], "follow", "full")


def case_dir_02():
    return ("dir-02-dir-with-name-type", "dir",
            {"d1": DB_MAIN}, {"looks.png/": None, "looks.png/a.txt": TEXT}, [
                {"path": "looks.png", "type": "dir"},
                {"path": "looks.png/a.txt", "type": "file"}], "follow", "full")


def case_dir_03():
    return ("dir-03-nested-dirs", "dir",
            {"d1": DB_MAIN}, {"a/b/c/": None}, [
                {"path": "a/b/c", "type": "dir"},
                {"path": "a/b", "type": "dir"},
                {"path": "a", "type": "dir"}], "nofollow", "full")


def case_dir_04():
    return ("dir-04-dir-nofollow", "dir",
            {"d1": DB_MAIN}, {"sub/": None}, [
                {"path": "sub", "type": "dir"}], "nofollow", "full")


def case_dir_05():
    return ("dir-05-dir-fast-attr", "dir",
            {"d1": DB_MAIN}, {"sub/": None}, [
                {"path": "sub", "type": "dir"},
                {"path": "sub/", "type": "dir"}], "follow", "fast")


def case_dir_06():
    return ("dir-06-root-is-a-dir", "dir",
            {"d1": DB_MAIN}, {"root/": None, "root/x.txt": TEXT}, [
                {"path": "root", "type": "dir"},
                {"path": "root/x.txt", "type": "file"}], "follow", "full")


def case_dir_07():
    return ("dir-07-host-db-dir", "dir",
            {"d1": {}}, {"hdir/": None, "hdir/a.txt": TEXT}, [
                {"path": "hdir", "type": "dir"},
                {"path": "hdir/a.txt", "type": "file"}], "follow", "full")


def case_dir_08():
    return ("dir-08-empty-db-dir", "dir",
            {"d1": {}}, {"edir/": None}, [
                {"path": "edir", "type": "dir"}], "follow", "full")


def case_dir_09():
    return ("dir-09-dir-with-slash-file", "dir",
            {"d1": DB_MAIN}, {"d/": None, "d/f.foo": FOO_BYTES}, [
                {"path": "d", "type": "dir"},
                {"path": "d/f.foo", "type": "file"}], "nofollow", "full")


def case_chr_01():
    return ("chr-01-dev-null", "chr",
            {"d1": DB_MAIN}, {}, [
                {"path": "/dev/null", "type": "chardev"}], "follow", "full")


def case_chr_02():
    return ("chr-02-dev-zero", "chr",
            {"d1": DB_MAIN}, {}, [
                {"path": "/dev/zero", "type": "chardev"}], "follow", "full")


def case_chr_03():
    return ("chr-03-dev-full", "chr",
            {"d1": DB_MAIN}, {}, [
                {"path": "/dev/full", "type": "chardev"}], "follow", "full")


def case_chr_04():
    return ("chr-04-dev-tty", "chr",
            {"d1": DB_MAIN}, {}, [
                {"path": "/dev/tty", "type": "chardev"}], "follow", "full")


def case_chr_05():
    return ("chr-05-dev-pts-ptmx", "chr",
            {"d1": DB_MAIN}, {}, [
                {"path": "/dev/pts/ptmx", "type": "chardev"}], "follow", "full")


def case_chr_06():
    return ("chr-06-dev-null-nofollow", "chr",
            {"d1": DB_MAIN}, {}, [
                {"path": "/dev/null", "type": "chardev"}], "nofollow", "full")


def case_chr_07():
    return ("chr-07-dev-null-fast", "chr",
            {"d1": DB_MAIN}, {}, [
                {"path": "/dev/null", "type": "chardev"}], "follow", "fast")


def case_chr_08():
    return ("chr-08-dev-zero-nofollow-fast", "chr",
            {"d1": DB_MAIN}, {}, [
                {"path": "/dev/zero", "type": "chardev"}], "nofollow", "fast")

def case_dir_10():
    return ("dir-10-host-db-subdir", "dir",
            {"d1": DB_HOST}, {"hsub/": None, "hsub/a.foo": FOO_BYTES}, [
                {"path": "hsub", "type": "dir"},
                {"path": "hsub/", "type": "dir"},
                {"path": "hsub/a.foo", "type": "file"}], "follow", "full")


def case_chr_09():
    return ("chr-09-host-db-dev-null", "chr",
            {"d1": {}}, {}, [
                {"path": "/dev/null", "type": "chardev"},
                {"path": "/dev/zero", "type": "chardev"}], "follow", "full")


def case_blk_01():
    return ("blk-01-dev-sda", "blk",
            {"d1": DB_MAIN}, {}, [
                {"path": "/dev/sda", "type": "blkdev"}], "follow", "full")


def case_blk_02():
    return ("blk-02-dev-sda1", "blk",
            {"d1": DB_MAIN}, {}, [
                {"path": "/dev/sda1", "type": "blkdev"}], "follow", "full")


def case_blk_03():
    return ("blk-03-dev-nvme0n1", "blk",
            {"d1": DB_MAIN}, {}, [
                {"path": "/dev/nvme0n1", "type": "blkdev"}], "follow", "full")


def case_blk_04():
    return ("blk-04-dev-sda-nofollow", "blk",
            {"d1": DB_MAIN}, {}, [
                {"path": "/dev/sda", "type": "blkdev"}], "nofollow", "full")


def case_blk_05():
    return ("blk-05-dev-sda-fast", "blk",
            {"d1": DB_MAIN}, {}, [
                {"path": "/dev/sda", "type": "blkdev"}], "follow", "fast")


def case_blk_06():
    return ("blk-06-dev-sda1-nofollow-fast", "blk",
            {"d1": DB_MAIN}, {}, [
                {"path": "/dev/sda1", "type": "blkdev"}], "nofollow", "fast")


def case_blk_07():
    return ("blk-07-host-db-dev-sda", "blk",
            {"d1": {}}, {}, [
                {"path": "/dev/sda", "type": "blkdev"}], "follow", "full")


def case_blk_08():
    return ("blk-08-dev-nvme1n1p1", "blk",
            {"d1": DB_MAIN}, {}, [
                {"path": "/dev/nvme1n1p1", "type": "blkdev"}], "follow", "full")


def case_blk_09():
    return ("blk-09-dev-dm0", "blk",
            {"d1": DB_MAIN}, {}, [
                {"path": "/dev/dm-0", "type": "blkdev"}], "follow", "full")


def case_fifo_01():
    return ("fifo-01-plain", "fifo",
            {"d1": DB_MAIN}, {}, [
                {"path": "pipe", "type": "fifo"}], "follow", "full")


def case_fifo_02():
    return ("fifo-02-nofollow", "fifo",
            {"d1": DB_MAIN}, {}, [
                {"path": "pipe", "type": "fifo"}], "nofollow", "full")


def case_fifo_03():
    return ("fifo-03-fast", "fifo",
            {"d1": DB_MAIN}, {}, [
                {"path": "pipe", "type": "fifo"}], "follow", "fast")


def case_fifo_04():
    return ("fifo-04-two-pipes", "fifo",
            {"d1": DB_MAIN}, {}, [
                {"path": "p1", "type": "fifo"},
                {"path": "p2", "type": "fifo"}], "follow", "full")


def case_fifo_05():
    return ("fifo-05-pipe-with-name-type", "fifo",
            {"d1": DB_MAIN}, {}, [
                {"path": "pipe.png", "type": "fifo"}], "follow", "full")


def case_fifo_06():
    return ("fifo-06-host-db-pipe", "fifo",
            {"d1": {}}, {}, [
                {"path": "pipe", "type": "fifo"}], "follow", "full")


def case_fifo_07():
    return ("fifo-07-pipe-in-subdir", "fifo",
            {"d1": DB_MAIN}, {"sub/": None}, [
                {"path": "sub", "type": "dir"},
                {"path": "sub/pipe", "type": "fifo"}], "nofollow", "full")


def case_fifo_08():
    return ("fifo-08-pipe-with-dot-name", "fifo",
            {"d1": DB_MAIN}, {}, [
                {"path": ".hidden-pipe", "type": "fifo"}], "follow", "full")


def case_fifo_09():
    return ("fifo-09-pipe-nofollow-fast", "fifo",
            {"d1": DB_MAIN}, {}, [
                {"path": "pipe", "type": "fifo"}], "nofollow", "fast")


def case_sock_01():
    return ("sock-01-plain", "sock",
            {"d1": DB_MAIN}, {}, [
                {"path": "sock", "type": "sock"}], "follow", "full")


def case_sock_02():
    return ("sock-02-nofollow", "sock",
            {"d1": DB_MAIN}, {}, [
                {"path": "sock", "type": "sock"}], "nofollow", "full")


def case_sock_03():
    return ("sock-03-fast", "sock",
            {"d1": DB_MAIN}, {}, [
                {"path": "sock", "type": "sock"}], "follow", "fast")


def case_sock_04():
    return ("sock-04-two-sockets", "sock",
            {"d1": DB_MAIN}, {}, [
                {"path": "s1", "type": "sock"},
                {"path": "s2", "type": "sock"}], "follow", "full")


def case_sock_05():
    return ("sock-05-socket-with-name-type", "sock",
            {"d1": DB_MAIN}, {}, [
                {"path": "sock.txt", "type": "sock"}], "follow", "full")


def case_sock_06():
    return ("sock-06-host-db-socket", "sock",
            {"d1": {}}, {}, [
                {"path": "sock", "type": "sock"}], "follow", "full")


def case_sock_07():
    return ("sock-07-socket-in-subdir", "sock",
            {"d1": DB_MAIN}, {"sub/": None}, [
                {"path": "sub", "type": "dir"},
                {"path": "sub/sock", "type": "sock"}], "nofollow", "full")


def case_sock_08():
    return ("sock-08-socket-with-dot-name", "sock",
            {"d1": DB_MAIN}, {}, [
                {"path": ".sock", "type": "sock"}], "follow", "full")


def case_sock_09():
    return ("sock-09-socket-nofollow-fast", "sock",
            {"d1": DB_MAIN}, {}, [
                {"path": "sock", "type": "sock"}], "nofollow", "fast")


def case_zero_01():
    return ("zero-01-empty-png", "zero",
            {"d1": DB_MAIN}, {"z.png": b""}, [
                {"path": "z.png", "type": "file"}], "follow", "full")


def case_zero_02():
    return ("zero-02-empty-unknown-name", "zero",
            {"d1": DB_MAIN}, {"bfile": b""}, [
                {"path": "bfile", "type": "file"}], "follow", "full")


def case_zero_03():
    return ("zero-03-empty-desktop-name", "zero",
            {"d1": DB_MAIN}, {"e.desktop": b""}, [
                {"path": "e.desktop", "type": "file"}], "follow", "full")


def case_zero_04():
    return ("zero-04-empty-txt", "zero",
            {"d1": DB_MAIN}, {"e.txt": b""}, [
                {"path": "e.txt", "type": "file"}], "follow", "full")


def case_zero_05():
    return ("zero-05-empty-foo", "zero",
            {"d1": DB_MAIN}, {"e.foo": b""}, [
                {"path": "e.foo", "type": "file"}], "follow", "full")


def case_zero_06():
    return ("zero-06-empty-nofollow", "zero",
            {"d1": DB_MAIN}, {"e.txt": b""}, [
                {"path": "e.txt", "type": "file"}], "nofollow", "full")


def case_zero_07():
    return ("zero-07-empty-fast", "zero",
            {"d1": DB_MAIN}, {"e.txt": b""}, [
                {"path": "e.txt", "type": "file"}], "follow", "fast")


def case_zero_08():
    return ("zero-08-two-empty-files", "zero",
            {"d1": DB_MAIN}, {"a.png": b"", "b": b""}, [
                {"path": "a.png", "type": "file"},
                {"path": "b", "type": "file"}], "follow", "full")


def case_zero_09():
    return ("zero-09-empty-host-db", "zero",
            {"d1": {}}, {"z.bin": b"", "z.png": b""}, [
                {"path": "z.bin", "type": "file"},
                {"path": "z.png", "type": "file"}], "follow", "full")


def case_empty_01():
    return ("empty-01-text-unknown-name", "empty",
            {"d1": DB_MAIN}, {"note": TEXT}, [
                {"path": "note", "type": "file"}], "follow", "full")


def case_empty_02():
    return ("empty-02-text-txt-name", "empty",
            {"d1": DB_MAIN}, {"note.txt": TEXT}, [
                {"path": "note.txt", "type": "file"}], "follow", "full")


def case_empty_03():
    return ("empty-03-binary-unknown-name", "empty",
            {"d1": DB_MAIN}, {"blob": BINARY}, [
                {"path": "blob", "type": "file"}], "follow", "full")


def case_empty_04():
    return ("empty-04-text-foo-name", "empty",
            {"d1": DB_MAIN}, {"x.foo": TEXT}, [
                {"path": "x.foo", "type": "file"}], "follow", "full")


def case_empty_05():
    return ("empty-05-png-unknown-name", "empty",
            {"d1": DB_MAIN}, {"pic": PNG_BYTES}, [
                {"path": "pic", "type": "file"}], "follow", "full")


def case_empty_06():
    return ("empty-06-text-nofollow", "empty",
            {"d1": DB_MAIN}, {"note": TEXT}, [
                {"path": "note", "type": "file"}], "nofollow", "full")


def case_empty_07():
    return ("empty-07-text-fast", "empty",
            {"d1": DB_MAIN}, {"note": TEXT}, [
                {"path": "note", "type": "file"}], "follow", "fast")


def case_empty_08():
    return ("empty-08-empty-db-unknown", "empty",
            {"d1": {}}, {"note": TEXT, "blob": BINARY}, [
                {"path": "note", "type": "file"},
                {"path": "blob", "type": "file"}], "follow", "full")


def case_empty_09():
    return ("empty-09-host-db-unknown", "empty",
            {"d1": DB_HOST}, {"note": TEXT, "blob": BINARY}, [
                {"path": "note", "type": "file"},
                {"path": "blob", "type": "file"}], "follow", "full")


def case_sym_01():
    return ("sym-01-link-to-file-follow", "sym",
            {"d1": DB_MAIN}, {"real.txt": TEXT}, [
                {"path": "real.txt", "type": "file"},
                {"path": "link", "type": "symlink", "target": "real.txt"}], "follow", "full")


def case_sym_02():
    return ("sym-02-link-to-file-nofollow", "sym",
            {"d1": DB_MAIN}, {"real.txt": TEXT}, [
                {"path": "real.txt", "type": "file"},
                {"path": "link", "type": "symlink", "target": "real.txt"}], "nofollow", "full")


def case_sym_03():
    return ("sym-03-link-to-dir-follow", "sym",
            {"d1": DB_MAIN}, {"sub/": None, "sub/a.txt": TEXT}, [
                {"path": "sub", "type": "dir"},
                {"path": "sub/a.txt", "type": "file"},
                {"path": "dlink", "type": "symlink", "target": "sub"}], "follow", "full")


def case_sym_04():
    return ("sym-04-link-to-dir-nofollow", "sym",
            {"d1": DB_MAIN}, {"sub/": None, "sub/a.txt": TEXT}, [
                {"path": "sub", "type": "dir"},
                {"path": "sub/a.txt", "type": "file"},
                {"path": "dlink", "type": "symlink", "target": "sub"}], "nofollow", "full")


def case_sym_05():
    return ("sym-05-link-fast", "sym",
            {"d1": DB_MAIN}, {"real.txt": TEXT}, [
                {"path": "real.txt", "type": "file"},
                {"path": "link", "type": "symlink", "target": "real.txt"}], "follow", "fast")


def case_sym_06():
    return ("sym-06-two-links", "sym",
            {"d1": DB_MAIN}, {"real.txt": TEXT, "real2.foo": FOO_BYTES}, [
                {"path": "real.txt", "type": "file"},
                {"path": "real2.foo", "type": "file"},
                {"path": "link1", "type": "symlink", "target": "real.txt"},
                {"path": "link2", "type": "symlink", "target": "real2.foo"}], "follow", "full")


def case_sym_07():
    return ("sym-07-link-with-name-type", "sym",
            {"d1": DB_MAIN}, {"real.bin": BINARY}, [
                {"path": "real.bin", "type": "file"},
                {"path": "link.png", "type": "symlink", "target": "real.bin"}], "follow", "full")


def case_sym_08():
    return ("sym-08-host-db-links", "sym",
            {"d1": {}}, {"real.txt": TEXT}, [
                {"path": "real.txt", "type": "file"},
                {"path": "link", "type": "symlink", "target": "real.txt"}], "follow", "full")


def case_sym_09():
    return ("sym-09-link-in-subdir", "sym",
            {"d1": DB_MAIN}, {"sub/real.txt": TEXT}, [
                {"path": "sub", "type": "dir"},
                {"path": "sub/real.txt", "type": "file"},
                {"path": "sub/link", "type": "symlink", "target": "real.txt"}], "nofollow", "full")


def case_brok_01():
    return ("brok-01-dangling-follow", "brok",
            {"d1": DB_MAIN}, {}, [
                {"path": "dang", "type": "symlink", "target": "nope"}], "follow", "full")


def case_brok_02():
    return ("brok-02-dangling-nofollow", "brok",
            {"d1": DB_MAIN}, {}, [
                {"path": "dang", "type": "symlink", "target": "nope"}], "nofollow", "full")


def case_brok_03():
    return ("brok-03-loop-follow", "brok",
            {"d1": DB_MAIN}, {}, [
                {"path": "l1", "type": "symlink", "target": "l2"},
                {"path": "l2", "type": "symlink", "target": "l1"}], "follow", "full")


def case_brok_04():
    return ("brok-04-loop-nofollow", "brok",
            {"d1": DB_MAIN}, {}, [
                {"path": "l1", "type": "symlink", "target": "l2"},
                {"path": "l2", "type": "symlink", "target": "l1"}], "nofollow", "full")


def case_brok_05():
    return ("brok-05-dangling-fast", "brok",
            {"d1": DB_MAIN}, {}, [
                {"path": "dang", "type": "symlink", "target": "nope"}], "follow", "fast")


def case_brok_06():
    return ("brok-06-dangling-in-subdir", "brok",
            {"d1": DB_MAIN}, {"sub/": None}, [
                {"path": "sub", "type": "dir"},
                {"path": "sub/dang", "type": "symlink", "target": "../nope"}], "follow", "full")


def case_brok_07():
    return ("brok-07-host-db-dangling", "brok",
            {"d1": {}}, {}, [
                {"path": "dang", "type": "symlink", "target": "nope"}], "follow", "full")


def case_brok_08():
    return ("brok-08-dangling-with-name-type", "brok",
            {"d1": DB_MAIN}, {}, [
                {"path": "dang.png", "type": "symlink", "target": "nope"}], "follow", "full")


def case_brok_09():
    return ("brok-09-empty-db-dangling", "brok",
            {"d1": {}}, {}, [
                {"path": "dang", "type": "symlink", "target": "nope"}], "follow", "full")


def case_nofollow_01():
    # nofollow over sym fixtures
    return ("nofollow-01-link-nofollow", "nofollow",
            {"d1": DB_MAIN}, {"real.txt": TEXT}, [
                {"path": "real.txt", "type": "file"},
                {"path": "link", "type": "symlink", "target": "real.txt"}], "nofollow", "full")


def case_nofollow_02():
    # nofollow over brok fixtures
    return ("nofollow-02-dangling-nofollow", "nofollow",
            {"d1": DB_MAIN}, {}, [
                {"path": "dang", "type": "symlink", "target": "nope"}], "nofollow", "full")


def case_nofollow_03():
    # nofollow over dir target
    return ("nofollow-03-dirlink-nofollow", "nofollow",
            {"d1": DB_MAIN}, {"sub/": None}, [
                {"path": "sub", "type": "dir"},
                {"path": "dlink", "type": "symlink", "target": "sub"}], "nofollow", "full")


def case_nofollow_04():
    # nofollow over loop
    return ("nofollow-04-loop-nofollow", "nofollow",
            {"d1": DB_MAIN}, {}, [
                {"path": "l1", "type": "symlink", "target": "l2"},
                {"path": "l2", "type": "symlink", "target": "l1"}], "nofollow", "full")


def case_nofollow_05():
    # nofollow over a regular file + fifo + sock
    return ("nofollow-05-mixed-nofollow", "nofollow",
            {"d1": DB_MAIN}, {"a.txt": TEXT}, [
                {"path": "a.txt", "type": "file"},
                {"path": "pipe", "type": "fifo"},
                {"path": "sock", "type": "sock"}], "nofollow", "full")


def case_nofollow_06():
    # nofollow over an empty file
    return ("nofollow-06-empty-nofollow", "nofollow",
            {"d1": DB_MAIN}, {"e.txt": b""}, [
                {"path": "e.txt", "type": "file"}], "nofollow", "full")


def case_nofollow_07():
    # nofollow over a directory
    return ("nofollow-07-dir-nofollow", "nofollow",
            {"d1": DB_MAIN}, {"sub/": None}, [
                {"path": "sub", "type": "dir"}], "nofollow", "full")


def case_nofollow_08():
    # nofollow over chardev + blkdev
    return ("nofollow-08-devices-nofollow", "nofollow",
            {"d1": DB_MAIN}, {}, [
                {"path": "/dev/null", "type": "chardev"},
                {"path": "/dev/sda", "type": "blkdev"}], "nofollow", "full")


def case_nofollow_09():
    # nofollow over sym + brok + file
    return ("nofollow-09-three-way-nofollow", "nofollow",
            {"d1": DB_MAIN}, {"real.txt": TEXT}, [
                {"path": "real.txt", "type": "file"},
                {"path": "link", "type": "symlink", "target": "real.txt"},
                {"path": "dang", "type": "symlink", "target": "nope"}], "nofollow", "full")


def case_follow_01():
    return ("follow-01-link-follow", "follow",
            {"d1": DB_MAIN}, {"real.txt": TEXT}, [
                {"path": "real.txt", "type": "file"},
                {"path": "link", "type": "symlink", "target": "real.txt"}], "follow", "full")


def case_follow_02():
    return ("follow-02-dangling-follow", "follow",
            {"d1": DB_MAIN}, {}, [
                {"path": "dang", "type": "symlink", "target": "nope"}], "follow", "full")


def case_follow_03():
    return ("follow-03-dirlink-follow", "follow",
            {"d1": DB_MAIN}, {"sub/": None}, [
                {"path": "sub", "type": "dir"},
                {"path": "dlink", "type": "symlink", "target": "sub"}], "follow", "full")


def case_follow_04():
    return ("follow-04-loop-follow", "follow",
            {"d1": DB_MAIN}, {}, [
                {"path": "l1", "type": "symlink", "target": "l2"},
                {"path": "l2", "type": "symlink", "target": "l1"}], "follow", "full")


def case_follow_05():
    return ("follow-05-mixed-follow", "follow",
            {"d1": DB_MAIN}, {"a.txt": TEXT}, [
                {"path": "a.txt", "type": "file"},
                {"path": "pipe", "type": "fifo"},
                {"path": "sock", "type": "sock"}], "follow", "full")


def case_follow_06():
    return ("follow-06-empty-follow", "follow",
            {"d1": DB_MAIN}, {"e.txt": b""}, [
                {"path": "e.txt", "type": "file"}], "follow", "full")


def case_follow_07():
    return ("follow-07-dir-follow", "follow",
            {"d1": DB_MAIN}, {"sub/": None}, [
                {"path": "sub", "type": "dir"}], "follow", "full")


def case_follow_08():
    return ("follow-08-devices-follow", "follow",
            {"d1": DB_MAIN}, {}, [
                {"path": "/dev/null", "type": "chardev"},
                {"path": "/dev/sda", "type": "blkdev"}], "follow", "full")


def case_follow_09():
    return ("follow-09-three-way-follow", "follow",
            {"d1": DB_MAIN}, {"real.txt": TEXT}, [
                {"path": "real.txt", "type": "file"},
                {"path": "link", "type": "symlink", "target": "real.txt"},
                {"path": "dang", "type": "symlink", "target": "nope"}], "follow", "full")


def case_certain_01():
    return ("certain-01-text-in-png", "certain",
            {"d1": DB_MAIN}, {"a.png": TEXT}, [
                {"path": "a.png", "type": "file"}], "follow", "full")


def case_certain_02():
    return ("certain-02-png-in-txt", "certain",
            {"d1": DB_MAIN}, {"a.txt": PNG_BYTES}, [
                {"path": "a.txt", "type": "file"}], "follow", "full")


def case_certain_03():
    return ("certain-03-html-in-txt", "certain",
            {"d1": DB_MAIN}, {"a.txt": HTML_BYTES}, [
                {"path": "a.txt", "type": "file"}], "follow", "full")


def case_certain_04():
    return ("certain-04-foo-content-png", "certain",
            {"d1": DB_MAIN}, {"a.foo": PNG_BYTES}, [
                {"path": "a.foo", "type": "file"}], "follow", "full")


def case_certain_05():
    return ("certain-05-text-in-png-nofollow", "certain",
            {"d1": DB_MAIN}, {"a.png": TEXT}, [
                {"path": "a.png", "type": "file"}], "nofollow", "full")


def case_certain_06():
    return ("certain-06-certain-fast", "certain",
            {"d1": DB_MAIN}, {"a.png": TEXT}, [
                {"path": "a.png", "type": "file"}], "follow", "fast")


def case_certain_07():
    return ("certain-07-certain-desktop-bytes", "certain",
            {"d1": DB_MAIN}, {"a.desktop": TEXT}, [
                {"path": "a.desktop", "type": "file"}], "follow", "full")


def case_certain_08():
    return ("certain-08-certain-two-files", "certain",
            {"d1": DB_MAIN}, {"a.png": TEXT, "b.txt": PNG_BYTES}, [
                {"path": "a.png", "type": "file"},
                {"path": "b.txt", "type": "file"}], "follow", "full")


def case_certain_09():
    return ("certain-09-certain-host-db", "certain",
            {"d1": DB_HOST}, {"a.png": TEXT}, [
                {"path": "a.png", "type": "file"}], "follow", "full")


def case_uncertain_01():
    return ("uncertain-01-png-in-readme", "uncertain",
            {"d1": DB_MAIN}, {"README": PNG_BYTES}, [
                {"path": "README", "type": "file"}], "follow", "full")


def case_uncertain_02():
    return ("uncertain-02-text-in-blobbin", "uncertain",
            {"d1": DB_MAIN}, {"blob.bin": TEXT}, [
                {"path": "blob.bin", "type": "file"}], "follow", "full")


def case_uncertain_03():
    return ("uncertain-03-html-in-pagehtml", "uncertain",
            {"d1": DB_MAIN}, {"page.html": HTML_BYTES}, [
                {"path": "page.html", "type": "file"}], "follow", "full")


def case_uncertain_04():
    return ("uncertain-04-binary-unknown", "uncertain",
            {"d1": DB_MAIN}, {"blob": BINARY}, [
                {"path": "blob", "type": "file"}], "follow", "full")


def case_uncertain_05():
    return ("uncertain-05-multi-foo-text", "uncertain",
            {"d1": DB_MULTI}, {"m.foo": TEXT}, [
                {"path": "m.foo", "type": "file"}], "follow", "full")


def case_uncertain_06():
    return ("uncertain-06-multi-foo-png-hi", "uncertain",
            {"d1": DB_MULTI}, {"m.foo": PNG_BYTES}, [
                {"path": "m.foo", "type": "file"}], "follow", "full")


def case_uncertain_07():
    return ("uncertain-07-multi-foo-png-lo", "uncertain",
            {"d1": DB_MULTI_HI}, {"m.foo": PNG_BYTES}, [
                {"path": "m.foo", "type": "file"}], "follow", "full")


def case_uncertain_08():
    return ("uncertain-08-desktop-no-name-type", "uncertain",
            {"d1": DB_MAIN}, {"appfile": DESKTOP_BYTES}, [
                {"path": "appfile", "type": "file"}], "follow", "full")


def case_uncertain_09():
    return ("uncertain-09-uncertain-host-db", "uncertain",
            {"d1": DB_HOST}, {"mystery": PNG_BYTES, "page.html": HTML_BYTES}, [
                {"path": "mystery", "type": "file"},
                {"path": "page.html", "type": "file"}], "follow", "full")


def case_fast_01():
    return ("fast-01-png-readme", "fast",
            {"d1": DB_MAIN}, {"README": PNG_BYTES}, [
                {"path": "README", "type": "file"}], "follow", "fast")


def case_fast_02():
    return ("fast-02-text-blobbin", "fast",
            {"d1": DB_MAIN}, {"blob.bin": TEXT}, [
                {"path": "blob.bin", "type": "file"}], "follow", "fast")


def case_fast_03():
    return ("fast-03-html-page", "fast",
            {"d1": DB_MAIN}, {"page.html": HTML_BYTES}, [
                {"path": "page.html", "type": "file"}], "follow", "fast")


def case_fast_04():
    return ("fast-04-binary-unknown", "fast",
            {"d1": DB_MAIN}, {"blob": BINARY}, [
                {"path": "blob", "type": "file"}], "follow", "fast")


def case_fast_05():
    return ("fast-05-multi-foo", "fast",
            {"d1": DB_MULTI}, {"m.foo": PNG_BYTES}, [
                {"path": "m.foo", "type": "file"}], "follow", "fast")


def case_fast_06():
    return ("fast-06-desktop-no-name-type", "fast",
            {"d1": DB_MAIN}, {"appfile": DESKTOP_BYTES}, [
                {"path": "appfile", "type": "file"}], "follow", "fast")


def case_fast_07():
    return ("fast-07-certain-fast", "fast",
            {"d1": DB_MAIN}, {"a.png": TEXT}, [
                {"path": "a.png", "type": "file"}], "follow", "fast")


def case_fast_08():
    return ("fast-08-zero-fast", "fast",
            {"d1": DB_MAIN}, {"z.png": b""}, [
                {"path": "z.png", "type": "file"}], "follow", "fast")


def case_fast_09():
    return ("fast-09-fast-host-db", "fast",
            {"d1": DB_HOST}, {"mystery": PNG_BYTES}, [
                {"path": "mystery", "type": "file"}], "follow", "fast")

def case_uncertain_10():
    return ("uncertain-10-png-in-foo-multi-hi", "uncertain",
            {"d1": DB_MULTI_HI}, {"m.foo": PNG_BYTES}, [
                {"path": "m.foo", "type": "file"}], "nofollow", "full")

def case_fast_10():
    return ("fast-10-fast-multi-hi-png", "fast",
            {"d1": DB_MULTI_HI}, {"m.foo": PNG_BYTES}, [
                {"path": "m.foo", "type": "file"}], "follow", "fast")


def case_certain_10():
    return ("certain-10-empty-db-certain", "certain",
            {"d1": {}}, {"a.png": TEXT}, [
                {"path": "a.png", "type": "file"}], "follow", "full")

def case_readerr_01():
    return ("readerr-01-000-uncertain-png", "readerr",
            {"d1": DB_MAIN}, {"secretdata": PNG_BYTES}, [
                {"path": "secretdata", "type": "unreadable"}], "follow", "full")

def case_readerr_10():
    return ("readerr-10-readable-png-control", "readerr",
            {"d1": DB_HOST}, {"mystery": PNG_BYTES}, [
                {"path": "mystery", "type": "file"}], "follow", "full")


def case_readerr_02():
    return ("readerr-02-000-text-uncertain", "readerr",
            {"d1": DB_MAIN}, {"secretdata": TEXT}, [
                {"path": "secretdata", "type": "unreadable"}], "follow", "full")


def case_readerr_03():
    return ("readerr-03-000-certain-name", "readerr",
            {"d1": DB_MAIN}, {"secret.txt": TEXT}, [
                {"path": "secret.txt", "type": "unreadable"}], "follow", "full")


def case_readerr_04():
    return ("readerr-04-000-multi-foo", "readerr",
            {"d1": DB_MULTI}, {"m.foo": PNG_BYTES}, [
                {"path": "m.foo", "type": "unreadable"}], "follow", "full")


def case_readerr_05():
    return ("readerr-05-locked-dir-iner", "readerr",
            {"d1": DB_MAIN}, {"locked/secretdata": PNG_BYTES}, [
                {"path": "locked/secretdata", "type": "file"}], "follow", "full")


def case_readerr_06():
    return ("readerr-06-readable-control", "readerr",
            {"d1": DB_MAIN}, {"mystery": PNG_BYTES}, [
                {"path": "mystery", "type": "file"}], "follow", "full")


def case_readerr_07():
    return ("readerr-07-000-nofollow", "readerr",
            {"d1": DB_MAIN}, {"secretdata": PNG_BYTES}, [
                {"path": "secretdata", "type": "unreadable"}], "nofollow", "full")


def case_readerr_08():
    return ("readerr-08-000-fast", "readerr",
            {"d1": DB_MAIN}, {"secretdata": PNG_BYTES}, [
                {"path": "secretdata", "type": "unreadable"}], "follow", "fast")


def case_readerr_09():
    return ("readerr-09-secret-two-paths", "readerr",
            {"d1": DB_MAIN}, {"s1": PNG_BYTES, "s2.txt": TEXT}, [
                {"path": "s1", "type": "unreadable"},
                {"path": "s2.txt", "type": "unreadable"}], "follow", "full")


BUILDERS = [
    case_dir_01, case_dir_02, case_dir_03, case_dir_04, case_dir_05,
    case_dir_06, case_dir_07, case_dir_08, case_dir_09, case_dir_10,
    case_chr_01, case_chr_02, case_chr_03, case_chr_04, case_chr_05,
    case_chr_06, case_chr_07, case_chr_08, case_chr_09,
    case_blk_01, case_blk_02, case_blk_03, case_blk_04, case_blk_05,
    case_blk_06, case_blk_07, case_blk_08, case_blk_09,
    case_fifo_01, case_fifo_02, case_fifo_03, case_fifo_04, case_fifo_05,
    case_fifo_06, case_fifo_07, case_fifo_08, case_fifo_09,
    case_sock_01, case_sock_02, case_sock_03, case_sock_04, case_sock_05,
    case_sock_06, case_sock_07, case_sock_08, case_sock_09,
    case_zero_01, case_zero_02, case_zero_03, case_zero_04, case_zero_05,
    case_zero_06, case_zero_07, case_zero_08, case_zero_09,
    case_empty_01, case_empty_02, case_empty_03, case_empty_04, case_empty_05,
    case_empty_06, case_empty_07, case_empty_08, case_empty_09,
    case_sym_01, case_sym_02, case_sym_03, case_sym_04, case_sym_05,
    case_sym_06, case_sym_07, case_sym_08, case_sym_09,
    case_brok_01, case_brok_02, case_brok_03, case_brok_04, case_brok_05,
    case_brok_06, case_brok_07, case_brok_08, case_brok_09,
    case_nofollow_01, case_nofollow_02, case_nofollow_03, case_nofollow_04,
    case_nofollow_05, case_nofollow_06, case_nofollow_07, case_nofollow_08,
    case_nofollow_09,
    case_follow_01, case_follow_02, case_follow_03, case_follow_04,
    case_follow_05, case_follow_06, case_follow_07, case_follow_08,
    case_follow_09,
    case_certain_01, case_certain_02, case_certain_03, case_certain_04,
    case_certain_05, case_certain_06, case_certain_07, case_certain_08,
    case_certain_09, case_certain_10,
    case_uncertain_01, case_uncertain_02, case_uncertain_03,
    case_uncertain_04, case_uncertain_05, case_uncertain_06,
    case_uncertain_07, case_uncertain_08, case_uncertain_09, case_uncertain_10,
    case_fast_01, case_fast_02, case_fast_03, case_fast_04, case_fast_05,
    case_fast_06, case_fast_07, case_fast_08, case_fast_09, case_fast_10,
    case_readerr_01, case_readerr_02, case_readerr_03, case_readerr_04,
    case_readerr_05, case_readerr_06, case_readerr_07, case_readerr_08,
    case_readerr_09, case_readerr_10,
]


# --------------------------------------------------------------------------
# verifier / builder
# --------------------------------------------------------------------------

def build_tree(root: str, tree: dict, files_meta: dict) -> None:
    for rel, data in sorted(tree.items()):
        ap = os.path.join(root, rel)
        if data is None:
            os.makedirs(ap, exist_ok=True)
        else:
            os.makedirs(os.path.dirname(ap), exist_ok=True)
            with open(ap, "wb") as fh:
                fh.write(data)


def create_paths(root: str, paths: list, sockets: list) -> None:
    for p in paths:
        kind = p["type"]
        rel = p["path"]
        if rel.startswith("/"):
            # absolute host path: chardev/blkdev must already exist.
            assert os.path.exists(rel), f"host path missing: {rel}"
            continue
        ap = os.path.join(root, rel)
        if kind == "dir":
            os.makedirs(ap, exist_ok=True)
        elif kind == "fifo":
            os.mkfifo(ap)
        elif kind == "sock":
            s = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
            s.bind(ap)
            sockets.append(s)
        elif kind == "symlink":
            os.makedirs(os.path.dirname(ap), exist_ok=True)
            os.symlink(p["target"], ap)
        elif kind == "unreadable":
            # The file bytes were already written by build_tree; lock it.
            os.chmod(ap, 0)
        elif kind in ("file", "chardev", "blkdev"):
            pass
        else:
            raise ValueError(f"unknown path type {kind}")


def gio_label(env: dict, attr: str, nofollow: bool, abspath: str):
    args = [GIO, "info", "-a",
            "standard::fast-content-type" if attr == "fast" else "standard::content-type"]
    if nofollow:
        args.append("-n")
    args.append(abspath)
    env_args = ["env", "-i", "LC_ALL=C"]
    for k, v in env.items():
        env_args.append(f"{k}={v}")
    r = subprocess.run(env_args + args, capture_output=True, text=True)
    for line in (r.stdout + r.stderr).splitlines():
        stripped = line.strip()
        for key in ("standard::fast-content-type", "standard::content-type"):
            if stripped.startswith(key + ":"):
                return stripped[len(key) + 1:].strip()
    return ("ERROR" if r.returncode != 0 else None)


def run_case(scratch_root: str, spec) -> dict:
    cid, cls, dbroots, files_extra, paths, mode, attr = spec
    case_root = os.path.join(scratch_root, "cases", cid)
    if os.path.exists(case_root):
        shutil.rmtree(case_root)
    os.makedirs(case_root)
    h = os.path.join(case_root, "h")
    os.makedirs(h)

    # db roots
    tree: dict = {}
    for name, db in dbroots.items():
        tree[name] = None
        for rel, data in db.items():
            tree[rel] = data
    # non-mime files
    for rel, data in files_extra.items():
        if data is None:
            tree[rel] = None
        else:
            tree[rel] = data

    build_tree(case_root, tree, files_extra)
    # create the non-file entries themselves
    sockets: list = []
    create_paths(case_root, paths, sockets)
    # unlock everything at the end, regardless
    try:
        env = {"HOME": h}
        dirs = [os.path.join(case_root, name) for name in dbroots.keys()]
        env["XDG_DATA_DIRS"] = ":".join(dirs)
        labels = []
        for p in paths:
            rel = p["path"]
            if rel.startswith("/"):
                abspath = rel
            else:
                abspath = os.path.join(case_root, rel)
            lab = gio_label(env, attr, mode == "nofollow", abspath)
            if lab is None:
                raise RuntimeError(f"gio returned no label for {abspath}: {p}")
            labels.append([lab])
    finally:
        for s in sockets:
            s.close()
        # unlock any chmod-000 entries
        for p in paths:
            if p["type"] == "unreadable" and not p["path"].startswith("/"):
                ap = os.path.join(case_root, p["path"])
                try:
                    os.chmod(ap, 0o644)
                except OSError:
                    pass
        for rel in files_extra:
            if rel.endswith("/"):
                continue
            ap = os.path.join(case_root, rel)
            try:
                os.chmod(ap, 0o644)
            except OSError:
                pass

    # env dict in schema form
    dirs = [n for n in dbroots.keys()]
    env_schema = {"HOME": "{root}/h", "XDG_DATA_HOME": None,
                  "XDG_DATA_DIRS": ":".join("{root}/" + d for d in dirs)}

    files_schema: dict = {}
    for rel in sorted(tree.keys()):
        if tree[rel] is None:
            continue
        ap = os.path.join(case_root, rel)
        with open(ap, "rb") as fh:
            files_schema[rel] = b64(fh.read())

    return {
        "id": cid,
        "class": cls,
        "env": env_schema,
        "files": files_schema,
        "mode": mode,
        "attr": attr,
        "paths": paths,
        "labels": labels,
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--scratch", default="/fast/scratch/hyaku/mado-r97/R97MExecCasesC1")
    ap.add_argument("--out", default=os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "..", "controls",
        "filetype-cases-r97.json"))
    args = ap.parse_args()

    specs = [b() for b in BUILDERS]
    ids = [s[0] for s in specs]
    assert len(ids) == len(set(ids)), "duplicate case ids"
    assert set(s[1] for s in specs) <= set(CLASSES)
    assert len(specs) >= 140, f"only {len(specs)} cases"

    cases = []
    for spec in specs:
        cases.append(run_case(args.scratch, spec))

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
