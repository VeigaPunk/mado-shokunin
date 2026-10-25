#!/usr/bin/env python3
"""RevC2Tip secondary probes: clause-list shrink (h1) and retired-why non-use.

REBUILT 2026-10-25 ~03:50 from the seat transcript after the ~03:45 external
sweep removed `.ufo/waves/round-35/scratch/`. Pre-sweep behaviour: these were
run as inline heredocs; the mutations are unchanged.
"""
import copy
import json
import subprocess
from pathlib import Path

LANE = Path("/home/vgpnk/Projects/shokunin/mado-shokunin")
SCR = LANE / ".ufo/waves/round-35/scratch/RevC2Tip/h1"
SCR.mkdir(parents=True, exist_ok=True)
F = json.loads((LANE / ".ufo/waves/round-35/c2/frozen.json").read_text())
C = json.loads((LANE / ".ufo/waves/round-35/c1/clauses.json").read_text())


def run(name, clauses):
    d = SCR / name
    d.mkdir(exist_ok=True)
    (d / "clauses.json").write_text(json.dumps(clauses, indent=1) + "\n")
    f = copy.deepcopy(F)
    f["clause_ledger"] = str((d / "clauses.json").resolve())
    (d / "frozen.json").write_text(json.dumps(f, indent=1) + "\n")
    p = subprocess.run(
        ["python3", "-I", ".ufo/waves/round-35/c2/count.py",
         "--repo", str(LANE), "--frozen", str((d / "frozen.json").resolve())],
        capture_output=True, text=True, cwd=str(LANE),
    )
    print(f"{name:34s} rc={p.returncode} {(p.stdout + p.stderr).strip()}")


c = copy.deepcopy(C)
c["live"] = [x for x in c["live"] if x["id"] != "digest-match"]
run("h1-drop-one-load-bearing", c)

c = copy.deepcopy(C)
c["live"] = [x for x in c["live"] if x["id"] == "o-nofollow-open"]
run("h1-live-only-declaration", c)

c = copy.deepcopy(C)
c["live"] = [x for x in c["live"] if x["id"] != "o-nofollow-open"]
run("h1-drop-declaration", c)

c = copy.deepcopy(C)
c["live"] = [x for x in c["live"] if x["id"] != "digest-match"]
c["retired"].append({"id": "digest-match", "why": "quietly retired"})
run("h1-drop-into-retired", c)

rw = SCR / "retwhy"
rw.mkdir(exist_ok=True)
for name, mut in [("empty-why", {"id": "x", "why": ""}), ("no-why", {"id": "y"})]:
    c = copy.deepcopy(C)
    c["retired"] = [mut]
    (rw / f"{name}-clauses.json").write_text(json.dumps(c, indent=1))
    f = copy.deepcopy(F)
    f["clause_ledger"] = str((rw / f"{name}-clauses.json").resolve())
    (rw / f"{name}-frozen.json").write_text(json.dumps(f, indent=1))
    p = subprocess.run(
        ["python3", "-I", ".ufo/waves/round-35/c2/count.py",
         "--repo", str(LANE), "--frozen", str((rw / f"{name}-frozen.json").resolve())],
        capture_output=True, text=True, cwd=str(LANE),
    )
    print(f"{name:34s} rc={p.returncode} {(p.stdout + p.stderr).strip()}")
