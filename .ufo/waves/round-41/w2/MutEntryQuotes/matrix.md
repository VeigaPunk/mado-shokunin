# MutEntryQuotes — single-token mutation matrix of the round-41 DATA bytes

Seat: MutEntryQuotes (wave w2, mado round 41, hyaku run 7, 2026-10-25).
Target revision: `07f2641696b5ac73de1404ea737a9f27e9819aa1` (base `ab2bfaab661c846d1de9d58c01651cd156a13949`).
Detector: `quality/counters/c2-r41-focus-entry-v2.py` (PRED-C2-r41-v2), run from a scratch clone at
`/tmp/mutentryq/clone` (never the lane). Driver: `mutate.py` (this directory). Results: `results.json`,
`review.json` (this directory). Reviewer script deliverable: `reviewer_check.py` (this directory).

## Method

1. Baseline: the pristine DATA tree scores `PRED-C2-r41-v2: admitted=1/1 verdict=TARGET_MET` — detector valid.
2. 53 single-token mutants (one logical edit, or one cell-pair swap, per mutant) were applied one at a time
   to `corpus/knowledge/hyprland-focus-grab-r41.md`, `corpus/SOURCES.md` (rows S283–S289, S037),
   `corpus/README.md` (r41 index row) and `corpus/lessons/round-41.md` (`## Gate`), committed in the
   scratch clone, scored with the counter, and reverted (worktree bytes restored from pristine copies
   after every run; restoration evidence below).
3. Every survivor was re-scored by `reviewer_check.py` — the scriptable part of a human-style review —
   run against the mutant tree; a survivor counts as "caught" only if it introduces a violation the
   pristine bytes do not have.

## Result

**43 of 53 mutants are still ADMITTED by PRED-C2-r41-v2.** All 10 controls were killed by their
expected clauses (b, h, g, c×3, f, d+g×2), so the survivors are genuine predicate blind spots, not a
broken harness. The reviewer script catches 36 of the 43 survivors mechanically; 6 are true human-only
findings and 1 is a repair.

## F-1 — DATA defect found in the landed bytes (pre-existing, counter-blind)

`corpus/SOURCES.md:235` (row S286, scope cell) says the portal binds "which **nine** it binds", and its
anchor cell lists nine branch names — but the pinned receipt has **ten** `INTERFACE ==` bind branches
(`zwlr_foreign_toplevel_manager_v` is missing from the list). The entry (§3, line 69) correctly says
"a fixed set of **ten** named branches", so the registry row contradicts both the entry and the receipt.
Reproduction:

```
git -C <lane-or-clone> show 07f2641:corpus/SOURCES.md | sed -n 235p   # "...which nine it binds..."
git -C <lane-or-clone> show 07f2641:.ufo/waves/round-41/fetch/xdph-PortalManager.cpp \
  | grep -o 'INTERFACE == [a-z_]*' | sort -u                            # 10 branches
```

The registry's own mutant R11 ("nine" → "ten") is the only edit in the sweep that makes the row agree
with its receipt — corroborating that the landed "nine" is the defect. Per the round contract this is a
DATA finding: the L1 should fix the S286 scope/anchor cells (ten branches; add the foreign-toplevel
name) before the round lands.

## F-2 — Coverage finding: what the predicate cannot protect

The 43 admitted mutants, by class:

- **prose numbers (14 admitted)** — every free prose number in the entry/README/lesson that is not a
  quote, locator, version, date or pid passes the counter. 12 of 14 are receipt-checkable and the
  reviewer script catches them (journal census, slice adverts, distinct names, focus occurrences,
  receipt byte sizes/line counts, branch count, grep exit code); `recheck: 90d → 95d` is caught only
  weakly (novel recheck class vs BASE vocabulary).
- **receipt metadata numbers in registry anchors (11 admitted)** — byte sizes, line counts and sha256
  prefixes of receipts cited in `SOURCES.md` anchor cells are completely unchecked by the counter;
  all are trivially script-checkable against the committed receipts (C2-size, C2-sha, C1-reg-lines).
- **OBS → INF flips (7 admitted)** — flipping a body `**OBS**` label to `**INF**` never changes the
  verdict (clause g only needs the id and quote on the line). 5 of 7 body flips are caught by the
  lane convention "OBS lines carry verbatim quotes, INF lines do not" (C4-inf-quote); the §6
  decision-table state cell is catchable only when the pointed section is unambiguous (E17, E19 caught;
  E16 escapes because §1 contains both an OBS and an INF line naming S283).
- **table cell swaps (5 admitted, 1 killed)** — swapping kind/tier cells in registry rows or
  request/event kind cells in the entry's §1 table passes; only S289's `own-work` swap dies (clause h).
  Kind/tier vocabulary catches R01/R02; the request/event table is catchable against the XML receipt
  (C10); tier grade swaps between A and B are human-only.
- **recheck scalars (2 admitted)** — `90d→95d` (entry) and `on-release→on-sunday` (held row S037,
  whose recheck cell the held-row rule never compares) pass; both flagged only as vocabulary-weak.
- **Gate ADMIT/REFUSE path swaps (2 admitted)** — the ADMIT target may be any of the 13 staged paths
  (counter clause i does not bind it to the entry's `assimilated-from` line); L04 is caught by
  C5-admit-from. Swapping which *extra* file a REFUSE names (L05) is semantic, human-only.
- **lesson prose (6 admitted)** — the Gate prose's receipt byte counts, journal line count, receipt
  census ("seven pre-wave receipts") and lesson cross-references (M41-6) are all unchecked; all but
  the M41-ref are scriptable against receipts/freeze tree.

### Escapes (survivors no committed-evidence script can convict)

| id | mutation | why script-resistant |
|---|---|---|
| E10 | assimilated-from "sections 1, 2 and 4" → "and 5" | staged `focus-control-surfaces-r28.md` has §1–§5, so the wrong section claim is provenance intent, not a dangling reference |
| E16 | §6 row-1 state OBS → INF | the pointed section holds both an OBS and an INF line naming the same id |
| R15 | S288 "HTTP 200" → "HTTP 201" | the fetch status exists only in `w1/ScrRowsDraft/rows-block.txt`, which is not committed at REV (weak cross-artifact check possible) |
| R16 | tier swap S283 "A" ↔ S285 "B" | grades are recorded judgment with no machine-readable record |
| L05 | REFUSE target r29 → r13 | the reason text stays bound to r29's story; r29 was an extra refusal outside assimilated-from |
| L06 | lesson ref "M41-6" → "M41-7" | `M41-7` already occurs in `w1/ScrLessonSkeleton.md`, so an existence check cannot discriminate |

(R11 is the seventh non-caught survivor — because it *repairs* F-1.)

## Reviewer script

`reviewer_check.py` (this directory) — pure-read, ~13 checks (C1–C12): census numbers, receipt sizes /
sha256 / line counts in anchors and lesson prose, freeze-receipt count, OBS/INF quote discipline, §6
state-vs-body consistency, ADMIT ↔ assimilated-from binding and disposition completeness, round
coherence, registry kind/tier/recheck vocabulary vs BASE, bind-branch count, grep exit code, XML table
kinds, M41-ref existence. Run:

```
python3 reviewer_check.py --repo <clone-root> [--rev 07f2641...] [--tree <mutant-dir>]
```

On the pristine DATA bytes it reports exactly one violation — F-1 above. On a mutant tree it prints
`FAIL <check>` lines for every scriptable survivor. All checks derive from committed evidence
(receipts at REV, the freeze commit `60c3914`, BASE registry) plus read-only w1 artifacts for C11.

## Full matrix (53 mutants)

| id | file:line | mutation | counter | reviewer |
|---|---|---|---|---|
| E01 | entry:14 | header 'Round: 41.' -> 'Round: 42.' | ADMITTED | script: C6-round |
| E02 | entry:67 | slice-session adverts 15 -> 16 (checkable vs journal) | ADMITTED | script: C1-slice-adverts |
| E03 | entry:131 | census bullet 'two portal sessions' -> 'three' | ADMITTED | script: C1-sessions |
| E04 | entry:69 | bind-branch count 'ten named branches' -> 'nine' (checkable vs receipt) | ADMITTED | script: C8-entry-branches |
| E05 | entry:71 | grep exit code 'exits 1' -> 'exits 2' (checkable vs receipt) | ADMITTED | script: C12-exit-code |
| E06 | entry:71 | 'occurs exactly once' -> 'exactly twice' (checkable vs journal) | ADMITTED | script: C1-focus-occurrences |
| E07 | entry:67 | latest-session distinct names 63 -> 62 (checkable vs census/journal) | ADMITTED | script: C1-distinct |
| E08 | entry:65 | first-session adverts 'with 15 adverts' -> '14' | ADMITTED | script: C1-slice-adverts-2 |
| E09 | entry:12 | entry recheck 90d -> 95d (any \d+d passes) | ADMITTED | script: C7-entry-recheck-vocab(weak) |
| E10 | entry:15 | assimilated-from 'sections 1, 2 and 4' -> 'and 5' | ADMITTED | human: provenance intent (staged r28 has §1–§5, so "sections 1,2,5" is not a dangling ref) |
| E11 | entry:19 | §1 first OBS (S283) -> INF | ADMITTED | script: C4-inf-quote |
| E12 | entry:45 | §2 CFocusGrab::start OBS -> INF | ADMITTED | script: C4-inf-quote |
| E13 | entry:61 | §3 journal census OBS -> INF | ADMITTED | script: C4-inf-quote |
| E14 | entry:87 | §4 quickshell sync OBS -> INF | ADMITTED | script: C4-inf-quote |
| E15 | entry:97 | §5 issue-565 body OBS -> INF | ADMITTED | script: C4-inf-quote |
| E16 | entry:115 | §6 decision-table state cell OBS -> INF (row 1) | ADMITTED | human: §1 holds BOTH an OBS and an INF line naming S283, so table-state is genuinely ambiguous to a script |
| E17 | entry:125 | §6 decision-table state cell OBS -> INF (last row) | ADMITTED | script: C4-table-state |
| E18 | entry:27 | §1 interface table: add_surface kind 'request' <-> cleared 'event' | ADMITTED | script: C10-table-kind |
| E19 | entry:120 | §6: 'Does the portal use it?' OBS <-> 'Who binds it' UNK | ADMITTED | script: C4-table-state |
| X01 | entry:11 | verified-at 2026-10-25 -> 2026-10-24 (control) | KILLED (clause b) | — |
| X02 | entry:63 | census sessions=2 -> 3 (control) | KILLED (clause h) | (also C1-census-line) |
| X03 | entry:61 | S289 line quote (ver 1) -> (ver 2) (control) | KILLED (clause g) | — |
| R01 | SOURCES.md:232 | S283 kind 'spec' <-> tier 'A' | ADMITTED | script: C7-kind,C7-tier |
| R02 | SOURCES.md:233 | S284 kind 'code' <-> tier 'A' | ADMITTED | script: C7-kind,C7-tier |
| R03 | SOURCES.md:238 | S289 kind 'own-work' <-> tier 'A' (control) | KILLED (clause h) | (C7 flags too) |
| R04 | SOURCES.md:232 | S283 anchor '5447 B' -> '5448 B' | ADMITTED | script: C2-size |
| R05 | SOURCES.md:234 | S285 anchor '2568 B' -> '2560 B' | ADMITTED | script: C2-size |
| R06 | SOURCES.md:235 | S286 anchor '24182 B' -> '24128 B' | ADMITTED | script: C2-size |
| R07 | SOURCES.md:236 | S287 anchor '475170 B' -> '475071 B' | ADMITTED | script: C2-size |
| R08 | SOURCES.md:237 | S288 anchor '1903 B' -> '1904 B' | ADMITTED | script: C2-size |
| R09 | SOURCES.md:238 | S289 anchor '19130 B' -> '19131 B' | ADMITTED | script: C2-size |
| R10 | SOURCES.md:238 | S289 anchor '153 lines' -> '152 lines' | ADMITTED | script: C1-reg-lines |
| R11 | SOURCES.md:235 | S286 scope 'which nine it binds' -> 'ten' | ADMITTED | REPAIR — fixes F-1 |
| R12 | SOURCES.md:49 | S037 (held) recheck 'on-release' -> 'on-sunday' | ADMITTED | script: C7-recheck-vocab(weak) |
| R13 | SOURCES.md:232 | S283 anchor sha256 '0bc60c14' -> '0bc60c15' | ADMITTED | script: C2-sha |
| R14 | SOURCES.md:234 | S285 anchor sha256 '6f7cecf1' -> '6f7cecf2' | ADMITTED | script: C2-sha |
| R15 | SOURCES.md:237 | S288 'HTTP 200' -> 'HTTP 201' | ADMITTED | weak script: HTTP 200 recorded only in w1/ScrRowsDraft/rows-block.txt (not committed at REV) |
| R16 | SOURCES.md:232 | tier swap S283 'A' <-> S285 'B' | ADMITTED | human: tier grades A/B are recorded judgment, no machine-readable record |
| X04 | SOURCES.md:232 | S283 status mined -> raw (control) | KILLED (clause c) | — |
| X05 | SOURCES.md:49 | S037 used-by drops the entry (control) | KILLED (clause c) | — |
| X06 | SOURCES.md:232 | S283 opened 2026-10-25 -> 2026-10-24 (control) | KILLED (clause c) | — |
| M01 | README.md:70 | README r41 row: Note cell <-> Holds cell | KILLED (clause f) | — (clause f's line-prefix match) |
| M02 | README.md:70 | README row '63 globals' -> '62' (checkable vs census) | ADMITTED | script: C1-readme-globals |
| M03 | README.md:70 | README row 'one focus-grab manager advert' -> 'no' | ADMITTED | script: C1-readme-adverts |
| M04 | README.md:70 | README row 'issue 565' -> 'issue 564' (checkable vs S287 locator) | ADMITTED | script: C9-issue |
| L01 | lesson:38 | Gate prose S037 receipt '1442 B' -> '1443 B' | ADMITTED | script: C2-lesson-size |
| L02 | lesson:38 | Gate prose journal '153 lines' -> '154' | ADMITTED | script: C1-lesson-journal-lines |
| L03 | lesson:38 | Gate prose 'the seven pre-wave receipts' -> 'eight' | ADMITTED | script: C3-freeze-count |
| L04 | lesson:34 | ADMIT staged path -> focus-grab-observed-semantics-r9.md | ADMITTED | script: C5-admit-from,C5b-disposition |
| L05 | lesson:35 | REFUSE staged path -> focus-grab-keyboard-routing-r13.md | ADMITTED | human: refusal reason<->target binding is semantic (r29 was an extra refusal, not in assimilated-from) |
| L06 | lesson:38 | Gate prose lesson ref 'M41-6' -> 'M41-7' | ADMITTED | human: M41-7 already exists in w1/ScrLessonSkeleton.md, existence check cannot discriminate |
| X07 | lesson:26 | GATE S284 sha256 flip (control) | KILLED (clause d,g) | — |
| X08 | lesson:27 | GATE S285 quote not in receipt (control) | KILLED (clause d,g) | — |

## Restoration evidence

All mutations lived in the disposable scratch clone `/tmp/mutentryq/clone` (created with
`git clone --no-hardlinks file://…`, reset to DATA before the sweep); the lane was never touched.
After the final revert, the worktree bytes were verified against the DATA blobs:

```
git -C /tmp/mutentryq/clone diff --quiet 07f2641696b5ac73de1404ea737a9f27e9819aa1 -- corpus/  # empty → identical
entry   4c08fc8333c14bfd4395160a8547ec7dcce975d69ead2374e25182c305a14de1  (blob = worktree)
SOURCES 768b839fa063085a024351e66b0160c8ab387ae96631e671d4489e59bf721818  (blob = worktree)
lesson  d8417b86456820cac68111a844590f5e0d119daa01b0a027f24c546e4986994d  (blob = worktree)
README  f3515b7bb14d6978506d5cda4e371bdbedb7153843b0cb3d2c37b7f8097d4833  (blob = worktree)
```

Scratch `/tmp/mutentryq` was removed after the artifacts were copied here.

Tooling record: no tools installed (system `python3` and `git` only; pacman untouched).
