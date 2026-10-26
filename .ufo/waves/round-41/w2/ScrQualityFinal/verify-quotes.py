#!/usr/bin/env python3
"""Verify every quote in criteria.md against committed bytes at 07f264.

Read-only: `git -C LANE show <rev>:<path>`. Normalizes backticks/asterisks
and whitespace runs before matching; enforces <= 25 words.
"""
import re
import subprocess
import sys

LANE = "/home/vgpnk/Projects/shokunin/mado-shokunin"
REV = "07f2641696b5ac73de1404ea737a9f27e9819aa1"

QUOTES = [
    # (quote, path, expected-line-ish note)
    ("MADO_AXIS checked=3 mismatched=0 at fb49621",
     "corpus/lessons/round-40-verifier-spotcheck.md", ":19"),
    ("one untracked `.ufo/waves/round-40/w1.ready.dispatched` (dispatch marker, no round work)",
     "corpus/lessons/round-40-verifier-spotcheck.md", ":15"),
    ("`ConnCrossClaim` returned `report: .ufo/waves/round-49/w1/ConnCrossClaim.md`",
     "corpus/lessons/round-40.md", ":135"),
    ("the reply cap (the mutant kept a post-check",
     "corpus/lessons/round-40.md", ":88"),
    ("read_live never executes the program: it reads the stub's own bytes",
     ".ufo/waves/round-41/w1/CritC1Cheat.md", ":75-76"),
    ("the payload is base64 inside a readable `0755` script",
     ".ufo/waves/round-41/w1/CritC1Cheat.md", ":89"),
    ("even when the fixture is live",
     ".ufo/waves/round-41/w1/CritC1Cheat.md", ":107"),
    ("A compiled execute-only program: the tool under test cannot read it",
     "quality/counters/c1-r41-globals-v2.py", ":551"),
    ("no copy of the journal on disk",
     "quality/counters/c1-r41-globals-v2.py", ":571"),
    ("The reference selftest is replaced by a four-line check of where the tool is running",
     ".ufo/waves/round-41/w1/CritC1Cheat.md", ":168"),
    ("`--selftest` computes a rolling hash of its own file",
     ".ufo/waves/round-41/w1/CritC1Cheat.md", ":184"),
    ("the exclusion is by *name substring*, so the code that matters can be renamed out of the sample",
     ".ufo/waves/round-41/w1/CritC1Cheat.md", ":221"),
    ("accepted_versions=[1..9], max_version_digits=1",
     ".ufo/waves/round-41/w1/ExecDiffFuzz.md", ":106"),
    ("so `[1952]` and `[01952]` are two sessions",
     ".ufo/waves/round-41/w1/ExecDiffFuzz.md", ":113"),
    ("in Python `\\d` is Unicode-aware",
     ".ufo/waves/round-41/w1/ExecDiffFuzz.md", ":119"),
    ("Five of six `-o` values, plus `--no-hostname` on the accepted format, leave a file with 78 adverts",
     ".ufo/waves/round-41/w1/ExecJournalFormat.md", ":40-41"),
    ("byte-for-byte the observable of a genuinely empty journal",
     ".ufo/waves/round-41/w1/ExecJournalFormat.md", ":42-43"),
    ("an input whose every advert is ignored is UNRECOGNIZED_FORMAT (exit 4), never a silent NO_SESSIONS",
     "tools/mado-globals.py", ":15-16"),
    ("The grammar is `journalctl -o short-iso` only",
     "tools/mado-globals.py", ":13"),
]


def norm(s):
    s = s.replace("`", "").replace("*", "")
    return re.sub(r"\s+", " ", s).strip()


def fetch(path):
    p = subprocess.run(["git", "-C", LANE, "show", "%s:%s" % (REV, path)],
                       capture_output=True, text=True)
    if p.returncode != 0:
        raise SystemExit("cannot read %s: %s" % (path, p.stderr[:200]))
    return norm(p.stdout)


def main():
    cache = {}
    bad = 0
    for q, path, loc in QUOTES:
        nq = norm(q)
        words = len(nq.split())
        if words > 25:
            print("FAIL %s (%d words > 25): %r" % (path + loc, words, q))
            bad += 1
            continue
        text = cache.get(path) or fetch(path)
        cache[path] = text
        if nq in text:
            print("OK %s (%d words)" % (path + loc, words))
        else:
            print("FAIL quote not found in %s%s: %r" % (path, loc, q))
            bad += 1
    print("QUOTES: n=%d all_ok=%d" % (len(QUOTES), bad == 0))
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
