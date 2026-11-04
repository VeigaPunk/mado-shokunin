# R76RevC1 — frozen C1 falsification review

Scope: base c3e0bc5f10b72964d54d18dc9b0706dc308dd1bf; freeze cb713254ee9926e036e594312fdc61b57825526b; controls SHA256 320f7e6b54e71776f2d5b179b9a8b09ee9185886e2aeb045af0ecc9171cc77ea (independently checked). Axes: calibration correctness, baseline provenance, evidence integrity, zero lane mutation. No repairs or admission verdict.

## P2 — `--base-rev` does not bind the advertised held counter

Frozen `quality/counters/c1-r76-outcome-field.py:345` resolves `base_sha` but never uses it. Lines 388–394 calculate `base_score` locally from the candidate mutant's parsed mz, not from any counter loaded at the base revision. This is a valid mz-only mathematical control, but not evidence that the held implementation exists or ran at the supplied revision.

Reproduce (paths below are lane-relative):

```sh
python3 -I .ufo/waves/round-76/w1/R76RevC1/frozen-counter.py \
 --repo /home/vgpnk/Projects/shokunin/mado-shokunin \
 --rev cb713254ee9926e036e594312fdc61b57825526b \
 --base-rev 74d3b7bacab1c8eb2300b82d39eb0fcadf62db12 \
 --controls .ufo/waves/round-76/controls/c1-outcome-cases-r76.json \
 --scratch-root /fast/scratch/hyaku/mado-r76/R76RevC1/absent-base
```

`git cat-file -e 74d3b7bacab1c8eb2300b82d39eb0fcadf62db12:quality/counters/c1-r75-harness-witness.py` returned 128: held counter absent. Expected for revision-bound provenance: setup rejection (rc 2, no target certificate), or an explicit statement that the base is only a locally reimplemented scoring rule. Observed rc 0:

`MADO_R76_OUTCOME_FIELD: cases=16 correct=16 mutants=4 killed=4 base_killed=0 verdict=TARGET_MET rev=cb713254ee9926e036e594312fdc61b57825526b`

Receipt: `w1/R76RevC1/absent-base.txt` (under this round directory).

Related evidence mismatch: `control-baseline-r76.txt:3–7` records 15/15 and the earlier mutants outcome-term-dropped/prefix-match/first-witness-wins/case-insensitive, not the final 16-case v3 outcome-summary-only/outcome-killed-only/outcome-killed-any/outcome-killed-or set. Expected if used as direct pre-freeze control evidence for the final four: those four names and 16-case denominator. Observed: different denominator and mutation recipes. The final measurement's base_score=16/16 is a separate local mz-only calculation; do not describe the old receipt as a direct run of the final four.

## P2 — frozen kill sentence contradicts the executed threshold

`claims-declaration-r76.md:67–69` explicitly freezes killed iff score is **below fifteen**, while frozen counter lines 393–394 use `< len(cases)`, i.e. below sixteen. The committed `measurement-c1-r76.txt:19–21` reports score=15/16 and killed=yes for three mutants.

Reproduce without rerunning a reported check: compare those receipt rows with the declaration's literal predicate. Expected under the written frozen predicate: three score-15 mutants survive, only the score-14 outcome-killed-or dies (killed=1, not 4). Observed executable predicate: killed=4. The header/docstring of the counter also repeatedly says fifteen cases and lists superseded mutation names. This is a frozen-spec/evidence inconsistency, not evidence that the executable misses its implemented 16-case target.

## Advisory — a second later valid contract row wins, including a different revision

Frozen counter `parse_row`, lines 245–251, scans backwards and accepts the first full regex match. It does not bind `rev=` to the fixture revision or cross-check mz/killed/verdict consistency.

Reproduce after `python3 .ufo/waves/round-76/w1/R76RevC1/attack.py` creates scratch fixtures:

```sh
python3 .ufo/waves/round-76/w1/R76RevC1/later-row.py \
 --repo /fast/scratch/hyaku/mado-r76/R76RevC1/attacks/fixtures/right \
 --rev HEAD --scratch-root /fast/scratch/hyaku/mado-r76/R76RevC1/later-row
```

Actual harness first prints mz=pass/verdict=TARGET_MET for the right fixture. Wrapper then prints mz=fail/verdict=TARGET_MISSED with rev=40 `a` characters. Observed harness rc=0; frozen `parse_row(stdout)` returns `('fail', 'fail')`, not `('pass', 'pass')`. Receipt: `w1/R76RevC1/later-row.txt`. This follows the parser's documented last-parsed-row policy, so it is a trust/row-authenticity limitation rather than a demonstrated violation of the two-field claim. It must not be represented as authenticating a unique row or measured revision.

## Advisory — broken echo rule still reaches TARGET_MET (disclosed limit confirmed)

Reproduction: `python3 .ufo/waves/round-76/w1/R76RevC1/echo-drop.py`. This test injects only candidate extraction bytes into the frozen counter: `green_with_witness` returns `bool(r72_green(out))`, removing witness equality; no canonical file or commit changes. All real fixture children, four named mutations, labels and scoring remain unchanged. The output hash identifies the modified candidate; its displayed rev remains the frozen extraction argument, so this is explicitly an injected-byte experiment, not a committed measurement revision.

Expected under the declared negative result (`claims-declaration-r76.md:50–55,82–87`): this rule defect remains unobservable through the final outcome because killed==2 already requires M-Z's witness. Observed: cases=16 correct=16 mutants=4 killed=4 base_killed=0 verdict=TARGET_MET, rc=0. Receipt: `w1/R76RevC1/echo-drop.txt`. Thus no erroneous v3 label was found; the fail/fail labels on green-absent and analogous cases necessarily allow this broken intermediate rule. The certificate covers the published outcome's observable green/kill terms, not witness-rule correctness in isolation.

## Required combined mz/outcome mutation

`attack.py` substitutes `g["credit"] = lambda out: False` and `outcome_green(...): return True` in isolated candidate bytes. Both scored fields change across the frozen population. Observed score=0/16, base_score=13/16: **killed=yes, base_killed=yes**, not base_killed=0. Receipt `w1/R76RevC1/attacks.txt:52`; reproduction `python3 .../R76RevC1/attack.py`. Expected exactly this under counter lines 389–394. Therefore base_killed=0 is conditional on the named outcome-only mutations preserving mz, not a general mutation-testing invariant; this condition is already disclosed at declaration lines 82–83.

## Three independently re-derived labels

Used fresh harness evidence lines, never the printed contract row as the oracle; receipt `w1/R76RevC1/attacks.txt` retains full outputs. Canonical logic: frozen r72 `measure()` sets mz from credited failed assertions, mr from real/forged child pair, sums the kills, then calls the r76 installed `contract_line`; frozen r76 `outcome_green` lines 141–146 requires green-with-witness AND killed==2.

| Case | Independent evidence | Derived (mz, verdict) | Frozen label |
|---|---|---|---|
| right | lines 8–14: SELFTEST 2/2 green=yes; M-Z 1 failed assertion, 1/2 killed=yes; M-R control green and forged credit=yes killed=yes | pass, pass | pass, pass |
| always-red | lines 25–31: SELFTEST 1/2 green=no; M-Z 1 failed assertion, 1/2 killed=yes; M-R killed=yes | pass, fail (red own summary despite two kills) | pass, fail |
| green-mutant | lines 42–48: SELFTEST 2/2 green=yes; M-Z 0 failed assertions, 2/2 killed=no; M-R killed=yes | fail, fail (one kill despite green own summary) | fail, fail |

## Residual risks and verification gaps

- LSP unavailable: `read xd://lsp` returned `No such tool`. No semantic references/definition/diagnostics service could be used; conclusions use the frozen source and exercised subprocess evidence, not grep as semantic proof.
- The committed label-derivation receipt is only a table of derived values; it contains no raw SELFTEST/M-Z/M-R lines or derivation command. This review supplies raw fresh evidence for three labels, not an independent reconstruction of all sixteen.
- No production tools, swarm runtime, routing or resume path changed in the scoped diff; continuity/saturation claims were not inferred from this C1-only review.
- No production repairs, installs or host probes. Only seat-owned reproduction scripts/receipts and this explicitly assigned report were written; fixture git mutations were confined to seat scratch with fixture-root assertions in the canonical builders. Scratch removed after preserving receipts.

Self-evaluation: accuracy 4 (injected-byte experiment explicitly distinguished from committed run); completeness 4 (all four requested attacks plus three labels; full sixteen-label independent reconstruction not requested/performed); clarity 4 (threshold disagreement separated from executable result); actionability 4 (reproduction drivers retained); conciseness 4 (raw outputs kept in receipts rather than repeated). Mean 4.0; preserve the distinction between mathematical mz-only control and executed held-counter provenance when routing findings.
