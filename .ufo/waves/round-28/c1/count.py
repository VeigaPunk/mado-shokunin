#!/usr/bin/env python3
"""mado round 28 C1 composite counter: the routed round-27 gate blind spots close.

The six legs are the C1-m27 claim. Each leg runs on committed bytes at REV only.

Leg h1-rotation: the frozen round-27 C2 counter on the round-27 sealed held-out set H1
must print TARGET_MET and kill the three named held-c1v2 survivors.
Leg h2-rotate: the same frozen counter on the rotated sealed set H2 (round-28) must print
TARGET_MET under its own frozen rule.
Leg refpub-kills: the same frozen counter on the public reference set (round-28) must kill
every valid row (h_killed == h_valid), ≥9 valid, ≥2 per subject.
Leg a1-predicates: the committed suite bytes contain the eight A1 probe names and do not
contain the softened `got < total` form for the one/two-missing/extra checks.
Leg q36-witness: the committed Q36-successor runner exits 0 and the receipts file names both
surviving case mutants.
Leg q37-open-ended: the extended population checker exits 0 on the round-27 C2 receipt and
the round-26 frozen artifact sha256 is unchanged.

Exit: 0 all legs pass; 1 any leg fails; 2 setup/usage error.
"""
import argparse
import hashlib
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
LANE = os.path.abspath(os.path.join(HERE, "..", "..", "..", ".."))
R27C2 = os.path.join(LANE, ".ufo/waves/round-27/c2/count-v2.py")
SUITE = os.path.join(LANE, "quality/counter-selftest.py")
H1_HELDOUT = "/fast/scratch/hyaku/mado-r27/heldout"
H1_SEAL = os.path.join(LANE, ".ufo/waves/round-27/c2/heldout-seal.txt")
H2_HELDOUT = "/fast/scratch/hyaku/mado-r28/heldout2"
H2_SEAL = os.path.join(LANE, ".ufo/waves/round-28/c2/heldout2-seal.txt")
REF_HELDOUT = "/fast/scratch/hyaku/mado-r28/refpub"
REF_SEAL = os.path.join(LANE, ".ufo/waves/round-28/c1/refpub-seal.txt")

Q36_RUNNER = os.path.join(LANE, ".ufo/waves/round-28/quality/q36-successor-run.sh")
Q36_RECEIPTS = os.path.join(LANE, "quality/q36-successor-receipts.txt")
Q37_CHECKER = os.path.join(LANE, "quality/check-population.py")
Q37_R26_ARTIFACT = ".ufo/waves/round-26/quality/check-population.py"
Q37_R26_SHA = "803e0096c994d301fa7fe9a9dd7e35255ee1f5bcf3f63d15956cdba8943d0f64"

R27_REG = ".ufo/waves/round-27/registration.md"
R27_RECEIPT = ".ufo/waves/round-27/evidence/c2-after-0b53bd86.txt"

A1_PROBES = ("c2-drift-extra", "c2-drift-missing", "c2-one-missing", "c2-one-extra",
             "c2-two-missing", "c2-two-extra", "c2-embed-at-min", "c2-embed-below-min")
# A1's strict form for the one/two missing/extra checks; A2's softened form uses got < total.
STRICT_PRED = ("rc == 1 and verdict == \"TARGET_MISSED\" and got == 0 and total == 51")
SOFTENED_PRED = ("got is not None and got < total")

HELD_C1V2_SURVIVORS = ("held-c1v2-node-subset", "held-c1v2-missing-version-guard",
                        "held-c1v2-extra-output-segment")


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
        raise SystemExit("SETUP_ERROR blob %s:%s missing" % (rev[:12], path))
    return p.stdout.encode()


def run(argv):
    p = subprocess.run(argv, capture_output=True, text=True)
    return p.returncode, p.stdout, p.stderr


def run_counter(rev, heldout, seal):
    return run([sys.executable, "-I", R27C2, rev, "--heldout", heldout, "--seal", seal])


def leg(ok, name, detail):
    print("LEG %-14s %s | %s" % (name, "PASS" if ok else "FAIL", detail))
    return bool(ok)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("rev")
    a = ap.parse_args()
    p = git("rev-parse", "--verify", a.rev + "^{commit}")
    if p.returncode != 0:
        raise SystemExit("SETUP_ERROR bad REV %s" % a.rev)
    rev = p.stdout.strip()
    print("counter c1-r28 sha256:%s rev=%s" % (sha(open(__file__, "rb").read()), rev))
    ok = True

    # --- leg h1-rotation -----------------------------------------------------
    rc, out, err = run_counter(rev, H1_HELDOUT, H1_SEAL)
    met = re.search(r"verdict=(TARGET_MET|TARGET_MISSED)", out)
    h1_ok = rc == 0 and met and met.group(1) == "TARGET_MET" and all(
        re.search(r"CASE H\s+H/HeldC1v2:%s\s+suite=A rc=1 KILLED" % re.escape(s), out)
        for s in HELD_C1V2_SURVIVORS)
    ok &= leg(h1_ok, "h1-rotation",
              "rc=%d %s" % (rc, met.group(1) if met else "no-verdict"))

    # --- leg h2-rotate ------------------------------------------------------
    rc, out, err = run_counter(rev, H2_HELDOUT, H2_SEAL)
    met = re.search(r"verdict=(TARGET_MET|TARGET_MISSED)", out)
    h2_ok = rc == 0 and met and met.group(1) == "TARGET_MET"
    ok &= leg(h2_ok, "h2-rotate",
              "rc=%d %s" % (rc, met.group(1) if met else "no-verdict"))

    # --- leg refpub-kills ----------------------------------------------------
    rc, out, err = run_counter(rev, REF_HELDOUT, REF_SEAL)
    m = re.search(r"h_killed=(\d+)/(\d+) h_need=\d+ h_valid=(\d+) h_min_per_subject=(\d+)", out)
    ref_ok = False
    if m:
        killed, total, valid, minper = map(int, m.groups())
        ref_ok = (rc == 0 and killed == total and valid >= 9 and minper >= 2)
    ok &= leg(ref_ok, "refpub-kills",
              "rc=%d %s" % (rc, m.group(0) if m else "no-h-tally"))

    # --- leg a1-predicates ---------------------------------------------------
    suite = blob(rev, "quality/counter-selftest.py").decode()
    a1_ok = all(p in suite for p in A1_PROBES) and STRICT_PRED in suite \
        and SOFTENED_PRED not in suite
    ok &= leg(a1_ok, "a1-predicates",
              "probes=%d/%d strict=%s softened=%s" % (
                  sum(p in suite for p in A1_PROBES), len(A1_PROBES),
                  STRICT_PRED in suite, SOFTENED_PRED in suite))

    # --- leg q36-witness -----------------------------------------------------
    rc, out, err = run(["bash", Q36_RUNNER])
    receipts = blob(rev, "quality/q36-successor-receipts.txt").decode()
    q36_ok = rc == 0 and "Q2-glob-case-sensitive" in receipts and "Q5-marker-case-insensitive" in receipts
    ok &= leg(q36_ok, "q36-witness", "rc=%d names=%s" % (
        rc, "Q2-glob-case-sensitive" in receipts and "Q5-marker-case-insensitive" in receipts))

    # --- leg q37-open-ended --------------------------------------------------
    rc, out, err = run([sys.executable, "-I", Q37_CHECKER, "--registration",
                         os.path.join(LANE, R27_REG), os.path.join(LANE, R27_RECEIPT)])
    q37_ok = rc == 0 and "verdict=PASS" in out
    r26_sha = sha(blob(rev, Q37_R26_ARTIFACT))
    q37_ok &= r26_sha == Q37_R26_SHA
    ok &= leg(q37_ok, "q37-open-ended", "rc=%d r26sha=%s" % (rc, r26_sha[:12]))

    print("PRED-C1-r28 verdict=%s" % ("TARGET_MET" if ok else "TARGET_MISSED"))
    print("exit=%d" % (0 if ok else 1))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
