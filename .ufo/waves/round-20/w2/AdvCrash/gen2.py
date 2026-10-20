#!/usr/bin/env python3
"""Batch 2: deep AST inside deferred bodies (def/lambda/class) — the shape
where 1f7f995 used iterative ast.walk but 28c6837 runs recursive scanners
(module_unsafe_names/update_bindings/eager_calls) via prepare_eval_calls."""
import json
import os
import sys

OUT = sys.argv[1]
os.makedirs(OUT, exist_ok=True)


def rec(name, arguments, idx=0):
    return {"type": "message", "timestamp": "t",
            "message": {"role": "assistant", "content": [
                {"type": "toolCall", "id": "c%d" % idx, "name": name,
                 "arguments": arguments}]}}


def ev(code, language="py", reset=None):
    a = {"code": code, "language": language}
    if reset is not None:
        a["reset"] = reset
    return rec("eval", a)


def write(name, records):
    with open(os.path.join(OUT, name + ".jsonl"), "w") as fh:
        for r in records:
            fh.write(json.dumps(r) + "\n")


D = 3000  # deep enough to trip default recursion (limit ~1000)

cases = {
    # --- deep expression inside a CALLED helper body (new-only expected) ---
    "deep_callsuffix_in_helper": ev(
        "def f():\n    x = a()" + "()" * D + "\nf()"),
    "deep_callsuffix_in_helper_uncalled": ev(
        "def f():\n    x = a()" + "()" * D),
    "deep_attrchain_in_helper": ev(
        "def f():\n    x = a" + ".b" * D + "\nf()"),
    "deep_binop_in_helper": ev(
        "def f():\n    x = " + "+".join("1" for _ in range(D)) + "\nf()"),
    "deep_list_in_helper": ev(
        "def f():\n    x = " + "[" * D + "1" + "]" * D + "\nf()"),
    "deep_paren_in_helper": ev(
        "def f():\n    x = " + "(" * D + "1" + ")" * D + "\nf()"),
    "deep_if_in_helper": ev(
        "def f():\n" + "".join("    " * (i + 1) + ("if x:\n" if i < 800 else "pass\n")
                               for i in range(800)) + "f()"),
    "deep_with_in_helper": ev(
        "def f():\n" + "".join("    " * (i + 1) +
                               ("with c():\n" if i < 600 else "pass\n")
                               for i in range(600)) + "f()"),
    "deep_try_in_helper": ev(
        "def f():\n" + "".join("    " * (i + 1) + "try:\n" for i in range(300)) +
        "    " * 301 + "pass\n" +
        "".join("    " * (300 - i) + "except E:\n" +
                "    " * (300 - i + 1) + ("try:\n" if i < 299 else "pass\n")
                for i in range(300)) + "f()"),
    "deep_stmt_nested_in_helper": ev(
        "def f():\n" + "".join("    " * (i + 1) +
                               ("for i in r:\n" if i < 900 else "pass\n")
                               for i in range(900)) + "f()"),
    "deep_match_in_helper": ev(
        "def f():\n    match x:\n" +
        "".join("        case [%d, *r%d]:\n            x = r%d\n" % (i, i, i)
                for i in range(400)) + "f()"),
    "deep_await_in_helper": ev(
        "async def f():\n    x = " + "await " * 600 + "g()\nawait f()"),
    "deep_walrus_in_helper": ev(
        "def f():\n    x = " + "(y := " * 600 + "1" + ")" * 600 + "\nf()"),
    "deep_tuple_target_in_helper": ev(
        "def f():\n    " + "(" * 600 + "x" + ",y)" * 600 + " = t\nf()"),

    # --- same shapes inside lambda body ---
    "deep_callsuffix_in_lambda": ev(
        "f = lambda: a()" + "()" * D + "\nf()"),
    "deep_attr_in_lambda": ev(
        "f = lambda: a" + ".b" * D + "\nf()"),
    "deep_lambda_body_uncalled": ev(
        "f = lambda: a()" + "()" * D),

    # --- inside class __init__ / methods ---
    "deep_callsuffix_in_init": ev(
        "class A:\n    def __init__(self):\n        x = a()" + "()" * D + "\nA()"),
    "deep_callsuffix_in_method": ev(
        "class A:\n    def m(self):\n        x = a()" + "()" * D + "\nA().m()"),
    "deep_attr_in_staticmethod": ev(
        "class A:\n    @staticmethod\n    def m():\n        x = a" + ".b" * D + "\nA.m()"),

    # --- cross-cell helper with deep body ---
    # (written below as multi-record)

    # --- nested inner def with deep body ---
    "deep_in_inner_def_called": ev(
        "def f():\n    def g():\n        x = a()" + "()" * D + "\n    g()\nf()"),

    # --- helper calling helper where inner has deep body ---
    "deep_body_via_chain": ev(
        "def inner():\n    x = a" + ".b" * D + "\n"
        "def outer():\n    inner()\nouter()"),

    # --- module-level deep inside class BODY (not method) ---
    "deep_expr_in_class_body": ev(
        "class A:\n    x = a()" + "()" * D),
    "deep_expr_in_class_body_called": ev(
        "class A:\n    x = a()" + "()" * D + "\nA()"),

    # --- quadratic-ish env/wrapper shells ---
    "env_wrapper_chain_20k": rec("bash", {"command": "env " * 20000 + "ls"}),
    "nohup_wrapper_chain_5k": rec("bash", {"command": "nohup " * 5000 + "ls"}),
    "exec_wrapper_chain_5k": rec("bash", {"command": "exec " * 5000 + "ls"}),

    # --- more malformed-but-parseable records ---
    "content_dict": {"type": "message", "message": {"role": "assistant",
        "content": {"type": "toolCall", "name": "bash",
                    "arguments": {"command": "sudo x"}}}},
    "content_item_list": {"type": "message", "message": {"role": "assistant",
        "content": [[{"type": "toolCall", "name": "bash",
                      "arguments": {"command": "sudo x"}}]]}},
    "toolcall_name_number": {"type": "message", "message": {"role": "assistant",
        "content": [{"type": "toolCall", "name": 7,
                     "arguments": {"command": "sudo x"}}]}},
    "toolcall_name_null": {"type": "message", "message": {"role": "assistant",
        "content": [{"type": "toolCall", "name": None,
                     "arguments": {"command": "sudo x"}}]}},
    "lang_list": ev("x=1", language=["py"]),
    "lang_dict": ev("x=1", language={"l": "py"}),
    "reset_with_nonstring_code": rec("eval", {"code": 5, "reset": True}),
    "float_inf_field": {"type": "message", "timestamp": 1e400,
        "message": {"role": "assistant", "content": [
            {"type": "toolCall", "name": "bash",
             "arguments": {"command": "ls"}}]}},
    "surrogate_escape": {"type": "message", "message": {"role": "assistant",
        "content": [{"type": "toolCall", "name": "bash",
                     "arguments": {"command": "echo \\ud800 x"}}]}},

    # --- mutual/deep helper shapes the new binder handles differently ---
    "helper_args_50_star": ev(
        "def f(*a):\n    subprocess.run(a)\n" +
        "f(" + ",".join("'x'" for _ in range(50)) + ")"),
    "helper_kwargs_50": ev(
        "def f(**k):\n    subprocess.run(k.get('c'))\n" +
        "f(" + ",".join("k%d='v'" % i for i in range(50)) + ",c=['pacman','-S','z'])"),
    "helper_recursive_kwarg_cycle": ev(
        "def f(n=0):\n    f(n=n)\nf()"),
    "two_helpers_mutual_kwarg": ev(
        "def a(x=0):\n    b(y=x)\ndef b(y=0):\n    a(x=y)\na()"),
    "partial_of_helper": ev(
        "import functools\ndef h(c):\n    subprocess.run(c)\n"
        "p = functools.partial(h, ['pacman','-S','z'])\np()"),
    "partial_of_partial": ev(
        "import functools, subprocess\n"
        "p = functools.partial(functools.partial, subprocess.run)\np()(['x'])"),
    "getattr_attr_call": ev(
        "import subprocess\ngetattr(subprocess, 'run')('pacman -S z', shell=True)"),
    "class_callable_instance": ev(
        "class A:\n    def __call__(self, c):\n        subprocess.run(c)\n"
        "A()(['pacman','-S','z'])"),
    "instance_call_no_dunder": ev(
        "class A:\n    pass\nA()(['x'])"),
    "method_on_call_result": ev(
        "def mk():\n    return A\nclass A:\n    def m(self):\n        subprocess.run(['x'])\nmk()().m()"),

    # --- deep JSON (valid line, deep structure) handled separately below ---
}

for name, r in cases.items():
    write(name, [r] if isinstance(r, dict) else r)

# multi-record cases
write("deep_helper_cross_cell", [
    ev("def f():\n    x = a()" + "()" * D),
    ev("f()")])
write("deep_helper_cross_cell_reset", [
    ev("def f():\n    x = a()" + "()" * D),
    ev("pass", reset=True),
    ev("f()")])

# deep JSON line: a well-formed JSON value nested 3000 deep
depth_json = "[" * 3000 + "]" * 3000
with open(os.path.join(OUT, "deep_json_line.jsonl"), "w") as fh:
    fh.write(depth_json + "\n")
# deep JSON inside arguments (line parses; code is small)
with open(os.path.join(OUT, "deep_json_arguments.jsonl"), "w") as fh:
    fh.write('{"type":"message","message":{"role":"assistant","content":'
             '[{"type":"toolCall","name":"bash","arguments":{"command":"ls",'
             '"deep":' + depth_json + '}}]}}\n')

print("batch2 done")
