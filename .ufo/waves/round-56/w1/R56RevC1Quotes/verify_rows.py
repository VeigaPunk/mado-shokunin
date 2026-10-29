import json, hashlib, os, re, subprocess, sys
LANE = "/home/vgpnk/Projects/shokunin/mado-shokunin"
PIN = LANE + "/.ufo/waves/round-56/fetch"
TBL = LANE + "/.ufo/waves/round-56/frozen-tables.json"
WORK = "/fast/scratch/hyaku/mado-r56/R56RevC1Quotes"
FREEZE = "3423ae285676c2a10273000f4519163472b443db"
t = json.load(open(TBL, encoding="utf-8"))
c = t["c1"]
rows_map = c["rows"]
out = []
def P(*a):
    out.append(" ".join(str(x) for x in a))

P("== tables sha256 ==")
P(hashlib.sha256(open(TBL, "rb").read()).hexdigest())
P("== pin files: working tree sha vs frozen; committed blob at freeze vs working tree ==")
for name, want in list(c["pin_sha256"].items()) + list(c["host_pin_sha256"].items()):
    data = open(os.path.join(PIN, name), "rb").read()
    got = hashlib.sha256(data).hexdigest()
    try:
        blob = subprocess.run(["git", "-C", LANE, "show", f"{FREEZE}:{c['pin_dir']}/{name}"], capture_output=True, check=True, env={"PATH": "/usr/bin:/bin", "HOME": WORK, "TMPDIR": WORK}).stdout
        cg = hashlib.sha256(blob).hexdigest()
        cmt = "committed=ok" if cg == want else "committed=MISMATCH"
    except subprocess.CalledProcessError as e:
        cmt = "committed=absent"
    P(f"{name}: wt={'ok' if got==want else 'MISMATCH'} {cmt}")

def lines_of(name):
    return open(os.path.join(PIN, name), "rb").read().split(b"\n")

def count_nonoverlap(hay, needle):
    n = 0; i = 0
    while True:
        j = hay.find(needle, i)
        if j < 0: return n
        n += 1; i = j + 1

P("")
P("== row checks: id | pin | sid->pin | line | quote-on-line | file-occurrences | lines-containing | pipe | ws ==")
allrows = [("K", r) for r in c["k"]] + [("H", r) for r in c["h"]]
fails = []
for kind, r in allrows:
    rid = r["id"]; pin = r["pin"]; q = r["quote"]; ln = r["line"]
    qb = q.encode("utf-8")
    L = lines_of(pin)
    full = open(os.path.join(PIN, pin), "rb").read()
    on_line = (1 <= ln <= len(L)) and (qb in L[ln-1])
    occ = count_nonoverlap(full, qb)
    lines_with = sum(1 for x in L if qb in x)
    pipe = "|" in q
    ws = (q != q.strip()) or ("\t" in q) or ("\\" in q)
    if kind == "K":
        sid = r["sid"]
        smap = "ok" if rows_map.get(sid) == pin else f"BAD(rows[{sid}]={rows_map.get(sid)})"
        smap = f"{sid}->{smap}"
    else:
        smap = "host"
    ok = on_line and occ == 1 and lines_with == 1 and not pipe and not ws and (kind=="H" or smap.endswith("ok"))
    if not ok: fails.append(rid)
    P(f"{rid} {pin}:{ln} line_has={on_line} occ={occ} lines={lines_with} pipe={pipe} ws={ws} sid={smap} len={len(q)}")
    if kind == "K" or True:
        P(f"    LINE: {L[ln-1].decode('utf-8','replace') if 1<=ln<=len(L) else '<OUT OF RANGE>'}")
P("")
P("K rows:", sum(1 for k,_ in allrows if k=='K'), "H rows:", sum(1 for k,_ in allrows if k=='H'))
P("sid set used by K:", sorted(set(r['sid'] for r in c['k'])), "new_row_ids", c['new_row_ids'])
P("rows registry map covers new ids:", all(x in rows_map for x in c['new_row_ids']))
P("FAILS:", fails or "none")
open(WORK + "/rows-check.txt", "w", encoding="utf-8").write("\n".join(out) + "\n")
print("\n".join(out))
