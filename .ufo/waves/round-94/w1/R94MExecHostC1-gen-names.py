#!/usr/bin/env python3
"""Round-94 host name list generator (seat R94MExecHostC1).

Synthesises candidate file names from the glob patterns of the host's globs2
files only (xdgmime search order).  Emits one name per line; any byte outside
printable ASCII 0x20-0x7E and any literal backslash 0x5C is written as \\xHH
(uppercase hex) so decoding \\x([0-9A-F]{2}) is unambiguous.

Per distinct glob pattern: the literal itself, '*'->'x', UPPER, Title,
leading 'A', a full-glob instance, and a two-extension variant for
dot-bearing names.  Plus 300 seeded random non-matching names.
"""
import fnmatch
import hashlib
import os
import random
import re
import sys

HOME = os.environ["HOME"]
XDG_DATA_HOME = os.environ.get("XDG_DATA_HOME")
XDG_DATA_DIRS = os.environ.get("XDG_DATA_DIRS") or "/usr/local/share:/usr/share"
SEED = 94
OUT = sys.argv[1]
SENTINELS = {b"__NOGLOBS__", b"__NOCASEGLOBS__"}
TWOEXT = [b".gz", b".tar", b".bak", b".new", b".orig"]


def globs2_files():
    order = []
    if XDG_DATA_HOME:
        order.append(os.path.join(XDG_DATA_HOME, "mime", "globs2"))
    for d in XDG_DATA_DIRS.split(":"):
        if d:
            order.append(os.path.join(d, "mime", "globs2"))
    return order


def parse_patterns(paths):
    """pattern bytes -> cs flag; xdgmime field order weight:mime:pattern[:cs]."""
    pats = {}
    for p in paths:
        for raw in open(p, "rb").read().split(b"\n"):
            line = raw.rstrip(b"\r")
            if not line or line.startswith(b"#"):
                continue
            fields = line.split(b":")
            if len(fields) < 3:
                continue
            pat = fields[2]
            if pat in SENTINELS:
                continue
            cs = len(fields) >= 4 and fields[3] == b"cs"
            prev = pats.get(pat)
            pats[pat] = cs if prev is None else (prev or cs)
    return pats


def expand(p):
    """A concrete name matching the full glob ('*'->chunk, '?'->q, class->member, brace->first alt)."""
    out = bytearray()
    i = 0
    while i < len(p):
        c = p[i]
        if c == 0x2A:
            out += b"chunk"
            i += 1
        elif c == 0x3F:
            out += b"q"
            i += 1
        elif c == 0x5B:  # [
            j = p.find(b"]", i + 1)
            if j < 0:
                out.append(c)
                i += 1
                continue
            body = p[i + 1 : j]
            if body.startswith(b"!"):
                out += b"z"
            elif b"-" in body:
                out += body[:1] or b"x"
            else:
                out += body[:1] or b"x"
            i = j + 1
        elif c == 0x7B:  # {
            j = p.find(b"}", i + 1)
            if j < 0:
                out.append(c)
                i += 1
                continue
            out += p[i + 1 : j].split(b",")[0]
            i = j + 1
        else:
            out.append(c)
            i += 1
    return bytes(out)


def esc(b):
    out = bytearray()
    for ch in b:
        if ch == 0x5C:
            out += b"\\x5C"
        elif 0x20 <= ch <= 0x7E:
            out.append(ch)
        else:
            out += ("\\x%02X" % ch).encode("ascii")
    return bytes(out)


def compile_matchers(pats):
    ms = []
    for pat, cs in pats.items():
        s = pat.decode("ascii", "replace")
        rx = re.compile(fnmatch.translate(s), 0 if cs else re.IGNORECASE)
        ms.append((rx, cs))
    return ms


CONS = "qwrtpsdfghjklzxcvbnm"
VOWS = "aeiouy"
EXTS = ["", ".zqx", ".qv9", ".xz", ".wqk", ".jv"]


def main():
    files = globs2_files()
    present = [p for p in files if os.path.isfile(p)]
    absent = [p for p in files if p not in present]
    blob = b"".join(open(p, "rb").read() for p in present)
    sha = hashlib.sha256(blob).hexdigest()
    pats = parse_patterns(present)
    matchers = compile_matchers(pats)

    derived = []
    for idx, pat in enumerate(sorted(pats)):
        xname = pat.replace(b"*", b"x")
        derived.append(pat)  # the literal itself
        derived.append(xname)
        derived.append(xname.upper())
        derived.append(xname.title())
        derived.append(b"A" + xname)
        derived.append(expand(pat))
        if b"." in xname:  # two-extension, x.tar.gz-shaped
            derived.append(xname + TWOEXT[idx % len(TWOEXT)])

    rng = random.Random(SEED)

    def rand_word():
        return "".join(rng.choice(CONS) + rng.choice(VOWS) for _ in range(rng.randint(3, 5)))

    def rand_name():
        n = rand_word()
        if rng.random() < 0.7:
            n += "-" + rand_word()
        n += rng.choice(EXTS)
        if rng.random() < 0.1:
            n = n.upper()
        return n

    def nonmatching(s):
        for rx, cs in matchers:
            if rx.fullmatch(s):
                return True
        return False

    randoms = []
    seen_rand = set(derived)
    guard = 0
    while len(randoms) < 300 and guard < 100000:
        guard += 1
        s = rand_name()
        if s in seen_rand or nonmatching(s):
            continue
        seen_rand.add(s)
        randoms.append(s.encode("ascii"))
    if len(randoms) < 300:
        print("ERROR: only %d random non-matching names" % len(randoms), file=sys.stderr)
        return 1

    allnames = sorted(set(derived) | set(randoms))
    with open(OUT, "wb") as f:
        f.write(
            ("# mimeglob host names r94 seed=%d patterns_sha256=%s\n" % (SEED, sha)).encode("ascii")
        )
        for n in allnames:
            f.write(esc(n) + b"\n")

    dot = sum(1 for n in allnames if b"." in n)
    cs_rows = sum(1 for cs in pats.values() if cs)
    print("files_in_sha_order:", ", ".join(present))
    print("files_absent:", ", ".join(absent) if absent else "(none)")
    print("patterns_sha256:", sha)
    print("distinct_patterns:", len(pats), "cs_flagged:", cs_rows)
    print("derived:", len(derived), "random_nonmatching:", len(randoms))
    print("total_deduped:", len(allnames), "with_dot:", dot)
    return 0


if __name__ == "__main__":
    sys.exit(main())
