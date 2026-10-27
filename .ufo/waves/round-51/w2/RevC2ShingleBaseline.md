# RevC2ShingleBaseline — C2 shingle replay

Axes: coverage + operability. Scope: independent replay of frozen C2 clause (c), including denominator/tokenizer/exclusions and an omitted candidate-bearing report example.

## Deliverables
- `.ufo/waves/round-51/w2/RevC2ShingleBaseline/shingle-replay.md` — independent replay calculations and evidence.

Report: `.ufo/waves/round-51/w2/RevC2ShingleBaseline/shingle-replay.md`

## Findings
- **PASS, literal frozen clause (c):** reran the counter at data revision `a0e34387b30538372a1bb219eb3ccdc74013d458`; it reproduces 66 base knowledge files + 3 candidate files, 2,900 unique entry 8-grams, max displayed overlap 0.1%, and TARGET_MET.
- **Scope limitation confirmed, not a literal predicate falsifier:** report `.ufo/waves/round-49/w1/ExecCounterC2/receipts/pos-entry.md` is outside `candidate/` and excluded; it has 976 unique 8-grams and 0 intersection with the current body (0/2,900). The w1 candidate body itself, also outside `candidate/`, is 98.8966% overlapping with the tested entry body; the counter excludes it as specified. See replay report for exact tokenizer, denominator, command, and pointers.
- Counter's one-decimal output does not disclose the exact max numerator; full independent per-reference numerator enumeration remains a verification gap, noted in the deliverable.
