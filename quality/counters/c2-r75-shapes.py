#!/usr/bin/env python3
r"""Round-75 C2 counting command: the guard census counts the copy spellings bound to a name and
the `del env[KEY]` cancellation (claim C2, round 75).

    python3 quality/counters/c2-r75-shapes.py --repo . --rev REV \
        --base-rev bd5a971532f37df85a78f6f566dd1e649b79de11 \
        --controls .ufo/waves/round-75/controls/c2-cases-r75.json --scratch-root DIR
    python3 quality/counters/c2-r75-shapes.py --selftest --scratch-root DIR

The successor adds two rule deltas to the round-74 classifier (frozen, never edited):

  D1 - a mapping that carries the guard key in key position guards the child whatever the
       binding's NAME: ``child = dict(env, GIT_NO_REPLACE_OBJECTS="1")`` or
       ``child = {**env, "GIT_NO_REPLACE_OBJECTS": "1"}`` handed as ``env=child`` counts, under
       the same dominance test the env-named flow uses (the binding strictly before the launch,
       no plain rebinding of the name in between). A copy without the key, a key in value
       position, and a rebound copy stay unguarded.
  D2 - ``del env[KEY]`` between a guard construction and the launch cancels the store: the key
       is removed from the mapping handed to the child (a delete of another key, and a delete
       before the store, cancel nothing).

The first thirty-six cases are carried byte-identically from the round-74 frozen set
(hash-checked); the eleven appended cases are the round-75 carriers and their negatives. The
twenty-population census is re-derived at --rev and must keep twenty readers, thirteen guarded,
zero unguarded. The do-nothing control is the round-74 classifier extracted at --base-rev and
scored on the same forty-seven cases in the same run; it must score exactly 41/47.

Printed receipt (last line, exact):

    MADO_R75_GUARD_SHAPES: population=<n> readers=<n> guarded=<n> unguarded=<n> controls=<n>/47 base_controls=<m>/47 verdict=<TARGET_MET|TARGET_MISSED> rev=<sha>

Exit 0 iff population 20, readers 13, guarded 13, unguarded 0, controls 47 and base_controls 41;
1 iff the measurement ran and missed (an absent base classifier prints base_controls=0); 2 on
usage/setup error with the reason on stderr and no contract line.

Declared limits: line order is not execution order (the same cross-method approximation the
attribute flow declares); one object-alias edge and one `os.environ` alias with no chains; the
name-neutral binding counts a mapping handed as `env=`, not the truth of its values; `del` is
modelled for a literal key in the same scope only; a syntactic approximation that does not
interpret values.
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

TOOL = "c2-r75-shapes.py"
BASE_COUNTER = "quality/counters/c2-r74-shapes.py"
KEY = "GIT_NO_REPLACE_OBJECTS"
POPULATION_RE = re.compile(r"^quality/check-[^/]+\.py$")
GIT_TOKEN_RE = re.compile(r"[\"']git[\"']")
VERB_RE = re.compile(
    r"[\"'](?:show|cat-file|rev-parse|ls-tree|log|diff|ls-files|merge-base|"
    r"rev-list|describe|blame|grep|for-each-ref|symbolic-ref|hash-object)\b[\"']")
FROZEN_POPULATION = 20
FROZEN_READERS = 13
FROZEN_GUARDED = 13
FROZEN_CONTROLS = 47
FROZEN_BASE_CONTROLS = 41
FROZEN_CONTROLS_SHA = "d99502ba23e969a981a856a06742d8da14e1684850c7ca0e0900cd2dc7767897"
HELD_CONTROLS = ".ufo/waves/round-74/controls/c2-cases-r74.json"
HELD_CONTROLS_SHA = "4db4cc70d1a8e86876f20a9527cfc7f0c7a344eb6d2655b398443b907b3a73d0"
HELD_CASES = 36
UNSAFE_ROOTS = ("/tmp", "/var/tmp", "/dev/shm")
CONTRACT_RE = re.compile(
    r"MADO_R75_GUARD_SHAPES: population=[0-9]+ readers=[0-9]+ guarded=[0-9]+ "
    r"unguarded=[0-9]+ controls=[0-9]+/47 base_controls=[0-9]+/47 "
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


def _symlink_component(path):
    """The first symlinked component of an absolute path, else None (R74Sentinel D1)."""
    parts = []
    current = os.path.abspath(path)
    while True:
        parts.append(current)
        parent = os.path.dirname(current)
        if parent == current:
            break
        current = parent
    for part in reversed(parts):
        if os.path.islink(part):
            return part
    return None


def absolute_scratch(value):
    if not value:
        raise UsageError("--scratch-root is required")
    root = os.path.realpath(os.path.abspath(value))
    if not os.path.isdir(root):
        raise UsageError("--scratch-root is not a directory: %s" % value)
    if os.path.islink(os.path.abspath(value)):
        raise UsageError("--scratch-root must not be a symlink")
    link = _symlink_component(value)
    if link is not None:
        raise UsageError("--scratch-root has a symlinked component: %s" % link)
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


def mapping_has_key(node, maps=frozenset()):
    """True only when KEY is an actual key of this mapping expression.

    A dict literal's own keys count, and a `**` expansion of another mapping literal is
    followed one level; a `dict(KEY=...)` call counts by its keyword, and a
    `dict(<args>, **module_mapping)` call counts when the named module mapping carries the
    key (round 71). Descendant dicts that sit inside a *value* are not keys of this mapping
    (review R69RevC2 finding 3).
    """
    if isinstance(node, ast.Dict):
        for key, value in zip(node.keys, node.values):
            if key is None:
                if mapping_has_key(value, maps):
                    return True
            elif isinstance(key, ast.Constant) and key.value == KEY \
                    and not isinstance(key.value, bool):
                return True
        return False
    if isinstance(node, ast.Call):
        if isinstance(node.func, ast.Name) and node.func.id == "dict":
            if any(kw.arg == KEY for kw in node.keywords):
                return True
            return any(kw.arg is None and isinstance(kw.value, ast.Name)
                       and kw.value.id in maps for kw in node.keywords)
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


def guard_construction_lines(nodes, dead_lines, maps=frozenset()):
    """name -> set of guard-construction lines in this scope (key position, live lines)."""
    out = {}
    for node in nodes:
        if isinstance(node, ast.Assign) and len(node.targets) == 1 \
                and node.lineno not in dead_lines:
            target = node.targets[0]
            if isinstance(target, ast.Name) and env_named(target.id) \
                    and mapping_has_key(node.value, maps):
                out.setdefault(target.id, set()).add(node.lineno)
            if isinstance(target, ast.Subscript) and isinstance(target.ctx, ast.Store):
                base, key = target.value, target.slice
                if isinstance(base, ast.Name) and env_named(base.id) \
                        and isinstance(key, ast.Constant) and key.value == KEY:
                    out.setdefault(base.id, set()).add(node.lineno)
        elif isinstance(node, ast.AnnAssign) and node.lineno not in dead_lines:
            target = node.target
            if isinstance(target, ast.Name) and env_named(target.id) \
                    and node.value is not None and mapping_has_key(node.value, maps):
                out.setdefault(target.id, set()).add(node.lineno)
        elif isinstance(node, ast.Call) and node.lineno not in dead_lines:
            if isinstance(node.func, ast.Attribute) \
                    and node.func.attr in ("update", "setdefault") \
                    and isinstance(node.func.value, ast.Name) \
                    and env_named(node.func.value.id) \
                    and any(kw.arg == KEY for kw in node.keywords):
                out.setdefault(node.func.value.id, set()).add(node.lineno)
    # Round-75 D1: a mapping that carries the key in key position guards the child whatever the
    # binding's name; the dominance test below decides whether the binding reaches the launch.
    for node in nodes:
        if isinstance(node, ast.Assign) and len(node.targets) == 1 \
                and node.lineno not in dead_lines:
            target = node.targets[0]
            if isinstance(target, ast.Name) and mapping_has_key(node.value, maps):
                out.setdefault(target.id, set()).add(node.lineno)
        elif isinstance(node, ast.AnnAssign) and node.lineno not in dead_lines:
            target = node.target
            if isinstance(target, ast.Name) and node.value is not None \
                    and mapping_has_key(node.value, maps):
                out.setdefault(target.id, set()).add(node.lineno)
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


def unguarded_rebindings(nodes, maps=frozenset()):
    out = {}
    for node in nodes:
        if isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name) and env_named(target.id) \
                        and not mapping_has_key(node.value, maps):
                    out.setdefault(target.id, set()).add(node.lineno)
        elif isinstance(node, ast.AnnAssign) and isinstance(node.target, ast.Name) \
                and env_named(node.target.id) and node.value is not None \
                and not mapping_has_key(node.value, maps):
            out.setdefault(node.target.id, set()).add(node.lineno)
    # Round-75: the dominance test follows every simple name the census can bind (D1 makes the
    # guard binding name-neutral), so a plain rebinding cancels a guard whatever the name; and a
    # `del env[KEY]` removes the key the guard stored, so it cancels too (literal key, same scope).
    for node in nodes:
        if isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name) and not mapping_has_key(node.value, maps):
                    out.setdefault(target.id, set()).add(node.lineno)
        elif isinstance(node, ast.AnnAssign) and isinstance(node.target, ast.Name) \
                and node.value is not None and not mapping_has_key(node.value, maps):
            out.setdefault(node.target.id, set()).add(node.lineno)
        elif isinstance(node, ast.Delete):
            for target in node.targets:
                if isinstance(target, ast.Subscript) and isinstance(target.ctx, ast.Del) \
                        and isinstance(target.value, ast.Name) \
                        and isinstance(target.slice, ast.Constant) \
                        and target.slice.value == KEY:
                    out.setdefault(target.value.id, set()).add(node.lineno)
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


def guard_producers(tree, maps=frozenset()):
    """Local functions that RETURN a guard-carrying env (guard before the return, no rebinding)."""
    out = set()
    dead = false_guarded_lines(tree)
    for fn in ast.walk(tree):
        if not isinstance(fn, (ast.FunctionDef, ast.AsyncFunctionDef)):
            continue
        nodes = scoped_nodes(fn)
        dead_here = dead | false_guarded_lines(fn)
        guarded = guard_construction_lines(nodes, dead_here, maps)
        rebinds = unguarded_rebindings(nodes, maps)
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
            elif mapping_has_key(node.value, maps):
                out.add(fn.name)
    return out


def inline_guarded_call(tree, producers, dead, maps=frozenset()):
    for node in ast.walk(tree):
        if not isinstance(node, ast.Call) or node.lineno in dead:
            continue
        for kw in node.keywords:
            if kw.arg != "env" or not call_is_git(node):
                continue
            if mapping_has_key(kw.value, maps):
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
    consts = const_key_names(tree)
    if global_guard(tree, dead, consts):
        return True
    if environ_transport_guard(tree, dead, consts):
        return True
    if twohop_guard(tree, dead, consts):
        return True
    if environ_alias_guard(tree, dead, consts):
        return True
    locals_ = local_functions(tree)
    maps = splat_mapping_names(tree)
    producers = guard_producers(tree, maps)
    if inline_guarded_call(tree, producers, dead, maps):
        return True
    if carrier_guard(tree, dead):
        return True
    module_nodes = scoped_nodes(tree)
    module_binds = guard_construction_lines(module_nodes, dead, maps)
    for name, lines in producer_calls(module_nodes, producers).items():
        module_binds.setdefault(name, set()).update(lines)
    for scope in function_scopes(tree):
        nodes = scoped_nodes(scope)
        binds = guard_construction_lines(nodes, dead, maps)
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
        rebinds = unguarded_rebindings(nodes, maps)
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



# --------------------------------------------------------------------------------------- carriers
def dotted(node):
    """`a.b` for a plain attribute chain, else None."""
    parts = []
    while isinstance(node, ast.Attribute):
        parts.append(node.attr)
        node = node.value
    if isinstance(node, ast.Name):
        parts.append(node.id)
        return ".".join(reversed(parts))
    return None


def attr_dotted(node):
    """`a.b` for a chain with at least one attribute; a bare name is not an attribute."""
    if not isinstance(node, ast.Attribute):
        return None
    return dotted(node)


def module_literals(tree):
    """name -> literal value for names the module binds exactly once to a literal."""
    seen = {}
    for stmt in tree.body:
        if isinstance(stmt, ast.Assign):
            targets = [t.id for t in stmt.targets if isinstance(t, ast.Name)]
            value = stmt.value if len(stmt.targets) == 1 else None
        elif isinstance(stmt, ast.AnnAssign) and isinstance(stmt.target, ast.Name) \
                and stmt.value is not None:
            targets = [stmt.target.id]
            value = stmt.value
        else:
            continue
        for name in targets:
            seen.setdefault(name, []).append(value)
    return {name: vals[0].value for name, vals in seen.items()
            if len(vals) == 1 and isinstance(vals[0], ast.Constant)}


def const_key_names(tree):
    """Module-level string constants whose value is the guard key."""
    return {name for name, value in module_literals(tree).items()
            if isinstance(value, str) and value == KEY}


def splat_mapping_names(tree):
    """Module-level names bound once to a mapping literal that carries the key."""
    out = set()
    for stmt in tree.body:
        if isinstance(stmt, ast.Assign) and len(stmt.targets) == 1 \
                and isinstance(stmt.targets[0], ast.Name) and isinstance(stmt.value, ast.Dict) \
                and mapping_has_key(stmt.value):
            out.add(stmt.targets[0].id)
    bound = [n for n in out if sum(
        1 for st in tree.body if isinstance(st, ast.Assign)
        and any(isinstance(t, ast.Name) and t.id == n for t in st.targets)) == 1]
    return set(bound)


def splat_aliases(nodes, dead, maps):
    """One-hop aliases of module splat mappings: alias name -> (bind line, rebinding lines).

    Round-71 review (R71RevC2 F1): the first implementation credited `**m` for the first
    `m = GUARD` binding with no later-rebind check, so an alias rebound before the splat
    (`m = {"LABEL": "x"}`) carried the dominance bypass. The alias must be bound exactly
    once, and a plain rebinding of it between the alias binding and the splat line defeats
    the carrier (a rebinding after the splat is harmless: the contents were already copied).
    """
    binds = {}
    counts = {}
    for node in nodes:
        if isinstance(node, ast.Assign) and len(node.targets) == 1 \
                and node.lineno not in dead:
            target = node.targets[0]
            if isinstance(target, ast.Name) and isinstance(node.value, ast.Name) \
                    and node.value.id in maps:
                binds.setdefault(target.id, node.lineno)
                counts[target.id] = counts.get(target.id, 0) + 1
    rebound = {}
    for node in nodes:
        if isinstance(node, ast.Assign) and node.lineno not in dead:
            for target in node.targets:
                if isinstance(target, ast.Name) and target.id in binds:
                    rebound.setdefault(target.id, set()).add(node.lineno)
    out = {}
    for name, line in binds.items():
        if counts.get(name) == 1:
            out[name] = (line, rebound.get(name, set()))
    return out


def key_is_guard(slice_node, consts):
    if isinstance(slice_node, ast.Constant) and slice_node.value == KEY \
            and not isinstance(slice_node.value, bool):
        return True
    return isinstance(slice_node, ast.Name) and slice_node.id in consts


def subscript_guard_lines(nodes, dead, consts, attr=False):
    """name-or-dotted-attribute -> guard lines where the key is a literal or a module constant."""
    out = {}
    for node in nodes:
        if not isinstance(node, ast.Assign) or len(node.targets) != 1 \
                or node.lineno in dead:
            continue
        target = node.targets[0]
        if not isinstance(target, ast.Subscript) or not isinstance(target.ctx, ast.Store):
            continue
        if not key_is_guard(target.slice, consts):
            continue
        base = target.value
        if attr:
            d = dotted(base)
            if d:
                out.setdefault(d, set()).add(node.lineno)
        elif isinstance(base, ast.Name) and env_named(base.id):
            out.setdefault(base.id, set()).add(node.lineno)
    return out


def alias_guard_lines(nodes, dead, consts):
    """env-named source name -> guard lines applied through a non-env-named alias of it."""
    aliases = {}
    for node in nodes:
        if isinstance(node, ast.Assign) and len(node.targets) == 1 \
                and node.lineno not in dead:
            target = node.targets[0]
            if isinstance(target, ast.Name) and isinstance(node.value, ast.Name) \
                    and env_named(node.value.id) and not env_named(target.id):
                aliases[target.id] = node.value.id
    out = {}
    for node in nodes:
        if not isinstance(node, ast.Assign) or len(node.targets) != 1 \
                or node.lineno in dead:
            continue
        target = node.targets[0]
        if isinstance(target, ast.Subscript) and isinstance(target.ctx, ast.Store) \
                and isinstance(target.value, ast.Name) and target.value.id in aliases \
                and key_is_guard(target.slice, consts):
            out.setdefault(aliases[target.value.id], set()).add(node.lineno)
    return out


def splat_guard_lines(nodes, dead, maps, aliases=None):
    """env-named name -> guard lines where a `**module_mapping` (or a one-hop alias of it,
    round 71) expands into its literal. An alias counts only when it is bound strictly
    before the splat line and is not rebound in between (R71RevC2 F1)."""
    if aliases is None:
        aliases = {}
    out = {}
    for node in nodes:
        if not isinstance(node, ast.Assign) or len(node.targets) != 1 \
                or node.lineno in dead:
            continue
        target = node.targets[0]
        if not (isinstance(target, ast.Name) and env_named(target.id)
                and isinstance(node.value, ast.Dict)):
            continue
        for key, value in zip(node.value.keys, node.value.values):
            if key is None and isinstance(value, ast.Name) \
                    and (value.id in maps or value.id in aliases):
                if value.id in aliases:
                    bind_line, rebinds = aliases[value.id]
                    if not (bind_line < node.lineno
                            and not any(bind_line < r < node.lineno for r in rebinds)):
                        continue
                out.setdefault(target.id, set()).add(node.lineno)
                break
    return out


def attribute_flow(tree, dead, consts):
    """Guard key stored on an attribute that reaches a git launch, in order and unreplaced.

    Round-70 review (R70RevC2 a13/a14) showed the first implementation accepted any store
    anywhere in the module: a later `self.env = {}` replacement and a call *before* the store
    both counted. The frozen sentence requires the same dominance test as the name flow, so the
    bounded implementation requires a store line strictly before the call line and no plain
    assignment to the same dotted attribute in between, either at the call's `env=` or through an
    env-named binding. Cross-method order is line order; a store in `__init__` precedes a use in
    another method, and the disclosure names that approximation.

    Round 71 adds one *object-alias edge*: an assignment `cfg.runner = runner` (a dotted target
    bound to a plain name) bridges the store's dotted name to the call's dotted name — a use
    `env=cfg.runner.env` resolves through the edge to `runner.env`. One edge, exact dotted
    names, no chains.
    """
    guarded = {}
    replaced = {}
    for node in ast.walk(tree):
        if not isinstance(node, ast.Assign) or node.lineno in dead:
            continue
        for target in node.targets:
            if isinstance(target, ast.Subscript) and isinstance(target.ctx, ast.Store):
                d = attr_dotted(target.value)
                if d and key_is_guard(target.slice, consts):
                    guarded.setdefault(d, set()).add(node.lineno)
            else:
                d = attr_dotted(target)
                if d:
                    replaced.setdefault(d, set()).add(node.lineno)
    if not guarded:
        return False

    object_edges = {}
    edge_lines = {}
    edge_counts = {}
    for node in ast.walk(tree):
        if not isinstance(node, ast.Assign) or node.lineno in dead:
            continue
        if len(node.targets) == 1 and isinstance(node.targets[0], ast.Attribute) \
                and isinstance(node.value, ast.Name):
            d = dotted(node.targets[0])
            edge_counts[d] = edge_counts.get(d, 0) + 1
            object_edges.setdefault(d, node.value.id)
            edge_lines.setdefault(d, node.lineno)
    object_edges = {d: s for d, s in object_edges.items() if edge_counts[d] == 1}

    def resolve(d, at_line):
        if "." not in d:
            return d
        prefix, last = d.rsplit(".", 1)
        # R71RevC2 F2: the bridge must exist at the launch — an edge bound after the
        # call line resolves nothing (the pre-bound object carries no guarded store).
        if prefix in object_edges and edge_lines.get(prefix, 1 << 30) < at_line:
            return object_edges[prefix] + "." + last
        return d

    # replacements recorded under an edge-resolved name count against the resolved store
    for d, d_lines in list(replaced.items()):
        at = min(d_lines) if d_lines else 0
        r = resolve(d, at)
        if r != d and r in guarded:
            replaced.setdefault(r, set()).update(d_lines)

    def store_before(d, line):
        for store in guarded.get(d, ()):
            if store < line and not any(store < r < line for r in replaced.get(d, ())):
                return True
        return False

    for node in ast.walk(tree):
        if not isinstance(node, ast.Call) or not call_is_git(node) or node.lineno in dead:
            continue
        for kw in node.keywords:
            if kw.arg == "env":
                d = attr_dotted(kw.value)
                if d and (store_before(d, node.lineno)
                          or store_before(resolve(d, node.lineno), node.lineno)):
                    return True

    bind_lines = {}
    for node in ast.walk(tree):
        if not isinstance(node, ast.Assign) or len(node.targets) != 1 \
                or node.lineno in dead:
            continue
        target = node.targets[0]
        d = attr_dotted(node.value)
        if isinstance(target, ast.Name) and env_named(target.id) and d \
                and (store_before(d, node.lineno)
                     or store_before(resolve(d, node.lineno), node.lineno)):
            bind_lines.setdefault(target.id, set()).add(node.lineno)
    if not bind_lines:
        return False
    locals_ = local_functions(tree)
    for scope in function_scopes(tree):
        nodes = scoped_nodes(scope)
        rebinds = unguarded_rebindings(nodes)
        for name, lines in bind_lines.items():
            uses = usage_lines(nodes, name, locals_)
            for line in lines:
                after = [use for use in uses if use > line]
                if after and not any(line < r < min(after) for r in rebinds.get(name, ())):
                    return True
    return False


def alias_store_guard(tree, dead):
    """The key stored through a one-hop alias of the mapping handed to a git launch.

    Round-71 shape (c): the env= name `n` is bound exactly once in scope to a mapping
    expression; an alias `a = n` exists; a subscript store `a[KEY] = …` (literal key or
    module constant key) sits strictly between the alias binding's store and the call, with no
    rebinding of `a` or `n` in between. Deeper chains stay uncovered.
    """
    for scope in function_scopes(tree):
        nodes = scoped_nodes(scope)
        binds = {}
        bind_counts = {}
        for node in nodes:
            if not isinstance(node, ast.Assign) or len(node.targets) != 1 \
                    or node.lineno in dead:
                continue
            target = node.targets[0]
            if isinstance(target, ast.Name) \
                    and (isinstance(node.value, ast.Dict)
                         or (isinstance(node.value, ast.Call)
                             and isinstance(node.value.func, ast.Name)
                             and node.value.func.id == "dict")):
                binds[target.id] = node.lineno
                bind_counts[target.id] = bind_counts.get(target.id, 0) + 1
        mapping_names = {n for n, c in bind_counts.items() if c == 1}
        if not mapping_names:
            continue
        aliases = {}
        for node in nodes:
            if not isinstance(node, ast.Assign) or len(node.targets) != 1 \
                    or node.lineno in dead:
                continue
            target = node.targets[0]
            if isinstance(target, ast.Name) and isinstance(node.value, ast.Name) \
                    and node.value.id in mapping_names:
                aliases.setdefault(target.id, node.value.id)
        if not aliases:
            continue
        consts = const_key_names(tree)
        stores = {}
        for node in nodes:
            if not isinstance(node, ast.Assign) or len(node.targets) != 1 \
                    or node.lineno in dead:
                continue
            target = node.targets[0]
            if isinstance(target, ast.Subscript) and isinstance(target.ctx, ast.Store) \
                    and isinstance(target.value, ast.Name) \
                    and target.value.id in aliases \
                    and key_is_guard(target.slice, consts):
                stores.setdefault(target.value.id, set()).add(node.lineno)
        if not stores:
            continue
        # any plain rebinding of the alias or the handed mapping, whatever its spelling
        rebound = {}
        for node in nodes:
            if isinstance(node, ast.Assign) and node.lineno not in dead:
                for target in node.targets:
                    if isinstance(target, ast.Name) and target.id in aliases.values() \
                            or isinstance(target, ast.Name) and target.id in aliases:
                        rebound.setdefault(target.id, set()).add(node.lineno)
        for node in nodes:
            if not isinstance(node, ast.Call) or not call_is_git(node) or node.lineno in dead:
                continue
            for kw in node.keywords:
                if kw.arg != "env" or not isinstance(kw.value, ast.Name):
                    continue
                n = kw.value.id
                if n not in mapping_names:
                    continue
                for a, src in aliases.items():
                    if src != n:
                        continue
                    for g in stores.get(a, ()):
                        blockers = rebound.get(a, set()) | rebound.get(n, set())
                        if g < node.lineno and not any(g < r < node.lineno
                                                       for r in blockers):
                            return True
    return False


def carrier_guard(tree, dead):
    """The round-70 carriers plus the four round-71 shapes, each under the dominance flows."""
    consts = const_key_names(tree)
    maps = splat_mapping_names(tree)
    if attribute_flow(tree, dead, consts):
        return True
    if alias_store_guard(tree, dead):
        return True
    module_nodes = scoped_nodes(tree)
    module_aliases = splat_aliases(module_nodes, dead, maps)
    module_binds = {}
    for extra in (subscript_guard_lines(module_nodes, dead, consts),
                  alias_guard_lines(module_nodes, dead, consts),
                  splat_guard_lines(module_nodes, dead, maps, module_aliases)):
        for name, lines in extra.items():
            module_binds.setdefault(name, set()).update(lines)
    locals_ = local_functions(tree)
    for scope in function_scopes(tree):
        nodes = scoped_nodes(scope)
        visible = consts if scope is tree else consts - assigned_names(nodes)
        scope_aliases = dict(module_aliases)
        scope_aliases.update(splat_aliases(nodes, dead, maps))
        binds = {}
        for extra in (subscript_guard_lines(nodes, dead, visible),
                      alias_guard_lines(nodes, dead, visible),
                      splat_guard_lines(nodes, dead, maps, scope_aliases)):
            for name, lines in extra.items():
                binds.setdefault(name, set()).update(lines)
        if scope is not tree:
            local_names = assigned_names(nodes) | set(binds)
            for name, lines in module_binds.items():
                if name not in local_names:
                    binds.setdefault(name, set()).update(lines)
        if not binds:
            continue
        rebinds = unguarded_rebindings(nodes, maps)
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



# --------------------------------------------------------------------------------------- r73 carriers
def global_guard(tree, dead, consts):
    """Round-73: a guard stored into a `global`-declared name from inside a function.

    ``global ENV`` makes the assignment bind module scope, so a store ``ENV[KEY] = "1"`` inside
    ``setup()`` guards the module mapping that a later ``env=ENV`` launch hands to the child.
    Bounded: the store sits in a function that declares the name ``global``; the launch line is
    strictly after the store (cross-function line order, the attribute-flow approximation); a
    plain replacement of the name between store and launch cancels the store.
    """
    stores = {}
    for fn in ast.walk(tree):
        if not isinstance(fn, (ast.FunctionDef, ast.AsyncFunctionDef)):
            continue
        globals_here = set()
        for node in ast.walk(fn):
            if isinstance(node, ast.Global):
                globals_here.update(node.names)
        if not globals_here:
            continue
        for node in ast.walk(fn):
            if not isinstance(node, ast.Assign) or node.lineno in dead:
                continue
            for target in node.targets:
                if isinstance(target, ast.Subscript) and isinstance(target.ctx, ast.Store) \
                        and isinstance(target.value, ast.Name) \
                        and target.value.id in globals_here \
                        and key_is_guard(target.slice, consts):
                    stores.setdefault(target.value.id, set()).add(node.lineno)
                elif isinstance(target, ast.Name) and target.id in globals_here \
                        and mapping_has_key(node.value):
                    stores.setdefault(target.id, set()).add(node.lineno)
    if not stores:
        return False
    replaced = {}

    def note_replacement(node):
        if not isinstance(node, ast.Assign) or node.lineno in dead:
            return
        for target in node.targets:
            if isinstance(target, ast.Name) and target.id in stores \
                    and not mapping_has_key(node.value):
                replaced.setdefault(target.id, set()).add(node.lineno)

    # Only an assignment that resolves to the module binding cancels a store: a module-level
    # assignment, or one inside a function that declares the name `global` (R73RevC2 F2).
    for node in tree.body:
        note_replacement(node)
    for fn in ast.walk(tree):
        if not isinstance(fn, (ast.FunctionDef, ast.AsyncFunctionDef)):
            continue
        globals_here = set()
        for node in ast.walk(fn):
            if isinstance(node, ast.Global):
                globals_here.update(node.names)
        if not stores.keys() & globals_here:
            continue
        for node in ast.walk(fn):
            note_replacement(node)

    # A launch inside a function that binds the name as a parameter or as a non-global local
    # does not resolve to the module binding (R73RevC2 F1).
    for scope in function_scopes(tree):
        nodes = scoped_nodes(scope)
        shadow = set()
        if scope is not tree:
            shadow.update(arg.arg for arg in scope.args.args)
            shadow.update(arg.arg for arg in scope.args.kwonlyargs)
            if scope.args.vararg is not None:
                shadow.add(scope.args.vararg.arg)
            if scope.args.kwarg is not None:
                shadow.add(scope.args.kwarg.arg)
            globals_here = set()
            for node in ast.walk(scope):
                if isinstance(node, ast.Global):
                    globals_here.update(node.names)
            shadow.update(name for name in assigned_names(nodes) if name not in globals_here)
        for node in nodes:
            if not isinstance(node, ast.Call) or not call_is_git(node) or node.lineno in dead:
                continue
            for kw in node.keywords:
                if kw.arg != "env" or not isinstance(kw.value, ast.Name):
                    continue
                name = kw.value.id
                if name in shadow:
                    continue
                for store in stores.get(name, ()):
                    if store < node.lineno and not any(store < r < node.lineno
                                                       for r in replaced.get(name, ())):
                        return True
    return False


def copies_environ(node):
    """`{**os.environ}` or `dict(os.environ)` - the two copy spellings the frozen set names."""
    if isinstance(node, ast.Dict) and len(node.keys) == 1 and node.keys[0] is None:
        return attr_dotted(node.values[0]) == "os.environ"
    if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) \
            and node.func.id == "dict" and len(node.args) == 1 and not node.keywords:
        return attr_dotted(node.args[0]) == "os.environ"
    return False


def environ_transport_guard(tree, dead, consts):
    """Round-73: the guard lives in the mutated process environment and is copied into the child.

    ``os.environ[KEY] = "1"`` before a launch whose ``env=`` copies the environment hands the key
    to the child. Bounded: the store precedes the launch line and a replacement of ``os.environ``
    in between cancels it; stores through an alias of ``os.environ`` are not followed.
    """
    stores = set()
    replaced = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Delete) and node.lineno not in dead:
            for target in node.targets:
                if isinstance(target, ast.Subscript) and isinstance(target.ctx, ast.Del) \
                        and attr_dotted(target.value) == "os.environ" \
                        and key_is_guard(target.slice, consts):
                    replaced.add(node.lineno)
            continue
        if not isinstance(node, ast.Assign) or node.lineno in dead:
            continue
        for target in node.targets:
            if isinstance(target, ast.Subscript) and isinstance(target.ctx, ast.Store) \
                    and attr_dotted(target.value) == "os.environ" \
                    and key_is_guard(target.slice, consts):
                stores.add(node.lineno)
            elif attr_dotted(target) == "os.environ":
                replaced.add(node.lineno)
    if not stores:
        return False
    for node in ast.walk(tree):
        if not isinstance(node, ast.Call) or not call_is_git(node) or node.lineno in dead:
            continue
        for kw in node.keywords:
            if kw.arg != "env" or not copies_environ(kw.value):
                continue
            for store in stores:
                if store < node.lineno and not any(store < r < node.lineno for r in replaced):
                    return True
    return False


# --------------------------------------------------------------------------------------- r74 carriers
def binding_nodes(tree, dead):
    """Every binding statement of a plain name, `Assign` and `AnnAssign` alike."""
    for node in ast.walk(tree):
        if not isinstance(node, (ast.Assign, ast.AnnAssign)):
            continue
        if node.lineno in dead:
            continue
        if isinstance(node, ast.Assign) and len(node.targets) == 1 \
                and isinstance(node.targets[0], ast.Name):
            yield node, node.targets[0], node.value
        elif isinstance(node, ast.AnnAssign) and isinstance(node.target, ast.Name) \
                and node.value is not None:
            yield node, node.target, node.value


def object_alias_map(tree, dead):
    """Plain name -> (dotted path, binding line) for names bound exactly once to a dotted chain.

    Round-74 review (R74RevC2 P2): `AnnAssign` bindings count too, and the binding line is kept
    so the alias edge must exist before the store that crosses it (R74RevC2 P2, `13_late_alias`).
    """
    binds = {}
    counts = {}
    for node, target, value in binding_nodes(tree, dead):
        counts[target.id] = counts.get(target.id, 0) + 1
        d = attr_dotted(value)
        if d:
            binds[target.id] = (d, node.lineno)
    return {n: v for n, v in binds.items() if counts.get(n) == 1}


def canonical_dotted(d, aliases):
    """`r.env` with `r = cfg.runner` -> `cfg.runner.env`; the longest alias prefix wins."""
    parts = d.split(".")
    for i in range(len(parts) - 1, 0, -1):
        prefix = ".".join(parts[:i])
        if prefix in aliases:
            return aliases[prefix][0] + "." + ".".join(parts[i:])
    return d


def root_name(d):
    return d.split(".", 1)[0]


def shadow_names(scope):
    """Parameter names of a function scope; a module scope shadows nothing."""
    if scope is None or scope is getattr(scope, "_module_marker", None):
        return set()
    if not isinstance(scope, (ast.FunctionDef, ast.AsyncFunctionDef)):
        return set()
    return {p.arg for p in _params(scope)}


def twohop_guard(tree, dead, consts):
    """Round-74: a guard stored through an object alias and handed at the other spelling.

    ``r = cfg.runner`` binds a plain name to a dotted path exactly once; the guard key stored at
    ``r.env[KEY]`` and a launch handing ``env=cfg.runner.env`` (or the reverse) name the same
    dotted path. The store must sit strictly before the launch, the alias edge must exist before
    the store (R74RevC2 P2), no replacement of that path may sit in between, and at least one side
    must actually cross the alias edge. A launch inside a function whose parameter shadows the
    alias root is not the module binding (R74RevC2 P1).
    """
    aliases = object_alias_map(tree, dead)
    if not aliases:
        return False
    guarded = {}
    replaced = {}
    for node in ast.walk(tree):
        if not isinstance(node, ast.Assign) or node.lineno in dead:
            continue
        for target in node.targets:
            if isinstance(target, ast.Subscript) and isinstance(target.ctx, ast.Store):
                d = attr_dotted(target.value)
                if d and key_is_guard(target.slice, consts):
                    canonical = canonical_dotted(d, aliases)
                    root = root_name(d)
                    bind = aliases.get(root, (None, 1 << 30))[1]
                    guarded.setdefault(canonical, []).append(
                        (node.lineno, d != canonical, bind))
            else:
                d = attr_dotted(target)
                if d:
                    replaced.setdefault(canonical_dotted(d, aliases), set()).add(node.lineno)
    if not guarded:
        return False
    for scope in function_scopes(tree):
        nodes = scoped_nodes(scope)
        shadow = shadow_names(scope)
        for node in nodes:
            if not isinstance(node, ast.Call) or not call_is_git(node) or node.lineno in dead:
                continue
            for kw in node.keywords:
                if kw.arg != "env":
                    continue
                d = attr_dotted(kw.value)
                if not d or root_name(d) in shadow:
                    continue
                canonical = canonical_dotted(d, aliases)
                crossed_call = d != canonical
                bind_call = aliases.get(root_name(d), (None, 1 << 30))[1]
                for store, crossed_store, bind_store in guarded.get(canonical, ()):
                    if not (crossed_call or crossed_store):
                        continue
                    store_ok = (not crossed_store) or bind_store < store
                    call_ok = (not crossed_call) or bind_call < node.lineno
                    if store_ok and call_ok and store < node.lineno \
                            and not any(store < r < node.lineno
                                        for r in replaced.get(canonical, ())):
                        return True
    return False


def environ_alias_names(tree, dead):
    """One-hop aliases of ``os.environ``: a plain name bound to it exactly once (either form)."""
    counts = {}
    binds = {}
    for node, target, value in binding_nodes(tree, dead):
        counts[target.id] = counts.get(target.id, 0) + 1
        if attr_dotted(value) == "os.environ":
            binds[target.id] = node.lineno
    return {n: line for n, line in binds.items() if counts.get(n) == 1}


def copies_alias(node, aliases):
    """``{**alias}`` or ``dict(alias)`` - a copy of the one-hop environment alias."""
    if isinstance(node, ast.Dict) and len(node.keys) == 1 and node.keys[0] is None \
            and isinstance(node.values[0], ast.Name):
        return node.values[0].id in aliases
    if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) \
            and node.func.id == "dict" and len(node.args) == 1 and not node.keywords \
            and isinstance(node.args[0], ast.Name):
        return node.args[0].id in aliases
    return False


def environ_alias_guard(tree, dead, consts):
    """Round-74: the guard key stored through a one-hop alias of ``os.environ``.

    ``env = os.environ`` once (``Assign`` or ``AnnAssign``), ``env[KEY] = "1"`` after the binding
    and before a git launch whose ``env=`` is the alias itself, ``dict(env)`` or ``{**env}``. A
    second binding leaves no alias; a ``del alias[KEY]`` between store and launch cancels the
    store; a store before the binding or after the launch is not a guard; a launch inside a
    function whose parameter shadows the alias name is not the module binding (R74RevC2 P1).
    """
    aliases = environ_alias_names(tree, dead)
    if not aliases:
        return False
    stores = {}
    cancels = {}
    for node in ast.walk(tree):
        if isinstance(node, ast.Delete) and node.lineno not in dead:
            for target in node.targets:
                if isinstance(target, ast.Subscript) and isinstance(target.ctx, ast.Del) \
                        and isinstance(target.value, ast.Name) \
                        and target.value.id in aliases and key_is_guard(target.slice, consts):
                    cancels.setdefault(target.value.id, set()).add(node.lineno)
            continue
        if not isinstance(node, ast.Assign) or node.lineno in dead:
            continue
        for target in node.targets:
            if isinstance(target, ast.Subscript) and isinstance(target.ctx, ast.Store) \
                    and isinstance(target.value, ast.Name) \
                    and target.value.id in aliases and key_is_guard(target.slice, consts):
                stores.setdefault(target.value.id, set()).add(node.lineno)
    if not stores:
        return False
    for scope in function_scopes(tree):
        nodes = scoped_nodes(scope)
        shadow = shadow_names(scope)
        for node in nodes:
            if not isinstance(node, ast.Call) or not call_is_git(node) or node.lineno in dead:
                continue
            for kw in node.keywords:
                if kw.arg != "env":
                    continue
                name = None
                if isinstance(kw.value, ast.Name) and kw.value.id in aliases:
                    name = kw.value.id
                elif isinstance(kw.value, ast.Dict) and copies_alias(kw.value, aliases):
                    name = kw.value.values[0].id
                elif isinstance(kw.value, ast.Call) and copies_alias(kw.value, aliases):
                    name = kw.value.args[0].id
                if name is None or name in shadow:
                    continue
                for store in stores.get(name, ()):
                    if aliases[name] < store and store < node.lineno \
                            and not any(store < c < node.lineno
                                        for c in cancels.get(name, ())):
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



def held_check(repo, sha, cases):
    """The round-73 control file must still hash to its frozen digest and match the held cases."""
    data = extract(repo, sha, HELD_CONTROLS)
    if data is None:
        raise SetupError("%s is absent at %s" % (HELD_CONTROLS, sha))
    digest = sha256_hex(data)
    if digest != HELD_CONTROLS_SHA:
        raise SetupError("held controls sha256 %s does not match the frozen digest" % digest)
    try:
        doc = json.loads(data.decode("utf-8"))
        held = doc["cases"]
    except (UnicodeDecodeError, ValueError, KeyError) as exc:
        raise SetupError("held controls unusable: %s" % exc)
    if len(held) != HELD_CASES:
        raise SetupError("held controls carry %d cases, frozen %d" % (len(held), HELD_CASES))
    by_name = {case["name"]: case for case in cases}
    for case in held:
        mine = by_name.get(case["name"])
        if mine is None or mine["src"] != case["src"] \
                or mine["expect_reader"] != case["expect_reader"] \
                or mine["expect_guard"] != case["expect_guard"]:
            raise SetupError("held case %r is not carried forward byte-identically"
                             % case["name"])
    emit("MADO_R75_HELD_CONTROLS path=%s cases=%d sha256=%s carried=yes"
         % (HELD_CONTROLS, len(held), digest))
    return len(held)


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
        emit("MADO_R75_BASE_COUNTER path=%s present=no" % BASE_COUNTER)
        return None
    path = os.path.join(scratch, "base-counter.py")
    os.makedirs(scratch, exist_ok=True)
    with open(path, "wb") as fh:
        fh.write(data)
    module = runpy.run_path(path)
    emit("MADO_R75_BASE_COUNTER path=%s present=yes sha256=%s" % (BASE_COUNTER, sha256_hex(data)))
    return module["classify"]


def score_cases(classify_fn, cases, leg="candidate"):
    correct = 0
    for case in cases:
        reader, guard = classify_fn(case["src"])
        ok = (reader == case["expect_reader"]) and (guard == case["expect_guard"])
        correct += int(ok)
        emit("MADO_R75_CONTROL leg=%s name=%s reader=%s guard=%s expect_reader=%s expect_guard=%s "
             "correct=%s"
             % (leg, case["name"], "yes" if reader else "no", "yes" if guard else "no",
                "yes" if case["expect_reader"] else "no",
                "yes" if case["expect_guard"] else "no", "yes" if ok else "no"))
    return correct


def contract_line(population, readers, guarded, unguarded, controls, base_controls, sha):
    return ("MADO_R75_GUARD_SHAPES: population=%d readers=%d guarded=%d unguarded=%d "
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
    work = os.path.join(scratch, "r75-c2-shapes")
    if os.path.isdir(work):
        shutil.rmtree(work)
    os.makedirs(work)

    cases = load_controls(os.path.abspath(args.controls))
    emit("MADO_R75_CONTROLS path=%s cases=%d sha256=%s"
         % (os.path.abspath(args.controls), len(cases), FROZEN_CONTROLS_SHA))

    sha = rev_parse(repo, args.rev)
    base_sha = rev_parse(repo, args.base_rev or args.rev)

    held_check(repo, sha, cases)

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
        emit("MADO_R75_READER file=%s reader=%s guard=%s"
             % (path, "yes" if reader else "no", "yes" if guard else "no"))
    unguarded = readers - guarded

    controls = score_cases(classify, cases)
    classify_base = base_classify(repo, base_sha, os.path.join(work, "base"))
    if classify_base is None:
        base_controls = 0
    else:
        base_controls = score_cases(classify_base, cases, leg="base")
        emit("MADO_R75_BASE controls=%d/%d (the held round-74 rule must miss the target)"
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
    'guarded-inline': ('def run(repo):\n    subprocess.run(["git", "-C", repo, "show", "HEAD:a"],\n                   env=dict(os.environ, GIT_NO_REPLACE_OBJECTS="1"))\n', True, True),
    'value-position-only': ('def run(repo):\n    env = {"PATH": "/usr/bin", "LABEL": "GIT_NO_REPLACE_OBJECTS"}\n    subprocess.run(["git", "-C", repo, "show", "HEAD:a"], env=env)\n', True, False),
    'dead-branch-only': ('def run(repo):\n    env = {"PATH": "/usr/bin"}\n    if False:\n        env["GIT_NO_REPLACE_OBJECTS"] = "1"\n    subprocess.run(["git", "-C", repo, "show", "HEAD:a"], env=env)\n', True, False),
    'uncalled-helper': ('def guarded_env():\n    env = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}\n    env["GIT_NO_REPLACE_OBJECTS"] = "1"\n    return env\n\n\ndef run(repo):\n    plain = {"PATH": "/usr/bin"}\n    subprocess.run(["git", "-C", repo, "show", "HEAD:a"], env=plain)\n', True, False),
    'overwritten-env': ('def run(repo):\n    env = {"PATH": "/usr/bin", "GIT_NO_REPLACE_OBJECTS": "1"}\n    env = {"PATH": "/usr/bin"}\n    subprocess.run(["git", "-C", repo, "show", "HEAD:a"], env=env)\n', True, False),
    'update-guard': ('def run(repo):\n    env = {}\n    env.update(GIT_NO_REPLACE_OBJECTS="1")\n    subprocess.run(["git", "-C", repo, "ls-tree", "-r", "HEAD"], env=env)\n', True, True),
    'subscript-guard': ('def git(repo, *args):\n    env = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}\n    env["GIT_NO_REPLACE_OBJECTS"] = "1"\n    return subprocess.run(["git", "-C", repo] + list(args), env=env)\n\n\ndef head(repo):\n    return git(repo, "show", "HEAD:a")\n', True, True),
    'module-constant': ('GIT_ENV = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}\nGIT_ENV["GIT_NO_REPLACE_OBJECTS"] = "1"\n\n\ndef head(repo):\n    return subprocess.run(["git", "-C", repo, "show", "HEAD:a"], env=GIT_ENV)\n', True, True),
    'producer-helper': ('def git_env(work):\n    env = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}\n    env["GIT_NO_REPLACE_OBJECTS"] = "1"\n    return env\n\n\ndef run(repo, work):\n    env = git_env(work)\n    return subprocess.run(["git", "-C", repo, "show", "HEAD:a"], env=env)\n', True, True),
    'argv-name-flow': ('def run(repo):\n    cmd = ["git", "-C", repo, "show", "HEAD:a"]\n    subprocess.run(cmd, capture_output=True, env=git_env())\n\n\ndef git_env():\n    env = {"PATH": "/usr/bin"}\n    env["GIT_NO_REPLACE_OBJECTS"] = "1"\n    return env\n', True, True),
    'mention-only': ('"""Reads objects with git show; GIT_NO_REPLACE_OBJECTS is not set here."""\n\n\ndef run(repo):\n    # the guard GIT_NO_REPLACE_OBJECTS is deliberately absent in this sample\n    subprocess.run(["git", "-C", repo, "show", "HEAD:a"], env=dict(os.environ))\n', True, False),
    'alias-carried': ('def run(repo):\n    base = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}\n    env = base\n    alias = env\n    alias["GIT_NO_REPLACE_OBJECTS"] = "1"\n    return subprocess.run(["git", "-C", repo, "show", "HEAD:a"], env=env)\n', True, True),
    'attribute-carried': ('class Runner:\n    def __init__(self):\n        self.env = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}\n        self.env["GIT_NO_REPLACE_OBJECTS"] = "1"\n\n    def head(self, repo):\n        return subprocess.run(["git", "-C", repo, "show", "HEAD:a"], env=self.env)\n', True, True),
    'splat-carried': ('GUARD = {"GIT_NO_REPLACE_OBJECTS": "1"}\n\n\ndef run(repo):\n    env = {**os.environ, **GUARD}\n    return subprocess.run(["git", "-C", repo, "show", "HEAD:a"], env=env)\n', True, True),
    'constant-key': ('KEY = "GIT_NO_REPLACE_OBJECTS"\n\n\ndef run(repo):\n    env = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}\n    env[KEY] = "1"\n    return subprocess.run(["git", "-C", repo, "show", "HEAD:a"], env=env)\n', True, True),
    'guarded-env-for-a-non-git-call': ('def run(repo):\n    plain = {"PATH": "/usr/bin"}\n    other = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}\n    other["GIT_NO_REPLACE_OBJECTS"] = "1"\n    subprocess.run(["git", "-C", repo, "show", "HEAD:a"], env=plain)\n    subprocess.run(["ls", "-l"], env=other)\n', True, False),
    'git-called-without-env': ('def run(repo):\n    env = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}\n    env["GIT_NO_REPLACE_OBJECTS"] = "1"\n    return subprocess.run(["git", "-C", repo, "show", "HEAD:a"])\n', True, False),
    'dict-call-splat': ('GUARD = {"GIT_NO_REPLACE_OBJECTS": "1"}\n\ndef run(repo):\n    env = dict(os.environ, **GUARD)\n    subprocess.run(["git", "-C", repo, "show", "HEAD:a"], env=env)\n', True, True),
    'dict-call-splat-object-alias': ('GUARD = {"GIT_NO_REPLACE_OBJECTS": "1"}\n\ndef run(repo):\n    m = GUARD\n    env = {**os.environ, **m}\n    subprocess.run(["git", "-C", repo, "show", "HEAD:a"], env=env)\n', True, True),
    'store-through-alias-two-hop': ('def run(repo):\n    e = {"PATH": "/usr/bin"}\n    staging = e\n    staging["GIT_NO_REPLACE_OBJECTS"] = "1"\n    subprocess.run(["git", "-C", repo, "show", "HEAD:a"], env=e)\n', True, True),
    'attribute-second-object': ('def run(repo):\n    runner.env = {}\n    runner.env["GIT_NO_REPLACE_OBJECTS"] = "1"\n    cfg.runner = runner\n    subprocess.run(["git", "-C", repo, "show", "HEAD:a"], env=cfg.runner.env)\n', True, True),
    'unguarded-dict-splat-negative': ('OTHER = {"LABEL": "x"}\n\ndef run(repo):\n    env = dict(os.environ, **OTHER)\n    subprocess.run(["git", "-C", repo, "show", "HEAD:a"], env=env)\n', True, False),
    'env-call-no-key-negative': ('def run(repo):\n    env = dict(os.environ)\n    subprocess.run(["git", "-C", repo, "show", "HEAD:a"], env=env)\n', True, False),
    'global-rebind-guard': ('ENV = {"PATH": "/usr/bin"}\n\ndef setup():\n    global ENV\n    ENV["GIT_NO_REPLACE_OBJECTS"] = "1"\n\ndef run(repo):\n    setup()\n    subprocess.run(["git", "-C", repo, "show", "HEAD:a"], env=ENV)\n', True, True),
    'environ-splat-guard': ('def run(repo):\n    os.environ["GIT_NO_REPLACE_OBJECTS"] = "1"\n    subprocess.run(["git", "-C", repo, "show", "HEAD:a"], env={**os.environ})\n', True, True),
    'environ-call-guard': ('def run(repo):\n    os.environ["GIT_NO_REPLACE_OBJECTS"] = "1"\n    subprocess.run(["git", "-C", repo, "show", "HEAD:a"], env=dict(os.environ))\n', True, True),
    'global-rebind-value-only': ('ENV = {"PATH": "/usr/bin"}\n\ndef setup():\n    global ENV\n    ENV["LABEL"] = "GIT_NO_REPLACE_OBJECTS"\n\ndef run(repo):\n    setup()\n    subprocess.run(["git", "-C", repo, "show", "HEAD:a"], env=ENV)\n', True, False),
    'environ-store-after-call': ('def run(repo):\n    subprocess.run(["git", "-C", repo, "show", "HEAD:a"], env={**os.environ})\n    os.environ["GIT_NO_REPLACE_OBJECTS"] = "1"\n', True, False),
    'twohop-attr-store-dotted-call': ('def run(repo):\n    r = cfg.runner\n    r.env["GIT_NO_REPLACE_OBJECTS"] = "1"\n    subprocess.run(["git", "-C", repo, "show", "HEAD:a"], env=cfg.runner.env)\n', True, True),
    'twohop-attr-store-alias-call': ('def run(repo):\n    r = cfg.runner\n    cfg.runner.env["GIT_NO_REPLACE_OBJECTS"] = "1"\n    subprocess.run(["git", "-C", repo, "show", "HEAD:a"], env=r.env)\n', True, True),
    'environ-alias-call-guard': ('def run(repo):\n    env = os.environ\n    env["GIT_NO_REPLACE_OBJECTS"] = "1"\n    subprocess.run(["git", "-C", repo, "show", "HEAD:a"], env=dict(env))\n', True, True),
    'environ-alias-splat-guard': ('def run(repo):\n    env = os.environ\n    env["GIT_NO_REPLACE_OBJECTS"] = "1"\n    subprocess.run(["git", "-C", repo, "show", "HEAD:a"], env={**env})\n', True, True),
    'twohop-attr-store-after-call': ('def run(repo):\n    r = cfg.runner\n    subprocess.run(["git", "-C", repo, "show", "HEAD:a"], env=r.env)\n    r.env["GIT_NO_REPLACE_OBJECTS"] = "1"\n', True, False),
    'twohop-attr-store-replaced': ('def run(repo):\n    r = cfg.runner\n    r.env["GIT_NO_REPLACE_OBJECTS"] = "1"\n    r.env = {"PATH": "/usr/bin"}\n    subprocess.run(["git", "-C", repo, "show", "HEAD:a"], env=r.env)\n', True, False),
    'environ-alias-no-store': ('def run(repo):\n    env = os.environ\n    subprocess.run(["git", "-C", repo, "show", "HEAD:a"], env=env)\n', True, False),
    'environ-alias-rebound': ('def run(repo):\n    env = os.environ\n    env = {"PATH": "/usr/bin"}\n    subprocess.run(["git", "-C", repo, "show", "HEAD:a"], env=env)\n', True, False),
    'copy-dict-kw-bound': ('def run(repo):\n    env = os.environ\n    child = dict(env, GIT_NO_REPLACE_OBJECTS="1")\n    subprocess.run(["git", "-C", repo, "show", "HEAD:a"], env=child)\n', True, True),
    'copy-splat-bound': ('def run(repo):\n    env = os.environ\n    child = {**env, "GIT_NO_REPLACE_OBJECTS": "1"}\n    subprocess.run(["git", "-C", repo, "show", "HEAD:a"], env=child)\n', True, True),
    'copy-dict-builtin-bound': ('def run(repo):\n    child = dict(os.environ, GIT_NO_REPLACE_OBJECTS="1")\n    subprocess.run(["git", "-C", repo, "show", "HEAD:a"], env=child)\n', True, True),
    'copy-dict-literal-base': ('def run(repo):\n    base = {"PATH": "/usr/bin"}\n    child = dict(base, GIT_NO_REPLACE_OBJECTS="1")\n    subprocess.run(["git", "-C", repo, "show", "HEAD:a"], env=child)\n', True, True),
    'copy-dict-no-key': ('def run(repo):\n    env = os.environ\n    child = dict(env)\n    subprocess.run(["git", "-C", repo, "show", "HEAD:a"], env=child)\n', True, False),
    'copy-dict-value-position': ('def run(repo):\n    child = dict(os.environ, LABEL="GIT_NO_REPLACE_OBJECTS")\n    subprocess.run(["git", "-C", repo, "show", "HEAD:a"], env=child)\n', True, False),
    'copy-rebound': ('def run(repo):\n    env = os.environ\n    child = dict(env, GIT_NO_REPLACE_OBJECTS="1")\n    child = dict(env)\n    subprocess.run(["git", "-C", repo, "show", "HEAD:a"], env=child)\n', True, False),
    'del-env-store-cancel': ('def run(repo):\n    env = {"PATH": "/usr/bin"}\n    env["GIT_NO_REPLACE_OBJECTS"] = "1"\n    del env["GIT_NO_REPLACE_OBJECTS"]\n    subprocess.run(["git", "-C", repo, "show", "HEAD:a"], env=env)\n', True, False),
    'del-env-literal-cancel': ('def run(repo):\n    env = {"PATH": "/usr/bin", "GIT_NO_REPLACE_OBJECTS": "1"}\n    del env["GIT_NO_REPLACE_OBJECTS"]\n    subprocess.run(["git", "-C", repo, "show", "HEAD:a"], env=env)\n', True, False),
    'del-other-key': ('def run(repo):\n    env = {"PATH": "/usr/bin"}\n    env["GIT_NO_REPLACE_OBJECTS"] = "1"\n    del env["PATH"]\n    subprocess.run(["git", "-C", repo, "show", "HEAD:a"], env=env)\n', True, True),
    'del-before-store': ('def run(repo):\n    env = {"PATH": "/usr/bin"}\n    del env["GIT_NO_REPLACE_OBJECTS"]\n    env["GIT_NO_REPLACE_OBJECTS"] = "1"\n    subprocess.run(["git", "-C", repo, "show", "HEAD:a"], env=env)\n', True, True),
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
    "guarded-env-for-a-non-git-call": ('def run(repo):\n'
                                        '    env = {"GIT_NO_REPLACE_OBJECTS": "1"}\n'
                                        '    subprocess.run(["ls", "-l"], env=env)\n'
                                        '    subprocess.run(["git", "-C", repo, "show", "HEAD:a"])\n',
                                        True, False),
    "git-called-without-env": ('def run(repo):\n'
                                '    env = {"GIT_NO_REPLACE_OBJECTS": "1"}\n'
                                '    subprocess.run(["git", "-C", repo, "show", "HEAD:a"], '
                                'capture_output=True)\n', True, False),
    "round70-attribute-rebound": ('class R:\n    def m(self, repo):\n'
                                  '        self.env = {}\n'
                                  '        self.env["GIT_NO_REPLACE_OBJECTS"] = "1"\n'
                                  '        self.env = {}\n'
                                  '        return subprocess.run(["git", "show", "HEAD:a"], '
                                  'env=self.env)\n', True, False),
    "round70-attribute-after-use": ('class R:\n    def m(self, repo):\n'
                                   '        self.env = {}\n'
                                   '        subprocess.run(["git", "show", "HEAD:a"], '
                                   'env=self.env)\n'
                                   '        self.env["GIT_NO_REPLACE_OBJECTS"] = "1"\n',
                                   True, False),
    "round70-const-key-shadow": ('KEY = "GIT_NO_REPLACE_OBJECTS"\n\n\n'
                                 'def run(repo):\n    KEY = "OTHER"\n'
                                 '    env = {"PATH": "/usr/bin"}\n    env[KEY] = "1"\n'
                                 '    return subprocess.run(["git", "-C", repo, "show", "HEAD:a"], '
                                 'env=env)\n', True, False),
    "r71-dict-call-splat-widened": ('GUARD = {"GIT_NO_REPLACE_OBJECTS": "1"}\n\n\n'
                                'def run(repo):\n    env = dict(os.environ, **GUARD)\n'
                                '    return subprocess.run(["git", "show", "HEAD:a"], env=env)\n',
                                True, True),
    "round70-two-hop-alias": ('def run(repo):\n    base = {}\n    a = base\n    b = a\n'
                              '    b["GIT_NO_REPLACE_OBJECTS"] = "1"\n'
                              '    return subprocess.run(["git", "show", "HEAD:a"], env=base)\n',
                              True, False),
    "r71-store-through-alias-deeper-chain-stays-off": (
        'def run(repo):\n    e = {"PATH": "/usr/bin"}\n    staging = e\n'
        '    hop = staging\n    hop["GIT_NO_REPLACE_OBJECTS"] = "1"\n'
        '    return subprocess.run(["git", "show", "HEAD:a"], env=e)\n', True, False),
    "r71-store-alias-rebound-between": (
        'def run(repo):\n    e = {"PATH": "/usr/bin"}\n    staging = e\n'
        '    staging["GIT_NO_REPLACE_OBJECTS"] = "1"\n    staging = {}\n'
        '    return subprocess.run(["git", "show", "HEAD:a"], env=e)\n', True, False),
    "r71-splat-alias-rebound-before-splat": (
        'GUARD = {"GIT_NO_REPLACE_OBJECTS": "1"}\n'
        'def run(repo):\n    m = GUARD\n    m = {"LABEL": "x"}\n'
        '    env = {**os.environ, **m}\n'
        '    return subprocess.run(["git", "show", "HEAD:a"], env=env)\n', True, False),
    "r71-attribute-edge-after-use": (
        'class Box: pass\n'
        'cfg = Box()\n'
        'cfg.runner = Box()\n'
        'cfg.runner.env = {"PATH": "/usr/bin"}\n'
        'def run(repo):\n'
        '    runner = Box()\n'
        '    runner.env = {}\n'
        '    runner.env["GIT_NO_REPLACE_OBJECTS"] = "1"\n'
        '    subprocess.run(["git", "show", "HEAD:a"], env=cfg.runner.env)\n'
        '    cfg.runner = runner\n', True, False),
    "r71-attribute-edge-replacement-between": (
        'def run(repo):\n    runner.env = {}\n'
        '    runner.env["GIT_NO_REPLACE_OBJECTS"] = "1"\n    cfg.runner = runner\n'
        '    cfg.runner.env = {}\n'
        '    return subprocess.run(["git", "show", "HEAD:a"], env=cfg.runner.env)\n',
        True, False),
    "module-visible-binding": ('GIT_ENV = {"PATH": "/usr/bin"}\n'
                               'GIT_ENV["GIT_NO_REPLACE_OBJECTS"] = "1"\n\n\n'
                               'def head(repo):\n'
                               '    return subprocess.run(["git", "-C", repo, "show", "HEAD:a"], '
                               'env=GIT_ENV)\n', True, True),
    "r73-global-rebind-replaced-between": ('ENV = {"PATH": "/usr/bin"}\n'
                                        'def setup():\n    global ENV\n'
                                        '    ENV["GIT_NO_REPLACE_OBJECTS"] = "1"\n\n\n'
                                        'def reset():\n    global ENV\n    ENV = {}\n\n\n'
                                        'def run(repo):\n    setup()\n    reset()\n'
                                        '    subprocess.run(["git", "show", "HEAD:a"], env=ENV)\n',
                                        True, False),
    "r73-global-without-declaration": ('ENV = {"PATH": "/usr/bin"}\n'
                                       'def setup():\n    ENV = {}\n'
                                       '    ENV["GIT_NO_REPLACE_OBJECTS"] = "1"\n\n\n'
                                       'def run(repo):\n    setup()\n'
                                       '    subprocess.run(["git", "show", "HEAD:a"], env=ENV)\n',
                                       True, False),
    "r73-environ-dead-branch-store": ('def run(repo):\n    if False:\n'
                                      '        os.environ["GIT_NO_REPLACE_OBJECTS"] = "1"\n'
                                      '    subprocess.run(["git", "show", "HEAD:a"], env={**os.environ})\n',
                                      True, False),
    "r73-environ-extended-splat-is-the-held-carrier": (
        'GUARD = {"GIT_NO_REPLACE_OBJECTS": "1"}\n\n\ndef run(repo):\n'
        '    env = {**os.environ, **GUARD}\n'
        '    subprocess.run(["git", "show", "HEAD:a"], env=env)\n', True, True),
    "r73-global-parameter-shadow": ('ENV = {"PATH": "/usr/bin"}\n'
                                    'def setup():\n    global ENV\n'
                                    '    ENV["GIT_NO_REPLACE_OBJECTS"] = "1"\n\n\n'
                                    'def run(repo, ENV=None):\n    setup()\n'
                                    '    subprocess.run(["git", "show", "HEAD:a"], env=ENV)\n',
                                    True, False),
    "r73-global-unrelated-local-rebind": ('ENV = {"PATH": "/usr/bin"}\n'
                                         'def setup():\n    global ENV\n'
                                         '    ENV["GIT_NO_REPLACE_OBJECTS"] = "1"\n\n\n'
                                         'def unused():\n    ENV = {}\n    return ENV\n\n\n'
                                         'def run(repo):\n    setup()\n'
                                         '    subprocess.run(["git", "show", "HEAD:a"], env=ENV)\n',
                                         True, True),
    "r73-environ-key-deleted": ('def run(repo):\n'
                               '    os.environ["GIT_NO_REPLACE_OBJECTS"] = "1"\n'
                               '    del os.environ["GIT_NO_REPLACE_OBJECTS"]\n'
                               '    subprocess.run(["git", "show", "HEAD:a"], env=dict(os.environ))\n',
                               True, False),
    "r73-environ-call-with-extra-keyword": (
        'def run(repo):\n    os.environ["GIT_NO_REPLACE_OBJECTS"] = "1"\n'
        '    subprocess.run(["git", "show", "HEAD:a"], env=dict(os.environ, EXTRA="1"))\n',
        True, False),
}


def _selftest_checks(scratch, controls_path):
    checks = []

    def want(name, cond):
        checks.append((name, bool(cond)))

    want("the population regex accepts only top-level quality/check-*.py",
         bool(POPULATION_RE.match("quality/check-index.py"))
         and not POPULATION_RE.match("quality/counters/c2-r70-carriers.py")
         and not POPULATION_RE.match("quality/check-x/helper.py")
         and not POPULATION_RE.match("quality/notes.md"))
    want("the embedded classification table covers forty-seven cases", len(CASES) == 47)
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
    want("verdict met on the frozen target", verdict_met(20, 13, 13, 0, 47, 41))
    want("verdict requires the frozen population", not verdict_met(19, 13, 13, 0, 47, 41))
    want("verdict requires the frozen reader count", not verdict_met(20, 12, 12, 0, 47, 41))
    want("verdict requires the frozen guarded count", not verdict_met(20, 13, 12, 1, 47, 41))
    want("verdict requires no unguarded reader", not verdict_met(20, 13, 13, 1, 47, 41))
    want("verdict requires every control correct", not verdict_met(20, 13, 13, 0, 46, 41))
    want("verdict requires the frozen base-control score",
         not verdict_met(20, 13, 13, 0, 47, 47))

    good = contract_line(20, 13, 13, 0, 47, 41, "a" * 40)
    want("the frozen target prints the met line",
         good == ("MADO_R75_GUARD_SHAPES: population=20 readers=13 guarded=13 unguarded=0 "
                  "controls=47/47 base_controls=41/47 verdict=TARGET_MET rev=" + "a" * 40))
    want("the target line matches the frozen contract shape",
         CONTRACT_RE.fullmatch(good) is not None)
    want("contract line refuses a wrong verdict word",
         not CONTRACT_RE.fullmatch(
             "MADO_R75_GUARD_SHAPES: population=20 readers=13 guarded=13 unguarded=0 "
             "controls=36/36 base_controls=32/36 verdict=DONE rev=" + "a" * 40))

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
            want("the frozen controls file carries 47 cases", len(cases) == 47)
            want("the frozen controls file matches the pinned digest", True)
        except SetupError:
            want("the frozen controls file carries 36 cases", False)
            want("the frozen controls file matches the pinned digest", False)
    os.makedirs(scratch, exist_ok=True)
    tampered = os.path.join(scratch, "controls-tampered.json")
    try:
        os.unlink(tampered)
    except FileNotFoundError:
        pass
    fd = os.open(tampered, os.O_WRONLY | os.O_CREAT | os.O_TRUNC | os.O_NOFOLLOW, 0o600)
    with os.fdopen(fd, "w", encoding="utf-8") as fh:
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
            print("MADO_R75_GUARD_SHAPES_SELFTEST FAIL: %s" % name)
    print("MADO_R75_GUARD_SHAPES_SELFTEST: %d/%d assertions passed" % (passed, len(checks)))
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
