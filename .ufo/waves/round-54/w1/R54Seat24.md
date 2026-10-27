# R54Seat24 — C1 counter mutation probe

**Axis:** operability, specifically whether the frozen C1 verifier contract can be falsified by a distinct input defect. **Verdict: INCONCLUSIVE (target unavailable).**

## Target and attacked predicate

Assigned item 24 asks for mutation-testing the proposed counter, focusing on malformed quotes, anchors, pin hashes, and an absent proposition. The governing predicate is `PRED-C1-r54` in `claims-frozen.md`: read `--repo`/`--rev` Git-object inputs, verify the four P19–P22 propositions' exact quote/pin/anchor claims and all six controls, and emit the frozen success line only on complete success. Registration §“C1 frozen controls” defines the six required red cases, including spliced quote, shifted anchor, hash tamper, wrong range, dropped proposition, and swapped pin.

The C1 implementation itself is not present at the inspected lane path, so there is no behavior-bearing candidate to mutate and no pristine/mutant/restored detector run can be honestly reported. The frozen baseline receipt independently records zero r54 counters and predicate absence at base (`receipts/before.txt`, lines 1–3); this is not a detector pass and cannot establish mutant kill.

## Reproducible availability check

Command:

```sh
for f in /home/vgpnk/Projects/shokunin/mado-shokunin/quality/counters/c1-r54-errata-truth.py /home/vgpnk/Projects/shokunin/mado-shokunin/quality/counters/c2-r54-uwsm-entry.py; do if test -e "$f"; then printf 'PRESENT %s\\n' "$f"; else printf 'ABSENT %s\\n' "$f"; fi; done
```

Actual output:

```text
ABSENT /home/vgpnk/Projects/shokunin/mado-shokunin/quality/counters/c1-r54-errata-truth.py
ABSENT /home/vgpnk/Projects/shokunin/mado-shokunin/quality/counters/c2-r54-uwsm-entry.py
```

## Mutation evidence

- Mutant: none. The assigned C1 candidate file is absent; inventing a substitute would test my implementation, not the proposed counter.
- Expected detector: the C1 counter's own bounded `--selftest`/`--repo` control detector per registration, covering the six named mutated trees. It could not be run because the implementation and detector are absent.
- Malformed quote / shifted or invalid anchor / altered pin hash / missing proposition: not executed; these inputs are already specified by registration controls C1-CTL-1 through C1-CTL-5, but without a runnable candidate these are not mutation outcomes.
- Output and verdict: no behavioral detector output; **inconclusive**, not killed or survived. The availability check is the only executed command.
- Before/after hashes and restoration: not applicable; no bytes were copied or changed. Scratch `/fast/scratch/hyaku/mado-r54/R54Seat24` did not exist when checked, and no scratch was created.
- Tool updates: none.

**Prerequisite to complete this probe:** the proposed C1 counter and its bounded detector must be available as a fixed candidate in an isolated scratch copy. Once supplied, run identical detector inputs on pristine, mutated, and restored bytes, recording hashes and actual outputs; do not infer a kill from the frozen baseline's absence receipt.
