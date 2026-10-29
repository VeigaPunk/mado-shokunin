#!/usr/bin/env python3
"""Stub C1 counter: MODE=GREENMISSED (generated; not a lane artifact)."""
import os
import sys

MODE = 'GREENMISSED'
LEGS = ''

FULL = "rows=30/30 hosts=3/3 sources=30/30 scope=30/30 content=33/33 new_rows=8/8"


def parse(argv):
    out = {}
    i = 0
    while i < len(argv):
        a = argv[i]
        if a.startswith("--") and i + 1 < len(argv):
            out[a] = argv[i + 1]
            i += 2
        else:
            i += 1
    return out


def main():
    args = parse(sys.argv[1:])
    rev = args.get("--rev", "0")
    repo = args.get("--repo", ".")
    counts = FULL
    verdict = "TARGET_MET"
    missed = "none"
    rc = 0
    if MODE == "GREEN":
        pass
    elif MODE == "REJECT":
        counts = "rows=0/30 hosts=0/3 sources=0/30 scope=0/30 content=0/33 new_rows=0/8"
        verdict = "TARGET_MISSED"
        missed = "index"
        rc = 1
    elif MODE == "KITCHEN":
        verdict = "TARGET_MET"
        missed = LEGS
        rc = 1
    elif MODE == "LEGS":
        counts = "rows=0/30 hosts=0/3 sources=0/30 scope=0/30 content=0/33 new_rows=0/8"
        verdict = "TARGET_MISSED"
        missed = LEGS
        rc = 1
    elif MODE == "GREENBADREV":
        rev = "0" * 40
    elif MODE == "GREENBADCOUNT":
        counts = "rows=30/30 hosts=3/3 sources=30/30 scope=30/30 content=32/33 new_rows=8/8"
    elif MODE == "GREENMISSED":
        missed = "prov"
    elif MODE == "NEWROWS390":
        counts = "rows=0/30 hosts=0/3 sources=0/30 scope=0/30 content=0/33 new_rows=0/8"
        verdict = "TARGET_MISSED"
        rc = 1
        path = os.path.join(repo, "corpus", "SOURCES.md")
        try:
            data = open(path, "rb").read().decode("utf-8", "replace")
        except OSError:
            data = ""
        missing = not any(l.lstrip().startswith("| S390 ") for l in data.split("\n"))
        missed = "new_rows" if missing else "prov"
    else:
        sys.stderr.write("unknown stub mode\n")
        return 2
    print("MADO_AUTORELOAD_ENTRY: rev=%s %s verdict=%s missed=%s" % (rev, counts, verdict, missed))
    return rc


if __name__ == "__main__":
    sys.exit(main())
