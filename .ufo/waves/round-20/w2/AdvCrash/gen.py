#!/usr/bin/env python3
"""AdvCrash fixture generator: odd-but-parseable transcripts for mado-tripwire.

Every emitted line is a well-formed transcript record (dict with "type").
Cases target crash/exit-2 surfaces: recursion in AST walkers, unbounded
classify_segment chains, quadratic literal folding, weird record shapes.
Written once; the --scan target is the generated directory (never executed).
"""
import json
import os
import sys

OUT = sys.argv[1] if len(sys.argv) > 1 else "/tmp/advcrash-fixtures"
os.makedirs(OUT, exist_ok=True)


def rec(name, arguments, idx=0):
    item = {"type": "toolCall", "id": "c%d" % idx, "name": name,
            "arguments": arguments}
    return {"type": "message", "timestamp": "2026-10-20T00:00:00Z",
            "message": {"role": "assistant", "content": [item]}}


def bash(command, idx=0):
    return rec("bash", {"command": command, "i": "x"}, idx)


def ev(code, language="py", idx=0, reset=None):
    args = {"code": code, "language": language, "i": "x"}
    if reset is not None:
        args["reset"] = reset
    return rec("eval", args, idx)


def write(name, records):
    path = os.path.join(OUT, name + ".jsonl")
    with open(path, "w", encoding="utf-8") as fh:
        for r in records:
            fh.write(json.dumps(r) + "\n")
    return path


cases = []

# --- JS cells (language filter) -------------------------------------------
cases.append(("js_cell", [ev("const x = 1;\nrequire('child_process').exec('pacman -S z')",
                             language="js")]))
cases.append(("js_cell_no_lang_key", [ev("console.log(1)", language=None)]))
cases.append(("js_cell_weird_lang", [ev("x=1", language=123)]))
cases.append(("js_cell_bool_lang", [ev("x=1", language=True)]))

# --- reset cells -----------------------------------------------------------
cases.append(("reset_cell", [
    ev("import subprocess\nX=['pacman','-S','z']"),
    ev("subprocess.run(X)", reset=True),
    ev("subprocess.run(['pacman','-S','z'])", reset=True)]))
cases.append(("reset_nonbool", [ev("x=1"), ev("y=2", reset="yes")]))
cases.append(("reset_only", [ev("pass", reset=True)]))

# --- non-dict arguments / odd records --------------------------------------
cases.append(("args_list", [rec("bash", ["sudo", "rm", "-rf", "/"])]))
cases.append(("args_string", [rec("bash", "sudo rm -rf /")]))
cases.append(("args_null", [rec("bash", None)]))
cases.append(("args_number", [rec("eval", 42)]))
cases.append(("content_string", [
    {"type": "message", "message": {"role": "assistant",
                                    "content": "sudo pacman -S x"}}]))
cases.append(("content_null", [
    {"type": "message", "message": {"role": "assistant", "content": None}}]))
cases.append(("content_items_mixed", [
    {"type": "message", "message": {"role": "assistant",
        "content": [None, 42, "sudo rm", {"type": "toolCall", "name": "bash"},
                    {"type": "toolCall", "name": "bash",
                     "arguments": {"command": "ls"}}]}}]))
cases.append(("toolcall_no_args_key", [
    {"type": "message", "message": {"role": "assistant",
        "content": [{"type": "toolCall", "name": "bash"}]}}]))
cases.append(("toolcall_unknown_name", [
    rec("write", {"path": "/x", "content": "pacman -S y"})]))
cases.append(("message_not_dict", [
    {"type": "message", "message": "sudo pacman -S x"}]))
cases.append(("role_user_toolcall", [
    {"type": "message", "message": {"role": "user",
        "content": [{"type": "toolCall", "name": "bash",
                     "arguments": {"command": "pacman -S x"}}]}}]))
cases.append(("code_nonstring", [ev(12345), ev(None), ev(["ls"]), ev({"a": 1})]))
cases.append(("command_nonstring", [
    rec("bash", {"command": 123}), rec("bash", {"command": None}),
    rec("bash", {"command": ["sudo", "rm"]}),
    rec("bash", {"command": {"x": 1}})]))
cases.append(("nested_type_missing", [
    {"type": "message", "message": {"role": "assistant",
        "content": [{"name": "bash", "arguments": {"command": "sudo x"}}]}}]))
cases.append(("unicode_all", [
    bash("echo " + "\U0001f600" * 200 + "; ls"),
    ev("# " + "\u00e9" * 500 + "\nx = 'caf\u00e9'"),
    {"type": "message", "message": {"role": "assistant", "content": [
        {"type": "toolCall", "name": "bash", "id": None,
         "arguments": {"command": "ls \u2028 ok"}}]}}]))

# --- huge cells ------------------------------------------------------------
cases.append(("huge_bash_cmd", [bash("echo " + "a" * 2_000_000)]))
cases.append(("huge_eval_comment", [ev("# " + "z" * 2_000_000 + "\nx = 1")]))
cases.append(("huge_eval_list", [
    ev("subprocess.run(['ls'" + ",'-l'" * 200_000 + "])")]))
cases.append(("huge_string_concat_2k", [
    ev("cmd = " + " + ".join(['"a"'] * 2000) + "\nsubprocess.run(cmd)")]))
cases.append(("huge_string_concat_20k", [
    ev("cmd = " + " + ".join(['"a"'] * 20000) + "\nsubprocess.run(cmd)")]))
cases.append(("huge_env_calls", [
    ev("\n".join("v%d = 'x%d'" % (i, i) for i in range(500)) + "\n" +
       "\n".join("subprocess.run(v%d)" % i for i in range(500)))]))
cases.append(("huge_many_stmts", [
    ev("\n".join("x%d = %d" % (i, i) for i in range(50_000)))]))

# --- deep python nesting (AST walkers recurse) ------------------------------
cases.append(("deep_paren_expr_2k", [ev("x = " + "(" * 2000 + "1" + ")" * 2000)]))
cases.append(("deep_paren_expr_10k", [ev("x = " + "(" * 10000 + "1" + ")" * 10000)]))
cases.append(("deep_list_literal_2k", [
    ev("x = " + "[" * 2000 + "1" + "]" * 2000)]))
cases.append(("deep_call_chain_500", [
    ev("x = " + "f(" * 500 + "1" + ")" * 500)]))
cases.append(("deep_call_chain_5k", [
    ev("x = " + "f(" * 5000 + "1" + ")" * 5000)]))
cases.append(("deep_call_suffix_2k", [
    ev("x = f()" + "()" * 2000)]))
cases.append(("deep_attr_chain_5k", [
    ev("x = a" + ".b" * 5000)]))
cases.append(("deep_dict_2k", [
    ev("x = " + "".join('{"k%d":' % i for i in range(2000)) + "1" +
       "}" * 2000)]))
cases.append(("deep_binop_2k", [
    ev("x = " + "+".join("1" for _ in range(2000)))]))
cases.append(("deep_binop_50k", [
    ev("x = " + "+".join("1" for _ in range(50000)))]))
cases.append(("deep_if_nesting_500", [
    ev("\n".join("    " * i + "if x:" for i in range(500)))]))
cases.append(("deep_tuple_target_500", [
    ev("(" * 500 + "x" + ",y)" * 500 + " = " + "(" * 500 + "1,2" + ")" * 500)]))
cases.append(("deep_await_300", [ev("x = " + "await " * 300 + "f()")]))

# --- helper recursion shapes -----------------------------------------------
def helpers_chain(n, harmful=True):
    lines = []
    lines.append("def h0():\n    subprocess.run(['pacman','-S','z'])")
    for i in range(1, n):
        lines.append("def h%d():\n    h%d()" % (i, i - 1))
    lines.append("h%d()" % (n - 1))
    return "\n".join(lines)

cases.append(("helpers_50_deep", [ev(helpers_chain(50))]))
cases.append(("helpers_200_deep", [ev(helpers_chain(200))]))
cases.append(("helpers_50_cross_cell", [
    ev(helpers_chain(30)), ev(helpers_chain(25))]))
cases.append(("self_recursive", [
    ev("def f():\n    f()\nf()")]))
cases.append(("self_recursive_spawn", [
    ev("def f():\n    subprocess.run(['pacman','-S','z'])\n    f()\nf()")]))
cases.append(("mutual_recursion", [
    ev("def a():\n    b()\ndef b():\n    a()\na()")]))
cases.append(("mutual_recursion_spawn", [
    ev("def a():\n    b()\ndef b():\n    subprocess.run(['rm','-rf','/'])\n    a()\na()")]))
cases.append(("helper_50_breadth", [
    ev("def h():\n    pass\n" + "\n".join("h()" for _ in range(50)))]))
cases.append(("helper_shadowed", [
    ev("def f():\n    subprocess.run(['x'])\nf = 42\nf()")]))
cases.append(("helper_lambda_default", [
    ev("def f(g=lambda: subprocess.run(['pacman','-S','z'])):\n    g()\nf()")]))
cases.append(("helper_lambda_default_call", [
    ev("def f(g=lambda: subprocess.run(['pacman','-S','z'])):\n    g()\nf(g=lambda: subprocess.run(['rm','-rf','/']))")]))
cases.append(("lambda_self", [
    ev("f = lambda: f()\nf()")]))
cases.append(("lambda_in_default_of_lambda", [
    ev("f = lambda g=(lambda: subprocess.run(['x'])): g()\nf()")]))
cases.append(("class_init_self", [
    ev("class A:\n    def __init__(self):\n        A()\nA()")]))
cases.append(("class_init_spawn", [
    ev("class A:\n    def __init__(self):\n        subprocess.run(['pacman','-S','z'])\nA()")]))
cases.append(("class_method_chain_60", [
    ev("class A:\n" +
       "    def m0(self):\n        subprocess.run(['x'])\n" +
       "".join("    def m%d(self):\n        self.m%d()\n" % (i, i - 1)
               for i in range(1, 60)) +
       "A().m59()")]))
cases.append(("class_no_init_attr_call", [
    ev("class A:\n    def run(self, c):\n        subprocess.run(c)\n"
       "A().run(['pacman','-S','z'])")]))
cases.append(("async_helper_chain_60", [
    ev("import subprocess\n" +
       "async def a0():\n    subprocess.run(['x'])\n" +
       "".join("async def a%d():\n    await a%d()\n" % (i, i - 1)
               for i in range(1, 60)) +
       "await a59()")]))
cases.append(("async_helper_no_await", [
    ev("async def a():\n    subprocess.run(['pacman','-S','z'])\na()")]))

# --- syntax errors / weird python ------------------------------------------
cases.append(("syntax_error_mid", [
    ev("x = 1\nsubprocess.run(['pacman','-S','z'])\ndef broken(:\n")]))
cases.append(("syntax_error_only", [ev("def (((x")]))
cases.append(("nul_in_code", [ev("x = 'a\x00b'\nsubprocess.run(['ls'])")]))
cases.append(("tabs_indent_mix", [
    ev("def f():\n\tsubprocess.run(['x'])\nf()")]))
cases.append(("top_level_await", [
    ev("import subprocess\nawait subprocess.run(['pacman','-S','z'])")]))
cases.append(("await_in_async", [
    ev("import subprocess\nasync def m():\n    await subprocess.run(['x'])\nawait m()")]))
cases.append(("async_comprehension", [
    ev("async def f():\n    r = [x async for x in gen()]\n"
       "    return [await g(x) async for x in gen() if await h(x)]")]))
cases.append(("async_for_with", [
    ev("async def f():\n    async with ctx() as c:\n        async for i in c:\n"
       "            subprocess.run(['pacman','-S','z'])\nf()")]))
cases.append(("walrus_spawn", [
    ev("import subprocess\nif (cmd := ['pacman','-S','z']):\n"
       "    subprocess.run(cmd)")]))
cases.append(("walrus_in_call", [
    ev("import subprocess\nsubprocess.run((x := ['pacman','-S','z']))")]))
cases.append(("walrus_nested_200", [
    ev("x = " + "(y := " * 200 + "1" + ")" * 200)]))
cases.append(("match_stmt", [
    ev("import subprocess\nmatch cmd:\n"
       "    case ['pacman', *rest]:\n        subprocess.run(['pacman','-S','z'])\n"
       "    case str() as s:\n        subprocess.run([s])\n"
       "    case _:\n        pass")]))
cases.append(("match_star_binding", [
    ev("match argv:\n    case ['sudo', *rest]:\n        print(rest)")]))
cases.append(("match_class_pattern", [
    ev("match x:\n    case Point(x=a, y=b):\n        print(a, b)")]))
cases.append(("dict_unpack_call", [
    ev("def f(**kw):\n    subprocess.run(kw['a'])\nf(**{'a': ['pacman','-S','z']})")]))
cases.append(("dict_unpack_nonstr", [
    ev("def f(**kw):\n    pass\nf(**{1: 2})")]))
cases.append(("starred_in_call", [
    ev("def f(*a):\n    subprocess.run(a)\nf(*['pacman','-S','z'])")]))
cases.append(("starred_dict_kwargs", [
    ev("import subprocess\nkw = {'shell': True}\nsubprocess.run('pacman -S z', **kw)")]))
cases.append(("double_star_lit", [
    ev("def f(**k):\n    subprocess.run(['rm','-rf','/'])\nf(**{'x': 1})")]))
cases.append(("posonly_kwonly", [
    ev("def f(a, /, b, *, c):\n    subprocess.run(a)\nf(['pacman','-S','z'], 2, c=3)")]))
cases.append(("too_many_args", [
    ev("def f(a):\n    subprocess.run(['x'])\nf(1, 2, 3)")]))
cases.append(("dupe_kwarg", [
    ev("def f(a):\n    subprocess.run(['x'])\nf(1, a=2)")]))
cases.append(("helper_defaults_later", [
    ev("def f(a, b='pacman -S z'):\n    subprocess.run(b)\nf('x')")]))
cases.append(("namedtuple_field", [
    ev("import collections\nP = collections.namedtuple('P', 'a')\n"
       "P(['pacman','-S','z'])")]))
cases.append(("partial_spawn", [
    ev("import functools, subprocess\nr = functools.partial(subprocess.run, 'sudo x')\nr()")]))
cases.append(("partial_spawn_kwargs", [
    ev("import functools, subprocess\n"
       "r = functools.partial(subprocess.run, shell=True)\nr('pacman -S z')")]))
cases.append(("getattr_call", [
    ev("import subprocess\ngetattr(subprocess, 'run')(['pacman','-S','z'])")]))
cases.append(("import_star", [
    ev("from subprocess import *\nrun(['pacman','-S','z'])")]))
cases.append(("import_star_mid", [
    ev("import subprocess\nfrom subprocess import *\nX = ['pacman','-S','z']\nrun(X)")]))
cases.append(("exec_in_cell", [
    ev("X = ['pacman','-S','z']\nexec('Y=1')\nsubprocess.run(X)")]))
cases.append(("globals_call", [
    ev("X = 'ls'\nglobals()\nsubprocess.run([X])")]))
cases.append(("del_builtin", [
    ev("import subprocess\ndel subprocess\nsubprocess.run(['x'])")]))
cases.append(("rebind_pure_name", [
    ev("print = lambda a: subprocess.run(a)\nprint(['pacman','-S','z'])")]))
cases.append(("frozenset_block_r19", [
    ev("BLOCK = frozenset(['pacman','-Q','hyprland'])")]))
cases.append(("frozenset_block_then_use", [
    ev("BLOCK = frozenset(['pacman','-Q','hyprland'])\nsubprocess.run(BLOCK)")]))
cases.append(("shadow_subprocess_var", [
    ev("subprocess = None\nsubprocess.run(['pacman','-S','z'])")]))
cases.append(("fstring_spawn", [
    ev("import subprocess\nsubprocess.run(f'pacman -S z')")]))
cases.append(("multiline_call", [
    ev("import subprocess\nsubprocess.run(\n    ['pacman',\n     '-S',\n     'z'\n    ]\n)")]))

# --- shell-side recursion / pathological -----------------------------------
cases.append(("sudo_chain_1500", [bash("sudo " * 1500 + "pacman -S z")]))
cases.append(("sudo_chain_20", [bash("sudo " * 20 + "pacman -S z")]))
cases.append(("eval_chain_1000", [bash("eval " * 1000 + "ls")]))
cases.append(("bash_c_chain_200", [
    bash("bash -c " + "'bash -c " * 60 + "ls" + "'" * 60)]))
cases.append(("su_c_chain", [
    bash("su -c " + "'su -c " * 40 + "ls" + "'" * 40)]))
cases.append(("systemd_run_chain", [
    bash("systemd-run " * 300 + "ls")]))
cases.append(("python_m_chain", [
    bash("python -m " + "python -m " * 200 + "sys")]))
cases.append(("huge_tokens", [bash(" ".join(["a"] * 200_000))]))
cases.append(("huge_segments", [bash(";".join(["ls"] * 50_000))]))
cases.append(("deep_subst_20", [bash("echo " + "$(" * 20 + "ls" + ")" * 20)]))
cases.append(("unbalanced_quotes", [bash("echo 'unterminated")]))
cases.append(("heredoc_unterminated", [bash("cat <<EOF\npacman -S z\n")]))
cases.append(("heredoc_shell_feed", [
    bash("bash <<EOF\npacman -S z\nEOF")]))
cases.append(("control_chars", [bash("echo \x01\x02\x7f; ls \x00 done")]))

# --- mixed / adversarial record order --------------------------------------
cases.append(("cell_order_reset", [
    ev("X = ['pacman','-S','z']"),
    ev("subprocess.run(X)"),
    ev("pass", reset=True),
    ev("subprocess.run(X)")]))
cases.append(("js_then_py_env", [
    ev("let X = 1", language="js"),
    ev("X = ['rm','-rf','/']\nsubprocess.run(X)")]))
cases.append(("empty_code", [ev(""), ev("   "), ev("\n\n")]))
cases.append(("empty_command", [bash(""), bash("   ")]))
cases.append(("only_toolresult", [
    {"type": "message", "message": {"role": "tool",
        "content": [{"type": "toolResult", "text": "pacman -S x"}]}}]))
cases.append(("duplicate_cells", [ev("x = 'ls'")] * 100))

# odd JSON primitives inside message
cases.append(("timestamp_weird", [
    {"type": "message", "timestamp": 12345, "message": {"role": "assistant",
        "content": [{"type": "toolCall", "name": "bash",
                     "arguments": {"command": "ls"}}]}},
    {"type": "message", "timestamp": None, "message": {"role": "assistant",
        "content": [{"type": "toolCall", "name": "bash",
                     "arguments": {"command": "ls"}}]}},
    {"type": "message", "timestamp": ["x"], "message": {"role": "assistant",
        "content": [{"type": "toolCall", "name": "bash",
                     "arguments": {"command": "ls"}}]}}]))

paths = []
for name, records in cases:
    paths.append(write(name, records))
print("wrote %d fixtures to %s" % (len(paths), OUT))
