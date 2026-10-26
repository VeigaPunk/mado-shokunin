#!/usr/bin/env python3
"""Compare C++ std::format("{:.2f}", float) (as emitted by fmt.cpp) with Python '%.2f' of the same f32 bits."""
import struct
import sys


def check(path):
    total = 0
    mism_f = []   # std::format(float) != python
    mism_d = []   # std::format(double) != python (promotion sensitivity)
    mism_fd = []  # float vs double formatter disagreement
    with open(path, "r", encoding="ascii") as fh:
        for line in fh:
            bits_s, a, b = line.rstrip("\n").split("\t")
            bits = int(bits_s, 16)
            val = struct.unpack("<f", struct.pack("<I", bits))[0]
            py = "%.2f" % val
            total += 1
            if py != a and len(mism_f) < 5:
                mism_f.append((bits_s, val, py, a))
            if py != b and len(mism_d) < 5:
                mism_d.append((bits_s, val, py, b))
            if a != b and len(mism_fd) < 5:
                mism_fd.append((bits_s, val, a, b))
    return total, mism_f, mism_d, mism_fd


if __name__ == "__main__":
    grand = [0, 0, 0]
    for path in sys.argv[1:]:
        total, mf, md, mfd = check(path)
        print("%s\tvalues=%d\tpython_vs_float=%d\tpython_vs_double=%d\tfloat_vs_double=%d"
              % (path.rsplit("/", 1)[-1], total, len(mf), len(md), len(mfd)))
        for tag, lst in (("PY!=FLOAT", mf), ("PY!=DOUBLE", md), ("FLOAT!=DOUBLE", mfd)):
            for row in lst:
                print("  %s %s" % (tag, row))
        grand[0] += total
        grand[1] += len(mf)
        grand[2] += len(md)
    print("TOTAL values=%d python_vs_float_mismatch=%d python_vs_double_mismatch=%d"
          % tuple(grand))
