#!/usr/bin/env python3
"""Round-69 C1 paired-recipe counter: does the r69 control harness kill the three frozen
paired (decision + oracle) forgeries, and does the r68 harness survive the same three?

    python3 quality/counters/c1-r69-paired-recipes.py --repo . --rev REV \
        --base-rev 04093b83f73a841117d3b31dbb2a6063f4f2a454 --scratch-root DIR
    python3 quality/counters/c1-r69-paired-recipes.py --selftest --scratch-root DIR

Exit 0 iff the extracted r69 harness's own --selftest is rc 0, all three frozen recipes
apply exactly once and each mutant's own --selftest exits nonzero (killed=3/3), and the
round-68 harness at --base-rev survives all three (base=0/3); 1 otherwise; 2 on usage or
setup error (reason on stderr).

What one measurement does (every write stays under the caller-declared scratch root):

  extract   quality/counters/c1-r69-landing-controls.py at --rev with a scrubbed git env
            (GIT_OPTIONAL_LOCKS=0, GIT_NO_REPLACE_OBJECTS=1, every inherited GIT_* dropped),
            so a planted refs/replace object in --repo cannot forge the extracted bytes.
  selftest  run the extracted harness `--selftest`: `selftest=<rc>`, or `absent` when the
            path does not exist at --rev.
  R1/R2/R3  apply each frozen recipe exactly once to a fresh scratch copy of the same bytes
            (the text must occur exactly once before mutating; otherwise `applicable=no` and
            the recipe is never counted killed); a mutant is killed iff its own `--selftest`
            exits nonzero.
  base      extract quality/counters/c1-r68-landing-controls.py at --base-rev, apply the
            same three recipes, and count the kills there (`base=<m>/3`); the round-68
            harness must survive all three.

Printed receipt (last line, exact):

    MADO_R69_PAIRED_RECIPES: selftest=<rc|absent> killed=<n>/3 applied=<k>/3 base=<m>/3 verdict=<TARGET_MET|TARGET_MISSED> rev=<sha>

Preceded by one `MADO_R69_*` evidence line per extraction, recipe, mutant (with its sha256)
and base mutant. `--selftest` is hermetic: it drives the real `measure()` body with scripted
children by patching the module-level `run`, spawns nothing (`subprocess.run` raises for the
whole check body), touches only <scratch-root>, and refuses /tmp-family or symlinked roots.
"""
import argparse
import contextlib
import hashlib
import io
import os
import re
import shutil
import subprocess
import sys

TOOL = "c1-r69-paired-recipes.py"
CANDIDATE = "quality/counters/c1-r69-landing-controls.py"
BASE = "quality/counters/c1-r68-landing-controls.py"
SCORE = 3
UNSAFE_ROOTS = ("/tmp", "/var/tmp", "/dev/shm")
BASE_ENV_KEYS = (
    "PATH", "HOME", "TMPDIR", "LC_ALL",
    "GIT_CONFIG_NOSYSTEM", "GIT_CONFIG_GLOBAL", "GIT_CONFIG_SYSTEM",
    "GIT_TERMINAL_PROMPT",
)

# Frozen recipes, byte for byte (declaration § C1). Both harnesses carry each text once.
R1_OLD = (b"            mr_killed = bool(u_ok and not control_ok(mr_rc, mr_marker)\n"
          b"                             and forged_credit(mr_rc, mr_marker))")
R1_NEW = b"            mr_killed = bool(u_ok and not control_ok(mr_rc, mr_marker))"
R2_OLD = b"        mz_killed = mz_rc != 0"
R2_NEW = b'        mz_killed = mz_rc != 0 or mz_summary == "none"'
R3_OLD = b"    subprocess.run = _no_spawn"
R3_NEW = b"    pass  # spawn guard removed by recipe"
RECIPES = (
    ("R1", R1_OLD, R1_NEW),
    ("R2", R2_OLD, R2_NEW),
    ("R3", R3_OLD, R3_NEW),
)
CONTRACT_RE = re.compile(
    r"MADO_R69_PAIRED_RECIPES: selftest=(?:[0-9]+|absent) killed=[0-3]/3 applied=[0-3]/3 "
    r"base=[0-3]/3 verdict=(?:TARGET_MET|TARGET_MISSED) rev=[0-9a-f]{40,64}"
)


class UsageError(Exception):
    pass


class SetupError(Exception):
    pass


class RecipeError(Exception):
    pass


# --------------------------------------------------------------------------------------------- env
def _base_env(home):
    return {
        "PATH": os.environ.get("PATH", "/usr/bin:/bin"),
        "HOME": home,
        "TMPDIR": home,
        "LC_ALL": "C",
        "GIT_CONFIG_NOSYSTEM": "1",
        "GIT_CONFIG_GLOBAL": os.devnull,
        "GIT_CONFIG_SYSTEM": os.devnull,
        "GIT_TERMINAL_PROMPT": "0",
    }


def git_env(home):
    """Guarded env for object reads: no inherited GIT_*, local replacements ignored."""
    env = _base_env(home)
    env["GIT_OPTIONAL_LOCKS"] = "0"
    env["GIT_NO_REPLACE_OBJECTS"] = "1"
    return env


def child_env(home):
    """Exact env handed to a child under test: inherited GIT_* scrubbed."""
    return _base_env(home)


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


# --------------------------------------------------------------------------------------------- process
def run(argv, env, cwd=None, input_bytes=None, timeout=900):
    return subprocess.run(argv, cwd=cwd, env=env, input=input_bytes,
                          stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=timeout)


def dec(data):
    return data.decode("utf-8", "replace")


def emit(line):
    print(line, flush=True)


def write_file(path, data):
    parent = os.path.dirname(path)
    if parent:
        os.makedirs(parent, exist_ok=True)
    with open(path, "wb") as fh:
        fh.write(data)
    os.chmod(path, 0o755 if path.endswith((".py", ".sh")) else 0o644)


def sha256_hex(data):
    return hashlib.sha256(data).hexdigest()


def assertion_fraction(out):
    """The last `<TOOL>_SELFTEST: n/m assertions passed` fraction, else `none`."""
    hit = "none"
    for line in out.splitlines():
        if "SELFTEST:" in line and "assertions passed" in line:
            m = re.search(r"(\d+/\d+)", line)
            if m:
                hit = m.group(1)
    return hit


# --------------------------------------------------------------------------------------------- extract
def resolve_rev(repo, rev, home):
    if not rev or rev.startswith("-"):
        raise SetupError("invalid rev")
    r = run(["git", "-C", repo, "rev-parse", "--verify", "--quiet", "--end-of-options",
             rev + "^{commit}"], env=git_env(home), cwd=repo)
    if r.returncode != 0:
        raise SetupError("rev does not resolve to a commit at --repo")
    sha = r.stdout.decode("ascii", "replace").strip()
    if not re.fullmatch(r"[0-9a-f]{40,64}", sha):
        raise SetupError("rev resolved to an unexpected object name")
    top = run(["git", "-C", repo, "rev-parse", "--show-toplevel"], env=git_env(home), cwd=repo)
    if top.returncode != 0:
        raise SetupError("--repo is not a git work tree")
    if os.path.realpath(top.stdout.decode("utf-8", "replace").strip()) != os.path.realpath(repo):
        raise SetupError("--repo is not the repository root")
    return sha


def path_present(repo, sha, rel, home):
    """True iff `rel` is a blob at `sha`; a missing path is absent, a read failure is setup."""
    probe = run(["git", "-C", repo, "cat-file", "-e", "%s:%s" % (sha, rel)],
                env=git_env(home), cwd=repo)
    if probe.returncode == 0:
        return True
    listed = run(["git", "-C", repo, "ls-tree", "-r", "--name-only", sha, "--", rel],
                 env=git_env(home), cwd=repo)
    if listed.returncode != 0:
        raise SetupError("cannot read the tree at %s" % sha)
    if listed.stdout.strip():
        raise SetupError("%s exists at %s but cannot be read" % (rel, sha))
    return False


def extract_blob(repo, sha, rel, home):
    r = run(["git", "-C", repo, "cat-file", "blob", "%s:%s" % (sha, rel)],
            env=git_env(home), cwd=repo)
    if r.returncode != 0:
        raise SetupError("cannot extract %s at %s" % (rel, sha))
    if not r.stdout:
        raise SetupError("extracted %s is empty" % rel)
    return r.stdout


# --------------------------------------------------------------------------------------------- recipes
def apply_recipe(data, name, old, new):
    """Apply one frozen recipe exactly once; refuse unless the text occurs exactly once."""
    count = data.count(old)
    if count != 1:
        raise RecipeError("%s text occurs %d times, expected exactly 1" % (name, count))
    out = data.replace(old, new, 1)
    if len(out) != len(data) - len(old) + len(new):
        raise RecipeError("%s replacement was not a single exact substitution" % name)
    try:
        compile(out, "<mutant %s>" % name, "exec")
    except (SyntaxError, ValueError, TypeError) as exc:
        raise RecipeError("%s mutant does not compile: %s" % (name, type(exc).__name__))
    return out


def run_harness(path, scratch, home, work):
    """Run one extracted/mutated harness `--selftest`; return (rc, assertions)."""
    r = run([sys.executable or "python3", path, "--selftest", "--scratch-root", scratch],
            env=child_env(home), cwd=work, timeout=900)
    return r.returncode, assertion_fraction(dec(r.stdout) + dec(r.stderr))


# --------------------------------------------------------------------------------------------- outcome
def outcome_exit(selftest_rc, killed, applied, base_killed):
    return 0 if (selftest_rc == 0 and killed == SCORE and applied == SCORE
                 and base_killed == 0) else 1


def outcome_verdict(selftest_rc, killed, applied, base_killed):
    return ("TARGET_MET" if (selftest_rc == 0 and killed == SCORE and applied == SCORE
                             and base_killed == 0) else "TARGET_MISSED")


def contract_line(selftest_field, killed, applied, base_killed, verdict, rev):
    return ("MADO_R69_PAIRED_RECIPES: selftest=%s killed=%d/3 applied=%d/3 base=%d/3 "
            "verdict=%s rev=%s" % (selftest_field, killed, applied, base_killed,
                                   verdict, rev))


# --------------------------------------------------------------------------------------------- measurement
def measure(args):
    scratch = absolute_scratch(args.scratch_root)
    if not args.repo or not args.rev or not args.base_rev:
        raise UsageError("--repo, --rev and --base-rev are required")
    repo = os.path.abspath(args.repo)
    if not os.path.isdir(repo):
        raise SetupError("--repo is not a directory: %s" % repo)
    work = os.path.join(scratch, "r69-c1")
    shutil.rmtree(work, ignore_errors=True)
    home = os.path.join(work, "home")
    os.makedirs(home)
    sha = resolve_rev(repo, args.rev, home)
    base_sha = resolve_rev(repo, args.base_rev, home)

    # --- candidate: extract, selftest, then one mutant per recipe -------------------------------
    selftest_rc = None
    applied = 0
    killed = 0
    if path_present(repo, sha, CANDIDATE, home):
        source = extract_blob(repo, sha, CANDIDATE, home)
        tree = os.path.join(work, "candidate", "tree")
        harness = os.path.join(tree, CANDIDATE)
        write_file(harness, source)
        emit("MADO_R69_EXTRACT path=%s rev=%s present=yes bytes=%d sha256=%s"
             % (CANDIDATE, sha, len(source), sha256_hex(source)))
        selftest_rc, frac = run_harness(harness, os.path.join(work, "candidate", "st"),
                                       home, work)
        emit("MADO_R69_SELFTEST harness=%s rc=%d assertions=%s"
             % (CANDIDATE, selftest_rc, frac))
        for name, old, new in RECIPES:
            count = source.count(old)
            try:
                mutant = apply_recipe(source, name, old, new)
            except RecipeError as exc:
                emit("MADO_R69_RECIPE name=%s occurrences=%d applicable=no note=%s"
                     % (name, count, exc))
                continue
            applied += 1
            mdir = os.path.join(work, "mutants", name)
            mpath = os.path.join(mdir, CANDIDATE)
            write_file(mpath, mutant)
            mrc, mfrac = run_harness(mpath, os.path.join(mdir, "st"), home, work)
            mkill = mrc != 0
            if mkill:
                killed += 1
            emit("MADO_R69_RECIPE name=%s occurrences=1 applicable=yes" % name)
            emit("MADO_R69_MUTANT name=%s path=%s recipe=%s from_sha256=%s rc=%d "
                 "assertions=%s killed=%s sha256=%s"
                 % (name, CANDIDATE, name, sha256_hex(source), mrc, mfrac,
                    "yes" if mkill else "no", sha256_hex(mutant)))
    else:
        emit("MADO_R69_EXTRACT path=%s rev=%s present=no" % (CANDIDATE, sha))

    # --- base: the r68 harness at --base-rev must survive the same three recipes ----------------
    if not path_present(repo, base_sha, BASE, home):
        raise SetupError("%s is absent at --base-rev %s" % (BASE, base_sha))
    base_source = extract_blob(repo, base_sha, BASE, home)
    base_tree = os.path.join(work, "base", "tree")
    write_file(os.path.join(base_tree, BASE), base_source)
    emit("MADO_R69_EXTRACT path=%s rev=%s present=yes bytes=%d sha256=%s"
         % (BASE, base_sha, len(base_source), sha256_hex(base_source)))
    base_killed = 0
    for name, old, new in RECIPES:
        try:
            bmutant = apply_recipe(base_source, name, old, new)
        except RecipeError as exc:
            # The declaration asserts each recipe text occurs exactly once in the r68 base
            # harness before scoring; a missing text voids the base leg, so it is not a
            # scored `base=0/3` (which would credit an unapplied recipe).
            raise SetupError("base recipe %s is not applicable: %s" % (name, exc))
        bdir = os.path.join(work, "base-mutants", name)
        bpath = os.path.join(bdir, BASE)
        write_file(bpath, bmutant)
        brc, bfrac = run_harness(bpath, os.path.join(bdir, "st"), home, work)
        bkill = brc != 0
        if bkill:
            base_killed += 1
        emit("MADO_R69_BASE_RECIPE name=%s occurrences=1 applicable=yes" % name)
        emit("MADO_R69_BASE_MUTANT name=%s path=%s recipe=%s from_sha256=%s rc=%d "
             "assertions=%s killed=%s sha256=%s"
             % (name, BASE, name, sha256_hex(base_source), brc, bfrac,
                "yes" if bkill else "no", sha256_hex(bmutant)))

    selftest_field = "absent" if selftest_rc is None else str(selftest_rc)
    verdict = outcome_verdict(selftest_rc, killed, applied, base_killed)
    emit(contract_line(selftest_field, killed, applied, base_killed, verdict, sha))
    return outcome_exit(selftest_rc, killed, applied, base_killed)


# --------------------------------------------------------------------------------------------- selftest
def raises(exc_type, fn):
    try:
        fn()
    except exc_type:
        return True
    except Exception:
        return False
    return False


SCRIPTED_SOURCE = b"\n".join((
    b'def measure():',
    b'    mz_summary = "none"',
    b'    mz_rc = 0',
    b'    try:',
    b'        mz_rc = 0',
    b'        mz_summary = "2/2"',
    b'        mz_killed = mz_rc != 0',
    b'    except ValueError:',
    b'        pass',
    b'    mr_rc = 0',
    b'    mr_marker = None',
    b'    u_ok = True',
    b'    try:',
    b'        if u_ok:',
    b'            mr_killed = bool(u_ok and not control_ok(mr_rc, mr_marker)',
    b'                             and forged_credit(mr_rc, mr_marker))',
    b'    except ValueError:',
    b'        pass',
    b'    return mz_killed, mr_killed',
    b'',
    b'',
    b'def selftest():',
    b'    subprocess.run = _no_spawn',
    b'',
))
SCRIPTED_NO_R3 = SCRIPTED_SOURCE.replace(b'    subprocess.run = _no_spawn\n', b'    pass\n')


def _compiles(data):
    try:
        compile(data, "<candidate>", "exec")
        return True
    except (SyntaxError, ValueError, TypeError):
        return False


def _scripted_run(case, sha, base_sha):
    """Deterministic stand-in for `run`: answers every argv the real body issues.

    The scripted cases drive the real `measure()` body (extraction, recipe application,
    mutant invocation, kill credit, base leg) with no process spawned, so a mutation of the
    kill-credit call sites changes the printed contract line.
    """
    calls = {"total": 0, "git": 0, "harness": 0}

    def fake(argv, env, cwd=None, input_bytes=None, timeout=900):
        calls["total"] += 1
        a = [str(x) for x in argv]
        out, rc = b"", 0
        if a[0] == "git":
            calls["git"] += 1
            if "rev-parse" in a and "--verify" in a:
                out = ((base_sha if "BASE" in " ".join(a) else sha) + "\n").encode()
            elif "--show-toplevel" in a:
                out = (a[a.index("--show-toplevel") - 2] + "\n").encode()
            elif "cat-file" in a and "-e" in a:
                rc = 1 if a[-1].split(":", 1)[-1] in case.get("absent", ()) else 0
            elif "cat-file" in a and "blob" in a:
                out = case["sources"][a[-1].split(":", 1)[-1]]
            elif "ls-tree" in a:
                out = (b"" if a[-1] in case.get("absent", ())
                       else (a[-1] + "\n").encode())
            else:
                rc = 1
        elif os.path.basename(a[0]).startswith("python"):
            calls["harness"] += 1
            path = a[1]
            if "/base-mutants/" in path:
                name = path.split("/base-mutants/", 1)[1].split("/", 1)[0]
                rc = case["base_mutant_rc"][name]
            elif "/mutants/" in path:
                name = path.split("/mutants/", 1)[1].split("/", 1)[0]
                rc = case["mutant_rc"][name]
            else:
                rc = case["candidate_rc"]
            if rc == 0:
                out = b"MADO_R69_LANDING_CONTROLS_SELFTEST: 59/59 assertions passed\n"
            else:
                out = (b"MADO_R69_SELFTEST FAIL: scripted mutant\n"
                       b"MADO_R69_LANDING_CONTROLS_SELFTEST: 57/59 assertions passed\n")
        else:
            rc = 127
        return subprocess.CompletedProcess(args=a, returncode=rc, stdout=out, stderr=b"")

    fake.calls = calls
    return fake


def _measure_case(work, case, sha, base_sha):
    """Run one scripted measurement through the real body; return (rc, line, lines, calls)."""
    scratch = os.path.join(work, "scripted-" + case["name"])
    os.makedirs(scratch, exist_ok=True)
    args = argparse.Namespace(repo=work, rev="HEAD", base_rev="BASE", scratch_root=scratch)
    saved = globals()["run"]
    fake = _scripted_run(case, sha, base_sha)
    globals()["run"] = fake
    buf = io.StringIO()
    try:
        with contextlib.redirect_stdout(buf):
            rc = measure(args)
    finally:
        globals()["run"] = saved
    lines = buf.getvalue().splitlines()
    hits = [ln for ln in lines if ln.startswith("MADO_R69_PAIRED_RECIPES:")]
    return rc, (hits[-1] if hits else "none"), lines, fake.calls


def _selftest_checks(work):
    checks = []

    def want(name, cond):
        checks.append((name, bool(cond)))

    sha = "a" * 40
    base_sha = "b" * 40

    want("frozen candidate path", CANDIDATE == "quality/counters/c1-r69-landing-controls.py")
    want("frozen base path", BASE == "quality/counters/c1-r68-landing-controls.py")
    want("three frozen recipes", SCORE == 3 and [r[0] for r in RECIPES] == ["R1", "R2", "R3"])
    want("R1 is the two-line paired-decision text", R1_OLD.count(b"\n") == 1
         and R1_OLD.startswith(b"            mr_killed = bool(")
         and R1_OLD.split(b"\n")[1].startswith(b"                             and forged_credit("))
    want("R2 is the parsed-mutant-run decision", R2_OLD == b"        mz_killed = mz_rc != 0"
         and R2_NEW == b'        mz_killed = mz_rc != 0 or mz_summary == "none"')
    want("R3 is the hermetic spawn guard assignment",
         R3_OLD == b"    subprocess.run = _no_spawn"
         and R3_NEW == b"    pass  # spawn guard removed by recipe")
    want("scripted fixture carries every recipe anchor once",
         all(SCRIPTED_SOURCE.count(old) == 1 for _n, old, _new in RECIPES))

    for name, old, new in RECIPES:
        mutant = apply_recipe(SCRIPTED_SOURCE, name, old, new)
        want("%s applies exactly once" % name,
             len(mutant) == len(SCRIPTED_SOURCE) - len(old) + len(new)
             and mutant.count(new) >= 1)
        want("%s mutant compiles" % name, _compiles(mutant))
    want("recipe refuses an absent text",
         raises(RecipeError, lambda: apply_recipe(b"x = 1\n", "R1", R1_OLD, R1_NEW)))
    want("recipe refuses a duplicated text",
         raises(RecipeError, lambda: apply_recipe(SCRIPTED_SOURCE + SCRIPTED_SOURCE,
                                                  "R1", R1_OLD, R1_NEW)))
    want("recipe refuses a text that does not compile after substitution",
         raises(RecipeError, lambda: apply_recipe(b"def f():\n    x = 1\n", "R2",
                                                  b"    x = 1\n", b"    if :\n")))

    want("met verdict is the exact frozen sentence", outcome_verdict(0, 3, 3, 0) == "TARGET_MET")
    want("exit zero only on selftest 0, 3/3 killed, 3/3 applied, base 0",
         outcome_exit(0, 3, 3, 0) == 0)
    want("killed<3 is a miss", outcome_exit(0, 2, 3, 0) == 1
         and outcome_verdict(0, 2, 3, 0) == "TARGET_MISSED")
    want("applied<3 is a miss", outcome_exit(0, 3, 2, 0) == 1
         and outcome_verdict(0, 3, 2, 0) == "TARGET_MISSED")
    want("base>0 is a miss", outcome_exit(0, 3, 3, 1) == 1
         and outcome_verdict(0, 3, 3, 1) == "TARGET_MISSED")
    want("red selftest is a miss", outcome_exit(1, 3, 3, 0) == 1
         and outcome_verdict(1, 3, 3, 0) == "TARGET_MISSED")
    want("absent selftest is a miss", outcome_exit(None, 0, 0, 0) == 1
         and outcome_verdict(None, 0, 0, 0) == "TARGET_MISSED")

    met_line = contract_line("0", 3, 3, 0, "TARGET_MET", sha)
    miss_line = contract_line("absent", 0, 0, 0, "TARGET_MISSED", sha)
    want("contract line is byte-exact for the met case",
         met_line == ("MADO_R69_PAIRED_RECIPES: selftest=0 killed=3/3 applied=3/3 base=0/3 "
                      "verdict=TARGET_MET rev=" + sha))
    want("contract line is byte-exact for the absent case",
         miss_line == ("MADO_R69_PAIRED_RECIPES: selftest=absent killed=0/3 applied=0/3 "
                       "base=0/3 verdict=TARGET_MISSED rev=" + sha))
    want("contract shape matches both lines",
         CONTRACT_RE.fullmatch(met_line) is not None
         and CONTRACT_RE.fullmatch(miss_line) is not None)
    want("contract shape refuses a wrong denominator",
         CONTRACT_RE.fullmatch(met_line.replace("killed=3/3", "killed=3/2")) is None)
    want("contract shape refuses a missing rev",
         CONTRACT_RE.fullmatch(met_line.rsplit(" rev=", 1)[0]) is None)

    want("scratch accepts its own real directory", absolute_scratch(work) == os.path.normpath(work))
    want("relative scratch resolves under cwd",
         absolute_scratch(os.path.join("rel", "scratch"))
         == os.path.normpath(os.path.join(os.getcwd(), "rel", "scratch")))
    for bad in ("", "/", "/tmp", "/tmp/x", "/var/tmp/x", "/dev/shm/x"):
        want("scratch refuses %r" % (bad or "<empty>"),
             raises(UsageError, lambda bad=bad: absolute_scratch(bad)))
    link = os.path.join(work, "link")
    os.symlink(work, link)
    try:
        want("symlinked scratch component refused",
             raises(UsageError, lambda: absolute_scratch(os.path.join(link, "child"))))
    finally:
        os.unlink(link)

    hostile = {
        "GIT_DIR": "/hostile",
        "GIT_WORK_TREE": "/hostile",
        "GIT_CONFIG_COUNT": "1",
        "GIT_CONFIG_KEY_0": "core.worktree",
        "GIT_CONFIG_VALUE_0": "/hostile",
        "GIT_REPLACE_REF_BASE": "refs/hostile/",
    }
    saved_env = {key: os.environ.get(key) for key in hostile}
    try:
        for key, value in hostile.items():
            os.environ[key] = value
        guarded_env = git_env(work)
        plain_env = child_env(work)
    finally:
        for key, value in saved_env.items():
            if value is None:
                os.environ.pop(key, None)
            else:
                os.environ[key] = value
    want("guarded git env scrubs inherited GIT_*", not (set(guarded_env) & set(hostile)))
    want("child env scrubs inherited GIT_*", not (set(plain_env) & set(hostile)))
    want("guarded git env pins optional locks and replacements",
         guarded_env.get("GIT_OPTIONAL_LOCKS") == "0"
         and guarded_env.get("GIT_NO_REPLACE_OBJECTS") == "1")
    want("extraction env alone carries the replacement guard",
         "GIT_NO_REPLACE_OBJECTS" not in plain_env)
    want("child env is exactly the explicit base env", set(plain_env) == set(BASE_ENV_KEYS))

    sources = {CANDIDATE: SCRIPTED_SOURCE, BASE: SCRIPTED_SOURCE}
    met = {"name": "met", "candidate_rc": 0,
           "mutant_rc": {"R1": 1, "R2": 1, "R3": 1},
           "base_mutant_rc": {"R1": 0, "R2": 0, "R3": 0}, "sources": sources}
    rc, line, lines, calls = _measure_case(work, met, sha, base_sha)
    want("scripted met prints the frozen met line",
         line == contract_line("0", 3, 3, 0, "TARGET_MET", sha))
    want("scripted met exits 0", rc == 0)
    want("scripted met drove the real body with scripted children",
         calls["harness"] == 7 and calls["git"] > 0)
    want("scripted met emits extraction evidence with a digest",
         any(ln.startswith("MADO_R69_EXTRACT path=" + CANDIDATE)
             and re.search(r"sha256=[0-9a-f]{64}$", ln) for ln in lines)
         and any(ln.startswith("MADO_R69_EXTRACT path=" + BASE) for ln in lines))
    want("scripted met emits one recipe line per frozen recipe",
         [ln for ln in lines if ln.startswith("MADO_R69_RECIPE ")] ==
         ["MADO_R69_RECIPE name=%s occurrences=1 applicable=yes" % name
          for name in ("R1", "R2", "R3")])
    want("scripted met emits mutant evidence with digests",
         all(any(ln.startswith("MADO_R69_MUTANT name=%s " % name)
                 and " killed=yes " in ln
                 and re.search(r"sha256=[0-9a-f]{64}$", ln) for ln in lines)
             for name in ("R1", "R2", "R3")))
    want("scripted met emits base mutant evidence",
         all(any(ln.startswith("MADO_R69_BASE_MUTANT name=%s " % name)
                 and " killed=no " in ln for ln in lines) for name in ("R1", "R2", "R3")))

    killed_low = {"name": "killed-low", "candidate_rc": 0,
                  "mutant_rc": {"R1": 1, "R2": 0, "R3": 1},
                  "base_mutant_rc": {"R1": 0, "R2": 0, "R3": 0}, "sources": sources}
    rc2, line2, _l2, _c2 = _measure_case(work, killed_low, sha, base_sha)
    want("killed<3 prints TARGET_MISSED",
         line2 == contract_line("0", 2, 3, 0, "TARGET_MISSED", sha) and rc2 == 1)
    want("killed<3 line matches the contract shape", CONTRACT_RE.fullmatch(line2) is not None)

    applied_low = {"name": "applied-low", "candidate_rc": 0,
                   "mutant_rc": {"R1": 1, "R2": 1},
                   "base_mutant_rc": {"R1": 0, "R2": 0, "R3": 0},
                   "sources": {CANDIDATE: SCRIPTED_NO_R3, BASE: SCRIPTED_SOURCE}}
    rc3, line3, lines3, _c3 = _measure_case(work, applied_low, sha, base_sha)
    want("applied<3 prints TARGET_MISSED",
         line3 == contract_line("0", 2, 2, 0, "TARGET_MISSED", sha) and rc3 == 1)
    want("applied<3 names the inapplicable recipe without counting a kill",
         any(ln.startswith("MADO_R69_RECIPE name=R3 occurrences=0 applicable=no")
             for ln in lines3)
         and not any(ln.startswith("MADO_R69_MUTANT name=R3 ") for ln in lines3))

    base_hit = {"name": "base-hit", "candidate_rc": 0,
                "mutant_rc": {"R1": 1, "R2": 1, "R3": 1},
                "base_mutant_rc": {"R1": 0, "R2": 1, "R3": 0}, "sources": sources}
    rc4, line4, _l4, _c4 = _measure_case(work, base_hit, sha, base_sha)
    want("base>0 prints TARGET_MISSED",
         line4 == contract_line("0", 3, 3, 1, "TARGET_MISSED", sha) and rc4 == 1)

    red = {"name": "red-selftest", "candidate_rc": 1,
           "mutant_rc": {"R1": 1, "R2": 1, "R3": 1},
           "base_mutant_rc": {"R1": 0, "R2": 0, "R3": 0}, "sources": sources}
    rc5, line5, _l5, _c5 = _measure_case(work, red, sha, base_sha)
    want("selftest!=0 prints TARGET_MISSED",
         line5 == contract_line("1", 3, 3, 0, "TARGET_MISSED", sha) and rc5 == 1)

    absent = {"name": "absent", "absent": (CANDIDATE,), "candidate_rc": 0,
              "mutant_rc": {}, "base_mutant_rc": {"R1": 0, "R2": 0, "R3": 0},
              "sources": sources}
    rc6, line6, lines6, _c6 = _measure_case(work, absent, sha, base_sha)
    want("absent candidate prints selftest=absent and TARGET_MISSED",
         line6 == contract_line("absent", 0, 0, 0, "TARGET_MISSED", sha) and rc6 == 1)
    want("absent candidate is never scored as applied",
         any(ln.startswith("MADO_R69_EXTRACT path=" + CANDIDATE) and " present=no" in ln
             for ln in lines6)
         and not any(ln.startswith("MADO_R69_RECIPE ") for ln in lines6))

    base_broken = {"name": "base-broken", "candidate_rc": 0,
                   "mutant_rc": {"R1": 1, "R2": 1, "R3": 1},
                   "base_mutant_rc": {"R1": 0, "R2": 0, "R3": 0},
                   "sources": {CANDIDATE: SCRIPTED_SOURCE, BASE: SCRIPTED_NO_R3}}
    want("an inapplicable base recipe is a setup error, not a credited base=0/3",
         raises(SetupError, lambda: _measure_case(work, base_broken, sha, base_sha)))
    return checks


def selftest(work):
    """Hermetic: every subprocess spawn raises, so the check body must stay pure."""
    saved_run = subprocess.run

    def _no_spawn(*_args, **_kwargs):
        raise AssertionError("selftest must not spawn a process")

    subprocess.run = _no_spawn
    try:
        checks = [("the hermetic spawn guard is installed for the check body",
                   subprocess.run is _no_spawn)]
        checks.append(("an attempted spawn under the guard raises",
                       raises(AssertionError, lambda: subprocess.run(["/bin/true"]))))
        try:
            checks.extend(_selftest_checks(work))
            checks.append(("the spawn guard is still installed after the scripted body",
                           subprocess.run is _no_spawn))
        except AssertionError:
            checks.append(("selftest body must not spawn a process", False))
    finally:
        subprocess.run = saved_run
    passed = sum(1 for _name, ok in checks if ok)
    for name, ok in checks:
        if not ok:
            print("MADO_R69_SELFTEST FAIL: %s" % name)
    print("MADO_R69_PAIRED_RECIPES_SELFTEST: %d/%d assertions passed" % (passed, len(checks)))
    return 0 if passed == len(checks) else 1


def selftest_main(scratch_arg):
    try:
        scratch = absolute_scratch(scratch_arg)
    except UsageError as exc:
        sys.stderr.write("%s: %s\n" % (TOOL, exc))
        return 2
    work = os.path.join(scratch, "r69-c1-selftest")
    shutil.rmtree(work, ignore_errors=True)
    os.makedirs(work)
    try:
        return selftest(work)
    finally:
        shutil.rmtree(work, ignore_errors=True)


# --------------------------------------------------------------------------------------------- main
def main(argv=None):
    ap = argparse.ArgumentParser(prog=TOOL, description=__doc__.splitlines()[0])
    ap.add_argument("--repo", default=None)
    ap.add_argument("--rev", default=None)
    ap.add_argument("--base-rev", default=None)
    ap.add_argument("--scratch-root", default=None)
    ap.add_argument("--selftest", action="store_true")
    args = ap.parse_args(argv)
    if args.selftest:
        return selftest_main(args.scratch_root)
    try:
        return measure(args)
    except UsageError as exc:
        sys.stderr.write("%s: usage error: %s\n" % (TOOL, exc))
        return 2
    except SetupError as exc:
        sys.stderr.write("%s: setup error: %s\n" % (TOOL, exc))
        return 2
    except (OSError, subprocess.SubprocessError) as exc:
        sys.stderr.write("%s: setup error: %s\n" % (TOOL, type(exc).__name__))
        return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
