#!/usr/bin/env python3
"""Round-95 C1 frozen case-set generator + oracle labeller (seat R95MExecCasesC1).

Builds .ufo/waves/round-95/controls/mimesniff-cases-r95.json in the shared CASE FILE SCHEMA:
labels come ONLY from the compiled oracle (.ufo/waves/round-95/controls/mimesniff-oracle-r95.c,
sha256 99df35f8...).  Intent checks ("want" lists) are printed for the seat's own review and
never alter labels.  Corrupt-offset caches are produced by patching a locally-built mime.cache
(the builder mirrors the xdgmimecache.c layout; it is byte-compared against the candidate's
build_cache on a random battery before use).  update-mime-database (real class) runs ONLY on a
directory inside this script's scratch tree.
"""
import base64
import json
import os
import shutil
import struct
import subprocess
import sys

LANE = "/home/vgpnk/Projects/shokunin/mado-shokunin"
S = os.path.dirname(os.path.abspath(__file__))
ORACLE = os.path.join(S, "oracle")
OUT_JSON = os.path.join(LANE, ".ufo/waves/round-95/controls/mimesniff-cases-r95.json")
REAL_DIR = os.path.join(S, "real2")
ORACLE_SHA = "99df35f8b3fd7005f30789f8866984a1bbceaff8dc6c1d326f0132eb7b4d124a"
GLIB = "2.90.1-1"

# ---------------------------------------------------------------- mime.cache builder

def u32(v):
    return struct.pack(">I", v & 0xFFFFFFFF)


def build_cache(aliases=(), parents=(), literals=(), globs=(), magic=(), version=(1, 2)):
    """mime.cache writer mirroring the xdgmimecache.c layout (same placement as the
    candidate's build_cache, plus a patch map).  Returns (blob, info)."""
    blob = bytearray(40)
    strings = {}
    hdr = {}

    def s(x):
        x = x.encode() if isinstance(x, str) else x
        if x not in strings:
            strings[x] = len(blob)
            blob.extend(x + b"\0")
        return strings[x]

    for a, m in aliases:
        s(a), s(m)
    for m, ps in parents:
        s(m)
        for p in ps:
            s(p)
    for lit, m, w in literals:
        s(lit), s(m)
    sfx = []
    flist = []
    for g, m, w in globs:
        if g.startswith("*") and len(g) > 1 and not any(c in g[1:] for c in "*?[]"):
            sfx.append((g[1:], m, w))   # suffixable: "*.ext" -> reverse-suffix tree
        else:
            flist.append((g, m, w))     # fnmatch list
        s(g)
        s(m)
    for _p, m, _ms in magic:
        s(m)

    def place_values(ml):
        ml["_v"] = len(blob)
        blob.extend(ml["value"])
        if ml.get("mask") is not None:
            ml["_m"] = len(blob)
            blob.extend(ml["mask"])
        else:
            ml["_m"] = 0
        for ch in ml.get("children", []):
            place_values(ch)

    for _p, _m, ms in magic:
        for ml in ms:
            place_values(ml)
    while len(blob) % 4:
        blob.append(0)

    def key(x):
        return x[0] if isinstance(x[0], bytes) else x[0].encode()

    hdr[4] = len(blob)
    al = sorted(aliases, key=key)
    blob.extend(u32(len(al)))
    for a, m in al:
        blob.extend(u32(s(a)) + u32(s(m)))
    hdr[8] = len(blob)
    pl = sorted(parents, key=key)
    plist_at = len(blob)
    blob.extend(u32(len(pl)) + b"\0" * (8 * len(pl)))
    for i, (m, ps) in enumerate(pl):
        at = len(blob)
        blob.extend(u32(len(ps)))
        for p in ps:
            blob.extend(u32(s(p)))
        blob[plist_at + 4 + 8 * i: plist_at + 12 + 8 * i] = u32(s(m)) + u32(at)
    hdr[12] = len(blob)
    ll = sorted(literals, key=key)
    blob.extend(u32(len(ll)))
    for lit, m, w in ll:
        blob.extend(u32(s(lit)) + u32(s(m)) + u32(w))
    hdr[16] = len(blob)
    if sfx:
        # reverse-suffix trie (xdgmimecache.c cache_glob_lookup_suffix): root block is
        # u32 n_entries + u32 array offset; nodes are 12 bytes (char, n_children, off);
        # terminal entries carry char 0 with (mime_offset, weight), sorted first.
        root = {}
        for suf, m, w in sfx:
            nd = root
            for ch in reversed(suf):
                nd = nd.setdefault(ch, {})
            nd.setdefault(0, []).append((m, w))
        tree = bytearray()
        base = len(blob) + 8   # absolute buffer offset where `tree` will be appended

        def emit(d):
            terms = d.get(0, [])
            keys = sorted(k for k in d if k != 0)
            off = len(tree)
            tree.extend(b"\0" * (12 * (len(terms) + len(keys))))
            for j, (m, w) in enumerate(terms):
                tree[off + 12 * j: off + 12 * j + 12] = u32(0) + u32(s(m)) + u32(w)
            for j, k in enumerate(keys):
                sub = d[k]
                ko = base + emit(sub)
                cnt = len(sub.get(0, [])) + len([x for x in sub if x != 0])
                at = off + 12 * (len(terms) + j)
                tree[at:at + 12] = u32(ord(k)) + u32(cnt) + u32(ko)
            return off

        cnt_root = len(root.get(0, [])) + len([k for k in root if k != 0])
        emit(root)
        blob.extend(u32(cnt_root) + u32(len(blob) + 8))
        blob.extend(tree)
    else:
        blob.extend(u32(0) + u32(len(blob) + 8))
    hdr[20] = len(blob)
    blob.extend(u32(len(flist)))
    for g, m, w in flist:
        blob.extend(u32(s(g)) + u32(s(m)) + u32(w))

    def place(mls):
        at = len(blob)
        blob.extend(b"\0" * (32 * len(mls)))
        for i, ml in enumerate(mls):
            kids = ml.get("children", [])
            ko = place(kids) if kids else 0
            ml["_rec"] = at + 32 * i
            ml["_ko"] = ko
            rec = (u32(ml["start"]) + u32(ml["length"]) + u32(ml.get("word", 1))
                   + u32(len(ml["value"])) + u32(ml["_v"]) + u32(ml["_m"])
                   + u32(len(kids)) + u32(ko))
            blob[ml["_rec"]: ml["_rec"] + 32] = rec
        return at

    hdr[24] = len(blob)
    magic_at = len(blob)
    blob.extend(u32(len(magic)) + u32(0) + u32(len(blob) + 12))
    mat = len(blob)
    blob.extend(b"\0" * (16 * len(magic)))
    entries = []
    for i, (p, m, ms) in enumerate(magic):
        mo = place(ms) if ms else 0
        off = mat + 16 * i
        blob[off: off + 16] = u32(p) + u32(s(m)) + u32(len(ms)) + u32(mo)
        entries.append({"off": off, "prio": p, "mime": m, "n": len(ms),
                        "mlo": mo, "matchlets": ms})
    for k in (28, 32, 36):
        hdr[k] = len(blob)
    blob.extend(u32(0))
    blob[0:4] = struct.pack(">HH", *version)
    for k, v in hdr.items():
        blob[k:k + 4] = u32(v)
    info = {"hdr": dict(hdr), "magic_at": magic_at, "entries": entries}
    return bytes(blob), info


def patch(blob, off, val):
    blob[off:off + 4] = u32(val)


# ---------------------------------------------------------------- case plumbing

CASES = []
_counts = {}


def add(cls, slug, env, files, inputs, want=None, expect_refusal=None, note=""):
    _counts[cls] = _counts.get(cls, 0) + 1
    cid = f"{cls}-{_counts[cls]:02d}-{slug}"
    case = {"id": cid, "class": cls, "env": env, "files": files, "inputs": inputs,
            "labels": None, "_want": want, "_note": note}
    if expect_refusal:
        case["expect_refusal"] = True
    CASES.append(case)
    return case


def b64(b):
    return base64.b64encode(b).decode("ascii")


def nm(x):
    return None if x is None else b64(x if isinstance(x, bytes) else x.encode())


E_S1 = {"HOME": "{root}/h", "XDG_DATA_HOME": None, "XDG_DATA_DIRS": "{root}/s1"}
E_S1_S2 = {"HOME": "{root}/h", "XDG_DATA_HOME": None, "XDG_DATA_DIRS": "{root}/s1:{root}/s2"}
E_DH_S1 = {"HOME": "{root}/h", "XDG_DATA_HOME": "{root}/dh", "XDG_DATA_DIRS": "{root}/s1"}
E_DH_S1_S2 = {"HOME": "{root}/h", "XDG_DATA_HOME": "{root}/dh", "XDG_DATA_DIRS": "{root}/s1:{root}/s2"}


def cf(files, d, blob):
    files[f"{d}/mime/mime.cache"] = b64(blob)


def ml(start, length, value, mask=None, children=()):
    return {"start": start, "length": length, "value": value, "mask": mask,
            "children": list(children)}


# ---------------------------------------------------------------- oracle driver

def materialize(root, envspec, files):
    if os.path.exists(root):
        shutil.rmtree(root)
    os.makedirs(root)
    os.makedirs(os.path.join(root, "h"), exist_ok=True)
    if envspec.get("XDG_DATA_HOME"):
        os.makedirs(os.path.join(root, envspec["XDG_DATA_HOME"].replace("{root}/", "")),
                    exist_ok=True)
    for d in envspec["XDG_DATA_DIRS"].replace("{root}/", "").split(":"):
        os.makedirs(os.path.join(root, d), exist_ok=True)
    for rel, b in files.items():
        p = os.path.join(root, rel)
        os.makedirs(os.path.dirname(p), exist_ok=True)
        with open(p, "wb") as fh:
            fh.write(base64.b64decode(b))


def run_oracle(root, envspec, inputs, tag):
    workdir = os.path.join(S, "data", tag)
    os.makedirs(workdir, exist_ok=True)
    args = []
    for i, (name, data) in enumerate(inputs):
        p = os.path.join(workdir, f"in{i}.bin")
        with open(p, "wb") as fh:
            fh.write(data)
        if name is not None and isinstance(name, str):
            name = name.encode()
        args.append(b"0" if name is None else b"=" + name)
        args.append(os.fsencode(p))
    env = {"LC_ALL": "C", "HOME": envspec["HOME"].replace("{root}", root)}
    if envspec.get("XDG_DATA_HOME") is not None:
        env["XDG_DATA_HOME"] = envspec["XDG_DATA_HOME"].replace("{root}", root)
    env["XDG_DATA_DIRS"] = envspec["XDG_DATA_DIRS"].replace("{root}", root)
    try:
        r = subprocess.run([ORACLE] + args, env=env, capture_output=True, timeout=10)
    except subprocess.TimeoutExpired:
        return None, "timeout"
    if r.returncode != 0:
        return None, f"rc={r.returncode}"
    lines = r.stdout.split(b"\n")
    if lines and lines[-1] == b"":
        lines.pop()
    if len(lines) != len(inputs):
        return None, f"lines={len(lines)} want={len(inputs)}"
    out = []
    for ln in lines:
        parts = ln.split(b"\t")
        if len(parts) != 2:
            return None, f"badline={ln!r}"
        out.append([parts[0].decode("utf-8", "surrogateescape"), int(parts[1])])
    return out, "ok"


# ---------------------------------------------------------------- real-class cache

def build_real():
    """update-mime-database on a scratch packages/*.xml; returns (cache_bytes, xml_bytes)."""
    if os.path.exists(REAL_DIR):
        shutil.rmtree(REAL_DIR)
    mimedir = os.path.join(REAL_DIR, "mimedir")
    os.makedirs(os.path.join(mimedir, "packages"))
    xml = b"""<?xml version="1.0" encoding="UTF-8"?>
<mime-info xmlns="http://www.freedesktop.org/standards/shared-mime-info">
  <mime-type type="app/x-myfm">
    <glob pattern="*.myfm"/>
    <alias type="app/x-myfm-old"/>
    <magic priority="79"><match type="string" offset="0" value="MYFM"/></magic>
  </mime-type>
  <mime-type type="app/x-nest">
    <glob pattern="*.nest"/>
    <sub-class-of type="app/x-myfm"/>
    <magic priority="60"><match type="string" offset="0" value="PKG"><match type="big16" offset="4" value="2"/><match type="byte" offset="6" value="65" mask="240"/></match></magic>
  </mime-type>
  <mime-type type="app/x-two">
    <glob pattern="*.two"/>
    <glob pattern="z.*"/>
    <sub-class-of type="app/x-myfm-old"/>
    <magic priority="10"><match type="string" offset="0" value="TWO"/></magic>
  </mime-type>
  <mime-type type="app/x-sub2">
    <glob pattern="*.sub2"/>
    <glob pattern="z.?*"/>
    <sub-class-of type="app/x-nest"/>
  </mime-type>
  <mime-type type="app/x-le32">
    <magic priority="50"><match type="little32" offset="2" value="256"/></magic>
  </mime-type>
  <mime-type type="app/x-big32">
    <magic priority="50"><match type="big32" offset="0" value="1094861636"/></magic>
  </mime-type>
  <mime-type type="app/x-range">
    <magic priority="50"><match type="string" offset="3:10" value="XY"/></magic>
  </mime-type>
  <mime-type type="app/x-byte">
    <magic priority="50"><match type="byte" offset="1" value="127"/></magic>
  </mime-type>
</mime-info>
"""
    with open(os.path.join(mimedir, "packages", "my.xml"), "wb") as fh:
        fh.write(xml)
    r = subprocess.run(["update-mime-database", mimedir], capture_output=True, timeout=60)
    cache_path = os.path.join(mimedir, "mime.cache")
    if r.returncode != 0 or not os.path.exists(cache_path):
        sys.stderr.write(r.stderr.decode() + r.stdout.decode())
        raise SystemExit("update-mime-database failed")
    bad = [ln for ln in r.stderr.decode().splitlines() if "Error" in ln or "error" in ln]
    if bad:
        print("UMD stderr errors:", bad)
    with open(cache_path, "rb") as fh:
        return fh.read(), xml


def add_real(cache, xml):
    # R1 plain magic, no name
    add("real", "myfm-data",
        E_S1, {"s1/mime/mime.cache": b64(cache), "s1/mime/packages/my.xml": b64(xml)},
        [(None, b"MYFM data here\n"), (None, b"MYFM")],
        want=[(0, "app/x-myfm", 0), (1, "app/x-myfm", 0)],
        note="real update-mime-database cache; string magic prio 79")
    # R2 one name type short-circuits even with non-matching data
    add("real", "glob-short-circuit",
        E_S1, {"s1/mime/mime.cache": b64(cache), "s1/mime/packages/my.xml": b64(xml)},
        [("x.myfm", b"\x01\x02binary"), ("x.nest", b"no magic here\n")],
        want=[(0, "app/x-myfm", 0), (1, "app/x-nest", 0)],
        note="single glob type: bytes never sniffed")
    # R3 sniff without name types
    add("real", "no-name-type",
        E_S1, {"s1/mime/mime.cache": b64(cache), "s1/mime/packages/my.xml": b64(xml)},
        [("a.nomatch", b"MYFM head")],
        want=[(0, "app/x-myfm", 0)])
    # R4 several name types + prio<80 sniff: alias-mediated and chained subclass paths
    add("real", "subclass-tiebreak",
        E_S1, {"s1/mime/mime.cache": b64(cache), "s1/mime/packages/my.xml": b64(xml)},
        [("z.q", b"MYFM data"), ("z.q", b"PKG\x00\x02\x00A\n"),
         ("z.q", b"plain text\n")],
        want=[(0, "app/x-two", 0), (1, "app/x-sub2", 0), (2, "app/x-two", 1)],
        note="z.q matches the two z.* list globs -> types [app/x-two, app/x-sub2]; "
             "MYFM (p79<80): x-two's parent is the ALIAS app/x-myfm-old, true only "
             "after unalias; PKG: x-sub2 -> x-nest -> x-myfm chain; text: no help")
    # R5 nested real magic
    add("real", "nested-children",
        E_S1, {"s1/mime/mime.cache": b64(cache), "s1/mime/packages/my.xml": b64(xml)},
        [(None, b"PKGA\x00\x02\x00A"), (None, b"PKGA\x00\x03AA"),
         (None, b"PKGA\x00\x02\x00z"), (None, b"PKGA\x00\x03\x00z"),
         (None, b"PKGA\x00\x02\x00B")],
        want=[(0, "app/x-nest", 0), (1, "app/x-nest", 0), (2, "app/x-nest", 0),
              (3, "application/octet-stream", 1), (4, "app/x-nest", 0)],
        note="children are an ANY group: big16 00 02 at 4 OR 'A' at 6 under mask 240; "
             "with both children failing the parent PKG alone does not match")
    # R6 word sizes pre-converted in the cache
    add("real", "word-sizes",
        E_S1, {"s1/mime/mime.cache": b64(cache), "s1/mime/packages/my.xml": b64(xml)},
        [(None, b"xx\x00\x01\x00\x00y\n"), (None, b"ABCDxy\n"), (None, b"\x01\x02")],
        want=[(0, "app/x-le32", 0), (1, "app/x-big32", 0), (2, "application/octet-stream", 1)],
        note="little32 256 -> 00 01 00 00 at 2; big32 1094861636 -> ABCD at 0")
    # R7 range a:b from XML
    add("real", "xml-range",
        E_S1, {"s1/mime/mime.cache": b64(cache), "s1/mime/packages/my.xml": b64(xml)},
        [(None, b"aaaXY\n"), (None, b"aaaaaaaaXY"), (None, b"aXY"),
         (None, b"aaaaaaaaaaaaXY")],
        want=[(0, "app/x-range", 0), (1, "app/x-range", 0), (2, "text/plain", 0),
              (3, "text/plain", 0)],
        note="offset 3:10 -> window positions 3..10; XY at 1 and at 12 are outside")
    # R8 byte type
    add("real", "xml-byte",
        E_S1, {"s1/mime/mime.cache": b64(cache), "s1/mime/packages/my.xml": b64(xml)},
        [(None, b"a\x7f\n"), (None, b"a\x7e\n")],
        want=[(0, "app/x-byte", 0), (1, "text/plain", 0)])
    # R9 cross-dir: real cache in s2, nothing in s1
    add("real", "second-dir",
        E_S1_S2, {"s2/mime/mime.cache": b64(cache), "s2/mime/packages/my.xml": b64(xml)},
        [(None, b"MYFM")],
        want=[(0, "app/x-myfm", 0)])
    # R10 user dir overrides: same cache under XDG_DATA_HOME
    add("real", "data-home-dir",
        E_DH_S1, {"dh/mime/mime.cache": b64(cache), "dh/mime/packages/my.xml": b64(xml)},
        [(None, b"MYFM"), ("x.myfm", b"junk")],
        want=[(0, "app/x-myfm", 0), (1, "app/x-myfm", 0)])


# ---------------------------------------------------------------- class: zerosize

def add_zerosize():
    empty_magic, _ = build_cache()
    g1, _ = build_cache(globs=[("*.txt", "txt/sub", 50)])
    g2, _ = build_cache(globs=[("*.two", "app/one", 50), ("*.two", "app/two", 50)])
    g2r, _ = build_cache(globs=[("*.two", "app/one", 50), ("*.two", "app/two", 50)],
                         magic=[(50, "app/rule", [ml(0, 1, b"HI")])])
    zdesk, _ = build_cache(globs=[("*.two", "app/one", 50), ("*.two", "app/two", 50)],
                           magic=[(80, "application/x-desktop", [ml(0, 1, b"[Desktop Entry]")])])
    vl0, _ = build_cache(magic=[(50, "app/vl0", [ml(0, 2, b"")])])
    p100, _ = build_cache(globs=[("*.two", "app/one", 50), ("*.two", "app/two", 50)],
                          magic=[(100, "app/big", [ml(0, 1, b"HI")])])
    add("zerosize", "empty-no-name", E_S1, {"s1/mime/mime.cache": b64(g1)},
        [(None, b""), ("a.txt", b""), ("a.txt", b"HI")],
        want=[(0, "application/x-zerosize", 0), (1, "txt/sub", 0), (2, "txt/sub", 0)],
        note="len==0 short-circuits sniffing; one name type ignores bytes")
    add("zerosize", "empty-two-types", E_S1, {"s1/mime/mime.cache": b64(g2)},
        [(None, b""), ("x.two", b"")],
        want=[(0, "application/x-zerosize", 0), (1, "application/x-zerosize", 0)],
        note="sniffed x-zerosize prio 100 >= 80 wins over two name types")
    add("zerosize", "empty-beats-rule", E_S1, {"s1/mime/mime.cache": b64(g2r)},
        [("x.two", b""), (None, b"")],
        want=[(0, "application/x-zerosize", 0), (1, "application/x-zerosize", 0)],
        note="empty data checked before any magic rule")
    add("zerosize", "empty-beats-p100-rule", E_S1, {"s1/mime/mime.cache": b64(p100)},
        [("x.two", b"")],
        want=[(0, "application/x-zerosize", 0)])
    add("zerosize", "empty-slash-name", E_S1, {"s1/mime/mime.cache": b64(g1)},
        [("d/", b""), ("d.txt/", b"")],
        want=[(0, "inode/directory", 1), (1, "inode/directory", 1)],
        note="trailing slash wins before everything, even empty data")
    add("zerosize", "empty-desktop-rule-no-type", E_S1, {"s1/mime/mime.cache": b64(zdesk)},
        [("zz.nomatch", b""), (None, b"")],
        want=[(0, "application/x-zerosize", 0), (1, "application/x-zerosize", 0)],
        note="empty data: not a desktop sniff, no rewrite")
    add("zerosize", "empty-home-layout", E_S1, {"h/.local/share/mime/mime.cache": b64(g1)},
        [(None, b""), ("a.txt", b"HI")],
        want=[(0, "application/x-zerosize", 0), (1, "txt/sub", 0)],
        note="XDG_DATA_HOME unset -> HOME/.local/share/mime")
    add("zerosize", "empty-vl0-rule", E_S1, {"s1/mime/mime.cache": b64(vl0)},
        [(None, b""), (None, b"q")],
        want=[(0, "application/x-zerosize", 0), (1, "app/vl0", 0)],
        note="value_length 0 matchlet would hold on any non-empty data, but len==0 wins")
    add("zerosize", "empty-dh-two-types", E_DH_S1_S2,
        {"dh/mime/mime.cache": b64(g2)}, [("x.two", b""), (None, b"")],
        want=[(0, "application/x-zerosize", 0), (1, "application/x-zerosize", 0)])


# ---------------------------------------------------------------- class: fallback

def add_fallback():
    nomatch, _ = build_cache(magic=[(50, "app/zz", [ml(0, 1, b"ZZ")])])
    empty_magic, _ = build_cache()
    add("fallback", "binary-at-128", E_S1, {"s1/mime/mime.cache": b64(nomatch)},
        [(None, b"a" * 128 + b"\x01"), (None, b"a" * 127 + b"\x01" + b"b"),
         (None, b"a" * 128 + b"\x01" + b"b")],
        want=[(0, "text/plain", 0), (1, "application/octet-stream", 1),
              (2, "text/plain", 0)],
        note="binary check reads only the first 128 bytes")
    add("fallback", "ctrl-matrix", E_S1, {"s1/mime/mime.cache": b64(empty_magic)},
        [(None, b"a\x08b\n"), (None, b"a\x09b\n"), (None, b"a\x0ab\n"),
         (None, b"a\x0cb\n"), (None, b"a\x0db\n"), (None, b"a\x0bb\n")],
        want=[(0, "text/plain", 0), (1, "text/plain", 0), (2, "text/plain", 0),
              (3, "text/plain", 0), (4, "text/plain", 0),
              (5, "application/octet-stream", 1)],
        note="fallback allows 9/10/13 only; 0x0b is binary there")
    add("fallback", "high-and-del", E_S1, {"s1/mime/mime.cache": b64(empty_magic)},
        [(None, b"a\x7fb\n"), (None, b"abc\x7f\x01def\n"), (None, b"a\x80b\n"),
         (None, b"a\xc2\xa4b\n"), (None, b"\x7f\x01")],
        want=[(0, "text/plain", 0), (1, "application/octet-stream", 1),
              (2, "text/plain", 0), (3, "text/plain", 0),
              (4, "application/octet-stream", 1)],
        note="0x7f alone passes the <32 check; DEL only matters for looks_like_text, "
             "which is consulted only when sniffed is UNKNOWN")
    add("fallback", "nul-edges", E_S1, {"s1/mime/mime.cache": b64(empty_magic)},
        [(None, b"a" * 127 + b"\x00" + b"bc"), (None, b"a" * 128 + b"\x00" + b"bc"),
         (None, b"\x1f" * 128 + b"tail")],
        want=[(0, "application/octet-stream", 1), (1, "text/plain", 0),
              (2, "application/octet-stream", 1)],
        note="0x00 at index 127 is inside the 128-byte window, at 128 it escapes")
    add("fallback", "exact-lengths", E_S1, {"s1/mime/mime.cache": b64(empty_magic)},
        [(None, b"a" * 127), (None, b"a" * 128), (None, b"a" * 129), (None, b"a")],
        want=[(0, "text/plain", 0), (1, "text/plain", 0), (2, "text/plain", 0),
              (3, "text/plain", 0)])
    add("fallback", "no-name-type-binary", E_S1, {"s1/mime/mime.cache": b64(nomatch)},
        [("x.bin", b"\x00\x01"), ("x.bin", b"ok text\n")],
        want=[(0, "application/octet-stream", 1), (1, "text/plain", 0)],
        note="name with no type behaves like name NULL except the desktop rewrite")
    add("fallback", "non-matching-rule", E_S1, {"s1/mime/mime.cache": b64(nomatch)},
        [(None, b"Z"), (None, b"ZZ"), (None, b"ZZZ"), (None, b"aZZb")],
        want=[(0, "text/plain", 0), (1, "app/zz", 0), (2, "app/zz", 0),
              (3, "text/plain", 0)],
        note="rule holds only from its range start; window [0,1) cannot reach aZZb")
    add("fallback", "no-magic-section-entries", E_S1,
        {"s1/mime/mime.cache": b64(empty_magic)},
        [(None, b"\x01\x02"), (None, b"text\n")],
        want=[(0, "application/octet-stream", 1), (1, "text/plain", 0)])
    add("fallback", "tab-heavy", E_S1, {"s1/mime/mime.cache": b64(empty_magic)},
        [(None, b"\t\t\t\n"), (None, b"a\rb\nc\td\n"), (None, b"\x0e\x0f text")],
        want=[(0, "text/plain", 0), (1, "text/plain", 0),
              (2, "application/octet-stream", 1)])
    add("fallback", "mixed-text-binary", E_S1, {"s1/mime/mime.cache": b64(nomatch)},
        [(None, b"word " * 40 + b"\x02"), (None, b"\x02" + b"word " * 40),
         (None, b"word " * 25)],
        want=[(0, "text/plain", 0), (1, "application/octet-stream", 1),
              (2, "text/plain", 0)],
        note="binary byte beyond byte 128 does not matter; at byte 0 it does")


# ---------------------------------------------------------------- class: lltext

def add_lltext():
    empty_magic, _ = build_cache()
    rule, _ = build_cache(magic=[(1, "app/lo", [ml(0, 1, b"BIN")])])
    add("lltext", "backspace-ok", E_S1, {"s1/mime/mime.cache": b64(empty_magic)},
        [(None, b"ab\x08cd"), (None, b"\x08\x08")],
        want=[(0, "text/plain", 0), (1, "text/plain", 0)],
        note="\\b is exempt even though it fails the binary check")
    add("lltext", "vt-binary", E_S1, {"s1/mime/mime.cache": b64(empty_magic)},
        [(None, b"ab\x0bcd"), (None, b"text\x0bmore text here\n"), (None, b"\x0b")],
        want=[(0, "application/octet-stream", 1), (1, "application/octet-stream", 1),
              (2, "application/octet-stream", 1)],
        note="0x0b VT: oracle says binary (g_ascii_isspace table quirk); "
             "the candidate treats VT as text - known deviation")
    add("lltext", "ff-text", E_S1, {"s1/mime/mime.cache": b64(empty_magic)},
        [(None, b"a\x0cb\n"), (None, b"\x0c\x0cpage\x0c")],
        want=[(0, "text/plain", 0), (1, "text/plain", 0)],
        note="0x0c FF is space for g_ascii_isspace -> passes looks_like_text")
    add("lltext", "tab-lf-cr-ok", E_S1, {"s1/mime/mime.cache": b64(empty_magic)},
        [(None, b"a\tb\nc\rd\n")],
        want=[(0, "text/plain", 0)])
    add("lltext", "del-alone", E_S1, {"s1/mime/mime.cache": b64(empty_magic)},
        [(None, b"a\x7fb\n"), (None, b"\x7f\x7f\x7f")],
        want=[(0, "text/plain", 0), (1, "text/plain", 0)],
        note="sniffed is TEXTPLAIN (not UNKNOWN) so looks_like_text never runs")
    add("lltext", "del-with-ctrl", E_S1, {"s1/mime/mime.cache": b64(empty_magic)},
        [(None, b"\x7f\x01"), (None, b"\x01\x7f")],
        want=[(0, "application/octet-stream", 1), (1, "application/octet-stream", 1)],
        note="now sniffed is UNKNOWN and looks_like_text rejects 0x7f")
    add("lltext", "ctrl-14-31", E_S1, {"s1/mime/mime.cache": b64(empty_magic)},
        [(None, b"a\x1eb\n"), (None, b"a\x1fb\n"), (None, b"a\x00b\n"),
         (None, b"a\x07b\n")],
        want=[(0, "application/octet-stream", 1), (1, "application/octet-stream", 1),
              (2, "application/octet-stream", 1), (3, "application/octet-stream", 1)])
    add("lltext", "rule-beats-lltext", E_S1, {"s1/mime/mime.cache": b64(rule)},
        [(None, b"BIN\x0b\x00\n"), (None, b"BIN ok\n")],
        want=[(0, "app/lo", 0), (1, "app/lo", 0)],
        note="a magic match means the fallback (and looks_like_text) never runs")


# ---------------------------------------------------------------- class: order

def add_order():
    a_then_b, ib = build_cache(magic=[(50, "app/one", [ml(0, 1, b"HI")]),
                                      (90, "app/two", [ml(0, 1, b"HI")])])
    b_then_a, _ = build_cache(magic=[(90, "app/two", [ml(0, 1, b"HI")]),
                                     (50, "app/one", [ml(0, 1, b"HI")])])
    eq, _ = build_cache(magic=[(50, "app/aa", [ml(0, 1, b"HI")]),
                               (50, "app/bb", [ml(0, 1, b"HI")])])
    oct_str, _ = build_cache(magic=[(0, "application/octet-stream", [ml(0, 1, b"HI")])])
    oct_first, _ = build_cache(magic=[(0, "application/octet-stream", [ml(0, 1, b"HI")]),
                                      (90, "app/hi", [ml(0, 1, b"HI")])])
    neg_first, _ = build_cache(magic=[(0xFFFFFFFF, "app/neg", [ml(0, 1, b"HI")]),
                                      (90, "app/hi", [ml(0, 1, b"HI")])])
    sec_ml, _ = build_cache(magic=[(50, "app/first", [ml(0, 1, b"NO"), ml(0, 1, b"HI")]),
                                   (90, "app/second", [ml(0, 1, b"HI")])])
    third, _ = build_cache(magic=[(90, "app/nomatch", [ml(0, 1, b"QQ")]),
                                  (10, "app/mid", [ml(0, 1, b"HI")]),
                                  (95, "app/last", [ml(0, 1, b"HI")])])
    add("order", "cache-order-beats-prio", E_S1, {"s1/mime/mime.cache": b64(a_then_b)},
        [(None, b"HI")], want=[(0, "app/one", 0)], note="first matching entry wins at p50")
    add("order", "swapped-high-prio-first", E_S1, {"s1/mime/mime.cache": b64(b_then_a)},
        [(None, b"HI")], want=[(0, "app/two", 0)])
    add("order", "equal-prio-first", E_S1, {"s1/mime/mime.cache": b64(eq)},
        [(None, b"HI")], want=[(0, "app/aa", 0)])
    add("order", "prio0-octet-string-alone", E_S1, {"s1/mime/mime.cache": b64(oct_str)},
        [(None, b"HI"), (None, b"\x01\x02")],
        want=[(0, "text/plain", 0), (1, "application/octet-stream", 1)],
        note="prio 0 never replaces; a cache-octet-stream is not the UNKNOWN constant "
             "but the fallback decides the answer anyway")
    add("order", "prio0-first-entry-swallows", E_S1,
        {"s1/mime/mime.cache": b64(oct_first)},
        [(None, b"HI")], want=[(0, "text/plain", 0)],
        note="first MATCH (prio 0) is the cache answer; the p90 entry is never consulted")
    add("order", "negative-first-entry-swallows", E_S1,
        {"s1/mime/mime.cache": b64(neg_first)},
        [(None, b"HI")], want=[(0, "text/plain", 0)],
        note="prio -1 matches first and is swallowed (not > 0)")
    add("order", "second-matchlet-of-first-entry", E_S1,
        {"s1/mime/mime.cache": b64(sec_ml)},
        [(None, b"HI")], want=[(0, "app/first", 0)])
    add("order", "third-entry-ignored", E_S1, {"s1/mime/mime.cache": b64(third)},
        [(None, b"HI")], want=[(0, "app/mid", 0)],
        note="p95 entry after the first match never wins within one cache")
    add("order", "entry-order-binary", E_S1, {"s1/mime/mime.cache": b64(a_then_b)},
        [(None, b"HI\x01")], want=[(0, "app/one", 0)],
        note="binary tail; the first entry still wins in cache order")


# ---------------------------------------------------------------- class: prio

def add_prio():
    def one(p, val=b"HI", mime="app/x"):
        blob, _ = build_cache(magic=[(p, mime, [ml(0, 1, val)])])
        return blob
    def two_with(p, mime="app/x", val=b"HI"):
        blob, _ = build_cache(globs=[("*.two", "app/one", 50), ("*.two", "app/two", 50)],
                              magic=[(p, mime, [ml(0, 1, val)])])
        return blob
    add("prio", "p0-never-wins", E_S1, {"s1/mime/mime.cache": b64(one(0))},
        [(None, b"HI"), (None, b"\x01\x02")],
        want=[(0, "text/plain", 0), (1, "application/octet-stream", 1)])
    oct_cache, _ = build_cache(
        magic=[(0, "application/octet-stream", [ml(0, 1, b"\x01\x02")])])
    add("prio", "p0-octet-string", E_S1, {"s1/mime/mime.cache": b64(oct_cache)},
        [(None, b"\x01\x02"), (None, b"text")],
        want=[(0, "application/octet-stream", 1), (1, "text/plain", 0)],
        note="cache string application/octet-stream is not the UNKNOWN constant, but "
             "prio 0 swallows it and the fallback answers")
    add("prio", "p1-wins", E_S1, {"s1/mime/mime.cache": b64(one(1))},
        [(None, b"HI")], want=[(0, "app/x", 0)])
    add("prio", "p79-tiebreak-nosubclass", E_S1,
        {"s1/mime/mime.cache": b64(two_with(79))},
        [("x.two", b"HI")], want=[(0, "app/one", 1)],
        note="two name types; sniff prio < 80, no name type subclasses app/x -> "
             "first, uncertain")
    add("prio", "p80-outright", E_S1, {"s1/mime/mime.cache": b64(two_with(80))},
        [("x.two", b"HI")], want=[(0, "app/x", 0)])
    add("prio", "p100-outright", E_S1, {"s1/mime/mime.cache": b64(two_with(100))},
        [("x.two", b"HI")], want=[(0, "app/x", 0)])
    add("prio", "p-neg-min-never", E_S1,
        {"s1/mime/mime.cache": b64(two_with(0x80000000))},
        [(None, b"HI"), ("x.two", b"HI")],
        want=[(0, "text/plain", 0), (1, "app/one", 1)],
        note="prio -2^31 never beats the 0 baseline: the sniffed side falls back and "
             "the two name types get no help -> first, uncertain")
    add("prio", "p-neg-1-wins", E_S1, {"s1/mime/mime.cache": b64(two_with(0xFFFFFFFF))},
        [("x.two", b"HI")], want=[(0, "app/one", 1)],
        note="prio -1 is NOT > 0: the rule is swallowed; the fallback TEXTPLAIN gives "
             "the name types no help -> first, uncertain")
    add("prio", "p-int-max", E_S1, {"s1/mime/mime.cache": b64(one(0x7FFFFFFF))},
        [(None, b"HI")], want=[(0, "app/x", 0)])
    add("prio", "p79-tiebreak-subclass", E_S1,
        {"s1/mime/mime.cache": b64(two_with(79, mime="app/one"))},
        [("x.two", b"HI")], want=[(0, "app/one", 0)],
        note="sniffed app/one, first name type app/one: equal -> subclass tie-break "
             "picks it, certain")


# ---------------------------------------------------------------- class: multicache

def add_multicache():
    t1, _ = build_cache(magic=[(50, "app/t1", [ml(0, 1, b"HI")])])
    t2, _ = build_cache(magic=[(50, "app/t2", [ml(0, 1, b"HI")])])
    t2b, _ = build_cache(magic=[(51, "app/t2", [ml(0, 1, b"HI")])])
    none2, _ = build_cache(magic=[(50, "app/none", [ml(0, 1, b"QQ")])])
    neg1, _ = build_cache(magic=[(0xFFFFFFFF, "app/neg", [ml(0, 1, b"HI")])])
    p1c2, _ = build_cache(magic=[(1, "app/p1", [ml(0, 1, b"HI")])])
    # cross-cache parent chain: c2 has child->mid, c1 has mid->base
    c1_chain, _ = build_cache(magic=[(50, "app/base", [ml(0, 1, b"BA")])],
                              parents=[("app/mid", ["app/base"])])
    c2_chain, _ = build_cache(globs=[("*.child", "app/child", 50), ("*.child", "app/other", 50)],
                              parents=[("app/child", ["app/mid"])])
    # alias in c2 for a sniffed string stored in c1
    c1_aj, _ = build_cache(magic=[(50, "image/x-jpg", [ml(0, 1, b"JP")])])
    c2_aj, _ = build_cache(aliases=[("image/x-jpg", "image/jpeg")],
                           globs=[("*.jpg", "image/jpeg", 50), ("*.jpg", "image/zzz", 50)])
    add("multicache", "equal-prio-first-dir", E_S1_S2,
        {"s1/mime/mime.cache": b64(t1), "s2/mime/mime.cache": b64(t2)},
        [(None, b"HI")], want=[(0, "app/t1", 0)])
    add("multicache", "strictly-greater-second", E_S1_S2,
        {"s1/mime/mime.cache": b64(t1), "s2/mime/mime.cache": b64(t2b)},
        [(None, b"HI")], want=[(0, "app/t2", 0)])
    add("multicache", "first-higher-keeps", E_S1_S2,
        {"s1/mime/mime.cache": b64(t2b), "s2/mime/mime.cache": b64(t1)},
        [(None, b"HI")], want=[(0, "app/t2", 0)])
    add("multicache", "second-no-match", E_S1_S2,
        {"s1/mime/mime.cache": b64(t1), "s2/mime/mime.cache": b64(none2)},
        [(None, b"HI")], want=[(0, "app/t1", 0)])
    add("multicache", "dh-first", E_DH_S1_S2,
        {"dh/mime/mime.cache": b64(t1), "s1/mime/mime.cache": b64(t2)},
        [(None, b"HI")], want=[(0, "app/t1", 0)],
        note="XDG_DATA_HOME dir comes first")
    add("multicache", "dh-lower-prio", E_DH_S1_S2,
        {"dh/mime/mime.cache": b64(t1), "s1/mime/mime.cache": b64(t2b)},
        [(None, b"HI")], want=[(0, "app/t2", 0)])
    add("multicache", "negative-then-p1", E_S1_S2,
        {"s1/mime/mime.cache": b64(neg1), "s2/mime/mime.cache": b64(p1c2)},
        [(None, b"HI")], want=[(0, "app/p1", 0)],
        note="-1 < 1: the second cache's p1 answer replaces")
    add("multicache", "negative-only-fallback", E_S1_S2,
        {"s1/mime/mime.cache": b64(neg1), "s2/mime/mime.cache": b64(none2)},
        [(None, b"HI")], want=[(0, "text/plain", 0)],
        note="negative match is swallowed, second cache does not match -> fallback")
    add("multicache", "cross-cache-parent-chain", E_S1_S2,
        {"s1/mime/mime.cache": b64(c1_chain), "s2/mime/mime.cache": b64(c2_chain)},
        [("x.child", b"BA"), ("x.other", b"BA")],
        want=[(0, "app/child", 0), (1, "app/base", 0)],
        note="x.child resolves to two types (app/child, app/other); subclass walks "
             "parent lists of every cache: child->mid (c2), mid->base (c1) -> child "
             "picked; x.other has no glob -> sniffed app/base certain")
    add("multicache", "cross-cache-alias", E_S1_S2,
        {"s1/mime/mime.cache": b64(c1_aj), "s2/mime/mime.cache": b64(c2_aj)},
        [("x.jpg", b"JP"), ("x.zz", b"JP")],
        want=[(0, "image/jpeg", 0), (1, "image/x-jpg", 0)],
        note="tie-break: unalias(name type image/jpeg)==image/jpeg; unalias(sniffed "
             "image/x-jpg) via c2 alias -> equal; x.zz has no glob -> the raw sniffed "
             "alias string is returned certain")


# ---------------------------------------------------------------- class: range

def add_range():
    def rng(start, length, val=b"AB", mime="app/r", prio=50):
        blob, _ = build_cache(magic=[(prio, mime, [ml(start, length, val)])])
        return blob
    add("range", "window-0-3", E_S1, {"s1/mime/mime.cache": b64(rng(0, 3))},
        [(None, b"AB"), (None, b"XAB"), (None, b"XXAB"), (None, b"XXXAB"),
         (None, b"ABAB")],
        want=[(0, "app/r", 0), (1, "app/r", 0), (2, "app/r", 0),
              (3, "text/plain", 0), (4, "app/r", 0)],
        note="i in [0,3): positions 0,1,2; XXXAB has AB at 3, outside the window")
    add("range", "window-at-end", E_S1, {"s1/mime/mime.cache": b64(rng(2, 1))},
        [(None, b"..AB"), (None, b".AB."), (None, b"..AB.")],
        want=[(0, "app/r", 0), (1, "text/plain", 0),
              (2, "app/r", 0)],
        note="value may end exactly at data end; single position i=2")
    add("range", "value-runs-past-end", E_S1, {"s1/mime/mime.cache": b64(rng(3, 1))},
        [(None, b"abcAB"), (None, b"abcA")],
        want=[(0, "app/r", 0), (1, "text/plain", 0)],
        note="i+value_length > len stops the scan with FALSE")
    add("range", "length-zero", E_S1, {"s1/mime/mime.cache": b64(rng(0, 0))},
        [(None, b"AB"), (None, b"\x01")],
        want=[(0, "text/plain", 0), (1, "application/octet-stream", 1)],
        note="empty window: loop never runs")
    vl0, _ = build_cache(magic=[(50, "app/vl0", [ml(0, 2, b"")])])
    add("range", "value-length-zero", E_S1, {"s1/mime/mime.cache": b64(vl0)},
        [(None, b"AB"), (None, b"q"), (None, b"\x00\x00")],
        want=[(0, "app/vl0", 0), (1, "app/vl0", 0), (2, "app/vl0", 0)],
        note="0-byte value memcmp == 0 holds at any scanned position")
    vl0_end, _ = build_cache(magic=[(50, "app/vl0", [ml(1, 1, b"")])])
    add("range", "value-length-zero-at-len", E_S1, {"s1/mime/mime.cache": b64(vl0_end)},
        [(None, b"q")],
        want=[(0, "app/vl0", 0)],
        note="i == len passes i+value_length > len (0-byte value)")
    add("range", "window-past-data", E_S1, {"s1/mime/mime.cache": b64(rng(1, 2))},
        [(None, b"A")],
        want=[(0, "text/plain", 0)],
        note="i=1: 1+2 > 1 -> immediate FALSE")
    add("range", "single-byte-value", E_S1,
        {"s1/mime/mime.cache": b64(rng(3, 1, b"Z", "app/z"))},
        [(None, b"abcZ"), (None, b"abcZZ"), (None, b"Zabc")],
        want=[(0, "app/z", 0), (1, "app/z", 0), (2, "text/plain", 0)],
        note="window [3,4): last byte; 'abcZZ' matches at i=3 before window ends")
    add("range", "window-past-end-early-match", E_S1,
        {"s1/mime/mime.cache": b64(rng(0, 10))},
        [(None, b"AB")], want=[(0, "app/r", 0)],
        note="window larger than data: first position already matches")


# ---------------------------------------------------------------- class: mask

def add_mask():
    def masked(val, mask, start=0, length=1, mime="app/m", prio=50):
        blob, _ = build_cache(magic=[(prio, mime, [ml(start, length, val, mask)])])
        return blob
    add("mask", "ff-equals-none", E_S1,
        {"s1/mime/mime.cache": b64(masked(b"AB", b"\xff\xff"))},
        [(None, b"AB"), (None, b"aB")],
        want=[(0, "app/m", 0), (1, "text/plain", 0)])
    add("mask", "high-nibble", E_S1,
        {"s1/mime/mime.cache": b64(masked(b"\x40\x40", b"\xf0\xf0"))},
        [(None, b"\x4f\x4a"), (None, b"\x40\x40"), (None, b"\x3f\x40"),
         (None, b"\xc0\x40")],
        want=[(0, "app/m", 0), (1, "app/m", 0), (2, "text/plain", 0),
              (3, "text/plain", 0)],
        note="only the high nibbles compare; non-matching data falls back")
    add("mask", "zero-mask-any", E_S1,
        {"s1/mime/mime.cache": b64(masked(b"AB", b"\x00\x00"))},
        [(None, b"zz"), (None, b"\x01\x02"), (None, b"AB")],
        want=[(0, "app/m", 0), (1, "app/m", 0), (2, "app/m", 0)],
        note="all-zero mask makes every byte compare equal")
    add("mask", "second-byte-only", E_S1,
        {"s1/mime/mime.cache": b64(masked(b"AB", b"\x00\xff"))},
        [(None, b"xB"), (None, b"xx"), (None, b"xBx")],
        want=[(0, "app/m", 0), (1, "text/plain", 0), (2, "app/m", 0)])
    add("mask", "past-data-length", E_S1,
        {"s1/mime/mime.cache": b64(masked(b"ABCD", b"\xff\xff\xff\xff"))},
        [(None, b"AB")],
        want=[(0, "text/plain", 0)],
        note="i+value_length > len before any masked byte is read")
    add("mask", "mask-rescues-mismatch", E_S1,
        {"s1/mime/mime.cache": b64(masked(b"\x41\x41", b"\xf0\x0f"))},
        [(None, b"\x4f\xf1")],
        want=[(0, "app/m", 0)],
        note="0x4f&0xf0==0x41&0xf0 and 0xf1&0x0f==0x41&0x0f")
    add("mask", "mask-window", E_S1,
        {"s1/mime/mime.cache": b64(masked(b"Z", b"\x0f", start=2, length=2))},
        [(None, b"aa\x05aq"), (None, b"aaaZ")],
        want=[(0, "application/octet-stream", 1), (1, "app/m", 0)],
        note="window [2,4): 'Z'&0x0f==0x0a matches 'Z' itself but not 0x05")
    add("mask", "odd-mask-offset", E_S1,
        {"s1/mime/mime.cache": b64(masked(b"AB", b"\xff\x0f"))},
        [(None, b"A\xa2")], want=[(0, "app/m", 0)],
        note="value/mask bytes need no alignment; 0xa2&0x0f == 'B'&0x0f")


# ---------------------------------------------------------------- class: nest

def add_nest():
    def two_level(parent_val, child_val, child_start=4, pmask=None, cmask=None):
        return build_cache(magic=[(50, "app/n", [
            ml(0, 1, parent_val, pmask, [ml(child_start, 1, child_val, cmask)])])])
    ok3, _ = build_cache(magic=[(50, "app/n3", [
        ml(0, 1, b"A", None, [ml(1, 1, b"B", None, [ml(2, 1, b"C")])])])])
    fail_mid, _ = build_cache(magic=[(50, "app/n3", [
        ml(0, 1, b"A", None, [ml(1, 1, b"X", None, [ml(2, 1, b"C")])])])])
    anyc, _ = build_cache(magic=[(50, "app/any", [
        ml(0, 1, b"N", None, [ml(4, 1, b"X"), ml(4, 1, b"Y")])])])
    boundskid_raw, ik = build_cache(magic=[(50, "app/bk", [
        ml(0, 1, b"P", None, [ml(4, 1, b"Q")])])])
    boundskid_raw = bytearray(boundskid_raw)
    # corrupt the parent's children count so the child list fails the bounds check
    parent_rec = ik["entries"][0]["matchlets"][0]["_rec"]
    patch(boundskid_raw, parent_rec + 24, 0xFFFFFF)
    add("nest", "parent-child-hold", E_S1, {"s1/mime/mime.cache": b64(two_level(b"P", b"Q")[0])},
        [(None, b"P\x00\x00\x00Q")], want=[(0, "app/n", 0)])
    add("nest", "child-fails", E_S1, {"s1/mime/mime.cache": b64(two_level(b"P", b"Q")[0])},
        [(None, b"P\x00\x00\x00R"), (None, b"Q\x00\x00\x00Q")],
        want=[(0, "application/octet-stream", 1), (1, "application/octet-stream", 1)],
        note="parent alone is not enough; child without parent neither")
    add("nest", "three-levels-hold", E_S1, {"s1/mime/mime.cache": b64(ok3)},
        [(None, b"ABC")], want=[(0, "app/n3", 0)])
    add("nest", "three-levels-mid-fails", E_S1, {"s1/mime/mime.cache": b64(fail_mid)},
        [(None, b"ABC"), (None, b"AXC")],
        want=[(0, "text/plain", 0), (1, "app/n3", 0)],
        note="fail_mid's mid value is X: ABC fails at level 2, AXC holds all three")
    add("nest", "any-child-holds", E_S1, {"s1/mime/mime.cache": b64(anyc)},
        [(None, b"N\x00\x00\x00X"), (None, b"N\x00\x00\x00Y"),
         (None, b"N\x00\x00\x00Z")],
        want=[(0, "app/any", 0), (1, "app/any", 0),
              (2, "application/octet-stream", 1)],
        note="children are an ANY group")
    add("nest", "deep-any", E_S1,
        {"s1/mime/mime.cache": b64(build_cache(magic=[(50, "app/d", [
            ml(0, 1, b"1", None, [ml(1, 1, b"2", None, [ml(2, 1, b"3"), ml(2, 1, b"4")]),
                                   ml(1, 1, b"5")])])])[0])},
        [(None, b"123"), (None, b"124"), (None, b"1x5"), (None, b"15x")],
        want=[(0, "app/d", 0), (1, "app/d", 0), (2, "text/plain", 0),
              (3, "app/d", 0)],
        note="grandchildren are any-of inside their child; child 5 wants 5 at index 1")
    add("nest", "child-at-offset", E_S1,
        {"s1/mime/mime.cache": b64(two_level(b"P", b"Q", child_start=10)[0])},
        [(None, b"P" + b"\x00" * 9 + b"Q"), (None, b"P" + b"\x00" * 9 + b"R")],
        want=[(0, "app/n", 0), (1, "application/octet-stream", 1)])
    add("nest", "child-bounds-corrupt", E_S1, {"s1/mime/mime.cache": b64(boundskid_raw)},
        [(None, b"P\x00\x00\x00Q")],
        want=[(0, "application/octet-stream", 1)],
        note="children list fails OUT_OF_BOUNDS -> matchlet false BEFORE its value test")
    add("nest", "masked-parent-child", E_S1,
        {"s1/mime/mime.cache": b64(two_level(b"\x10", b"Q", pmask=b"\xf0")[0])},
        [(None, b"\x1f\x00\x00\x00Q"), (None, b"\x0f\x00\x00\x00Q")],
        want=[(0, "app/n", 0), (1, "application/octet-stream", 1)])


# ---------------------------------------------------------------- class: bounds

def add_bounds():
    # in-page corruptions (answerable) and past-page corruptions (oracle crashes -> UNSUPPORTED)
    base, ik = build_cache(magic=[(50, "app/x", [ml(0, 1, b"HI")])])
    size = len(base)
    # b1 unaligned magic list pointer
    c = bytearray(base); patch(c, 24, 101)
    add("bounds", "magic-list-unaligned", E_S1, {"s1/mime/mime.cache": b64(bytes(c))},
        [(None, b"HI")], want=[(0, "text/plain", 0)],
        note="OUT_OF_BOUNDS rejects unaligned list offset")
    # b2 magic list pointer past EOF but inside the zero-filled last page
    c = bytearray(base); patch(c, 24, size + 60)
    add("bounds", "magic-list-in-page", E_S1, {"s1/mime/mime.cache": b64(bytes(c))},
        [(None, b"HI")], want=[(0, "text/plain", 0)],
        note="offset > size -> OUT_OF_BOUNDS -> no rules -> fallback")
    # b3 matchlet list offset past EOF in-page
    c = bytearray(base)
    e0 = ik["entries"][0]["off"]
    patch(c, e0 + 12, size + 60)
    add("bounds", "matchlets-in-page", E_S1, {"s1/mime/mime.cache": b64(bytes(c))},
        [(None, b"HI")], want=[(0, "text/plain", 0)])
    # b4 value offset past EOF in-page -> zeros value
    c = bytearray(base)
    rec = ik["entries"][0]["matchlets"][0]["_rec"]
    patch(c, rec + 16, size + 60)
    add("bounds", "value-zeros-ghost", E_S1, {"s1/mime/mime.cache": b64(bytes(c))},
        [(None, b"\x00\x00\x00\x00xy"), (None, b"HI")],
        want=[(0, "app/x", 0), (1, "text/plain", 0)],
        note="value reads as 2 zero bytes from the zero-filled page")
    # b5 mask offset past EOF in-page -> all-zero mask matches any
    c = bytearray(base)
    rec = ik["entries"][0]["matchlets"][0]["_rec"]
    patch(c, rec + 20, size + 60)
    add("bounds", "mask-zeros-any", E_S1, {"s1/mime/mime.cache": b64(bytes(c))},
        [(None, b"HI"), (None, b"zz")],
        want=[(0, "app/x", 0), (1, "app/x", 0)],
        note="(v&0)==(d&0) for every byte")
    # b6 mimetype offset past EOF in-page -> empty type string
    c = bytearray(base)
    e0 = ik["entries"][0]["off"]
    patch(c, e0 + 4, size + 60)
    add("bounds", "mime-offset-empty-string", E_S1, {"s1/mime/mime.cache": b64(bytes(c))},
        [(None, b"HI"), ("x.two", b"HI")],
        want=[(0, "", 0), (1, "", 0)],
        note="type reads as \"\" (zeros); never the UNKNOWN constant")
    # b7 mimetype offset far past the mapping -> strdup faults -> UNSUPPORTED
    c = bytearray(base)
    patch(c, e0 + 4, 0x7F000000)
    add("bounds", "mime-offset-far", E_S1, {"s1/mime/mime.cache": b64(bytes(c))},
        [(None, b"HI")], want=None,
        note="oracle faults reading the type string; tool must refuse (exit 3)")
    # b8 value offset far past the mapping -> read faults -> UNSUPPORTED
    c = bytearray(base)
    rec = ik["entries"][0]["matchlets"][0]["_rec"]
    patch(c, rec + 16, 0x7F000000)
    add("bounds", "value-offset-far", E_S1, {"s1/mime/mime.cache": b64(bytes(c))},
        [(None, b"HI")], want=None,
        note="oracle faults reading value bytes; tool must refuse (exit 3)")
    # b9 mask offset far past the mapping -> UNSUPPORTED
    c = bytearray(base)
    patch(c, rec + 20, 0x7F000000)
    add("bounds", "mask-offset-far", E_S1, {"s1/mime/mime.cache": b64(bytes(c))},
        [(None, b"HI")], want=None)
    # b10 children offset in-page past EOF -> OUT_OF_BOUNDS -> matchlet false
    pk, pk_i = build_cache(magic=[(50, "app/pk", [ml(0, 1, b"P", None, [ml(4, 1, b"Q")])])])
    c = bytearray(pk)
    prec = pk_i["entries"][0]["matchlets"][0]["_rec"]
    patch(c, prec + 28, len(pk) + 60)
    add("bounds", "children-in-page", E_S1, {"s1/mime/mime.cache": b64(bytes(c))},
        [(None, b"P\x00\x00\x00Q")], want=[(0, "application/octet-stream", 1)],
        note="child list fails the bounds check before the parent value test")
    # b11 children list straddling EOF: co = size-32, n=1 (crafted trailing record)
    c = bytearray(pk)
    prec = pk_i["entries"][0]["matchlets"][0]["_rec"]
    val_at = len(c) + 32
    child = (u32(4) + u32(1) + u32(1) + u32(1) + u32(val_at) + u32(0)
             + u32(0) + u32(0))
    c.extend(child)
    c.extend(b"Q")
    patch(c, prec + 24, 1)          # n_children = 1 (already 1)
    patch(c, prec + 28, len(c) - 33)  # co = size-32
    add("bounds", "children-straddle-eof", E_S1, {"s1/mime/mime.cache": b64(bytes(c))},
        [(None, b"P\x00\x00\x00Q")], want=[(0, "app/pk", 0)],
        note="co=size-32 with n=1 passes OUT_OF_BOUNDS ((size-co)//32 == 1)")


# ---------------------------------------------------------------- class: wrap

def add_wrap():
    def w(start, length, val=b"AB", mime="app/w", vl=None, value=None):
        v = value if value is not None else val
        blob, ik = build_cache(magic=[(50, mime, [ml(start, length, v)])])
        if vl is not None:
            blob = bytearray(blob)
            rec = ik["entries"][0]["matchlets"][0]["_rec"]
            patch(blob, rec + 12, vl)
        return bytes(blob)
    add("wrap", "rs-rl-wrap-empty", E_S1,
        {"s1/mime/mime.cache": b64(w(0xFFFFFFFF, 2))},
        [(None, b"AB"), (None, b"\x00\x00\x00\x00AB")],
        want=[(0, "text/plain", 0), (1, "application/octet-stream", 1)],
        note="range_start+range_length wraps to 1: window [0xFFFFFFFF,1) is empty")
    add("wrap", "rs-rl-wrap-empty-2", E_S1,
        {"s1/mime/mime.cache": b64(w(0xFFFFFFFE, 4))},
        [(None, b"AB")], want=[(0, "text/plain", 0)])
    add("wrap", "length-zero", E_S1, {"s1/mime/mime.cache": b64(w(0, 0))},
        [(None, b"AB")], want=[(0, "text/plain", 0)])
    add("wrap", "rl-huge-wrap", E_S1, {"s1/mime/mime.cache": b64(w(5, 0xFFFFFFFB))},
        [(None, b"AB")], want=[(0, "text/plain", 0)],
        note="5 + 0xFFFFFFFB wraps to 0: empty window")
    add("wrap", "rs-max-rl-max", E_S1,
        {"s1/mime/mime.cache": b64(w(0xFFFFFFFF, 0xFFFFFFFF))},
        [(None, b"AB")], want=[(0, "text/plain", 0)])
    add("wrap", "vl-m32-at-i0", E_S1,
        {"s1/mime/mime.cache": b64(w(0, 1, value=b"Z", vl=0xFFFFFFFF))},
        [(None, b"AZ")],
        want=[(0, "text/plain", 0)],
        note="i+value_length == 2^32-1: no wrap; C and tool both stop on i+vl > len")
    add("wrap", "vl-m32-at-i1-ub", E_S1,
        {"s1/mime/mime.cache": b64(w(1, 1, value=b"Z", vl=0xFFFFFFFF))},
        [("x.a", b"AY")],
        want=[(0, "text/plain", 0)],
        note="i+value_length wraps to 0: C memcmps with a huge count but the first "
             "byte already differs ('Z' vs 'Y'), so GLib answers the fallback; the "
             "tool refuses (i+value_length passes 2^32). EXPECTED DISAGREEMENT")
    add("wrap", "rs-1-rl-2-wrap", E_S1,
        {"s1/mime/mime.cache": b64(w(0xFFFFFFFF, 0xFFFFFFFF))},
        [(None, b"AB"), (None, b"")],
        want=[(0, "text/plain", 0), (1, "application/x-zerosize", 0)])


# ---------------------------------------------------------------- class: desktop

def add_desktop():
    d80, _ = build_cache(magic=[(80, "application/x-desktop", [ml(0, 1, b"[Desktop Entry]")])])
    d40, _ = build_cache(magic=[(40, "application/x-desktop", [ml(0, 1, b"[Desktop Entry]")])])
    d0, _ = build_cache(magic=[(0, "application/x-desktop", [ml(0, 1, b"[Desktop Entry]")])])
    empty, _ = build_cache()
    two, _ = build_cache(globs=[("*.two", "app/one", 50), ("*.two", "app/two", 50)],
                         magic=[(80, "application/x-desktop", [ml(0, 1, b"[Desktop Entry]")])])
    dsk = b"[Desktop Entry]\nType=Application\nName=x\nExec=x\n"
    dtxt = {"s1/mime/mime.cache": b64(d80)}
    gtxt, _ = build_cache(globs=[("*.txt", "txt/sub", 50)],
                          magic=[(80, "application/x-desktop", [ml(0, 1, b"[Desktop Entry]")])])
    add("desktop", "no-name", E_S1, dtxt,
        [(None, dsk), (None, b"[Desktop Entry]")],
        want=[(0, "application/x-desktop", 0), (1, "application/x-desktop", 0)])
    add("desktop", "with-txt-name", E_S1, dtxt,
        [("a.txt", dsk), ("a.txt", b"[Desktop Entry]")],
        want=[(0, "text/plain", 0), (1, "text/plain", 0)],
        note="filename known -> x-desktop sniff is rewritten to text/plain")
    add("desktop", "with-typeless-name", E_S1, dtxt,
        [("zz.nomatch", dsk)],
        want=[(0, "text/plain", 0)],
        note="even a name with no type triggers the desktop rewrite")
    add("desktop", "own-extension", E_S1,
        {"s1/mime/mime.cache": b64(build_cache(globs=[("*.desktop", "application/x-desktop", 50)],
                                               magic=[(80, "application/x-desktop",
                                                      [ml(0, 1, b"[Desktop Entry]")])])[0])},
        [("x.desktop", dsk)], want=[(0, "application/x-desktop", 0)],
        note="exactly one name type: bytes never read")
    add("desktop", "truncated-value", E_S1, dtxt,
        [(None, b"[Desktop Entr"), ("a.txt", b"[Desktop EntrX")],
        want=[(0, "text/plain", 0), (1, "text/plain", 0)],
        note="15-byte prefix does not match the 16-byte value")
    add("desktop", "prio40-rewrite", E_S1, {"s1/mime/mime.cache": b64(d40)},
        [(None, dsk), ("a.txt", dsk)],
        want=[(0, "application/x-desktop", 0), (1, "text/plain", 0)],
        note="rewrite is strcmp-based, priority-independent")
    add("desktop", "no-builtin", E_S1, {"s1/mime/mime.cache": b64(empty)},
        [(None, dsk), ("a.txt", dsk)],
        want=[(0, "text/plain", 0), (1, "text/plain", 0)],
        note="no rule: [Desktop Entry] is just text; x-desktop is not built into GLib")
    add("desktop", "prio80-rewritten-outright", E_S1, {"s1/mime/mime.cache": b64(two)},
        [("x.two", dsk)],
        want=[(0, "text/plain", 0)],
        note="rewritten sniffed text/plain still carries prio 80 -> wins outright "
             "over the two name types")
    add("desktop", "prio0-no-win", E_S1, {"s1/mime/mime.cache": b64(d0)},
        [(None, dsk), ("a.txt", dsk)],
        want=[(0, "text/plain", 0), (1, "text/plain", 0)],
        note="prio 0 never wins: fallback text either way")
    add("desktop", "glob-txt-shortcut", E_S1,
        {"s1/mime/mime.cache": b64(gtxt)},
        [("a.txt", dsk)], want=[(0, "txt/sub", 0)])


# ---------------------------------------------------------------- class: name1

def add_name1():
    lit, _ = build_cache(literals=[("Makefile", "txt/make", 50)])
    lit_cs, _ = build_cache(literals=[("Makefile", "txt/make", 50 | 0x100)])
    glo, _ = build_cache(globs=[("*.txt", "txt/sub", 50)])
    cls_glob, _ = build_cache(globs=[("a[0-9].png", "img/num", 50)])
    alias_t, _ = build_cache(aliases=[("text/x-old", "text/x-new")],
                             globs=[("*.old", "text/x-old", 50)],
                             magic=[(90, "text/plain", [ml(0, 1, b"T")])])
    add("name1", "literal", E_S1, {"s1/mime/mime.cache": b64(lit)},
        [("Makefile", b"\x00\x01bin"), ("Makefile", b"")],
        want=[(0, "txt/make", 0), (1, "txt/make", 0)],
        note="one name type: bytes never sniffed, even empty")
    add("name1", "literal-case-sensitive", E_S1, {"s1/mime/mime.cache": b64(lit_cs)},
        [("Makefile", b"x"), ("makefile", b"x"), ("MAKEFILE", b"x")],
        want=[(0, "txt/make", 0), (1, "text/plain", 0), (2, "text/plain", 0)],
        note="cs literal: lowercase name finds nothing (case_sensitive_check is false)")
    add("name1", "suffix-glob", E_S1, {"s1/mime/mime.cache": b64(glo)},
        [("a.txt", b"\x01"), ("A.TXT", b"\x01"), (".txt", b"\x01"),
         ("dir/a.txt", b"\x01")],
        want=[(0, "txt/sub", 0), (1, "txt/sub", 0), (2, "txt/sub", 0),
              (3, "txt/sub", 0)],
        note="lookups run on the lowercased basename; .txt matches *.txt too")
    add("name1", "beats-p90-rule", E_S1,
        {"s1/mime/mime.cache": b64(build_cache(globs=[("*.txt", "txt/sub", 50)],
                                               magic=[(90, "app/hi", [ml(0, 1, b"HI")])])[0])},
        [("a.txt", b"HI")], want=[(0, "txt/sub", 0)],
        note="single name type never consults the bytes")
    add("name1", "class-glob", E_S1, {"s1/mime/mime.cache": b64(cls_glob)},
        [("a5.png", b"x"), ("ax.png", b"x")],
        want=[(0, "img/num", 0), (1, "text/plain", 0)])
    add("name1", "alias-type-shortcut", E_S1, {"s1/mime/mime.cache": b64(alias_t)},
        [("x.old", b"T"), ("x.old", b"other")],
        want=[(0, "text/x-old", 0), (1, "text/x-old", 0)],
        note="the stored (aliased) type is returned verbatim; one type -> no sniff, "
             "so the p90 text/plain rule is never consulted and no unalias happens")
    add("name1", "empty-name", E_S1, {"s1/mime/mime.cache": b64(glo)},
        [("", b"text\n")], want=[(0, "text/plain", 0)],
        note="empty filename -> basename . -> no type -> sniffed")
    add("name1", "dot-and-dotdot", E_S1, {"s1/mime/mime.cache": b64(glo)},
        [(".", b"text\n"), ("..", b"text\n"), ("x.", b"text\n")],
        want=[(0, "text/plain", 0), (1, "text/plain", 0), (2, "text/plain", 0)])
    add("name1", "star-name", E_S1,
        {"s1/mime/mime.cache": b64(build_cache(globs=[("*", "app/all", 50)])[0])},
        [("*", b"x"), ("anything", b"x")],
        want=[(0, "app/all", 0), (1, "app/all", 0)],
        note="literal-looking glob * is an fnmatch glob matching everything")


# ---------------------------------------------------------------- class: name0

def add_name0():
    empty_magic, _ = build_cache()
    g1, _ = build_cache(globs=[("*.txt", "txt/sub", 50)])
    add("name0", "random-name", E_S1, {"s1/mime/mime.cache": b64(empty_magic)},
        [("zzq.qqq", b"text\n"), ("zzq.qqq", b"\x01\x02")],
        want=[(0, "text/plain", 0), (1, "application/octet-stream", 1)])
    add("name0", "empty-name-binary", E_S1, {"s1/mime/mime.cache": b64(empty_magic)},
        [("", b"\x01\x02"), ("", b"")],
        want=[(0, "application/octet-stream", 1), (1, "application/x-zerosize", 0)])
    add("name0", "dot-names", E_S1, {"s1/mime/mime.cache": b64(g1)},
        [(".hidden.txt", b"x"), (".hidden", b"text\n")],
        want=[(0, "txt/sub", 0), (1, "text/plain", 0)],
        note="dotfiles get no special treatment at the guess level")
    add("name0", "star-and-wild", E_S1, {"s1/mime/mime.cache": b64(g1)},
        [("*", b"text\n"), ("*.txt", b"x"), ("?.txt", b"x")],
        want=[(0, "text/plain", 0), (1, "txt/sub", 0), (2, "txt/sub", 0)],
        note="'*.txt' and '?.txt' as NAMES both match the glob *.txt via fnmatch")
    add("name0", "trailing-dot", E_S1, {"s1/mime/mime.cache": b64(g1)},
        [("x.", b"text\n"), ("x..", b"text\n")],
        want=[(0, "text/plain", 0), (1, "text/plain", 0)])
    add("name0", "space-and-dash", E_S1, {"s1/mime/mime.cache": b64(g1)},
        [("a b.txt", b"x"), ("-x.txt", b"x")],
        want=[(0, "txt/sub", 0), (1, "txt/sub", 0)])
    add("name0", "no-type-empty-data", E_S1, {"s1/mime/mime.cache": b64(empty_magic)},
        [("zzq.qqq", b"")], want=[(0, "application/x-zerosize", 0)])
    add("name0", "path-like-name", E_S1, {"s1/mime/mime.cache": b64(g1)},
        [("no/such/dir.txt", b"x"), ("a/b/c", b"text\n")],
        want=[(0, "txt/sub", 0), (1, "text/plain", 0)],
        note="basename is taken before the glob lookup")


# ---------------------------------------------------------------- class: nameN

def add_nameN():
    dup, _ = build_cache(globs=[("*.dup", "app/one", 50), ("*.dup", "app/two", 50)])
    dup_r, _ = build_cache(globs=[("*.dup", "app/one", 50), ("*.dup", "app/two", 50)],
                           magic=[(90, "app/sniff", [ml(0, 1, b"HI")])])
    dup_r79_sub, _ = build_cache(globs=[("*.dup", "app/one", 50), ("*.dup", "app/two", 50)],
                                 magic=[(79, "app/base", [ml(0, 1, b"HI")])],
                                 parents=[("app/two", ["app/base"])])
    many, _ = build_cache(globs=[(f"*.m{i:02d}", f"app/t{i:02d}", 50) for i in range(12)])
    lit_wild, _ = build_cache(literals=[("README", "app/readme", 50)],
                              globs=[("READ*", "app/readwild", 50)])
    oct_pair, _ = build_cache(globs=[("*.sp", "inode/x-foo", 50), ("*.oc", "application/octet-stream", 50)],
                              magic=[(50, "application/octet-stream", [ml(0, 1, b"OC")])])
    two_sub, _ = build_cache(globs=[("*.s", "t/sub1", 50), ("*.s", "t/sub2", 50)],
                             magic=[(50, "t/base", [ml(0, 1, b"S")])],
                             parents=[("t/sub1", ["t/base"]), ("t/sub2", ["t/base"])])
    weights, _ = build_cache(globs=[("*.w", "app/lo", 10), ("*.w", "app/hi", 90)])
    empty_mime, ik = build_cache(globs=[("*.two", "app/one", 50), ("*.two", "app/two", 50)],
                                 magic=[(50, "app/tmp", [ml(0, 1, b"HI")])])
    c = bytearray(empty_mime)
    patch(c, ik["entries"][0]["off"] + 4, len(empty_mime) + 60)
    empty_str = bytes(c)
    add("nameN", "two-same-weight", E_S1, {"s1/mime/mime.cache": b64(dup)},
        [("x.dup", b"text\n")], want=[(0, "app/one", 1)],
        note="conflicts, sniffed text/plain is no help -> first, uncertain")
    add("nameN", "sniff-p90-outright", E_S1, {"s1/mime/mime.cache": b64(dup_r)},
        [("x.dup", b"HI")], want=[(0, "app/sniff", 0)])
    add("nameN", "sniff-p79-subclass", E_S1, {"s1/mime/mime.cache": b64(dup_r79_sub)},
        [("x.dup", b"HI")], want=[(0, "app/two", 0)],
        note="app/two subclasses the sniffed app/base -> picked over app/one")
    add("nameN", "twelve-glob-cache-single-match", E_S1, {"s1/mime/mime.cache": b64(many)},
        [("z.m07", b"\x01\x02"), ("z.m07", b"")],
        want=[(0, "app/t07", 0), (1, "app/t07", 0)],
        note="12-glob cache; only *.m07 matches -> one name type short-circuits, "
             "bytes never sniffed (even empty)")
    many2, _ = build_cache(globs=[("z.m*", f"app/t{i:02d}", 50) for i in range(12)])
    add("nameN", "twelve-types-one-name", E_S1, {"s1/mime/mime.cache": b64(many2)},
        [("z.m07", b"\x01\x02")],
        want=[(0, "app/t00", 1)],
        note="12 matching globs, capped at 10 name types; first wins, uncertain")
    add("nameN", "literal-and-glob", E_S1, {"s1/mime/mime.cache": b64(lit_wild)},
        [("README", b"text\n"), ("READMEX", b"text\n")],
        want=[(0, "app/readme", 0), (1, "app/readwild", 0)],
        note="a literal hit returns ONE type outright (certain); a single glob match "
             "is likewise one type, certain")
    add("nameN", "octet-special-pick", E_S1, {"s1/mime/mime.cache": b64(oct_pair)},
        [("x.sp", b"OC"), ("x.oc", b"OC")],
        want=[(0, "inode/x-foo", 0), (1, "application/octet-stream", 0)],
        note="both inputs have a single name type and short-circuit certain; the "
             "subclass interplay of octet-stream sniffing is pinned in the subclass "
             "class")
    add("nameN", "first-subclass-wins", E_S1, {"s1/mime/mime.cache": b64(two_sub)},
        [("x.s", b"S")], want=[(0, "t/sub1", 0)],
        note="both name types subclass the sniffed base; the first in order is taken")
    add("nameN", "weights-order", E_S1, {"s1/mime/mime.cache": b64(weights)},
        [("x.w", b"text\n")],
        want=[(0, "app/hi", 1)],
        note="types are sorted by weight descending before the first is taken")
    add("nameN", "empty-sniffed-string", E_S1, {"s1/mime/mime.cache": b64(empty_str)},
        [("x.two", b"HI")],
        want=[(0, "app/one", 1)],
        note="corrupt mimetype offset -> sniffed \"\" (p50): not UNKNOWN, <80, "
             "no subclass -> first name type, uncertain")


# ---------------------------------------------------------------- class: subclass

def add_subclass():
    def chain(names, sniffed, sniff_val=b"BA", prio=50):
        parents = [(names[i], [names[i + 1]]) for i in range(len(names) - 1)]
        blob, _ = build_cache(globs=[("*.c", names[0], 50), ("*.c", "other/x", 50)],
                              magic=[(prio, sniffed, [ml(0, 1, sniff_val)])],
                              parents=parents)
        return blob
    add("subclass", "direct-parent", E_S1,
        {"s1/mime/mime.cache": b64(chain(["app/child", "app/base"], "app/base"))},
        [("x.c", b"BA")],
        want=[(0, "app/child", 0)],
        note="two name types (app/child, other/x); only app/child subclasses app/base")
    add("subclass", "grandparent-chain", E_S1,
        {"s1/mime/mime.cache": b64(chain(["app/c1", "app/c2", "app/c3", "app/base"], "app/base"))},
        [("x.c", b"BA")], want=[(0, "app/c1", 0)],
        note="parents resolved transitively over three levels")
    add("subclass", "cycle-exercised", E_S1,
        {"s1/mime/mime.cache": b64(build_cache(
            globs=[("*.c", "app/x", 50), ("*.c", "other/x", 50)],
            magic=[(50, "app/b", [ml(0, 1, b"BA")])],
            parents=[("app/x", ["app/a"]), ("app/a", ["app/b"]), ("app/b", ["app/a"])])[0])},
        [("x.c", b"BA")], want=[(0, "app/x", 0)],
        note="a<->b cycle: the walk hits b (equal) before revisiting a; terminates")
    add("subclass", "cycle-blocks", E_S1,
        {"s1/mime/mime.cache": b64(build_cache(
            globs=[("*.c", "app/y", 50), ("*.c", "other/x", 50)],
            magic=[(50, "app/w", [ml(0, 1, b"BA")])],
            parents=[("app/y", ["app/z"]), ("app/z", ["app/y"])])[0])},
        [("x.c", b"BA")], want=[(0, "app/y", 1)],
        note="closed cycle never reaches app/w -> first, uncertain")
    sup, _ = build_cache(globs=[("*.c", "media/kind", 50), ("*.c", "other/x", 50)],
                         magic=[(50, "media/*", [ml(0, 1, b"BA")])])
    add("subclass", "x-slash-star-supertype", E_S1, {"s1/mime/mime.cache": b64(sup)},
        [("x.c", b"BA")], want=[(0, "media/kind", 0)],
        note="sniffed base media/* shares the media type -> supertype match, no parents")
    tp, _ = build_cache(globs=[("*.c", "text/x-plain", 50), ("*.c", "other/x", 50)],
                        magic=[(50, "text/plain", [ml(0, 1, b"BA")])])
    add("subclass", "text-plain-special", E_S1, {"s1/mime/mime.cache": b64(tp)},
        [("x.c", b"BA"), ("zz.nomatch", b"BA")],
        want=[(0, "text/x-plain", 0), (1, "text/plain", 0)],
        note="text/plain is a superclass of every text/* without parents; with no "
             "name types the sniffed string is returned certain")
    octc, _ = build_cache(globs=[("*.c", "inode/x-foo", 50), ("*.c", "app/thing", 50)],
                          magic=[(50, "application/octet-stream", [ml(0, 1, b"OC")])])
    add("subclass", "octet-special", E_S1, {"s1/mime/mime.cache": b64(octc)},
        [("x.c", b"OC")],
        want=[(0, "app/thing", 0)],
        note="application/octet-stream is a superclass of everything except inode/*; "
             "the inode name type fails, app/thing is picked")
    octc2, _ = build_cache(globs=[("*.c", "inode/x-foo", 50), ("*.c", "inode/x-bar", 50)],
                           magic=[(50, "application/octet-stream", [ml(0, 1, b"OC")])])
    add("subclass", "inode-blocked", E_S1, {"s1/mime/mime.cache": b64(octc2)},
        [("x.c", b"OC")], want=[(0, "inode/x-foo", 1)],
        note="both name types are inode/* -> no subclass -> first, uncertain")
    # deep parent chain (1200): the C recursion is fine; the candidate's Python recursion
    # hits its recursion limit -> expected tool crash (finding), oracle label kept.
    N = 1200
    names = [f"app/d{i:04d}" for i in range(N)]
    parents = [(names[i], [names[i + 1]]) for i in range(N - 1)]
    deep, _ = build_cache(globs=[("*.c", names[0], 50), ("*.c", "other/x", 50)],
                          magic=[(50, names[-1], [ml(0, 1, b"BA")])],
                          parents=parents)
    add("subclass", "deep-chain-1200", E_S1, {"s1/mime/mime.cache": b64(deep)},
        [("x.c", b"BA")], want=[(0, names[0], 0)],
        note="1200-level parent chain; C resolves it, the candidate is expected to "
             "die with RecursionError (exit != 0/3) - EXPECTED DISAGREEMENT")


# ---------------------------------------------------------------- class: alias

def add_alias():
    a1, _ = build_cache(aliases=[("text/x-old", "text/x-new")],
                        magic=[(50, "text/x-old", [ml(0, 1, b"T")])],
                        globs=[("*.new", "text/x-new", 50), ("*.new", "other/x", 50)])
    add("alias", "sniff-alias-string", E_S1, {"s1/mime/mime.cache": b64(a1)},
        [(None, b"T"), ("x.new", b"T")],
        want=[(0, "text/x-old", 0), (1, "text/x-new", 0)],
        note="sniff output is never unaliased (text/x-old); tie-break unaliases BOTH "
             "sides so text/x-new == unalias(text/x-old) -> picked, certain")
    chain, _ = build_cache(aliases=[("a/one", "a/two"), ("a/two", "a/three")],
                           globs=[("*.three", "a/three", 50), ("*.three", "other/x", 50)],
                           magic=[(50, "a/one", [ml(0, 1, b"T")])])
    add("alias", "single-step-unalias", E_S1, {"s1/mime/mime.cache": b64(chain)},
        [("x.three", b"T")],
        want=[(0, "a/three", 1)],
        note="unalias is one step: a/three stays a/three, a/one becomes a/two -> "
             "not equal, no parents -> first, uncertain")
    self_a, _ = build_cache(aliases=[("app/me", "app/me")],
                            globs=[("*.me", "app/me", 50), ("*.me", "other/x", 50)],
                            magic=[(50, "app/me", [ml(0, 1, b"T")])])
    add("alias", "self-alias", E_S1, {"s1/mime/mime.cache": b64(self_a)},
        [("x.me", b"T")], want=[(0, "app/me", 0)],
        note="self-alias: unalias is identity, tie-break equal -> picked")
    ghost, _ = build_cache(aliases=[("ghost", "real/one")],
                           globs=[("*.gh", "ghost", 50), ("*.gh", "other/x", 50)],
                           magic=[(50, "real/one", [ml(0, 1, b"T")])])
    add("alias", "ghost-name-type", E_S1, {"s1/mime/mime.cache": b64(ghost)},
        [("x.gh", b"T")],
        want=[(0, "ghost", 0)],
        note="name type 'ghost' unaliases to real/one == sniffed -> picked; the "
             "returned type is the undefined string 'ghost', certain")
    nameside, _ = build_cache(aliases=[("text/x-old", "text/x-new")],
                              globs=[("*.old", "text/x-old", 50), ("*.old", "other/x", 50)],
                              magic=[(50, "text/x-new", [ml(0, 1, b"T")])])
    add("alias", "alias-on-name-side", E_S1, {"s1/mime/mime.cache": b64(nameside)},
        [("x.old", b"T"), ("zz.nomatch", b"T")],
        want=[(0, "text/x-old", 0), (1, "text/x-new", 0)],
        note="name type text/x-old unaliases to text/x-new == sniffed -> picked; "
             "without name types the raw sniffed answer is returned")
    audio, _ = build_cache(aliases=[("audio/*", "media/sound")],
                           globs=[("*.w", "media/x-wav", 50), ("*.w", "other/x", 50)],
                           magic=[(50, "audio/*", [ml(0, 1, b"T")])])
    add("alias", "supertype-unaliased-away", E_S1, {"s1/mime/mime.cache": b64(audio)},
        [("x.w", b"T")],
        want=[(0, "media/x-wav", 1)],
        note="the supertype check sees the UNALIASED base media/sound (no /*) -> "
             "no match -> first, uncertain")
    rev, _ = build_cache(aliases=[("image/jpg", "image/jpeg")],
                         globs=[("*.j", "image/jpeg", 50), ("*.j", "other/x", 50)],
                         magic=[(50, "image/jpg", [ml(0, 1, b"T")])])
    add("alias", "reverse-direction", E_S1, {"s1/mime/mime.cache": b64(rev)},
        [("x.j", b"T")],
        want=[(0, "image/jpeg", 0)],
        note="unalias(sniffed image/jpg) -> image/jpeg == name type -> picked")
    tp2, _ = build_cache(aliases=[("text/plain", "text/plain2")],
                         globs=[("*.p", "text/x-plain", 50), ("*.p", "other/x", 50)],
                         magic=[(50, "text/plain", [ml(0, 1, b"T")])])
    add("alias", "alias-defeats-text-special", E_S1, {"s1/mime/mime.cache": b64(tp2)},
        [("x.p", b"T"), ("zz.nomatch", b"T")],
        want=[(0, "text/x-plain", 1), (1, "text/plain", 0)],
        note="sniffed string text/plain unaliases to text/plain2 BEFORE the "
             "text/plain special case -> no subclass -> first, uncertain; without "
             "name types the string is returned certain")
    c1_m, _ = build_cache(magic=[(50, "m/alias", [ml(0, 1, b"T")])])
    c2_m, _ = build_cache(aliases=[("m/alias", "m/canon")],
                          globs=[("*.a", "m/canon", 50), ("*.a", "other/x", 50)])
    add("alias", "cross-cache-alias-on-sniffed", E_S1_S2,
        {"s1/mime/mime.cache": b64(c1_m), "s2/mime/mime.cache": b64(c2_m)},
        [("x.a", b"T")],
        want=[(0, "m/canon", 0)],
        note="sniffed m/alias (stored string in s1) unaliases via s2 to m/canon == "
             "name type -> picked")


# ---------------------------------------------------------------- class: slash

def add_slash():
    g1, _ = build_cache(globs=[("*.txt", "txt/sub", 50)])
    add("slash", "simple", E_S1, {"s1/mime/mime.cache": b64(g1)},
        [("d/", b"text\n")], want=[(0, "inode/directory", 1)])
    add("slash", "double", E_S1, {"s1/mime/mime.cache": b64(g1)},
        [("d//", b"text\n"), ("d///", b"text\n")],
        want=[(0, "inode/directory", 1), (1, "inode/directory", 1)])
    add("slash", "root-slash", E_S1, {"s1/mime/mime.cache": b64(g1)},
        [("/", b"text\n")], want=[(0, "inode/directory", 1)])
    add("slash", "nested-empty-data", E_S1, {"s1/mime/mime.cache": b64(g1)},
        [("a/b/", b"")], want=[(0, "inode/directory", 1)])
    add("slash", "desktop-data", E_S1,
        {"s1/mime/mime.cache": b64(build_cache(globs=[("*.txt", "txt/sub", 50)],
                                               magic=[(80, "application/x-desktop",
                                                      [ml(0, 1, b"[Desktop Entry]")])])[0])},
        [("d/", b"[Desktop Entry]\n")],
        want=[(0, "inode/directory", 1)],
        note="the slash shortcut runs before any sniffing")
    add("slash", "no-trailing-control", E_S1, {"s1/mime/mime.cache": b64(g1)},
        [("d/x", b"text\n"), ("d/.", b"text\n")],
        want=[(0, "text/plain", 0), (1, "text/plain", 0)],
        note="'d/.' does not end in '/': basename lookup runs")
    add("slash", "glob-name-with-slash", E_S1, {"s1/mime/mime.cache": b64(g1)},
        [("x.txt/", b"junk")],
        want=[(0, "inode/directory", 1)],
        note="trailing slash wins even though x.txt has a type")
    add("slash", "inner-slash-only", E_S1, {"s1/mime/mime.cache": b64(g1)},
        [("d//d", b"text\n")],
        want=[(0, "text/plain", 0)])


# ---------------------------------------------------------------- class: mode

def add_mode():
    ok, _ = build_cache(magic=[(50, "app/x", [ml(0, 1, b"HI")])])
    v10, _ = build_cache(version=(1, 0))
    v11, _ = build_cache(magic=[(50, "app/x", [ml(0, 1, b"HI")])], version=(1, 1))
    v20, _ = build_cache(version=(2, 2))
    garbage = bytes(range(60))
    add("mode", "all-absent", E_S1_S2, {},
        [(None, b"text\n"), (None, b"\x01\x02")],
        want=[(0, "text/plain", 0), (1, "application/octet-stream", 1)],
        expect_refusal=True,
        note="no cache anywhere: GLib falls back; the tool refuses (text mode)")
    add("mode", "bad-major", E_S1, {"s1/mime/mime.cache": b64(v20)},
        [(None, b"text\n")], want=[(0, "text/plain", 0)],
        expect_refusal=True, note="major 2 -> not a cache")
    add("mode", "minor-zero", E_S1, {"s1/mime/mime.cache": b64(v10)},
        [(None, b"text\n")], want=[(0, "text/plain", 0)],
        expect_refusal=True, note="minor 0 < 1 -> not a cache")
    add("mode", "minor-one-loads", E_S1, {"s1/mime/mime.cache": b64(v11)},
        [(None, b"HI"), (None, b"text\n")],
        want=[(0, "app/x", 0), (1, "text/plain", 0)],
        note="minor 1 IS a loadable cache: no refusal")
    add("mode", "truncated-39", E_S1, {"s1/mime/mime.cache": b64(ok[:39])},
        [(None, b"HI")], want=[(0, "text/plain", 0)],
        expect_refusal=True, note="< 40 bytes -> not a cache")
    add("mode", "header-only-40", E_S1, {"s1/mime/mime.cache": b64(ok[:40])},
        [(None, b"HI"), (None, b"\x01")],
        want=[(0, "text/plain", 0), (1, "application/octet-stream", 1)],
        note="exactly 40 bytes: loads, but every section is out of bounds -> fallback; "
             "NOT a refusal (a cache loaded)")
    add("mode", "garbage-bytes", E_S1, {"s1/mime/mime.cache": b64(garbage)},
        [(None, b"text\n")], want=[(0, "text/plain", 0)],
        expect_refusal=True, note="60 garbage bytes: wrong version -> not a cache")
    add("mode", "bad-cache-and-none", E_S1_S2,
        {"s1/mime/mime.cache": b64(v10)},
        [(None, b"text\n")], want=[(0, "text/plain", 0)],
        expect_refusal=True, note="no loadable cache in ANY dir -> text mode")
    add("mode", "bad-cache-plus-good", E_S1_S2,
        {"s1/mime/mime.cache": b64(v10), "s2/mime/mime.cache": b64(ok)},
        [(None, b"HI")], want=[(0, "app/x", 0)],
        note="one loadable cache anywhere -> cache mode")


# ---------------------------------------------------------------- class: extras

def add_more(cache, xml):
    g1, _ = build_cache(globs=[("*.txt", "txt/sub", 50)])
    add("mode", "dh-set-ignores-home", E_DH_S1,
        {"h/.local/share/mime/mime.cache": b64(g1)},
        [(None, b""), ("a.txt", b"HI")],
        want=[(0, "application/x-zerosize", 0), (1, "text/plain", 0)],
        expect_refusal=True,
        note="XDG_DATA_HOME set: the HOME/.local/share cache is invisible (the oracle "
             "answers via the fallback, proving GLib never consults it); no loadable "
             "cache anywhere -> the tool refuses (text mode)")
    empty_magic, _ = build_cache()
    add("fallback", "printable-sweep", E_S1, {"s1/mime/mime.cache": b64(empty_magic)},
        [(None, bytes(range(32, 127))), (None, b"x" * 200 + b"\x01")],
        want=[(0, "text/plain", 0), (1, "text/plain", 0)],
        note="every printable byte passes; ctrl at 200 is outside the window")
    add("fallback", "ctrl-at-zero-long", E_S1, {"s1/mime/mime.cache": b64(empty_magic)},
        [(None, b"\x02" + b"word " * 60)],
        want=[(0, "application/octet-stream", 1)])
    add("lltext", "vt-past-window", E_S1, {"s1/mime/mime.cache": b64(empty_magic)},
        [(None, b"a" * 128 + b"\x0b" + b"tail"), (None, b"a" * 127 + b"\x0b")],
        want=[(0, "text/plain", 0), (1, "application/octet-stream", 1)],
        note="0x0b at index 128 escapes the binary window (and looks_like_text sees "
             "it but that only matters when sniffed is UNKNOWN)")
    o3, _ = build_cache(magic=[(50, "app/p1", [ml(0, 1, b"X")]),
                               (50, "app/p2", [ml(0, 1, b"Y")]),
                               (50, "app/p3", [ml(0, 1, b"Z")])])
    add("order", "first-match-of-three", E_S1, {"s1/mime/mime.cache": b64(o3)},
        [(None, b"Y.."), (None, b"Z.."), (None, b"X..")],
        want=[(0, "app/p2", 0), (1, "app/p3", 0), (2, "app/p1", 0)],
        note="the entry whose matchlet holds first in cache order wins, at equal prio")
    c2small, _ = build_cache(magic=[(2, "app/small", [ml(0, 1, b"HI")])])
    add("prio", "two-vs-one-cross-cache", E_S1_S2,
        {"s1/mime/mime.cache": b64(build_cache(magic=[(1, "app/one", [ml(0, 1, b"HI")])])[0]),
         "s2/mime/mime.cache": b64(c2small)},
        [(None, b"HI")], want=[(0, "app/small", 0)],
        note="strictly greater wins across caches at low priorities too")
    t1, _ = build_cache(magic=[(50, "app/t1", [ml(0, 1, b"HI")])])
    t2b, _ = build_cache(magic=[(60, "app/t2", [ml(0, 1, b"HI")])])
    add("multicache", "three-dirs-highest", E_DH_S1_S2,
        {"dh/mime/mime.cache": b64(t1), "s1/mime/mime.cache": b64(t1),
         "s2/mime/mime.cache": b64(t2b)},
        [(None, b"HI")], want=[(0, "app/t2", 0)],
        note="dh and s1 answer the same type at p50; s2's p60 replaces both")
    add("range", "mid-window", E_S1,
        {"s1/mime/mime.cache": b64(build_cache(magic=[(50, "app/r", [ml(2, 3, b"AB")])])[0])},
        [(None, b"..AB."), (None, b"...AB"), (None, b".AB..")],
        want=[(0, "app/r", 0), (1, "app/r", 0), (2, "text/plain", 0)],
        note="window [2,5): positions 2,3,4; AB at 1 is outside")
    add("mask", "wild-prefix", E_S1,
        {"s1/mime/mime.cache": b64(build_cache(
            magic=[(50, "app/m", [ml(0, 1, b"XYZ", b"\x00\x00\xff")])])[0])},
        [(None, b"abZ"), (None, b"abY"), (None, b"abX")],
        want=[(0, "app/m", 0), (1, "text/plain", 0), (2, "text/plain", 0)],
        note="only the third byte compares; non-matching printable data falls back")
    p3, _ = build_cache(magic=[(50, "app/mid", [ml(0, 1, b"M", None, [
        ml(2, 1, b"L"), ml(3, 1, b"N"), ml(4, 1, b"O")])])])
    add("nest", "three-children-middle", E_S1, {"s1/mime/mime.cache": b64(p3)},
        [(None, b"M.zN."), (None, b"MLN.."), (None, b"M...O")],
        want=[(0, "app/mid", 0), (1, "text/plain", 0), (2, "app/mid", 0)],
        note="any of the three children (L@2, N@3, O@4) holding confirms the parent")
    nomatchb, ikb = build_cache(magic=[(50, "app/x", [ml(0, 1, b"HI")])])
    c0 = bytearray(nomatchb)
    patch(c0, ikb["magic_at"], 0)  # n_entries = 0
    add("bounds", "magic-entry-count-zero", E_S1, {"s1/mime/mime.cache": b64(bytes(c0))},
        [(None, b"HI")], want=[(0, "text/plain", 0)],
        note="zero magic entries: lookup returns NULL, fallback answers")
    add("wrap", "huge-window-no-wrap", E_S1,
        {"s1/mime/mime.cache": b64(build_cache(magic=[(50, "app/w", [ml(0, 0xFFFFFFFF, b"AB")])])[0])},
        [(None, b"AB"), (None, b"A")],
        want=[(0, "app/w", 0), (1, "text/plain", 0)],
        note="0 + 0xFFFFFFFF does not wrap; the window is huge and the value matches "
             "at the first position")
    add("desktop", "prio40-tiebreak-subclass", E_S1,
        {"s1/mime/mime.cache": b64(build_cache(
            globs=[("*.p", "text/x-plain", 50), ("*.p", "other/x", 50)],
            magic=[(40, "application/x-desktop", [ml(0, 1, b"[Desktop Entry]")])])[0])},
        [("x.p", b"[Desktop Entry]\n")],
        want=[(0, "text/x-plain", 0)],
        note="rewritten sniffed text/plain carries prio 40 < 80 -> tie-break: "
             "text/x-plain subclasses text/plain (special case) -> picked certain")
    add("name1", "case-sensitive-glob", E_S1,
        {"s1/mime/mime.cache": b64(build_cache(globs=[("*.cs", "txt/cs", 50 | 0x100)])[0])},
        [("x.cs", b"\x01"), ("X.CS", b"\x01")],
        want=[(0, "txt/cs", 0), (1, "application/octet-stream", 1)],
        note="cs-flagged glob: the lowered pass skips it, the exact-name pass takes "
             "x.cs; X.CS finds nothing")
    add("name0", "dots-and-binary", E_S1, {"s1/mime/mime.cache": b64(empty_magic)},
        [("...", b"\x01\x02"), ("..?", b"\x01\x02")],
        want=[(0, "application/octet-stream", 1), (1, "application/octet-stream", 1)])
    w3, _ = build_cache(globs=[("*.w", "app/hi", 90), ("*.w", "app/mid", 50),
                               ("*.w", "app/lo", 10)])
    add("nameN", "three-weights", E_S1, {"s1/mime/mime.cache": b64(w3)},
        [("x.w", b"text\n")], want=[(0, "app/hi", 1)],
        note="three types sorted by weight descending; first wins, uncertain")
    emp80, ik80 = build_cache(globs=[("*.two", "app/one", 50), ("*.two", "app/two", 50)],
                              magic=[(80, "app/tmp", [ml(0, 1, b"HI")])])
    c80 = bytearray(emp80)
    patch(c80, ik80["entries"][0]["off"] + 4, len(emp80) + 60)
    add("nameN", "empty-sniffed-p80", E_S1, {"s1/mime/mime.cache": b64(bytes(c80))},
        [("x.two", b"HI")], want=[(0, "", 0)],
        note="sniffed \"\" with prio 80 >= 80 wins outright over both name types")
    ta, _ = build_cache(aliases=[("text/x-alias", "text/plain")],
                        globs=[("*.p", "text/x-plain", 50), ("*.p", "other/x", 50)],
                        magic=[(50, "text/x-alias", [ml(0, 1, b"T")])])
    add("alias", "alias-to-textplain-special", E_S1, {"s1/mime/mime.cache": b64(ta)},
        [("x.p", b"T")], want=[(0, "text/x-plain", 0)],
        note="unalias(sniffed text/x-alias) -> text/plain fires the text/* special -> "
             "the text/x-plain name type is picked")
    add("slash", "glob-type-and-slash", E_S1, {"s1/mime/mime.cache": b64(g1)},
        [("a.txt/", b"junk"), ("//", b"junk"), ("a//", b"junk")],
        want=[(0, "inode/directory", 1), (1, "inode/directory", 1),
              (2, "inode/directory", 1)])
    v13, _ = build_cache(version=(1, 3))
    add("mode", "minor-three", E_S1, {"s1/mime/mime.cache": b64(v13)},
        [(None, b"HI")], want=[(0, "text/plain", 0)],
        expect_refusal=True, note="minor 3 > 2 -> not a cache")
    add("real", "word-near-miss",
        E_S1, {"s1/mime/mime.cache": b64(cache), "s1/mime/packages/my.xml": b64(xml)},
        [(None, b"xx\x01\x00\x00\x00y\n"), (None, b"ABDCxy\n"),
         ("z.q", b"TWO??"), ("x.nest", b"junk")],
        want=[(0, "application/octet-stream", 1), (1, "text/plain", 0), (2, "app/x-two", 0),
              (3, "app/x-nest", 0)],
        note="byte-swapped little32 and big32 near-misses fall back; TWO holds on its "
             "own prio-10 rule; single glob type short-circuits")

def main():
    print("== builder cross-check vs candidate build_cache ==")
    sys.path.insert(0, os.path.join(S, "tools"))
    import importlib.util
    spec = importlib.util.spec_from_file_location("cand", os.path.join(S, "tools", "mado-mimesniff.py"))
    cand = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(cand)
    import random
    rng = random.Random(95)
    bad = 0
    for t in range(60):
        al = [(f"a/t{i}", f"b/t{i}") for i in range(rng.randint(0, 3))]
        pa = [(f"p/c{i}", [f"p/b{i}", f"p/d{i}"]) for i in range(rng.randint(0, 3))]
        li = [(f"L{i}", f"t/l{i}", rng.randint(0, 100)) for i in range(rng.randint(0, 3))]
        gl = [("z.t*" if i % 2 else "*.[a-z]", f"t/g{i}", rng.randint(0, 100))
              for i in range(rng.randint(0, 3))]
        mg = [(rng.choice([0, 1, 50, 79, 80, 100]), f"t/m{i}",
               [ml(rng.randint(0, 4), rng.randint(1, 3), bytes(rng.randbytes(2)),
                   mask=None if rng.random() < 0.7 else bytes(rng.randbytes(2)),
                   children=[ml(0, 1, b"Z")] if rng.random() < 0.3 else [])])
              for i in range(rng.randint(0, 3))]
        mine, _ = build_cache(aliases=al, parents=pa, literals=li, globs=gl, magic=mg)
        theirs = cand.build_cache(aliases=al, parents=pa, literals=li, globs=gl, magic=[
            (p, m, [{"start": x["start"], "length": x["length"], "value": x["value"],
                     "mask": x["mask"], "children": [{"start": c["start"], "length": c["length"],
                                                     "value": c["value"], "mask": None} for c in x["children"]]}
                    for x in ms]) for p, m, ms in mg])
        if mine != theirs:
            bad += 1
    print(f"   cross-check: {60 - bad}/60 byte-identical")

    print("== real cache (update-mime-database in scratch) ==")
    cache, xml = build_real()
    add_real(cache, xml)

    print("== building classes ==")
    add_zerosize()
    add_fallback()
    add_lltext()
    add_order()
    add_prio()
    add_multicache()
    add_range()
    add_mask()
    add_nest()
    add_bounds()
    add_wrap()
    add_desktop()
    add_name1()
    add_name0()
    add_nameN()
    add_subclass()
    add_alias()
    add_slash()
    add_mode()
    add_more(cache, xml)

    print(f"== {len(CASES)} cases assembled; labelling with the oracle ==")
    want_fail = 0
    unsupported = 0
    for case in CASES:
        tag = case["id"]
        root = os.path.join(S, "roots", tag)
        materialize(root, case["env"], case["files"])
        labels, why = run_oracle(root, case["env"], case["inputs"], tag)
        if labels is None:
            labels = [["UNSUPPORTED", None]] * len(case["inputs"])
            unsupported += 1
            print(f"   UNSUPPORTED {tag} ({why})")
        case["labels"] = labels
        for (i, t, u) in (case.get("_want") or []):
            if labels[i] != [t, u]:
                want_fail += 1
                print(f"   WANT-MISMATCH {tag}[{i}]: oracle={labels[i]!r} want={[t, u]!r}")
        case.pop("_want", None)

    per_class = {}
    for c in CASES:
        per_class[c["class"]] = per_class.get(c["class"], 0) + 1
    print("== per-class counts ==")
    for cls in ("zerosize fallback lltext order prio multicache range mask nest bounds "
                "wrap desktop name1 name0 nameN subclass alias slash mode real").split():
        flag = "" if per_class.get(cls, 0) >= 8 else "  <-- BELOW 8"
        print(f"   {cls:11s} {per_class.get(cls, 0):3d}{flag}")
    print(f"total={len(CASES)} unsupported_cases={unsupported} want_mismatches={want_fail}")

    out = {"version": 1, "oracle_src_sha256": ORACLE_SHA, "glib2": GLIB,
           "cases": []}
    for c in CASES:
        oc = {k: v for k, v in c.items() if not k.startswith("_")}
        oc["inputs"] = [{"name_b64": None if n is None else b64(n.encode() if isinstance(n, str) else n),
                         "data_b64": b64(d)} for n, d in c["inputs"]]
        out["cases"].append(oc)
    os.makedirs(os.path.dirname(OUT_JSON), exist_ok=True)
    with open(OUT_JSON, "w") as fh:
        json.dump(out, fh, indent=1)
    print(f"wrote {OUT_JSON} ({os.path.getsize(OUT_JSON)} bytes)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
