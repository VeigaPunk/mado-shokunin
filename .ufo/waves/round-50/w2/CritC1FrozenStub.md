# CritC1FrozenStub — w2 falsify of PRED-C1-r50

## Verdict

1. **c13 control re-verified: HOLDS.** The r49-paste do-nothing misses on the frozen counter,
   byte-for-byte the same clause vector as `receipts/controls-c1.txt`
   (`a:1 b:1 c:1 d:1 e:1 f:0 g:1 h:1 i:1 j:1 r:0 admitted=0/1 verdict=TARGET_MISSED rc=1`).
2. **REAL DEFECT found: the frozen counter admits a cheaper do-nothing.** The round-49
   candidate bytes — which sit in the base tree at
   `.ufo/waves/round-49/candidate/hyprland-bind-key-match-r49.md` (committed via `dd2e827e`,
   present at base `8ae47b95`) — pasted at the round-50 entry path pass every clause except
   f/r, and a **single-line, ~10-word insertion** naming `.ufo/waves/round-50/receipts/
   binds-live-r50.txt` flips the verdict to `TARGET_MET`. Both variants admitted:
   - `v4-r49-recycle` `ad66a6b4…` (one 5-line receipt-citation sentence added): all 11
     clauses 1, `admitted=1/1 verdict=TARGET_MET rc=0`.
   - `v4b-minimal` `a285d153…` (one-line insertion, diff in `v4b-entry-diff.txt`): all 11
     clauses 1, `admitted=1/1 verdict=TARGET_MET rc=0`.
   The freeze's c13 control ("the do-nothing that skips writing the new entry cannot reach
   the target") therefore holds by ~10 words.

## Exact clause gap

- Clause **f** binds the entry to the receipt only through the receipt's *values*
  (binds=192, named=142 code=42 mouse=6 switch=2, resolve int=0, digest
  `9a47199e2297…`). The host bind plane is byte-stable across rounds — the round-50 receipt
  restates the round-49 values exactly — so last round's prose still agrees.
- Clause **r** replays the live capture and compares to the receipt; it binds the entry to
  the *current* host state, never to round-50 work (`replay=ok` for the recycled text).
- Clause **i**'s novelty probe compares shingles only against `corpus/knowledge` +
  `corpus/lessons` at base, and the dup-grep covers `corpus/` only; prior-round candidate
  bytes under `.ufo/` are invisible to it (recycled text reads `overlap=0.014 dup=0`).
- No clause measures round-over-round freshness of the entry body: nothing rejects an entry
  that is a prior-round candidate plus a receipt citation.

The counter is strict elsewhere (so this is a fixable freshness hole, not general
weakness): `v2-no-quotes` (real entry, every backticked quote span stripped) MISSES
(`e:0 j:0 i:0` — quote-grounded steps and the ground tuple vanish), and `v3-wrong-usedby`
(rows S352-S363 used-by repointed at a different new file) MISSES (`b:0 used=0` on all ten
rows). Quoting and used-by binding are enforced; freshness is not.

## Smallest safe correction

Add a freshness check to clause i (or as a new clause): compute the entry's similarity
(shingles, the probe's own unit) against every `corpus/knowledge/hyprland-bind-key-match-r*.md`
**and** every `.ufo/waves/round-*/candidate/*.md` present at base, and fail above a small
threshold (the honest round-50 entry differs from the r49 candidate by 44 diff lines out of
~135, i.e. ~2/3 of its lines carry over; a recycled-with-10-words entry is ~99% identical).
Value-only binding in f cannot be hardened — the receipt values legitimately repeat while
the host state is unchanged.

## Method (all evidence under this seat dir)

- Counter run read-only from the lane; scored on a `git clone -q --shared` of the lane under
  scratch (deleted after receipts were copied). Counter sha256
  `e162d6717915f5585c40853afa8223d0398e50f0de37da4fd02004d2b08a84c0` = freeze registration.
- TMPDIR under scratch (outside the scored clone, as the counter demands); live replay used
  the read-only `hyprctl binds -j` / `getoption` path with HOME/XDG_* sandboxed by the
  counter itself; no host mutation, no subagents, no installs.
- Fixture revs and full receipts: `fixture-revs.txt`, `receipts/*.txt` in this seat dir.

## Deliverables

- `receipts/c13-rebuild.txt` — control re-verification (MISSED, matches freeze).
- `receipts/v4-r49-recycle.txt`, `receipts/v4b-minimal.txt` — wrongly-admitted do-nothings.
- `receipts/v2-no-quotes.txt`, `receipts/v3-wrong-usedby.txt` — counter strictness probes.
- `v4b-entry-diff.txt` — the entire ~10-word delta that reaches TARGET_MET.
- `fixture-revs.txt` — fixture construction and revs.
