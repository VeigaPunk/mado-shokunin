import json, hashlib, os, sys
LANE = "/home/vgpnk/Projects/shokunin/mado-shokunin"
PIN = os.path.join(LANE, ".ufo/waves/round-55/fetch")
T = json.load(open(os.path.join(LANE, ".ufo/waves/round-55/frozen-tables.json"), encoding="utf-8"))
c1 = T["c1"]
rows = [("K", r) for r in c1["k"]] + [("H", r) for r in c1["h"]]

def sha(b): return hashlib.sha256(b).hexdigest()

# pin hashes
pin_status = {}
for name, want in c1["pin_sha256"].items():
    b = open(os.path.join(PIN, name), "rb").read()
    pin_status[name] = (sha(b) == want, len(b), b.count(b"\r\n"), b.count(b"\n"))

cache = {}
def lines_of(name):
    if name not in cache:
        raw = open(os.path.join(PIN, name), "rb").read()
        txt = raw.decode("utf-8", errors="strict")
        cache[name] = (txt.split("\n"), txt)
    return cache[name]

print("PIN HASHES (name, sha_ok, bytes, CRLF, LF):")
for k, v in pin_status.items():
    print(f"  {k}: sha_ok={v[0]} bytes={v[1]} crlf={v[2]} lf={v[3]}")
print()
print("ROWS: id | file | line | substring_at_line | line_occurrences_in_file | total_occurrences | char_len | byte_len | line_text_trunc")
bad = []
for kind, r in rows:
    pin = r["pin"]
    if kind == "K":
        fname = pin
    else:
        fname = pin
    if pin == "host-input.conf" or pin == "host-getoption.json":
        pass
    ls, txt = lines_of(pin)
    ln = r["line"]
    q = r["quote"]
    at = ls[ln-1] if 1 <= ln <= len(ls) else None
    sub_at = (at is not None and q in at)
    line_occ = sum(1 for l in ls if q in l)
    total_occ = txt.count(q)
    # also check the line the quote would be in if the stated line is wrong
    found_lines = [i+1 for i,l in enumerate(ls) if q in l]
    print(f"{r['id']} | {pin} | {ln} | {sub_at} | {line_occ} at {found_lines} | {total_occ} | {len(q)} | {len(q.encode())} | {at.strip()[:90] if at else None!r}")
    if not sub_at or line_occ != 1 or total_occ != 1:
        bad.append(r["id"])
print()
print("FAILS:", bad if bad else "none")
