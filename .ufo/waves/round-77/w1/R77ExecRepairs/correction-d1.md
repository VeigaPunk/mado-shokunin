# D1 — missing provenance trio in the two round-76 knowledge entries

Seat R77ExecRepairs, round 77, 2026-11-04. Lane HEAD `0fa69f41d81275db102bbe08cf5d6a86a5dfe8f7`.
Source dispositions: round-76 spot-check D1 (`corpus/lessons/round-76-verifier-spotcheck.md` §6)
and the round-77 declaration's routed-defect D1.

## Fact

`corpus/knowledge/outcome-field-r76.md` and `corpus/knowledge/interprocedural-del-r76.md` were
landed in round 76 without the CORPUS.md provenance trio every prior lane entry opens with
(`source:`, `verified-at:`, `recheck:`). Both cite their rows only in a closing `Sources:` line,
so a freshness sweep cannot read the fields.

Rows, as dispositioned: **S450/S455 for C1** and **S453/S454/S455/S456 for C2**.

## Landed state (verified at HEAD)

The append-only `## Correction (round 77)` blocks are already present, landed by
`3e35d0a9672b49cd1d908cf821c8a3c6e33e6696` (round-77 integration; 9 added lines per file):

    $ grep -n 'Correction (round 77)' corpus/knowledge/outcome-field-r76.md corpus/knowledge/interprocedural-del-r76.md
    corpus/knowledge/outcome-field-r76.md:112:## Correction (round 77)
    corpus/knowledge/interprocedural-del-r76.md:96:## Correction (round 77)

If a re-landing tree does not carry them, append the two blocks below verbatim at the end of each
file; never rewrite the entry body (append-only correction, per the spot-check fix).

## Block 1 — corpus/knowledge/outcome-field-r76.md

```markdown
## Correction (round 77)

This entry opens without the CORPUS.md provenance trio (round-76 closure defect D1). The fields,
supplied append-only and re-derived in round 77:

source: S450, S455
verified-at: 2026-11-04 (the round-76 counts re-derived from committed bytes; the entry's own numbers remain the round-76 receipts)
recheck: `python3 -I quality/counters/c1-r76-outcome-field.py --repo . --rev 3588a527eba555a94e497097b0467efc04274c6d --base-rev c3e0bc5f10b72964d54d18dc9b0706dc308dd1bf --controls .ufo/waves/round-76/controls/c1-outcome-cases-r76.json --scratch-root DIR`
```

## Block 2 — corpus/knowledge/interprocedural-del-r76.md

```markdown
## Correction (round 77)

This entry opens without the CORPUS.md provenance trio (round-76 closure defect D1). The fields,
supplied append-only and re-derived in round 77:

source: S453, S454, S455, S456
verified-at: 2026-11-04 (the round-76 counts re-derived from committed bytes; the entry's own numbers remain the round-76 receipts)
recheck: `python3 -I quality/counters/c2-r76-shapes.py --repo . --rev 3588a527eba555a94e497097b0467efc04274c6d --base-rev c3e0bc5f10b72964d54d18dc9b0706dc308dd1bf --controls .ufo/waves/round-76/controls/c2-cases-r76.json --scratch-root DIR`
```

## Fields and rows, named exactly

- `outcome-field-r76.md`: missing `source:` (S450 — CPython v3.14.8 `secrets.token_hex`, the
  caller-supplied challenge token and the child's echo; S455 — the call-parameter row) plus
  `verified-at:` and `recheck:` above. The entry's closing line records that S455's substantive
  citation sits in the sibling entry; the registry `used-by` agrees (S450 lists this entry,
  S455 lists `interprocedural-del-r76.md` only).
- `interprocedural-del-r76.md`: missing `source:` (S453 subscription deletion; S454 the copy
  constructor's keyword pairs; S455 the argument-in-slot row; S456 deleting an unbound name) plus
  `verified-at:` and `recheck:` above. Registry `used-by` for all four rows names this entry.
