# R86ReviewerC1 — C1 attack report (round mado 86, wave 1)

Seat: R86ReviewerC1 (leaf; no subagents). Freeze: `237ecf4e69a4986108f719f3beeafe111adaa033`.
Instrument: `quality/counters/c1-r86-refusal-records.py` (frozen blob sha256 `d651c6aab255826301954782beba0e5b145a9fc37ae24e0b2571393383ce4df4`).
Control sets (worktree == freeze, verified three-way): `c1-cases-r86.json` `f6dd9cdef7da…`, `c1-cases-r85.json` `bacae37d29d0…`; `tools/mado-barfoot.py` `62626fce852b…`.
All forgeries were scored by the counter's own functions, imported unmodified (`importlib`, `python3 -I`) from the frozen blob, over the frozen 75-case set: `run_cases(tool, cases, workroot, label, rule=expected_ok)`. The battery was run twice — once against the worktree counter and once against the frozen blob — with byte-identical results (docstring-only difference; see F3-findings below).

## Verdict summary

The frozen rule survives the canonical attacks (plain duplicate, wrong cause, compound cause, embedded token, partial stage flood) but **four forgeries score 75/75 under the r86 rule**, three of which also score 75/75 under the held r85 rule — so for them the claimed increment (held full marks, r86 refuses) does not exist. Per the frozen kill rule, a forgery the counter scores full marks is a hole in the claim, not a footnote.

## Frozen-instrument rerun (task 3)

Command (absolute paths; scratch root inside my seat scratch):

```sh
git -C /home/vgpnk/Projects/shokunin/mado-shokunin show \
  237ecf4e69a4986108f719f3beeafe111adaa033:quality/counters/c1-r86-refusal-records.py \
  > /fast/scratch/hyaku/mado-r86/R86ReviewerC1/c1-frozen-counter.py
python3 -I /fast/scratch/hyaku/mado-r86/R86ReviewerC1/c1-frozen-counter.py \
  --repo /home/vgpnk/Projects/shokunin/mado-shokunin \
  --rev 237ecf4e69a4986108f719f3beeafe111adaa033 \
  --base-rev 2b6dd76b65de4dfe701db87db13b7e448b3538ee \
  --controls /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-86/controls/c1-cases-r86.json \
  --carried /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-85/controls/c1-cases-r85.json \
  --scratch-root /fast/scratch/hyaku/mado-r86/R86ReviewerC1/c1-frozen
```

Observed (stdout, frozen bytes, rc 0):

```
MADO_R86_REFUSALS: cases=75 correct=75 mutants=51 killed=51 base_correct=75/75 carried=72/72 tool_selftest=152/152 flooding=48/75 held_flooding=75/75 verdict=TARGET_MET rev=237ecf4e69a4986108f719f3beeafe111adaa033 tool_sha256=62626fce852bc5bef263a26ddee78b12c6fc9b2883e41ef55c015becf3a76fb5
MADO_R86_CONTROL: sha256=f6dd9cdef7daa2e6b51c95f27cf8ebe8509188c551ff18ed42a176a08d8620bf carried=72/72 flooding=48/75 held_rule_flooding=75/75 flooding_sha256=3c5ec8b280e1c9d2e947afbc8a0991fe1174343c2026f26612dd10f71c4f3948
MADO_R86_BASE: correct=75/75 rule=held-r85-tool base_rev=2b6dd76b65de4dfe701db87db13b7e448b3538ee base_sha256=62626fce852bc5bef263a26ddee78b12c6fc9b2883e41ef55c015becf3a76fb5
```

51 `MADO_R86_MUTANT` lines, zero `killed=no`; selftest `MADO_R86_REFUSALS_SELFTEST: 152/152`. The parallel run from the drifted worktree bytes printed the identical verdict line (rc 0 both) — consistent with the docstring-only drift. The controls match the declaration: flooding forgery 48/75 under the r86 rule and 75/75 under the held rule, held tool 75/75 under the r86 rule (`base_correct`), carried 72/72.

## Findings, by severity

### S1 — forgeries the r86 rule scores full marks (claim holes)

**S1-a · F4 stderr-flood — SURVIVED 75/75 (r86) AND 75/75 (held r85).**
Construction (one-line anchor mutations of the frozen tool, both stages; `FLOOD` = the ten `CAUSE_VOCAB` tokens joined by single spaces; anchor occurs exactly once per stage, verified):

```python
old = '        print("MADO_BARFOOT: ERROR (stage=model%s %s)" % (cause_tag(exc), exc))'
new = old + '\n        print("MADO_BARFOOT: FLOOD: ' + FLOOD + '", file=sys.stderr)'
# same for stage=setup
```

Observed: `FORGERY F4 stderr-flood rule=expected_ok score= 75/ 75 SURVIVED` and `rule=held_ok score= 75/ 75 SURVIVED`.
Cause: `expected_ok`/`held_ok` receive only `stdout` (`rc, stdout, stderr = run(argv, outdir)` → `rule(case, rc, stdout)`); the counter captures stderr and never inspects it. The refusal records stay on stdout and parse perfectly, so every clause of the frozen predicate holds while the tool floods all ten tokens on stderr. This breaks the claim's letter — "a tool that prints every cause token among the honest answer is refused" — because this tool prints every cause token and is **not** refused; and it breaks the increment claim, since the held rule gives it full marks too. The flood/refusal distinction the counter sells is stream-accidental, not semantic.

**S1-b · F5 space-shifted duplicate record — SURVIVED 75/75 (r86).**
Construction (both stages):

```python
old = '        print("MADO_BARFOOT: ERROR (stage=setup%s %s)" % (cause_tag(exc), exc))'
new = old + '\n        print(" MADO_BARFOOT: ERROR (stage=setup%s %s)" % (cause_tag(exc), exc))'
# note the leading space inside the second string literal
```

Observed: `FORGERY F5 space-shifted-duplicate rule=expected_ok score= 75/ 75 SURVIVED`. Module-level probes agree: a second record with one leading space (or tab, or appended after the first record on the same line) is invisible to `parse_refusal_records` (`^`-anchored, `re.M`), so `len(records) != 1` passes, and the duplicate's cause token is subtracted by the `foreign` set difference. The declaration freezes "must occur **exactly once**"; this tool prints the record **twice** and is scored honest. The plain duplicate (both copies at column 0) is caught (48/75), so the exactly-once clause is enforced only against column-0 duplicates — whitespace defeats it.

### S2 — scope gaps (forgeries outside what the negative observation watches)

**S2-a · F6 result-path flood — SURVIVED 75/75 (r86) AND 75/75 (held r85).**

```python
old = 'def emit(rows, verdict):\n    for kind, text in rows:'
new = 'def emit(rows, verdict):\n    print("MADO_BARFOOT: FLOOD: ' + FLOOD + '")\n    for kind, text in rows:'
```

Observed: `FORGERY F6 result-path-flood rule=expected_ok score= 75/ 75 SURVIVED` (held rule identical). On refusal paths `emit` never runs, so refusal stdout stays clean; the 48 result cases are judged solely by `parse_result` field equality — no vocabulary check exists on result-case stdout at all. A tool that prints all ten tokens on every success line is a flood by any reading and scores full marks under both rules.

**S2-b · F7 unicode look-alike flood on refusal stdout — SURVIVED 75/75 (r86).**

```python
mangled = FLOOD.replace("a", "а")   # every ASCII 'a' -> Cyrillic а U+0430, all ten tokens mangled
old = '        print("MADO_BARFOOT: ERROR (stage=model%s %s)" % (cause_tag(exc), exc))'
new = old + '\n        print("MADO_BARFOOT: FLOOD: ' + mangled + '")'
# same for stage=setup
```

Observed: `FORGERY F7 unicode-lookalike-flood rule=expected_ok score= 75/ 75 SURVIVED`. The negative observation is `token in stdout` — an ASCII substring test — so a flood line printed immediately before the record on the same stream evades it whenever one letter per token is a homoglyph. Visually the stdout is indistinguishable from the declared flooding forgery. (A look-alike in the record's own cause field is still caught — cause equality is exact — so this is an evasion of the flood detector, not of the record match.)

### S3 — instrument and declaration hygiene (defects, no fix applied)

- **Frozen counter docstring contradicts its own population.** The frozen blob's contract line reads `mutants=53 killed=53` (line 15) while `MUTANTS = 51`, `len(MUTATIONS) == 51` (selftest-enforced) and the declaration say 51. The docstring can never match the printed line.
- **The frozen instrument drifted in the working tree mid-wave, by another seat.** At wave start `git status --short` showed the counter clean; minutes later the worktree copy differed from the freeze blob (worktree `4ff50ac2e8d5…` vs freeze/HEAD `d651c6aab255…`), `git status` now reports `M quality/counters/c1-r86-refusal-records.py`, mtime `2026-11-05 00:15:58`. The entire diff is the docstring line `mutants=53 killed=53` → `mutants=51 killed=51`. Semantics are unchanged (my battery reproduces byte-identical scores under both copies), but an uncommitted edit to a declared-frozen instrument during scoring violates the declaration's own freeze rule ("nothing in this file is edited after a seat has scored"). My first full run unknowingly used the drifted bytes; the quoted rerun above is from the exact freeze blob.
- **Declaration ↔ instrument output-shape mismatches.** The declaration's quoted line omits the `base_correct=<b>/75` field the counter always prints, and quotes `tool_selftest=152/152` as a fixed literal while the counter's rc clause accepts any `p == n > 0`. The executable contract is the counter's; the declaration's quoted shape is not what the instrument prints.
- **A spurious cause on a cause-free refusal case is accepted** (`expected_ok({"expect": {"error": True, "rc": 2, "stage": "setup"}}, 2, "MADO_BARFOOT: ERROR (stage=setup cause=alloc-unknown-namespace x)\n")` → True). This follows the frozen predicate ("its cause must equal the expected cause **where the case binds one**"), so it is a scope note, not a defect: the record's own cause token is always self-exempted from the foreign check.

### Verified strong (attacks the rule survived — for the record)

| Attack | Score under r86 `expected_ok` | Result |
|---|---|---|
| F1 duplicate record, both copies at column 0 (both stages) | 48/75 (all 27 refusal cases fail) | CAUGHT |
| F2 right stage, cause = another of the ten (`alloc-negative` raise → `alloc-unknown-namespace`) | 0/1 on `alloc-negative-cause` | CAUGHT |
| F3a compound cause, want is strict prefix (`alloc-negative-extra`) | 0/1 on `alloc-negative-cause` | CAUGHT |
| F3b correct cause in record, foreign token `alloc-non-integer` inside the free-text message | 0/1 on `alloc-negative-cause` | CAUGHT |
| F8 flood on setup-stage refusals only, model records honest | 57/75 (18 setup refusal cases fail) | CAUGHT |
| Probes: leading-space record refused; record without trailing space refused; wrong stage refused; CRLF accepted | — | as predicted |

## Task 2 — ten-token vocabulary completeness: VERIFIED COMPLETE

AST walk over the frozen tool (all `Call` nodes with func name `Setup`/`Unmodelled`): the cause literals at raise sites are exactly

`alloc-duplicate-key, alloc-not-object, alloc-empty-namespace, alloc-non-integer, alloc-negative, alloc-unknown-namespace, namespace-duplicate-bar, namespace-duplicate-surface, namespace-duplicate-cross-level, live-duplicate-surface`

— zero non-literal cause arguments, `vocab − raised = ∅`, `raised − vocab = ∅`. `cause=%s` is emitted from exactly one site (`cause_tag`), and the three selftest-fixture strings (`edge-outside-anchor`, `margin-top`, `margin-bottom`) are never raised. The case set binds exactly these ten causes (14 refusal cases bind none). Earlier grep hits for the fixture strings were verified to be selftest/fixture literals, not raise sites.

## Residual risk and verification gaps

- The four S1/S2 survivors are construction-level proofs against the frozen functions; I did not run the counter end-to-end against a forged tool (impossible without mutating the repo or the frozen instrument — both forbidden), so the survivors are established at the `expected_ok`/`run_cases` layer, which is the layer the counter's own flooding control exercises.
- I scored forgeries only against C1's rule; C2 and the carried r85 instrument were not touched (not my claim).
- The frozen full-run line quoted above is the authoritative rerun; the parallel worktree-byte run exited rc 0 with the byte-identical verdict line, so the drift had no effect on any printed number.
- CPU contention from sibling seats' concurrent counter runs makes exact wall-times unreproducible; scores are deterministic.
