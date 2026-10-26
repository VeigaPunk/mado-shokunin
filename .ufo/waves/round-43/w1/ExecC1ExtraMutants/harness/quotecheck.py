import json
import os
import re
import subprocess

LANE = "/home/vgpnk/Projects/shokunin/mado-shokunin"
SEAT = os.path.join(LANE, ".ufo/waves/round-43/w1/ExecC1ExtraMutants")
REPORT = os.path.join(LANE, ".ufo/waves/round-43/w1/ExecC1ExtraMutants.md")
OUT = open(os.path.join(SEAT, "quotecheck.txt"), "w")
ok = True


def chk(name, cond, detail=""):
    global ok
    ok &= bool(cond)
    OUT.write("%-44s %s %s\n" % (name, "PASS" if cond else "FAIL", detail))
    print("%-44s %s %s" % (name, "PASS" if cond else "FAIL", detail))


def line_of(path, n):
    return open(path, encoding="utf-8", errors="replace").read().splitlines()[n - 1]


# 1. quotes, each with its locator (<= 25 words)
for scope, text in (("report", open(REPORT, encoding="utf-8").read()),
                    ("survivors", open(os.path.join(SEAT, "survivors.md"), encoding="utf-8").read())):
    for quote in re.findall(r'"([^"\n]{8,200})"', text):
        words = len(quote.split())
        if words > 25:
            chk("quote<=25words %r" % quote[:30], False, "words=%d" % words)
for q, path, n in [("decoded as UTF-8 with errors replaced",
                    os.path.join(LANE, "quality/counters/c1-r42-geometry.py"), 26),
                   ("decoded as UTF-8 with errors replaced",
                    os.path.join(LANE, ".ufo/waves/round-42/c1/ctl-ref-tool.py.txt"), 25),
                   ("decoded as UTF-8 with errors replaced", REPORT, None)]:
    if n is None:
        chk("quote-in-report %r" % q[:30], q in open(REPORT, encoding="utf-8").read())
    else:
        src = line_of(path, n)
        chk("quote@%s:%d" % (os.path.basename(path), n), q in src, src.strip()[:60])
chk("quote-locators-present-in-report", "c1-r42-geometry.py:26" in open(REPORT).read())

# 2. reference identity
d = subprocess.run(["diff", "-q", os.path.join(SEAT, "ref.py"),
                    os.path.join(LANE, ".ufo/waves/round-42/c1/ctl-ref-tool.py.txt")],
                   capture_output=True, text=True)
chk("ref.py == ctl-ref-tool.py.txt", d.returncode == 0, d.stdout.strip())
d2 = subprocess.run(["diff", "-q", os.path.join(SEAT, "ref.py"),
                     os.path.join(LANE, "tools/mado-geometry.py")], capture_output=True, text=True)
chk("ref.py == tools/mado-geometry.py@HEAD", d2.returncode == 0, d2.stdout.strip())

# 3. survivors.md shape
sv = open(os.path.join(SEAT, "survivors.md"), encoding="utf-8").read()
rows = [ln for ln in sv.splitlines() if re.match(r"\|\s*\d+\s*\| `N", ln)]
chk("survivors.md table rows == 68", len(rows) == 68, str(len(rows)))
chk("survivors.md survivor sections == 15", sv.count("\n### `N") == 15, str(sv.count("\n### `N")))
chk("survivors.md EQUIVALENT count", sv.count("— EQUIVALENT") == 13, str(sv.count("— EQUIVALENT")))
chk("survivors.md MISSING CHECK count", sv.count("— MISSING CHECK") == 2, str(sv.count("— MISSING CHECK")))

# 4. results
res = json.load(open(os.path.join(SEAT, "results.json")))
chk("results entries == 68", len(res) == 68, str(len(res)))
met = [r for r in res if r["met"]]
chk("MET == 15, MISSED == 53", (len(met), len(res) - len(met)) == (15, 53),
    "%d/%d" % (len(met), len(res) - len(met)))
nofix = [r["name"] for r in res if not r["met"]
         and not [f for f in r["fails"] if not f.startswith("clause-")]]
chk("every killed mutant has a failing fixture", not nofix, ",".join(nofix))
chk("mutant files == 68", len([f for f in os.listdir(os.path.join(SEAT, "mutants"))
                               if f.endswith(".py")]) == 68)
chk("nonce range", all(r["final"].split("nonce=")[-1].startswith("exm43") for r in res),
    res[0]["final"].split("nonce=")[-1] + ".." + res[-1]["final"].split("nonce=")[-1])

# 5. novelty census against the registered control runner
import ast
reg = open(os.path.join(LANE, ".ufo/waves/round-42/ctl/run-c1-controls.py")).read()
pairs = []
for node in ast.walk(ast.parse(reg)):
    if isinstance(node, ast.List):
        for el in node.elts:
            if isinstance(el, ast.Tuple) and len(el.elts) == 3 \
                    and all(isinstance(x, ast.Constant) for x in el.elts):
                pairs.append((el.elts[0].value, el.elts[1].value, el.elts[2].value))
chk("registered MUTANTS == 38", len(pairs) == 38, str(len(pairs)))
regold = {p[1] for p in pairs}
fresh = [r for r in res if r["old"] not in regold]
dup = [r["name"] for r in res if any((r["old"], r["new"]) == (p[1], p[2]) for p in pairs)]
chk("fresh-site mutants == 47", len(fresh) == 47, str(len(fresh)))
chk("same-site mutants == 21", 68 - len(fresh) == 21, str(68 - len(fresh)))
chk("no duplicate (old,new) pair", not dup, ",".join(dup))

# 6. equiv / witness receipts
eq = open(os.path.join(SEAT, "equiv.txt")).read()
fuzz = re.findall(r"fuzz (\S+)\s+cases=(\d+) identical=(\d+) differ=(\d+)", eq)
chk("10 report-level fuzz rows, 0 differ", len(fuzz) == 10 and all(int(f[3]) == 0 for f in fuzz),
    ",".join("%s:%s/%s" % (f[0], f[2], f[1]) for f in fuzz[:3]) + " ...")
hunks = re.findall(r"(N\d+-[a-z0-9-]+)\s+hunks=(\d+) removed=(\d+) added=(\d+)", eq)
chk("15 single-hunk/one-line diffs", len(hunks) == 15 and all(
    h[1] == "1" and h[2] == "1" and h[3] == "1" for h in hunks), "%d entries" % len(hunks))
w = open(os.path.join(SEAT, "witness.txt")).read()
chk("witness C: 6 identical stdin sizes", w.count("same=True") >= 6)
chk("witness E: N48 ref rc=4 / mut rc=0", "ref:  rc=4" in w and "mut:  rc=0" in w)
chk("witness F: N51 leak observable", w.count("same=False") == 3)
chk("witness G: N68 identical stdout x4", w.count("same_stdout=True same_rc=True") == 4)

# 7. the report's own numbers appear
rpt = open(REPORT, encoding="utf-8").read()
for phrase in ("47 of my 68", "53 `TARGET_MISSED`, 15 `TARGET_MET`", "17 kills are narrow",
               "size0` 25", "exactly MAX_BYTES is legal"):
    chk("report claim %r" % phrase[:28], phrase in rpt)

OUT.write("\nOVERALL %s\n" % ("PASS" if ok else "FAIL"))
print("\nOVERALL", "PASS" if ok else "FAIL")
