#!/usr/bin/env python3
"""Verify the numbers this seat's report claims, from the files in this directory
and read-only git queries against the lane.  No session value is printed.

Run:  python3 .ufo/waves/round-49/w1/ExecSessionTriage/verify-claims.py
      (from the lane root; needs git, no network, writes nothing)
"""
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
LANE = subprocess.run(["git", "-C", HERE, "rev-parse", "--show-toplevel"],
                      capture_output=True, text=True).stdout.strip()
BASE = "03e4ae76aff7a4be59cb69970dd553baa319695a"
TIP = "5f37c1b87b3ce5e438d19284e32b2e46fd548a92"
GATE = "82c9053ae2e8b7db2fb8c0e195c32b8b151a593cf9412dcae3589427ac2dfa6f"

passed = failed = 0


def check(name, cond, detail=""):
    global passed, failed
    if cond:
        passed += 1
        print("PASS %s%s" % (name, (" " + detail) if detail else ""))
    else:
        failed += 1
        print("FAIL %s%s" % (name, (" " + detail) if detail else ""))


def read(rel):
    with open(os.path.join(HERE, rel), encoding="utf-8") as fh:
        return fh.read()


def git(*args):
    return subprocess.run(["git", "-C", LANE, *args], capture_output=True, check=True).stdout


# ---- gate runs -------------------------------------------------------------
r1, r2, r3 = read("receipts/01-gate-base-scope-ufo.txt"), read("receipts/02-gate-base-scope-all.txt"), read("receipts/03-gate-tip-scope-ufo.txt")
r4, r5, r6 = read("receipts/04-gate-47-sidecars-committed.txt"), read("receipts/05-gate-plus-3-pairs-scope-ufo.txt"), read("receipts/06-gate-rule-extensions-scope-all.txt")
check("base scope-ufo findings=159", "findings=159 rev=" + BASE in r1)
check("base scope-ufo waived=3", "SESSION_MATERIAL_WAIVED: findings=3 files=1" in r1)
check("base scope-all findings=167", "findings=167 rev=" + BASE in r2)
check("base scope-all rules 39/41/59/3/25",
      "R1_CLIENT_DUMP=39 R2_PROC_TABLE=41 R3_MONITOR_IDENT=59 R4_HOME_LISTING=3 R5_SERIAL_PROSE=25" in r2)
f1 = {ln for ln in r1.splitlines() if ln.startswith("FINDING")}
f3 = {ln for ln in r3.splitlines() if ln.startswith("FINDING")}
check("tip scope-ufo FINDING set identical (gate reads revisions)", f1 == f3 and len(f1) == 159)
check("47 sidecars: findings=110 waived=52", "findings=110" in r4 and "SESSION_MATERIAL_WAIVED: findings=52 files=48" in r4)
check("47 sidecars: 2 refusals, both rule-not-listed",
      len([ln for ln in r4.splitlines() if ln.startswith("WAIVER_REJECTED")]) == 2
      and all("reason=rule-not-listed" in ln for ln in r4.splitlines() if ln.startswith("WAIVER_REJECTED")))
check("+3 pairs: findings=107 waived=55", "findings=107" in r5 and "SESSION_MATERIAL_WAIVED: findings=55 files=51" in r5)
rej = [ln for ln in r6.splitlines() if ln.startswith("WAIVER_REJECTED")]
check("rule extensions: 7 refusals", len(rej) == 7, "got %d" % len(rej))
check("gate self-marker refused path-outside-waves",
      len([ln for ln in rej if "path-outside-waves" in ln]) == 3)
check("serial rule refused serial-rule-not-waivable",
      len([ln for ln in rej if "serial-rule-not-waivable" in ln]) == 1)

# ---- triage table ----------------------------------------------------------
rows = [ln.split("\t") for ln in read("triage.tsv").splitlines()[1:] if ln]
check("triage rows=167", len(rows) == 167, "got %d" % len(rows))
cls = {}
for _f, _r, c, k, _e in rows:
    cls.setdefault(k, [0, 0, set()])
    cls[k][0] += 1
    cls[k][1] += int(c)
    cls[k][2].add(_f)
check("class counts 40/52/48/27",
      [cls["REAL"][0], cls["SYNTHETIC"][0], cls["SYNTHETIC-NC"][0], cls["SYNTHETIC-GATE"][0]] == [40, 52, 48, 27])
check("no unclassified / no FP row", "UNCLASSIFIED" not in cls and "FALSE-POSITIVE" not in cls)
check("counted instances 1182", sum(v[1] for v in cls.values()) == 1182)
check("distinct files 140", len(set(r[0] for r in rows)) == 140)
check("REAL findings 851 / R2 rows 760 / R4 67 / R5 24",
      cls["REAL"][1] == 851
      and sum(int(r[2]) for r in rows if r[3] == "REAL" and r[1] == "R2_PROC_TABLE") == 760
      and sum(int(r[2]) for r in rows if r[3] == "REAL" and r[1] == "R4_HOME_LISTING") == 67
      and sum(int(r[2]) for r in rows if r[3] == "REAL" and r[1] == "R5_SERIAL_PROSE") == 24)

# ---- sidecars --------------------------------------------------------------
side = [ln.split("\t") for ln in read("sidecars-47.tsv").splitlines()[1:] if ln]
check("sidecars rows=47", len(side) == 47, "got %d" % len(side))
for col, name in ((2, "target tracked"), (3, "sha-match"), (5, "marker ok")):
    check("all 47 %s" % name,
          all((r[col] == "yes" if col == 2 else r[col] == "sha-match" if col == 3 else r[col] == "ok") for r in side))
check("all 47 registry row present", all(r[4].startswith("yes:") for r in side))
check("all 47 measured waiver non-none", all(r[6] != "waived=none" for r in side))
check("no sidecar problem", not any("MISMATCH" in r[3] or "MALFORMED" in r[5] for r in side))

# ---- lane facts (read-only git) -------------------------------------------
gate_now = git("cat-file", "blob", BASE + ":quality/check-session-material.py")
import hashlib
check("gate at base = 82c9053a", hashlib.sha256(gate_now).hexdigest() == GATE)
check("gate at tip = gate at base",
      hashlib.sha256(git("cat-file", "blob", TIP + ":quality/check-session-material.py")).hexdigest() == GATE)
reg = [ln for ln in git("show", BASE + ":quality/session-material-waivers.txt").decode().splitlines()
       if ln and not ln.startswith("#")]
check("registry rows=48 at base", len(reg) == 48, "got %d" % len(reg))
check("registry sha at tip = 4d007fe8",
      hashlib.sha256(git("cat-file", "blob", TIP + ":quality/session-material-waivers.txt")).hexdigest()
      .startswith("4d007fe8124523a1a8e2a021a182d5c65f0e99f74d3c69c7d3272289be12604e"))
copies = {
    ".ufo/waves/round-45/w1/ExecPrivacyGate/check-session-material.py": "889f8f057bf04fc76ed93dd7ee86e3b0bd9fc1dca3a6bfb712c672da4646e3fb",
    ".ufo/waves/round-48/w2/MutRoutedR3/receipts/out/old-gate-base.py": "889f8f057bf04fc76ed93dd7ee86e3b0bd9fc1dca3a6bfb712c672da4646e3fb",
    ".ufo/waves/round-47/w1/ExecSessionMarker/check-session-material.py": "a4a0a084e745f511048d5be445bed4959a18b5d64798a55da06c74cc0d08e9c9",
    ".ufo/waves/round-46/w1/ExecSerialRule/gate.py": "a36224e2aa9f1f86817f9a9b504d7389804b452003d29bbedc233f9997960ddf",
    ".ufo/waves/round-46/w1/ExecSessionTriage/check-session-material.py": "3fc480a40510c4038ea4f7db3d8fd76194d20e00732f17eb0adb2ac662e49cfa",
    ".ufo/waves/round-48/w1/ExecSessionMarker/check-session-material.py": GATE,
}
for path, want in copies.items():
    got = hashlib.sha256(git("cat-file", "blob", BASE + ":" + path)).hexdigest()
    check("copy digest " + path.split("/")[-1] + " @" + path.split("/")[3], got == want)
installed = sum(1 for ln in git("ls-files", "--others", "--exclude-standard").decode().splitlines()
                if ln.endswith(".synthetic"))
check("47 untracked sidecars in the lane", installed == 47, "got %d" % installed)
same = 0
for ln in git("ls-files", "--others", "--exclude-standard").decode().splitlines():
    if not ln.endswith(".synthetic"):
        continue
    a = open(os.path.join(LANE, ln), "rb").read()
    b = open(os.path.join(LANE, ".ufo/waves/round-48/w1/ExecSessionMarker/sidecars", ln), "rb").read()
    same += (a == b)
check("47/47 sidecars byte-identical to the round-48 install set", same == 47, "got %d" % same)

print("\nCLAIMS_CHECK passed=%d failed=%d" % (passed, failed))
sys.exit(0 if failed == 0 else 1)
