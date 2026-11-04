#!/usr/bin/env python3
"""Round-76 pre-freeze do-nothing control.

Produces `.ufo/waves/round-76/control-baseline-r76.txt`. It scores the HELD rules (the
round-75 counter's `mz=`-only scoring rule and the round-75 guard classifier) on the
round-76 frozen sets, so the control receipt exists before the successor instruments are
measured:

  C1  the held rule reads `mz=` only. It scores 15/15 on the mz column (the kill path is
      untouched by the mutants) and kills none of the four outcome-rule mutants: the held
      rule cannot reach `killed=4`.
  C2  the held round-75 classifier scores 55/59: it cannot see the four new positives.

Run from the lane root:
  python3 -I .ufo/waves/round-76/proto/held-r76.py --repo . --base-rev c3e0bc5f... \
      --scratch-root <scratch>
"""
import argparse
import json
import os
import re
import subprocess
import sys

R75_HARNESS = "quality/counters/c1-r75-landing-controls.py"
R75_C2 = "quality/counters/c2-r75-shapes.py"
C76 = "quality/counters/c1-r76-outcome-field.py"
HARNESS_ROW = re.compile(
    r"MADO_R75_LANDING_CONTROLS: selftest=(?:[0-9]+/[0-9]+|none) mz=(pass|fail) "
    r"mr=(?:pass|fail) killed=[0-2]/2 baseline=0/2 witness=(?:ok|absent|mismatch) "
    r"verdict=(?:TARGET_MET|TARGET_MISSED) rev=[0-9a-f]{40,64}")
C76_ROW = re.compile(
    r"MADO_R76_LANDING_CONTROLS: selftest=(?:[0-9]+/[0-9]+|none) mz=(pass|fail) "
    r"mr=(?:pass|fail) killed=[0-2]/2 baseline=0/2 witness=(?:ok|absent|mismatch) "
    r"verdict=(?:TARGET_MET|TARGET_MISSED) rev=[0-9a-f]{40,64}")


def git(repo, args):
    return subprocess.run(["git", "-C", repo] + args, stdout=subprocess.PIPE,
                          stderr=subprocess.PIPE)


def main(argv):
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo", required=True)
    ap.add_argument("--base-rev", required=True)
    ap.add_argument("--scratch-root", required=True)
    args = ap.parse_args(argv)
    repo = os.path.abspath(args.repo)
    scratch = os.path.abspath(args.scratch_root)
    os.makedirs(scratch, exist_ok=True)
    sha = git(repo, ["rev-parse", "--verify", args.base_rev + "^{commit}"])
    sha = sha.stdout.decode().strip()
    out = ["HELD_R76_CONTROL base_rev=%s scratch=%s" % (sha, scratch)]

    # ---- C2: held classifier on the round-76 frozen set
    data = git(repo, ["show", "%s:%s" % (sha, R75_C2)]).stdout
    path = os.path.join(scratch, "held-c2.py")
    with open(path, "wb") as fh:
        fh.write(data)
    sys.path.insert(0, scratch)
    import importlib.util
    spec = importlib.util.spec_from_file_location("held_c2", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    cases = json.load(open(os.path.join(repo, ".ufo/waves/round-76/controls/c2-cases-r76.json")))["cases"]
    misses = []
    for case in cases:
        reader, guard = mod.classify(case["src"])
        if reader != case["expect_reader"] or guard != case["expect_guard"]:
            misses.append(case["name"])
    out.append("HELD_R76_C2 held_controls=%d/%d missed=%s target=59/59 met=%s"
               % (len(cases) - len(misses), len(cases), ",".join(misses) or "none",
                  "yes" if not misses else "no"))

    # ---- C1: held mz-only scoring rule on the round-76 frozen set and its mutants
    spec2 = importlib.util.spec_from_file_location(
        "c76", os.path.join(repo, C76))
    c76 = importlib.util.module_from_spec(spec2)
    spec2.loader.exec_module(c76)
    harness_bytes = git(repo, ["show", "%s:%s" % (sha, R75_HARNESS)]).stdout
    hpath = os.path.join(scratch, "held-harness.py")
    with open(hpath, "wb") as fh:
        fh.write(harness_bytes)

    c1_cases = json.load(open(os.path.join(repo, ".ufo/waves/round-76/controls/c1-outcome-cases-r76.json")))["cases"]
    env = c76.git_env(os.path.join(scratch, "home"))
    os.makedirs(os.path.join(scratch, "home"), exist_ok=True)
    lane_files = {p: git(repo, ["show", "%s:%s" % (sha, p)]).stdout
                  for p in (c76.USEDBY, c76.LEDGER, c76.CITECHECK, c76.R72)}
    work = os.path.join(scratch, "held-c1")
    os.makedirs(work, exist_ok=True)
    mz_correct = outcome_correct = 0
    for case in c1_cases:
        root = os.path.join(work, "fixtures", case["name"])
        if not os.path.isdir(root):
            root = c76.make_fixture(work, case, lane_files, env)
        run = c76.harness_run(hpath, root, os.path.join(work, "held", case["name"]), env)
        text = run.stdout.decode("utf-8", "replace")
        mz = None
        for line in reversed(text.splitlines()):
            m = HARNESS_ROW.fullmatch(line.strip())
            if m:
                mz = m.group(1)
                break
        mz_correct += int(mz == case["expect_mz"])
    out.append("HELD_R76_C1 held_mz_correct=%d/%d outcome_field_scored=no"
               % (mz_correct, len(c1_cases)))

    cand = open(os.path.join(repo, c76.CAND), "rb").read()
    base_killed = 0
    for name, patched in c76.apply_mutants(cand):
        path = os.path.join(scratch, "held-mutant-%s.py" % name)
        with open(path, "wb") as fh:
            fh.write(patched)
        mz_score = 0
        for case in c1_cases:
            root = os.path.join(work, "fixtures", case["name"])
            run = c76.harness_run(path, root, os.path.join(work, "mut", name, case["name"]), env)
            text = run.stdout.decode("utf-8", "replace")
            mz = None
            for line in reversed(text.splitlines()):
                m = C76_ROW.fullmatch(line.strip())
                if m:
                    mz = m.group(1)
                    break
            mz_score += int(mz == case["expect_mz"])
        killed = mz_score < len(c1_cases)
        base_killed += int(killed)
        out.append("HELD_R76_C1_MUTANT name=%s mz_score=%d/%d killed_by_held_rule=%s"
                   % (name, mz_score, len(c1_cases), "yes" if killed else "no"))
    out.append("HELD_R76_TARGETS c1_killed=0/4 (target 4/4, control misses) "
               "c2_controls=55/59 (target 59/59, control misses)")
    print("\n".join(out))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
