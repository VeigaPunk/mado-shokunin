# Seat ScrConsidertheseLesson — report (round 40, w1)

Assignment: draft the considerthese-mining paragraph for `considerthese/2026-10-25.md` proposal 2 into the
round-40 lesson. Leaf seat; no dispatch, no background jobs, no compositor verb, no counter run.

## Behavior delivered

- Draft at `.ufo/waves/round-40/w1/ScrConsidertheseLesson/mined.md` (16 KB), with the four required parts:
  (1) the proposal quoted verbatim with its date (`considerthese/2026-10-25.md:47`), plus its lineage as a
  restatement of `2026-10-24.md:47`; (2) the lane's grounding — what the watchdog digest actually shows,
  with every counting command and its output; (3) the disposition — a lesson table, no QUALITY criterion;
  (4) the status of every later proposal (#1–#6 of 2026-10-25).
- A ready-to-paste lesson paragraph (§5 of the draft) in the voice of `corpus/lessons/round-39.md`'s
  `### considerthese` subsection, and the per-round table it refers to (§2.4).

## Findings (each with what it attacks)

1. **The proposal's two numbers reproduce, from two different sources.** Rounds 32–37: 8
   `launch mado round=N` lines, 2 `lane-dead-no-report` lines (r35, r37) → 2/6 lost attempt 1; closure
   receipts give 4 dirty / 2 clean → 4/6. Commands and quoted receipts in `mined.md` §2.2/§2.4.
   Supports: the proposal's premise is accurate, so the table is worth landing.
2. **The digest cannot supply the dirty half — proven with a positive probe, not an absence.**
   `grep -icE 'leftover|porcelain|untracked|git status|dirty|sweep'` on
   `/home/vgpnk/Projects/shokunin/.ufo/watchdog.log` → `1`, and that hit is free text in kaidoku's failure
   reason (`watchdog.log:568`). Mado round 31 *did* have a dirt event —
   `$HOME/.local/state/shokunin-hyaku/events.log:1381` `inline sweep lane=mado round=31 :: report
   uncommitted at return` — and the digest's four round-31 lines carry none of it (`grep -c sweep` → 0).
   Attacks the proposal's mechanism as written: a "0 dirty closures" read from the digest is a
   criterion-62 null-channel zero.
3. **The measurement exists and is discarded.** `scripts/hyaku/inline.sh:126` prints
   `WARN lane repo has uncommitted changes: N paths` to the driver's stdout; `:130`'s
   `log "complete …"` writes only the attempt to the digest; `ev()` (`:29`) reaches `events.log` but is
   never called for worktree dirt. One `ev`/`log` call at `:126` would close the gap — fleet driver,
   operator-owned, outside this lane. Recorded as an observation, not a claim.
4. **Counting rule: count `launch` lines, never the `attempt=` field.** Round 28 carries seven
   `attempt=1`, five `attempt=2` and four `attempt=3` lines because the counter resets after an
   invalidation (`grep -E '(launch|lane-dead-no-report) mado round=28' | grep -oE 'attempt=[0-9]+'`).
   Attacks any table built from the attempt field.
5. **Round 32's dirt was inherited.** Its 5 paths were round-30 leftovers, classed "status-neutral" at
   `round-32-verifier-spotcheck.md:18`; a bare `closure clean yes/no` column misattributes it. The table
   needs the own-vs-inherited distinction.
6. **No QUALITY criterion.** No mistake class backs one; criteria 62 (null channel) and 63 (worktree
   witness) already cover the two failure modes; `SCORECARD.md:898-900` is the precedent for declining;
   and the calibration metric (`SCORECARD.md:244`) only counts criteria citing a `lessons/` mistake.
7. **Proposal 1 of 2026-10-25 is already closed** as QUALITY criterion 60 (`corpus/QUALITY.md:367-368`,
   which cites `2026-10-24.md` proposal 1) — the reflection restated a landed proposal, so the mined
   paragraph must not re-open it.
8. **Proposal 3 status is `[INFERENCE]`, not measured.** Round 38 landed the v3 pair
   (`round-38.md:4`, `:58-59`) and round 39 recorded the proposal as served by C1's re-registration
   (`round-39.md:81-82`); I did not run either counter, so "crib and snapshot cases rejected" is stated
   as inference from those lines.
9. **Proposals 4, 5, 6 remain open.** #4 (`mado-eventq.py` on a schedule) is operator-owned, no decision
   in round-39 or the round-40 registration (`grep -rniE 'schedule|cron|timer' …` → exit 1, no hits).
   #5 (one first-hand fact per day) and #6 (shorten the window) cannot be judged until
   `considerthese/2026-10-26.md` exists; `ls considerthese/` shows `2026-10-25.md` newest.
10. **Sibling table landed mid-flight and reconciles cell-by-cell — no conflict.** `ExecWatchdogTable/table.md`
    (mtime 17:57) gives 10 launches / 2 dead / 8 complete for rounds 32–39 and closure yes for r32, r33,
    r35, r36, r38 / no for r34, r37, r39 — identical to this seat's independent derivation (§2.4). Its §B
    states the same limit ("the count is a phrase-mention count, not a verdict") and it adds per-attempt
    spans (r35 attempt 1: 4h08m30s before dying; r37 attempt 1: 40m55s). Nothing in it contradicts a
    number here; `mined.md` §2.4 records the reconciliation and §6 splits what each artifact uniquely
    contributes.

## Gates

- None executed. This is a records seat: no counter, checker, selftest or axis command was run, so no gate
  is claimed as passed. The lane's harm-watch commands (`mado-verify.sh --selftest`, `check-index.py`,
  `check-axis-scores.py`, `sources-census.sh validate`) remain the L1's to run at round end.
- The draft's numbers are re-read from committed receipts and from the two digests, never re-measured.

## Touched surfaces

- Written: `.ufo/waves/round-40/w1/ScrConsidertheseLesson/mined.md`,
  `.ufo/waves/round-40/w1/ScrConsidertheseLesson.md` (this report). Nothing else.
- Read-only, outside the lane: `/home/vgpnk/Projects/shokunin/.ufo/watchdog.log`,
  `/home/vgpnk/Projects/shokunin/scripts/hyaku/inline.sh`,
  `/home/vgpnk/Projects/shokunin/scripts/shokunin-watchdog.sh`,
  `$HOME/.local/state/shokunin-hyaku/events.log`.
- Read-only, inside the lane: `considerthese/2026-10-24.md`, `considerthese/2026-10-25.md`,
  `corpus/lessons/round-{32..39}*.md`, `corpus/QUALITY.md`, `SCORECARD.md`,
  `.ufo/waves/round-40/registration.md`, `.ufo/waves/round-40/w1-spec.json`.
- `considerthese/2026-10-25.md` was not edited. No tracked file was edited.

## Out of scope / left to the L1

- `corpus/lessons/round-40.md` does not exist yet (`ls` → no such file); the paragraph in `mined.md` §5 is
  for the L1 to paste into its `### considerthese` subsection, not for this seat to create.
- `ExecWatchdogTable/table.md` was absent at the first pass and landed mid-flight (mtime 17:57); it is read
  and reconciled (finding 10, `mined.md` §2.4). The lesson should take its §A/§B rows plus the per-attempt
  spans, and keep from this draft: the source split, the two counting rules, the digest-vs-closure channel
  probe, the driver line numbers and the disposition.
- The driver fix at `inline.sh:126` is the operator's, not the lane's.

## Tooling

- No tool installed or updated; no package operation. `python3` (stdlib), `grep`, `sed`, `awk` only.
