#!/usr/bin/env python3
"""Round-68 C1 counter: the control harness must kill its own forged kill credit (claim C1,
attempt 1).

    python3 quality/counters/c1-r68-selfmutants.py --repo . --rev REV --base-rev REV2 \
        --scratch-root DIR
    python3 quality/counters/c1-r68-selfmutants.py --selftest --scratch-root DIR

The scored artifact is `quality/counters/c1-r68-landing-controls.py` at --rev: a harness whose
`--selftest` drives the real measurement body with scripted children, so a mutation of the
kill-credit call sites changes the expected contract line. Three frozen single-point recipes
are applied to a scratch copy of it (each asserted to occur exactly once):

  S1  `mr_killed = bool(`                    ->  `mr_killed = True or bool(`
  S2  `mz_killed = mz_rc != 0`               ->  `mz_killed = True`
  S3  `killed = int(mz_killed) + int(mr_killed)` -> `killed = 2`

A mutant is *killed* iff its own `--selftest` exits nonzero while the unmutated copy exits 0.
The same three recipes are applied to the base harness `quality/counters/c2-r67-landing-
controls.py` at --base-rev (the do-nothing control): a base survivor is a mutant whose
selftest still exits 0 there. A recipe that does not occur exactly once prints `applicable=no` and is
never counted as killed.

Printed receipt (last line, exact):

    MADO_R68_SELFMUTANTS: selftest=<rc|absent> killed=<n>/3 applied=<k>/3 base=<m>/3 verdict=<TARGET_MET|TARGET_MISSED> rev=<sha>

Exit 0 iff the candidate selftest is rc 0 and killed == 3; 1 otherwise; 2 on setup/usage
error. Every write stays under the caller-declared scratch root.
"""
import argparse
import hashlib
import os
import re
import shutil
import subprocess
import sys

TOOL = "c1-r68-selfmutants.py"
CANDIDATE = "quality/counters/c1-r68-landing-controls.py"
BASE_HARNESS = "quality/counters/c2-r67-landing-controls.py"
RECIPES = (
    ("S1", "mr_killed = bool(", "mr_killed = True or bool("),
    ("S2", "mz_killed = mz_rc != 0", "mz_killed = True"),
    ("S3", "killed = int(mz_killed) + int(mr_killed)", "killed = 2"),
)
CONTRACT_RE = re.compile(
    r"MADO_R68_SELFMUTANTS: selftest=(?:[0-9]+|absent) killed=[0-3]/3 applied=[0-3]/3 "
    r"base=[0-3]/3 verdict=(?:TARGET_MET|TARGET_MISSED) rev=[0-9a-f]{40,64}")
UNSAFE_ROOTS = ("/tmp", "/var/tmp", "/dev/shm")


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


def run(argv, cwd=None, timeout=900):
    return subprocess.run(argv, cwd=cwd, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                          env=git_env(), timeout=timeout)


def dec(data):
    return data.decode("utf-8", "replace")


def emit(line):
    print(line, flush=True)


def sha256_hex(data):
    return hashlib.sha256(data).hexdigest()


def absolute_scratch(root):
    if not root:
        raise UsageError("--scratch-root is required")
    path = os.path.abspath(root)
    real = os.path.realpath(path)
    if real in ("/",):
        raise UsageError("unsafe scratch root (filesystem root)")
    for bad in UNSAFE_ROOTS:
        if real == bad or real.startswith(bad + "/"):
            raise UsageError("unsafe scratch root: %s" % real)
    if os.path.exists(path) and not os.path.isdir(path):
        raise UsageError("scratch root is not a directory: %s" % path)
    os.makedirs(path, exist_ok=True)
    return path


def resolve(repo, rev):
    r = run(["git", "-C", repo, "rev-parse", "--verify", "--quiet", "--end-of-options",
             rev + "^{commit}"], cwd=repo)
    if r.returncode != 0:
        raise SetupError("--rev does not resolve to a commit at --repo")
    sha = r.stdout.decode("ascii", "replace").strip()
    if not re.fullmatch(r"[0-9a-f]{40,64}", sha):
        raise SetupError("--rev resolved to an unexpected object name")
    return sha


def blob(repo, sha, path):
    r = run(["git", "-C", repo, "cat-file", "blob", "%s:%s" % (sha, path)], cwd=repo)
    return r.stdout if r.returncode == 0 else None


# --------------------------------------------------------------------------------------------- recipes
def apply_recipe(text, find, replace):
    """Return (mutant text, applied) — exactly-one-occurrence, compiles, differs."""
    count = text.count(find)
    if count != 1:
        return None, count
    mutant = text.replace(find, replace, 1)
    if mutant == text or mutant.count(find) != 0:
        return None, count
    try:
        compile(mutant, "<mutant>", "exec")
    except (SyntaxError, ValueError, TypeError):
        return None, count
    return mutant, count


def selftest_rc(path, work, tag):
    r = run([sys.executable or "python3", "-I", path, "--selftest",
             "--scratch-root", os.path.join(work, "st-" + tag)], cwd=work)
    return r.returncode, dec(r.stdout) + dec(r.stderr)


def score_harness(text, work, tag, sha):
    """Run the unmutated copy and every frozen recipe on one harness text."""
    path = os.path.join(work, "%s.py" % tag)
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(text)
    os.chmod(path, 0o755)
    base_rc, out = selftest_rc(path, work, tag)
    emit("MADO_R68_SELFTEST_FIXTURE harness=%s sha256=%s rc=%d assertions=%s"
         % (tag, sha256_hex(text.encode("utf-8")), base_rc,
            (re.search(r"SELFTEST: ([0-9]+/[0-9]+)", out).group(1)
             if re.search(r"SELFTEST: ([0-9]+/[0-9]+)", out) else "none")))
    killed = applied = 0
    survivors = []
    for name, find, replace in RECIPES:
        mutant, count = apply_recipe(text, find, replace)
        if mutant is None:
            emit("MADO_R68_SELF_MUTANT harness=%s recipe=%s find=%r occurrences=%d "
                 "applicable=no killed=no" % (tag, name, find, count))
            continue
        applied += 1
        mpath = os.path.join(work, "%s-%s.py" % (tag, name))
        with open(mpath, "w", encoding="utf-8") as fh:
            fh.write(mutant)
        os.chmod(mpath, 0o755)
        rc, mout = selftest_rc(mpath, work, "%s-%s" % (tag, name))
        died = rc != 0
        killed += int(died)
        if not died:
            survivors.append(name)
        emit("MADO_R68_SELF_MUTANT harness=%s recipe=%s find=%r occurrences=%d "
             "recipe_sha256=%s rc=%d assertions=%s applicable=yes killed=%s"
             % (tag, name, find, count, sha256_hex(mutant.encode("utf-8")), rc,
                (re.search(r"SELFTEST: ([0-9]+/[0-9]+)", mout).group(1)
                 if re.search(r"SELFTEST: ([0-9]+/[0-9]+)", mout) else "none"),
                "yes" if died else "no"))
    return {"rc": base_rc, "killed": killed, "applied": applied, "survivors": survivors}


def measure(args):
    scratch = absolute_scratch(args.scratch_root)
    if not args.repo or not args.rev:
        raise UsageError("--repo and --rev are required")
    repo = os.path.abspath(args.repo)
    if not os.path.isdir(repo):
        raise SetupError("--repo is not a directory: %s" % repo)
    work = os.path.join(scratch, "r68-c1")
    shutil.rmtree(work, ignore_errors=True)
    os.makedirs(work)
    sha = resolve(repo, args.rev)
    cand_bytes = blob(repo, sha, CANDIDATE)
    result = {"rc": "absent", "killed": 0, "applied": 0, "survivors": list("S1 S2 S3".split())}
    if cand_bytes is not None:
        emit("MADO_R68_EXTRACT path=%s bytes=%d sha256=%s"
             % (CANDIDATE, len(cand_bytes), sha256_hex(cand_bytes)))
        result = score_harness(dec(cand_bytes), work, "candidate", sha)
    else:
        emit("MADO_R68_EXTRACT path=%s state=absent rev=%s" % (CANDIDATE, sha))

    base_killed = 0
    if args.base_rev:
        bsha = resolve(repo, args.base_rev)
        base_bytes = blob(repo, bsha, BASE_HARNESS)
        if base_bytes is None:
            raise SetupError("%s absent at --base-rev %s" % (BASE_HARNESS, bsha))
        emit("MADO_R68_BASE_EXTRACT path=%s bytes=%d sha256=%s rev=%s"
             % (BASE_HARNESS, len(base_bytes), sha256_hex(base_bytes), bsha))
        base = score_harness(dec(base_bytes), work, "base", bsha)
        base_killed = base["killed"]
        emit("MADO_R68_BASE_CONTROL survivors=%s killed=%d/%d applied=%d"
             % (",".join(base["survivors"]) or "none", base_killed, len(RECIPES),
                base["applied"]))

    met = result["rc"] == 0 and result["killed"] == len(RECIPES)
    line = ("MADO_R68_SELFMUTANTS: selftest=%s killed=%d/%d applied=%d/%d base=%d/%d "
            "verdict=%s rev=%s"
            % (result["rc"], result["killed"], len(RECIPES), result["applied"],
               len(RECIPES), base_killed, len(RECIPES),
               "TARGET_MET" if met else "TARGET_MISSED", sha))
    if not CONTRACT_RE.fullmatch(line):
        raise SetupError("emitted contract line does not match CONTRACT_RE")
    emit(line)
    return 0 if met else 1


# --------------------------------------------------------------------------------------------- selftest
SYNTH = "".join([
    "mr_killed = bool(a and b)\n",
    "mz_killed = mz_rc != 0\n",
    "killed = int(mz_killed) + int(mr_killed)\n",
])


def _selftest_checks():
    checks = []

    def want(name, cond):
        checks.append((name, bool(cond)))

    for name, find, replace in RECIPES:
        mutant, count = apply_recipe(SYNTH, find, replace)
        want("recipe %s applies exactly once" % name, count == 1 and mutant is not None)
        want("recipe %s removes its target text" % name,
             mutant is not None and find not in mutant)
        want("recipe %s is deterministic" % name,
             apply_recipe(SYNTH, find, replace)[0] == mutant)
        want("recipe %s refuses an absent target" % name,
             apply_recipe("x = 1\n", find, replace) == (None, 0))
        want("recipe %s refuses a duplicated target" % name,
             apply_recipe(SYNTH + find + "\n", find, replace)[0] is None)
    want("base harness text keeps the S1 target", "mr_killed = bool(" in SYNTH)
    want("contract line matches the frozen shape",
         CONTRACT_RE.fullmatch(
             "MADO_R68_SELFMUTANTS: selftest=0 killed=3/3 applied=3/3 base=0/3 "
             "verdict=TARGET_MET rev=" + "a" * 40) is not None)
    want("contract line renders an absent candidate",
         CONTRACT_RE.fullmatch(
             "MADO_R68_SELFMUTANTS: selftest=absent killed=0/3 applied=0/3 base=0/3 "
             "verdict=TARGET_MISSED rev=" + "a" * 40) is not None)
    want("emitted-line check accepts the met line",
         CONTRACT_RE.fullmatch("MADO_R68_SELFMUTANTS: selftest=0 killed=3/3 applied=3/3 "
                               "base=0/3 verdict=TARGET_MET rev=" + "a" * 40) is not None)
    want("contract line refuses an out-of-range kill count",
         CONTRACT_RE.fullmatch(
             "MADO_R68_SELFMUTANTS: selftest=0 killed=4/3 applied=3/3 base=0/3 "
             "verdict=TARGET_MET rev=" + "a" * 40) is None)
    want("sha256 helper matches the empty digest",
         sha256_hex(b"") == "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855")
    for bad in ("", "/", "/tmp", "/tmp/x", "/var/tmp/x", "/dev/shm/x"):
        try:
            absolute_scratch(bad)
            ok = False
        except UsageError:
            ok = True
        want("scratch refuses %r" % (bad or "<empty>"), ok)
    return checks


def selftest():
    real_run = subprocess.run
    spawned = []

    def forbid(*a, **k):
        spawned.append(a)
        raise AssertionError("selftest must not spawn")

    subprocess.run = forbid
    try:
        checks = _selftest_checks()
    finally:
        subprocess.run = real_run
    passed = sum(1 for _n, ok in checks if ok)
    for name, ok in checks:
        if not ok:
            print("MADO_R68_SELF_SELFTEST FAIL: %s" % name)
    print("MADO_R68_SELFMUTANTS_SELFTEST: %d/%d assertions passed" % (passed, len(checks)))
    if spawned:
        print("MADO_R68_SELF_SELFTEST FAIL: spawned=%d" % len(spawned))
        return 1
    return 0 if passed == len(checks) else 1


# --------------------------------------------------------------------------------------------- cli
def main(argv=None):
    ap = argparse.ArgumentParser(prog=TOOL, description=__doc__.splitlines()[0])
    ap.add_argument("--repo")
    ap.add_argument("--rev")
    ap.add_argument("--base-rev")
    ap.add_argument("--scratch-root")
    ap.add_argument("--selftest", action="store_true")
    args = ap.parse_args(argv)
    try:
        if args.selftest:
            return selftest()
        return measure(args)
    except UsageError as exc:
        print("%s: usage error: %s" % (TOOL, exc), file=sys.stderr)
        return 2
    except SetupError as exc:
        print("%s: setup error: %s" % (TOOL, exc), file=sys.stderr)
        return 2
    except (OSError, subprocess.SubprocessError) as exc:
        print("%s: setup error: %s" % (TOOL, type(exc).__name__), file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
