#!/usr/bin/env python3
"""RevC2Tip: per-observable mutation harness for PRED-C2-r35-v1.

Writes ONLY under the scratch dir. Reads lane bytes read-only.
Each case copies the committed frozen spec and clause ledger into scratch,
mutates exactly one input, and runs the committed counter unchanged.
"""
import copy
import json
import subprocess
import sys
from pathlib import Path

LANE = Path("/home/vgpnk/Projects/shokunin/mado-shokunin")
SCR = LANE / ".ufo/waves/round-35/scratch/RevC2Tip"
COUNTER = ".ufo/waves/round-35/c2/count.py"
FROZEN = LANE / ".ufo/waves/round-35/c2/frozen.json"
CLAUSES = LANE / ".ufo/waves/round-35/c1/clauses.json"
BLOBDOC = LANE / ".ufo/waves/round-35/ledger/RevFrozenBlobs-r35.md"

SCR.mkdir(parents=True, exist_ok=True)
(SCR / "cases").mkdir(exist_ok=True)

BASE_FROZEN = json.loads(FROZEN.read_text())
BASE_CLAUSES = json.loads(CLAUSES.read_text())


def run(name, frozen, clauses):
    cdir = SCR / "cases" / name
    cdir.mkdir(exist_ok=True)
    cl = cdir / "clauses.json"
    cl.write_text(json.dumps(clauses, indent=1) + "\n")
    fz = copy.deepcopy(frozen)
    fz["clause_ledger"] = str(cl)
    fp = cdir / "frozen.json"
    fp.write_text(json.dumps(fz, indent=1) + "\n")
    p = subprocess.run(
        ["python3", "-I", str(LANE / COUNTER), "--repo", str(LANE), "--frozen", str(fp)],
        capture_output=True, text=True,
    )
    out = (p.stdout + p.stderr).strip().replace("\n", " | ")
    print(f"{name:28s} rc={p.returncode} {out}")
    return p.returncode, p.stdout.strip()


def cp():
    return copy.deepcopy(BASE_CLAUSES)


def cf():
    return copy.deepcopy(BASE_FROZEN)


clause = lambda n, i: next(c for c in n["live"] if c["id"] == i)

print("== baseline: unmodified copies in scratch ==")
run("baseline", cf(), cp())

print("== O1 uncovered: what bytes produce it ==")
c = cp()
del clause(c, "digest-match")["control"]
run("u1-no-control", cf(), c)

c = cp()
clause(c, "digest-match")["control"]["receipt"] = ".ufo/waves/round-35/controls/c1-donothing.txt"
run("u2-receipt-swapped", cf(), c)

c = cp()
fake = SCR / "fake-receipt.txt"
fake.write_text("verdict=TARGET_MISSED\n")
clause(c, "digest-match")["control"]["receipt"] = str(fake)
run("u3-grep-only-receipt", cf(), c)

c = cp()
clause(c, "digest-match")["control"]["receipt"] = ".ufo/waves/round-35/controls/nope.txt"
run("u4-missing-receipt", cf(), c)

c = cp()
clause(c, "digest-match")["control"]["receipt"] = ".ufo/waves/round-35/controls/golden.txt"
run("u5-met-receipt", cf(), c)

print("== O2 retired ==")
c = cp()
c["retired"] = []
run("r1-no-retired", cf(), c)

c = cp()
c["retired"][0]["id"] = "invented-clause-not-in-r34"
run("r2-invented-id", cf(), c)

c = cp()
c["retired"][0]["id"] = "digest-match"  # id present in live -> not counted
run("r3-retired-is-live-renewal", cf(), c)

c = cp()
c["retired"].append({"id": "second-invented", "why": "x"})
run("r4-two-retired", cf(), c)

print("== O3 toctou_declared ==")
c = cp()
clause(c, "digest-match")["not-load-bearing"] = {"reason": "copied declaration"}
run("t1-second-declaration", cf(), c)

c = cp()
del clause(c, "o-nofollow-open")["not-load-bearing"]
clause(c, "o-nofollow-open")["control"] = {
    "tree": "controls/c1-entry-symlink",
    "receipt": ".ufo/waves/round-35/controls/c1-entry-symlink.txt",
}
run("t2-declaration-removed", cf(), c)

c = cp()
clause(c, "digest-match")["not-load-bearing"] = {"reason": ""}
run("t3-empty-reason", cf(), c)

c = cp()
c["live"].reverse()
run("t4-reordered-live", cf(), c)

print("== O4 ledger_tip_ok ==")
f = cf()
f["frozen_blobs"][3]["blob_id"] = "0" * 40
run("l1-blob-corrupt", f, cp())

f = cf()
f["frozen_blobs"].pop()
run("l2-blob-dropped", f, cp())

f = cf()
f["r34_tip"] = "19e4ab3171c1540c40d6b12097745af98053b07d"
run("l3-tip-swapped", f, cp())

f = cf()
nodoc = SCR / "doc-notip.md"
nodoc.write_text("# ledger without the tip string\n\nno hash here\n")
f["blob_ledger"] = str(nodoc)
run("l4-doc-without-tip", f, cp())

f = cf()
wrongdoc = SCR / "doc-wrong-table.md"
wrongdoc.write_text(
    "# fake ledger\n\n"
    "dff394109f3cc3d851309ad7c67dd3b35b46adf2\n\n"
    "| Path | blob |\n|---|---|\n| totally/wrong/path.py | " + "f" * 40 + " |\n"
)
f["blob_ledger"] = str(wrongdoc)
run("l5-doc-table-wrong-tip-present", f, cp())

f = cf()
f["frozen_blobs"][0]["path"] = ".ufo/waves/round-34/c1/count.py"
run("l6-path-blob-mismatch", f, cp())

print("== gates ==")
f = cf()
f["predicate"] = f["predicate"] + " "
run("g1-predicate-drift", f, cp())
f = cf()
f["target"]["uncovered"] = 1
run("g2-target-drift", f, cp())
