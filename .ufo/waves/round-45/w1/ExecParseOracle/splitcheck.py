#!/usr/bin/env python3
"""Ground the model's CVarList2 transcription in the pinned C++ source itself.

Builds pins/varlist_driver.cpp against hyprutils v0.14.2 src/string/VarList2.cpp and
src/string/String.cpp (the lane's frozen fetch/hyprutils-String.cpp), feeds the same random strings to
both, and reports mismatches. Build tree lives in /fast/scratch/hyaku/mado-r45/ExecParseOracle/build.

Usage: python3 splitcheck.py [--n 4000]
"""
import argparse
import json
import os
import random
import shutil
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
LANE = os.path.abspath(os.path.join(HERE, "..", "..", "..", "..", ".."))
BUILD = "/fast/scratch/hyaku/mado-r45/ExecParseOracle/build"
PINS = os.path.join(HERE, "pins")
FETCH = os.path.join(LANE, ".ufo", "waves", "round-45", "fetch")

sys.path.insert(0, HERE)
import model as M  # noqa: E402


def build():
    inc = os.path.join(BUILD, "include", "hyprutils", "string")
    os.makedirs(inc, exist_ok=True)
    shutil.copy(os.path.join(PINS, "include_hyprutils_string_VarList2.hpp"),
                os.path.join(inc, "VarList2.hpp"))
    shutil.copy(os.path.join(PINS, "include_hyprutils_string_String.hpp"),
                os.path.join(inc, "String.hpp"))
    shutil.copy(os.path.join(PINS, "src_string_VarList2.cpp"), os.path.join(BUILD, "VarList2.cpp"))
    shutil.copy(os.path.join(FETCH, "hyprutils-String.cpp"), os.path.join(BUILD, "String.cpp"))
    shutil.copy(os.path.join(PINS, "varlist_driver.cpp"), os.path.join(BUILD, "varlist_driver.cpp"))
    cmd = ["g++", "-std=c++2b", "-O1", "-Iinclude", "-o", "varlist_driver", "varlist_driver.cpp",
           "VarList2.cpp", "String.cpp"]
    subprocess.run(cmd, cwd=BUILD, check=True)
    return os.path.join(BUILD, "varlist_driver"), cmd


ALPHABET = [",", "\\", " ", "\t", "\r", "\v", "\f", "a", "1", "x", "D", ".", "-", "="]
WORDS = ["DP-1", "1920x1080", "@100", "0x0", "1.25", "mirror", "desc:Dell", "auto", "00",
         "transform", ", 3", "\\,", " eDP-1 "]


def gen(n, rng):
    out = set()
    while len(out) < n:
        if rng.random() < 0.5:
            k = rng.randint(0, 22)
            out.add("".join(rng.choice(ALPHABET) for _ in range(k)))
        else:
            out.add(", ".join(rng.choice(WORDS) for _ in range(rng.randint(0, 4))))
    return sorted(out)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--n", type=int, default=4000)
    ap.add_argument("--seed", type=int, default=45)
    args = ap.parse_args()
    driver, cmd = build()
    rng = random.Random(args.seed)
    cases = gen(args.n, rng)
    payload = "\n".join(c.replace("\n", " ") for c in cases) + "\n"
    res = subprocess.run([driver], input=payload.encode(), capture_output=True, check=True)
    got = {}
    for raw in res.stdout.split(b"\n"):
        if b"\t" not in raw:
            continue
        idx, _, body = raw.partition(b"\t")
        try:
            got[int(idx)] = json.loads(body.decode("utf-8", errors="replace"))
        except ValueError:
            got[int(idx)] = None
    bad = []
    ub = []
    compared = 0
    for k, src in enumerate(cases):
        want = got.get(k)
        mine = M.varlist2(src)
        if src.count("\\") >= 2:
            # Pinned-source hazard, not a model question: m_args holds string_views into m_copyStrings,
            # and a second escaped field reallocates that vector, so earlier views dangle (UB). Measured
            # separately; see receipts/varlist-ub.txt.
            ub.append((src, want, mine))
            continue
        compared += 1
        if want != mine:
            bad.append((src, want, mine))
    out = ["# CVarList2 differential: pinned C++ vs model.varlist2",
           "build: " + " ".join(cmd) + "   (cwd %s)" % BUILD,
           "cases=%d compared=%d mismatches=%d  excluded(>=2 escapes, upstream view invalidation)=%d"
           % (len(cases), compared, len(bad), len(ub))]
    for src, want, mine in bad[:20]:
        out.append("MISMATCH %r cpp=%r model=%r" % (src, want, mine))
    with open(os.path.join(HERE, "receipts", "varlist-ub.txt"), "w", encoding="utf-8") as fh:
        fh.write("# cases where the pinned splitter's own views dangle (>=2 escaped fields)\n")
        fh.write("cases=%d\n" % len(ub))
        for src, want, mine in ub[:12]:
            fh.write("cpp=%r model=%r\n" % (want, mine))
    text = "\n".join(out) + "\n"
    with open(os.path.join(HERE, "receipts", "splitcheck.txt"), "w", encoding="utf-8") as fh:
        fh.write(text)
    sys.stdout.write(text)


if __name__ == "__main__":
    main()
