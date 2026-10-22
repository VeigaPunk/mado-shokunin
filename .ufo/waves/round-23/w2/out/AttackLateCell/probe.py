#!/usr/bin/env python3
"""Scratch probe: author candidate fixtures, derive truth with the repair
truth.py CHILD (recording fake subprocess), scan with base and tip."""
import json, runpy, subprocess, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
LANE = Path("/home/vgpnk/Projects/shokunin/mado-shokunin")
BASE = HERE / "base/tool.py"
TIP = HERE / "tool.py"
TRUTH = runpy.run_path(str(LANE / ".ufo/waves/round-23/repair/truth.py"), run_name="truth_mod")
CHILD, safe = TRUTH["CHILD"], TRUTH["safe"]
scan = runpy.run_path(str(LANE / ".ufo/waves/round-21/oracle/measure.py"), run_name="oracle_mod")["scan"]


def q(tag):
    return '["pacman", "-Q", "r23w2-%s"]' % tag


def s(tag):
    return '["pacman", "-S", "r23w2-%s"]' % tag


CASES = {
"LateEnclosingLocalBeforeCall": f"""import subprocess
def outer():
    argv = {s('early-cell')}
    def inner():
        subprocess.run(argv)
    argv = {q('late-cell')}
    inner()
outer()
""",
"LateEnclosingLocalViaRelay": f"""import subprocess
def outer():
    argv = {s('early-cell')}
    def inner():
        subprocess.run(argv)
    def relay():
        argv = {s('relay-foreign')}
        inner()
    argv = {q('late-cell')}
    relay()
outer()
""",
"NonlocalRebindInSibling": f"""import subprocess
def outer():
    argv = {s('before-nonlocal')}
    def inner():
        subprocess.run(argv)
    def rebind():
        nonlocal argv
        argv = {q('after-nonlocal')}
    rebind()
    inner()
outer()
""",
"NonlocalRebindInNestedSetter": f"""import subprocess
def outer():
    argv = {s('before-setter')}
    def inner():
        def setter():
            nonlocal argv
            argv = {q('after-setter')}
        setter()
        subprocess.run(argv)
    inner()
outer()
""",
"LoopClosureCalledAfterLoop": f"""import subprocess
def outer():
    for argv in ({s('loop-first')}, {q('loop-last')}):
        def cb():
            subprocess.run(argv)
    cb()
outer()
""",
"ModuleLoopClosureCalledAfterLoop": f"""import subprocess
for argv in ({s('mloop-first')}, {q('mloop-last')}):
    def cb():
        subprocess.run(argv)
cb()
""",
"LoopClosuresCollectedThenCalled": f"""import subprocess
def outer():
    cbs = []
    for argv in ({s('coll-first')}, {q('coll-last')}):
        def cb():
            subprocess.run(argv)
        cbs.append(cb)
    for cb in cbs:
        cb()
outer()
""",
"FactoryLocalRebindBeforeReturn": f"""import subprocess
def make():
    argv = {s('factory-early')}
    def run():
        subprocess.run(argv)
    argv = {q('factory-late')}
    return run
make()()
""",
"FactoryTwoInvocationsFirstCalled": f"""import subprocess
def make(argv):
    def run():
        subprocess.run(argv)
    return run
first = make({q('first-frame')})
second = make({s('second-frame')})
first()
""",
"OuterTwoCallsNestedCallsLate": f"""import subprocess
def outer(argv):
    def inner():
        subprocess.run(argv)
    return inner
def relay(cb, argv):
    cb()
relay(outer({q('cell-one')}), {s('relay-arg')})
""",
"LateEnclosingLocalAfterFirstCall": f"""import subprocess
def outer():
    argv = {q('cell-a')}
    def inner():
        subprocess.run(argv)
    inner()
    argv = {q('cell-b')}
    inner()
outer()
""",
"RebindInsideLoopBodyAfterDef": f"""import subprocess
def outer():
    argv = {s('pre-loop')}
    def inner():
        subprocess.run(argv)
    for argv in ({q('loop-bound')},):
        pass
    inner()
outer()
""",
"NonlocalRebindThenCallInSibling": f"""import subprocess
def outer():
    argv = {s('before-nonlocal')}
    def inner():
        subprocess.run(argv)
    def rebind_and_call():
        nonlocal argv
        argv = {q('after-nonlocal')}
        inner()
    rebind_and_call()
outer()
""",
"ForwarderNonlocalRebindsThenCalls": f"""import subprocess
def outer():
    argv = {s('before-forward')}
    def inner():
        subprocess.run(argv)
    def forward(cb):
        nonlocal argv
        argv = {q('after-forward')}
        cb()
    forward(inner)
outer()
""",
"CallerGlobalDeclRebindsHelperGlobal": f"""import subprocess
argv = {s('module-early')}
def helper():
    subprocess.run(argv)
def caller():
    global argv
    argv = {q('module-late')}
    helper()
caller()
""",
"SecondFrameInvokesFirstFrameClosure": f"""import subprocess
def noop():
    pass
def outer(argv, cb):
    def inner():
        subprocess.run(argv)
    cb()
    return inner
first = outer({q('first-invocation')}, noop)
outer({s('second-invocation')}, first)
""",
"WalrusRebindSameStatement": f"""import subprocess
def outer():
    argv = {s('pre-walrus')}
    def inner():
        subprocess.run(argv)
    [argv := {q('walrus')}, inner()]
outer()
""",
"LateRebindForwardedClosure": f"""import subprocess
def outer():
    argv = {s('early-forwarded')}
    def inner():
        subprocess.run(argv)
    def forward(cb):
        cb()
    argv = {q('late-forwarded')}
    forward(inner)
outer()
""",
"LoopDirectRun": f"""import subprocess
for argv in ({q('direct-first')}, {q('direct-last')}):
    subprocess.run(argv)
""",
"LoopDefCalledInsideLoop": f"""import subprocess
def outer():
    for argv in ({q('inloop-first')}, {q('inloop-last')}):
        def cb():
            subprocess.run(argv)
        cb()
outer()
""",
"LoopBodyDefConstantCalledAfter": f"""import subprocess
for n in (1, 2):
    def cb():
        subprocess.run({q('const-after-loop')})
cb()
""",
"LoopRebindsLocalClosureCalledAfter": f"""import subprocess
def outer():
    argv = {s('pre-loop-local')}
    def cb():
        subprocess.run(argv)
    for n in (1, 2):
        argv = {q('loop-assigned')}
    cb()
outer()
""",
"SecondFrameRelayInvokesFirstClosure": f"""import subprocess
def noop():
    pass
def outer(argv, cb):
    def inner():
        subprocess.run(argv)
    def relay():
        cb()
    relay()
    return inner
first = outer({q('first-relay')}, noop)
outer({s('second-relay')}, first)
""",
"IfRebindsEnclosingBeforeCall": f"""import subprocess
def outer(flag):
    argv = {s('pre-if')}
    def inner():
        subprocess.run(argv)
    if flag:
        argv = {q('if-bound')}
    inner()
outer(True)
""",
"IfBodyDefConstant": f"""import subprocess
if True:
    def cb():
        subprocess.run({q('if-body-def')})
cb()
""",
"TryBodyDefConstant": f"""import subprocess
try:
    def cb():
        subprocess.run({q('try-body-def')})
finally:
    pass
cb()
""",
"WhileBodyDefConstant": f"""import subprocess
n = 0
while n < 1:
    def cb():
        subprocess.run({q('while-body-def')})
    n = 1
cb()
""",
}


def record(name, code):
    return json.dumps({"type": "message", "message": {"role": "assistant", "content": [
        {"type": "toolCall", "name": "eval", "id": name + "-0",
         "arguments": {"language": "py", "reset": False, "code": code}}]}})


def rows(got):
    payload = got.get("payload", {}) or {}
    unparsed = sum(r.get("eval_unparsed", 0) + r.get("unparsed_spawns", 0) for r in payload.get("files", []))
    return sorted({(r.get("class"), r.get("command"), r.get("evidence")) for r in payload.get("findings", [])}), unparsed


def main(outdir, names):
    outdir = Path(outdir)
    (outdir / "fixtures").mkdir(parents=True, exist_ok=True)
    report = []
    for name in names:
        code = CASES[name]
        assert safe(code), name
        path = outdir / "fixtures" / (name + ".jsonl")
        path.write_text(record(name, code) + "\n")
        p = subprocess.run([sys.executable, "-I", "-S", "-c", CHILD], input=code,
                           capture_output=True, text=True, timeout=15)
        assert p.returncode == 0, p.stderr
        executed = sorted(set(json.loads(p.stdout)))
        out = dict(id=name, executed=executed)
        for label, tool in (("base", BASE), ("tip", TIP)):
            got = scan(tool, path)
            r, u = rows(got)
            out[label] = dict(exit=got.get("exit"), error=got.get("error"), unparsed=u, rows=r)
        report.append(out)
    print(json.dumps(report, indent=1))


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2:] or list(CASES))
