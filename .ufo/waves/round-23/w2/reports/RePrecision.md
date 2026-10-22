# RePrecision: C1 precision guard at the landed tip (round 23, wave 2)

Seat: MadoR23.RePrecision (leaf reviewer). Scope: run `tw-precision.py` at tip `2f1134f38930fc8b067d2d7f5bba126338faabdd` and base `a28e4815aabfa85f55274884000fb2608355f8cf`, compare per case, and attack the result. No lane file was edited. Raw receipts sit outside the lane in `/fast/scratch/hyaku/mado-r23/RePrecision/`.

## Verdict

**PASS for the precision guard as registered.** Tip 2f1134f scores 166/175, the same as base a28e481. The passing set is identical (166 names each). No case that passes at base fails at the tip. No case changed verdict on the 175 precision cases, at any level I compared.

Coverage caveat, not a guard failure: 32 of the 184 changed executable lines in the tip classifier are never executed by the precision suite, and 28 of those are not executed by the repair fixtures either (see the Medium finding below).

## Commands and receipts

Every guard run used `prlimit --as=402653184 --cpu=15 --` (384 MiB address space, 15 s CPU), one child at a time, with cwd at the lane. The `outer_address_space_cap` of 402653184 is the same cap that round-21's recorded precision runs carry (`.ufo/waves/round-21/evidence/final/precision-legacy-a6cef89.json`). Command shape:

    prlimit --as=402653184 --cpu=15 -- python3 -I /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-20/tw-precision.py <REV> > /fast/scratch/hyaku/mado-r23/RePrecision/precision-<REV>.json

| Run | rc | wall | Receipt (under /fast/scratch/hyaku/mado-r23/RePrecision/) | sha256 |
|---|---|---|---|---|
| tip 2f1134f, precision | 0 | 6.62 s | precision-2f1134f38930fc8b067d2d7f5bba126338faabdd.json | 98103261a58856afde5106fa5060063024e444dc9111cf9428ef456fd5748827 |
| base a28e481, precision | 0 | 6.63 s | precision-a28e4815aabfa85f55274884000fb2608355f8cf.json | 33d6e66e162a3662851babd209bf34a165ebe19d9ca744f094546d69167345f0 |
| tip 2f1134f, held-out (`--heldout`) | 0 | 0.49 s | heldout-2f1134f38930fc8b067d2d7f5bba126338faabdd.json | 3ce141462207e98e0612f07d21091a5b234cdcfdd2dd6440e55b52e6e2b069f3 |
| base a28e481, held-out (`--heldout`) | 0 | 0.47 s | heldout-a28e4815aabfa85f55274884000fb2608355f8cf.json | fddc4db1d993fc823ac15b8e84851c1fc0c5a6ca42eea280322781228c126ede |

Identity checks (`git show <rev>:<path> | sha256sum`, read-only):
- `tools/mado-tripwire.py`: base a28e481 and e33ea30 are `cd9da20c2f562efbd30967e00c0c630026de6e6d06ef74399eb1a46ccf00ea84`. C1 commit 2e592af and tip 2f1134f are `41489991163627f56de79bc360d4f13454fa5d50787a5802927b9cac562ca009`. The only commit touching `tools/` in a28e481..2f1134f is 2e592af.
- `.ufo/waves/round-20/tw-precision.py` is `bd3bdc23747a6d8f195e69528f532988202db4ab3476d141a8ff46871e42a8e7` at base, at tip and in the working tree. Nothing under `.ufo/waves/round-20/` changed between base and tip.
- Suite pin f3da504: `precision/expected.json` is `1039c4fa6ede43b1f08cca231e6c713aa032722e4955f89dbd8b8f3de092254f`, and `precision-heldout/expected.json` is `78b168b0db86502df23b6204a5a9a3e1f53189df5cf0257fef6c1d1214b3901a`. Both match the hashes recorded in `.ufo/waves/round-21/w1/reports/ScoutOldSuite.md`.
- Base a28e481 is an ancestor of tip 2f1134f, and tip is an ancestor of master.

## Results, tip versus base

| | tip 2f1134f | base a28e481 |
|---|---|---|
| passed / 175 | 166 (score 9.4857) | 166 (score 9.4857) |
| P | 66/66 | 66/66 |
| S | 17/17 | 17/17 |
| W | 21/22 | 21/22 |
| H | 47/52 | 47/52 |
| L | 15/18 | 15/18 |
| verdicts clean / findings (exit 0 / exit 1) | 106 / 69 | 106 / 69 |

## Per-case comparison (175 cases)

- Passing names: identical sets, 166 each, zero symmetric difference.
- Regressions (base pass, tip fail): **none**.
- Improvements (base fail, tip pass): **none**.
- Cases whose verdict changed: **none**, at every level I checked:
  - pass status: 0 changed;
  - normalized verdict (the harness's `got`: exit plus the multiset of class, rule, line, evidence): 0 changed;
  - full verdict (complete stdout bytes plus exit code, base and tip each run separately on the same case path): 175 of 175 byte-identical.
- Held-out (12 cases, reported beside the score, not scored): 2 of 12 at both revisions; no flips; full verdict byte-identical 12 of 12.
- Round-22's recorded precision run (`.ufo/waves/round-22/evidence/resume/precision-final.json`, rev 579109a6, tool cd9da20c) passes the same 166 names as base and as tip.

The nine cases that fail at both revisions (unchanged, listed for the record):
1. L-CasePureCrossCell-reset-clears-helper
2. W-CaseWrapperForms-class-method-instance
3. H-CaseDryRunBash-commit-dry-run
4. H-CaseHelpDryRunEval-pct-bash-dry-runs
5. L-CaseLeadsInvisible-reset-cleared-helper
6. L-AdoptW2-AdvHelperFn-b14
7. H-AdoptW2-AdvVcs-p33-git-dryrun
8. H-AdoptW2-RerunPrecision-corpus-jj-var-verb-help
9. H-AdoptW2-RerunPrecision-corpus-git-commit-a-dry-run-short

## Sensitivity: the change is live on the repair fixtures

To rule out a dead harness, I ran the base and tip classifier copies (`git show <rev>:tools/mado-tripwire.py`) on the 12 committed repair fixtures. Fixture bytes came from `git show 2f1134f:.ufo/waves/round-23/repair/fixtures/...`, and all 12 match the `sha256` fields in `repair/expected.json`.

Full verdict bytes differ on 6 fixtures. These are not part of the precision guard and are listed so the verdict-change list is complete:
- ReturnedGlobalCallableShadow: base's lead `pacman -S r22-foreign-callable` is gone at tip.
- ForwarderInvokesCallback: base's observed host_mutation `pacman -S r23-forward-foreign` becomes observed `pacman -Q r23-forward-global`; `unparsed_spawns` 1 becomes 0.
- CallerLocalShadowsHelperGlobal: base's observed `pacman -S r23-local-foreign` becomes `pacman -Q r23-local-global`.
- ForwardExistingClosureWithoutFrameContamination, ForwarderPassesCallerArgument, ForwarderInvokesFactoryClosure: findings unchanged; only `unparsed_spawns` changes, 1 becomes 0 (checked field by field).

Identical on 6: ReturnedGlobalHelper, CallerArgumentBeforeClosureOverlay, NestedDefReadsDefiningFrame, LateGlobalRebinding, CallbackStoredInDict, CallbackStoredOnAttribute.

My own re-implementation of the frozen exact rule (exit 0 or 1; sorted (class, command, evidence) rows equal to `want`; unparsed sum 0; no `forbid_any` command at any tier; this is not the `truth.py` recording fake) gives base 4 of 10 and tip 10 of 10 on the exact cases. The two present-kind cases have identical bytes at both revisions; I did not adjudicate them. The official counter `repair/measure.py` was not run by me.

## Coverage: what this guard can see

Method: for each of the 175 precision cases and the 12 repair fixtures, one child `python3 -I -m trace --count --file=<pkl> --coverdir=<dir> tool-tip.py --scan <case>` under the same caps. Every traced verdict equals the harness's recorded verdict (0 mismatches over 175). Changed lines are the `+` ranges of `git diff -U0 a28e4815 2f1134f -- tools/mado-tripwire.py` (257 lines), of which 184 are executable (tip file: 3701 lines, 2908 executable).

- Executed by at least one precision case: 152 of 184 (82.6%).
- Executed by at least one repair fixture: 142 of 184 (77.2%).
- Executed by no precision case: 32. Of these, 28 are executed by neither population and 4 by repair fixtures only.

The 32 precision-blind lines (tip line numbers):
- own_names (def 1347): 1359, 1361, 1369 (neither)
- prepare_eval_calls (def 2267): 2294 (neither)
- scope_view (def 2435): 2443 (neither)
- parameter_escapes (def 2471): 2487-2489, 2491, 2496-2500, 2508-2509 (neither); 2494-2495, 2502 (repair only)
- argument_position (def 2516): 2522-2523 (neither)
- reference_escapes (def 2527): 2546, 2549-2552, 2554 (neither)
- take (nested in spawn_scan; def 2684): 2722, 2733, 2744, 2772 (neither); 2972 (repair only)

Coverage data: `/fast/scratch/hyaku/mado-r23/RePrecision/cov/summary.json`.

## Findings by severity

**High: none.** No base-passing case fails at tip. The count is 166, which meets the floor. No verdict changed on the precision population.

**Medium (evidence gap for the C1 no-harm claim, not a guard failure).** This guard is silent on 32 of the 184 changed executable lines, and 28 of them are reached by no fixture I ran. They sit in the escape-analysis helpers (`parameter_escapes`, `reference_escapes`, `argument_position`, `scope_view`, `own_names`), in `prepare_eval_calls`, and in the nested `take` callbacks inside `spawn_scan`. "Zero change on precision" therefore says nothing about those branches. Their no-harm evidence must come from other populations (the 1356-file corpus comparator, the oracles, the selftests). I did not measure those populations. Advice: have the corpus comparator owner confirm these lines are exercised there, or record them as unexercised.

**Low (guard scope).** `tw-precision.py` compares exit plus the multiset of (class, rule, line, evidence) only. It is blind to counts, per-file unparsed counters and command text. On this population the full verdict bytes are identical, so there is no present harm. But a future unparsed-counter regression would pass this guard. Advice: keep unparsed-counter adjudication in the corpus guard as a hard gate, as the registration's clarification 8 already says.

**Low (operability hygiene).** `tw-precision.py` has no internal caps. Its per-child timeout is 120 s (line 177), against the registered 15 s CPU and 384 MiB address space. The caps hold only when the caller wraps the guard, as I did. The full run takes 6.6 s, far below the caps. Advice: record the wrapper in the receipt, as the round-21 record does with `outer_address_space_cap`.

**Info (positive checks).** Every child returned a verdict code (0 or 1), so no run produced `could_not_evaluate` or a timeout. Normalized verdicts from the guard run agree with separate traced invocations on all 175 cases, and base and tip full stdout agree byte for byte. The guard reproduces round-22's recorded passing set. The suite and script are unchanged base to tip.

## Residual risk and verification gaps

- Not run by me: the official repair counter `repair/measure.py` and its `truth.py` recording fake, the corpus comparator, the oracle, the selftests, and the resource population.
- Coverage was measured on the precision and repair populations only. The held-out suite was not traced.
- Each revision was guarded once. Determinism rests on the byte-identical full-verdict runs, the trace runs, and the round-22 record, not on repeated guard runs.

## Tooling record (operator directive)

No installs and no updates were performed. Tools used: python3 3.14.8 (`/usr/bin/python3.14`), util-linux `prlimit` 2.42.4, and `/usr/bin/jq` jq-1.8.2 for cross-checks. The shell's `jq` is a builtin, `jaq` 3.1.1, not the official binary. I used it for the first-pass list extraction and then re-derived every jq-based list with `/usr/bin/jq`; all lists matched. Lane access was read-only (`git show`, `rev-parse`, `ls-tree`, `log`, `merge-base`, `diff`, one `git status`). The only lane write is this report; a `mkdir -p` on the existing `w2/reports/` directory was a no-op.
