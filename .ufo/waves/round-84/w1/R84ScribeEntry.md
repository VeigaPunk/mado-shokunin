# R84ScribeEntry — report-only knowledge drafts

## Scope and axes

Axes: C1 coverage; C2 operability; non-regression in provenance accuracy and host/write boundaries. This seat drafts knowledge and Gate/Mistakes text only. No counters, fixtures, live reads, builds, tests, judge, commits or publication were executed. No round acceptance or score increase is asserted.

Frozen revision: `3f9eec3906ddd1492e8bc08325e83064f00111ea`; base: `7fd43921294116299dfce1443d56a951b9c81493`. All artifact paths below are lane-root-relative. Draft destinations below are suggestions, not files created by this seat.

## Knowledge entry 1 — namespace discipline (draft only)

Suggested destination: `corpus/knowledge/bar-footprint-namespace-discipline-r84.md`.

source: S486, RFC8259 §4 Objects, https://www.rfc-editor.org/rfc/rfc8259.txt; lane identity grammar in `.ufo/waves/round-84/claims-declaration-r84.md` §C1; controls `.ufo/waves/round-84/controls/c1-cases-r84.json`.
verified-at: frozen revision above contains those controls and `.ufo/waves/round-84/receipts/control-c1-r84-at-base.txt`; the committed receipt records the held base tool at correct=58/61, TARGET_MISSED, exit=1. This seat read the receipt, not a fresh execution or candidate pass.
recheck: use the declaration's revision-bound `quality/counters/c1-r84-namespaces.py` invocation with the frozen controls, carried r83 controls, explicit base and isolated scratch; require the full declared predicate and reviewer findings, not a diagnostic-only result.

RFC8259 says JSON object names SHOULD be unique and documents divergent duplicate-name handling, including last-value selection. That supports rejecting repeated allocation JSON keys before decoding discards evidence; it does not impose layer-shell namespace uniqueness. Refusing two extras sharing a namespace or an extra reusing the bar namespace is this lane join's input grammar. The three named controls are `duplicate-extra-namespaces`, `duplicate-bar-namespace`, and `duplicate-allocation-keys`. The held tool misses all three. Whether the candidate satisfies the full predicate is not established by this report. The prior allocation-source causal gap is not claimed repaired.

## Knowledge entry 2 — producer status (draft only)

Suggested destination: `corpus/knowledge/runbook-producer-status-r84.md`.

source: S487, Bash Reference Manual §3.2.3 Pipelines, https://www.gnu.org/software/bash/manual/html_node/Pipelines.html; `.ufo/waves/round-84/controls/c2-runbook-cases-r84.json`; committed fixtures `.ufo/waves/round-84/fixtures/{failing-producer,pipefail-guard}.sh`.
verified-at: frozen revision above contains the controls, fixtures and `.ufo/waves/round-84/receipts/control-c2-r84-unguarded.txt`. The committed receipt records producer rc7, unguarded pipeline rc0, synthetic stdout `b true`, matched=0/1, TARGET_MISSED, exit=1. Guard fixture bytes were read, not executed by this seat.
recheck: use the declaration's revision-bound `quality/counters/c2-r84-runbook.py` invocation with carried controls and isolated scratch; separately retain the guarded fixture's observed status and bind it to the measured shell and revision.

Bash normally reports the last pipeline command's status; pipefail instead reports the rightmost nonzero status, or zero if all succeed. A successful `cat` therefore can conceal a producer that emits plausible output and exits 7. The committed guard fixture explicitly compares unguarded and guarded pipelines using `/bin/sh`; the manual's Bash semantics alone do not prove that shell supports the option. The declaration specifies fifteen guarded pipeline rows plus two synthetic fixture rows. Expected guarded=7 is a declared target here, not an observed result from this seat. Synthetic producer output is not a live tray-health reading, successful D-Bus query, or proof of host producer behavior.

## Suggested Gate text (not applied)

- C1: retain raw allocation JSON through duplicate-key detection. Require all three ambiguity refusals and all carried cases, the declared selftest, and constant=enumerated=41 with 41 scored kills under the frozen rule. Missing anchors earn no kill. Only the complete declared predicate can justify TARGET_MET; `--no-mutants` cannot.
- C2: require the frozen 33-case predicate, 26/26 shapes, 33/33 anchors and rows, and 29/29 mutants killed under its existing rule, with SKILL/tool/fixture bytes bound to the measured revision. Retain synthetic unguarded rc0 versus guarded rc7 evidence separately from authorized live observations. Do not convert an unavailable or unsupported shell guard into a successful measurement.
- Preserve the independent standing-gate, index, ledger, axis-publication and source-census requirements. This report does not execute or waive them. Population receipt `.ufo/waves/round-84/receipts/population-before-scoring-r84.txt` records C1 41=41 and C2 29=29, exit=0; enumeration agreement alone is not mutation-kill evidence.

## Suggested Mistakes text (not applied)

- Do not elevate RFC8259's SHOULD to a universal MUST, or JSON member-name guidance to a layer-shell namespace requirement. The namespace refusal is local grammar.
- Do not parse away repeated allocation keys and then claim duplicates were tested. Keep the raw-input control load-bearing.
- Do not infer producer success from plausible stdout or a successful tail, infer `/bin/sh` support from Bash documentation, or describe a synthetic failing producer as live tray health.
- Do not promote retained baseline misses, source registry labels, fixture source code, planned rows, or population equality into fresh candidate success. Finite controls also do not erase r83's documented causal limitations.

## Provenance, commands and outcomes

Read-only source inspection used the read/grep tools; no source fetch was performed by this seat. The local fetched RFC text at `.ufo/waves/round-84/fetch/rfc8259.txt:322-334` contains the uniqueness guidance; Bash text at `.ufo/waves/round-84/fetch/bash-pipelines.html:119-125` contains the status semantics. Those fetched files were not in the frozen inventory returned below. This seat did not independently validate fetch hashes or freshness.

The task calls S486/S487 “planned rows”; the observed working-tree `corpus/SOURCES.md:438-439` labels both `mined`. This is a status/provenance distinction, not evidence of candidate execution. Their row destinations were absent from the frozen inventory queried below; this seat creates neither destination. No broader conflict adjudication is attempted.

Exact shell commands executed, from the lane root except scratch lifecycle:

1. `mkdir -p /fast/scratch/hyaku/mado-r84/R84ScribeEntry` — completed with no output; scratch lifecycle only.
2. `git ls-tree -r --name-only 3f9eec3906ddd1492e8bc08325e83064f00111ea -- .ufo/waves/round-84 corpus/knowledge/bar-footprint-namespace-discipline-r84.md corpus/knowledge/runbook-producer-status-r84.md` — listed the declaration, both controls, both fixtures, census-start and the three retained control/population receipts; neither proposed knowledge destination appeared. This unguarded inventory read was supplemented by guarded content reads below; no replacement-ref audit is claimed.
3. `git --no-replace-objects show 3f9eec3906ddd1492e8bc08325e83064f00111ea:.ufo/waves/round-84/receipts/control-c2-r84-unguarded.txt` — returned the retained TARGET_MISSED receipt quoted above. Its `exit=1` is receipt content, not this read command's outcome.
4. `git --no-replace-objects show 3f9eec3906ddd1492e8bc08325e83064f00111ea:.ufo/waves/round-84/receipts/control-c1-r84-at-base.txt` — returned the retained 58/61 TARGET_MISSED receipt. Its first line describes `r84 counter run_cases` rather than preserving a complete reproducible original invocation; no exact original counter command is invented here.
5. `git --no-replace-objects show 3f9eec3906ddd1492e8bc08325e83064f00111ea:.ufo/waves/round-84/fixtures/pipefail-guard.sh` — returned fixture source comparing two contained pipelines; not fixture execution.
6. `rmdir /fast/scratch/hyaku/mado-r84/R84ScribeEntry` — completed with no output; empty scratch removed, no receipts generated there.

## Touched surfaces and limits

Only durable write: `.ufo/waves/round-84/w1/R84ScribeEntry.md` (this report). No production, registry, lesson, fleet, sibling, git-index or jj-state writes. No credentials, raw sessions, r56 artifacts, compositor/service/config mutation, screenshots, input capture, or real identifying values are included. No tools were installed or upgraded; host tooling rules were read and the pacman pause respected.

Domain-share accounting: C1 concerns the lane's model input grammar; C2 concerns runbook pipeline-status semantics. Neither supplies new live tray-health evidence. Drafts are intentionally report-only; integration and canonical judgment remain outside this seat.

Self-evaluation: accuracy 4/5 (fetched-source hashes not independently validated); completeness 4/5 (candidate outcomes deliberately unavailable to this scribe-only evidence set); clarity 4/5 (dense paths retained for audit); actionability 4/5 (integration still belongs to planner); conciseness 4/5 (command ledger adds length required for provenance). Mean 4.0/5. Highest-impact improvement at integration: attach actual revision-bound candidate and guarded-fixture receipts without rewriting these historical baseline outcomes. The user should agree that these limits are explicit rather than passes implied.
