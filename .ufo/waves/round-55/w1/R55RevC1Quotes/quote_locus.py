import json, os
LANE = "/home/vgpnk/Projects/shokunin/mado-shokunin"
PIN = os.path.join(LANE, ".ufo/waves/round-55/fetch")
T = json.load(open(os.path.join(LANE, ".ufo/waves/round-55/frozen-tables.json"), encoding="utf-8"))
rows = T["c1"]["k"] + T["c1"]["h"]
for r in rows:
    ls = open(os.path.join(PIN, r["pin"]), encoding="utf-8").read().split("\n")
    full = ls[r["line"] - 1]
    s = full.strip()
    q = r["quote"]
    i = full.index(q)
    before = full[:i].strip()
    after = full[i + len(q):].strip()
    kind = "WHOLE" if s == q else "PARTIAL"
    print(f"{r['id']} len={len(q)} {kind} line_len={len(s)} outside_before={before!r} outside_after={after!r}")
    print(f"   quote-line: {s}")
