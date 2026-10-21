# GateRound20WrongTopicShonen — C2 assessment

## Verdict

The frozen round-20 transcription is correctly rejected by the current gate as a wrong-topic assessment. The result is deterministic for the exact fixture. However, a nearby non-proving variant passes as `clean`: the gate's SHONEN test is lexical topic-presence, not evidence validation. Therefore the rejection is robust for these four exact rows, but a clean result must not be read as proof that the underlying promotion criteria were satisfied.

C2 has no C1 classifier/result dependency in the examined `--check` path.

## Evidence

- Observed lane HEAD: `f499a8db7171b7476fe9f204ab9edbac5a956fa9`.
- Tested production bytes: `/home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-assessment.py`, SHA-256 `5101c317d521c4df9c55ed2c909c2feacb0f5fbe9662f46ce91dbdd04f7c20e7`.
- Frozen fixture: `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-21/assessment-fixtures/cases/round20_wrong_topic_shonen.json`, SHA-256 `e3170afabef6593d87a373fd4daabca3cc78259093a2e83bc8ec804753521d36`.
- `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-21/assessment-fixtures/expected.json` hashes to `aa691e53f2771a79a7fa185fb56a0b949f7893b129e4fd8eaecd108c02f33a5e`, matching the fixture's registered/current expectation digests. The population file at `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-21/assessment-fixtures/snapshots/population-baseline.txt` hashes from its actual bytes to `16e14eaa77f0094660d269b88208e56df589b30c8cada50ee04a9dba7d4d07ed`, matching the fixture's declared digest.
- The frozen oracle expects code `1`, result `failed` for this case and describes the four rows as claims/receipts, no-harm, sources, and mistakes rather than the canonical promotion boxes (`/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-21/assessment-fixtures/expected.json:170-179`). The actual SHONEN text I inspected matched the four transcribed rows.
- In `mado-assessment.py`, `SUBJECTS` defines the canonical texts (lines 20-25); `check` appends `wrong_topic_shonen` when the exact subject substring is absent (lines 142-144). The expected finding map contains `round20_wrong_topic_shonen` → `wrong_topic_shonen` (lines 181-186).

## Bounded runs

Python 3.14.8; production tool bytes above. I copied only the frozen case, `expected.json`, and the baseline population file into a private temporary root—no C1 result/corpus artifacts or other lane data.

- Frozen fixture, run twice: each process exit `1`; JSON `code: 1`, `result: "failed"`, `finding_ids: ["wrong_topic_shonen"]`. The process exit agreed with JSON code on both runs, and the output identity was stable. Actual expectation/population digests in the output matched the byte hashes above.
- One altered artifact: a nearby four-row variant whose evidence strings mention each exact canonical subject but explicitly say the subject is merely declared and unproved (e.g. source not opened/no execution). Variant SHA-256 `fa992ee4be8339c8bc6175846864364050379a8aeb328e81c2a4c1fd341a1495`. Process exit `0`; JSON `code: 0`, `result: "clean"`, `finding_ids: ["assessment_clean"]`; exit agrees with JSON code. This is a semantic false-positive acceptance for evidence sufficiency, not a false classification of the original transcript's absent topic strings. It follows the implementation's explicit comment that this check tests the declared subject, not whether evidence proves it.

## C1 independence and limits

Static inspection: the tool imports only standard-library modules; the `--check` call goes through `evaluate`/`check` and reads the supplied JSON and rooted files. The only `subprocess.run` is in `selftest` (lines 190-191), where it re-invokes this assessment tool for fixture cases; it is not on the exercised `--check` path. The minimal-root run also succeeded without any C1 artifact, classifier, scanner result, or corpus input. This supports no C1 dependency for this C2 result.

Timestamp values and oracle author/independence fields are fixture assertions; the tool does not authenticate chronology or authorship. Likewise, any named-verifier syntax is only an assertion, not authenticated identity. The case uses `~` marks, and neither this result nor the variant establishes that any promotion claim is true. No full selftest or corpus/suite was run; no tools were installed.

Report: `.ufo/waves/round-21/w2/reports/GateRound20WrongTopicShonen.md`
