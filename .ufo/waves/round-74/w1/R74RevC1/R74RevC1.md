# R74RevC1 — C1 adversarial review

## Axes and scope

Calibration: agreement with the frozen C1 sentence and replay discrimination. Operability: deterministic, isolated reproduction. No-harm: committed lane bytes, held instruments, receipts, and sibling work remain untouched. C2 is context only. No runtime routing, resume, admission, or saturation changes are in this assigned diff; no judgment/admission is made here.

Read first: `.ufo/waves/round-74/claims-declaration-r74.md`. Reviewed the two added C1 files at freeze commit `b73db773aaf67c9b26c8cf1a4cd567dec3af11f4` with read-only `git show`, their current definitions and caller, the frozen controls, and all three named receipts. The exercised rule SHA-256 is `6a6d77f4ad6777a01c49fa0c4e46a7d510e4f525c71a0c4c3f6280bb01394516`, identical to measurement-c1-r74.txt:3.

## Findings, by severity

### P2 — Witness grammar narrows “16 hex,” allowing a wrong last hex witness to be ignored

Defect class: contract/grammar mismatch, with both false rejection and false acceptance.

Frozen declaration:37–41 requires the last parsed `MADO_LANDING_WITNESS: <16 hex>` to equal the supplied challenge. `quality/counters/c1-r74-witness-rule.py:37` instead permits only `[0-9a-f]{16}`; :63–65 ignores a nonmatching line and retains the earlier token, and :80–81 then grants credit.

Two reproduced disagreements against that literal frozen sentence:

* `uppercase-witness-matching-challenge`: witness `A1B2C3D4E5F60718`, caller challenge exactly `A1B2C3D4E5F60718`, one fail detail, summary `1/2`: rule **reject**, frozen **accept**. Exact cause :37 and :63. Although the production challenge generator emits lowercase, the frozen caller-supplied-token contract does not say lowercase.
* `valid-then-uppercase-wrong-witness`: correct lowercase witness followed by `MADO_LANDING_WITNESS: DEADBEEFDEADBEEF`, one fail detail, summary `1/2`: rule **accept**, frozen **reject**. Exact cause :37, :63–65, :81. This disagreement occurs with the normal lowercase production challenge: the later wrong 16-hex witness is silently ignored.

The rule's own :169 labels its selftest grammar “16 lowercase hex”; that narrower implementation statement does not amend the frozen sentence. If “parsed” was intended to mean lowercase-only, this is a specification ambiguity rather than an implementation error under that alternate interpretation. The literal frozen text is the review oracle; no new oracle was substituted into the measured denominator. Recommendation: align implementation to the frozen hex grammar rather than retroactively change the frozen declaration.

### P2 — Counting caller reuses one challenge across all twelve child runs

Defect class: challenge freshness/child-binding gap in caller, not arithmetic failure.

`quality/counters/c1-r74-replay-witness.py:282–285` generates and emits one nonce **outside** the :289 case loop. Each different Bash child receives that same nonce at :291–292, and the same nonce is passed to `candidate_credit` at :294. This is not a per-child/per-run challenge despite declaration:37–39 and rule:16–17 describing one.

Fixtures `same-nonce-child-A` and `same-nonce-child-B` launch separate Bash children; B emits exactly the captured bytes accepted for A. Both receive credit against the same supplied nonce. Both also satisfy the *stateless* frozen `credit(out, nonce)` predicate: it has no child identity or consumption input. Thus this is **not** a disagreement with that function predicate and should not be counted as a third fixture disagreement. It demonstrates that the canonical caller's challenge reuse makes a captured block from another child in the same measurement acceptable. The committed receipt independently shows only one challenge at measurement-c1-r74.txt:5 for twelve scenarios at :6–17.

Recommendation: create the challenge inside the child-launch loop and retain one challenge per evaluated child. No request is made to authenticate assertion truth, which declaration:54–57 explicitly excludes. This does not invalidate the observed 12/12 frozen controls; those four replay negatives have absent or wrong tokens, not a token captured from an earlier child in the same measurement.

## Executed fixture results

Driver: `.ufo/waves/round-74/w1/R74RevC1/fixtures.py` (imports rule with `runpy.run_path`). Full inputs, stdout/stderr separation, caller tokens, and results: sibling `fixtures-results.json`.

| New fixture | Rule | Frozen predicate | Agreement |
|---|---|---|---|
| Witness after summary | accept | accept | yes |
| Witness only on stderr; summary/details stdout | accept | accept | yes |
| Summaries `2/2` then `1/2`, one witness/detail | accept | accept | yes |
| Witness trailing spaces | accept | accept | yes* |
| Witness CRLF | accept | accept | yes* |
| Uppercase witness, lowercase challenge | reject | reject | yes |
| Uppercase witness, same uppercase challenge | reject | accept | **no** |
| 17-hex witness | reject | reject | yes |
| Summary `p=3 > n=2` | reject | reject | yes |
| Genuine captured detail, stale witness | reject | reject | yes |
| Correct witness then uppercase wrong 16-hex witness | accept | reject | **no** |
| Correct witness then malformed 17-hex witness | accept | accept | yes |
| Correct witness then valid lowercase wrong witness | reject | reject | yes |
| Separate child A, shared nonce | accept | accept | yes; identity unobservable |
| Separate child B replaying A, shared nonce | accept | accept | yes; identity unobservable |

*The frozen sentence does not specify outer whitespace/line-ending treatment. The oracle uses the existing line normalization (`splitlines`/`strip`) for these rows, not a new whitespace rejection policy. Uppercase tokens are compared byte-for-byte, not case-folded; a mismatched uppercase token is correctly rejected when it is the sole witness. A 17-hex line is malformed, so it cannot replace the last parsed valid witness.

Command exercised (exit 0):

```text
python3 -I /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-74/w1/R74RevC1/fixtures.py --scratch-root /fast/scratch/hyaku/mado-r74/R74RevC1 --output-dir /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-74/w1/R74RevC1
fixtures=15 agreements=13 disagreements=2
```

The stale captured block rejection closes the specified round-72 limit for an actually stale token. Summary selection uses the last parsed summary (:46–51); `p >= n` and zero totals reject (:75–77); exact fail-count mismatch rejects (:78–79). Summary and witness need not be adjacent or ordered. Stderr-only witness works because the canonical caller combines stdout then stderr (:293); the rule itself has no stream API.

## Residual risk and verification gaps

* LSP device unavailable: reading `xd://lsp` returned “No such tool”; status, references, definitions, and diagnostics could not be requested. Caller discovery used literal grep under quality/tools and direct line inspection, not semantic proof of absence of other callers.
* Stream concatenation preserves neither global emission chronology nor necessarily a boundary newline. No claim of temporal last-witness authenticity is supported; the frozen API takes one combined text string. Cross-stream ordering variants beyond the assigned split-stream case were not exercised.
* `credit` authenticates only equality to a supplied token and arithmetic consistency, not assertion truth, child identity, token single-use, or process success. No claim of comprehensive replay protection or saturation is justified by the finite 12/12 receipt.
* Re-read, did not rerun or rewrite: committed C1 receipt reports 12/12, base 8/12; C2 receipt reports 36/36, base 32/36 and census 20/13/13/0; pre-freeze receipt reports held 8/12 and 32/36. No unrelated selftests, builds, linters, or state checks were run.
* No committed files changed, no git/jj mutation, no installations, no additional agent/runtime dispatch. Fixture driver and persistent receipt are within the seat's own directory. Scratch was used explicitly and removed after the persistent result was written. The conflicting shorter root report path in the assignment was not written because the hard bound permits only this seat directory.

## Self-evaluation

Accuracy 4/5: observed results and exact lines cited; “16 hex” versus lowercase-only “parsed” remains an explicit interpretation boundary. Completeness 5/5: all eight requested categories covered by fifteen fixtures, including two actual children. Clarity 4/5: distinguishes API disagreement from caller freshness; grammar discussion necessarily has two interpretations. Actionability 5/5: exact implementation lines and scoped recommendations supplied. Conciseness 4/5: full fixture table and evidence increase length but keep the review reproducible. Mean 4.4/5. Highest-impact improvement: authoritative clarification of the non-frozen grammar terminology would remove interpretation risk; none was invented here. Would the user agree? The retained executable cases allow independent inspection.
