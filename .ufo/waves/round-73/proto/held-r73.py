#!/usr/bin/env python3
"""Round-73 pre-freeze do-nothing control (proto; not a scored counter).

    python3 -I .ufo/waves/round-73/proto/held-r73.py --repo . \
        --base-rev d3f6c9f5d8b3401c01f189e8cd4b8dbc917a2bce --scratch-root DIR

C1 leg: apply the four named rule mutations to the held round-72 harness bytes and score each
one on (a) the round-73 ten-case outcome set and (b) the held round-72 eight-case set. The
do-nothing control is the held eight-case denominator: it must kill only two of the four.
C2 leg: score the held round-71 classifier on the round-73 twenty-eight-case guard set; it must
miss exactly the three new positive shapes.
"""
import argparse
import json
import os
import subprocess
import sys

BASE = None
REPO = None


def git(*args):
    return subprocess.check_output(["git", "-C", REPO, *args], text=True)


def show(path):
    return git("show", "%s:%s" % (BASE, path))


def sha(blob):
    import hashlib
    return hashlib.sha256(blob.encode()).hexdigest()


MUTANTS = [
    ("N1-zero-guard-dropped",
     "    return total > 0 and passed == total\n",
     "    return passed == total\n"),
    ("N2-last-prefix-match",
     "        if re.fullmatch(r\"MADO_LANDING_COUNTERS_SELFTEST: [0-9]+/[0-9]+ assertions passed\",\n                        line.strip()):\n            return line.strip()\n",
     "        if line.startswith(\"MADO_LANDING_COUNTERS_SELFTEST:\"):\n            return line.strip()\n"),
    ("N3-pass-le-total",
     "    return total > 0 and passed == total\n",
     "    return total > 0 and passed <= total\n"),
    ("N4-kill-count-only",
     "    return \"TARGET_MET\" if summary_green(selftest_out) and killed == 2 else \"TARGET_MISSED\"\n",
     "    return \"TARGET_MET\" if killed == 2 else \"TARGET_MISSED\"\n"),
]


def load_harness(src, name):
    ns = {"__name__": name}
    exec(compile(src, name, "exec"), ns)
    return ns


def score(cases, verdict_fn):
    good = 0
    misses = []
    for case in cases:
        got = verdict_fn(case["gate_out"], case["killed"])
        ok = got == case["expected"]
        good += 1 if ok else 0
        if not ok:
            misses.append(case["id"])
    return good, misses


def main(argv=None):
    global BASE, REPO
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo", required=True)
    ap.add_argument("--base-rev", required=True)
    ap.add_argument("--scratch-root", required=True)
    args = ap.parse_args(argv)
    REPO = args.repo
    BASE = args.base_rev
    os.makedirs(args.scratch_root, exist_ok=True)
    harness_path = "quality/counters/c1-r72-landing-controls.py"
    src = show(harness_path)
    ns = load_harness(src, "held_r72")
    new = json.load(open(".ufo/waves/round-73/controls/c1-outcomes-r73.json"))["cases"]
    held = json.load(open(".ufo/waves/round-72/controls/c2-controls-r72.json"))["cases"]
    print("PROTO_R73_C1 harness=%s sha=%s base=%s" % (harness_path, sha(src), BASE))
    print("PROTO_R73_C1 pristine held_rule: new_set=%d/%d held_set=%d/%d"
          % (score(new, ns["outcome_verdict"])[0], len(new),
             score(held, ns["outcome_verdict"])[0], len(held)))
    killed_new = killed_held = 0
    for name, old, rep in MUTANTS:
        if src.count(old) != 1:
            print("PROTO_R73_C1 mutant=%s APPLY_FAIL count=%d" % (name, src.count(old)))
            continue
        mutated = src.replace(old, rep)
        mns = load_harness(mutated, name)
        gnew, mnew = score(new, mns["outcome_verdict"])
        gheld, mheld = score(held, mns["outcome_verdict"])
        kn = gnew < len(new)
        kh = gheld < len(held)
        killed_new += 1 if kn else 0
        killed_held += 1 if kh else 0
        print("PROTO_R73_C1 mutant=%s new=%d/%d killed=%s misses=%s | held=%d/%d killed=%s misses=%s"
              % (name, gnew, len(new), "yes" if kn else "NO", ",".join(mnew) or "-",
                 gheld, len(held), "yes" if kh else "NO", ",".join(mheld) or "-"))
    print("PROTO_R73_C1 killed: new_set=%d/4 held_set=%d/4" % (killed_new, killed_held))

    guard_src = show("quality/counters/c2-r71-shapes.py")
    gns = load_harness(guard_src, "held_r71")
    cases = json.load(open(".ufo/waves/round-73/controls/c2-cases-r73.json"))["cases"]
    good = 0
    misses = []
    for case in cases:
        reader, guard = gns["classify"](case["src"])
        ok = reader == case["expect_reader"] and guard == case["expect_guard"]
        good += 1 if ok else 0
        if not ok:
            misses.append("%s(reader=%s guard=%s)" % (case["name"], reader, guard))
    print("PROTO_R73_C2 held_r71 sha=%s controls=%d/%d misses=%s"
          % (sha(guard_src), good, len(cases), " ".join(misses) or "-"))
    return 0


if __name__ == "__main__":
    sys.exit(main())
