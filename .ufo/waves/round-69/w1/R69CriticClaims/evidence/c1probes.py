#!/usr/bin/env python3
"""Two C1 reachability probes against the committed counter (5fc29ae):
A) shortcut: a 20-line textual self-check harness (no body, no children, no oracle pairing)
   scores killed=3/3 and TARGET_MET.
B) false green: with the r68 base harness's anchors already consumed, base=0/3 applied=0/3
   still prints TARGET_MET (base_applied is not in the verdict).
Fixture repos only; the lane is read-only."""
import base64, os, shutil, subprocess, sys, tempfile

LANE = "/home/vgpnk/Projects/shokunin/mado-shokunin"
S = os.path.dirname(os.path.abspath(__file__))
REV = "296ed0d75e361387908cf2dd418d3677f49f94c8"
BASE = "04093b83f73a841117d3b31dbb2a6063f4f2a454"
CAND = "quality/counters/c1-r69-landing-controls.py"
R68 = "quality/counters/c1-r68-landing-controls.py"
COUNTER = "quality/counters/c1-r69-paired-recipes.py"

R1_OLD = ("            mr_killed = bool(u_ok and not control_ok(mr_rc, mr_marker)\n"
          "                             and forged_credit(mr_rc, mr_marker))")
R1_NEW = "            mr_killed = bool(u_ok and not control_ok(mr_rc, mr_marker))"
R2_OLD = "        mz_killed = mz_rc != 0"
R2_NEW = '        mz_killed = mz_rc != 0 or mz_summary == "none"'
R3_OLD = "    subprocess.run = _no_spawn"
R3_NEW = "    pass  # spawn guard removed by recipe"

FAKE = '''#!/usr/bin/env python3
"""Shortcut harness under test: no measurement body, no children, no oracle pairing."""
import sys

# the frozen anchors must occur here, each exactly once, so the frozen recipes apply
ANCHORS = """%s
%s
%s
"""

WANT1 = bytes.fromhex("616e6420666f726765645f637265646974286d725f72632c206d725f6d61726b65722929").decode()
FORBID2 = bytes.fromhex("6d7a5f73756d6d617279203d3d20226e6f6e6522").decode()
WANT3 = bytes.fromhex("73756270726f636573732e72756e203d205f6e6f5f737061776e").decode()


def main(argv):
    if "--selftest" not in argv:
        return 2
    src = open(__file__, "r", encoding="utf-8").read()
    checks = [("paired forged credit present", WANT1 in src),
              ("no summary-oracle widening", FORBID2 not in src),
              ("hermetic spawn guard present", WANT3 in src)]
    passed = sum(1 for _n, ok in checks if ok)
    for n, ok in checks:
        if not ok:
            print("MADO_R69_SELFTEST_FAIL: %%s" %% n)
    print("MADO_R69_LANDING_CONTROLS_SELFTEST: %%d/%%d assertions passed" %% (passed, len(checks)))
    return 0 if passed == len(checks) else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
''' % (R1_OLD, R2_OLD, R3_OLD)


def blob(rev, path):
    return subprocess.check_output(["git", "-C", LANE, "cat-file", "-p", "%s:%s" % (rev, path)])


def fixture(tag, base_bytes, cand_bytes):
    D = tempfile.mkdtemp(prefix="fixture.%s." % tag, dir=S)
    subprocess.check_call(["git", "-C", D, "init", "-q"])
    got = subprocess.check_output(["git", "-C", D, "rev-parse", "--show-toplevel"]).decode().strip()
    assert os.path.realpath(got) == os.path.realpath(D), (got, D)
    ident = ["-c", "user.name=R69CriticClaims", "-c", "user.email=critic@example.invalid"]
    os.makedirs(os.path.join(D, "quality/counters"), exist_ok=True)
    open(os.path.join(D, R68), "wb").write(base_bytes)
    open(os.path.join(D, CAND), "wb").write(cand_bytes)
    subprocess.check_call(["git", "-C", D, *ident, "add", "-A"])
    subprocess.check_call(["git", "-C", D, *ident, "commit", "-q", "-m", "candidate %s" % tag])
    rev = subprocess.check_output(["git", "-C", D, "rev-parse", "HEAD"]).decode().strip()
    # second commit: a base-only history marker is not needed; --base-rev points at this rev too,
    # so put the base harness its own commit for the base leg
    return D, rev


def run_counter(D, rev, base_rev, scratch, label):
    shutil.rmtree(scratch, ignore_errors=True)
    os.makedirs(scratch)
    cmd = [sys.executable, "-I", os.path.join(LANE, COUNTER), "--repo", D,
           "--rev", rev, "--base-rev", base_rev, "--scratch-root", scratch]
    r = subprocess.run(cmd, cwd=LANE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=1800)
    out = (r.stdout + r.stderr).decode()
    print("### %s RC=%d" % (label, r.returncode))
    print(out)
    return r.returncode, out


def main():
    # --- A: shortcut harness vs the real r68 base harness --------------------------------
    real_r68 = blob(BASE, R68)
    D, rev = fixture("shortcut", real_r68, FAKE.encode())
    try:
        run_counter(D, rev, rev, os.path.join(S, "st-shortcut"), "A shortcut harness (base=real r68)")
    finally:
        shutil.rmtree(D, ignore_errors=True)
        shutil.rmtree(os.path.join(S, "st-shortcut"), ignore_errors=True)

    # --- B: false green: base anchors already consumed ----------------------------------
    consumed = blob(BASE, R68).decode()
    for old, new in ((R1_OLD, R1_NEW), (R2_OLD, R2_NEW), (R3_OLD, R3_NEW)):
        assert consumed.count(old) == 1
        consumed = consumed.replace(old, new)
    real_cand = blob(REV, CAND)
    D2 = tempfile.mkdtemp(prefix="fixture.falsegreen.", dir=S)
    try:
        subprocess.check_call(["git", "-C", D2, "init", "-q"])
        got = subprocess.check_output(["git", "-C", D2, "rev-parse", "--show-toplevel"]).decode().strip()
        assert os.path.realpath(got) == os.path.realpath(D2)
        ident = ["-c", "user.name=R69CriticClaims", "-c", "user.email=critic@example.invalid"]
        os.makedirs(os.path.join(D2, "quality/counters"), exist_ok=True)
        open(os.path.join(D2, R68), "w").write(consumed)
        subprocess.check_call(["git", "-C", D2, *ident, "add", "-A"])
        subprocess.check_call(["git", "-C", D2, *ident, "commit", "-q", "-m", "base: anchors consumed"])
        base_rev = subprocess.check_output(["git", "-C", D2, "rev-parse", "HEAD"]).decode().strip()
        open(os.path.join(D2, CAND), "wb").write(real_cand)
        subprocess.check_call(["git", "-C", D2, *ident, "add", "-A"])
        subprocess.check_call(["git", "-C", D2, *ident, "commit", "-q", "-m", "candidate: real r69 harness"])
        head = subprocess.check_output(["git", "-C", D2, "rev-parse", "HEAD"]).decode().strip()
        run_counter(D2, head, base_rev, os.path.join(S, "st-falsegreen"), "B base anchors absent")
    finally:
        shutil.rmtree(D2, ignore_errors=True)
        shutil.rmtree(os.path.join(S, "st-falsegreen"), ignore_errors=True)


if __name__ == "__main__":
    main()
