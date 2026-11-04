# R72CriticClaims — frozen-claim falsification review

Axes: **C1 calibration** (M-Z kill credit requires matching run failure detail); **C2 operability** (outcome follows the gate summary, not its exit status).

Scope: read-only review of frozen declaration, controls, baselines, receipts and committed instruments. No production changes, fixture builds, harness measurement reruns, git mutations, installations, or judge/admission decisions. The probes execute AST-selected pure functions from committed bytes, not the instrument modules or their entry points. All four commands exited 0. Evidence files below are siblings of this report.

## Q1 — Verdict: neither constant/no-verdict control reaches either target

Command run:

```sh
python3 -I /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-72/w1/R72CriticClaims/audit.py q1
```

Evidence: `q1.txt`; actual frozen JSON labels scored through each committed counter's own `score()`:

| Control | C1 correct | C2 correct |
|---|---:|---:|
| Always negative (`mz=fail` / `TARGET_MISSED`) | 5/8 | 6/8 |
| Always positive (`mz=pass` / `TARGET_MET`) | 3/8 | 2/8 |
| Missing compared answer (`None`) | 0/8 | 0/8 |

Both targets require 8/8 in addition to the held baseline condition. C1's three credit-positive modes and C2's two green cases reject the always-negative controls. The always-negative C2 control exceeds the held 4/8 but **does not** meet the frozen target. No constant-control correction needed.

## Q2 — Verdict: scoring is not circular in measurement, but a wrong successor still scores 8/8; shared last-summary interpretation violates a literal frozen predicate

Command run:

```sh
python3 -I /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-72/w1/R72CriticClaims/audit.py q2
```

Evidence: `q2.txt`; implementation pointers at the measured revision:

- `quality/counters/c1-r72-summary-credit.py:188-189` and `quality/counters/c2-r72-outcome.py:142-143`: neither `score()` accepts a missing compared answer. C1 compares an M-Z token, not the enclosing harness's overall contract verdict; its `parse_mz` at 177-185 does not validate a full contract line.
- C1's embedded `EXPECT` equals the frozen C1 JSON exactly today. It is nevertheless a second authority: measurement uses the Python constants, not that JSON.
- C2's `expected_from_summary` at 101-105 reimplements the predicate, but `measure` at 222-226 compares against `case["expected"]`, not that helper. The helper validates labels in selftest only (259-261). Therefore the measured 8/8 is not automatically manufactured by calling the reference helper as its oracle.
- C2's base leg really invokes `held.outcome_verdict(case["gate_rc"], case["killed"])` (224), not a counter-local approximation. AST-selected execution of that exact committed function returns **4/8**; the candidate's own function returns **8/8**.

### Counterexample A: an incorrect C2 successor remains observationally perfect on the frozen set

The probe's deliberately wrong successor uses the **first** regex match, compares numerator and denominator, and omits `n > 0`. It scores **8/8**, yet returns `TARGET_MET` for `MADO_LANDING_COUNTERS_SELFTEST: 0/0 assertions passed` with killed=2, where the frozen predicate requires `TARGET_MISSED`. The eight C2 cases contain neither zero denominators nor multiple summaries. This is an observed finite-set blind spot, **not** proof the actual successor has the zero-denominator defect: it correctly checks `total > 0`.

Impacted axis: C2; premature saturation beyond the eight cases. Smallest safe correction: keep the finite 8/8 claim explicitly finite; any future coverage extension should add zero-denominator and last-summary controls in a newly frozen denominator, not silently revise this one.

### Counterexample B: last *parsed* versus last *prefix-matching* summary

Frozen text for both claims says the **last parsed** summary. Actual `last_summary` in the successor (`quality/counters/c1-r72-landing-controls.py:298-302`) selects the last line beginning with the summary prefix **before** checking whether it parses. Thus:

```text
SELFTEST FAIL 1: x
MADO_LANDING_COUNTERS_SELFTEST: 1/2 assertions passed
MADO_LANDING_COUNTERS_SELFTEST: garbled
```

C1 actual `credit` is **False**; applying the literal last-successfully-parsed-summary predicate gives **True** (one detail line, one failed assertion).

```text
MADO_LANDING_COUNTERS_SELFTEST: 2/2 assertions passed
MADO_LANDING_COUNTERS_SELFTEST: garbled
```

C2 actual outcome at killed=2 is **TARGET_MISSED**; the literal last-successfully-parsed-summary predicate gives **TARGET_MET**. These are pure-function results, not whole-harness runs. Neither frozen control set contains this mixed valid/garbled sequence. C2's reference helper repeats the prefix-first interpretation, so its selftest oracle would not expose this disagreement.

Impacted axes: C1 and C2. This is a **fixable predicate/implementation mismatch if “parsed” means successfully parsed**. The C2 declaration also says a garbled summary earns no green, making mixed valid/garbled streams textually ambiguous; conservative fail-closed behavior may instead be an intentional tradeoff. Smallest safe correction: explicitly resolve that ambiguity against the frozen claim before crediting broader last-parsed semantics. If literal parsed semantics govern, scan backward for a full grammar match; if last-prefix fail-closed semantics govern, record the narrower supported behavior without rewriting the frozen declaration. Do not treat this review as a judge decision.

## Q3 — Verdict: declaration, baseline receipts, and measured numbers agree at the stated instrument revision

Commands run:

```sh
python3 -I /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-72/w1/R72CriticClaims/audit.py q3
git -C /home/vgpnk/Projects/shokunin/mado-shokunin ls-tree -r 9bcb4fd5b598844f168230dc05e441721d95b272 -- quality/counters/c1-r72-summary-credit.py quality/counters/c2-r72-outcome.py quality/counters/c1-r72-landing-controls.py .ufo/waves/round-72/controls/c1-modes-r72.json .ufo/waves/round-72/controls/c2-controls-r72.json .ufo/waves/round-72/claims-declaration-r72.md
```

Evidence: `q3.txt`; read-only `git ls-tree` returned all six paths, including both counters and successor harness.

- Candidate: `9bcb4fd5b598844f168230dc05e441721d95b272`; base: `976684a27e99c2508037a60eec415f550f53d70e`.
- C1 receipt: `cases=8 correct=8 base_correct=6 verdict=TARGET_MET`, `C1_RC=0`. Pre-freeze baseline contains exactly six correct held cases out of eight.
- C2 receipt: `cases=8 correct=8 base_correct=4 verdict=TARGET_MET`, `C2_RC=0`. Pre-freeze baseline contains exactly four correct held cases out of eight.
- Committed candidate harness SHA-256 is `d0d3bfd2b8306062e7ea7323377dea1371df93c4a9447a7a28c4927becfe7c62`; committed base harness is `f836499594fb4fa8898336b1a47241614bb2b9ddb6f93c369a9e00ece0f185f1`, matching both measurement receipts.
- Both committed control hashes match the declaration. Thus the measured revision **does contain** the instruments. This checks provenance and receipt arithmetic, not a fresh C1 whole-harness measurement.

No revision-identity correction indicated.

## Q4 — Verdict: disjoint scored observations/control sets, but not the literal function-only isolation declared

Command run:

```sh
python3 -I /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-72/w1/R72CriticClaims/audit.py q4
```

Evidence: `q4.txt` and source pointers:

- C1 `measure` (273-329) extracts the **entire** successor/base harnesses, builds a git fixture, runs each full harness through `run_harness` (262-269), and parses `mz`. It does **not** import/score only `credit`, contrary to the declaration's introductory separability sentence. It also extracts three real child instruments and exercises M-R machinery. Its return-code tuple elements are discarded at 315/317, so an ordinary C2 outcome change need not alter the scored M-Z observation; that is weaker than isolated execution.
- The whole successor `measure` calls `summary_green` at 476-478, before M-Z, and calls the C2-dependent contract formatter before returning at 575-578. A C2 helper exception can therefore prevent C1 from producing its scored marker. This cross-axis failure path is a **source-derived inference**, not an executed fixture mutation.
- C2 imports the **whole** two modules (`load_module`, 133-139), then calls only their outcome functions for scored observations (223-224). C1 credit is not called by C2 measurement.
- Neither counter consumes the other's control set. C2 reads its own JSON; C1 reads neither JSON and relies on duplicated constants that currently match its own JSON. No numerical contamination was observed.

Impacted axes: C1/C2 causal attribution and claim provenance. Smallest safe correction: qualify the current evidence as **disjoint output scoring with shared harness execution/import**, not function-only verification; retain frozen receipts unchanged. If strict isolation is required for an admission criterion, a future instrument should extract/load the selected predicate and dependency closure and bind C1 labels to one frozen authority, then obtain a new frozen measurement. This review does not implement or admit that change.

## Handoff

No production edits or tool installs. Scratch was created explicitly and removed empty after evidence was written into this directory. Existing receipts were read, not rewritten. Report path intentionally remains inside the seat's sole authorized write directory; the assignment's shorter trailing path would have escaped it.

Self-evaluation: accuracy 4/5 (mixed valid/garbled wording is explicitly ambiguous); completeness 5/5 (all four questions have commands and retained outputs); clarity 4/5 (Q2 separates two distinct limitations); actionability 4/5 (strict-isolation correction requires a newly frozen instrument); conciseness 4/5 (detail retained for reproducibility). Overall 4.2/5. Highest-impact improvement: resolve “last parsed” wording without changing historical evidence. Would the user agree? The report distinguishes executed results, source-derived inference, finite-set limits, and decisions reserved for the canonical judge.
