#!/usr/bin/env python3
"""RerunControlsV2 quote check: every quotation in RerunControlsV2.md that is lifted from a lane source must appear
(whitespace-normalised) inside the cited line range, and be at most 25 words. Locators were computed with grep -n;
this script re-checks them against the files, not against the report's own text."""
import re

LANE = "/home/vgpnk/Projects/shokunin/mado-shokunin/"
CASES = [
    ("LOG.md", 2502, 2502, "controls 0 of 20 met"),
    (".ufo/waves/round-44/registration-v2.md", 30, 30,
     "the lattice share varies with the nonce, the verdict does not"),
    (".ufo/waves/round-44/registration-v2.md", 34, 37, "CTL_C1v2 VERDICT: PASS (controls scoring"),
    (".ufo/waves/round-44/registration-v2.md", 35, 36, "X1 sandbox gate = cheat E ported"),
    (".ufo/waves/round-44/registration-v2.md", 35, 36, "caught by **e** only"),
    (".ufo/waves/round-44/registration-v2.md", 35, 36, "caught by **b5** only"),
    (".ufo/waves/round-44/registration-v2.md", 59, 62, "positive control P"),
    (".ufo/waves/round-44/registration-v2.md", 59, 62, "CTL_C2v2 VERDICT: PASS (wrong=0 of 11; positive"),
    ("corpus/lessons/round-44.md", 167, 167, "0 of 20 met"),
    ("quality/counters/c1-r44-geometry-states-v2.py", 209, 209, 'rng = old.rng_for(rev, nonce, "sgen", i)'),
    ("quality/counters/c1-r44-geometry-states-v2.py", 243, 243, 'rng = old.rng_for(rev, nonce, "fsmany", 0)'),
    ("quality/counters/c1-r42-geometry.py", 336, 336, "def rng_for(rev, nonce, tag, i)"),
    (".ufo/waves/round-44/ctl/run-c1-controls-v2.py", 48, 48,
     'counter = os.path.join(a.repo, "quality", "counters", "c1-r44-geometry-states-v2.py")'),
    (".ufo/waves/round-44/ctl/run-c2-controls-v2.py", 74, 74,
     'counter = os.path.join(a.repo, "quality", "counters", "c2-r44-gkeep-size-request-v2.py")'),
    (".ufo/waves/round-44/receipts/ctl-c1-v2.txt", 23, 23,
     "CTL_C1v2 VERDICT: PASS (controls scoring TARGET_MET: 0 of 20; reference met: 1)"),
    (".ufo/waves/round-44/receipts/ctl-c2-v2.txt", 13, 13,
     "CTL_C2v2 VERDICT: PASS (wrong=0 of 11; positive admitted=1)"),
]

norm = lambda s: re.sub(r"\s+", " ", s).strip()
bad = 0
for path, lo, hi, quote in CASES:
    lines = open(LANE + path, encoding="utf-8").read().splitlines()
    window = norm(" ".join(lines[lo - 1:hi]))
    found = norm(quote) in window
    words = len(norm(quote).split())
    ok = found and words <= 25
    bad += not ok
    print("%-4s %-58s %5d-%-5d words=%2d %s" % ("OK" if ok else "FAIL", path, lo, hi, words,
          "found" if found else "NOT FOUND: " + repr(norm(quote))))
print("QUOTE-CHECK: %s (%d cases, %d failures)" % ("PASS" if not bad else "FAIL", len(CASES), bad))
raise SystemExit(0 if not bad else 1)
