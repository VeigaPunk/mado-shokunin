#!/usr/bin/env python3
"""Prototype: key-position + dominance guard classifier (round-69 C2 design check)."""
import ast
import re
import subprocess
import sys

KEY = "GIT_NO_REPLACE_OBJECTS"
GIT_TOKEN_RE = re.compile(r"[\"']git[\"']")
VERB_NAMES = {"show", "cat-file", "rev-parse", "ls-tree", "log", "diff", "ls-files",
              "merge-base", "rev-list", "describe", "blame", "grep", "for-each-ref",
              "symbolic-ref", "hash-object"}
VERB_RE = re.compile(
    r"[\"'](?:show|cat-file|rev-parse|ls-tree|log|diff|ls-files|merge-base|"
    r"rev-list|describe|blame|grep|for-each-ref|symbolic-ref|hash-object)\b[\"']")


def env_named(name):
    return "env" in name.lower()


def is_git_argv(node):
    """A literal argv sequence naming git and an object-read verb."""
    if not isinstance(node, (ast.List, ast.Tuple)):
        return False
    texts = [e.value for e in node.elts
             if isinstance(e, ast.Constant) and isinstance(e.value, str)]
    return any(t == "git" for t in texts)


ARGV_NAMES = set()


def argv_binding_names(tree):
    """Names bound to an expression that contains a literal argv naming git."""
    out = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Assign):
            for t in node.targets:
                if isinstance(t, ast.Name):
                    for sub in ast.walk(node.value):
                        if is_git_argv(sub):
                            out.add(t.id)
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


def carries_key_keyposition(node):
    """True iff the mapping expression puts KEY in key position."""
    if node is None:
        return False
    for n in ast.walk(node):
        if isinstance(n, ast.Dict):
            for k in n.keys:
                if isinstance(k, ast.Constant) and k.value == KEY and not isinstance(k.value, bool):
                    return True
        if isinstance(n, ast.Call):
            for kw in n.keywords:
                if kw.arg == KEY:
                    return True
    return False


def is_falsey_constant(test):
    return isinstance(test, ast.Constant) and not test.value


def false_guarded_lines(tree):
    """Line numbers inside a literal-false branch."""
    bad = set()

    def walk(node):
        for child in ast.iter_child_nodes(node):
            if isinstance(child, (ast.If, ast.While)) and is_falsey_constant(child.test):
                for sub in ast.walk(child):
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


def body_of(scope):
    return scope.body if hasattr(scope, "body") else []


def local_functions(tree):
    out = {}
    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            out.setdefault(node.name, node)
    return out


def param_env_names(fn):
    names = set()
    a = fn.args
    for arg in list(a.posonlyargs) + list(a.args) + list(a.kwonlyargs):
        if env_named(arg.arg):
            names.add(arg.arg)
    return names


def callee_passes_env_to_git(fn):
    """Inside fn, is an env-named parameter handed to a git call?"""
    params = param_env_names(fn)
    if not params:
        return False
    for node in ast.walk(fn):
        if isinstance(node, ast.Call) and call_is_git(node):
            for kw in node.keywords:
                if kw.arg == "env" and isinstance(kw.value, ast.Name) and kw.value.id in params:
                    return True
    return False


def usage_lines(scope, name, tree, locals_):
    """Lines where `name` is handed to a git call (directly or one hop)."""
    lines = set()
    for node in ast.walk(scope):
        if not isinstance(node, ast.Call):
            continue
        handed = False
        for kw in node.keywords:
            if kw.arg == "env" and isinstance(kw.value, ast.Name) and kw.value.id == name:
                handed = True
        for arg in node.args:
            if isinstance(arg, ast.Name) and arg.id == name:
                handed = True
        if not handed:
            continue
        if call_is_git(node):
            lines.add(node.lineno)
            continue
        fn = None
        if isinstance(node.func, ast.Name):
            fn = locals_.get(node.func.id)
        elif isinstance(node.func, ast.Attribute):
            fn = locals_.get(node.func.attr)
        if fn is not None and callee_passes_env_to_git(fn):
            lines.add(node.lineno)
    return lines


def guard_producers(tree):
    """Local functions whose return value is a key-position-carrying env."""
    out = set()
    for fn in ast.walk(tree):
        if not isinstance(fn, (ast.FunctionDef, ast.AsyncFunctionDef)):
            continue
        dead = false_guarded_lines(fn)
        local = {}
        for node in ast.walk(fn):
            if isinstance(node, ast.Assign) and len(node.targets) == 1:
                t = node.targets[0]
                if isinstance(t, ast.Name) and env_named(t.id) \
                        and carries_key_keyposition(node.value) and node.lineno not in dead:
                    local.setdefault(t.id, True)
                if isinstance(t, ast.Subscript) and isinstance(t.ctx, ast.Store) \
                        and isinstance(t.value, ast.Name) and env_named(t.value.id) \
                        and isinstance(t.slice, ast.Constant) and t.slice.value == KEY \
                        and node.lineno not in dead:
                    local.setdefault(t.value.id, True)
            elif isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute) \
                    and node.func.attr in ("update", "setdefault") \
                    and isinstance(node.func.value, ast.Name) \
                    and env_named(node.func.value.id) \
                    and any(kw.arg == KEY for kw in node.keywords) \
                    and node.lineno not in dead:
                local.setdefault(node.func.value.id, True)
        for node in ast.walk(fn):
            if isinstance(node, ast.Return) and node.value is not None:
                if isinstance(node.value, ast.Name) and local.get(node.value.id):
                    out.add(fn.name)
                elif carries_key_keyposition(node.value):
                    out.add(fn.name)
    return out


def guarded_names(scope, dead_lines, producers=frozenset()):
    """name -> list of guard lines (key-position construction, not in a dead branch)."""
    out = {}
    for node in ast.walk(scope):
        if isinstance(node, ast.Assign) and len(node.targets) == 1:
            t = node.targets[0]
            if isinstance(t, ast.Name) and env_named(t.id) and carries_key_keyposition(node.value):
                if node.lineno not in dead_lines:
                    out.setdefault(t.id, set()).add(node.lineno)
            if isinstance(t, ast.Name) and env_named(t.id) \
                    and isinstance(node.value, ast.Call) \
                    and isinstance(node.value.func, ast.Name) \
                    and node.value.func.id in producers \
                    and node.lineno not in dead_lines:
                out.setdefault(t.id, set()).add(node.lineno)
            if isinstance(t, ast.Subscript) and isinstance(t.ctx, ast.Store):
                base = t.value
                key = t.slice
                if (isinstance(base, ast.Name) and env_named(base.id)
                        and isinstance(key, ast.Constant) and key.value == KEY
                        and node.lineno not in dead_lines):
                    out.setdefault(base.id, set()).add(node.lineno)
        elif isinstance(node, ast.AnnAssign):
            t = node.target
            if isinstance(t, ast.Name) and env_named(t.id) and node.value is not None \
                    and carries_key_keyposition(node.value) and node.lineno not in dead_lines:
                out.setdefault(t.id, set()).add(node.lineno)
        elif isinstance(node, ast.Call):
            if (isinstance(node.func, ast.Attribute)
                    and node.func.attr in ("update", "setdefault")
                    and isinstance(node.func.value, ast.Name) and env_named(node.func.value.id)
                    and any(kw.arg == KEY for kw in node.keywords)
                    and node.lineno not in dead_lines):
                out.setdefault(node.func.value.id, set()).add(node.lineno)
    return out


def unguarded_rebindings(scope):
    """name -> set of lines where the env-named name is rebound without the key."""
    out = {}
    for node in ast.walk(scope):
        if isinstance(node, ast.Assign):
            for t in node.targets:
                if isinstance(t, ast.Name) and env_named(t.id):
                    if not carries_key_keyposition(node.value):
                        out.setdefault(t.id, set()).add(node.lineno)
        elif isinstance(node, ast.AnnAssign) and isinstance(node.target, ast.Name) \
                and env_named(node.target.id) and node.value is not None:
            if not carries_key_keyposition(node.value):
                out.setdefault(node.target.id, set()).add(node.lineno)
    return out


def inline_guarded_call(tree, producers=frozenset()):
    for node in ast.walk(tree):
        if not isinstance(node, ast.Call):
            continue
        for kw in node.keywords:
            if kw.arg != "env":
                continue
            if not call_is_git(node):
                continue
            if carries_key_keyposition(kw.value):
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
    if inline_guarded_call(tree, producers):
        return True
    for scope in function_scopes(tree):
        binds = guarded_names(scope, dead, producers)
        if not binds:
            continue
        rebinds = unguarded_rebindings(scope)
        for name, guard_lines in binds.items():
            uses = usage_lines(scope, name, tree, locals_)
            for g in guard_lines:
                after = [u for u in uses if u > g]
                if not after:
                    continue
                first_use = min(after)
                if any(g < r < first_use for r in rebinds.get(name, ())):
                    continue
                return True
    return False


def is_reader(src):
    return bool(GIT_TOKEN_RE.search(src)) and bool(VERB_RE.search(src))


def classify(src):
    reader = is_reader(src)
    return reader, (has_guard(src) if reader else False)


def main():
    repo = sys.argv[1]
    rev = sys.argv[2] if len(sys.argv) > 2 else "HEAD"
    names = subprocess.check_output(
        ["git", "-C", repo, "ls-tree", "-r", "--name-only", rev, "--", "quality"],
        text=True).splitlines()
    pop = sorted(p for p in names if re.match(r"^quality/check-[^/]+\.py$", p))
    readers = guarded = 0
    for p in pop:
        src = subprocess.check_output(["git", "-C", repo, "show", "%s:%s" % (rev, p)],
                                      text=True)
        r, g = classify(src)
        if r:
            readers += 1
            guarded += int(g)
        print("FILE %s reader=%s guard=%s" % (p, "yes" if r else "no", "yes" if g else "no"))
    print("SUMMARY population=%d readers=%d guarded=%d unguarded=%d"
          % (len(pop), readers, guarded, readers - guarded))


if __name__ == "__main__":
    main()
