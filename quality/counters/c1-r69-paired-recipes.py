#!/usr/bin/env python3
r"""Round-69 C1 counter: the hardened control harness must kill its own paired forgeries
(claim C1, attempt 1).

    python3 quality/counters/c1-r69-paired-recipes.py --repo . --rev REV --base-rev BASE \
        --scratch-root DIR
    python3 quality/counters/c1-r69-paired-recipes.py --selftest --scratch-root DIR

Scored artifact: `quality/counters/c1-r69-landing-controls.py` at --rev (a harness whose
`--selftest` drives the real measurement body with scripted children AND pairs each decision
with its oracle: a crashing M-R child is not a kill, an M-Z run with no assertion summary is
not a kill, and the hermetic spawn guard is asserted live). Three frozen single-point recipes
are applied to a scratch copy of it (each asserted to occur exactly once):

  R1  `mr_killed = bool(u_ok and not control_ok(mr_rc, mr_marker)` + continuation
      `and forged_credit(mr_rc, mr_marker))`
      ->  `mr_killed = bool(u_ok and not control_ok(mr_rc, mr_marker))`
  R2  `mz_killed = mz_rc != 0`
      ->  `mz_killed = mz_rc != 0 or mz_summary == "none"`
  R3  `subprocess.run = _no_spawn`
      ->  `pass  # spawn guard removed by recipe`

A mutant is *killed* iff its own `--selftest` exits nonzero while the unmutated copy exits 0.
The same three recipes are applied at --base-rev to the round-68 harness
`quality/counters/c1-r68-landing-controls.py` (the do-nothing control): it must survive all
three, so the claimed work — not the recipe text — is what earns the score. A recipe whose text
does not occur exactly once is `applicable=no` and is never counted as killed.

Frozen by `.ufo/waves/round-69/claims-declaration-r69.md`; do-nothing receipts in
`.ufo/waves/round-69/control-baseline-r69.txt`.

Printed receipt (last line, exact):

    MADO_R69_PAIRED_RECIPES: selftest=<rc|absent> killed=<n>/3 applied=<k>/3 base=<m>/3 verdict=<TARGET_MET|TARGET_MISSED> rev=<sha>

Exit 0 iff the candidate selftest is rc 0, killed == 3, applied == 3 and base == 0; 1
otherwise; 2 on setup/usage error. Every write stays under the caller-declared scratch root.
"""
import argparse
import hashlib
import os
import re
import shutil
import subprocess
import sys

TOOL = "c1-r69-paired-recipes.py"
CANDIDATE = "quality/counters/c1-r69-landing-controls.py"
BASE_HARNESS = "quality/counters/c1-r68-landing-controls.py"
R1_OLD = ("            mr_killed = bool(u_ok and not control_ok(mr_rc, mr_marker)\n"
          "                             and forged_credit(mr_rc, mr_marker))")
R1_NEW = "            mr_killed = bool(u_ok and not control_ok(mr_rc, mr_marker))"
RECIPES = (
    ("R1", R1_OLD, R1_NEW),
    ("R2", "mz_killed = mz_rc != 0", 'mz_killed = mz_rc != 0 or mz_summary == "none"'),
    ("R3", "subprocess.run = _no_spawn", "pass  # spawn guard removed by recipe"),
)
CANDIDATE_PATH = CANDIDATE
BASE_PATH = BASE_HARNESS
UNSAFE_ROOTS = ("/tmp", "/var/tmp", "/dev/shm")
CONTRACT_RE = re.compile(
    r"MADO_R69_PAIRED_RECIPES: selftest=(?:[0-9]+|absent) killed=[0-3]/3 applied=[0-3]/3 "
    r"base=[0-3]/3 verdict=(?:TARGET_MET|TARGET_MISSED) rev=[0-9a-f]{40,64}")


class UsageError(Exception):
    pass


class SetupError(Exception):
    pass


# --------------------------------------------------------------------------------------------- env
def git_env():
    """Object reads only: every inherited GIT_* dropped, replacements ignored."""
    env = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}
    env["GIT_OPTIONAL_LOCKS"] = "0"
    env["GIT_NO_REPLACE_OBJECTS"] = "1"
    env["LC_ALL"] = "C"
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


# --------------------------------------------------------------------------------------------- measurement
def git(repo, args, timeout=900):
    r = run(["git", "-C", repo] + list(args), cwd=repo, timeout=timeout)
    return r


def rev_parse(repo, rev):
    r = git(repo, ["rev-parse", "--verify", rev + "^{commit}"])
    if r.returncode != 0:
        raise SetupError("cannot resolve --rev %s: %s" % (rev, dec(r.stderr).strip()[:200]))
    return dec(r.stdout).strip()


def extract(repo, sha, path):
    """Bytes of <path> at <sha>, or None when the path is absent there."""
    r = git(repo, ["show", "%s:%s" % (sha, path)])
    if r.returncode != 0:
        return None
    return r.stdout


def write_file(path, data):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "wb") as fh:
        fh.write(data)


def candidate_selftest(path, scratch):
    r = run([sys.executable, "-I", path, "--selftest", "--scratch-root", scratch], timeout=900)
    return r.returncode, dec(r.stdout) + dec(r.stderr)


def mutation_score(tree, source, scratch, label):
    """Apply every recipe once to `source`; return (killed, applied, details)."""
    killed = applied = 0
    details = []
    for name, old, new in RECIPES:
        count = source.count(old)
        detail = {"recipe": name, "occurrences": count, "applied": False,
                  "killed": False, "rc": None, "sha256": "absent"}
        if count != 1:
            emit("MADO_R69_RECIPE label=%s recipe=%s occurrences=%d applicable=no"
                 % (label, name, count))
            details.append(detail)
            continue
        applied += 1
        mutant = source.replace(old, new, 1)
        path = os.path.join(tree, "mut-%s-%s.py" % (label, name))
        write_file(path, mutant.encode("utf-8"))
        compile_run = run([sys.executable, "-I", "-m", "py_compile", path], timeout=300)
        if compile_run.returncode != 0:
            emit("MADO_R69_MUTANT label=%s recipe=%s occurrences=1 compiles=no killed=no "
                 "note=a syntax break is not a semantic kill" % (label, name))
            detail["compiles"] = False
            details.append(detail)
            continue
        rc, out = candidate_selftest(path, os.path.join(scratch, "st-%s-%s" % (label, name)))
        detail.update({"applied": True, "rc": rc, "killed": rc != 0,
                       "sha256": sha256_hex(mutant.encode("utf-8"))})
        killed += int(rc != 0)
        emit("MADO_R69_MUTANT label=%s recipe=%s occurrences=1 rc=%d killed=%s sha256=%s line=%s"
             % (label, name, rc, "yes" if rc != 0 else "no", detail["sha256"],
                (out.strip().splitlines() or ["none"])[-1][:160]))
        details.append(detail)
    return killed, applied, details


def contract_line(selftest_rc, killed, applied, base, sha):
    return ("MADO_R69_PAIRED_RECIPES: selftest=%s killed=%d/3 applied=%d/3 base=%d/3 "
            "verdict=%s rev=%s"
            % ("absent" if selftest_rc is None else selftest_rc, killed, applied, base,
               "TARGET_MET" if verdict_met(selftest_rc, killed, applied, base) else "TARGET_MISSED",
               sha))


def verdict_met(selftest_rc, killed, applied, base):
    return selftest_rc == 0 and killed == 3 and applied == 3 and base == 0


def measure(args):
    repo = os.path.abspath(args.repo)
    if not os.path.isdir(repo):
        raise SetupError("--repo is not a directory: %s" % args.repo)
    scratch = absolute_scratch(args.scratch_root)
    work = os.path.join(scratch, "r69-c1-paired")
    if os.path.isdir(work):
        shutil.rmtree(work)
    tree = os.path.join(work, "tree")
    os.makedirs(tree)

    sha = rev_parse(repo, args.rev)
    base_rev = args.base_rev or sha
    base_sha = rev_parse(repo, base_rev)

    candidate = extract(repo, sha, CANDIDATE_PATH)
    selftest_rc = None
    killed = applied = 0
    if candidate is None:
        emit("MADO_R69_EXTRACT path=%s present=no sha256=absent" % CANDIDATE_PATH)
    else:
        emit("MADO_R69_EXTRACT path=%s present=yes bytes=%d sha256=%s"
             % (CANDIDATE_PATH, len(candidate), sha256_hex(candidate)))
        path = os.path.join(tree, "candidate.py")
        write_file(path, candidate)
        selftest_rc, out = candidate_selftest(path, os.path.join(scratch, "st-candidate"))
        emit("MADO_R69_SELFTEST instrument=%s rc=%d line=%s"
             % (CANDIDATE_PATH, selftest_rc, (out.strip().splitlines() or ["none"])[-1][:160]))
        killed, applied, _ = mutation_score(tree, dec(candidate), scratch, "candidate")

    base = extract(repo, base_sha, BASE_PATH)
    if base is None:
        emit("MADO_R69_EXTRACT path=%s present=no sha256=absent" % BASE_PATH)
        raise SetupError("the base harness %s is absent at --base-rev %s: the do-nothing leg "
                         "cannot be run, so no verdict is claimed" % (BASE_PATH, base_sha))
    else:
        emit("MADO_R69_EXTRACT path=%s present=yes bytes=%d sha256=%s"
             % (BASE_PATH, len(base), sha256_hex(base)))
        base_tree = os.path.join(work, "base")
        os.makedirs(base_tree, exist_ok=True)
        base_killed, base_applied, _ = mutation_score(base_tree, dec(base), scratch, "base")
        emit("MADO_R69_BASE killed=%d/3 applied=%d/3 (the r68 harness must survive all three)"
             % (base_killed, base_applied))
    line = contract_line(selftest_rc, killed, applied, base_killed, sha)
    if not CONTRACT_RE.fullmatch(line):
        raise SetupError("emitted contract line does not match CONTRACT_RE")
    emit(line)
    return 0 if verdict_met(selftest_rc, killed, applied, base_killed) else 1


# --------------------------------------------------------------------------------------------- selftest
STUB_HARNESS = (
    "def measure():\n"
    + R1_OLD + "\n"
    "        mz_killed = mz_rc != 0\n"
    "        return killed\n"
    "\n"
    "def selftest():\n"
    "    subprocess.run = _no_spawn\n"
    "    return 0\n"
)


def _scripted_run(case, sha):
    """Stand-in for `run`: answers every argv the measurement issues, spawns nothing."""
    state = {"compiles": 0}

    def fake(argv, cwd=None, timeout=900):
        a = [str(x) for x in argv]
        out = b""
        rc = 0
        if a[0] == "git":
            joined = " ".join(a)
            if "rev-parse" in a and "--verify" in joined:
                out = (sha + "\n").encode()
            elif "show" in a:
                path = a[-1].split(":", 1)[-1]
                if path == CANDIDATE_PATH:
                    if case["candidate"] is None:
                        rc = 128
                        out = b"fatal: path does not exist in HEAD\n"
                    else:
                        out = case["candidate"].encode()
                elif path == BASE_PATH:
                    if case["base"] is None:
                        rc = 128
                    else:
                        out = case["base"].encode()
                else:
                    rc = 128
            else:
                rc = 1
        elif os.path.basename(a[0]).startswith("python"):
            joined = " ".join(a)
            if "py_compile" in a:
                rc = case.get("compile_rc", 0) if state["compiles"] == 0 else 0
                state["compiles"] += 1
            elif "/base/" in joined:
                rc = case["base_rc"]
            elif "mut-" in joined:
                rc = case["mutant_rc"]
            else:
                rc = case["candidate_rc"]
            out = b"MADO_R69_LANDING_CONTROLS_SELFTEST: 1/1 assertions passed\n"
        else:
            rc = 127
        return subprocess.CompletedProcess(args=a, returncode=rc, stdout=out, stderr=b"")
    return fake


def _measure_case(scratch, case, sha):
    args = argparse.Namespace(repo=scratch, rev="HEAD", base_rev="BASE",
                              scratch_root=os.path.join(scratch, "case-" + case["name"]))
    os.makedirs(args.scratch_root, exist_ok=True)
    saved = globals()["run"]
    globals()["run"] = _scripted_run(case, sha)
    buf = []
    try:
        old_stdout = sys.stdout

        class _Capture(object):
            def write(self, text):
                buf.append(text)
                return len(text)

            def flush(self):
                pass
        sys.stdout = _Capture()
        try:
            rc = measure(args)
        finally:
            sys.stdout = old_stdout
    finally:
        globals()["run"] = saved
    lines = [ln for ln in "".join(buf).splitlines()
             if ln.startswith("MADO_R69_PAIRED_RECIPES:")]
    return rc, (lines[-1] if lines else "none")


def _selftest_checks(scratch):
    checks = []

    def want(name, cond):
        checks.append((name, bool(cond)))

    sha = "a" * 40
    happy = {"name": "happy", "candidate": STUB_HARNESS, "base": STUB_HARNESS,
             "candidate_rc": 0, "mutant_rc": 1, "base_rc": 0}
    rc, line = _measure_case(scratch, happy, sha)
    want("scripted happy path prints the met line",
         line == ("MADO_R69_PAIRED_RECIPES: selftest=0 killed=3/3 applied=3/3 base=0/3 "
                  "verdict=TARGET_MET rev=" + sha))
    want("scripted happy path exits 0", rc == 0)

    survivors = {"name": "survivors", "candidate": STUB_HARNESS, "base": STUB_HARNESS,
                 "candidate_rc": 0, "mutant_rc": 0, "base_rc": 0}
    rc2, line2 = _measure_case(scratch, survivors, sha)
    want("a surviving recipe is not a kill",
         line2 == ("MADO_R69_PAIRED_RECIPES: selftest=0 killed=0/3 applied=3/3 base=0/3 "
                   "verdict=TARGET_MISSED rev=" + sha))
    want("survivor path exits 1", rc2 == 1)

    shorter = STUB_HARNESS.replace("subprocess.run = _no_spawn\n", "")
    inapplicable = {"name": "inapplicable", "candidate": shorter, "base": STUB_HARNESS,
                    "candidate_rc": 0, "mutant_rc": 1, "base_rc": 0}
    rc3, line3 = _measure_case(scratch, inapplicable, sha)
    want("a recipe that does not occur exactly once is not applicable",
         line3 == ("MADO_R69_PAIRED_RECIPES: selftest=0 killed=2/3 applied=2/3 base=0/3 "
                   "verdict=TARGET_MISSED rev=" + sha))
    want("inapplicable path exits 1", rc3 == 1)

    absent = {"name": "absent", "candidate": None, "base": STUB_HARNESS,
              "candidate_rc": 0, "mutant_rc": 1, "base_rc": 0}
    rc4, line4 = _measure_case(scratch, absent, sha)
    want("an absent candidate harness is not a pass",
         line4 == ("MADO_R69_PAIRED_RECIPES: selftest=absent killed=0/3 applied=0/3 base=0/3 "
                   "verdict=TARGET_MISSED rev=" + sha))
    want("absent path exits 1", rc4 == 1)

    base_hurt = {"name": "base-hurt", "candidate": STUB_HARNESS, "base": STUB_HARNESS,
                 "candidate_rc": 0, "mutant_rc": 1, "base_rc": 1}
    rc5, line5 = _measure_case(scratch, base_hurt, sha)
    want("a base-leg kill blocks the target (the do-nothing control must survive)",
         line5 == ("MADO_R69_PAIRED_RECIPES: selftest=0 killed=3/3 applied=3/3 base=3/3 "
                   "verdict=TARGET_MISSED rev=" + sha))
    want("base-hurt path exits 1", rc5 == 1)

    red = {"name": "red", "candidate": STUB_HARNESS, "base": STUB_HARNESS,
           "candidate_rc": 1, "mutant_rc": 1, "base_rc": 0}
    rc6, line6 = _measure_case(scratch, red, sha)
    want("a red candidate selftest is not a pass",
         line6 == ("MADO_R69_PAIRED_RECIPES: selftest=1 killed=3/3 applied=3/3 base=0/3 "
                   "verdict=TARGET_MISSED rev=" + sha))
    want("red path exits 1", rc6 == 1)

    broken = {"name": "compile-red", "candidate": STUB_HARNESS, "base": STUB_HARNESS,
              "candidate_rc": 0, "mutant_rc": 1, "base_rc": 0, "compile_rc": 1}
    rc7, line7 = _measure_case(scratch, broken, sha)
    want("a mutant that does not compile is not credited as a kill",
         line7 == ("MADO_R69_PAIRED_RECIPES: selftest=0 killed=2/3 applied=3/3 base=0/3 "
                   "verdict=TARGET_MISSED rev=" + sha))
    want("compile-red path exits 1", rc7 == 1)
    want("every scripted contract line matches the frozen shape",
         all(CONTRACT_RE.fullmatch(x) is not None
             for x in (line, line2, line3, line4, line5, line6, line7)))
    want("contract line refuses a wrong verdict word",
         not CONTRACT_RE.fullmatch(
             "MADO_R69_PAIRED_RECIPES: selftest=0 killed=3/3 applied=3/3 base=0/3 "
             "verdict=DONE rev=" + "a" * 40))
    want("verdict requires the candidate selftest green", not verdict_met(1, 3, 3, 0))
    want("verdict requires all three kills", not verdict_met(0, 2, 3, 0))
    want("verdict requires every recipe applied", not verdict_met(0, 3, 2, 0))
    want("verdict requires the base leg to survive", not verdict_met(0, 3, 3, 1))
    want("verdict met on the frozen target", verdict_met(0, 3, 3, 0))
    absent_base = {"name": "absent-base", "candidate": STUB_HARNESS, "base": None,
                   "candidate_rc": 0, "mutant_rc": 1, "base_rc": 0}
    want("an absent base harness is a setup refusal, never a pass",
         _raises(SetupError, lambda: _measure_case(scratch, absent_base, sha)))
    parsed = build_parser().parse_args(["--repo", ".", "--rev", "HEAD", "--scratch-root", "x"])
    want("--base-rev is not silently defaulted", parsed.base_rev is None)

    frozen = ["--repo", ".", "--rev", "HEAD", "--base-rev", "BASE",
              "--scratch-root", "/scratch/dir"]
    try:
        parsed = build_parser().parse_args(frozen)
        parsed_ok = (parsed.scratch_root == "/scratch/dir" and parsed.base_rev == "BASE")
    except SystemExit:
        parsed_ok = False
    want("the frozen counting command's argument set parses", parsed_ok)
    want("every recipe text occurs exactly once in the stub harness",
         all(STUB_HARNESS.count(old) == 1 for _name, old, _new in RECIPES))
    return checks


def selftest(scratch):
    """Hermetic: every subprocess spawn raises, so the check body must stay pure."""
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
            checks.extend(_selftest_checks(scratch))
        except AssertionError:
            checks.append(("selftest body must not spawn a process", False))
    finally:
        subprocess.run = saved_run
    passed = sum(1 for _name, ok in checks if ok)
    for name, ok in checks:
        if not ok:
            print("MADO_R69_PAIRED_RECIPES_SELFTEST FAIL: %s" % name)
    print("MADO_R69_PAIRED_RECIPES_SELFTEST: %d/%d assertions passed" % (passed, len(checks)))
    return 0 if passed == len(checks) else 1


def _raises(exc_type, fn):
    try:
        fn()
    except exc_type:
        return True
    except Exception:
        return False
    return False


# --------------------------------------------------------------------------------------------- cli
def build_parser():
    parser = argparse.ArgumentParser(prog=TOOL, description=__doc__.splitlines()[0])
    parser.add_argument("--repo")
    parser.add_argument("--rev")
    parser.add_argument("--base-rev", default=None)
    parser.add_argument("--scratch-root")
    parser.add_argument("--selftest", action="store_true")
    return parser


def main(argv):
    args = build_parser().parse_args(argv)
    try:
        scratch = absolute_scratch(args.scratch_root)
        if args.selftest:
            return selftest(scratch)
        if not args.repo or not args.rev or not args.base_rev:
            raise UsageError("--repo, --rev and --base-rev are required")
        return measure(args)
    except UsageError as exc:
        sys.stderr.write("%s: %s\n" % (TOOL, exc))
        return 2
    except SetupError as exc:
        sys.stderr.write("%s: %s\n" % (TOOL, exc))
        return 2
    except (OSError, subprocess.SubprocessError) as exc:
        sys.stderr.write("%s: setup failure: %s\n" % (TOOL, exc))
        return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
