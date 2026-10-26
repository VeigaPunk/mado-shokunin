#!/usr/bin/env python3
"""CritC1V2Cheat: verify every quote used in the report against its cited line.

Each entry is (relative path in the lane, 1-based line, exact substring). The script prints the
verbatim source line for every quote, so Report quotes are machine-checked, never typed.
"""
import os
import sys

LANE = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                    "..", "..", "..", "..", ".."))
SEAT = os.path.dirname(os.path.abspath(__file__))
Q = [
    ("quality/counters/c1-r44-geometry-states-v2.py", 34,
     "b5  state-blind teeth: a copy of the tool whose first lines rebind `json.loads`"),
    ("quality/counters/c1-r44-geometry-states-v2.py", 53,
     "parses JSON without json.loads, or detects the rebinding, defeats it"),
    ("quality/counters/c1-r44-geometry-states-v2.py", 37,
     "environment invariance: the inputs of the fixed fixtures fs0, max0, fsmix0, fsclient0 and fsagree0"),
    ("quality/counters/c1-r44-geometry-states-v2.py", 387,
     'argv = ["--clients", cpath, "--rules", rpath]'),
    ("quality/counters/c1-r44-geometry-states-v2.py", 391,
     'p = subprocess.run([os.path.realpath(sys.executable), "-I", tool] + argv, cwd=d, env=env,'),
    ("quality/counters/c1-r44-geometry-states-v2.py", 427,
     'tmp = tempfile.mkdtemp(prefix="mado-c1r44-", dir=parent)'),
    ("quality/counters/c1-r44-geometry-states-v2.py", 337, 'env["C1R42_TMP"] = tmp'),
    ("quality/counters/c1-r44-geometry-states-v2.py", 304,
     'and "fullscreen" in c.value.lower() for c in ast.walk(fn))'),
    ("quality/counters/c1-r42-geometry.py", 115,
     'ENV = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}'),
    ("quality/counters/c1-r42-geometry.py", 442, "env=ENV, input=stdin)"),
    (".ufo/waves/round-44/registration-v2.md", 25,
     "state-blind teeth: a copy whose `json.loads` renames the `fullscreen` key"),
    (".ufo/waves/round-44/registration-v2.md", 39,
     "b5 binds the `json.loads` path only; e compares one second environment"),
    ("/usr/lib/python3.14/json/__init__.py", 298, "return loads(fp.read(),"),
    ("/usr/lib/python3.14/json/__init__.py", 352, "return _default_decoder.decode(s)"),
    ("__seat__/cheat-h-harness-gate.py", 198, 'if "mado-c1r44" not in cwd:'),
    ("__seat__/cheat-h-harness-gate.py", 200,
     'if "C1R42_TMP" in os.environ and "--selftest" not in sys.argv:'),
    ("__seat__/cheat-h-harness-gate.py", 214, "if not harness():"),
    ("__seat__/cheat-i2-vacuous-detect.py", 320, 'if fn.__name__ != "loads":'),
    ("__seat__/cheat-i2-vacuous-detect.py", 323, "probe = fn('{\"fullscreen\": 2}')"),
    ("__seat__/cheat-j-honest-jsondecoder.py", 187, 'doc = DEC.decode(data.decode("utf-8"))'),
]


def main():
    bad = 0
    for rel, line, needle in Q:
        path = os.path.join(SEAT, rel[9:]) if rel.startswith("__seat__/") else os.path.join(LANE, rel)
        try:
            text = open(path, encoding="utf-8").read().split("\n")
        except OSError as exc:
            print("MISSING %s: %s" % (rel, exc))
            bad += 1
            continue
        got = text[line - 1] if 0 < line <= len(text) else ""
        ok = needle in got
        bad += not ok
        print("%s %s:%d  %r" % ("ok  " if ok else "FAIL", rel, line, got.strip()[:140]))
    print("QUOTES verified=%d failed=%d" % (len(Q) - bad, bad))
    return 0 if not bad else 1


if __name__ == "__main__":
    sys.exit(main())
