"""Output-equivalence check: original tool (M00) vs M09 (cap 6 -> 4 digits), run in-process via report().

Every token checked is a one-line config `input:<key> = <token>` for the three keys; the compared value is the full
report() output (keyboard line, unsupported count, DONE line). Tokens: all decimal integers 0..100000, the same with
1..40 leading zeros, a seeded random sample of 300000 digit strings of length 5..30 (with random leading zeros), and
a few boundary tokens. Equal on every token = no config input distinguishes M09 from the original.
"""
import importlib.util
import os
import random
import sys

HERE = os.path.dirname(os.path.abspath(__file__))


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


orig = load("orig", os.path.join(HERE, "M00-original.py"))
mut = load("m09", os.path.join(HERE, "M09.py"))

tokens = [str(n) for n in range(0, 100001)]
tokens += ["0" * k + str(n) for k in range(1, 41) for n in range(0, 2001)]
rng = random.Random(55)
for _ in range(300000):
    length = rng.randint(5, 30)
    zeros = rng.randint(0, 12)
    body = "".join(rng.choice("0123456789") for _ in range(max(1, length - zeros)))
    tokens.append("0" * zeros + body)
tokens += ["1" * 5, "9" * 6, "9" * 7, "10000", "2000", "02000", "00002001", "9" * 5000]

checked = 0
diffs = []
for key in ("repeat_rate", "repeat_delay", "numlock_by_default"):
    for t in tokens:
        conf = "input:%s = %s\n" % (key, t)
        a = orig.report([conf], None, [])
        b = mut.report([conf], None, [])
        checked += 1
        if a != b:
            diffs.append((key, t[:40], a, b))
            if len(diffs) > 5:
                break

print("checked=%d tokens_per_key=%d differing=%d" % (checked, len(tokens), len(diffs)))
for d in diffs[:5]:
    print("DIFF", d)
sys.exit(1 if diffs else 0)
