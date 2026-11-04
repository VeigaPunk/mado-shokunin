#!/usr/bin/env python3
r"""Round-72 C1 counting command: the landing kill credit requires the run's own failure detail
(claim C1, round 72).

    python3 quality/counters/c1-r72-summary-credit.py --repo . --rev REV \
        --base-rev 976684a27e99c2508037a60eec415f550f53d70e --scratch-root DIR
    python3 quality/counters/c1-r72-summary-credit.py --selftest --scratch-root DIR

What is scored. The round-71 credit line credits any parsed
`MADO_LANDING_COUNTERS_SELFTEST: <p>/<n> assertions passed` with `p < n`. That credits a summary
line no assertion of this run produced (a bare echo) and a summary whose failure count is not
backed by the run's own `SELFTEST FAIL` lines. Round 72's `credit(out)` requires the LAST parsed
summary to report `p < n` with `n > 0` AND the run's own `SELFTEST FAIL` lines to number exactly
`n - p`; both captured streams are read, as in round 71.

Eight scenarios, each a REAL `bash` child built into a scratch git fixture; in every scenario the
harness's M-Z leg deletes the frozen clause `[ "$citations" -gt 0 ] && ` and runs the mutated
lane:

  carried (round-71 set, expectations unchanged):
  liar-success    genuine `1/2` summary, exit 0                          -> pass
  stderr-genuine  the genuine `1/2` summary on stderr only, exit 1       -> pass
  liar-kill       `2/2` summary with an unrelated exit 1                 -> fail
  crash-stderr    exit 2 with stderr noise and no summary                -> fail
  new (round-72 D1):
  bare-failing    a `0/2` summary line and no `SELFTEST FAIL` line       -> fail
  mismatch-detail a `0/2` summary beside three `SELFTEST FAIL` lines     -> fail
  last-wins-pass  a `1/2` block, then `2/2` last                          -> fail
  last-wins-fail  a `2/2` line, then one fail line and `1/2` last         -> pass

Both harnesses run against the same fixture: the candidate at `--rev` (round 72) and the frozen
round-71 harness at `--base-rev` (the do-nothing control). The control must score exactly 6/8;
the candidate must score 8/8. Every write stays under the caller-declared scratch root, which
refuses /tmp-family and symlinked roots.

Printed receipt (last line, exact):

    MADO_R72_SUMMARY_CREDIT: cases=8 correct=<n> base_correct=<m> verdict=<TARGET_MET|TARGET_MISSED> rev=<sha>

Exit 0 iff correct == 8 and base_correct == 6; 1 iff the measurement ran and missed (the
candidate harness absent at `--rev` prints `correct=absent`); 2 on usage/setup error, with the
reason on stderr and no contract line.

Selftest: `--selftest` is hermetic - it spawns nothing, touches only <scratch-root>, and drives
the decision functions (marker parse, scoring, verdict) plus the fixture lane template's
structural invariants. It does not claim that a real bash child behaves as the fixture says; the
measurement itself runs those.

Declared limits: the eight scenarios are fixture lanes, not a fault-coverage claim; the fixture
is the counter's own instrument and is not the lane's real landing instrument; a captured summary
replayed with its own matching detail lines remains byte-indistinguishable from a genuine run -
the rule bounds the summary to the run's own fail lines, it does not authenticate them.
"""
import argparse
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys

TOOL = "c1-r72-summary-credit.py"
CANDIDATE = "quality/counters/c1-r72-landing-controls.py"
BASE_HARNESS = "quality/counters/c1-r71-landing-controls.py"
CHILDREN = ("quality/counters/c3-r56-used-by.py",
            "quality/check-tool-ledger.py",
            "tools/mado-receipt-citecheck.py")
LANE = "quality/landing-counters.sh"
CAND_PREFIX = "MADO_R72_LANDING_CONTROLS:"
BASE_PREFIX = "MADO_R71_LANDING_CONTROLS:"
MODES = ("liar-success", "stderr-genuine", "liar-kill", "crash-stderr",
         "bare-failing", "mismatch-detail", "last-wins-pass", "last-wins-fail")
EXPECT = {"liar-success": "pass", "stderr-genuine": "pass",
          "liar-kill": "fail", "crash-stderr": "fail",
          "bare-failing": "fail", "mismatch-detail": "fail",
          "last-wins-pass": "fail", "last-wins-fail": "pass"}
FROZEN_CORRECT = 8
FROZEN_BASE_CORRECT = 6
Z_CLAUSE = b'[ "$citations" -gt 0 ] && '
UNSAFE_ROOTS = ("/tmp", "/var/tmp", "/dev/shm")
CONTRACT_RE = re.compile(
    r"MADO_R72_SUMMARY_CREDIT: cases=8 correct=(?:absent|[0-8]) base_correct=[0-8] "
    r"verdict=(?:TARGET_MET|TARGET_MISSED) rev=[0-9a-f]{40,64}")
LANE_TEMPLATE = """#!/usr/bin/env bash
# fixture lane for the r71 real-children probe (mode: @MODE@)
set -u
MODE=@MODE@
verify() {
  local citations=$1 resolved=$2 missing=$3
  [ "$citations" -gt 0 ] && [ "$citations" -eq "$((resolved+missing))" ] || return 1
  if [ "$missing" -eq 0 ]; then return 0; fi
  return 1
}
N=0
P=0
check() { N=$((N+1)); if [ "$2" = "$3" ]; then P=$((P+1)); printf 'SELFTEST ok %d: %s\\n' "$N" "$1"; else printf 'SELFTEST FAIL %d: %s want=%s got=%s\\n' "$N" "$1" "$2" "$3"; fi; }
verify 1 1 0; check 'one citation resolves' 0 "$?"
zero=0
verify 0 0 0 || zero=1
if [ "$zero" -eq 1 ]; then
  check 'zero citations refused' 1 1
  printf 'MADO_LANDING_COUNTERS_SELFTEST: %d/%d assertions passed\\n' "$P" "$N"
  [ "$P" -eq "$N" ]
else
  case "$MODE" in
    liar-success) check 'zero citations refused' 1 0; printf 'MADO_LANDING_COUNTERS_SELFTEST: %d/%d assertions passed\\n' "$P" "$N"; exit 0 ;;
    stderr-genuine) check 'zero citations refused' 1 0; printf 'MADO_LANDING_COUNTERS_SELFTEST: %d/%d assertions passed\\n' "$P" "$N" >&2; [ "$P" -eq "$N" ] ;;
    liar-kill) check 'citation arithmetic holds' 0 0; printf 'MADO_LANDING_COUNTERS_SELFTEST: %d/%d assertions passed\\n' "$P" "$N"; exit 1 ;;
    crash-stderr) printf 'fatal: assertion harness collapsed before any summary\\n' >&2; exit 2 ;;
    bare-failing) printf 'MADO_LANDING_COUNTERS_SELFTEST: 0/2 assertions passed\\n'; exit 1 ;;
    mismatch-detail) printf 'SELFTEST FAIL 2: a want=1 got=0\\nSELFTEST FAIL 3: b want=1 got=0\\nSELFTEST FAIL 4: c want=1 got=0\\n'; printf 'MADO_LANDING_COUNTERS_SELFTEST: 0/2 assertions passed\\n'; exit 1 ;;
    last-wins-pass) check 'zero citations refused' 1 0; printf 'MADO_LANDING_COUNTERS_SELFTEST: 1/2 assertions passed\\n'; printf 'MADO_LANDING_COUNTERS_SELFTEST: 2/2 assertions passed\\n'; exit 1 ;;
    last-wins-fail) printf 'MADO_LANDING_COUNTERS_SELFTEST: 2/2 assertions passed\\n'; printf 'SELFTEST FAIL 9: zero citations refused want=1 got=0\\n'; printf 'MADO_LANDING_COUNTERS_SELFTEST: 1/2 assertions passed\\n'; exit 1 ;;
  esac
fi
"""


class UsageError(Exception):
    pass


class SetupError(Exception):
    pass


# --------------------------------------------------------------------------------------------- env
def git_env():
    env = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}
    env["GIT_OPTIONAL_LOCKS"] = "0"
    env["GIT_NO_REPLACE_OBJECTS"] = "1"
    env["LC_ALL"] = "C"
    return env


def child_env():
    env = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}
    env["LC_ALL"] = "C"
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    return env


def run(argv, cwd=None, timeout=900):
    return subprocess.run(argv, cwd=cwd, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                          env=git_env(), timeout=timeout)


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
    norm = os.path.normcase(root)
    for unsafe in UNSAFE_ROOTS:
        if norm == unsafe or norm.startswith(unsafe + os.sep):
            raise UsageError("--scratch-root under %s is refused" % unsafe)
    return root


# --------------------------------------------------------------------------------------------- decisions
def parse_mz(out, prefix):
    """`pass`/`fail` from the last line with `prefix`, else None."""
    got = None
    for line in out.splitlines():
        if line.startswith(prefix):
            m = re.search(r"\bmz=(pass|fail)\b", line)
            if m:
                got = m.group(1)
    return got


def score(expect, got):
    return True if got is None else got == expect


def verdict_met(correct, base_correct):
    return correct == FROZEN_CORRECT and base_correct == FROZEN_BASE_CORRECT


def contract_line(correct, base_correct, sha):
    return ("MADO_R72_SUMMARY_CREDIT: cases=8 correct=%s base_correct=%d verdict=%s rev=%s"
            % ("absent" if correct is None else str(correct), base_correct,
               "TARGET_MET" if verdict_met(correct, base_correct) else "TARGET_MISSED", sha))


# --------------------------------------------------------------------------------------------- fixture
def write_file(path, data):
    d = os.path.dirname(path)
    if d:
        os.makedirs(d, exist_ok=True)
    with open(path, "wb") as fh:
        fh.write(data)


def git(fx, args, identity=False):
    argv = ["git"]
    if identity:
        argv += ["-c", "user.name=r71-c1", "-c", "user.email=r71-c1@example.invalid",
                 "-c", "commit.gpgsign=false"]
    argv += ["-C", fx] + list(args)
    r = run(argv, cwd=fx)
    if r.returncode != 0:
        raise SetupError("git %s failed in the fixture: %s"
                         % (" ".join(args), dec(r.stderr).strip()[:200]))
    return r


def build_fixture(work, children):
    """Scratch git repo: three commits, one per scenario mode. Returns (path, {mode: rev})."""
    fx = os.path.join(work, "fx")
    shutil.rmtree(fx, ignore_errors=True)
    os.makedirs(fx)
    git(fx, ["init", "-q", "."])
    top = dec(git(fx, ["rev-parse", "--show-toplevel"]).stdout).strip()
    if os.path.realpath(top) != os.path.realpath(fx):
        raise SetupError("fixture repo toplevel %r is not the scratch dir" % top)
    for rel, data in children.items():
        write_file(os.path.join(fx, rel), data)
    revs = {}
    for mode in MODES:
        write_file(os.path.join(fx, LANE),
                   LANE_TEMPLATE.replace("@MODE@", mode).encode("utf-8"))
        os.chmod(os.path.join(fx, LANE), 0o755)
        git(fx, ["add", "-A"])
        git(fx, ["commit", "-qm", "fixture mode %s" % mode], identity=True)
        revs[mode] = dec(git(fx, ["rev-parse", "HEAD"]).stdout).strip()
        emit("MADO_R72_FIXTURE mode=%s rev=%s lane_sha256=%s"
             % (mode, revs[mode], sha256_hex(open(os.path.join(fx, LANE), "rb").read())))
    return fx, revs


def resolve_rev(repo, rev):
    r = run(["git", "-C", repo, "rev-parse", "--verify", rev + "^{commit}"], cwd=repo)
    if r.returncode != 0:
        raise SetupError("cannot resolve %s: %s" % (rev, dec(r.stderr).strip()[:200]))
    return dec(r.stdout).strip()


def extract(repo, sha, path):
    r = run(["git", "-C", repo, "show", "%s:%s" % (sha, path)], cwd=repo)
    if r.returncode != 0:
        return None
    return r.stdout


def run_harness(harness_path, prefix, fx, rev, scratch):
    os.makedirs(scratch, exist_ok=True)
    argv = [sys.executable or "python3", "-I", harness_path,
            "--repo", fx, "--rev", rev, "--scratch-root", scratch]
    r = subprocess.run(argv, cwd=scratch, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                       env=child_env(), timeout=900)
    out = dec(r.stdout) + dec(r.stderr)
    return r.returncode, parse_mz(out, prefix), out


# --------------------------------------------------------------------------------------------- measurement
def measure(args):
    scratch = absolute_scratch(args.scratch_root)
    if not args.repo or not args.rev or not args.base_rev:
        raise UsageError("--repo, --rev and --base-rev are required")
    repo = os.path.abspath(args.repo)
    if not os.path.isdir(repo):
        raise SetupError("--repo is not a directory: %s" % repo)
    work = os.path.join(scratch, "r72-c1")
    shutil.rmtree(work, ignore_errors=True)
    os.makedirs(work)
    sha = resolve_rev(repo, args.rev)
    base_sha = resolve_rev(repo, args.base_rev)
    emit("MADO_R72_REVS rev=%s base=%s" % (sha, base_sha))

    candidate = extract(repo, sha, CANDIDATE)
    if candidate is None:
        emit("MADO_R72_HARNESS role=candidate path=%s present=no" % CANDIDATE)
        emit(contract_line(None, 0, sha))
        return 1
    cand_path = os.path.join(work, "candidate.py")
    write_file(cand_path, candidate)
    emit("MADO_R72_HARNESS role=candidate path=%s present=yes sha256=%s"
         % (CANDIDATE, sha256_hex(candidate)))

    base = extract(repo, base_sha, BASE_HARNESS)
    if base is None:
        raise SetupError("%s is absent at the base revision %s" % (BASE_HARNESS, base_sha))
    base_path = os.path.join(work, "base.py")
    write_file(base_path, base)
    emit("MADO_R72_HARNESS role=base path=%s sha256=%s" % (BASE_HARNESS, sha256_hex(base)))

    children = {}
    for rel in CHILDREN:
        data = extract(repo, sha, rel)
        if data is None:
            raise SetupError("fixture child %s is absent at %s" % (rel, sha))
        children[rel] = data
    fx, revs = build_fixture(work, children)

    correct = 0
    base_correct = 0
    for mode in MODES:
        _, got, _ = run_harness(cand_path, CAND_PREFIX, fx, revs[mode],
                                os.path.join(work, "cand-" + mode))
        _, base_got, _ = run_harness(base_path, BASE_PREFIX, fx, revs[mode],
                                     os.path.join(work, "base-" + mode))
        ok = score(EXPECT[mode], got)
        base_ok = score(EXPECT[mode], base_got)
        correct += int(ok)
        base_correct += int(base_ok)
        emit("MADO_R72_SCENARIO mode=%s expect_mz=%s candidate_mz=%s base_mz=%s "
             "correct=%s base_correct=%s rev=%s"
             % (mode, EXPECT[mode], got or "none", base_got or "none",
                "yes" if ok else "no", "yes" if base_ok else "no", revs[mode]))

    emit(contract_line(correct, base_correct, sha))
    return 0 if verdict_met(correct, base_correct) else 1


# --------------------------------------------------------------------------------------------- selftest
def _selftest_checks(work):
    checks = []

    def want(name, cond):
        checks.append((name, bool(cond)))

    want("candidate path is the round-72 harness",
         CANDIDATE.endswith("c1-r72-landing-controls.py"))
    want("base path is the frozen round-71 harness",
         BASE_HARNESS.endswith("c1-r71-landing-controls.py"))
    want("eight scenarios", MODES == (
        "liar-success", "stderr-genuine", "liar-kill", "crash-stderr",
        "bare-failing", "mismatch-detail", "last-wins-pass", "last-wins-fail"))
    want("expectations", EXPECT == {
        "liar-success": "pass", "stderr-genuine": "pass", "liar-kill": "fail",
        "crash-stderr": "fail", "bare-failing": "fail", "mismatch-detail": "fail",
        "last-wins-pass": "fail", "last-wins-fail": "pass"})
    want("frozen totals", FROZEN_CORRECT == 8 and FROZEN_BASE_CORRECT == 6)

    line = ("MADO_R72_LANDING_CONTROLS: selftest=62/62 mz=pass mr=pass killed=2/2 "
            "baseline=0/2 verdict=TARGET_MET rev=" + "a" * 40)
    base_line = ("MADO_R71_LANDING_CONTROLS: selftest=0 mz=pass mr=pass killed=2/2 "
                 "baseline=0/2 verdict=TARGET_MET rev=" + "a" * 40)
    want("candidate line parses pass", parse_mz(line, CAND_PREFIX) == "pass")
    want("base line parses pass", parse_mz(base_line, BASE_PREFIX) == "pass")
    want("prefixes do not cross-parse",
         parse_mz(base_line, CAND_PREFIX) is None and parse_mz(line, BASE_PREFIX) is None)
    want("crash line parses fail",
         parse_mz("MADO_R72_LANDING_CONTROLS: selftest=62/62 mz=fail mr=pass killed=1/2 "
                  "baseline=0/2 verdict=TARGET_MISSED rev=" + "a" * 40, CAND_PREFIX) == "fail")
    want("absent marker is none", parse_mz("boom\n", CAND_PREFIX) is None)

    want("liar-success pass is correct", score("pass", "pass"))
    want("stderr-genuine pass is correct", score("pass", "pass"))
    want("liar-kill pass is a false credit", not score("fail", "pass"))
    want("bare-failing pass is a false credit", not score("fail", "pass"))
    want("mismatch-detail pass is a false credit", not score("fail", "pass"))
    want("last-wins-fail fail is a false rejection", not score("pass", "fail"))
    want("missing verdict is not correct", not score("pass", None))

    want("8/8 and base 6/8 is met", verdict_met(8, 6))
    want("7/8 is not met", not verdict_met(7, 6))
    want("base 7/8 is not met", not verdict_met(8, 7))
    want("base 5/8 is not met", not verdict_met(8, 5))

    want("contract line parses",
         CONTRACT_RE.fullmatch(contract_line(8, 6, "a" * 40)) is not None)
    want("miss line parses",
         CONTRACT_RE.fullmatch(contract_line(1, 6, "a" * 40)) is not None)
    want("absent line parses",
         CONTRACT_RE.fullmatch(contract_line(None, 0, "a" * 40)) is not None)
    want("met line is TARGET_MET",
         " verdict=TARGET_MET " in contract_line(8, 6, "a" * 40))
    want("base miss line is TARGET_MISSED",
         " verdict=TARGET_MISSED " in contract_line(8, 5, "a" * 40))

    lane = LANE_TEMPLATE.encode("utf-8")
    want("fixture lane carries the frozen clause exactly once", lane.count(Z_CLAUSE) == 1)
    want("fixture lane has one mode slot", lane.count(b"@MODE@") == 2)
    want("fixture lane pins the zero-citation assertion",
         b"check 'zero citations refused'" in lane)
    want("fixture lane carries all eight mode labels",
         all(("    %s)" % m).encode() in lane for m in MODES))
    want("fixture lane never refers to the counter", b"c1-r72-summary-credit" not in lane)

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
    checks = _selftest_checks(work)
    passed = 0
    for name, ok in checks:
        if ok:
            passed += 1
        else:
            print("MADO_R72_SUMMARY_CREDIT_SELFTEST FAIL: %s" % name)
    print("MADO_R72_SUMMARY_CREDIT_SELFTEST: %d/%d assertions passed" % (passed, len(checks)))
    return 0 if passed == len(checks) else 1


# --------------------------------------------------------------------------------------------- cli
def main(argv):
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--repo")
    parser.add_argument("--rev")
    parser.add_argument("--base-rev", dest="base_rev")
    parser.add_argument("--scratch-root", dest="scratch_root")
    parser.add_argument("--selftest", action="store_true")
    args = parser.parse_args(argv)
    try:
        scratch = absolute_scratch(args.scratch_root)
        work = os.path.join(scratch, "r72-c1-selftest")
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
