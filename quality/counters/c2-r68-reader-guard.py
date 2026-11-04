#!/usr/bin/env python3
"""Round-68 C2 counter: the standing gate population reads git objects only through a guarded
environment (claim C2, attempt 1).

    python3 quality/counters/c2-r68-reader-guard.py --repo . --rev REV --controls PATH \
        --scratch-root DIR
    python3 quality/counters/c2-r68-reader-guard.py --selftest --scratch-root DIR

Population: every tracked file whose path matches `quality/check-*.py` at --rev (the
lane's standing gates, enumerated from git objects, never the worktree).

Reader: the blob contains a `git` command token and at least one quoted object-read verb from
the frozen vocabulary below. Guard: the blob's AST constructs an environment that carries the
string `GIT_NO_REPLACE_OBJECTS` as (a) a dict-literal key, (b) a subscript store index
(`env["GIT_NO_REPLACE_OBJECTS"] = ...`), (c) a keyword argument (`dict(NAME="1")`,
`update(NAME="1")`), or (d) a constant inside any `env=` keyword subtree. A comment, a
docstring or a bare prose mention is not a guard construction.

Target: `readers > 0 and unguarded == 0`, plus every frozen control case correct. Exit 0 on
TARGET_MET, 1 on TARGET_MISSED, 2 on setup/usage error (reason on stderr).

--controls scores a JSON case set of the shape
`{"cases": [{"name": ..., "src": ..., "expect_reader": true|false, "expect_guard": ...}]}`.
--selftest is hermetic: it classifies in-memory sources only, spawns nothing (asserted by
patching subprocess.run), and writes nothing.
"""
import argparse
import ast
import json
import os
import re
import subprocess
import sys

TOOL = "c2-r68-reader-guard.py"
POPULATION_RE = re.compile(r"^quality/check-[^/]+\.py$")
GIT_TOKEN_RE = re.compile(r"(?<![A-Za-z0-9_-])git(?![A-Za-z0-9_-])")
VERBS = ("show", "cat-file", "ls-tree", "rev-parse", "diff-tree", "log", "merge-base",
         "for-each-ref")
VERB_RE = re.compile(r"[\"'](%s)[\"']" % "|".join(re.escape(v) for v in VERBS))
KEY = "GIT_NO_REPLACE_OBJECTS"
CONTRACT_RE = re.compile(
    r"MADO_R68_READER_GUARD: population=[0-9]+ readers=[0-9]+ guarded=[0-9]+ "
    r"unguarded=[0-9]+ controls=[0-9]+/[0-9]+ verdict=(?:TARGET_MET|TARGET_MISSED) "
    r"rev=[0-9a-f]{40,64}")


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


def run(argv, cwd, timeout=600):
    return subprocess.run(argv, cwd=cwd, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                          env=git_env(), timeout=timeout)


def git(repo, args, timeout=600):
    r = run(["git", "-C", repo] + list(args), cwd=repo, timeout=timeout)
    if r.returncode != 0:
        raise SetupError("git %s failed (rc=%d): %s"
                         % (args[0], r.returncode,
                            r.stderr.decode("utf-8", "replace").strip()[:200]))
    return r.stdout


# --------------------------------------------------------------------------------------------- classification
def is_reader(src):
    return bool(GIT_TOKEN_RE.search(src)) and bool(VERB_RE.search(src))


def has_guard(src):
    """True iff the source builds an environment that carries the replacement guard.

    An environment is a value reaching an `env=` keyword, or a value bound to a name that
    says `env` (`env`, `GIT_ENV`, `git_env` locals) — including a subscript store on that
    name. A mention in a comment, a docstring or an unrelated data dictionary is not one.
    """
    try:
        tree = ast.parse(src)
    except SyntaxError:
        return False

    def env_named(node):
        return isinstance(node, ast.Name) and "env" in node.id.lower()

    def carries_key(node):
        for n in ast.walk(node):
            if isinstance(n, ast.Constant) and n.value == KEY:
                return True
            if isinstance(n, ast.keyword) and n.arg == KEY:
                return True
        return False

    for node in ast.walk(tree):
        if isinstance(node, ast.Assign):
            for target in node.targets:
                if env_named(target) and carries_key(node.value):
                    return True
                if (isinstance(target, ast.Subscript) and env_named(target.value)
                        and isinstance(target.ctx, ast.Store)):
                    sl = target.slice
                    if isinstance(sl, ast.Constant) and sl.value == KEY:
                        return True
        elif isinstance(node, ast.Call):
            for kw in node.keywords:
                if kw.arg == "env" and carries_key(kw.value):
                    return True
    return False


def classify(src):
    reader = is_reader(src)
    return reader, (has_guard(src) if reader else False)


# --------------------------------------------------------------------------------------------- measurement
def measure(repo, rev, controls_path):
    if not os.path.isdir(repo):
        raise SetupError("--repo is not a directory: %s" % repo)
    sha = git(repo, ["rev-parse", "--verify", rev + "^{commit}"]).decode("ascii").strip()
    names = git(repo, ["ls-tree", "-r", "--name-only", sha, "--", "quality"]).decode(
        "utf-8", "replace").splitlines()
    population = sorted(p for p in names if POPULATION_RE.match(p))
    if not population:
        raise SetupError("population is empty at %s" % sha)
    readers = guarded = 0
    for path in population:
        src = git(repo, ["show", "%s:%s" % (sha, path)]).decode("utf-8", "replace")
        reader, guard = classify(src)
        if reader:
            readers += 1
            guarded += int(guard)
        print("MADO_R68_READER file=%s reader=%s guard=%s"
              % (path, "yes" if reader else "no", "yes" if guard else "no"))
    unguarded = readers - guarded

    controls_total = correct = 0
    if controls_path:
        try:
            with open(controls_path, "r", encoding="utf-8") as fh:
                cases = json.load(fh)["cases"]
        except (OSError, ValueError, KeyError) as exc:
            raise SetupError("controls file unusable: %s" % exc)
        controls_total = len(cases)
        for case in cases:
            reader, guard = classify(case["src"])
            ok = (reader == case["expect_reader"]) and (guard == case["expect_guard"])
            correct += int(ok)
            print("MADO_R68_CONTROL name=%s reader=%s guard=%s expect_reader=%s "
                  "expect_guard=%s correct=%s"
                  % (case["name"], "yes" if reader else "no", "yes" if guard else "no",
                     "yes" if case["expect_reader"] else "no",
                     "yes" if case["expect_guard"] else "no", "yes" if ok else "no"))
    met = (readers > 0 and unguarded == 0 and controls_total > 0
           and correct == controls_total)
    print("MADO_R68_READER_GUARD: population=%d readers=%d guarded=%d unguarded=%d "
          "controls=%d/%d verdict=%s rev=%s"
          % (len(population), readers, guarded, unguarded, correct, controls_total,
             "TARGET_MET" if met else "TARGET_MISSED", sha))
    return 0 if met else 1


# --------------------------------------------------------------------------------------------- selftest
GUARDED_DICT = '''\
def git_env():
    env = {"PATH": "/usr/bin", "GIT_NO_REPLACE_OBJECTS": "1"}
    return env


def run(repo):
    subprocess.run(["git", "-C", repo, "show", "HEAD:a"], env=git_env())
'''
UNGUARDED_DICT = '''\
def run(repo):
    subprocess.run(["git", "-C", repo, "show", "HEAD:a"],
                   env={"PATH": "/usr/bin", "GIT_OPTIONAL_LOCKS": "0"})
'''
INHERIT = '''\
def run(repo):
    subprocess.run(["git", "-C", repo, "cat-file", "-p", "HEAD:a"])
'''
AXIS_SHAPE = '''\
def git(repo, *args):
    return subprocess.run(["git", "-C", repo] + list(args), capture_output=True,
                          env={k: v for k, v in os.environ.items()
                               if not k.startswith("GIT_")})


def head(repo):
    return git(repo, "show", "HEAD:a")
'''
SUBSCRIPT_GUARD = '''\
def git_env():
    env = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}
    env["GIT_OPTIONAL_LOCKS"] = "0"
    env["GIT_NO_REPLACE_OBJECTS"] = "1"
    return env


def run(repo):
    subprocess.run(["git", "-C", repo, "ls-tree", "-r", "HEAD"], env=git_env())
'''
MODULE_CONST_GUARD = '''\
GIT_ENV = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}
GIT_ENV["GIT_NO_REPLACE_OBJECTS"] = "1"


def git(repo, *args):
    return subprocess.run(["git", "-C", repo] + list(args), env=GIT_ENV)


def head(repo):
    return git(repo, "show", "HEAD:a")
'''
UNRELATED_DICT = '''\
def run(repo):
    labels = {"GIT_NO_REPLACE_OBJECTS": "documented"}
    subprocess.run(["git", "-C", repo, "show", "HEAD:a"], env=labels)
'''
COMMENT_ONLY = '''\
# The guard GIT_NO_REPLACE_OBJECTS is deliberately not set here.
def run(repo):
    subprocess.run(["git", "-C", repo, "rev-parse", "HEAD"])
'''
DOCSTRING_ONLY = '''\
"""Reads objects with git show; GIT_NO_REPLACE_OBJECTS is not set."""


def run(repo):
    subprocess.run(["git", "-C", repo, "show", "HEAD:a"], env=dict(os.environ))
'''
DICT_KEYWORD_GUARD = '''\
def run(repo):
    env = dict(os.environ, GIT_NO_REPLACE_OBJECTS="1")
    subprocess.run(["git", "-C", repo, "log", "-1"], env=env)
'''
NON_READER = '''\
def build(repo):
    subprocess.run(["git", "-C", repo, "init", "-q"])
    subprocess.run(["git", "-C", repo, "add", "-A"])
'''


def _selftest_checks():
    checks = []

    def want(name, cond):
        checks.append((name, bool(cond)))

    want("guarded dict is reader+guard", classify(GUARDED_DICT) == (True, True))
    want("unguarded dict is reader without guard", classify(UNGUARDED_DICT) == (True, False))
    want("inherited env is reader without guard", classify(INHERIT) == (True, False))
    want("comprehension env is reader without guard", classify(AXIS_SHAPE) == (True, False))
    want("subscript store is a guard", classify(SUBSCRIPT_GUARD) == (True, True))
    want("module-const env with guard is a guard", classify(MODULE_CONST_GUARD) == (True, True))
    want("comment mention is not a guard", classify(COMMENT_ONLY) == (True, False))
    want("docstring mention is not a guard", classify(DOCSTRING_ONLY) == (True, False))
    want("dict() keyword is a guard", classify(DICT_KEYWORD_GUARD) == (True, True))
    want("unrelated dict handed to env is not a guard",
         classify(UNRELATED_DICT) == (True, False))
    want("git init/add only is not a reader", classify(NON_READER) == (False, False))
    want("verb without the git token is not a reader",
         classify("x = ['show', 'cat-file']\n") == (False, False))
    want("git token without a verb is not a reader",
         classify("subprocess.run(['git', '-C', d, 'status'])\n") == (False, False))
    want("broken source is not a guard", classify("def f(:\n") == (False, False))
    want("contract line shape",
         bool(CONTRACT_RE.fullmatch(
             "MADO_R68_READER_GUARD: population=20 readers=13 guarded=13 unguarded=0 "
             "controls=7/7 verdict=TARGET_MET rev=" + "a" * 40)))
    want("contract line refuses a wrong verdict word",
         not CONTRACT_RE.fullmatch(
             "MADO_R68_READER_GUARD: population=20 readers=13 guarded=13 unguarded=0 "
             "controls=7/7 verdict=DONE rev=" + "a" * 40))
    want("guard inside a non-env call keyword is not a guard",
         classify('def f(repo):\n    g(["git", "-C", repo, "show", "HEAD:a"], '
                  'labels={"GIT_NO_REPLACE_OBJECTS": "1"})\n')[1] is False)
    return checks


def selftest():
    """Hermetic: no process may spawn while the classifier is exercised."""
    real_run = subprocess.run
    spawned = []

    def forbid(*args, **kwargs):
        spawned.append(args)
        raise AssertionError("selftest spawned a process")

    subprocess.run = forbid
    try:
        checks = _selftest_checks()
    finally:
        subprocess.run = real_run
    passed = 0
    for name, ok in checks:
        if ok:
            passed += 1
        else:
            print("MADO_R68_SELFTEST FAIL: %s" % name)
    print("MADO_R68_READER_GUARD_SELFTEST: %d/%d assertions passed" % (passed, len(checks)))
    if spawned:
        print("MADO_R68_SELFTEST FAIL: spawned=%d" % len(spawned))
        return 1
    return 0 if passed == len(checks) else 1


# --------------------------------------------------------------------------------------------- cli
def main(argv=None):
    ap = argparse.ArgumentParser(add_help=True)
    ap.add_argument("--repo")
    ap.add_argument("--rev")
    ap.add_argument("--controls")
    ap.add_argument("--selftest", action="store_true")
    args = ap.parse_args(argv)
    try:
        if args.selftest:
            return selftest()
        if not args.repo or not args.rev:
            raise UsageError("--repo and --rev are required")
        return measure(os.path.abspath(args.repo), args.rev, args.controls)
    except UsageError as exc:
        print("%s: %s" % (TOOL, exc), file=sys.stderr)
        return 2
    except SetupError as exc:
        print("%s: setup error: %s" % (TOOL, exc), file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
