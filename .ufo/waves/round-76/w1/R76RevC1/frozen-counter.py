#!/usr/bin/env python3
r"""Round-76 C1 counting command: the successor counter certifies the contract outcome field,
not only the M-Z kill decision (claim C1, round 76).

    python3 quality/counters/c1-r76-outcome-field.py --repo . --rev REV \
        --base-rev c3e0bc5f10b72964d54d18dc9b0706dc308dd1bf \
        --controls .ufo/waves/round-76/controls/c1-outcome-cases-r76.json --scratch-root DIR
    python3 quality/counters/c1-r76-outcome-field.py --selftest --scratch-root DIR

What is scored. Fifteen REAL `bash` fixture lanes, one per frozen mode, each committed into its
own scratch git fixture whose `quality/landing-counters.sh` is the mode-driven test double; the
fixture carries the real `c3-r56-used-by.py`, `check-tool-ledger.py`,
`mado-receipt-citecheck.py` and the frozen `c1-r72-landing-controls.py` bytes at --rev. The
candidate harness `quality/counters/c1-r76-landing-controls.py` is run on every fixture through
the actual pipeline (extraction, instrument selftest, M-Z zero-citation clause deletion, M-R
replacement-ref pair, credit and outcome decisions).

Two fields are scored per case against the frozen expectation:

  mz       the M-Z kill decision (what the held round-75 counter scores);
  verdict  the contract outcome (the field the held counter never reads).

Four named mutations of the outcome rule are then applied to the candidate harness bytes at
unique anchors and each mutated harness is scored on the same fifteen cases:

  outcome-term-dropped   the outcome ignores the challenge echo (round-75's surviving C1-M2)
  prefix-match           the echo comparison becomes a prefix test (needs the widened grammar)
  first-witness-wins     the first parsed echo wins instead of the last
  case-insensitive       the echo comparison folds case (needs the case-changing challenge)

A mutant is killed iff its two-field score is below fifteen. The held scoring rule reads `mz=`
only, so every mutant's mz score stays fifteen and `base_killed` is zero: the control cannot
reach the target.

Printed receipt (last line, exact):

    MADO_R76_OUTCOME_FIELD: cases=15 correct=15 mutants=4 killed=4 base_killed=0 verdict=<TARGET_MET|TARGET_MISSED> rev=<sha>

Exit 0 iff cases == 15, correct == 15, mutants == 4, killed == 4 and base_killed == 0; 1 iff the
measurement ran and missed (an absent candidate prints `correct=absent`); 2 on usage/setup error
with the reason on stderr and no contract line.

Selftest: `--selftest` is hermetic - it spawns nothing, touches only <scratch-root>, and checks
the fixture template (one frozen zero-citation clause, one mode placeholder, `marker_valid`
present), the sixteen frozen cases and both expectation columns, the four mutant anchors (each
exactly once in the frozen rule snippet), the contract shape and the scratch refusals.

Declared limits: the fixture lanes are test doubles, not the production instrument; the mutants
patch the outcome helper only (the kill path is not mutated, which is the point of
`base_killed=0`); the challenge authenticates the echo, not the truth of the assertions; the
fifteen modes are rule separators, not fault coverage.
"""
import argparse
import json
import hashlib
import os
import re
import shutil
import subprocess
import sys

TOOL = "c1-r76-outcome-field.py"
CAND = "quality/counters/c1-r76-landing-controls.py"
R72 = "quality/counters/c1-r72-landing-controls.py"
USEDBY = "quality/counters/c3-r56-used-by.py"
LEDGER = "quality/check-tool-ledger.py"
CITECHECK = "tools/mado-receipt-citecheck.py"
FROZEN_CASES = 16
FROZEN_CORRECT = 16
FROZEN_MUTANTS = 4
FROZEN_KILLED = 4
FROZEN_BASE_KILLED = 0
CONTROLS_SHA = "320f7e6b54e71776f2d5b179b9a8b09ee9185886e2aeb045af0ecc9171cc77ea"
UNSAFE_ROOTS = ("/tmp", "/var/tmp", "/dev/shm")
Z_CLAUSE = b'[ "$citations" -gt 0 ] && '
RULE_SNIPPET = '''def outcome_green(r72_green, selftest_out, nonce, killed):
    return bool(green_with_witness(r72_green, selftest_out, nonce)) and killed == 2
'''
MUTANTS = (
    ("outcome-summary-only",
     "    return bool(green_with_witness(r72_green, selftest_out, nonce)) and killed == 2\n",
     "    return bool(green_with_witness(r72_green, selftest_out, nonce))\n"),
    ("outcome-killed-only",
     "    return bool(green_with_witness(r72_green, selftest_out, nonce)) and killed == 2\n",
     "    return killed == 2\n"),
    ("outcome-killed-any",
     "    return bool(green_with_witness(r72_green, selftest_out, nonce)) and killed == 2\n",
     "    return bool(green_with_witness(r72_green, selftest_out, nonce)) and killed >= 1\n"),
    ("outcome-killed-or",
     "    return bool(green_with_witness(r72_green, selftest_out, nonce)) and killed == 2\n",
     "    return bool(green_with_witness(r72_green, selftest_out, nonce)) or killed == 2\n"),
)
CAND_RE = re.compile(
    r"MADO_R76_LANDING_CONTROLS: selftest=(?:[0-9]+/[0-9]+|none) mz=(pass|fail) mr=(?:pass|fail) "
    r"killed=[0-2]/2 baseline=0/2 witness=(?:ok|absent|mismatch) "
    r"verdict=(TARGET_MET|TARGET_MISSED) rev=[0-9a-f]{40,64}")
CONTROLS_LINE = re.compile(r"MADO_R76_CHALLENGE source=[^\n]* has_letter=yes ")
CONTRACT_RE = re.compile(
    r"MADO_R76_OUTCOME_FIELD: cases=16 correct=(?:absent|[0-9]{1,2}) mutants=[0-9]{1,2} "
    r"killed=[0-9]{1,2} base_killed=[0-9]{1,2} "
    r"verdict=(?:TARGET_MET|TARGET_MISSED) rev=[0-9a-f]{40,64}")

LANE_TEMPLATE = """#!/usr/bin/env bash
# round-76 outcome-field fixture lane - a test double, not a production instrument
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
    green-overlong|overlong)
      [ -n "$nonce" ] && printf 'MADO_LANDING_WITNESS: %s00\\n' "$nonce" ;;
    green-last-wrong)
      [ -n "$nonce" ] && printf 'MADO_LANDING_WITNESS: %s\\n' "$nonce"
      printf 'MADO_LANDING_WITNESS: 0123456789abcdef\\n' ;;
    uppercase|green-uppercase)
      [ -n "$nonce" ] && printf 'MADO_LANDING_WITNESS: %s\\n' "$(printf '%s' "$nonce" | tr 'a-f' 'A-F')" ;;
    right|liar-success|always-red|green-mutant|zero-denominator|mismatch-detail)
      [ -n "$nonce" ] && printf 'MADO_LANDING_WITNESS: %s\\n' "$nonce" ;;
    stale) printf 'MADO_LANDING_WITNESS: 0123456789abcdef\\n' ;;
    wrong) printf 'MADO_LANDING_WITNESS: ffffffffffffffff\\n' ;;
    last-wrong)
      [ -n "$nonce" ] && printf 'MADO_LANDING_WITNESS: %s\\n' "$nonce"
      printf 'MADO_LANDING_WITNESS: 0123456789abcdef\\n' ;;
    *) : ;;
  esac
}

report() {
  case "$MODE" in
    crash) exit 1 ;;
    green-mutant|green-absent|green-overlong|green-last-wrong|green-uppercase)
      printf 'MADO_LANDING_COUNTERS_SELFTEST: 2/2 assertions passed\\n' ;;
    always-red)
      printf 'SELFTEST FAIL 1: the frozen arithmetic always reports this failure\\n'
      printf 'MADO_LANDING_COUNTERS_SELFTEST: 1/2 assertions passed\\n' ;;
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


def parse_row(out):
    """The last parsed successor contract row as (mz, verdict) with verdict MET -> pass."""
    for line in reversed(out.splitlines()):
        m = CAND_RE.fullmatch(line.strip())
        if m:
            return m.group(1), ("pass" if m.group(2) == "TARGET_MET" else "fail")
    return None, None


def has_case_changing_challenge(out):
    for line in out.splitlines():
        if CONTROLS_LINE.match(line.strip()):
            return True
    return False


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
    r = git(root, ["-c", "user.name=mado-r76-fixture", "-c", "user.email=fixture@example.invalid",
                   "-c", "commit.gpgsign=false", "commit", "-qm", "fixture"], env)
    if r.returncode != 0:
        raise SetupError("fixture commit failed: %s" % dec(r.stderr)[:200])
    return root


def harness_run(harness, repo, scratch, env):
    return run([sys.executable, "-I", harness, "--repo", repo, "--rev", "HEAD",
                "--scratch-root", scratch], env)


def apply_mutants(source):
    """Return (name, patched_source) pairs; every anchor must occur exactly once."""
    text = source.decode("utf-8")
    out = []
    for name, old, new in MUTANTS:
        count = text.count(old)
        if count != 1:
            raise SetupError("mutant %s anchor occurs %d times, frozen rule needs exactly one"
                             % (name, count))
        patched = text.replace(old, new, 1)
        if patched == text:
            raise SetupError("mutant %s did not change the source" % name)
        try:
            compile(patched, "<mutant-%s>" % name, "exec")
        except SyntaxError as exc:
            raise SetupError("mutant %s does not compile: %s" % (name, exc))
        out.append((name, patched.encode("utf-8")))
    return out


def measure(args):
    scratch = absolute_scratch(args.scratch_root)
    if not args.repo or not args.rev or not args.base_rev or not args.controls:
        raise UsageError("--repo, --rev, --base-rev and --controls are required")
    repo = os.path.abspath(args.repo)
    if not os.path.isdir(repo):
        raise SetupError("--repo is not a directory: %s" % args.repo)
    work = os.path.join(scratch, "r76-c1")
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
    if len(MUTANTS) != FROZEN_MUTANTS:
        raise SetupError("mutant table carries %d entries, frozen %d"
                         % (len(MUTANTS), FROZEN_MUTANTS))
    print("MADO_R76_CONTROLS path=%s cases=%d sha256=%s"
          % (os.path.abspath(args.controls), len(cases), CONTROLS_SHA), flush=True)

    sha = resolve_rev(repo, args.rev, env)
    base_sha = resolve_rev(repo, args.base_rev, env)
    r = git(repo, ["show", "%s:%s" % (sha, CAND)], env)
    cand_bytes = r.stdout if r.returncode == 0 else None
    lane_files = {path: extract(repo, sha, path, env)
                  for path in (USEDBY, LEDGER, CITECHECK, R72)}
    print("MADO_R76_HARNESS path=%s sha256=%s rev=%s"
          % (CAND, sha256_hex(cand_bytes) if cand_bytes is not None else "absent", sha),
          flush=True)
    if cand_bytes is None:
        print("MADO_R76_OUTCOME_FIELD: cases=%d correct=absent mutants=%d killed=0 base_killed=0 "
              "verdict=TARGET_MISSED rev=%s" % (len(cases), len(MUTANTS), sha), flush=True)
        return 1
    cand_path = os.path.join(work, "candidate.py")
    with open(cand_path, "wb") as fh:
        fh.write(cand_bytes)

    correct = 0
    challenge_ok = True
    for case in cases:
        fixture = make_fixture(work, case, lane_files, env)
        out = dec(harness_run(cand_path, fixture, os.path.join(work, "cand", case["name"]),
                              env).stdout)
        got_mz, got_verdict = parse_row(out)
        letter = has_case_changing_challenge(out)
        challenge_ok = challenge_ok and letter
        ok = (got_mz == case["expect_mz"] and got_verdict == case["expect_verdict"])
        correct += int(ok)
        print("MADO_R76_CASE name=%s mode=%s expect_mz=%s expect_verdict=%s candidate_mz=%s "
              "candidate_verdict=%s challenge=%s correct=%s"
              % (case["name"], case["mode"], case["expect_mz"], case["expect_verdict"],
                 got_mz or "absent", got_verdict or "absent",
                 "letter" if letter else "none", "yes" if ok else "no"), flush=True)

    killed = base_killed = 0
    for name, patched in apply_mutants(cand_bytes):
        path = os.path.join(work, "mutant-%s.py" % name)
        with open(path, "wb") as fh:
            fh.write(patched)
        score = base_score = 0
        for case in cases:
            fixture = os.path.join(work, "fixtures", case["name"])
            out = dec(harness_run(path, fixture, os.path.join(work, "mut", name, case["name"]),
                                  env).stdout)
            got_mz, got_verdict = parse_row(out)
            if got_mz == case["expect_mz"] and got_verdict == case["expect_verdict"]:
                score += 1
            if got_mz == case["expect_mz"]:
                base_score += 1
        is_killed = score < len(cases)
        is_base_killed = base_score < len(cases)
        killed += int(is_killed)
        base_killed += int(is_base_killed)
        print("MADO_R76_MUTANT name=%s score=%d/%d base_score=%d/%d killed=%s base_killed=%s"
              % (name, score, len(cases), base_score, len(cases),
                 "yes" if is_killed else "no", "yes" if is_base_killed else "no"), flush=True)

    met = (len(cases) == FROZEN_CASES and correct == FROZEN_CORRECT
           and killed == FROZEN_KILLED and base_killed == FROZEN_BASE_KILLED and challenge_ok)
    line = ("MADO_R76_OUTCOME_FIELD: cases=%d correct=%d mutants=%d killed=%d base_killed=%d "
            "verdict=%s rev=%s"
            % (len(cases), correct, len(MUTANTS), killed, base_killed,
               "TARGET_MET" if met else "TARGET_MISSED", sha))
    if not CONTRACT_RE.fullmatch(line):
        raise SetupError("emitted contract line does not match CONTRACT_RE")
    print(line, flush=True)
    return 0 if met else 1


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

    modes = ["right", "liar-success", "always-red", "green-mutant", "green-absent",
             "green-overlong", "green-last-wrong", "green-uppercase", "uppercase", "stale",
             "absent", "overlong", "wrong", "last-wrong", "crash", "zero-denominator",
             "mismatch-detail"]
    want("the frozen mode list is the seventeen fixture modes",
         all(m in LANE_TEMPLATE for m in modes) and len(modes) == 17)
    want("the case count is sixteen", FROZEN_CASES == 16)
    want("the kill targets are four and the base target zero",
         FROZEN_KILLED == 4 and FROZEN_BASE_KILLED == 0 and FROZEN_MUTANTS == len(MUTANTS))
    want("each mutant anchor occurs exactly once in the frozen rule snippet",
         all(RULE_SNIPPET.count(old) == 1 for _name, old, _new in MUTANTS))
    want("each mutant replacement differs from its anchor",
         all(old != new for _name, old, new in MUTANTS))
    good = ("MADO_R76_OUTCOME_FIELD: cases=16 correct=16 mutants=4 killed=4 base_killed=0 "
            "verdict=TARGET_MET rev=" + "a" * 40)
    want("the contract shape accepts the met line", CONTRACT_RE.fullmatch(good) is not None)
    want("the contract shape accepts an absent candidate",
         CONTRACT_RE.fullmatch(good.replace("correct=16", "correct=absent")) is not None)
    want("the contract shape refuses a wrong verdict word",
         CONTRACT_RE.fullmatch(good.replace("TARGET_MET", "DONE")) is None)
    want("the candidate row carries both scored fields", CAND_RE.fullmatch(
        "MADO_R76_LANDING_CONTROLS: selftest=2/2 mz=fail mr=pass killed=2/2 baseline=0/2 "
        "witness=ok verdict=TARGET_MET rev=" + "a" * 40) is not None)
    want("an over-long echo parses as a mismatch in the fixture lane",
         "green-overlong|overlong)" in LANE_TEMPLATE and "%s00" in LANE_TEMPLATE)
    want("the always-red mode keeps the M-Z kill while the summary stays red",
         "always-red)" in LANE_TEMPLATE and "always reports this failure" in LANE_TEMPLATE)

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
            print("MADO_R76_OUTCOME_FIELD_SELFTEST FAIL: %s" % name)
    print("MADO_R76_OUTCOME_FIELD_SELFTEST: %d/%d assertions passed" % (passed, len(checks)))
    return 0 if passed == len(checks) else 1


# --------------------------------------------------------------------------------------------- cli
def build_parser():
    parser = argparse.ArgumentParser(prog=TOOL, description=__doc__.splitlines()[0])
    parser.add_argument("--repo")
    parser.add_argument("--rev")
    parser.add_argument("--base-rev", dest="base_rev")
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
