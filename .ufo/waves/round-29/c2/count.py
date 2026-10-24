#!/usr/bin/env python3
"""mado round 29 C2 counter: the four round-28-closure routed defects repaired in records.

PRED-C2-r29 (frozen; identical sentence in registration, this counter and receipts):
  At REV, this counter exits 0 and prints `CHECK R1..R4 PASS` and
  `PRED-C2-r29 verdict=TARGET_MET`.

Checks (each over committed bytes at REV):
  R1 — guard-pin repair recorded: .ufo/waves/round-29/c1/count.py pins the frozen
       count-v4.py at 635ae788... (and no longer at 3d7d301f...), and the red-before
       control receipt controls/C1K1-r28composite.txt shows the unrepaired composite's
       `normal=missing mutant=missing` + `PRED-C1-r28 verdict=TARGET_MISSED`.
  R2 — ephemeral-input policy adopted at data time: this registration names the committed
       receipt basis (ReviewerSuiteMonotone.md), QUALITY 39, and the owner.
  R3 — standalone boolword-v5 receipts committed: evidence/v5-standalone-normal.txt
       carries cases_pass=41/41 boolword_pass=2/2 verdict=TARGET_MET and
       evidence/v5-standalone-mutant.txt carries boolword_pass=0/2 verdict=TARGET_MISSED.
  R4 — the §6.6 tenth record defect repaired: SCORECARD.md carries the append-only
       `§6.6 erratum (round 29)` block naming the corrected citation location.

Usage: python3 -I c2/count.py REV
Exit: 0 TARGET_MET, 1 TARGET_MISSED, 2 setup/usage error.
"""
import argparse
import hashlib
import subprocess
import sys

V4_PIN = "635ae788fd897c8f1fba88e4ab2ffcb95e7f79a88703b82e49a8729ce7d271a1"
V4_OLD = "3d7d301fb9315f9a6cea2427db7c39e556482b30d3f4283373579ae665afd136"
C1 = ".ufo/waves/round-29/c1/count.py"
K1 = ".ufo/waves/round-29/controls/C1K1-r28composite.txt"
REG = ".ufo/waves/round-29/registration.md"
NORMAL = ".ufo/waves/round-29/evidence/v5-standalone-normal.txt"
MUTANT = ".ufo/waves/round-29/evidence/v5-standalone-mutant.txt"
SCORECARD = "SCORECARD.md"


def git(*args):
    env = dict(__import__("os").environ, GIT_OPTIONAL_LOCKS="0")
    return subprocess.run(["git"] + list(args), capture_output=True, text=True, env=env)


def blob(rev, path):
    p = git("show", "%s:%s" % (rev, path))
    return p.stdout if p.returncode == 0 else None


def check(ok, name, detail):
    print("CHECK %-3s %s | %s" % (name, "PASS" if ok else "FAIL", detail))
    return bool(ok)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("rev")
    a = ap.parse_args()
    p = git("rev-parse", "--verify", a.rev + "^{commit}")
    if p.returncode != 0:
        print("SETUP_ERROR bad REV %s" % a.rev)
        print("exit=2")
        return 2
    rev = p.stdout.strip()

    ok = True

    # R1 — guard-pin repair recorded, with the red-before control receipt.
    c1 = blob(rev, C1)
    k1 = blob(rev, K1)
    pin_ok = c1 is not None and V4_PIN in c1 and V4_OLD not in c1
    red_ok = k1 is not None and "normal=missing mutant=missing" in k1 \
        and "PRED-C1-r28 verdict=TARGET_MISSED" in k1
    ok &= check(pin_ok and red_ok, "R1",
                "pin-635ae788=%s old-pin-absent=%s red-before=%s"
                % (pin_ok, c1 is not None and V4_OLD not in c1, red_ok))

    # R2 — ephemeral-input preservation policy recorded at data time.
    reg = blob(rev, REG) or ""
    r2 = ("ReviewerSuiteMonotone.md" in reg and "QUALITY 39" in reg
          and "owner" in reg)
    ok &= check(r2, "R2", "registration-names-receipt-basis-and-owner=%s" % r2)

    # R3 — standalone boolword-v5 receipts committed.
    normal = blob(rev, NORMAL)
    mutant = blob(rev, MUTANT)
    n_ok = normal is not None and "cases_pass=41/41" in normal \
        and "boolword_pass=2/2" in normal and "verdict=TARGET_MET" in normal
    m_ok = mutant is not None and "boolword_pass=0/2" in mutant \
        and "verdict=TARGET_MISSED" in mutant
    ok &= check(n_ok and m_ok, "R3", "normal-41/41=%s mutant-0/2=%s" % (n_ok, m_ok))

    # R4 — §6.6 tenth record defect repaired in SCORECARD.md.
    sc = blob(rev, SCORECARD) or ""
    r4 = "§6.6 erratum (round 29)" in sc
    ok &= check(r4, "R4", "scorecard-erratum-block=%s" % r4)

    print("PRED-C2-r29 verdict=%s" % ("TARGET_MET" if ok else "TARGET_MISSED"))
    print("exit=%d" % (0 if ok else 1))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
