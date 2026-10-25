# QUALITY criteria 69–72 — draft (round 41, w1, seat ScrQualityCriteria)

Append after criterion 68 (`corpus/QUALITY.md:383`, file ends at 68). No renumbering, no rewrite of
65–68. Each criterion below is drafted in the file's own style: rule, `Check:`, `Shown able to fail:`,
`(lesson: …)`, and each is grounded in a **round-40 defect that a verifier routed**, not in a
hypothesis. The four grounds are:

| # | defect (as routed) | where it is recorded |
|---|---|---|
| 69 | a tip receipt cited by the report but never committed | `corpus/lessons/round-40-verifier-spotcheck.md:19` defect (b); §6 item 2 at `:92` |
| 70 | a dispatch marker left untracked in the lane | `corpus/lessons/round-40-verifier-spotcheck.md:15` leftovers row; §6 item 1 at `:91` |
| 71 | a seat report written under another round | `corpus/lessons/round-40.md:134-138` M40-6 |
| 72 | an equivalent mutant created by redundant code | `corpus/lessons/round-40.md:88-89` (M40-1, the reply-cap survivor) |

Every `Check:` below was executed in both directions this seat; the transcript is
`.ufo/waves/round-41/w1/ScrQualityCriteria/receipts.txt` (re-derive with
`bash .ufo/waves/round-41/w1/ScrQualityCriteria/run-checks.sh`). All checks read committed bytes only;
no check writes the lane.

---

69. A measurement a report quotes is evidence only when a receipt carrying that measurement is committed at the revision the report attributes it to, and the receipt's own bytes name that revision; a report's tip-state number therefore has a receipt in the tip tree, and a number measured at the tip that exists only in the working tree is not a receipt. `Check:` extract every revision token the report writes in measurement form (`rev=<hex>`, `rev <hex>`, `at <hex>`) and require, at the report's revision, one committed receipt under that round's `receipts/` whose bytes contain the token — `python3 .ufo/waves/round-41/w1/ScrQualityCriteria/check69.py --repo . --rev <rev> --report <report> --receipts .ufo/waves/round-<N>/receipts` (`--text` to read a report held outside the tree); a `MISSING <token>` line is a violation. `Shown able to fail:` round-40's tip `fb49621` — the report cites `MADO_AXIS checked=3 mismatched=0 at fb49621` (`corpus/lessons/round-40-verifier-spotcheck.md:19`, at `cd950ec`) while `git grep -l fb49621 fb49621 -- .ufo/waves/round-40/receipts/` prints nothing and the only committed axis receipt is `receipts/axis-base.txt` at `rev=9fc511d`; the check reads `MISSING fb49621 … FAIL 1/1`, exit 1. Passing instance, same shape: round-41's freeze `60c3914` carries `receipts/axis-base.txt` naming `rev=ab2bfaa…`, and the check reads `PASS 1/1`, exit 0. Extends criterion 63 (which commits a worktree reading beside its receipt) to the revision the reading is *attributed* to. Limit: the check binds the citation to a receipt's bytes, not the report's number to the receipt's number — a receipt naming the revision with a different count still passes, and the count itself stays the reader's re-derivation. (lesson: lessons/round-40-verifier-spotcheck.md §1 defect (b), §6 item 2 — routed, not repaired)

70. Every marker a wave writes into its own directory (`w1.ready`, `w1.ready.dispatched`, any `*.ready`) is either committed at the revision the round closes on or absent from the tree; the observable is disk presence against that revision's tree, never `git status`, because `status` compares the worktree to `HEAD` and a marker committed by a later round's dispatch commit stops appearing as untracked while remaining absent from the revision being judged. `Check:` `bash .ufo/waves/round-41/w1/ScrQualityCriteria/check70.sh . <rev> .ufo/waves/round-<N>` — it lists the revision's tracked markers, then every marker on disk; an `UNTRACKED <path>` or `DIRTY` line is a violation (`VERDICT: DIRTY_MARKER`, exit 1). `Shown able to fail:` at round-40's tip `fb49621` the check reads `UNTRACKED .ufo/waves/round-40/w1.ready.dispatched` while `git cat-file -e fb49621:…w1.ready.dispatched` reports `exists on disk, but not in 'fb49621'` — the routed defect (`corpus/lessons/round-40-verifier-spotcheck.md:15`, "one untracked `.ufo/waves/round-40/w1.ready.dispatched` (dispatch marker, no round work)", `…spotcheck.md:15` at `cd950ec`); the same wave at `cd950ec`, where the dispatch commit tracked the marker, reads `VERDICT: CLEAN`, exit 0, and the mktemp fixture committed in this seat's receipt reads CLEAN with both markers committed and `DIRTY_MARKER` once a third marker is left on disk. Extends criterion 63 with the case that made the round-40 reading stale. Limit: the check names marker *files*, not the wave's run state — a marker deleted from disk and never committed is indistinguishable from a wave that never wrote one, so the receipt that says which markers the driver wrote stays the registration's job. (lesson: lessons/round-40-verifier-spotcheck.md §1 leftovers row, §6 item 1 — routed, not repaired)

71. A seat's returned report path resolves inside the running round's wave directory, under the seat's own name, and exists at the revision the wave's results are read at: an absolute path is root-dependent and another round's path is a dead report, whatever text the seat returned. `Check:` `python3 .ufo/waves/round-41/w1/ScrQualityCriteria/check71.py --repo . --rev <rev> --results .ufo/waves/round-<N>/w1-results.json --round <N>` — each row's `report` must match `^\.ufo/waves/round-<N>/w1/<Seat>\.md$`, name its own seat, and satisfy `git cat-file -e <rev>:<path>`; a `FOREIGN`/`SEAT-MISMATCH`/`UNTRACKED` line is a violation. `Shown able to fail:` round-40's results at `fb49621` read `FOREIGN ConnCrossClaim returned .ufo/waves/round-49/w1/ConnCrossClaim.md` (the routed M40-6: "`ConnCrossClaim` returned `report: .ufo/waves/round-49/w1/ConnCrossClaim.md`", `corpus/lessons/round-40.md:135`) and `FOREIGN ScoutOptionTypes returned /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-40/w1/ScoutOptionTypes.md` — the second instance is this seat's measurement, same class, a lane-relative path returned as an absolute one; `RESOLVED ok=33 bad=2 … exit 1`. Passing instance: the same file with only those two rows dropped reads `PASS every returned report resolves inside round-40`, exit 0, so the check is not failing on the other 33 seats' environment. Limit: 29 of the 64 rows returned no `report` key at all and are counted, not judged — a criterion over path discipline does not decide whether a seat owes a report file. (lesson: lessons/round-40.md#mistakes M40-6 — routed, fix "none")

72. Before a mutant is counted as a control, every site that enforces the mutated property is enumerated and the patch removes all of them; a one-site patch over a two-site property is an equivalent mutant, and it is either repaired to remove the surviving site or declared equivalent beside the declaration that names the surviving site or the measurement that proves the equivalence. `Check:` `python3 .ufo/waves/round-41/w1/ScrQualityCriteria/check72.py --repo . --rev <rev> --controls <round>/ctl/run-c1-v2-controls.py --receipt <round>/receipts/ctl-c1-v2.txt` — every mutant named in the controls file has a receipt row, every non-`REF-`/`P-` row is below target (`SURVIVOR <name>` otherwise), and every `… is an equivalent mutant` declaration carries a `receipts/<file>` that exists at the revision or a named code site (`splitlines()`, `:NNN`); otherwise `EQUIV-UNARGUED`. `Shown able to fail:` the reply-cap property is enforced at three sites in `tools/mado-options.py:942-951` (a bounded read, `too_long = len(raw) > REPLY_CAP`, and the raise); a copy patched to remove only the read bound (`.ufo/waves/round-41/w1/ScrQualityCriteria/partial-m38.patch.txt`) scores `fixtures=19/19 … verdict=TARGET_MET`, exit 0, under the frozen round-40 v2 counter — the survivor the lesson records ("the reply cap (the mutant kept a post-check -> the control now removes both)", `corpus/lessons/round-40.md:88-89`) — and the check reads `SURVIVOR M38-partial-readcap-only … FAIL 1 defect(s)`, exit 1. The committed controls pass both ways: `M38-reply-cap-dropped` removes both sites (`ctl/run-c1-v2-controls.py:149-151`) and scores `fixtures=18/19 … TARGET_MISSED` (`receipts/ctl-c1-v2.txt:46`), `M43` declares its equivalence with `receipts/f32-equivalence.txt` (`ctl/run-c1-v2-controls.py:163-164`, the file reads `0 of 999` differences), `X15` declares it with the parse site `splitlines()` (`ctl/run-c2-v2-controls.py:247`); both committed receipts read `PASS`, exit 0. Extends criterion 65 (one mutant per spelling class) with the case where the mutant *class* is right and the patch is incomplete. Limit: a named site is a source-level argument, not a measurement — X15's equivalence is argued from the counter's own parse rule and has no swept receipt, and this criterion accepts that while recording it as the weaker of the two forms. (lesson: lessons/round-40.md#mistakes M40-1 — the reply-cap survivor and its repair)

---

## Notes for the L1 (integrator)

- **Numbering.** These are 69–72 because `corpus/QUALITY.md` ends at 68 (`wc -l` → 383; last line is
  criterion 68). Appending them leaves 65–68 byte-identical.
- **Lesson citations.** All four cite committed round-40 sources that resolve today
  (`corpus/lessons/round-40.md`, `corpus/lessons/round-40-verifier-spotcheck.md`). If the round-41
  lesson records these as `M41-n`, extend the parenthetical (`…; lessons/round-41.md#mistakes M41-n`)
  rather than replacing the round-40 pointer — criterion 54's anchor rule resolves each `file#anchor`
  against its own file, so both can stand.
- **Criterion 69's limit is deliberate**: the check pins the citation, not the arithmetic. Making it
  pin the numbers would require every report to restate its receipt's line verbatim; that is a
  stronger rule and would need its own mistake behind it.
- **Criterion 70 changes an existing habit**: the round-40 spot-check read the leftover with
  `git status --porcelain`. That reading went stale the moment round-41's dispatch commit tracked the
  marker (`cd950ec`); the check therefore compares disk to the *revision*, and the receipt records
  both readings (fail at `fb49621`, clean at `cd950ec`).
- **Nothing here is applied.** `corpus/QUALITY.md` was not edited: the counters, registration, controls
  and reference are frozen, and the integrator owns the append.

## Artifacts (this seat)

| path | what |
|---|---|
| `.ufo/waves/round-41/w1/ScrQualityCriteria/criteria.md` | this draft |
| `.ufo/waves/round-41/w1/ScrQualityCriteria/check69.py` | check for criterion 69 |
| `.ufo/waves/round-41/w1/ScrQualityCriteria/check70.sh` | check for criterion 70 |
| `.ufo/waves/round-41/w1/ScrQualityCriteria/check71.py` | check for criterion 71 |
| `.ufo/waves/round-41/w1/ScrQualityCriteria/check72.py` | check for criterion 72 |
| `.ufo/waves/round-41/w1/ScrQualityCriteria/run-checks.sh` | runs all four, both directions |
| `.ufo/waves/round-41/w1/ScrQualityCriteria/receipts.txt` | transcript of the 10 runs + ground bytes |
| `.ufo/waves/round-41/w1/ScrQualityCriteria/partial-m38.patch.txt` | the one-site patch that makes M38 equivalent |
| `.ufo/waves/round-41/w1/ScrQualityCriteria/partial-m38-score.txt` | its score under the frozen v2 counter (19/19, exit 0) |
| `.ufo/waves/round-41/w1/ScrQualityCriteria/scratch/` | the four input files the checks read (report claims, results copy, survivor receipt) |
