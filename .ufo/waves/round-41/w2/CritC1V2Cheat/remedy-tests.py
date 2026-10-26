#!/usr/bin/env python3
"""Test the remedies proposed in cheats.md against the cheats and the reference.

R1  b3 gains a semantics-preserving, AST-visible variant: every comparison with
    a dunder (==, !=, <, <=, >, >=, in, not in) becomes a method call, so the
    Compare-node set changes while behaviour does not.  A structural fingerprint
    (C13) must die; the honest reference must survive.
R2  imports_ok flags any Subscript/Attribute on __builtins__ (and any dynamic
    import reached through it), so C13's `ast`, C14's `exec` and C21's `_thread`
    are visible to clause g while the reference is untouched.
R3  a "same answer off the judge's diet" control: the same tool, same journal,
    once under the judge's env (HOME=/nonexistent, RLIMIT_NPROC=1) and once with
    a normal HOME and no limit.  C15 and C16 must differ; the reference must not.
"""
import ast
import importlib.util
import os
import shutil
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
LANE = os.path.abspath(os.path.join(HERE, "..", "..", "..", "..", ".."))
COUNTER = os.path.join(LANE, "quality", "counters", "c1-r41-globals-v2.py")
REF = os.path.join(LANE, ".ufo", "waves", "round-41", "c1",
                   "ctl-ref-tool-v2.py.txt")
spec = importlib.util.spec_from_file_location("c1v2", COUNTER)
M = importlib.util.module_from_spec(spec)
spec.loader.exec_module(M)
M.NONCE[0] = "c0ffee00deadbeef"
REV = "07f2641696b5ac73de1404ea737a9f27e9819aa1"

DUNDER = {ast.Eq: "__eq__", ast.NotEq: "__ne__", ast.Lt: "__lt__",
          ast.LtE: "__le__", ast.Gt: "__gt__", ast.GtE: "__ge__",
          ast.In: "__contains__", ast.NotIn: "__contains__"}


class R1(ast.NodeTransformer):
    """Semantics-preserving: `a OP b` -> `a.__op__(b)`; `a in b` -> `b.__contains__(a)`."""

    def visit_Compare(self, node):
        self.generic_visit(node)
        if len(node.ops) != 1 or type(node.ops[0]) not in DUNDER:
            return node
        op = node.ops[0]
        left, right = node.left, node.comparators[0]
        if isinstance(op, (ast.In, ast.NotIn)):
            left, right = right, left
        call = ast.Call(func=ast.Attribute(value=left, attr=DUNDER[type(op)],
                                           ctx=ast.Load()),
                        args=[right], keywords=[])
        if isinstance(op, ast.NotIn):
            return ast.copy_location(ast.UnaryOp(op=ast.Not(), operand=call),
                                     node)
        return ast.copy_location(call, node)


def r1(text):
    return ast.unparse(R1().visit(ast.parse(text)))


def selftest(text, tag, env):
    d = tempfile.mkdtemp(prefix="rem-" + tag + "-")
    path = os.path.join(d, "mado-globals.py")
    with open(path, "w") as fh:
        fh.write(text)
    try:
        p = subprocess.run([sys.executable, "-I", path, "--selftest"],
                           capture_output=True, text=True, env=env, cwd=d,
                           timeout=300)
    finally:
        shutil.rmtree(d, ignore_errors=True)
    m = M.re.search(r"MADO_GLOBALS_SELFTEST: (\d+)/(\d+) passed", p.stdout)
    k, n = (int(m.group(1)), int(m.group(2))) if m else (0, 0)
    return p.returncode, k, n, bool(m)


JUDGE_ENV = {"HOME": "/nonexistent", "PATH": "/usr/bin", "LC_ALL": "C"}
HOST_ENV = {"HOME": "/home/vgpnk", "PATH": "/usr/bin", "LC_ALL": "C"}


def remedy_r1():
    print("== R1: b3 variant that rewrites comparisons into dunder calls")
    ref = open(REF).read()
    for name, text in [("reference", ref),
                       ("c13", open(os.path.join(HERE,
                        "c13-ast-fingerprint.py")).read()),
                       ("c14", open(os.path.join(HERE,
                        "c14-exec-model.py")).read())]:
        before = selftest(text, "r1a", JUDGE_ENV)
        after = selftest(r1(text), "r1b", JUDGE_ENV)
        print("%-10s as-is rc=%s %d/%d | after R1 transform rc=%s %d/%d -> %s"
              % (name, before[0], before[1], before[2], after[0], after[1],
                 after[2], "CAUGHT" if (after[0] != 0 or not after[3]
                                        or after[1] != after[2]) else "survives"))


def r2_imports_ok(src):
    """M.imports_ok plus: no Subscript/Attribute on __builtins__."""
    try:
        tree = ast.parse(src)
    except SyntaxError:
        return False
    for node in ast.walk(tree):
        if isinstance(node, ast.Subscript) and isinstance(node.value, ast.Name) \
                and node.value.id in ("__builtins__", "builtins"):
            return False
        if isinstance(node, ast.Attribute) and isinstance(node.value, ast.Name) \
                and node.value.id in ("__builtins__", "builtins"):
            return False
    return M.imports_ok(src)


def remedy_r2():
    print("== R2: clause g flags Subscript/Attribute on __builtins__")
    ref = open(REF, "rb").read()
    print("%-28s current g=%d with R2 g=%d" % ("reference", M.imports_ok(ref),
                                               r2_imports_ok(ref.decode())))
    for name in sorted(os.listdir(HERE)):
        if not (name.startswith("c") and name.endswith(".py")):
            continue
        src = open(os.path.join(HERE, name), "rb").read()
        print("%-28s current g=%d with R2 g=%d" % (
            name, M.imports_ok(src), r2_imports_ok(src.decode())))


def remedy_r3():
    print("== R3: same tool, same journal, judge env vs normal env")
    j = (M.line(M.T1, "4242", "hyprland_focus_grab_manager_v1", 1) + "\n"
         + M.line(M.T1, "4242", "wl_seat", 3) + "\n").encode()
    tmp = tempfile.mkdtemp(prefix="rem-r3-")
    os.chmod(tmp, 0o755)
    try:
        d, fx, mark, jp, _ = M.prepare(tmp, "r3", j)
        tools = [("reference", open(REF).read())]
        for name in ("c15-home-backdoor.py", "c16-nproc-detect.py"):
            tools.append((name, open(os.path.join(HERE, name)).read()))
        for name, text in tools:
            td = os.path.join(tmp, M.opaque("t-" + name), "tool")
            os.makedirs(td)
            os.chmod(os.path.dirname(td), 0o755)
            os.chmod(td, 0o755)
            tool = os.path.join(td, "mado-globals.py")
            with open(tool, "w") as fh:
                fh.write(text)
            outs = {}
            for tag, nproc, env in (
                    ("judge", True, {"XDG_RUNTIME_DIR": "/run/user/1000"}),
                    ("host", False, {"XDG_RUNTIME_DIR": "/run/user/1000",
                                     "HOME": "/home/vgpnk"})):
                rc, out, err = M.run_sandboxed(
                    tool, d, ["--journal-file", jp],
                    os.path.join(fx, "bin") + ":/usr/bin",
                    ro=[os.path.dirname(tool)], rw=[mark], cwd=fx,
                    extra_env=env, timeout=120, nproc=nproc)
                outs[tag] = (rc, out.decode("utf-8", "replace"))
            same = outs["judge"] == outs["host"]
            print("%-24s judge_rc=%s host_rc=%s identical=%s" % (
                name, outs["judge"][0], outs["host"][0], int(same)))
            if not same:
                print("   judge_last=%r" % outs["judge"][1].splitlines()[-1][:110])
                print("   host_last =%r" % outs["host"][1].splitlines()[-1][:110])
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


if __name__ == "__main__":
    remedy_r1()
    remedy_r2()
    remedy_r3()
