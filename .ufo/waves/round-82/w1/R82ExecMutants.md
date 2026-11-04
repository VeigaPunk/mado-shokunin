# R82ExecMutants — independent mutation of the C1 allocation instrument

Seat `R82ExecMutants`, round 82 wave 1. Read-only over the lane: every experiment ran in
`/fast/scratch/hyaku/mado-r82/R82ExecMutants` (removed at exit); durable copies of the six
mutants, the frozen command output, the independent driver and its logs are under
`.ufo/waves/round-82/w1/R82ExecMutants/`. No frozen instrument, control set or claim
declaration was written; no git mutation was run.

## Instrument identity (checked, not assumed)

| object | digest / size |
|---|---|
| lane freeze | `780c30fcae12d74ce8ab3b871a0888696c2415d9` (HEAD was `b6146ee6…`, unused) |
| `tools/mado-barfoot.py` extracted from the freeze | `380075284d7d5c6f56a82600935d512def617223be27f33241ff5dbcb0bcab59`, 1580 lines — byte-identical to the lane file |
| `quality/counters/c1-r82-allocation-band.py` | `1e9f394df80284e78f1fdf3f24cb5e14d1e4091f4880ccc60a2a45060b54612d` |
| `.ufo/waves/round-82/controls/c1-cases-r82.json` | `e404bb3fa93d5f12338129adc8733574084e6fab2ee12fbb471dd45df94a315f`, 47 cases |

## Step 1 — the counter's own 47 cases against the extracted tool: 47/47

Two independent paths, both from the extracted bytes:

(a) Own driver (`runner.py`, a fresh implementation: writes each fixture, runs
`python3 -I <tool>`, parses `MADO_BARFOOT_RESULT`/`MADO_BARFOOT_ATTR` independently and
compares every `expect` field, including `attr_ns` and the refusal `stage`):

```
python3 runner.py tool.py c1-cases.json work-base tool
PASS 47/47 FAIL 0: -
```

Saved as `out-base.txt`. (The baseline uses the same case bytes as the control set —
sha256 above — from the scratch copy.)

(b) The frozen command itself prints `cases=47 correct=47` (summary in step 4).

## Step 4 — the frozen command once: all 34 named mutants die

Run verbatim from the lane root, output saved as `frozen-counter-output.txt`:

```
cd /home/vgpnk/Projects/shokunin/mado-shokunin
python3 -I quality/counters/c1-r82-allocation-band.py --repo . \
  --rev 780c30fcae12d74ce8ab3b871a0888696c2415d9 \
  --base-rev 6ea2386d49318a5f223097c78b5fe79c31b064f8 \
  --controls .ufo/waves/round-82/controls/c1-cases-r82.json \
  --carried .ufo/waves/round-81/controls/c1-cases-r81.json \
  --scratch-root /fast/scratch/hyaku/mado-r82/R82ExecMutants/frozen
```

- rc 0; stdout is **byte-identical** to `.ufo/waves/round-82/receipts/measurement-c1-r82.txt`
  (`diff -u` → no output, `IDENTICAL`).
- 34 `MADO_R82_MUTANT` lines; `killed=yes` ×34, `killed=no` ×0.
- Summary line:
  `MADO_R82_BARFOOT: cases=47 correct=47 mutants=34 killed=34 base_correct=39/47 carried=39/39 tool_selftest=133/133 verdict=TARGET_MET rev=780c30fc… tool_sha256=38007528…`

The 34 per-mutant correct counts read off those lines (all `killed=yes`):

```
opposite-margin-dropped 36   horizontal-margin-leak 36   level-bottom-swap 46
right-extent-flip 45         per-side-margin-dropped 46   negative-margin-accepted 46
opposite-edge-wrong 46       static-dropped 44            static-order-swapped 44
static-first-wins 43         static-box-unoffset 43       static-selector-ignored 46
attr-edge-order 31           running-bounds-ignored 34    exclusive-edge-ignored 46
edge-guard-dropped 46        invalid-area-kept 46         full-box-uses-usable 46
empty-box-contributes 46     same-level-order-ignored 46  zone-margin-not-added 46
attribution-not-summed 31    tie-round-trunc 46           round-width-spec 46
auto-gate-open 44            auto-gate-and 44             auto-axis-swapped 46
auto-dynamic-kept 46         alloc-explicit-overridden 12 alloc-zero-accepted 46
alloc-axis-lost 43           alloc-negative-accepted 46   alloc-unknown-kept 46
alloc-composition-ignored 46
```

## Steps 2–3 — six independent mutants of the new allocation code

`gen_mutants.py` asserts every anchor occurs exactly once in `tool.py` and writes
`mutants/mutant-<name>.py`; each mutant differs from the frozen bytes by exactly one hunk
(checked with `diff -u`). `runner.py <mutant> c1-cases.json <work> <name>` scored each
against all 47 cases. Mutants are frozen-tool edits only; copies are in
`.ufo/waves/round-82/w1/R82ExecMutants/mutants/` with `SHA256SUMS.txt`.

| # | mutant (sha256 / `tool.py` line) | semantic change | failed / 47 | separating case |
|---|---|---|---|---|
| 1 | `zero-guard-tests-declaration` `16818194…` / `:468` | zero-band guard evaluates the **declaration** (`spec[axis] <= 0`, always true in the dynamic case) instead of the resolved allocation | **4** | `alloc-dyn-height-top` (also `alloc-dyn-height-margin`, `alloc-dyn-width-dock`, `alloc-composition-dyn-bar`) |
| 2 | `alloc-wrong-axis` `5980a5d9…` / `:460` | allocation looked up on the cross axis (horizontal surfaces read `width`, vertical read `height`) | **35** | `alloc-explicit-ignored` inside the new class; first carried separator `host-top` |
| 3 | `alloc-overrides-explicit` `f6e08004…` / `:461-465` | allocation is consulted before the declaration, so a positive declared band is overridden | **1** | `alloc-explicit-ignored` |
| 4 | `alloc-bool-accepted` `b3dbeff5…` / `:448` | the `isinstance(value, bool)` exclusion is dropped, so JSON `true`/`false` parse as an allocation | **0 → GAP** | none — see below |
| 5 | `composition-allocation-dropped` `d029e421…` / `:803` | the composed bar's band is resolved against `{}`, not the declaration | **1** | `alloc-composition-dyn-bar` |
| 6 | `alloc-margin-double-counted` `807aa281…` / `:481` | a dynamic band's height gets both margins added while the dynamic branch already places the origin at the top margin | **1** | `alloc-dyn-height-margin` |

Notes that matter for interpretation:

1. **`:468` mutant** still passes `alloc-zero-refused`: the mutated guard also fires for an
   allocation of 0 (it raises the same `Unmodelled`, rc 3, stage=model), so that case does
   **not** separate this mutant — the four dynamic-band success cases do.
2. **`:460` mutant** fails 35 cases, but only `alloc-explicit-ignored` separates the axis
   *within the new class*: in `alloc-dyn-height-top`, `alloc-dyn-height-margin`,
   `alloc-dyn-width-dock` and `alloc-composition-dyn-bar` both declared axes are 0, so
   either lookup finds 0 and falls through to the allocation. The other 34 failures are the
   carried static-band cases (`host-top` first).
3. **`:448` mutant is a real gap.** No case carries a boolean allocation; the eight new
   cases exercise negative (setup), zero (model) and unknown-namespace (setup) refusals but
   not the type rejection. The mutant is not behaviourally equivalent to the frozen tool:
   with the `alloc-dyn-height-top` fixture and `{"waybar": true}` (ad-hoc, outside the 47):

   ```
   frozen                       rc=2 | MADO_BARFOOT: ERROR (stage=setup the allocation for 'waybar' is not an integer)
   mutant-alloc-bool-accepted   rc=1 | MADO_BARFOOT_RESULT: monitor=M1 box=DIFFER reserved=GT band=34 expected=1 verdict=DIFFER
   ```

   (`bool-probe.txt`.) The same line's non-bool non-integer rejection is also unexercised by
   the case set; only the counter's private `--selftest` covers it. The minimal closing case
   would be a 48th `alloc-bool-refused`: config `height = 0` top, `allocation {"waybar":
   true}`, expecting rc 2 stage=setup. Frozen controls were not edited — the L1 decides
   whether to add it.
4. Each mutant is distinct from the counter's list: `alloc-zero-accepted` relaxes the guard
   to `< 0` (mine retargets the guard at the declaration), `alloc-explicit-overridden` drops
   the declaration with `if False` (mine prefers the allocation), `alloc-axis-lost` replaces
   the axis lookup with the raw `bar["height"]` (mine swaps the lookup axis),
   `alloc-composition-ignored` makes the composition assignment a self-assignment (mine
   passes an empty map), and `alloc-margin-double-counted`/`alloc-bool-accepted` have no
   counterpart (the counter's `zone-margin-not-added` is the auto-zone path).

## Observed results

- The frozen tool scores 47/47 under an independently written driver and under the frozen
  counter; the frozen command reproduces the receipt byte-for-byte, including
  `base_correct=39/47`, `tools_selftest=133/133`, 34/34 mutants killed.
- The new allocation code has one unexercised branch: the boolean exclusion in
  `parse_allocation` (`tools/mado-barfoot.py:448`). No frozen-instrument defect was found.
- No tools were installed or upgraded (pacman paused; nothing needed).

Evidence: `frozen-counter-output.txt`, `out-base.txt`, `out-mutant-*.txt`, `mutants/`,
`bool-probe.txt`, `runner.py`, `gen_mutants.py`, `SHA256SUMS.txt` in
`/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-82/w1/R82ExecMutants/`.

STATUS: ok
