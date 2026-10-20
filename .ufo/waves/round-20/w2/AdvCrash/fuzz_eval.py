#!/usr/bin/env python3
"""Grammar fuzzer: call classify_eval/classify_shell of both tool revisions
in-process (source exec'd, never the transcript code) and diff exceptions.
Any non-RecursionError exception or new-only RecursionError is a candidate.
"""
import random
import sys

sys.setrecursionlimit(10000)  # let RecursionError surface deep, not at fuzzer frames

NEW = {'__name__': 'new'}
exec(compile(open('/tmp/tw-28c6837.py').read(), 'tw28', 'exec'), NEW)
OLD = {'__name__': 'old'}
exec(compile(open('/tmp/tw-1f7f995.py').read(), 'tw1f7', 'exec'), OLD)

random.seed(20261020)

NAMES = ["a", "b", "c", "f", "g", "h", "subprocess", "os", "sp", "print",
         "tool", "asyncio", "X", "run", "Popen"]
STRS = ["'x'", "'pacman -S z'", "'-l'", "''", '"cmd"', "f'v{n}'", "b'b'"]


def expr(d):
    if d <= 0:
        return random.choice(NAMES + STRS + ["1", "None", "True", "[]", "['x','y']"])
    k = random.randrange(14)
    if k == 0:
        return "%s(%s)" % (expr(d - 1), ", ".join(expr(d - 1) for _ in range(random.randrange(3))))
    if k == 1:
        return "%s.%s" % (expr(d - 1), random.choice(["run", "x", "m", "Popen"]))
    if k == 2:
        return "[%s]" % ", ".join(expr(d - 1) for _ in range(random.randrange(3)))
    if k == 3:
        return "{%s: %s}" % (expr(d - 1), expr(d - 1))
    if k == 4:
        return "%s + %s" % (expr(d - 1), expr(d - 1))
    if k == 5:
        return "lambda %s: %s" % (random.choice(NAMES[:3]), expr(d - 1))
    if k == 6:
        return "(%s if %s else %s)" % (expr(d - 1), expr(d - 1), expr(d - 1))
    if k == 7:
        return "[%s for %s in %s]" % (expr(d - 1), random.choice(NAMES[:3]), expr(d - 1))
    if k == 8:
        return "*%s" % expr(d - 1)
    if k == 9:
        return "%s[%s]" % (expr(d - 1), expr(d - 1))
    if k == 10:
        return "%s(**%s)" % (expr(d - 1), expr(d - 1))
    if k == 11:
        return "%s(%s=%s)" % (expr(d - 1), random.choice(NAMES[:3]), expr(d - 1))
    if k == 12:
        return "await %s" % expr(d - 1)
    return "(%s)" % expr(d - 1)


def stmt(d):
    k = random.randrange(15)
    if k == 0:
        return "%s = %s" % (random.choice(NAMES), expr(d))
    if k == 1:
        return "def %s(%s):\n    %s" % (
            random.choice(NAMES[:3]),
            ", ".join(random.sample(NAMES[:3], random.randrange(3))),
            stmt(d - 1) if d else "pass")
    if k == 2:
        return "async def %s():\n    %s" % (random.choice(NAMES[:3]), stmt(d - 1) if d else "pass")
    if k == 3:
        return "class %s:\n    %s" % (random.choice(["A", "B", "C"]),
                                      stmt(d - 1) if d else "pass")
    if k == 4:
        return "import %s" % random.choice(["subprocess", "os", "asyncio", "functools",
                                            "subprocess as sp", "os.path"])
    if k == 5:
        return "from %s import %s" % (random.choice(["subprocess", "os", "functools", "."]),
                                      random.choice(["run", "*", "Popen", "partial"]))
    if k == 6:
        return "if %s:\n    %s" % (expr(1), stmt(d - 1) if d else "pass")
    if k == 7:
        return "for %s in %s:\n    %s" % (random.choice(NAMES[:3]), expr(1),
                                          stmt(d - 1) if d else "pass")
    if k == 8:
        return "try:\n    %s\nexcept E as %s:\n    %s" % (
            stmt(d - 1) if d else "pass", random.choice(NAMES[:3]),
            stmt(d - 1) if d else "pass")
    if k == 9:
        return "with %s as %s:\n    %s" % (expr(1), random.choice(NAMES[:3]),
                                           stmt(d - 1) if d else "pass")
    if k == 10:
        return "match %s:\n    case %s:\n        %s" % (
            expr(1), random.choice(["[x, *rest]", "str() as s", "_", "Point(x=a)"]),
            stmt(d - 1) if d else "pass")
    if k == 11:
        return "%s" % expr(d)
    if k == 12:
        return "del %s" % random.choice(NAMES)
    if k == 13:
        return "while %s:\n    %s" % (expr(1), stmt(d - 1) if d else "pass")
    return "global %s" % random.choice(NAMES[:3])


def cell():
    return "\n".join(stmt(random.randrange(1, 4)) for _ in range(random.randrange(1, 5)))


SHELL_BITS = ["sudo ", "doas ", "env ", "nohup ", "exec ", "time ", "eval ",
              "bash -c 'x' ", "su -c 'x' ", "systemd-run ", "stdbuf -o0 ",
              "VAR=1 ", "command -v ls ", "xargs ", "find . -exec "]
WORDS = ["pacman -S z", "ls", "git add .", "jj new", "uv tool install x",
         "pip install y", "systemctl restart x", "hyprctl reload", "kill -9 1",
         "omarchy-thing", "python -m pip install z", "cargo install q",
         "$(ls)", "`id`", "| sh", "&& rm -rf /", "; cat /etc/passwd"]


def shcell():
    n = random.randrange(1, 8)
    parts = []
    for _ in range(n):
        if random.randrange(3):
            parts.append(random.choice(WORDS))
        else:
            parts.append(random.choice(SHELL_BITS) + random.choice(WORDS))
    return " ".join(parts)


def run(fn, *a):
    try:
        return ("ok", fn(*a))
    except RecursionError:
        return ("recursion", None)
    except BaseException as e:
        return ("exc:%s:%s" % (type(e).__name__, e), None)


fails = []
for i in range(6000):
    c = cell()
    rn = run(NEW["classify_eval"], c, "py", {}, {})
    ro = run(OLD["classify_eval"], c, "py", {})
    if rn[0] != "ok" or ro[0] != "ok":
        fails.append(("eval", c, rn[0], ro[0]))
        if len(fails) > 40:
            break
for i in range(4000):
    c = shcell()
    rn = run(NEW["classify_shell"], c)
    ro = run(OLD["classify_shell"], c)
    if rn[0] != "ok" or ro[0] != "ok":
        fails.append(("shell", c, rn[0], ro[0]))
        if len(fails) > 60:
            break

print("total anomalies: %d" % len(fails))
for kind, c, rn, ro in fails[:60]:
    flag = " NEW-ONLY" if (rn != "ok" and ro == "ok") else ""
    print("--- %s new=%s old=%s%s" % (kind, rn, ro, flag))
    print("   %r" % c[:300])
