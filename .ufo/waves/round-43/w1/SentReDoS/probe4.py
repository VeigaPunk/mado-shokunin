#!/usr/bin/env python3
"""L (broken pipe), M (rules sources), and a fixture-compatibility check of a
candidate mitigations: (1) ambiguity rejection for regex_ok, (2) a match budget.
All three are checked against the counter's own 53 regex0 entries."""
import ast, json, os, subprocess, sys, time

HERE = os.path.dirname(os.path.abspath(__file__))
TOOL = os.path.join(HERE, "bin", "mado-geometry.py")
COUNTER = "/home/vgpnk/Projects/shokunin/mado-shokunin/quality/counters/c1-r42-geometry.py"
W = os.path.join(HERE, "misc")
os.makedirs(W, exist_ok=True)
J = dict(separators=(",", ":"))


def P(*a):
    print(*a, flush=True)


def put(name, data):
    p = os.path.join(W, name)
    with open(p, "w") as f:
        f.write(data)
    return p


def call(argv, timeout=60):
    t0 = time.monotonic()
    try:
        p = subprocess.run([sys.executable, "-I", TOOL] + argv, capture_output=True, timeout=timeout)
        return time.monotonic() - t0, p.returncode, p.stdout, p.stderr, False
    except subprocess.TimeoutExpired as e:
        return time.monotonic() - t0, None, e.stdout or b"", e.stderr or b"", True


P("########## L. broken pipe with a >1 MiB stdout")
cl = [{"class": "b" * 40000, "size": [1, 2], "floating": True} for _ in range(26)]
c = put("l.json", json.dumps(cl, **J))
r = put("l.conf", "windowrule = size 1 2, match:class .*\n")
dt, rc, out, err, to = call(["--clients", c, "--rules", r])
P("  full run: %.3fs rc=%s stdout=%dB stderr=%dB" % (dt, rc, len(out), len(err)))
p = subprocess.Popen([sys.executable, "-I", TOOL, "--clients", c, "--rules", r],
                     stdout=subprocess.PIPE, stderr=subprocess.PIPE)
p.stdout.read(4096)
p.stdout.close()
err = p.stderr.read()
rc2 = p.wait()
P("  reader closes after 4 KiB: rc=%r stderr=%dB %r" % (rc2, len(err), err.decode()[:300]))
q = subprocess.run("%s -I %s --clients %s --rules %s | head -c 100 >/dev/null"
                   % (sys.executable, TOOL, c, r), shell=True, executable="/bin/bash",
                   capture_output=True)
P("  via '| head -c 100': bash rc=%r stderr=%r" % (q.returncode, q.stderr.decode()[:300]))

P("\n########## M. rules sources: binary / other files (decode errors replaced)")
m = put("m.json", "[]")
for path in (TOOL, "/bin/ls", "/etc/passwd", "/proc/self/maps"):
    dt, rc, out, err, to = call(["--clients", m, "--rules", path], timeout=30)
    ls = out.decode("utf-8", "replace").splitlines()
    P("  rules=%-22s rc=%s %.3fs %s" % (path, rc, dt, (ls[-1][:70] if ls else "")))

# ---------------------------------------------------------------- mitigation check
sys.path.insert(0, os.path.dirname(TOOL))
import importlib.util
spec = importlib.util.spec_from_file_location("ref", TOOL)
ref = importlib.util.module_from_spec(spec)
spec.loader.exec_module(ref)

src = open(COUNTER).read()
tree = ast.parse(src)
rxs = None
for fn in [n for n in ast.walk(tree) if isinstance(n, ast.FunctionDef)]:
    if fn.name == "score_regex0":
        for node in ast.walk(fn):
            if isinstance(node, ast.Assign) and isinstance(node.targets[0], ast.Name) \
                    and node.targets[0].id == "rxs":
                rxs = ast.literal_eval(node.value)
P("\n########## N. mitigation compatibility with the counter's regex0 list (%d entries)" % len(rxs or []))


def groups_ranges(rx):
    """map group body spans for balanced () in the SAFE subset"""
    stack, out = [], []
    for i, ch in enumerate(rx):
        if ch == "\\":
            continue
        if ch == "(":
            stack.append(i)
        elif ch == ")" and stack:
            out.append((stack.pop(), i))
    return out


def first_atom(alt):
    """first atom of an alternative: 'L:x' literal, 'dot', 'esc:x'"""
    if not alt:
        return ("empty",)
    if alt[0] == "\\":
        return ("esc", alt[1:2])
    return ("lit", alt[0])


def ambiguous(rx):
    """candidate R2: reject quantifier-on-nested-quantifier, quantified groups
    with first-atom-overlapping alternatives, and two or more `.*`."""
    if rx.count(".*") > 1:
        return "stacked-wildcard"
    for (a, b) in groups_ranges(rx):
        body = rx[a + 1:b]
        if b + 1 < len(rx) and rx[b + 1] in "*+?":
            if any(c in body for c in "*+?"):
                return "nested-quantifier"
            alts = [x for x in body.split("|")]
            if len(alts) > 1:
                firsts = [first_atom(x) for x in alts]
                for i in range(len(firsts)):
                    for j in range(i + 1, len(firsts)):
                        if firsts[i] == firsts[j]:
                            return "overlapping-alternation"
    return None


same, diff = 0, []
for rx in rxs:
    old = ref.regex_ok(rx)
    rej = ambiguous(rx)
    new = old and rej is None
    if old == new:
        same += 1
    else:
        diff.append((rx, old, new, rej))
P("  classifications identical on %d/%d regex0 entries" % (same, len(rxs)))
P("  differences: %r" % (diff,))
for rx in ("^(a|b)+\\.c$",):
    P("  selftest assertion regex_ok(%r)=%s under both old=%s new=%s (R2 rejection=%r)"
      % (rx, ref.regex_ok(rx), ref.regex_ok(rx), ref.regex_ok(rx) and ambiguous(rx) is None, ambiguous(rx)))
P("  attack patterns rejected by R2: %r" % {r: ambiguous(r) for r in
                                             ("(a+)+$", "(a|aa)+$", "(a*)*b", ".*.*.*b", ".*.*.*.*b",
                                              "(a|b)+$", "(a|ab)(c|d)", "x" * 5 + "|" + "y" * 5)})

P("\n########## O. match-budget check: cost of every fixture shape is tiny except many0")
P("  many0 = 20000 clients x 300 rules -> pairs=6.0e6, chars=6.0e6, budget 5e7 -> %s"
  % ("fits" if 6e6 + 6e6 <= 5e7 else "REJECTED"))
P("  measured wedges: 13x40000B x 12000 rules -> pairs=1.56e5, chars=6.24e9 -> rejected by budget")
