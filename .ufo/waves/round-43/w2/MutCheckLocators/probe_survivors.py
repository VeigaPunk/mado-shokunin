#!/usr/bin/env python3
"""Distinguishing-input probe for the surviving mutants.

For every SURVIVED row in matrix.tsv, runs pristine and the mutant on a small
prose input chosen to expose the removed behaviour (or records the
equivalence/latency proof when no input can distinguish them). Fetch fixtures
are the checker's own selftest fixtures (REC/PLAIN imported from pristine.py),
written to a private temp dir.
"""

import importlib.util
import os
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from mutrun import BASE, MUTANTS, apply_once  # noqa: E402

spec = importlib.util.spec_from_file_location("pristine", os.path.join(HERE, "pristine.py"))
pristine = importlib.util.module_from_spec(spec)
spec.loader.exec_module(pristine)  # main() is import-guarded
REC, PLAIN = pristine.REC, pristine.PLAIN

# survivor -> (prose lines, note); fixture fetch = rec.cpp (REC) + plain.conf (PLAIN)
PROBES = {
    "range-slice-offbyone": (["`epsilon` at `rec.cpp:9`"],
        "last receipt line (9 = int epsilon = 9;) is never citable in the mutant"),
    "token-len-4": (["`foo` at `rec.cpp:2`"],
        "3-char token foo absent from line 2: pristine MISS, mutant NOFRAG"),
    "token-lower-boundary": (["`lpha` at `rec.cpp:2`"],
        "lpha occurs only inside alpha: pristine MISS, mutant OK"),
    "attr-before-inclusive": (["`alpha`rec.cpp:2"],
        "fragment ends exactly at locator start: pristine OK, mutant NOFRAG"),
    "attr-after-exclusive": (["rec.cpp:2`alpha`"],
        "fragment starts exactly at locator end: pristine OK, mutant NOFRAG"),
    "id-re-digit-lead": (["value `123` at `plain.conf:2`"],
        "digit-leading token 123: pristine NOFRAG (no tokens), mutant MISS"),
    "locator-no-lookbehind": (["-rec.cpp:2"],
        "preceding '-' blocks a start at 'r' in pristine (name cannot start with '-'): "
        "pristine locators=0, mutant matches rec.cpp:2 mid-word"),
    "locator-no-lookahead": (["`alpha` at rec.cpp:2x"],
        "range bleeds into x: pristine locators=0, mutant checks rec.cpp:2"),
    "summary-swapped": (["`beta` at `rec.cpp:2`", "`alpha` at `rec.cpp:5`"],
        "two locators one miss: pristine locators=2 miss=1, mutant locators=1 miss=2"),
}

LATENT = {
    "teeth-one-direction":
        "equivalent on every current input: the flipped run of the frozen 18-case table always "
        "breaks both ways (measured constants flips=11 ok_to_miss=4 miss_to_ok=5, all > 0), so the "
        "removed ok_to_miss/miss_to_ok clauses are tautologies today; latent missing assertion - a "
        "future table whose flip is one-directional would now pass selftest",
    "selftest-min-cases-dropped":
        "equivalent on every current input: the frozen CASES table has k=18 >= 12, so the removed "
        "k >= 12 clause is a tautology today; latent missing assertion - a future table shorter than "
        "12 cases would now pass selftest",
    "no-re-escape":
        "equivalent by construction: fragment_tokens only returns ID_RE matches, i.e. strings over "
        "[A-Za-z0-9_], and re.escape is the identity on exactly that set (verified by enumeration in "
        "this probe), so the mutated regex string equals the original for every reachable token",
}


def run(path, fetch, prose):
    p = subprocess.run([sys.executable, path, "--fetch", fetch, prose],
                       capture_output=True, text=True, timeout=60)
    return "rc=%d\n%s%s" % (p.returncode, p.stdout, p.stderr)


def main():
    root = tempfile.mkdtemp(prefix="mutprobe.")
    fetch = os.path.join(root, "fetch")
    os.makedirs(fetch)
    with open(os.path.join(fetch, "rec.cpp"), "w") as fh:
        fh.write("\n".join(REC) + "\n")
    with open(os.path.join(fetch, "plain.conf"), "w") as fh:
        fh.write("\n".join(PLAIN) + "\n")
    ppath = os.path.join(root, "pristine.py")
    with open(ppath, "w") as fh:
        fh.write(BASE)

    surv = []
    with open(os.path.join(HERE, "matrix.tsv")) as fh:
        next(fh)
        for line in fh:
            name, _cat, _s, _c, verdict, _h = line.rstrip("\n").split("\t")
            if verdict == "SURVIVED":
                surv.append(name)

    lines = ["# survivor distinguishing-input evidence", ""]
    for name in surv:
        src = apply_once(name, dict((m[0], (m[2], m[3])) for m in MUTANTS)[name][0],
                         dict((m[0], (m[2], m[3])) for m in MUTANTS)[name][1])
        mpath = os.path.join(root, "m_%s.py" % name)
        with open(mpath, "w") as fh:
            fh.write(src)
        lines.append("## %s" % name)
        if name in PROBES:
            prose_lines, note = PROBES[name]
            prose = os.path.join(root, "prose-%s.md" % name)
            with open(prose, "w") as fh:
                fh.write("\n".join(prose_lines) + "\n")
            lines.append("input: %r" % prose_lines)
            lines.append("expectation: %s" % note)
            lines.append("```")
            lines.append("--- pristine ---")
            lines.append(run(ppath, fetch, prose).rstrip("\n"))
            lines.append("--- mutant %s ---" % name)
            lines.append(run(mpath, fetch, prose).rstrip("\n"))
            lines.append("```")
        elif name in LATENT:
            lines.append("no distinguishing input exists today; classification: %s" % LATENT[name])
        else:
            lines.append("NO PROBE DEFINED (harness survivor without a probe entry)")
        os.remove(mpath)
        lines.append("")

    # mechanical proof for no-re-escape: re.escape identity on word-char strings
    import itertools
    import re as _re
    alpha = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_"
    bad = [s for n in (1, 2, 3) for s in map("".join, itertools.product(alpha, repeat=n))
           if _re.escape(s) != s]
    lines.append("## no-re-escape mechanical check")
    lines.append("re.escape != identity on %d of %d word-char strings of length 1-3"
                 % (len(bad), len(alpha) * (len(alpha) ** 2 + len(alpha) + 1)))

    print("\n".join(lines))


if __name__ == "__main__":
    main()
