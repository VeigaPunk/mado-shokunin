# R56W3ScoutRouted — routed-defect sweep (round 56, wave 3, attempt 2)

Seat: `R56W3ScoutRouted` (scout, leaf member, no subagent dispatch).
Scored tree: lane tip `0f3a54361a9824484d0801679ceb1fd8ac7c32e1` (= content revision `8a7b734627b06583a9106fcc0940f0a180ff331d` + attempt-1 receipts/LOG/SCORECARD/lesson).

**Deliverable (the table):** `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-56/w3/R56W3ScoutRouted/receipts/routed-a2.md`
**Receipts:** `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-56/w3/R56W3ScoutRouted/receipts/routed-a2-instruments.txt`

Report: `.ufo/waves/round-56/w3/R56W3ScoutRouted.md`

## What I attacked

The lane's own record: every defect that a lesson or a verifier spot-check **routed to a later round**, checked for whether it landed by `0f3a5436`. Sources read in full:

- `corpus/lessons/round-49.md` … `round-56.md` (8 lessons, whole files)
- every `corpus/lessons/round-*-verifier-spotcheck.md` (44 files, r12→r55) — the routed section of each, header-matched
- the errata blocks the lessons cite, `registration-v2.md` (E1–E11) and `registration-v2-errata.md` (E12–E14)
- `.ufo/waves/round-56/w2/*.md` (33 wave-2 seat reports) — routed/findings/survivor sections
- the lane's own routed-defect ledger `.ufo/waves/round-46/w1/ScrRoutedAges/ages.md` (42 rows, r38–r45), which QUALITY 90 names as the first instance of the ledger rule

## What I did

Read-only. No lane file edited, no git/jj mutation of any kind, no dispatch, no task/background job, no write outside my seat directory and my scratch. Every claim in the table is backed by either a named committed artifact or a one-line check I actually ran; the decisive lines are quoted in the table's last column.

Method: `git archive 0f3a5436 corpus/lessons` into scratch → extract routed sections → map each defect to its owner round → verify landing with `git show`/`git ls-tree`/`git grep` at named revisions, or `grep`/`ls`/`test -f` on the working tree (whose tracked bytes equal the tip: `git diff --stat 0f3a5436 -- corpus/lessons` is empty), or a read-only gate under `--work` in scratch.

Format follows the lane's own precedent (`ages.md`, QUALITY 90): `id | defect | routed at | owner round | landed by tip? | evidence`.

## The table in one paragraph

Routed items land at four different rates. Items routed to the round that immediately follows land (r49→r50 through r55→r56: the QUALITY criteria, the errata entries, the counter rebuilds, the freeze-order instrument, the wave-done receipt — all landed). Items routed **across** rounds do not: the ages ledger's durable open queue (R38-3, R38-4, R40-2, R40-3, R41-2/3a/3b/4, R44-D7, R45-D2, R45-D3, R45-D5) is still open at 6–12 rounds. The **r56→r57** items are all open, as the round's own SCORECARD says. And several r56 wave-2 findings were closed **between the wave-2 report and the tip commit** — the entry's `mktemp -d`, the superseded divergence list, the C3 wording, the old→new log, the after-inventory receipt — so a wave-2 report alone is not a list of open items.

## Defects found (severity relative to the round-56 claims)

**Blocking the claim:** none found. The three frozen claims still measure as the receipts say (`MADO_AUTORELOAD_ENTRY … TARGET_MET`, `MADO_R56_C2 … TARGET_MET`, `MADO_USED_BY … TARGET_MET`, `MADO_R56_CONTROLS c1 12/12 c2 4/4 c3 9/9` — `.ufo/waves/round-56/receipts/at-final.txt`).

**Weakens the claim (open at tip):**

1. **C1 is entailment-blind.** A 33-row template proposition, a fully negated entry, a neighbour shift and a hand-written set of ten false propositions all reach `TARGET_MET` with `content=33/33` (`w2/R56W2CritC1Forge.md` J1b / B2 / T2b / T5). The r56 counter has no entailment leg. This is the round's declared limit, not a hidden defect, but it is the largest single item in the r57 plan.
2. **The `scope:` bound is off by one against the pin's true line count** (`w2/R56W2CritC1Forge.md` T4a/T4b): `ConfigWatcher.cpp` has 111 newline-terminated lines, the counter's bound is `len(blob.split(b"\n"))` = 112, so an anchor one line past the end is accepted. The bound is the counter's own E3 rule.
3. **The C2 sandbox silently degrades.** `quality/r56_ctl_c2.py` falls back to an unsandboxed run when `bwrap` is absent, in which state the export directory (holding every fixture's `expected.out`/`expected.rc`/`note.txt`/`args.json`) is reachable; the seat measured a fid-deriving scanning tool at **15/18 committed + 7/8 hold-out** without bwrap (`w2/R56W2ConnCross.md` T2-10). The staged-path names also differ from E6's frozen text in three ways.
4. **The C2 hold-out was revealed before the wave that attacks it.** Reveal commit `2e39282e` (21:54:28) precedes the wave-2 dispatch `19be88b6` (22:04:27) (`w2/R56W2ScribeRecords.md` D5), so the wave-2 "hold-out attack" cannot count as one.
5. **`check-freeze-order.py` cannot see the v2 contract files.** `grep -cE "registration-v2\|claims-frozen-v2\|frozen-tables-v2\|c3-name-only" quality/check-freeze-order.py` → **0**; the script's `REQUIRED`/`OPTIONAL` tuples name only v1 (`quality/check-freeze-order.py:36-37`). A post-launch edit to `registration-v2.md` still reads `verdict=OK` (`w2/R56W2RevHarmWatch.md` D4). This is the M55-1 instrument itself, blind to half the round-56 freeze.
6. **The C3 harness's population is ungated.** `judge_good` does not compare `entries`/`rows` against the harness's own 71/328: a green counter printing `entries=0 rows=0` scores `good=ok` (`w2/R56W2MutC3Harness.md` D2, probe `receipts/07-population-probe.txt`). Fourteen non-equivalent harness mutants survive. The harness's own "independent" model reports `missing=24` on the GOOD tree while the counter reports `missing=0` (D4), so its `missing` effectiveness baseline is 24, not 0.
7. **The `check-index.py` gate has still no registry row of its own.** The r30/r31 requirement was satisfied only by a *mention* inside the `mado-axis-scores` row's cells (`SKILL.md:770`); `awk '/^## Gate registry/,/^## [^G]/' SKILL.md | grep -E "^\| " | grep -c "check-index.py"` → 1 (that same row), and no `mado-index` row exists.
8. **The session-material gate is still red and its finding count grew**: `check-session-material.py --rev 0f3a5436` → `findings=274`, exit 1 (97 at r45, 115 at r46, 159 at r48).
9. **The r55 lesson correction was never appended.** `corpus/lessons/round-55.md:25` still says `Rows 314 → 317` and `:42` still says `(317 rows)`; `grep -niE "errata\|correction\|appended" corpus/lessons/round-55.md` → **0**; `git log 13f0acbe..0f3a5436 -- corpus/lessons/round-55.md` → **empty**. The registry now holds 332 rows, so the stale sentence is two rounds further out of date than when the r55 spot-check routed it.

**Cosmetic:** stale harness docstrings (`r56_ctl_c1.py:6,23` say "ten"/`k=10` while `N_CONTROLS=12`; `r56_ctl_c3.py:6,19` say "six"/`k=6` while 9; `check-r56-controls.py:8` cites v1 `claims-frozen.md`; the C1 counter docstring names `PRED-C1-r56`, not `-v2`); the C3 base receipt's field set differs from the frozen sentence; the r54 seat sidecars still absent.

**Operator-owned (not lane-actionable):** all four SHONEN boxes `[~]` (`SHONEN.md:5,7,9,11`, last touched `7cd7f331` 2026-10-15 — 41 rounds); the r52/r53 L0 questions; the r34 package id remap.

## Things that did not run / could not be verified

- **The two killed wave-2 seats** (`R56W2MutC3Counter`, `R56W2MutC2Harness`) produced no report, so no routed item exists for them; nothing in this sweep can speak to what they would have routed.
- **Table 12 (spot-checks r12–r37) is coarser** than Tables 1–11: those items are closed by recorded pointers in later lessons, and I did not re-derive each of their ~120 individual bullets with its own command. The ages ledger (`ages.md`) covers r38–r45 with the same method and is the lane's own precedent; Tables 1–11 and 13 are the per-item, per-check part.
- **I did not re-run any counter, harness or gate** except three read-only instruments under `--work` in scratch (`check-axis-scores.py`, `check-session-material.py`, and the `ls`/`grep`/`test -f` probes), because the seat's job is the record, not the claims.
- **Semantic truth of any lesson's claims was not assessed** — out of scope for a routed-defect sweep.
- **R45-D2's serial identity** could not be re-derived: the serial string I searched for (`9EKLQ`) does not occur in `corpus/knowledge` at tip, so I could not reproduce the "3 held entries + 21 wave files" count; the absence of any `M45-2` correction in r46–r56 is the evidence I report instead.
- **Tooling:** nothing installed or upgraded by this seat; the pacman guard was not invoked; no `~/.local/bin` or PATH write.

## Cleanup

Scratch `/fast/scratch/hyaku/mado-r56/R56W3ScoutRouted/` (the archived lesson tree, the two extraction files `routed-sections.txt` and `w2-next.txt`, and the gate work dirs) was removed after the receipts were copied into the seat directory. No lane working-tree file was modified: `git status --porcelain` in the lane shows only the untracked attempt-2 and w3 artifacts that were already there plus my own seat directory.

## Tooling record

Per the operator's tooling authorization and the pacman pause: **no install or upgrade was performed by this seat** — the task needed none (all evidence is `git` plumbing, `grep`/`ls`/`test -f`, and two read-only Python gates). No pacman transaction was issued, so no update-safety gate was entered.
