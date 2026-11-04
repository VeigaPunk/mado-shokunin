#!/usr/bin/env python3
"""Round-69 C2 counter: the guard census requires key position **and** dominance.

    python3 quality/counters/c2-r69-guard-dominance.py --repo . --rev REV \
        --base-rev BASE --controls .ufo/waves/round-69/controls/c2-controls-r69.json \
        --scratch-root DIR
    python3 quality/counters/c2-r69-guard-dominance.py --selftest --scratch-root DIR

Population: every tracked file whose path matches `quality/check-*.py` at `--rev`, enumerated
from git objects (never the worktree) through a scrubbed git environment.

Reader: the blob carries a `git` command token and at least one quoted object-read verb from
the frozen vocabulary (the round-68 rule, unchanged).

Guarded: the blob puts `GIT_NO_REPLACE_OBJECTS` in **key position** of an environment mapping
and that guarded environment **dominates** a process launch of `git`.
  * key position: a dict-literal key, a spread (`{**{KEY: "1"}}`, `dict(**{KEY: "1"})`), a
    subscript store `env[KEY] = ...`, an `update`/`setdefault` keyword on an env-named name, or
    a `dict(KEY=...)` keyword. The same string in value position is not a key.
  * dominance, one module, one hop:
      (a) inline `env=<guarded mapping>` (or `env=<producer call>`) at the git call;
      (b) an env-named name bound to a guarded mapping (or to a local producer that returns
          one), used as `env=` at the git call with no intervening rebinding of the name to a
          mapping without the key;
      (c) the guarded name passed as an argument for a locally defined function's env-named
          parameter, where that parameter is passed as `env=` at the git call.
  Constructions inside a literal-false branch (`if False:` / `while False:`) do not count; the
  `else` arm of such a branch is live.

Controls: the frozen JSON must parse, carry exactly 11 cases, and hash to
`975ca3ba37341b5a058dec4fa76278d548996738e8b517616181824a841f90b9`; a case scores correct
only when reader and guard both match. Anything else is a setup error (exit 2).

Base leg: `quality/counters/c2-r68-reader-guard.py` is extracted at `--base-rev` into
`--scratch-root` and loaded; its `classify` scores the same 11 cases (`base_controls=<m>/11`).
The round-68 classifier must score 7/11 on this set — the do-nothing control.

Contract line (exact):

    MADO_R69_GUARD_DOMINANCE: population=20 readers=13 guarded=13 unguarded=0 \
controls=<n>/11 base_controls=<m>/11 verdict=<TARGET_MET|TARGET_MISSED> rev=<sha>

Exit 0 iff population==20, readers==13, guarded==13, unguarded==0, controls==11/11 and
base_controls==7/11; 1 otherwise; 2 on setup/usage error (reason on stderr).

Bounds (the claim says so): a bounded syntactic approximation — one module, one hop, no
alias/attribute/container flow (so `env[KEY_NAME]` where a constant name holds the string is
*not* a key position), no path-sensitivity beyond a literal-false branch, no cross-module
producer. It does not interpret the value: `GIT_NO_REPLACE_OBJECTS=0` would also disable the
guard at runtime, and a guarded environment is not evidence that git ran.

`--selftest` is hermetic: it parses and classifies in-memory sources only, spawns nothing
(every `subprocess` entry point is replaced by a tripwire for the duration), and writes
nothing; it validates `--scratch-root` with the lane's refusal rules and never creates it.
"""
import argparse
import ast
import hashlib
import importlib.util
import json
import os
import re
import subprocess
import sys

TOOL = "c2-r69-guard-dominance.py"
POPULATION_RE = re.compile(r"^quality/check-[^/]+\.py$")
GIT_TOKEN_RE = re.compile(r"(?<![A-Za-z0-9_-])git(?![A-Za-z0-9_-])")
VERBS = ("show", "cat-file", "ls-tree", "rev-parse", "diff-tree", "log", "merge-base",
         "for-each-ref")
VERB_RE = re.compile(r"[\"'](%s)[\"']" % "|".join(re.escape(v) for v in VERBS))
KEY = "GIT_NO_REPLACE_OBJECTS"
BASE_COUNTER = "quality/counters/c2-r68-reader-guard.py"
CONTROLS_SHA256 = "975ca3ba37341b5a058dec4fa76278d548996738e8b517616181824a841f90b9"
FROZEN_POPULATION = 20
FROZEN_READERS = 13
FROZEN_GUARDED = 13
FROZEN_UNGUARDED = 0
FROZEN_CONTROLS = 11
FROZEN_BASE_CONTROLS = 7
UNSAFE_ROOTS = ("/tmp", "/var/tmp", "/dev/shm")
CONTRACT_RE = re.compile(
    r"MADO_R69_GUARD_DOMINANCE: population=[0-9]+ readers=[0-9]+ guarded=[0-9]+ "
    r"unguarded=[0-9]+ controls=[0-9]+/[0-9]+ base_controls=[0-9]+/[0-9]+ "
    r"verdict=(?:TARGET_MET|TARGET_MISSED) rev=[0-9a-f]{40,64}")
SCOPE_BOUNDARIES = (ast.FunctionDef, ast.AsyncFunctionDef, ast.Lambda, ast.ClassDef)


class UsageError(Exception):
    pass


class SetupError(Exception):
    pass


def yesno(flag):
    return "yes" if flag else "no"


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


def scratch_root(root):
    """The lane's scratch guard: absolute, symlink-free, outside the tmp family, a directory."""
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


# --------------------------------------------------------------------------------------------- ast
def env_named(name):
    return "env" in name.lower()


def is_key_literal(node):
    return isinstance(node, ast.Constant) and isinstance(node.value, str) and node.value == KEY


def is_git_argv(node):
    """A literal argv sequence naming git: a list/tuple with a `git` element."""
    if not isinstance(node, (ast.List, ast.Tuple)):
        return False
    return any(isinstance(el, ast.Constant) and el.value == "git" for el in node.elts)


def argv_binding_names(tree):
    """Names bound to an expression that contains a literal argv naming git."""
    out = set()
    for node in ast.walk(tree):
        value = getattr(node, "value", None)
        targets = getattr(node, "targets", None)
        if isinstance(node, (ast.Assign, ast.AnnAssign)) and value is not None:
            targets = targets or [node.target]
            if any(is_git_argv(sub) for sub in ast.walk(node.value)):
                for target in targets:
                    if isinstance(target, ast.Name):
                        out.add(target.id)
    return out


def carries_key(node):
    """True iff the expression is a mapping that puts KEY in key position.

    A plain nested value (`{"LABEL": {KEY: "1"}}`) is not key position; a `**` spread of a
    mapping literal is (its keys land in this mapping), and so is a `dict(KEY=...)` keyword.
    """
    if node is None:
        return False
    if isinstance(node, ast.Dict):
        for key, value in zip(node.keys, node.values):
            if key is None:
                if carries_key(value):
                    return True
            elif is_key_literal(key):
                return True
        return False
    if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id == "dict":
        for kw in node.keywords:
            if kw.arg == KEY:
                return True
            if kw.arg is None and carries_key(kw.value):
                return True
    return False


def dead_lines(tree):
    """Line numbers inside a literal-false branch body (the `else` arm is live)."""
    bad = set()

    def walk(node):
        for child in ast.iter_child_nodes(node):
            if isinstance(child, (ast.If, ast.While)) and isinstance(
                    child.test, ast.Constant) and not child.test.value:
                for stmt in child.body:
                    for sub in ast.walk(stmt):
                        if hasattr(sub, "lineno"):
                            bad.add(sub.lineno)
            walk(child)

    walk(tree)
    return bad


def function_scopes(tree):
    yield tree
    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            yield node


def all_functions(tree):
    return [node for node in ast.walk(tree)
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))]


def local_functions(tree):
    out = {}
    for node in all_functions(tree):
        out.setdefault(node.name, node)
    return out


def scope_nodes(scope):
    """Statements of this lexical scope; nested function/class bodies are not entered."""
    stack = list(getattr(scope, "body", []))
    while stack:
        node = stack.pop()
        if isinstance(node, SCOPE_BOUNDARIES):
            continue
        if hasattr(node, "lineno"):
            yield node
        for child in ast.iter_child_nodes(node):
            stack.append(child)


def scope_params(scope):
    args = getattr(scope, "args", None)
    if args is None:
        return set()
    names = {arg.arg for arg in list(args.posonlyargs) + list(args.args) + list(args.kwonlyargs)}
    if args.vararg is not None:
        names.add(args.vararg.arg)
    if args.kwarg is not None:
        names.add(args.kwarg.arg)
    return names


class Census:
    """One blob's guard census: argv names, dead lines, producers, lexical scopes."""

    def __init__(self, tree):
        self.tree = tree
        self.argv_names = argv_binding_names(tree)
        self.dead = dead_lines(tree)
        self.functions = local_functions(tree)
        self.parents = {}
        for parent in ast.walk(tree):
            for child in ast.iter_child_nodes(parent):
                self.parents[child] = parent
        self.producers = self._producers()

    # -- git call detection ---------------------------------------------------------------------
    def call_is_git(self, call):
        for arg in list(call.args) + [kw.value for kw in call.keywords]:
            if is_git_argv(arg):
                return True
            if isinstance(arg, ast.Name) and arg.id in self.argv_names:
                return True
            for sub in ast.walk(arg):
                if is_git_argv(sub):
                    return True
        return False

    def is_producer_call(self, value, producers):
        return (isinstance(value, ast.Call) and isinstance(value.func, ast.Name)
                and value.func.id in producers)

    # -- guarded constructions ------------------------------------------------------------------
    def guarded_constructions(self, scope, producers):
        """name -> lines where this scope puts KEY into the name's mapping or binds a guarded map."""
        out = {}
        for node in scope_nodes(scope):
            if node.lineno in self.dead:
                continue
            if isinstance(node, ast.Assign):
                for target in node.targets:
                    if isinstance(target, ast.Name) and env_named(target.id):
                        if carries_key(node.value) or self.is_producer_call(node.value, producers):
                            out.setdefault(target.id, set()).add(node.lineno)
                    elif (isinstance(target, ast.Subscript) and isinstance(target.ctx, ast.Store)
                          and isinstance(target.value, ast.Name) and env_named(target.value.id)
                          and is_key_literal(target.slice)):
                        out.setdefault(target.value.id, set()).add(node.lineno)
            elif isinstance(node, ast.AnnAssign):
                target = node.target
                if (isinstance(target, ast.Name) and env_named(target.id)
                        and node.value is not None
                        and (carries_key(node.value)
                             or self.is_producer_call(node.value, producers))):
                    out.setdefault(target.id, set()).add(node.lineno)
            elif isinstance(node, ast.Call):
                func = node.func
                if (isinstance(func, ast.Attribute) and func.attr in ("update", "setdefault")
                        and isinstance(func.value, ast.Name) and env_named(func.value.id)
                        and any(kw.arg == KEY for kw in node.keywords)):
                    out.setdefault(func.value.id, set()).add(node.lineno)
        return out

    def rebindings(self, scope, producers):
        """name -> lines where a plain assignment replaces the mapping without the key."""
        out = {}
        for node in scope_nodes(scope):
            if node.lineno in self.dead:
                continue
            if isinstance(node, ast.Assign):
                for target in node.targets:
                    if (isinstance(target, ast.Name) and env_named(target.id)
                            and not carries_key(node.value)
                            and not self.is_producer_call(node.value, producers)):
                        out.setdefault(target.id, set()).add(node.lineno)
            elif isinstance(node, ast.AnnAssign) and isinstance(node.target, ast.Name) \
                    and env_named(node.target.id) and node.value is not None \
                    and not carries_key(node.value) \
                    and not self.is_producer_call(node.value, producers):
                out.setdefault(node.target.id, set()).add(node.lineno)
        return out

    def plain_binding_lines(self, scope, name):
        """Lines where a plain assignment rebinds `name` (mutations such as env[k] = v do not)."""
        lines = []
        for node in scope_nodes(scope):
            if isinstance(node, ast.Assign):
                for target in node.targets:
                    if isinstance(target, ast.Name) and target.id == name:
                        lines.append(node.lineno)
            elif isinstance(node, ast.AnnAssign) and isinstance(node.target, ast.Name) \
                    and node.target.id == name and node.value is not None:
                lines.append(node.lineno)
            elif isinstance(node, ast.For) and isinstance(node.target, ast.Name) \
                    and node.target.id == name:
                lines.append(node.lineno)
        return lines

    def _producers(self):
        out = set()
        for fn in all_functions(self.tree):
            guards = self.guarded_constructions(fn, frozenset())
            returns = sorted((node for node in scope_nodes(fn)
                              if isinstance(node, ast.Return) and node.lineno not in self.dead),
                             key=lambda node: node.lineno)
            if returns and self._returns_guarded(fn, returns, guards):
                out.add(fn.name)
        return out

    def _returns_guarded(self, fn, returns, guards):
        """Every reachable return of a producer must hand back a key-carrying mapping."""
        for ret in returns:
            if ret.value is None:
                return False
            if isinstance(ret.value, ast.Name):
                guards_here = guards.get(ret.value.id, set())
                if not guards_here:
                    return False
                rebinds = [line for line in self.plain_binding_lines(fn, ret.value.id)
                           if line <= ret.lineno]
                if not rebinds or max(rebinds) in guards_here \
                        or any(max(rebinds) < line <= ret.lineno for line in guards_here):
                    continue
                return False
            elif not carries_key(ret.value):
                return False
        return True

    # -- one-hop flow ---------------------------------------------------------------------------
    def env_params_reaching_git(self, fn):
        """Env-named parameters of fn handed as `env=` to a git call in fn's own scope."""
        params = {name for name in scope_params(fn) if env_named(name)}
        if not params:
            return set()
        guards = self.guarded_constructions(fn, self.producers)
        out = set()
        for node in scope_nodes(fn):
            if not isinstance(node, ast.Call) or node.lineno in self.dead:
                continue
            if not self.call_is_git(node):
                continue
            for kw in node.keywords:
                if kw.arg != "env" or not isinstance(kw.value, ast.Name):
                    continue
                name = kw.value.id
                if name not in params:
                    continue
                rebinds = [line for line in self.plain_binding_lines(fn, name)
                           if line < node.lineno]
                if rebinds and max(rebinds) not in guards.get(name, set()):
                    continue
                out.add(name)
        return out

    def argument_binds(self, call, name, targets):
        """Is `name` passed at the position of one of the parameters in `targets`?"""
        fn = self.functions.get(call.func.id) if isinstance(call.func, ast.Name) else (
            self.functions.get(call.func.attr) if isinstance(call.func, ast.Attribute) else None)
        if fn is None:
            return False
        positional = list(fn.args.posonlyargs) + list(fn.args.args)
        for index, arg in enumerate(call.args):
            if isinstance(arg, ast.Starred):
                break
            if isinstance(arg, ast.Name) and arg.id == name and index < len(positional) \
                    and positional[index].arg in targets:
                return True
        for kw in call.keywords:
            if kw.arg in targets and isinstance(kw.value, ast.Name) and kw.value.id == name:
                return True
        return False

    # -- lexical resolution ---------------------------------------------------------------------
    def function_chain(self, node):
        chain = []
        cur = self.parents.get(node)
        while cur is not None:
            if isinstance(cur, (ast.FunctionDef, ast.AsyncFunctionDef, ast.Lambda)):
                chain.append(cur)
            cur = self.parents.get(cur)
        chain.reverse()
        return chain

    def binds_name(self, scope, name):
        if name in scope_params(scope):
            return True
        for node in scope_nodes(scope):
            if isinstance(node, ast.Assign):
                if any(isinstance(t, ast.Name) and t.id == name for t in node.targets):
                    return True
            elif isinstance(node, ast.AnnAssign) and isinstance(node.target, ast.Name) \
                    and node.target.id == name:
                return True
            elif isinstance(node, ast.AugAssign) and isinstance(node.target, ast.Name) \
                    and node.target.id == name:
                return True
            elif isinstance(node, ast.For) and isinstance(node.target, ast.Name) \
                    and node.target.id == name:
                return True
            elif isinstance(node, ast.With):
                for item in node.items:
                    if isinstance(item.optional_vars, ast.Name) and item.optional_vars.id == name:
                        return True
            elif isinstance(node, ast.ExceptHandler) and node.name == name:
                return True
            elif isinstance(node, ast.NamedExpr) and isinstance(node.target, ast.Name) \
                    and node.target.id == name:
                return True
        return False

    def shadowed(self, guard_scope, call, name):
        chain = self.function_chain(call)
        start = 0
        if guard_scope is not self.tree:
            for index, scope in enumerate(chain):
                if scope is guard_scope:
                    start = index + 1
                    break
            else:
                return True
        for scope in chain[start:]:
            if self.binds_name(scope, name):
                return True
        return False

    # -- dominance ------------------------------------------------------------------------------
    def call_mentions(self, call, name):
        for arg in list(call.args) + [kw.value for kw in call.keywords]:
            if isinstance(arg, ast.Name) and arg.id == name:
                return True
        return False

    def use_lines(self, scope, name):
        """Lines where this scope's binding of `name` reaches a process launch of git."""
        lines = set()
        for node in ast.walk(scope):
            if not isinstance(node, ast.Call) or not self.call_mentions(node, name):
                continue
            if self.shadowed(scope, node, name):
                continue
            if self.call_is_git(node):
                if any(kw.arg == "env" and isinstance(kw.value, ast.Name)
                       and kw.value.id == name for kw in node.keywords):
                    lines.add(node.lineno)
                continue
            targets = set()
            fn = self.functions.get(node.func.id) if isinstance(node.func, ast.Name) else (
                self.functions.get(node.func.attr) if isinstance(node.func, ast.Attribute) else None)
            if fn is not None:
                targets = self.env_params_reaching_git(fn)
            if targets and self.argument_binds(node, name, targets):
                lines.add(node.lineno)
        return lines

    def inline_guarded_call(self):
        for node in ast.walk(self.tree):
            if not isinstance(node, ast.Call) or node.lineno in self.dead:
                continue
            if not self.call_is_git(node):
                continue
            for kw in node.keywords:
                if kw.arg != "env":
                    continue
                if carries_key(kw.value) or self.is_producer_call(kw.value, self.producers):
                    return True
        return False

    def dominates(self):
        if self.inline_guarded_call():
            return True
        for scope in function_scopes(self.tree):
            guards = self.guarded_constructions(scope, self.producers)
            if not guards:
                continue
            rebinds = self.rebindings(scope, self.producers)
            for name, guard_lines in guards.items():
                uses = self.use_lines(scope, name)
                for guard in sorted(guard_lines):
                    later = sorted(line for line in uses if line > guard)
                    if not later:
                        continue
                    first = later[0]
                    if any(guard < line < first for line in rebinds.get(name, ())):
                        continue
                    return True
        return False


def is_reader(src):
    return bool(GIT_TOKEN_RE.search(src)) and bool(VERB_RE.search(src))


def has_guard(src):
    try:
        tree = ast.parse(src)
    except SyntaxError:
        return False
    if not GIT_TOKEN_RE.search(src):
        return False
    return Census(tree).dominates()


def classify(src):
    reader = is_reader(src)
    return reader, (has_guard(src) if reader else False)


# --------------------------------------------------------------------------------------------- controls
def load_controls(path):
    try:
        with open(path, "rb") as handle:
            raw = handle.read()
    except OSError as exc:
        raise SetupError("controls file unusable: %s" % exc)
    digest = hashlib.sha256(raw).hexdigest()
    if digest != CONTROLS_SHA256:
        raise SetupError("controls file sha256 %s does not match the frozen digest" % digest)
    try:
        payload = json.loads(raw.decode("utf-8"))
    except (UnicodeDecodeError, ValueError) as exc:
        raise SetupError("controls file is not JSON: %s" % exc)
    cases = payload.get("cases") if isinstance(payload, dict) else None
    if not isinstance(cases, list):
        raise SetupError("controls file carries no cases list")
    if len(cases) != FROZEN_CONTROLS:
        raise SetupError("controls file carries %d cases, the frozen set has %d"
                         % (len(cases), FROZEN_CONTROLS))
    for index, case in enumerate(cases):
        if not isinstance(case, dict):
            raise SetupError("control case %d is not an object" % index)
        for field in ("name", "src"):
            if not isinstance(case.get(field), str):
                raise SetupError("control case %d has no string %s" % (index, field))
        for field in ("expect_reader", "expect_guard"):
            if not isinstance(case.get(field), bool):
                raise SetupError("control case %d has no boolean %s" % (index, field))
    return cases


def load_base_classify(repo, base_sha, scratch):
    """Extract the round-68 counter at --base-rev into scratch and return its classify."""
    try:
        blob = git(repo, ["show", "%s:%s" % (base_sha, BASE_COUNTER)])
    except SetupError as exc:
        raise SetupError("base counter absent at %s: %s" % (base_sha, exc))
    try:
        os.makedirs(scratch, exist_ok=True)
        target = os.path.join(scratch, "c2-r68-reader-guard.py")
        with open(target, "wb") as handle:
            handle.write(blob)
    except OSError as exc:
        raise SetupError("cannot place the base counter under the scratch root: %s" % exc)
    spec = importlib.util.spec_from_file_location("mado_r69_base_reader_guard", target)
    if spec is None or spec.loader is None:
        raise SetupError("cannot load the base counter from %s" % target)
    module = importlib.util.module_from_spec(spec)
    try:
        spec.loader.exec_module(module)
    except Exception as exc:  # noqa: BLE001 - any import failure is a setup error here
        raise SetupError("base counter import failed: %s" % exc)
    classify_fn = getattr(module, "classify", None)
    if not callable(classify_fn):
        raise SetupError("base counter exposes no callable classify")
    return classify_fn


# --------------------------------------------------------------------------------------------- measure
def verdict_met(population, readers, guarded, unguarded, correct, controls_total,
                base_correct, base_total):
    """The frozen target, verbatim: counts and control scores are all part of it."""
    return (population == FROZEN_POPULATION and readers == FROZEN_READERS
            and guarded == FROZEN_GUARDED and unguarded == FROZEN_UNGUARDED
            and controls_total == FROZEN_CONTROLS and correct == controls_total
            and base_total == FROZEN_CONTROLS and base_correct == FROZEN_BASE_CONTROLS)


def contract_line(population, readers, guarded, unguarded, correct, controls_total,
                  base_correct, base_total, verdict, sha):
    return ("MADO_R69_GUARD_DOMINANCE: population=%d readers=%d guarded=%d unguarded=%d "
            "controls=%d/%d base_controls=%d/%d verdict=%s rev=%s"
            % (population, readers, guarded, unguarded, correct, controls_total,
               base_correct, base_total, verdict, sha))


def resolve(repo, rev):
    return git(repo, ["rev-parse", "--verify", rev + "^{commit}"]).decode(
        "ascii", "replace").strip()


def blob(repo, sha, path):
    return git(repo, ["show", "%s:%s" % (sha, path)]).decode("utf-8", "replace")


def measure(repo, rev, base_rev, controls_path, scratch_arg):
    if not os.path.isdir(repo):
        raise SetupError("--repo is not a directory: %s" % repo)
    scratch = scratch_root(scratch_arg)
    cases = load_controls(controls_path)
    sha = resolve(repo, rev)
    base_sha = resolve(repo, base_rev)
    names = git(repo, ["ls-tree", "-r", "--name-only", sha, "--", "quality"]).decode(
        "utf-8", "replace").splitlines()
    population = sorted(path for path in names if POPULATION_RE.match(path))
    if not population:
        raise SetupError("population is empty at %s" % sha)
    readers = guarded = 0
    for path in population:
        reader, guard = classify(blob(repo, sha, path))
        if reader:
            readers += 1
            guarded += int(guard)
        print("MADO_R69_GUARD file=%s reader=%s guard=%s"
              % (path, yesno(reader), yesno(guard)))
    unguarded = readers - guarded

    correct = 0
    for case in cases:
        reader, guard = classify(case["src"])
        ok = reader == case["expect_reader"] and guard == case["expect_guard"]
        correct += int(ok)
        print("MADO_R69_CONTROL name=%s reader=%s guard=%s expect_reader=%s "
              "expect_guard=%s correct=%s"
              % (case["name"], yesno(reader), yesno(guard),
                 yesno(case["expect_reader"]), yesno(case["expect_guard"]), yesno(ok)))

    base_classify = load_base_classify(repo, base_sha, scratch)
    base_correct = 0
    for case in cases:
        reader, guard = base_classify(case["src"])
        ok = reader == case["expect_reader"] and guard == case["expect_guard"]
        base_correct += int(ok)
        print("MADO_R69_BASE_CONTROL name=%s reader=%s guard=%s expect_reader=%s "
              "expect_guard=%s correct=%s"
              % (case["name"], yesno(reader), yesno(guard),
                 yesno(case["expect_reader"]), yesno(case["expect_guard"]), yesno(ok)))

    met = verdict_met(len(population), readers, guarded, unguarded, correct, len(cases),
                      base_correct, len(cases))
    line = contract_line(len(population), readers, guarded, unguarded, correct, len(cases),
                         base_correct, len(cases),
                         "TARGET_MET" if met else "TARGET_MISSED", sha)
    if not CONTRACT_RE.fullmatch(line):
        raise SetupError("emitted contract line does not match CONTRACT_RE")
    print(line)
    return 0 if met else 1


# --------------------------------------------------------------------------------------------- selftest
CONTROL_CASES = (
    ("guarded-inline",
     '''\
def run(repo):
    subprocess.run(["git", "-C", repo, "show", "HEAD:a"],
                   env=dict(os.environ, GIT_NO_REPLACE_OBJECTS="1"))
''', True, True),
    ("value-position-only",
     '''\
def run(repo):
    env = {"PATH": "/usr/bin", "LABEL": "GIT_NO_REPLACE_OBJECTS"}
    subprocess.run(["git", "-C", repo, "show", "HEAD:a"], env=env)
''', True, False),
    ("dead-branch-only",
     '''\
def run(repo):
    env = {"PATH": "/usr/bin"}
    if False:
        env["GIT_NO_REPLACE_OBJECTS"] = "1"
    subprocess.run(["git", "-C", repo, "show", "HEAD:a"], env=env)
''', True, False),
    ("uncalled-helper",
     '''\
def guarded_env():
    env = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}
    env["GIT_NO_REPLACE_OBJECTS"] = "1"
    return env


def run(repo):
    plain = {"PATH": "/usr/bin"}
    subprocess.run(["git", "-C", repo, "show", "HEAD:a"], env=plain)
''', True, False),
    ("overwritten-env",
     '''\
def run(repo):
    env = {"PATH": "/usr/bin", "GIT_NO_REPLACE_OBJECTS": "1"}
    env = {"PATH": "/usr/bin"}
    subprocess.run(["git", "-C", repo, "show", "HEAD:a"], env=env)
''', True, False),
    ("update-guard",
     '''\
def run(repo):
    env = {}
    env.update(GIT_NO_REPLACE_OBJECTS="1")
    subprocess.run(["git", "-C", repo, "ls-tree", "-r", "HEAD"], env=env)
''', True, True),
    ("subscript-guard",
     '''\
def git(repo, *args):
    env = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}
    env["GIT_NO_REPLACE_OBJECTS"] = "1"
    return subprocess.run(["git", "-C", repo] + list(args), env=env)


def head(repo):
    return git(repo, "show", "HEAD:a")
''', True, True),
    ("module-constant",
     '''\
GIT_ENV = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}
GIT_ENV["GIT_NO_REPLACE_OBJECTS"] = "1"


def head(repo):
    return subprocess.run(["git", "-C", repo, "show", "HEAD:a"], env=GIT_ENV)
''', True, True),
    ("producer-helper",
     '''\
def git_env(work):
    env = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}
    env["GIT_NO_REPLACE_OBJECTS"] = "1"
    return env


def run(repo, work):
    env = git_env(work)
    return subprocess.run(["git", "-C", repo, "show", "HEAD:a"], env=env)
''', True, True),
    ("argv-name-flow",
     '''\
def run(repo):
    cmd = ["git", "-C", repo, "show", "HEAD:a"]
    subprocess.run(cmd, capture_output=True, env=git_env())


def git_env():
    env = {"PATH": "/usr/bin"}
    env["GIT_NO_REPLACE_OBJECTS"] = "1"
    return env
''', True, True),
    ("mention-only",
     '''\
"""Reads objects with git show; GIT_NO_REPLACE_OBJECTS is not set here."""


def run(repo):
    # the guard GIT_NO_REPLACE_OBJECTS is deliberately absent in this sample
    subprocess.run(["git", "-C", repo, "show", "HEAD:a"], env=dict(os.environ))
''', True, False),
)
REJECTED_SHAPES = ("value-position-only", "dead-branch-only", "uncalled-helper",
                   "overwritten-env")
ACCEPTED_SHAPES = ("guarded-inline", "update-guard", "subscript-guard", "module-constant",
                   "producer-helper", "argv-name-flow")

DEAD_INLINE = '''\
import os, subprocess
KEY = "GIT_NO_REPLACE_OBJECTS"
if False:
    subprocess.run(["git", "show", "HEAD:a"], env={"GIT_NO_REPLACE_OBJECTS": "1"})
'''
DEAD_ELSE = '''\
import subprocess
if False:
    pass
else:
    env = {"GIT_NO_REPLACE_OBJECTS": "1"}
subprocess.run(["git", "show", "HEAD:a"], env=env)
'''
PRODUCER_OVERWRITE = '''\
import subprocess
def git_env():
    env = {"GIT_NO_REPLACE_OBJECTS": "1"}
    env = {}
    return env
env = git_env()
subprocess.run(["git", "show", "HEAD:a"], env=env)
'''
PRODUCER_LATE = '''\
import subprocess
def git_env():
    env = {}
    return env
    env["GIT_NO_REPLACE_OBJECTS"] = "1"
env = git_env()
subprocess.run(["git", "show", "HEAD:a"], env=env)
'''
SIBLING_SCOPE = '''\
import subprocess
def never():
    env = {"GIT_NO_REPLACE_OBJECTS": "1"}


def run():
    subprocess.run(["git", "show", "HEAD:a"], env=env)
'''
NESTED_KEY_VALUE = '''\
import subprocess
env = {"LABEL": {"GIT_NO_REPLACE_OBJECTS": "1"}}
subprocess.run(["git", "show", "HEAD:a"], env=env)
'''
ONEHOP_WRONG_PARAM = '''\
import subprocess
def launch(env, other_env):
    subprocess.run(["git", "show", "HEAD:a"], env=other_env)


def run(repo):
    env = {"GIT_NO_REPLACE_OBJECTS": "1"}
    launch(env, {})
'''
ONEHOP_OK = '''\
import subprocess
def launch(repo, env):
    subprocess.run(["git", "show", "HEAD:a"], env=env)


def run(repo):
    env = {"GIT_NO_REPLACE_OBJECTS": "1"}
    launch(repo, env)
'''
CLOSURE_ENV = '''\
import subprocess
def outer():
    env = {"GIT_NO_REPLACE_OBJECTS": "1"}
    def inner():
        subprocess.run(["git", "show", "HEAD:a"], env=env)
    return inner()
'''
SPLAT_LITERAL = '''\
import subprocess
env = {**{"GIT_NO_REPLACE_OBJECTS": "1"}}
subprocess.run(["git", "show", "HEAD:a"], env=env)
'''
NAME_KEY_SUBSCRIPT = '''\
import subprocess
KEY = "GIT_NO_REPLACE_OBJECTS"
env = {}
env[KEY] = "1"
subprocess.run(["git", "show", "HEAD:a"], env=env)
'''
PRODUCER_DIRECT = '''\
import subprocess
def git_env():
    return {"GIT_NO_REPLACE_OBJECTS": "1"}
env = git_env()
subprocess.run(["git", "show", "HEAD:a"], env=env)
'''
MULTITARGET_REBIND = '''\
import subprocess
def run():
    env = {"GIT_NO_REPLACE_OBJECTS": "1"}
    env = other = {}
    subprocess.run(["git", "show", "HEAD:a"], env=env)
'''
PARAM_REBIND = '''\
import subprocess
def launch(env):
    env = {}
    subprocess.run(["git", "show", "HEAD:a"], env=env)


def run():
    env = {"GIT_NO_REPLACE_OBJECTS": "1"}
    launch(env)
'''
UNREACHABLE_RETURN = '''\
import subprocess
def git_env():
    env = {}
    return env
    return {"GIT_NO_REPLACE_OBJECTS": "1"}
env = git_env()
subprocess.run(["git", "show", "HEAD:a"], env=env)
'''


def _raises(exc_type, fn):
    try:
        fn()
    except exc_type:
        return True
    except Exception:  # noqa: BLE001 - a different exception is a failed assertion
        return False
    return False


def _selftest_checks(scratch):
    checks = []

    def want(name, cond):
        checks.append((name, bool(cond)))

    for name, src, expect_reader, expect_guard in CONTROL_CASES:
        want("control %s classifies as declared" % name,
             classify(src) == (expect_reader, expect_guard))
    for name, src, _, _ in CONTROL_CASES:
        if name in REJECTED_SHAPES:
            want("rejected shape %s is reader+unguarded" % name,
                 classify(src) == (True, False))
        if name in ACCEPTED_SHAPES:
            want("accepted shape %s stays reader+guarded" % name,
                 classify(src) == (True, True))

    want("dead inline guard is not a guard", classify(DEAD_INLINE) == (True, False))
    want("a literal-false else arm is live", classify(DEAD_ELSE) == (True, True))
    want("producer rebound without the key is not a producer",
         classify(PRODUCER_OVERWRITE) == (True, False))
    want("guard constructed only after the return is not a producer",
         classify(PRODUCER_LATE) == (True, False))
    want("a sibling scope's guard does not dominate", classify(SIBLING_SCOPE) == (True, False))
    want("a nested mapping value is not key position",
         classify(NESTED_KEY_VALUE) == (True, False))
    want("one-hop argument for the wrong parameter does not dominate",
         classify(ONEHOP_WRONG_PARAM) == (True, False))
    want("one-hop argument for the env parameter dominates",
         classify(ONEHOP_OK) == (True, True))
    want("a closure use of the guarded name dominates",
         classify(CLOSURE_ENV) == (True, True))
    want("a spread literal mapping is key position", classify(SPLAT_LITERAL) == (True, True))
    want("a name-keyed subscript is outside the key-position rule",
         classify(NAME_KEY_SUBSCRIPT) == (True, False))
    want("a producer returning a mapping literal dominates",
         classify(PRODUCER_DIRECT) == (True, True))
    want("a multi-target rebinding without the key kills the guard",
         classify(MULTITARGET_REBIND) == (True, False))
    want("a callee parameter rebound without the key is not one-hop dominance",
         classify(PARAM_REBIND) == (True, False))
    want("an unguarded return before a guarded one is not a producer",
         classify(UNREACHABLE_RETURN) == (True, False))

    want("verdict met on the frozen target", verdict_met(20, 13, 13, 0, 11, 11, 7, 11))
    want("verdict rejects population 19", not verdict_met(19, 13, 13, 0, 11, 11, 7, 11))
    want("verdict rejects readers 12", not verdict_met(20, 12, 12, 0, 11, 11, 7, 11))
    want("verdict rejects guarded 12", not verdict_met(20, 13, 12, 1, 11, 11, 7, 11))
    want("verdict rejects an unguarded reader", not verdict_met(20, 13, 13, 1, 11, 11, 7, 11))
    want("verdict rejects controls 10/11", not verdict_met(20, 13, 13, 0, 10, 11, 7, 11))
    want("verdict rejects a controls total of 10", not verdict_met(20, 13, 13, 0, 10, 10, 7, 11))
    want("verdict rejects base_controls 11/11", not verdict_met(20, 13, 13, 0, 11, 11, 11, 11))
    want("verdict rejects base_controls 6/11", not verdict_met(20, 13, 13, 0, 11, 11, 6, 11))

    line = contract_line(20, 13, 13, 0, 11, 11, 7, 11, "TARGET_MET", "a" * 40)
    want("contract line matches the frozen shape", CONTRACT_RE.fullmatch(line) is not None)
    want("contract line carries the frozen target",
         line == ("MADO_R69_GUARD_DOMINANCE: population=20 readers=13 guarded=13 "
                  "unguarded=0 controls=11/11 base_controls=7/11 verdict=TARGET_MET "
                  "rev=" + "a" * 40))
    want("contract line refuses a wrong verdict word",
         not CONTRACT_RE.fullmatch(line.replace("TARGET_MET", "DONE")))
    want("contract line refuses a short rev", not CONTRACT_RE.fullmatch(line[:-39]))

    frozen = ["--repo", ".", "--rev", "HEAD",
              "--base-rev", "04093b83f73a841117d3b31dbb2a6063f4f2a454",
              "--controls", ".ufo/waves/round-69/controls/c2-controls-r69.json",
              "--scratch-root", "/fast/scratch/x"]
    parsed = build_parser().parse_args(frozen)
    want("the frozen counting command parses",
         parsed.repo == "." and parsed.rev == "HEAD"
         and parsed.base_rev == "04093b83f73a841117d3b31dbb2a6063f4f2a454"
         and parsed.controls == ".ufo/waves/round-69/controls/c2-controls-r69.json"
         and parsed.scratch_root == "/fast/scratch/x")
    parsed = build_parser().parse_args(["--selftest", "--scratch-root", "/fast/scratch/x"])
    want("the selftest command parses",
         parsed.selftest and parsed.scratch_root == "/fast/scratch/x")

    want("scratch accepts its own real directory",
         scratch_root(scratch) == os.path.normpath(scratch))
    want("relative scratch resolves under cwd",
         scratch_root(os.path.join("rel", "scratch"))
         == os.path.normpath(os.path.join(os.getcwd(), "rel", "scratch")))
    for bad in ("", "/", "/tmp", "/tmp/x", "/var/tmp/x", "/dev/shm/x"):
        want("scratch refuses %r" % (bad or "<empty>"),
             _raises(UsageError, lambda bad=bad: scratch_root(bad)))
    want("scratch refuses a regular file",
         _raises(UsageError, lambda: scratch_root(os.path.abspath(__file__))))
    return checks


def selftest(scratch_arg):
    try:
        scratch = scratch_root(scratch_arg)
    except UsageError as exc:
        print("%s: %s" % (TOOL, exc), file=sys.stderr)
        return 2
    saved = {}
    spawned = []

    def forbid(*args, **kwargs):
        spawned.append(args)
        raise AssertionError("selftest spawned a process")

    for attr in ("run", "Popen", "call", "check_call", "check_output"):
        saved[attr] = getattr(subprocess, attr)
        setattr(subprocess, attr, forbid)
    try:
        checks = _selftest_checks(scratch)
    finally:
        for attr, fn in saved.items():
            setattr(subprocess, attr, fn)
    passed = 0
    for name, ok in checks:
        if ok:
            passed += 1
        else:
            print("MADO_R69_GUARD_DOMINANCE_SELFTEST FAIL: %s" % name)
    print("MADO_R69_GUARD_DOMINANCE_SELFTEST: %d/%d assertions passed"
          % (passed, len(checks)))
    if spawned:
        print("MADO_R69_GUARD_DOMINANCE_SELFTEST FAIL: spawned=%d" % len(spawned))
        return 1
    return 0 if passed == len(checks) else 1


# --------------------------------------------------------------------------------------------- cli
def build_parser():
    ap = argparse.ArgumentParser(add_help=True)
    ap.add_argument("--repo")
    ap.add_argument("--rev")
    ap.add_argument("--base-rev", dest="base_rev")
    ap.add_argument("--controls")
    ap.add_argument("--scratch-root", dest="scratch_root")
    ap.add_argument("--selftest", action="store_true")
    return ap


def main(argv=None):
    args = build_parser().parse_args(argv)
    try:
        if args.selftest:
            return selftest(args.scratch_root)
        if not args.repo:
            raise UsageError("--repo is required")
        if not args.rev:
            raise UsageError("--rev is required")
        if not args.base_rev:
            raise UsageError("--base-rev is required")
        if not args.controls:
            raise UsageError("--controls is required")
        return measure(os.path.abspath(args.repo), args.rev, args.base_rev, args.controls,
                       args.scratch_root)
    except UsageError as exc:
        print("%s: %s" % (TOOL, exc), file=sys.stderr)
        return 2
    except SetupError as exc:
        print("%s: setup error: %s" % (TOOL, exc), file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
