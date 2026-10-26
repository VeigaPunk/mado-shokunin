# ScrScorecard (scribe) - SCORECARD Round 46 section, capabilities row, LOG.md entry skeleton

## Deliverable

`.ufo/waves/round-46/w1/ScrScorecard/draft.md` (~15 KB): a copy-paste-ready SCORECARD Round 46 section
(intro + controls paragraph + 4-column claim table + `### Capabilities (round 46)` row + sources/saturation/planned
+ `### Planned (round 47; intent only)` + `### Wave w1 outcome (round 46)`), a LOG.md Round 46 entry skeleton, an
`<AFTER>` placeholder map, and four flags for the L1. Insertion points: after `SCORECARD.md:2623`, at the end of
`LOG.md` (`:2513`). Nothing tracked was edited; no counter was run; no data commit was made; no scratch clone was
needed.

## What is filled and how it was verified

| Draft value | Provenance (command / file:line) | Check |
|---|---|---|
| freeze `8c5434c6`, base `b22ea56b` | `git log --diff-filter=A --format="%H %s" -- .ufo/waves/round-46/registration.md` -> `8c5434c6... round-46: freeze C1 ... and C2 ...`; registration.md `Base:` line | hash string found in the commit that added the registration (see F3) |
| axes at base 62/62, 73/73, 12/12, `checked=3 mismatched=0` | `receipts/axis-base.txt` | literal fragment count 1 |
| C1 controls PASS 0 of 23, reference met | `receipts/ctl-c1.txt` last line | literal fragment count 1 |
| C2 controls PASS wrong=0 of 15, P admitted | `receipts/ctl-c2.txt` last line | literal fragment count 1 |
| C1 before line (0/90, 0/150, tool=absent, MISSED) | `receipts/c1-before-base.txt` | literal fragment count 1 |
| C2 before line (admitted=0/1, clauses a-j = 0) | `receipts/c2-before-base.txt` | literal fragment count 1 each |
| C1 target line (90/90, 150/150, MET) | `receipts/ctl-c1.txt` REF line + registration C1 target | literal fragment count 1 in ctl-c1 |
| capability row live run (`keyboards=10 agree=9 virtual=1 ... verdict=OK`), tool sha `b229efd0...` | `receipts/live-devices-host-l1.txt` | literal fragment count 1 each |
| census line values (`default_layout=us ... virtual_prefix=hl-virtual-keyboard`) | `l1-draft/entry.md` (one line) | literal count 1 there, 0 in registration.md (F1) |
| "selftest 48/48", "band 64-128", ten pins, 28 surfaces, verdict codes 5/1/3/4/0 | registration.md / counter docstrings | literal hits recorded below |
| rows 252 -> 262 (S316-S325) | `grep -cE '^\| S[0-9]{3,} \|' corpus/SOURCES.md` -> 252; last row `S315`; `build-pos.py` ROWS list = 10 rows | command output |
| entries 62 -> 63 | `ls corpus/knowledge/*.md \| wc -l` -> 62 | command output |
| base census 10 warnings (9 W04 + 1 W01) | `grep -c '^mado\tW' receipts/census-before.txt` -> 10 | command output |
| 66 seats / role split / attack 29 of 66 = 44 % | `.ufo/waves/round-46/w1-spec.json` items (66), `collections.Counter(role)` | command output |
| verdict order + exit map in the capability row | registration C1 sentence; reference docstring (test order) | see flag 4 of the draft |

Quote verification ran as one script over the receipts and the registration: 14 fragments, 12 literal hits, 2 misses,
both explained (F1, F3). No fragment was typed from memory.

## Findings

- **F1 (attacks the draft's census citation).** `registration.md:45-46` wraps the census line after
  `scroll_factor_max=100`, so a literal grep of the full line against the registration returns 0. The one-line
  source is `.ufo/waves/round-46/l1-draft/entry.md` (literal count 1), which is what the LOG skeleton quotes;
  the L1 should cite the entry, or the counter's own `<D>/<F>/<n>` template, not the registration, when a checker
  greps the line.
- **F2 (would have broken a published table).** The capability row lists the verdicts with `|` separators
  (registration C1 wording). Unescaped in a GFM table that yields 10 cells instead of 4; the draft writes `\|`
  and a script counting unescaped pipes reports 6 split-parts (4 columns) on every row of both tables
  (`draft.md:28-31,39-41`).
- **F3 (freeze hash is not in the registration file).** The registration carries the base but not its own freeze
  commit; the draft cites `8c5434c6` as the commit that added it (convention of `SCORECARD.md:2596` for round 45),
  proven by `git log --diff-filter=A`.
- **F4 (base census baseline for the after-diff).** 10 warnings at base: nine W04 URL repeats (S030, S042, S045,
  S097, S119, S120, S121, S303, S307) and one W01 (S277). The draft states the count so the after-census can be
  diffed: S317 and S320 should each add one W04 line, and nothing else should change.
- **F5 (supported: round size).** 66 seats is at the run-9 floor of 64 and inside the frozen band 64-128, so the
  round-45 D1 conformance defect (41 seats) is answered; the draft's wave-outcome line records it.

## Out of scope / not done

- No counter invocation (`c1-r46-devices.py`, `c2-r46-input-device-entry.py`) - after values stay `<AFTER>`; a
  scribe that ran them would decorate the report with a number the L1 has not committed.
- No compositor read of my own (no `hyprctl` call); the live figures quoted are the L1's freeze receipt.
- No edit of `SCORECARD.md`, `LOG.md`, counters, registration, reference, pins or controls.
- No host package operation; no tool installed.
- The seat report names used in `<AFTER>` markers come from `w1-spec.json`; whether each seat actually reports is
  unverified here (the reports were not read).

## Paths

- Draft: `.ufo/waves/round-46/w1/ScrScorecard/draft.md`
- Report: `.ufo/waves/round-46/w1/ScrScorecard.md`
