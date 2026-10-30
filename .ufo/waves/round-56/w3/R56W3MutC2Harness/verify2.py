#!/usr/bin/env python3
"""R56W3MutC2Harness stage 2 — E09 rerun (fixed anchor) + proposal verification.

Proposals verified here (each: pristine+proposal stays green, the mutant+proposal is caught):

  PR-wrong-rc  kills E10 ("the exit status is not compared"):
      add ctl/wrong-rc.py — replays a committed expected.out but exits 1 — as a fifth control with the
      registered expectation "passes 0 of 26" (same family as empty/sibling-reader), denominator 5.
  PR-jail      kills B01/B04/B05 (sandbox-flag drops that no fixture can see):
      the harness must self-probe the jail it builds (cwd, /proc, interfaces, /lib) and fail closed on a
      shape deviation.
  PR-argv      kills B09 ("--die-with-parent is dropped"):
      the harness must assert the sandbox argv it builds still carries --die-with-parent/--unshare-all.

The proposal patches are applied to COPIES in scratch; the lane is never touched.

Usage: verify2.py <scratch-dir> <deliverable-dir>
"""
import json
import os
import shutil
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import driver  # noqa: E402  (reuse the stage-1 definitions and helpers)

SCRATCH = os.path.abspath(sys.argv[1])
DELIVER = os.path.abspath(sys.argv[2])
REPO = os.path.join(SCRATCH, "repo")
DELIVERABLES = os.path.join(DELIVER, "receipts")

WRONGRC_CTL = '''#!/usr/bin/env python3
"""r56 C2 control proposal (PR-wrong-rc): replays a committed fixture's expected.out but exits 1.
It must pass 0 of the 26 fixtures: the correct comparison rejects it on the exit status."""
import sys
from pathlib import Path

sys.stdout.write((Path(__file__).resolve().parent.parent / "fixtures/c2/F02/expected.out").read_text())
sys.exit(1)
'''

JAIL_PROBE_SRC = ("import json,os,socket;print(json.dumps({'cwd':os.getcwd(),"
                  "'proc':os.path.isdir('/proc'),"
                  "'ifaces':[i[1] for i in socket.if_nameindex()],"
                  "'lib':os.path.exists('/lib')},sort_keys=True))")

JAIL_EXPECT = {"cwd": "/w", "ifaces": ["lo"], "lib": True, "proc": False}

# ---------------------------------------------------------------- patches -------------------------------------------------------------
PATCH_WRONGRC = [
    ('CONTROLS = ("const-host", "empty", "sibling-reader", "lookup-committed")',
     'CONTROLS = ("const-host", "empty", "sibling-reader", "lookup-committed", "wrong-rc")'),
    ('elif name in ("empty", "sibling-reader"):',
     'elif name in ("empty", "sibling-reader", "wrong-rc"):'),
    ('fx_ok and ctl_ok == 4)', 'fx_ok and ctl_ok == 5)'),
    ('controls=%d/4', 'controls=%d/5'),
]

JAIL_BLOCK = (
    '        jail_ok = True\n'
    '        jail_probe = os.path.join(tooldir, "jailprobe.py")\n'
    '        with open(jail_probe, "w") as f:\n'
    '            f.write(' + repr(JAIL_PROBE_SRC) + ')\n'
    '        jstage = os.path.join(work, "jailstage")\n'
    '        os.makedirs(os.path.join(jstage, "tree"), exist_ok=True)\n'
    '        jout, jrc = staged_run(python, jail_probe, [], jstage, os.path.join(work, "jailcwd"), env, True)\n'
    '        shutil.rmtree(jstage, ignore_errors=True)\n'
    '        try:\n'
    '            jrep = json.loads(jout.decode("utf-8", "replace"))\n'
    '        except Exception:\n'
    '            jrep = None\n'
    '        if jrep != ' + repr(JAIL_EXPECT) + ':\n'
    '            jail_ok = False\n'
)

JAIL_ORIG_TAIL = (
    '        sys.stderr.write("r56_ctl_c2: sandbox=%s fixture_commit=%s control_scores=%s\\n" % '
    '("bwrap" if _BWRAP else "none", "ok" if fx_ok else "bad", ctl_detail))\n'
    '        met = (a == 18 and b == 8 and ho_commit == "ok" and fx_ok and ctl_ok == 4)'
)
JAIL_NEW_TAIL = (
    JAIL_BLOCK +
    '        sys.stderr.write("r56_ctl_c2: sandbox=%s fixture_commit=%s control_scores=%s\\n" % '
    '("bwrap" if _BWRAP else "none", "ok" if fx_ok else "bad", ctl_detail))\n'
    '        met = (a == 18 and b == 8 and ho_commit == "ok" and fx_ok and ctl_ok == 4 and jail_ok)'
)

PATCH_JAIL = [
    (JAIL_ORIG_TAIL, JAIL_NEW_TAIL),
]

PATCH_ARGV = [
    ('               python, "-I", program] + args',
     '               python, "-I", program] + args\n'
     '        if "--die-with-parent" not in cmd or "--unshare-all" not in cmd:\n'
     '            raise Setup("sandbox flag missing: the staged layout alone does not hide the answer key")'),
]

E09_FIXED = ("E09", "expect", driver.HARNESS,
             '        rel = os.path.relpath(full, root)\n        if os.path.islink(full):',
             '        rel = os.path.relpath(full, root)\n        if False:',
             "symlinks are not committed as link text (fixed anchor)")


def sha(path):
    with open(path, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()


import hashlib  # noqa: E402


def build_harness(tag, edits, base_dir):
    """copy of the pristine quality/ with edits applied; returns the dir."""
    d = os.path.join(SCRATCH, "harness-" + tag)
    shutil.rmtree(d, ignore_errors=True)
    os.makedirs(d)
    for f in (driver.DISPATCH, driver.HARNESS):
        shutil.copyfile(os.path.join(base_dir, os.path.basename(f)), os.path.join(d, os.path.basename(f)))
    src = open(os.path.join(d, "r56_ctl_c2.py")).read()
    for old, new in edits:
        if src.count(old) != 1:
            raise SystemExit("patch anchor count %d for %r" % (src.count(old), old[:60]))
        src = src.replace(old, new)
    with open(os.path.join(d, "r56_ctl_c2.py"), "w") as f:
        f.write(src)
    return d


def run(harness_dir, repo, rev, tag, mode="plain"):
    out = os.path.join(SCRATCH, "o2-" + tag)
    work = os.path.join(SCRATCH, "w2-" + tag)
    return driver.run_harness(harness_dir, repo, rev, work, out, mode), out


def main():
    os.makedirs(DELIVERABLES, exist_ok=True)
    with open(os.path.join(DELIVERABLES, "summary.json")) as f:
        prev = json.load(f)
    revs = prev["probe_revs"]
    base = os.path.join(SCRATCH, "pristine")
    mutroot = os.path.join(SCRATCH, "mut")
    results = {}

    # ---- 1. E09 rerun with the fixed anchor --------------------------------
    mid, family, target, old, new, note = E09_FIXED
    d = os.path.join(mutroot, mid)
    shutil.rmtree(d, ignore_errors=True)
    os.makedirs(d)
    for f in (driver.DISPATCH, driver.HARNESS):
        shutil.copyfile(os.path.join(base, os.path.basename(f)), os.path.join(d, os.path.basename(f)))
    p = os.path.join(d, "r56_ctl_c2.py")
    src = open(p).read()
    assert src.count(old) == 1, src.count(old)
    open(p, "w").write(src.replace(old, new))
    obs = driver.probe_runs(d, REPO, revs, mid, SCRATCH)
    ref = prev["pristine"]
    diffs = [k for k in sorted(ref) if obs[k] != tuple(ref[k])]
    rec = {"family": family, "note": note, "file": target, "old": old, "new": new,
           "diff_probes": diffs, "strict_probes": [x for x in diffs if x in driver.STRICT],
           "verdict": "KILLED-STRICT" if any(x in driver.STRICT for x in diffs) else ("KILLED-EXTENDED" if diffs else "SURVIVED"),
           "observables": {k: list(v) for k, v in obs.items()}}
    results["E09"] = rec
    d2 = os.path.join(DELIVERABLES, mid)
    shutil.rmtree(d2, ignore_errors=True)
    os.makedirs(d2)
    for probe in sorted(ref):
        s = os.path.join(SCRATCH, "o-%s-%s" % (mid, probe))
        if os.path.isdir(s):
            shutil.copytree(s, os.path.join(d2, probe))
    with open(os.path.join(d2, "mutant.json"), "w") as f:
        json.dump(rec, f, indent=1, sort_keys=True)
    print("E09 rerun:", rec["verdict"], diffs, flush=True)

    # ---- 2. a probe rev with ctl/wrong-rc.py added --------------------------
    stub = os.path.join(REPO, ".ufo/waves/round-56/ctl/wrong-rc.py")
    base_rev = revs["P1_base"]
    driver.git(REPO, "checkout", "-q", base_rev, "--", ".")
    driver.git(REPO, "clean", "-qfd")
    with open(stub, "w") as f:
        f.write(WRONGRC_CTL)
    driver.git(REPO, "add", "-A")
    driver.git(REPO, "-c", "user.name=ctl", "-c", "user.email=ctl@ctl", "commit", "-q", "-m", "probe wrong-rc stub")
    rev_wrongrc = driver.git(REPO, "rev-parse", "HEAD").stdout.decode().strip()
    driver.git(REPO, "checkout", "-q", base_rev, "--", ".")
    driver.git(REPO, "clean", "-qfd")
    print("wrong-rc stub rev:", rev_wrongrc, flush=True)

    def check(label, harness_dir, rev, expect_verdict):
        obs, out = run(harness_dir, REPO, rev, label)
        line = obs[1]
        verdict = "TARGET_MET" if "verdict=TARGET_MET" in line else ("SETUP" if "verdict" not in line else "TARGET_MISSED")
        ok = verdict == expect_verdict
        results[label] = {"stdout": line, "rc": obs[0], "verdict": verdict, "expected": expect_verdict, "pass": ok}
        print("%-34s %-13s rc=%s %s" % (label, verdict, obs[0], "OK" if ok else "MISMATCH"), flush=True)
        shutil.copytree(out, os.path.join(DELIVERABLES, "proposals", label), dirs_exist_ok=True)
        return ok

    os.makedirs(os.path.join(DELIVERABLES, "proposals"), exist_ok=True)
    all_ok = True

    # ---- 3. PR-wrong-rc vs E10 ---------------------------------------------
    pristine_pr = build_harness("pristine-wrongrc", PATCH_WRONGRC, base)
    e10_src = json.load(open(os.path.join(DELIVERABLES, "E10", "mutant.json")))
    e10_dir = os.path.join(mutroot, "E10")
    obs10, _ = run(pristine_pr, REPO, rev_wrongrc, "pristine-wrongrc-run")
    # rebuild the E10 mutant + proposal
    d = os.path.join(SCRATCH, "harness-E10-wrongrc")
    shutil.rmtree(d, ignore_errors=True)
    os.makedirs(d)
    for f in (driver.DISPATCH, driver.HARNESS):
        shutil.copyfile(os.path.join(base, os.path.basename(f)), os.path.join(d, os.path.basename(f)))
    src = open(os.path.join(d, "r56_ctl_c2.py")).read()
    assert src.count(e10_src["old"]) == 1
    src = src.replace(e10_src["old"], e10_src["new"])
    for old, new in PATCH_WRONGRC:
        assert src.count(old) == 1, (old[:50], src.count(old))
        src = src.replace(old, new)
    open(os.path.join(d, "r56_ctl_c2.py"), "w").write(src)
    all_ok &= check("PR-wrong-rc/pristine", pristine_pr, rev_wrongrc, "TARGET_MET")
    all_ok &= check("PR-wrong-rc/E10", d, rev_wrongrc, "TARGET_MISSED")

    # ---- 4. PR-jail vs B01/B04/B05 -----------------------------------------
    pristine_jail = build_harness("pristine-jail", PATCH_JAIL, base)
    all_ok &= check("PR-jail/pristine", pristine_jail, revs["P1_base"], "TARGET_MET")
    for mid in ("B01", "B04", "B05"):
        m = json.load(open(os.path.join(DELIVERABLES, mid, "mutant.json")))
        d = os.path.join(SCRATCH, "harness-%s-jail" % mid)
        shutil.rmtree(d, ignore_errors=True)
        os.makedirs(d)
        for f in (driver.DISPATCH, driver.HARNESS):
            shutil.copyfile(os.path.join(base, os.path.basename(f)), os.path.join(d, os.path.basename(f)))
        src = open(os.path.join(d, "r56_ctl_c2.py")).read()
        assert src.count(m["old"]) == 1, (mid, src.count(m["old"]))
        src = src.replace(m["old"], m["new"])
        for old, new in PATCH_JAIL:
            assert src.count(old) == 1, (old[:50], src.count(old))
            src = src.replace(old, new)
        open(os.path.join(d, "r56_ctl_c2.py"), "w").write(src)
        all_ok &= check("PR-jail/%s" % mid, d, revs["P1_base"], "TARGET_MISSED")

    # ---- 5. PR-argv vs B09 --------------------------------------------------
    pristine_argv = build_harness("pristine-argv", PATCH_ARGV, base)
    all_ok &= check("PR-argv/pristine", pristine_argv, revs["P1_base"], "TARGET_MET")
    m = json.load(open(os.path.join(DELIVERABLES, "B09", "mutant.json")))
    d = os.path.join(SCRATCH, "harness-B09-argv")
    shutil.rmtree(d, ignore_errors=True)
    os.makedirs(d)
    for f in (driver.DISPATCH, driver.HARNESS):
        shutil.copyfile(os.path.join(base, os.path.basename(f)), os.path.join(d, os.path.basename(f)))
    src = open(os.path.join(d, "r56_ctl_c2.py")).read()
    assert src.count(m["old"]) == 1
    src = src.replace(m["old"], m["new"])
    for old, new in PATCH_ARGV:
        assert src.count(old) == 1, (old[:50], src.count(old))
        src = src.replace(old, new)
    open(os.path.join(d, "r56_ctl_c2.py"), "w").write(src)
    all_ok &= check("PR-argv/B09", d, revs["P1_base"], "SETUP")

    with open(os.path.join(DELIVERABLES, "proposals", "verify2.json"), "w") as f:
        json.dump(results, f, indent=1, sort_keys=True)
    print("ALL PROPOSAL CHECKS:", "PASS" if all_ok else "FAIL", flush=True)


if __name__ == "__main__":
    main()
