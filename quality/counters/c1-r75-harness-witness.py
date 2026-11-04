#!/usr/bin/env python3
r"""Round-75 C1 counting command: the successor harness credits the M-Z kill only on the run's
own echo of its per-run challenge (claim C1, round 75).

    python3 quality/counters/c1-r75-harness-witness.py --repo . --rev REV \
        --base-rev bd5a971532f37df85a78f6f566dd1e649b79de11 \
        --controls .ufo/waves/round-75/controls/c1-harness-cases-r75.json --scratch-root DIR
    python3 quality/counters/c1-r75-harness-witness.py --selftest --scratch-root DIR

What is scored. Eleven REAL `bash` fixture lanes, one per frozen mode, each committed into its
own scratch git fixture whose `quality/landing-counters.sh` is the mode-driven test double; the
fixture carries the real `c3-r56-used-by.py`, `check-tool-ledger.py`,
`mado-receipt-citecheck.py` and the frozen `c1-r72-landing-controls.py` bytes at --rev. Each
fixture is measured twice, as a child process, by the actual harness pipeline (extraction,
instrument selftest, M-Z zero-citation clause deletion, credit decision):

  candidate  `c1-r75-landing-controls.py` at --rev: it draws one fresh
             `secrets.token_hex(8)` per run, hands it to the child in `MADO_LANDING_NONCE`
             and credits the M-Z kill only when the child's last parsed
             `MADO_LANDING_WITNESS: <16 hex>` line equals that challenge;
  base       the frozen round-72 harness at --base-rev: arithmetic only, so it credits every
             replay whose detail lines add up.

The frozen expectation labels the modes: only `right` and `liar-success` credit the kill (the
exit status is not read, the echo is). The do-nothing control must score exactly 6/11; the
candidate must score 11/11.

Printed receipt (last line, exact):

    MADO_R75_HARNESS_WITNESS: cases=11 correct=<n> base_correct=<m> verdict=<TARGET_MET|TARGET_MISSED> rev=<sha>

Exit 0 iff cases == 11, correct == 11 and base_correct == 6; 1 iff the measurement ran and
missed (an absent candidate harness prints `correct=absent`); 2 on usage/setup error with the
reason on stderr and no contract line.

Selftest: `--selftest` is hermetic - it spawns nothing, touches only <scratch-root>, and checks
the fixture template (one frozen zero-citation clause, one mode placeholder, `marker_valid`
present), the eleven frozen modes and labels, the contract shape and the scratch refusals.

Declared limits: the fixture lanes are test doubles, not the production instrument; the r72
harness is scored through the same fixture so both legs see identical children; the challenge
authenticates the echo, not the truth of the assertions; the eleven modes are rule separators,
not fault coverage.
"""
import argparse
import json
import hashlib
import os
import re
import shutil
import subprocess
import sys

TOOL = "c1-r75-harness-witness.py"
CAND = "quality/counters/c1-r75-landing-controls.py"
BASE = "quality/counters/c1-r72-landing-controls.py"
R72 = "quality/counters/c1-r72-landing-controls.py"
USEDBY = "quality/counters/c3-r56-used-by.py"
LEDGER = "quality/check-tool-ledger.py"
CITECHECK = "tools/mado-receipt-citecheck.py"
FROZEN_CASES = 11
FROZEN_CORRECT = 11
FROZEN_BASE_CORRECT = 6
CONTROLS_SHA = "f1e851a9d6133b44f6d538e97c8448bbeb174dcb5ba0a6906fe962ed3e8a6c31"
UNSAFE_ROOTS = ("/tmp", "/var/tmp", "/dev/shm")
Z_CLAUSE = b'[ "$citations" -gt 0 ] && '
CAND_RE = re.compile(
    r"MADO_R75_LANDING_CONTROLS: selftest=(?:[0-9]+/[0-9]+|none) mz=(pass|fail) mr=(?:pass|fail) "
    r"killed=[0-2]/2 baseline=0/2 witness=(?:ok|absent|mismatch) "
    r"verdict=(?:TARGET_MET|TARGET_MISSED) rev=[0-9a-f]{40,64}")
BASE_RE = re.compile(
    r"MADO_R72_LANDING_CONTROLS: selftest=(?:[0-9]+/[0-9]+|none) mz=(pass|fail) mr=(?:pass|fail) "
    r"killed=[0-2]/2 baseline=0/2 verdict=(?:TARGET_MET|TARGET_MISSED) rev=[0-9a-f]{40,64}")
CONTRACT_RE = re.compile(
    r"MADO_R75_HARNESS_WITNESS: cases=11 correct=(?:absent|[0-9]{1,2}) base_correct=[0-9]{1,2} "
    r"verdict=(?:TARGET_MET|TARGET_MISSED) rev=[0-9a-f]{40,64}")

LANE_TEMPLATE = """#!/usr/bin/env bash
# round-75 harness-witness fixture lane - a test double, not a production instrument
set -u
MODE=@MODE@

marker_valid() {
  local citations=0 resolved=0 missing=0 rc=0
  [ "$citations" -gt 0 ] && [ "$citations" -eq "$((resolved+missing))" ] || return 1
  if [ "$rc" -eq 0 ]; then [ "$missing" -eq 0 ]; else [ "$missing" -gt 0 ]; fi
}

witness_echo() {
  local nonce=${MADO_LANDING_NONCE:-}
  case "$MODE" in
    right|liar-success|green-mutant|zero-denominator|mismatch-detail)
      [ -n "$nonce" ] && printf 'MADO_LANDING_WITNESS: %s\\n' "$nonce" ;;
    uppercase)
      [ -n "$nonce" ] && printf 'MADO_LANDING_WITNESS: %s\\n' "$(printf '%s' "$nonce" | tr 'a-f' 'A-F')" ;;
    stale) printf 'MADO_LANDING_WITNESS: 0123456789abcdef\\n' ;;
    wrong) printf 'MADO_LANDING_WITNESS: ffffffffffffffff\\n' ;;
    absent) : ;;
    last-wrong)
      [ -n "$nonce" ] && printf 'MADO_LANDING_WITNESS: %s\\n' "$nonce"
      printf 'MADO_LANDING_WITNESS: 0123456789abcdef\\n' ;;
    *) : ;;
  esac
}

report() {
  case "$MODE" in
    crash) exit 1 ;;
    green-mutant) printf 'MADO_LANDING_COUNTERS_SELFTEST: 2/2 assertions passed\\n' ;;
    zero-denominator) printf 'MADO_LANDING_COUNTERS_SELFTEST: 0/0 assertions passed\\n' ;;
    mismatch-detail)
      printf 'SELFTEST FAIL 1: detail line one\\n'
      printf 'SELFTEST FAIL 2: detail line two\\n'
      printf 'MADO_LANDING_COUNTERS_SELFTEST: 1/2 assertions passed\\n' ;;
    *)
      if marker_valid; then
        printf 'SELFTEST FAIL 1: citecheck zero citations refused (marker accepted)\\n'
        printf 'MADO_LANDING_COUNTERS_SELFTEST: 1/2 assertions passed\\n'
      else
        printf 'MADO_LANDING_COUNTERS_SELFTEST: 2/2 assertions passed\\n'
      fi ;;
  esac
  witness_echo
  exit 0
}
report
"""


class UsageError(Exception):
    pass


class SetupError(Exception):
    pass


def dec(data):
    return data.decode("utf-8", "replace")


def sha256_hex(data):
    return hashlib.sha256(data).hexdigest()


def absolute_scratch(root):
    if not root:
        raise UsageError("--scratch-root is required")
    path = os.path.normpath(root if os.path.isabs(root) else os.path.join(os.getcwd(), root))
    probe = path
    while True:
        if os.path.islink(probe):
            raise UsageError("scratch root contains a symlink component: %s" % probe)
        parent = os.path.dirname(probe)
        if parent == probe:
            break
        probe = parent
    real = os.path.realpath(path)
    for bad in UNSAFE_ROOTS:
        if real == bad or real.startswith(bad + "/"):
            raise UsageError("unsafe scratch root (tmp-family): %s" % path)
    if real == "/":
        raise UsageError("unsafe scratch root (filesystem root)")
    if os.path.exists(path) and not os.path.isdir(path):
        raise UsageError("scratch root is not a directory: %s" % path)
    return path


def child_env(home):
    return {
        "PATH": os.environ.get("PATH", "/usr/bin:/bin"),
        "HOME": home,
        "TMPDIR": home,
        "LC_ALL": "C",
        "GIT_CONFIG_NOSYSTEM": "1",
        "GIT_CONFIG_GLOBAL": os.devnull,
        "GIT_CONFIG_SYSTEM": os.devnull,
        "GIT_TERMINAL_PROMPT": "0",
        "GIT_OPTIONAL_LOCKS": "0",
    }


def git_env(home):
    env = child_env(home)
    env["GIT_NO_REPLACE_OBJECTS"] = "1"
    return env


def run(argv, env, cwd=None, timeout=900):
    return subprocess.run(argv, cwd=cwd, env=env, stdout=subprocess.PIPE,
                          stderr=subprocess.PIPE, timeout=timeout)


def git(repo, args, env):
    return run(["git", "-C", repo] + list(args), env, cwd=repo)


def resolve_rev(repo, rev, env):
    r = git(repo, ["rev-parse", "--verify", rev + "^{commit}"], env)
    if r.returncode != 0:
        raise SetupError("cannot resolve %s: %s" % (rev, dec(r.stderr).strip()[:200]))
    return dec(r.stdout).strip()


def extract(repo, sha, path, env):
    r = git(repo, ["show", "%s:%s" % (sha, path)], env)
    if r.returncode != 0:
        raise SetupError("%s is absent at %s" % (path, sha))
    return r.stdout


def parse_decision(out, rx):
    for line in reversed(out.splitlines()):
        m = rx.fullmatch(line.strip())
        if m:
            return m.group(1)
    return None


def make_fixture(work, case, lane_files, env):
    root = os.path.join(work, "fixtures", case["name"])
    os.makedirs(root)
    for rel, data in lane_files.items():
        path = os.path.join(root, rel)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "wb") as fh:
            fh.write(data)
    lane = os.path.join(root, "quality/landing-counters.sh")
    with open(lane, "w", encoding="utf-8") as fh:
        fh.write(LANE_TEMPLATE.replace("@MODE@", case["mode"]))
    r = git(root, ["init", "-q"], env)
    if r.returncode != 0:
        raise SetupError("fixture git init failed: %s" % dec(r.stderr)[:200])
    top = git(root, ["rev-parse", "--show-toplevel"], env)
    if top.returncode != 0 or os.path.realpath(dec(top.stdout).strip()) != os.path.realpath(root):
        raise SetupError("fixture toplevel mismatch for %s" % case["name"])
    r = git(root, ["add", "-A"], env)
    if r.returncode != 0:
        raise SetupError("fixture git add failed: %s" % dec(r.stderr)[:200])
    r = git(root, ["-c", "user.name=mado-r75-fixture", "-c", "user.email=fixture@example.invalid",
                   "-c", "commit.gpgsign=false", "commit", "-qm", "fixture"], env)
    if r.returncode != 0:
        raise SetupError("fixture commit failed: %s" % dec(r.stderr)[:200])
    return root


def harness_run(harness, repo, scratch, env):
    return run([sys.executable, "-I", harness, "--repo", repo, "--rev", "HEAD",
                "--scratch-root", scratch], env)


def measure(args):
    scratch = absolute_scratch(args.scratch_root)
    if not args.repo or not args.rev or not args.base_rev or not args.controls:
        raise UsageError("--repo, --rev, --base-rev and --controls are required")
    repo = os.path.abspath(args.repo)
    if not os.path.isdir(repo):
        raise SetupError("--repo is not a directory: %s" % args.repo)
    work = os.path.join(scratch, "r75-c1")
    shutil.rmtree(work, ignore_errors=True)
    os.makedirs(work)
    home = os.path.join(work, "home")
    os.makedirs(home)
    env = git_env(home)

    raw = open(os.path.abspath(args.controls), "rb").read()
    if sha256_hex(raw) != CONTROLS_SHA:
        raise SetupError("controls sha256 %s does not match the frozen digest"
                         % sha256_hex(raw))
    try:
        cases = json.loads(dec(raw))["cases"]
    except (ValueError, KeyError) as exc:
        raise SetupError("controls file unusable: %s" % exc)
    if len(cases) != FROZEN_CASES:
        raise SetupError("controls file carries %d cases, frozen %d"
                         % (len(cases), FROZEN_CASES))
    print("MADO_R75_CONTROLS path=%s cases=%d sha256=%s"
          % (os.path.abspath(args.controls), len(cases), CONTROLS_SHA), flush=True)

    sha = resolve_rev(repo, args.rev, env)
    base_sha = resolve_rev(repo, args.base_rev, env)
    # The frozen contract promises a measured miss, not a setup error, when the candidate
    # harness is absent (R75RevC1 P2): an absent candidate prints `correct=absent`, rc 1.
    r = git(repo, ["show", "%s:%s" % (sha, CAND)], env)
    cand_bytes = r.stdout if r.returncode == 0 else None
    base_bytes = extract(repo, base_sha, BASE, env)
    lane_files = {path: extract(repo, sha, path, env)
                  for path in (USEDBY, LEDGER, CITECHECK, R72)}
    print("MADO_R75_HARNESS path=%s sha256=%s rev=%s"
          % (CAND, sha256_hex(cand_bytes) if cand_bytes is not None else "absent", sha),
          flush=True)
    print("MADO_R75_BASE_HARNESS path=%s sha256=%s rev=%s"
          % (BASE, sha256_hex(base_bytes), base_sha), flush=True)
    cand_path = os.path.join(work, "candidate.py") if cand_bytes is not None else None
    base_path = os.path.join(work, "base.py")
    if cand_path is not None:
        with open(cand_path, "wb") as fh:
            fh.write(cand_bytes)
    with open(base_path, "wb") as fh:
        fh.write(base_bytes)

    correct = base_correct = 0
    for case in cases:
        fixture = make_fixture(work, case, lane_files, env)
        if cand_path is not None:
            cand = harness_run(cand_path, fixture, os.path.join(work, "cand", case["name"]), env)
            cand_out = dec(cand.stdout) + dec(cand.stderr)
        else:
            cand_out = ""
        base = harness_run(base_path, fixture, os.path.join(work, "base", case["name"]), env)
        base_out = dec(base.stdout) + dec(base.stderr)
        cand_decision = parse_decision(cand_out, CAND_RE)
        base_decision = parse_decision(base_out, BASE_RE)
        want = "pass" if case["expect_kill"] else "fail"
        ok_cand = cand_decision == want
        ok_base = base_decision == want
        correct += int(ok_cand)
        base_correct += int(ok_base)
        print("MADO_R75_CASE name=%s mode=%s expect=%s candidate=%s base=%s correct=%s"
              % (case["name"], case["mode"], want,
                 cand_decision if cand_decision else "absent",
                 base_decision if base_decision else "absent",
                 "yes" if ok_cand else "no"), flush=True)
    correct_field = "absent" if cand_path is None else str(correct)
    line = ("MADO_R75_HARNESS_WITNESS: cases=%d correct=%s base_correct=%d verdict=%s rev=%s"
            % (len(cases), correct_field, base_correct,
               "TARGET_MET" if (len(cases) == FROZEN_CASES and correct == FROZEN_CORRECT
                                and base_correct == FROZEN_BASE_CORRECT) else "TARGET_MISSED",
               sha))
    if not CONTRACT_RE.fullmatch(line):
        raise SetupError("emitted contract line does not match CONTRACT_RE")
    print(line, flush=True)
    return 0 if (len(cases) == FROZEN_CASES and correct == FROZEN_CORRECT
                 and base_correct == FROZEN_BASE_CORRECT) else 1


# --------------------------------------------------------------------------------------------- selftest
def selftest(scratch):
    checks = []

    def want(name, cond):
        checks.append((name, bool(cond)))

    want("the fixture template carries the frozen clause exactly once",
         LANE_TEMPLATE.encode().count(Z_CLAUSE) == 1)
    want("the fixture template has one mode placeholder", LANE_TEMPLATE.count("@MODE@") == 1)
    want("the fixture template keeps the marker_valid contract",
         "marker_valid() {" in LANE_TEMPLATE and "witness_echo()" in LANE_TEMPLATE)
    want("every template line is quoted safely",
         '"@MODE@"' not in LANE_TEMPLATE and LANE_TEMPLATE.endswith("report\n"))

    modes = ["right", "liar-success", "uppercase", "stale", "absent", "wrong", "last-wrong",
             "crash", "zero-denominator", "mismatch-detail", "green-mutant"]
    want("the frozen mode list is the eleven separators",
         all(m in LANE_TEMPLATE for m in modes) and len(modes) == 11)
    want("the case count is eleven", FROZEN_CASES == 11)
    want("only the two genuine modes are labelled a credit", FROZEN_CORRECT == 11
         and FROZEN_BASE_CORRECT == 6)
    good = ("MADO_R75_HARNESS_WITNESS: cases=11 correct=11 base_correct=6 verdict=TARGET_MET "
            "rev=" + "a" * 40)
    want("the contract shape accepts the met line", CONTRACT_RE.fullmatch(good) is not None)
    want("the contract shape accepts an absent candidate",
         CONTRACT_RE.fullmatch(good.replace("correct=11", "correct=absent")) is not None)
    want("the contract shape refuses a wrong verdict word",
         CONTRACT_RE.fullmatch(good.replace("TARGET_MET", "DONE")) is None)
    want("the candidate contract row carries mz", CAND_RE.fullmatch(
        "MADO_R75_LANDING_CONTROLS: selftest=1/2 mz=pass mr=pass killed=2/2 baseline=0/2 "
        "witness=ok verdict=TARGET_MET rev=" + "a" * 40) is not None)
    want("the base contract row carries mz", BASE_RE.fullmatch(
        "MADO_R72_LANDING_CONTROLS: selftest=1/2 mz=fail mr=pass killed=1/2 baseline=0/2 "
        "verdict=TARGET_MISSED rev=" + "a" * 40) is not None)
    want("decision parsing takes the last parsed row",
         parse_decision("MADO_R72_LANDING_CONTROLS: x mz=fail y\n"
                        "MADO_R72_LANDING_CONTROLS: selftest=none mz=pass mr=fail killed=0/2 "
                        "baseline=0/2 verdict=TARGET_MISSED rev=" + "b" * 40, BASE_RE) == "pass")

    for bad in ("/tmp/x", "/var/tmp/x", "/dev/shm/x"):
        try:
            absolute_scratch(bad)
            refused = False
        except UsageError:
            refused = True
        want("scratch refuses %s" % bad, refused)
    os.makedirs(scratch, exist_ok=True)
    link = os.path.join(scratch, "link-scratch")
    try:
        os.symlink(scratch, link)
    except FileExistsError:
        pass
    try:
        absolute_scratch(os.path.join(link, "child"))
        refused = False
    except UsageError:
        refused = True
    want("scratch refuses a symlinked component", refused)

    passed = sum(1 for _n, ok in checks if ok)
    for name, ok in checks:
        if not ok:
            print("MADO_R75_HARNESS_WITNESS_SELFTEST FAIL: %s" % name)
    print("MADO_R75_HARNESS_WITNESS_SELFTEST: %d/%d assertions passed" % (passed, len(checks)))
    return 0 if passed == len(checks) else 1


# --------------------------------------------------------------------------------------------- cli
def build_parser():
    parser = argparse.ArgumentParser(prog=TOOL, description=__doc__.splitlines()[0])
    parser.add_argument("--repo")
    parser.add_argument("--rev")
    parser.add_argument("--base-rev", dest="base_rev", default=None)
    parser.add_argument("--controls")
    parser.add_argument("--scratch-root", dest="scratch_root")
    parser.add_argument("--selftest", action="store_true")
    return parser


def main(argv):
    args = build_parser().parse_args(argv)
    try:
        scratch = absolute_scratch(args.scratch_root)
        if args.selftest:
            return selftest(scratch)
        return measure(args)
    except UsageError as exc:
        sys.stderr.write("%s: %s\n" % (TOOL, exc))
        return 2
    except SetupError as exc:
        sys.stderr.write("%s: %s\n" % (TOOL, exc))
        return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
