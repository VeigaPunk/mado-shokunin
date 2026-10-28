# R55 w1 — seat R55ScribeEntryA (C1 entry draft, scoped)

Seat role: scribe for the C1 knowledge entry `corpus/knowledge/hyprland-keyboard-repeat-numlock-r55.md`. Draft only; the L1 integrates. No tracked file, SOURCES.md, README, git state or host state was changed. No subagent, no background job, no commit.

## 1. What I did

1. Read the frozen contract: `claims-frozen.md` (C1 text), `registration.md` §C1 (grammar, legs, controls, new S378–S380 rows), `frozen-tables.json` (`c1.k` 18 rows, `c1.h` 6 rows, `pin_sha256`, `new_row_pins`), and the pins under `fetch/`. Read the pinned source ranges I needed (InputManager 1205–1295, IKeyboard.cpp 101–145, SeatManager 169–185, Seat.cpp 431–455 and 594–615, IKeyboard.hpp 111–131, ConfigValues 271–287, legacy ConfigManager 1089–1137, wayland.xml 2728–2751).
2. Confirmed the frozen tree: the committed pin bytes at freeze commit `54dacbd843d64ba744cd3f1bdc2ec622e5010039` equal the working-tree pins (receipt below). Lane HEAD is `dbc2eefe…` (the w1 spec commit after the freeze).
3. Wrote `gen_entry.py` (a copy is in my deliverable dir). It takes the K and H pin cell and quote cell only from `frozen-tables.json`, and asserts that each extra (E) quote is an exact substring of its named pin line, failing closed otherwise. Propositions are my text; each is checked for length (K ≥40, H ≥20) and for no pipe or backtick.
4. Wrote `verify.py` (a copy is in my deliverable dir), independent of the generator. It parses the drafted entry back and checks the trio, row counts, pin cells, quote cells, quote-in-pin-line, all 10 pin sha256s, expected S-ids, proposition lengths and duplicate ids.
5. Ran the verifier on the draft and on five scratch mutants that apply the frozen C1 control mutations (negative test, below).

## 2. Commands and decisive output

Generator (`python3 -I gen_entry.py`):
```
wrote …/w1/R55ScribeEntryA/entry.md bytes=15482 K=18 H=6 E=10
```

Verifier on the draft (`python3 -I …/verify.py …/entry.md > …/verify.txt`, rc=0):
```
pins sha256 ok=10/10
provenance trio ok
K/H rows ok=24/24
E rows ok=10/10 ids=['E01', …, 'E10']
duplicate ids: none
VERIFY_SUMMARY … kh_rows=24/24 extra=10 pins=10/10 failures=0 verdict=OK
```
Full per-pin sha256 lines are in `verify.txt`.

Negative test (`negative-controls.txt`), mutants applied to a scratch copy of the entry:
```
ctl2_spliced_K04   -> FAIL quote:K04 quote cell != frozen             rc=1
ctl3_shift_K01     -> FAIL anchor:K01 pin cell …:1219 != …:1220        rc=1
ctl4_wrong_src_K10 -> FAIL source_cell:K10 S316 != S378                rc=1
ctl5_drop_K17      -> FAIL row:K17 count=0                             rc=1
ctl6_forged_H02    -> FAIL quote:H02 quote cell != frozen              rc=1
```
The verifier fails every mutant; it does not print `host:H02` for ctl6 (see §4, item A).

Committed-vs-tree pins and the committed freeze verifier (`receipts-host-and-pins.txt`):
```
Hyprland-InputManager.cpp committed=feedf32e2e3d23ae tree=feedf32e2e3d23ae   (all 10 equal)
FREEZE_VERIFY: bad=0 frozen-tables.sha256=bf46c889… OK
```

Host reads (read-only, `receipts-host-and-pins.txt`):
```
hyprctl getoption input:repeat_rate -j       -> {"option": "input:repeat_rate", "int": 40, "set": true }
hyprctl getoption input:repeat_delay -j      -> {"option": "input:repeat_delay", "int": 250, "set": true }
hyprctl getoption input:numlock_by_default -j -> {"option": "input:numlock_by_default", "int": 1, "set": true }
hyprctl version -> Hyprland 0.56.2 … commit efb50993780079460b0cbed1363e2166a2de1d9f clean
```
The live reads agree with the committed host pins (H04–H06). The file declares 40 / 250 / true (H01–H03). The entry states that a declaration and a read are not delivery to clients.

## 3. Deliverables

- `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-55/w1/R55ScribeEntryA/entry.md` — the complete C1 draft: trio first, settles/UNKNOWN, chain, K01–K18 (18 rows), H01–H06 (6 rows), E01–E10 extra rows, Limits, How-to-verify.
- `…/w1/R55ScribeEntryA/verify.txt` — output of `verify.py` on the draft (verdict OK).
- `…/w1/R55ScribeEntryA/verify.py` — independent checker (receipt).
- `…/w1/R55ScribeEntryA/gen_entry.py` — generator (receipt; K/H cells from `frozen-tables.json`).
- `…/w1/R55ScribeEntryA/negative-controls.txt` — mutant runs (receipt).
- `…/w1/R55ScribeEntryA/receipts-host-and-pins.txt` — host reads, committed-vs-tree hashes, freeze-verify tail (receipt).
- This report: `…/w1/R55ScribeEntryA.md`.

S-ids used by rows (per registration): K01–K07 S316; K08–K09 S319; K10 S378; K11–K12 S379; K13–K15 S318; K16 S317; K17 S052; K18 S380. H rows use `host`.

Proposed registry rows for integration (not written; SOURCES.md is an integration surface): S378, S379 and S380 with the URLs and anchors in `registration.md` §C1 — the L1 writes them.

## 4. Defects, ambiguities and risks

A. **C1-CTL-6 required leg may not be reachable as written.** The control changes the H02 *cell* quote to `repeat_delay = 300`. That cell is not a substring of `host-input.conf:15`, so a `host:H02` check on the cell would fire. The same change makes the cell differ from the frozen quote, so `quote:H02` fires. The control passes only if the counter lists every missed leg in `missed=` rather than the first. My verifier reports `quote:H02` only, so its output does not show `host:H02`. Status: unverified until the counter exists; the frozen text does not say whether `missed=` lists all legs.

B. **Registry anchor ranges do not cover three cited lines.** The counter checks only S-id URL suffix, commit and status, not the anchor text, so none of these would be caught by it.
- S318 records `Hyprland-ConfigValues.cpp:271-279`. K14 is at line 280 (`input:repeat_delay` default 600, range 0–2000). The frozen contract fixes K14 to S318, so the L1 must widen S318's anchor to 271-280 at integration.
- S052 records wl_keyboard `:2573-2699`. The wl_keyboard interface spans 2573–2752 in the pin (`</interface>` at 2752). K17 (line 2741) and E04/E05 (lines 2732, 2740) sit outside the recorded range. Widen S052's anchor at integration.
- S316 records applyConfigToKeyboard `:1213-1295`. E08 (line 1195, `applyConfigToKeyboard(keeb);` inside setupKeyboard) is outside it. E08 is an extra row only; it is flagged in the entry's Limits. Either widen S316 or drop E08.

C. **K07 is a line-level fact with an unexercised consequence.** Line 1271 compares the unclamped names `REPEATDELAY`/`REPEATRATE` with the stored fields, which lines 1282–1283 write as `std::max(0, …)`. The entry states only what the line shows. Whether a negative configured value can reach the comparison is UNKNOWN (the hyprlang enforcement of `min` is not pinned); the resulting "early return would not fire" is labelled [INFERENCE] and not exercised.

D. **Range enforcement is not pinned.** K13/K14 declare `min`/`max`. The pins do not show how the config layer treats out-of-range values (clamp, reject or ignore). The entry lists this as UNKNOWN. The C2 tool model (`unsupported`, line ignored) is a model, not a source fact, and the entry does not cite it as one.

E. **`"set": true` in host-getoption.json is undefined by any pinned row.** Recorded as UNKNOWN.

F. **Host keyboard listing differs between reads.** My first `hyprctl devices -j` listing (in the scratch read) showed `hl-virtual-keyboard-fcitx5` with main=True; the receipt listing taken later shows nine keyboards with `yubikey…` main=True and no virtual keyboard line. I did not use the device listing in any row; I record the discrepancy as observed, not explained.

G. **QUALITY 104 wording.** The "only" in K09 and K10 was checked against the branch sets (IKeyboard.cpp:122–131 no else; SeatManager.cpp:176–177 single-statement if). K11's send condition is stated as "not both equal" — the line 442 condition is `!m_owner || version<4 || (rate==m_lastRate && delay==m_lastDelayMs)`. K04/K05 say "floored at zero, no upper bound applied on this line". No row says a running host behaves in some way.

H. **Propositions name context beyond their quote in two places.** K10's proposition names the line-176 guard, which its own quote (line 177) does not contain; the guard is quoted by E09 and checked in Limits. K17's proposition is restricted to its quote; the rate-zero sentence start is quoted by E05 and the wording is not in K17's cell. No pipe or backtick appears in any cell (`||` in K11 was replaced by wording).

## 5. Not verified / not run

- The counter `quality/counters/c1-r55-kbd-entry.py` and the harness `quality/check-r55-controls.py` are not in the tree at this commit; they cannot run here. The C1 verdicts (`MADO_KBD_ENTRY … TARGET_MET`, `MADO_R55_CONTROLS … controls=7/7`) are therefore **not** observed. My verifier is an independent check of the same grammar, not the frozen counter.
- The C1-CTL-7 pin-tamper control (a changed hex nibble plus appended pin byte) was not run; the pin-hash leg was exercised only on the untampered pins (10/10).
- The README index row (`knowledge/hyprland-keyboard-repeat-numlock-r55.md`) and SOURCES.md rows S378–S380 are not written; they are L1 integration items.
- Sentence-to-pin entailment (QUALITY 104 as a full audit) is not performed here; that is the w2 audit named in `claims-frozen.md`.
- Hold-out: I did not open, list or use `fixtures/c2-holdout/` or any hold-out path; none was encountered. I did not run `tools/mado-kbdopts.py` (C2 is another seat).

## 6. Tooling and host

- No tool was installed or upgraded. No pacman transaction, no `~/.local/bin` write.
- Host: only read verbs run — `hyprctl getoption … -j` (×3), `hyprctl version`, `hyprctl devices -j`, and the committed `input.conf` pin. No `keyword`, `dispatch`, `reload`, or config write.
- Git: read verbs only (`cat-file`, `show`, `log`, `rev-parse`) against the lane; no commit, stash, checkout, reset, or jj.
- Scratch `/fast/scratch/hyaku/mado-r55/R55ScribeEntryA/` (generator copy, mutant files, raw verifier output) is removed before yield; receipts were copied into the deliverable directory first.
