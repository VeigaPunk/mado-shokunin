# R76Mutant — frozen-set mutation probe

Axes: frozen-set discrimination; exact byte restoration; isolated execution.
Revision: `cb713254ee9926e036e594312fdc61b57825526b` (freeze v2).

## Detector and results

Used committed bytes obtained with read-only `git show`. The same bounded behavioral detector ran on pristine, mutated and restored bytes for each probe. C1 uses the frozen counter's real fixture builder, harness runner and two-field `(mz, verdict)` parser across all 16 frozen cases. C2 invokes the committed classifier on all 59 frozen sources, comparing both reader and guard labels. Both control-file hashes were checked against their committed counter constants. Kill rule: a score below 16/16 or 59/59 respectively, provided pristine and restored controls both attain the target. This probe does not claim to rerun the full population census or the four named outcome mutations.

| Own mutation | Pristine | Mutated | Restored | Verdict | Separating frozen cases |
|---|---:|---:|---:|---|---|
| `constant`: `outcome_green` returns `True` | 16/16 | 2/16 | 16/16 | killed | all except `right`, `liar-success` |
| `grammar16`: witness regex `{16,}` → `{16}` | 16/16 | 16/16 | 16/16 | survived | none |
| `forward`: `last_witness` iterates `out.splitlines()` without reversing | 16/16 | 15/16 | 16/16 | killed | `last-wins-wrong` |
| `d3-anyarg`: cancellation records every positional `ast.Name` argument, not just argument zero, without consulting the deleted parameter | 59/59 | 59/59 | 59/59 | survived | none |
| `d4-twobind`: `keyed_names` accepts binding counts `<= 2`, not `== 1` | 59/59 | 58/59 | 59/59 | killed | `dynamic-key-rebound` |

Constant-return separators, explicitly: `always-red`, `absent-witness`, `overlong-witness`, `last-wins-wrong`, `uppercase-echo`, `stale-witness`, `wrong-witness`, `green-mutant`, `green-absent`, `green-overlong`, `green-uppercase`, `crash`, `zero-denominator`, `mismatch-detail`.

### Named coverage gaps

- **G1 grammar regression unobserved by two-field labels.** Rejecting an overlong witness as absent rather than parsing it as mismatch still produces the expected `mz=fail` and `verdict=TARGET_MISSED`. The frozen score does not inspect `witness=`. Survival is a detector-coverage finding, not evidence that the narrowed grammar satisfies G1. The harness's own direct selftest is a different detector and was not substituted here.
- **D3 positional overreach unobserved.** Broadening cancellation to every positional argument still scores 59/59. The frozen set has no separator for this broadening; no parameter-sensitive case is established by this result. This does not change the declared simple-first-argument limit or certify all interprocedural calls.

## Actual output and receipts

Command (cwd was the private scratch directory):

```sh
python3 -I /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-76/w1/R76Mutant/probe.py
```

Exit status: 0. Output:

```text
constant killed 2 / 16 ['always-red', 'absent-witness', 'overlong-witness', 'last-wins-wrong', 'uppercase-echo', 'stale-witness', 'wrong-witness', 'green-mutant', 'green-absent', 'green-overlong', 'green-uppercase', 'crash', 'zero-denominator', 'mismatch-detail']
grammar16 survived 16 / 16 []
forward killed 15 / 16 ['last-wins-wrong']
d3-anyarg survived 59 / 59 []
d4-twobind killed 58 / 59 ['dynamic-key-rebound']
```

Preserved driver: `.ufo/waves/round-76/w1/R76Mutant/probe.py` (expects the separately prepared scratch copies described above).
Full per-case expected/actual results, C1 subprocess exit codes/stdout/stderr, and restoration hashes: `.ufo/waves/round-76/w1/R76Mutant/results.json`.
The driver invokes the original counter helpers rather than introducing alternate expected labels. Each fixture's builder asserts its git toplevel equals its private fixture directory before any add/commit. No production or sibling file was edited; no fleet git mutation occurred.

## Restoration evidence

Original and restored SHA-256 are identical for each target:

- C1 harness, all three probes: `b6003941fc37bb111a3dc5e26b6c7c060b9cb85c87b2f152bc14476713003ed0`.
- C2 counter, both probes: `2638d44f8da59fc847a9e17aa894c63b45b11bee4d1536f7ab0b894b02987ef8`.

Mutated SHA-256:

| Mutation | SHA-256 |
|---|---|
| constant | `fe2484d922eed27c6bb6f9102a2dfc2638b412d25a9cde3d5fa99fe3f18b6063` |
| grammar16 | `e4253f38e87d4a8a6a20360cab632a29b37cb0ffcbd19f5bef9bdda1139111a2` |
| forward | `c1e198a5cde7ad4527a31359e03f68b3a83b7f23f93c10da35b4d135ad69e275` |
| d3-anyarg | `3a18696aa45e6e64ad9a91fd1883284c4c5216872aa08c816342e6a56a7a38ac` |
| d4-twobind | `7a22409062dd9c468d1a361ca674ba375d5f598c6323000dd9c2debc717646b4` |

Exact source bytes were restored before each restored behavioral run. Scratch was removed after preserving receipts. No installs or upgrades were needed.

## Self-evaluation

Accuracy 4/5: raw per-case output and hashes support the scores; no full-census inference is made. Completeness 4/5: all five assigned probes have three-leg evidence, but the driver requires preparing its scratch payloads to reproduce. Clarity 4/5: named survivors distinguish field coverage from rule correctness. Actionability 4/5: two gaps identify the missing observations/call shapes, without changing the frozen contract. Conciseness 4/5: complete hashes and separator lists make this longer than the result table. Overall 4.0/5. Highest-impact improvement would be a separately commissioned parameter-sensitive separator and explicit witness-state scoring; neither was added to the frozen set. User-agreement self-check: this reports both survivors rather than hiding them.
