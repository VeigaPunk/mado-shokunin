#!/usr/bin/env python3
r"""Round-69 C1 control harness: the standing landing instrument and its git-reading
children, measured against the two frozen defect controls (claim C1, round 69).

    python3 quality/counters/c1-r69-landing-controls.py --repo . --rev REV --scratch-root DIR
    python3 quality/counters/c1-r69-landing-controls.py --selftest --scratch-root DIR

Exit map: 0 iff the extracted instrument's own --selftest is rc 0 AND both frozen defect
mutants are killed (2/2); 1 iff the measurement ran and the contract was not met (red
selftest or a surviving mutant); 2 on usage/setup error - reason on stderr, no contract
line printed.

What one measurement does (every write stays under the caller-declared scratch root):

  extract  the four instrument files at --rev into <scratch>/r69-c1/tree/ with a scrubbed
           git env carrying GIT_OPTIONAL_LOCKS=0 and GIT_NO_REPLACE_OBJECTS=1, so a planted
           replacement in the source repo cannot forge the extracted bytes:
             quality/landing-counters.sh
             quality/counters/c3-r56-used-by.py
             quality/check-tool-ledger.py
             tools/mado-receipt-citecheck.py
  selftest run the extracted landing instrument `--selftest`: the candidate is expected green.
  M-Z      copy the tree, delete the exact frozen zero-citation guard clause
           `[ "$citations" -gt 0 ] && ` once (asserting exactly one occurrence first; the
           mutant must still pass `bash -n`), and re-run `--selftest`: the mutation is killed
           iff that selftest exits nonzero (the instrument's zero-citation case must go red).
  M-R      build a scratch fixture repo whose real tree lacks `corpus/cited.md` while a receipt
           in the worktree cites it, then plant a `refs/replace` ref on the root tree so the
           path appears; copy the extracted citecheck child, delete the exact
           GIT_NO_REPLACE_OBJECTS guard line (asserting exactly one occurrence first; a
           token-rename fallback is used only when the line cannot be deleted without breaking
           the file), and run both children on the same fixture with an env that carries NO
           GIT_NO_REPLACE_OBJECTS (all inherited GIT_* scrubbed): the unmutated child must read
           the real tree (rc 1, TARGET_MISSED, missing=1) and the mutant must credit the forged
           tree (rc 0, TARGET_MET) - that pair is the kill.

Printed receipt (last line, exact):

    MADO_R69_LANDING_CONTROLS: selftest=<rc> mz=<pass|fail> mr=<pass|fail> killed=<n>/2 baseline=0/2 verdict=<TARGET_MET|TARGET_MISSED> rev=<sha>

Preceded by one `MADO_R69_*` evidence line per extraction, mutant (with its sha256), R-control
leg, and the exact environment handed to the child under test. Mutant bytes are never claimed
killed when the recipe was inapplicable: a missing guard yields `recipe=none killed=no`, and
the unverified leg is named.

Selftest: `--selftest` is hermetic - it spawns nothing, touches only <scratch-root>, and
refuses /tmp-family or symlinked roots. It drives the real `measure()` body with scripted
children (git, bash and python answered in-process) so the kill-credit decisions and the
printed contract line are exercised without a child. On top of that it asserts the hermetic
spawn guard is installed for the check body, and that an attempted spawn under it raises.

Declared limits: the paired assertions cover two hazards of the kill-credit logic only - a
crashing M-R child (rc 2, no MADO_CITECHECK marker) is not a kill, and an M-Z run whose
combined output carries no `MADO_LANDING_COUNTERS_SELFTEST:` summary is not a kill. Both use
scripted stand-ins; the harness claims nothing about real children in those positions, and
the real-children leg stays the harm-watch leg.
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

TOOL = "c1-r69-landing-controls.py"
LANE = "quality/landing-counters.sh"
USEDBY = "quality/counters/c3-r56-used-by.py"
LEDGER = "quality/check-tool-ledger.py"
CITECHECK = "tools/mado-receipt-citecheck.py"
EXTRACT = (LANE, USEDBY, LEDGER, CITECHECK)
Z_PATH = LANE
R_PATH = CITECHECK
Z_CLAUSE = b'[ "$citations" -gt 0 ] && '
R_TOKEN = b"GIT_NO_REPLACE_OBJECTS"
R_RENAME = b"GIT_R67_NO_REPLACE_DISABLED"
BASELINE = "0/2"
UNSAFE_ROOTS = ("/tmp", "/var/tmp", "/dev/shm")
BASE_ENV_KEYS = (
    "PATH", "HOME", "TMPDIR", "LC_ALL",
    "GIT_CONFIG_NOSYSTEM", "GIT_CONFIG_GLOBAL", "GIT_CONFIG_SYSTEM",
    "GIT_TERMINAL_PROMPT",
)
CONTRACT_RE = re.compile(
    r"MADO_R69_LANDING_CONTROLS: selftest=[0-9]+ mz=(?:pass|fail) mr=(?:pass|fail) "
    r"killed=[0-2]/2 baseline=0/2 verdict=(?:TARGET_MET|TARGET_MISSED) rev=[0-9a-f]{40,64}"
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


def fixture_env(home):
    """Fixture-building env: scrubbed GIT_* but replacements left active (planted on purpose)."""
    env = _base_env(home)
    env["GIT_OPTIONAL_LOCKS"] = "0"
    return env


def child_env(home):
    """Exact env handed to a child under test: inherited GIT_* scrubbed, no replacement guard."""
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


def write_tree(files, dest):
    for rel in EXTRACT:
        write_file(os.path.join(dest, rel), files[rel])


def sha256_hex(data):
    return hashlib.sha256(data).hexdigest()


# --------------------------------------------------------------------------------------------- extract
def resolve_rev(repo, rev, home):
    if not rev or rev.startswith("-"):
        raise SetupError("invalid --rev")
    r = run(["git", "-C", repo, "rev-parse", "--verify", "--quiet", "--end-of-options",
             rev + "^{commit}"], env=git_env(home), cwd=repo)
    if r.returncode != 0:
        raise SetupError("--rev does not resolve to a commit at --repo")
    sha = r.stdout.decode("ascii", "replace").strip()
    if not re.fullmatch(r"[0-9a-f]{40,64}", sha):
        raise SetupError("--rev resolved to an unexpected object name")
    top = run(["git", "-C", repo, "rev-parse", "--show-toplevel"], env=git_env(home), cwd=repo)
    if top.returncode != 0:
        raise SetupError("--repo is not a git work tree")
    if os.path.realpath(top.stdout.decode("utf-8", "replace").strip()) != os.path.realpath(repo):
        raise SetupError("--repo is not the repository root")
    return sha


def extract(repo, sha, tree, home):
    files = {}
    for rel in EXTRACT:
        r = run(["git", "-C", repo, "cat-file", "blob", "%s:%s" % (sha, rel)],
                env=git_env(home), cwd=repo)
        if r.returncode != 0:
            raise SetupError("cannot extract %s at %s" % (rel, sha))
        files[rel] = r.stdout
        if not files[rel]:
            raise SetupError("extracted %s is empty" % rel)
    write_tree(files, tree)
    return files


# --------------------------------------------------------------------------------------------- mutation recipes
def mutate_clause(data):
    """Delete the frozen zero-citation guard clause exactly once."""
    count = data.count(Z_CLAUSE)
    if count != 1:
        raise RecipeError("zero-citation clause occurs %d times, expected exactly 1" % count)
    out = data.replace(Z_CLAUSE, b"", 1)
    if out.count(Z_CLAUSE) != 0 or len(data) - len(out) != len(Z_CLAUSE):
        raise RecipeError("zero-citation clause deletion was not exact")
    return out


def _parses(data):
    try:
        compile(data, "<mutant>", "exec")
        return True
    except (SyntaxError, ValueError, TypeError):
        return False


def neutralize_guard(data):
    """Remove the child's own GIT_NO_REPLACE_OBJECTS guard; return (bytes, recipe, line)."""
    count = data.count(R_TOKEN)
    if count != 1:
        raise RecipeError("GIT_NO_REPLACE_OBJECTS occurs %d times, expected exactly 1" % count)
    lines = data.splitlines(keepends=True)
    hits = [i for i, line in enumerate(lines) if R_TOKEN in line]
    if len(hits) != 1:
        raise RecipeError("guard token is not confined to one line")
    line = lines[hits[0]]
    body = b"".join(lines[:hits[0]] + lines[hits[0] + 1:])
    if body.count(R_TOKEN) == 0 and _parses(body):
        return body, "line-delete", line
    renamed = b"".join(line.replace(R_TOKEN, R_RENAME) if R_TOKEN in line else line for line in lines)
    if renamed.count(R_TOKEN) == 0 and _parses(renamed):
        return renamed, "token-rename", line
    raise RecipeError("guard line cannot be removed without breaking the child")


# --------------------------------------------------------------------------------------------- evidence parsing
def citecheck_marker(out):
    """(verdict, missing) from the last MADO_CITECHECK marker, else None."""
    hit = None
    for line in out.splitlines():
        if line.startswith("MADO_CITECHECK:"):
            m = re.search(r"missing=([0-9]+)\b.*\bverdict=(TARGET_MET|TARGET_MISSED)\b", line)
            if m:
                hit = (m.group(2), int(m.group(1)))
    return hit


def control_ok(rc, marker):
    """The R control passes only when the child read the real (defective) tree."""
    return rc == 1 and marker == ("TARGET_MISSED", 1)


def forged_credit(rc, marker):
    """The hazard the guard prevents: a green verdict over the forged tree."""
    return rc == 0 and marker == ("TARGET_MET", 0)


def last_summary(out):
    for line in reversed(out.splitlines()):
        if line.startswith("MADO_LANDING_COUNTERS_SELFTEST:"):
            return line.strip()
    return "none"


def summary_fraction(out):
    line = last_summary(out)
    m = re.search(r"(\d+/\d+)", line)
    return m.group(1) if m else "none"


def count_fails(out):
    return sum(1 for line in out.splitlines() if line.startswith("SELFTEST FAIL"))


def describe_env(env):
    """Exact key set and values of the child env, PATH summarized (host PATH is long noise)."""
    parts = ["no_replace_objects=%s"
             % ("absent" if "GIT_NO_REPLACE_OBJECTS" not in env else "PRESENT"),
             "keys=%s" % ",".join(sorted(env))]
    for key in sorted(env):
        if key == "PATH":
            dirs = env[key].split(os.pathsep)
            parts.append("PATH=%s...(%d dirs)" % (dirs[0] if dirs else "", len(dirs)))
        else:
            parts.append("%s=%s" % (key, env[key]))
    return " ".join(parts)


def outcome_exit(selftest_rc, killed):
    return 0 if selftest_rc == 0 and killed == 2 else 1


def outcome_verdict(selftest_rc, killed):
    return "TARGET_MET" if selftest_rc == 0 and killed == 2 else "TARGET_MISSED"


def contract_line(selftest_rc, mz, mr, killed, rev):
    return ("MADO_R69_LANDING_CONTROLS: selftest=%d mz=%s mr=%s killed=%d/2 baseline=%s "
            "verdict=%s rev=%s" % (selftest_rc, mz, mr, killed, BASELINE,
                                   outcome_verdict(selftest_rc, killed), rev))


# --------------------------------------------------------------------------------------------- R fixture
def ls_tree_names(repo, rev, env, home):
    r = run(["git", "-C", repo, "ls-tree", "-r", "--name-only", rev], env=env, cwd=home)
    if r.returncode != 0:
        raise SetupError("git ls-tree failed in the R fixture")
    return r.stdout.decode("utf-8", "replace").splitlines()


def build_r_fixture(work, home):
    """Fixture: the real tree lacks corpus/cited.md; a planted root-tree replacement adds it."""
    d = os.path.join(work, "r", "fixture")
    os.makedirs(d)
    env = fixture_env(home)

    def git(*args, input_bytes=None):
        r = run(["git", "-C", d] + list(args), env=env, cwd=work, input_bytes=input_bytes)
        if r.returncode != 0:
            raise SetupError("fixture git %s failed (rc=%d)" % (args[0], r.returncode))
        return r

    git("init", "-q")
    top = git("rev-parse", "--show-toplevel").stdout.decode("utf-8", "replace").strip()
    if os.path.realpath(top) != os.path.realpath(d):
        raise SetupError("fixture is not its own git root")
    receipt_rel = os.path.join(".ufo", "waves", "round-66", "receipts")
    write_file(os.path.join(d, receipt_rel, "a.txt"), b"cites corpus/cited.md\n")
    write_file(os.path.join(d, "keep.txt"), b"keep\n")
    git("add", "-A")
    git("-c", "user.name=r69-c1", "-c", "user.email=r69-c1@example.invalid",
        "-c", "commit.gpgsign=false", "commit", "-qm", "r69-c1 replacement-ref fixture")
    rev = git("rev-parse", "HEAD").stdout.decode("ascii", "replace").strip()
    if not re.fullmatch(r"[0-9a-f]{40,64}", rev):
        raise SetupError("fixture revision is malformed")
    real_tree = git("rev-parse", rev + "^{tree}").stdout.decode("ascii", "replace").strip()
    blob = git("hash-object", "-w", "--stdin",
               input_bytes=b"cited file\n").stdout.decode("ascii", "replace").strip()
    git("read-tree", real_tree)
    git("update-index", "--add", "--cacheinfo", "100644,%s,corpus/cited.md" % blob)
    forged_tree = git("write-tree").stdout.decode("ascii", "replace").strip()
    git("read-tree", rev)
    git("replace", real_tree, forged_tree)
    if real_tree not in git("replace", "-l").stdout.decode("utf-8", "replace").split():
        raise SetupError("replace ref was not planted")
    forged_names = ls_tree_names(d, rev, fixture_env(home), home)
    guarded_names = ls_tree_names(d, rev, git_env(home), home)
    if "corpus/cited.md" not in forged_names:
        raise SetupError("planted tree replacement is not visible")
    if "corpus/cited.md" in guarded_names:
        raise SetupError("GIT_NO_REPLACE_OBJECTS does not hide the forged path")
    return {
        "dir": d,
        "rev": rev,
        "real_tree": real_tree,
        "forged_tree": forged_tree,
        "receipt": os.path.join(d, receipt_rel),
    }


def run_r_child(child, fixture, work, home):
    argv = [sys.executable or "python3", child,
            "--repo", fixture["dir"], "--rev", fixture["rev"], "--paths", fixture["receipt"]]
    r = run(argv, env=child_env(home), cwd=work, timeout=300)
    out = dec(r.stdout) + dec(r.stderr)
    return {"rc": r.returncode, "marker": citecheck_marker(out), "argv": argv, "out": out}


# --------------------------------------------------------------------------------------------- measurement
def measure(args):
    scratch = absolute_scratch(args.scratch_root)
    if not args.repo or not args.rev:
        raise UsageError("--repo and --rev are required")
    repo = os.path.abspath(args.repo)
    if not os.path.isdir(repo):
        raise SetupError("--repo is not a directory: %s" % repo)
    work = os.path.join(scratch, "r69-c1")
    shutil.rmtree(work, ignore_errors=True)
    home = os.path.join(work, "home")
    os.makedirs(home)
    sha = resolve_rev(repo, args.rev, home)
    tree = os.path.join(work, "tree")
    files = extract(repo, sha, tree, home)
    for rel in EXTRACT:
        emit("MADO_R69_EXTRACT path=%s bytes=%d sha256=%s"
             % (rel, len(files[rel]), sha256_hex(files[rel])))
    emit("MADO_R69_EXTRACT rev=%s files=%d" % (sha, len(files)))

    # --- extracted instrument's own selftest -----------------------------------------------------
    r = run(["bash", os.path.join(tree, LANE), "--selftest",
             "--scratch-root", os.path.join(work, "st")], env=child_env(home), cwd=work, timeout=900)
    selftest_rc = r.returncode
    emit("MADO_R69_SELFTEST instrument=%s rc=%d assertions=%s"
         % (LANE, selftest_rc, summary_fraction(dec(r.stdout) + dec(r.stderr))))

    # --- M-Z: zero-citation guard clause deleted -------------------------------------------------
    clause_count = files[Z_PATH].count(Z_CLAUSE)
    mz_rc = None
    mz_fails = None
    mz_summary = "none"
    mz_recipe = "none"
    mz_sha = "absent"
    mz_killed = False
    mz_note = ""
    try:
        mz_bytes = mutate_clause(files[Z_PATH])
        mz_recipe = "clause-delete"
        mz_tree = os.path.join(work, "mz")
        write_tree(files, mz_tree)
        mz_path = os.path.join(mz_tree, Z_PATH)
        write_file(mz_path, mz_bytes)
        syntax = run(["bash", "-n", mz_path], env=child_env(home), cwd=work, timeout=120)
        if syntax.returncode != 0:
            raise RecipeError("mutant fails bash -n (rc=%d)" % syntax.returncode)
        mz_sha = sha256_hex(mz_bytes)
        r = run(["bash", mz_path, "--selftest",
                 "--scratch-root", os.path.join(work, "mz-st")],
                env=child_env(home), cwd=work, timeout=900)
        mz_rc = r.returncode
        mz_out = dec(r.stdout) + dec(r.stderr)
        mz_fails = count_fails(mz_out)
        mz_summary = summary_fraction(mz_out)
        mz_killed = mz_rc != 0
    except RecipeError as exc:
        mz_note = str(exc)
    emit("MADO_R69_MUTANT M-Z path=%s clause_count=%d recipe=%s removed=%s from_sha256=%s "
         "rc=%s failed_assertions=%s assertions=%s killed=%s sha256=%s%s"
         % (Z_PATH, clause_count, mz_recipe,
            repr(Z_CLAUSE.decode("ascii")) if mz_recipe != "none" else "none",
            sha256_hex(files[Z_PATH]), "-" if mz_rc is None else mz_rc,
            "-" if mz_fails is None else mz_fails, mz_summary,
            "yes" if mz_killed else "no", mz_sha,
            (" note=%s" % mz_note) if mz_note else ""))

    # --- M-R: replacement-ref guard removed from the citecheck child ----------------------------
    # Bound target is the citecheck child (L1 steering 2026-11-03): its explicit env constructor
    # is the guard, and the tree-replacement fixture exercises exactly its `ls-tree` read.
    emit("MADO_R69_GUARDS citecheck=%d usedby=%d ledger=%d"
         % (files[CITECHECK].count(R_TOKEN), files[USEDBY].count(R_TOKEN),
            files[LEDGER].count(R_TOKEN)))
    guard_count = files[R_PATH].count(R_TOKEN)
    fixture = build_r_fixture(work, home)
    emit("MADO_R69_R_CONTROL fixture_rev=%s real_tree=%s forged_tree=%s "
         "forged_visible=yes guarded_visible=no"
         % (fixture["rev"], fixture["real_tree"], fixture["forged_tree"]))
    cenv = child_env(home)
    emit("MADO_R69_CHILD_ENV %s" % describe_env(cenv))
    unmutated = run_r_child(os.path.join(tree, R_PATH), fixture, work, home)
    u_ok = control_ok(unmutated["rc"], unmutated["marker"])
    emit("MADO_R69_R_CHILD role=unmutated rc=%d verdict=%s missing=%s control=%s"
         % (unmutated["rc"],
            unmutated["marker"][0] if unmutated["marker"] else "none",
            unmutated["marker"][1] if unmutated["marker"] else "-",
            "green" if u_ok else "red"))

    mr_rc = None
    mr_marker = None
    mr_recipe = "none"
    mr_sha = "absent"
    mr_removed = "none"
    mr_killed = False
    mr_note = ""
    if guard_count == 1:
        try:
            mr_bytes, mr_recipe, guard_line = neutralize_guard(files[R_PATH])
            mr_removed = repr(guard_line.decode("utf-8", "replace"))
            mr_sha = sha256_hex(mr_bytes)
            mr_tree = os.path.join(work, "mr")
            write_tree(files, mr_tree)
            mr_path = os.path.join(mr_tree, R_PATH)
            write_file(mr_path, mr_bytes)
            mutant = run_r_child(mr_path, fixture, work, home)
            mr_rc = mutant["rc"]
            mr_marker = mutant["marker"]
            mr_killed = bool(u_ok and not control_ok(mr_rc, mr_marker)
                             and forged_credit(mr_rc, mr_marker))
        except RecipeError as exc:
            mr_note = str(exc)
    else:
        mr_note = "guard absent at rev (count=%d): recipe not applicable" % guard_count
    emit("MADO_R69_MUTANT M-R path=%s guard_count=%d recipe=%s removed_line=%s "
         "from_sha256=%s rc=%s verdict=%s missing=%s forged_credit=%s killed=%s sha256=%s%s"
         % (R_PATH, guard_count, mr_recipe, mr_removed, sha256_hex(files[R_PATH]),
            "-" if mr_rc is None else mr_rc,
            mr_marker[0] if mr_marker else "none",
            mr_marker[1] if mr_marker else "-",
            "yes" if (mr_rc is not None and forged_credit(mr_rc, mr_marker)) else "no",
            "yes" if mr_killed else "no", mr_sha,
            (" note=%s" % mr_note) if mr_note else ""))

    killed = int(mz_killed) + int(mr_killed)
    emit(contract_line(selftest_rc, "pass" if mz_killed else "fail",
                       "pass" if mr_killed else "fail", killed, sha))
    return outcome_exit(selftest_rc, killed)


# --------------------------------------------------------------------------------------------- selftest
def raises(exc_type, fn):
    try:
        fn()
    except exc_type:
        return True
    except Exception:
        return False
    return False


def _scripted_run(case, sha):
    """Deterministic stand-in for `run`: answers every argv the measurement issues.

    The two scripted cases drive the real `measure()` body (extraction, mutant
    construction, child invocation, kill credit) with no process spawned, so a
    mutation of the kill-credit call sites changes the printed contract line.
    """
    fixture_dir = {}

    def fake(argv, env, cwd=None, input_bytes=None, timeout=900):
        a = [str(x) for x in argv]
        out, rc = b"", 0
        if a[0] == "git":
            joined = " ".join(a)
            if "cat-file" in a:
                path = a[-1].split(":", 1)[-1]
                if path.endswith("landing-counters.sh"):
                    out = b'#!/bin/bash\n[ "$citations" -gt 0 ] && echo ok\n'
                else:
                    out = b'env = dict(os.environ, GIT_NO_REPLACE_OBJECTS="1")\n'
            elif "--show-toplevel" in a:
                out = (a[a.index("--show-toplevel") - 2] + "\n").encode()
            elif "--verify" in a:
                out = (sha + "\n").encode()
            elif "rev-parse" in a and any(t.endswith("^{tree}") for t in a):
                out = ("b" * 40 + "\n").encode()
            elif "rev-parse" in a:
                out = (("c" if "HEAD" in joined else "b") * 40 + "\n").encode()
            elif "hash-object" in a:
                out = ("f" * 40 + "\n").encode()
            elif "write-tree" in a:
                out = ("d" * 40 + "\n").encode()
            elif "replace" in a and "-l" in a:
                out = ("b" * 40 + "\n").encode()
            elif "ls-tree" in a:
                names = (["keep.txt"] if "GIT_NO_REPLACE_OBJECTS" in env
                         else ["corpus/cited.md", "keep.txt"])
                out = ("\n".join(names) + "\n").encode()
            elif any(t in a for t in ("init", "add", "read-tree", "update-index",
                                      "commit", "replace")):
                out = b""
            else:
                rc = 1
        elif os.path.basename(a[0]) == "bash":
            if "-n" in a:
                out = b""
            elif any(t.endswith("landing-counters.sh") for t in a):
                if "/mz/" in " ".join(a):
                    rc = case["mz_rc"]
                    out = case.get("mz_stdout",
                                   b"MADO_LANDING_COUNTERS_SELFTEST: 60/62 assertions passed\n")
                else:
                    out = b"MADO_LANDING_COUNTERS_SELFTEST: 62/62 assertions passed\n"
            else:
                rc = case["mz_rc"]
                out = b"MADO_LANDING_COUNTERS_SELFTEST: 60/62 assertions passed\n"
        elif os.path.basename(a[0]).startswith("python"):
            if "/mr/" in " ".join(a):
                marker = case.get("child_marker")
                out = ("" if marker is None else (marker % sha)).encode()
                rc = case["child_rc"]
            else:
                out = (MISSED_MARKER % sha).encode()
                rc = 1
        else:
            rc = 127
        return subprocess.CompletedProcess(args=a, returncode=rc, stdout=out, stderr=b"")

    return fake


def _measure_case(work, case, sha):
    """Run one scripted measurement through the real body; return (rc, contract line)."""
    scratch = os.path.join(work, "scripted-" + case["name"])
    os.makedirs(scratch, exist_ok=True)
    args = argparse.Namespace(repo=work, rev="HEAD", scratch_root=scratch)
    saved = globals()["run"]
    globals()["run"] = _scripted_run(case, sha)
    buf = io.StringIO()
    try:
        with contextlib.redirect_stdout(buf):
            rc = measure(args)
    finally:
        globals()["run"] = saved
    lines = [ln for ln in buf.getvalue().splitlines()
             if ln.startswith("MADO_R69_LANDING_CONTROLS:")]
    return rc, (lines[-1] if lines else "none")


MET_MARKER = ("MADO_CITECHECK: rev=%s files=1 citations=1 resolved=1 missing=0 "
              "skipped_large=0 verdict=TARGET_MET (VERSION r64-v1)")
MISSED_MARKER = ("MADO_CITECHECK: rev=%s files=1 citations=1 resolved=0 missing=1 "
                 "skipped_large=0 verdict=TARGET_MISSED (VERSION r64-v1)")


def _scripted_checks(work):
    """The measurement path itself, driven by scripted children (no spawn)."""
    checks = []

    def want(name, cond):
        checks.append((name, bool(cond)))

    sha = "a" * 40
    met = {"name": "both-killed", "mz_rc": 1, "child_rc": 0, "child_marker": MET_MARKER}
    rc, line = _measure_case(work, met, sha)
    want("scripted both-killed prints the met line",
         line == ("MADO_R69_LANDING_CONTROLS: selftest=0 mz=pass mr=pass killed=2/2 "
                  "baseline=0/2 verdict=TARGET_MET rev=" + sha))
    want("scripted both-killed exits 0", rc == 0)

    none = {"name": "none-killed", "mz_rc": 0, "child_rc": 1,
            "child_marker": MISSED_MARKER}
    rc2, line2 = _measure_case(work, none, sha)
    want("scripted none-killed prints the miss line",
         line2 == ("MADO_R69_LANDING_CONTROLS: selftest=0 mz=fail mr=fail killed=0/2 "
                   "baseline=0/2 verdict=TARGET_MISSED rev=" + sha))
    want("scripted none-killed exits 1", rc2 == 1)
    want("both scripted lines match the frozen contract shape",
         CONTRACT_RE.fullmatch(line) is not None and CONTRACT_RE.fullmatch(line2) is not None)

    crash = {"name": "mr-crash", "mz_rc": 1, "child_rc": 2, "child_marker": None}
    rc3, line3 = _measure_case(work, crash, sha)
    want("a crashing M-R child is not a kill (decision + oracle pair)",
         line3 == ("MADO_R69_LANDING_CONTROLS: selftest=0 mz=pass mr=fail killed=1/2 "
                   "baseline=0/2 verdict=TARGET_MISSED rev=" + sha))
    want("mr-crash exits 1", rc3 == 1)

    mute = {"name": "mz-unparseable", "mz_rc": 0,
            "mz_stdout": b"bash: mz: synthetic crash before any assertion\n",
            "child_rc": 1, "child_marker": MISSED_MARKER}
    rc4, line4 = _measure_case(work, mute, sha)
    want("an M-Z run with no assertion summary is not a kill",
         line4 == ("MADO_R69_LANDING_CONTROLS: selftest=0 mz=fail mr=fail killed=0/2 "
                   "baseline=0/2 verdict=TARGET_MISSED rev=" + sha))
    want("mz-unparseable exits 1", rc4 == 1)
    want("paired scripted lines match the frozen contract shape",
         CONTRACT_RE.fullmatch(line3) is not None and CONTRACT_RE.fullmatch(line4) is not None)
    return checks


def _selftest_checks(work):
    checks = []

    def want(name, cond):
        checks.append((name, bool(cond)))

    want("frozen extraction list", EXTRACT == (
        "quality/landing-counters.sh",
        "quality/counters/c3-r56-used-by.py",
        "quality/check-tool-ledger.py",
        "tools/mado-receipt-citecheck.py"))
    want("M-Z target is the extracted landing instrument", Z_PATH == EXTRACT[0])
    want("M-R target is the extracted citecheck child", R_PATH == CITECHECK and R_PATH in EXTRACT)
    want("frozen clause token", Z_CLAUSE == b'[ "$citations" -gt 0 ] && ')
    want("frozen guard token", R_TOKEN == b"GIT_NO_REPLACE_OBJECTS")

    clause_src = b'  [ "$citations" -gt 0 ] && [ "$citations" -eq 1 ] || return 1\n'
    want("clause deletion removes exactly the token",
         mutate_clause(clause_src) == b'  [ "$citations" -eq 1 ] || return 1\n')
    want("clause absent refuses", raises(RecipeError, lambda: mutate_clause(b'[ "$x" -gt 0 ] || return 1\n')))
    want("clause duplicated refuses", raises(RecipeError, lambda: mutate_clause(clause_src + clause_src)))
    want("clause deletion is deterministic", mutate_clause(clause_src) == mutate_clause(clause_src))

    inline = (b'def f(cmd):\n'
              b'    return run(cmd,\n'
              b'        env=dict(os.environ, GIT_NO_REPLACE_OBJECTS="1"),\n'
              b'    )\n')
    out, recipe, line = neutralize_guard(inline)
    want("guard line-delete recipe", recipe == "line-delete")
    want("guard line-delete keeps the rest byte-identical",
         out == b'def f(cmd):\n    return run(cmd,\n    )\n' and line.count(R_TOKEN) == 1)
    want("guard gone after line deletion", out.count(R_TOKEN) == 0 and _parses(out))

    nested = (b'def f(cmd):\n'
              b'    return run(cmd,\n'
              b'        env={"PATH": "/bin", "GIT_NO_REPLACE_OBJECTS": "1"})\n')
    out2, recipe2, _ = neutralize_guard(nested)
    want("non-deletable guard falls back to token rename", recipe2 == "token-rename")
    want("renamed guard is not the git key",
         out2.count(R_TOKEN) == 0 and R_RENAME in out2 and _parses(out2))
    want("guard absent refuses", raises(RecipeError, lambda: neutralize_guard(b'x = 1\n')))
    want("guard duplicated refuses", raises(RecipeError, lambda: neutralize_guard(
        b'a = "GIT_NO_REPLACE_OBJECTS"\nb = "GIT_NO_REPLACE_OBJECTS"\n')))

    met = ("MADO_CITECHECK: rev=abc files=1 citations=1 resolved=1 missing=0 "
           "skipped_large=0 verdict=TARGET_MET (VERSION r64-v1)")
    missed = ("MADO_CITECHECK: rev=abc files=1 citations=1 resolved=0 missing=1 "
              "skipped_large=0 verdict=TARGET_MISSED (VERSION r64-v1)")
    want("marker parse forged", citecheck_marker(met) == ("TARGET_MET", 0))
    want("marker parse real", citecheck_marker(missed) == ("TARGET_MISSED", 1))
    want("marker parse junk", citecheck_marker("CITECHECK resolved: x") is None)
    want("control green needs the real read", control_ok(1, ("TARGET_MISSED", 1)))
    want("control rejects forged read", not control_ok(0, ("TARGET_MET", 0)))
    want("control rejects setup error", not control_ok(2, None))
    want("forged credit is rc0 + TARGET_MET + missing=0",
         forged_credit(0, ("TARGET_MET", 0)) and not forged_credit(1, ("TARGET_MISSED", 1)))

    want("exit zero only on green selftest and 2/2", outcome_exit(0, 2) == 0)
    want("one kill is a miss", outcome_exit(0, 1) == 1)
    want("red selftest is a miss", outcome_exit(1, 2) == 1)
    want("verdict met only on green 2/2",
         outcome_verdict(0, 2) == "TARGET_MET"
         and outcome_verdict(0, 1) == "TARGET_MISSED"
         and outcome_verdict(2, 2) == "TARGET_MISSED")

    line = contract_line(0, "pass", "pass", 2, "a" * 40)
    want("contract line matches the frozen shape",
         CONTRACT_RE.fullmatch(line) is not None and " baseline=0/2 " in line)
    want("contract line reports the miss",
         contract_line(0, "pass", "fail", 1, "a" * 40)
         == ("MADO_R69_LANDING_CONTROLS: selftest=0 mz=pass mr=fail killed=1/2 "
             "baseline=0/2 verdict=TARGET_MISSED rev=" + "a" * 40))

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
    saved = {key: os.environ.get(key) for key in hostile}
    try:
        for key, value in hostile.items():
            os.environ[key] = value
        guarded_env = git_env(work)
        plain_env = child_env(work)
    finally:
        for key, value in saved.items():
            if value is None:
                os.environ.pop(key, None)
            else:
                os.environ[key] = value
    want("guarded git env scrubs inherited GIT_*", not (set(guarded_env) & set(hostile)))
    want("child env scrubs inherited GIT_*", not (set(plain_env) & set(hostile)))
    want("guarded git env pins optional locks and replacements",
         guarded_env.get("GIT_OPTIONAL_LOCKS") == "0"
         and guarded_env.get("GIT_NO_REPLACE_OBJECTS") == "1")
    want("child env carries no replacement guard", "GIT_NO_REPLACE_OBJECTS" not in plain_env)
    want("child env is exactly the explicit base env", set(plain_env) == set(BASE_ENV_KEYS))

    want("child env evidence names the guard state and key set",
         describe_env(plain_env).startswith("no_replace_objects=absent keys=")
         and "GIT_NO_REPLACE_OBJECTS" not in describe_env(plain_env))
    want("child env evidence detects a present guard",
         describe_env(dict(plain_env, GIT_NO_REPLACE_OBJECTS="1")).startswith("no_replace_objects=PRESENT"))
    want("sha256 helper matches the empty digest",
         sha256_hex(b"") == "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855")
    want("sha256 helper is deterministic", sha256_hex(b"x") == sha256_hex(b"x"))
    checks.extend(_scripted_checks(work))
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
        try:
            checks.append(("an attempted spawn under the guard raises",
                           raises(AssertionError,
                                  lambda: subprocess.run(["/bin/true"]))))
        except AssertionError:
            checks.append(("an attempted spawn under the guard raises", False))
        try:
            checks.extend(_selftest_checks(work))
        except AssertionError:
            checks.append(("selftest body must not spawn a process", False))
    finally:
        subprocess.run = saved_run
    passed = sum(1 for _name, ok in checks if ok)
    for name, ok in checks:
        if not ok:
            print("MADO_R69_SELFTEST FAIL: %s" % name)
    print("MADO_R69_LANDING_CONTROLS_SELFTEST: %d/%d assertions passed" % (passed, len(checks)))
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
