#!/usr/bin/env python3
"""verify-quotes.py - every quote criteria.md lifts is <= 25 words, located, and present at its
location in the committed bytes (or the lane file for round-41 paths).

Run from the lane root: python3 .ufo/waves/round-41/w1/ScrQualityCriteria/verify-quotes.py
Exit 0 = every quote verified; 1 = a quote is absent, over 25 words, or the locator is wrong.
"""
import re
import subprocess
import sys

REV = "fb49621"  # round-40 tip: the bytes the routed defects are recorded in

# (quote, path, first line, last line, rev) - the locator is the line range in the named file.
# The spot-check landed at cd950ec (round-41 dispatch); the lesson was already at fb49621.
SPOTCHECK_REV = "cd950ec"
QUOTES = [
    ("MADO_AXIS checked=3 mismatched=0 at fb49621",
     "corpus/lessons/round-40-verifier-spotcheck.md", 19, 19, SPOTCHECK_REV),
    ("one untracked `.ufo/waves/round-40/w1.ready.dispatched` (dispatch marker, no round work)",
     "corpus/lessons/round-40-verifier-spotcheck.md", 15, 15, SPOTCHECK_REV),
    ("`ConnCrossClaim` returned `report: .ufo/waves/round-49/w1/ConnCrossClaim.md`",
     "corpus/lessons/round-40.md", 135, 135, REV),
    ("the reply cap (the mutant kept a post-check -> the control now removes both)",
     "corpus/lessons/round-40.md", 88, 89, REV),
]

# byte locators: the exact text that must sit on the named lines
LOCATORS = [
    (".ufo/waves/round-40/receipts/ctl-c1-v2.txt", 46,
     "control=M38-reply-cap-dropped"),
    (".ufo/waves/round-40/ctl/run-c1-v2-controls.py", 163,
     "M43 (float64 instead of float32 alpha) is an equivalent mutant"),
    (".ufo/waves/round-40/ctl/run-c2-v2-controls.py", 247,
     "X15 (CRLF receipt) is an equivalent mutant under v2"),
    ("tools/mado-options.py", 942, "raw = proc.stdout.read(REPLY_CAP + 1)"),
    ("tools/mado-options.py", 943, "too_long = len(raw) > REPLY_CAP"),
]


def show(path, rev):
    r = subprocess.run(["git", "show", "%s:%s" % (rev, path)],
                       capture_output=True, text=True)
    return None if r.returncode else r.stdout.splitlines()


def norm(text):
    return re.sub(r"\s+", " ", text).strip()


def main():
    bad = 0
    for quote, path, first, last, rev in QUOTES:
        lines = show(path, rev)
        if lines is None:
            print("UNREADABLE %s at %s" % (path, rev))
            bad += 1
            continue
        span = norm("\n".join(lines[first - 1:last]))
        words = len(quote.split())
        here = norm(quote) in span
        flag = "ok" if here and words <= 25 else "BAD"
        print("%s words=%d %s:%d-%d@%s %r" % (flag, words, path, first, last, rev, quote))
        if not here or words > 25:
            bad += 1
            print("    span read: %r" % span[:200])
    for path, line, text in LOCATORS:
        lines = show(path, REV)
        if lines is None or text not in lines[line - 1]:
            print("BAD locator %s:%d %r" % (path, line, text))
            bad += 1
        else:
            print("ok locator %s:%d %r" % (path, line, text))
    print("VERDICT: %s (%d defect(s))" % ("PASS" if not bad else "FAIL", bad))
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
