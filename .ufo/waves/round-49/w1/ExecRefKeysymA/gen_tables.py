#!/usr/bin/env python3
"""Generate the compact keysym tables embedded in mado-keysym.py.

Reads the pinned libxkbcommon 1.13.2 sources (same tag the host's
libxkbcommon 1.13.2-1 was built from) and emits one base85(zlib(json)) blob:

  src/ks_tables.h            name -> keysym (all names), keysym -> canonical name
  src/keysym-utf.c           keysymtab[]: keysym, deprecated, Unicode code point
  src/keysym-case-mappings.c case predicates: has_lower / has_upper runs

Inputs are the `pins/` files in this directory (sha256 recorded in the report).
"""
import base64
import json
import struct
import re
import sys
import zlib

HERE = __file__.rsplit("/", 1)[0]


def read(name):
    with open(f"{HERE}/pins/{name}", "r", encoding="utf-8") as f:
        return f.read()


def c_int(tok):
    tok = tok.strip()
    return int(tok, 0) if tok.lower().startswith(("0x", "-0x")) else int(tok, 10)


def parse_ks_tables(text):
    # 1. the names blob: "..." string literals after `keysym_names =`
    m = re.search(r'static const char \*keysym_names =\n(.*?);\n', text, re.S)
    if not m:
        raise SystemExit("names blob not found")
    blob = b"".join(
        bytes(lit, "utf-8").decode("unicode_escape").encode("latin-1")
        for lit in re.findall(r'"((?:[^"\\]|\\.)*)"', m.group(1))
    )
    def name_at(off):
        end = blob.index(b"\0", off)
        return blob[off:end].decode("ascii")

    def parse_array(arrname):
        m = re.search(
            r"static const struct name_keysym " + arrname + r"\[\] = \{(.*?)\n\};",
            text, re.S)
        if not m:
            raise SystemExit(f"{arrname} not found")
        return [tuple(c_int(x) for x in (a, b))
                for a, b in re.findall(r"\{\s*(0x[0-9a-f]+|\d+),\s*(\d+)\s*\}", m.group(1))]

    name_to_keysym = [(name_at(off), ks) for ks, off in parse_array("name_to_keysym")]
    keysym_to_name = [(ks, name_at(off)) for ks, off in parse_array("keysym_to_name")]
    return name_to_keysym, keysym_to_name


def parse_keysymtab(text):
    m = re.search(r"static const struct codepair keysymtab\[\] = \{(.*?)\n\};", text, re.S)
    if not m:
        raise SystemExit("keysymtab not found")
    out = []
    for ks, dep, ucs in re.findall(
            r"\{\s*(0x[0-9a-f]+),\s*(true|false),\s*(0x[0-9a-f]+)\s*\}", m.group(1)):
        out.append([int(ks, 16), int(dep == "true"), int(ucs, 16)])
    return out


def parse_case_tables(text):
    def arr(name, count):
        m = re.search(r"static const [a-z0-9_]+ " + name + r"\[" + str(count) + r"\] = \{(.*?)\n\};",
                      text, re.S)
        if not m:
            raise SystemExit(f"{name} not found")
        return [c_int(x) for x in re.findall(r"-?0x[0-9a-fA-F]+|-?\d+", m.group(1))]

    NUM = r"(-?(?:0x[0-9a-fA-F]+|\d+))"

    def data_block(start_marker, end_marker):
        i = text.index(start_marker)
        j = text.index(end_marker, i)
        return [tuple(c_int(x) for x in t) for t in
                re.findall(r"\{" + NUM + r",\s*" + NUM + r",\s*" + NUM + r"\}", text[i:j])]

    legacy = data_block("legacy_keysym_data[47]", "legacy_keysym_offsets1[540]")
    unicode_ = data_block("unicode_data[1019]", "unicode_offsets1[908]")
    return {
        "legacy": (legacy, arr("legacy_keysym_offsets1", 540), arr("legacy_keysym_offsets2", 40)),
        "unicode": (unicode_, arr("unicode_offsets1", 908), arr("unicode_offsets2", 498)),
    }


def decode(data, off1, off2, ks, s1, s2, mask, addmask):
    return data[off1[off2[ks >> s1] + ((ks >> s2) & mask)] + (ks & addmask)]


def runs(entries):
    """entries: list of (value, flags) -> [[start, end, flags], ...] skipping 0."""
    out = []
    for v, f in entries:
        if f == 0:
            continue
        if out and out[-1][1] + 1 == v and out[-1][2] == f:
            out[-1][1] = v
        else:
            out.append([v, v, f])
    return out


def varints(values):
    out = bytearray()
    for v in values:
        while True:
            b = v & 0x7F
            v >>= 7
            out.append(b | (0x80 if v else 0))
            if not v:
                break
    return bytes(out)


def pack_runs(entries):
    """(value, flags) in ascending value order -> LEB128 delta start + flags byte."""
    out = bytearray()
    prev_end = -1
    for v, f in entries:
        if f == 0:
            continue
        out += varints([v - prev_end - 1])
        out.append(f)
        prev_end = v
    return bytes(out)


def main():
    ks_tables = read("ks_tables.h")
    utf = read("keysym-utf.c")
    case = read("keysym-case-mappings.c")

    name_to_keysym, keysym_to_name = parse_ks_tables(ks_tables)
    keysymtab = parse_keysymtab(utf)

    ct = parse_case_tables(case)
    legacy, l1, l2 = ct["legacy"]
    uni, u1, u2 = ct["unicode"]
    legacy_entries = []
    for ks in range(0x13bf):
        e = decode(legacy, l1, l2, ks, 7, 1, 0x3f, 1)
        legacy_entries.append((ks, (1 if e[1] else 0) | (2 if e[0] else 0)))
    uni_entries = []
    for cp in range(0x100, 0x1f18a):
        e = decode(uni, u1, u2, cp, 8, 3, 0x1f, 7)
        uni_entries.append((cp, (1 if e[1] else 0) | (2 if e[0] else 0)))

    names = sorted(n for n, _ in name_to_keysym)
    index = {n: i for i, n in enumerate(names)}
    k2n = sorted(keysym_to_name)
    canon = {ks: index[n] for ks, n in k2n}

    # name -> keysym is fully implied by the canonical map except for alias names
    aliases = [(index[n], ks) for n, ks in name_to_keysym
               if canon.get(ks) != index[n]]
    assert len(names) == len(set(names))
    assert len(aliases) == len(names) - len(k2n), (len(aliases), len(names), len(k2n))
    assert dict((n, ks) for n, ks in name_to_keysym)["a"] == 0x61
    assert canon[0x2f] == index["slash"]

    sections = [
        ("names", "\n".join(names).encode("ascii")),
        ("kvals", varints([k for k, _ in k2n])),
        ("knames", struct.pack("<%dH" % len(k2n), *[index[n] for _, n in k2n])),
        ("alias", varints([i for i, _ in aliases] + [v for _, v in aliases])),
        ("u", b"".join(struct.pack("<HH", ks | (0x8000 if dep else 0), ucs)
                       for ks, dep, ucs in keysymtab)),
        ("cl", pack_runs(legacy_entries)),
        ("cu", pack_runs(uni_entries)),
    ]
    header = json.dumps(dict([(name, len(data)) for name, data in sections]
                             + [("alias_n", len(aliases))]),
                        separators=(",", ":")).encode()
    raw = header + b"\n" + b"".join(data for _, data in sections)
    blob = base64.b85encode(zlib.compress(raw, 9)).decode()
    sys.stderr.write(
        f"names={len(names)} aliases={len(aliases)} k2n={len(k2n)} "
        f"keysymtab={len(keysymtab)} raw={len(raw)} blob={len(blob)} " +
        " ".join(f"{n}={len(d)}" for n, d in sections) + "\n")
    print(blob)


if __name__ == "__main__":
    main()
