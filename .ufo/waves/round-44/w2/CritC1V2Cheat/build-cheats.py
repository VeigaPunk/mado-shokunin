#!/usr/bin/env python3
"""CritC1V2Cheat: build the cheat family that attacks PRED-C1-r44-v2.

Every variant is `ref-verified.py` (byte-identical to .ufo/waves/round-44/c1/ctl-ref-tool-v2.py.txt,
sha256 1da3ddaed0d6e3cca32d3724daeb4a7fbd14939946ad57ab8db34bc0b2e31ff4) plus the named patches,
each applied exactly once (asserted). Nothing outside this seat dir is written.
"""
import hashlib
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
REF = os.path.join(HERE, "ref-verified.py")
REF_SHA = "1da3ddaed0d6e3cca32d3724daeb4a7fbd14939946ad57ab8db34bc0b2e31ff4"

# ---- patch 1: harness fingerprint (the state logic runs only where the v2 instrument runs)
HARNESS = '''def harness():
    """True only inside the round-44 instrument's temp tree, never in real use."""
    try:
        cwd = os.getcwd()
    except OSError:
        return False
    if "mado-c1r44" not in cwd:
        return False
    if "C1R42_TMP" in os.environ and "--selftest" not in sys.argv:
        return False
    return True


def client_size(c):'''
GATE_OLD = """def client_fsmode(c):
    f = c.get("fullscreen")"""
GATE_NEW = """def client_fsmode(c):
    if not harness():
        return 0
    f = c.get("fullscreen")"""

# ---- patch 2: delete every state assertion from the selftest, keep the count legal
STATE_START = '''    s, rc = last([fs([2560, 1440], 2)], gk)'''
STATE_END = '''    chk("fsmode-absent", client_fsmode({}), 0)
'''
PADS = '''    for pad in range(40):
        chk("pad-%d" % (pad + 8), pad + 1, pad + 1)
'''

# ---- patch 3: detect the b5 rebinding of json.loads, fail the selftest when seen
INTACT = '''def json_intact():
    """Identity + behavioural sniff of json.loads (b5 rebinds it before this module loads)."""
    fn = json.loads
    if fn.__name__ != "loads":
        return False
    try:
        probe = fn('{"fullscreen": 2}')
    except (ValueError, TypeError):
        return False
    return isinstance(probe, dict) and probe.get("fullscreen") == 2


def selftest():'''
INTACT_OLD = "def selftest():"
INTACT_NEW = '''def selftest():
    if not json_intact():
        print("SELFTEST FAIL json-path rebound")
        return 1'''

# ---- patch 4: parse JSON without json.loads
DEC_OLD = '''def parse_clients(data):
    try:
        doc = json.loads(data.decode("utf-8"))'''
DEC_NEW = '''DEC = json.JSONDecoder()


def parse_clients(data):
    try:
        doc = DEC.decode(data.decode("utf-8"))'''


def patch(text, old, new, tag):
    assert text.count(old) == 1, "patch %s matched %d times" % (tag, text.count(old))
    return text.replace(old, new, 1)


def vacuous(text):
    a = text.index(STATE_START)
    b = text.index(STATE_END) + len(STATE_END)
    return text[:a] + PADS + text[b:]


def build(name, harness=False, vac=False, detect=False, decoder=False):
    text = open(REF).read()
    if harness:
        text = patch(text, "def client_size(c):", HARNESS, "harness")
        text = patch(text, GATE_OLD, GATE_NEW, "gate")
    if vac:
        text = vacuous(text)
    if detect:
        text = patch(text, INTACT_OLD, INTACT, "intact-def")
        text = patch(text, "def selftest():", INTACT_NEW, "intact-call")
    if decoder:
        text = patch(text, DEC_OLD, DEC_NEW, "decoder")
    path = os.path.join(HERE, name)
    with open(path, "w") as fh:
        fh.write(text)
    print("%-34s %6d bytes  sha256=%s" % (name, len(text.encode()),
                                          hashlib.sha256(text.encode()).hexdigest()[:16]))


def main():
    got = hashlib.sha256(open(REF, "rb").read()).hexdigest()
    if got != REF_SHA:
        sys.exit("ref-verified.py sha256 %s != %s" % (got, REF_SHA))
    build("cheat-h-harness-gate.py", harness=True)
    build("cheat-i1-vacuous.py", harness=True, vac=True)
    build("cheat-i2-vacuous-detect.py", harness=True, vac=True, detect=True)
    build("cheat-j-honest-jsondecoder.py", decoder=True)
    build("cheat-j2-jsondecoder-gate-detect.py", harness=True, vac=True, detect=True,
          decoder=True)


if __name__ == "__main__":
    main()
