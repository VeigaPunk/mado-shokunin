# mado round 73 — lesson

author: mado L1 integration draft, prepared by R73ScribeLesson (scribe; no instrument execution).
date: 2026-11-04
base: `d3f6c9f5d8b3401c01f189e8cd4b8dbc917a2bce`
frozen declaration: `.ufo/waves/round-73/claims-declaration-r73.md`, commit
`87e4c61ac90e9ac587c9f65ac7844ded268d9046`
measured instruments: `1459cca11fb5d3956a6e9a128217852dd0c28cb9`
pre-freeze do-nothing receipt: `.ufo/waves/round-73/control-baseline-r73.txt`

## Outcome and boundaries

Axes: calibration (C1), operability (C2); no-harm obligations preserve the held navigation,
ledger and gate surfaces. Both committed candidate receipts end in `TARGET_MET` at the measured
instrument revision. The seat reread receipts, not reran measurements. The assignment records rc 0
for both; their text files contain verdict lines, not independently captured process statuses.

| claim | committed measurement | do-nothing control | evidence |
|---|---|---|---|
| C1 calibration: the frozen outcome set separates four named mutations of the landing outcome rule | `cases=10 mutants=4 killed=4 base_killed=2 verdict=TARGET_MET` | held eight-case set kills 2/4 | `.ufo/waves/round-73/measurement-c1-r73.txt`, final line; `control-baseline-r73.txt`, `PROTO_R73_C1 killed` |
| C2 operability: global-declared mapping guards and mutated-process-environment transports count | `population=20 readers=13 guarded=13 unguarded=0 controls=28/28 base_controls=25/28 verdict=TARGET_MET` | held round-71 classifier scores 25/28 | `.ufo/waves/round-73/measurement-c2-r73.txt`, final line; `control-baseline-r73.txt`, `PROTO_R73_C2` |

Counting commands (from the frozen declaration; recorded here, not executed by this scribe):

```sh
python3 -I quality/counters/c1-r73-summary-mutants.py --repo . \
  --rev 1459cca11fb5d3956a6e9a128217852dd0c28cb9 \
  --base-rev d3f6c9f5d8b3401c01f189e8cd4b8dbc917a2bce --scratch-root DIR
python3 -I quality/counters/c2-r73-shapes.py --repo . \
  --rev 1459cca11fb5d3956a6e9a128217852dd0c28cb9 \
  --base-rev d3f6c9f5d8b3401c01f189e8cd4b8dbc917a2bce \
  --controls .ufo/waves/round-73/controls/c2-cases-r73.json --scratch-root DIR
```

C1 adds `zero-denominator` and `valid-then-garbled` to the byte-carried held eight cases.
N1 (drop `n > 0`) and N2 (prefix-match parser) survive the held denominator but fail these
respective new cases. N3 (relaxed comparison) and N4 (kill-count-only verdict) already fail held
cases. Four named syntactic mutations are not general fault coverage or full harness execution.

C2's held classifier misses exactly `global-rebind-guard`, `environ-splat-guard` and
`environ-call-guard`; the candidate receipt lists each as correct. Its guard model is syntactic:
one `global` declaration, cross-function **line order, not execution order**, one `os.environ`
store and the two copy forms `{**os.environ}` / `dict(os.environ)`. A store in a function that
runs after the launch can still count when its source line comes first. No cross-module producer,
`os.environ` alias support or value interpretation is claimed; alias chains stay bounded by the
held carrier model.

One v1 wave has 13 seats; the L1 holds planner because the validator rejects `planner` as a swarm
role. No planner is dispatched (frozen declaration opening). No desktop, compositor, session,
service or live configuration behavior is measured here. No promotion or axis retirement is claimed.
The declaration's no-harm obligations are obligations, not this seat's execution evidence.

## Mistakes

Evidence basis: prior routed defects are the non-author record in
`corpus/lessons/round-72-verifier-spotcheck.md` § Routed defects for round 73. This round's draft
history is disclosed by `.ufo/waves/round-73/make-spec-r73.py:165-170`; the committed classifier
shows the final regression and selftest checks, not the discarded draft's observed failure output.
A proposed check below does not become a demonstrated repair without its own red/green receipt.

| mistake | class | evidence pointer | captured-by | fix and the failure it can show; evidence status |
|---|---|---|---|---|
| M73-1: registry/lesson selftest tallies stayed at 83/83 and 24/24 after the r72 repair changed them to 87/87 and 25/25. | number-drift | r72 verifier § Routed defects item 1; `quality/tool-ledger.md:161,163`, `SKILL.md:731`, r72 outcome entry §5 as cited there | CORPUS count-carries-command rule; non-author spot-check caught it | Correct or revision-qualify current registry references; compare each pinned tally to that revision's selftest output. The verifier supplies the contradictory old/new values; this seat does not certify a landed correction. |
| M73-2: the report named `w1/R72ExecBattery.md`, but the deliverable is `w1/R72ExecBattery/R72ExecBattery.md`. | reference-drift | r72 verifier § Routed defects item 2 | CORPUS evidence-pointer requirement; non-author spot-check | Append the correct pointer in the next report/erratum, never rewrite filed report bytes. A path-resolution check distinguishes the missing old pointer from the actual deliverable. Correction not executed by this seat. |
| M73-3: rejected S446 lacked a located quote even though rejected rows also require one. | landing | r72 verifier § Discernment row S446 and § Routed defects item 3; `corpus/lessons/round-72.md` § Gate | CORPUS SOURCES rule 1; non-author re-open | Add a real ≤25-word located quote at `Doc/builtins/stdtypes.rst` in an append-only correction/Gate record. A per-new-row URL/date/quote/location audit must reject the original omission; no substitute quote is invented here. |
| M73-4: r69 deliverable-check reds remained open and unnamed through r72. | landing | r72 verifier § Routed defects item 4, carrying r71 item 7 | none in r72 report; non-author carry-forward review | Repair under an r69 correction or explicitly name the deferred debt and reason. Compare the routed-defect list to closure dispositions: omission must fail. This draft names it as unresolved; no r69 repair is claimed. |
| M73-5: the report called held W04 warnings the only warnings, omitting held W01 S277. | number-drift | r72 verifier § Routed defects item 5 (39 W0 lines on each side, including W01) | CORPUS count-carries-command and negative-claim-carries-sweep rules | Append an erratum: held W04 family **and** held W01 S277; no new warning was shown by that verifier. Full warning-class enumeration can falsify “only W04.” Counts are inherited verifier evidence, not a new census. |
| M73-6: the operator addendum's route sentence disagreed with live `task.agentModelOverrides`. | scope | r72 verifier § Conformance, Prompt contract; § Routed defects item 6 | prompt's own config-is-authority rule prevented demonstrated routing effect | Operator-side refresh against authoritative routing config; a text/config comparison can show the mismatch. Not lane debt, not a reason to probe or modify host config here. |
| M73-7: the first r73 classifier treated a store inside a function that runs after the launch as a guard; the L1 initially wrote that regression's label the wrong way round. | scope | r73 `make-spec-r73.py:165-169`; declaration C2 Declared limits; `quality/counters/c2-r73-shapes.py:895-902,1310-1316` | classifier selftest expectation comparison; disclosed limit rather than an execution-order proof | Keep the line-order limit explicit. The committed `r73-global-rebind-replaced-between` case expects `(True, False)` when a replacement intervenes; `_selftest_checks` compares all regression classifications. Wrong replacement handling or a reversed expected label can fail that comparison. This does not repair general execution-order analysis; historical red output was not supplied to this seat. |
| M73-8: embedded-case literals first used doubled newline escapes, making invalid snippets; only the selftest caught them. | vacuous | r73 `make-spec-r73.py:169-170`; committed classifier `REGRESSIONS` and `_selftest_checks:1349-1366` | embedded classification selftest, not the frozen measurement alone | Keep real newline escapes in snippet literals and expected reader/guard comparisons. Invalid source is classified `(False, False)`; positive-reader expectations expose broken literals instead of silently scoring meaningless snippets. Historical failure is dispatch-disclosed, not a rerun or preserved red receipt here. |
| M73-9: the held eight-case outcome set passed two broken rules while reporting its own cases green. | vacuous | r72 lesson § Mutation evidence; r73 baseline and C1 measurement, N1/N2 lines | r72 mutation battery, then r73 frozen mutant-kill counter | Add the two frozen cases under a new denominator. The committed receipt demonstrates N1/N2 fail new cases while surviving held cases, and all four mutants are killed. This is demonstrated finite-set discrimination, not universal rule correctness. |

## Gate

Merge-time source slots only: the source scout owns fetch receipts; these are **not** completed
admissions, new registry rows or external spot-check results. The L1 must replace each marked
field with the fetched evidence before landing this lesson. Source URLs are the frozen source
plan; no quote, access date, fetch identity or admission decision is inferred from that plan.

| source slot | URL | access date | located quote (≤25 words) | disposition and grounding |
|---|---|---|---|---|
| <S447> | https://raw.githubusercontent.com/python/cpython/v3.14.8/Doc/reference/simple_stmts.rst | <fill by L1 after the fetch> | <fill by L1 after the fetch> | <fill by L1 after the fetch>; `global` binding semantics |
| <S448> | https://raw.githubusercontent.com/python/cpython/v3.14.8/Doc/library/os.rst | <fill by L1 after the fetch> | <fill by L1 after the fetch> | <fill by L1 after the fetch>; process environment mapping |
| <S449> | https://raw.githubusercontent.com/python/cpython/v3.14.8/Doc/library/subprocess.rst | <fill by L1 after the fetch> | <fill by L1 after the fetch> | <fill by L1 after the fetch>; child `env` transport |

For every slot, retain the exact file/section/line locator and quote word count with the scout's
receipt pointer. All new rows, including any rejects, need URL/date/located quote (CORPUS SOURCES
rule 1); rejection requires a reason and flip condition. Do not infer a reject or manufacture one.
Existing-row `status`, `recheck` or `used-by` changes require old→new disclosure if the L1 makes
them; this seat made none. Non-author Gate re-open/spot-check remains closure-owned; no result is
claimed by this draft. The standalone merge variant is `draft/gate-block.md` in this seat's directory.
