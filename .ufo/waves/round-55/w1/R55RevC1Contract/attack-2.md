# PRED-C1-r55 attack (seat R55RevC1Contract-2; second, independent attack on the frozen predicate)

Frozen predicate not changed. Base freeze commit `54dacbd8` (corpus + round-55 archived into a scratch fixture repo, never the lane). `frozen-tables.json` sha256 `bf46c8896a1861fec746f8900aabe54faf7aaaa3ff5691ed0a05e8e9d4179490`.

## Verdict

1. A junk entry reaches `TARGET_MET` and `good=ok 7/7` **under the GFM-escape reading** of the cell grammar. Every leg is satisfied by copying frozen bytes, writing filler propositions and adding four registry rows, one of which (S381) carries a constructed URL that returns HTTP 404.
2. **Under the literal grammar ("no `|` inside a cell") no entry can reach `TARGET_MET`**: frozen K16's quote contains `||`. This is a predicate-blocking defect, not a seat failure.
3. The seat-level "K17 source_cell" leg cannot be met honestly with the existing registry: S052's URL does not contain the frozen commit. The only passing route is a fabricated URL.
4. A human reviewer rejects the junk on every one of the 24 rows: no proposition states a fact.

## Method and what was built

- `c1check.py` (scratch, copied to `attack-2/`): my own re-implementation of the §C1 legs from the contract text. Reads only git objects at `--rev`. `--cells strict` (frozen literal grammar, default) or `--cells gfm` (a cell may hold `\|`; the escape is undone before comparison). Not the wave counter; I did not run or read the counter.
- `build_attack.py` (copied to `attack-2/`): builds the junk entry J1, variants, and the seven frozen C1 controls, each in a fresh scratch repo (`git init` + commit with `-c user.name=ctl -c user.email=ctl@ctl`; `rev-parse --show-toplevel` asserted equal to the fixture dir before the first commit). Output: `attack-2/build.log`, `attack-2/results.json`.
- Junk J1 (`attack-2/J1-entry.md`): provenance trio (`source: S316, S317, S318, S319, S378, S379, S380, S381`, `verified-at: 2026-10-28`, `recheck: on-release`); 24 rows copied byte-for-byte from `frozen-tables.json` (`id`, `pin:line`, quote); propositions are `Filler proposition K01 for the junk attack entry; not a claim.` (63 chars; H rows 33 chars, both above the 40/20 minimums); S-ids chosen by URL suffix (S316 InputManager, S319 IKeyboard.cpp, S318 ConfigValues, S317 legacy ConfigManager, S378 SeatManager, S379 Seat.cpp, S380 IKeyboard.hpp, S381 wayland, see D2). K16 quote written with `\|\|` (only way to put it in a table cell). Added to the tree: `corpus/SOURCES.md` rows S378–S381 (opened `2026-10-28`, tier A, `mined`, used-by = entry path, filler scope/teaches) and one `corpus/README.md` row.
- `attack-2/probe.py` / `probe.txt`: topic and overlap clause probes (below).

## Results (all runs use the same fixture repo; `strict` and `gfm` shown)

| fixture | strict | gfm |
|---|---|---|
| J1 cheapest junk | TARGET_MISSED `row:K16` (18 of 18 otherwise pass) | **TARGET_MET** `rows=18/18 hosts=6/6 sources=18/18 new_rows=3/3 missed=none` |
| J2 identifier-stuffed junk | TARGET_MISSED `row:K16` | **TARGET_MET** `rows=18/18 hosts=6/6 sources=18/18 new_rows=3/3 missed=none` |
| J0 K17 → honest S052 reuse | `row:K16,source_cell:K17` | `source_cell:K17` (sources 17/18) |
| J1 minus S378–S380 rows | `…source_cell:K10,K11,K12,K18,new_rows` | `source_cell:K10,K11,K12,K18,new_rows` (new_rows=0/3) |
| J1 minus README row | `index,row:K16` | `index` |
| J1 minus entry file | `entry_absent,provenance,row:*` | same |

Frozen controls applied to J1 under `gfm` (each must print TARGET_MISSED and the named leg):

| control | mutation | got `missed=` | required | ok |
|---|---|---|---|---|
| C1-CTL-1 | delete entry | `entry_absent,provenance,row:*` | `entry_absent` | yes |
| C1-CTL-2 | K04 `REPEATRATE) ;` | `quote:K04` | `quote:K04` | yes |
| C1-CTL-3 | K01 `:1220`→`:1219` | `anchor:K01` | `anchor:K01` | yes |
| C1-CTL-4 | K10 S378→S316 | `source_cell:K10` | `source_cell:K10` | yes |
| C1-CTL-5 | drop K17 row | `row:K17` | `row:K17` | yes |
| C1-CTL-6 | H02 `250`→`300` | `quote:H02,host:H02` | `host:H02` | yes |
| C1-CTL-7 | nibble in table + space in `Hyprland-IKeyboard.cpp` | `tables_sha,pin_hash` | `pin_hash` | yes |

So the junk gives the frozen harness line `MADO_R55_CONTROLS: claim=c1 good=ok controls=7/7 verdict=OK` (with my harness; the frozen harness was not run) and the frozen counter line for success. Under `strict`, `good=bad`, so the harness would print `verdict=FAIL` for every entry.

Strict run of the honest-looking K17 path (J0) also shows the wayland registry row fails by construction (D2).

## Declared limit, quantified: what junk satisfies, clause by clause

| leg | junk J1 satisfies? | how | what the leg does NOT check |
|---|---|---|---|
| `entry_absent` | yes | file exists | content |
| `provenance` | yes | literal `verified-at: 2026-10-28`, `source:` names registry ids | that the named ids were read |
| `index` | yes | one README row | README row content |
| `row:<id>` | yes (K16 only under strict) | 5-cell row, id first | proposition content; length 40/20 is enforced only by my reading (D5) |
| `anchor:<id>` | yes | copied `pin:line` | that the line is what the proposition says |
| `quote:<id>` | yes | copied quote, substring of real pin line | that the proposition follows from the quote |
| `pin_hash` | yes (cannot be forged without also changing tables) | real pin bytes | nothing further |
| `source_cell:<id>` | 17/18 with existing rows; K17 only via S381 | S-id whose URL ends with the pin suffix, contains the commit, status `mined` | the row's scope/anchor/teaches cells; URL is never fetched; the SHA in the anchor is never compared to pin bytes; `opened` is not checked here |
| `new_rows` | yes, by writing 3 rows | `opened 2026-10-28`, tier A, `mined`, URL suffix in `new_row_pins`, used-by names entry | that the rows were opened or that their anchor lines match the pins. The date and status are self-asserted text. Removing S378–S380 drops it to 0/3 (measured) |
| `host:<id>` | yes | H quote is a substring of the committed host copy | live host state (the pin is a committed copy; `hyprctl` never run); the proposition |
| `tables_sha` | yes (unchanged) | frozen tables | n/a |

What junk **cannot** satisfy: any leg that needs bytes other than the frozen ones (a forged quote is caught by `quote:`/`host:`, a forged pin by `pin_hash`), a source pointing at the wrong pin (`source_cell`, CTL-4), and under strict grammar K16 at all.

## What a human reviewer rejects in J1 (and in J2)

1. All 24 propositions state no fact (`Filler proposition K01 … not a claim.`); a sentence-to-pin audit fails 24/24. J2 is worse in a different way: `Restates the quoted identifiers devname getDeviceInt repeat_rate without stating a keyboard fact about K01.` says on its face that it asserts nothing.
2. The registry rows S378–S381 read `filler scope` / `filler teaches, nothing opened`: the registry itself says nothing was opened, yet they carry `opened 2026-10-28`.
3. S381's URL (`…/efb50993…/subprojects/wayland/1.26.0/protocol/wayland.xml`) returns **HTTP 404** (`curl` read on 2026-10-28); S378's real-path URL returns 200 (positive control). The counter never fetches, so it cannot tell.
4. `verified-at: 2026-10-28` with no reading recorded; H rows assert host values with no live read.
5. K16's quote is written `\|\|` — the bytes differ from the frozen quote; only the GFM reading accepts it.

## Proposed clause (text, NOT frozen; the predicate is unchanged)

> **prop_topic:<id>** — for each K and H row, the proposition cell contains, case-insensitively, at least one of `repeat`, `delay`, `numlock`. Reported in `missed=` like every other leg; applies to all 24 rows.

Measured (`attack-2/probe.txt`):
- J1: 0/24 pass → **stops the cheap junk.**
- J2 (identifier-stuffed): 22/24 pass → **does not stop it.**
- Honest-looking probe sentences (8 hand-written, not a full set): 7/8 pass; K16 `A value the user never set falls back to the global option.` fails (false positive).

A stronger clause that also stops J2 would be **prop_frozen:<id>**: the 24 proposition sentences stored in `frozen-tables.json` and compared byte-for-byte. That costs the L1 authoring 24 sentences before the freeze, and turns C1's proposition content into transcription of the L1's wording, so the sentence-to-pin audit moves to freeze time.

**Can it be frozen now? No.** `claims-frozen.md` and `registration.md` are frozen, and the seats are scoring; adding a leg now edits the predicate, which is an honest stop, not a fix. **Next-round cost** of prop_topic: a registration §C1 leg; a control C1-CTL-8 (J1 must fail it); calibration on a full human-written set of 24 honest propositions (only 8 probed here, so the false-positive rate is unmeasured); a re-freeze before `.ready`; a counter change. Roughly one round of work, with a known FP on K16-style wording.

## Defects and ambiguities in the frozen contract (inputs shown)

- **D1 (predicate-blocking).** Strict grammar says "no `|` inside a cell", but `frozen-tables.json` `c1.k` K16 quote is `if ((!VAL || !VAL->m_bSetByUser) && !fallback.empty())`, which has `||`. Result: `row:K16` for every entry under strict, including J1. Any honest entry is blocked the same way. Needs an L1 ruling (e.g. GFM `\|` with unescape) recorded before scoring; I did not patch it.
- **D2 (predicate-blocking for K17).** `source_cell` requires the URL to contain the frozen commit `efb50993…`. The only registry row for the wayland pin, S052, has URL `https://gitlab.freedesktop.org/wayland/wayland/-/raw/1.26.0/protocol/wayland.xml` (no commit). `new_row_pins` does not include wayland, so no new row can be honest. Registration says "reuse S052", which contradicts the leg as written. The only route to pass is a constructed URL (J1: S381, 404).
- **D3 (control ambiguity).** C1-CTL-6 requires `host:H02`. That leg only fires if the host check tests the row's own quote cell, not frozen equality; a counter that reports only the first failing leg, or only frozen equality, prints `quote:H02` alone and fails the control. My checker reports all failing legs and evaluates `host:` on the cell.
- **D4 (control wording).** C1-CTL-7 "change one hex nibble … AND of its pin bytes": I read it as the table's sha nibble changed and one space appended to the pin. Read as both values changed consistently, only `tables_sha` fires and the control fails.
- **D5 (unnamed leg).** The 40/20-character proposition minimums appear in the grammar but no leg names them. I filed them under `row:<id>`; a counter may ignore them entirely.
- **D6 (undefined numerator).** `sources=<c>/<d>` never defines `c`. I used K rows passing `source_cell` over 18.
- **D7 (index exactness).** The index leg says "exactly one README row `` | `path` | ``", while existing README rows carry a note after the path. I matched the cell prefix `` | `path` ``.
- **D8 (who writes new_rows).** `new_rows` reads SOURCES at `--rev`, but the registration says the L1 writes S378–S380 at integration. A seat's rev therefore fails `new_rows` unless the seat writes them itself (J1 did). The row check also never binds the rows to pin bytes (see the table).

## Not verified / limits

- My checker is my reading of the contract; the frozen counter and harness were not run and not consulted. Where the text is ambiguous I chose a reading and report both (`strict`/`gfm`).
- "Human reviewer" judgments are mine; no full honest entry was written, so the false-positive rate of prop_topic is measured on 8 sentences only.
- Network: two read-only HTTP GETs (`curl`), no installs, no host calls (`hyprctl` not run), no hold-out fixture touched. I read the first 400 bytes of a peer's file only to identify it and did not use its content.
- Scratch dir removed after this write-up; receipts are in `attack-2/`. The `build_attack.py` copy references scratch paths; it is a receipt, not a runnable deliverable.
