#!/usr/bin/env python3
r"""Round-74 C1 counting command: the credit rule requires the run's own witness of the
counter's per-run challenge (claim C1, round 74).

    python3 quality/counters/c1-r74-replay-witness.py --repo . --rev REV \
        --base-rev bd5a971532f37df85a78f6f566dd1e649b79de11 \
        --controls .ufo/waves/round-74/controls/c1-replay-cases-r74.json --scratch-root DIR
    python3 quality/counters/c1-r74-replay-witness.py --selftest --scratch-root DIR

What is scored. Twelve REAL `bash` children, one per frozen case, each a copy of the lane's
landing-counter fixture with the frozen zero-citation clause deleted once (the harness's own
M-Z mutation, asserted to occur exactly once). Every child is run with its OWN fresh challenge in
`MADO_LANDING_NONCE` (one `secrets.token_hex(8)` per case, never the frozen stale value); a
genuine child echoes it in `MADO_LANDING_WITNESS: <16 hex>`, a replay child carries a stale,
wrong, missing or last-wrong witness.

Two rules are scored on the same twelve outputs in the same run:

  candidate  `credit(out, nonce)` extracted from `quality/counters/c1-r74-witness-rule.py`
             at --rev: the round-72 arithmetic plus the last parsed witness equals the challenge;
  base       the frozen round-72 `credit(out)` extracted from
             `quality/counters/c1-r72-landing-controls.py` at --base-rev: the arithmetic only,
             so it credits every replay whose detail lines add up.

The eight round-72 modes are carried by name and expectation; the four replay modes are the
round-74 negatives. The do-nothing control must score exactly 8/12; the candidate must score
12/12.

Printed receipt (last line, exact):

    MADO_R74_REPLAY_WITNESS: cases=12 correct=<n> base_correct=<m> verdict=<TARGET_MET|TARGET_MISSED> rev=<sha>

Exit 0 iff cases == 12, correct == 12 and base_correct == 8; 1 iff the measurement ran and
missed (an absent candidate rule prints `correct=absent`); 2 on usage/setup error with the reason
on stderr and no contract line.

Selftest: `--selftest` is hermetic - it spawns nothing, touches only <scratch-root>, checks the
frozen case structure and the carried labels, the contract line shape, the fixture template's
mutation marker and the scratch refusals. It does not claim that a real bash child behaves as the
fixture says; the measurement itself runs those.

Declared limits: the challenge authenticates the run's echo, not the truth of the assertions; the
twelve cases are fixture lanes, not fault coverage; the candidate rule is a standalone instrument
and is not wired into the frozen round-72 harness this round.
"""
import argparse
import hashlib
import json
import os
import re
import runpy
import secrets
import shutil
import subprocess
import sys

TOOL = "c1-r74-replay-witness.py"
CANDIDATE = "quality/counters/c1-r74-witness-rule.py"
BASE_HARNESS = "quality/counters/c1-r72-landing-controls.py"
FROZEN_CASES = 12
FROZEN_CORRECT = 12
FROZEN_BASE_CORRECT = 8
FROZEN_CONTROLS_SHA = "17c95774044fb2d8125b9f4bf85bdcb947babb60e438424f246b77785574727c"
CARRIED = (
    ("liar-success", "pass"), ("stderr-genuine", "pass"), ("liar-kill", "fail"),
    ("crash-stderr", "fail"), ("bare-failing", "fail"), ("mismatch-detail", "fail"),
    ("last-wins-pass", "fail"), ("last-wins-fail", "pass"),
)
REPLAY = ("replay-captured", "replay-no-witness", "witness-mismatch", "witness-last-wins")
STALE = "0123456789abcdef"
UNSAFE_ROOTS = ("/tmp", "/var/tmp", "/dev/shm")
CONTRACT_RE = re.compile(
    r"MADO_R74_REPLAY_WITNESS: cases=12 correct=(?:absent|[0-9]{1,2}) base_correct=[0-9]{1,2} "
    r"verdict=(?:TARGET_MET|TARGET_MISSED) rev=[0-9a-f]{40,64}")
Z_MARK = "ZCLAUSE"
LANE_TEMPLATE = """#!/usr/bin/env bash
# fixture lane for the round-74 replay probe (mode: @MODE@)
set -u
MODE=@MODE@
verify() {
  local citations=$1 resolved=$2 missing=$3
  ZCLAUSE[ "$citations" -eq "$((resolved+missing))" ] || return 1
  if [ "$missing" -eq 0 ]; then return 0; fi
  return 1
}
N=0
P=0
check() { N=$((N+1)); if [ "$2" = "$3" ]; then P=$((P+1)); printf 'SELFTEST ok %d: %s\\n' "$N" "$1"; else printf 'SELFTEST FAIL %d: %s want=%s got=%s\\n' "$N" "$1" "$2" "$3"; fi; }
witness() { printf 'MADO_LANDING_WITNESS: %s\\n' "$1"; }
verify 1 1 0; check 'one citation resolves' 0 "$?"
zero=0
verify 0 0 0 || zero=1
if [ "$zero" -eq 1 ]; then
  check 'zero citations refused' 1 1
  witness "${MADO_LANDING_NONCE:-}"
  printf 'MADO_LANDING_COUNTERS_SELFTEST: %d/%d assertions passed\\n' "$P" "$N"
  [ "$P" -eq "$N" ]
else
  case "$MODE" in
    liar-success) check 'zero citations refused' 1 0; witness "${MADO_LANDING_NONCE:-}"; printf 'MADO_LANDING_COUNTERS_SELFTEST: %d/%d assertions passed\\n' "$P" "$N"; exit 0 ;;
    stderr-genuine) check 'zero citations refused' 1 0; witness "${MADO_LANDING_NONCE:-}" >&2; printf 'MADO_LANDING_COUNTERS_SELFTEST: %d/%d assertions passed\\n' "$P" "$N" >&2; [ "$P" -eq "$N" ] ;;
    liar-kill) check 'citation arithmetic holds' 0 0; witness "${MADO_LANDING_NONCE:-}"; printf 'MADO_LANDING_COUNTERS_SELFTEST: %d/%d assertions passed\\n' "$P" "$N"; exit 1 ;;
    crash-stderr) printf 'fatal: assertion harness collapsed before any summary\\n' >&2; exit 2 ;;
    bare-failing) printf 'MADO_LANDING_COUNTERS_SELFTEST: 0/2 assertions passed\\n'; exit 1 ;;
    mismatch-detail) printf 'SELFTEST FAIL 2: a want=1 got=0\\nSELFTEST FAIL 3: b want=1 got=0\\nSELFTEST FAIL 4: c want=1 got=0\\n'; printf 'MADO_LANDING_COUNTERS_SELFTEST: 0/2 assertions passed\\n'; exit 1 ;;
    last-wins-pass) check 'zero citations refused' 1 0; witness "${MADO_LANDING_NONCE:-}"; printf 'MADO_LANDING_COUNTERS_SELFTEST: 1/2 assertions passed\\n'; printf 'MADO_LANDING_COUNTERS_SELFTEST: 2/2 assertions passed\\n'; exit 1 ;;
    last-wins-fail) witness "${MADO_LANDING_NONCE:-}"; printf 'MADO_LANDING_COUNTERS_SELFTEST: 2/2 assertions passed\\n'; printf 'SELFTEST FAIL 9: zero citations refused want=1 got=0\\n'; printf 'MADO_LANDING_COUNTERS_SELFTEST: 1/2 assertions passed\\n'; exit 1 ;;
    replay-captured) witness "@STALE@"; printf 'SELFTEST FAIL 9: zero citations refused want=1 got=0\\n'; printf 'MADO_LANDING_COUNTERS_SELFTEST: 1/2 assertions passed\\n'; exit 1 ;;
    replay-no-witness) printf 'SELFTEST FAIL 9: zero citations refused want=1 got=0\\n'; printf 'MADO_LANDING_COUNTERS_SELFTEST: 1/2 assertions passed\\n'; exit 1 ;;
    witness-mismatch) witness "deadbeefdeadbeef"; printf 'SELFTEST FAIL 9: zero citations refused want=1 got=0\\n'; printf 'MADO_LANDING_COUNTERS_SELFTEST: 1/2 assertions passed\\n'; exit 1 ;;
    witness-last-wins) witness "${MADO_LANDING_NONCE:-}"; witness "deadbeefdeadbeef"; printf 'SELFTEST FAIL 9: zero citations refused want=1 got=0\\n'; printf 'MADO_LANDING_COUNTERS_SELFTEST: 1/2 assertions passed\\n'; exit 1 ;;
  esac
fi
"""


class UsageError(Exception):
    pass


class SetupError(Exception):
    pass


def git_env():
    env = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}
    env["GIT_OPTIONAL_LOCKS"] = "0"
    env["GIT_NO_REPLACE_OBJECTS"] = "1"
    env["LC_ALL"] = "C"
    return env


def child_env(nonce):
    env = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}
    env["LC_ALL"] = "C"
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    env["MADO_LANDING_NONCE"] = nonce
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


def score(expect, got):
    return got is not None and got == expect


def verdict_met(correct, base_correct):
    return correct == FROZEN_CORRECT and base_correct == FROZEN_BASE_CORRECT


def contract_line(correct, base_correct, sha):
    return ("MADO_R74_REPLAY_WITNESS: cases=12 correct=%s base_correct=%d verdict=%s rev=%s"
            % ("absent" if correct is None else str(correct), base_correct,
               "TARGET_MET" if verdict_met(correct, base_correct) else "TARGET_MISSED", sha))


def load_controls(path):
    try:
        with open(path, "rb") as fh:
            data = fh.read()
    except OSError as exc:
        raise SetupError("controls file unreadable: %s" % exc)
    digest = sha256_hex(data)
    if digest != FROZEN_CONTROLS_SHA:
        raise SetupError("controls file sha256 %s does not match the frozen digest" % digest)
    try:
        doc = json.loads(data.decode("utf-8"))
        cases = doc["cases"]
    except (UnicodeDecodeError, ValueError, KeyError) as exc:
        raise SetupError("controls file unusable: %s" % exc)
    if len(cases) != FROZEN_CASES:
        raise SetupError("controls file carries %d cases, frozen %d" % (len(cases), FROZEN_CASES))
    by_name = {case["name"]: case for case in cases}
    if len(by_name) != FROZEN_CASES:
        raise SetupError("controls file carries duplicate case names")
    for name, expect in CARRIED:
        case = by_name.get(name)
        if case is None or case["expect"] != expect or case["class"] != "carried-r72":
            raise SetupError("the round-72 case %r is not carried with its frozen label" % name)
    for name in REPLAY:
        case = by_name.get(name)
        if case is None or case["expect"] != "fail" or case["class"] != "replay":
            raise SetupError("the replay case %r is not frozen as a fail" % name)
    if doc.get("stale_nonce") != STALE:
        raise SetupError("the frozen stale nonce is not %r" % STALE)
    return cases


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


def build_lane(mode, work):
    lane = LANE_TEMPLATE.replace("@MODE@", mode).replace("@STALE@", STALE)
    if lane.count(Z_MARK) != 1:
        raise SetupError("the fixture lane does not carry the frozen clause exactly once")
    lane = lane.replace(Z_MARK, "")
    path = os.path.join(work, "lane-%s.sh" % mode)
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(lane)
    os.chmod(path, 0o755)
    return path


def measure(args):
    scratch = absolute_scratch(args.scratch_root)
    if not args.repo or not args.rev or not args.base_rev or not args.controls:
        raise UsageError("--repo, --rev, --base-rev and --controls are required")
    repo = os.path.abspath(args.repo)
    if not os.path.isdir(repo):
        raise SetupError("--repo is not a directory: %s" % repo)
    cases = load_controls(os.path.abspath(args.controls))
    emit("MADO_R74_CONTROLS path=%s cases=%d sha256=%s"
         % (os.path.abspath(args.controls), len(cases), FROZEN_CONTROLS_SHA))
    work = os.path.join(scratch, "r74-c1")
    shutil.rmtree(work, ignore_errors=True)
    os.makedirs(work)
    sha = resolve_rev(repo, args.rev)
    base_sha = resolve_rev(repo, args.base_rev)
    emit("MADO_R74_REVS rev=%s base=%s" % (sha, base_sha))

    candidate = extract(repo, sha, CANDIDATE)
    if candidate is None:
        emit("MADO_R74_RULE role=candidate path=%s present=no" % CANDIDATE)
        emit(contract_line(None, 0, sha))
        return 1
    cand_path = os.path.join(work, "candidate.py")
    with open(cand_path, "wb") as fh:
        fh.write(candidate)
    emit("MADO_R74_RULE role=candidate path=%s present=yes sha256=%s"
         % (CANDIDATE, sha256_hex(candidate)))
    candidate_credit = runpy.run_path(cand_path)["credit"]

    base = extract(repo, base_sha, BASE_HARNESS)
    if base is None:
        raise SetupError("%s is absent at the base revision %s" % (BASE_HARNESS, base_sha))
    base_path = os.path.join(work, "base.py")
    with open(base_path, "wb") as fh:
        fh.write(base)
    emit("MADO_R74_RULE role=base path=%s sha256=%s" % (BASE_HARNESS, sha256_hex(base)))
    base_credit = runpy.run_path(base_path)["credit"]

    correct = 0
    base_correct = 0
    for case in cases:
        nonce = secrets.token_hex(8)
        while nonce == STALE:
            nonce = secrets.token_hex(8)
        emit("MADO_R74_CHALLENGE case=%s nonce=%s len=%d"
             % (case["name"], nonce, len(nonce)))
        lane = build_lane(case["mode"], work)
        r = subprocess.run(["bash", lane], cwd=work, stdout=subprocess.PIPE,
                           stderr=subprocess.PIPE, env=child_env(nonce), timeout=120)
        out = dec(r.stdout) + dec(r.stderr)
        cand = "pass" if candidate_credit(out, nonce) else "fail"
        held = "pass" if base_credit(out) else "fail"
        ok = score(case["expect"], cand)
        base_ok = score(case["expect"], held)
        correct += int(ok)
        base_correct += int(base_ok)
        emit("MADO_R74_SCENARIO name=%s expect=%s candidate=%s base=%s correct=%s "
             "base_correct=%s rc=%d"
             % (case["name"], case["expect"], cand, held,
                "yes" if ok else "no", "yes" if base_ok else "no", r.returncode))

    emit(contract_line(correct, base_correct, sha))
    return 0 if verdict_met(correct, base_correct) else 1


def _selftest_checks(work):
    checks = []

    def want(name, cond):
        checks.append((name, bool(cond)))

    want("candidate path is the round-74 witness rule",
         CANDIDATE.endswith("c1-r74-witness-rule.py"))
    want("base path is the frozen round-72 harness",
         BASE_HARNESS.endswith("c1-r72-landing-controls.py"))
    want("twelve frozen cases", FROZEN_CASES == 12)
    want("eight carried labels and expectations",
         CARRIED == (("liar-success", "pass"), ("stderr-genuine", "pass"),
                     ("liar-kill", "fail"), ("crash-stderr", "fail"),
                     ("bare-failing", "fail"), ("mismatch-detail", "fail"),
                     ("last-wins-pass", "fail"), ("last-wins-fail", "pass")))
    want("four replay negatives", REPLAY == ("replay-captured", "replay-no-witness",
                                             "witness-mismatch", "witness-last-wins"))
    want("frozen totals", FROZEN_CORRECT == 12 and FROZEN_BASE_CORRECT == 8)
    want("the fixture lane carries the mutation marker exactly once",
         LANE_TEMPLATE.count(Z_MARK) == 1)
    want("the fixture lane carries all twelve mode labels",
         all(("    %s)" % name).encode() in LANE_TEMPLATE.encode("utf-8")
             for name in [c[0] for c in CARRIED] + list(REPLAY)))
    want("the fixture lane never refers to the counter",
         b"c1-r74-replay-witness" not in LANE_TEMPLATE.encode("utf-8"))
    want("the fixture lane echoes the challenge", b"MADO_LANDING_NONCE" in
         LANE_TEMPLATE.encode("utf-8"))

    want("met line is TARGET_MET", " verdict=TARGET_MET " in contract_line(12, 8, "a" * 40))
    want("a candidate miss is TARGET_MISSED",
         " verdict=TARGET_MISSED " in contract_line(11, 8, "a" * 40))
    want("a base miss is TARGET_MISSED",
         " verdict=TARGET_MISSED " in contract_line(12, 9, "a" * 40))
    want("contract line parses", CONTRACT_RE.fullmatch(contract_line(12, 8, "a" * 40)) is not None)
    want("absent line parses", CONTRACT_RE.fullmatch(contract_line(None, 0, "a" * 40)) is not None)
    want("the contract line refuses a wrong verdict word",
         not CONTRACT_RE.fullmatch(
             "MADO_R74_REPLAY_WITNESS: cases=12 correct=12 base_correct=8 verdict=DONE rev="
             + "a" * 40))
    want("score accepts the expected value", score("fail", "fail") and score("pass", "pass"))
    want("score rejects a missing value", not score("pass", None))
    want("verdict requires both legs", verdict_met(12, 8) and not verdict_met(11, 8)
         and not verdict_met(12, 9))

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
            print("MADO_R74_REPLAY_WITNESS_SELFTEST FAIL: %s" % name)
    print("MADO_R74_REPLAY_WITNESS_SELFTEST: %d/%d assertions passed" % (passed, len(checks)))
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
        work = os.path.join(scratch, "r74-c1-selftest")
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
