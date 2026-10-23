# ScribeSkillRegistry report

## Outcome

Drafted six SKILL gate-registry rows using the existing eight-column header. The three round-27 rows are explicitly marked **lands this round, pending**; their contract-derived commands and verdicts are not execution evidence. `SKILL.md` and all gate/product files were left unchanged.

## Registry shape and provenance

The requested registry search found the exact header at `SKILL.md:600-601`: `name`, `gate/probe`, `entry command`, `verdict map`, `self-test command / spelling`, `pinned-value path`, `write scope`, `owner`. Its adjacent note says commands run from the lane root (`SKILL.md:595-598`). The draft copies those columns without adding a status column.

The round-27 registration states that C2 is intended to gate two offline suites, with 8/8 green runs, all 15 W mutants killed, and held-out kill/validity thresholds (`.ufo/waves/round-27/registration.md:30-50`). The separate routed Q36 task requires a `.md` and `.txt` receipt glob, per-shape `--seeds N`, strict chronology, and red/green evidence at `.ufo/waves/round-27/quality/q36-successor-receipts.txt` (`.ufo/waves/round-27/w1-run.json`, item `ExecQ36Repair`). Those are contracts, not observed outcomes.

## Evidence and findings recorded

- Round-26 counter self-test: `quality/counter-selftest-green.txt` records `SELFTEST pass=9 total=9`, exit 0, against its pinned C1-v1 and C2 counters. `counter-selftest-red.txt` records mutated-copy failures. M26-8 later found 6/10 self-test mutants survived and the active C1-v2 pristine compatibility check failed 7/9; the defect details are in `.ufo/waves/round-26/w2/reports/MutSelftest.md`.
- Round-26 population checker: `quality/q37-population-red-green.txt` records the synthetic 41-case green, mismatch reds, real before-receipts, and unreadable-input exit 2. M26-8 found that the five committed population fixtures missed 3/6 mutants; survivors were CASE-anywhere, first-PRED-only, and parse-error exit 0 (`.ufo/waves/round-26/w2/reports/MutQ37.md`).
- Round-26 control-receipt checker: `quality/q36-mutants.txt` records `Q36MUTANTS killed=8/8 fixtures=10` and legacy parity. M26-8 also records that this checker only considered `.md` controls, so round-26 `.txt` receipts were excluded and the gate failed (`corpus/lessons/round-26.md`, M26-8 row). The round-27 successor task is the contract to address the extension and seed-count defect.
- At drafting time, no round-27 quality-suite source or result receipt was present. The R27 rows therefore identify their contract source and predecessor evidence, state pending pins/write details where not yet specified, and avoid implying a run.

## Commands and execution status

No gate, self-test, build, mutation runner, shell command, git/jj command, or host probe was run for this documentation assignment. Existing receipts above were read as evidence and were not regenerated.

The registry-shape inspection used the repository regex-search tool on `SKILL.md` with pattern `registry|Gate standard`; the observed header is at lines 600-601. Additional source reads covered the round-27 registration and Q36 task, round-26 gate sources, and the cited round-26 reports/receipts. Commands appearing in the draft are registry entries (or explicitly provisional contract commands), not commands executed by this seat.

## Touched surfaces and limits

Created only:

- `.ufo/waves/round-27/drafts/skill-registry.md` — six prose registry rows, with all R27 successors marked pending.
- `.ufo/waves/round-27/w1/reports/ScribeSkillRegistry.md` — this report.

No package/tool was installed or updated. No runtime or gate verdict was produced. R27 commands, exit details, pins, and write scopes for the unlanded suites/checker still require confirmation from their landed implementations and receipts before these draft rows are promoted into `SKILL.md`.
