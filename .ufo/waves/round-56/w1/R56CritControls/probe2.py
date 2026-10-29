import json, re, os
W="x/.ufo/waves/round-56"
T=json.load(open(f"{W}/frozen-tables.json"))
c1=T["c1"]
pins={}
for f in c1["pin_sha256"]:
    pins[f]=open(f"{W}/fetch/{f}",encoding="utf-8",errors="replace").read().split("\n")
for f in c1["host_pin_sha256"]:
    pins[f]=open(f"{W}/fetch/{f}",encoding="utf-8",errors="replace").read().split("\n")
# 1. Control 3 discriminator: is "200" present in same pin (pin-wide digit loosening would admit it)?
for f,L in pins.items():
    hits=[(i+1,l.strip()[:90]) for i,l in enumerate(L) if re.search(r"(?<![0-9])200(?![0-9])",l)]
    if hits: print("200 in",f,len(hits),hits[:3])
print("control3 number 200 search done")
# 2. digits of frozen quotes+lines: which K quotes contain numeric runs
for row in c1["k"]+c1["h"]:
    d=re.findall(r"(?<![A-Za-z0-9_])[0-9]+(?![A-Za-z0-9_])",row["quote"])
    if d: print("quote digits",row["id"],d)
# 3. tokens in placeholder propositions vs quotes (control 2 tok discriminator)
def toks(s): return set(re.findall(r"[A-Za-z_][A-Za-z0-9_]{3,}",s))
hits_per={}
for row in c1["k"]+c1["h"]:
    ph = (f"placeholder proposition text for row {row['id']}, not a claim about any source line" if row["id"].startswith("K")
          else f"placeholder host proposition {row['id']}, not a read")
    shared = toks(ph) & toks(row["quote"])
    hits_per[row["id"]]=sorted(shared)
print("placeholder tok overlap rows with overlap:", {k:v for k,v in hits_per.items() if v})
print("placeholder len K/H min ok:", all(len(f"placeholder proposition text for row {r['id']}, not a claim about any source line")>=40 for r in c1['k']), all(len(f"placeholder host proposition {r['id']}, not a read")>=20 for r in c1['h']))
# 4. K quotes length vs 40-char minimum for proposition (copy-the-quote cheapest entries)
print("quotes shorter than 40 chars:", [(r["id"],len(r["quote"])) for r in c1["k"] if len(r["quote"])<40])
# 5. quote-as-proposition: uniqueness and tok self-overlap => passes tok trivially
print("quote-as-proposition self tok overlap always true when quote has an identifier of len>=4:",
      all(toks(r["quote"]) for r in c1["k"]+c1["h"]))
# 6. Distinct-sid check for control 4: K10 frozen sid
print("K10 sid", [r["sid"] for r in c1["k"] if r["id"]=="K10"], "pin", [r["pin"] for r in c1["k"] if r["id"]=="K10"])
# 7. Which rows share pin ConfigWatcher and their lines (num allowed set)
cw=sorted(r["line"] for r in c1["k"]+c1["h"] if r["pin"]=="Hyprland-ConfigWatcher.cpp")
print("ConfigWatcher frozen lines:",cw)
# 8. control 9 pin byte: is there a pin-byte mutation that is invisible to quotes? check ConfigWatcher length, and a byte in a line that is never quoted
L=pins["Hyprland-ConfigWatcher.cpp"]
quoted={r["line"] for r in c1["k"] if r["pin"]=="Hyprland-ConfigWatcher.cpp"}
print("ConfigWatcher lines total",len(L),"unquoted lines count",len(L)-len(quoted))
# 9. control 6 & 10: confirm S-ids
print("new_row_ids", c1["new_row_ids"], "rows", c1["rows"])
# 10. H rows vs host pins: quote in host pin (host:<id>) — check each H quote occurs in its host pin
for r in c1["h"]:
    print(r["id"], r["pin"], "quote-in-pin-line", r["quote"] in pins[r["pin"]][r["line"]-1])
