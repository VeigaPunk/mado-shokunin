# mado round 84 — frozen claim declaration

Base: `7fd43921294116299dfce1443d56a951b9c81493` (master, ahead=0 behind=0 tracked=0 untracked=0 at start).
Two causally separable claims: C1 coverage of ambiguous allocation/declaration identities; C2 operability of producer-status propagation in the executable desktop runbook. Neither counter reads the other's instrument. L1 MadoR84 holds the planner seat.
Lowest-axis ties retain coverage and operability. Dormant freshness remains operator-owned; no retirement or score waiver. Saturation 9.0/window 3 unchanged. Existing 102/102 navigation, 86/86 calibration, 12/12 operability and 152/152 ledger are prior-round evidence, not fresh measurements.

## C1 — coverage: ambiguous namespace declarations are refused

Before: the held r83 bar-footprint tool silently keeps the last repeated allocation key, permits two extra surfaces to share a namespace, and permits an extra to reuse the bar's namespace. After: these three named declaration classes are setup refusals, not arbitrary predictions. This is a restriction of the join's input grammar, NOT a claim that layer-shell globally requires unique namespaces.

Control set: `.ufo/waves/round-84/controls/c1-cases-r84.json`, 61 cases, first 58 carried parsed-equal from r83. New cases: duplicate-extra-namespaces, duplicate-bar-namespace, duplicate-allocation-keys. Raw allocation input is preserved so JSON decoding cannot erase the duplicate before scoring. Sources: S486 RFC8259 section 4 (JSON uniqueness guidance), and the tool's own identity grammar; external protocol uniqueness is explicitly rejected.

Counter: `quality/counters/c1-r84-namespaces.py`. Counting command:

```sh
python3 -I quality/counters/c1-r84-namespaces.py --repo . --rev REV --base-rev 7fd43921294116299dfce1443d56a951b9c81493 --controls .ufo/waves/round-84/controls/c1-cases-r84.json --carried .ufo/waves/round-83/controls/c1-cases-r83.json --scratch-root DIR
```

Predicate: all 61 frozen cases score correct, all 41 enumerated mutants are killed, the held r83 tool scores exactly 58/61, the first 58 cases are carried parsed-equal, and the tool selftest is green; only then TARGET_MET.
Kill rule: a mutant is killed only when its scored case count is below 61; missing anchors earn no kill. Diagnostic --no-mutants prints MUTANTS_SKIPPED, never TARGET_MET.
Pre-scoring population assertion binds constant=enumerated=41. Do-nothing receipt `receipts/control-c1-r84-at-base.txt`: held tool 58/61, TARGET_MISSED. Target cannot be reached unchanged. Bounded score moves 10*58/61 to 10*61/61 only if the predicate verifies; no domain-mastery claim.

## C2 — operability: a failed producer is not a successful pipeline

Before: a producer emitting plausible `b true` then exiting 7 is hidden by a successful tail (`cat`), returning rc0. After: fifteen pipeline command rows explicitly enable pipefail; two contained, read-only fixture rows demonstrate unguarded=0/guarded=7 and bind a failed producer's rc7 plus its plausible stdout. No host producer is made to fail and no fixture is represented as live tray state. Source S487 Bash manual section 3.2.3 grounds pipeline status semantics; support by this host's /bin/sh is measured by the fixture.

Control set: `.ufo/waves/round-84/controls/c2-runbook-cases-r84.json`, 33 cases, first 31 carried from r83. Fifteen pipeline rows supersede only argv and skill_anchor to declare the guard; outcomes/churn/negatives remain unchanged. Counter `quality/counters/c2-r84-runbook.py` prints the superseded names.

```sh
python3 -I quality/counters/c2-r84-runbook.py --repo . --rev REV --controls .ufo/waves/round-84/controls/c2-runbook-cases-r84.json --carried .ufo/waves/round-83/controls/c2-runbook-cases-r83.json --scratch-root DIR
```

Predicate: cases=33 executed=33 matched=33 shapes=26/26 anchors=33/33 rows=33/33 and mutants=29 killed=29, with SKILL/tool/fixture bytes bound to REV; only then TARGET_MET.
Kill rule: mutated counter exits nonzero and its observed matched count is below 33 (or no contract parses); exact behavior is the counter's existing rule, not authentication of child honesty. Diagnostic --no-mutants prints MUTANTS_SKIPPED.
Population assertion constant=enumerated=29 precedes scoring. Do-nothing receipt `receipts/control-c2-r84-unguarded.txt` runs the guarded fixture's producer command WITHOUT the guard: pipeline rc0, plausible stdout, failed-case matched=0/1, TARGET_MISSED. This substantive control, not a section-heading refusal, is the before-state.

## Freeze and integration boundary

Both predicates, targets and kill rules are fixed before candidate scoring. `receipts/population-before-scoring-r84.txt` records enumeration assertions before either candidate is measured. Counter population mistakes remain honest misses; no target narrowing. Source truths are limited to the statements above. Existing r83 causal-cheat limitations are not claimed solved.

Harm watch: standing gate selftest, index, ledger, axis publication; no config plane, compositor or service writes; no credential/session-material capture. SOURCES census must end exit0. Round83 routed R1 missing SKILL registry rows will be added, R2 population assertion is implemented, R3 connector overlap review is explicitly assigned. Assimilation: none. considerthese/2026-11-04.md proposal 1 is the one proposed adoption (domain-share line in lesson/report); proposal7 labeling continues an already-held rule.
