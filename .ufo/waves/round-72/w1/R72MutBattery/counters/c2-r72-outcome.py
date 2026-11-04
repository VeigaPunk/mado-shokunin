#!/usr/bin/env python3
r"""Round-72 C2 counting command: the harness outcome verdict reads the gate's own summary
(claim C2, round 72).

    python3 quality/counters/c2-r72-outcome.py --repo . --rev REV \
        --base-rev 976684a27e99c2508037a60eec415f550f53d70e \
        --controls .ufo/waves/round-72/controls/c2-controls-r72.json --scratch-root DIR
    python3 quality/counters/c2-r72-outcome.py --selftest --scratch-root DIR

What is scored. The round-71 harness greens a run when the extracted instrument's `--selftest`
exits 0 (`outcome_exit(selftest_rc, killed)`), whatever its own summary says; a failing summary
at exit 0 is green and a fully green summary at exit 2 is red. Round 72's `outcome_verdict`
reads the LAST parsed `MADO_LANDING_COUNTERS_SELFTEST: <p>/<n> assertions passed` summary of
that run: green iff `n > 0` and `p == n`; a missing or garbled summary is not green; the kill
count still requires 2/2. The exit status is evidence, not the outcome.

The command extracts both harnesses at the scored revision and the frozen base revision, loads
them as modules, and calls each one's committed decision function on the same eight frozen
`(gate_out, gate_rc, killed)` cases. It scores the committed functions, not a whole harness run.

Printed receipt (last line, exact):

    MADO_R72_OUTCOME: cases=8 correct=<n> base_correct=<m> verdict=<TARGET_MET|TARGET_MISSED> rev=<sha>

Exit 0 iff correct == 8 and base_correct == 4; 1 iff the measurement ran and missed (the
candidate harness absent at `--rev` prints `correct=absent`); 2 on usage/setup error with the
reason on stderr and no contract line.

Selftest: `--selftest` is hermetic - it spawns nothing, touches only <scratch-root>, checks the
frozen case set's structure, the parse/scoring/verdict helpers, and imports both committed
harnesses from the lane root to assert their decision tables answer the frozen truth labels.

Declared limits: eight cases over the summary grammar the production instrument prints; the
counter scores the committed decision functions, not an end-to-end harness execution; a case
where the summary and the exit status contradict is scored by the summary by design (the exit
status cannot carry the assertion result - held ground S441/S435).
"""
import argparse
import hashlib
import importlib.util
import json
import os
import re
import shutil
import sys

TOOL = "c2-r72-outcome.py"
CANDIDATE = "quality/counters/c1-r72-landing-controls.py"
BASE_HARNESS = "quality/counters/c1-r71-landing-controls.py"
FROZEN_CASES = 8
FROZEN_CORRECT = 8
FROZEN_BASE_CORRECT = 4
UNSAFE_ROOTS = ("/tmp", "/var/tmp", "/dev/shm")
CONTRACT_RE = re.compile(
    r"MADO_R72_OUTCOME: cases=8 correct=(?:absent|[0-8]) base_correct=[0-8] "
    r"verdict=(?:TARGET_MET|TARGET_MISSED) rev=[0-9a-f]{40,64}")
SUMMARY_RE = re.compile(r"MADO_LANDING_COUNTERS_SELFTEST: (\d+)/(\d+) assertions passed")


class UsageError(Exception):
    pass


class SetupError(Exception):
    pass


def dec(data):
    return data.decode("utf-8", "replace")


def emit(line):
    print(line, flush=True)


def sha256_hex(data):
    return hashlib.sha256(data).hexdigest()


def absolute_scratch(value):
    if not value:
        raise UsageError("--scratch-root is required")
    root = os.path.realpath(os.path.abspath(value))
    if not os.path.isdir(root):
        raise UsageError("--scratch-root is not a directory: %s" % value)
    if os.path.islink(os.path.abspath(value)):
        raise UsageError("--scratch-root must not be a symlink")
    for unsafe in UNSAFE_ROOTS:
        if root == unsafe or root.startswith(unsafe + os.sep):
            raise UsageError("--scratch-root under %s is refused" % unsafe)
    return root


def last_summary(out):
    for line in reversed(out.splitlines()):
        if line.startswith("MADO_LANDING_COUNTERS_SELFTEST:"):
            return line.strip()
    return ""


def expected_from_summary(out, killed):
    """The frozen predicate, restated here only to validate the frozen labels in the selftest."""
    m = SUMMARY_RE.fullmatch(last_summary(out))
    green = bool(m) and int(m.group(2)) > 0 and int(m.group(1)) == int(m.group(2))
    return "TARGET_MET" if green and killed == 2 else "TARGET_MISSED"


def load_controls(path):
    try:
        with open(path, "rb") as fh:
            blob = fh.read()
        data = json.loads(blob.decode("utf-8"))
    except (OSError, ValueError) as exc:
        raise SetupError("cannot read controls %s: %s" % (path, exc))
    cases = data.get("cases")
    if not isinstance(cases, list) or len(cases) != FROZEN_CASES:
        raise SetupError("controls must carry exactly %d cases" % FROZEN_CASES)
    ids = set()
    for case in cases:
        for key in ("id", "gate_out", "gate_rc", "killed", "expected"):
            if key not in case:
                raise SetupError("case missing %s" % key)
        if case["id"] in ids:
            raise SetupError("duplicate case id %s" % case["id"])
        ids.add(case["id"])
        if case["expected"] not in ("TARGET_MET", "TARGET_MISSED"):
            raise SetupError("case %s has an invalid expected verdict" % case["id"])
        if case["killed"] not in (0, 1, 2):
            raise SetupError("case %s has an invalid kill count" % case["id"])
    return blob, cases


def load_module(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise SetupError("cannot load %s" % path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def score(expected, got):
    return got is not None and got == expected


def verdict_met(correct, base_correct):
    return correct == FROZEN_CORRECT and base_correct == FROZEN_BASE_CORRECT


def contract_line(correct, base_correct, sha):
    return ("MADO_R72_OUTCOME: cases=8 correct=%s base_correct=%d verdict=%s rev=%s"
            % ("absent" if correct is None else str(correct), base_correct,
               "TARGET_MET" if verdict_met(correct, base_correct) else "TARGET_MISSED", sha))


def git_env():
    env = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}
    env["GIT_OPTIONAL_LOCKS"] = "0"
    env["GIT_NO_REPLACE_OBJECTS"] = "1"
    env["LC_ALL"] = "C"
    return env


def run(argv, cwd=None):
    import subprocess
    return subprocess.run(argv, cwd=cwd, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                          env=git_env(), timeout=300)


def resolve_rev(repo, rev):
    r = run(["git", "-C", repo, "rev-parse", "--verify", rev + "^{commit}"], cwd=repo)
    if r.returncode != 0:
        raise SetupError("cannot resolve %s: %s" % (rev, dec(r.stderr).strip()[:200]))
    return dec(r.stdout).strip()


def extract(repo, sha, path):
    r = run(["git", "-C", repo, "show", "%s:%s" % (sha, path)], cwd=repo)
    return r.stdout if r.returncode == 0 else None


def measure(args):
    if not args.repo or not args.rev or not args.base_rev or not args.controls:
        raise UsageError("--repo, --rev, --base-rev and --controls are required")
    repo = os.path.abspath(args.repo)
    if not os.path.isdir(repo):
        raise SetupError("--repo is not a directory: %s" % repo)
    scratch = absolute_scratch(args.scratch_root)
    work = os.path.join(scratch, "r72-c2")
    shutil.rmtree(work, ignore_errors=True)
    os.makedirs(work)
    blob, cases = load_controls(args.controls)
    emit("MADO_R72_CONTROLS path=%s cases=%d sha256=%s"
         % (os.path.abspath(args.controls), len(cases), sha256_hex(blob)))
    sha = resolve_rev(repo, args.rev)
    base_sha = resolve_rev(repo, args.base_rev)
    emit("MADO_R72_REVS rev=%s base=%s" % (sha, base_sha))

    candidate = extract(repo, sha, CANDIDATE)
    base = extract(repo, base_sha, BASE_HARNESS)
    if base is None:
        raise SetupError("%s is absent at the base revision %s" % (BASE_HARNESS, base_sha))
    if candidate is None:
        emit("MADO_R72_HARNESS role=candidate path=%s present=no" % CANDIDATE)
        emit("MADO_R72_HARNESS role=base path=%s sha256=%s" % (BASE_HARNESS, sha256_hex(base)))
        emit(contract_line(None, 0, sha))
        return 1
    cand_path = os.path.join(work, "candidate.py")
    base_path = os.path.join(work, "base.py")
    with open(cand_path, "wb") as fh:
        fh.write(candidate)
    with open(base_path, "wb") as fh:
        fh.write(base)
    emit("MADO_R72_HARNESS role=candidate path=%s present=yes sha256=%s"
         % (CANDIDATE, sha256_hex(candidate)))
    emit("MADO_R72_HARNESS role=base path=%s sha256=%s" % (BASE_HARNESS, sha256_hex(base)))
    cand = load_module(cand_path, "r72_candidate")
    held = load_module(base_path, "r71_held")

    correct = 0
    base_correct = 0
    for case in cases:
        got = cand.outcome_verdict(case["gate_out"], case["killed"])
        base_got = held.outcome_verdict(case["gate_rc"], case["killed"])
        ok = score(case["expected"], got)
        base_ok = score(case["expected"], base_got)
        correct += int(ok)
        base_correct += int(base_ok)
        emit("MADO_R72_CASE case=%s expect=%s candidate=%s base=%s correct=%s base_correct=%s"
             % (case["id"], case["expected"], got, base_got,
                "yes" if ok else "no", "yes" if base_ok else "no"))

    emit(contract_line(correct, base_correct, sha))
    return 0 if verdict_met(correct, base_correct) else 1


# --------------------------------------------------------------------------------------------- selftest
def _selftest_checks(work, lane_root):
    checks = []

    def want(name, cond):
        checks.append((name, bool(cond)))

    want("candidate path is the round-72 harness",
         CANDIDATE.endswith("c1-r72-landing-controls.py"))
    want("base path is the frozen round-71 harness",
         BASE_HARNESS.endswith("c1-r71-landing-controls.py"))

    here = os.path.dirname(os.path.abspath(__file__))
    controls = os.path.join(here, "..", "..", ".ufo", "waves", "round-72",
                            "controls", "c2-controls-r72.json")
    cases = None
    try:
        _blob, cases = load_controls(controls)
    except SetupError as exc:
        want("frozen controls load: %s" % exc, False)
    if cases is not None:
        want("frozen controls carry eight unique cases", len(cases) == 8)
        want("frozen labels match the frozen predicate",
             all(expected_from_summary(c["gate_out"], c["killed"]) == c["expected"]
                 for c in cases))
        want("frozen set keeps a green summary with a nonzero exit",
             any(c["id"] == "green-summary-exit2" for c in cases))
        want("frozen set keeps a failing summary at exit zero",
             any(c["id"] == "failing-summary-exit0" for c in cases))

    want("last summary wins", last_summary(
        "MADO_LANDING_COUNTERS_SELFTEST: 1/2 assertions passed\n"
        "MADO_LANDING_COUNTERS_SELFTEST: 2/2 assertions passed\n")
        .endswith("2/2 assertions passed"))
    want("absent summary is empty", last_summary("boom\n") == "")
    want("green needs p == n and n > 0",
         expected_from_summary("MADO_LANDING_COUNTERS_SELFTEST: 2/2 assertions passed", 2)
         == "TARGET_MET"
         and expected_from_summary("MADO_LANDING_COUNTERS_SELFTEST: 1/2 assertions passed", 2)
         == "TARGET_MISSED"
         and expected_from_summary("MADO_LANDING_COUNTERS_SELFTEST: 0/0 assertions passed", 2)
         == "TARGET_MISSED")
    want("kills still require 2/2",
         expected_from_summary("MADO_LANDING_COUNTERS_SELFTEST: 2/2 assertions passed", 1)
         == "TARGET_MISSED")
    want("score needs a verdict", not score("TARGET_MET", None))
    want("8/8 and base 4/8 is met", verdict_met(8, 4))
    want("7/8 is not met", not verdict_met(7, 4))
    want("base 5/8 is not met", not verdict_met(8, 5))

    want("contract line parses",
         CONTRACT_RE.fullmatch(contract_line(8, 4, "a" * 40)) is not None)
    want("miss line parses",
         CONTRACT_RE.fullmatch(contract_line(1, 4, "a" * 40)) is not None)
    want("absent line parses",
         CONTRACT_RE.fullmatch(contract_line(None, 0, "a" * 40)) is not None)

    green = "MADO_LANDING_COUNTERS_SELFTEST: 62/62 assertions passed"
    failed = "MADO_LANDING_COUNTERS_SELFTEST: 60/62 assertions passed"
    cand_mod = load_module(os.path.join(lane_root, CANDIDATE), "r72_candidate_selftest")
    held_mod = load_module(os.path.join(lane_root, BASE_HARNESS), "r71_held_selftest")
    want("candidate greens a green summary at exit 2 (D2)",
         cand_mod.outcome_verdict(green, 2) == "TARGET_MET")
    want("candidate reds a failing summary at exit 0 (D2)",
         cand_mod.outcome_verdict(failed, 2) == "TARGET_MISSED")
    want("candidate reds a missing summary", cand_mod.outcome_verdict("boom\n", 2) == "TARGET_MISSED")
    want("held greens the same failing-summary rc-0 shape (the defect)",
         held_mod.outcome_verdict(0, 2) == "TARGET_MET")
    want("held reds the green-summary rc-2 shape (the defect)",
         held_mod.outcome_verdict(2, 2) == "TARGET_MISSED")

    want("scratch refuses /tmp", _refuses("/tmp/whatever"))
    want("scratch refuses a symlink", _refuses_symlink(work))
    return checks


def _refuses(path):
    try:
        absolute_scratch(path)
    except UsageError:
        return True
    return False


def _refuses_symlink(work):
    target = os.path.join(work, "symlink-target")
    link = os.path.join(work, "symlink-root")
    os.makedirs(target, exist_ok=True)
    if not os.path.islink(link):
        os.symlink(target, link)
    return _refuses(link)


def selftest(work):
    lane_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    checks = _selftest_checks(work, lane_root)
    passed = sum(1 for _name, ok in checks if ok)
    for name, ok in checks:
        if not ok:
            print("MADO_R72_OUTCOME_SELFTEST FAIL: %s" % name)
    print("MADO_R72_OUTCOME_SELFTEST: %d/%d assertions passed" % (passed, len(checks)))
    return 0 if passed == len(checks) else 1


def main(argv):
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--repo")
    parser.add_argument("--rev")
    parser.add_argument("--base-rev", dest="base_rev")
    parser.add_argument("--controls")
    parser.add_argument("--scratch-root", dest="scratch_root")
    parser.add_argument("--selftest", action="store_true")
    args = parser.parse_args(argv)
    try:
        scratch = absolute_scratch(args.scratch_root)
        work = os.path.join(scratch, "r72-c2-selftest")
        if args.selftest:
            shutil.rmtree(work, ignore_errors=True)
            os.makedirs(work)
            return selftest(work)
        return measure(args)
    except UsageError as exc:
        print("%s: usage: %s" % (TOOL, exc), file=sys.stderr)
        return 2
    except SetupError as exc:
        print("%s: setup: %s" % (TOOL, exc), file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
