source: S450 — CPython `Doc/library/secrets.rst`, fetched `.ufo/waves/round-74/fetch/secrets.rst.1:78-84`; own-work — `.ufo/waves/round-74/{claims-declaration-r74.md,controls/c1-replay-cases-r74.json,control-baseline-r74.txt,measurement-c1-r74.txt}`, `quality/counters/{c1-r74-witness-rule.py,c1-r74-replay-witness.py}`
verified-at: `b73db773aaf67c9b26c8cf1a4cd567dec3af11f4` (frozen instruments and measured candidate revision)
recheck: `python3 -I quality/counters/c1-r74-replay-witness.py --repo . --rev b73db773aaf67c9b26c8cf1a4cd567dec3af11f4 --base-rev bd5a971532f37df85a78f6f566dd1e649b79de11 --controls .ufo/waves/round-74/controls/c1-replay-cases-r74.json --scratch-root /fast/scratch/hyaku/mado-r74/R74ScribeC1` — run from the lane root after creating that explicit scratch directory; command documented, not executed by this scribe.

# Replay-witness kill credit (round 74, C1)

## Rule

Credit is not the child's exit status: `credit(out, nonce)` requires the last fully parsed `MADO_LANDING_COUNTERS_SELFTEST: <p>/<n> assertions passed` summary to have `n > 0`, `p < n`, and exactly `n - p` matching `SELFTEST FAIL <index>: ` detail lines, and additionally requires the last fully parsed `MADO_LANDING_WITNESS: <16 lowercase hex>` line to equal the caller's challenge. The arithmetic is the held round-72 rule; the witness comparison is the successor's additional condition. The counting command above concatenates captured stdout then stderr and scores both rules on each identical output. Its `measure()` generates the challenge with `secrets.token_hex(8)`, excluding the frozen stale token, and supplies it through `MADO_LANDING_NONCE`; it uses one generated challenge for the complete measurement, not a new challenge for each child. S450 supports the hexadecimal token representation: “Return a random text string, in hexadecimal.” The source describes token generation, not proof that assertions are truthful or that the harness is wired.

## Frozen case table

All names, modes and expectations below come from the frozen controls JSON; results come from the `MADO_R74_SCENARIO` lines produced by the recheck command above and retained in `measurement-c1-r74.txt`. Here `pass` means kill credit granted, not a green child selftest. The refusal explanations are grounded in `credit()` and the counter's `LANE_TEMPLATE`; they are not separate executed gates. This is the measurement case set, not the witness rule's separate internal selftest table.

| name | mode | expectation | which rule refuses it / why |
|---|---|---|---|
| `liar-success` | `liar-success` | pass | Neither: failing summary and matching details with current witness earn credit despite successful child exit. |
| `stderr-genuine` | `stderr-genuine` | pass | Neither: captured stderr carries a genuine failing summary and current witness. |
| `liar-kill` | `liar-kill` | fail | Both: green summary cannot earn kill credit despite unsuccessful child exit. |
| `crash-stderr` | `crash-stderr` | fail | Both: crash has no parsed summary. |
| `bare-failing` | `bare-failing` | fail | Both: failing summary lacks matching fail detail lines. |
| `mismatch-detail` | `mismatch-detail` | fail | Both: detail count disagrees with summary deficit. |
| `last-wins-pass` | `last-wins-pass` | fail | Both: last parsed summary is green. |
| `last-wins-fail` | `last-wins-fail` | pass | Neither: last parsed summary is failing with matching details and current witness. |
| `replay-captured` | `replay-captured` | fail | Successor only: captured block has stale witness; held arithmetic credits it. |
| `replay-no-witness` | `replay-no-witness` | fail | Successor only: no parsed witness; held arithmetic credits it. |
| `witness-mismatch` | `witness-mismatch` | fail | Successor only: wrong witness; held arithmetic credits it. |
| `witness-last-wins` | `witness-last-wins` | fail | Successor only: current witness is followed by a wrong parsed witness; held arithmetic credits it. |

## Measurement and do-nothing control

Counting command: the full `recheck:` invocation above. On its frozen denominator, the held rule scores **8/12 → successor 12/12**, with all four replay refusals supplying the difference and all eight carried expectations unchanged. These quantities are the command's `base_correct`, `correct`, and per-scenario lines, not an independent scribe measurement. The receipt binds the candidate revision to the `verified-at:` revision and the held extraction to the base revision in that command.

The pre-freeze receipt, attributed by the declaration to `.ufo/waves/round-74/proto/held-r74.py` (an uncommitted prototype, not a scored counter), records the following exact lines. Its original full shell invocation is not included in the receipt; no exact historical invocation is inferred. The scored recheck command above independently includes the held leg on the same outputs.

```text
HELD_R74: c1_correct=8/12 c2_correct=32/36
HELD_R74_C1_TARGET: 12/12 required, held=8/12 -> TARGET_MISSED
```

The retained candidate measurement ends with this exact contract line:

```text
MADO_R74_REPLAY_WITNESS: cases=12 correct=12 base_correct=8 verdict=TARGET_MET rev=b73db773aaf67c9b26c8cf1a4cd567dec3af11f4
```

The declaration reports measurement exit status `0`; this scribe did not rerun it. The text receipt itself contains the contract line but no shell exit-status trailer. The recheck command's frozen gate requires `cases == 12`, `correct == 12`, and `base_correct == 8`; a measured miss returns `1`, and usage/setup errors return `2` without a contract line. These are instrument semantics, not additional observed executions.

## Declared limits and open wiring question

- The challenge authenticates the run's echo, not the truth of its assertions. A child that echoes the current challenge and fabricates internally consistent failing arithmetic can still receive credit.
- The fixture set exercised by the recheck command is not fault coverage or a general adversarial-replay proof. The held rule still credits a captured summary accompanied by its matching details; the successor rejects the frozen stale/missing/wrong/last-wrong witness modes.
- The successor is a standalone instrument. The frozen round-72 harness is not edited. Open wiring question: in a separately authorized change, where will the actual harness caller generate and pass the challenge and require the child echo before granting landing kill credit? This draft supplies no claim that such integration exists.
- C2, no-harm selftests, registry/index/ledger checks and global axis preservation are outside this C1 scribe's execution evidence. The declaration lists obligations; reading that contract does not execute them.

## Scribe handoff and provenance

Behavior/axes: C1 calibration evidence fidelity and reusable knowledge-entry completeness; C2 operability is context only. The draft preserves the held-vs-successor distinction without upgrading receipt text or contract obligations into new execution evidence.

Touched surface: only this draft. No production instruments, frozen controls, corpus entry, source registry, or committed receipts were rewritten; no runtime, test, measurement, git mutation, commit, publish, or deployment was invoked by this seat. No tools were installed or upgraded.

Executed shell command (directory preparation), returned `OK`:

```sh
mkdir -p /fast/scratch/hyaku/mado-r74/R74ScribeC1 /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-74/w1/R74ScribeC1 && echo OK
```

All evidence was read from the requested declaration, receipts, controls, instrument source, fetched source, and the corpus shape exemplar `corpus/knowledge/control-set-mutant-kill-r73.md`; the baseline prototype header and fixture template were additionally inspected for provenance. No receipt was generated in scratch. Cleanup command: `rmdir /fast/scratch/hyaku/mado-r74/R74ScribeC1` (outcome returned separately in the seat handoff).

Known assignment conflicts, preserved verbatim for canonical adjudication:

> Your only write directory: /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-74/w1/R74ScribeC1/.

> Report: write your scoped findings to .ufo/waves/round-74/w1/R74ScribeC1.md

The latter path is outside the explicit write directory, so the scoped findings are included here instead; that outside path was not written.

> round: mado lane counter 74. Shape: ONE v1 wave of 12 seats (band 8–16); the L1 holds the
> planner seat (the validator rejects `planner` as a swarm role).

> Round mado 74, ONE v1 wave (13 seats).

The declaration and assignment differ on wave size; neither is evidence of executed seat population, and this C1 draft makes no seat-count claim.

Self-evaluation (editorial, not a gate): accuracy 4/5 — historical full baseline invocation is absent and explicitly not invented; completeness 4/5 — requested outside-directory report cannot be written within the bound; clarity 4/5 — provenance appendix is longer than the reusable entry; actionability 4/5 — harness wiring remains intentionally outside scope; conciseness 4/5 — verbatim conflicts add necessary handoff length. Overall 4.0/5. Improvement: L1 can separate this handoff appendix when applying the corpus entry and retain it as audit evidence; no new runs are needed to improve presentation. Would the user agree? The draft exposes the remaining evidence and path limits rather than asserting completion beyond this seat.
