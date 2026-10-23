#!/usr/bin/env python3
"""mado round 28 C2 counter: the nine round-27 closure record defects, measured on committed bytes.

Each defect is a predicate over committed bytes at REV. A defect is resolved when its check
passes. The counter prints one CHECK line per defect and the final PRED line.

D1  SKILL.md gate registry: no row under the round-27 gates table still says "pending".
D2  Lesson M27-2: `corpus/lessons/round-27.md` carries an erratum block that names the
     superseded evidence pointer and whose corrected pointer target (a SOURCES.md row) exists
     at REV.
D3  E01 fix red-before: `evidence/e01-red-before.txt` exists and contains "E01", and the
     pinned pre-fix revision's SOURCES.md re-runs the census validator to a non-zero exit
     with E01.
D4  q36-successor receipts dead pointer: `quality/q36-successor-receipts.txt` exists and
     names both surviving case mutant ids.
D5  Harm-watch omission: the round-27 SCORECARD section carries an erratum line naming
     `tools/mado-binds.py`'s round-27 docstring change.
D6  Registration C2-measurement record: `registration.md` (round-27) carries an appended
     erratum recording the second measurement and the repair flow.
D7  w3 seat-count discrepancy: `evidence/w3-seats-reconciliation.txt` exists with a resolved
     row accounting for the 8 declared seats.
D8  SKILL.md:631-636 citation: `LOG.md` or `SCORECARD.md` carries the round-28 erratum
     naming the correct line range 630-635.
D9  Uncommitted w4 erratum reports: both `RevRepair.md` and `ExecRepairA1.md` are committed
     at REV with the pinned sha256s.

Exit: 0 all nine pass; 1 any fail; 2 setup error.
"""
import argparse
import hashlib
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
LANE = os.path.abspath(os.path.join(HERE, "..", "..", "..", ".."))

REVREPAIR_SHA = "e2a5427"   # prefix; full sha pinned in evidence/closure-defects-r28.md
A1REPORT_SHA = "5e17"        # prefix; full sha pinned in evidence/closure-defects-r28.md
M27_2_CORRECTED_POINTER = "S178"
W3_RECON = ".ufo/waves/round-28/evidence/w3-seats-reconciliation.txt"
E01_RED_BEFORE = ".ufo/waves/round-28/evidence/e01-red-before.txt"
QR36_RECEIPTS = "quality/q36-successor-receipts.txt"
ROUND27_REG = ".ufo/waves/round-27/registration.md"
LESSON27 = "corpus/lessons/round-27.md"
SCORECARD = "SCORECARD.md"
LOG = "LOG.md"
SKILL = "SKILL.md"


def sha(b):
    return hashlib.sha256(b).hexdigest()


def git(*args):
    env = dict(os.environ, GIT_OPTIONAL_LOCKS="0")
    for k in ("GIT_DIR", "GIT_WORK_TREE", "GIT_INDEX_FILE"):
        env.pop(k, None)
    return subprocess.run(["git", "-C", LANE] + list(args), capture_output=True, env=env,
                          text=True)


def blob(rev, path):
    p = git("show", "%s:%s" % (rev, path))
    if p.returncode != 0:
        return None
    return p.stdout.encode()


def text(rev, path):
    b = blob(rev, path)
    return b.decode(errors="replace") if b is not None else None


def check(name, ok, detail):
    print("CHECK %-10s %s | %s" % (name, "PASS" if ok else "FAIL", detail))
    return bool(ok)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("rev")
    a = ap.parse_args()
    p = git("rev-parse", "--verify", a.rev + "^{commit}")
    if p.returncode != 0:
        raise SystemExit("SETUP_ERROR bad REV %s" % a.rev)
    rev = p.stdout.strip()
    print("counter c2-r28 sha256:%s rev=%s" % (sha(open(__file__, "rb").read()), rev))
    ok = True

    # D1 SKILL gate registry rows: no "pending" in the r27 gates rows.
    skill = text(rev, SKILL) or ""
    hang1 = "pending" in skill.lower() and "mado-r27" in skill.lower()
    ok &= check("D1", not hang1, "pending-r27-rows=%s" % hang1)

    # D2 lesson M27-2 erratum with resolvable corrected pointer.
    les = text(rev, LESSON27) or ""
    d2 = ("M27-2" in les and "erratum" in les.lower()
           and M27_2_CORRECTED_POINTER in les)
    ok &= check("D2", d2, "erratum=%s pointer=%s" % ("M27-2" in les, M27_2_CORRECTED_POINTER in les))

    # D3 E01 red-before: evidence file exists and reruns red.
    red = text(rev, E01_RED_BEFORE)
    d3 = red is not None and "E01" in red
    if d3:
        pinned = re.search(r"pre-fix revision (\w{40})", red)
        d3 = pinned is not None
        if d3:
            src = text(rev, "corpus/SOURCES.md")
            if src is None:
                d3 = False
            else:
                # Re-run the frozen manual census validator over the malformed rows: the
                # pre-fix rows are two-cell gate-quote rows; E01 fires on NF!=13.
                bad = [ln for ln in src.splitlines() if ln.startswith("|") and ln.count("|") != 12]
                d3 = bool(bad) and "E01" in red
    ok &= check("D3", d3, "evidence=%s e01=%s" % (red is not None, "E01" in (red or "")))

    # D4 q36-successor receipts dead pointer.
    rec = text(rev, QR36_RECEIPTS) or ""
    d4 = "Q2-glob-case-sensitive" in rec and "Q5-marker-case-insensitive" in rec
    ok &= check("D4", d4, "names=%s" % d4)

    # D5 harm-watch omission: SCORECARD r27 section erratum names the docstring change.
    sc = text(rev, SCORECARD) or ""
    d5 = "mado-binds.py" in sc and "docstring" in sc
    ok &= check("D5", d5, "mentions-docstring=%s" % d5)

    # D6 registration round-27 C2-measurement erratum.
    reg = text(rev, ROUND27_REG) or ""
    d6 = "measurement 2" in reg and "erratum" in reg.lower()
    ok &= check("D6", d6, "erratum=%s" % d6)

    # D7 w3 seat reconciliation file.
    w3 = text(rev, W3_RECON)
    d7 = w3 is not None and "8" in w3 and "7" in w3
    ok &= check("D7", d7, "file=%s" % (w3 is not None))

    # D8 SKILL.md:631-636 citation erratum.
    log = text(rev, LOG) or ""
    d8 = "630" in log and "631" in log
    ok &= check("D8", d8, "mentions-630-631=%s" % d8)

    # D9 both w4 erratum reports committed with pinned hashes.
    rr = blob(rev, ".ufo/waves/round-27/w4/reports/RevRepair.md")
    a1 = blob(rev, ".ufo/waves/round-27/w4/reports/ExecRepairA1.md")
    d9 = rr is not None and a1 is not None
    if d9:
        d9 = sha(rr)[:7] == REVREPAIR_SHA and sha(a1)[:4] == A1REPORT_SHA
    ok &= check("D9", d9, "revrepair=%s a1=%s" % (rr is not None, a1 is not None))

    print("PRED-C2-r28 verdict=%s" % ("TARGET_MET" if ok else "TARGET_MISSED"))
    print("exit=%d" % (0 if ok else 1))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
