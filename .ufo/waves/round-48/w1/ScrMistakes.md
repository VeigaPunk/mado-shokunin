# Seat ScrMistakes — round 48, w1 (BUILD)

**Deliverable.** `.ufo/waves/round-48/w1/ScrMistakes/mistakes.md` — rows M48-1..M48-5 (closure D1-D4 plus the
M47-7 capture) and drafts for QUALITY criteria 96-100, each with a runnable check, its failing input and a green
control. Seat instruments, controls, quotes and 15 receipts live in the same directory.

## Behavior

| row | class | input | red | green |
|---|---|---|---|---|
| M48-1 (D1) | `contract-narrowing` | `tools/mado-terminal.py` vs the freeze blob `762d042c…` | `added=3 unregistered=3 verdict=NARROWED` rc 1 | erratum registered, and no-delta: rc 0 |
| M48-2 (D2) | `unreceipted-number` | round-47 report vs every round-47 receipt (1598 files) | `tokens=11 missing=1` rc 1; the missing token is `findings=128`; criterion 69's own instrument returns PASS on the same bytes | number corrected to a receipted value: `missing=0` rc 0 |
| M48-3 (D3) | `routing` | 44 w2 + 41 w1 seat reports vs report and lesson | `finding_seats=7 unrouted=4` rc 1 (w2) and `unrouted=1` (w1) | four routing lines added: `unrouted=0` rc 0 |
| M48-4 (D4) | `locator` | the round-47 entry `xdg-terminal-selection-r47.md` | `locators=7 checked=4 violations=4` rc 1 (1 `UNK-HEAD-CUT`, 3 `AMBIGUOUS README.md`) | range corrected + README qualified: `checked=7 violations=0` rc 0 |
| M48-5 (M47-7) | `provider` | round-47 and round-48 `w1-spec.json` | `enforced=0 prose=4 verdict=PROSE-ONLY` rc 1 for both | dispatch carrying `ulimit -f 1024`: rc 0 |

Proposed criteria: **96** (landed contract not narrower than the frozen one), **97** (a report's count token carries
a committed receipt — extends 69), **98** (every seat reporting a frozen-instrument blind spot is routed by name),
**99** (a corpus-to-corpus locator resolves to one file and anchors its `[UNK]` item — extends 77), **100** (a wave's
scratch bound is enforced by the dispatch, not prose). Non-duplication is argued against 31, 34, 52, 61, 64, 69, 77,
90, 93 in `mistakes.md` § "Duplicate check", with the criteria's own lines cited.

Locator discipline: every `file:line` this seat writes is emitted by `verify-quotes.py` (37 located quotes, each
computed by grep, `differ=0`) and `verify-quotes.py --doc mistakes.md` reads the prose back against those receipts —
`locators=32 untyped=0 verdict=OK`. Both instruments are shown able to fail (one altered quote → `DIFFER`; one typed
locator → `UNTYPED`) in `receipts/instrument-bite.txt`.

## Gates

None run, by design: no lane counter, no registry gate, no fixture build, no resolver run, no `xkbcli`, no compositor
verb, no host cache write, no package transaction, no tool install, no clone. The only executions are this seat's own
five checkers, `verify-quotes.py`, and read-only `git show`/`git grep`/`sha256sum`/`grep`/`wc`. No report or pool
state was written outside the seat directory.

## Touched surfaces (all new; no tracked file edited)

`.ufo/waves/round-48/w1/ScrMistakes/{mistakes.md, check96.py, check97.py, check98.py, check99.py, check100.py,
verify-quotes.py, quotes.json, make-receipts.sh, controls/ (7 files), receipts/ (14 files)}` and this report
`.ufo/waves/round-48/w1/ScrMistakes.md`. Nothing else in the lane was written; nothing outside the lane was written
(the round-47 report was read only).

## Out of scope / not claimed

- I did not re-check the C1 warm-cache contract or the C2 entry content; only the closure's D-list and the earlier
  uncited classes.
- The criteria numbers (96-100) and their texts are drafts for the L1's freeze; this seat freezes nothing.
- Criterion 98's detection is by seat name, a proxy for routing (declared in the criterion text). The four unrouted
  seats are listed with their finding text so a reader can judge substantive routing without the proxy.
- Green controls are copies this seat made (`controls/`), not the round's own state.

## Findings against the closure

1. **D1 is confirmed and is partly a behaviour delta, not a wording one**: the FIFO refusal exists only in the landed
   bytes (`tools/mado-terminal.py:529`); HOME unset and the loop guard existed in the frozen bytes
   (`.ufo/waves/round-47/l1-draft/mado-terminal.py:407` = `tools/mado-terminal.py:410`), so the freeze under-declared
   it. `added=3 unregistered=3`.
2. **D2 is a recurrence of an existing criterion that is blind to its shape**: criterion 69 keys on `rev=` tokens and
   its instrument returns `PASS 1/1` on the report carrying `findings=128`.
3. **D3 is larger than one seat**: 4 of 7 w2 finding seats are unrouted (`ExecC1Determinism`, `MutC1Counter`,
   `MutC2Counter`, `RevengerCache`), and the w1 axis seat `ExecAxisBase` states "the operability axis is blind to
   `tools/`" with no routing either.
4. **D4 recurs from M46-6**, which was left captured-by none, and the same entry carries three more locators
   (`README.md:218`, `README.md:300-301`, `README.md:179-180`) that resolve to three different files.
5. **M47-7 is mined but uncaptured**: the lesson row exists, no criterion cites it (`grep -c M47-7 corpus/QUALITY.md`
   → 0), and this round's own dispatch still bounds scratch in prose (`enforced=0 prose=4`).

## Artifact paths

| path | what |
|---|---|
| `.ufo/waves/round-48/w1/ScrMistakes/mistakes.md` | the deliverable: rows, criteria, duplicate check, sweep, receipt index |
| `…/check96.py` … `check100.py` | one instrument per proposed criterion |
| `…/verify-quotes.py`, `…/quotes.json` | located-quote and locator-traceability verifier (37 quotes) |
| `…/make-receipts.sh` | reproduces every receipt below in one run |
| `…/controls/` | green controls (registered erratum, corrected report/entry, capped spec, mutant quotes, typed locator) |
| `…/receipts/d1-contract-delta.txt` | frozen/landed shas, contract diff, registration contract line, FIFO arm delta |
| `…/receipts/d2-report-number.txt` | report line, empty `git grep findings=128`, receipted siblings, criterion 69 PASS |
| `…/receipts/d3-routing.txt` | seat finding lines, `report=0 lesson=0` counts, closure's own routing |
| `…/receipts/d4-locator.txt` | cited lines, `check-locators locators=0`, the three README candidates |
| `…/receipts/m47-7-mined.txt` | lesson row, criteria citations, prose ceilings, `ulimit` counts |
| `…/receipts/check96-run.txt` … `check100-run.txt` | red and green for each proposed criterion |
| `…/receipts/near-duplicates.txt`, `unmined-sweep.txt` | the non-duplication evidence and the `captured-by: none` sweep |
| `…/receipts/quote-check.txt`, `doc-locators.txt`, `instrument-bite.txt` | 37/37 quotes OK, 32/32 locators traceable, both instruments shown able to fail |
