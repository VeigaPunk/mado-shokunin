#!/usr/bin/env python3
"""Verify the proposed harness additions against the verdict-level survivors of drive.py.

P1 golden  : each control's full missed set must equal the set the pristine harness records on the real counter
             (GOLD derived from an UNCLIPPED copy of the pristine module; the pinned sets are embedded in the source).
P2 echo7   : control 11 must also see echo:K07 (the quote of exactly 30 characters, the threshold row).
P3 rowloc  : a control may report row-grammar legs only for the row it mutates (control 7 -> row:K17, control 8 -> row:K05),
             never row:<other> (a row the mutation did not touch).

Each addition is applied as a text insertion after the unique anchor `why = judge_control(sha, rc, rec, err, check)`
(or the `_need_echo` header for P2). A proposal is VERIFIED when: pristine+P is OK (12/12, exit 0) on the real counter,
and the survivor+P is FAIL. Every run uses the real counter exported at the revision.
"""
import json
import os
import re
import shutil
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

SCR = Path("/fast/scratch/hyaku/mado-r56/R56W2MutC1Harness")
REPO = SCR / "repo"
REV = "a96bd38b6cc042e87430ef7c65ecd7cf56b1140c"
CHECK = SCR / "pristine" / "check-r56-controls.py"
PRIS = SCR / "pristine" / "r56_ctl_c1.py"
OUT = SCR / "proposals"
ENV = {"PATH": os.environ.get("PATH", "/usr/bin:/bin"), "LC_ALL": "C.UTF-8"}
ANCHOR = "            why = judge_control(sha, rc, rec, err, check)"
ANCHOR = "        why = judge_control(sha, rc, rec, err, check)"


def run_harness(mod_src: str, name: str) -> dict:
    d = OUT / name
    if d.exists():
        shutil.rmtree(d)
    d.mkdir(parents=True)
    shutil.copy(CHECK, d / "check-r56-controls.py")
    (d / "r56_ctl_c1.py").write_text(mod_src)
    work = d / "work"
    work.mkdir()
    p = subprocess.run([sys.executable, "-I", str(d / "check-r56-controls.py"), "--claim", "c1", "--repo", str(REPO),
                        "--rev", REV, "--work", str(work)], capture_output=True, timeout=900, env=ENV, cwd=str(d))
    (d / "stdout.txt").write_text(p.stdout.decode())
    (d / "stderr.txt").write_text(p.stderr.decode())
    shutil.rmtree(work, ignore_errors=True)
    return {"rc": p.returncode, "out": p.stdout.decode().strip(), "err": p.stderr.decode()}


def derive_gold():
    """Unclipped pristine copy: run on the real counter and read each control's full missed list."""
    src = PRIS.read_text()
    assert src.count("def _clip(legs: list, n: int = 8) -> str:") == 1
    unclipped = src.replace("def _clip(legs: list, n: int = 8) -> str:", "def _clip(legs: list, n: int = 10**9) -> str:")
    r = run_harness(unclipped, "gold-unclipped")
    assert r["out"].endswith("controls=12/12 verdict=OK"), r["out"]
    gold = {}
    for line in r["err"].split("\n"):
        m = re.match(r"^(C1-CTL-\d\d) .*: ok \(required .*?\) - counter missed=(.*)$", line)
        if m:
            legs = [] if m.group(2) == "none" else m.group(2).split(",")
            gold[m.group(1)] = sorted(legs)
    assert len(gold) == 12, sorted(gold)
    return gold


def apply(src: str, proposal: str, gold: dict) -> str:
    if proposal == "P1":
        assert src.count(ANCHOR) == 1, "anchor count %d" % src.count(ANCHOR)
        ins = ANCHOR + "\n        if why is None and sorted(rec[\"legs\"]) != GOLD[cid]:\n" \
              "            why = \"missed set differs from pinned golden: %s\" % _clip(rec[\"legs\"])"
        src = src.replace(ANCHOR, ins, 1)
        gold_src = "GOLD = {\n" + "".join("    %r: %r,\n" % (k, v) for k, v in sorted(gold.items())) + "}\n\n\n"
        src = src.replace("CONTROLS = [\n", gold_src + "CONTROLS = [\n", 1)
        return src
    if proposal == "P2":
        old = "def _need_echo(rec):\n"
        assert src.count(old) == 1, "P2 anchor"
        return src.replace(old, old + "    if \"echo:K07\" not in rec[\"legs\"]:\n"
                                  "        return \"echo:K07 (30-character quote) not in missed=%s\" % rec[\"missed\"]\n", 1)
    if proposal == "P3":
        assert src.count(ANCHOR) == 1, "anchor count %d" % src.count(ANCHOR)
        ins = ANCHOR + "\n        if why is None and any(l.startswith(\"row:\") and l not in ROWOK.get(cid, ()) for l in rec[\"legs\"]):\n" \
              "            why = \"row-grammar leg outside the mutated row: %s\" % _clip([l for l in rec[\"legs\"] if l.startswith(\"row:\") and l not in ROWOK.get(cid, ())])"
        src = src.replace(ANCHOR, ins, 1)
        rowok = 'ROWOK = {"C1-CTL-07": ("row:K17",), "C1-CTL-08": ("row:K05",)}\n\n\n'
        src = src.replace("CONTROLS = [\n", rowok + "CONTROLS = [\n", 1)
        return src
    raise SystemExit("unknown proposal " + proposal)


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    gold = derive_gold()
    (OUT / "gold.json").write_text(json.dumps(gold, indent=1, sort_keys=True))
    print("gold legs per control:", {k: len(v) for k, v in sorted(gold.items())})
    targets = ["PRISTINE"] + sys.argv[1:]
    jobs = []
    for prop in ["P1", "P2", "P3"]:
        for t in targets:
            if t == "PRISTINE":
                base = PRIS.read_text()
            else:
                base = (SCR / "mutants" / t / "r56_ctl_c1.py").read_text()
            try:
                src = apply(base, prop, gold)
            except AssertionError as e:
                jobs.append((prop, t, None, "anchor mismatch: %s" % e))
                continue
            jobs.append((prop, t, src, None))
    results = {}
    with ThreadPoolExecutor(max_workers=8) as ex:
        futs = {}
        for prop, t, src, err in jobs:
            if src is None:
                results[(prop, t)] = {"rc": None, "out": "NOT APPLIED: " + err, "err": ""}
                continue
            futs[(prop, t)] = ex.submit(run_harness, src, "%s-%s" % (prop, t))
        for k, f in futs.items():
            results[k] = f.result()
    for prop in ["P1", "P2", "P3"]:
        for t in targets:
            r = results[(prop, t)]
            print("%s on %-10s rc=%-4s %s" % (prop, t, r["rc"], r["out"][-70:]))
    summary = {"%s|%s" % k: {"rc": v["rc"], "out": v["out"]} for k, v in results.items()}
    (OUT / "summary.json").write_text(json.dumps(summary, indent=1))


if __name__ == "__main__":
    main()
