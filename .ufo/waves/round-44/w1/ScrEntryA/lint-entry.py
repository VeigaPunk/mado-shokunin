#!/usr/bin/env python3
"""Seat-side lint of the drafted C2 entry: simulates the frozen counter's clauses
b, d (quote side), g and h against the draft and quotes.tsv, and prints every check."""
import hashlib, importlib.util, os, re, sys

LANE = "/home/vgpnk/Projects/shokunin/mado-shokunin"
FETCH = LANE + "/.ufo/waves/round-44/fetch"
SEAT = LANE + "/.ufo/waves/round-44/w1/ScrEntryA"
ENTRY = SEAT + "/hyprland-gkeep-size-request-r44.md"
COUNTER = LANE + "/quality/counters/c2-r44-gkeep-size-request.py"

spec = importlib.util.spec_from_file_location("c2r44", COUNTER)
c2 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(c2)

text = open(ENTRY, encoding="utf-8").read()
lines = c2.unfenced(text)

rows = []
with open(SEAT + "/quotes.tsv", encoding="utf-8") as f:
    next(f)
    for ln in f:
        i, q, fn, at, sha = ln.rstrip("\n").split("\t")
        rows.append((i, q, fn, int(at), sha))
blobs = {i: open(os.path.join(FETCH, fn), "rb").read() for i, q, fn, at, sha in rows}

fails = []
def chk(name, ok, detail=""):
    print(("PASS " if ok else "FAIL ") + name + (" :: " + detail if detail else ""))
    if not ok:
        fails.append(name)

# --- clause b: header window ---
head, fenced, later = [], False, []
for k, l in enumerate(text.splitlines()):
    if re.match(r"^\s{0,3}(```|~~~)", l):
        fenced = not fenced
        continue
    if not fenced:
        if k < 20:
            head.append(l)
        elif re.match(r"^(source|verified-at|recheck):", l):
            later.append((k + 1, l))
ids = []
for l in head:
    m = c2.SRC_RE.match(l)
    if m and m.group(1) not in ids:
        ids.append(m.group(1))
va = [l for l in head if l.startswith("verified-at:")]
rc = [l for l in head if l.startswith("recheck:")]
cited = set(re.findall(r"\b[Ss]\d{3,}\b", "\n".join(lines)))
ghosts = sorted(cited - set(ids))
chk("b.sources>=4", len(ids) >= 4, "ids=%s" % ids)
chk("b.verified-at once", len(va) == 1 and va[0].split(":", 1)[1].strip() == "2026-10-26", str(va))
chk("b.recheck once+valid", len(rc) == 1 and c2.recheck_ok(rc[0].split(":", 1)[1].strip()), str(rc))
chk("b.no key line after line 20", not later, str(later))
chk("b.no ghost ids", not ghosts, "ghosts=%s cited=%s" % (ghosts, sorted(cited)))
print("head lines 1..%d: %s" % (len(head), [l[:40] for l in head]))

# --- clause d quote side ---
for i, q, fn, at, sha in rows:
    nq = re.sub(r"\s+", " ", q)
    blob = blobs[i]
    d = hashlib.sha256(blob).hexdigest()
    got_at = c2.quote_at(blob, nq)
    occ = len(c2.occurrences(blob, nq))
    wc = len(q.split())
    others = [j for j in blobs if j != i and nq in c2.norm_receipt(blobs[j])]
    ok = (d == sha and got_at == at and occ == 1 and 3 <= wc <= 25
          and c2.quote_in_code(blob, nq, fn) and not others
          and (i == "S164" or c2.PINS.get(fn) == d))
    chk("d %s" % i, ok, "at=%s/%s occ=%d words=%d sha_ok=%s in_code=%s others=%s pin=%s"
        % (got_at, at, occ, wc, d == sha, c2.quote_in_code(blob, nq, fn), others,
           c2.PINS.get(fn) == d))

# --- clause g: one claim line per id, quote + locator; all id lines bound ---
entry_lines = [re.sub(r"\s+", " ", l) for l in lines
               if l not in ("gkeep client default_size=420x500 size_request_calls=0 application_id=org.omarchy.gkeep",
                            "hyprland sendWindowSize xdg_setSize=1 x11_configure=1")
               and not l.startswith("gkeep client ")
               and not l.startswith("hyprland sendWindowSize ")
               and not l.startswith("source:")]
for i, q, fn, at, sha in rows:
    nq = re.sub(r"\s+", " ", q)
    hits = [l for l in entry_lines if re.search(r"\b%s\b" % i, l)]
    claim = [l for l in hits if nq in l and ("%s:%d" % (fn, at)) in l
             and len(set(re.findall(r"\bS\d{3,}\b", l))) == 1]
    unbound = [l[:60] for l in hits if not (nq in l and ("%s:%d" % (fn, at)) in l)]
    chk("g %s" % i, len(claim) >= 1 and not unbound,
        "lines_naming_id=%d claim=%d unbound=%s" % (len(hits), len(claim), unbound))

# --- clause h: census lines exact, once each ---
want = ["gkeep client default_size=420x500 size_request_calls=0 application_id=org.omarchy.gkeep",
        "hyprland sendWindowSize xdg_setSize=1 x11_configure=1"]
for w in want:
    n = sum(1 for l in lines if l == w)
    chk("h census %r" % w[:30], n == 1, "exact lines=%d" % n)
# recompute with the counter's own parser against the pinned receipts
gates = {i: [(FETCH + "/" + fn, sha, q)] for i, q, fn, at, sha in rows}
raw = {i: blobs[i] for i, _, _, _, _ in rows}
h_ok, h_want = c2.host_census([i for i, _, _, _, _ in rows], {}, gates, raw, lines)
chk("h recomputation", h_ok, "counter wants %s" % h_want)

print("\nRESULT:", "ALL PASS" if not fails else "FAILURES: %s" % fails)
sys.exit(0 if not fails else 1)
