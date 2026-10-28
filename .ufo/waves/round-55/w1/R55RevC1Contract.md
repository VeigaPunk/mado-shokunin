# Seat R55RevC1Contract — report (round 55, wave w1)

Scope: attack PRED-C1-r55 as frozen. Deliverable: `.ufo/waves/round-55/w1/R55RevC1Contract/attack.md`. Supporting receipts: `.ufo/waves/round-55/w1/R55RevC1Contract/receipts/` and the attack scripts `c1_attack_check.py`, `c1x_split.py`, `build_junk_and_controls.py` in the same directory. Predicate, registration, frozen tables and controls were read and not edited.

## What I did

1. Read `claims-frozen.md`, `registration.md` and `frozen-tables.json` (lines 1–200 and 200–393, raw) at the lane's committed tree; read `fetch/SHA256SUMS.txt`, `receipts/before.txt`, and the base registry rows S052, S043, S215, S316–S319, S162.
2. Built a scratch repo `/fast/scratch/hyaku/mado-r55/R55RevC1Contract/base-2TQV` from `git archive 3b55b6e9` + `git archive 54dacbd8 .ufo/waves/round-55` (lane read-only; the `rev-parse --show-toplevel` check passed before the first commit).
3. Wrote an independent C1 checker from the contract text (`c1_attack_check.py`): literal grammar by default, `--escaped-pipes` for GFM, `--propose-clause` for the non-frozen C1-X.
4. Built junk entries (`build_junk_and_controls.py`): A = filler propositions with frozen rows copied, fabricated trio, README row, registry rows S378–S381 (S381 fabricated URL); B = A with honest K17→S052; C = stuffed propositions.
5. Ran the checker on base, A, B, C; ran the seven frozen C1 controls on A (each in a fresh repo); split C1-X into its two sub-checks (`c1x_split.py`).

Host reads: none. Hold-out: not looked for, not opened, not encountered. Tools installed: none. Lane/fleet/sibling writes: none; no commits, no git mutations in the lane. Scratch removed before yield.

## Commands and decisive output

```
python3 -I c1_attack_check.py --repo <D0> --rev b50d44a3… --work <W>            (base)
MADO_KBD_ENTRY: rev=b50d44a3… rows=0/18 hosts=0/6 sources=0/18 new_rows=0/3 verdict=TARGET_MISSED missed=new_rows,entry_absent

python3 -I c1_attack_check.py --repo <junkA> --rev 2dd07426… --work <W> --escaped-pipes
MADO_KBD_ENTRY: rev=2dd07426… rows=18/18 hosts=6/6 sources=18/18 new_rows=3/3 verdict=TARGET_MET missed=none

python3 -I c1_attack_check.py --repo <junkA> --rev 2dd07426… --work <W>            (literal grammar)
MADO_KBD_ENTRY: … rows=17/18 … verdict=TARGET_MISSED missed=row:K16

python3 -I c1_attack_check.py --repo <junkB> --rev 30126e4b… --work <W> --escaped-pipes
MADO_KBD_ENTRY: … rows=18/18 hosts=6/6 sources=17/18 new_rows=3/3 verdict=TARGET_MISSED missed=source_cell:K17
# K17: source cell 'S052' is not a mined registry row whose URL ends '1.26.0/protocol/wayland.xml' and contains efb50993

seven frozen controls on junkA (fresh repos):
CTL C1-CTL-1 absent: expected=entry_absent pass=True          missed=entry_absent
CTL C1-CTL-2 spliced-quote: expected=quote:K04 pass=True      missed=quote:K04
CTL C1-CTL-3 shifted-anchor: expected=anchor:K01 pass=True    missed=anchor:K01
CTL C1-CTL-4 wrong-source: expected=source_cell:K10 pass=True missed=source_cell:K10
CTL C1-CTL-5 dropped-row: expected=row:K17 pass=True          missed=row:K17
CTL C1-CTL-6 host-forged: expected=host:H02 pass=True         missed=host:H02
CTL C1-CTL-7 pin-tamper: expected=pin_hash pass=True          missed=tables_sha,pin_hash
ATTACK_C1_CONTROLS: good=ok controls=7/7

c1x_split.py (NOT frozen):
junkA: C1X-id bad 24/24; C1X-dissim bad 24/24
junkB: C1X-id bad 24/24; C1X-dissim bad 24/24
junkC: C1X-id bad 11/24; C1X-dissim bad 19/24
```

Pin shas, `frozen-tables.json` sha (`bf46c889…`, embedded in the checker) and all 24 frozen quote-in-pin substrings hold at the freeze commit (junk A passes them).

## Result

- A junk entry satisfies the frozen C1 predicate and the seven-control harness: `TARGET_MET`, `good=ok controls=7/7`. It is 24 copied rows with 40/20-char placeholder propositions, a fabricated provenance trio, one README row and four registry rows.
- Legs a junk entry cannot fail without being a real transcription: `anchor`, `quote`, `host`, `pin_hash`, `tables_sha`. Legs it satisfies by fabrication: `new_rows` (shape only), `source_cell:K17` (fabricated URL). Full per-leg table in `attack.md` §3.
- Honest entries are blocked under the frozen text: `row:K16` (quote contains `||`, grammar forbids `|` in a cell) and `source_cell:K17` (S052 URL lacks the commit; the only other wayland row S043 is a local path). These are defects in the frozen predicate, not in any seat's work.

## Proposed clause (text only, not frozen)

C1-X: for each K/H row, the proposition contains at least two whole-word identifiers from that row's frozen quote (all of them if the quote has fewer than two); a failing row is `prop:<id>`. It stops junk A (24/24 fail) and not the stuffed junk C (13/24 pass). Could not be frozen now: the predicate has been fixed and a falsified predicate is an honest stop. Next-round cost: new predicate id and freeze commit before `.ready`; a new counter leg; an eighth control in the harness; regenerated `frozen-tables.json` with a re-embedded sha; re-run of the real entry (good=ok); a sealed stuffed-junk hold-out. Roughly one full round.

## Defects / ambiguities for L1 (none edited)

- D1 K16 vs the no-`|` rule; GFM `\|` escape is needed and unspecified.
- D2 K17 honest path impossible (S052 URL lacks `efb50993`); the reused-row rule and the contains-commit rule conflict for this pin.
- D3 `new_rows` "URL ending in a `new_row_pins` suffix": keys are basenames, no URL ends in them; only `source_suffix` values are workable.
- D4 C1-CTL-7 trips `tables_sha` as well; harness semantics for `missed=` (membership vs exact) unstated.
- D5 `sources=<n>/<n>` denominator unstated (18 assumed).
- D6 H-row S-cell `host` not enforced by any leg.
- D7 `recheck:` has no value grammar.
- D8 anchor cell "pin file" assumed basename.

## Could not verify

- The frozen counter and harness do not exist at `dbc2eefe` (`quality/counters/c1-r55-kbd-entry.py`, `quality/check-r55-controls.py` absent); all legs are from my re-implementation of the contract text, not from running the frozen code.
- No URL was fetched; S381's URL is unresolved and "not established by the pin set" refers only to the frozen table.
- Proposition-to-quote entailment was not checked beyond the identifier observation (the declared limit).
- Host files were not read on the host; no `hyprctl` run.
- Hold-out: not looked for, not opened.

## Deliverables

- `.ufo/waves/round-55/w1/R55RevC1Contract/attack.md`
- `.ufo/waves/round-55/w1/R55RevC1Contract/receipts/{run.txt,c1x-split.txt,junkA-entry.md,junkB-entry-honestK17.md,junkC-entry-stuffed.md,junkA-registry-rows.txt,junkA-readme-row.txt}`
- `.ufo/waves/round-55/w1/R55RevC1Contract/{c1_attack_check.py,c1x_split.py,build_junk_and_controls.py}`

Checks the main agent should run: the frozen `quality/counters/c1-r55-kbd-entry.py` and `quality/check-r55-controls.py --claim c1` once the counter exists, to confirm whether D1/D2 reproduce under the frozen code; `freeze-verify.py` on the freeze commit (not re-run by me).
