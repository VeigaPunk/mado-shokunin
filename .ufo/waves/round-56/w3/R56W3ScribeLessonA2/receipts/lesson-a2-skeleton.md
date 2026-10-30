# Attempt-2 lesson skeleton for `corpus/lessons/round-56.md` — R56W3ScribeLessonA2 (2026-10-30)

**What this file is.** A scaffold, not lesson prose. Every `<FINDINGS>` is an unfilled slot for the L1. Nothing in the
append block below is settled: no value, verdict, row, quote, count or admission may be read as true until the L1 replaces
the placeholder with the evidence named in the *Fill map* at the foot of this file. Text in `{braces}` is instruction to the
filler, not text to keep.

**Append target.** `corpus/lessons/round-56.md` — append-only. The attempt-1 sections above the append point (including the
existing `## Gate`, `## Registry changes old→new`, `## Mistakes`, `## Wave-2 findings applied and routed`, `## Considerthese
and assimilation`, `## Census`) stay byte-identical. The attempt-2 block is appended at the attempt-2 tip `<FINDINGS: attempt-2
commit sha>` (the file's last section at the attempt-1 tip `0f3a54361a9824484d0801679ceb1fd8ac7c32e1` is `## Census`).

**Heading note.** The three headings below are the names the seat spec fixes (the attempt-2 section header, the Gate
(attempt 2) heading and the Registry changes (attempt 2) heading). If the lane's markdown style wants them nested under the
attempt-2 h2, demote the latter two to h3 at integration — do not rename them, and do not merge them into the attempt-1
Gate / Registry-changes sections.

**Provenance of the structural facts quoted below.** Seat roster and role mix: `.ufo/waves/round-56/w3-spec.json` (64 items;
untracked at the attempt-1 tip — commit reference `<FINDINGS>`). Attempt-1 wave shape: `.ufo/waves/round-56/receipts/at-final.txt`
(last line) and `.ufo/waves/round-56/w1-results.json`. Attempt-2 L1 self-verification: `.ufo/waves/round-56/receipts/attempt2-l1.txt`
(untracked at the attempt-1 tip). Attempt-2 drafts: `.ufo/waves/round-56/attempt2/s396-s397-draft.md`. Frozen contract:
`.ufo/waves/round-56/claims-frozen.md` (v1, freeze `3423ae285676c2a10273000f4519163472b443db`),
`.ufo/waves/round-56/claims-frozen-v2.md` + `registration-v2.md` + `frozen-tables-v2.json` (v2, pre-data re-registration
`323a69c9014da1cebece67bb111b70a5630f4a60`, tables sha256
`9511151ac2f72097310780357b4a3018e799691cca11905bf75a7e5f6bd795e2`), integration errata `15015e77402bf544403f8f387dac4e48e29cdaa6`
(E12-E14). Those four revisions are never edited by this round.

--- BEGIN APPEND BLOCK ---

## Attempt 2 (2026-10-30 re-dispatch) — wave w3 settled

Attempt 1 (2026-10-28) landed all three frozen claims and stopped honestly: wave 1 settled 43 of 43 seats
(`.ufo/waves/round-56/w1-results.json`), the operator wrap-up stopped wave 2 mid-flight — 33 of 35 seats reported,
`R56W2MutC3Counter` and `R56W2MutC2Harness` were killed with no report, no `w2-results.json` was written — and the round
published its lesson, LOG, SCORECARD and final receipts at the attempt-1 tip `0f3a54361a9824484d0801679ceb1fd8ac7c32e1`
(content revision `8a7b734627b06583a9106fcc0940f0a180ff331d`). Attempt 2 re-dispatches the round on 2026-10-30 as ONE wave
against the same frozen v2 contract: wave `w3`, 64 seats, one role mix of 16 executor, 7 mutation-tester, 6 critic, 15
reviewer, 10 scout, 2 connector, 1 simplifier, 4 scribe, 1 sentinel and 2 revenger seats. The claims are NOT re-frozen and
NOT widened: v1 (`3423ae28`), v2 (`323a69c9`) and the integration errata (`15015e77`) stand byte-identical, and every
predicate, counter, kill rule and target of this round is the one attempt 1 ran. What attempt 2 adds is re-verification at the
attempt-1 tip, second samples of the row and host evidence, an independent reading of the frozen instruments, the
adjudication the attempt-1 wave could not finish, and two queued registry rows drafted but not yet integrated.

Seats reported: `<FINDINGS: N of 64>`. Seats dead (killed with no report): `<FINDINGS: list, or "none">`. Wave results file
written: `<FINDINGS: .ufo/waves/round-56/w3-results.json written | not written, and why>`. Attempt-2 tip commit:
`<FINDINGS: sha>`. Re-verification outcome per claim: `<FINDINGS: C1 / C2 / C3 — one line each, with the seat that ran it>`.

### Wave w3 seats (attempt 2)

`reported` = the seat's report exists at `.ufo/waves/round-56/w3/<Seat>.md`; `dead` = the seat was killed or produced no
report; `lesson input` = what the seat's findings change in this lesson (often "none").

| # | seat | role | reported | dead | lesson input |
|---|---|---|---|---|---|
| 1 | `R56W3ExecReverifyC1` | executor | `<FINDINGS>` | `<FINDINGS>` | `<FINDINGS>` |
| 2 | `R56W3ExecReverifyC2` | executor | `<FINDINGS>` | `<FINDINGS>` | `<FINDINGS>` |
| 3 | `R56W3ExecReverifyC3` | executor | `<FINDINGS>` | `<FINDINGS>` | `<FINDINGS>` |
| 4 | `R56W3ExecHarmWatch` | executor | `<FINDINGS>` | `<FINDINGS>` | `<FINDINGS>` |
| 5 | `R56W3ExecFreezeOrder` | executor | `<FINDINGS>` | `<FINDINGS>` | `<FINDINGS>` |
| 6 | `R56W3ExecSessionMaterial` | executor | `<FINDINGS>` | `<FINDINGS>` | `<FINDINGS>` |
| 7 | `R56W3ExecCrit107Build` | executor | `<FINDINGS>` | `<FINDINGS>` | `<FINDINGS>` |
| 8 | `R56W3ExecBaseBefore` | executor | `<FINDINGS>` | `<FINDINGS>` | `<FINDINGS>` |
| 9 | `R56W3ExecLiveGetoption` | executor | `<FINDINGS>` | `<FINDINGS>` | `<FINDINGS>` |
| 10 | `R56W3ExecFixDivA` | executor | `<FINDINGS>` | `<FINDINGS>` | `<FINDINGS>` |
| 11 | `R56W3ExecFixDivB` | executor | `<FINDINGS>` | `<FINDINGS>` | `<FINDINGS>` |
| 12 | `R56W3ExecWaveEvidence` | executor | `<FINDINGS>` | `<FINDINGS>` | `<FINDINGS>` |
| 13 | `R56W3ExecInherited` | executor | `<FINDINGS>` | `<FINDINGS>` | `<FINDINGS>` |
| 14 | `R56W3ExecProbeC3NewRows` | executor | `<FINDINGS>` | `<FINDINGS>` | `<FINDINGS>` |
| 15 | `R56W3ExecHoldoutReseal` | executor | `<FINDINGS>` | `<FINDINGS>` | `<FINDINGS>` |
| 16 | `R56W3ExecTagPin` | executor | `<FINDINGS>` | `<FINDINGS>` | `<FINDINGS>` |
| 17 | `R56W3MutC3Counter` | mutation-tester | `<FINDINGS>` | `<FINDINGS>` | `<FINDINGS>` |
| 18 | `R56W3MutC2Harness` | mutation-tester | `<FINDINGS>` | `<FINDINGS>` | `<FINDINGS>` |
| 19 | `R56W3MutKillC1` | mutation-tester | `<FINDINGS>` | `<FINDINGS>` | `<FINDINGS>` |
| 20 | `R56W3MutKillC2` | mutation-tester | `<FINDINGS>` | `<FINDINGS>` | `<FINDINGS>` |
| 21 | `R56W3MutKillC3` | mutation-tester | `<FINDINGS>` | `<FINDINGS>` | `<FINDINGS>` |
| 22 | `R56W3MutBwrapChannels` | mutation-tester | `<FINDINGS>` | `<FINDINGS>` | `<FINDINGS>` |
| 23 | `R56W3MutC107Spec` | mutation-tester | `<FINDINGS>` | `<FINDINGS>` | `<FINDINGS>` |
| 24 | `R56W3CritC1Forge` | critic | `<FINDINGS>` | `<FINDINGS>` | `<FINDINGS>` |
| 25 | `R56W3CritC2Cheat` | critic | `<FINDINGS>` | `<FINDINGS>` | `<FINDINGS>` |
| 26 | `R56W3CritC3Allowlist` | critic | `<FINDINGS>` | `<FINDINGS>` | `<FINDINGS>` |
| 27 | `R56W3CritC1Grammar` | critic | `<FINDINGS>` | `<FINDINGS>` | `<FINDINGS>` |
| 28 | `R56W3CritHarnessC1` | critic | `<FINDINGS>` | `<FINDINGS>` | `<FINDINGS>` |
| 29 | `R56W3CritCensus` | critic | `<FINDINGS>` | `<FINDINGS>` | `<FINDINGS>` |
| 30 | `R56W3RevAuditA2A` | reviewer | `<FINDINGS>` | `<FINDINGS>` | `<FINDINGS>` |
| 31 | `R56W3RevAuditA2B` | reviewer | `<FINDINGS>` | `<FINDINGS>` | `<FINDINGS>` |
| 32 | `R56W3RevAuditA2C` | reviewer | `<FINDINGS>` | `<FINDINGS>` | `<FINDINGS>` |
| 33 | `R56W3RevAuditA2D` | reviewer | `<FINDINGS>` | `<FINDINGS>` | `<FINDINGS>` |
| 34 | `R56W3RevAuditA2E` | reviewer | `<FINDINGS>` | `<FINDINGS>` | `<FINDINGS>` |
| 35 | `R56W3RevAuditA2F` | reviewer | `<FINDINGS>` | `<FINDINGS>` | `<FINDINGS>` |
| 36 | `R56W3RevUsedByHedge` | reviewer | `<FINDINGS>` | `<FINDINGS>` | `<FINDINGS>` |
| 37 | `R56W3RevProcFdinfo` | reviewer | `<FINDINGS>` | `<FINDINGS>` | `<FINDINGS>` |
| 38 | `R56W3RevDocsA2` | reviewer | `<FINDINGS>` | `<FINDINGS>` | `<FINDINGS>` |
| 39 | `R56W3RevLessonGate` | reviewer | `<FINDINGS>` | `<FINDINGS>` | `<FINDINGS>` |
| 40 | `R56W3RevEntryVerify` | reviewer | `<FINDINGS>` | `<FINDINGS>` | `<FINDINGS>` |
| 41 | `R56W3RevAnchorDeep` | reviewer | `<FINDINGS>` | `<FINDINGS>` | `<FINDINGS>` |
| 42 | `R56W3RevEntryCross` | reviewer | `<FINDINGS>` | `<FINDINGS>` | `<FINDINGS>` |
| 43 | `R56W3RevTrendAudit` | reviewer | `<FINDINGS>` | `<FINDINGS>` | `<FINDINGS>` |
| 44 | `R56W3RevLiveBoundary` | reviewer | `<FINDINGS>` | `<FINDINGS>` | `<FINDINGS>` |
| 45 | `R56W3ScoutRows1b` | scout | `<FINDINGS>` | `<FINDINGS>` | `<FINDINGS>` |
| 46 | `R56W3ScoutRows2b` | scout | `<FINDINGS>` | `<FINDINGS>` | `<FINDINGS>` |
| 47 | `R56W3ScoutRows3b` | scout | `<FINDINGS>` | `<FINDINGS>` | `<FINDINGS>` |
| 48 | `R56W3ScoutRows4b` | scout | `<FINDINGS>` | `<FINDINGS>` | `<FINDINGS>` |
| 49 | `R56W3ScoutRows5b` | scout | `<FINDINGS>` | `<FINDINGS>` | `<FINDINGS>` |
| 50 | `R56W3ScoutNewSrc1` | scout | `<FINDINGS>` | `<FINDINGS>` | `<FINDINGS>` |
| 51 | `R56W3ScoutNewSrc2` | scout | `<FINDINGS>` | `<FINDINGS>` | `<FINDINGS>` |
| 52 | `R56W3ScoutAdjacency` | scout | `<FINDINGS>` | `<FINDINGS>` | `<FINDINGS>` |
| 53 | `R56W3ScoutRouted` | scout | `<FINDINGS>` | `<FINDINGS>` | `<FINDINGS>` |
| 54 | `R56W3ScoutGoalState` | scout | `<FINDINGS>` | `<FINDINGS>` | `<FINDINGS>` |
| 55 | `R56W3ConnCrossSrc` | connector | `<FINDINGS>` | `<FINDINGS>` | `<FINDINGS>` |
| 56 | `R56W3ConnCrossClaim` | connector | `<FINDINGS>` | `<FINDINGS>` | `<FINDINGS>` |
| 57 | `R56W3SimplInstruments` | simplifier | `<FINDINGS>` | `<FINDINGS>` | `<FINDINGS>` |
| 58 | `R56W3ScribeGateA2` | scribe | `<FINDINGS>` | `<FINDINGS>` | `<FINDINGS>` |
| 59 | `R56W3ScribeRegistryA2` | scribe | `<FINDINGS>` | `<FINDINGS>` | `<FINDINGS>` |
| 60 | `R56W3ScribeLessonA2` | scribe | `<FINDINGS>` | `<FINDINGS>` | `<FINDINGS>` |
| 61 | `R56W3ScribeReportTables` | scribe | `<FINDINGS>` | `<FINDINGS>` | `<FINDINGS>` |
| 62 | `R56W3SentNewFiles` | sentinel | `<FINDINGS>` | `<FINDINGS>` | `<FINDINGS>` |
| 63 | `R56W3RevWatchTable` | revenger | `<FINDINGS>` | `<FINDINGS>` | `<FINDINGS>` |
| 64 | `R56W3RevFreezeBlind` | revenger | `<FINDINGS>` | `<FINDINGS>` | `<FINDINGS>` |

### Wave-w3 findings applied and routed

Applied at the attempt-2 tip: `<FINDINGS: what landed, with the seat that proved it>`. Routed to round 57:
`<FINDINGS: item, seat, why it cannot be closed here>`. Not applied (and why): `<FINDINGS>`.

## Gate (attempt 2)

The attempt-1 `## Gate` above stands as written; this block adds only what attempt 2 settles. No row in this block may be
admitted without (a) a located quote at a stated pin line of at most 25 words, (b) the bytes fetched twice
independently, and (c) the row's own 11-cell shape checked against the census.

### Admitted (attempt 2)

- **Row S396** — Linux man-pages 6.19 `inotify_add_watch(2)`, the kernel's one-watch-per-inode rule behind the watcher's
  duplicate-path and symlink watch rows. L1 draft byte values (NOT yet confirmed by an independent fetch):
  sha256 `98fe7feb381fa2687e8a3962e6d78a49cb1ad07c543f93449dcb42d6712c3d6d`, 11,345 B, 258 lines — pin
  `.ufo/waves/round-56/fetch/man7-inotify_add_watch.2.html` (untracked at the attempt-1 tip — commit reference `<FINDINGS>`);
  independent fetch result: `<FINDINGS: sha256 and byte count as re-measured, and the seat that measured it>`. Located quote: `<FINDINGS: quote text, exactly as the bytes have it, <=25 words>` at pin line
  `<FINDINGS: line>`. Why the lane lacked it: `<FINDINGS>`. Status/tier/used-by as landed:
  `<FINDINGS: queued | mined; tier; used-by cell>`. Independent second fetch: `<FINDINGS: seat, sha256 agreement>`.

| row | URL | access date | located quote | pin line |
|---|---|---|---|---|
| S396 | `https://man7.org/linux/man-pages/man2/inotify_add_watch.2.html` | 2026-10-30 | `<FINDINGS>` | `<FINDINGS>` |

- **Row S397** — Linux man-pages 6.19 `proc_pid_fdinfo(5)`, the `/proc` fdinfo fields the watch-table comparison reads.
  L1 draft byte values (NOT yet confirmed by an independent fetch):
  sha256 `f9e12387bf013d7c016f0015de5801932022a2fe6786d53e1cc84c385952d8a1`, 14,694 B, 366 lines — pin
  `.ufo/waves/round-56/fetch/man7-proc_pid_fdinfo.5.html` (untracked at the attempt-1 tip — commit reference `<FINDINGS>`);
  independent fetch result: `<FINDINGS: sha256 and byte count as re-measured, and the seat that measured it>`.
  Located quote: `<FINDINGS: quote text, exactly as the bytes have it, <=25 words>` at pin line `<FINDINGS: line>`. Why the
  lane lacked it: `<FINDINGS>`. Status/tier/used-by as landed: `<FINDINGS>`. Independent second fetch:
  `<FINDINGS: seat, sha256 agreement>`.

| row | URL | access date | located quote | pin line |
|---|---|---|---|---|
| S397 | `https://man7.org/linux/man-pages/man5/proc_pid_fdinfo.5.html` | 2026-10-30 | `<FINDINGS>` | `<FINDINGS>` |

- Other admissions attempt 2 makes: `<FINDINGS: none | list>`.

### Rejected (attempt 2)

Each rejection keeps its reason and names its flip condition, as attempt 1 did.

- `<FINDINGS: what was rejected>` — reason: `<FINDINGS>`. **Flip:** `<FINDINGS: the condition that would change this>`.

### Re-verification receipts (attempt 2)

The three frozen claims are re-run UNCHANGED at the attempt-2 tip; the frozen sentences are not re-opened by this block. A
null or failing result is a finding to record here, not a reason to edit the claim (a change that would move a frozen
predicate is a ROUTED finding for round 57).

| claim | frozen command | attempt-2 result line | seat | receipt |
|---|---|---|---|---|
| C1 | `python3 -I quality/counters/c1-r56-autoreload-entry.py --repo . --rev <rev> --work <scratch>` | `<FINDINGS>` | `<FINDINGS>` | `<FINDINGS: path>` |
| C1 controls | `python3 -I quality/check-r56-controls.py --claim c1 --repo . --rev <rev> --work <scratch>` | `<FINDINGS>` | `<FINDINGS>` | `<FINDINGS: path>` |
| C2 | `python3 -I quality/check-r56-controls.py --claim c2 --repo . --rev <rev> --work <scratch>` | `<FINDINGS>` | `<FINDINGS>` | `<FINDINGS: path>` |
| C3 | `python3 -I quality/counters/c3-r56-used-by.py --repo . --rev <rev> --work <scratch>` | `<FINDINGS>` | `<FINDINGS>` | `<FINDINGS: path>` |
| C3 controls | `python3 -I quality/check-r56-controls.py --claim c3 --repo . --rev <rev> --work <scratch>` | `<FINDINGS>` | `<FINDINGS>` | `<FINDINGS: path>` |
| tool selftest | `bash tools/mado-verify.sh --selftest` | `<FINDINGS>` | `<FINDINGS>` | `<FINDINGS: path>` |
| index | `python3 -I quality/check-index.py --repo . --rev <rev>` | `<FINDINGS>` | `<FINDINGS>` | `<FINDINGS: path>` |
| tool ledger | `python3 -I quality/check-tool-ledger.py --repo . --rev <rev>` | `<FINDINGS>` | `<FINDINGS>` | `<FINDINGS: path>` |
| census | `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin mado` | `<FINDINGS>` | `<FINDINGS>` | `<FINDINGS: path>` |

The attempt-2 L1 self-verification already on disk (`.ufo/waves/round-56/receipts/attempt2-l1.txt`) reports: C1
`rows=30/30 hosts=3/3 sources=30/30 scope=30/30 content=33/33 new_rows=8/8 verdict=TARGET_MET missed=none` and
`controls=12/12 verdict=OK`; C2 `fixtures=18/18 holdout=8/8 holdout_commit=ok controls=4/4 verdict=TARGET_MET`; C3
`entries=71 rows=332 missing=0 extra=0 dangling=0 conflict=0 stale=0 lost=0 exempt=24 verdict=TARGET_MET missed=none` and
`controls=9/9 verdict=OK` — all at scratch commit `d9b469e1b6d18e6f3dcb0bcface40c32de27c8fc` (a `git archive` export of the
attempt-1 tip, trees equal). That receipt also records a SETUP FAILURE worth keeping in the lesson: the C3 counter failed
closed (`rc=2`, "base revision objects are absent") and the C3 harness could not run control 1 until the frozen base
`13f0acbe3a15da2d9c08357a576d91dcadc85273` was fetched into the scratch repo. Attempt-2 wave seats re-ran the same three
claims independently; the table above carries their result lines, which this paragraph does NOT pre-empt:
`<FINDINGS: any difference between the L1's receipt and the seats' re-runs>`.

C3 caveat that the attempt-2 rows must not disturb: the C3 `extra` leg counts any `used-by` path outside the entry set, so
a lesson path in a `used-by` cell would flip `TARGET_MET` to `TARGET_MISSED` at the new tip. S396 and S397 therefore land
`queued` with `used-by —`, and flip `queued` to `mined` only in a later round that cites them from an entry (old→new logged
then). `<FINDINGS: the C3 counter's measured behaviour on the attempt-2 registry, from the seat that measured it>`.

### Outside spot-check (attempt 2)

Ready for the non-author closure: `<FINDINGS: what is offered, and what the closure is asked to rule>`. Attempt-1's offer
stands unchanged unless a seat below contradicts it.

## Registry changes (attempt 2)

The attempt-1 registry change (`319 → 332` rows, new ids S383-S395, cell 11 (`used-by`) edits on 23 pre-existing rows only,
full old→new table in `.ufo/waves/round-56/receipts/used-by-old-to-new.md`) STAYS as landed; attempt 2 does not undo it and
does not re-edit any of those 23 cells unless a wave seat proves one of them wrong — in which case the change is an
append-only correction with its own old→new line here. Attempt 2 adds two rows IF they land: `332 → 334`, new ids S396
(`inotify_add_watch(2)`) and S397 (`proc_pid_fdinfo(5)`), both `queued` with `used-by —`, both pinned to bytes fetched on
2026-10-30 and both counted by the census as new ids only. Attempt-2 old→new table:

| row | cell | old | new | why |
|---|---|---|---|---|
| S396 | (new row, 11 cells) | — | `<FINDINGS>` | queued; no entry cites it |
| S397 | (new row, 11 cells) | — | `<FINDINGS>` | queued; no entry cites it |
| `<FINDINGS: any existing row corrected in attempt 2>` | `<FINDINGS: cell number and name>` | `<FINDINGS>` | `<FINDINGS>` | `<FINDINGS: seat and evidence>` |

Rows in the registry after attempt 2: `<FINDINGS: 332 | 334, with the counting command and its output>`. Entries after
attempt 2: `<FINDINGS: count and command>`. `status`, `recheck` and every cell other than `used-by` on existing rows:
unchanged in attempt 2 — `<FINDINGS: confirm or correct>`. Census verdict after attempt 2: `<FINDINGS>`.

--- END APPEND BLOCK ---

## Fill map (scribe meta — not part of the append block)

| placeholder block | fill from |
|---|---|
| wave paragraph (seats reported / dead / results file / tip sha) | `.ufo/waves/round-56/w3/` report files; the operator's wave result file, if one is written |
| seat table `reported` column | presence of `.ufo/waves/round-56/w3/<Seat>.md` |
| seat table `dead` column | the operator's kill list for wave w3 (attempt 1's precedent: `R56W2MutC3Counter`, `R56W2MutC2Harness`) |
| seat table `lesson input` column | each seat's own report; `none` is a valid value |
| Gate S396 / S397 quote, pin line, byte hashes | `w3/R56W3ScribeGateA2/receipts/gate-draft.md`, `w3/R56W3ScoutNewSrc1/`, `w3/R56W3ScoutNewSrc2/`, the pins under `.ufo/waves/round-56/fetch/`, and `w3/R56W3RevLessonGate.md` (the pre-integration audit of the draft rows) |
| Gate S396 / S397 full 11-cell rows | `w3/R56W3ScribeRegistryA2/` (drafted rows) and `.ufo/waves/round-56/attempt2/s396-s397-draft.md` |
| Gate rejections | `w3/R56W3RevLessonGate.md`, `w3/R56W3ScoutRouted.md`, and the wave-3 critic seats |
| re-verification table | `w3/R56W3ExecReverifyC1/`, `…C2/`, `…C3/`, `w3/R56W3ExecHarmWatch/`, `w3/R56W3ExecBaseBefore/`, `w3/R56W3CritCensus.md`, `w3/R56W3ExecWaveEvidence/` |
| C3 caveat sentence (registry behaviour with the new rows) | `w3/R56W3ExecProbeC3NewRows/receipts/c3-newrows-a2.txt` |
| registry old→new table | the census run after the rows land (`sources-census.sh validate --root /home/vgpnk/Projects/shokunin mado`) and the C3 counter run at the attempt-2 tip |
| routed-to-round-57 list | attempt 1's `## Wave-2 findings applied and routed` section plus the wave-3 seats that re-attacked those items |
| owed round-55 lesson correction | `w3/R56W3ExecInherited/corrections/round-55-append.md` (belongs in `corpus/lessons/round-55.md`, NOT in this file) |

**Do not fill:** anything the waves did not measure. A placeholder stays a placeholder and is reported as "not settled in
attempt 2" rather than being written from inference.
