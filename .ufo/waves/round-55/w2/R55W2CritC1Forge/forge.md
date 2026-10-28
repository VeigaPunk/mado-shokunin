# R55W2CritC1Forge — can PRED-C1-r55 be defeated as integrated?

Scope: attack `quality/counters/c1-r55-kbd-entry.py` (the real counter, unchanged) and `quality/check-r55-controls.py --claim c1` (the real harness, unchanged) on forged entries. Scored rev under test: `57584ed67716340b3d466fa04333ac0bab3fb79e`. Driver: `receipts/forge.py` (copy of the scratch driver). Receipts: `receipts/` next to this file.

## Setup (what ran)

- Base: `git archive 57584ed… | tar -x` into a scratch `git init` repo, committed as `base` (tree `feecf8d8…` equal to `57584ed^{tree}`; lane untouched — only `git archive`/`cat-file`/`ls-tree` reads of the lane).
- Each variant: `git clone --no-hardlinks` of `base` into scratch, one edit to `corpus/knowledge/hyprland-keyboard-repeat-numlock-r55.md`, one commit (`-c user.name=ctl -c user.email=ctl@ctl`), `git rev-parse --show-toplevel` asserted equal to the clone dir before the commit.
- The counter blob at every variant is `53ec8a1a84555a7c7a7dc5941c422a48a6d31ddf`, the same blob as `57584ed:quality/counters/c1-r55-kbd-entry.py`. The harness blob is `a61d5c28…`, the same as at the scored rev. `frozen-tables-v2.json`, pins, SOURCES.md and README.md are identical to the scored rev in every variant (`git diff --name-only HEAD~1 HEAD` lists only the entry file).
- Commands (per variant `V`, scratch repo `$V`, rev `$SHA`):
  - `python3 -I $V/quality/counters/c1-r55-kbd-entry.py --repo $V --rev $SHA --work $W`
  - `python3 -I $V/quality/check-r55-controls.py --claim c1 --repo $V --rev $SHA --work $W`
- Baseline at the lane itself (read-only, `receipts/lane-baseline-57584ed.txt`): counter `TARGET_MET rows=18/18 hosts=6/6 sources=18/18 new_rows=3/3`, rc 0; harness `good=ok controls=7/7 verdict=OK`, rc 0. The harness and counter are working as described on the honest entry.

## Results (decisive output, `receipts/summary.json`, per-variant `receipts/<name>/`)

| variant | what the forgery is | counter (rc) | harness |
|---|---|---|---|
| control-base | none (archive of scored rev) | `TARGET_MET … missed=none` (0) | `good=ok controls=7/7 verdict=OK` |
| control-entry-absent | entry file deleted; README/SOURCES kept | `rows=0/18 … verdict=TARGET_MISSED missed=entry_absent` (1) | `good=bad controls=0/7 verdict=FAIL` (1) |
| **J1-junk-placeholder** | provenance trio + 18 K rows + 6 H rows; frozen quote and anchor per row; every proposition the placeholder `placeholder proposition text for row K04, not a claim about any source line` (or `placeholder host proposition H0x, not a read`); real registry S-ids; no prose | `rows=18/18 hosts=6/6 sources=18/18 new_rows=3/3 verdict=TARGET_MET missed=none` (0) | `good=ok controls=7/7 verdict=OK` |
| **B1-false-K04-cap200** | only K04's proposition changed: `The stored repeat rate m_repeatRate is capped at 200 by std::max(0, REPEATRATE) on this line.`; quote `std::max(0, REPEATRATE);` unchanged | `TARGET_MET … missed=none` (0) | `good=ok controls=7/7 verdict=OK` |
| **B2-false-all-rows** | all 18 K and 6 H propositions replaced with sentences that contradict their quotes (e.g. K01 "never reads repeat_rate; hard-codes 25"; K13 "default 2500 and a maximum of 20"; H04 "returned 4 for input:repeat_rate, not 40"); lengths ≥40/≥20 | `TARGET_MET … missed=none` (0) | `good=ok controls=7/7 verdict=OK` |
| **C1-same-family-swap** | K13, K14, K15 cite `S215` instead of `S318`; K16 cites `S162` instead of `S317`; quotes, anchors, propositions as honest | `TARGET_MET … missed=none` (0) | `good=ok controls=7/7 verdict=OK` |
| **P1-provenance-forged-S999** | line 1 `source: S999, S317, …` (no such registry id); everything else honest | `TARGET_MET … missed=none` (0) | `good=ok controls=7/7 verdict=OK` |

Decisive lines (verbatim, from `receipts/<variant>/counter.out` and `harness.out`):

- J1: `MADO_KBD_ENTRY: rev=8ff1bec293c467d01a987bd9c19c4dad23202408 rows=18/18 hosts=6/6 sources=18/18 new_rows=3/3 verdict=TARGET_MET missed=none` / `MADO_R55_CONTROLS: claim=c1 good=ok controls=7/7 verdict=OK`
- B1: `… rows=18/18 hosts=6/6 sources=18/18 new_rows=3/3 verdict=TARGET_MET missed=none`; the K04 row in the tree reads `| K04 | The stored repeat rate m_repeatRate is capped at 200 by std::max(0, REPEATRATE) on this line. | S316 | Hyprland-InputManager.cpp:1282 | `std::max(0, REPEATRATE);` |`
- C1: K13 row `| K13 | … | S215 | Hyprland-ConfigValues.cpp:279 | `"input:repeat_rate", … ` |`; `… verdict=TARGET_MET missed=none`
- P1: first line of the entry `source: S999, S317, S318, S319, S052 (existing registry rows), …`; `… verdict=TARGET_MET missed=none`

Every variant keeps the frozen grammar (5 cells, single-space pipes, backtick quote, `<pin>:<line>` anchor, ≥40/≥20-char proposition, `S###` or `host`), so none is a syntactic rejection; the counter's acceptance is the content of a valid row, not a parser gap (QUALITY 105 requirement met for every reported pass).

## Why each passes (from the counter's code, `c1-r55-kbd-entry.py`)

- `split_row` / the row check read the cell count and the id; the proposition is tested only by `len(prop) >= 40` (K) or `>= 20` (H) and by "no leading/trailing whitespace". Nothing reads its meaning (lines 297–305, 377–381). So J1 and B2 pass; B1 is the same test with one sentence.
- `quote:<id>` and `anchor:<id>` bind the quote text to its pin line (`fr["quote"] in pin_line`). The quote is genuine in all variants, so the frozen quote leg is satisfied by true text next to a false claim.
- `source_ok` (lines 266–276) checks that the row's S-id names exactly one registry row, that it is `mined`, and that its last URL ends with the pin's `source_suffix` (and contains the commit for `Hyprland-*` pins). It does not read the registry's `teaches`, `scope` or `anchor` cells. S215 (`ConfigValues.cpp`, scope "the shipped defaults of the compositor's two log switches", anchor lines 629/632) and S162 (`ConfigManager.cpp`, windowrule handlers) both satisfy it for pins of the same file. So C1 passes. S378 → S316 (cross-family) is still caught by `source_cell:K10` (harness CTL-4), so the gap is exactly the same-family swap.
- `provenance` (lines 335–340) checks that the head contains an `S###` token on a `source:` line, the literal `verified-at: 2026-10-28`, and a non-empty `recheck:`. It does not check that the S-id is in the registry. P1 shows this.
- Harness: every control is a mutation of the honest tree; none inspects the propositions, and none can. Junk and false-proposition trees pass the 7 controls exactly as the honest tree does (J1, B1, B2, C1, P1 all `controls=7/7`).

## Verdicts a human reviewer would reject

| variant | counter | human reviewer | reason |
|---|---|---|---|
| J1 junk | TARGET_MET | REJECT | 18+6 rows whose propositions say nothing about any source; it is a do-nothing-equivalent that carries only frozen quotes |
| B1 K04 cap-200 | TARGET_MET | REJECT | pin line `Hyprland-InputManager.cpp:1282` is `std::max(0, REPEATRATE);`: a floor at zero, no cap; the row claims a cap |
| B2 all-rows false | TARGET_MET | REJECT | every row contradicts its own quote (24 rows) |
| C1 same-family swap | TARGET_MET | REJECT (K13–K16) | the quote is real, but the cited registry rows (S215: log-switch defaults at lines 629/632; S162: windowrule handlers) do not scope lines 277–280 or 1119 of the pin; the citation is wrong although the file family matches |
| P1 forged S999 | TARGET_MET | REJECT (provenance) | `S999` is not a registry id; the provenance line is a claim without a referent |

The counter's own purpose (quote identity at an exact pin line, row and host binding) survives every variant. What fails is the reading "TARGET_MET = a sourced entry": the counter cannot tell B1/B2/J1 from the honest entry, and it cannot tell S215-for-K13 from S318-for-K13 (the only check that could is the registry-scope read the registration does not require).

## Do-nothing control and the v2 errata

- The registered do-nothing control (entry absent, `control-entry-absent`, and harness CTL-1) scores `TARGET_MISSED missed=entry_absent`, so the absent control does not meet the target. That part of the picture is unchanged by v2: the v2 table (E1–E9) changes quotes, `source_cell` URL rule, host lookup, row/sources counts, control legs and the hold-out commitment; none adds a content check to the proposition.
- The do-nothing-equivalent that matters is J1 (quotes, anchors, real S-ids, placeholder propositions). It meets the target under the counter as shipped and the harness as shipped. Under §9 as stated in the round's claims ("predicate wrong" if a do-nothing-equivalent control meets the target), this is the predicate-wrong outcome for PRED-C1-r55 as a sourced-entry predicate. The L1 already records this (`registration-v2.md` "Unchanged and still declared limits"); this run quantifies it: it is not a rare edge, it is the cheapest path to TARGET_MET.
- v2 changed the picture in one respect. The registration-v2 text says v1 could not be met by any entry (K16's quote contained `||` against "no `|` inside a cell"; K17's registry URL could not contain the frozen commit). Under v1 no junk entry could reach TARGET_MET either. v2 makes the target reachable, and the reachable route the counter accepts includes J1. I did not run the v1 tables (the counter embeds the v2 sha; running v1 would need an edited instrument), so this rests on the v2 text and the counter's code: UNVERIFIED by run.

## What this does not show

- It does not show the honest entry's propositions are wrong; the sentence-to-pin audit (a separate seat) is what decides that. I read B1/B2 only as forgeries that the counter misses.
- No mutation touched the lane. All writes are in `/fast/scratch/hyaku/mado-r55/R55W2CritC1Forge/` (removed before yield) and this deliverable directory. No hyprctl, no config, no fleet repo, no commits in the lane.
- Tools: none installed; no pacman; the driver uses only python3 -I and git.
