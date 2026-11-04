#!/usr/bin/env python3
r"""Round-69 C2 counter: the guard census requires key position and dominance, not a mention
(claim C2, attempt 1).

    python3 quality/counters/c2-r69-guard-dominance.py --repo . --rev REV --base-rev BASE \
        --controls .ufo/waves/round-69/controls/c2-controls-r69.json --scratch-root DIR
    python3 quality/counters/c2-r69-guard-dominance.py --selftest \
        [--controls <frozen file>] --scratch-root DIR

Population: every tracked `quality/check-[^/]+\.py` file at --rev, read through a scrubbed git
environment (`GIT_OPTIONAL_LOCKS=0`, `GIT_NO_REPLACE_OBJECTS=1`, inherited GIT_* dropped).
Reader: a `git` token plus one of the frozen object-read verbs (the round-68 rule, unchanged).

Guarded (the new predicate, frozen in `.ufo/waves/round-69/claims-declaration-r69.md` C2):

  1. KEY POSITION. The guard key counts only as a *key* of an environment mapping — a
     dict-literal key, a subscript store `env[KEY] = …`, an `update`/`setdefault` keyword, or a
     `dict(KEY=…)` keyword. A string with the same value in value position is not a guard.
  2. DOMINANCE. The guarded environment must reach a `git` launch: the call's argv literal (or a
     name bound to one) contains `git`, and the environment reaches it by exactly one of
       (a) an inline `env=<guarded mapping>` at that call;
       (b) an env-named name bound to a guarded mapping (or to a local *producer* function that
           returns one) used as `env=` or as an argument at that call, with no intervening
           rebinding of that name to a mapping without the key;
       (c) the guarded name passed as an argument to a locally defined function whose env-named
           parameter is passed as `env=` at that call.
     Constructions inside a literal-false branch (`if False:` / `while False:`) do not count.

Frozen controls: 11 cases at `.ufo/waves/round-69/controls/c2-controls-r69.json`, sha256
`975ca3ba37341b5a058dec4fa76278d548996738e8b517616181824a841f90b9`. The base leg extracts the
round-68 counter `quality/counters/c2-r68-reader-guard.py` at --base-rev and scores the same
cases with its `classify`; the do-nothing control scores 7/11, so the target is not reachable
by keeping the held rule (`.ufo/waves/round-69/control-baseline-r69.txt`).

Printed receipt (last line, exact):

    MADO_R69_GUARD_DOMINANCE: population=<n> readers=<n> guarded=<n> unguarded=<n> controls=<n>/11 base_controls=<n>/11 verdict=<TARGET_MET|TARGET_MISSED> rev=<sha>

Exit 0 iff population == 20, readers == 13, guarded == 13, unguarded == 0, controls == 11 and
base_controls == 7; 1 otherwise; 2 on setup/usage error. Every write stays under the
caller-declared scratch root. Declared limits: one module, one hop, no alias/attribute/container
flow, no path-sensitivity beyond a literal-false branch, no cross-module producer; a guarded
environment does not authenticate objects and does not protect an already-rewritten repository.
"""
import argparse
import ast
import hashlib
import json
import os
import re
import runpy
import shutil
import subprocess
import sys

TOOL = "c2-r69-guard-dominance.py"
BASE_COUNTER = "quality/counters/c2-r68-reader-guard.py"
KEY = "GIT_NO_REPLACE_OBJECTS"
POPULATION_RE = re.compile(r"^quality/check-[^/]+\.py$")
GIT_TOKEN_RE = re.compile(r"[\"']git[\"']")
VERB_RE = re.compile(
    r"[\"'](?:show|cat-file|rev-parse|ls-tree|log|diff|ls-files|merge-base|"
    r"rev-list|describe|blame|grep|for-each-ref|symbolic-ref|hash-object)\b[\"']")
FROZEN_POPULATION = 20
FROZEN_READERS = 13
FROZEN_GUARDED = 13
FROZEN_CONTROLS = 11
FROZEN_BASE_CONTROLS = 7
FROZEN_CONTROLS_SHA = "975ca3ba37341b5a058dec4fa76278d548996738e8b517616181824a841f90b9"
UNSAFE_ROOTS = ("/tmp", "/var/tmp", "/dev/shm")
CONTRACT_RE = re.compile(
    r"MADO_R69_GUARD_DOMINANCE: population=[0-9]+ readers=[0-9]+ guarded=[0-9]+ "
    r"unguarded=[0-9]+ controls=[0-9]+/11 base_controls=[0-9]+/11 "
    r"verdict=(?:TARGET_MET|TARGET_MISSED) rev=[0-9a-f]{40,64}")


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


# --------------------------------------------------------------------------------------------- classification
ARGV_NAMES = set()


def env_named(name):
    return "env" in name.lower()


def is_git_argv(node):
    if not isinstance(node, (ast.List, ast.Tuple)):
        return False
    texts = [e.value for e in node.elts
             if isinstance(e, ast.Constant) and isinstance(e.value, str)]
    return any(t == "git" for t in texts)


def mapping_has_key(node):
    """True only when KEY is an actual key of this mapping expression.

    A dict literal's own keys count, and a `**` expansion of another mapping literal is
    followed one level; a `dict(KEY=...)` call counts by its keyword. Descendant dicts that
    sit inside a *value* are not keys of this mapping (review R69RevC2 finding 3).
    """
    if isinstance(node, ast.Dict):
        for key, value in zip(node.keys, node.values):
            if key is None:
                if mapping_has_key(value):
                    return True
            elif isinstance(key, ast.Constant) and key.value == KEY \
                    and not isinstance(key.value, bool):
                return True
        return False
    if isinstance(node, ast.Call):
        if isinstance(node.func, ast.Name) and node.func.id == "dict":
            return any(kw.arg == KEY for kw in node.keywords)
    return False


def argv_binding_names(tree):
    out = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name):
                    for sub in ast.walk(node.value):
                        if is_git_argv(sub):
                            out.add(target.id)
                            break
    return out


def call_is_git(call):
    for arg in list(call.args) + [k.value for k in call.keywords]:
        if is_git_argv(arg):
            return True
        if isinstance(arg, ast.Name) and arg.id in ARGV_NAMES:
            return True
        for sub in ast.walk(arg):
            if is_git_argv(sub):
                return True
    return False


def is_falsey_constant(test):
    return isinstance(test, ast.Constant) and not test.value


def false_guarded_lines(node):
    """Lines of the *body* of a literal-false branch; a live `else` arm stays live."""
    bad = set()

    def walk(current):
        for child in ast.iter_child_nodes(current):
            if isinstance(child, ast.If) and is_falsey_constant(child.test):
                for stmt in child.body:
                    for sub in ast.walk(stmt):
                        if hasattr(sub, "lineno"):
                            bad.add(sub.lineno)
            elif isinstance(child, ast.While) and is_falsey_constant(child.test):
                for stmt in list(child.body) + list(child.orelse):
                    for sub in ast.walk(stmt):
                        if hasattr(sub, "lineno"):
                            bad.add(sub.lineno)
            walk(child)

    walk(node)
    return bad


def scoped_nodes(scope):
    """Nodes belonging to this lexical scope only (never a nested def/lambda/class body)."""
    out = []
    stack = list(getattr(scope, "body", []))
    while stack:
        node = stack.pop()
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.Lambda, ast.ClassDef)):
            continue
        out.append(node)
        for child in ast.iter_child_nodes(node):
            if isinstance(child, (ast.FunctionDef, ast.AsyncFunctionDef, ast.Lambda,
                                  ast.ClassDef)):
                continue
            stack.append(child)
    return out


def assigned_names(nodes):
    """Every name this scope binds (any value), so a module binding can be shadowed."""
    out = set()
    for node in nodes:
        if isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name):
                    out.add(target.id)
                elif isinstance(target, ast.Subscript) and isinstance(target.value, ast.Name):
                    out.add(target.value.id)
        elif isinstance(node, ast.AnnAssign) and isinstance(node.target, ast.Name):
            out.add(node.target.id)
        elif isinstance(node, (ast.For, ast.AsyncFor)) and isinstance(node.target, ast.Name):
            out.add(node.target.id)
        elif isinstance(node, ast.withitem) and isinstance(node.optional_vars, ast.Name):
            out.add(node.optional_vars.id)
    return out


def function_scopes(tree):
    yield tree
    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            yield node


def local_functions(tree):
    out = {}
    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            out.setdefault(node.name, node)
    return out


def _params(fn):
    a = fn.args
    return list(a.posonlyargs) + list(a.args) + list(a.kwonlyargs)


def callee_passes_param_to_git(fn, pname):
    """Inside fn, is parameter `pname` the value handed to env= at a git call?"""
    for node in scoped_nodes(fn):
        if isinstance(node, ast.Call) and call_is_git(node):
            for kw in node.keywords:
                if kw.arg == "env" and isinstance(kw.value, ast.Name) \
                        and kw.value.id == pname:
                    return True
    return False


def _matched_env_params(fn, call, name):
    """Parameters of fn that the argument carrying `name` binds to (position or keyword)."""
    bound = []
    params = _params(fn)
    for index, arg in enumerate(call.args):
        if isinstance(arg, ast.Name) and arg.id == name and index < len(params):
            bound.append(params[index].arg)
    for kw in call.keywords:
        if kw.arg and isinstance(kw.value, ast.Name) and kw.value.id == name:
            bound.append(kw.arg)
    return [p for p in bound if env_named(p)]


def guard_construction_lines(nodes, dead_lines):
    """name -> set of guard-construction lines in this scope (key position, live lines)."""
    out = {}
    for node in nodes:
        if isinstance(node, ast.Assign) and len(node.targets) == 1 \
                and node.lineno not in dead_lines:
            target = node.targets[0]
            if isinstance(target, ast.Name) and env_named(target.id) \
                    and mapping_has_key(node.value):
                out.setdefault(target.id, set()).add(node.lineno)
            if isinstance(target, ast.Subscript) and isinstance(target.ctx, ast.Store):
                base, key = target.value, target.slice
                if isinstance(base, ast.Name) and env_named(base.id) \
                        and isinstance(key, ast.Constant) and key.value == KEY:
                    out.setdefault(base.id, set()).add(node.lineno)
        elif isinstance(node, ast.AnnAssign) and node.lineno not in dead_lines:
            target = node.target
            if isinstance(target, ast.Name) and env_named(target.id) \
                    and node.value is not None and mapping_has_key(node.value):
                out.setdefault(target.id, set()).add(node.lineno)
        elif isinstance(node, ast.Call) and node.lineno not in dead_lines:
            if isinstance(node.func, ast.Attribute) \
                    and node.func.attr in ("update", "setdefault") \
                    and isinstance(node.func.value, ast.Name) \
                    and env_named(node.func.value.id) \
                    and any(kw.arg == KEY for kw in node.keywords):
                out.setdefault(node.func.value.id, set()).add(node.lineno)
    return out


def producer_calls(nodes, producers):
    """name -> guard lines produced by assigning a call to a local guard producer."""
    out = {}
    for node in nodes:
        if not isinstance(node, ast.Assign) or len(node.targets) != 1:
            continue
        target = node.targets[0]
        if isinstance(target, ast.Name) and env_named(target.id) \
                and isinstance(node.value, ast.Call) \
                and isinstance(node.value.func, ast.Name) \
                and node.value.func.id in producers:
            out.setdefault(target.id, set()).add(node.lineno)
    return out


def unguarded_rebindings(nodes):
    out = {}
    for node in nodes:
        if isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name) and env_named(target.id) \
                        and not mapping_has_key(node.value):
                    out.setdefault(target.id, set()).add(node.lineno)
        elif isinstance(node, ast.AnnAssign) and isinstance(node.target, ast.Name) \
                and env_named(node.target.id) and node.value is not None \
                and not mapping_has_key(node.value):
            out.setdefault(node.target.id, set()).add(node.lineno)
    return out


def usage_lines(nodes, name, locals_):
    """Lines where `name` (same scope only) is handed to a git launch or a matching helper."""
    lines = set()
    for node in nodes:
        if not isinstance(node, ast.Call):
            continue
        if call_is_git(node):
            handed = any(kw.arg == "env" and isinstance(kw.value, ast.Name)
                         and kw.value.id == name for kw in node.keywords)
            handed = handed or any(isinstance(arg, ast.Name) and arg.id == name
                                   for arg in node.args)
            if handed:
                lines.add(node.lineno)
            continue
        fn = None
        if isinstance(node.func, ast.Name):
            fn = locals_.get(node.func.id)
        elif isinstance(node.func, ast.Attribute):
            fn = locals_.get(node.func.attr)
        if fn is None:
            continue
        for pname in _matched_env_params(fn, node, name):
            if callee_passes_param_to_git(fn, pname):
                lines.add(node.lineno)
                break
    return lines


def guard_producers(tree):
    """Local functions that RETURN a guard-carrying env (guard before the return, no rebinding)."""
    out = set()
    dead = false_guarded_lines(tree)
    for fn in ast.walk(tree):
        if not isinstance(fn, (ast.FunctionDef, ast.AsyncFunctionDef)):
            continue
        nodes = scoped_nodes(fn)
        dead_here = dead | false_guarded_lines(fn)
        guarded = guard_construction_lines(nodes, dead_here)
        rebinds = unguarded_rebindings(nodes)
        for node in nodes:
            if not isinstance(node, ast.Return) or node.value is None:
                continue
            if isinstance(node.value, ast.Name) and node.value.id in guarded:
                name = node.value.id
                for guard_line in guarded[name]:
                    if guard_line < node.lineno and not any(
                            guard_line < r < node.lineno for r in rebinds.get(name, ())):
                        out.add(fn.name)
                        break
            elif mapping_has_key(node.value):
                out.add(fn.name)
    return out


def inline_guarded_call(tree, producers, dead):
    for node in ast.walk(tree):
        if not isinstance(node, ast.Call) or node.lineno in dead:
            continue
        for kw in node.keywords:
            if kw.arg != "env" or not call_is_git(node):
                continue
            if mapping_has_key(kw.value):
                return True
            if isinstance(kw.value, ast.Call) and isinstance(kw.value.func, ast.Name) \
                    and kw.value.func.id in producers:
                return True
    return False


def has_guard(src):
    try:
        tree = ast.parse(src)
    except SyntaxError:
        return False
    if not GIT_TOKEN_RE.search(src):
        return False
    global ARGV_NAMES
    ARGV_NAMES = argv_binding_names(tree)
    dead = false_guarded_lines(tree)
    locals_ = local_functions(tree)
    producers = guard_producers(tree)
    if inline_guarded_call(tree, producers, dead):
        return True
    module_nodes = scoped_nodes(tree)
    module_binds = guard_construction_lines(module_nodes, dead)
    for name, lines in producer_calls(module_nodes, producers).items():
        module_binds.setdefault(name, set()).update(lines)
    for scope in function_scopes(tree):
        nodes = scoped_nodes(scope)
        binds = guard_construction_lines(nodes, dead)
        produced = producer_calls(nodes, producers)
        for name, lines in produced.items():
            binds.setdefault(name, set()).update(lines)
        if scope is not tree:
            local_names = assigned_names(nodes) | set(binds)
            for name, lines in module_binds.items():
                if name not in local_names:
                    binds = dict(binds)
                    binds[name] = set(lines)
        if not binds:
            continue
        rebinds = unguarded_rebindings(nodes)
        for name, guard_lines in binds.items():
            uses = usage_lines(nodes, name, locals_)
            for guard_line in guard_lines:
                after = [use for use in uses if use > guard_line]
                if not after:
                    continue
                first_use = min(after)
                if any(guard_line < r < first_use for r in rebinds.get(name, ())):
                    continue
                return True
    return False


def is_reader(src):
    return bool(GIT_TOKEN_RE.search(src)) and bool(VERB_RE.search(src))


def classify(src):
    reader = is_reader(src)
    return reader, (has_guard(src) if reader else False)


# --------------------------------------------------------------------------------------------- measurement
def verdict_met(population, readers, guarded, unguarded, controls, base_controls):
    return (population == FROZEN_POPULATION and readers == FROZEN_READERS
            and guarded == FROZEN_GUARDED and unguarded == 0
            and controls == FROZEN_CONTROLS and base_controls == FROZEN_BASE_CONTROLS)


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
    if len(cases) != FROZEN_CONTROLS:
        raise SetupError("controls file carries %d cases, frozen %d" % (len(cases), FROZEN_CONTROLS))
    return cases


def git(repo, args):
    return run(["git", "-C", repo] + list(args), cwd=repo)


def rev_parse(repo, rev):
    r = git(repo, ["rev-parse", "--verify", rev + "^{commit}"])
    if r.returncode != 0:
        raise SetupError("cannot resolve %s: %s" % (rev, dec(r.stderr).strip()[:200]))
    return dec(r.stdout).strip()


def population_at(repo, sha):
    r = git(repo, ["ls-tree", "-r", "--name-only", sha, "--", "quality"])
    if r.returncode != 0:
        raise SetupError("ls-tree failed at %s" % sha)
    return sorted(p for p in dec(r.stdout).splitlines() if POPULATION_RE.match(p))


def extract(repo, sha, path):
    r = git(repo, ["show", "%s:%s" % (sha, path)])
    if r.returncode != 0:
        return None
    return r.stdout


def base_classify(repo, base_sha, scratch):
    data = extract(repo, base_sha, BASE_COUNTER)
    if data is None:
        emit("MADO_R69_BASE_COUNTER path=%s present=no" % BASE_COUNTER)
        return None
    path = os.path.join(scratch, "base-counter.py")
    os.makedirs(scratch, exist_ok=True)
    with open(path, "wb") as fh:
        fh.write(data)
    module = runpy.run_path(path)
    emit("MADO_R69_BASE_COUNTER path=%s present=yes sha256=%s" % (BASE_COUNTER, sha256_hex(data)))
    return module["classify"]


def score_cases(classify_fn, cases):
    correct = 0
    for case in cases:
        reader, guard = classify_fn(case["src"])
        ok = (reader == case["expect_reader"]) and (guard == case["expect_guard"])
        correct += int(ok)
        emit("MADO_R69_CONTROL name=%s reader=%s guard=%s expect_reader=%s expect_guard=%s "
             "correct=%s"
             % (case["name"], "yes" if reader else "no", "yes" if guard else "no",
                "yes" if case["expect_reader"] else "no",
                "yes" if case["expect_guard"] else "no", "yes" if ok else "no"))
    return correct


def contract_line(population, readers, guarded, unguarded, controls, base_controls, sha):
    return ("MADO_R69_GUARD_DOMINANCE: population=%d readers=%d guarded=%d unguarded=%d "
            "controls=%d/%d base_controls=%d/%d verdict=%s rev=%s"
            % (population, readers, guarded, unguarded, controls, FROZEN_CONTROLS,
               base_controls, FROZEN_CONTROLS,
               "TARGET_MET" if verdict_met(population, readers, guarded, unguarded,
                                           controls, base_controls) else "TARGET_MISSED",
               sha))


def measure(args):
    repo = os.path.abspath(args.repo)
    if not os.path.isdir(repo):
        raise SetupError("--repo is not a directory: %s" % args.repo)
    scratch = absolute_scratch(args.scratch_root)
    work = os.path.join(scratch, "r69-c2-dominance")
    if os.path.isdir(work):
        shutil.rmtree(work)
    os.makedirs(work)

    cases = load_controls(os.path.abspath(args.controls))
    emit("MADO_R69_CONTROLS path=%s cases=%d sha256=%s"
         % (os.path.abspath(args.controls), len(cases), FROZEN_CONTROLS_SHA))

    sha = rev_parse(repo, args.rev)
    base_sha = rev_parse(repo, args.base_rev or args.rev)

    population = population_at(repo, sha)
    if not population:
        raise SetupError("population is empty at %s" % sha)
    readers = guarded = 0
    for path in population:
        data = extract(repo, sha, path)
        if data is None:
            raise SetupError("population file vanished at %s: %s" % (sha, path))
        reader, guard = classify(dec(data))
        if reader:
            readers += 1
            guarded += int(guard)
        emit("MADO_R69_READER file=%s reader=%s guard=%s"
             % (path, "yes" if reader else "no", "yes" if guard else "no"))
    unguarded = readers - guarded

    controls = score_cases(classify, cases)
    classify_base = base_classify(repo, base_sha, os.path.join(work, "base"))
    if classify_base is None:
        base_controls = 0
    else:
        base_controls = score_cases(classify_base, cases)
        emit("MADO_R69_BASE controls=%d/%d (the round-68 rule must miss the target)"
             % (base_controls, FROZEN_CONTROLS))

    line = contract_line(len(population), readers, guarded, unguarded, controls,
                         base_controls, sha)
    if not CONTRACT_RE.fullmatch(line):
        raise SetupError("emitted contract line does not match CONTRACT_RE")
    emit(line)
    return 0 if verdict_met(len(population), readers, guarded, unguarded, controls,
                            base_controls) else 1


# --------------------------------------------------------------------------------------------- selftest
CASES = {
    "guarded-inline": ('def run(repo):\n    subprocess.run(["git", "-C", repo, "show", "HEAD:a"],\n'
                       '                   env=dict(os.environ, GIT_NO_REPLACE_OBJECTS="1"))\n',
                       True, True),
    "value-position-only": ('def run(repo):\n'
                            '    env = {"PATH": "/usr/bin", "LABEL": "GIT_NO_REPLACE_OBJECTS"}\n'
                            '    subprocess.run(["git", "-C", repo, "show", "HEAD:a"], env=env)\n',
                            True, False),
    "dead-branch-only": ('def run(repo):\n    env = {"PATH": "/usr/bin"}\n    if False:\n'
                         '        env["GIT_NO_REPLACE_OBJECTS"] = "1"\n'
                         '    subprocess.run(["git", "-C", repo, "show", "HEAD:a"], env=env)\n',
                         True, False),
    "uncalled-helper": ('def guarded_env():\n    env = {"PATH": "/usr/bin"}\n'
                        '    env["GIT_NO_REPLACE_OBJECTS"] = "1"\n    return env\n\n\n'
                        'def run(repo):\n    plain = {"PATH": "/usr/bin"}\n'
                        '    subprocess.run(["git", "-C", repo, "show", "HEAD:a"], env=plain)\n',
                        True, False),
    "overwritten-env": ('def run(repo):\n'
                        '    env = {"PATH": "/usr/bin", "GIT_NO_REPLACE_OBJECTS": "1"}\n'
                        '    env = {"PATH": "/usr/bin"}\n'
                        '    subprocess.run(["git", "-C", repo, "show", "HEAD:a"], env=env)\n',
                        True, False),
    "update-guard": ('def run(repo):\n    env = {}\n    env.update(GIT_NO_REPLACE_OBJECTS="1")\n'
                     '    subprocess.run(["git", "-C", repo, "ls-tree", "-r", "HEAD"], env=env)\n',
                     True, True),
    "subscript-guard": ('def git(repo, *args):\n    env = {"PATH": "/usr/bin"}\n'
                        '    env["GIT_NO_REPLACE_OBJECTS"] = "1"\n'
                        '    return subprocess.run(["git", "-C", repo] + list(args), env=env)\n\n\n'
                        'def head(repo):\n    return git(repo, "show", "HEAD:a")\n',
                        True, True),
    "module-constant": ('GIT_ENV = {"PATH": "/usr/bin"}\n'
                        'GIT_ENV["GIT_NO_REPLACE_OBJECTS"] = "1"\n\n\n'
                        'def head(repo):\n'
                        '    return subprocess.run(["git", "-C", repo, "show", "HEAD:a"], '
                        'env=GIT_ENV)\n', True, True),
    "producer-helper": ('def git_env(work):\n    env = {"PATH": "/usr/bin"}\n'
                        '    env["GIT_NO_REPLACE_OBJECTS"] = "1"\n    return env\n\n\n'
                        'def run(repo, work):\n    env = git_env(work)\n'
                        '    return subprocess.run(["git", "-C", repo, "show", "HEAD:a"], '
                        'env=env)\n', True, True),
    "argv-name-flow": ('def run(repo):\n    cmd = ["git", "-C", repo, "show", "HEAD:a"]\n'
                       '    subprocess.run(cmd, capture_output=True, env=git_env())\n\n\n'
                       'def git_env():\n    env = {"PATH": "/usr/bin"}\n'
                       '    env["GIT_NO_REPLACE_OBJECTS"] = "1"\n    return env\n',
                       True, True),
    "mention-only": ('"""Reads objects with git show; GIT_NO_REPLACE_OBJECTS is not set."""\n'
                     '\n\n'
                     'def run(repo):\n'
                     '    # the guard GIT_NO_REPLACE_OBJECTS is deliberately absent\n'
                     '    subprocess.run(["git", "-C", repo, "show", "HEAD:a"], '
                     'env=dict(os.environ))\n', True, False),
}


REGRESSIONS = {
    "dead-inline": ('def run(repo):\n    if False:\n'
                    '        subprocess.run(["git", "-C", repo, "show", "HEAD:a"], '
                    'env={"GIT_NO_REPLACE_OBJECTS": "1"})\n'
                    '    subprocess.run(["git", "-C", repo, "show", "HEAD:a"], '
                    'env={"PATH": "/usr/bin"})\n', True, False),
    "producer-overwrite": ('def git_env():\n    env = {"GIT_NO_REPLACE_OBJECTS": "1"}\n'
                           '    env = {}\n    return env\n\n\n'
                           'def run(repo):\n    env = git_env()\n'
                           '    subprocess.run(["git", "-C", repo, "show", "HEAD:a"], env=env)\n',
                           True, False),
    "producer-late": ('def git_env():\n    env = {}\n    return env\n'
                      '    env = {"GIT_NO_REPLACE_OBJECTS": "1"}\n\n\n'
                      'def run(repo):\n    env = git_env()\n'
                      '    subprocess.run(["git", "-C", repo, "show", "HEAD:a"], env=env)\n',
                      True, False),
    "nested-key-value": ('def run(repo):\n'
                         '    env = {"LABEL": {"GIT_NO_REPLACE_OBJECTS": "1"}}\n'
                         '    subprocess.run(["git", "-C", repo, "show", "HEAD:a"], env=env)\n',
                         True, False),
    "sibling-scope": ('def never():\n    env = {"GIT_NO_REPLACE_OBJECTS": "1"}\n'
                      '    return env\n\n\ndef run(repo):\n'
                      '    subprocess.run(["git", "-C", repo, "show", "HEAD:a"], env=env)\n',
                      True, False),
    "onehop-wrong-parameter": ('def git(repo, other_env, env):\n'
                               '    subprocess.run(["git", "-C", repo, "show", "HEAD:a"], '
                               'env=other_env)\n\n\ndef run(repo):\n'
                               '    env = {"GIT_NO_REPLACE_OBJECTS": "1"}\n'
                               '    other_env = {"PATH": "/usr/bin"}\n'
                               '    return git(repo, other_env, env)\n', True, False),
    "dead-else-valid": ('def run(repo):\n    if False:\n        env = {"PATH": "/usr/bin"}\n'
                        '    else:\n        env = {"GIT_NO_REPLACE_OBJECTS": "1"}\n'
                        '    subprocess.run(["git", "-C", repo, "show", "HEAD:a"], env=env)\n',
                        True, True),
    "module-visible-binding": ('GIT_ENV = {"PATH": "/usr/bin"}\n'
                               'GIT_ENV["GIT_NO_REPLACE_OBJECTS"] = "1"\n\n\n'
                               'def head(repo):\n'
                               '    return subprocess.run(["git", "-C", repo, "show", "HEAD:a"], '
                               'env=GIT_ENV)\n', True, True),
}


def _selftest_checks(scratch, controls_path):
    checks = []

    def want(name, cond):
        checks.append((name, bool(cond)))

    want("the population regex accepts only top-level quality/check-*.py",
         bool(POPULATION_RE.match("quality/check-index.py"))
         and not POPULATION_RE.match("quality/counters/c2-r69-guard-dominance.py")
         and not POPULATION_RE.match("quality/check-x/helper.py")
         and not POPULATION_RE.match("quality/notes.md"))
    want("the embedded classification table covers eleven cases", len(CASES) == 11)
    for name, (src, reader, guard) in CASES.items():
        want("classify %s is (%s, %s)" % (name, reader, guard),
             classify(src) == (reader, guard))
    rejected = ("value-position-only", "dead-branch-only", "uncalled-helper", "overwritten-env")
    want("the four rejected shapes are reader without guard",
         all(classify(CASES[n][0]) == (True, False) for n in rejected))
    want("a broken source is not a guard", classify("def f(:\n") == (False, False))
    want("git init/add only is not a reader",
         classify('def f(repo):\n    subprocess.run(["git", "-C", repo, "init", "-q"])\n')
         == (False, False))
    want("guard inside a non-env keyword is not a guard",
         classify('def f(repo):\n    g(["git", "-C", repo, "show", "HEAD:a"], '
                  'labels={"GIT_NO_REPLACE_OBJECTS": "1"})\n')[1] is False)

    for name, (src, reader, guard) in REGRESSIONS.items():
        want("review regression %s is (%s, %s)" % (name, reader, guard),
             classify(src) == (reader, guard))
    want("verdict met on the frozen target", verdict_met(20, 13, 13, 0, 11, 7))
    want("verdict requires the frozen population", not verdict_met(19, 13, 13, 0, 11, 7))
    want("verdict requires the frozen reader count", not verdict_met(20, 12, 12, 0, 11, 7))
    want("verdict requires the frozen guarded count", not verdict_met(20, 13, 12, 1, 11, 7))
    want("verdict requires no unguarded reader", not verdict_met(20, 13, 13, 1, 11, 7))
    want("verdict requires every control correct", not verdict_met(20, 13, 13, 0, 10, 7))
    want("verdict requires the frozen base-control score",
         not verdict_met(20, 13, 13, 0, 11, 11))

    good = contract_line(20, 13, 13, 0, 11, 7, "a" * 40)
    want("the frozen target prints the met line",
         good == ("MADO_R69_GUARD_DOMINANCE: population=20 readers=13 guarded=13 unguarded=0 "
                  "controls=11/11 base_controls=7/11 verdict=TARGET_MET rev=" + "a" * 40))
    want("the target line matches the frozen contract shape",
         CONTRACT_RE.fullmatch(good) is not None)
    want("contract line refuses a wrong verdict word",
         not CONTRACT_RE.fullmatch(
             "MADO_R69_GUARD_DOMINANCE: population=20 readers=13 guarded=13 unguarded=0 "
             "controls=11/11 base_controls=7/11 verdict=DONE rev=" + "a" * 40))

    frozen = ["--repo", ".", "--rev", "HEAD", "--base-rev", "BASE",
              "--controls", "cases.json", "--scratch-root", "/scratch/dir"]
    try:
        parsed = build_parser().parse_args(frozen)
        parsed_ok = (parsed.scratch_root == "/scratch/dir"
                     and parsed.controls == "cases.json" and parsed.base_rev == "BASE")
    except SystemExit:
        parsed_ok = False
    want("the frozen counting command's argument set parses", parsed_ok)

    if controls_path:
        try:
            cases = load_controls(os.path.abspath(controls_path))
            want("the frozen controls file carries 11 cases", len(cases) == 11)
            want("the frozen controls file matches the pinned digest", True)
        except SetupError:
            want("the frozen controls file carries 11 cases", False)
            want("the frozen controls file matches the pinned digest", False)
    os.makedirs(scratch, exist_ok=True)
    tampered = os.path.join(scratch, "controls-tampered.json")
    with open(tampered, "w", encoding="utf-8") as fh:
        fh.write(json.dumps({"cases": []}))
    want("a controls file with the wrong digest is refused",
         _raises(SetupError, lambda: load_controls(tampered)))
    return checks


def _raises(exc_type, fn):
    try:
        fn()
    except exc_type:
        return True
    except Exception:
        return False
    return False


def selftest(scratch, controls_path):
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
            checks.extend(_selftest_checks(scratch, controls_path))
        except AssertionError:
            checks.append(("selftest body must not spawn a process", False))
    finally:
        subprocess.run = saved_run
    passed = sum(1 for _name, ok in checks if ok)
    for name, ok in checks:
        if not ok:
            print("MADO_R69_GUARD_DOMINANCE_SELFTEST FAIL: %s" % name)
    print("MADO_R69_GUARD_DOMINANCE_SELFTEST: %d/%d assertions passed" % (passed, len(checks)))
    return 0 if passed == len(checks) else 1


# --------------------------------------------------------------------------------------------- cli
def build_parser():
    parser = argparse.ArgumentParser(prog=TOOL, description=__doc__.splitlines()[0])
    parser.add_argument("--repo")
    parser.add_argument("--rev")
    parser.add_argument("--base-rev", default=None)
    parser.add_argument("--controls")
    parser.add_argument("--scratch-root")
    parser.add_argument("--selftest", action="store_true")
    return parser


def main(argv):
    args = build_parser().parse_args(argv)
    try:
        scratch = absolute_scratch(args.scratch_root)
        if args.selftest:
            return selftest(scratch, args.controls)
        if not args.repo or not args.rev or not args.controls:
            raise UsageError("--repo, --rev and --controls are required")
        return measure(args)
    except UsageError as exc:
        sys.stderr.write("%s: %s\n" % (TOOL, exc))
        return 2
    except SetupError as exc:
        sys.stderr.write("%s: %s\n" % (TOOL, exc))
        return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
