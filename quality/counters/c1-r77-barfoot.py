#!/usr/bin/env python3
"""mado — PRED-C1-r77-v1: score the bar-footprint join on a frozen case set.

The counter extracts `tools/mado-barfoot.py` from the revision under test, runs it
against fifteen frozen case artifacts, and checks the published verdict per case.
It then kills five named single-anchor mutations of the join rule and scores a
naive live-echo control that skips the join entirely.

Counting command (round 77):
  python3 -I quality/counters/c1-r77-barfoot.py --repo . --rev REV \
      --controls .ufo/waves/round-77/controls/c1-cases-r77.json --scratch-root DIR

Contract: MADO_R77_BARFOOT: cases=15 correct=15 mutants=5 killed=5 base_correct=8/15
tool_selftest=18/18 verdict=TARGET_MET rev=<hash>  (rc 0 iff every clause holds).

Exit map: 0 target met · 1 target missed · 2 setup error (never a verdict).
Writes only inside the caller's --scratch-root generation directory; removes it.
"""

import argparse
import json
import os
import re
import shutil
import stat
import subprocess
import sys
import tempfile

CASES = 15
MUTANTS = 5

MUTATIONS = [
    ("level-top-swap", 'LEVEL = {"background": 0, "bottom": 1, "top": 2, "overlay": 3}',
     'LEVEL = {"background": 0, "bottom": 1, "top": 1, "overlay": 3}'),
    ("exclusive-false-ignored", 'if not bar["exclusive"]:', "if False:"),
    ("no-centred-width", 'if bar["width"] > 1:', 'if bar["width"] > 100000:'),
    ("reserved-wrong-edge", 'RESERVED_INDEX = {"left": 0, "top": 1, "right": 2, "bottom": 3}',
     'RESERVED_INDEX = {"left": 0, "top": 3, "right": 2, "bottom": 1},'),
    ("per-side-margin-dropped",
     'sides[side] = value if isinstance(value, int) and not isinstance(value, bool) else 0',
     'sides[side] = 0'),
]

LEVEL = {"background": 0, "bottom": 1, "top": 2, "overlay": 3}


class Setup(Exception):
    pass


def sha256(data):
    import hashlib
    return hashlib.sha256(data).hexdigest()


def run(argv, cwd, timeout=60):
    env = {
        "PATH": os.environ.get("PATH", "/usr/bin:/bin"),
        "LC_ALL": "C",
        "LANG": "C",
        "PYTHONDONTWRITEBYTECODE": "1",
    }
    try:
        proc = subprocess.run(argv, cwd=cwd, env=env, stdout=subprocess.PIPE,
                              stderr=subprocess.PIPE, timeout=timeout, stdin=subprocess.DEVNULL)
        return proc.returncode, proc.stdout.decode("utf-8", "replace"), proc.stderr.decode("utf-8", "replace")
    except subprocess.TimeoutExpired:
        return 124, "", "timeout"
    except OSError as exc:
        raise Setup("cannot run child: %s" % exc)


def parse_result(stdout):
    box = reserved = verdict = None
    m = re.search(r"^MADO_BARFOOT_RESULT: .*?box=(\S+) reserved=(\S+).*?verdict=(\S+)\s*$", stdout, re.M)
    if m:
        box, reserved, verdict = m.group(1), m.group(2), m.group(3)
    m = re.search(r"^MADO_BARFOOT: verdict=(\S+)\s*$", stdout, re.M)
    if m:
        verdict = m.group(1)
    return box, reserved, verdict


def case_files(case, outdir):
    os.makedirs(outdir, exist_ok=True)
    cfg = os.path.join(outdir, "config.json")
    with open(cfg, "w") as fh:
        json.dump(case["config"], fh)
    layers = os.path.join(outdir, "layers.json")
    if "layers_raw" in case:
        with open(layers, "w") as fh:
            fh.write(case["layers_raw"])
    else:
        with open(layers, "w") as fh:
            json.dump(case["layers"], fh)
    monitors = os.path.join(outdir, "monitors.json")
    with open(monitors, "w") as fh:
        json.dump(case["monitors"], fh)
    return cfg, layers, monitors


def expected_ok(case, rc, stdout):
    exp = case["expect"]
    if exp.get("error"):
        return rc == exp["rc"] and "ERROR (stage=setup" in stdout
    box, reserved, verdict = parse_result(stdout)
    return (rc == exp["rc"] and box == exp["box"] and reserved == exp["reserved"]
            and verdict == exp["verdict"])


def run_cases(tool, cases, workroot, label):
    correct = 0
    rows = []
    for index, case in enumerate(cases):
        outdir = os.path.join(workroot, "%s-%02d" % (label, index))
        cfg, layers, monitors = case_files(case, outdir)
        argv = [sys.executable, "-I", tool, "--config", cfg, "--layers", layers, "--monitors", monitors]
        if case.get("monitor"):
            argv += ["--monitor", case["monitor"]]
        rc, stdout, stderr = run(argv, outdir)
        ok = expected_ok(case, rc, stdout)
        correct += 1 if ok else 0
        box, reserved, verdict = parse_result(stdout)
        rows.append((case["name"], rc, box, reserved, verdict, ok))
    return correct, rows


def naive_score(cases):
    """The live-echo control: no config model, no reserved model, no drift."""
    correct = 0
    for case in cases:
        if "layers_raw" in case:
            continue  # cannot read the reply -> not a verdict
        cfg = case["config"]
        level = LEVEL.get(cfg.get("layer", "bottom"))
        monitor = case.get("monitor") or case["monitors"][0]["name"]
        entries = case["layers"].get(monitor, {}).get("levels", {}).get(str(level), [])
        hits = [e for e in entries if e.get("namespace") == "waybar"]
        if not hits:
            got = {"rc": 3, "box": "NO_LAYER", "reserved": "NOT_CHECKED", "verdict": "NO_LAYER"}
        else:
            mon = next(m for m in case["monitors"] if m["name"] == monitor)
            edge = {"top": 1, "right": 2, "bottom": 3, "left": 0}[cfg.get("position", "top")]
            got = {"rc": 0, "box": "MATCH",
                   "reserved": "EQ" if mon["reserved"][edge] > 0 else "NOT_APPLIED",
                   "verdict": "CLEAN"}
        exp = case["expect"]
        if (got["rc"] == exp.get("rc") and got["box"] == exp.get("box")
                and got["reserved"] == exp.get("reserved") and got["verdict"] == exp.get("verdict")):
            correct += 1
    return correct


def apply_mutation(source, anchor, replacement, name):
    count = source.count(anchor)
    if count != 1:
        raise Setup("mutant %s anchor occurs %d times, not once" % (name, count))
    return source.replace(anchor, replacement)


def selftest():
    checks = total = 0

    def ok(cond, label):
        nonlocal checks, total
        total += 1
        if cond:
            checks += 1
        else:
            print("MADO_R77_BARFOOT_SELFTEST_FAIL: %s" % label)

    tmp = tempfile.mkdtemp(prefix="c1r77-self-")
    try:
        cases = [{
            "name": "self",
            "config": {"position": "top", "layer": "top", "height": 26},
            "layers": {"M1": {"levels": {"0": [], "1": [], "2": [
                {"namespace": "waybar", "x": 0, "y": 0, "w": 1920, "h": 26, "alpha": 1, "pid": 1}], "3": []}}},
            "monitors": [{"name": "M1", "width": 1920, "height": 1080, "reserved": [0, 26, 0, 0]}],
            "expect": {"rc": 0, "box": "MATCH", "reserved": "EQ", "verdict": "CLEAN"},
        }]
        ok(expected_ok(cases[0], 0,
                       "MADO_BARFOOT_RESULT: monitor=M1 box=MATCH reserved=EQ band=26 expected=26 verdict=CLEAN\n"
                       "MADO_BARFOOT: verdict=CLEAN\n"), "correct expectation accepted")
        ok(not expected_ok(cases[0], 0,
                           "MADO_BARFOOT_RESULT: monitor=M1 box=DIFFER reserved=EQ band=26 expected=26 verdict=DIFFER\n"
                           "MADO_BARFOOT: verdict=DIFFER\n"), "wrong expectation refused")
        ok(not expected_ok(cases[0], 2, "MADO_BARFOOT: ERROR (stage=setup x)\n"), "setup path not a verdict")
        ok(naive_score([]) == 0, "empty base scores zero")
        for name, anchor, repl in MUTATIONS:
            src = "a\n" + anchor + "\nb\n"
            ok(apply_mutation(src, anchor, repl, name) == "a\n" + repl + "\nb\n", "anchor %s" % name)
            try:
                apply_mutation("a\nb\n", anchor, repl, name)
                ok(False, "missing anchor refused %s" % name)
            except Setup:
                ok(True, "missing anchor refused %s" % name)
        ok(sha256(b"x") == sha256(b"x") and len(sha256(b"x")) == 64, "sha256 stable")
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    print("MADO_R77_BARFOOT_SELFTEST: %d/%d" % (checks, total))
    return 0 if checks == total else 1


def main(argv):
    ap = argparse.ArgumentParser(add_help=True)
    ap.add_argument("--repo")
    ap.add_argument("--rev")
    ap.add_argument("--controls")
    ap.add_argument("--scratch-root")
    ap.add_argument("--selftest", action="store_true")
    args = ap.parse_args(argv)
    if args.selftest:
        return selftest()
    if not (args.repo and args.rev and args.controls and args.scratch_root):
        print("MADO_R77_BARFOOT: ERROR (stage=setup usage)")
        return 2
    try:
        repo = os.path.abspath(args.repo)
        if args.scratch_root == "/":
            raise Setup("refusing / as the scratch root")
        if os.path.islink(args.scratch_root):
            raise Setup("refusing a symlinked scratch root")
        os.makedirs(args.scratch_root, exist_ok=True)
        if not os.path.isdir(args.scratch_root):
            raise Setup("scratch root is not a directory")
        workroot = tempfile.mkdtemp(prefix="c1-r77-", dir=args.scratch_root)
        tool_path = os.path.join(workroot, "mado-barfoot.py")
        rc, source, err = run(["git", "-C", repo, "show", args.rev + ":tools/mado-barfoot.py"],
                             workroot, timeout=60)
        if rc != 0:
            raise Setup("cannot extract tools/mado-barfoot.py at %s: %s" % (args.rev, err.strip()))
        with open(tool_path, "w") as fh:
            fh.write(source)
        tool_sha = sha256(source.encode())
        proc = subprocess.run(["git", "-C", repo, "rev-parse", args.rev], stdout=subprocess.PIPE,
                              stderr=subprocess.PIPE)
        rev_full = proc.stdout.decode().strip()
        if proc.returncode != 0 or not rev_full:
            raise Setup("cannot resolve --rev %r" % args.rev)
        with open(args.controls) as fh:
            control = json.load(fh)
        cases = control["cases"]
        if len(cases) != CASES:
            raise Setup("control set carries %d cases, frozen target expects %d" % (len(cases), CASES))
        control_sha = sha256(open(args.controls, "rb").read())

        rc, out, err = run([sys.executable, "-I", tool_path, "--selftest"], workroot)
        m = re.search(r"MADO_BARFOOT_SELFTEST: (\d+)/(\d+)", out)
        tool_selftest = "%s/%s" % (m.group(1), m.group(2)) if m else "0/0"
        selftest_ok = rc == 0 and m and m.group(1) == m.group(2)

        correct, rows = run_cases(tool_path, cases, workroot, "cand")
        for name, crc, box, reserved, verdict, ok in rows:
            print("MADO_R77_CASE: name=%s rc=%d box=%s reserved=%s verdict=%s correct=%s"
                  % (name, crc, box, reserved, verdict, "yes" if ok else "no"))

        killed = 0
        for name, anchor, repl in MUTATIONS:
            try:
                mutated = apply_mutation(source, anchor, repl, name)
            except Setup as exc:
                print("MADO_R77_BARFOOT: ERROR (stage=setup %s)" % exc)
                return 2
            mutant_path = os.path.join(workroot, "mutant-%s.py" % name)
            with open(mutant_path, "w") as fh:
                fh.write(mutated)
            mcorrect, _ = run_cases(mutant_path, cases, workroot, "mut-" + name)
            dead = mcorrect < CASES
            killed += 1 if dead else 0
            print("MADO_R77_MUTANT: name=%s correct=%d/%d killed=%s"
                  % (name, mcorrect, CASES, "yes" if dead else "no"))

        base = naive_score(cases)
        print("MADO_R77_BASE: correct=%d/%d rule=live-echo(no-config-model,no-reserved-model,no-drift)" % (base, CASES))
        print("MADO_R77_CONTROL: sha256=%s" % control_sha)
        target = correct == CASES and killed == MUTANTS and base < CASES and selftest_ok
        print("MADO_R77_BARFOOT: cases=%d correct=%d mutants=%d killed=%d base_correct=%d/%d "
              "tool_selftest=%s verdict=%s rev=%s tool_sha256=%s"
              % (CASES, correct, MUTANTS, killed, base, CASES, tool_selftest,
                 "TARGET_MET" if target else "TARGET_MISSED", rev_full, tool_sha))
        return 0 if target else 1
    except Setup as exc:
        print("MADO_R77_BARFOOT: ERROR (stage=setup %s)" % exc)
        return 2
    finally:
        try:
            shutil.rmtree(workroot, ignore_errors=True)
        except NameError:
            pass


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
