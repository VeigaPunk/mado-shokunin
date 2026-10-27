#!/usr/bin/env python3
import subprocess, sys, os
S = "/fast/scratch/hyaku/mado-r52/Attack06"
F = S + "/fixtures/repo"
COUNTER = F + "/quality/counters/c1-r52-ledger.py"
HEAD = subprocess.run(["git","-C",F,"rev-parse","HEAD"],capture_output=True,text=True,check=True).stdout.strip()

HDR = """# fixture ledger

| instrument | description | accountability pointer |
|---|---|---|
"""
rows = {
 "alpha":    "| `tools/alpha.sh` | Prints the widget verdict for the alpha checker instrument. | `PROVINCE.md:7` |",
 "gate":     "| `quality/check-tool-ledger.py` | Derives the tracked-instrument population at a revision and checks its accountability ledger. | `PROVINCE.md:5` |",
 "c52":      "| `quality/counters/c1-r52-ledger.py` | PRED-C1-r52: checks complete population, non-self evidence pointers and a bounded lexical context signal; not semantic entailment. | `PROVINCE.md:6` |",
}
def mk(name, **over):
    r = dict(rows); r.update(over)
    text = HDR + r["alpha"] + "\n" + r["gate"] + "\n" + r["c52"] + "\n"
    p = os.path.join(S, "fixtures", "fix-" + name + ".md")
    open(p, "w").write(text)
    pr = subprocess.run([sys.executable,"-I",COUNTER,"--repo",F,"--rev",HEAD,
                         "--ledger",p,"--work",S+"/work"],
                        capture_output=True,text=True)
    line = [l for l in pr.stdout.splitlines() if l.startswith("C1_R52:")][-1]
    det = [l for l in pr.stdout.splitlines() if l.startswith("detail:")]
    print("== %-38s rc=%d" % (name, pr.returncode))
    print("   " + line.split(" rev=")[0])
    for d in det: print("   " + d)
    if pr.stderr.strip(): print("   STDERR " + pr.stderr.strip()[:200])

mk("V0-green")
mk("V1-worktree-desc",
   c52="| `quality/counters/c1-r52-ledger.py` | PRED-C1-r52: checks complete population, non-self evidence pointers and a bounded lexical context signal; not semantic entailment. | `PROVINCE.md:6` |")
mk("V2-worktree-pointer",
   c52="| `quality/counters/c1-r52-ledger.py` | PRED-C1-r52: checks complete population, non-self evidence pointers and a bounded lexical context signal; not semantic entailment. | `.ufo/waves/round-52/registration.md` |")
mk("V3-honest-paraphrase",
   c52="| `quality/counters/c1-r52-ledger.py` | Checks the tool ledger for population completeness, non-self evidence pointers and a bounded lexical context signal. | `PROVINCE.md:6` |")
mk("V4-honest-plain",
   c52="| `quality/counters/c1-r52-ledger.py` | Verifies that every instrument has one row and an accountable pointer in the tool ledger. | `PROVINCE.md:6` |")
mk("V5-pointer-is-ledger",
   c52="| `quality/counters/c1-r52-ledger.py` | Derives the tracked-instrument population at a revision and checks its accountability ledger. | `quality/tool-ledger.md:9` |")
mk("V6-honest-desc-unresolvable-ptr",
   c52="| `quality/counters/c1-r52-ledger.py` | Reads `quality/tool-ledger.md` and checks each instrument row. | `.ufo/waves/round-52/registration.md` |")
