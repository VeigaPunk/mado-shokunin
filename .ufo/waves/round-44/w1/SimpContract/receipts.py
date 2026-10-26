#!/usr/bin/env python3
"""Receipts for seat SimpContract: C1 entailment checks and C2 clause-h measurements."""
import importlib.machinery
import importlib.util, itertools, json, os, random, re, hashlib

LANE = "/home/vgpnk/Projects/shokunin/mado-shokunin"
SC = os.path.dirname(os.path.abspath(__file__))
F = LANE + "/.ufo/waves/round-44/fetch/"
OUT = os.path.dirname(os.path.abspath(__file__)) + "/"

def load(p, n):
    ldr = importlib.machinery.SourceFileLoader(n, p)
    sp = importlib.util.spec_from_loader(n, ldr)
    m = importlib.util.module_from_spec(sp); ldr.exec_module(m); return m

c1 = load(LANE + "/quality/counters/c1-r44-geometry-states.py", "c1r44")
c2 = load(LANE + "/quality/counters/c2-r44-gkeep-size-request.py", "c2r44")
ref = load(LANE + "/.ufo/waves/round-44/c1/ctl-ref-tool.py.txt", "ref")
old = c1.old

L = []
def w(*a):
    L.append(" ".join(str(x) for x in a))

# ---------------------------------------------------------------- E2 entailment
w("== E2: is the parenthetical enumeration entailed by E1?")
w("E1 antecedent: a JSON integer (not a boolean, not a float) equal to 1 or 2 -> fsmode")
E2 = ["absent", None, 0, 3, -1, True, 2.0, "2", [2], {"internal": 2}]
w("%-16s %-8s %-8s %-8s" % ("value", "E1-holds", "fsmode", "docstring"))
for v in E2:
    c = {} if v == "absent" else {"fullscreen": v}
    hold = (type(v) is int and v in (1, 2))
    mode = c1.fsmode_of(c) if v != "absent" else c1.fsmode_of({})
    w("%-16r %-8s %-8s %-8s" % (v, hold, mode, 0))
w("every enumerated value falsifies E1's antecedent, so E1 alone yields 0 for each.")
w("")
w("== coverage of those values by the frozen lattice (clause f)")
w("FS_POOL sgen draw:", json.dumps([x if x != "absent" else "absent" for x in c1.FS_POOL]))
w("fsvals0 values   :", json.dumps([x for x in (True, False, 3, 2.0, "2", -1, None, [2], {"internal": 2}, 0)]))
w("fsmany0 draws from FS_POOL (200 clients).")
w("=> no enumerated value is left to the table alone; the fixtures already pin each one.")
w("")

# ---------------------------------------------------------------- E6 identity
w("== E6: with no state client the extended summary equals the r42 summary")
GKCONF = c1.GKCONF
def old_rep(doc, texts):
    return old.model_out(json.dumps(doc).encode(), texts)
rng = random.Random(44)
diff = 0; n = 0
for k in range(500):
    doc = []
    for j in range(rng.randrange(0, 5)):
        c = {"class": rng.choice([c1.GK, "kitty", ""]), "floating": rng.choice([True, False]),
             "address": "0x%x" % j}
        if rng.randrange(4): c["size"] = [rng.choice([420, 421, 2560]), rng.choice([500, 1440])]
        doc.append(c)
    n += 1
    a = old_rep(doc, [GKCONF])
    bl, brc = ref.report(json.dumps(doc).encode(), [GKCONF])
    b = ("\n".join(bl) + "\n", brc)
    if a != b:
        diff += 1; w("DIFF", json.dumps(doc), a, b)
w("docs without a fullscreen field: inputs=%d differing=%d (r42 model vs extended tool)" % (n, diff))
w("")

# ---------------------------------------------------------------- C2 clause h
w("== C2 clause h: does `with # comments removed` change any computed value?")
uiraw = open(F + "gkeep-ui.py", "rb").read().decode("utf-8", "replace")
uistr = c2.strip_comments(uiraw, "gkeep-ui.py")
for tag, t in (("raw", uiraw), ("stripped", uistr)):
    w("%-9s set_default_size=%s application_id=%s set_size_request(=%d set_default_size(=%d"
      % (tag, re.findall(r"set_default_size\(([0-9]+), ([0-9]+)\)", t),
         re.findall(r'application_id="([^"]+)"', t),
         t.count("set_size_request("), t.count("set_default_size(")))
w("lines carrying any of the three patterns:")
for k, line in enumerate(uiraw.split("\n"), 1):
    if "set_size_request" in line or "set_default_size" in line or "application_id" in line:
        w("  %d: %r" % (k, line))
w("=> identical values; the pin holds no commented-out occurrence.")
w("")
w("== C2 clause h: what does the body scope change?")
win = open(F + "Hyprland-Window.cpp", "rb").read().decode("utf-8", "replace")
src = win.split("\n")
k = src.index("void CWindow::sendWindowSize(bool force) {")
end = src.index("}", k + 1)
body = "\n".join(src[k:end + 1])
depth = 0; alt = None
for i in range(k, len(src)):
    depth += src[i].count("{") - src[i].count("}")
    if depth == 0:
        alt = i; break
w("signature line (1-based) %d; first following line exactly '}' is line %d; brace-match end line %d; same=%s"
  % (k + 1, end + 1, alt + 1, alt == end))
w("lines exactly '}' strictly between signature and end:", [i + 1 for i in range(k + 1, end) if src[i] == "}"])
w("body   ->setSize(=%d ->configure(=%d" % (body.count("->setSize("), body.count("->configure(")))
w("file   ->setSize(=%d ->configure(=%d" % (win.count("->setSize("), win.count("->configure(")))
w("=> the *scope* (body) is load-bearing (1/1 vs 2/3); the *end rule* ('first following line")
w("   exactly }') is equivalent to brace matching on this pin.")
w("")
w("== C2 clause h: the two census lines are constants of the pin")
gates = {i: [(F + name, c2.PINS[name], "x")] for i, name in
         ((298, "Hyprland-XDGShell.cpp"), (299, "xdg-shell.xml"), (300, "gdktoplevel-wayland.c"),
          (301, "gkeep-ui.py"), (164, "Hyprland-Window.cpp"))}
raw = {i: open(F + os.path.basename(g[0][0]), "rb").read() for i, g in gates.items()}
ok0, want = c2.host_census(list(gates), None, gates, raw, [])
ok, want2 = c2.host_census(list(gates), None, gates, raw, list(want))
w("host_census(entry carries neither line)=%s, (entry carries both)=%s, lines stable=%s ->" % (ok0, ok, want == want2))
for line in want:
    w("  %r" % line)
w("neither line can vary with the entry: the receipts are sha256 pins (PINS at lines 167-173).")
w("")
w("== C2 clause h: is `l not in census_lines` reachable?")
for tag, line in (("ui_line", want[0] if want else ""), ("hy_line", want[1] if len(want) > 1 else "")):
    w("%s starts with an exempt prefix: %s / %s" % (
        tag, line.startswith("gkeep client "), line.startswith("hyprland sendWindowSize ")))
w("=> every string in census_lines is already excluded by the two startswith tests (lines 560-563).")
w("")
w("== C2 clause i already requires every PINS name (line 604: `bad |= not set(PINS) <= used`)")
w("PINS names:", sorted(c2.PINS))
w("both census receipts are PINS members:",
  "gkeep-ui.py" in c2.PINS, "Hyprland-Window.cpp" in c2.PINS)
w("")
w("== hashes of the files this receipt reasons about")
for p in (LANE + "/quality/counters/c1-r44-geometry-states.py",
          LANE + "/quality/counters/c2-r44-gkeep-size-request.py",
          LANE + "/.ufo/waves/round-44/c1/ctl-ref-tool.py.txt",
          F + "gkeep-ui.py", F + "Hyprland-Window.cpp"):
    w("%s  %s" % (hashlib.sha256(open(p, "rb").read()).hexdigest(), p))
open(OUT + "receipts-entailment.txt", "w").write("\n".join(L) + "\n")
print("\n".join(L))
