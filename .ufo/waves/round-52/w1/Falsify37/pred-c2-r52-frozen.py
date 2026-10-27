#!/usr/bin/env python3
"""PRED-C2-r52-frozen (seat Falsify37 fixture checker).

Implements exactly the checkable predicates the frozen round-52 C2 claim puts
under counter enforcement (registration.md, C2):

  "a new committed counter checks proposition count, row/pin/quote bindings and
   complete mapping"

and nothing more - per the claim's own disclaimer, "This is not automated
semantic-entailment proof". The quote-binding half reuses the lane's PRODUCTION
binding code (quality/counters/c2-r51-dispatch-entry.py: bind_row, manifest,
registry, quote_candidates, tables, shingles, clause_a/b/c/d) unmodified, so the
demonstration is "the lane's own binding predicate admits this fixture", not
"my reimplementation admits it".

Clauses:
  a  entry present + README index row names it          (production clause_a)
  b  source rows bound to pins at verifying quotes      (production clause_b)
  p  proposition count >= 4; each declared proposition maps to an opened-this-
     round S-row, a manifest pin present at rev, a located quote <= 25 words
     verbatim in the pinned bytes at the cited line, and a non-empty written
     support rationale; complete mapping over every declared proposition
     (structural only - the frozen predicate's checkable half)
  c  novelty shingle overlap vs base knowledge          (production clause_c)
  d  held citations resolve at base                     (production clause_d)

Verdict TARGET_MET iff a,b,p,c,d all pass.
"""
import importlib.util
import json
import os
import re
import sys

sys.dont_write_bytecode = True  # never write __pycache__ into the lane tree

LANE = "/home/vgpnk/Projects/shokunin/mado-shokunin"
COUNTER = LANE + "/quality/counters/c2-r51-dispatch-entry.py"

spec = importlib.util.spec_from_file_location("prod", COUNTER)
prod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(prod)

# fixture target: the adversarial entry replaces the r51 entry
prod.ENTRY = "corpus/knowledge/hyprland-dispatcher-entail-bypass-r52.md"
prod.ENTRY_NAME = "hyprland-dispatcher-entail-bypass-r52.md"
# ROW_MIN/ROW_MAX (364-379), OPENED (2026-10-27), FETCH_ROOT, REGISTRY, README,
# MIN_ROWS, MAX_QUOTE_WORDS stay at production values - they match this round.

ENTRY = prod.ENTRY
OPENED = prod.OPENED
MIN_PROPS = 4


def load_registry(repo, rev):
    return prod.registry(prod.text_of(prod.show(repo, rev, prod.REGISTRY)))


def load_manifest(entry_text):
    return prod.manifest(entry_text)


def pins_at(repo, rev):
    return {p.rsplit("/", 1)[-1] for p in prod.ls_files(repo, rev, prod.FETCH_ROOT)}


def make_loader(repo, rev, cache):
    def loader(name):
        if name not in cache:
            cache[name] = prod.show(repo, rev, prod.FETCH_ROOT + "/" + name)
        return cache[name]
    return loader


def parse_propositions(entry_text):
    """Declared propositions from the ## Propositions table: [(pid, cells, raw_line)]."""
    out, in_sec = [], False
    for line in entry_text.splitlines():
        if line.startswith("## "):
            in_sec = line.strip().lower() == "## propositions"
            continue
        if not in_sec or not line.strip().startswith("|"):
            continue
        cells = prod.cells_of(line)
        if prod.is_rule(cells) or not cells:
            continue
        if re.fullmatch(r"P\d+", prod.clean(cells[0])):
            out.append((prod.clean(cells[0]), cells, line))
    return out


def clause_p(repo, rev, entry_text, reg, man, at_rev, loader):
    """Proposition count + row/pin/quote bindings + complete mapping (structural)."""
    props = parse_propositions(entry_text)
    notes, details = [], []
    if len(props) < MIN_PROPS:
        return 0, "propositions=%d<%d" % (len(props), MIN_PROPS), []

    low_header = [prod.clean(c).lower() for c in
                  prod.cells_of([l for l in entry_text.splitlines()
                                 if l.strip().startswith("|") and "proposition" in l.lower()][0])]
    i_row = low_header.index("row")
    i_pin = low_header.index("pin")
    i_quote = low_header.index("quote")
    i_loc = low_header.index("locator")
    i_rat = low_header.index("supportrationale")

    bound = 0
    for pid, cells, raw in props:
        why = []
        rowid = prod.clean(cells[i_row]) if i_row < len(cells) else ""
        pin = prod.pin_cell(cells[i_pin]) if i_pin < len(cells) else ""
        quote = prod.cells_of(raw)[i_quote] if i_quote < len(cells) else ""
        loc = prod.clean(cells[i_loc]) if i_loc < len(cells) else ""
        rat = cells[i_rat].strip() if i_rat < len(cells) else ""

        m = re.fullmatch(r"S\d{3,}", rowid)
        row = reg.get(rowid) if m else None
        if row is None:
            why.append("row_invalid")
        elif prod.clean(row.get("status", "")).lower() != "mined":
            why.append("row_status")
        elif prod.clean(row.get("opened", "")) != OPENED:
            why.append("row_opened")

        if pin not in man:
            why.append("pin_unmapped")
        elif pin not in at_rev:
            why.append("pin_absent_at_rev")

        quote_txt = ""
        qm = prod.BACKTICK_RE.search(quote or "")
        if qm:
            quote_txt = qm.group(1)
        elif (qm := prod.DQUOTE_RE.search(quote or "")):
            quote_txt = qm.group(1)
        n_words = len(prod.words(quote_txt)) if quote_txt else 999
        if not quote_txt or n_words > prod.MAX_QUOTE_WORDS:
            why.append("quote_len:%d" % n_words)

        loc_ok = False
        lm = prod.LOC_RE.search(loc or "")
        if lm and pin:
            span = prod.at_lines(loader(pin), int(lm.group(2)),
                                 int(lm.group(3)) if lm.group(3) else int(lm.group(2)))
            if span is not None and prod.collapse(quote_txt) in prod.collapse(span):
                loc_ok = True
        if not loc_ok:
            why.append("quote_not_at_locator")

        if len(prod.words(rat)) < 5:
            why.append("rationale_thin")

        # production cross-check: the lane's own bind_row on this very line
        prod_bound, prod_why = prod.bind_row(rowid, [raw], man, at_rev, loader)
        cross = "prod_bind=ok" if prod_bound else "prod_bind=%s" % prod_why

        if why:
            notes.append("%s=%s" % (pid, ",".join(why)))
        else:
            bound += 1
        details.append("%s row=%s pin=%s quote_words=%d locator=%s rationale_words=%d %s"
                       % (pid, rowid, pin, n_words, loc, len(prod.words(rat)), cross))

    complete = bound == len(props)
    ok = 1 if (bound >= MIN_PROPS and complete) else 0
    detail = "propositions=%d mapped=%d/%d complete=%s" % (len(props), bound, len(props), complete)
    if notes:
        detail += " miss=" + ",".join(notes)
    return ok, detail, details


def main(argv):
    repo = os.path.abspath(argv[0])
    rev = prod.resolve_rev(repo, argv[1])
    base = prod.resolve_rev(repo, argv[2])
    work = argv[3]
    entry_blob = prod.show(repo, rev, ENTRY)
    if entry_blob is None:
        print("P_C2_R52: entry absent at rev")
        return 1
    entry_text = prod.text_of(entry_blob)

    reg = load_registry(repo, rev)
    man = load_manifest(entry_text)
    at_rev = pins_at(repo, rev)
    cache = {}
    loader = make_loader(repo, rev, cache)

    a, _, adet = prod.clause_a(repo, rev)
    print("P_C2_R52: a ok=%d %s" % (a, adet if len(adet) < 80 else adet[:77] + "..."))

    b, bdet = prod.clause_b(repo, rev, entry_text)
    print("P_C2_R52: b ok=%d %s" % (b, bdet))

    p, pdet, pdetails = clause_p(repo, rev, entry_text, reg, man, at_rev, loader)
    print("P_C2_R52: p ok=%d %s" % (p, pdet))
    for d in pdetails:
        print("P_C2_R52:   %s" % d)

    c, cdet, _ = prod.clause_c(repo, rev, base, entry_text)
    print("P_C2_R52: c ok=%d %s" % (c, cdet))

    base_kn = prod.knowledge_at_base(repo, base)
    d, ddet, _ = prod.clause_d(repo, base, entry_text, base_kn)
    print("P_C2_R52: d ok=%d %s" % (d, ddet))

    met = a + b + p + c + d
    admitted = 1 if met == 5 else 0
    record = {"pred": "P-C2-r52-frozen", "rev": rev, "base": base, "entry": ENTRY,
              "a": a, "b": b, "p": p, "c": c, "d": d,
              "clauses_met": met, "admitted": admitted}
    with open(os.path.join(work, "pred-c2-r52-frozen.json"), "w") as fh:
        json.dump(record, fh, indent=1, sort_keys=True)
    print("P_C2_R52: clauses=abpcd clauses_met=%d admitted=%d/1 verdict=%s rev=%s"
          % (met, admitted, "TARGET_MET" if admitted else "TARGET_MISSED", rev))
    return 0 if admitted else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
