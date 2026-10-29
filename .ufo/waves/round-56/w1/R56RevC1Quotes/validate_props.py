import json, re, sys
TBL = "/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-56/frozen-tables.json"
RD = "/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-56/w1/R56RevC1Quotes/rows.md"
c = json.load(open(TBL))["c1"]
rows = {r["id"]: r for r in c["k"] + c["h"]}
pat = re.compile(r"^- (K\d{2}|H\d{2}) — MAX: (.+?) — NOT: (.+?) — FLAG: (.+)$")
seen = {}
bad = []
got = 0
for ln in open(RD, encoding="utf-8"):
    m = pat.match(ln.rstrip("\n"))
    if not m: continue
    got += 1
    rid, mx = m.group(1), m.group(2)
    r = rows[rid]
    minlen = 40 if rid.startswith("K") else 20
    probs = []
    if len(mx) < minlen: probs.append(f"len{len(mx)}<{minlen}")
    if "|" in mx or mx != mx.strip(): probs.append("pipe/ws")
    if mx in seen: probs.append("dup-of " + seen[mx])
    seen[mx] = rid
    qt = set(re.findall(r"[A-Za-z_][A-Za-z0-9_]{3,}", r["quote"]))
    mt = set(re.findall(r"[A-Za-z_][A-Za-z0-9_]{3,}", mx))
    if not (qt & mt): probs.append("tok")
    allowed = set(re.findall(r"[0-9]+", r["quote"])) | {"0","1","2","3"} | {str(r["line"])}
    if r["pin"].startswith("Hyprland"):
        allowed |= {str(x["line"]) for x in c["k"] if x["pin"] == r["pin"]}
    nums = re.findall(r"(?<![A-Za-z0-9_])[0-9]+(?![A-Za-z0-9_])", mx)
    bad_nums = [n for n in nums if n not in allowed]
    if bad_nums: probs.append("num:" + ",".join(bad_nums))
    print(rid, f"len={len(mx)}", "OK" if not probs else "FAIL " + " ".join(probs))
    if probs: bad.append(rid)
print("parsed", got, "of 33; failing:", bad or "none")
