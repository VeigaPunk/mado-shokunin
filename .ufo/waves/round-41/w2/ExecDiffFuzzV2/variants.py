#!/usr/bin/env python3
"""Harness-teeth probe: build four known-wrong one-sentence variants of the
delivered tool and re-run the quick systematic corpus against each. If the
sweep is sensitive, each variant shows >0 disagreements; if it were vacuous,
all would show 0 like the reference."""
import os
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import fuzz as F  # noqa: E402

SRC = F.TOOL_SRC.decode("utf-8")
OUT = os.path.join(F.SEAT, "variants")
os.makedirs(OUT, exist_ok=True)


def build(name, subs, allow_many=False):
    src = SRC
    for old, new in subs:
        n = src.count(old)
        if n < 1 or (n != 1 and not allow_many):
            raise SystemExit("%s: %d occurrences of %r" % (name, n, old))
        src = src.replace(old, new)
    path = os.path.join(OUT, name + ".py")
    with open(path, "w") as fh:
        fh.write(src)
    return path


VARIANTS = {
    "ascii-digits": ([("[0-9]", "\\d")], True),
    "str-max": ([("max(ent[1], ver)",
                   "ver if str(ver) > str(ent[1]) else ent[1]")], False),
    "int-pid": ([("cur[\"pid\"] != pid",
                   "int(cur[\"pid\"]) != int(pid)")], False),
    "splitlines": ([("for line in text.split(\"\\n\")",
                     "for line in text.splitlines()")], False),
}


def main():
    for name, (subs, many) in VARIANTS.items():
        path = build(name, subs, many)
        print("built", name, path)
        p = subprocess.run([F.PY, "-I", os.path.join(F.SEAT, "fuzz.py"),
                            "--quick", "--jobs", "4", "--tool", path],
                           capture_output=True, text=True, timeout=1800)
        print(p.stdout)
        if p.returncode != 0:
            print("STDERR:", p.stderr[-2000:])
    return 0


if __name__ == "__main__":
    sys.exit(main())
