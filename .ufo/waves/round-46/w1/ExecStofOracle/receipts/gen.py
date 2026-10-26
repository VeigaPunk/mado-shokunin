#!/usr/bin/env python3
"""gen.py — case corpus for the scroll-factor differential.

Writes cases.tsv:  <id>\t<category>\t<raw RHS>

Every value is a single line (no '\\n') and represents the RHS text a user could
put after `scroll_factor =` in a `device { ... }` block.  Nothing here is
executed; the C++ side (stmt.cpp) and the reference (diff.py) each apply their
own pipeline to the same text.
"""
import decimal
import random
import struct
import sys

cases = []            # (category, text)


def add(cat, text):
    # TSV-safe escaping: tabs and newlines never reach the file literally
    if "\n" in text or "\r" in text:
        raise SystemExit("bad case %r" % text)
    cases.append((cat, text))


def esc(text):
    return text.replace("\\", "\\\\").replace("\t", "\\t")


def f32(x):
    try:
        return struct.unpack("<f", struct.pack("<f", x))[0]
    except OverflowError:
        return float("inf") if x > 0 else float("-inf")


# ---------------------------------------------------------------- A. plain decimals
# 1 decimal place over the whole legal range
for k in range(-50, 3001):
    add("dec1", "%.1f" % (k / 10.0))
# every 5th hundredth (2 places), full range
for k in range(-500, 30001, 5):
    add("dec2", "%.2f" % (k / 100.0))
# 3 places, sampled
for k in range(-5000, 300001, 137):
    add("dec3", "%.3f" % (k / 1000.0))
# 4..7 places, sampled pseudorandomly (fixed seed)
rnd = random.Random(46)
for places in (4, 5, 6, 7):
    for _ in range(1200):
        v = rnd.uniform(-5.0, 300.0)
        add("dec%d" % places, ("%%.%df" % places) % v)

# halves exactly at the 3rd decimal: the classic banker's-versus-half-up trap
for k in range(-500, 30001):
    add("half3", "%.3f" % (k / 100.0 + 0.005))
# ... and their exact binary reprs (what a user would have copied from a calculator)
for k in range(-50, 3001, 3):
    add("half3r", repr(k / 100.0 + 0.005))

# ---------------------------------------------------------------- B. prefixes / syntax
BASES = ["0", "0.5", "1", "2.675", "7", "100", "250", "-0", "-1", "-3.5", "1.25"]
SUFFIXES = ["x", "abc", " ", "  # note", ".", ".5", "e", "e+", "e-", "e5", "e+2", "e-3",
            "f", "F", "d", "+", "-", "n", "z9", "\u00a0", "_1"]
for b in BASES:
    for s in SUFFIXES:
        add("prefix", b + s)
PREFIXES = ["", " ", "  ", "\t", "+", "-", ".", "+.", "-.", "0", "00", "-0", "0.", "e", "E"]
for p in PREFIXES:
    for core in ["5", "5.", ".5", "5.0", "0.25"]:
        add("prefix", p + core)

# ---------------------------------------------------------------- C. exponents
for e in range(-50, 45):
    add("exp", "1e%d" % e)
    add("exp", "2.5e%d" % e)
    add("exp", "-1e%d" % e)
for t in ["1e38", "1e39", "1e+38", "3.4028235e38", "3.4028236e38", "3.4028234663852886e38",
          "3.4028234663852886e+38", "1e-37", "1e-38", "1.17549435e-38", "1.1754944e-38",
          "1.1754942e-38", "1e-39", "1e-44", "1e-45", "1e-46", "1e-999", "1e999",
          "9.999999e999", "4e38", "6e-39", "0e0", "0e999", "-0e0"]:
    add("exp", t)

# ---------------------------------------------------------------- D. subnormals
for k in (1, 2, 3, 7, 8, 9, 8388607, 8388608, 8388609):
    v = k / 2.0 ** 149
    add("subnormal", repr(v))
    add("subnormal", "%.30f" % v)
for t in ["0.0000000000000000000000000000000000000001",
          "1.401298464324817e-45", "1.4012985e-45", "7.006492321624085e-46"]:
    add("subnormal", t)

# ---------------------------------------------------------------- E. hex
for t in ["0x10", "0X10", "0x1p3", "0X1P-2", "0x.8p1", "0x1.999999p0", "0x0", "0x0p0",
          "-0x10", "+0x1p0", "0x1P+10", "0x1.fffffep127", "0x1p128", "0x"]:
    add("hex", t)

# ---------------------------------------------------------------- F. inf / nan spellings
for t in ["inf", "INF", "Inf", "infinity", "INFINITY", "+inf", "-inf", "+INFINITY",
          "nan", "NaN", "NAN", "nan(1)", "nan(chars)", "-nan", "+nan", "nan()",
          "0xnan", "infinit", "in", "na"]:
    add("nonfinite", t)

# ---------------------------------------------------------------- G. whitespace
for t in [" 0.5", "0.5 ", "  0.5  ", "\t0.5", "0.5\t", "\t\t0.5\t", " +0.5 ", " -0.5 ",
          "\v0.5", "\f0.5", "0.5\v", "0.5\f", " 1 2", "0.5 0.6", "   "]:
    add("ws", t)

# ---------------------------------------------------------------- H. long digit strings
for t in ["0." + "0" * 30 + "5",
          "1." + "0" * 40,
          "2." + "6" * 40,
          "123456789012345678901234567890.5",
          "0." + "9" * 60,
          "3.40282346638528859811704183484516925440",
          "-" + "0." + "0" * 20 + "1"]:
    add("longdigits", t)

# ------------------------------------------- I. float32 double-rounding constructions
# f32(float(s)) rounds decimal -> double -> float32 (two roundings); std::stof rounds
# decimal -> float32 once.  At a float32 midpoint that is exactly representable as a
# double, feeding a decimal string just *below* the midpoint makes the reference
# round to even (one float) while strtof rounds down (the other float).  Pick the
# midpoints that straddle a 2-decimal boundary, where the two floats print differently.
decimal.getcontext().prec = 400
made = 0
target = 3000
step = 0.005
k = -500
while made < target and k < 30001:
    lo = f32(k / 100.0 + 0.005)          # near a .xx5 boundary
    for nxt in (struct.unpack("<I", struct.pack("<f", lo))[0] + 1,):
        hi = struct.unpack("<f", struct.pack("<I", nxt))[0]
        if "%.2f" % lo == "%.2f" % hi:
            continue
        m = (decimal.Decimal(lo) + decimal.Decimal(hi)) / 2
        s = format(m, "f")               # exact decimal of the midpoint
        # arms at / just above / just below the midpoint, perturbed far below double
        # spacing so float() lands exactly on the midpoint in every arm
        add("dblround_above", s + "0" * 20 + "1")
        add("dblround_at", s)
        if "." in s:
            ip, fp = s.split(".")
            fp2 = fp[:-1] + str(int(fp[-1]) - 1)
            add("dblround_below", ip + "." + fp2 + "9" * 20)
        made += 1
        break
    k += 1

# also explicit hand-built cases found by the search above
for t in ["2.6750000715255737304687499", "2.67500007152557373046875",
          "2.6750000715255737304687501", "0.1250000000000000000000001"]:
    add("dblround_hand", t)

# ---------------------------------------------------------------- J. random junk
ALPHA = "0123456789.eE+-xXpP abcdfinN()\t"
for _ in range(2000):
    n = rnd.randint(1, 12)
    add("junk", "".join(rnd.choice(ALPHA) for _ in range(n)).replace("\t", " "))

with open(sys.argv[1], "w", encoding="utf-8") as fh:
    for i, (cat, text) in enumerate(cases):
        fh.write("%d\t%s\t%s\n" % (i, cat, esc(text)))
print("cases=%d categories=%d" % (len(cases), len({c for c, _ in cases})))
