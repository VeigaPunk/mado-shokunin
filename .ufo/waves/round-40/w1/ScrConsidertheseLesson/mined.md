# considerthese mining — `2026-10-25.md` proposal 2 (round 40, seat ScrConsidertheseLesson)

Status: draft for the round-40 lesson's `### considerthese` subsection (`corpus/lessons/round-40.md`,
append-only, not yet created at read time: `ls corpus/lessons/round-40.md` → no such file).
Sources: proposal file (read-only), the fleet watchdog digest (read-only, outside the lane),
`scripts/hyaku/inline.sh` (read-only), the lane's `corpus/lessons/round-{32..39}-verifier-spotcheck.md`,
`corpus/QUALITY.md`, `SCORECARD.md`. No counter was re-run. Every number below is either a command I ran
or a quoted receipt line.

---

## 1. The proposal, quoted with its date

`considerthese/2026-10-25.md:47` (file dated 2026-10-25, window 2026-10-22 09:52 → 2026-10-25 09:52 BRT,
covering rounds 32–37):

> 2. **Count dead attempts and dirty closures from the watchdog digests.** Two of six rounds lost
> attempt 1 and four of six closed with leftover files. A small table each day (round, attempts,
> closure clean yes/no) would make this fleet-level problem visible without me reading every
> spot-check.

**Lineage — this is a restatement, not a new proposal.** `considerthese/2026-10-24.md:47` already said:

> 2. **Report run reliability as its own line.** Dead attempts, OOM kills and provider 429s cost round
> 28 seven attempts this window. I should count them from the LOG and watchdog lines and surface them
> to João, since they are fleet problems he can fix, not lane problems.

Round 39 mined `2026-10-24.md` proposal 4 and `2026-10-25.md` proposal 3 and nothing else
(`corpus/lessons/round-39.md:80-82`), so the reliability proposal has been carried unmined for one day
and is now stated a second time with concrete numbers. That carry is the reason it lands as a table now
rather than a third time as prose.

## 2. The lane's grounding — what the digest actually shows

### 2.1 The digest's whole vocabulary for this lane

`/home/vgpnk/Projects/shokunin/.ufo/watchdog.log` (1418 lines; `log()` in
`scripts/shokunin-watchdog.sh` is `echo "$(date -Is) $*" >> "$UFO/watchdog.log"`). For mado:

```
W=/home/vgpnk/Projects/shokunin/.ufo/watchdog.log
grep -E '\bmado\b' "$W" | sed -E 's/^[0-9T:.+-]+ //' | awk '{print $1}' | sort | uniq -c | sort -rn
#   45 launch
#   25 complete
#   15 lane-dead-no-report
```

Three verbs, no fourth. For rounds 32–39 the slice is complete and verb-pure:

```
grep -cE 'mado round=3[2-9]' "$W"                                     # 20
grep -E 'mado round=3[2-9]' "$W" | grep -vcE ' launch | complete | lane-dead-no-report '   # 0
```

(20 = 10 launch + 2 dead + 8 complete; digest pinned at `wc -l` 1419,
`sha256 784433719336f097…`.) There is no cleanliness field anywhere in the file.

### 2.2 The attempts half is derivable, and reproduces the proposal's numbers

```
grep -cE '^[^ ]+ launch mado round=3[2-7] ' "$W"                       # 8
grep -cE 'lane-dead-no-report mado round=3[2-7];' "$W"                 # 2
grep -cE '^[^ ]+ complete mado round=3[2-7];' "$W"                     # 6
```

The two deaths in that window are quoted in full:

```
2026-10-25T03:23:08-03:00 lane-dead-no-report mado round=35; retry same round (hyaku-inline attempt=1: run-6: attempt-1 orphan — no report, session died 2026-10-24 ~23:30 -03)
2026-10-25T06:46:34-03:00 lane-dead-no-report mado round=37; retry same round (hyaku-inline attempt=1: run-6: L1 returned after 40m with no commits and no report (abandoned mid-round; uncommitted work inherited by next attempt))
```

So **"two of six rounds lost attempt 1" is exact** (r35, r37; r32, r33, r34, r36 launched once each and
completed on attempt 1).

**Counting rule the table must use:** count `launch mado round=N` lines, never the `attempt=` field.
The field is not monotonic — round 28 carries `attempt=1` seven times and `attempt=2` five times across
its launch and dead lines (`grep -E '(launch|lane-dead-no-report) mado round=28' "$W" | grep -oE
'attempt=[0-9]+' | sort | uniq -c` → `7 attempt=1`, `5 attempt=2`, `4 attempt=3`), because the counter
resets after an invalidation. Attempts read off that field would be wrong; launches are unambiguous.

### 2.3 The dirty-closure half is **not** in the digest — and this is a null channel, not a zero

```
grep -icE 'leftover|porcelain|untracked|git status|dirty|sweep' "$W"   # 1
```

The single hit is free text inside another lane's failure reason (`kaidoku round=20 … retain checkpoint5c0b46c and all dirty author evidence`, `watchdog.log:568`), not a field, and not mado.

The decisive probe is a **positive** one — a round where dirt is known to have existed:

- `$HOME/.local/state/shokunin-hyaku/events.log:1381`:
  `2026-10-24T04:25:18-03:00 inline sweep lane=mado round=31 :: report uncommitted at return (attribution defect)`
- the watchdog log's four round-31 lines carry no trace of it
  (`grep -E 'mado round=31' "$W"` → `launch` 04:08:04, `lane-dead-no-report` 04:11:14, `launch` 04:11:17,
  `complete` 04:25:19; `grep -c 'sweep' "$W"` → 0).

A known dirt event produced zero digest lines. Under `corpus/QUALITY.md:371-372` (criterion 62: a zero
count is evidence of absence only when the same channel is shown, in the same round, to carry the class
being counted) a "0 dirty closures" read off the watchdog log is refused, not read as a negative.

**Why the signal exists but is not written.** `scripts/hyaku/inline.sh` measures worktree dirt at
closure and then throws the measurement away:

- `:126` `[ -n "$(git -C "$cwd" status --porcelain)" ] && echo "WARN lane repo has uncommitted changes: $(git -C "$cwd" status --porcelain | wc -l) paths"` — plain `echo`, driver stdout only;
- `:130` `log "complete $lane round=$n; hyaku-inline attempt=$(claim "$lane" attempt)"` — the `log` call that reaches the watchdog carries the attempt and nothing about the tree.

The `ev()` helper (`inline.sh:29`) writes `$STATE/events.log`, and that channel does carry dirt — but only
for the report file (`inline sweep lane=… round=… :: report uncommitted at return`), never for the
worktree. One `ev`/`log` call at `:126` would make the proposal's second half derivable. That edit is in
the **fleet driver**, outside this lane's write scope and operator-owned; it is recorded here as an
observation for the lesson, not as a lane claim.

### 2.4 Where the dirty column does come from

The lane's own closure receipts, per round — `jj-lane.sh state` (`tracked=`/`untracked=`) and
`git status --porcelain`, quoted in each `round-NN-verifier-spotcheck.md`:

| round | launches | dead attempts | closure worktree | receipt |
|---|---|---|---|---|
| 32 | 1 | 0 | dirty — 5 paths, all round-30 leftovers (inherited) | `round-32-verifier-spotcheck.md:18`, `:84` |
| 33 | 1 | 0 | dirty — 19 untracked dirs, no tracked modifications | `round-33-verifier-spotcheck.md:19`, `:25` |
| 34 | 1 | 0 | clean — `tracked=0 untracked=0`, porcelain empty | `round-34-verifier-spotcheck.md:41-43` |
| 35 | 2 | 1 | dirty — `tracked=8 untracked=2` | `round-35-verifier-spotcheck.md:45-48`, `:218` |
| 36 | 1 | 0 | dirty — 1 untracked seat report (`DistillerFindings.md`, 19,033 B) | `round-36-verifier-spotcheck.md:21` |
| 37 | 2 | 1 | clean — `tracked=0 untracked=0`, porcelain empty | `round-37-verifier-spotcheck.md:20` |
| 38 | 1 | 0 | dirty — 3 modified seat reports (+187/−7) | `round-38-verifier-spotcheck.md:17` |
| 39 | 1 | 0 | clean — porcelain empty | `round-39-verifier-spotcheck.md:16-17` |

Rounds 32–37: **2/6 dead, 4/6 dirty** — the proposal's two numbers reproduce exactly, from two different
sources. Rounds 32–39: 2/8 dead, 5/8 dirty.

**Reconciliation with the sibling seat.** `w1/ExecWatchdogTable/table.md` landed after this draft's first
pass. It agrees on every cell of both halves: §A gives 10 launches / 2 dead / 8 complete for 32–39 with
the same per-round split as the table above, and its §B closure column reads yes for r32, r33, r35, r36,
r38 and no for r34, r37, r39 — the same 5/3 (and 4/2 over 32–37) that §2.4 records from the receipts.
Its §B also states the limit this draft relies on ("the count is a **phrase-mention** count, not a
verdict") and quotes the same decisive lines, e.g. r32 `:18` "all round-30 leftovers". It adds per-attempt
spans (§A2: r35 attempt 1 ran 4h08m30s before dying; r37 attempt 1 ran 40m55s), which the lesson table can
take directly. Nothing in it contradicts a number here; the lesson should take its §A/§B rows and this
draft's source split, counting rules and §2.3.

One correction the table must carry: round 32's 5 paths were **round-30 leftovers**, i.e. inherited dirt
caught at round-32 closure, and the round-32 spot-check classes them "status-neutral"
(`:18`). A bare `closure clean yes/no` column marks r32 dirty and misattributes it; the table needs the
own-vs-inherited distinction (or a footnote) or the number is misleading. The round-32 receipt also
records that the driver's own `WARN … 5 paths` reproduced — the same line as `inline.sh:126`, confirming
the measurement fires and simply is not persisted.

## 3. Disposition

1. **Lands as a lesson table, not a claim and not a QUALITY criterion.** Two columns, two sources:
   `launches`/`dead attempts` from the watchdog digest (commands in §2.2, counted by `launch` lines);
   `closure worktree` from the round's spot-check receipt (criterion 63 already requires a worktree
   reading to commit its raw witness beside the receipt). The table states which column came from which
   source, and states that the digest cannot supply the second one.
2. **No QUALITY criterion, because no mistake backs one.** The lane's convention is that a criterion is
   the fix for a classed mistake — `corpus/lessons/round-39.md` `## Mistakes` gives each entry a
   `Class / Evidence / Captured-by / Fix`, and criteria are credited only where a mistake names them
   (M39-1 → criteria 49 and 61; M39-2 → "none"). Nothing in this window is classed as a mistake of the
   "reliability was not reported" kind: the dirt events were routed as defects with their own receipts
   (round-32 D7, round-36 R1, round-35 D8), and the null-channel risk is already covered by criterion 62,
   the worktree-witness rule by criterion 63. The precedent for declining is `SCORECARD.md:898-900`
   ("A tripwire criterion was proposed and **not** added to QUALITY (it would be C3 work inflating C1's
   fraction)"). Adding a criterion here would also move the calibration axis
   (`SCORECARD.md:244`, lesson-grounded criteria) without a lesson `#mistakes` row to cite — the metric
   counts criteria that cite `lessons/`, and a criterion citing a proposal instead would not count.
3. **The proposal's own mechanism is half-unsound as written** ("from the watchdog digests"): the
   attempts half is derivable, the dirty half is not, and reading it as a zero would be a criterion-62
   violation. The lesson table therefore fixes the proposal's source, and the driver-side one-line fix is
   named as operator-owned and out of lane scope. This is the same transferable rule as the window's
   round-37 reject (a zero from a log that could not have recorded the event), applied to the lane's own
   bookkeeping.
4. **Not a claim, no counter.** Nothing here is a capability or coverage claim; it rides in the lesson's
   `### considerthese` subsection as prose plus the table, exactly as round 39 mined its two proposals
   (`corpus/lessons/round-39.md:80-82`).

## 4. Which later proposals remain open (`2026-10-25.md`)

| # | Proposal (2026-10-25) | Status after this round | Evidence |
|---|---|---|---|
| 1 | domain-vs-meta ratio as a running number | **closed / landed** — restatement of `2026-10-24.md:46`; landed as QUALITY criterion 60, which cites `considerthese/2026-10-24.md` proposal 1 and requires the ratio plus its command in every round report | `corpus/QUALITY.md:367-368` |
| 2 | count dead attempts and dirty closures from the watchdog digests | **mined this round** — lesson table per §3; mechanism corrected (attempts from the digest, closures from the spot-check receipts) | this file, §2–§3 |
| 3 | watch M37-5 by name (are the C1 crib and C2 snapshot cases rejected now?) | **served, verdict not re-run here** — round 38 landed the v3 re-grounding pair ("discriminating the round-37 v2 cribs", "the live triplet closing the v3 `live` clause"), and round 39 recorded the proposal as served by C1's re-registration. I did not execute either counter this round, so "both cases rejected" is `[INFERENCE]` from those two lesson lines, not a measurement | `corpus/lessons/round-38.md:4`, `:58-59`; `corpus/lessons/round-39.md:81-82` |
| 4 | ask whether `mado-eventq.py` should run on a schedule (and what enabling logs would cost) | **open** — operator-owned (it is a suggestion to João); no schedule/cron/timer decision appears in the round-39 lesson or the round-40 registration | `grep -rniE 'schedule|cron|timer' corpus/lessons/round-39.md .ufo/waves/round-40/registration.md` → no hits |
| 5 | verify one fact first-hand per day, read-only | **open** — restatement of `2026-10-24.md:50`; the 2026-10-25 file self-reports one first-hand check (the `mado-eventq.py` docstring, the SOURCES row count). Recurrence is unobservable from the lane: no `considerthese/2026-10-26.md` exists yet | `ls considerthese/` → newest `2026-10-25.md`; `considerthese/2026-10-25.md` self-report |
| 6 | shorten the window to what is new | **open** — the 2026-10-25 file still declares the three-day window on line 3 and claims it led with new content; whether it recurs is only checkable in the next file, which does not exist | `considerthese/2026-10-25.md:3`; no `2026-10-26.md` |

Also still open from `2026-10-24.md` and unmined: #3 (follow up routed items — practised as the reflection's
"Carried items" table, never landed as a lane artifact), #5 (= 2026-10-25 #5), #6 (time-of-day pattern —
partially practised: the 2026-10-25 file states launch/completion clock times).

## 5. Ready-to-paste paragraph for `corpus/lessons/round-40.md` § `### considerthese`

> `considerthese/2026-10-25.md` proposal 2 (2026-10-25: count dead attempts and dirty closures from the
> watchdog digests, as a daily round/attempts/closure-clean table) is mined as a lesson table, not as a
> claim. It is a restatement of `2026-10-24.md` proposal 2, carried unmined through round 39. Its two
> numbers reproduce: for rounds 32–37 the digest gives 8 `launch mado round=N` lines and 2
> `lane-dead-no-report` lines (r35, r37 — 2/6 lost attempt 1), and the closure receipts give 4 dirty and
> 2 clean closures (r32 5 inherited round-30 paths, r33 19 untracked, r35 `tracked=8 untracked=2`, r36 one
> untracked seat report; r34 and r37 `untracked=0`, porcelain empty). The table below splits the sources
> — rows reconciled cell-by-cell with `w1/ExecWatchdogTable/table.md` §A/§B, which adds per-attempt spans —
> because the digest cannot carry the second column: `grep -icE
> 'leftover|porcelain|untracked|git status|dirty|sweep'` on the watchdog log returns 1 hit, free text in
> another lane's failure reason, while mado round 31 — which the events log records as
> `inline sweep … report uncommitted at return` — leaves no trace in the digest at all. The measurement
> exists and is discarded: `scripts/hyaku/inline.sh:126` prints `WARN lane repo has uncommitted changes: N
> paths` to the driver's stdout, and `:130`'s `log "complete …"` writes only the attempt. So the
> proposal's "from the watchdog digests" holds for attempts and is a null channel for closures (criterion
> 62 refuses that zero); the closure column is read from each round's `-verifier-spotcheck.md`, whose
> worktree witness criterion 63 already binds. Counting rule: count `launch` lines, not the `attempt=`
> field, which is not monotonic (round 28 carries seven `attempt=1` and five `attempt=2` lines). Round 32's
> five paths were round-30 leftovers, so the column needs the own-vs-inherited distinction. No QUALITY
> criterion is added: no mistake class backs one, criteria 62 and 63 already cover the two failure modes,
> and `SCORECARD.md:898-900` is the precedent for declining. The driver-side fix (one `ev`/`log` call at
> `inline.sh:126`) is operator-owned and outside the lane. Later proposals still open: #3 (M37-5 by name)
> is served by round 38's v3 pair and round 39's C1 re-registration but its verdict was not re-run this
> round; #4 (`mado-eventq.py` on a schedule) is open and operator-owned; #5 (one first-hand fact per day)
> and #6 (shorten the window) stay open until `considerthese/2026-10-26.md` exists. #1 is already closed as
> QUALITY criterion 60.

## 6. Limits of this draft

- `ExecWatchdogTable/table.md` was absent at the first pass and landed mid-flight (mtime 17:57). It is now
  read and reconciled in §2.4: it supplies the per-round counts and the closure yes/no with fixed-string
  pins, and per-attempt spans; it does not attempt the digest-versus-closure channel question (§2.3), the
  `attempt=`-field non-monotonicity (§2.2), the driver line numbers, or a disposition. The lesson should
  take its rows and keep those four things from here.
- No counter, checker or gate was executed. The proposal-3 status is `[INFERENCE]` from two lesson lines.
- The watchdog log is fleet state and was read only; it is append-only and live, so line numbers are as of
  `wc -l` 1419 (`sha256 784433719336f097…`). Nothing outside the lane was written.
- Closure state for rounds 32–39 is quoted from committed spot-check receipts, not re-measured; the
  worktrees of those rounds no longer exist.
