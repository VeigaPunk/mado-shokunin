#!/usr/bin/env python3
"""Falsify22 driver: run the frozen C2 counter checks against the fixture entry,
then demonstrate the completeness gap (unmapped material factual proposition).

Checks replicated from the frozen predicate (claims-frozen.md / registration.md):
  1. at least four substantive propositions are declared
  2. each declared proposition maps to an opened-this-round S### row
  3. each declared proposition maps to a pin path whose bytes are present
  4. each declared proposition's located quote is <=25 words and verifies
     byte-exactly (whitespace-collapsed) inside the pinned file
  5. index row names the entry
Then:
  6. completeness scan: find material factual propositions in the body that are
     NOT in the declared map, and check one of them against the pinned truth.
"""
import os, re, sys

SEAT = os.path.dirname(os.path.abspath(__file__))
REPO = "/home/vgpnk/Projects/shokunin/mado-shokunin"
FETCH = os.path.join(REPO, ".ufo/waves/round-51/fetch")
ENTRY = os.path.join(SEAT, "fixture-entry.md")
README = os.path.join(SEAT, "fixture-README.md")
OPENED = {"S364", "S365", "S366", "S367", "S368", "S369"}
MAX_QUOTE_WORDS = 25

def collapse(s):
    return re.sub(r"\s+", " ", s).strip()

def table_after(lines, header):
    i = lines.index(header)
    rows = []
    started = False
    for ln in lines[i + 1:]:
        s = ln.strip()
        if s.startswith("|"):
            cells = [c.strip() for c in s.strip("|").split("|")]
            if all(re.fullmatch(r":?-{2,}:?", c or "") for c in cells):
                continue  # rule row
            if not started:
                started = True  # header row
                continue
            rows.append(cells)
        elif started:
            break
    return rows

def main():
    text = open(ENTRY).read()
    lines = text.splitlines()
    print("== frozen C2 counter checks (replicated) ==")

    rows = table_after(lines, "## Propositions")
    n = len(rows)
    c1 = n >= 4
    print(f"[1] proposition count: {n} declared -> {'PASS' if c1 else 'FAIL'} (need >=4)")

    ok2 = ok3 = ok4 = True
    for r in rows:
        pid, prop, row, pin, quote, rationale = r[:6]
        rowid = re.search(r"S\d{3,}", row)
        rowid = rowid.group(0) if rowid else None
        a = bool(rowid and rowid in OPENED)
        path = os.path.join(FETCH, pin + ".cpp") if not pin.endswith((".hpp", ".md")) else os.path.join(FETCH, pin)
        if not os.path.exists(path):
            path = os.path.join(FETCH, pin)
        b = os.path.exists(path)
        q = collapse(quote.strip("`"))
        w = len(q.split())
        c = w <= MAX_QUOTE_WORDS
        pinned = collapse(open(path).read()) if b else ""
        d = q in pinned
        ok2 &= a; ok3 &= b; ok4 &= c and d
        print(f"    {pid}: row={rowid} opened={'PASS' if a else 'FAIL'} "
              f"pin_present={'PASS' if b else 'FAIL'} quote_words={w} "
              f"<={MAX_QUOTE_WORDS}={'PASS' if c else 'FAIL'} quote_verifies={'PASS' if d else 'FAIL'}")

    index = open(README).read()
    c5 = "fixture-entry" in index
    print(f"[5] index row names entry: {'PASS' if c5 else 'FAIL'}")

    counter_pass = c1 and ok2 and ok3 and ok4 and c5
    print(f"counter verdict: {'TARGET_MET' if counter_pass else 'TARGET_MISSED'}")

    print()
    print("== completeness scan (the attacked clause) ==")
    # material factual proposition smuggled in Observations, outside the map:
    claim = "the socket verb lowercases the name before the table lookup"
    body = text.split("## Observations", 1)[1]
    present = claim in collapse(body)
    mapped = claim in collapse(" ".join("|".join(r) for r in rows))
    print(f"unmapped material factual proposition present in body: {present}")
    print(f"represented in declared proposition map:              {mapped}")

    # pinned-truth verdict on the smuggled claim:
    hyprctl = open(os.path.join(FETCH, "Hyprland-HyprCtl.cpp")).read().splitlines()
    seg = "\n".join(hyprctl[1142:1150])
    folds_in_socket = "tolower" in seg.lower() or "transform" in seg.lower()
    cfg = open(os.path.join(FETCH, "Hyprland-legacy-ConfigManager.cpp")).read()
    folds_in_parse = "std::ranges::transform(HANDLER, HANDLER.begin(), ::tolower);" in cfg
    print("pinned bytes HyprCtl.cpp:1143-1150 (socket path):")
    print(seg)
    print(f"socket path folds case: {folds_in_socket}  | bind parse path folds case: {folds_in_parse}")
    print(f"smuggled claim is FALSE per pinned bytes: {not folds_in_socket and folds_in_parse}")
    print(f"counter detected the unmapped false claim: {False}")
    print()
    print(f"RESULT: counter_pass={counter_pass} unmapped_false_claim_undetected={present and not mapped}")
    return 0

if __name__ == "__main__":
    sys.exit(main())
