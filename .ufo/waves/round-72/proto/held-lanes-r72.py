#!/usr/bin/env python3
r"""Round-72 PRE-FREEZE prototype: score the HELD (round-71) legs on the round-72 control sets.

This is not a scored counter. It exists to produce the do-nothing baselines
`.ufo/waves/round-72/control-baseline-c{1,2}-r72.txt` BEFORE the claims are frozen:
a do-nothing control must miss the frozen target, or the target/counter is wrong.

C1 leg: build a scratch git fixture whose lane emits one of eight summary shapes and run the
held round-71 landing harness (`quality/counters/c1-r71-landing-controls.py`) against each
fixture revision, reading its `mz=` credit. The truth (expect_mz) is the frozen label:
credit is earned only when the last parsed summary reports p < n AND the run's own
`SELFTEST FAIL` lines number exactly n - p.

C2 leg: import the held round-71 harness's `outcome_verdict(selftest_rc, killed)` and score
the eight frozen (summary, rc, killed) cases: the truth is green only when the last parsed
`MADO_LANDING_COUNTERS_SELFTEST: p/n assertions passed` summary has n > 0 and p == n.

    python3 .ufo/waves/round-72/proto/held-lanes-r72.py --repo LANE --rev REV --scratch-root DIR

Writes nothing outside the scratch root; prints one PROTO_R72_* line per case and a summary.
"""
import argparse
import hashlib
import importlib.util
import json
import os
import shutil
import subprocess
import sys

CANDIDATE = "quality/counters/c1-r71-landing-controls.py"
CHILDREN = ("quality/counters/c3-r56-used-by.py",
            "quality/check-tool-ledger.py",
            "tools/mado-receipt-citecheck.py")
LANE = "quality/landing-counters.sh"
PREFIX = "MADO_R71_LANDING_CONTROLS:"
UNSAFE_ROOTS = ("/tmp", "/var/tmp", "/dev/shm")

MODES = ("liar-success", "stderr-genuine", "liar-kill", "crash-stderr",
         "bare-failing", "mismatch-detail", "last-wins-pass", "last-wins-fail")
EXPECT = {"liar-success": "pass", "stderr-genuine": "pass",
          "liar-kill": "fail", "crash-stderr": "fail",
          "bare-failing": "fail", "mismatch-detail": "fail",
          "last-wins-pass": "fail", "last-wins-fail": "pass"}

LANE_TEMPLATE = """#!/usr/bin/env bash
# fixture lane for the r72 pre-freeze held-leg probe (mode: @MODE@)
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

C2_CASES = [
    {"id": "green-summary-exit0",
     "gate_out": "MADO_LANDING_COUNTERS_SELFTEST: 12/12 assertions passed",
     "gate_rc": 0, "killed": 2, "expected": "TARGET_MET"},
    {"id": "failing-summary-exit0",
     "gate_out": "MADO_LANDING_COUNTERS_SELFTEST: 3/12 assertions passed",
     "gate_rc": 0, "killed": 2, "expected": "TARGET_MISSED"},
    {"id": "green-summary-exit2",
     "gate_out": "MADO_LANDING_COUNTERS_SELFTEST: 12/12 assertions passed",
     "gate_rc": 2, "killed": 2, "expected": "TARGET_MET"},
    {"id": "no-summary-exit0",
     "gate_out": "bash: script: usage: --repo required",
     "gate_rc": 0, "killed": 2, "expected": "TARGET_MISSED"},
    {"id": "garbled-summary-exit0",
     "gate_out": "MADO_LANDING_COUNTERS_SELFTEST: twelve/twelve assertions passed",
     "gate_rc": 0, "killed": 2, "expected": "TARGET_MISSED"},
    {"id": "failing-summary-exit2",
     "gate_out": "MADO_LANDING_COUNTERS_SELFTEST: 11/12 assertions passed",
     "gate_rc": 2, "killed": 2, "expected": "TARGET_MISSED"},
    {"id": "no-summary-exit2",
     "gate_out": "fatal: cannot parse the instrument output",
     "gate_rc": 2, "killed": 2, "expected": "TARGET_MISSED"},
    {"id": "green-summary-killed1",
     "gate_out": "MADO_LANDING_COUNTERS_SELFTEST: 12/12 assertions passed",
     "gate_rc": 0, "killed": 1, "expected": "TARGET_MISSED"},
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


def run(argv, cwd=None):
    return subprocess.run(argv, cwd=cwd, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                          env=git_env(), timeout=900)


def write_file(path, data):
    d = os.path.dirname(path)
    if d:
        os.makedirs(d, exist_ok=True)
    with open(path, "wb") as fh:
        fh.write(data)


def git(fx, args, identity=False):
    argv = ["git"]
    if identity:
        argv += ["-c", "user.name=r72-proto", "-c", "user.email=r72-proto@example.invalid",
                 "-c", "commit.gpgsign=false"]
    argv += ["-C", fx] + list(args)
    r = run(argv, cwd=fx)
    if r.returncode != 0:
        raise SetupError("git %s failed: %s" % (" ".join(args), dec(r.stderr).strip()[:200]))
    return r


def resolve_rev(repo, rev):
    r = run(["git", "-C", repo, "rev-parse", "--verify", rev + "^{commit}"], cwd=repo)
    if r.returncode != 0:
        raise SetupError("cannot resolve %s: %s" % (rev, dec(r.stderr).strip()[:200]))
    return dec(r.stdout).strip()


def extract(repo, sha, path):
    r = run(["git", "-C", repo, "show", "%s:%s" % (sha, path)], cwd=repo)
    return r.stdout if r.returncode == 0 else None


def build_fixture(work, children):
    fx = os.path.join(work, "fx")
    shutil.rmtree(fx, ignore_errors=True)
    os.makedirs(fx)
    git(fx, ["init", "-q", "."])
    top = dec(git(fx, ["rev-parse", "--show-toplevel"]).stdout).strip()
    if os.path.realpath(top) != os.path.realpath(fx):
        raise SetupError("fixture toplevel %r is not the scratch dir" % top)
    for rel, data in children.items():
        write_file(os.path.join(fx, rel), data)
    revs = {}
    for mode in MODES:
        write_file(os.path.join(fx, LANE), LANE_TEMPLATE.replace("@MODE@", mode).encode("utf-8"))
        os.chmod(os.path.join(fx, LANE), 0o755)
        git(fx, ["add", "-A"])
        git(fx, ["commit", "-qm", "fixture mode %s" % mode], identity=True)
        revs[mode] = dec(git(fx, ["rev-parse", "HEAD"]).stdout).strip()
    return fx, revs


def parse_mz(out):
    got = None
    for line in out.splitlines():
        if line.startswith(PREFIX):
            m = __import__("re").search(r"\bmz=(pass|fail)\b", line)
            if m:
                got = m.group(1)
    return got


def run_harness(harness, fx, rev, scratch):
    os.makedirs(scratch, exist_ok=True)
    argv = [sys.executable or "python3", "-I", harness,
            "--repo", fx, "--rev", rev, "--scratch-root", scratch]
    r = subprocess.run(argv, cwd=scratch, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                       env=child_env(), timeout=900)
    return dec(r.stdout) + dec(r.stderr)


def load_module(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo", required=True)
    ap.add_argument("--rev", required=True)
    ap.add_argument("--scratch-root", required=True)
    args = ap.parse_args()
    scratch = absolute_scratch(args.scratch_root)
    repo = os.path.abspath(args.repo)
    work = os.path.join(scratch, "proto-r72")
    shutil.rmtree(work, ignore_errors=True)
    os.makedirs(work)
    sha = resolve_rev(repo, args.rev)
    emit("PROTO_R72_REV rev=%s harness=%s harness_sha256=%s"
         % (sha, CANDIDATE, sha256_hex(extract(repo, sha, CANDIDATE))))
    harness = os.path.join(work, "held.py")
    write_file(harness, extract(repo, sha, CANDIDATE))
    children = {}
    for rel in CHILDREN:
        data = extract(repo, sha, rel)
        if data is None:
            raise SetupError("fixture child %s absent at %s" % (rel, sha))
        children[rel] = data
    fx, revs = build_fixture(work, children)
    for mode in MODES:
        out = run_harness(harness, fx, revs[mode], os.path.join(work, "held-" + mode))
        got = parse_mz(out)
        ok = got == EXPECT[mode]
        emit("PROTO_R72_C1 mode=%s expect_mz=%s held_mz=%s correct_for_held=%s rev=%s"
             % (mode, EXPECT[mode], got or "none", "yes" if ok else "NO", revs[mode]))
    held = load_module(harness, "held_r71")
    correct = 0
    for case in C2_CASES:
        got = held.outcome_verdict(case["gate_rc"], case["killed"])
        ok = got == case["expected"]
        correct += int(ok)
        emit("PROTO_R72_C2 case=%s expect=%s held=%s held_correct=%s"
             % (case["id"], case["expected"], got, "yes" if ok else "NO"))
    emit("PROTO_R72_SUMMARY c1_modes=%d c2_cases=%d c2_held_correct=%d"
         % (len(MODES), len(C2_CASES), correct))
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except (UsageError, SetupError) as exc:
        sys.stderr.write("proto-r72: %s\n" % exc)
        sys.exit(2)
