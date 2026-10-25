# CritVacuous — PRED-C1-r35-v1 is vacuous: right shape, junk content, TARGET_MET

Seat: critic (leaf, no dispatch). Date: 2026-10-24.
Question: does a tree with the correct *shape* but empty/junk *content* reach `TARGET_MET`?
**Answer: yes.** Construction under `.ufo/waves/round-35/scratch/CritVacuous/`.

## Verdict

```sh
$ python3 -I .ufo/waves/round-35/c1/count.py \
    --root .ufo/waves/round-35/scratch/CritVacuous \
    --frozen .ufo/waves/round-35/c1/frozen.json
PRED-C1-r35-v1 closed_entries=3 closed_rows=8 open_cites=0 verdict=TARGET_MET
exit=0
```

## The construction (12 files, zero knowledge)

- `corpus/SOURCES.md` — no header, no URLs. Eight rows of literal `junk` cells; each
  row's only load-bearing content is cell 5 `anchor:<frozen-sha256>` (a substring
  carrier), cell 7 `mined`, cell 9 `30d`, cell 10 the citing entry path.
- Three entries — each is **only** `gate-quote: S### <nonsense>` lines plus filler
  admitting nothing was observed or fetched. E.g.
  `corpus/knowledge/idle-lock-chain-armed-r14.md` is 30 bytes: `gate-quote: S205 snarfg plugh`.
- Eight receipts — ASCII noise, e.g. S204.receipt.txt in full:
  `garbage garbage garbage wump kvik garbage garbage garbage`.
  **None of the eight receipts matches its `frozen.json` sha256** (verified by
  `sha256sum`: e.g. S203 actual `f114cf88…` vs recorded `1b7fa87f…`).

## What the predicate fails to check

1. **Receipt content integrity — the named clause `digest-match` is text-only dead code.**
   `count.py:166` computes `digest = hashlib.sha256(blob).hexdigest()` and **never uses
   it**. The only anchor check (`count.py:189`) is `receipt["sha256"] in cs[5]` — a
   substring test of the *recorded* digest from `frozen.json` against row text. The row
   just repeats the registry's own digest; no comparison to the actual file bytes ever
   occurs. A receipt may contain anything — including a *different document* — as long
   as it contains the chosen quote. The clause ledger `c1/clauses.json` lists
   `digest-match` as live with control `c1-digest`, but that control mutates the row
   cell, not the file; no control can kill the receipt-content mismatch because none is
   asked to.

2. **Entry semantic content — entirely unchecked.** `gate_quote` (`count.py:127-135`)
   scans for lines starting `gate-quote: {sid} ` and returns the remainder. Nothing else
   in the entry is read: no topic check (unlike r24's `TOPIC_RE`), no claim-support
   check, no quote-to-claim anchoring, no minimum content. An entry consisting solely of
   its `gate-quote` lines passes. The quote itself is a *free variable* — I choose it,
   then embed it in my own junk receipt, so `quote in blob` is trivially satisfiable
   rather than an evidence anchor.

3. **Everything in the row besides cells 5,7,9,10 — unchecked.** Cells 0-4, 6, 8
   (id/date/source fields, URL, title, etc. in the real registry) are never read.
   `nf_ok` counts to 11 fields; their content beyond the four checked cells is free.
   Cell 5 needs only to *contain* the recorded digest string — `anchor:garbage<sha>` or
   the sha alone both pass.

4. **No provenance or freshness.** No URL resolution, no re-fetch (unlike r24's counted
   mode), no host observation, no requirement that the receipt predate or relate to the
   entry. The whole tree is self-referential: I authored rows, quotes, and receipts in
   one pass.

5. **No cross-file consistency beyond set equality.** `used-by == citing` (frozen.json's
   own admit list) — quoting the spec back at itself, not a check on the world.

## Root cause, one line

The predicate validates **shape** (file exists, row parseable, token sets equal,
substring membership) but never **grounds** any byte: the computed receipt digest is
discarded, and no clause connects entry prose, row provenance fields, or receipt origin
to anything outside the tree.

## Smallest repairs (each kills this construction)

- Compare the computed digest: `digest == receipt["sha256"]` (makes receipts
  content-pinned; then `sha256 in cs[5]` actually binds row→file).
- Require the entry to contain the quote **outside** the gate-quote line, or a claim
  line anchored to the quote — otherwise entries carry zero asserted content.
- Constrain cell 5 to an anchor grammar (e.g. `sha256:<hex>` exact) and validate the
  URL/title cells the census already parses (E09 covers recheck only).

## Scope note

This kills `TARGET_MET` as evidence that the idle-lock offer surface was measured: the
frozen cite set can be satisfied by a tree containing no observed fact about the bar
module, the menu entry, or the indicator. Golden still passes under all three repairs
above only if its receipts are byte-pinned (they are committed, so `digest ==` is
checkable).
