# R55W2MutC1CounterA — report (wave w2, mutation of the C1 counter)

Scope: mutate `quality/counters/c1-r55-kbd-entry.py` at scored revision `57584ed67716340b3d466fa04333ac0bab3fb79e` and run the counter's own selftest and the independent harness (`quality/check-r55-controls.py --claim c1`) against each mutant. Full table, commands and receipts: `.ufo/waves/round-55/w2/R55W2MutC1CounterA/mutants.md`; mutant files in `.ufo/waves/round-55/w2/R55W2MutC1CounterA/mutants/` (32 files, sha256 in `receipts/manifest.json`).

## What ran

- Export of the lane's counter, harness, frozen tables, pins and the entry/README/SOURCES inputs by `git archive` at the scored revision into scratch; committed in a scratch repo (`fa1d6c70…`), toplevel asserted, identity `ctl`. Lane not edited, no git write against the lane.
- Baseline, unmutated: counter `TARGET_MET … missed=none` rc 0; selftest `50/50 passed`; harness `good=ok controls=7/7 verdict=OK`.
- 32 one-edit mutants (11 leg-drops as required, 1 flip per leg-related comparison, plus clause drops). Each run with `python3 -I`: selftest and harness (`--counter` on the mutant copy).
- Eight real-tree demonstrations (A–H) and one unit probe (m25): unchanged counter versus the mutant on one scored-tree edit each.
- Nothing installed, no `hyprctl` call, no pacman, no service change. Scratch removed before yield.

## Verdicts

| target | verdict | evidence |
|---|---|---|
| The shipped C1 counter reproduces its green line and its selftest on the scored tree | SURVIVES | baseline in `receipts/baseline/` (TARGET_MET, selftest 50/50, harness 7/7) |
| The 11 required leg-drop mutants are each detected by the selftest or the harness | SURVIVES | m01–m11 all killed (table in `mutants.md`) |
| The frozen harness (7 controls + good tree) kills every one-edit mutant of the counter | BROKEN | 9 of 32 survive all checks: m16, m19, m20, m21, m22, m24, m25, m26, m32 |
| Verdict-level: a weakened counter reaches TARGET_MET on a tree the shipped counter marks TARGET_MISSED | BROKEN (for the mutants; not the shipped counter) | demos A (m16 foreign commit on S318 → TARGET_MET), B (m19 leading space in K01 proposition → TARGET_MET), C (m20 `\|  K07 \|` → TARGET_MET), D (m21 S379 opened 2026-10-26 → TARGET_MET), E (m22 S379 tier B → TARGET_MET) |
| Leg identity: the frozen harness distinguishes the named leg for the anchor and quote clauses | BROKEN (for the mutants) | demo F (m24: `row:K01` → `anchor:K01`), demo G (m26: `quote:K01,pin_hash` → `pin_hash`), demo H (m32: `row:K05` → `quote:K05`) — verdict unchanged, leg name lost |
| Legs with no frozen-harness control | BROKEN (coverage gap) | `provenance`, `index`, `new_rows` have no required control; `tables_sha` only as collateral of C1-CTL-7 (m11 leaves the harness at 7/7). Selftest covers them. |

## Leg-to-control summary (from `mutants.md`)

- Harness controls exercise: entry_absent (CTL-1), row (CTL-5, K17 only), anchor (CTL-3, K01 only), quote (CTL-2 K04; CTL-6 H02), pin_hash (CTL-7), source_cell (CTL-4, K10 S-id only), host (CTL-6, H02 only).
- No harness control: provenance, index, new_rows. tables_sha: no required control.
- Unguarded by both selftest and harness: source commit clause (m16), proposition whitespace (m19), id-cell spacing (m20), new-row `opened` (m21), new-row tier (m22), `\|` in anchor cell (m24), pin-line final-line bound (m25, stricter only), quote substring clause (m26), `\|` in quote cell (m32).

## Smallest kill tests (text; details in `mutants.md`)

- m16: S318 registry URL with a foreign commit → expect `source_cell:K13,K14,K15`.
- m19 / m20: K01 proposition with a double space after the first pipe; K07 id cell `|  K07 |` → expect `row:K01` / `row:K07`.
- m21 / m22: S379 `opened` 2026-10-26 / tier B → expect `new_rows=2/3 missed=new_rows`.
- m24: K01 anchor `…:1220|x` → expect `row:K01`.
- m25: unit `pin_line(b"line one\nline two",2) == "line two"`.
- m26: edit one character of the K01 quote inside the pin (no table change) → expect `missed=pin_hash,quote:K01`.
- m32: K05 quote with `\|` → expect `row:K05`.

## Not verified / limits

- 32 one-edit mutants, not exhaustive. Not mutated: `valid_shape`, the `count_new_rows` loop, the fence regex, `PROV_WINDOW`, and the harness itself.
- The counter's selftest is synthetic (the good tree is generated); it is not independent of the counter. Only the harness judges the real entry, and only through its good tree and seven controls.
- The proposed kill tests are text; only the demonstrations (A–H, m25 unit) were run, on the unchanged counter and the mutants.
- Whether the L1 adds any proposed control to the frozen harness is a decision for the L1; this seat reports the gap only.
- Mutation runs used copies in scratch; the lane has no change from this seat. `git -C <lane> status` shows only other seats' untracked artifacts.
