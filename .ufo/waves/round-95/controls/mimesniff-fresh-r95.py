#!/usr/bin/env python3
"""mimesniff-fresh-r95 — seeded random case generator for the round-95 C1 mimesniff wave.

`python3 -I mimesniff-fresh-r95.py --seed N --count K --out FILE` writes K random cases
in the CASE FILE SCHEMA of the round-95 declaration ({"version", "oracle_src_sha256",
"glib2", "cases": [...]}) WITHOUT labels: every case carries "labels": [] and the counter
labels them with the live oracle.  Deterministic for a given seed; stdlib only; ASCII.

Each case: 1-3 XDG data dirs (XDG_DATA_HOME optional, XDG_DATA_DIRS always set), 1-2
mime.cache fixtures built by an embedded mime.cache 1.2 writer (the layout of
xdgmimecache.c: suffixable globs in the reverse-suffix trie, other globs in the fnmatch
list, literals/aliases/parents lists, magic entries with 32-byte matchlets), and 1-6
inputs whose data is derived from the rules (holding, near-miss, both-children-fail,
random text, random binary, empty) plus an optional filename.  Classes are assigned by
dominant feature: prio order multicache range mask nest name1 nameN subclass alias.
"""
import argparse
import base64
import json
import random
import struct

ORACLE_SHA = "99df35f8b3fd7005f30789f8866984a1bbceaff8dc6c1d326f0132eb7b4d124a"
GLIB = "2.90.1-1"

M32 = 0xFFFFFFFF


def u32(v):
    return struct.pack(">I", v & M32)


def ml(start, length, value, mask=None, children=()):
    return {"start": start, "length": length, "value": bytes(value),
            "mask": None if mask is None else bytes(mask), "children": list(children)}


def build_cache(aliases=(), parents=(), literals=(), globs=(), magic=(), version=(1, 2)):
    """mime.cache 1.2 writer mirroring the xdgmimecache.c layout (validated byte-for-byte
    against the candidate's build_cache and against update-mime-database output)."""
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
            sfx.append((g[1:], m, w))
        else:
            flist.append((g, m, w))
        s(g)
        s(m)
    for _p, m, _ms in magic:
        s(m)

    def place_values(ml_):
        ml_["_v"] = len(blob)
        blob.extend(ml_["value"])
        if ml_.get("mask") is not None:
            ml_["_m"] = len(blob)
            blob.extend(ml_["mask"])
        else:
            ml_["_m"] = 0
        for ch in ml_.get("children", []):
            place_values(ch)

    for _p, _m, ms in magic:
        for m_ in ms:
            place_values(m_)
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
        root = {}
        for suf, m, w in sfx:
            nd = root
            for ch in reversed(suf):
                nd = nd.setdefault(ch, {})
            nd.setdefault(0, []).append((m, w))
        tree = bytearray()
        base = len(blob) + 8

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
        for i, m_ in enumerate(mls):
            kids = m_.get("children", [])
            ko = place(kids) if kids else 0
            m_["_rec"] = at + 32 * i
            rec = (u32(m_["start"]) + u32(m_["length"]) + u32(1) + u32(len(m_["value"]))
                   + u32(m_["_v"]) + u32(m_["_m"]) + u32(len(kids)) + u32(ko))
            blob[m_["_rec"]: m_["_rec"] + 32] = rec
        return at

    hdr[24] = len(blob)
    magic_at = len(blob)
    blob.extend(u32(len(magic)) + u32(0) + u32(len(blob) + 12))
    mat = len(blob)
    blob.extend(b"\0" * (16 * len(magic)))
    for i, (p, m, ms) in enumerate(magic):
        mo = place(ms) if ms else 0
        off = mat + 16 * i
        blob[off: off + 16] = u32(p) + u32(s(m)) + u32(len(ms)) + u32(mo)
    for k in (28, 32, 36):
        hdr[k] = len(blob)
    blob.extend(u32(0))
    blob[0:4] = struct.pack(">HH", *version)
    for k, v in hdr.items():
        blob[k:k + 4] = u32(v)
    return bytes(blob)


ALPHA = b"ABXY.?!"
PRIOS = [0, 1, 30, 50, 79, 80, 90, 100, 0x80000000, 0xFFFFFFFF]
ENVS = [("S1", {"HOME": "{root}/h", "XDG_DATA_HOME": None, "XDG_DATA_DIRS": "{root}/s1"}),
        ("S1S2", {"HOME": "{root}/h", "XDG_DATA_HOME": None,
                  "XDG_DATA_DIRS": "{root}/s1:{root}/s2"}),
        ("DHS1", {"HOME": "{root}/h", "XDG_DATA_HOME": "{root}/dh",
                  "XDG_DATA_DIRS": "{root}/s1"}),
        ("DHS1S2", {"HOME": "{root}/h", "XDG_DATA_HOME": "{root}/dh",
                    "XDG_DATA_DIRS": "{root}/s1:{root}/s2"})]


def gen_case(rng, idx):
    env_name, env = ENVS[rng.randrange(len(ENVS))]
    ndirs = {"S1": 1, "S1S2": 2, "DHS1": 2, "DHS1S2": 3}[env_name]
    dirkeys = {"S1": ["s1"], "S1S2": ["s1", "s2"],
               "DHS1": ["dh", "s1"], "DHS1S2": ["dh", "s1", "s2"]}[env_name]
    typepool = [f"t/{c}" for c in "abcdefg"]
    files = {}
    all_rules = []   # (dirkey, prio, mime, matchlet) for data derivation
    n_globs = rng.randrange(0, 3)
    namespec = []    # (glob, mime, weight) kept per cache for name cases
    for dk in dirkeys:
        aliases = []
        for _ in range(rng.randrange(0, 2)):
            a, m = rng.sample(typepool, 2)
            aliases.append((a, m))
        parents = []
        for _ in range(rng.randrange(0, 2)):
            a, m = rng.sample(typepool, 2)
            parents.append((a, [m]))
        literals = [(f"L{i}", rng.choice(typepool), rng.choice([50, 60, 70]))
                    for i in range(rng.randrange(0, 2))]
        globs = []
        for i in range(n_globs):
            m = rng.choice(typepool)
            if rng.random() < 0.6:
                globs.append((f"*.{rng.choice('xyzw')}{i}", m, rng.choice([40, 50, 60])))
            else:
                globs.append((f"z.t{i}", m, rng.choice([40, 50, 60])))
            namespec.append(globs[-1])
        magic = []
        for _ in range(rng.randrange(1, 4)):
            mime = rng.choice(typepool)
            prio = PRIOS[rng.randrange(len(PRIOS))]
            kids = []
            for _ in range(rng.randrange(0, 2)):
                kids.append(ml(rng.randrange(5, 9), 1, bytes([rng.choice(ALPHA)])))
            m_ = ml(rng.randrange(0, 6), rng.randrange(1, 4),
                    bytes(rng.choice(ALPHA) for _ in range(rng.randrange(1, 4))),
                    mask=None if rng.random() < 0.7 else
                    bytes(rng.choice(ALPHA) for _ in range(rng.randrange(1, 4))),
                    children=kids)
            magic.append((prio, mime, [m_]))
            all_rules.append((dk, prio, mime, m_))
        files[f"{dk}/mime/mime.cache"] = base64.b64encode(
            build_cache(aliases=aliases, parents=parents, literals=literals,
                        globs=globs, magic=magic)).decode("ascii")

    def hold_data(rule):
        _dk, _prio, _mime, m_ = rule
        out = bytearray(b"?" * 12)
        end = (m_["start"] + m_["length"]) & M32
        positions = [p for p in range(0, max(end, 1))
                     if p + len(m_["value"]) <= len(out)]
        if not positions:
            return bytes(out)
        p = positions[rng.randrange(len(positions))]
        out[p:p + len(m_["value"])] = m_["value"]
        return bytes(out)

    def near_data(rule):
        d = bytearray(hold_data(rule))
        if d:
            d[rng.randrange(len(d))] ^= 1 << rng.randrange(3, 8)
        return bytes(d)

    inputs = []
    for _ in range(rng.randrange(1, 7)):
        kind = rng.random()
        name = None
        if kind < 0.35 or not all_rules:
            r = rng.random()
            if r < 0.45:
                data = bytes(rng.choice(ALPHA) for _ in range(rng.randrange(1, 12)))
            elif r < 0.6:
                data = b""
            else:
                data = bytes(rng.randrange(0, 256) for _ in range(rng.randrange(1, 12)))
        elif kind < 0.75:
            rule = all_rules[rng.randrange(len(all_rules))]
            data = hold_data(rule) if rng.random() < 0.6 else near_data(rule)
        else:
            rule = all_rules[rng.randrange(len(all_rules))]
            _dk, _prio, _mime, m_ = rule
            out = bytearray(b"?" * 12)
            if m_["children"]:
                k = m_["children"][0]
                end = (k["start"] + k["length"]) & M32
                out[k["start"]:min(end, 12)] = k["value"]
            data = bytes(out)
        r = rng.random()
        if r < 0.4:
            name = None
        elif r < 0.65 and namespec:
            g, _m, _w = namespec[rng.randrange(len(namespec))]
            base = "z.t0" if g.startswith("z.") else "file" + g[1:]
            name = base.encode()
        else:
            name = ("".join(rng.choice("abc.qrs") for _ in range(rng.randrange(1, 8)))).encode()
        inputs.append({"name": name, "data": data})

    cls = "order"
    r = rng.random()
    if r < 0.18:
        cls = "prio"
    elif r < 0.3:
        cls = "multicache" if ndirs > 1 else "order"
    elif r < 0.42:
        cls = "mask"
    elif r < 0.54:
        cls = "nest"
    elif r < 0.66:
        cls = "range"
    elif r < 0.78:
        cls = "name1" if any(i["name"] for i in inputs) else "name0"
    elif r < 0.9:
        cls = "nameN"
    else:
        cls = rng.choice(["subclass", "alias"])
    return {"id": f"gen-{idx:04d}", "class": cls, "env": env, "files": files,
            "inputs": [{"name": i["name"], "data": i["data"]} for i in inputs],
            "labels": []}


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--seed", type=int, required=True)
    ap.add_argument("--count", type=int, required=True)
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    rng = random.Random(a.seed)
    cases = []
    for i in range(a.count):
        c = gen_case(rng, i)
        cases.append({"id": c["id"], "class": c["class"], "env": c["env"],
                      "files": c["files"],
                      "inputs": [{"name_b64": None if i["name"] is None else
                                  base64.b64encode(i["name"]).decode("ascii"),
                                  "data_b64": base64.b64encode(i["data"]).decode("ascii")}
                                 for i in c["inputs"]],
                      "labels": []})
    doc = {"version": 1, "oracle_src_sha256": ORACLE_SHA, "glib2": GLIB, "cases": cases}
    with open(a.out, "w") as fh:
        json.dump(doc, fh, indent=1, sort_keys=True)
    print(f"mimesniff-fresh-r95: seed={a.seed} count={a.count} out={a.out}")


if __name__ == "__main__":
    main()
