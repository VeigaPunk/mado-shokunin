#!/usr/bin/env python3
"""Round-96 C1 byte-level probe harness (seat R96MProbeC1; read-only).

Builds synthetic fixture roots for the TEXT-mode magic surface of GLib 2.90.1's
g_content_type_guess, runs the compiled round-95 oracle on every input, and,
when --candidate is given, runs the C1 candidate over the same fixture bytes and
prints every disagreement (fixture bytes, oracle answer, candidate answer).

Usage:
  probes-r96.py --oracle PATH [--candidate PATH] [--scratch DIR] [--json OUT]
                [--groups a,b,...]

Fixtures are written only under --scratch.  No network, no host mutation.
ASCII only.  stdlib only (the harness may spawn the oracle and the candidate;
neither is the submitted candidate so the structural rules do not bind here).
"""
from __future__ import annotations

import argparse
import json
import os
import re
import struct
import subprocess
import sys

HEADER = b"MIME-Magic\x00\n"


def ml(indent, offset, value, mask=None, word=None, rng=None, declared=None):
    """One matchlet line (no trailing newline)."""
    b = b""
    if indent is not None:
        b += str(indent).encode()
    b += b">" + str(offset).encode() + b"="
    n = len(value) if declared is None else declared
    b += struct.pack(">H", n) + value
    if mask is not None:
        b += b"&" + mask
    if word is not None:
        b += b"~" + str(word).encode()
    if rng is not None:
        b += b"+" + str(rng).encode()
    return b


def sect(prio, typ, lines):
    out = b"[" + str(prio).encode() + b":" + typ + b"]\n"
    for ln in lines:
        out += ln + b"\n"
    return out


def P(pid, group, d1, inputs, note="", d2=None, dh=None, files=None, chmod=(), dirs=None):
    return {"id": pid, "group": group, "d1": d1, "d2": d2, "dh": dh,
            "files": files or {}, "chmod": chmod, "dirs": dirs, "inputs": inputs,
            "note": note}


def fuzz_probes(count, seed):
    """Random magic files from the parser's own grammar (seeded, reproducible).

    The point is differential: every construct the tools disagree on is a rule my hand probes
    may have missed.  Bytes are drawn to hit the parser's decision points, not to look like a
    real /usr/share/mime/magic.
    """
    import random
    rnd = random.Random(seed)
    out = []
    for k in range(count):
        parts = [HEADER if rnd.random() < 0.9 else
                 rnd.choice([b"MIME-Magic\x00", b"MIME-Magic\x00\r", b"", b"MIME-Magic\x00\n\n"])]
        for _s in range(rnd.randint(1, 4)):
            prio = rnd.choice(["0", "1", "50", "50", "80", "100", "2147483647",
                               "2147483648", "", "007", "9" * 31])
            typ = rnd.choice([b"t/a", b"t/b", b"", b"a b", b"x/\xff", b"__NOMAGIC__",
                              b"application/octet-stream", b"text/plain", b"t/" + b"z" * 130])
            parts.append(b"[" + prio.encode() + b":" + typ + b"]" + rnd.choice([b"\n", b"\r\n", b"junk\n"]))
            for _m in range(rnd.randint(0, 4)):
                line = b""
                ind = rnd.choice([None, 0, 0, 1, 2, 3, 9])
                if ind is not None:
                    line += (b"0" if rnd.random() < 0.1 else b"") + str(ind).encode()
                off = rnd.choice(["0", "0", "1", "2", "3", "5", "127", "65535",
                                  "0000", "2147483647", "4294967295"])
                line += b">" + off.encode() + b"="
                vlen = rnd.choice([0, 1, 1, 2, 2, 3, 4, 0x100])
                decl = vlen
                if rnd.random() < 0.15:
                    decl = rnd.choice([vlen + 1, 0x4241])
                if rnd.random() < 0.1:
                    line += struct.pack(">H", decl)
                else:
                    line += struct.pack(">H", decl)
                val = bytes(rnd.choice([0, 0x41, 0x20, 0x0A, 0xFF, rnd.randrange(256)])
                            for _ in range(min(vlen, 6)))
                if vlen > len(val):
                    val = val + b"A" * (vlen - len(val))
                line += val
                if rnd.random() < 0.35:
                    line += b"&" + bytes(rnd.choice([0, 0xFF, rnd.randrange(256)])
                                         for _ in range(len(val)))
                if rnd.random() < 0.35:
                    line += b"~" + rnd.choice([b"0", b"1", b"2", b"4", b"3", b""])
                if rnd.random() < 0.35:
                    line += b"+" + rnd.choice([b"0", b"1", b"2", b"5", b"10", b""])
                line += rnd.choice([b"\n", b"\n", b"\n", b"\r\n", b"\x00\n", b""])
                parts.append(line)
        magic = b"".join(parts)
        inputs = []
        for _i in range(3):
            n = rnd.choice([0, 1, 1, 2, 3, 4, 8])
            inputs.append((None, bytes(rnd.randrange(256) for _ in range(n))))
        out.append(P("fz-%04d" % k, "fuzz", magic, inputs,
                     note="seeded fuzz seed=%d magic=%r" % (seed, magic[:200])))
    return out


def probes():
    out = []

    # ---- (a) 256-byte value sweep and 256-byte mask sweep -------------------
    for v in range(256):
        magic = HEADER + sect(50, b"probe/value-%03d" % v,
                              [ml(0, 0, bytes([v]))])
        wait = bytes([(v + 1) & 0xFF])
        out.append(P("a-value-%03d" % v, "value", magic,
                     [(None, bytes([v])), (None, wait), (None, bytes([v, v])),
                      (None, b"")],
                     note="value byte %02x" % v))
    for m in range(256):
        magic = HEADER + sect(50, b"probe/mask-%03d" % m,
                              [ml(0, 0, bytes([m]), mask=bytes([m]))])
        out.append(P("a-mask-%03d" % m, "mask", magic,
                     [(None, bytes([m])), (None, bytes([m ^ 0xFF])),
                      (None, b"\x00"), (None, b"")],
                     note="mask byte %02x equals the value byte" % m))

    # ---- (b) offset / length bounds ---------------------------------------
    out.append(P("b-len0-off0", "bounds", HEADER + sect(50, b"probe/b01", [ml(0, 0, b"A")]),
                 [(None, b""), (None, b"A"), (None, b"B"), (None, b"AA")],
                 note="1-byte value at offset 0; len 0,1,1,2"))
    out.append(P("b-len2-off0", "bounds", HEADER + sect(50, b"probe/b02", [ml(0, 0, b"AB")]),
                 [(None, b"AB"), (None, b"A"), (None, b"ABX"), (None, b"BA")],
                 note="2-byte value at offset 0"))
    out.append(P("b-len2-off1", "bounds", HEADER + sect(50, b"probe/b03", [ml(0, 1, b"AB")]),
                 [(None, b"XAB"), (None, b"XA"), (None, b"X"), (None, b"XABX")],
                 note="2-byte value at offset 1: i+vlen == len matches, > fails"))
    out.append(P("b-len2-off2", "bounds", HEADER + sect(50, b"probe/b04", [ml(0, 2, b"AB")]),
                 [(None, b"XXAB"), (None, b"XXA"), (None, b"XX"), (None, b"XXXAB")],
                 note="offset 2 vs len 3"))
    out.append(P("b-len2-off3", "bounds", HEADER + sect(50, b"probe/b05", [ml(0, 3, b"AB")]),
                 [(None, b"XXX"), (None, b"XXXA"), (None, b"XXXAB")],
                 note="offset == len and offset+1 == len"))
    out.append(P("b-len1-off4", "bounds", HEADER + sect(50, b"probe/b06", [ml(0, 4, b"A")]),
                 [(None, b"AAAA"), (None, b"AAAAA")],
                 note="offset 4 vs len 4 / 5"))
    out.append(P("b-len0-off0-r1", "bounds", HEADER + sect(50, b"probe/b08", [ml(0, 0, b"", rng=1)]),
                 [(None, b"Z"), (None, b""), (None, b"\x00")],
                 note="zero-length value matches at any in-bounds offset"))
    out.append(P("b-len0-off5", "bounds", HEADER + sect(50, b"probe/b08b", [ml(0, 5, b"")]),
                 [(None, b"Z"), (None, b"ZZZZZ"), (None, b"ZZZZZZ")],
                 note="zero-length value beyond len must fail (i + 0 > len)"))
    out.append(P("b-len0-off0-r0", "bounds", HEADER + sect(50, b"probe/b09", [ml(0, 0, b"", rng=0)]),
                 [(None, b"Z"), (None, b"")],
                 note="range 0 never compares"))
    out.append(P("b-big-off", "bounds", HEADER + sect(50, b"probe/b10", [ml(0, 65535, b"A")]),
                 [(None, b"AAAA")],
                 note="offset 65535 with 4-byte data"))
    out.append(P("b-off-overflow", "bounds",
                 HEADER + sect(50, b"probe/b11", [ml(0, 4294967295, b"A")])
                 + sect(40, b"probe/b11b", [ml(0, 0, b"A")]),
                 [(None, b"A")],
                 note="offset > INT_MAX is a parse error; next section must answer"))
    out.append(P("b-off-intmax", "bounds", HEADER + sect(50, b"probe/b12", [ml(0, 2147483647, b"A")]),
                 [(None, b"A")],
                 note="offset INT_MAX parses; i+vlen wraps unsigned and exceeds len"))

    # ---- (c) range --------------------------------------------------------
    out.append(P("c01-r1", "range", HEADER + sect(50, b"probe/c01", [ml(0, 0, b"B", rng=1)]),
                 [(None, b"AAAAB")], note="range 1 from 0 misses the B at index 4"))
    out.append(P("c02-r2", "range", HEADER + sect(50, b"probe/c02", [ml(0, 0, b"B", rng=2)]),
                 [(None, b"AAAAB")], note="range 2 from 0 still misses"))
    out.append(P("c03-r2-off3", "range", HEADER + sect(50, b"probe/c03", [ml(0, 3, b"B", rng=2)]),
                 [(None, b"AAAAB"), (None, b"AAAAB"[:4])],
                 note="range 2 from 3: index 4 is the last valid offset"))
    out.append(P("c04-r1-off4", "range", HEADER + sect(50, b"probe/c04", [ml(0, 4, b"B", rng=1)]),
                 [(None, b"AAAAB")], note="range 1 at the last byte"))
    out.append(P("c05-r0", "range", HEADER + sect(50, b"probe/c05", [ml(0, 0, b"B", rng=0)]),
                 [(None, b"AAAAB"), (None, b"B")], note="range 0: the loop body never runs"))
    out.append(P("c06-out-of-bounds-false", "range",
                 HEADER + sect(50, b"probe/c06", [ml(0, 0, b"ZZ", rng=10)]),
                 [(None, b"AAAA"), (None, b"ZZ")],
                 note="i+vlen > len must return FALSE, not skip the matchlet"))
    out.append(P("c07-mid", "range", HEADER + sect(50, b"probe/c07", [ml(0, 1, b"AB", rng=3)]),
                 [(None, b"ABAB"), (None, b"ABAA")],
                 note="hit at i=2 after a miss at i=1"))
    out.append(P("c08-tail", "range", HEADER + sect(50, b"probe/c08", [ml(0, 3, b"B", rng=4)]),
                 [(None, b"AAAAB")],
                 note="range runs past the end but index 4 matches first"))

    # ---- (d) word sizes ---------------------------------------------------
    out.append(P("d-w1-len3", "word", HEADER + sect(50, b"probe/d01", [ml(0, 0, b"ABC", word=1)]),
                 [(None, b"ABC"), (None, b"abc")], note="word 1, odd value length 3"))
    out.append(P("d-w2-len3", "word",
                 HEADER + sect(50, b"probe/d02", [ml(0, 0, b"ABC", word=2)])
                 + sect(40, b"probe/d02b", [ml(0, 0, b"ABC")]),
                 [(None, b"ABC")],
                 note="word 2 with value length 3 is a parse error; next section answers"))
    out.append(P("d-w2-swap", "word",
                 HEADER + sect(50, b"probe/d03", [ml(0, 0, b"\x00\x01\x00\x02", word=2)]),
                 [(None, b"\x01\x00\x02\x00"), (None, b"\x00\x01\x00\x02"),
                  (None, b"\x01\x00\x02\x00\xff")],
                 note="word 2 swaps each BE pair at parse"))
    out.append(P("d-w2-len0", "word", HEADER + sect(50, b"probe/d04", [ml(0, 0, b"", word=2)]),
                 [(None, b"Z"), (None, b"")], note="word 2 with value length 0"))
    out.append(P("d-w4-len6", "word",
                 HEADER + sect(50, b"probe/d05", [ml(0, 0, b"ABCDEF", word=4)])
                 + sect(40, b"probe/d05b", [ml(0, 0, b"ABCDEF", word=1)]),
                 [(None, b"ABCDEF")],
                 note="word 4 with length 6 is a parse error (6 % 4 != 0)"))
    out.append(P("d-w4-swap", "word",
                 HEADER + sect(50, b"probe/d06", [ml(0, 0, b"\x00\x01\x02\x03", word=4)]),
                 [(None, b"\x03\x02\x01\x00"), (None, b"\x00\x01\x02\x03")],
                 note="word 4 swaps the 4-byte word"))
    out.append(P("d-w0-len3", "word",
                 HEADER + sect(50, b"probe/d07", [ml(0, 0, b"ABC", word=0)]),
                 [(None, b"ABC"), (None, b"CBA")],
                 note="word 0 passes the 1|2|4 check and is never used"))
    out.append(P("d-w3", "word",
                 HEADER + sect(50, b"probe/d08", [ml(0, 0, b"AB", word=3)])
                 + sect(40, b"probe/d08b", [ml(0, 0, b"AB")]),
                 [(None, b"AB")], note="word 3 is rejected at parse"))
    out.append(P("d-w2-mask", "word",
                 HEADER + sect(50, b"probe/d10",
                               [ml(0, 0, b"\x00\x01", mask=b"\x00\xFF", word=2)]),
                 [(None, b"\x01\x99"), (None, b"\x00\x00"), (None, b"\x01\x00"),
                  (None, b"\x00\x99")],
                 note="value and mask both swapped per word"))
    out.append(P("d-w4-mask-len2", "word",
                 HEADER + sect(50, b"probe/d11",
                               [ml(0, 0, b"\x00\x01", mask=b"\x00\x01", word=4)])
                 + sect(40, b"probe/d11b", [ml(0, 0, b"\x01\x00")]),
                 [(None, b"\x01\x00")],
                 note="word 4 with length 2 is rejected; next section answers"))

    # ---- (e) indent -------------------------------------------------------
    out.append(P("e-indent0", "indent", HEADER + sect(50, b"probe/e01", [ml(0, 0, b"A")]),
                 [(None, b"A")], note="top-level matchlet"))
    out.append(P("e-indent1-first", "indent", HEADER + sect(50, b"probe/e02", [ml(1, 0, b"A")]),
                 [(None, b"A")], note="a lone indent-1 matchlet is never compared"))
    out.append(P("e-indent9", "indent", HEADER + sect(50, b"probe/e03", [ml(9, 0, b"A")]),
                 [(None, b"A")], note="indent 9 at top level"))
    out.append(P("e-chain01", "indent",
                 HEADER + sect(50, b"probe/e04", [ml(0, 0, b"A"), ml(1, 1, b"B")]),
                 [(None, b"AB"), (None, b"AC"), (None, b"AB" + b"Z")],
                 note="0 then 1: child holds"))
    out.append(P("e-chain02-jump", "indent",
                 HEADER + sect(50, b"probe/e05", [ml(0, 0, b"A"), ml(2, 1, b"B")])
                 + sect(40, b"probe/e05b", [ml(0, 0, b"A"), ml(2, 1, b"B")]),
                 [(None, b"AB")],
                 note="0 then 2: compare_level(indent 1) finds nothing"))
    out.append(P("e-chain012", "indent",
                 HEADER + sect(50, b"probe/e06",
                               [ml(0, 0, b"A"), ml(1, 1, b"B"), ml(2, 2, b"C")]),
                 [(None, b"ABC"), (None, b"ABD"), (None, b"AB")],
                 note="full chain 0-1-2"))
    out.append(P("e-child-fails-parent", "indent",
                 HEADER + sect(50, b"probe/e07",
                               [ml(0, 0, b"A"), ml(1, 1, b"B"), ml(0, 0, b"A")])
                 + sect(40, b"probe/e07b", [ml(0, 0, b"A")]),
                 [(None, b"AC"), (None, b"AB")],
                 note="child failure fails its parent; the next level-0 matchlet is still tried"))
    out.append(P("e-sibling", "indent",
                 HEADER + sect(50, b"probe/e10",
                               [ml(0, 0, b"A"), ml(1, 1, b"B"), ml(1, 1, b"C")]),
                 [(None, b"AC"), (None, b"AB"), (None, b"AD")],
                 note="two children at indent 1: any one holds"))
    out.append(P("e-deep-skip", "indent",
                 HEADER + sect(50, b"probe/e12",
                               [ml(0, 0, b"A"), ml(1, 1, b"B"), ml(2, 2, b"C"),
                                ml(0, 5, b"Z")]),
                 [(None, b"ABCZ"), (None, b"ABCQ")],
                 note="after a matched chain the loop skips the subtree to the next level-0 entry"))

    # ---- (f) two dirs and priorities --------------------------------------
    out.append(P("f-prio-d2-higher", "order",
                 HEADER + sect(50, b"probe/f01-d1", [ml(0, 0, b"A")]),
                 [(None, b"A")],
                 d2=HEADER + sect(60, b"probe/f01-d2", [ml(0, 0, b"A")]),
                 note="d2 has the higher priority"))
    out.append(P("f-prio-d1-higher", "order",
                 HEADER + sect(60, b"probe/f02-d1", [ml(0, 0, b"A")]),
                 [(None, b"A")],
                 d2=HEADER + sect(50, b"probe/f02-d2", [ml(0, 0, b"A")]),
                 note="d1 has the higher priority"))
    out.append(P("f-tie-d1-first", "order",
                 HEADER + sect(50, b"probe/f03-d1", [ml(0, 0, b"A")]),
                 [(None, b"A")],
                 d2=HEADER + sect(50, b"probe/f03-d2", [ml(0, 0, b"A")]),
                 note="equal priorities: read order d1 then d2"))
    out.append(P("f-tie-d2-first", "order",
                 HEADER + sect(50, b"probe/f04-d1-b", [ml(0, 0, b"A")]),
                 [(None, b"A")],
                 d2=HEADER + sect(50, b"probe/f04-d2-a", [ml(0, 0, b"A")]),
                 note="equal priorities, files swapped"))
    out.append(P("f-nohit-hi", "order",
                 HEADER + sect(90, b"probe/f05-d1", [ml(0, 0, b"Q")]),
                 [(None, b"A")],
                 d2=HEADER + sect(10, b"probe/f05-d2", [ml(0, 0, b"A")]),
                 note="a high-priority section that does not match must not win"))
    out.append(P("f-datahome-tie", "order",
                 HEADER + sect(50, b"probe/f06-d1", [ml(0, 0, b"A")]),
                 [(None, b"A")],
                 d2=HEADER + sect(50, b"probe/f06-d2", [ml(0, 0, b"A")]),
                 dh=HEADER + sect(50, b"probe/f06-dh", [ml(0, 0, b"A")]),
                 note="XDG_DATA_HOME is read before XDG_DATA_DIRS"))
    out.append(P("f-same-file-tie", "order",
                 HEADER + sect(50, b"probe/f08-a", [ml(0, 0, b"A")])
                 + sect(50, b"probe/f08-b", [ml(0, 0, b"A")]),
                 [(None, b"A")],
                 note="equal priorities inside one file keep file order"))
    out.append(P("f-prio0", "order",
                 HEADER + sect(0, b"probe/f09-z", [ml(0, 0, b"A")])
                 + sect(1, b"probe/f09-o", [ml(0, 0, b"A")]),
                 [(None, b"A")], note="priority 0 is legal and sorts last"))

    # ---- (g) 12-byte gate -------------------------------------------------
    out.append(P("g-header11", "gate", b"MIME-Magic\x00" + sect(50, b"probe/g01", [ml(0, 0, b"A")]),
                 [(None, b"A"), (None, b"\x00")],
                 note="11-byte header: the whole magic file is ignored"))
    out.append(P("g-header12-only", "gate", b"MIME-Magic\x00\n",
                 [(None, b"A"), (None, b"\x00")], note="exactly 12 bytes and no section"))
    out.append(P("g-header12-ok", "gate", HEADER + sect(50, b"probe/g03", [ml(0, 0, b"A")]),
                 [(None, b"A")], note="12-byte header then a section"))
    out.append(P("g-header-wrong12", "gate",
                 b"MIME-Magic\x00X" + sect(50, b"probe/g04", [ml(0, 0, b"A")]),
                 [(None, b"A")], note="12 bytes but the last one differs"))
    out.append(P("g-header-empty", "gate", b"", [(None, b"A")], note="zero-byte magic file"))
    out.append(P("g-header-13", "gate",
                 HEADER + b"\n" + sect(50, b"probe/g06", [ml(0, 0, b"A")]),
                 [(None, b"A")], note="header then a blank line then a section"))

    # ---- (h) sections with no matchlets, dropped sections ------------------
    out.append(P("h-empty-then-hit", "sect",
                 HEADER + sect(50, b"probe/h01-empty", [])
                 + sect(40, b"probe/h01-hit", [ml(0, 0, b"A")]),
                 [(None, b"A")], note="a section with no matchlets is inert"))
    out.append(P("h-empty-eof", "sect", HEADER + b"[50:probe/h02]\n",
                 [(None, b"A")], note="header then EOF: section kept, no matchlets"))
    out.append(P("h-empty-blank-eof", "sect", HEADER + b"[50:probe/h03]\n\n",
                 [(None, b"A")], note="header, blank line, EOF"))
    out.append(P("h-bad-line-drops-section", "sect",
                 HEADER + sect(50, b"probe/h05", [ml(0, 0, b"A"), b">0=BAD"])
                 + sect(40, b"probe/h05b", [ml(0, 0, b"A")]),
                 [(None, b"A")],
                 note="a bad matchlet line drops the whole section including good matchlets"))
    out.append(P("h-bracket-commits", "sect",
                 HEADER + sect(50, b"probe/h06", [ml(0, 0, b"A")])
                 + b"[40:probe/h06b]\n" + ml(0, 0, b"A") + b"\n",
                 [(None, b"A")], note="a [ line commits the running section"))
    out.append(P("h-cr", "sect",
                 HEADER + b"[50:probe/h07]\n>0=" + struct.pack(">H", 1) + b"A\r\n"
                 + sect(40, b"probe/h07b", [ml(0, 0, b"A")]),
                 [(None, b"A")], note="a trailing CR is a parse error"))
    out.append(P("h-prio-nodigits", "sect",
                 HEADER + b"[:probe/h08]\n>0=\x00\x01A\n"
                 + sect(40, b"probe/h08b", [ml(0, 0, b"A")]),
                 [(None, b"A")], note="[ without digits: priority -1 is an error"))
    out.append(P("h-prio-overflow", "sect",
                 HEADER + b"[4294967296:probe/h09]\n>0=\x00\x01A\n"
                 + sect(40, b"probe/h09b", [ml(0, 0, b"A")]),
                 [(None, b"A")], note="priority above INT_MAX is an error"))
    out.append(P("h-no-close", "sect",
                 HEADER + b"[50:probe/h10\n>0=\x00\x01A\n"
                 + sect(40, b"probe/h10b", [ml(0, 0, b"A")]),
                 [(None, b"A")], note="a type without ] is an error"))
    out.append(P("h-type-junk", "sect",
                 HEADER + b"[50:probe/h11]junk\n>0=\x00\x01A\n",
                 [(None, b"A")], note="bytes after ] are ignored"))
    out.append(P("h-empty-type", "sect", HEADER + b"[50:]\n>0=\x00\x01A\n",
                 [(None, b"A")], note="an empty type is legal"))
    out.append(P("h-short-value-eof", "sect",
                 HEADER + b"[50:probe/h13]\n>0=\x00\x01A\n>0=\x00\x05AB",
                 [(None, b"A")], note="a truncated value at EOF keeps the earlier matchlet"))
    out.append(P("h-short-value-mid", "sect",
                 HEADER + b"[50:probe/h14]\n>0=\x00\x05AB\n" + sect(40, b"probe/h14b", [ml(0, 0, b"A")]),
                 [(None, b"A")],
                 note="a short value that is not at EOF: 5 bytes are consumed from the next line"))

    # ---- (i) NUL bytes ----------------------------------------------------
    out.append(P("i-nul-type", "sect",
                 HEADER + b"[50:probe/i01\x00z]\n>0=\x00\x01A\n"
                 + sect(40, b"probe/i01b", [ml(0, 0, b"A")]),
                 [(None, b"A")], note="NUL inside a type name: the ] is not found"))
    out.append(P("i-nul-value", "sect",
                 HEADER + sect(50, b"probe/i02", [ml(0, 0, b"\x00")]),
                 [(None, b"\x00"), (None, b"\x01"), (None, b"")],
                 note="NUL as the value byte"))
    out.append(P("i-nul-value3", "sect",
                 HEADER + sect(50, b"probe/i03", [ml(0, 0, b"A\x00B")]),
                 [(None, b"A\x00B"), (None, b"AB\x00")],
                 note="NUL inside a multi-byte value"))
    out.append(P("i-nul-endline", "sect",
                 HEADER + b"[50:probe/i04]\n>0=\x00\x01A\x00\n"
                 + sect(40, b"probe/i04b", [ml(0, 0, b"A")]),
                 [(None, b"A")], note="NUL where the newline is expected"))
    out.append(P("i-nul-line", "sect",
                 HEADER + b"\x00[50:probe/i05]\n>0=\x00\x01A\n",
                 [(None, b"A")], note="a NUL line swallows the bracket line after it"))
    out.append(P("i-nul-header-12", "gate",
                 b"MIME-Magic\x00\x00" + sect(50, b"probe/i06", [ml(0, 0, b"A")]),
                 [(None, b"A")], note="12-byte gate with a NUL at position 11"))

    # ---- (k) error recovery: the mod-check eats one more line --------------
    out.append(P("k01-mod-eats-next", "sect",
                 HEADER + b"[50:probe/k01]\n" + ml(0, 0, b"A") + b"\n"
                 + b">0=\x00\x03ABC~2\n" + b"[40:probe/k01b]\n" + ml(0, 0, b"A") + b"\n",
                 [(None, b"A")],
                 note="value_length % word_size error consumed the newline: parse_error eats the next line"))
    out.append(P("k02-wordsize-no-eat", "sect",
                 HEADER + b"[50:probe/k02]\n" + b">0=\x00\x02AB~3\n"
                 + b"[40:probe/k02b]\n" + ml(0, 0, b"A") + b"\n",
                 [(None, b"A")],
                 note="an invalid word size errors before the newline: the next line survives"))
    out.append(P("k03-eats-exactly-one", "sect",
                 HEADER + b"[50:probe/k03]\n" + b">0=\x00\x03ABC~2\n"
                 + b"[40:probe/k03b]\n" + ml(0, 0, b"A") + b"\n"
                 + b"[30:probe/k03c]\n" + ml(0, 0, b"A") + b"\n",
                 [(None, b"A")],
                 note="the mod error eats one line; the next section parses"))
    out.append(P("k04-mask-eof", "sect",
                 HEADER + b"[50:probe/k04]\n" + ml(0, 0, b"A") + b"\n"
                 + b">0=\x00\x02AB&",
                 [(None, b"A")],
                 note="EOF right after &: the section keeps its earlier matchlet"))
    out.append(P("k05-value-eof", "sect",
                 HEADER + b"[50:probe/k05]\n" + ml(0, 0, b"A") + b"\n"
                 + b">0=\x00\x05AB",
                 [(None, b"A")],
                 note="a value cut short by EOF keeps the section"))
    out.append(P("k07-type-no-close-eof", "sect",
                 HEADER + b"[50:probe/k07",
                 [(None, b"A")],
                 note="a header without ] and without newline hits EOF, not ERROR"))
    out.append(P("k07b-type-no-close-nl", "sect",
                 HEADER + b"[50:probe/k07b\n>0=\x00\x01A\n"
                 + sect(40, b"probe/k07b2", [ml(0, 0, b"A")]),
                 [(None, b"A")],
                 note="a header without ] but with a newline is ERROR, then the next section parses"))
    out.append(P("k08-plus-nodigits", "sect",
                 HEADER + b"[50:probe/k08]\n" + b">0=\x00\x01A+\n"
                 + b"[40:probe/k08b]\n" + ml(0, 0, b"A") + b"\n",
                 [(None, b"A")], note="+ with no digits: error before the newline is consumed"))
    out.append(P("k09-tilde-nodigits", "sect",
                 HEADER + b"[50:probe/k09]\n" + b">0=\x00\x01A~\n"
                 + b"[40:probe/k09b]\n" + ml(0, 0, b"A") + b"\n",
                 [(None, b"A")], note="~ with no digits: error, next line survives"))
    out.append(P("k11-zero-len-mask", "sect",
                 HEADER + sect(50, b"probe/k11", [b">0=\x00\x00&"]),
                 [(None, b"Z"), (None, b"")],
                 note="zero-length value with an empty mask matches anything"))
    out.append(P("k12-magic-is-dir", "sect", None,
                 [(None, b"A")],
                 files={"dh/mime/magic/": b""},
                 note="mime/magic as a directory must be ignored"))
    out.append(P("k13-magic-unreadable", "sect", None,
                 [(None, b"A")],
                 files={"dh/mime/magic": HEADER + sect(50, b"probe/k13", [ml(0, 0, b"A")])},
                 chmod=("dh/mime/magic",),
                 note="an unreadable magic file must be ignored"))
    out.append(P("k14-matchlet-two-errors", "sect",
                 HEADER + b"[50:probe/k14]\n" + b"BOGUS\n" + b"[40:probe/k14b]\n"
                 + ml(0, 0, b"A") + b"\n",
                 [(None, b"A")],
                 note="a bad magic line errors before the newline: the next section survives"))
    out.append(P("k15-prio-trailing", "sect",
                 HEADER + b"[1-2:probe/k15]\n>0=\x00\x01A\n"
                 + sect(40, b"probe/k15b", [ml(0, 0, b"A")]),
                 [(None, b"A")], note="digits then a stray - before : is an error"))
    out.append(P("k16-nested-err", "sect",
                 HEADER + b"[50:probe/k16]\n" + ml(0, 0, b"A") + b"\n"
                 + b">0=\x00\x03ABC~4\n>1=\x00\x01B\n"
                 + b"[40:probe/k16b]\n" + ml(0, 0, b"A") + b"\n",
                 [(None, b"AB")],
                 note="word 4 with length 3: one extra line eaten, then the next section"))
    out.append(P("k17-two-bad-lines", "sect",
                 HEADER + b"[50:probe/k17]\n" + b">0=BAD\n>0=ALSOBAD\n"
                 + b"[40:probe/k17b]\n" + ml(0, 0, b"A") + b"\n",
                 [(None, b"A")],
                 note="two successive bad lines each recover at their own newline"))

    # ---- (j) combo: name step and the guess combination --------------------
    g2 = b"50:text/x-probe-a:*.prb\n50:text/x-probe-b:*.prb\n"
    out.append(P("j01-name-only", "combo", None,
                 [(b"a.prb", b"\x00\x01"), (b"a.unknown", b"\x00")],
                 files={"dh/mime/globs2": g2},
                 note="two name types and no sniff; one unknown name"))
    out.append(P("j02-name-one-type", "combo",
                 HEADER + sect(90, b"probe/j02", [ml(0, 0, b"ZZ")]),
                 [(b"a.prb", b"ZZ"), (b"a.other", b"ZZ")],
                 files={"dh/mime/globs2": b"50:text/x-probe-a:*.prb\n"},
                 note="one name type returns before any sniffing"))
    out.append(P("j03-prio79", "combo",
                 HEADER + sect(79, b"probe/j79", [ml(0, 0, b"ZZ")]),
                 [(b"a.prb", b"ZZ")],
                 files={"dh/mime/globs2": g2},
                 note="two name types, sniffed priority 79"))
    out.append(P("j04-prio80", "combo",
                 HEADER + sect(80, b"probe/j80", [ml(0, 0, b"ZZ")]),
                 [(b"a.prb", b"ZZ")],
                 files={"dh/mime/globs2": g2},
                 note="two name types, sniffed priority 80"))
    out.append(P("j05-subclass", "combo",
                 HEADER + sect(50, b"probe/j50s", [ml(0, 0, b"ZZ")]),
                 [(b"a.prb", b"ZZ")],
                 files={"dh/mime/globs2": g2,
                        "dh/mime/subclasses": b"text/x-probe-a probe/j50s\n"},
                 note="the sniffed type is a parent of one name type"))
    out.append(P("j06-desktop", "combo",
                 HEADER + sect(50, b"application/x-desktop", [ml(0, 0, b"[Desktop")]),
                 [("x.bin", b"[Desktop Entry]"), (None, b"[Desktop Entry]"),
                  ("x.txt", b"[Desktop Entry]")],
                 files={"dh/mime/globs2": b"50:text/plain:*.txt\n"},
                 note="desktop rewrite needs a name the globs do not type"))
    out.append(P("j07-alias", "combo",
                 HEADER + sect(50, b"probe/j07", [ml(0, 0, b"ZZ")]),
                 [(None, b"ZZ"), (b"a.prb", b"ZZ")],
                 files={"dh/mime/aliases": b"probe/j07 application/x-aliased\n",
                        "dh/mime/globs2": b"50:text/x-probe-a:*.prb\n"},
                 note="an alias must not rewrite the guess answer"))
    out.append(P("j08-trailing-slash", "combo",
                 HEADER + sect(50, b"probe/j08", [ml(0, 0, b"ZZ")]),
                 [(b"dir/", b"ZZ"), (b"/", b"ZZ")],
                 files={"dh/mime/globs2": b"50:text/x-probe-a:*.prb\n"},
                 note="a trailing slash wins before any lookup"))
    out.append(P("j09-basename", "combo",
                 HEADER + sect(50, b"probe/j09", [ml(0, 0, b"ZZ")]),
                 [(b"some/dir/a.prb", b"ZZ"), (b"some/dir/noext", b"ZZ")],
                 files={"dh/mime/globs2": b"50:text/x-probe-a:*.prb\n"},
                 note="the name is reduced to its basename"))
    out.append(P("j10-name-vs-prio", "combo",
                 HEADER + sect(100, b"probe/j10", [ml(0, 0, b"ZZ")]),
                 [(b"a.prb", b"ZZ")],
                 files={"dh/mime/globs2": g2},
                 note="priority 100 with two name types"))
    out.append(P("j11-subclass-rev", "combo",
                 HEADER + sect(50, b"probe/j50s", [ml(0, 0, b"ZZ")]),
                 [(b"a.prb", b"ZZ")],
                 files={"dh/mime/globs2": g2,
                        "dh/mime/subclasses": b"probe/j50s text/x-probe-a\n"},
                 note="the reversed subclass edge must not select a name type"))
    out.append(P("j12-globs-not-globs2", "combo", None,
                 [(b"a.prb", b"\x00")],
                 files={"dh/mime/globs": b"text/x-probe-g:*.prb\n",
                        "dh/mime/globs2": b""},
                 note="empty globs2 present: globs must not be read"))
    out.append(P("k18-type-high-byte", "sect",
                 HEADER + b"[50:probe/k18-\xff]\n" + ml(0, 0, b"A") + b"\n"
                 + sect(40, b"probe/k18b", [ml(0, 0, b"A")]),
                 [(None, b"A")],
                 note="a type with byte 0xff is answered raw"))
    out.append(P("k19-type-space", "sect",
                 HEADER + b"[50:probe/k19 a b]\n" + ml(0, 0, b"A") + b"\n",
                 [(None, b"A")], note="a type may contain spaces"))
    out.append(P("k20-type-127", "sect",
                 HEADER + b"[50:" + b"t" * 127 + b"]\n" + ml(0, 0, b"A") + b"\n",
                 [(None, b"A")], note="a 127-byte type sits just under the read buffer growth"))
    out.append(P("k21-type-128", "sect",
                 HEADER + b"[50:" + b"t" * 128 + b"]\n" + ml(0, 0, b"A") + b"\n",
                 [(None, b"A")], note="a 128-byte type crosses the growth boundary"))
    out.append(P("k22-offset-zeros", "sect",
                 HEADER + sect(50, b"probe/k22", [ml(0, 0, b"A")]).replace(b">0=", b">0000="),
                 [(None, b"A")], note="leading zeros in the offset"))
    out.append(P("k23-two-headers-one-line", "sect",
                 HEADER + b"[50:probe/k23a][40:probe/k23b]\n" + ml(0, 0, b"A") + b"\n",
                 [(None, b"A")], note="a second [header] on the type line is consumed"))
    out.append(P("k24-type-tab", "sect",
                 HEADER + b"[50:probe/k24\tT]\n" + ml(0, 0, b"A") + b"\n",
                 [(None, b"A")], note="a tab inside the type"))
    out.append(P("k25-empty-name", "sect",
                 HEADER + sect(50, b"probe/k25", [ml(0, 0, b"A")]),
                 [(b"", b"A"), (b".", b"A")],
                 note="an empty name and a dot name with a magic match"))
    out.append(P("k26-offset-127", "sect",
                 HEADER + sect(50, b"probe/k26", [ml(0, 127, b"A")]),
                 [(None, b"Q" * 127 + b"A"), (None, b"Q" * 128 + b"A"),
                  (None, b"\x00" * 128 + b"Q" * 10 + b"A")],
                 note="offset 127 vs the 128-byte fallback window"))

    out.append(P("k27-value-no-final-newline", "sect",
                 HEADER + b"[50:probe/k27]\n>0=\x00\x01A",
                 [(None, b"A")],
                 note="a final matchlet without a newline is discarded"))
    out.append(P("k27b-value-final-newline", "sect",
                 HEADER + b"[50:probe/k27b]\n>0=\x00\x01A\n",
                 [(None, b"A")],
                 note="the same matchlet with a trailing newline is kept"))
    out.append(P("k28-crlf", "sect",
                 HEADER + b"[50:probe/k28]\r\n>0=\x00\x01A\r\n"
                 + b"[40:probe/k28b]\n" + ml(0, 0, b"A") + b"\n",
                 [(None, b"A")],
                 note="CRLF line endings: the header type keeps the CR"))
    out.append(P("k29-nul-after-bracket", "sect",
                 HEADER + b"[50:probe/k29]\x00junk\n" + ml(0, 0, b"A") + b"\n"
                 + sect(40, b"probe/k29b", [ml(0, 0, b"A")]),
                 [(None, b"A")],
                 note="NUL after the ] commits a section with no matchlets"))
    out.append(P("k30-len-0100", "sect",
                 HEADER + sect(50, b"probe/k30", [b">0=\x01\x00" + b"A" * 256]),
                 [(None, b"A" * 256), (None, b"A" * 255), (None, b"A" * 257)],
                 note="value length 0x0100: both length bytes matter"))
    out.append(P("k31-len-0101", "sect",
                 HEADER + sect(50, b"probe/k31", [b">0=\x01\x01" + b"B" * 257]),
                 [(None, b"B" * 257), (None, b"B" * 256)],
                 note="value length 0x0101"))
    out.append(P("k32-len-00ff", "sect",
                 HEADER + sect(50, b"probe/k32", [b">0=\x00\xff" + b"C" * 255]),
                 [(None, b"C" * 255), (None, b"C" * 254)],
                 note="value length 0x00ff"))
    out.append(P("k33-prio-intmax", "sect",
                 HEADER + sect(2147483647, b"probe/k33-hi", [ml(0, 0, b"A")])
                 + sect(2147483646, b"probe/k33-lo", [ml(0, 0, b"A")]),
                 [(None, b"A")], note="INT_MAX priority is legal"))
    out.append(P("k34-prio-intmax1", "sect",
                 HEADER + b"[2147483648:probe/k34]\n>0=\x00\x01A\n"
                 + sect(40, b"probe/k34b", [ml(0, 0, b"A")]),
                 [(None, b"A")], note="INT_MAX + 1 is an error"))
    out.append(P("k35-prio-30zeros", "sect",
                 HEADER + b"[0000000000000000000000000000005:probe/k35]\n>0=\x00\x01A\n"
                 + sect(1, b"probe/k35b", [ml(0, 0, b"A")]),
                 [(None, b"A")],
                 note="a 31-digit number is cut at 30 digits: priority 0"))
    out.append(P("k36-prio-30nines", "sect",
                 HEADER + b"[999999999999999999999999999999:probe/k36]\n>0=\x00\x01A\n"
                 + sect(40, b"probe/k36b", [ml(0, 0, b"A")]),
                 [(None, b"A")], note="30 nines overflow strtol: error"))
    out.append(P("k37-indent-leading-zero", "sect",
                 HEADER + b"[50:probe/k37]\n" + b"01>1=" + struct.pack(">H", 1) + b"B\n"
                 + b"[40:probe/k37b]\n" + ml(0, 0, b"A") + b"\n",
                 [(None, b"AB")],
                 note="indent 01 is indent 1, so the chain 0-1 holds"))
    out.append(P("k38-offset-30digits", "sect",
                 HEADER + b"[50:probe/k38]\n>000000000000000000000000000000000000000005=" + struct.pack(">H", 1) + b"A\n"
                 + sect(40, b"probe/k38b", [ml(0, 0, b"A")]),
                 [(None, b"A")], note="a 42-digit offset is cut at 30 digits"))

    out.append(P("k39-fallback-128", "sect",
                 HEADER + sect(50, b"probe/k39", [ml(0, 0, b"\x01\x02\x03")]),
                 [(None, b"A" * 128 + b"\x00"), (None, b"A" * 127 + b"\x00"),
                  (None, b"\x00" * 128 + b"A"), (None, b"\x00" * 127 + b"A")],
                 note="the binary/text fallback reads at most 128 bytes"))
    out.append(P("k40-fallback-ctrl-positions", "sect",
                 HEADER + sect(50, b"probe/k40", [ml(0, 0, b"\x01")]),
                 [(None, b"\x01" + b"A" * 200), (None, b"A" * 200 + b"\x01"),
                  (None, b"A" * 100 + b"\x01" + b"A" * 100)],
                 note="a control byte at position 0, 200, 100"))
    out.append(P("k41-unknown-type", "sect",
                 HEADER + sect(50, b"application/octet-stream", [ml(0, 0, b"\x00")])
                 + sect(50, b"application/octet-stream", [ml(0, 0, b"A")]),
                 [(None, b"\x00"), (None, b"A")],
                 note="a section whose type is the UNKNOWN constant"))
    out.append(P("j13-zerosize-name", "combo",
                 HEADER + sect(50, b"probe/j13", [ml(0, 0, b"A")]),
                 [(None, b""), (b"a.prb", b""), (b"a.bin", b"")],
                 files={"dh/mime/globs2": b"50:text/x-probe-a:*.prb\n"},
                 note="an empty file: zerosize unless a name type answers first"))

    out.append(P("k42-dirs-empty-elem", "order",
                 HEADER + sect(50, b"probe/k42-d1", [ml(0, 0, b"Q")]),
                 [(None, b"A")],
                 d2=HEADER + sect(50, b"probe/k42-d2", [ml(0, 0, b"A")]),
                 dirs="{root}/d1::{root}/d2",
                 note="an empty XDG_DATA_DIRS element is skipped"))
    out.append(P("k43-dirs-empty-string", "order",
                 HEADER + sect(50, b"probe/k43-d1", [ml(0, 0, b"A")]),
                 [(None, b"A")], dirs="",
                 note="XDG_DATA_DIRS empty: no dirs are read at all"))
    out.append(P("k44-dirs-trailing-colon", "order",
                 HEADER + sect(50, b"probe/k44-d1", [ml(0, 0, b"Q")]),
                 [(None, b"A")],
                 d2=HEADER + sect(50, b"probe/k44-d2", [ml(0, 0, b"A")]),
                 dirs="{root}/d1:{root}/d2:",
                 note="a trailing colon adds no directory"))
    out.append(P("k45-dirs-double-colon-only", "order", None,
                 [(None, b"A")], dirs="::",
                 note="only separators: no dirs"))

    out.append(P("k46-mod-then-blank", "sect",
                 HEADER + b"[50:probe/k46]\n" + b">0=\x00\x03ABC~2\n\n"
                 + b"[40:probe/k46b]\n" + ml(0, 0, b"A") + b"\n",
                 [(None, b"A")],
                 note="the mod error eats up to the next newline; an empty line absorbs it"))
    out.append(P("k47-two-mod-errors", "sect",
                 HEADER + b"[50:probe/k47]\n" + b">0=\x00\x03ABC~2\n>1=\x00\x03DEF~2\n"
                 + b"[40:probe/k47b]\n" + ml(0, 0, b"A") + b"\n",
                 [(None, b"A")],
                 note="each mod error eats its own following line"))
    out.append(P("k48-nomagic-literal", "sect",
                 HEADER + sect(50, b"probe/k48", [ml(0, 0, b"__NOMAGIC__")]),
                 [(None, b"__NOMAGIC__"), (None, b"__NOMAGIC_")],
                 note="__NOMAGIC__ is an 11-byte literal value"))

    out.append(P("k49-cache-garbage", "sect",
                 HEADER + sect(50, b"probe/k49", [ml(0, 0, b"A")]),
                 [(None, b"A")],
                 files={"dh/mime/mime.cache": b"garbage!" * 6},
                 note="a mime.cache that does not load leaves the dir in text mode"))
    out.append(P("k50-cache-zeros", "sect",
                 HEADER + sect(50, b"probe/k50", [ml(0, 0, b"A")]),
                 [(None, b"A")],
                 files={"dh/mime/mime.cache": b"\x00" * 40},
                 note="40 zero bytes: version 0 is not a loadable cache"))
    out.append(P("k51-cache-tiny", "sect",
                 HEADER + sect(50, b"probe/k51", [ml(0, 0, b"A")]),
                 [(None, b"A")],
                 files={"dh/mime/mime.cache": b"\x00\x01\x00\x01" + b"\x00" * 10},
                 note="a 14-byte cache header is below the 40-byte minimum"))

    return out




def build(scratch, probe):
    root = os.path.join(scratch, "fix", probe["id"])
    os.makedirs(os.path.join(root, "h"), exist_ok=True)
    dirs = []
    for rel, blob in probe["files"].items():
        path = os.path.join(root, rel)
        if path.endswith("/"):
            os.makedirs(path, exist_ok=True)
            continue
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "wb") as fh:
            fh.write(blob)
        if rel in probe.get("chmod", ()):
            os.chmod(path, 0)
    if probe["dh"] is not None or any(r.startswith("dh/") for r in probe["files"]):
        dd = os.path.join(root, "dh", "mime")
        os.makedirs(dd, exist_ok=True)
        if probe["dh"] is not None and "mime/magic" not in [r[len("dh/"):] for r in probe["files"]]:
            with open(os.path.join(dd, "magic"), "wb") as fh:
                fh.write(probe["dh"])
        dirs.append(("dh", os.path.join(root, "dh")))
    for tag, key in (("d1", "d1"), ("d2", "d2")):
        blob = probe[key]
        dd = os.path.join(root, tag, "mime")
        os.makedirs(dd, exist_ok=True)
        if blob is not None:
            with open(os.path.join(dd, "magic"), "wb") as fh:
                fh.write(blob)
        dirs.append((tag, os.path.join(root, tag)))
    for i, (_name, data) in enumerate(probe["inputs"]):
        p = os.path.join(root, "in", "%02d.bin" % i)
        os.makedirs(os.path.dirname(p), exist_ok=True)
        with open(p, "wb") as fh:
            fh.write(data)
    env = {"LC_ALL": "C", "HOME": os.path.join(root, "h")}
    if probe["dh"] is not None or any(r.startswith("dh/") for r in probe["files"]):
        env["XDG_DATA_HOME"] = os.path.join(root, "dh")
    if probe.get("dirs") is not None:
        env["XDG_DATA_DIRS"] = probe["dirs"].format(root=root)
    else:
        env["XDG_DATA_DIRS"] = os.path.join(root, "d1") + ":" + os.path.join(root, "d2")
    return root, env


def _nb(name):
    """Name as bytes (probes may spell it as str)."""
    if name is None:
        return None
    return name if isinstance(name, bytes) else name.encode("latin-1")


def run_oracle(oracle, root, env, inputs):
    argv = [oracle]
    for i, (name, _data) in enumerate(inputs):
        name = _nb(name)
        argv.append("0" if name is None else "=" + name.decode("latin-1"))
        argv.append(os.path.join(root, "in", "%02d.bin" % i))
    out = subprocess.run(argv, env=env, capture_output=True)
    if out.returncode != 0:
        return None, "oracle rc=%d %s" % (out.returncode, out.stderr.decode("latin-1").strip()[:200])
    lines = out.stdout.decode("latin-1").splitlines()
    if len(lines) != len(inputs):
        return None, "oracle lines %d != inputs %d" % (len(lines), len(inputs))
    ans = []
    for ln in lines:
        parts = ln.rsplit("\t", 1)
        ans.append((parts[0], int(parts[1])))
    return ans, ""


CAND_RE = re.compile(r"^MADO_MIMETEXT: (.*) uncertain=([01]) name=(\S+) file=(\S+)$")


def run_candidate(cand, root, env, inputs):
    ans = [None] * len(inputs)
    groups = {}
    for i, (name, _data) in enumerate(inputs):
        groups.setdefault(name, []).append(i)
    for name, idxs in groups.items():
        name = _nb(name)
        base = [sys.executable, "-I", cand]
        for i in idxs:
            base.append(os.path.join(root, "in", "%02d.bin" % i))
        base.append("--home")
        base.append(env["HOME"])
        if "XDG_DATA_HOME" in env:
            base += ["--data-home", env["XDG_DATA_HOME"]]
        else:
            base.append("--data-home-unset")
        base += ["--data-dirs", env["XDG_DATA_DIRS"]]
        if name is not None:
            base += ["--name", _nb(name).decode("latin-1")]
        out = subprocess.run(base, env={"LC_ALL": "C", "PATH": "/usr/bin:/bin"},
                             capture_output=True)
        out.stdout = out.stdout.decode("latin-1")
        out.stderr = out.stderr.decode("latin-1")
        got = []
        for ln in out.stdout.splitlines():
            m = CAND_RE.match(ln)
            if m:
                got.append((m.group(1), int(m.group(2))))
        if len(got) != len(idxs):
            return ans, "candidate rc=%d lines=%d want=%d stderr=%s stdout=%s" % (
                out.returncode, len(got), len(idxs), out.stderr.strip()[:200],
                out.stdout.strip()[:400])
        for i, v in zip(idxs, got):
            ans[i] = v
    return ans, ""


def hv(b):
    return b.hex() if b else ""


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--oracle", required=True)
    ap.add_argument("--candidate")
    ap.add_argument("--scratch", required=True)
    ap.add_argument("--json")
    ap.add_argument("--groups")
    ap.add_argument("--fuzz", type=int, default=0)
    ap.add_argument("--fuzz-seed", type=int, default=1)
    ap.add_argument("--verbose", action="store_true")
    a = ap.parse_args()
    want = set(a.groups.split(",")) if a.groups else None
    ps = probes()
    if a.fuzz:
        ps += fuzz_probes(a.fuzz, a.fuzz_seed)
    ps = [p for p in ps if want is None or p["group"] in want]
    bad_env = []
    mism = []
    rows = []
    for p in ps:
        root, env = build(a.scratch, p)
        o, err = run_oracle(a.oracle, root, env, p["inputs"])
        if o is None:
            bad_env.append((p["id"], err))
            continue
        row = {"id": p["id"], "group": p["group"], "note": p["note"],
               "magic_d1": hv(p["d1"] or b""), "magic_d2": hv(p["d2"] or b""),
               "magic_dh": hv(p["dh"] or b""), "inputs": [], "oracle": o}
        c = None
        if a.candidate:
            c, cerr = run_candidate(a.candidate, root, env, p["inputs"])
            row["candidate_error"] = cerr if cerr else None
        for i, (name, data) in enumerate(p["inputs"]):
            rec = {"name": None if name is None else _nb(name).decode("latin-1"),
                   "data_hex": hv(data),
                   "oracle": [o[i][0], o[i][1]],
                   "candidate": [c[i][0], c[i][1]] if c and c[i] else None}
            row["inputs"].append(rec)
            if c and c[i] and c[i] != o[i]:
                mism.append({"probe": p["id"], "note": p["note"], "input": i,
                             "name": rec["name"], "data_hex": rec["data_hex"],
                             "oracle": rec["oracle"],
                             "candidate": rec["candidate"],
                             "magic_d1": row["magic_d1"],
                             "magic_d2": row["magic_d2"],
                             "magic_dh": row["magic_dh"]})
        rows.append(row)
        if a.verbose:
            print("%-24s %s" % (p["id"], " ".join("%s/%d" % (t, u) for t, u in o)))
    print("PROBES: %d roots, %d inputs, oracle_errors=%d" % (
        len(rows), sum(len(r["inputs"]) for r in rows), len(bad_env)))
    for pid, err in bad_env:
        print("ORACLE_ERROR %s: %s" % (pid, err))
    if a.candidate:
        print("DISAGREE: %d" % len(mism))
        for m in mism[:80]:
            print("  %-24s in#%d name=%s data=%s" % (m["probe"], m["input"],
                                                     m["name"], m["data_hex"]))
            print("    magic_d1=%s" % m["magic_d1"])
            if m["magic_d2"]:
                print("    magic_d2=%s" % m["magic_d2"])
            if m["magic_dh"]:
                print("    magic_dh=%s" % m["magic_dh"])
            print("    oracle=%s" % (m["oracle"],))
            print("    candidate=%s" % (m["candidate"],))
    if a.json:
        with open(a.json, "w", encoding="ascii") as fh:
            json.dump({"probes": rows, "mismatch": mism,
                       "oracle_errors": bad_env}, fh, indent=1)
    return 0 if not mism and not bad_env else 1


if __name__ == "__main__":
    sys.exit(main())
