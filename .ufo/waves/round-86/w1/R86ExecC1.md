# R86ExecC1 — independent re-execution of claim C1 (refusal records)

Seat: R86ExecC1 (executor, leaf). Wave: round-86 w1. Instrument: `quality/counters/c1-r86-refusal-records.py`
(read and run only — not edited). Freeze revision: `237ecf4e69a4986108f719f3beeafe111adaa033`.
Base revision: `2b6dd76b65de4dfe701db87db13b7e448b3538ee`.

## Instrument-bytes note (disclosed, measured)

The frozen counter file at `237ecf4e` is **not** the current working-tree file: the lane has since
applied the disclosed repair in `.ufo/waves/round-86/receipts/instrument-repair-r86.md` ("C1 — one
documentation repair, no predicate change"). I extracted both byte strings and compared them:

- `git show 237ecf4e:quality/counters/c1-r86-refusal-records.py` vs working tree → **exactly one
  line differs**, the module docstring contract line: frozen bytes read `mutants=53 killed=53`,
  working tree reads `mutants=51 killed=51`.
- AST comparison with the module docstring stripped → **identical**. `MUTANTS = 51`,
  `len(MUTATIONS) == 51`, and the declaration's target sentence (`killed == 51`) all agree with the
  repaired prose; the frozen docstring was stale bookkeeping (the repair receipt's own account).
- Both my runs executed the working-tree (repaired) bytes via the exact frozen CLI. The executable
  predicate — cases, mutants, flooding construction, carried check, kill rule — is byte-identical
  to the freeze. This is a prose-only delta, already disclosed by L1 in the repair receipt; I am
  reporting it, not fixing it.

## Execution

Run twice into `/fast/scratch/hyaku/mado-r86/R86ExecC1/c1` (transcripts kept as `run1.txt`,
`run2.txt`; each 129 lines, stderr empty). Command, verbatim:

```sh
cd /home/vgpnk/Projects/shokunin/mado-shokunin && python3 -I quality/counters/c1-r86-refusal-records.py \
  --repo . --rev 237ecf4e69a4986108f719f3beeafe111adaa033 \
  --base-rev 2b6dd76b65de4dfe701db87db13b7e448b3538ee \
  --controls .ufo/waves/round-86/controls/c1-cases-r86.json \
  --carried .ufo/waves/round-85/controls/c1-cases-r85.json \
  --scratch-root /fast/scratch/hyaku/mado-r86/R86ExecC1/c1
```

- Run 1: rc **0**, wall ~414 s.
- Run 2: rc **0**, wall ~332 s.
- `diff run1.txt run2.txt` → **identical** (deterministic).
- Transcript tallies: 75 `MADO_R86_CASE` lines, all `correct=yes`; 51 `MADO_R86_MUTANT` lines, all
  `killed=yes`; no `correct=no` or `killed=no` anywhere.

## MADO_R86_REFUSALS line (verbatim, both runs)

```
MADO_R86_REFUSALS: cases=75 correct=75 mutants=51 killed=51 base_correct=75/75 carried=72/72 tool_selftest=152/152 flooding=48/75 held_flooding=75/75 verdict=TARGET_MET rev=237ecf4e69a4986108f719f3beeafe111adaa033 tool_sha256=62626fce852bc5bef263a26ddee78b12c6fc9b2883e41ef55c015becf3a76fb5
```

## Flooding control (bytes-only verification)

- `MADO_R86_CONTROL` line: `sha256=f6dd9cdef7daa2e6b51c95f27cf8ebe8509188c551ff18ed42a176a08d8620bf
  carried=72/72 flooding=48/75 held_rule_flooding=75/75
  flooding_sha256=3c5ec8b280e1c9d2e947afbc8a0991fe1174343c2026f26612dd10f71c4f3948`
- flooding / held_flooding pair: **48/75 vs 75/75** — the record rule refuses the flood on the 27
  refusal cases; the held substring rule still gives it full marks. Matches the declaration's
  control-1 numbers (48/75 and 75/75) exactly.
- Determinism from bytes only: I re-derived the flooding source independently —
  `git show 237ecf4e:tools/mado-barfoot.py`, then applied the counter's own two-stage mutation
  (`stage=model`, then `stage=setup`; each anchor occurs exactly once; replacement prints
  `MADO_BARFOOT: FLOOD: ` + the ten `CAUSE_VOCAB` tokens joined by spaces before the unchanged
  refusal print). Resulting sha256:
  **`3c5ec8b280e1c9d2e947afbc8a0991fe1174343c2026f26612dd10f71c4f3948`** — identical to the
  counter's `flooding_sha256`. No randomness, timestamps or environment enters the construction.
- Held tool: `MADO_R86_BASE: correct=75/75 ... base_rev=2b6dd76b... base_sha256=62626fce...` —
  the r85 tool scores full marks under the r86 rule (increment is the rule, not the tool).
  `git show` of `tools/mado-barfoot.py` at freeze and base revs both hash to
  `62626fce852bc5bef263a26ddee78b12c6fc9b2883e41ef55c015becf3a76fb5`, and HEAD's copy is the same
  bytes.

## Carried set (counted with jq)

- `.ufo/waves/round-85/controls/c1-cases-r85.json` → `jq '.cases | length'` = **72**
- `.ufo/waves/round-86/controls/c1-cases-r86.json` → `jq '.cases | length'` = **75**
- `jq '.cases[0:72] == input'` against the r85 file → **true** (parsed-equal).
- Canonical-JSON sha256 of `cases[:72]` vs the whole r85 `cases` array → both
  `cd92b7edf1e5fdf10e5376ed038510502fb6dbb84fbff58f085cd3fb142afd16`.
- `cases[72:]` names: `alloc-negative-cause`, `alloc-bool-cause`, `alloc-float-band` — exactly the
  three witnesses the declaration names.

## Counter-vs-declaration consistency

Every printed number matches the frozen target sentence: `correct=75`, `killed=51`, `carried=72/72`,
`tool_selftest=152/152` (instrument selftest separately run: `MADO_R86_REFUSALS_SELFTEST: 127/127`,
rc 0 — the selftest's internal check count is the instrument's own, distinct from the tool's),
`flooding=48/75 < 75`, `held_flooding=75/75`, `verdict=TARGET_MET`, rc 0. **No inconsistency found**
between the printed counters and the declaration's target sentence at the executed (repaired)
instrument bytes; the only delta from the literal freeze bytes is the disclosed docstring fix.

## Findings / risks

1. **Instrument bytes ≠ freeze bytes (prose only).** The working-tree counter differs from
   `237ecf4e` in one docstring line. Executable behavior is identical (AST-minus-docstring equal).
   Disclosed in `receipts/instrument-repair-r86.md`; reproduced here for the record.
2. The r86 control file's `carried` field is `61` (round-85 carried count) while `cases` length is
   75 — metadata only; the counter enforces the real check (`cases[:72] == carried cases`), which
   passes. Not a defect.
3. `flooding=48/75` is not "the flood refused everywhere" — it is the 27 refusal-binding cases
   refused plus the 48 non-refusal cases passing, exactly as the declaration's control-1 describes.

No instrument was edited; no git mutation was run; scratch retained at
`/fast/scratch/hyaku/mado-r86/R86ExecC1/c1/` (`run1.txt`, `run2.txt`, `c1-frozen-bytes.py` for
reproduction; transient per-case dirs removed by the counter itself).
