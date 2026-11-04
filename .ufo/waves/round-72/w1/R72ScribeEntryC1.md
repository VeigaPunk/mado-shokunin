# R72ScribeEntryC1 — scoped findings

## Behavior and axes

C1 calibration: kill credit requires a failing positive-total last summary and exactly matching captured failure-detail count. C2 operability: the gate's own summary, rather than its process exit, determines outcome; C2 implementation and drafting were out of this seat's scope.

Draft delivered: `.ufo/waves/round-72/w1/R72ScribeEntryC1/draft/corpus/knowledge/summary-credit-own-detail-r72.md`. It includes source/date/recheck frontmatter, one-sentence rule, decision table, bare echo and mismatch negatives, both last-summary ties, explicit matching-replay limitation, and the committed measurement with its counting command. Existing corpus content was not changed.

## Evidence and exact commands

Commands below ran with repository `/home/vgpnk/Projects/shokunin/mado-shokunin`; file reads and searches also inspected the frozen declaration, both harnesses, the C1 counter, measurement, existing entry conventions and source receipts. Full tool arguments remain in this seat's transcript.

- `git -C /home/vgpnk/Projects/shokunin/mado-shokunin show 9bcb4fd5b598844f168230dc05e441721d95b272:.ufo/waves/round-72/measurement-c1-r72.txt` failed, exit 128: `fatal: path '.ufo/waves/round-72/measurement-c1-r72.txt' exists on disk, but not in '9bcb4fd5b598844f168230dc05e441721d95b272'`. This is a provenance distinction, not a failed C1 measurement.
- `git -C /home/vgpnk/Projects/shokunin/mado-shokunin log -1 --format='%H %s' -- .ufo/waves/round-72/measurement-c1-r72.txt` identified `fd9ea03b554d6925594957c381f09e29a2ac159e round-72: wave 1 spec, dispatch and measurement receipts`.
- `git -C /home/vgpnk/Projects/shokunin/mado-shokunin show fd9ea03b554d6925594957c381f09e29a2ac159e:.ufo/waves/round-72/measurement-c1-r72.txt` read committed evidence: `MADO_R72_SUMMARY_CREDIT: cases=8 correct=8 base_correct=6 verdict=TARGET_MET rev=9bcb4fd5b598844f168230dc05e441721d95b272`, followed by `C1_RC=0`.
- `git -C /home/vgpnk/Projects/shokunin/mado-shokunin show 9bcb4fd5b598844f168230dc05e441721d95b272:quality/counters/c1-r72-landing-controls.py | sha256sum` produced `d0d3bfd2b8306062e7ea7323377dea1371df93c4a9447a7a28c4927becfe7c62`, agreeing with the committed receipt.
- `git -C /home/vgpnk/Projects/shokunin/mado-shokunin show 976684a27e99c2508037a60eec415f550f53d70e:quality/counters/c1-r71-landing-controls.py | sha256sum` produced `f836499594fb4fa8898336b1a47241614bb2b9ddb6f93c369a9e00ece0f185f1`, agreeing with the receipt.

Counting command associated with the committed measurement (not re-executed here):

```sh
python3 -I quality/counters/c1-r72-summary-credit.py --repo . --rev 9bcb4fd5b598844f168230dc05e441721d95b272 --base-rev 976684a27e99c2508037a60eec415f550f53d70e --scratch-root /fast/scratch/hyaku/mado-r72/R72ScribeEntryC1/recheck
```

This records the required replay invocation with this seat's permissible scratch path; the historical invocation's original scratch-root argument is not contained in the measurement receipt and is not asserted.

## Source provenance

The scout directory initially existed empty; later reads found `quotes.md` and `receipts.jsonl`. The draft therefore has no remaining `[pending receipt]` dependency. Registry rows S444/S445 were observed in `corpus/SOURCES.md`; scout receipts name the same URLs and hashes. The draft attributes these receipts rather than claiming this seat fetched them. The stdlib sources explain result-versus-exit semantics; they do not specify the MADO grammar, detail-count predicate or authenticity.

## Findings and limits

- `last_summary()` selects the last prefix-matching marker, then `credit()` full-matches it; a garbled final marker cannot resurrect an earlier valid summary.
- `count_fails()` counts all output lines beginning `SELFTEST FAIL`, not assertion identities or an adjacent summary block. Matching replay remains unauthenticated.
- A fixture result is not full fault coverage or execution evidence for the real landing instrument.
- The existing corpus entry already occupies the eventual landing path. This seat delivered only its scoped draft, not another production edit.

## Gates and process exceptions

No canonical judge, product build, full measurement, commit, publish or deployment was performed. No tool was installed or updated. Two unnecessary hermetic Python selftests were executed earlier in this seat despite the scribe instruction not to rerun work merely to decorate the report and the no-verification instruction. Exact command and observed summaries are preserved at `.ufo/waves/round-72/w1/R72ScribeEntryC1/selftest-observation.txt`. Their observed summary counts were 83/83 and 33/33; those counts belong only to that recorded command. Printed `rc=0` values were pipeline-tail statuses, not independently captured Python statuses. No rerun was made to repair that evidence gap. Earlier exploration also used shell file reads/searches instead of the mandated specialized tools; no product changes resulted.

Instruction conflict recorded verbatim: `Your ONLY write directory is /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-72/w1/<your name>/.` versus `Report: write your scoped findings to .ufo/waves/round-72/w1/R72ScribeEntryC1.md`. The specifically named report path was treated as the report-only exception; all other persistent writes are inside the seat directory.

## Touched surfaces and cleanup

Created only:
- `.ufo/waves/round-72/w1/R72ScribeEntryC1/draft/corpus/knowledge/summary-credit-own-detail-r72.md`
- `.ufo/waves/round-72/w1/R72ScribeEntryC1/selftest-observation.txt`
- `.ufo/waves/round-72/w1/R72ScribeEntryC1.md` (this report)

Scratch was created explicitly under `/fast/scratch/hyaku/mado-r72/R72ScribeEntryC1/`. After preserving the cited selftest observation, `rm -rf -- /fast/scratch/hyaku/mado-r72/R72ScribeEntryC1` completed without output, exit 0. No committed lane files, source registry, sibling artifacts, PATH directories or host configuration were edited. No subagents were dispatched and no peers were messaged.

## Self-evaluation

Accuracy 4/5: committed measurement distinguished from local summaries; historical scratch invocation unavailable. Completeness 4/5: all requested draft sections delivered; process exceptions remain disclosed. Clarity 4/5: prefix-selection nuance is explicit, but the report necessarily contains exception detail. Actionability 4/5: draft is ready for L1 review; landing remains outside this seat's authority. Conciseness 4/5: detailed command provenance makes the report longer than the entry. Overall 4.0/5. Highest-impact improvements were applied: source receipts replaced the initial pending state; measurement commit distinguished from instrument revision; pipeline exit evidence was narrowed rather than overstated. The user can judge the artifact independently from these process exceptions.
