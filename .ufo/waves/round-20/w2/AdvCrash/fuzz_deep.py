#!/usr/bin/env python3
"""Deep-structure sweep: one deep construct per case, inside a called helper
(new code path) and at module level (shared path). Compares both revisions."""
import sys

sys.setrecursionlimit(100000)
NEW = {'__name__': 'new'}
exec(compile(open('/tmp/tw-28c6837.py').read(), 'tw28', 'exec'), NEW)
OLD = {'__name__': 'old'}
exec(compile(open('/tmp/tw-1f7f995.py').read(), 'tw1f7', 'exec'), OLD)

D = 800

shapes = {
    "attr_chain": "a" + ".b" * D,
    "call_suffix": "a()" + "()" * D,
    "call_prefix": "f(" * D + "1" + ")" * D,
    "binop_add": "+".join("1" for _ in range(D)),
    "binop_mixed": "+".join("'s'" if i % 2 else "1" for i in range(D)),
    "list_nest": "[" * D + "1" + "]" * D,
    "tuple_nest": "(" * D + "1," + "1," * (D - 1) + ")" * D,
    "paren_nest": "(" * D + "1" + ")" * D,
    "dict_nest": "".join("{0:" for _ in range(D)) + "1" + "}" * D,
    "set_nest": "{1}",  # sets can't nest; placeholder
    "subscript": "a" + "[0]" * D,
    "await_chain": "await " * D + "g()",
    "unary": "-" * D + "1",
    "not_chain": "not " * D + "x",
    "starred_list": "[" + "*a," * D + "1]",
    "cond_expr": "1 " + "if x else 1 " * D + "if x else 2" + " else 3" * 0,
    "lambda_nest": "".join("(lambda x: " for _ in range(300)) + "x" + ")(1)" * 300,
    "compare_chain": " < ".join("x" for _ in range(D)),
    "fstring_parts": "f'" + "{x}" * D + "'",
    "slice_nest": "a" + "[::2]" * D,
    "attr_call_mix": "".join(".m()" for _ in range(D)),
}

# statement-level deep shapes
stmt_shapes = {
    "if_nest": lambda d: "".join("    " * i + "if x:\n" for i in range(d)) + "    " * d + "pass",
    "for_nest": lambda d: "".join("    " * i + "for i in r:\n" for i in range(d)) + "    " * d + "pass",
    "while_nest": lambda d: "".join("    " * i + "while x:\n" for i in range(d)) + "    " * d + "pass",
    "with_nest": lambda d: "".join("    " * i + "with c():\n" for i in range(d)) + "    " * d + "pass",
    "try_nest": lambda d: "".join("    " * i + "try:\n" for i in range(d)) +
        "    " * d + "pass\n" + "".join(
            "    " * (d - 1 - i) + "except:\n" + "    " * (d - i) +
            ("try:\n" if i < d - 1 else "pass\n") for i in range(d)),
    "elif_chain": lambda d: "if x:\n    pass\n" + "".join(
        "elif y:\n    pass\n" for _ in range(d)) + "else:\n    pass",
    "match_case_nest": lambda d: "match x:\n" + "".join(
        "    case [%d, *r]:\n        pass\n" % i for i in range(d)),
    "tuple_target": lambda d: "(" * d + "x" + ",y)" * d + " = t",
    "assign_chain": lambda d: "x" + " = y" * 0 + " = ".join("n%d" % i for i in range(d)) + " = 1",
}


def run(fn, code):
    try:
        if fn is NEW["classify_eval"]:
            fn(code, "py", {}, {})
        else:
            fn(code, "py", {})
        return "ok"
    except RecursionError:
        return "recursion"
    except BaseException as e:
        return "exc:%s" % type(e).__name__


def scan(code, label):
    rn = run(NEW["classify_eval"], code)
    ro = run(OLD["classify_eval"], code)
    flag = ""
    if rn != "ok" and ro == "ok":
        flag = "  <<< NEW-ONLY"
    elif rn != ro:
        flag = "  <<< DIFF"
    if rn != "ok" or ro != "ok":
        print("%-38s new=%-10s old=%-10s%s" % (label, rn, ro, flag))


for name, ex in shapes.items():
    scan("def f():\n    x = %s\nf()" % ex, "helper_expr/%s" % name)
for name, gen in stmt_shapes.items():
    try:
        body = gen(300)
    except Exception as e:
        print("%s gen error %s" % (name, e))
        continue
    indented = "\n".join("    " + ln for ln in body.split("\n"))
    scan("def f():\n%s\nf()" % indented, "helper_stmt/%s" % name)

# module level for reference on a few
for name in ("attr_chain", "call_suffix", "binop_add"):
    scan("x = %s" % shapes[name], "module_expr/%s" % name)

# misc non-recursion probes
probes = {
    "from_dot_import": "from . import x\nx()",
    "from_dotdot_import": "from .. import x\nx()",
    "import_no_alias_deep": "import a.b.c.d\na.b.c.d.run(['x'])",
    "conditional_helper": "if True:\n    def f():\n        subprocess.run(['x'])\nf()",
    "helper_in_try": "try:\n    def f():\n        subprocess.run(['x'])\nexcept E:\n    pass\nf()",
    "helper_in_for": "for i in [1]:\n    def f():\n        subprocess.run(['x'])\nf()",
    "class_kwarg_helper": "def f(**k):\n    subprocess.run(k['c'])\nf(**{'c': ['x']})",
    "call_kwarg_none": "def f(**k):\n    pass\nf(**x)",
    "posonly_kw": "def f(a, /):\n    subprocess.run(a)\nf(a=['x'])",
    "kwonly_no_default": "def f(*, a):\n    subprocess.run(a)\nf()",
    "self_named_param": "class A:\n    def m(self):\n        subprocess.run(self)\nA().m()",
    "nested_class_method": "class A:\n    class B:\n        def m(self):\n            subprocess.run(['x'])\nA.B().m()",
    "method_via_instance_var": "class A:\n    def m(self, c):\n        subprocess.run(c)\n"
                             "a = A()\na.m(['pacman','-S','z'])",
    "decorated_helper": "@deco\ndef f():\n    subprocess.run(['x'])\nf()",
    "async_for_in_helper": "async def f():\n    async for i in g():\n        subprocess.run(['x'])\nawait f()",
    "yield_in_helper": "def f():\n    yield subprocess.run(['x'])\nnext(f())",
    "helper_returning_helper": "def out():\n    def inn():\n        subprocess.run(['x'])\n    return inn\nout()()",
    "closure_var": "def out():\n    c = ['x']\n    def inn():\n        subprocess.run(c)\n    inn()\nout()",
    "walrus_helper_arg": "def f(c):\n    subprocess.run(c)\nf(c := ['x'])",
    "star_call_on_helper": "def f(*a):\n    subprocess.run(a)\nf(*['x'])",
    "double_star_call": "def f(**k):\n    subprocess.run(k)\nf(**{'a':1})",
    "import_in_helper": "def f():\n    import subprocess\n    subprocess.run(['x'])\nf()",
    "global_rebind_in_helper": "X = 'ls'\ndef f():\n    global X\n    X = 'rm'\nf()\nsubprocess.run([X])",
    "nonlocal_in_helper": "def out():\n    c = ['x']\n    def inn():\n        nonlocal c\n        subprocess.run(c)\n    inn()\nout()",
    "type_alias_stmt": "type X = list[int]",
    "match_seq_capture": "match x:\n    case [a, b, *rest]:\n        subprocess.run(rest)",
    "match_or_pattern": "match x:\n    case 'a' | 'b':\n        pass",
    "match_guard": "match x:\n    case a if a:\n        pass",
    "match_class_kw": "match x:\n    case P(y=b):\n        pass",
    "await_subprocess_exec": "import asyncio\nawait asyncio.create_subprocess_exec('pacman','-S','z')",
    "os_execv": "import os\nos.execv('/bin/sh', ['sh', '-c', 'pacman -S z'])",
    "os_spawnlp": "import os\nos.spawnlp(os.P_WAIT, 'pacman', '-S', 'z')",
    "tool_bash_dict": "tool.bash({'command': 'pacman -S z'})",
    "tool_bash_nonstr": "tool.bash({'command': 5})",
    "tool_bash_var": "tool.bash({'command': cmd})",
    "sp_alias": "import subprocess as sp\nsp.run(['pacman','-S','z'])",
    "sp_bare": "sp.run(['pacman','-S','z'])",
    "run_alias": "from subprocess import run\nrun(['pacman','-S','z'])",
    "partial_kwarg_shell": "import functools, subprocess\n"
                           "functools.partial(subprocess.run, shell=True)('ls')",
    "namedtuple_named": "import collections\nT = collections.namedtuple('T','a')\nT(['x'])",
    "lambda_default_called": "f = lambda g=lambda: subprocess.run(['x']): g()\nf()",
    "helper_kw_default_lambda": "def f(g=lambda: 1):\n    g()\nf()",
    "deep_args_count": "def f(*a):\n    pass\nf(" + ",".join("1" for _ in range(500)) + ")",
    "huge_kwargs": "def f(**k):\n    pass\nf(" + ",".join("k%d=1" % i for i in range(500)) + ")",
}
for name, code in probes.items():
    scan(code, "probe/%s" % name)
print("done")
