#!/usr/bin/env python3
"""filetype-fresh-r97 - seeded fresh case generator for the round-97 C1 path-content-type wave.

  python3 -I filetype-fresh-r97.py --seed HEX --dir D [--out FILE] [--count N]

Writes N fresh case roots under --dir (one "case-NNN" root per case, deleted first if
present) and prints one JSON line per case to stdout AND to --out: a dict with
id, class, env, files, mode, attr, paths, labels.

Every label is measured at generation time by running the installed oracle on the
BUILT root:

  env -i LC_ALL=C HOME=<root>/h XDG_DATA_HOME=<root>/dh XDG_DATA_DIRS=<root>/db \\
      /usr/bin/gio info -a standard::<full|fast-content-type> [-n] <path>

Labels are never copied from a frozen file.  A path whose oracle run exits nonzero
without an attribute line (missing target, symlink loop, ENOTDIR, EACCES on stat) is
DROPPED from the case with a counted note, so every shipped case is scoreable
end-to-end; the ERROR/refusal leg is covered by the frozen case file and the host
list instead.

Fixture coverage per class: dir, chr, blk, fifo, sock, zero (size-0 with typed
names), empty (no-type names, text bytes), sym (live + dir symlinks), brok (broken
+ loop), nofollow (symlink-to-{file,dir,broken,fifo} measured with -n), follow
(same family measured following), certain (one name type: never sniffed),
uncertain (no/many name types: the sniff decides), fast (attr=fast on typed and
untyped names), readerr (mode 000: open denied, name-only answer kept).
Device fixtures (chr/blk) are absolute host paths declared in the case's paths.
Database modes cycle per case: text (the eight host text files copied into
<root>/db/mime), cache (host mime.cache + globs + globs2 copied into <root>/db/mime),
none (<root>/db empty).  Both modes and both attrs are additionally randomized
across the non-dedicated classes.

Deterministic for a given seed on the same host.  stdlib only; ASCII output.
"""
from __future__ import annotations

import argparse
import base64
import hashlib
import json
import os
import random
import shutil
import socket
import subprocess
import sys
import tempfile

GIO = "/usr/bin/gio"
GLIB = "2.90.1-1"
SHARED_MIME_INFO = "2.5.1-2"
CLASSES = ["dir", "chr", "blk", "fifo", "sock", "zero", "empty", "sym", "brok",
           "nofollow", "follow", "certain", "uncertain", "fast", "readerr"]
DB_CYCLE = ["text", "cache", "none"]
TEXT_FILES = ["magic", "globs", "globs2", "aliases", "subclasses", "icons",
              "generic-icons", "XMLnamespaces"]
CACHE_FILES = ["mime.cache", "globs", "globs2"]
HOST_MIME = "/usr/share/mime"
GIO_TIMEOUT = 15.0

PNG = b"\x89PNG\r\n\x1a\n" + b"\x00\x00\x00\x0dIHDR" + b"\x00" * 8
PDF = b"%PDF-1.4\n%\xe2\xe3\xcf\xd3\n" + b"\x00" * 8
ZIP = b"PK\x03\x04\x14\x00\x00\x00" + b"\x00" * 8
ELF = b"\x7fELF\x02\x01\x01\x00" + b"\x00" * 8
OGG = b"OggS\x00\x02\x00\x00" + b"\x00" * 8
TXT = b"hello world\nsecond line\n"
DESKTOP = b"[Desktop Entry]\nType=Application\nName=T\nExec=/bin/true\n"
SH = b"#!/bin/sh\necho hi\n"


def sha256_file(path):
    with open(path, "rb") as fh:
        return hashlib.sha256(fh.read()).hexdigest()


def gio_label(root, env, rel, attr, nofollow):
    """Run the oracle on one built path; return its type string."""
    path = rel if rel.startswith("/") else os.path.join(root, rel)
    e = {"LC_ALL": "C", "HOME": env["HOME"].replace("{root}", root)}
    if env.get("XDG_DATA_HOME") is not None:
        e["XDG_DATA_HOME"] = env["XDG_DATA_HOME"].replace("{root}", root)
    else:
        e.pop("XDG_DATA_HOME", None)
    e["XDG_DATA_DIRS"] = env["XDG_DATA_DIRS"].replace("{root}", root)
    gio_attr = "content-type" if attr == "full" else "fast-content-type"
    args = [GIO, "info", "-a", "standard::%s" % gio_attr]
    if nofollow:
        args.append("-n")
    args.append(path)
    try:
        proc = subprocess.run(args, env=e, stdout=subprocess.PIPE,
                              stderr=subprocess.PIPE, timeout=GIO_TIMEOUT)
    except subprocess.TimeoutExpired:
        return "ERROR"
    out = proc.stdout.decode("utf-8", "replace")
    value = None
    key = "standard::%s:" % gio_attr
    for line in out.splitlines():
        s = line.strip()
        if s.startswith(key):
            value = s[len(key):].strip()
            break
    if value is None:
        return "ERROR"
    return value


def b64(path):
    with open(path, "rb") as fh:
        return base64.b64encode(fh.read()).decode("ascii")


class Gen:
    def __init__(self, rng):
        self.rng = rng

    def build_db_files(self, root, db_kind):
        """Return the case's files dict for the db tree; build the dirs."""
        db = os.path.join(root, "db")
        os.makedirs(db, exist_ok=True)
        files = {}
        if db_kind == "text":
            os.makedirs(os.path.join(db, "mime"), exist_ok=True)
            for name in TEXT_FILES:
                src = os.path.join(HOST_MIME, name)
                shutil.copy2(src, os.path.join(db, "mime", name))
                files["db/mime/" + name] = b64(src)
        elif db_kind == "cache":
            os.makedirs(os.path.join(db, "mime"), exist_ok=True)
            for name in CACHE_FILES:
                src = os.path.join(HOST_MIME, name)
                shutil.copy2(src, os.path.join(db, "mime", name))
                files["db/mime/" + name] = b64(src)
        # none: an empty db dir; no mime/ subdir at all
        return files

    def case(self, cls, root, idx, occurrence=0):
        rng = self.rng
        first = occurrence == 0
        if cls == "nofollow":
            mode = "nofollow"
        elif cls == "follow":
            mode = "follow"
        else:
            mode = "nofollow" if rng.random() < 0.25 else "follow"
        if cls == "fast":
            attr = "fast"
        else:
            attr = "fast" if rng.random() < 0.2 else "full"
        if cls == "uncertain" and occurrence < 4:
            # canonical combos so the sniff legs are guaranteed:
            # 0 = text DB + full + follow (a magic hit must exist);
            # 1 = cache DB + full + follow; 2 = none DB + full + follow;
            # 3 = text DB + fast (the fast gate: never sniffs);
            # later occurrences fall through to the randomized cycle.
            db_kind, attr, mode = [("text", "full", "follow"),
                                   ("cache", "full", "follow"),
                                   ("none", "full", "follow"),
                                   ("text", "fast", "follow")][occurrence]
        elif first:
            # canonical combos so the key branches are guaranteed:
            # brok first = nofollow (a symlink loop is scoreable only there);
            # certain first = none DB (a name win needs no database);
            # every other class first = text DB + full attr.
            if cls == "certain":
                db_kind, attr, mode = "none", "full", "follow"
            elif cls == "brok":
                db_kind, attr, mode = "text", "full", "nofollow"
            else:
                db_kind, attr, mode = "text", "full", mode
        else:
            db_kind = DB_CYCLE[idx % len(DB_CYCLE)]
        nofollow = mode == "nofollow"
        env = {"HOME": "{root}/h", "XDG_DATA_HOME": "{root}/dh",
               "XDG_DATA_DIRS": "{root}/db"}
        os.makedirs(os.path.join(root, "h"), exist_ok=True)
        os.makedirs(os.path.join(root, "dh"), exist_ok=True)
        files = self.build_db_files(root, db_kind)
        paths = []   # list of (rel, ptype, target)
        labels = []

        def add(rel, ptype, target=None):
            paths.append({"path": rel, "type": ptype, "target": target})

        def meas(rel):
            labels.append(gio_label(root, env, rel, attr, nofollow))

        def w(rel, data, mode_oct=None):
            p = os.path.join(root, rel)
            d = os.path.dirname(p)
            if d and not os.path.isdir(d):
                os.makedirs(d, exist_ok=True)
            with open(p, "wb") as fh:
                fh.write(data)
            if mode_oct is not None:
                os.chmod(p, mode_oct)

        def lnk(rel, target):
            p = os.path.join(root, rel)
            if os.path.lexists(p):
                os.remove(p)
            os.symlink(target, p)

        def fifo(rel):
            p = os.path.join(root, rel)
            if os.path.exists(p):
                os.remove(p)
            os.mkfifo(p)

        def sock(rel):
            p = os.path.join(root, rel)
            if os.path.lexists(p):
                os.remove(p)
            srv = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
            srv.bind(p)
            srv.close()
            try:
                os.unlink(p)
            except OSError:
                pass
            srv2 = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
            srv2.bind(p)
            srv2.close()
            # the listening socket file remains on disk after close

        if cls == "dir":
            os.makedirs(os.path.join(root, "sub"), exist_ok=True)
            os.makedirs(os.path.join(root, "sub", "named.png.d"), exist_ok=True)
            os.makedirs(os.path.join(root, "sub.png"), exist_ok=True)
            add("sub", "dir")
            add("sub/named.png.d", "dir")
            add("sub.png", "dir")
            add("sub/", "dir")
            add("h/", "dir")
            add("h", "dir")
        elif cls == "chr":
            for dev in ("/dev/null", "/dev/zero", "/dev/full", "/dev/random",
                        "/dev/urandom", "/dev/tty"):
                if os.path.exists(dev):
                    add(dev, "chardev")
        elif cls == "blk":
            for dev in ("/dev/dm-0", "/dev/nvme0n1", "/dev/sda", "/dev/loop0"):
                if os.path.exists(dev):
                    add(dev, "blkdev")
        elif cls == "fifo":
            fifo("pipe")
            add("pipe", "fifo")
            if rng.random() < 0.5:
                fifo("pipe.log")
                add("pipe.log", "fifo")
        elif cls == "sock":
            sock("s.sock")
            add("s.sock", "sock")
            if rng.random() < 0.5:
                sock("s.data")
                add("s.data", "sock")
        elif cls == "zero":
            w("empty.png", b"")
            w("empty", b"")
            w("empty.bin", b"")
            w("empty.tar.gz", b"")
            w("zeroext", b"")
            add("empty.png", "file")
            add("empty", "file")
            add("empty.bin", "file")
            add("empty.tar.gz", "file")
            add("zeroext", "file")
        elif cls == "empty":
            w("notefile", TXT)
            w("README", TXT)
            w("script", SH)
            add("notefile", "file")
            add("README", "file")
            add("script", "file")
        elif cls == "sym":
            w("target.png", PNG)
            os.makedirs(os.path.join(root, "sub"), exist_ok=True)
            lnk("link.png", "target.png")
            lnk("linkdir", "sub")
            add("link.png", "symlink", "target.png")
            add("linkdir", "symlink", "sub")
        elif cls == "brok":
            lnk("broken", "no-such-target-xyz")
            lnk("loop1", "loop2")
            lnk("loop2", "loop1")
            add("broken", "symlink", "no-such-target-xyz")
            # a loop answers only under NOFOLLOW (follow mode cannot stat it:
            # ELOOP -> the oracle refuses -> the generic drop rule removes it)
            add("loop1", "symlink", "loop2")
        elif cls == "nofollow":
            w("target.png", PNG)
            os.makedirs(os.path.join(root, "sub"), exist_ok=True)
            fifo("pipe")
            lnk("nl.png", "target.png")
            lnk("nldir", "sub")
            lnk("nlbroken", "no-such-target-xyz")
            lnk("nlfifo", "pipe")
            add("nl.png", "symlink", "target.png")
            add("nldir", "symlink", "sub")
            add("nlbroken", "symlink", "no-such-target-xyz")
            add("nlfifo", "symlink", "pipe")
        elif cls == "follow":
            w("target.png", PNG)
            os.makedirs(os.path.join(root, "sub"), exist_ok=True)
            fifo("pipe")
            lnk("fl.png", "target.png")
            lnk("fldir", "sub")
            lnk("flfifo", "pipe")
            add("fl.png", "symlink", "target.png")
            add("fldir", "symlink", "sub")
            add("fldir/", "symlink", "sub")
            add("flfifo", "symlink", "pipe")
        elif cls == "certain":
            w("pic.png", PNG)
            w("doc.pdf", PDF)
            w("tone.ogg", OGG)
            w("arch.zip", ZIP)
            w("app.desktop", DESKTOP)
            add("pic.png", "file")
            add("doc.pdf", "file")
            add("tone.ogg", "file")
            add("arch.zip", "file")
            add("app.desktop", "file")
        elif cls == "uncertain":
            w("mystery.png", TXT)          # one name type; sniff never runs
            w("multi.dat", PNG)            # no name type; the sniff decides
            w("plain", TXT)                # no name type; text fallback
            w("entry.conf", DESKTOP)       # desktop bytes under a plain name
            w("bin.blob", ELF)             # no name type; magic decides
            add("mystery.png", "file")
            add("multi.dat", "file")
            add("plain", "file")
            add("entry.conf", "file")
            add("bin.blob", "file")
        elif cls == "fast":
            w("f.png", PNG)
            w("f.txt", TXT)
            w("f.bin", b"\x00\x01\x02")
            add("f.png", "file")
            add("f.txt", "file")
            add("f.bin", "file")
        elif cls == "readerr":
            w("locked.png", PNG, 0o000)
            w("locked", TXT, 0o000)
            w("locked.bin", b"\x00\x01\x02", 0o000)
            add("locked.png", "unreadable")
            add("locked", "unreadable")
            add("locked.bin", "unreadable")

        # measure every path live
        for pinfo in paths:
            meas(pinfo["path"])

        # drop ERROR-labelled paths (refusal leg: frozen cases + host list cover it);
        # contract 2: the labels list holds one one-element list ["<type>"] per path.
        kept_paths, kept_labels, dropped = [], [], []
        for pinfo, lb in zip(paths, labels):
            if lb == "ERROR":
                dropped.append(pinfo["path"])
            else:
                kept_paths.append(pinfo)
                kept_labels.append([lb])

        cid = "%s-%02d-%s" % (cls, idx, db_kind)
        return {"id": cid, "class": cls, "db_kind": db_kind, "env": env,
                "files": files, "mode": mode, "attr": attr,
                "paths": kept_paths, "labels": kept_labels,
                "dropped_paths": dropped}


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--seed", required=True, help="hex seed")
    ap.add_argument("--dir", required=True, help="parent dir for the case roots")
    ap.add_argument("--out", default=None, help="also write the JSONL envelope here")
    ap.add_argument("--count", type=int, default=120, help="cases (default 120)")
    a = ap.parse_args()

    if not os.path.exists(GIO):
        sys.stderr.write("filetype-fresh-r97: SETUP_ERROR %s missing\n" % GIO)
        return 2
    gio_sha = sha256_file(GIO)
    seed = int(a.seed, 16)
    rng = random.Random(seed)
    os.makedirs(a.dir, exist_ok=True)

    gen = Gen(rng)
    plan = [CLASSES[i % len(CLASSES)] for i in range(a.count)]
    rng.shuffle(plan)
    occ = {}
    cases = []
    dropped_total = 0
    empty_cases = 0
    for i, cls in enumerate(plan):
        root = os.path.join(a.dir, "case-%03d" % i)
        if os.path.isdir(root):
            shutil.rmtree(root)
        os.makedirs(root, exist_ok=True)
        c = gen.case(cls, root, i, occurrence=occ.get(cls, 0))
        occ[cls] = occ.get(cls, 0) + 1
        if not c["paths"]:
            empty_cases += 1
        dropped_total += len(c["dropped_paths"])
        cases.append(c)

    label_census = {}
    class_census = {}
    db_census = {}
    for c in cases:
        class_census[c["class"]] = class_census.get(c["class"], 0) + 1
        db_census[c["db_kind"]] = db_census.get(c["db_kind"], 0) + 1
        for lb in c["labels"]:
            t = lb[0]
            label_census[t] = label_census.get(t, 0) + 1
    n_paths = sum(len(c["paths"]) for c in cases)
    sys.stderr.write("filetype-fresh-r97: seed=%s cases=%d paths=%d dropped_paths=%d "
                     "empty_cases=%d gio=%s gio_sha256=%s\n"
                     % (a.seed, len(cases), n_paths, dropped_total, empty_cases,
                        GIO, gio_sha))
    sys.stderr.write("filetype-fresh-r97: classes=%s\n"
                     % json.dumps(class_census, sort_keys=True))
    sys.stderr.write("filetype-fresh-r97: db_modes=%s\n"
                     % json.dumps(db_census, sort_keys=True))
    for k in sorted(label_census):
        sys.stderr.write("filetype-fresh-r97: label %s %d\n" % (k, label_census[k]))
    if empty_cases:
        sys.stderr.write("filetype-fresh-r97: SETUP_ERROR empty cases=%d\n" % empty_cases)
        return 2
    # stdout: exactly one JSON object per case (compact, ASCII) - this is the contract.
    fh_out = open(a.out, "w") if a.out else None
    for c in cases:
        line = json.dumps(c, sort_keys=True, ensure_ascii=True)
        print(line)
        if fh_out:
            fh_out.write(line + "\n")
    if fh_out:
        fh_out.close()
        sys.stderr.write("filetype-fresh-r97: wrote %s\n" % a.out)
    return 0


if __name__ == "__main__":
    sys.exit(main())
