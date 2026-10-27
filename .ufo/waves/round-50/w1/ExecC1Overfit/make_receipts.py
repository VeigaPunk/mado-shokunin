#!/usr/bin/env python3
"""Assemble the citable receipts for the clause-g probe runs.

Reads the frozen counter's own stdout per run (kept in scratch while it exists), keeps the clause
lines, the clause=f FAIL count + first three FAIL lines, every clause=g FAIL line, and the final
verdict line; rewrites scratch clone paths to <scratch-clone>. A scratch path is never citable, so
only this copy goes into the seat dir.

Usage: make_receipts.py <run-dir> <seat-receipts-dir> <pairs...>   pairs are variant:nonce
"""
import os
import re
import sys

SCRATCH = re.compile(r"/fast/scratch/[^ ]*")
KEEP = re.compile(r"clause=(meta|t|j|i)")
CLONE = "<scratch-clone>"


def main(argv):
    rundir, outdir = argv[1], argv[2]
    pairs = argv[3:]
    os.makedirs(outdir, exist_ok=True)
    for pair in pairs:
        variant, nonce = pair.split(":")
        src = os.path.join(rundir, "%s-%s.txt" % (variant, nonce))
        lines = open(src, encoding="utf-8", errors="replace").read().splitlines()
        f_fail = [ln for ln in lines if re.search(r"clause=f fixture=.* FAIL", ln)]
        g_fail = [ln for ln in lines if re.search(r"clause=g case=.* FAIL", ln)]
        out = ["# run: %s-%s.txt" % (variant, nonce),
               "# command: python3 -I quality/counters/c1-r49-keysym.py --repo <clone> --rev HEAD"
               " --work <scratch> --nonce %s" % nonce,
               "# receipt assembled from the counter's own stdout (run in scratch, copied here)"]
        for ln in lines:
            if KEEP.search(ln) or ln.startswith("PRED-C1-r49 clause=s ") \
                    or re.search(r"clause=f fixtures", ln) or re.search(r"clause=g generated", ln) \
                    or re.search(r"clause=r ", ln) or ln.startswith("PRED-C1-r49: "):
                out.append(SCRATCH.sub(CLONE, ln))
        pos = len(out)
        out.insert(pos, "# clause=f FAIL count: %d" % len(f_fail))
        out[pos:pos] = [SCRATCH.sub(CLONE, ln) for ln in f_fail[:3]]
        out.append("# clause=g FAIL count: %d" % len(g_fail))
        out.extend(SCRATCH.sub(CLONE, ln) for ln in g_fail)
        path = os.path.join(outdir, "r50-c1-%s-nonce%s.txt" % (variant, nonce))
        with open(path, "w", encoding="utf-8") as fh:
            fh.write("\n".join(out) + "\n")
        print("%s lines=%d" % (path, len(out)))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
