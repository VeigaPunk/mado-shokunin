# CriticAdmission — partly falsified: v3.1 repairs the known recall losses, but the 175 target still misses and C2's 30′ point is not independent of C1

## Per-claim readings

| Claim | Verdict | Basis |
|---|---|---|
| C1 operability / tripwire precision | **improved**; strict target **not met** | Same axis and same pinned `tw-precision.py` counter: 29/175 at `1f7f995` → 172/175 at `a8960de`; registered 175/175 still misses by three. The attempt-2 guard fixes the known M9 population (52 lost → 0), but does not change the score. |
| C2 calibration | **improved**, conservatively 21/29; 22/30 is conditional | `measure.py` c1 is 20/28 → 22/30. Criterion 29 has its own isolation check; 30′ reads C1's P/L counter, so that point is not causally independent. `21/29 = 7.2414` remains above `20/28 = 7.1429`; 30′ is positive but incomplete precision evidence (L is 17/18). |
| Frontier (S113–S115; M9–M15) | **improved**, with a process caveat | Three tier-A source rows and M9–M15 are present in the current lesson. M13 candidly records that A2 registration followed sandbox measurement; this limits prospective independence of the new guard, not the value of checking known failures. |
| “No axis harmed” overall | **unprovable** | Registered corpus diff reports zero lost rows on 7,889 stable files, but 150 files were excluded, 7,253 rows were added without truth adjudication, the held-out set is 2/12 at `a8960de` (one fewer pass than at `9c54c56`), and 20 VCS false positives remain in the measured fixture population. The known recursive-helper cost is fixed; an ~89 s parity case remains. |

## Findings (highest severity first)

### 1. C1 is the same claim/counter, but the registered N/N target remains false

- **Reproduce:** `python3 -I .ufo/waves/round-20/tw-precision.py a8960de655e6ea8c0a3bf74f5542041d9fe25b39`
- **Input fixture + SHA-256:** `.ufo/waves/round-20/precision/CaseAdoptW2--AdoptW2-AdvHelperFn-b14.jsonl` — `118b0136e43d282ddffabafee2d13880ac63e60b9facd3453a000cd089052c7a`.
- **Observed vs expected:** final counter `172/175` (P 66/66, S 17/17, W 21/22, H 51/52, L 17/18); b14 wants exit 1 with `package_query/pacman:-Q/evidence:lead`, but gets exit 0 and no findings. `175/175` is not achieved. The same counter was used for the original C1 claim; attempt 2 changes the tool, not the axis or suite.
- **Revisions compared:** `1f7f995` 29/175; `28c6837` 172/175; `a8960de` 172/175. The other two failures are `W-CaseWrapperForms-class-method-instance` and `H-AdoptW2-RerunPrecision-corpus-jj-var-verb-help`.
- **Impacted axis:** C1 target attainment and lead coverage. The other new counter is supplemental; it must not be presented as a substitute for the unchanged 175-case score.
- **Smallest safe correction:** keep the literal `172/175` verdict and named failures. Fix b14 or explicitly narrow its scope in a future pre-registered suite; do not edit this suite after observing the result.

### 2. C2's 30′ evidence is coupled to C1 and does not test the removal side that M9 exposed

- **Reproduce:** `python3 -I .ufo/waves/round-20/tw-precision.py a8960de655e6ea8c0a3bf74f5542041d9fe25b39`; `python3 .ufo/waves/round-20/a2/a2-guards.py a8960de655e6ea8c0a3bf74f5542041d9fe25b39 --fixtures-rev 6a7d9ca0d2124a4077074b800c94a9bc1184441c`.
- **Input fixture + SHA-256:** `.ufo/waves/round-20/w2/AdvRecallShapes/fixtures/ar01-asyncio-run-cse.jsonl` — `238666f5785c14e54572d93794e555485a661697f3350c54fbfe6c3c4b3e3094`.
- **Observed vs expected:** at `28c6837`, this reachable `asyncio.run(m())` spawn is silent; the frozen A2 guard reports `recall_lost=52`. At `a8960de`, that guard reports `recall_lost=0`. Meanwhile 30′'s three legs are still P 66/66, L 17/18, and zero lost rows in the `9c54c56` corpus diff. Thus the three legs alone admitted the `28c6837` detector despite M9. The final detector has a separate removal-side guard that catches and fixes this population; 30′ itself does not.
- **Counterexample to the 30′ L check:** `.ufo/waves/round-20/precision/CaseAdoptW2--AdoptW2-AdvHelperFn-b14.jsonl` (SHA-256 `118b0136e43d282ddffabafee2d13880ac63e60b9facd3453a000cd089052c7a`) wants an invisible-body `package_query/pacman:-Q/evidence:lead`; `a8960de` emits no row. The criterion's runnable check describes L as “invisible body → lead”, so 17/18 is not a full pass. The weaker “marker on every emitted row” clause can be true vacuously for a missing row; it does not cure the coverage miss.
- **Revisions compared:** `9c54c56`/`1f7f995` → `28c6837` → `a8960de`; M9 was 52 losses at `28c6837`, 0 at `a8960de`.
- **Causal separability:** no for the 30′ point. Its red and green P/L numbers come from the C1 `tw-precision.py`; its lead family has the remaining b14 miss above. Criterion 29 is independent. `measure.py` c1 reproduces 20/28 = 7.1429 → 22/30 = 7.3333; if 30′ is not counted as an independent point, the disclosed 21/29 = 7.2414 remains an improvement. A 30′-red reading would be 21/30 = 7.0000, below baseline. M9 is a separate recall/removal failure: it does not falsify the precision-only purpose of 30′, but it demonstrates why 30′ cannot stand in for detector-wide no-harm; b14 independently leaves the runnable L check short of full pass.
- **Impacted axes:** C2 calibration independence; C1 recall/no-harm scope. M9 makes 30′ unearned as standalone evidence for detector-wide admission; b14 also leaves the documented L check at 17/18. The scorecard/QUALITY note disclose M9 and queue a removal-side requirement for round 21.
- **Smallest safe correction:** report `22/30` as conditional on the 30′ swap and keep `21/29` beside it; do not describe the C1-derived evidence as independent or all 30′ legs as fully green. Keep the removal-side guard visible as separate evidence.

### 3. Held-out and VCS negatives leave a real precision/generalization limit

- **Reproduce:** `python3 -I .ufo/waves/round-20/tw-precision.py 9c54c56a6a7528675027b7f628f97a1b8d1b8e8d --heldout`; then `python3 -I .ufo/waves/round-20/tw-precision.py a8960de655e6ea8c0a3bf74f5542041d9fe25b39 --heldout`; also the A2 guard command above.
- **Input fixtures + SHA-256:** `.ufo/waves/round-20/precision-heldout/CaseAdoptW2--AdoptW2-RerunPrecision-fx3-jj-log-version.jsonl` — `d0c9fa48961b5291e539568b347948aac6dd6c48ed7188bb4fc3c448bf4799ae`; `.ufo/waves/round-20/w2/AdvVcsForms/fixtures/jj-root.jsonl` — `a285d2bb2a10bd0bebd93c7c370eea062c52f1647975313804d781d52adb3820`.
- **Observed vs expected:** held-out is 3/12 at `9c54c56`, 0/12 at `28c6837`, and 2/12 at `a8960de` (final full suite plus held-out is 174/187). At final, fx3 expects clean but emits `vcs_write/jj:log/evidence:observed`; the recorded jj 0.45.1 probe reports `jj log --version` exit 2 and no op. The final A2 guard also lists `jj-root.jsonl` among 20 false-positive VCS forms; its measured truth is no write. These are outside the scored 175, so they do not change 172/175, but they disprove broad held-out/no-false-positive language.
- **Revisions compared:** held-out `9c54c56` 3/12 → `28c6837` 0/12 → `a8960de` 2/12; A2 VCS false positives 31 → 20, not zero.
- **Live-corpus evidence:** the `9c54c56` → `a8960de` diff receipt reports 0 lost on 7,889 stable files, 7,253 additions, and 150 exclusions from 8,039 starting files. Input/evidence artifact `.ufo/waves/round-20/a2/evidence/corpus-diff-9c54c56-vs-a8960de.json` SHA-256 `b758abd3c29aec4259747974f11620fb1f4fdac6df78578dae2438e0192eaf2b`. The additions are listed in 99 groups but are detector output, not truth adjudication; zero losses is a bounded result, not proof that every added row is true.
- **Impacted axes:** held-out precision and generalization. The exclusions and added-row counts bound, but do not invalidate, the registered zero-loss result.
- **Smallest safe correction:** keep the no-harm statement bounded to the stable digest-matched corpus and registered guards; report held-out 2/12 and residual `vcs_fp=20` alongside it. Add the false-positive and wrapper cases to a future pre-registration if they are intended to gate admission.

### 4. M13 timing weakens prospective force but does not invalidate the repair

- **Reproduce:** inspect `SCORECARD.md:1347-1376` and `corpus/lessons/round-20.md:27` (M13).
- **Input documents + SHA-256:** `SCORECARD.md` — `e19fc710654d787d609c28ccd3f12bbf75b3d1997e7bcae668d9162b2d47ebd6`; `corpus/lessons/round-20.md` — `1cd80c3af440ac38d888f83b34554f3a19138e90a8c50db9dbe7aecad2a14306`.
- **Observed vs expected:** the registration states it was written after the sandbox draft had been developed and measured, though before the repair landed; the frozen populations and nine A2 fixtures predate the tool edit. This is disclosed, not hidden. It is not disqualifying for the original C1 counter/target or the pre-measurement C2 criteria, but it means the A2 guard's successful red-to-green result is targeted confirmation, not blind prospective evidence.
- **Revisions compared:** pre-draft registration/guards at `e629f73` versus A2 guard registration at `6a7d9ca`, followed by `3610e3e` and `a8960de`.
- **Impacted axis:** process independence of the new guard only.
- **Smallest safe correction:** keep the known-defect rechecks as such; register the next round's acceptance population and before-receipts before opening/measuring the draft, as M13 already requires.

### 5. Revision-bound `measure.py` rejection disagrees with the “rejected=[] at tip” disposition

- **Reproduce:** `python3 .ufo/waves/round-17/measure.py a8960de655e6ea8c0a3bf74f5542041d9fe25b39`.
- **Input document + SHA-256:** committed `a8960de` version of `corpus/knowledge/tripwire-precision-r20.md` — `199002895c14733a2da8b9da0c828f953ca66402dc4da564e21ab6b61a2058bf`; current worktree version — `38685fb989e4792cbea167f796b1c9c0edd47e05ef5100c90c8b1296aca567b7`; receipt `.ufo/waves/round-20/a2/evidence/harm/harm-measure-round-17.txt` — `c101fc3ddcc3a091a6dce70427ba596fe2dd2a65ba9e974169b6cae74c87748c`.
- **Observed vs expected:** the revision-pinned receipt at `a8960de` reports `rejected=[tripwire-precision-r20.md, MALFORMED, surface line must be exactly surface: P<n>]`; the current worktree note has `scope:` and no such malformed line. The C1 measure remains 22/30 and province count remains 6, but the disposition claim that `measure.py rejected=[] at tip` does not hold for the committed `a8960de` bytes.
- **Revisions compared:** committed `a8960de` versus the current worktree note; this is a revision/provenance mismatch, not a change to the c1 fraction.
- **Impacted axis:** the `measure.py` rejection facet and revision-bounded documentation, not the C1 score or the 6/6 province count.
- **Smallest safe correction:** keep the existing receipt as historical, do not attribute the worktree fix to `a8960de`, and re-run against the commit that contains `scope:` before claiming `rejected=[]`.

### 6. Runtime cost: the attempt-1 recursion regression is fixed; a parity outlier remains

- **Reproduce:** `python3 .ufo/waves/round-20/a2/a2-guards.py a8960de655e6ea8c0a3bf74f5542041d9fe25b39 --fixtures-rev 6a7d9ca0d2124a4077074b800c94a9bc1184441c`.
- **Input fixtures + SHA-256:** `.ufo/waves/round-20/a2/fixtures/hang-selfrec-40.jsonl` — `8c7dd76da0014e0be5e6d102103a0ebc46a5309f0782c0f0ec38187a28df86ab`; `.ufo/waves/round-20/w2/AdvCrash/fixtures/huge_bash_cmd.jsonl` — `0e73ec4cf310e8a0b5c813151614464278333a0ba64a80cbb85df670baf05c2d`.
- **Observed vs expected:** `hang-selfrec-40` falls from 54.764 s at `28c6837` to 0.034 s in my `a8960de` guard run (receipt rounds to 0.037 s); no A2 guard timeout. The same run's slowest file is `huge_bash_cmd.jsonl` at 88.728 s. AdvCrash measured the ~88 s 2 MiB single-token cost on both old and repaired tools, so this is a severe parity cost, not a newly introduced slowdown.
- **Revisions compared:** `28c6837` → `a8960de`; the new recursive-helper outlier is fixed, while the large-token parser cost is reported as symmetric with the older tool.
- **Impacted axis:** wall-clock cost. Registered `timeouts=none` passes its 120 s guard, but it is not a claim of uniformly cheap scans.
- **Smallest safe correction:** keep the measured contrast and parity limitation explicit; do not describe timeout-free execution as a runtime-cost guarantee.

## Limits

- Transcript fixtures were scanned as data; no payloads were executed. I did not run the whole-corpus diff myself; I read its revision-bound receipt and JSON artifact.
- The held-out suite is explicitly outside the scored 175. Its 2/12 result is a generalization/no-harm counterexample, not a retroactive change to the registered target.
- The 7,253 live-corpus additions are not individually truth-adjudicated here. No install/update was needed.

## Installs

none