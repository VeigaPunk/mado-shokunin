#!/usr/bin/env python3
"""Source-only W blocklist; never execute or import either subject.

Patterns are frozen from round-27/c2/mutants-w.json, SHA-256
0ad0e46c1a6e61f369c30ab08d6a998f6dce7d16436087b5df57fb8f22323608.
A nonempty `new` matches by literal byte containment, even inside `old`.
"""
import argparse
from pathlib import Path


PATTERNS = {
    "c1": (
        ("c1-drop-bezier", b"ok = gn == en and gb == eb", b"ok = gn == en"),
        (
            "c1-accept-nonjson",
            b'verdict[lab] = (False, err or "output is not [nodes, beziers]")',
            b'verdict[lab] = (True, err or "output is not [nodes, beziers]")',
        ),
        ("c1-pass-90pct", b"met = npass == len(built)", b"met = npass * 10 >= 9 * len(built)"),
        (
            "c1-skip-base-guard",
            b"if node_set(b1) != node_set(b2) or bez_set(b1) != bez_set(b2):",
            b"if False:",
        ),
    ),
    "c2": (
        (
            "c2-accept-nonjson",
            b'verdict[lab] = (False, err or "stdout is not a JSON array of objects", len(exp))',
            b'verdict[lab] = (True, err or "stdout is not a JSON array of objects", len(exp))',
        ),
        (
            "c2-pass-90pct",
            b"met = npass == len(built) and embed_hits == 0",
            b"met = npass * 10 >= 9 * len(built) and embed_hits == 0",
        ),
        ("c2-skip-base-guard", b"        if n1 or n2:", b"        if False:"),
        ("c2-embed-min-1000", b"EMBED_MIN = 12", b"EMBED_MIN = 1000"),
        (
            "c2-drop-arg",
            b"nm, ne, missing, extra = V3.compare(got, exp)",
            b"nm, ne, missing, extra = V3.compare([dict(e, arg=None) for e in got], [dict(e, arg=None) for e in exp])",
        ),
    ),
}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--c1", required=True)
    parser.add_argument("--c2", required=True)
    parser.add_argument("--rev", required=True)
    args = parser.parse_args()
    for subject, patterns in PATTERNS.items():
        source = Path(getattr(args, subject)).read_bytes()
        for mutant_id, old, new in patterns:
            if (new in source) if new else (old not in source):
                print("W-BLOCKLIST reject %s %s" % (subject, mutant_id))
                return 1
    print("W-BLOCKLIST accept")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
