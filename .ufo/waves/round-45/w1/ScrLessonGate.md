# ScrLessonGate — round 45 w1 report (C2 lesson draft: Gate, registry changes, search log)

Seat: `ScrLessonGate` (leaf; no dispatch). Lane: `/home/vgpnk/Projects/shokunin/mado-shokunin`. Freeze read first:
`.ufo/waves/round-45/registration.md` (base `0c89478a`, freeze `22a8dedd`).

## Behavior

Wrote the paste-ready `corpus/lessons/round-45.md` draft at
`.ufo/waves/round-45/w1/ScrLessonGate/round-45.md` (167 lines, three `##` sections — `## Gate`,
`## Registry changes`, `## Search log`; `## Mistakes` deliberately absent, left to ScrMistakes).

- **Gate**: 15 candidates, 9 admitted as new rows S302-S310, 6 rejected with evidence. Nine column-0 `GATE` lines,
  one per cited id, byte-identical to `l1-draft/build-pos.py`'s output. Each admitted source carries its URL, the
  access date 2026-10-26, a <= 25-word quote with a `grep -n` locator, its registry anchor cell, and the admission
  reason. Rejected: held-row reuse of S158 and S162, the wiki at `main`, a live host dump as a row,
  `src/output/Monitor.hpp`, and hyprlang sources.
- **Registry changes**: nine new rows (absent → `mined`, opened `2026-10-26`, recheck `90d`, used-by the new entry),
  inserted after S301 (`corpus/SOURCES.md:250`) landing at :251-:259; held S158/S162 unchanged; one README index row
  after `corpus/README.md:72` landing at :73; census 238 → 247 rows.
- **Search log**: three questions (chain sources; held-row reuse; live dump as a row) with
  identified/screened/included/excluded counts 12/12/9/3, 2/2/0/2, 1/1/0/1 (total 15/15/9/6, matching the Gate table)
  and a stop rationale per question.

## Gates run (evidence)

| # | check | receipt | outcome |
|---|---|---|---|
| 1 | nine pins vs `PINS` (sha256 + >= 256 B) and quote semantics with the frozen counter's own helpers (`quote_at`, `occurrences`, `quote_in_code`) | `ScrLessonGate/quote-verify.txt` | 9/9 `pin_match=1`; every quote 3-10 words, one word-bounded occurrence, comment-stripped match, distinct; cross-receipt foreign = 0; `ALL_QUOTES_OK=1` |
| 2 | `grep -n` locators for the nine quotes against `.ufo/waves/round-45/fetch/` | `ScrLessonGate/gate-greps.txt` | :134, :1345, :38, :46, :1001, :242 (collapsed match starts :241), :27, :59, :11 |
| 3 | PRED-C2-r45 clause d over the draft (frozen counter's `GATE_RE`, `PINS`, `FETCH` semantics) | `ScrLessonGate/clause-d.txt` | `ids=9 outside=0`, every id bound, `CLAUSE_D_OK=1` |
| 4 | draft Gate lines vs lines rebuilt from `build-pos.py` + lane fetch bytes | `ScrLessonGate/gate-line-match.txt` | `GATE_LINES_IDENTICAL=1` |
| 5 | full predicate on a scratch clone of the freeze with `build-pos.py` applied and this draft as the lesson | `ScrLessonGate/c2-with-lesson.txt` | `clauses=a:1 b:1 c:1 d:1 e:1 f:1 g:1 h:1 i:1 j:1 admitted=1`, `PRED-C2-r45: admitted=1/1 verdict=TARGET_MET rev=72502d21…`, exit 0; 17 clause-j surfaces cited (run on the final draft bytes) |
| 6 | rejected-candidate evidence: wiki pin vs `main`, `isNumber`→`isNumber2` delegation, host version, held-row coverage | `ScrLessonGate/candidates-evidence.txt` | pinned wiki HTTP 200 / 10563 B / sha `f2ac7025…04b9` (equals the pin); `main` HTTP 404; `isNumber` at `Parser.cpp:197,214,265` → `hyprutils-String.cpp:46-47`; `hyprctl version`: Hyprland 0.56.2 @ efb50993, Hyprutils 0.14.2, Hyprlang 0.6.8; S158 coverage of :242 and :313-321 = 0, S162 coverage of :1293-1387 = 0 |

Also observed once in a scratch clone (clone removed per the SCRATCH directive, so not citable by path): the
`build-pos.py`-applied clone differs from the freeze by 4 files / 113 insertions / 0 deletions, `corpus/SOURCES.md`
row count 238 → 247, and no deleted content line — i.e. the delta in `## Registry changes` is exactly the
generator's, and no held row is rewritten.

## Touched surfaces

- Written (all new): `.ufo/waves/round-45/w1/ScrLessonGate/round-45.md` plus receipts/scripts
  `quote-verify.txt`, `gate-greps.sh`, `gate-greps.txt`, `candidates-evidence.sh`, `candidates-evidence.txt`,
  `check_lesson.py`, `clause-d.txt`, `check_gatelines.py`, `gate-line-match.txt`, `verify_gate.py`,
  `c2-with-lesson.txt`; and this report `.ufo/waves/round-45/w1/ScrLessonGate.md`.
- Read-only: `.ufo/waves/round-45/registration.md`, `l1-draft/{entry.md,build-pos.py}`,
  `quality/counters/c2-r45-monitor-entry.py`, `.ufo/waves/round-45/fetch/*` (9), `corpus/SOURCES.md`,
  `corpus/README.md`, `.ufo/waves/round-45/receipts/fetch-sha256.txt`, `SKILL.md`.
- No lane tracked file edited; `corpus/lessons/round-45.md` does not exist in the lane
  (`ls` → "No such file"), so the draft is the only copy and the L1 owns the integration.
- Host: one read-only compositor call, `hyprctl version`. No `dispatch`/`keyword`/`reload`/`setprop`/`--batch`/
  `output`/`plugin`/`kill`; no Wayland client; no service change; no pacman (installed nothing; `python3`, `git`,
  `curl`, `sh` already present).
- Git: only in throwaway clones under `/fast/scratch/hyaku/mado-r45/ScrLessonGate/`, each after
  `git -C "$D" rev-parse --show-toplevel` returned `$D`; that directory is deleted. Nothing was committed in the lane
  or the fleet.

## Out of scope / not done

- `## Mistakes` (ScrMistakes), the C1 tool, and the integration into `corpus/` (L1 only). No commit, push or
  publication. Routed round-44 defects D1-D7 and considerthese proposal 1 are not touched by this draft.

## Findings (each names what it attacks or supports)

1. **Held-row reuse is blocked by frozen anchors, not by URL duplication** — attacks reusing S158/S162 for the
   monitor lines; supports the new rows S303/S307. Evidence: `quote-verify.txt` lines `S158 anchor covers
   HyprCtl.cpp:242 -> 0`, `:313-321 -> 0`, `S162 anchor covers ConfigManager.cpp:1293-1387 -> 0`; scope equality is
   0 for both pairs, so clause e's same-scope test is what makes the shared URL the census W04 case.
2. **The wiki at `main` no longer serves the cited page** — attacks a "wiki at main" row; supports S310's pinned
   commit. `main/content/Configuring/Monitors.md` → HTTP 404 today, while the pinned commit returns HTTP 200,
   10563 B, sha256 `f2ac7025b7d7dd13b467ad52a5ca7b4da39e198f3ae4c6a675f92a38cd0304b9` = the pin
   (`candidates-evidence.txt` §A). A main-ref row could not satisfy clause d's sha binding.
3. **S309's call-site precision** (for the critic/reviewer seats, not a defect I correct) — the entry's §1 attributes
   the number test to `isNumber2`, while `CConfigManager`'s parsers call `isNumber` (`Hyprland-Parser.cpp:197,214,265`),
   which delegates (`hyprutils-String.cpp:46-47`). The row description ("the number test Hyprland's scale and
   transform parsers call") and the Gate quote (`hyprutils-String.cpp:59`) stay true; only a sentence naming the
   function directly is loose. Supports S309 as admitted; flags the wording for the non-author reading.
4. **S307 locator nuance** — the collapsed match of the S307 quote starts at `Hyprland-HyprCtl.cpp:241` (the
   `"physicalHeight"` part), while `grep -n '"refreshRate"'` returns :242. The entry's `:241-242` and my draft's
   `:241-242` are consistent with both computations; a reviewer grepping only the second field could read a mismatch.
5. **The Gate lines are exactly the generator's** — supports the L1's integration: pasting this draft keeps clause d
   satisfied (`gate-line-match.txt`, and clause d re-run over the draft in check 3), and the whole predicate admits
   1/1 with this lesson in place (check 5). This is a compatibility check of my artifact, not a claim of C2 data.

No conflict between the registration, the frozen counters and the frozen pins was observed; nothing here needs the
canonical judge's arbitration beyond finding 3 (wording only).

## Artifact paths (relative to the lane)

- `.ufo/waves/round-45/w1/ScrLessonGate/round-45.md` — the draft to integrate as `corpus/lessons/round-45.md`.
- `.ufo/waves/round-45/w1/ScrLessonGate/{quote-verify.txt,gate-greps.txt,clause-d.txt,gate-line-match.txt,candidates-evidence.txt,c2-with-lesson.txt}`
  — receipts named in the table above.
- `.ufo/waves/round-45/w1/ScrLessonGate/{verify_gate.py,check_lesson.py,check_gatelines.py,gate-greps.sh,candidates-evidence.sh}`
  — the read-only scripts that produced them.
