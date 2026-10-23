# CapArtifactOnlyAssessmentIn1464 — C2 row re-run: SCORECARD.md:1464 at `41cc04c8`

Leaf executor, mado round 25 attempt 3, wave `a3w1` (PRE-DATA). Assigned item: C2 capability-row re-run under the
C2 row contract. Read-only against the lane; the only file written is this report. No lane/fleet `git`/`jj` write
command was issued (sandbox clone only, `GIT_DIR`/`GIT_WORK_TREE`/`GIT_INDEX_FILE` unset). No `hyprctl` call, no
package/service/compositor change, nothing installed. Every process started has finished; the sandbox clone was
deleted (see §G).

## A. The row

- Location: `SCORECARD.md:1464` at base `41cc04c8d593837a0d5078bffaacdaa163d12897`, table header `:1462`
  (`| Capability | What it can now do | Evidence pointer | First-working round |`) under the heading
  `### Capabilities demonstrated this round` (`:1460`, round 21).
- Capability: `artifact-only assessment integrity`.
- Stated claim (row cells, quote): "Validate declared chronology/order, actual input/expectation hashes, historical
  rejection disclosure and the four canonical SHONEN subjects, without a C1 dependency; distinguish
  clean/failed/could-not-evaluate, not authenticate identities or prove evidence sufficiency". First-working round:
  `21`.
- Demonstration command (row): `python3 -I tools/mado-assessment.py --selftest .ufo/waves/round-21/assessment-fixtures`.
- Evidence pointer (row): the same `--selftest` command, plus "same C2 output under three C1 intervention states and
  killed digest-check mutant, receipts above" — i.e. the round-21 final receipts
  `.ufo/waves/round-21/evidence/final/assessment-{delivered,independence,mutation,na}-a6cef89.json`.

## B. Sandbox and revision

```
mkdir -p /fast/scratch/hyaku/mado-r25a3/c2
env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git clone -q /home/vgpnk/Projects/shokunin/mado-shokunin \
  /fast/scratch/hyaku/mado-r25a3/c2/CapArtifactOnlyAssessmentIn1464
env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git -C /fast/scratch/hyaku/mado-r25a3/c2/CapArtifactOnlyAssessmentIn1464 \
  checkout -q --detach 41cc04c8
git -C ... rev-parse HEAD            -> 41cc04c8d593837a0d5078bffaacdaa163d12897
git -C ... status --porcelain        -> (empty)
sha256sum tools/mado-assessment.py   -> 66aefd03f25d834fbfcfee6b295c1c032f01b2a94ca321396b7558cca59de9d4
```

The tool's bytes at `41cc04c8` are the same sha256 the round-21 measurement recorded (`SCORECARD.md:1446`), and the
independence receipt names the same `gate_sha256`. The four evidence-pointer receipts named in §A all exist at
`41cc04c8` (`git cat-file -e` present for all four).

## C. Re-run

Command as executed (the row's command, under the contract wrappers `timeout 600` and
`prlimit --as=4000000000`), in the sandbox clone at `41cc04c8`:

```
timeout 600 prlimit --as=4000000000 python3 -I tools/mado-assessment.py --selftest .ufo/waves/round-21/assessment-fixtures
```

Run 1 (`> selftest-out.txt`): `exit=0`, stdout 9,225 bytes / 1 line, stderr 0 bytes.
Run 2 (`> selftest-out2.txt`): `exit=0`, wall 0.984 s, stdout 9,225 bytes / 1 line, stderr 0 bytes.
Both stdout files are byte-identical: `sha256:1e58c91ba5a5f6c84f4e2619cab4453b691604d38bdef1465a5def86c11ede98`.
An earlier un-captured run also printed `exit=0` with the same visible head (stdout was too long for the display
capture; it was not hashed).

### Verbatim stdout (single 9,225-byte line, exactly as printed; `exit=0`)

```
{"cases": [{"exit": 0, "got": {"actual_expectations_sha256": "aa691e53f2771a79a7fa185fb56a0b949f7893b129e4fd8eaecd108c02f33a5e", "actual_inputs": [{"path": "snapshots/population-baseline.txt", "sha256": "16e14eaa77f0094660d269b88208e56df589b30c8cada50ee04a9dba7d4d07ed"}], "authority": "artifact assertions only; no authenticated chronology, authorship, semantic proof or promotion authority", "code": 0, "finding_ids": ["assessment_clean"], "result": "clean"}, "id": "baseline_valid", "pass": true, "want": {"code": 0, "result": "clean"}}, {"exit": 1, "got": {"actual_expectations_sha256": "aa691e53f2771a79a7fa185fb56a0b949f7893b129e4fd8eaecd108c02f33a5e", "actual_inputs": [{"path": "snapshots/population-baseline.txt", "sha256": "16e14eaa77f0094660d269b88208e56df589b30c8cada50ee04a9dba7d4d07ed"}], "authority": "artifact assertions only; no authenticated chronology, authorship, semantic proof or promotion authority", "code": 1, "finding_ids": ["late_registration"], "result": "failed"}, "id": "late_registration_after_measurement", "pass": true, "want": {"code": 1, "result": "failed"}}, {"exit": 1, "got": {"actual_expectations_sha256": "aa691e53f2771a79a7fa185fb56a0b949f7893b129e4fd8eaecd108c02f33a5e", "actual_inputs": [{"path": "snapshots/population-baseline.txt", "sha256": "16e14eaa77f0094660d269b88208e56df589b30c8cada50ee04a9dba7d4d07ed"}], "authority": "artifact assertions only; no authenticated chronology, authorship, semantic proof or promotion authority", "code": 1, "finding_ids": ["late_registration"], "result": "failed"}, "id": "late_registration_after_implementation", "pass": true, "want": {"code": 1, "result": "failed"}}, {"exit": 1, "got": {"actual_expectations_sha256": "aa691e53f2771a79a7fa185fb56a0b949f7893b129e4fd8eaecd108c02f33a5e", "actual_inputs": [{"path": "snapshots/population-mutated.txt", "sha256": "c02069a203b8c1306e61b8470c8fe916e08fd5db23fd433c95b6f87ed82e84fc"}], "authority": "artifact assertions only; no authenticated chronology, authorship, semantic proof or promotion authority", "code": 1, "finding_ids": ["population_digest_changed"], "result": "failed"}, "id": "population_file_mutated", "pass": true, "want": {"code": 1, "result": "failed"}}, {"exit": 2, "got": {"code": 2, "error": "missing or invalid sha256", "finding_ids": ["assessment_input_invalid"], "result": "could-not-evaluate"}, "id": "missing_registered_input_sha256", "pass": true, "want": {"code": 2, "result": "could-not-evaluate"}}, {"exit": 1, "got": {"actual_expectations_sha256": "aa691e53f2771a79a7fa185fb56a0b949f7893b129e4fd8eaecd108c02f33a5e", "actual_inputs": [{"path": "snapshots/population-baseline.txt", "sha256": "16e14eaa77f0094660d269b88208e56df589b30c8cada50ee04a9dba7d4d07ed"}], "authority": "artifact assertions only; no authenticated chronology, authorship, semantic proof or promotion authority", "code": 1, "finding_ids": ["oracle_not_independent"], "result": "failed"}, "id": "oracle_tool_generated_not_independent", "pass": true, "want": {"code": 1, "result": "failed"}}, {"exit": 1, "got": {"actual_expectations_sha256": "aa691e53f2771a79a7fa185fb56a0b949f7893b129e4fd8eaecd108c02f33a5e", "actual_inputs": [{"path": "snapshots/population-baseline.txt", "sha256": "16e14eaa77f0094660d269b88208e56df589b30c8cada50ee04a9dba7d4d07ed"}], "authority": "artifact assertions only; no authenticated chronology, authorship, semantic proof or promotion authority", "code": 1, "finding_ids": ["expectations_changed"], "result": "failed"}, "id": "expectation_digest_changed", "pass": true, "want": {"code": 1, "result": "failed"}}, {"exit": 2, "got": {"code": 2, "error": "canonical four-box assessment incomplete", "finding_ids": ["assessment_input_invalid"], "result": "could-not-evaluate"}, "id": "shonen_missing_box", "pass": true, "want": {"code": 2, "result": "could-not-evaluate"}}, {"exit": 2, "got": {"code": 2, "error": "canonical four-box assessment incomplete", "finding_ids": ["assessment_input_invalid"], "result": "could-not-evaluate"}, "id": "shonen_duplicate_box", "pass": true, "want": {"code": 2, "result": "could-not-evaluate"}}, {"exit": 1, "got": {"actual_expectations_sha256": "aa691e53f2771a79a7fa185fb56a0b949f7893b129e4fd8eaecd108c02f33a5e", "actual_inputs": [{"path": "snapshots/population-baseline.txt", "sha256": "16e14eaa77f0094660d269b88208e56df589b30c8cada50ee04a9dba7d4d07ed"}], "authority": "artifact assertions only; no authenticated chronology, authorship, semantic proof or promotion authority", "code": 1, "finding_ids": ["unnamed_nonauthor_verifier"], "result": "failed"}, "id": "shonen_x_without_nonauthor", "pass": true, "want": {"code": 1, "result": "failed"}}, {"exit": 2, "got": {"code": 2, "error": "empty assessment evidence", "finding_ids": ["assessment_input_invalid"], "result": "could-not-evaluate"}, "id": "shonen_empty_evidence", "pass": true, "want": {"code": 2, "result": "could-not-evaluate"}}, {"exit": 1, "got": {"actual_expectations_sha256": "aa691e53f2771a79a7fa185fb56a0b949f7893b129e4fd8eaecd108c02f33a5e", "actual_inputs": [{"path": "snapshots/population-baseline.txt", "sha256": "16e14eaa77f0094660d269b88208e56df589b30c8cada50ee04a9dba7d4d07ed"}], "authority": "artifact assertions only; no authenticated chronology, authorship, semantic proof or promotion authority", "code": 1, "finding_ids": ["historical_target_rewritten"], "result": "failed"}, "id": "history_suppresses_old_three_misses", "pass": true, "want": {"code": 1, "result": "failed"}}, {"exit": 1, "got": {"actual_expectations_sha256": "aa691e53f2771a79a7fa185fb56a0b949f7893b129e4fd8eaecd108c02f33a5e", "actual_inputs": [{"path": "snapshots/population-baseline.txt", "sha256": "16e14eaa77f0094660d269b88208e56df589b30c8cada50ee04a9dba7d4d07ed"}], "authority": "artifact assertions only; no authenticated chronology, authorship, semantic proof or promotion authority", "code": 1, "finding_ids": ["historical_target_rewritten"], "result": "failed"}, "id": "history_round20_admitted_true", "pass": true, "want": {"code": 1, "result": "failed"}}, {"exit": 1, "got": {"actual_expectations_sha256": "aa691e53f2771a79a7fa185fb56a0b949f7893b129e4fd8eaecd108c02f33a5e", "actual_inputs": [{"path": "snapshots/population-baseline.txt", "sha256": "16e14eaa77f0094660d269b88208e56df589b30c8cada50ee04a9dba7d4d07ed"}], "authority": "artifact assertions only; no authenticated chronology, authorship, semantic proof or promotion authority", "code": 1, "finding_ids": ["historical_target_rewritten"], "result": "failed"}, "id": "history_c2_independent_true", "pass": true, "want": {"code": 1, "result": "failed"}}, {"exit": 2, "got": {"code": 2, "error": "month must be in 1..12, not 19", "finding_ids": ["assessment_input_invalid"], "result": "could-not-evaluate"}, "id": "malformed_timestamp", "pass": true, "want": {"code": 2, "result": "could-not-evaluate"}}, {"exit": 2, "got": {"code": 2, "error": "empty or oversized population/measurements", "finding_ids": ["assessment_input_invalid"], "result": "could-not-evaluate"}, "id": "population_empty", "pass": true, "want": {"code": 2, "result": "could-not-evaluate"}}, {"exit": 2, "got": {"code": 2, "error": "missing or invalid author", "finding_ids": ["assessment_input_invalid"], "result": "could-not-evaluate"}, "id": "oracle_author_missing", "pass": true, "want": {"code": 2, "result": "could-not-evaluate"}}, {"exit": 0, "got": {"actual_expectations_sha256": "aa691e53f2771a79a7fa185fb56a0b949f7893b129e4fd8eaecd108c02f33a5e", "actual_inputs": [{"path": "snapshots/population-baseline.txt", "sha256": "16e14eaa77f0094660d269b88208e56df589b30c8cada50ee04a9dba7d4d07ed"}], "authority": "artifact assertions only; no authenticated chronology, authorship, semantic proof or promotion authority", "code": 0, "finding_ids": ["assessment_clean"], "result": "clean"}, "id": "shonen_x_with_named_nonauthor", "pass": true, "want": {"code": 0, "result": "clean"}}, {"exit": 1, "got": {"actual_expectations_sha256": "aa691e53f2771a79a7fa185fb56a0b949f7893b129e4fd8eaecd108c02f33a5e", "actual_inputs": [{"path": "snapshots/population-baseline.txt", "sha256": "16e14eaa77f0094660d269b88208e56df589b30c8cada50ee04a9dba7d4d07ed"}], "authority": "artifact assertions only; no authenticated chronology, authorship, semantic proof or promotion authority", "code": 1, "finding_ids": ["wrong_topic_shonen"], "result": "failed"}, "id": "round20_wrong_topic_shonen", "pass": true, "want": {"code": 1, "result": "failed"}}, {"exit": 0, "got": {"actual_expectations_sha256": "aa691e53f2771a79a7fa185fb56a0b949f7893b129e4fd8eaecd108c02f33a5e", "actual_inputs": [{"path": "snapshots/population-baseline.txt", "sha256": "16e14eaa77f0094660d269b88208e56df589b30c8cada50ee04a9dba7d4d07ed"}], "authority": "artifact assertions only; no authenticated chronology, authorship, semantic proof or promotion authority", "code": 0, "finding_ids": ["assessment_clean"], "result": "clean"}, "id": "round20_canonical_shonen_corrected", "pass": true, "want": {"code": 0, "result": "clean"}}], "code": 0, "finding_ids": ["assessment_oracle_match"], "pass": 20, "result": "selftest", "seal_sha256": "99516c349637f2aefaef5c106ec7973c8af638bd4a22c79c835a49e0559fe686", "tool_sha256": "66aefd03f25d834fbfcfee6b295c1c032f01b2a94ca321396b7558cca59de9d4", "total": 20}
exit=0
```

### Derived per-case view (same bytes, re-rendered for width — not additional evidence)

Top level: `code=0`, `result=selftest`, `pass=20`, `total=20`, `finding_ids=["assessment_oracle_match"]`,
`tool_sha256=66aefd03…`, `seal_sha256=99516c34…`. All 20 cases `pass=true`; three result classes are exercised
(3 `clean`, 9 `failed`, 8 `could-not-evaluate` at the `want` level; `got` matches `want` in every case).

| case | exit | result | finding |
|---|---|---|---|
| baseline_valid | 0 | clean | assessment_clean |
| late_registration_after_measurement | 1 | failed | late_registration |
| late_registration_after_implementation | 1 | failed | late_registration |
| population_file_mutated | 1 | failed | population_digest_changed |
| missing_registered_input_sha256 | 2 | could-not-evaluate | assessment_input_invalid |
| oracle_tool_generated_not_independent | 1 | failed | oracle_not_independent |
| expectation_digest_changed | 1 | failed | expectations_changed |
| shonen_missing_box | 2 | could-not-evaluate | assessment_input_invalid |
| shonen_duplicate_box | 2 | could-not-evaluate | assessment_input_invalid |
| shonen_x_without_nonauthor | 1 | failed | unnamed_nonauthor_verifier |
| shonen_empty_evidence | 2 | could-not-evaluate | assessment_input_invalid |
| history_suppresses_old_three_misses | 1 | failed | historical_target_rewritten |
| history_round20_admitted_true | 1 | failed | historical_target_rewritten |
| history_c2_independent_true | 1 | failed | historical_target_rewritten |
| malformed_timestamp | 2 | could-not-evaluate | assessment_input_invalid |
| population_empty | 2 | could-not-evaluate | assessment_input_invalid |
| oracle_author_missing | 2 | could-not-evaluate | assessment_input_invalid |
| shonen_x_with_named_nonauthor | 0 | clean | assessment_clean |
| round20_wrong_topic_shonen | 1 | failed | wrong_topic_shonen |
| round20_canonical_shonen_corrected | 0 | clean | assessment_clean |

The row's stated behaviors are visible in the run: chronology (`late_registration_*`), input/expectation hashes
(`population_file_mutated`, `expectation_digest_changed`, `missing_registered_input_sha256`), historical rejection
disclosure (`history_*`), the four canonical SHONEN subjects (`shonen_*`, `round20_*_shonen`), and the three-state
distinction (`clean` / `failed` / `could-not-evaluate`). The run does not re-execute the round-21 independence and
mutation runners; their receipts exist at `41cc04c8` (§B) and name `gate_sha256` equal to the tool bytes measured here.

## D. SCORECARD-wide grep for later rows or text that supersede or contradict this row

Grepped `git show 41cc04c8:SCORECARD.md` for `assessment` (case-insensitive) and read the round-24 section and the
round-21 residual disposition. Every hit:

- `:1440` round-21 registration bullet: describes the same capability; not a later row.
- `:1446` round-21 measured facts: tool sha256 (matches; measured code).
- `:1452` round-21 `C2 calibration / artifact-assessment capability` counted row: before 0 → after 1 demonstrated
  gate; consistent, earlier than `:1464`.
- `:1464` the row under test.
- `:1472` `**C2: improved as a separately demonstrated, bounded capability; round admission remains false.**` — a
  later (later in the same round-21 report) disposition that bounds *admission*, not the demonstrated behavior; it
  restates 20/20 fixture verdicts and the C1-intervention equality. It does not contradict the row's technical claim,
  and the row itself already disclaims authentication/sufficiency.
- `:1586` round-24 capability status table: `| artifact-only assessment integrity | works | mado-assessment.py
  --selftest: pass = total, exit 0 at 8e5d9369 |` — a later re-demonstration that agrees with this re-run.
- `:1570` "This table supersedes the implied `works` of every earlier row; the earlier rows stay as written." — makes
  `:1586` the operative present-tense status for this capability.
- `:1588-1600` wave-2 scope correction to the round-24 table: the frozen 12-row C2 population is heading-scoped; this
  capability is one of the 12 and stays `works`. No contradiction.
- Unrelated generic uses at `:50`, `:762`, `:1474` (a seat name `FinalAssessmentReview`).

No later text reports this capability as failing, absent, removed or renamed, and no later row supersedes it other
than `:1586`/`:1570` re-affirming `works`. Observed status: **works**.

## E. Ledger line

| SCORECARD.md:1464 | artifact-only assessment integrity | Validate declared chronology, input/expectation hashes, rejection disclosure and four canonical SHONEN subjects without C1; distinguish clean/failed/could-not-evaluate | observed at 41cc04c8: works — exit 0, pass=20 total=20 code=0 result=selftest finding_ids=["assessment_oracle_match"], stdout 9,225 B sha256:1e58c91b…1ede98, two runs byte-identical, wall 0.984 s | cd /fast/scratch/hyaku/mado-r25a3/c2/CapArtifactOnlyAssessmentIn1464 && timeout 600 prlimit --as=4000000000 python3 -I tools/mado-assessment.py --selftest .ufo/waves/round-21/assessment-fixtures | SCORECARD.md:1586 (round-24 status table, works at 8e5d9369; :1570 declares it supersedes earlier implied works); :1472 bounds it to bounded, not admitted |

## F. What this re-run does not show

- It re-runs the fixture selftest only; it does not prove semantic sufficiency or authenticated chronology (the row
  says so explicitly). It does not re-run the independence/mutation runners; those receipts are present and
  hash-consistent but were not re-executed here.
- It says nothing about the current tip `1ed41fa8` except that the tool file still exists; the assigned base is
  `41cc04c8`.
- The fixture population is the round-21 one; nothing here re-derives it.

## G. Cleanup and process check

```
rm -rf /fast/scratch/hyaku/mado-r25a3/c2/CapArtifactOnlyAssessmentIn1464
ls /fast/scratch/hyaku/mado-r25a3/c2   -> (removed; see run log below)
pgrep -af "capartifactonlyassessmentin1464|mado-assessment" -> no match
```

The clone `CapArtifactOnlyAssessmentIn1464` is deleted; `pgrep` finds no matching process. Residual scratch retained
outside the lane: the two captured stdout files `selftest-out.txt` and `selftest-out2.txt` (9,225 B each,
`sha256:1e58c91b…1ede98`) under `/fast/scratch/hyaku/mado-r25a3/c2/` (that directory is shared with sibling Cap
seats' clones, which are theirs, not mine), plus the embedded verbatim stdout in §C. A first attempt to time the run
with `/usr/bin/time` failed (`error: command not found: /usr/bin/time`, exit 127, nothing executed); that attempt's
empty redirect file `selftest-time.txt` was removed, and timing was taken with `date +%s.%N` instead. None of the
retained files is a lane file or holds credentials.

## H. Risks and blockers

- None blocking. The row's claim holds at the assigned base under the documented command.
- Risk carried by the row itself (unchanged): the `works` status is a fixture-suite fact, not proof of semantic
  assessment integrity; the round-24 wave-2 correction and the round-21 residual disposition both say the same.
- Minor: the row's evidence pointer cites round-21 receipts, which are present and hash-consistent but not re-executed
  here; a later C2 row re-run that wants independence/mutation evidence should execute
  `.ufo/waves/round-21/assessment-{independence,mutation}.py` explicitly.
