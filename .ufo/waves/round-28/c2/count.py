#!/usr/bin/env python3
"""mado round 28 C2 counter: the nine round-27 closure record defects, measured on committed bytes.

Each defect is a predicate over committed bytes at REV. A defect is resolved when its check
passes. The counter prints one CHECK line per defect and the final PRED line.

D1  SKILL.md gate registry: no row under the round-27 gates table still says "pending".
D2  Lesson M27-2: `corpus/lessons/round-27.md` carries an erratum block that names the
     superseded evidence pointer and whose corrected pointer target (a SOURCES.md row) exists
     at REV.
D3 E01 red-before: committed malformed two-cell S178–S182 fixture is rejected by the frozen census
     validator with five E01 rows; a clone of REV's corrected SOURCES.md validates cleanly.
     The receipt pins the fixture sha and the validator sha.
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
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
LANE = os.path.abspath(os.path.join(HERE, "..", "..", "..", ".."))

REVREPAIR_SHA = "2ee4116645657382176134617c02e73ae96b43296747babece8de61d41d8577f"
A1REPORT_SHA = "94d656ce41972e1764387921fb5cc825f900dcfaa49425e0e32f94b85201d4a4"
M27_2_CORRECTED_POINTER = "S178"
W3_RECON = ".ufo/waves/round-28/evidence/w3-seats-reconciliation.txt"
E01_RED_BEFORE = ".ufo/waves/round-28/evidence/e01-red-before.txt"
QR36_RECEIPTS = "quality/q36-successor-receipts.txt"
ROUND27_REG = ".ufo/waves/round-27/registration.md"
LESSON27 = "corpus/lessons/round-27.md"
SCORECARD = "SCORECARD.md"
LOG = "LOG.md"
SKILL = "SKILL.md"
E01_FIXTURE = ".ufo/waves/round-28/evidence/e01-red-before/SOURCES.md"
CENSUS_SHA = "3fb7261569f46423dd80ecc23e0a23789a7926f667c7a3fc559d2439d4a64e30"
CENSUS = "/home/vgpnk/Projects/shokunin/scripts/sources-census.sh"


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

    # D1: inspect only the three r27 registry rows, not historical text elsewhere in SKILL.
    skill = text(rev, SKILL) or ""
    rows = [ln for ln in skill.splitlines() if ln.startswith("| mado-r27-")]
    names = {ln.split("|", 2)[1].strip() for ln in rows}
    expected = {"mado-r27-counter-selftest", "mado-r27-population-suite", "mado-r27-control-receipts"}
    d1 = names == expected and len(rows) == 3 and all(
        "pending" not in ln.lower() and "provisional" not in ln.lower() for ln in rows)
    ok &= check("D1", d1, "rows=%d names=%s pending=%s" % (
        len(rows), ",".join(sorted(names)), any("pending" in ln.lower() for ln in rows)))

    # D2: the appended lesson erratum supersedes the malformed row pointer and links actual rows.
    les = text(rev, LESSON27) or ""
    sources = text(rev, "corpus/SOURCES.md") or ""
    d2 = ("Round-27 erratum (round 28)" in les
          and "corpus/SOURCES.md:195-199" in les
          and all("| S%d |" % n in sources for n in range(178, 183)))
    ok &= check("D2", d2, "erratum=%s rows=%d/5" % (
        "Round-27 erratum (round 28)" in les,
        sum("| S%d |" % n in sources for n in range(178, 183))))

    # D3: run the frozen census validator on a committed malformed-row fixture (red)
    # and on an isolated checkout of REV's real registry (green).
    red = blob(rev, E01_RED_BEFORE)
    fixture = blob(rev, E01_FIXTURE)
    census_bytes = open(CENSUS, "rb").read()
    d3 = (red is not None and fixture is not None and sha(census_bytes) == CENSUS_SHA
          and ("fixture_sha256=" + sha(fixture)) in red.decode(errors="replace"))
    if d3:
        with tempfile.TemporaryDirectory(prefix="mado-r28-e01-") as td:
            fixture_root = os.path.join(td, "fixture")
            srcpath = os.path.join(fixture_root, "corpus", "SOURCES.md")
            os.makedirs(os.path.dirname(srcpath))
            with open(srcpath, "wb") as stream:
                stream.write(fixture)
            p_red = subprocess.run([CENSUS, "validate", "--file", srcpath, "--today", "2026-10-23"],
                                   capture_output=True, text=True)
            e01_lines = [line for line in p_red.stdout.splitlines() if "\tE01\t" in line]
            clone = os.path.join(td, "lane")
            p_clone = subprocess.run(["git", "clone", "--quiet", "--no-hardlinks", LANE, clone],
                                     capture_output=True, text=True)
            p_checkout = subprocess.run(["git", "-C", clone, "checkout", "--quiet", "--detach", rev],
                                        capture_output=True, text=True) if p_clone.returncode == 0 else None
            if p_checkout is not None and p_checkout.returncode == 0:
                p_green = subprocess.run([CENSUS, "validate", clone, "--today", "2026-10-23"],
                                         capture_output=True, text=True)
                d3 = (p_red.returncode == 1 and len(e01_lines) == 5
                      and p_green.returncode == 0 and "E01" not in p_green.stdout
                      and "exit=1" in red.decode(errors="replace"))
            else:
                d3 = False
    ok &= check("D3", d3, "red-fixture=%s census-sha=%s red/green=%s" % (
        fixture is not None, sha(census_bytes)[:12], d3))

    # D4 q36-successor receipts dead pointer.
    rec = text(rev, QR36_RECEIPTS) or ""
    d4 = "Q2-glob-case-sensitive" in rec and "Q5-marker-case-insensitive" in rec
    ok &= check("D4", d4, "names=%s" % d4)

    # D5: exact r27 harm-watch omission and its append-only correction.
    sc = text(rev, SCORECARD) or ""
    d5 = ("round-27 harm-watch erratum" in sc
          and "tools/mado-binds.py" in sc and "docstring" in sc)
    ok &= check("D5", d5, "erratum=%s binds-docstring=%s" % (
        "round-27 harm-watch erratum" in sc, "tools/mado-binds.py" in sc and "docstring" in sc))

    # D6: registration records both measured C2 attempts and the repair path.
    reg = text(rev, ROUND27_REG) or ""
    d6 = ("round-27 measurement erratum" in reg and "measurement 1" in reg
          and "measurement 2" in reg and "repair flow" in reg)
    ok &= check("D6", d6, "both-measurements=%s repair-flow=%s" % (
        "measurement 1" in reg and "measurement 2" in reg, "repair flow" in reg))

    # D7: reconcile counts without inventing the unreported identity.
    w3 = text(rev, W3_RECON) or ""
    d7 = ("declared=8" in w3 and "reports=7" in w3 and "unreported=1" in w3
          and "identity=unknown" in w3)
    ok &= check("D7", d7, "8 declared / 7 reports / 1 unknown=%s" % d7)

    # D8: identify both the superseded range and the actual round-27 source range.
    log = text(rev, LOG) or ""
    d8 = ("round-27 SKILL citation erratum" in log and "631-636" in log and "630-635" in log)
    ok &= check("D8", d8, "superseded=631-636 corrected=630-635 present=%s" % d8)

    # D9 both w4 erratum reports committed with pinned hashes.
    rr = blob(rev, ".ufo/waves/round-27/w4/reports/RevRepair.md")
    a1 = blob(rev, ".ufo/waves/round-27/w4/reports/ExecRepairA1.md")
    d9 = rr is not None and a1 is not None
    if d9:
        d9 = sha(rr) == REVREPAIR_SHA and sha(a1) == A1REPORT_SHA
    ok &= check("D9", d9, "revrepair=%s a1=%s" % (rr is not None, a1 is not None))

    print("PRED-C2-r28 verdict=%s" % ("TARGET_MET" if ok else "TARGET_MISSED"))
    print("exit=%d" % (0 if ok else 1))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
