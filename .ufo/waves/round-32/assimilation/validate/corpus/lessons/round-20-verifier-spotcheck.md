author: hyaku closure (Main, non-author integrator)

# Round 20 — independent verifier spot-check

Verdict: **rejected-harmed**, status **ok**, admitted **false**. The committed report is real work, not a marker. C1 remains harmed and C2 does not verify independently. No author file was changed.

## Authority and measured revision

- Claim base: `1f7f995caa25627db804e996cccd87fe38a3a1b6`.
- Delivered author tip: `39e213192dcf48cb094e2c159c3cd21522de0a8f`.
- Main measured committed bytes, not a moving worktree, on 2026-10-21.
- The author measured tool behavior at `a8960de655e6ea8c0a3bf74f5542041d9fe25b39`. The delivered tripwire, precision counter, attempt-2 guard counter and round-17 measurement tool are byte-identical to that revision. Their SHA-256 values are respectively `a57d4fe9277ff06c9b5916fc731e91f05bcd69cf05639cb2090ebcb00b5b6458`, `bd3bdc23747a6d8f195e69528f532988202db4ab3476d141a8ff46871e42a8e7`, `414034d57ad38719df9489201c71fce7cb39edc29a5bf25ab971cbc57a4836ef`, `de4c422b55c67f822cb9f0be21fe5e879e3d15c46830565c1c661381817cfcdc`.
- Parent did not author this lane's round-20 changes. Two proposed fresh closure coordinators could not run: an idle coordinator's wake returned a provider backoff before any answer, and a fresh spawn was refused by the job cap. Main performed the closure; RecoverReadyLanes separately re-counted committed C1/C2 receipts and reopened source decisions read-only. That advice is not a separate judge.
- Rendered prompt labels such as `@m_opus` are not an assertion about Main's answering model.

## Step-1 conformance

Observed commands:

- `scripts/hyaku/jj-lane.sh state /home/vgpnk/Projects/shokunin/mado-shokunin`: branch `master`, local and remote `39e213192dcf48cb094e2c159c3cd21522de0a8f`, ahead=0, behind=0, tracked=0, untracked=0.
- `git log -1 --format='%H %an <%ae> %aI' -- .ufo/reports/round-20/mado.md`: report commit `75bb7c1bd2d9f244d80175d2452e673176a8d7e4`, mado-shokunin, 2026-10-21T04:38:14-03:00. Author tip is dated 04:37:57-03:00: report lands after the final cited author work.
- `git merge-base --is-ancestor REV refs/heads/master` succeeded for all 15 checked cited work revisions: base, pre-harm baseline, registration `e629f73`, suite `f3da504`, attempt-1 landings `f8576f7`/`ed4bf22`/`38d1b36`, attempt-2 registration `6a7d9ca`, receipts `107955e`, tools `3610e3e`/`a8960de`, documentation `94b6925`/`c2a306db8a0425925111c46ba2c2083f48e63611`, review `4386045f73ef892bbc01f361c81ac4e8436795be`, final author tip.
- Full prompt contract is byte-identical to `templates/round-prompt.md` after the driver's lane/round/root/repo/axes substitutions, before its addendum. It contains the five child-lane items. Explicit operator routing directives govern over historical bucket labels.
- The report has a SHONEN heading and four `[~]` rows. **Defect:** those rows describe claim measurement/no-harm/sources/mistakes rather than assessing the four actual SHONEN checklist boxes. No promotion evidence is inferred.
- All eight attempt-2 review reports exist under `.ufo/waves/round-20/a2/review/`. The first report's pending-review wording is expressly superseded by its final disposition.

## C1 — operability

**Re-measured:** each committed precision case's observed `got` object was compared with its frozen `want` object, not with the report's total or the counter's copied pass count.

Reproducer (plain JSON accounting; does not execute the lane's gate or transcript data):

```sh
for path in .ufo/waves/round-20/evidence/precision-1f7f995.txt .ufo/waves/round-20/a2/evidence/precision-a8960de655e6ea8c0a3bf74f5542041d9fe25b39.txt; do
  git -C /home/vgpnk/Projects/shokunin/mado-shokunin show "39e213192dcf48cb094e2c159c3cd21522de0a8f:$path" |
    jq -Rrc 'fromjson? | select(.cases) | {total:(.cases|length),pass:([.cases[]|select(.got==.want)]|length),flag_disagreements:([.cases[]|select((.got==.want)!=.pass)]|length)}'
done
```

Observed: before `{total:175,pass:29,flag_disagreements:0}`; after `{total:175,pass:172,flag_disagreements:0}`. A separate Python comparison found 175 distinct case names, identical before/after case order and identical expectations. After families: P 66/66, L 17/18, S 17/17, W 21/22, H 51/52. The three failures are `W-CaseWrapperForms-class-method-instance`, `L-AdoptW2-AdvHelperFn-b14`, and `H-AdoptW2-RerunPrecision-corpus-jj-var-verb-help`. Registered target 175/175 remains missed by three; changing that population after observing outcomes would not verify this claim.

**Evidence-verified, not re-executed:** the fixed guard receipt has recall_lost=0, crash_flip=0, pure_rows=0, vcs_fn=0, vcs_fp=20 on its registered populations. This does not override the committed residual counterexamples. `CriticRecallV3.md` retains the invoked partialmethod miss relative to the claim base. `ReviewV3Diff.md` records lost recursive-shell-string coverage and lost callback literals, plus spurious leads for functions merely printed. `CriticPrecisionV3.md` records 18 false leads and a missed process-capable stdlib call. `ReviewRuntimeV3.md` records large shallow inputs capped above 1,800 MiB, while older tools completed around 80–167 MiB. Main did not rerun these resource-heavy or host-facing checks.

**Ruling:** operability **harmed**, not an improvement rescued by 172/175 or green thin guards. Known behavioral regressions remain in the byte-identical delivered tool. The author's final report and SCORECARD disposition correctly withdraw the initial no-harm reading.

## C2 — calibration

Committed `.ufo/waves/round-20/a2/evidence/harm/harm-measure-round-17.txt` binds `a8960de` and the measurement-tool digest above; its JSON records 30 criteria and 22 lesson-cited criteria. RecoverReadyLanes independently recounted 22/30. The conservative 21/29 reading removes the disputed replacement criterion 30-prime.

`SCORECARD.md:1300-1309` explicitly states that 30-prime uses C1's P/L counter and is not independent of C1; `corpus/QUALITY.md:249-259` confirms the shared runnable check and the L leg remains 17/18. Criterion 29 has separate fail-closed isolation evidence, but the declared two-claim combination cannot gain causal independence by re-labelling the shared evidence. The final report already discloses this.

**Ruling:** calibration **unprovable** as the separately declared claim. Literal counter growth is verified as a bounded count, not established independent discernment. No exploratory `unprovable-but-better` admission is supplied.

## Sources, admit/reject spot-check and learning trends

Source census executed: `scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin mado` → exit 0, `mado ok`, four W04 duplicate-URL warnings (S030, S042, S045, S097).

Independent table parse over committed `corpus/SOURCES.md`: whole-round base 98 rows (A91/B1/C6; mined81/queued8/rejected9) → delivered 115 (A108/B1/C6; mined98/queued8/rejected9). Added S099–S115. The report's 112→115 is the attempt-2 interval, not the whole round's base interval.

| Sample | Lane decision | Reopened evidence | Outside result |
|---|---|---|---|
| S113 process-management documentation | admit | CPython v3.14.8 `Doc/library/os.rst:4419-4422`; RecoverReadyLanes reopened it, located the ten-word process-management sentence and matched the source receipt | agree for documentation scope, not installed-host proof |
| S114 JSON serializer documentation | admit | Main reopened `https://raw.githubusercontent.com/python/cpython/v3.14.8/Doc/library/json.rst:245-273`; `dumps` and its serializer description occur at 260–266 | agree; quote is within the cited range and below 25 words |
| A tree page as a byte-level source anchor | reject | Main reopened `https://github.com/jj-vcs/jj/tree/v0.38.0/cli/src/commands/git`; it is an HTML directory listing at v0.38.0, not the declared v0.45.1 raw source | agree with the Gate's raw/version-specific admission rule |
| Wrong `Doc/library/functions.rst` location | reject/not admitted at that location | Main and RecoverReadyLanes reopened the exact v3.14.8 raw URL; HTTP 404. S105 instead points to `Doc/builtins/functions.rst` | agree; an absent target is not source support |

- **expansion: harmed.** The new admitted `corpus/knowledge/tripwire-precision-r20.md` did not exist at the base, but it still asserts restored recall and swept recursive bodies (lines 19, 29) that the committed residual reviews falsify. Its own Limits section does not disclose the residual recursive/partialmethod/resource failures. These are not made admissible knowledge merely by adding source rows or capability rows. This fails the lane's separation/currentness bar (QUALITY 3 and 28) and the learning contract's rule for admitted entries failing their own bar.
- **quality: harmed.** The new tool's behavioral/resource counterexamples remain unresolved; a source-row census and a passing thin guard do not discharge them. This agrees with the final author revision, not the superseded early report.
- **discernment: improved, bounded to the sampled source decisions and honest rejection.** Sampled admits/rejects agree with outside reopens; the author retained and acknowledged contradictory reviews. This is not a claim that C2's coupled counter establishes independent calibration.

Axes: operability harmed; calibration unprovable; depth, coverage, freshness and adjacency unchanged in this closure (no additional improvement claimed). No new capability is admitted by this rejected round. SHONEN remains author-asserted only; no `[x]`, promotion or mint.

## Routed defects for the next eligible repair round

1. Preserve the 175-case population and explicitly retain the three misses; repair the actual residual recall/precision/resource regressions rather than weaken the target, skip members or reinterpret thin guards as no-harm proof.
2. Separate C2's evidence causally from C1; retain 22/30 as conditional historical accounting and 21/29 as the disclosed conservative reading, not an independent claim pass.
3. Append a correction inside the knowledge entry for the residual counterexamples and resource limits; a correction elsewhere does not remove its current overclaims.
4. Make resource/counterexample evidence durable. Several residual reports cite detailed harnesses, input manifests and raw outcomes only under `/tmp`; committed reports record observations, but those paths are not durable replay authority. Do not rerun memory-heavy probes on the live host without safe bounds.
5. Correct SHONEN assessment rows to the actual checklist in the next report. Preserve old filed bytes and the final withdrawal of no-harm.
6. Freeze whole-corpus inputs before making reproducible corpus-diff claims. Current live-session totals are dated observations only.
7. Attempt-2 registration followed a sandbox draft measurement (disclosed M13). Next registration and independent oracle must be committed before tool results are examined.

## Dispatch digest and verification limits

- `2026-10-20T16:25:22-03:00 launch mado round=20 ... driver=hyaku-inline attempt=1`
- `2026-10-21T02:47:18-03:00 lane-dead-no-report mado round=20 ... attempt=1`
- `2026-10-21T02:47:20-03:00 launch mado round=20 ... driver=hyaku-inline attempt=2`
- `2026-10-21T04:38:35-03:00 complete mado round=20; hyaku-inline attempt=2`

Registries have w1 85 assigned and w2 78 assigned; author reports w2 76 delivered/two dead. The eight committed attempt-2 residual reports bring total spent seats to 171. No dead seat was credited or replaced by this closure.

Main ran only read-only Git/JSON/hash/table measurements, the shared source census and public-source opens. No lane gate, compositor, package manager, host probe or fixture transcript code was executed. Tool installations: none.
