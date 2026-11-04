#!/usr/bin/env python3
r"""Round-73 C1 counting command: the frozen outcome set separates the four named rule mutations
(claim C1, round 73).

    python3 quality/counters/c1-r73-summary-mutants.py --repo . --rev REV \
        --base-rev d3f6c9f5d8b3401c01f189e8cd4b8dbc917a2bce \
        --controls .ufo/waves/round-73/controls/c1-outcomes-r73.json --scratch-root DIR
    python3 quality/counters/c1-r73-summary-mutants.py --selftest --scratch-root DIR

What is scored. The frozen ten-case outcome set (`.ufo/waves/round-73/controls/c1-outcomes-r73.json`)
must separate four named mutations of the committed round-72 outcome rule: each mutation's
`outcome_verdict` answer must differ from the frozen truth on at least one case. The held
round-72 eight-case set is scored the same way in the same run; the do-nothing control keeps it
and separates only two (the round-72 mutation battery's GAP-1 survivor and its selftest-only F1
repair).

The four mutations are literal substitutions of the harness bytes extracted at `--rev`; each
substitution is asserted to apply exactly once and to be the only delta:

    N1  summary_green's `total > 0 and passed == total` -> `passed == total`
        (the r72 mutation battery's M3; only `zero-denominator` separates it)
    N2  `last_parsed_summary` -> the pre-repair last-prefix-match scan
        (the r72 F1 defect; only `valid-then-garbled` separates it)
    N3  `total > 0 and passed == total` -> `total > 0 and passed <= total` (the M2 family)
    N4  `outcome_verdict` -> the kill count alone (the r72 mutation battery's M4)

Printed receipt (last line, exact):

    MADO_R73_MUTANT_KILL: cases=10 mutants=4 killed=<n> base_killed=<m> verdict=<TARGET_MET|TARGET_MISSED> rev=<sha>

Exit 0 iff cases == 10, mutants == 4, killed == 4 and base_killed == 2; 1 iff the measurement
ran and missed (an absent candidate harness prints `killed=absent`); 2 on usage/setup error with
the reason on stderr and no contract line.

Selftest: `--selftest` is hermetic - it spawns nothing, touches only <scratch-root>, checks the
frozen case structure and labels, the mutation table's applicability against a synthetic copy of
the rule functions, the scoring/verdict helpers and the contract line shape.

Declared limits: four named mutations of one rule family are not fault coverage; the sub-wait is
a bounded syntactic mutation of the committed source, not an arbitrary program mutation; the
counter scores the committed decision functions, not a harness execution; a mutation that changes
behaviour only outside these ten cases is not counted.
"""
import argparse
import hashlib
import json
import os
import re
import sys

TOOL = "c1-r73-summary-mutants.py"
CANDIDATE = "quality/counters/c1-r72-landing-controls.py"
HELD_CONTROLS = ".ufo/waves/round-72/controls/c2-controls-r72.json"
HELD_CONTROLS_SHA = "640fb44fdb1f31b4706b381c905fde4b5dae769bfd3e5b656bdb374bad58a793"
HELD_CASES = 8
FROZEN_CASES = 10
FROZEN_MUTANTS = 4
FROZEN_KILLED = 4
FROZEN_BASE_KILLED = 2
UNSAFE_ROOTS = ("/tmp", "/var/tmp", "/dev/shm")
CONTRACT_RE = re.compile(
    r"MADO_R73_MUTANT_KILL: cases=10 mutants=4 killed=(?:absent|[0-4]) base_killed=[0-4] "
    r"verdict=(?:TARGET_MET|TARGET_MISSED) rev=[0-9a-f]{40,64}")
SUMMARY_RE = re.compile(r"MADO_LANDING_COUNTERS_SELFTEST: (\d+)/(\d+) assertions passed")

MUTANTS = [
    ("N1-zero-guard-dropped",
     "    return total > 0 and passed == total\n",
     "    return passed == total\n"),
    ("N2-last-prefix-match",
     "        if re.fullmatch(r\"MADO_LANDING_COUNTERS_SELFTEST: [0-9]+/[0-9]+ assertions passed\",\n"
     "                        line.strip()):\n"
     "            return line.strip()\n",
     "        if line.startswith(\"MADO_LANDING_COUNTERS_SELFTEST:\"):\n"
     "            return line.strip()\n"),
    ("N3-pass-le-total",
     "    return total > 0 and passed == total\n",
     "    return total > 0 and passed <= total\n"),
    ("N4-kill-count-only",
     "    return \"TARGET_MET\" if summary_green(selftest_out) and killed == 2 "
     "else \"TARGET_MISSED\"\n",
     "    return \"TARGET_MET\" if killed == 2 else \"TARGET_MISSED\"\n"),
]


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


def load_module(src, name):
    ns = {"__name__": name}
    exec(compile(src, name, "exec"), ns)
    return ns


def expected_from_summary(out, killed):
    """The frozen predicate, restated here only to validate the frozen labels in the selftest."""
    for line in reversed(out.splitlines()):
        if SUMMARY_RE.fullmatch(line.strip()):
            m = SUMMARY_RE.fullmatch(line.strip())
            green = int(m.group(2)) > 0 and int(m.group(1)) == int(m.group(2))
            return "TARGET_MET" if green and killed == 2 else "TARGET_MISSED"
    return "TARGET_MISSED"


def load_controls(path):
    try:
        with open(path, "rb") as fh:
            blob = fh.read()
    except OSError as exc:
        raise SetupError("controls unreadable: %s" % exc)
    try:
        doc = json.loads(dec(blob))
        cases = doc["cases"]
    except (ValueError, KeyError) as exc:
        raise SetupError("controls unusable: %s" % exc)
    if not isinstance(cases, list) or len(cases) != FROZEN_CASES:
        raise SetupError("controls must carry exactly %d cases" % FROZEN_CASES)
    ids = set()
    for case in cases:
        if not isinstance(case, dict):
            raise SetupError("a case is not an object")
        for key in ("id", "gate_out", "gate_rc", "killed", "expected"):
            if key not in case:
                raise SetupError("a case is missing %r" % key)
        if case["expected"] not in ("TARGET_MET", "TARGET_MISSED"):
            raise SetupError("case %r has an unknown expected verdict" % case["id"])
        if case["id"] in ids:
            raise SetupError("duplicate case id %r" % case["id"])
        ids.add(case["id"])
    return cases


def score(cases, verdict_fn):
    good = 0
    misses = []
    for case in cases:
        got = verdict_fn(case["gate_out"], case["killed"])
        if got == case["expected"]:
            good += 1
        else:
            misses.append(case["id"])
    return good, misses


def git(repo, args):
    import subprocess
    return subprocess.run(["git", "-C", repo] + list(args), stdout=subprocess.PIPE,
                          stderr=subprocess.PIPE, timeout=900,
                          env={"PATH": os.environ.get("PATH", "/usr/bin:/bin"),
                               "GIT_OPTIONAL_LOCKS": "0", "LC_ALL": "C"})


def rev_parse(repo, rev):
    r = git(repo, ["rev-parse", "--verify", rev + "^{commit}"])
    if r.returncode != 0:
        raise SetupError("cannot resolve %s: %s" % (rev, dec(r.stderr).strip()[:200]))
    return dec(r.stdout).strip()


def extract(repo, sha, path):
    r = git(repo, ["show", "%s:%s" % (sha, path)])
    if r.returncode != 0:
        return None
    return dec(r.stdout)


def held_check(repo, sha, cases):
    """The round-72 control file must still hash to its frozen digest and match the held cases."""
    data = extract(repo, sha, HELD_CONTROLS)
    if data is None:
        raise SetupError("%s is absent at %s" % (HELD_CONTROLS, sha))
    digest = sha256_hex(data.encode())
    if digest != HELD_CONTROLS_SHA:
        raise SetupError("held controls sha256 %s does not match the frozen digest" % digest)
    try:
        held = json.loads(data)["cases"]
    except (ValueError, KeyError) as exc:
        raise SetupError("held controls unusable: %s" % exc)
    if len(held) != HELD_CASES:
        raise SetupError("held controls carry %d cases, frozen %d" % (len(held), HELD_CASES))
    by_id = {case["id"]: case for case in cases}
    for case in held:
        mine = by_id.get(case["id"])
        if mine is None or mine["gate_out"] != case["gate_out"] \
                or mine["gate_rc"] != case["gate_rc"] or mine["killed"] != case["killed"] \
                or mine["expected"] != case["expected"]:
            raise SetupError("held case %r is not carried forward byte-identically" % case["id"])
    emit("MADO_R73_HELD_CONTROLS path=%s cases=%d sha256=%s carried=yes"
         % (HELD_CONTROLS, len(held), digest))
    return held


def verdict_met(killed, base_killed):
    return killed == FROZEN_KILLED and base_killed == FROZEN_BASE_KILLED


def contract_line(killed, base_killed, sha):
    return ("MADO_R73_MUTANT_KILL: cases=%d mutants=%d killed=%s base_killed=%d verdict=%s rev=%s"
            % (FROZEN_CASES, FROZEN_MUTANTS, killed, base_killed,
               "TARGET_MET" if killed == FROZEN_KILLED and base_killed == FROZEN_BASE_KILLED
               else "TARGET_MISSED", sha))


def measure(args):
    repo = os.path.abspath(args.repo)
    if not os.path.isdir(repo):
        raise SetupError("--repo is not a directory: %s" % args.repo)
    scratch = absolute_scratch(args.scratch_root)
    cases = load_controls(os.path.abspath(args.controls))
    emit("MADO_R73_CONTROLS path=%s cases=%d sha256=%s"
         % (os.path.abspath(args.controls), len(cases), sha256_hex(open(
             os.path.abspath(args.controls), "rb").read())))

    sha = rev_parse(repo, args.rev)
    base_sha = rev_parse(repo, args.base_rev or args.rev)
    emit("MADO_R73_REVS rev=%s base=%s" % (sha, base_sha))
    held = held_check(repo, sha, cases)

    base_data = extract(repo, base_sha, CANDIDATE)
    if base_data is None:
        raise SetupError("the base harness %s is absent at %s" % (CANDIDATE, base_sha))
    if base_data != extract(repo, sha, CANDIDATE):
        raise SetupError("the candidate harness differs between --base-rev and --rev; the "
                         "carried comparison is not a base-rev comparison")
    base_module = load_module(base_data, "mado_r73_base")
    base_good, base_misses = score(held, base_module["outcome_verdict"])
    if base_good != len(held):
        raise SetupError("the base harness does not answer the held eight-case set "
                         "(misses=%s)" % ",".join(base_misses))
    emit("MADO_R73_BASE_PROVENANCE base=%s harness_same=yes held_set=8/8"
         % base_sha)

    data = extract(repo, sha, CANDIDATE)
    if data is None:
        emit("MADO_R73_HARNESS role=candidate path=%s present=no" % CANDIDATE)
        line = contract_line("absent", 0, sha)
        if not CONTRACT_RE.fullmatch(line):
            raise SetupError("emitted contract line does not match CONTRACT_RE")
        emit(line)
        return 1
    emit("MADO_R73_HARNESS role=candidate path=%s present=yes sha256=%s"
         % (CANDIDATE, sha256_hex(data.encode())))

    pristine = load_module(data, "mado_r73_pristine")
    good, misses = score(cases, pristine["outcome_verdict"])
    emit("MADO_R73_PRISTINE correct=%d/%d misses=%s" % (good, len(cases), ",".join(misses) or "-"))
    if good != len(cases):
        raise SetupError("the committed rule does not answer its own frozen set (misses=%s)"
                         % ",".join(misses))

    killed = base_killed = 0
    for name, old, new in MUTANTS:
        count = data.count(old)
        if count != 1:
            raise SetupError("mutation %s does not apply exactly once (count=%d)" % (name, count))
        mutated = data.replace(old, new)
        if mutated == data:
            raise SetupError("mutation %s is a no-op" % name)
        module = load_module(mutated, "mado_r73_" + name.replace("-", "_"))
        gnew, mnew = score(cases, module["outcome_verdict"])
        gheld, mheld = score(held, module["outcome_verdict"])
        kn = gnew < len(cases)
        kh = gheld < len(held)
        killed += 1 if kn else 0
        base_killed += 1 if kh else 0
        emit("MADO_R73_MUTANT mutant=%s new=%d/%d killed=%s misses=%s | held=%d/%d killed=%s "
             "misses=%s" % (name, gnew, len(cases), "yes" if kn else "NO", ",".join(mnew) or "-",
                            gheld, len(held), "yes" if kh else "NO", ",".join(mheld) or "-"))

    emit("MADO_R73_KILLED killed=%d/%d base_killed=%d/%d (the held eight-case set must separate "
         "only two)" % (killed, FROZEN_MUTANTS, base_killed, FROZEN_MUTANTS))
    line = contract_line(killed, base_killed, sha)
    if not CONTRACT_RE.fullmatch(line):
        raise SetupError("emitted contract line does not match CONTRACT_RE")
    emit(line)
    return 0 if verdict_met(killed, base_killed) else 1


# --------------------------------------------------------------------------------------------- selftest
CASES = {
    "zero-denominator": ("MADO_LANDING_COUNTERS_SELFTEST: 0/0 assertions passed", 0, 2,
                         "TARGET_MISSED"),
    "valid-then-garbled": ("MADO_LANDING_COUNTERS_SELFTEST: 12/12 assertions passed\n"
                           "MADO_LANDING_COUNTERS_SELFTEST: runner cleanup complete", 0, 2,
                           "TARGET_MET"),
    "green-summary-exit2": ("MADO_LANDING_COUNTERS_SELFTEST: 12/12 assertions passed", 2, 2,
                            "TARGET_MET"),
    "failing-summary-exit0": ("MADO_LANDING_COUNTERS_SELFTEST: 3/12 assertions passed", 0, 2,
                              "TARGET_MISSED"),
}

RULE = '''
def last_parsed_summary(out):
    for line in reversed(out.splitlines()):
        if re.fullmatch(r"MADO_LANDING_COUNTERS_SELFTEST: [0-9]+/[0-9]+ assertions passed",
                        line.strip()):
            return line.strip()
    return ""


def summary_green(out):
    line = last_parsed_summary(out)
    m = re.fullmatch(r"MADO_LANDING_COUNTERS_SELFTEST: (\\d+)/(\\d+) assertions passed", line)
    if not m:
        return False
    passed, total = int(m.group(1)), int(m.group(2))
    return total > 0 and passed == total


def outcome_verdict(selftest_out, killed):
    return "TARGET_MET" if summary_green(selftest_out) and killed == 2 else "TARGET_MISSED"
'''


def _raises(exc_type, fn):
    try:
        fn()
    except exc_type:
        return True
    except Exception:
        return False
    return False


def _selftest_checks(scratch, controls_path):
    checks = []

    def want(name, cond):
        checks.append((name, bool(cond)))

    import re as _re
    base_ns = {"re": _re, "__name__": "rule"}
    exec(compile(RULE, "rule", "exec"), base_ns)
    want("the synthetic rule greens a green summary",
         base_ns["outcome_verdict"]("MADO_LANDING_COUNTERS_SELFTEST: 12/12 assertions passed", 2)
         == "TARGET_MET")
    want("the synthetic rule refuses a zero denominator",
         base_ns["outcome_verdict"]("MADO_LANDING_COUNTERS_SELFTEST: 0/0 assertions passed", 2)
         == "TARGET_MISSED")
    want("the synthetic rule reads the last parsed summary past a malformed tail",
         base_ns["outcome_verdict"]("MADO_LANDING_COUNTERS_SELFTEST: 12/12 assertions passed\n"
                                    "MADO_LANDING_COUNTERS_SELFTEST: cleanup complete", 2)
         == "TARGET_MET")
    want("the mutation table carries four named deltas", len(MUTANTS) == 4)
    for name, old, new in MUTANTS:
        count = RULE.count(old)
        want("mutation %s applies exactly once to the synthetic rule" % name, count == 1)
        if count == 1:
            ns = {"re": _re, "__name__": name}
            exec(compile(RULE.replace(old, new), name, "exec"), ns)
            differs = any(ns["outcome_verdict"](out, killed) != base_ns["outcome_verdict"](out,
                                                                                           killed)
                          for out, _rc, killed, _exp in CASES.values())
            want("mutation %s changes at least one embedded case" % name, differs)
    want("the embedded case table carries the two new labels", set(CASES) >= {
        "zero-denominator", "valid-then-garbled"})
    want("the embedded labels agree with the frozen predicate",
         all(expected_from_summary(out, killed) == expected
             for out, _rc, killed, expected in CASES.values()))
    want("verdict met on the frozen target", verdict_met(4, 2))
    want("verdict refuses a held-set kill of four", not verdict_met(4, 3))
    want("verdict refuses a weak new set", not verdict_met(3, 2))
    good = contract_line(4, 2, "a" * 40)
    want("the frozen target prints the met line",
         good == ("MADO_R73_MUTANT_KILL: cases=10 mutants=4 killed=4 base_killed=2 "
                  "verdict=TARGET_MET rev=" + "a" * 40))
    want("the target line matches the frozen contract shape",
         CONTRACT_RE.fullmatch(good) is not None)
    want("contract line refuses a wrong verdict word",
         not CONTRACT_RE.fullmatch(
             "MADO_R73_MUTANT_KILL: cases=10 mutants=4 killed=4 base_killed=2 "
             "verdict=DONE rev=" + "a" * 40))
    frozen = ["--repo", ".", "--rev", "HEAD", "--base-rev", "BASE",
              "--controls", "cases.json", "--scratch-root", "/scratch/dir"]
    try:
        parsed = build_parser().parse_args(frozen)
        parsed_ok = (parsed.scratch_root == "/scratch/dir" and parsed.controls == "cases.json"
                     and parsed.base_rev == "BASE" and parsed.rev == "HEAD")
    except SystemExit:
        parsed_ok = False
    want("the frozen counting command's argument set parses", parsed_ok)
    want("the usage example names --controls", "--controls" in (__doc__ or ""))
    if controls_path:
        try:
            cases = load_controls(os.path.abspath(controls_path))
            want("the frozen controls file carries 10 cases", len(cases) == 10)
        except SetupError:
            want("the frozen controls file carries 10 cases", False)
    os.makedirs(scratch, exist_ok=True)
    tampered = os.path.join(scratch, "cases-tampered.json")
    with open(tampered, "w", encoding="utf-8") as fh:
        fh.write(json.dumps({"cases": []}))
    want("a controls file with the wrong case count is refused",
         _raises(SetupError, lambda: load_controls(tampered)))
    return checks


def selftest(scratch, controls_path):
    """Hermetic: every subprocess spawn raises, so the check body must stay pure."""
    import subprocess
    saved_run = subprocess.run

    def _no_spawn(*_args, **_kwargs):
        raise AssertionError("selftest must not spawn a process")

    subprocess.run = _no_spawn
    try:
        checks = [("the hermetic spawn guard is installed for the check body",
                   subprocess.run is _no_spawn)]
        checks.append(("an attempted spawn under the guard raises",
                       _raises(AssertionError, lambda: subprocess.run(["/bin/true"]))))
        try:
            checks.extend(_selftest_checks(scratch, controls_path))
        except AssertionError:
            checks.append(("selftest body must not spawn a process", False))
    finally:
        subprocess.run = saved_run
    passed = sum(1 for _name, ok in checks if ok)
    for name, ok in checks:
        if not ok:
            print("MADO_R73_MUTANT_KILL_SELFTEST FAIL: %s" % name)
    print("MADO_R73_MUTANT_KILL_SELFTEST: %d/%d assertions passed" % (passed, len(checks)))
    return 0 if passed == len(checks) else 1


# --------------------------------------------------------------------------------------------- cli
def build_parser():
    parser = argparse.ArgumentParser(prog=TOOL, description=__doc__.splitlines()[0])
    parser.add_argument("--repo")
    parser.add_argument("--rev")
    parser.add_argument("--base-rev", default=None)
    parser.add_argument("--controls")
    parser.add_argument("--scratch-root")
    parser.add_argument("--selftest", action="store_true")
    return parser


def main(argv):
    args = build_parser().parse_args(argv)
    try:
        scratch = absolute_scratch(args.scratch_root)
        if args.selftest:
            return selftest(scratch, args.controls)
        if not args.repo or not args.rev or not args.controls:
            raise UsageError("--repo, --rev and --controls are required")
        return measure(args)
    except UsageError as exc:
        sys.stderr.write("%s: %s\n" % (TOOL, exc))
        return 2
    except SetupError as exc:
        sys.stderr.write("%s: %s\n" % (TOOL, exc))
        return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
