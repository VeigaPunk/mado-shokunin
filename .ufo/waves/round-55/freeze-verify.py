#!/usr/bin/env python3
"""r55 freeze verifier: every frozen quote sits at its frozen line of its pin, every pin hashes to its frozen sha256,
every committed C2 fixture file hashes to its frozen sha256. Run from the lane root. Prints FREEZE_VERIFY lines; exit 0 only if all hold."""
import hashlib, json, os, sys
LANE = os.getcwd()
W = ".ufo/waves/round-55"
T = json.load(open(f"{W}/frozen-tables.json"))
bad = 0
def sha(p): return hashlib.sha256(open(p, "rb").read()).hexdigest()
def lines(p): return open(p, encoding="utf-8").read().split("\n")
for f, h in T["c1"]["pin_sha256"].items():
    ok = sha(f"{W}/fetch/{f}") == h
    bad += not ok
    print(f"pin {f} {'ok' if ok else 'BAD'}")
for row in T["c1"]["k"] + T["c1"]["h"]:
    L = lines(f"{W}/fetch/{row['pin']}")
    ok = 0 < row["line"] <= len(L) and row["quote"] in L[row["line"] - 1] and len(row["quote"]) >= 10
    bad += not ok
    print(f"{row['id']} {row['pin']}:{row['line']} {'ok' if ok else 'BAD'}")
c3 = T["c3"]
okp = sha(c3["pin"]) == c3["pin_sha256"]; bad += not okp
print(f"c3 pin {'ok' if okp else 'BAD'}")
L = lines(c3["pin"])
for row in c3["q"]:
    ok = L[row["line"] - 1].strip() == row["quote"]
    bad += not ok
    print(f"{row['id']} :{row['line']} {'ok' if ok else 'BAD'}")
for d, files in T["c2"]["fixture_file_sha256"].items():
    for f, h in files.items():
        ok = sha(f"{W}/fixtures/c2/{d}/{f}") == h
        bad += not ok
        if not ok: print(f"fixture {d}/{f} BAD")
print(f"fixtures {len(T['c2']['fixture_file_sha256'])} dirs checked")
print(f"FREEZE_VERIFY: bad={bad} frozen-tables.sha256={sha(f'{W}/frozen-tables.json')} {'OK' if not bad else 'FAIL'}")
sys.exit(1 if bad else 0)
