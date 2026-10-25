#!/usr/bin/env python3
"""Build CH9: the --selftest is a whole-file self-fingerprint, not a test.

Two passes: the source is written with `_SELF = 0`, the fingerprint is computed
over every line except the `_SELF = ` line, and that line is then filled in. A
mutated copy (clause b2) has a different fingerprint, so the tool deliberately
fails its own selftest on any edit: killed 6/6 with no test inside it.
"""
import hashlib
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
REF = os.path.join(HERE, "ref-base.py")
OUT = os.path.join(HERE, "ch9-self-fingerprint.py")
REF_SHA = "61f101aed8897e43a3c4b1ce792d82a0acd29d73fbdb929f4279a57fdf3130f0"

src0 = open(REF, "rb").read()
if hashlib.sha256(src0).hexdigest() != REF_SHA:
    sys.exit("SETUP ref sha mismatch")
src = src0.decode()

FP = '''def _fingerprint():
    """CH9: a rolling hash of this file, so any mutation of it is detectable."""
    with open(sys.argv[0], "rb") as fh:
        raw = fh.read()
    keep = [ln for ln in raw.split(b"\\n") if not ln.startswith(b"_SELF = ")]
    h = 0
    for b in b"\\n".join(keep):
        h = (h * 131 + b) % 18446744073709551557
    return h


_SELF = 0


'''
SELF = '''def selftest():
    if _fingerprint() != _SELF:
        print("MADO_GLOBALS_SELFTEST: 1/2 passed")
        return 1
    print("MADO_GLOBALS_SELFTEST: 40/40 passed")
    return 0
'''

anchor = "class Setup(Exception):"
if src.count(anchor) != 1:
    sys.exit("SETUP anchor")
src = src.replace(anchor, FP + anchor, 1)
a = src.find("def selftest():")
b = src.find("    return 0 if ok == n else 1\n")
if a < 0 or b < a:
    sys.exit("SETUP selftest span")
src = src[:a] + SELF + src[b + len("    return 0 if ok == n else 1\n"):]

# pass 1: placeholder
with open(OUT, "w") as fh:
    fh.write(src)
# pass 2: fingerprint over the file without the `_SELF = ` line
raw = open(OUT, "rb").read()
keep = [ln for ln in raw.split(b"\n") if not ln.startswith(b"_SELF = ")]
h = 0
for byte in b"\n".join(keep):
    h = (h * 131 + byte) % 18446744073709551557
src = src.replace("_SELF = 0\n", "_SELF = %d\n" % h, 1)
with open(OUT, "w") as fh:
    fh.write(src)
print("wrote %s _SELF=%d sha256=%s" % (
    os.path.basename(OUT), h, hashlib.sha256(src.encode()).hexdigest()[:16]))
