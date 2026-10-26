status: ok
seat: ScrLessonSkeleton — round 44 (hyaku run 9, inline v1 wave w1), Godspeed leaf, no subagents
target: draft `corpus/lessons/round-44.md` — `## Gate`, assimilation ledger, `## Mistakes`, `## Round-43 errata`
deliverable: `.ufo/waves/round-44/w1/ScrLessonSkeleton/round-44-lesson.md` (262 lines)
supporting: `w1/ScrLessonSkeleton/gate-check.py` + `gate-check.txt` (re-runnable Gate/ADMIT/REFUSE check), `w1/ScrLessonSkeleton/c1-demo/` (the M44-8 evidence: two client fixtures, one rules file, four run outputs, `commands.txt`)

## What I did not do

No tracked file edited, nothing committed, no git/jj write anywhere. No campaign tool run inside the package. The two lane
counters were **not executed** (I imported their *functions* read-only to check quotes and Gate grammar, which is what the
round-43 lesson says the L1 does). The control receipts were read as bytes, not executed. No `hyprctl` read, no Wayland
client, no compositor access. No tools installed. Scratch `/fast/scratch/hyaku/mado-r44/ScrLessonSkeleton/` deleted; every
cited byte is copied into the seat dir.

## Gate (draft lines 40-58) — mechanically checked

Run: `python3 -I .ufo/waves/round-44/w1/ScrLessonSkeleton/gate-check.py` → `.ufo/waves/round-44/w1/ScrLessonSkeleton/gate-check.txt`
(`GATE ALL OK`, `exit=0`). It uses the frozen counter's own `GATE_RE`, `norm`, `occurrences`, `quote_at`, `quote_in_code`,
`PINS`, `STAGED`, `ADMIT_RE`, `REFUSE_RE` and `BAD_LOC`.

| id | receipt | sha256 (== pin) | words | locator (`quote_at`) | in code | in other 4 pins |
|---|---|---|---|---|---|---|
| S164 | `fetch/Hyprland-Window.cpp` | `d735d454…` ✓ | 7 | 1752 | yes | 0 |
| S298 | `fetch/Hyprland-XDGShell.cpp` | `d90b534c…` ✓ | 5 | 354 | yes | 0 |
| S299 | `fetch/xdg-shell.xml` | `7ba7f9c8…` ✓ | 22 | 1150 | yes | 0 |
| S300 | `fetch/gdktoplevel-wayland.c` | `0ee38458…` ✓ | 3 | 681 | yes | 0 |
| S301 | `fetch/gkeep-ui.py` | `07a3c4a5…` ✓ | 5 | 476 | yes | 0 |

`GATE S` lines outside the `## Gate` section: **0**. No two ids share a path, a hash or a quote. ADMIT/REFUSE: 1 ADMIT naming
`corpus/knowledge/hyprland-gkeep-size-request-r44.md` (byte-equal to the counter's `ENTRIES`, `c2-r44-gkeep-size-request.py:150`)
and 4 REFUSE, each path `merge/mado/knowledge/corpus/knowledge/<STAGED name>`, each reason 27-34 distinct words with an `if`
flip. `BAD_LOC` hits in the draft: 0. C1's three `fetch-c1/` grounding pins deliberately carry no GATE line — they have no
registry row, so no id to bind (stated in the draft).

## Assimilation ledger (draft) — decisions

ADMIT `gkeep-client-size-request-r12.md` (the predecessor; its staged S311 → held S164 by document, staged S312 → new S301;
its tag-form URL is not carried because clause e+ wants the commit form; `verified-at` re-dated 2026-10-26).
REFUSE `-r13`, `-r14`, `-r15` (their decisive receipt is a `lanes/mado/round1[345]/fetch/...` path that does not exist in this
lane: `git ls-tree -r --name-only HEAD | grep -c 'lanes/mado/round[0-9]*/fetch'` → 0) and `-r9` (its two distinctive links
need `docs.gtk.org` and the wiki page, neither pinned; its two round-9 receipts absent here). No new decision on r8, r10 and
observation-route r11 — round 43 refused them (`corpus/lessons/round-43.md:46,47,48`). r30: refusal was withdrawn in round 43
and it is still not adopted (no pin, no row). r31: off-theme residue. Package ids S203-S349 are never carried; mapping is by
document (`assimilation/renumber-map.tsv`).

## Mistakes (draft `## Mistakes`) — mapped to the routed defects

M44-1 ← D1 (under-cited refusal reason + mis-mapped S310) · M44-2 ← D2 (S293 title) · M44-3 ← D3 (SKILL.md:276 TILED cell) ·
M44-4 ← D4 (pointers absent at the data commit, off-range receipt locator) · M44-5 ← D5 (37 vs 38 seats; M43-1..8 vs ..9) ·
M44-6 ← D6 (open predicate defects) · M44-7 ← D7 (no committed tip axis receipt) · **M44-8 = this round's C1 finding**.

## Findings

1. **F1 (supports C2 clauses d and i).** The draft's Gate section satisfies every condition I could check mechanically with
   the frozen counter's own functions; receipt `gate-check.txt`. Quote lengths 3-22 words, word-bounded, unique, outside
   comments, absent from the other four pins. The entry seat can cite S164, S298-S301 unchanged; the census lines
   (`gkeep client default_size=420x500 size_request_calls=0 application_id=org.omarchy.gkeep`,
   `hyprland sendWindowSize xdg_setSize=1 x11_configure=1`) are recomputed and correct (F9).
2. **F2 (supports C1's *why*; attacks `tools/mado-geometry.py` at base `6a1a905`).** The round-43 tool reports a **fullscreen**
   gkeep client (`fullscreen: 2`, floating, `size 2560x1440`, the monitor box) as `verdict=DIFFER`, exit 1 — a false report —
   and a **maximized** one (`fullscreen: 1`, not floating, `2544x1380`, the work area) as `verdict=TILED` with the top-level
   `verdict=OK`, exit 0 — a false clearance. The frozen reference gives `FULLSCREEN` / `MAXIMIZED`, exit 0, ` maximized=…
   fullscreen=…`. Evidence: `w1/ScrLessonSkeleton/c1-demo/` (`commands.txt`; four outputs; re-run from the seat dir and
   diffed byte-identical). The two sizes are Hyprland's own (`.ufo/waves/round-44/fetch-c1/Hyprland-FullscreenHandler.cpp:191-199`).
   Captured by nothing in round 43: `PRED-C1-r42` never varied `fullscreen` and the tool's docstring lists only
   BADSIZE | TILED | AGREE | DIFFER. This is M44-8.
3. **F3 (attacks the closure's D1 *citation*, not its substance).** `corpus/lessons/round-43-verifier-spotcheck.md:97` routes D1
   as "`round-43.md:75`"; the r10 `REFUSE` line is at `:46` and `:74` is the ledger row that re-grounds S310
   (`grep -n 'REFUSE merge/mado/knowledge/corpus/knowledge/gkeep-size-rule-application-r10.md' corpus/lessons/round-43.md` → 46).
   Recorded verbatim as conflict C1 below and as erratum E4.
4. **F4 (confirms D4).** `git ls-tree -r --name-only 1959770 .ufo/waves/round-43/w1/ExecOracleGkeep/` → **0 files** (both
   receipts the entry cites landed after the data commit; 2 at the tip). `gkeep-shm.c`'s "sets app_id and title, attaches a
   200x200 shm buffer and commits" block is `:150-159` (150 app_id, 151 title, 157-159 attach/damage/commit), not the
   `:156-164` the receipt cites.
5. **F5 (confirms D5).** `git show 5add5b4:.ufo/waves/round-43/w1-spec.json` → 38 items; `HEAD:.ufo/waves/round-43/w1-results.json`
   → 38 results; `.ufo/waves/round-43/registration.md:5` says "37 seats". `SCORECARD.md:2548` says "Mistakes M43-1..8";
   `grep -c '^\*\*M43-' corpus/lessons/round-43.md` → 9.
6. **F6 (confirms D7).** At the closing tip `5846662` the committed axis logs stop at
   `.ufo/waves/round-43/w2/ExecHarmTip/logs/tip-2a3707c-axis.log:4` (`mismatched=0 rev=2a3707c…`); no log carries `rev=5846662`
   (`git grep -n 'MADO_AXIS:' 5846662 -- .ufo/waves/round-43/w2/ExecHarmTip/logs/`). Round 44 already commits a base receipt
   (`receipts/axis-base.txt`, three MATCH rows, `rev=6a1a905…`).
7. **F7 (locator precision for the C1 seat).** `fullscreen` in `clients -j` is *valued* at
   `.ufo/waves/round-44/fetch-c1/Hyprland-HyprCtl.cpp:431` (JSON) and `:451` (plain text), both
   `getFullscreenModes(w).internal`; `:410-411` is only the JSON template key. The draft cites `:431`/`:451` so a later seat
   does not cite the template for the value. `size` is `GEOMETRIC_GOAL` at `:427-428`.
8. **F8 (supports clause i).** The ADMIT target equals the counter's `ENTRIES[0]` exactly; the 4 REFUSE paths are STAGED names
   under the required prefix and none equals the ADMIT target, so `adm`/`ref` in `score()` both match.
9. **F9 (supports clause h).** Recomputed from the pins with the counter's rules: one `set_default_size(420, 500)`, zero
   `set_size_request(`, one `application_id="org.omarchy.gkeep"`; `sendWindowSize` body `Hyprland-Window.cpp:1732-1754` holds
   one `->setSize(` and one `->configure(`. Both census lines in the draft are the counter's own strings.
10. **F10 (supports the errata).** `CWindow::getReportedSize()` for Wayland returns `m_current.ackedSize`
    (`fetch/Hyprland-Window.cpp:1861-1866`, written by `onAck` at `:1526`), so the closure's D1 note that the flip's "the
    reported size" is ack-derived holds — the errata cite it rather than repeat it unchecked.

## Conflicts (verbatim, for the canonical judge)

- **C1.** Closure D1: "lesson `round-43.md:75` r10 refusal reason cites S291/S293 (box path) but not the reported-field links
  S294/S158" (`round-43-verifier-spotcheck.md:97`). The same lesson's `REFUSE` line for r10 is at `corpus/lessons/round-43.md:46`;
  `:74-75` is the ledger row. Substance unrefuted; locator recomputed.
- **C2.** The task names 11 residue files under `knowledge/corpus/knowledge/` (10 staged + the round-43 admit); the counter's
  `STAGED` holds 10 — the admitted `gkeep-size-to-real-size-r11.md` is excluded by the round's own predicate. The draft's
  ledger covers all 10 STAGED files plus the admitted one for completeness.
- **C3.** `registration.md:5` on round 44 says "the seat counts are recorded from each wave's `*-results.json`", while the task
  header states 38 w1 seats; `w1-spec.json` has 38 items, so both agree — no conflict, recorded because round 43's own
  registration carried a stale 37.

## Values the L1 must fill (16 `<<L1>>` markers in the draft)

w2 seat count; `receipts/census-after.txt`; the C1 and C2 after-data/after-tip receipts; the SCORECARD append (round 44
section, and the M43-1..9 correction); the S293 supersession seat (with S290-S292, S296, S297); the SKILL.md:276 TILED cell
(C1's landing); the tip axis receipt; the knowledge-count and README index row; the entry's clause-h confirmation; the
`CritC2Cheat`/`ExecC2Positive`/`ExecC1ExtraMutants` outcomes for M44-6; the `SentLiveReads` live receipt; and the
reason-to-receipt coverage checker M44-1 asks for (no such checker exists today).

## Checks the main agent should run (not run by this seat)

`python3 -I quality/counters/c2-r44-gkeep-size-request.py --repo . --rev <data tip>` once the entry, rows, README row and this
lesson are in place (it scores this lesson's Gate), and
`python3 -I quality/counters/c1-r44-geometry-states.py --repo . --rev <data tip> --work <scratch>`; plus
`python3 -I .ufo/waves/round-44/w1/ScrLessonSkeleton/gate-check.py` after any edit to the Gate lines.
