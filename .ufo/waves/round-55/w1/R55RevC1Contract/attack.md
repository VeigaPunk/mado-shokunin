# Attack on PRED-C1-r55 as frozen (seat R55RevC1Contract, wave w1, round 55)

Predicate attacked: `quality/counters/c1-r55-kbd-entry.py` leg set + `quality/check-r55-controls.py --claim c1`, as written in
`registration.md` §C1 and `claims-frozen.md` C1. Freeze commit `54dacbd8`; base `3b55b6e9`. Predicate unchanged.

## 0. Result

- A non-work entry reaches `TARGET_MET` and the harness reaches `good=ok controls=7/7` (the frozen C1 controls, all seven
  `TARGET_MISSED` with the named leg). The entry is 24 rows copied from `frozen-tables.json`, one-sentence placeholder
  propositions, a fabricated provenance trio, one README row and four registry rows (one with a fabricated URL).
- Under the literal table grammar the predicate is also unreachable for two rows with an honest entry: K16 (its quote contains
  `||`, and the grammar forbids `|` in a cell) and K17 (the only wayland registry row, S052, has a URL that does not contain
  the frozen commit). An honest entry therefore cannot reach `TARGET_MET` as written; a junk entry can, by fabrication.
- The counter checks quote identity and row/host binding. It does not check that a proposition says anything that the quote
  supports. That is the declared limit (QUALITY 104/105); the attack shows the limit is the whole content check.

## 1. What was built (scratch only; lane untouched)

- Scratch repo `base-2TQV` = `git archive 3b55b6e9` + `git archive 54dacbd8 .ufo/waves/round-55`, one commit.
- `c1_attack_check.py`: an independent re-implementation of the §C1 legs from the contract text. It reads git objects at `--rev`
  only. It is not the wave counter: `quality/counters/c1-r55-kbd-entry.py` and `quality/check-r55-controls.py` are absent at
  `dbc2eefe`, so no frozen counter was run. Modes: literal table grammar (default), `--escaped-pipes` (GFM `\|`),
  `--propose-clause` (non-frozen C1-X, §5).
- `build_junk_and_controls.py`: builds junk entries from `frozen-tables.json` (rows copied verbatim), appends README and
  registry rows, runs the checker on each, then applies the seven frozen C1 controls to a copy of junk A (each in a fresh repo,
  toplevel asserted first).
- Junk A (`receipts/junkA-entry.md`): K01–K18 and H01–H06 with placeholder propositions (K ≥ 40 chars, H ≥ 20 chars);
  `source:` S316, S317, S318, S319, S378–S381; `verified-at: 2026-10-28`; `recheck: on-release`. S378–S380 are the three
  registration new rows (tier A, `mined`, `opened` 2026-10-28, `used-by` the entry path, URLs at `efb50993`, shas copied from
  the frozen pin table). S381 is fabricated: `https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993…/1.26.0/protocol/wayland.xml`,
  a path the pin set does not establish; it was not fetched.
- Junk B: identical except K17 → S052 (honest wayland row). Junk C: stuffed propositions (quote identifiers copied in plus a
  seeded 8-word salad).

## 2. Commands and decisive output (`receipts/run.txt`)

```
BEFORE(base+freeze, no entry): MADO_KBD_ENTRY: … rows=0/18 hosts=0/6 sources=0/18 new_rows=0/3 verdict=TARGET_MISSED missed=new_rows,entry_absent rc= 1
A junk-filler (K17->S381 fabricated): 2dd07426… rc= 0
MADO_KBD_ENTRY: rev=2dd07426… rows=18/18 hosts=6/6 sources=18/18 new_rows=3/3 verdict=TARGET_MET missed=none
A under LITERAL grammar (no escaped pipes): 1
MADO_KBD_ENTRY: … rows=17/18 hosts=6/6 sources=17/18 new_rows=3/3 verdict=TARGET_MISSED missed=row:K16
# K16: row missing, duplicated or cell count != 5 (cells=[7])
B junk-filler with honest K17->S052: 30126e4b… rc= 1
MADO_KBD_ENTRY: … rows=18/18 hosts=6/6 sources=17/18 new_rows=3/3 verdict=TARGET_MISSED missed=source_cell:K17
# K17: source cell 'S052' is not a mined registry row whose URL ends '1.26.0/protocol/wayland.xml' and contains efb50993
C junk-stuffed: e2464635… rc= 0
MADO_KBD_ENTRY: … rows=18/18 hosts=6/6 sources=18/18 new_rows=3/3 verdict=TARGET_MET missed=none
CTL C1-CTL-1 absent: expected=entry_absent rc=1 pass=True | … missed=entry_absent
CTL C1-CTL-2 spliced-quote: expected=quote:K04 rc=1 pass=True | … missed=quote:K04
CTL C1-CTL-3 shifted-anchor: expected=anchor:K01 rc=1 pass=True | … missed=anchor:K01
CTL C1-CTL-4 wrong-source: expected=source_cell:K10 rc=1 pass=True | … missed=source_cell:K10
CTL C1-CTL-5 dropped-row: expected=row:K17 rc=1 pass=True | … missed=row:K17
CTL C1-CTL-6 host-forged: expected=host:H02 rc=1 pass=True | … hosts=5/6 missed=host:H02
CTL C1-CTL-7 pin-tamper: expected=pin_hash rc=1 pass=True | … missed=tables_sha,pin_hash
ATTACK_C1_CONTROLS: good=ok controls=7/7
```

Every frozen quote is a substring of its pin line at the freeze commit (all 24 pass `quote_in_pin` in junk A), and every pin
and `frozen-tables.json` hashes to the embedded sha. The registry rows S316, S317, S318, S319, S052 already carry the frozen
pin shas (`feedf32e…`, `9db68cf4…`, `a76f0507…`, `8a800efe…`, `cc860987…`), so the pin-to-registry consistency holds at base.

## 3. Per-leg accounting: what junk A satisfies and what it cannot

| leg | junk A | how | can a junk entry fail it? |
|---|---|---|---|
| `entry_absent` | satisfied | file created | no |
| `provenance` | satisfied | trio written; `recheck:` value unconstrained | no (any text passes) |
| `index` | satisfied | one README row | no |
| `row:<id>` ×24 | satisfied | copy of frozen row; propositions ≥ 40/20 chars | only by length, which is trivial to pad |
| `anchor:<id>` ×24 | satisfied | copy of `pin:line` | only if the copy is wrong |
| `quote:<id>` ×18 | satisfied | copy of frozen quote | only by a wrong copy; literal grammar fails K16 (`\|\|`) |
| `host:<id>` ×6 | satisfied | copy of host pin line text | can only choose a substring of the frozen quote; H values are fixed by `pin_hash` |
| `pin_hash` | satisfied | pins untouched | cannot forge the pins without tripping the leg |
| `tables_sha` | satisfied | tables untouched | cannot change without tripping the leg |
| `source_cell:K10,K11,K12,K18` | satisfied | fabricated-shape rows S378–S380 | yes only if the S-id is wrong |
| `source_cell:K17` | satisfied only by fabrication | S381 URL with the Hyprland commit and wayland suffix | an honest entry cannot pass it (junk B: `missed=source_cell:K17`) |
| `source_cell:K01–K16` | satisfied | existing mined rows S316–S319, S317 | no |
| `new_rows` (3 needed) | satisfied | three registry rows with the required fields | counter checks shape, not that a source was opened |

Summary: the counter can distinguish a junk entry from a transcription only through the four cell-shape legs and the one
registry-row check. Everything else is satisfiable by copying the frozen tables. The one leg a junk entry cannot satisfy
without fabrication is `source_cell:K17`, and an honest entry cannot satisfy it at all under the literal reading (§6, D2).

## 4. What a human reviewer would reject in junk A

1. All 24 propositions are the same placeholder sentence with the row id changed. They say nothing about the pinned code.
2. The `source:` line lists nine S-ids; nothing maps a claim to a source beyond the anchor cell.
3. S378–S381 are registry rows with filler `anchor`, `teaches` and `scope` cells. S381's URL names a Hyprland-repo path the
   pin set does not establish, and it was never fetched.
4. The README row says "attack filler"; the entry has no analysis, no statement of what the host reads, and no limit section.
5. The rows are a transcription of `frozen-tables.json`. A reviewer comparing the entry to the pins learns nothing that the
   tables did not already say.

## 5. Proposed clause (text only, not frozen; not in the predicate)

**C1-X (proposed).** For each K or H row that has exactly one row in the entry, the proposition cell contains at least two
whole-word identifiers (matching `[A-Za-z_][A-Za-z0-9_]{2,}`) that occur in that row's frozen quote; if the quote has fewer
than two such identifiers, all of them must occur. A failing row is reported as `prop:<id>` and fails the predicate.

Measured on this attack (`receipts/c1x-split.txt`):

- Junk A (placeholder propositions): identifier sub-check fails **24/24**. Clause stops the junk entry.
- Junk C (quote identifiers copied in plus word salad): identifier sub-check fails **11/24**; the 13 rows that pass show that
  C1-X alone does not stop a stuffed entry. A dissimilarity sub-check (`difflib` ratio < 0.6 across propositions) catches
  19/24 of junk C, but a seeded word salad with more variety would pass it too, so it is not a stop either.
- Junk B (K17 honest, others placeholders): identifier sub-check fails 24/24.

**Could it be frozen now? No.** The predicate, legs and controls are frozen; `claims-frozen.md` says no predicate changes
after any seat has scored, and a falsified predicate is an honest stop. Adding C1-X now would be an edit of the frozen text
and an invalid run.

**What it would cost next round:** a new predicate (for example PRED-C1-r56) in a freeze commit before any `.ready`; the
counter gets the leg `prop:<id>`; `check-r55-controls.py`'s successor gets an eighth control (junk-filler entry → `prop:<id>`
expected); `frozen-tables.json` regenerated and its sha re-embedded; the real entry re-run against the new leg (good=ok must
still hold); and a sealed stuffed-junk hold-out to measure the bypass. In practice it is one full round (freeze → dispatch →
score), i.e. the round after this one.

## 6. Defects and ambiguities in the frozen text (found by the attack; none edited)

- **D1 — K16 cannot be written under the stated row grammar.** registration §C1: "no `|` inside a cell". The frozen K16 quote
  is `if ((!VAL || !VAL->m_bSetByUser) && !fallback.empty())`, which contains `||`. Under the literal reading `row:K16` fails for
  every entry (junk A literal run: `missed=row:K16`). Only a GFM `\|` escape makes it representable, and the contract does not
  say that the escaped cell is compared after unescaping. Junk A passes only under the escape reading (`--escaped-pipes`).
- **D2 — K17 cannot be satisfied honestly.** `source_cell:K17` requires the registry row's URL to contain the frozen commit
  `efb50993…`. The only wayland registry row is S052 (`gitlab.freedesktop.org/…/1.26.0/protocol/wayland.xml`, no commit). S043
  is a `/usr/share/…` local path, not a URL. Junk B shows `missed=source_cell:K17`. The reused-row rule in registration §C1
  ("S052 (wayland 1.26.0 wayland.xml)") and the contains-commit rule conflict for this pin.
- **D3 — `new_rows` suffix is ambiguous.** Registration says a registry row's URL must end "in a `new_row_pins` suffix". The
  `new_row_pins` keys are basenames (`Hyprland-SeatManager.cpp`); no URL ends in such a key (the URL ends `…/SeatManager.cpp`).
  The only workable reading is the `source_suffix` values; the attack uses that.
- **D4 — C1-CTL-7 trips two legs.** The mutation edits `frozen-tables.json` as well as the pin; `tables_sha` is missed alongside
  `pin_hash` (junk run: `missed=tables_sha,pin_hash`). The harness must accept a superset; the text does not say whether
  `missed=` is compared exactly or by membership.
- **D5 — `sources=<n>/<n>` denominator unstated.** The attack uses 18 (K rows).
- **D6 — H rows' S-cell (`host`) is shape-only.** The contract writes `| H01 | … | host | …` but no leg checks the cell.
- **D7 — `recheck:` has no value grammar**, so provenance accepts any text.
- **D8 — anchor "pin file" is unstated as basename.** The attack assumes `Hyprland-InputManager.cpp:1220`-style cells, which is
  what the frozen `pin` field holds.

## 7. Not verified

- The frozen counter and the frozen harness were not run: neither file exists at `dbc2eefe`. All legs above come from the
  attack checker, a re-implementation of the contract text.
- No URL was fetched. S381's URL was not resolved; "not established by the pin set" is a statement about the frozen table only.
- Propositions were not checked against the quotes beyond the attack's placeholder/identifier observations (the declared limit).
- Host files were not read. No `hyprctl` command ran.
- The sealed hold-out was not looked for or opened. No hold-out path was encountered.
- Tooling: none installed; no pacman transaction; no lane, fleet or sibling writes; no commits in the lane.
