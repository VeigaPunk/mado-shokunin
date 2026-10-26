# Dead weight in the landed entry, lesson and SKILL subsection

Seat `SimpEntryLesson`, w2 (falsify) of round 43. Target revision: the data commit
`1959770657f1f8665097c1aed4be6c1cbb07139f`; lane tip for pointer re-checks: `2a3707c83d55eb1333e1bf6ff1c5c38001c11eaa`.
Lane: `/home/vgpnk/Projects/shokunin/mado-shokunin`. Nothing tracked in the lane was edited; every proposed change was
applied to a scratch clone and the gate re-run there (evidence in `receipt-*.txt` beside this file).

Files attacked: `corpus/knowledge/hyprland-gkeep-geometry-r43.md` (entry), `corpus/lessons/round-43.md` (lesson),
`SKILL.md:246-288` (`### Rule size versus reported size`).

## Method

- Every path any of the three files names was tested at the data commit, at the tip and on disk:
  `git -C <lane> cat-file -e <rev>:<path>` per path; full table in `pointer-audit.tsv` (40 distinct pointers; 25 resolve at
  the data commit, 11 resolve only at the tip or on disk, 4 resolve nowhere — the 4 are F2 and F3 below plus the
  forward-declared report placeholder listed under "considered and retained").
- Redundancy was looked for mechanically (cross- and intra-document sentence overlap, Jaccard ≥0.42 within a document and
  ≥0.55 across the three) and then read: the pass surfaced the three census lines (clause h requires them in the entry,
  and the lesson re-derives them — both load-bearing), the entry title against the lesson's opening summary, and the
  held-row/recheck pair F7 carries below. No cross-document duplicate was found beyond those, so each redundancy below is
  argued from the two texts side by side.
- Safety is judged against `PRED-C2-r43-v2` as implemented by `quality/counters/c2-r43-gkeep-entry-v2.py` (clauses a-i;
  `g+` = `all_body_lines_bound`, `:329-347`), not against the prose description in `registration-v2.md`.
- Proof that the retained content still passes: scratch clone at the data commit, deletions applied, scratch commit
  `c8c3769472f8f7c27302d9640fe328950dc7728b` — `PRED-C2-r43-v2: admitted=1/1 verdict=TARGET_MET` exit 0
  (`receipt-c2-v2-after-deletions.txt`), `CHECK_LOCATORS: locators=10 miss=0` (`receipt-locators-after-deletions.txt`),
  C1 `fixtures=37/37 … TARGET_MET` (`receipt-c1-after-deletions.txt`); diff `3 files changed, 13 insertions(+), 15
  deletions(-)` (`scratch-diff.txt`).

## Verdict

| # | location at the data commit | class | action | C2 v2 |
|---|---|---|---|---|
| F1 | entry `:78` | redundant (third statement of one fact) | delete the trailing clause | SAFE |
| F2 | lesson `:93` | dead pointer (wrong receipt name) | rename the receipt | SAFE |
| F3 | lesson `:205-208` | dead pointers (2) + wrong base receipt | replace the tip clauses, fix the base receipt | SAFE |
| F4 | lesson `:124` | unverifiable as written (off-by-one locator) | `:60` → `:60-61` | SAFE |
| F5 | lesson `:170` | unverifiable as written (lower bound where 38 was measured) | `36 or more` → `38` | SAFE |
| F6 | lesson `:74` | unverifiable as written (the cited command cannot match anything) | drop the `\` before each alternation pipe | SAFE |
| F7 | lesson `:29-30` | redundant (says what `:89-90` and `:91` say) | shorten to one clause | SAFE |
| F8 | `SKILL.md:278-279` | redundant (restates the block it introduces) | keep only the run conditions | SAFE, and no gate reads `SKILL.md` |
| F9 | `SKILL.md:286-288` | redundant (restates the `NO_MATCHING_CLIENT` table row) | delete the first sentence | SAFE, no gate reads `SKILL.md` |
| F10 | `SKILL.md:254-255` | dead weight (registration line of a command) | drop `, command registered at :2007` | SAFE, optional |

## Findings, exact text

### F1 — entry `:78`, one fact stated three times

The GOAL-is-not-the-drawn-size fact appears in the licence table (`:27`), in §3 (`:56`, with the `popin 87%` evidence,
which is the only place that grounds it), and again in the closing list as a trailing clause. The closing list's job is
to name what the entry does not establish; the trailing clause duplicates the table row.

before (entry `:78`):

```
- The current (drawn) size of a gkeep window at any moment on the host; the GOAL is what every read verb reports.
```

after:

```
- The current (drawn) size of a gkeep window at any moment on the host.
```

Safety: the line names no cited id, so clause `g+` does not bind it; it is not one of the three census lines of clause
`h`; the deletion leaves the claim of the bullet intact. Proved: `admitted=1/1` with this edit in the scratch commit.

### F2 — lesson `:93`, the census receipt name is wrong

before:

```
- Census after the data commit: `receipts/census-after.txt` (expected: the same W04 ×7 (S030, S042, S045, S097, S119, S120, S121) + W01 S277 set as `receipts/census-before.txt`, exit 0).
```

after:

```
- Census after the data commit: `receipts/census-after-data.txt` — the same W04 ×7 (S030, S042, S045, S097, S119, S120, S121) + W01 S277 set as `receipts/census-before.txt`, `mado ok`, exit 0.
```

Evidence: `git cat-file -e 1959770657f1:.ufo/waves/round-43/receipts/census-after.txt` → "does not exist in
'1959770657f1…'"; the same at the tip `2a3707c`; on disk absent; `ls .ufo/waves/round-43/receipts/ | grep census` →
`census-after-data.txt`, `census-before.txt`. The receipt itself ends `mado ok … exit=0`, so the replacement states a
measured result instead of an "expected" one (`receipt-dead-pointers.txt`). Earlier rounds used the name
`census-after.txt` (round-41 lesson `:281`), which is where the slip comes from; this round's file is
`census-after-data.txt`.

### F3 — lesson `:205-208`, two tip receipts that do not exist, and the v1 base receipt cited as the v2 base

before:

```
- C1 at the data commit: `receipts/c1-after-data.txt`; at the tip: `receipts/c1-after-tip.txt`. Base: `fixtures=0/37
  tool=absent verdict=TARGET_MISSED` (`receipts/c1-before-base.txt`).
- C2 (v2) at the data commit: `receipts/c2-after-data.txt`; at the tip: `receipts/c2-after-tip.txt`. Base: `admitted=0/1`
  (`receipts/c2-before-base.txt`).
```

after:

```
- C1 at the data commit: `receipts/c1-after-data.txt`; the tip is measured by the spot-check command above. Base: `fixtures=0/37
  tool=absent verdict=TARGET_MISSED` (`receipts/c1-before-base.txt`).
- C2 (v2) at the data commit: `receipts/c2-after-data.txt`; the tip is measured by the spot-check command above. Base:
  `admitted=0/1` (`receipts/c2-v2-before-base.txt`).
```

Evidence: `c1-after-tip.txt` and `c2-after-tip.txt` exist in no commit and on no disk
(`git cat-file -e` at `1959770657f1` and at `2a3707c` → absent; `ls .ufo/waves/round-43/receipts/*tip*` → no such file);
the receipts directory holds 17 files, none a tip receipt. The base receipt quoted for C2 v2 was
`c2-before-base.txt`, whose first line reads `PRED-C2-r43 …` — the v1 counter; the registered v2 base is
`c2-v2-before-base.txt`, first line `PRED-C2-r43-v2 …` (`receipt-dead-pointers.txt`). Both say `admitted=0/1`, so the
number was right and the pointer was wrong. The tip check already exists as a command in the spot-check table
(lesson `:198-199`, `python3 -I quality/counters/… --repo . --rev <rev>`); the replacement points there instead of at
receipts that were never produced. The registration's target is "at the data commit and the tip", so the tip run is still
owed — this deletion makes the record honest about that, it does not create the tip evidence.

### F4 — lesson `:124`, a locator one line short of the line it quotes

before: `` `receipt.txt:60` — `LOC …/LOG-a35cfdf.md:2483 Hyprland-HyprCtl.cpp:394-395,412-413 fragments=6 supported=1 verdict=MISS`, `CHECK_LOCATORS: locators=1 miss=1`, ``

after: `` `receipt.txt:60-61` — `LOC …/LOG-a35cfdf.md:2483 Hyprland-HyprCtl.cpp:394-395,412-413 fragments=6 supported=1 verdict=MISS`, `CHECK_LOCATORS: locators=1 miss=1`, ``

Evidence: `grep -n` in the gate receipt puts the `LOC … verdict=MISS` line at `:60` and the `CHECK_LOCATORS: locators=1
miss=1` line at `:61` (`receipt-dead-pointers.txt`). This is the M43-1 class (a locator computed for where a quote
starts) inside the mistake record that names that class; the sibling locators in the same sentence, `:67` and `:72-73`,
already name the right lines.

### F5 — lesson `:170`, a count stated as a lower bound

before: `` round 43's `ls .ufo/waves/round-43/w1/*.md | wc -l` → 36 or more; ``

after: `` round 43's `ls .ufo/waves/round-43/w1/*.md | wc -l` → 38; ``

Evidence: the command prints `38` at the tip (`receipt-dead-pointers.txt`; `git ls-tree -r --name-only HEAD
.ufo/waves/round-43/w1/ | grep -c '\.md$'` → 147 files under that tree, 38 at its top level; `ls
.ufo/waves/round-43/w1/*.md | wc -l` → 38). The lesson itself states 38 seats at `:20`, so "36 or more" is a second,
weaker statement of the same measurement.

### F6 — lesson `:74`, a grep whose escaping makes it a tautology

before:

```
`git grep -ciE 'set_default_size\|GEOMETRIC_GOAL\|RE2::FullMatch\|rendered geometry' a35cfdf -- corpus/knowledge PROVINCE.md SKILL.md tools` finds none)
```

after:

```
`git grep -ciE 'set_default_size|GEOMETRIC_GOAL|RE2::FullMatch|rendered geometry' a35cfdf -- corpus/knowledge PROVINCE.md SKILL.md tools` finds none)
```

Evidence: under `-E`, `\|` is an escaped *literal* pipe, so the pattern as written can only match a string containing
`set_default_size|GEOMETRIC_GOAL|…` and prints no hits whatever the tree contains — it cannot discriminate. The fact it
is cited for still holds: the corrected command prints no hits either at the base
(`receipt-dead-pointers.txt`, both invocations, rc=1). Replacement keeps the claim and makes the command able to fail.
The same escaped string is in the frozen `registration.md:34`; that file is frozen and this seat does not edit it, so
the lesson should not copy the defect forward.

### F7 — lesson `:29-30`, the held-row edit is stated twice

before:

```
carries exactly one `verified-at: 2026-10-26` (PRED-C2-r43 clauses b and c). No held row's opened/recheck date changes this round; the only
held-row edits this round are the used-by additions on S155 and S158, logged below.
```

after:

```
carries exactly one `verified-at: 2026-10-26` (PRED-C2-r43 clauses b and c). No held row's `opened`/`recheck` cell changes this round; the used-by
additions are logged below.
```

Evidence: `:89-90` names both held rows with their exact old→new `used-by` cells, and `:91` states "No row's `status` and
no row's `recheck` cell changes this round". The deleted clause repeated `:89-90` one screen early. Safety: lesson prose
outside `## Gate` and outside the ADMIT/REFUSE lines is read by no clause of the counter — `score()` takes the lesson
only through `section(lesson, "## Gate")` and the GATE/ADMIT/REFUSE regexes (counter `:468`, `:477-479`, `:580-581`) —
and naming `S155`/`S158` in lesson prose is free, because the `g+` binding applies to the entry, not the lesson.

### F8 — `SKILL.md:278-279`, prose that restates the block under it

before:

```
Host run 2026-10-26, no gkeep window open: the gkeep rule file declares `size 420 500` and the dump holds four tiled
clients, so nothing matches.
```

after:

```
Host run 2026-10-26 with no gkeep window open:
```

Evidence: the block two lines below prints `MADO_GEOM_RULE: … effect=size arg=420x500 …` and the summary
`clients=4 … matched=0 … verdict=NO_MATCHING_CLIENT` — the same three facts, from the tool itself. Row `:225` repeats
the summary again (that repetition is the row convention and is kept). Only the run conditions (date, no gkeep window
open) cannot be read off the block, so only they stay.

### F9 — `SKILL.md:286-288`, a caveat the verdict table already carries

before:

```
NO_MATCHING_CLIENT is not "the rule works": it says only that no mapped window carried the class. What a live gkeep
window would report needs that window open — an operator act, not a mado probe, and the rendered size after the
animation stays `[UNK]` either way.
```

after:

```
What a live gkeep window would report needs that window open — an operator act, not a mado probe, and the rendered size
after the animation stays `[UNK]`.
```

Evidence: the licence table row `:272` already says NO_MATCHING_CLIENT "does not license … that the rule works, or that
the file declares none" — the deleted sentence is that cell in prose. What the paragraph adds and the table does not is
the operator-act and rendered-size-`[UNK]` part; that part stays.

### F10 — `SKILL.md:254-255`, optional: the command's registration line

before:

```
What the reported size is. The `clients` reply prints `"size": [{}, {}]` (`Hyprland-HyprCtl.cpp:395`, command
registered at `:2007`) from `w->size(Desktop::View::IGeometric::GEOMETRIC_GOAL)` (`:427-428` in the JSON format, `:448`
```

after:

```
What the reported size is. The `clients` reply prints `"size": [{}, {}]` (`Hyprland-HyprCtl.cpp:395`) from
`w->size(Desktop::View::IGeometric::GEOMETRIC_GOAL)` (`:427-428` in the JSON format, `:448`
```

Evidence: `:2007` does hold `registerCommand(SHyprCtlCommand{"clients", true, clientsRequest});` (verified by `grep -n`),
so the pointer is accurate — it is simply not needed to establish *what the size is*, and the formatter is already
identified by `:395`/`:427-428`. Left un-applied because the loss is one parenthetical and the win is one parenthetical;
it is listed so the L1 can take it or leave it without re-deriving the judgement.

## UNSAFE — deletions that would break `PRED-C2-r43-v2` (retained)

- Entry `:3-12` (`source:` lines): clause b needs ≥4 distinct source lines inside the first 20 unfenced lines and clause
  i needs all ten PINS cited through them. A `source:` line outside the window is also a clause-b failure.
- Entry `:13` `verified-at` and `:14` `recheck`: clause b requires exactly one of each, inside the window.
- Entry `:32`, `:34`, `:40`, `:42`, `:44`, `:46`, `:52`, `:54`, `:60`, `:66` — the ten id-bearing claim lines. Each cited
  id needs one entry line that names only that id, carries its Gate quote and (for the nine non-HTML receipts) the
  computed `Hyprland-*.cpp:<line>` locator; clause `g+` (`all_body_lines_bound`, counter `:329-347`) then requires *every*
  unfenced line that names an id to carry its quote and locator, so the id-bearing lines cannot be shortened either. The
  counter prints exactly one bound line per id (`receipt-c2-v2-after-deletions.txt`).
- Entry `:70-74` (the three census lines): clause h needs each of the three strings exactly once, and they are excluded
  from the body binding, so they must stay byte-identical.
- Lesson `:34-43` (`GATE <id> …`): clause d needs exactly one per cited id, in `## Gate`, with the pinned sha256 and
  quote, and no `GATE S###` line outside the section.
- Lesson `:45-49` (`ADMIT`/`REFUSE`): clause i needs the ADMIT at the exact package path and each REFUSE to hold a flip
  word and a reason of ≥4 words; the four REFUSE lines and the ADMIT are load-bearing.
- Nothing in `SKILL.md` is read by any checker (`grep -rln 'SKILL' quality/ scripts/` → no file), so its findings are
  reader-value only; the C2 counter never opens it.

## Considered and retained (tradeoff)

- Entry licence table rows `:23-28` — they restate each section's conclusion, but their `state` cell (`OBS`, `INF`,
  `UNK`) is stated nowhere else as a licence; deleting a row would cost the map, not a duplicate.
- Entry `:62` "Two agreeing numbers are not one observation …" — kept: it is the sentence that prevents the over-read the
  oracle result then resolves; deleting it would drop the warning and leave the resolution alone.
- Lesson `:205-208` numbers vs the opening paragraph `:11-18` — the numbers appear twice, but so do they in
  `corpus/lessons/round-41.md:281-283`; the house shape is "claim at the top, measurements at the bottom". Only the
  pointers were repaired, not the convention.
- `merge/mado/…` paths (entry `:17`, lesson `:45-49`, ledger `:74-83`) — unresolvable relative to the lane, but clause i
  mandates the string, the root is named in `registration.md:77`
  (`/home/vgpnk/Projects/shokuknow/merge/mado/`), and the files exist there: the ledger's "S302-S305 ↔ S291-S294" is a
  document-name mapping and holds (r11 `:11-14` names DefaultFloatingAlgorithm.cpp, Target.cpp, WindowTarget.cpp,
  GeometricMovableAnimated.cpp — the four documents of S291-S294, in that order).
- Lesson spot-check row `:194`: `.ufo/reports/round-43/mado.md` does not exist at the data commit — it is the report the
  L1 is writing, in a table marked "(closure)"; a forward-declared placeholder, not a dead pointer.
- Lesson `:62` and `:124` elided paths (`…/efb5099…/src/debug/HyprCtl.cpp`, `LOC …/LOG-a35cfdf.md:2483`) — shorthand;
  each full path is in the registry row or the gate receipt. Not changed.

## Late-landed pointers (resolve at the tip, not at the data commit; no deletion)

11 pointers in the three files resolve only at `2a3707c` or on disk, never at `1959770657f1`: the entry's w1 artifacts
(`ExecGoalVsValue/finding.md`, `ExecOracleGkeep/20-observation.txt`, and the relative `10-cases.txt` beside it), the
lesson's two after-data receipts (`c1-after-data.txt`, `c2-after-data.txt`), six w1 report paths (`CritC2Cheat.md`,
`CritC2Cheat/run-more.log`, `CritClaimSizing.md`, `CritClaimSizing/c2-4new-receipt.txt`, `ExecLocatorGate/receipt.txt`,
`RevC2Counter/findings.md`) and the fleet `watchdog.log`. Wave artifacts land in the commit after the data commit by
design, so these are correct provenance; the audit is in `pointer-audit.tsv`.

## Receipts (in this seat directory)

- `pointer-audit.tsv` — 40 pointers × (data commit, tip, disk).
- `receipt-dead-pointers.txt` — the four missing pointers, the census receipts, the v1/v2 base receipts, the w1 report
  count, the ExecLocatorGate line numbers, the grep escaping pair, the absence of a SKILL reader.
- `receipt-c2-v2-after-deletions.txt`, `receipt-locators-after-deletions.txt`,
  `receipt-c1-after-deletions.txt` — the gates on the scratch commit holding F1-F9.
- `scratch-diff.txt` — the whole applied diff (3 files, 13 insertions, 15 deletions).

## Tool state

No tool installed or updated. `python3` (system), `git` (system) only. Scratch clone under
`/fast/scratch/hyaku/mado-r43/SimpEntryLesson/` was removed at seat end; the commit it produced is not in the lane.
