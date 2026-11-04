# R85ScribeLesson — round-85 lesson

Seat: scribe. Lane root `/home/vgpnk/Projects/shokunin/mado-shokunin`.
Freeze revision `3905311c75a39c5710413105865c0a1a7dd0116a`; base
`5f174ca48d4f9cf94abf1a8c58b7d6f88733aced`; successor `d7c40e6d1b9a7476f2ff48254d577799ce9901e4`.
Scratch `/fast/scratch/hyaku/mado-r85/R85ScribeLesson` (removed before yield).

## What was written

`corpus/lessons/round-85.md` (26,725 B, 190 lines at handoff). Nothing else in the lane was written
by this seat. No git mutation, no tool install, no pacman transaction, no subagent dispatch, no
sibling write, no operator/fleet-root/`MANIFEST.json` touch.

The lesson has the contract's sections: `## Mistakes` (10 mined rows, class · evidence pointer ·
captured-by · fix shown able to fail), `## Gate` (every new SOURCES row opened this round with URL,
access date, a located ≤25-word quote, scope and tier; three rejects with reasons and flip
conditions; the registry old→new table), `## Considerthese` (proposal 2, mined and grounded by
measurement), and the domain-share line.

## SOURCES rows the L1 must add (and the used-by pointers)

The registry rows are already in the working `corpus/SOURCES.md` (L1 owns that file; this seat did
not edit it). Exact state as measured against base `5f174ca4` — **422 rows → 425 rows**:

| row | id | kind / tier / status | opened | recheck | used-by |
|---|---|---|---|---|---|
| new | **S488** | POSIX.1-2024 Shell Command Language — https://pubs.opengroup.org/onlinepubs/9799919799/utilities/V3_chap02.html — spec / A / mined | 2026-11-04 | 180d | `corpus/knowledge/runbook-status-classes-r85.md, corpus/lessons/round-85.md` |
| new | **S489** | Bash maintainer Reference Manual — https://tiswww.case.edu/php/chet/bash/bashref.html — docs / A / mined | 2026-11-04 | on-release | `corpus/knowledge/runbook-status-classes-r85.md, corpus/lessons/round-85.md` |
| new | **S490** | Bash maintainer Reference Manual exit builtin — …#Bourne-Shell-Builtins — docs / A / **rejected** | 2026-11-04 | 180d | `corpus/lessons/round-85.md` |

Old-row cells changed (used-by only; `status`, `recheck`, `opened` unchanged on every pre-existing
row) — this is the exact old→new the L1 asked to be logged:

- **S486** used-by
  old: `corpus/knowledge/bar-footprint-namespace-discipline-r84.md, corpus/lessons/round-84.md`
  new: `corpus/knowledge/bar-footprint-namespace-discipline-r84.md, corpus/lessons/round-84.md, corpus/knowledge/bar-footprint-identity-causes-r85.md`
- **S487** used-by
  old: `corpus/knowledge/runbook-producer-status-r84.md, corpus/lessons/round-84.md`
  new: `corpus/knowledge/runbook-producer-status-r84.md, corpus/lessons/round-84.md, corpus/knowledge/runbook-status-classes-r85.md`

**Correction the L1 must land append-only:** the round's `LOG.md:4175` sentence "Registry422→425;
old cells unchanged" is no longer accurate — S486 and S487 used-by cells *did* change (by append).
The lesson records the two rows and the exact old→new strings; the LOG sentence needs an appended
correction naming them.

## Quotes (each read from the committed pins, none invented)

- **S488** (pinned `fetch/S488.bin`, 357,953 B, sha256 `0889867a…`): "The exit status of the last
  (rightmost) command specified in the pipeline." — 12 words, bytes **133030–133104**, §2.9.2
  Pipelines → Exit Status table, row *pipefail = no, no `!`*. Re-verified byte-exact by this seat
  (tag-stripped, whitespace-normalised == the quote).
- **S488, second clause**: "Otherwise, if the command terminated due to the receipt of a signal, the
  shell shall assign it an exit status greater than 128." — 23 words, bytes **109001–109128** (one
  raw newline between "status" and "greater"). Re-verified byte-exact. POSIX says **>128**, not
  `128+N`.
- **S489** (pinned `fetch/S489-alt-tiswww.bin`, 1,040,870 B, sha256 `b91026ac…`): "When a command
  terminates on a fatal signal whose number is N, Bash uses the value 128+N as the exit status." —
  21 words, bytes **239046–239200**. The raw span carries `<var class="var">N</var>`; dropping the
  tags without leaving whitespace gives the quoted form, and a whitespace-collapsing strip of the
  same span gives "N ," / "128+ N" — the same bytes, 24 tokens. Both forms are recorded.
- **S490 (rejected)** (same pin): "Exit the shell, returning a status of n to the shell's parent." —
  12 words, bytes **266270–266361**. Reason: `exit 141` returns the same number as signal-13
  death, so a numeric status cannot prove the termination cause. Flip: separately observed
  termination metadata.

The GNU URL named by the frozen declaration was **not** pinned (5 attempts, curl rc 28, TCP connect
timeout on both resolved addresses); the pins file records that endpoint under its own key with no
bytes, and no quote is taken from it. The S489 registry row is the maintainer copy that was actually
opened.

## Mistakes mined (10 rows)

Required three, all mined with the corrections the L1 stated:

- **M85-1 survivor** — round-84's stage-only refusal binding. Evidence
  `corpus/lessons/round-84-verifier-spotcheck.md:108` and the r84 scorer's
  `quality/counters/c1-r84-namespaces.py:272-287` (stage test only, no cause term). Captured-by
  QUALITY 141. Fix shown able to fail: the r85 cause clause and the `cause-dropped` mutant; the
  wrong-reason tool still scores 72/72 because `alloc-negative` has no cause-bound witness.
- **M85-2 number-drift** — the declaration's C2 ancestry sentence claims **nine** round-84 mutants
  were dropped; AST enumeration of both frozen counters shows **one** dropped (`rc-blind`),
  28 carried with byte-identical anchors, 9 new. Captured-by none (QUALITY 137 binds the count, not
  the ancestry). Fix shown able to fail: the dropped anchor occurs 0× in the r85 counter.
- **M85-3 attribution** — round-84's R3 receipt-attribution defect, still open
  (`receipts/frozen-input-crosswalk-r85.json` says its scope is identity, not chronology; the
  successor counter still prints `tree=bound`). Captured-by none. Fix shown able to fail: the
  score receipt prints input sha256 at both revisions and states the C2 counter's own sha changed
  between observations.

Seven more mined from this round's own evidence: the four C2 survivors (M85-4), the C1 cause-flood
hole (M85-5), `128+N` vs `exit 141` (M85-6), the frozen C2 setup refusal and the round-84 heading
that yields 0 rows (M85-7), the declaration's §2.9.3/§3.7.6 locator drift and the unreachable GNU
endpoint (M85-8), the red instrument-ledger gate at the freeze (M85-9), and the `shapes=26/26`
reading (M85-10).

## Considerthese

**Proposal 2** ("check whether a claim stands when its wave-done receipt is red") — still
unimplemented, now grounded by measurement rather than a pointer. This seat ran the lane's own
`quality/check-wave-done.py` over rounds 57–84 at `d7c40e6d`: `verdict=MISSING` for exactly
**71, 79, 81, 83** (11, 1, 5 and 3 blank seats), `OK` for the rest. `SCORECARD.md` publishes
"improved" claim rows for 71, 79 and 81 and "measured target met; outside closure pending" for
round 83's C2 — four rounds with a published claim verdict over a red wave receipt. QUALITY 102/103
bind the *report*, not the *published claim row*; `quality/check-wave-done.py` is the only file in
the lane that mentions wave-done, so nothing couples the two. The lesson states the first
implementation (a check that each round with a published claim row has `verdict=OK`) and its
failure case (it must report those four reds today).

Proposal 1 was mined in round 84 and is not re-adopted. Assimilation: none.

## Domain-share line

Two new entries, both desktop-surface: `knowledge/bar-footprint-identity-causes-r85.md` (which
layer-surface declaration the join refuses, and under which cause) and
`knowledge/runbook-status-classes-r85.md` (what status a read-only runbook row's producer must
report, and how a guarded pipeline propagates it). The lane's harness-side learning (QUALITY
140–142, the counter repairs, the four survivors) is lane-internal and is deliberately not counted
as knowledge.

One measured caveat recorded in the lesson: the lane's own domain/meta counter
`quality/ratio-domain-meta.py` cannot see rounds 84 and 85 — its heading pattern is
`^##\s+Round\s+(\d+)` (`:61`) while `SCORECARD.md:4912`/`4967` are titled `## Round84 …` /
`## Round85 …` without the space, so `--from 84 --to 85` prints `domain=0 meta=0 window=84-85
default=0` while `--from 83 --to 85` prints four rows, all from round 83. The count above is
therefore a curation judgement over `corpus/knowledge/`, not a tool output. The heading drift is
reported here for the L1; no SCORECARD edit was made by this seat.

## Verification actually run by this seat

- `python3 -I quality/check-tool-ledger.py --repo . --rev 3905311c…` → `population=156
  ledger_rows=154 uncovered=2 … verdict=TARGET_MISSED` (the freeze's red).
- `python3 -I quality/check-tool-ledger.py --repo . --rev d7c40e6d…` → `ledger_rows=156 uncovered=0
  bad_pointer=2` — the two new ledger rows point at `corpus/lessons/round-85.md`, which is not in
  that revision's tree; the checker scores committed blobs only, so the pointer resolves when this
  lesson is committed.
- `python3 quality/check-wave-done.py --repo . --rev d7c40e6d… --round N` for N = 57…84 → MISSING
  at 71, 79, 81, 83; OK elsewhere.
- `python3 quality/ratio-domain-meta.py --repo . --rev d7c40e6d… --from 84 --to 85` → `domain=0
  meta=0 window=84-85 default=0`; `--from 83 --to 85` → four rows, all from round 83.
- `python3 -I quality/check-locators.py --fetch .ufo/waves/round-85/fetch corpus/lessons/round-85.md`
  → `CHECK_LOCATORS: locators=0 miss=0`.
- AST enumeration of both frozen counters (round-84 vs round-85 mutant lists and their
  anchor/replacement pairs), and byte-span re-verification of every quote against the pinned
  bytes.
- The frozen C2 control's `version` row read back from the freeze blob and from the working file:
  value `^Hyprland [0-9]+\.[0-9]+\.[0-9]+ built from branch \S+ at commit [0-9a-f]{7,40} clean
  \([^)]*\)\.$` with `anchor: line`, and `omarchy-version` `^[0-9]+\.[0-9]+\.[0-9]+$` — the strict
  anchored form, identical on both sides, with the control file byte-identical to the freeze
  (`sha256 de8a68fe…`). The lesson now states that value, so the two anchor-mutant survivors
  (M85-4) are explained from the frozen bytes rather than left implicit.
- Registry delta computed by diffing the parsed row table of `git show 5f174ca4:corpus/SOURCES.md`
  against the working file (422 → 425 rows; only the two used-by cells differ among old rows).

**Not run by this seat:** the two round-85 counter batteries (run by `R85ExecScore` and the
reviewers; quoted as evidence-verified), the census end-run, the outside-lane admit/reject
spot-check, and any promotion review. No tool was installed; pacman stays paused; no fleet-root,
sibling-lane, operator, `.ufo/state/`, `.scratch/` or `MANIFEST.json` file was written.

## Files

- `corpus/lessons/round-85.md` (the lesson — the only lane file this seat wrote)
- `.ufo/waves/round-85/w1/R85ScribeLesson.md` (this report)
