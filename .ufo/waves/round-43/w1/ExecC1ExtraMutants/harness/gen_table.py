import json
import os

SEAT = "/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-43/w1/ExecC1ExtraMutants"
res = json.load(open(os.path.join(SEAT, "results.json")))
res.sort(key=lambda r: r["name"])

CL = json.load(open(os.path.join(SEAT, "classify.json")))
rows = []
for r in res:
    fx = [f.split(" (")[0] for f in r["fails"] if not f.startswith("clause-")]
    try:
        cl = [kv.split(":")[0] for kv in r["clauses"].split("clauses=")[1].split()
              if kv.endswith(":0")]
    except IndexError:
        cl = ["?"]
    if r["met"]:
        verdict = "TARGET_MET (survivor)"
        why = "none — 37/37 fixtures, clauses a,b,b2,b3,g all 1"
    else:
        verdict = "TARGET_MISSED (killed)"
        parts = []
        parts.append("fixtures: " + ", ".join(fx[:4]) + ("(+%d)" % (len(fx) - 4) if len(fx) > 4 else ""))
        if cl:
            parts.append("clauses: " + ", ".join("%s=0" % c for c in cl))
        why = "; ".join(parts)
    edit = "%s -> %s" % (r["old"].replace("\n", "\\n"), r["new"].replace("\n", "\\n"))
    if len(edit) > 150:
        edit = edit[:147] + "..."
    rows.append((r["name"], r["category"], edit, verdict, why))

lines = []
A = lines.append
A("# C1 mutation population — 68 new single-defect mutants of the reference tool")
A("")
A("Reference: `.ufo/waves/round-42/c1/ctl-ref-tool.py.txt` (`ref.py` here; `diff` against `tools/mado-geometry.py` at HEAD is empty).")
A("Each mutant is one text replacement asserted to match the reference exactly once (`mutants.json` records the pair; "
  "`diff -u ref.py mutants/<name>.py` is one hunk, one removed line, one added line — section B of `equiv.txt`); "
  "every mutant file compiles.")
A("")
A("Scoring command per mutant (private nonce `exm43NNNN`, `C1R42_TMP` under `/fast/scratch/hyaku/mado-r43/ExecC1ExtraMutants/run/<name>`):")
A("")
A("```")
A("cd /home/vgpnk/Projects/shokunin/mado-shokunin && C1R42_TMP=<scratch>/<name> \\")
A("  python3 -I quality/counters/c1-r42-geometry.py --repo . \\")
A("    --rev b2e2efd6e268920d31f3c32cf52dc097dd6e1d22 \\")
A("    --base a35cfdfcdeb3bd42d1a2cd960faf22ceac1bef3f \\")
A("    --tool .ufo/waves/round-43/w1/ExecC1ExtraMutants/mutants/<name>.py --nonce <nonce>")
A("```")
A("")
A("`verdict` is the counter's own final-line verdict; a mutant that reaches `TARGET_MET` is a survivor the predicate does not kill.")
A("Raw per-run data: `results.json` (final line, clauses line, every failing fixture line).")
A("")
A("| # | mutant | category | edit (reference -> mutant) | verdict | failing fixtures / clauses |")
A("|---|---|---|---|---|---|")
for i, (name, cat, edit, verdict, why) in enumerate(rows, 1):
    A("| %d | `%s` | %s | `%s` | %s | %s |" % (i, name, cat, edit.replace("|", "\\|"), verdict, why))
A("")
A("Totals: %d mutants, %d killed, %d survivors." % (
    len(rows), sum(1 for r in res if not r["met"]), sum(1 for r in res if r["met"])))
A("")
A("## Survivors")
A("")
for r in res:
    if not r["met"]:
        continue
    c = CL[r["name"]]
    A("### `%s` — %s" % (r["name"], c["kind"]))
    A("")
    A("* edit: `%s` -> `%s`" % (r["old"].replace("\n", "\\n"), r["new"].replace("\n", "\\n")))
    A("* counter: `%s`" % r["final"].split("PRED-C1-r42: ")[-1])
    A("* %s" % c["text"])
    A("")
open(os.path.join(SEAT, "survivors.md"), "w").write("\n".join(lines) + "\n")
print("wrote survivors.md rows=%d" % len(rows))
print("survivors:", [r["name"] for r in res if r["met"]])
