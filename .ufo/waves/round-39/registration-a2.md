# mado round 39 — attempt-2 freeze addendum (before any attempt-2 data commit)

Attempt 2 (L1 `MadoR39a2`) inherits attempt 1's freeze commit `457d1b1` (registration.md,
C1 manifest, base receipts) and its dispatched wave `w1` (64 seats, ready file
`l1=MadoR39`; the attempt-1 L1 ended mid-round with no data commit). registration.md is not
edited. This addendum lands in its own commit before the tool, the entry, the rows or any
other data for C2/C3.

## What the attempt-1 freeze did not freeze

registration.md declares C2's predicate as "the docstring of
`quality/counters/c3-r39-options.py`" and C3's as "the docstring of
`quality/counters/c4-r39-options-entry.py`", but neither file was in the freeze commit:

- the C2 counter was written by seat ExecOptionsCounter after dispatch (draft
  `PRED-C3-r39-v1`, sha256 `16544cbd…1c35`, preserved byte-exact as
  `c2/c3-r39-options.v1-draft.py.txt`); seats CritC2Control and RevC2Counter scored it
  and showed it cannot reach TARGET_MET for any tool (clause f is `not tool_present`
  inside an `all()`), cannot run the fixture (sandbox lacks `trees/`), never sees its
  `MADO_OPTIONS_ROWS` marker and misreads the selftest line; and that a hardcoding stub
  passes its content clauses under a repaired runner;
- the C3 counter never existed (`git log --all -- quality/counters/c4-r39-options-entry.py`
  empty; CritC3Control).

So C2 **as declared** (v1 draft) is unreachable: reported as an honest miss of the
v1 draft, never re-labelled. The predicates below are frozen here, before data, and are
the ones the round scores; the report names both.

## C2 — `PRED-C3-r39-v2` (docstring of `quality/counters/c3-r39-options.py` at this commit)

- Counting command: `cd /home/vgpnk/Projects/shokunin/mado-shokunin && python3 -I quality/counters/c3-r39-options.py --repo . --rev <rev>`
- The counter generates 8 config trees seeded by sha256(REV:i) plus 2 `--getoption` merge
  trees and 1 FIFO strict tree, and scores the committed tool against its own reference
  last-declarer model. A tool that replays recorded outputs cannot pass.
- Before (base `08be4eb`): tool absent → `fixtures=0/11 tool=absent verdict=TARGET_MISSED`.
- Target: `fixtures=11/11 tool=present verdict=TARGET_MET`, exit 0, at the data commit.
- Kill rule: anything else at the data commit is a miss; no narrowing.
- Controls (scratch repo, receipts `c2/ctl-*.txt`, `c2/ctl-scratch.env`):
  base → `0/11 absent MISSED`; **wave-v1 tool** (`cee78d99…`, the seat-built tool before
  the attempt-2 repair) → `1/11 MISSED` (it lists flag-variant binds and `windowrule { }`
  fields as options); first-declarer mutant → `1/11 MISSED`; replay stub (prints the seat
  fixture's recorded rows) → `0/11 MISSED`; empty stub → `0/11 MISSED`; the attempt-2 tool
  bytes at the time of this freeze → `11/11 MET` (reachability, scratch rev).
- Robustness (not a control, recorded): 150 synthetic revs × 10 generated fixtures with
  the attempt-2 tool → 0 disagreements of 1500.

## C3 — `PRED-C4-r39-v1` (docstring of `quality/counters/c4-r39-options-entry.py` at this commit)

- Counting command: `cd /home/vgpnk/Projects/shokunin/mado-shokunin && python3 -I quality/counters/c4-r39-options-entry.py --repo . --rev <rev>`
- Before (base): `admitted=0/1 verdict=TARGET_MISSED` (receipt `c3/c4ctl-base.txt`).
- Target: `admitted=1/1 verdict=TARGET_MET`, exit 0, at the data commit.
- Kill rule: as C2.
- Controls (scratch clone, receipts `c3/c4ctl-*.txt`): wiring without committed receipts
  (N1), a Gate quote absent from its receipt (N2), an S219 receipt that does not name the
  tool's sha256 (N3), no index row (N4), a duplicate S218 row (N5), status `queued` (N6),
  an OBS line without the quote (N7), no Gate lines at all (N8) → each `0/1 MISSED` on its
  targeted clause; a fabricated self-consistent set (P) → `1/1 MET` — the declared residual.
- S218 is the 0.56.0 hyprlang page (era-matched to the host's hyprlang config; the wave's
  alternative, the 0.56.0 Variables page, documents the Lua `hl.config()` syntax the host
  does not run and is refused for this row).

## C1 — unchanged

Frozen at `457d1b1`; measured 19/19 at the freeze commit by seat ExecC1After
(`w1/ExecC1After/after-freeze.txt`); re-measured at the round tip by the L1.

## Assimilation correction (no claim)

registration.md assigned the 0.56.0 Dispatchers page to a new row S220. That URL is held
as S196 (byte-identical receipt, `f9b51362…`): a second row would be a within-scope
duplicate URL. The amendment cites S196 (re-opened this round) and S018; S220 is used
for the 0.54.0 Keywords page (`## Sourcing (multi-file)`, LINEAR order), which the C3
entry cites.
