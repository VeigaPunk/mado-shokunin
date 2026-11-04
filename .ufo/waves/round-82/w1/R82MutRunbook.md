# R82MutRunbook — independent mutation probe of the C2 instrument

Seat: `R82MutRunbook` (leaf). Wave: round 82, w1. Lane: `/home/vgpnk/Projects/shokunin/mado-shokunin`.
Freeze under test: `780c30fcae12d74ce8ab3b871a0888696c2415d9` (base `6ea2386d49318a5f223097c78b5fe79c31b064f8`).
Instrument: `quality/counters/c2-r82-runbook.py`, sha256 `1e8eb49928bfc9b8e5e1e72da74c0496cbe6d095fe3fdc72c479fffd80b3fb0f`
(pinned value `1e8eb499…`, re-hashed after every run: unchanged). Controls
`.ufo/waves/round-82/controls/c2-runbook-cases-r82.json` sha256 `f64d7d5db40fc1da3d75c15315274264dfb53c38396135b978dff7b0b04b36d5`,
carried `.ufo/waves/round-81/controls/c2-runbook-cases-r81.json`. All work read-only over the lane; every
mutant ran from `/fast/scratch/hyaku/mado-r82/R82MutRunbook/`. No tool installs, no `task`, no commits.

## Axes

1. **Discrimination** — does the frozen 29-case set kill a plausible defect in each matcher arm?
2. **Locus** — is the kill carried by an r82-new row (operability) or by a carried row (regression)?
3. **Redundancy** — is a surviving mutant a real looseness (GAP) or a semantically neutral edit (EQUIVALENT)?

## 1. Baseline reproduction (frozen command, run once, verbatim)

```
python3 -I quality/counters/c2-r82-runbook.py --repo . --rev 780c30fcae12d74ce8ab3b871a0888696c2415d9 \
  --controls .ufo/waves/round-82/controls/c2-runbook-cases-r82.json \
  --carried .ufo/waves/round-81/controls/c2-runbook-cases-r81.json \
  --scratch-root /fast/scratch/hyaku/mado-r82/R82MutRunbook/work
```

- Output is **byte-identical** to `.ufo/waves/round-82/receipts/measurement-c2-r82.txt` (`diff` empty).
- `cases=29 executed=29 matched=29 shapes=24/24 anchors=29/29 rows=29/29 control_new=0/3 mutants=25 killed=25 verdict=TARGET_MET`.
- `--selftest`: `MADO_R82_RUNBOOK_SELFTEST: 90/90`, rc 0. (The wave brief's `133/133` is the C1 tool
  `tools/mado-barfoot.py`; the C2 instrument's own count is 90 checks — not a discrepancy.)
- Frozen 25 mutants: **25/25 killed**. Weakest kill is `rc-blind` at `matched=19/29`; the other 24 sit at
  25–28/29. Per-mutant lines: `base-run.txt`.

## 2. Five authored mutations (none of the 25; each = base + one bounded replacement)

| # | mutant | site | selftest | full run | matched | cases broken | verdict |
|---|---|---|---|---|---|---|---|
| M1 | `regex-search-to-match` | `:311-312` | 90/90 | rc 1 | 27/29 | `tray-owner`, `tray-interface` | **KILLED** |
| M2 | `lines-shape-floor-minus-one` | `:317-319` | 89/90 | rc 1 | 27/29 | `omarchy-menu-keybindings`, `tray-methods` | **KILLED** |
| M3 | `array-fields-dict-accepted` | `:385-387` | 90/90 | rc 0 | 29/29 | — | **GAP** |
| M4 | `refusal-stage-prefix` | `:431` | 90/90 | rc 0 | 29/29 | — | **GAP** |
| M5 | `row-binding-double-bind-allowed` | `:678-680` | 90/90 | rc 0 | 29/29 | — | **EQUIVALENT** |

Each mutant source is in `w1/R82MutRunbook/`; diffs vs base are 2/2/5/2/2 lines. Full run outputs
(`mutant-<name>.run.txt`) carry all 29 probes; selftests (`mutant-<name>.selftest.txt`).

### M1 `regex-search-to-match` — KILLED by two r82-new rows
`return re.search(value, text)` → `re.match(value, text)`. The three `^`-anchored carried patterns
(`version`, `monitors-size`, `omarchy-version`) still match at position 0, so the mutant survives them; the two
tray census patterns are unanchored-at-0 and rely on `(?m)^` to find a line inside a multi-line `busctl`
table, so both break:

```
MADO_R82_PROBE: name=tray-owner row=26 kind=regex match=no rc=0 out='NAME      PID PROCESS ...'
MADO_R82_PROBE: name=tray-interface row=27 kind=regex match=no rc=0 out='NAME   TYPE  SIGNATURE ...'
```

This is the operability axis doing work: only the round-82 tray rows pin "search a line, not a prefix".
Selftest does **not** catch it (its regex checks are `^`-anchored).

### M2 `lines-shape-floor-minus-one` — KILLED by one carried and one new row
`len(lines) < min_lines` → `< min_lines - 1`. Separated at both boundaries the frozen set happens to pin:
`omarchy-menu-keybindings` (min_lines 100; its negative #3 is exactly **99** lines) and `tray-methods`
(min_lines 2; its negative #1 is exactly **1** line, `.RegisterStatusNotifierItem method s - -`). Both probes flip
to `match=no`. The instrument's own selftest also dies on this one: `SELFTEST_FAIL: lines shape length floor`
→ `89/90`, rc 1.

### M3 `array-fields-dict-accepted` — **GAP** at `c2-r82-runbook.py:385-387`
The arm accepts any `dict` and iterates its values:

```python
if not isinstance(data, (list, dict)) or len(data) < value.get("min_items", 1):
    return False
items = list(data.values()) if isinstance(data, dict) else data
return all(fields_ok(item, value) for item in items)
```

Witness, using the frozen `monitors-dump` schema verbatim:

| input | base | mutant |
|---|---|---|
| `[{"name":"DP-1","width":3440,"height":1440,"reserved":[0,26,0,0],"scale":1.0}]` | True | True |
| `{"DP-1": {"name":"DP-1",...same fields...}}` (JSON object, not array) | **False** | **True** |

No frozen case supplies an object-form reply: `monitors-dump`'s two negatives are both arrays (bad `int4`,
empty `name`), and the selftest's `array_fields` checks are array-only. So the "array" in `array_fields` is
not frozen — an output-keyed map (the shape `hyprctl layers -j` actually uses, handled correctly by
`levels_dump`) passes the monitors row as free.

### M4 `refusal-stage-prefix` — **GAP** at `c2-r82-runbook.py:431`
Dropping the trailing space of `"ERROR (stage=%s "` accepts any stage that merely *starts with* the frozen
stage:

| reply (rc 3, stage=`model`) | base | mutant |
|---|---|---|
| `MADO_BARFOOT: ERROR (stage=model a reason)` | True | True |
| `MADO_BARFOOT: ERROR (stage=modeling a reason)` | **False** | **True** |
| `MADO_BARFOOT: ERROR (stage=model2 a reason)` | **False** | **True** |
| `MADO_BARFOOT: ERROR (stage=setup unreadable)` | False | False |

All four refusal cases' negatives pin `stage=setup` only, so the boundary between `model` and `model*` is
unfrozen. Note this is *not* the frozen `refusal-stage-blind` mutant (which accepts any stage and is killed at
25/29); the frozen set kills the coarse edit but not the one-character boundary edit.

### M5 `row-binding-double-bind-allowed` — **EQUIVALENT**, not a gap
Disabling the duplicate-anchor raise (`:678-680`) survives at 29/29, but the mutant is behaviourally neutral:
with `CASES == 29` and `len(hits) != 1` raised first (`:675-677`), any duplicate drops `len(bindings)` below 29
and the independent guard at `:682-683` refuses the same set. Verified with a doctored controls copy whose
rows 27/28 share one anchor (`controls-double-bind.json`):

| binary | output | rc |
|---|---|---|
| base | `ERROR (stage=setup row 27 is bound by 'tray-interface' and 'tray-methods')` | 2 |
| M5 | `ERROR (stage=setup only 28 of 29 rows are bound)` | 2 |

Same verdict, different diagnostic. The duplicate check is a message-quality guard, not a discriminator — its
survival is not a coverage hole in the case set, and no case could close it without changing the `CASES`
invariant.

## 3. Findings

| id | finding | code | risk | closes with |
|---|---|---|---|---|
| G1 | `array_fields` accepts a JSON object (values checked as items) — the array contract is unfrozen | `quality/counters/c2-r82-runbook.py:385-387` | medium: an output-keyed map satisfies `monitors-dump` | one negative, `kind=array_fields`, object of one valid monitor |
| G2 | refusal stage boundary unpinned: `stage=model*` accepted (missing trailing-separator guard) | `quality/counters/c2-r82-runbook.py:431` | low: a sibling stage sharing the `model` prefix passes as the modelled refusal | one negative, rc 3, `ERROR (stage=modeling …)` |
| G3 | duplicate-row guard at `:678-680` is redundant with the `len(bindings)` guard at `:682-683` | `quality/counters/c2-r82-runbook.py:678-680` | none: equivalent mutant (proved above) | no action; keep for the message |

No frozen value, receipt, instrument or control byte was touched: after all runs
`c2-r82-runbook.py = 1e8eb499…`, `mado-barfoot.py = 38007528…`, `c1-r82-allocation-band.py = 1e9f394d…`,
`c2-runbook-cases-r82.json = f64d7d5d…`, each equal to the pinned hashes. The measured claim
(29/29 matched, 24/24 shapes, 29/29 anchors, control_new 0/3, 25/25 killed) reproduces exactly; G1/G2 are
separation-power gaps for a later round, not falsifications of this claim.

## 4. Hygiene

- Wrote only `/fast/scratch/hyaku/mado-r82/R82MutRunbook/` and
  `.ufo/waves/round-82/w1/R82MutRunbook/` (mutants, selftests, run logs, `mutants.json`) plus this report.
- No `/tmp` writes, no writes to the fleet root or any sibling lane, no `git` mutation, no subagents, no peer
  messages. Scratch root `/fast/scratch/hyaku/mado-r82/R82MutRunbook` removed after the probe (mutants and
  logs preserved in the seat directory).
- A sibling seat committed `3ec7fb75` (corpus/sources) while this probe ran; the freeze is still an ancestor
  and every frozen byte re-hashed to its pinned value, so the measurements are unaffected.

STATUS: ok
