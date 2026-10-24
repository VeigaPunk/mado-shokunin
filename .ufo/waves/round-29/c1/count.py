#!/usr/bin/env python3
"""mado round 29 C1 composite counter: the round-28 composite repaired (routed defects 1-2).

Identical six-leg shape to the frozen round-28 composite (.ufo/waves/round-28/c1/count.py,
which is never edited), with exactly two rule changes declared in the round-29 registration
before data:

* leg h1-rotation -> h1-receipt: the ephemeral H1 directory was cleaned before the round-28
  closure (M28-2), so per QUALITY 39 this leg verifies from the committed w2 receipt
  .ufo/waves/round-28/w2/reports/ReviewerSuiteMonotone.md (named verification basis, owner
  mado, recorded at data time in the round-29 registration). The receipt names the new-suite
  run h_killed=18/18 verdict=TARGET_MET, the monotone verdict, and the three held-c1v2
  survivors rc=1 KILLED.
* leg boolword-v5: the guard pin for the frozen round-27 count-v4.py bytes is corrected from
  the never-matching 3d7d301f... (M28-1) to the committed 635ae788...; the leg now prints
  real tallies instead of normal=missing mutant=missing.

Legs h2-rotate, refpub-kills, q36-witness and q37-open-ended restate the round-28 leg rules
verbatim. Smoke-run once at freeze per QUALITY 38; full output committed. The suites are the
committed bytes of REV: the frozen round-27 counter clones REV and runs
`quality/counter-selftest.py` / `quality/population-suite.py` from the clone.

Exit: 0 all legs pass; 1 any leg fails; 2 setup/usage error.
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
R27C2 = os.path.join(LANE, ".ufo/waves/round-27/c2/count-v2.py")
SUITE = os.path.join(LANE, "quality/counter-selftest.py")
H1_HELDOUT = "/fast/scratch/hyaku/mado-r27/heldout"
H1_SEAL = os.path.join(LANE, ".ufo/waves/round-27/c2/heldout-seal.txt")
H2_HELDOUT = os.path.join(LANE, ".ufo/waves/round-28/c2/heldout2")
H2_SEAL_REL = ".ufo/waves/round-28/c2/heldout2-seal.txt"
H2_SEAL = os.path.join(LANE, H2_SEAL_REL)
REF_HELDOUT = os.path.join(LANE, ".ufo/waves/round-28/c1/refpub")
REF_SEAL_REL = ".ufo/waves/round-28/c1/refpub-seal.txt"
REF_SEAL = os.path.join(LANE, REF_SEAL_REL)
R28C1V5 = ".ufo/waves/round-28/c1/count-v5.py"
EXACTBOOL_TOOL = ".ufo/waves/round-28/c1/ref-mutants/exactbool-tool.py"
V5_SEED = "28c1a8c0ffee0001"
V5_HOME_REL = ".ufo/waves/round-28/c1/synthetic-home"
V5_HOME_CONFIG_REL = V5_HOME_REL + "/.config/hypr/hyprland.conf"

Q36_RUNNER_REL = "quality/q36-successor-run.sh"
Q36_RECEIPTS = "quality/q36-successor-receipts.txt"
Q37_CHECKER_REL = "quality/check-population.py"
Q37_R26_ARTIFACT = ".ufo/waves/round-26/quality/check-population.py"
Q37_R26_SHA = "803e0096c994d301fa7fe9a9dd7e35255ee1f5bcf3f63d15956cdba8943d0f64"

R27_REG = ".ufo/waves/round-27/registration.md"
R27_RECEIPT = ".ufo/waves/round-27/evidence/c2-after-0b53bd86.txt"

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
    """Committed bytes of PATH at REV, or None: a missing artifact fails its leg, not setup."""
    p = git("show", "%s:%s" % (rev, path))
    return p.stdout.encode() if p.returncode == 0 else None


def seal_bytes(path):
    try:
        with open(path, "rb") as stream:
            return stream.read()
    except OSError:
        return None


def run(argv):
    p = subprocess.run(argv, capture_output=True, text=True)
    return p.returncode, p.stdout, p.stderr


def run_counter(rev, heldout, seal):
    return run([sys.executable, "-I", R27C2, rev, "--heldout", heldout, "--seal", seal])

def run_v5(rev, tool_mutant=None):
    script_path = os.path.join(LANE, R28C1V5)
    committed = blob(rev, R28C1V5)
    if committed is None:
        return 2, "SETUP_ERROR count-v5.py missing at REV"
    if not os.path.isfile(script_path) or sha(open(script_path, "rb").read()) != sha(committed):
        return 2, "SETUP_ERROR count-v5 bytes do not match REV"
    v4 = blob(rev, ".ufo/waves/round-27/c1/count-v4.py")
    if v4 is None or sha(v4) != "635ae788fd897c8f1fba88e4ab2ffcb95e7f79a88703b82e49a8729ce7d271a1":
        return 2, "SETUP_ERROR frozen count-v4 bytes changed"
    home_config = blob(rev, V5_HOME_CONFIG_REL)
    home_config_path = os.path.join(LANE, V5_HOME_CONFIG_REL)
    if home_config is None or not os.path.isfile(home_config_path) or sha(open(home_config_path, "rb").read()) != sha(home_config):
        return 2, "SETUP_ERROR synthetic HOME bytes do not match REV"
    with tempfile.TemporaryDirectory(prefix="mado-r28-boolword-") as td:
        args = [sys.executable, "-I", script_path, rev, "--seed", V5_SEED, "--jobs", "2"]
        if tool_mutant:
            mutant = blob(rev, tool_mutant)
            mutant_path = os.path.join(td, "exactbool-tool.py")
            with open(mutant_path, "wb") as stream:
                stream.write(mutant)
            args += ["--tool-file", mutant_path]
        env = dict(os.environ, HOME=os.path.join(LANE, V5_HOME_REL))
        p = subprocess.run(args, cwd=LANE, env=env, capture_output=True, text=True)
        return p.returncode, p.stdout + p.stderr


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

    # --- leg h1-receipt (QUALITY 39 named committed-receipt basis) -------------
    # The ephemeral H1 directory was cleaned before the round-28 closure (M28-2);
    # the round-29 registration names this committed w2 receipt as the leg's
    # verification basis (owner: mado, recorded at data time).
    H1_RECEIPT_REL = ".ufo/waves/round-28/w2/reports/ReviewerSuiteMonotone.md"
    receipt = (blob(rev, H1_RECEIPT_REL) or b"").decode()
    new_run = re.search(r"new:\s+PRED-C2-r27-v2 .*h_killed=18/18 .*verdict=TARGET_MET", receipt)
    survivors_killed = all(
        re.search(r"%s\s+suite=A rc=1 KILLED" % re.escape(s), receipt)
        for s in HELD_C1V2_SURVIVORS)
    h1_ok = (new_run is not None and "monotone" in receipt.lower() and survivors_killed)
    ok &= leg(h1_ok, "h1-receipt",
              "basis=%s new-run=%s monotone=%s survivors-killed=%s" % (
                  H1_RECEIPT_REL, new_run is not None, "monotone" in receipt.lower(), survivors_killed))


    # --- leg boolword-v5 ----------------------------------------------------
    rc, out = run_v5(rev)
    normal = re.search(r"PRED-C1-r28-v5 cases_pass=(\d+)/(\d+) boolword_pass=(\d+)/(\d+) verdict=(TARGET_MET|TARGET_MISSED)", out)
    exact_rc, exact_out = run_v5(rev, EXACTBOOL_TOOL)
    mutant = re.search(r"PRED-C1-r28-v5 cases_pass=(\d+)/(\d+) boolword_pass=(\d+)/(\d+) verdict=(TARGET_MET|TARGET_MISSED)", exact_out)
    bool_ok = (normal is not None and rc == 0 and normal.group(1, 2, 3, 4, 5) == ("41", "41", "2", "2", "TARGET_MET")
               and mutant is not None and exact_rc == 1 and mutant.group(3, 4, 5) == ("0", "2", "TARGET_MISSED"))
    ok &= leg(bool_ok, "boolword-v5", "normal=%s mutant=%s" % (
        normal.group(0) if normal else "missing", mutant.group(0) if mutant else "missing"))

    # --- leg h2-rotate ------------------------------------------------------
    local_seal = seal_bytes(H2_SEAL)
    seal_ok = local_seal is not None and blob(rev, H2_SEAL_REL) == local_seal
    rc, out, err = run_counter(rev, H2_HELDOUT, H2_SEAL)
    met = re.search(r"verdict=(TARGET_MET|TARGET_MISSED)", out)
    h2_ok = seal_ok and rc == 0 and met and met.group(1) == "TARGET_MET"
    ok &= leg(h2_ok, "h2-rotate",
              "seal-at-rev=%s rc=%d %s" % (seal_ok, rc, met.group(1) if met else "no-verdict"))

    # --- leg refpub-kills ----------------------------------------------------
    local_seal = seal_bytes(REF_SEAL)
    seal_ok = local_seal is not None and blob(rev, REF_SEAL_REL) == local_seal
    rc, out, err = run_counter(rev, REF_HELDOUT, REF_SEAL)
    m = re.search(r"h_killed=(\d+)/(\d+) h_need=\d+ h_valid=(\d+) h_min_per_subject=(\d+)", out)
    ref_ok = False
    if m:
        killed, total, valid, minper = map(int, m.groups())
        ref_ok = (seal_ok and rc == 0 and killed == total and valid >= 9 and minper >= 2)
    ok &= leg(ref_ok, "refpub-kills",
              "seal-at-rev=%s rc=%d %s" % (seal_ok, rc, m.group(0) if m else "no-h-tally"))

    # --- leg q36-witness -----------------------------------------------------
    runner_blob = blob(rev, Q36_RUNNER_REL)
    checker_blob = blob(rev, "quality/check-control-receipts.py")
    receipts = (blob(rev, Q36_RECEIPTS) or b"").decode()
    if runner_blob is None or checker_blob is None:
        ok &= leg(False, "q36-witness", "runner-or-checker missing at REV")
    else:
      with tempfile.TemporaryDirectory(prefix="mado-r28-q36-") as td:
        runner_path = os.path.join(td, "q36-successor-run.sh")
        checker_path = os.path.join(td, "check-control-receipts.py")
        with open(runner_path, "wb") as stream:
            stream.write(runner_blob)
        with open(checker_path, "wb") as stream:
            stream.write(checker_blob)
        env = dict(os.environ, MADO_Q36_CHECKER=checker_path)
        p = subprocess.run(["bash", runner_path], cwd=LANE, env=env,
                           capture_output=True, text=True)
      q36_ok = (p.returncode == 0 and "Q2-glob-case-sensitive" in receipts
                and "Q5-marker-case-insensitive" in receipts)
      ok &= leg(q36_ok, "q36-witness", "rc=%d names=%s" % (
          p.returncode, "Q2-glob-case-sensitive" in receipts and "Q5-marker-case-insensitive" in receipts))

    # --- leg q37-open-ended --------------------------------------------------
    checker_blob = blob(rev, Q37_CHECKER_REL)
    registration = blob(rev, R27_REG)
    receipt = blob(rev, R27_RECEIPT)
    r26 = blob(rev, Q37_R26_ARTIFACT)
    if checker_blob is None or registration is None or receipt is None or r26 is None:
        ok &= leg(False, "q37-open-ended", "checker/registration/receipt/r26 missing at REV")
        print("PRED-C1-r29 verdict=%s" % ("TARGET_MET" if ok else "TARGET_MISSED"))
        print("exit=%d" % (0 if ok else 1))
        return 0 if ok else 1
    with tempfile.TemporaryDirectory(prefix="mado-r28-q37-") as td:
        checker_path = os.path.join(td, "check-population.py")
        registration_path = os.path.join(td, "registration.md")
        receipt_path = os.path.join(td, "c2-after.txt")
        for path, content in ((checker_path, checker_blob), (registration_path, registration),
                              (receipt_path, receipt)):
            with open(path, "wb") as stream:
                stream.write(content)
        p = subprocess.run([sys.executable, "-I", checker_path, "--registration",
                            registration_path, receipt_path], cwd=LANE, capture_output=True, text=True)
    q37_ok = p.returncode == 0 and "verdict=PASS" in p.stdout
    r26_sha = sha(r26)
    q37_ok &= r26_sha == Q37_R26_SHA
    ok &= leg(q37_ok, "q37-open-ended", "rc=%d r26sha=%s" % (p.returncode, r26_sha[:12]))

    print("PRED-C1-r29 verdict=%s" % ("TARGET_MET" if ok else "TARGET_MISSED"))
    print("exit=%d" % (0 if ok else 1))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
