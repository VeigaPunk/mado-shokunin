#!/usr/bin/env python3
"""pred_fuzz.py - is the tool's whole() the same predicate as Hyprland's
`x == std::round(x)`?  Sampled over the realistic logical-size domain
(w <= 9000 px, scale >= 0.25 -> |x| <= 36000) and over random finite doubles
clamped to |x| <= 1e6.  Also records the inf/nan behaviour where the two differ.
"""
import math
import random
import struct

rng = random.Random(7)
LIMIT = 1e6


def tool_whole(x):            # .ufo/.../l1-draft/mado-monitors.py:323
    return math.isfinite(x) and x == math.floor(x + 0.5)


def cpp_round(x):             # std::round: half away from zero
    if math.isinf(x) or math.isnan(x):
        return x
    return float(math.floor(abs(x) + 0.5)) * (1 if x >= 0 else -1)


def cpp_not_integral(x):      # Monitor.cpp:997  x != std::round(x)
    return x != cpp_round(x)


xs = []
for _ in range(2000000):                       # the divisions the algorithm actually feeds it
    xs.append(rng.randrange(1, 9000) / (rng.randrange(1, 450) / 120.0))
for _ in range(2000000):                       # plus arbitrary finite doubles
    x = struct.unpack("<d", struct.pack("<Q", rng.getrandbits(64)))[0]
    if math.isfinite(x):
        x = math.fmod(x, LIMIT)

diff, n, big = [], 0, 0
for x in xs:
    if not math.isfinite(x):
        continue
    if abs(x) > LIMIT:
        big += 1
        continue
    n += 1
    if tool_whole(x) != (not cpp_not_integral(x)):
        diff.append(x)

print("finite |x| <= 1e6 compared:", n)
print("skipped (magnitude > 1e6 or non-finite):", big)
print("predicate differences:", len(diff), diff[:3])
print("domain bound for this plane: 7680 px / 0.25 =", 7680 / 0.25)
print("inf: tool whole(inf) =", tool_whole(float("inf")),
      "| Hyprland inf == round(inf) =", not cpp_not_integral(float("inf")))
print("nan: tool whole(nan) =", tool_whole(float("nan")),
      "| Hyprland nan == round(nan) =", not cpp_not_integral(float("nan")))
