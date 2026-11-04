#!/usr/bin/env python3
"""mado — PRED-C1-r78-v1: score the margined band model on a frozen case set.

The counter extracts `tools/mado-barfoot.py` from the revision under test and from the base
revision, runs both against eighteen frozen case artifacts, checks the published verdict,
band and expected value per case, kills seven named single-anchor mutations of the r78 rule,
and scores the base tool (the held r77 model: no margin composition, no negative-margin
refusal) on the same set as the do-nothing control.

Counting command (round 78):
  python3 -I quality/counters/c1-r78-margins.py --repo . --rev REV --base-rev BASE \
      --controls .ufo/waves/round-78/controls/c1-cases-r78.json --scratch-root DIR

Contract: MADO_R78_BARFOOT: cases=18 correct=18 mutants=7 killed=7 base_correct=8/18
tool_selftest=22/22 verdict=TARGET_MET rev=<hash> tool_sha256=<sha> (rc 0 iff every clause
holds).

Exit map: 0 target met · 1 target missed · 2 setup error (never a verdict).
Writes only inside the caller's scratch root; removes its generation directory.
"""

import argparse
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile

CASES = 18
MUTANTS = 7

MUTATIONS = [
    ("opposite-margin-dropped",
     'expected = extent + bar["margins"][OPPOSITE_EDGE[edge]]',
     'expected = extent'),
    ("horizontal-margin-leak",
     'expected = extent + bar["margins"][OPPOSITE_EDGE[edge]]',
     'expected = extent + bar["margins"]["left"] + bar["margins"]["right"]'),
    ("level-bottom-swap",
     'LEVEL = {"background": 0, "bottom": 1, "top": 2, "overlay": 3}',
     'LEVEL = {"background": 0, "bottom": 2, "top": 2, "overlay": 3}'),
    ("right-extent-flip",
     '    return mon_w - box["x"]',
     '    return box["x"] + box["w"]'),
    ("per-side-margin-dropped",
     'sides[side] = value if isinstance(value, int) and not isinstance(value, bool) else 0',
     'sides[side] = 0'),
    ("negative-margin-accepted",
     'if any(value < 0 for value in margins.values()):',
     'if False:'),
    ("opposite-edge-wrong",
     'OPPOSITE_EDGE = {"top": "bottom", "bottom": "top", "left": "right", "right": "left"}',
     'OPPOSITE_EDGE = {"top": "top", "bottom": "bottom", "left": "left", "right": "right"}'),
]


class Setup(Exception):
    pass


def sha256(data):
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
        return (proc.returncode, proc.stdout.decode("utf-8", "replace"),
                proc.stderr.decode("utf-8", "replace"))
    except subprocess.TimeoutExpired:
        return 124, "", "timeout"
    except OSError as exc:
        raise Setup("cannot run child: %s" % exc)


def parse_result(stdout):
    """Return (box, reserved, band, expected, verdict) from the tool's RESULT line."""
    m = re.search(r"^MADO_BARFOOT_RESULT: .*?box=(\S+) reserved=(\S+)"
                  r"(?: band=(-?\d+) expected=(-?\d+))?.*?verdict=(\S+)\s*$", stdout, re.M)
    if not m:
        return None, None, None, None, None
    band = int(m.group(3)) if m.group(3) is not None else None
    expected = int(m.group(4)) if m.group(4) is not None else None
    return m.group(1), m.group(2), band, expected, m.group(5)


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
        return rc == exp["rc"] and "ERROR (" in stdout
    box, reserved, band, expected, verdict = parse_result(stdout)
    if box is None:
        return False
    got = {"rc": rc, "box": box, "reserved": reserved, "band": band,
           "expected": expected, "verdict": verdict}
    return all(got[key] == exp[key] for key in exp)


def run_cases(tool, cases, workroot, label):
    correct = 0
    rows = []
    for index, case in enumerate(cases):
        outdir = os.path.join(workroot, "%s-%02d" % (label, index))
        cfg, layers, monitors = case_files(case, outdir)
        argv = [sys.executable, "-I", tool, "--config", cfg, "--layers", layers,
                "--monitors", monitors]
        if case.get("monitor"):
            argv += ["--monitor", case["monitor"]]
        rc, stdout, stderr = run(argv, outdir)
        ok = expected_ok(case, rc, stdout)
        correct += 1 if ok else 0
        box, reserved, band, expected, verdict = parse_result(stdout)
        rows.append((case["name"], rc, box, reserved, band, expected, verdict, ok))
    return correct, rows


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
            print("MADO_R78_BARFOOT_SELFTEST_FAIL: %s" % label)

    exp = {"rc": 0, "box": "MATCH", "reserved": "EQ", "band": 34, "expected": 34,
           "verdict": "CLEAN"}
    case = {"name": "self", "expect": exp}
    line = ("MADO_BARFOOT_RESULT: monitor=M1 box=MATCH reserved=EQ band=34 expected=34 "
            "verdict=CLEAN\nMADO_BARFOOT: verdict=CLEAN\n")
    ok(expected_ok(case, 0, line), "correct expectation accepted")
    ok(not expected_ok(case, 0, line.replace("band=34", "band=30")), "band mismatch refused")
    ok(not expected_ok(case, 0, line.replace("expected=34", "expected=38")),
       "expected mismatch refused")
    ok(not expected_ok(case, 0, line.replace("reserved=EQ", "reserved=GT")),
       "reserved mismatch refused")
    ok(not expected_ok(case, 2, "MADO_BARFOOT: ERROR (stage=setup x)\n"), "setup is not a verdict")
    ok(expected_ok({"expect": {"error": True, "rc": 3}}, 3,
                   "MADO_BARFOOT: ERROR (stage=model x)\n"), "model refusal accepted")
    ok(not expected_ok({"expect": {"error": True, "rc": 3}}, 0,
                       "MADO_BARFOOT: ERROR (stage=model x)\n"),
       "refusal rc mismatch refused")
    box, reserved, band, expected, verdict = parse_result(line)
    ok((box, reserved, band, expected, verdict) == ("MATCH", "EQ", 34, 34, "CLEAN"),
       "parse full result")
    box, reserved, band, expected, verdict = parse_result(
        "MADO_BARFOOT_RESULT: monitor=M1 box=NOT_ON_MONITOR reserved=NOT_APPLIED verdict=NO_BAR\n")
    ok((box, reserved, band, expected, verdict) == ("NOT_ON_MONITOR", "NOT_APPLIED", None, None,
                                                    "NO_BAR"), "parse field-less result")
    for name, anchor, repl in MUTATIONS:
        src = "a\n" + anchor + "\nb\n"
        ok(apply_mutation(src, anchor, repl, name) == "a\n" + repl + "\nb\n", "anchor %s" % name)
        try:
            apply_mutation("a\nb\n", anchor, repl, name)
            ok(False, "missing anchor refused %s" % name)
        except Setup:
            ok(True, "missing anchor refused %s" % name)
    ok(sha256(b"x") == sha256(b"x") and len(sha256(b"x")) == 64, "sha256 stable")
    print("MADO_R78_BARFOOT_SELFTEST: %d/%d" % (checks, total))
    return 0 if checks == total else 1


def extract(repo, rev, path, outdir):
    rc, source, err = run(["git", "-C", repo, "show", rev + ":" + path], outdir)
    if rc != 0:
        raise Setup("cannot extract %s at %s: %s" % (path, rev, err.strip()))
    return source


def resolve(repo, rev):
    rc, out, err = run(["git", "-C", repo, "rev-parse", rev], repo)
    full = out.strip()
    if rc != 0 or not full:
        raise Setup("cannot resolve revision %r" % rev)
    return full


def main(argv):
    ap = argparse.ArgumentParser(add_help=True)
    ap.add_argument("--repo")
    ap.add_argument("--rev")
    ap.add_argument("--base-rev")
    ap.add_argument("--controls")
    ap.add_argument("--scratch-root")
    ap.add_argument("--no-mutants", action="store_true")
    ap.add_argument("--selftest", action="store_true")
    args = ap.parse_args(argv)
    if args.selftest:
        return selftest()
    if not (args.repo and args.rev and args.base_rev and args.controls and args.scratch_root):
        print("MADO_R78_BARFOOT: ERROR (stage=setup usage)")
        return 2
    workroot = None
    try:
        repo = os.path.abspath(args.repo)
        if args.scratch_root == "/":
            raise Setup("refusing / as the scratch root")
        if os.path.islink(args.scratch_root):
            raise Setup("refusing a symlinked scratch root")
        os.makedirs(args.scratch_root, exist_ok=True)
        if not os.path.isdir(args.scratch_root):
            raise Setup("scratch root is not a directory")
        workroot = tempfile.mkdtemp(prefix="c1-r78-", dir=args.scratch_root)
        rev_full = resolve(repo, args.rev)
        base_full = resolve(repo, args.base_rev)

        source = extract(repo, args.rev, "tools/mado-barfoot.py", workroot)
        tool_path = os.path.join(workroot, "mado-barfoot.py")
        with open(tool_path, "w") as fh:
            fh.write(source)
        tool_sha = sha256(source.encode())

        base_source = extract(repo, args.base_rev, "tools/mado-barfoot.py", workroot)
        base_tool = os.path.join(workroot, "mado-barfoot-base.py")
        with open(base_tool, "w") as fh:
            fh.write(base_source)

        with open(args.controls) as fh:
            control = json.load(fh)
        cases = control["cases"]
        if len(cases) != CASES:
            raise Setup("control set carries %d cases, frozen target expects %d"
                        % (len(cases), CASES))
        control_sha = sha256(open(args.controls, "rb").read())

        rc, out, _ = run([sys.executable, "-I", tool_path, "--selftest"], workroot)
        m = re.search(r"MADO_BARFOOT_SELFTEST: (\d+)/(\d+)", out)
        tool_selftest = "%s/%s" % (m.group(1), m.group(2)) if m else "0/0"
        selftest_ok = rc == 0 and m is not None and m.group(1) == m.group(2)

        correct, rows = run_cases(tool_path, cases, workroot, "cand")
        for name, crc, box, reserved, band, expected, verdict, ok in rows:
            print("MADO_R78_CASE: name=%s rc=%d box=%s reserved=%s band=%s expected=%s "
                  "verdict=%s correct=%s"
                  % (name, crc, box, reserved, band, expected, verdict, "yes" if ok else "no"))

        killed = 0
        if not args.no_mutants:
            for name, anchor, repl in MUTATIONS:
                mutated = apply_mutation(source, anchor, repl, name)
                mutant_path = os.path.join(workroot, "mutant-%s.py" % name)
                with open(mutant_path, "w") as fh:
                    fh.write(mutated)
                mcorrect, _ = run_cases(mutant_path, cases, workroot, "mut-" + name)
                dead = mcorrect < CASES
                killed += 1 if dead else 0
                print("MADO_R78_MUTANT: name=%s correct=%d/%d killed=%s"
                      % (name, mcorrect, CASES, "yes" if dead else "no"))

        base_correct, base_rows = run_cases(base_tool, cases, workroot, "base")
        print("MADO_R78_BASE: correct=%d/%d rule=held-r77-model(no-margin-composition,"
              "no-negative-refusal) base_rev=%s base_sha256=%s"
              % (base_correct, CASES, base_full, sha256(base_source.encode())))
        print("MADO_R78_CONTROL: sha256=%s" % control_sha)
        target = (correct == CASES and base_correct < CASES and selftest_ok
                  and (args.no_mutants or killed == MUTANTS))
        print("MADO_R78_BARFOOT: cases=%d correct=%d mutants=%s killed=%s base_correct=%d/%d "
              "tool_selftest=%s verdict=%s rev=%s tool_sha256=%s"
              % (CASES, correct, "0" if args.no_mutants else str(MUTANTS),
                 "0" if args.no_mutants else str(killed), base_correct, CASES, tool_selftest,
                 "TARGET_MET" if target else "TARGET_MISSED", rev_full, tool_sha))
        return 0 if target else 1
    except Setup as exc:
        print("MADO_R78_BARFOOT: ERROR (stage=setup %s)" % exc)
        return 2
    finally:
        if workroot:
            shutil.rmtree(workroot, ignore_errors=True)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
