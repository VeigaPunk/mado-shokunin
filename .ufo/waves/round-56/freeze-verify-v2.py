#!/usr/bin/env python3
"""r56 freeze verifier v2 (also: allowlist sha256, frozen allowlist row count, stub presence). Run from the lane root. Proves: every pin and host capture hashes to its frozen sha256; every frozen K/H quote is a
single-line, pipe-free substring at its frozen line (and unique in its pin); every committed C2 fixture file matches the frozen fixture
table and the committed-fixture commitment; the frozen K table carries 30 K + 3 H rows. Prints FREEZE_VERIFY lines; exit 0 only if all hold."""
import hashlib, json, os, sys
W = ".ufo/waves/round-56"
T = json.load(open(f"{W}/frozen-tables-v2.json"))
bad = 0
def sha(p): return hashlib.sha256(open(p, "rb").read()).hexdigest()
def lines(p): return open(p, encoding="utf-8").read().split("\n")
c1 = T["c1"]
for f, h in list(c1["pin_sha256"].items()) + list(c1["host_pin_sha256"].items()):
    ok = sha(f"{W}/fetch/{f}") == h; bad += not ok; print(f"pin {f} {'ok' if ok else 'BAD'}")
for row in c1["k"] + c1["h"]:
    L = lines(f"{W}/fetch/{row['pin']}")
    q = row["quote"]
    ok = 0 < row["line"] <= len(L) and q in L[row["line"] - 1] and len(q) >= 10 and "|" not in q and "\n" not in q and sum(q in x for x in L) == 1
    bad += not ok; print(f"{row['id']} {row['pin']}:{row['line']} {'ok' if ok else 'BAD'}")
bad += len(c1["k"]) != 30 or len(c1["h"]) != 3
print(f"rows K={len(c1['k'])} H={len(c1['h'])}")
ent = []
root = f"{W}/fixtures/c2"
for dp, dn, fn in os.walk(root):
    for n in fn + [d for d in dn if os.path.islink(os.path.join(dp, d))]:
        p = os.path.join(dp, n); rel = os.path.relpath(p, root)
        ent.append((rel, "l", hashlib.sha256(os.readlink(p).encode()).hexdigest()) if os.path.islink(p) else (rel, "f", sha(p)))
ent.sort(key=lambda e: e[0].encode())
h = hashlib.sha256()
for rel, kind, d in ent: h.update(("%s\0%s\0%s\n" % (rel, kind, d)).encode())
ok = h.hexdigest() == T["c2"]["fixture_commit_sha256"]; bad += not ok; print(f"fixture commitment {'ok' if ok else 'BAD'} files={len(ent)}")
for rel, kind, d in ent:
    e = T["c2"]["fixture_files"].get(rel)
    if not e or e["kind"] != kind or e["sha256"] != d: bad += 1; print("fixture file BAD", rel)
ids = sorted({r.split("/")[0] for r, _, _ in ent if r.split("/")[0].startswith("F")})
ok = len(ids) == 18; bad += not ok; print(f"fixture dirs {len(ids)}")
al = T["c3"]
ok = sha(f"{W}/c3-name-only.tsv") == al["allowlist_sha256"] and sum(1 for _ in open(f"{W}/c3-name-only.tsv")) == al["exempt"]; bad += not ok; print(f"c3 allowlist {'ok' if ok else 'BAD'} rows={al['exempt']}")
ok = os.path.isfile(f"{W}/ctl/sibling-reader.py"); bad += not ok; print(f"ctl/sibling-reader.py {'ok' if ok else 'BAD'}")
print(f"FREEZE_VERIFY_V2: bad={bad} frozen-tables.sha256={sha(f'{W}/frozen-tables-v2.json')} {'OK' if not bad else 'FAIL'}")
sys.exit(1 if bad else 0)
