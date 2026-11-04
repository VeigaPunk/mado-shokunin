#!/usr/bin/env python3
r"""Round-75 C1 successor landing harness: the M-Z kill credit and the contract outcome require
the run's own echo of a per-run challenge (claim C1, round 75).

    python3 quality/counters/c1-r75-landing-controls.py --repo . --rev REV --scratch-root DIR
    python3 quality/counters/c1-r75-landing-controls.py --selftest --scratch-root DIR

The successor generation loads the frozen round-72 harness from the measured repository at
--rev (its bytes pinned by sha256, so a drifting generation is refused), installs the round-75
rule, and drives the frozen `measure()` body unchanged: the four-file extraction, the
extracted instrument's selftest, the M-Z zero-citation clause deletion, the M-R
replacement-ref pair and the contract line's provenance are the round-72 ones. Only the credit
rule, the outcome rule, the child environment and the contract line's shape differ.

Rule (frozen by `.ufo/waves/round-75/claims-declaration-r75.md` § C1):

    credit(out, nonce) is True iff the round-72 rule credits AND the LAST parsed
    `MADO_LANDING_WITNESS: <16 hex>` line equals the challenge byte-exactly.
    The contract outcome is green iff the round-72 outcome is green AND the challenge echoed.

The challenge is one `secrets.token_hex(8)` drawn per run (the round-74 ground, S450); the child
receives it in `MADO_LANDING_NONCE` and the standing instrument `quality/landing-counters.sh`
(round-75 generation) echoes it in `MADO_LANDING_WITNESS: <16 hex>`. A captured block from an
earlier run cannot carry the challenge generated now, so a replayed summary with its own
matching detail lines earns neither the kill nor the green outcome.

Printed receipt (last line, exact):

    MADO_R75_LANDING_CONTROLS: selftest=<p/n|none> mz=<pass|fail> mr=<pass|fail> killed=<n>/2 baseline=0/2 witness=<ok|absent|mismatch> verdict=<TARGET_MET|TARGET_MISSED> rev=<sha>

Preceded by the round-72 evidence lines under the `MADO_R75_` prefix, plus one
`MADO_R75_CHALLENGE` line naming the challenge source (never the value in the contract line
nor in the child-env evidence line, which redacts it).

Exit map: 0 iff the extracted instrument's own summary is green with the challenge echoed AND
both frozen defect mutants are killed; 1 iff the measurement ran and the contract was not met;
2 on usage/setup error - reason on stderr, no contract line printed.

Declared limits. The challenge authenticates the run's echo, not the truth of the assertions: a
child that echoes the challenge and reports arithmetic it did not perform still passes the
arithmetic check the harness is built on. The harness scores the extracted instrument at --rev;
the fixture-lane evidence (real `bash` children, one per frozen mode) lives in the round
counter `quality/counters/c1-r75-harness-witness.py`. Wrapping the frozen generation by import
is the generation mechanism: the frozen bytes are read from git, never edited, and the pin makes
a silent edit a setup error.
"""
import argparse
import hashlib
import os
import re
import runpy
import secrets
import sys
import tempfile

TOOL = "c1-r75-landing-controls.py"
R72 = "quality/counters/c1-r72-landing-controls.py"
R72_SHA256 = "b6108c86e8e03befce50256e2381ec08f199a1ab7fe192aeedef70459c45857d"
UNSAFE_ROOTS = ("/tmp", "/var/tmp", "/dev/shm")
WITNESS_RE = re.compile(r"MADO_LANDING_WITNESS: ([0-9a-fA-F]{16})")
SELFTEST_RE = re.compile(
    r"MADO_LANDING_COUNTERS_SELFTEST: (\d+)/(\d+) assertions passed")
CONTRACT_RE = re.compile(
    r"MADO_R75_LANDING_CONTROLS: selftest=(?:[0-9]+/[0-9]+|none) mz=(?:pass|fail) "
    r"mr=(?:pass|fail) killed=[0-2]/2 baseline=0/2 witness=(?:ok|absent|mismatch) "
    r"verdict=(?:TARGET_MET|TARGET_MISSED) rev=[0-9a-f]{40,64}")


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


def last_witness(out):
    """The LAST parsed challenge echo; a malformed later marker cannot suppress a real one."""
    for line in reversed(out.splitlines()):
        m = WITNESS_RE.fullmatch(line.strip())
        if m:
            return m.group(1)
    return None


def witness_state(out, nonce):
    got = last_witness(out)
    if got is None:
        return "absent"
    return "ok" if got == nonce else "mismatch"


def rewrite_prefix(line):
    """The one prefix move: every frozen evidence line reports under the round-75 name."""
    if line.startswith("MADO_R72"):
        return "MADO_R75" + line[len("MADO_R72"):]
    return line


def green_with_witness(r72_green, out, nonce):
    return bool(r72_green(out)) and last_witness(out) == nonce


def credit_with_witness(r72_credit, out, nonce):
    return bool(r72_credit(out)) and last_witness(out) == nonce


def summary_fraction(out):
    for line in reversed(out.splitlines()):
        m = SELFTEST_RE.fullmatch(line.strip())
        if m:
            return "%s/%s" % (m.group(1), m.group(2))
    return "none"


def git_env(home):
    env = {
        "PATH": os.environ.get("PATH", "/usr/bin:/bin"),
        "HOME": home,
        "TMPDIR": home,
        "LC_ALL": "C",
        "GIT_CONFIG_NOSYSTEM": "1",
        "GIT_CONFIG_GLOBAL": os.devnull,
        "GIT_CONFIG_SYSTEM": os.devnull,
        "GIT_TERMINAL_PROMPT": "0",
        "GIT_OPTIONAL_LOCKS": "0",
        "GIT_NO_REPLACE_OBJECTS": "1",
    }
    return env


def load_generation(args, scratch):
    import subprocess
    repo = os.path.abspath(args.repo)
    if not os.path.isdir(repo):
        raise SetupError("--repo is not a directory: %s" % args.repo)
    if not args.rev:
        raise SetupError("--rev is required")
    # R75Sentinel P2: the generation and its home live in a private unpredictable directory
    # beneath the validated scratch root, so a pre-populated shared tree cannot seed a symlink
    # the check-then-open path would follow.
    private = tempfile.mkdtemp(prefix="r75-c1-gen-", dir=scratch)
    home = os.path.join(private, "gen-home")
    os.makedirs(home)
    env = git_env(home)
    r = subprocess.run(["git", "-C", repo, "rev-parse", "--verify", args.rev + "^{commit}"],
                       env=env, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=300)
    if r.returncode != 0:
        raise SetupError("cannot resolve %s: %s" % (args.rev, dec(r.stderr).strip()[:200]))
    sha = dec(r.stdout).strip()
    r = subprocess.run(["git", "-C", repo, "show", "%s:%s" % (sha, R72)],
                       env=env, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=300)
    if r.returncode != 0:
        raise SetupError("%s is absent at %s" % (R72, sha))
    data = r.stdout
    digest = sha256_hex(data)
    if digest != R72_SHA256:
        raise SetupError("frozen generation %s sha256 %s does not match the round-75 pin %s"
                         % (R72, digest, R72_SHA256))
    path = os.path.join(private, "c1-r72-landing-controls.py")
    fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_TRUNC | os.O_NOFOLLOW, 0o600)
    with os.fdopen(fd, "wb") as fh:
        fh.write(data)
    return sha, digest, runpy.run_path(path)


def install_rule(mod, nonce):
    """Install the round-75 rule into the loaded generation's own globals."""
    g = mod["measure"].__globals__
    r72_credit = mod["credit"]
    r72_green = mod["summary_green"]
    base_env = mod["_base_env"]

    def emit(line):
        print(rewrite_prefix(line), flush=True)

    def child_env(home):
        env = dict(base_env(home))
        env["MADO_LANDING_NONCE"] = nonce
        return env

    def contract_line(selftest_out, mz, mr, killed, rev):
        state = witness_state(selftest_out, nonce)
        verdict = "TARGET_MET" if green_with_witness(r72_green, selftest_out, nonce) \
            and killed == 2 else "TARGET_MISSED"
        return ("MADO_R75_LANDING_CONTROLS: selftest=%s mz=%s mr=%s killed=%d/2 baseline=0/2 "
                "witness=%s verdict=%s rev=%s"
                % (summary_fraction(selftest_out), mz, mr, killed, state, verdict, rev))

    base_describe = mod["describe_env"]

    def describe_env(env):
        # The frozen r72 evidence line prints every non-PATH value; the round-75 child env
        # carries the live challenge, so the wrapper redacts that one value (the sentinel's
        # finding at round 75: the challenge is per-run, but a committed log need not carry it).
        redacted = {k: ("<challenge>" if k == "MADO_LANDING_NONCE" else v)
                    for k, v in env.items()}
        return base_describe(redacted)

    g["emit"] = emit
    g["child_env"] = child_env
    g["describe_env"] = describe_env
    g["credit"] = lambda out: credit_with_witness(r72_credit, out, nonce)
    g["summary_green"] = lambda out: green_with_witness(r72_green, out, nonce)
    g["contract_line"] = contract_line


def measure(args):
    scratch = absolute_scratch(args.scratch_root)
    sha, digest, mod = load_generation(args, scratch)
    nonce = secrets.token_hex(8)
    install_rule(mod, nonce)
    print("MADO_R75_CHALLENGE source=secrets.token_hex(8) length=16 generation_sha256=%s rev=%s"
          % (digest, sha), flush=True)
    rc = mod["measure"](args)
    line = None
    return rc


# --------------------------------------------------------------------------------------------- selftest
def selftest(scratch):
    checks = []

    def want(name, cond):
        checks.append((name, bool(cond)))

    want("witness grammar is 16 hex, either case",
         last_witness("MADO_LANDING_WITNESS: deadbeefdeadbeef\n") == "deadbeefdeadbeef"
         and last_witness("MADO_LANDING_WITNESS: DEADBEEFDEADBEEF\n") == "DEADBEEFDEADBEEF")
    want("witness grammar rejects 15 and 17 hex and non-hex",
         last_witness("MADO_LANDING_WITNESS: deadbeefdeadbee\n") is None
         and last_witness("MADO_LANDING_WITNESS: deadbeefdeadbeef0\n") is None
         and last_witness("MADO_LANDING_WITNESS: nothexnothexnotx\n") is None)
    want("the last parsed witness wins",
         last_witness("MADO_LANDING_WITNESS: deadbeefdeadbeef\n"
                      "MADO_LANDING_WITNESS: 0123456789abcdef\n") == "0123456789abcdef")
    want("a malformed trailing marker cannot suppress a real witness",
         last_witness("MADO_LANDING_WITNESS: deadbeefdeadbeef\n"
                      "MADO_LANDING_WITNESS: cleanup complete\n") == "deadbeefdeadbeef")

    nonce = "deadbeefdeadbeef"
    fail_out = ("SELFTEST FAIL 1: a\nSELFTEST FAIL 2: b\n"
                "MADO_LANDING_COUNTERS_SELFTEST: 0/2 assertions passed\n")
    green_out = "MADO_LANDING_COUNTERS_SELFTEST: 2/2 assertions passed\n"
    want("credit accepts the exact echo", credit_with_witness(_r72_credit, fail_out + "MADO_LANDING_WITNESS: " + nonce + "\n", nonce))
    want("credit refuses a stale echo",
         not credit_with_witness(_r72_credit, fail_out + "MADO_LANDING_WITNESS: 0123456789abcdef\n", nonce))
    want("credit refuses an absent echo", not credit_with_witness(_r72_credit, fail_out, nonce))
    want("credit refuses an uppercase echo of a lowercase challenge",
         not credit_with_witness(_r72_credit, fail_out + "MADO_LANDING_WITNESS: DEADBEEFDEADBEEF\n", nonce))
    want("credit refuses the last-wrong pair",
         not credit_with_witness(_r72_credit, fail_out + "MADO_LANDING_WITNESS: " + nonce
                                 + "\nMADO_LANDING_WITNESS: 0123456789abcdef\n", nonce))
    want("credit keeps the round-72 arithmetic",
         not credit_with_witness(_r72_credit, fail_out + "SELFTEST FAIL 3: c\nMADO_LANDING_WITNESS: "
                                  + nonce + "\n", nonce))

    want("the green outcome needs the echo",
         green_with_witness(_r72_green, green_out + "MADO_LANDING_WITNESS: " + nonce + "\n", nonce)
         and not green_with_witness(_r72_green, green_out, nonce))
    want("the prefix move rewrites only evidence lines",
         rewrite_prefix("MADO_R72_MUTANT M-Z killed=yes") == "MADO_R75_MUTANT M-Z killed=yes"
         and rewrite_prefix("SELFTEST FAIL 1: a") == "SELFTEST FAIL 1: a")

    good_ok = ("MADO_R75_LANDING_CONTROLS: selftest=2/2 mz=fail mr=pass killed=1/2 baseline=0/2 "
               "witness=ok verdict=TARGET_MET rev=" + "a" * 40)
    good_no = ("MADO_R75_LANDING_CONTROLS: selftest=2/2 mz=fail mr=pass killed=1/2 baseline=0/2 "
               "witness=absent verdict=TARGET_MISSED rev=" + "a" * 40)
    want("the contract shape carries the witness state",
         CONTRACT_RE.fullmatch(good_ok) is not None and CONTRACT_RE.fullmatch(good_no) is not None)
    want("the contract shape refuses a wrong witness word",
         CONTRACT_RE.fullmatch(good_ok.replace("witness=ok", "witness=maybe")) is None)
    want("the pin is a sha256 hex digest", re.fullmatch(r"[0-9a-f]{64}", R72_SHA256) is not None)

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
    file_path = os.path.join(scratch, "not-a-dir")
    with open(file_path, "w", encoding="utf-8") as fh:
        fh.write("x")
    try:
        absolute_scratch(file_path)
        refused = False
    except UsageError:
        refused = True
    want("scratch refuses a non-directory", refused)

    passed = sum(1 for _n, ok in checks if ok)
    for name, ok in checks:
        if not ok:
            print("MADO_R75_HARNESS_SELFTEST FAIL: %s" % name)
    print("MADO_R75_HARNESS_SELFTEST: %d/%d assertions passed" % (passed, len(checks)))
    return 0 if passed == len(checks) else 1


def _r72_credit(out):
    """The round-72 D1 arithmetic, inlined so the selftest needs no generation load."""
    line = ""
    for candidate in reversed(out.splitlines()):
        if SELFTEST_RE.fullmatch(candidate.strip()):
            line = candidate.strip()
            break
    m = SELFTEST_RE.fullmatch(line)
    if not m:
        return False
    passed, total = int(m.group(1)), int(m.group(2))
    if total <= 0 or passed >= total:
        return False
    fails = sum(1 for candidate in out.splitlines()
                if re.match(r"SELFTEST FAIL [0-9]+: ", candidate))
    return fails == total - passed


def _r72_green(out):
    line = ""
    for candidate in reversed(out.splitlines()):
        if SELFTEST_RE.fullmatch(candidate.strip()):
            line = candidate.strip()
            break
    m = SELFTEST_RE.fullmatch(line)
    if not m:
        return False
    passed, total = int(m.group(1)), int(m.group(2))
    return total > 0 and passed == total


# --------------------------------------------------------------------------------------------- cli
def build_parser():
    parser = argparse.ArgumentParser(prog=TOOL, description=__doc__.splitlines()[0])
    parser.add_argument("--repo")
    parser.add_argument("--rev")
    parser.add_argument("--scratch-root", dest="scratch_root")
    parser.add_argument("--selftest", action="store_true")
    return parser


def main(argv):
    args = build_parser().parse_args(argv)
    try:
        scratch = absolute_scratch(args.scratch_root)
        if args.selftest:
            return selftest(scratch)
        if not args.repo or not args.rev:
            raise UsageError("--repo and --rev are required")
        return measure(args)
    except UsageError as exc:
        sys.stderr.write("%s: %s\n" % (TOOL, exc))
        return 2
    except SetupError as exc:
        sys.stderr.write("%s: %s\n" % (TOOL, exc))
        return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
