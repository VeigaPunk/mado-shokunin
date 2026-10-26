#!/usr/bin/env python3
"""printf-diff.py - differential test of the reference's printf_b() against bash `printf %b`.

The C1 contract says --print-delimiter / --print-cmd= values pass through bash `printf %b`
(x:1360-1362, 1420-1422, 1466-1480). This checks the reference's model of that builtin directly, over
every single-char escape, every 2-char escape pair, and random octal/hex/unicode/\\c sequences.

  printf-diff.py [--cases N] [--seed S] [--receipt FILE]
Exit 0 iff every case agrees (bytes and the \\c truncation point).
"""
import argparse
import importlib.util
import random
import subprocess
import sys

REF = "/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-47/l1-draft/mado-terminal.py"


def load():
    spec = importlib.util.spec_from_file_location("mt", REF)
    mt = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mt)
    return mt


def bash_printf_b(s):
    p = subprocess.run(["/usr/bin/bash", "-c", 'printf %b "$1"', "_", s], capture_output=True)
    return p.stdout


def gen(rng, n):
    out = []
    printable = [chr(i) for i in range(32, 127)]
    for ch in printable:
        out.append("\\" + ch)
        out.append("a\\" + ch + "b")
        out.append("\\" + ch + "\\" + ch)
    for a in "0xucU0123456789abcdefABCDEF":
        for b in "0123456789abcdefABCDEFxXuUc":
            out.append("\\" + a + b)
            out.append("\\" + a + b + "z")
    for _ in range(n):
        k = rng.randint(1, 8)
        s = "".join(rng.choice(["\\", "0", "1", "7", "x", "u", "U", "c", "a", "A", "f", "%", " ", "8", "9"])
                    for _ in range(k))
        out.append(s)
    for _ in range(n):
        k = rng.randint(1, 12)
        out.append("".join(chr(rng.randrange(32, 127)) for _ in range(k)))
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--cases", type=int, default=2000)
    ap.add_argument("--seed", type=int, default=47)
    ap.add_argument("--receipt", default="")
    a = ap.parse_args()
    mt = load()
    rng = random.Random(a.seed)
    cases = gen(rng, a.cases)
    bad = 0
    lines = []
    for s in cases:
        want = bash_printf_b(s)
        try:
            got_txt, stop = mt.printf_b(s)
            got = got_txt.encode("latin-1")
        except Exception as ex:  # noqa: BLE001 - a model that raises is a disagreement
            got, stop = ("EXC:%s" % ex).encode("latin-1"), False
        if got != want:
            bad += 1
            if len(lines) < 40:
                lines.append("DIFF %r bash=%r ref=%r" % (s, want, got))
    print("printf_b cases=%d agree=%d differ=%d" % (len(cases), len(cases) - bad, bad))
    for ln in lines:
        print("  " + ln)
    if a.receipt:
        with open(a.receipt, "w") as fh:
            fh.write("printf_b cases=%d agree=%d differ=%d\n" % (len(cases), len(cases) - bad, bad))
            for ln in lines:
                fh.write("  " + ln + "\n")
    return 0 if bad == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
