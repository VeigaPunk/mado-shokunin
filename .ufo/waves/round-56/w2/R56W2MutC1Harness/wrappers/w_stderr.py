#!/usr/bin/env python3
"""Wrapper oracle: runs the REAL counter, then forges one property of its output (mode=stderr)."""
import re
import subprocess
import sys

REAL = '/fast/scratch/hyaku/mado-r56/R56W2MutC1Harness/real/c1-r56-autoreload-entry.py'
MODE = 'stderr'


def main():
    p = subprocess.run([sys.executable, "-I", REAL] + sys.argv[1:], capture_output=True)
    out = p.stdout.decode("utf-8", "replace")
    err = p.stderr.decode("utf-8", "replace")
    rc = p.returncode
    lines = [l for l in out.split("\n") if l.strip()]
    line = lines[0] if lines else ""
    if MODE == "rev":
        line = re.sub(r"rev=\S+", "rev=" + "0" * 40, line)
    elif MODE == "rc0":
        rc = 0
    elif MODE == "rc2":
        rc = 2 if "verdict=TARGET_MISSED" in line else rc
    elif MODE == "dup":
        lines = [line, line]
    elif MODE == "stderr":
        err = err + "warning: forged diagnostic\n"
    elif MODE == "content":
        line = re.sub(r"content=\d+/33", "content=33/33", line)
    elif MODE == "verdictword":
        line = line.replace("verdict=TARGET_MISSED", "verdict=TARGET_MAYBE")
    elif MODE == "denom":
        line = re.sub(r"rows=(\d+)/30", r"rows=\1/31", line)
    elif MODE == "goodonly":
        if "verdict=TARGET_MET missed=none" in line:
            line = re.sub(r"content=\d+/33", "content=32/33", line)
    if MODE == "dup":
        sys.stdout.write("\n".join(lines) + "\n")
    else:
        sys.stdout.write(line + ("\n" if line else ""))
    sys.stderr.write(err)
    return rc


if __name__ == "__main__":
    sys.exit(main())
