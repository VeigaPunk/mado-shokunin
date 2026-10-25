# Seat MutC1Controls — mutation probe of the C1 reference tool (round-40 w1)

Status: COMPLETE. 22 NEW single-defect mutants (ids M17–M52 continuing the shipped M01–M16) of
`.ufo/waves/round-40/c1/ctl-ref-tool.py.txt`, each scored with the frozen counter at the freeze
rev. **8 killed, 14 survived.** Every survivor is a coverage finding in `PRED-C1-r40-v1`'s
fixture space, listed below with the one-line change and the spelling/path that would kill it.
No contract, counter, fixture or sibling file was changed.

## What was attacked
The C1 reachability control: the reference live tool scores `fixtures=13/13` on the frozen
counter. Question: do further plausible single defects survive it? A 13/13 mutant means the
counter's generated trees/stubs/harness cannot distinguish the defective tool from the reference.

## Protocol (pristine / mutated / restored)
- Detector (bounded, same for every byte state):
  `python3 -I quality/counters/c1-r40-live.py --repo . --rev 5e7e88525cc539563de7746361b2650802e81809 --tool <file>`;
  metric = `fixtures=P/13` from the final line; P == 13 → SURVIVOR.
- **Pristine**: `fixtures=13/13 tool=present verdict=TARGET_MISSED`, clauses `a:1 b:0 g:1 k:1`,
  `clause=b rc=0 selftest=71/71` — matches the registration's declared control behavior
  (reachable fixtures, target not met because clause b needs n ≥ 79).
- **Mutated**: 22 files under `.ufo/waves/round-40/w1/MutC1Controls/mutants/`, each the pristine
  bytes with ONE substitution (asserted to match exactly once before writing; every mutant
  `py_compile`-clean).
- **Restored**: the reference file was never written; sha256 identical before and after
  (`f96d9e0a0d2fe1bccb87940244db079de88c6794f03d66a36304d574694a08aa`); `git status --porcelain
  -- .ufo/waves/round-40/c1/` empty; detector re-run on the unchanged bytes after all 22 mutant
  runs: `fixtures=13/13` again.

## Killed mutants (8) — observed detector output
| id | site (ref line) | one-line change | fixtures | first failure observed |
|----|----|----|----|----|
| M27 | 568 | `rgb(` comma branch requires `count(",") == 3` (4 parts) | 7/13 | gen0 `optx03:ginh3` mismatch≠agreement* (comma-rgb gradient colours unparsed) |
| M28 | 561 | rgba 8-hex decode `(x >> 8)…(x & 0xFF)` → `(x >> 4)…(x & 0xF)` | 3/13 | gen0 `optx06:grad6` mismatch |
| M34 | 598 | custom shape test `toks[-1].endswith("deg")` → `toks` (everything graded as gradient) | 0/13 | gen0 gap+weight keys mismatch |
| M38 | 724 | CtlError stderr text fixed (`live merge failed`), key unnamed | 10/13 | fail0/bad0 `rc=5 named=0`, missing0 `rc=5` |
| M45 | 626 | `text=True` dropped from the hyprctl subprocess | 0/13 | gen0 `optx08:bool8` "malformed reply" (bytes stdout breaks the `no such option` sentinel compare) |
| M48 | 638 | reply-form tuple loses `"custom"` | 0/13 | gen0 `optx012:grad12` "unknown reply form" |
| M50 | 671 | probe rows labeled `agreement` instead of `live-default` | 12/13 | probe0 `zzprobe:one/two` |
| M52 | 655 | mismatch condition `not isset or not native_equal` → `and` | 0/13 | gen0 differ/unset keys all `agreement` |
| M67 | 583 | decimal int test `v.lstrip("-").isdigit()` → `v.isdigit()` (negatives dropped) | 0/13 | gen0 `optx014:num14` (quirk num is negative in every tree) |

## SURVIVORS (14) — one-line change + what would kill it
| id | site (ref line) | one-line change | kill spelling / path |
|----|----|----|----|
| M17 | 553 | rgba comma alpha `int(round(x*255))` → `int(x*255)` | generator `ALPHAS` gains a value where `int(a*255) != round(a*255)`, e.g. `"0.5"` (127.5 → 127 vs 128); current grid {1, 0.8, 0.4} multiplies to exact floats 255.0/204.0/102.0 (verified), so truncation is invisible |
| M18 | 632 | sentinel `text == "no such option"` → `"no such option" in text` | a str-form fixture whose live value is the phrase itself (declared str `no such option` → stub emits JSON containing it → mutant misreads config-only) |
| M19 | 631 | spurious strictness: reject when `p.stdout != text + "\n"` | stub emitting a padded reply (leading spaces / blank lines around the JSON) → mutant exits 5 on a valid run |
| M20 | 663-664 | probe de-dup `if key in seen: continue` removed | `score_probe` passing a duplicate `--probe` key or a probe naming a declared key → duplicate argv/row fails the argv-shape check |
| M21 | 665-666 | probe-loop `native_query` wrapped in `try/except CtlError: continue` | a failure fixture whose failing key is a **probe** key (stub mode `fail:<probe-key>`); `score_fail`'s victim is always `sorted(fx.opts)[3]`, a declared key, so probe-loop failures are unreachable |
| M23 | 594 | float compare `abs(fd-fl) < 1e-6` → `fd == fl` | float fixture where declared/live differ within 1e-6 but not exactly (declared with >2 decimals, e.g. `1.3700001` vs live 1.37); generator emits 2-decimal strings vs `round(...,2)` lives — always exactly equal |
| M24 | 596 | str compare drops `.strip()` on the live side | str fixture with padded declared/live value (e.g. ` w123 `); generator strs are `w%d`, never padded |
| M25 | 618 | weight lookup drops `.lower()` | weight fixture with uppercase/mixed-case name (`BOLD` → live 700); `WSPELL` is lowercase-only |
| M26 | 602 | gradient angle `int(tok[:…deg])` → `float(...)` | gradient fixture with a fractional angle token (`45.5deg`): `int()` raises → mismatch, `float()` accepts; fixture angles are {0,45,90}deg |
| M32 | 614 | 2-value gap expansion `[n0,n1,n0,n1]` → `[n0,n0,n1,n1]` (CSS v/h swapped) | any fixture with a 2-integer gap of distinct values (`5 9` → live `5 9 5 9`, mutant `5 5 9 9`). **Seed-dependent**: at rev 5e7e885 no 2-value gap materialized in any of the 13 fixtures (first gap instance is always the 3-value quirk; second instances sample gap 6/8 × n=2 1/4 ≈ 7.7% chance of none) |
| M40 | 672 | `rows.sort(key=…)` removed from `merge_live` | counter asserting row order (`[r["key"] for r in rows] == sorted(...)`); labels are compared as dicts, so order is invisible (only the tool's own selftest checks order, and clause b is already 0) |
| M41 | 654 | `row["live"] = str(value)` → `row["live"] = value` (raw int/float) | counter asserting the live field's type/value (`isinstance(row["live"], str)` or `== str(value)`); only presence (`is None`) is checked |
| M43 | 695 | `--hyprctl` default `"hyprctl"` → `""` | one valid fixture run omitting `--hyprctl` (exercising the default program lookup); every `check_live` passes the stub explicitly |
| M19-note | — | (see M19) | — |

## Coverage findings (the blind spots, grouped)
1. **Generator value space**: alpha grid on the exact-integer lattice (M17), lowercase-only
   weight names (M25), integer-only gradient angles (M26), float declared/live always exactly
   equal (M23), str values never padded (M24), no 2-value gap at this rev (M32, seed-dependent).
2. **Stub reply protocol**: replies are always clean single-line JSON (M19), never contain the
   sentinel phrase (M18), always carry `set` and a known form; the sentinel is only exercised in
   text mode (M45 dies on the bytes/str sentinel compare, not on JSON parsing).
3. **Harness checks**: labels (got/want), argv shape, live-presence, tree immutability and exit
   codes/messages are checked — but row order (M40), row field types (M41), the `set` field, and
   the `--hyprctl` default path (M43) are not; probe keys are never duplicated (M20) and never a
   failure victim (M21).

## Safety / harm watch
- Writes confined to `.ufo/waves/round-40/w1/MutC1Controls/` (mutants/) plus this report; no
  tracked file edited; no git mutation (read-only `rev-parse`/`status` only); no pacman; **no
  tools installed** (operator authorization unused — system `python3` stdlib sufficed); no
  compositor contact (the counter drives a stub `hyprctl`; this seat never ran host `hyprctl`);
  the counter's own `mkdtemp` scratch is removed by the counter; nothing else left in /tmp.

## Verdict
The frozen counter kills 8 of 22 further single-defect mutants but **14 survive 13/13** — the
fixture space has systematic blind spots (value-space grid, stub reply hygiene, harness field
checks). Per the mutation-testing contract these are coverage findings only: the counter, the
fixtures and the reference tool are untouched, and the survivors do not weaken the C1 claim —
they bound what its fixtures can prove.
