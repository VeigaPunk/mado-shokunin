#!/usr/bin/env python3
"""DRAFT decision-table probe for the r95 knowledge entry (scribe seat).

Builds fixture mime.cache databases from the candidate's build_cache, runs the C oracle
(env -i LC_ALL=C HOME/XDG_DATA_HOME/XDG_DATA_DIRS) and the candidate copy, and prints one row per
(state, name, data) with oracle vs tool.  Nothing here is a measurement.
"""
import importlib.util
import json
import os
import shutil
import subprocess
import sys

S = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location("ms", os.path.join(S, "tools", "mado-mimesniff.py"))
ms = importlib.util.module_from_spec(spec)
spec.loader.exec_module(ms)

ORACLE = os.path.join(S, "oracle")
TOOL = os.path.join(S, "tools", "mado-mimesniff.py")
FX = os.path.join(S, "fx")


def ml(start, length, value, mask=None, word=1, children=()):
    return {"start": start, "length": length, "value": value, "mask": mask, "word": word,
            "children": list(children)}


ROWS = []


def case(cid, note, caches, inputs, data=None):
    """caches: {dirbase: cache_kwargs or None}; inputs: [(name|None, databytes)]."""
    root = os.path.join(FX, cid)
    if os.path.isdir(root):
        shutil.rmtree(root)
    for d in ("h", "dh", "s1", "s2"):
        os.makedirs(os.path.join(root, d), exist_ok=True)
    if not caches:
        caches = {"dh": {}}
    for base, kw in caches.items():
        mdir = os.path.join(root, base, "mime")
        os.makedirs(mdir, exist_ok=True)
        with open(os.path.join(mdir, "mime.cache"), "wb") as fh:
            fh.write(ms.build_cache(**kw))
    env = {"LC_ALL": "C", "HOME": os.path.join(root, "h"),
           "XDG_DATA_HOME": os.path.join(root, "dh"),
           "XDG_DATA_DIRS": os.path.join(root, "s1") + ":" + os.path.join(root, "s2")}
    pairs, files = [], []
    for i, (name, data) in enumerate(inputs):
        p = os.path.join(root, "data%02d" % i)
        with open(p, "wb") as fh:
            fh.write(data)
        pairs += ["=" + name if name is not None else "0", p]
        files.append(p)
    o = subprocess.run(["env", "-i"] + ["%s=%s" % kv for kv in env.items()] + [ORACLE] + pairs,
                       capture_output=True, text=True)
    if o.returncode != 0:
        ROWS.append((cid, note, "ORACLE_RC%d" % o.returncode, o.stderr.strip().splitlines()[-1:], None))
        return
    olines = o.stdout.splitlines()
    for i, (name, data) in enumerate(inputs):
        lab = olines[i] if i < len(olines) else "?"
        cmd = [sys.executable, "-I", TOOL, "--json", "--home", env["HOME"],
               "--data-home", env["XDG_DATA_HOME"], "--data-dirs", env["XDG_DATA_DIRS"]]
        if name is not None:
            cmd += ["--name", name]
        t = subprocess.run(cmd + [files[i]], capture_output=True, text=True,
                           env={"PATH": "/nonexistent-empty", "LC_ALL": "C", "HOME": env["HOME"],
                                "XDG_DATA_HOME": env["XDG_DATA_HOME"], "XDG_DATA_DIRS": env["XDG_DATA_DIRS"]})
        if t.returncode == 0:
            r = json.loads(t.stdout)["results"][0]
            got = "%s\t%d" % (r["type"], r["uncertain"])
            ok = got == lab
        else:
            got = "EXIT%d %s" % (t.returncode, (t.stdout or t.stderr).strip()[:40])
            ok = lab.startswith("UNSUPPORTED")
        nm = "NULL" if name is None else repr(name)
        ROWS.append((cid, note, nm, repr(data)[:40], lab, got, "ok" if ok else "DIFF"))


C = ms.build_cache

# --- fallback / looks_like_text bytes
case("f-vt", "VT 0x0b only byte between text and binary classes", {}, [(None, b"ab\x0bcd")])
case("f-ff", "FF 0x0c", {}, [(None, b"ab\x0ccd")])
case("f-bs", "BS 0x08", {}, [(None, b"ab\x08cd")])
case("f-del", "DEL 0x7f", {}, [(None, b"ab\x7fcd")])
case("f-soh", "SOH 0x01", {}, [(None, b"ab\x01cd")])
case("f-nul", "NUL 0x00", {}, [(None, b"ab\x00cd")])
case("f-tab", "TAB 0x09", {}, [(None, b"ab\tcd")])
case("f-128", "0x01 after the first 128 bytes", {}, [(None, b"a" * 128 + b"\x01")])
case("f-127", "0x01 at index 127", {}, [(None, b"a" * 127 + b"\x01")])
case("f-empty", "empty data, no name", {}, [(None, b"")])
case("f-high", "high-bit byte (UTF-8 continuation)", {}, [(None, b"caf\xc3\xa9\n")])
case("f-vt130", "VT past the 128-byte fallback window", {}, [(None, b"a" * 130 + b"\x0b")])
case("f-nul130", "NUL past the 128-byte fallback window", {}, [(None, b"a" * 130 + b"\x00")])
case("f-us", "US 0x1f", {}, [(None, b"ab\x1fcd")])
case("f-vt-early", "VT plus BS: looks_like_text looks at the whole data", {}, [(None, b"ab\x08c\x0bd")])

# --- name step interaction
NAMES = dict(globs=[("*.one", "t/single", 50), ("*.two", "app/x-a", 50), ("*.two", "app/x-b", 50),
                    ("*.dup", "app/child", 50), ("*.dup", "text/x-old", 50)])
NAMES_P = dict(parents=[("app/child", ["app/mid"]), ("app/mid", ["app/base"])],
               aliases=[("text/x-old", "text/x-new")], **NAMES)
case("n-one", "one name type: data not read (binary bytes)", {"dh": NAMES_P}, [("x.one", b"\x01\x02HI")])
case("n-dir", "trailing slash with data", {}, [("d/", b"HI")])
case("n-two-empty", "empty data beats two name types", {"dh": NAMES_P}, [("x.two", b"")])
case("n-none-text", "no name type, text data", {"dh": NAMES_P}, [("zz", b"plain words\n")])
case("n-none-bin", "no name type, binary data", {"dh": NAMES_P}, [("zz", b"\x01\x02")])
case("n-single-noname", "text data, name NULL", {"dh": NAMES_P}, [(None, b"plain words\n")])
case("n-dot", "name with no extension, text data", {}, [("README", b"hello\n")])
case("n-basename", "directory component in the name", NAMES and {"dh": NAMES_P}, [("dir.txt/f.one", b"\x01HI")])

# --- magic: priority gate and same-cache order
M = dict(magic=[(90, "app/hi", [ml(0, 1, b"HI")]),
                (79, "app/mid", [ml(0, 1, b"MI")]),
                (0, "app/zero", [ml(0, 1, b"Z0")]),
                (0x80000000, "app/neg", [ml(0, 1, b"NG")]),
                (50, "app/range", [ml(2, 3, b"RG")]),
                (55, "app/masked", [ml(0, 1, b"\x10\x00", b"\xf0\x00")]),
                (50, "app/nest", [ml(0, 1, b"NE", children=[ml(4, 1, b"X"), ml(4, 1, b"Y")])]),
                (40, "application/x-desktop", [ml(0, 1, b"[Desktop Entry]")]),
                (60, "app/b-eq", [ml(0, 1, b"EQ")]),
                (70, "app/word", [ml(0, 2, b"WD", None, 4)]),
                (60, "app/base", [ml(0, 1, b"BA")])])
case("m-prio90", "magic prio 90 with no name", {"dh": M}, [(None, b"HI there")])
case("m-prio79-name", "magic prio 79, two name types, no subclass", {"dh": dict(M, **NAMES_P)},
     [("x.two", b"MI x")])
case("m-prio79-sub", "magic prio 79, name type is a subclass", {"dh": dict(M, **NAMES_P)},
     [("x.dup", b"BA x")])
case("m-prio79-sub-alias", "magic prio 79, alias in subclass", {"dh": dict(M, **NAMES_P)},
     [("x.dup", b"plain\n")])
case("m-prio0", "magic prio 0 is discarded", {"dh": M}, [(None, b"Z0 x")])
case("m-negative", "magic prio 2^31 (negative int)", {"dh": M}, [(None, b"NG x")])
case("m-range", "range start 2 length 3", {"dh": M}, [(None, b"\x01\x01\x01\x01RG"), (None, b"\x01\x01RG")])
case("m-mask", "mask on the first byte", {"dh": M}, [(None, b"\x1f\x99")])
case("m-nest", "child must hold", {"dh": M}, [(None, b"NE\x01\x01Y"), (None, b"NE\x01\x01Z")])
case("m-word", "word_size 4 in the cache, raw byte compare", {"dh": M}, [(None, b"WDxx")])
case("m-order", "same cache: lower prio first in list", {"dh": dict(magic=[(30, "app/lo", [ml(0, 1, b"LO")]),
                                                                          (95, "app/hi", [ml(0, 1, b"LO")])])},
     [(None, b"LO x")])
case("m-caches", "across caches: strictly greater wins, equal keeps first",
     {"dh": dict(magic=[(90, "app/a90", [ml(0, 1, b"AA")]), (60, "app/a60", [ml(0, 1, b"EQ")])]),
      "s1": dict(magic=[(95, "app/b95", [ml(0, 1, b"AA")]), (60, "app/b60", [ml(0, 1, b"EQ")])])},
     [(None, b"AA"), (None, b"EQ")])
case("m-desktop", "desktop sniff with and without a name", {"dh": M},
     [(None, b"[Desktop Entry]\n"), ("zz.nomatch", b"[Desktop Entry]\n"), ("zz.desktop", b"[Desktop Entry]\n")])

# --- magic value longer than data, offset past data
case("m-short", "value longer than data, offset past data",
     {"dh": dict(magic=[(90, "app/long", [ml(0, 4, b"ABCD")]), (80, "app/far", [ml(200, 1, b"X")])])},
     [(None, b"ABC"), (None, b"AB"), (None, b"X")])


case("n-single-beats-hi", "one name type wins over a prio-90 magic match", {"dh": dict(M, **NAMES_P)},
     [("x.one", b"HI")])
case("n-two-hi", "two name types, prio-90 magic wins", {"dh": dict(M, **NAMES_P)}, [("x.two", b"HI")])
case("n-two-bin", "two name types, binary data, no magic", {"dh": NAMES_P}, [("x.two", b"\x01\x02")])
case("n-textplain-sub", "sniffed text/plain rescues a text/* name type",
     {"dh": dict(magic=[(60, "text/plain", [ml(0, 2, b"TP")])],
                 globs=[("*.tt", "text/x-a", 50), ("*.tt", "text/x-b", 50)])}, [("x.tt", b"TP x")])
case("n-two-zero-name", "name with no type, magic prio 60", {"dh": M}, [("zz", b"EQ x")])


case("m-unknown-literal", "a magic entry naming application/octet-stream is a real type",
     {"dh": dict(magic=[(60, "application/octet-stream", [ml(0, 2, b"OB")])])}, [(None, b"OB\x01")])
case("n-one-empty", "one name type beats even empty data", {"dh": NAMES_P}, [("x.one", b"")])


def main():
    print("%-16s %-46s %-12s %-26s %-18s %-18s %s" % ("case", "note", "name", "data", "oracle", "tool", "verdict"))
    bad = 0
    for r in ROWS:
        print("%-16s %-46s %-12s %-26s %-18s %-18s %s" % r if len(r) == 7 else r)
        if len(r) == 7 and r[6] != "ok":
            bad += 1
    print("ROWS=%d DIFFS=%d" % (len(ROWS), bad))


main()
