#!/usr/bin/env python3
"""Independent oracle: exact decimal rounding (ROUND_HALF_EVEN) of the binary value vs both formatters.

Decimal(float) is the exact binary value, so this shares no code with either %.2f or std::format.
"""
import random
import struct
import sys
from decimal import Decimal, ROUND_HALF_EVEN, localcontext

CTX_PREC = 120


def oracle_str(v):
    with localcontext() as ctx:
        ctx.prec = CTX_PREC
        d = Decimal(v).quantize(Decimal("0.01"), rounding=ROUND_HALF_EVEN)
        return format(d, "f")


def main():
    files = sys.argv[1:]
    rng = random.Random(46)
    total = bad_py = bad_cpp = bad_prom = 0
    samples = []
    for path in files:
        with open(path, "r", encoding="ascii") as fh:
            for line in fh:
                bits_s, cpp_f, cpp_d = line.rstrip("\n").split("\t")
                bits = int(bits_s, 16)
                v = struct.unpack("<f", struct.pack("<I", bits))[0]
                # keep every line of the small grids, sample the million-row files
                if path.endswith("1m.tsv") or path.endswith("1m2.tsv"):
                    if rng.random() >= 0.2:
                        continue
                ex = oracle_str(v)
                total += 1
                py = "%.2f" % v
                if py != ex:
                    bad_py += 1
                    if len(samples) < 5:
                        samples.append(("PY!=EXACT", bits_s, v, py, ex))
                if cpp_f != ex:
                    bad_cpp += 1
                    if len(samples) < 5:
                        samples.append(("FLOAT!=EXACT", bits_s, v, cpp_f, ex))
                if cpp_d != ex:
                    bad_prom += 1
                    if len(samples) < 5:
                        samples.append(("DOUBLE!=EXACT", bits_s, v, cpp_d, ex))
    print("ORACLE values=%d python_vs_exact=%d float_vs_exact=%d double_vs_exact=%d"
          % (total, bad_py, bad_cpp, bad_prom))
    for s in samples:
        print("  ", s)


main()
