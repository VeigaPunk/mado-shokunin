# ResourceCli — CLI stack reservation and deep parser coverage

## Axes

- **Deep-input coverage:** can the CLI still parse deep Python transcript cells supported by the previous stack reservation?
- **Verdict integrity:** does an unparsed cell get reported as clean?
- **Operability:** does the smaller reservation help fit under the 384 MiB address-space cap?

## Verdict

**64 MiB is not established as no-harm.** On the current candidate, an existing 5,000-level nested-call fixture returns `clean`/exit 0 with `eval_unparsed: 1`. The verdict path ignores that counter. This is direct evidence that this deep cell is unparsed while the top-level verdict remains clean. Historical 512 MiB-era results report the same fixture as clean, but their runner discarded `eval_unparsed`; therefore I cannot establish from those records whether this is a regression caused by the reservation change or whether the prior clean result also carried an unparsed count. Retain that comparison as unresolved rather than claiming either equivalence or a proven stack-only regression.

## Evidence

- Tested candidate: commit `f499a8db7171b7476fe9f204ab9edbac5a956fa9` (current candidate identity supplied by L1); exact tested scanner SHA-256 `2e152f6dcd9a0d13ffc1d64e88bcc600548e66bd04c34f92dbc5a0808338372d`. The scanner SHA was unchanged on the post-probe read.
- Current source sets `STACK_BYTES = 64 * 1024 * 1024` and `RECURSION_LIMIT = 50000` (`tools/mado-tripwire.py:3111-3112`). The captured pre-change scanner snapshot sets `STACK_BYTES = 512 * 1024 * 1024` (`.ufo/waves/round-21/evidence/tool-before.py:2890`).
- One bounded scanner-only CLI probe used the existing `.ufo/waves/round-20/w2/AdvCrash/fixtures/deep_call_chain_5k.jsonl` fixture (SHA-256 `7042b281042a38718494c4c227851f577fe713aece3fad599659094757ac7699`) through `.ufo/waves/round-21/oracle/measure.py`'s `scan` API: one isolated child, 384 MiB `RLIMIT_AS`, 15-second timeout. The tool returned exit 0, `MADO_TRIPWIRE: clean`, `eval_unparsed: 1`, `findings: []`, and empty stderr. The probe did not execute fixture code.
- The fixture is a 5,000-deep nested Python call expression, not a shell command. Its generator records that shape in `AdvCrash/gen.py:121-124`. In the current scanner, `classify_eval` catches compile exceptions as `eval_unparsed` (`tools/mado-tripwire.py:2028-2033`), while `verdict_of` bases `clean` solely on findings (`:2604-2609`). The exact exception was not included in the probe payload, so attributing the unparsed count to stack exhaustion is an inference, not a directly observed exception.
- Existing historical results say both old revisions `28c6837` and `1f7f995` returned exit 0/clean on this fixture (`AdvCrash/results/scan-per-file.json:393-405`). The historical runner only recorded exit, label, error, and stderr (`AdvCrash/run.py:21-32`), not `eval_unparsed`; it cannot establish parser success. A separate historical report states those runs used a 512 MiB stack reservation and records 9,500- and 10,001-level call inputs as clean, but likewise reports only verdicts (`round-20/a2/review/ReviewRuntimeV3.md:44-49`).
- No fresh 512 MiB/old-tool run was made. The only new probe was the single current-candidate run above. Historical resource receipts are for measured commit `843d301d1b17af78427918f7845af336b2218de0` and scanner SHA `56ff93751ac09a75065534b5a8d7af5f94986369cee6963b49d27912fce73e11`, not this candidate; I do not treat them as current-candidate operability evidence.

## Impact and smallest safe correction

- **Verdict integrity is affected directly:** the current output says `clean` despite `eval_unparsed: 1`. That counter is visible in JSON, so the parser degradation is not absent from the payload, but consumers relying on the headline verdict can miss it.
- **Deep-input recall is a plausible regression, not proven attributable to 64 MiB:** the old clean-only records lack the metric needed for a fair comparison. The probe fixture contains no protected command, so no lost finding was directly demonstrated.
- **Operability benefit remains unverified for this candidate:** source confirms the 64 MiB reservation, but the committed 384 MiB resource receipts exercised a different scanner hash.

Smallest safe correction: do not treat the 64 MiB change as no-harm until this already-existing 5,000-deep fixture is shown to have `eval_unparsed == 0` under the candidate. If 64 MiB cannot preserve that coverage, retain a sufficiently large reservation or replace the depth-sensitive recursive path; at minimum, a recursion/parse failure must not produce a headline `clean` verdict. Re-run the existing deep fixture and resource workload together under the stated cap in L1's final verification, capturing `eval_unparsed` as well as exit/label.

## Tooling

No tools installed or updated.