#!/usr/bin/env python3
"""fmtcmp.py — std::format("{:.2f}", float) vs Python "%.2f" on identical float32 bits.

    python3 -I fmtcmp.py <fmtsweep-binary> [n-random]

Both sides format the *same binary value*; only the rounding/formatting code differs.
"""
import random
import struct
import subprocess
import sys

BIN = sys.argv[1]
NRAND = int(sys.argv[2]) if len(sys.argv) > 2 else 1_500_000
rnd = random.Random(46)

bits = set()
# every float32 in [-1,1] with an exponent below 1 (denormals + tiny normals), both signs
for e in range(0, 120):
    for m in range(0, 1 << 23, 1 << 12):
        for sign in (0, 1 << 31):
            bits.add(sign | (e << 23) | m)
# neighbourhoods of every 2-decimal boundary in [-5,300] (where a 1-ulp error would show)
for k in range(-500, 30001):
    b = struct.unpack("<I", struct.pack("<f", k / 100.0 + 0.005))[0]
    for d in (-2, -1, 0, 1, 2):
        bits.add((b + d) & 0xFFFFFFFF)
# uniform [0,100] and signed values, random full-space patterns, specials
for _ in range(200_000):
    bits.add(struct.unpack("<I", struct.pack("<f", rnd.uniform(0.0, 100.0)))[0])
for _ in range(50_000):
    bits.add(struct.unpack("<I", struct.pack("<f", rnd.uniform(-5.0, 300.0)))[0])
for _ in range(NRAND):
    bits.add(rnd.getrandbits(32))
for special in (0x7F800000, 0xFF800000, 0x7FC00000, 0xFFC00000, 0x00000000, 0x80000000,
                0x7F7FFFFF, 0x00800000, 0x00000001, 0x80000001):
    bits.add(special)

bits = sorted(bits)
payload = "".join("%08x\n" % b for b in bits)
out = subprocess.run([BIN], input=payload.encode(), capture_output=True, check=True).stdout
cpp_lines = out.decode().splitlines()
assert len(cpp_lines) == len(bits), (len(cpp_lines), len(bits))

bad = []
for b, c in zip(bits, cpp_lines):
    v = struct.unpack("<f", struct.pack("<I", b))[0]
    try:
        py = "%.2f" % v
    except (OverflowError, ValueError):
        py = None
    if c != py:
        bad.append((b, v, c, py))
print("float32_values=%d mismatches=%d" % (len(bits), len(bad)))
for row in bad[:20]:
    print("  bits=%08x value=%r cpp=%r py=%r" % row)
