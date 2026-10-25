#!/usr/bin/env python3
"""Independent re-derivation of PRED-C1-r35-v1 from bytes; no import of count.py.
Reports the predicate's three numbers twice:
  strictA = counter's reading (anchor carries frozen spec digest string)
  strictB = literal reading (anchor carries sha256 of the receipt bytes)
"""
import hashlib, json, os, re, stat, sys

ROOT = sys.argv[1]; FROZEN = sys.argv[2]
spec = json.load(open(FROZEN))
ROW = re.compile(r"^ {0,3}\|\s*(S[0-9]+)\s*\|")
ISO = re.compile(r"^\d{4}-\d{2}-\d{2}$"); CAD = re.compile(r"^\d+d$")
SYM = re.compile(r"^[A-Za-z][A-Za-z0-9 _-]*$")

def path_ok(rel):
    p = os.path.join(ROOT, rel)
    try:
        st = os.lstat(p)
        if not stat.S_ISREG(st.st_mode) or st.st_nlink != 1: return None
        real = os.path.realpath(p)
        if not real.startswith(os.path.realpath(ROOT) + os.sep) and real != os.path.realpath(ROOT): return None
        return open(p, 'rb').read()
    except OSError:
        return None

def cells(line):
    parts = line.split('|')
    if parts and parts[0] == '': parts = parts[1:]
    if parts and parts[-1] == '': parts = parts[:-1]
    return [x.strip() for x in parts]

sources_b = path_ok('corpus/SOURCES.md')
sources = sources_b.decode('utf-8', 'replace') if sources_b else ''
rows = {}
for ln in sources.splitlines():
    m = ROW.match(ln)
    if m: rows.setdefault(m.group(1), []).append(ln)

tally = {'A': {'closed_entries': 0, 'closed_rows': 0, 'open_cites': 0},
         'B': {'closed_entries': 0, 'closed_rows': 0, 'open_cites': 0}}
detail = []
for mode in ('A', 'B'):
    for rel, ids in spec['entries'].items():
        eb = path_ok(rel); eclosed = eb is not None
        e = eb.decode('utf-8', 'replace') if eb is not None else ''
        for sid in ids:
            blob = path_ok(spec['receipts'][sid]['path'])
            actual = hashlib.sha256(blob).hexdigest() if blob is not None else ''
            lines = [l for l in e.splitlines() if l.startswith(f"gate-quote: {sid} ")]
            quote = lines[0][len(f"gate-quote: {sid} "):] if len(lines) == 1 else None
            rws = rows.get(sid, []); row = rws[0] if len(rws) == 1 else None
            cs = cells(row) if row is not None else []
            ok = False
            if blob is not None and row is not None and len(cs) == 11:
                ub = {t.strip() for t in cs[10].split(',') if t.strip()}
                citing = {r for r, ri in spec['entries'].items() if sid in ri}
                anchor = cs[5]
                digest_ok = spec['receipts'][sid]['sha256'] in anchor
                if mode == 'B': digest_ok = digest_ok and actual in anchor
                ok = (ub == citing and cs[7] == 'mined'
                      and (ISO.match(cs[9]) or CAD.match(cs[9]) or SYM.match(cs[9]))
                      and digest_ok and quote is not None
                      and 1 <= len(quote.split()) <= 25 and quote.encode() in blob)
            if ok: tally[mode]['closed_rows'] += 1
            else:
                tally[mode]['open_cites'] += 1; eclosed = False
            if mode == 'A':
                detail.append({
                    'sid': sid, 'entry': rel,
                    'row_count': len(rws), 'cells': len(cs),
                    'anchor_has_frozen_digest': blob is not None and row is not None and len(cs) == 11 and spec['receipts'][sid]['sha256'] in cs[5],
                    'anchor_has_actual_digest': blob is not None and row is not None and len(cs) == 11 and actual in cs[5],
                    'receipt_digest_matches_freezer': actual == spec['receipts'][sid]['sha256'],
                    'quote_words': len(quote.split()) if quote is not None else None,
                    'quote_is_substring': bool(blob is not None and quote is not None and quote.encode() in blob),
                    'closed_counter_reading': ok,
                })
        if eclosed: tally[mode]['closed_entries'] += 1

for mode in ('A', 'B'):
    t = tally[mode]
    print(f"INDEPENDENT-C1 strict{mode} closed_entries={t['closed_entries']} "
          f"closed_rows={t['closed_rows']} open_cites={t['open_cites']}")
print("per-cite:", json.dumps(detail, indent=1))
print("sids_mentioned_in_entries:",
      sorted({m.group(0) for rel in spec['entries'] for m in re.finditer(r'S2[0-9]{2}', open(os.path.join(ROOT, rel)).read())}))
