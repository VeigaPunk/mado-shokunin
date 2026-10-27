#!/usr/bin/env python3
"""Seat-local conjunct test: does the quoted bytes even mention each conjunct?

Splits each proposition at '; ' and ' and ' into conjuncts, tokenises the quote and the
conjunct, and reports conjuncts whose token overlap is below the stated threshold.
This is a *measurement*, not an entailment proof: it only shows that a conjunct has no
lexical footprint in the quote the frozen predicate accepts.
"""
import re, sys
sys.path.insert(0, '/fast/scratch/hyaku/mado-r52/Falsify05')
import c2ref

THRESHOLD = 0.34
TOK = re.compile(r"[A-Za-z0-9_]{2,}")

def toks(s):
    return {t.lower() for t in TOK.findall(c2ref.collapse(s))}

def conjuncts(prop):
    parts = re.split(r";\s*|\s+and\s+|\s+but\s+", prop)
    return [p.strip(" .") for p in parts if len(c2ref.words(p)) >= 3]

def main(path, root):
    lines = c2ref.read_lines(path)
    header, low, rows, idx = c2ref.prop_table(lines)
    pidx, qidx = idx
    ridx = next((i for i in range(len(low)) if i not in (pidx, qidx)
                 and low[i] in ("row", "s-row", "srow")), None)
    man = c2ref.manifest(lines)
    pins = c2ref.pin_index(root)
    flagged = 0
    for _n, cells in rows:
        prop = cells[pidx]
        quote = cells[qidx].strip().strip("`").strip()
        qt = toks(quote)
        for c in conjuncts(prop):
            ct = toks(c)
            if not ct:
                continue
            j = len(ct & qt) / len(ct)
            if j < THRESHOLD:
                flagged += 1
                print("FLAG overlap=%.2f conjunct=%r" % (j, c))
                print("           quote=%r" % quote)
    print("flagged_conjuncts=%d rows=%d threshold=%.2f" % (flagged, len(rows), THRESHOLD))

if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
