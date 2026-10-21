# RegistrationAudit — chronological evidence and C2 baseline review

**Axes:** chronology/provenance; C2 fail-closed calibration; scope/evidence honesty.

## Findings

### Registration chronology — consistent with preregistration, not authenticated

The round-22 registration names base `741122d177ae8ff68a73768777f20484d5bdcbe4` and declares that proposals freeze before implementation (`registration.md:3,5-13`). The observed registration commit `a963ce67e303db94201507a93018416e4e44fd23` records author time `2026-10-21T11:18:17-03:00` and committer time `2026-10-21T11:18:18-03:00`; it adds `registration.md`, `audit-contract.json`, and `w1-spec.json` and modifies `SCORECARD.md`. Two other observed registration commits (`387fba0eee40cbaac10ac735d2b0fa9b3c436e26`, `5471d9e2ff4c1e685636f5e8fbc5dae2649a7c09`) show the same additions at `11:18:17-03:00`.

The all-ref history for `tools/mado-tripwire.py` has no post-registration round-22 production edit. Its last observed path commit is round-21 commit `a6cef8984d3815775587ab634ce558e13338b0eb` (author/committer time `2026-10-21T06:37:21-03:00`). The latest observed commit `80506328d5e46079261d39c0e1e19b8ede0d7c89` has parent `a963ce67e303db94201507a93018416e4e44fd23` and no changed paths. Thus the observed history is consistent with registration before any round-22 production implementation, but there is no later implementation commit to compare against. The registration postdates the round-21 implementation.

These are Git author/committer timestamp assertions, not authenticated timestamps or proof of author identity, prior knowledge, or when the bytes were first written. I did not inspect index/worktree state; uncommitted or earlier hidden implementation cannot be excluded.

### C2 — strong fail-closed contract, unresolved historical baseline representation

`audit-contract.json` specifies exact integer/bool claims, exact snapshot SHA-256, nonempty file population, finding-row evidence `observed|lead`, nonempty class/command, summed `eval_unparsed`/`unparsed_spawns`, and `clean:true` only with no findings and zero errors. Missing/invalid evidence is uncertainty, not observed. It also explicitly invalidates duplicate JSON keys, malformed JSON, booleans-as-counts, negative counts, nonfinite numbers, path escapes/symlinks, and snapshots over 2 MiB (`audit-contract.json:5-10`). This is a good contract boundary: an unconditional-green audit must not satisfy the registered invalid fixtures or mutant-kill gate.

The retained actual r19 receipts do not have that schema:

- `.ufo/waves/round-19/evidence/final/tw-recall-after.txt` (SHA-256 `8ff13d23d3ffeab946a301a3457360edc3abf52ea833611ac2a0d6dba48ec1c1`) and `.ufo/waves/round-19/evidence/harm/harm-tw-recall.txt` (SHA-256 `6cbdd4949d30dc0f65e6f4a22a64406fe22ae7cd0bbce5ae1083b5856f55247d`) each contain six incident-line rows with `file`, `line`, and `detected:true`, but no `class`, `command`, or evidence tier. They refer to different measured commits (`7b4839d…` and `01b8094…`), so the intended canonical C3 source also needs to be stated.
- `.ufo/waves/round-19/frozen/expected.json` (SHA-256 `50d2a45e2602cb430b94043f6c658204b0b1802e8c1931cb2a3eda167af02435`) has eleven `expected_findings` rows with `file`, `line`, `class`, and `rule`, but no `command` or evidence tier. `RerunC3.md:41-55` enumerates the eleven scan rows; `CriticC3W2.md:23-32,151-157` explains the six incident-line result as five non-guessing detections and one lead heuristic.

**Unresolved C2 acceptance ambiguity:** “five observed plus one lead” counts the six incident lines, while the audit contract compares counts against finding rows and the historical scan inventory has eleven rows. The six-row receipts also lack explicit evidence markers. Do not collapse eleven findings into six rows or silently label raw `detected:true` as observed. Preserve the historical receipt bytes/digest and use a separately identified, digest-bound mapping if that is the intended test input; define whether claims count incidents or finding rows. Until then, a C2 green is not established. On the raw unmarked receipt, the contract's missing-marker rule calls for uncertainty (code 2) unless a separate mapping establishes the evidence tier. If “red” specifically means code 1, rather than any non-green result, registration must state how a contradiction is distinguishable from missing evidence. A false all-observed claim must not pass on the same fixed population; correct 5/1 scope may be green only after the counting grain and mapping are fixed.

No C2 auditor, proposal, baseline execution, fixture result, or mutant-kill result was reviewed or run. The notes directory had no files when inspected. The contract's requirements are not execution evidence.

## Work performed and gates

Read the round-22 registration, audit contract, work specification, round-21 binding review, and cited r19 receipts/reviews. Read-only Git history commands:

- `git log --all --format='%H%x09%aI%x09%cI%x09%s' -- .ufo/waves/round-22/registration.md .ufo/waves/round-22/audit-contract.json .ufo/waves/round-22/w1`
- `git show --format=fuller --stat --name-status a963ce67e303db94201507a93018416e4e44fd23 && git show --format=fuller --stat --name-status 387fba0eee40cbaac10ac735d2b0fa9b3c436e26 && git show --format=fuller --stat --name-status 5471d9e2ff4c1e685636f5e8fbc5dae2649a7c09`
- `git log --all --date-order -n 40 --format='%H%x09%aI%x09%cI%x09%s'`
- `git show --format=raw --stat --name-status 80506328d5e46079261d39c0e1e19b8ede0d7c89 && git show --format=raw --stat --name-status 27380477ff1e9811283f5a5143b38018c9930f75 && git log --all --format='%H%x09%aI%x09%cI%x09%s' -- tools/mado-tripwire.py`
- `sha256sum .ufo/waves/round-22/registration.md .ufo/waves/round-22/audit-contract.json .ufo/waves/round-19/evidence/final/tw-recall-after.txt .ufo/waves/round-19/evidence/harm/harm-tw-recall.txt .ufo/waves/round-19/frozen/expected.json`

Outcomes are recorded above and in the JSON notes. No production edits, detector measurements, payload execution, tests/builds/linters/formatters/smokes, package queries, installs, or shared `lesson`/`SOURCES`/`LOG` changes. No runtime or artifact baseline was executed.

## Affected surfaces and limits

Only this seat's audit notes and report were authored. No product code or shared records changed. No installations. Exact unresolved items: the canonical r19 C3 receipt, the C2 count grain (six incident rows vs eleven finding rows), the red-code interpretation on unmarked raw rows, and whether any uncommitted implementation exists.

Report: `.ufo/waves/round-22/w1/reports/RegistrationAudit.md`
