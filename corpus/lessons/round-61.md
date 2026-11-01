# Round 61 — mado lesson (hyaku run 12)

Base `cccda4dacc1009f767799ce62fe112fd53d2d47a` (the r60 verifier spot-check).
Host: Windows 11 Home, build 26200, as in rounds 57-60. Three claims: **C1
calibration** (the r60 carry-in corrections — the r60 lesson's Census section
named three receipt files that do not exist under those names
(`navigation-landing-r60.txt`, `usedby-after-r60.txt`, `ledger-landing-r60.txt`;
the runs live in `landing-counters-r60.txt`'s three named sections, the base
used-by run is `usedby-before-r60.txt`) and the r59 lesson's line-74
"+4/−0 each" — the last standing member of the number-shape drift class round
60 corrected in SCORECARD/LOG/SKILL; both corrected append-only as
`## Corrections (round 61)` blocks with re-derivation commands, defect bytes
untouched), **C2 coverage** (sourced entry
`knowledge/windows-display-topology-r61.md` — rows S412-S417 opened in full
before any row was written; the native display-topology plane and the
display-mode layer: work area, refresh rate, mode index series — ground no
committed entry held), **C3 operability** (capability acquisition
`tools/mado-win-display.py` — the durable display-topology observer: selftest
10/10, live x2 byte-identical, from-file, ERROR rc=2, crosscheck 5/5, ledger
100 → 101). L1-only round again: the MISSION ≥8-L2 dispatch floor has no
surface on this host (disclosed since r57, L0 open; unchanged). The security
boundary held throughout: no r56-era credential material was opened or
surfaced; the round touched only the files named in the report.

## Gate

### Admitted

- **Rows S412-S417** (tier A, `mined`, opened 2026-11-01 on the Windows host;
  every page opened in full via fetch BEFORE any row was written; every quote
  below is a verbatim substring of the opened body):

  | row | URL | located quote (≤25 words) |
  |---|---|---|
  | S412 | `https://learn.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-enumdisplaymonitors` | "The EnumDisplayMonitors function enumerates display monitors (including invisible pseudo-monitors associated with the mirroring drivers)" (ms.date 2018-12-05, git_commit 9267262487657894a8af112d7165006fed5035a7, updated_at 2024-02-22) |
  | S413 | `https://learn.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-getmonitorinfow` | "The GetMonitorInfo function retrieves information about a display monitor." (same ms.date; git_commit a9040b7bd365036907a35293e28d8cd449e31b87, updated_at 2024-11-20) |
  | S414 | `https://learn.microsoft.com/en-us/windows/win32/api/winuser/ns-winuser-monitorinfo` | rcWork: "A RECT structure that specifies the work area rectangle of the display monitor, expressed in virtual-screen coordinates." (same ms.date/commit as S412) |
  | S415 | `https://learn.microsoft.com/en-us/windows/win32/api/winuser/ns-winuser-monitorinfoexw` | "The MONITORINFOEX structure is a superset of the MONITORINFO structure." (same ms.date/commit as S413) |
  | S416 | `https://learn.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-enumdisplaysettingsa` | "This API does not participate in DPI virtualization. The output given is always in terms of physical pixels" (ms.date 2018-12-05, git_commit fa53641576e3603fa7b66d3a4ad969d3ce49d6f3, updated_at 2025-07-01) |
  | S417 | `https://learn.microsoft.com/en-us/windows/win32/api/wingdi/ns-wingdi-devmodew` | dmDisplayFrequency: "For displays, specifies the frequency, in hertz, of a display device in its current mode." (ms.date 2023-06-13, git_commit f014fff5b27fe5eb5115f15dd6762713bc73c697, updated_at 2025-05-21) |

  One search sweep, bounded to the six documented functions/structures the
  round's probe and tool actually call (search log § Round 61); no
  rejected-row event — all six opened pages were included. One URL-correction
  event before any row was written (the first MONITORINFO fetch guessed the
  windef.h path and 404'd; the structure lives in winuser.h — recorded in the
  search log, mined as M61-2). No reused rows this round: none of the six
  URLs was previously held.

- **Entry** `knowledge/windows-display-topology-r61.md`: 4 host rows
  (H17-H20, each with its re-derivation command; probe and tool are committed
  receipt artifacts, two byte-identical runs each rc=0), 10 documented rows
  (K28-K37, `[INF-docs]`, dated), 4 joins (J17-J20; J17 carries the
  directional work-area caveat with the band's owner `[UNK]`, J20 the
  documented no-DPI-virtualization pin that makes the caller-awareness
  `[UNK]` of the DPI entries not arise here), and finding D03 (a 1-mode
  driver list beside the three-way DPI-mode split of r58 D02). Limits
  restated: no rendered pixel (screen-capture scope stays an open L0
  question, routed around), point-in-time topology/modes, no Shell surface
  read. Layers stay separate per QUALITY 15/16.

- **Capability (C3)**: `tools/mado-win-display.py` (`VERSION r61-v1`): selftest
  10/10 rc=0 (after three red assertion-authoring runs, M61-1); live
  `MADO_WINDISPLAY: CLEAN (monitors=1 primary=\\.\DISPLAY1 mode=1920x1080@64
  work=1920x1032)` rc=0 twice, byte-identical; `--from-file` re-derives from
  the committed snapshot rc=0; malformed snapshot → `MADO_WINDISPLAY: ERROR
  (stage=parse …)` rc=2, raw bytes never echoed; crosscheck 5/5 stable fields
  AGREE against the independently executed probe (receipt
  `windisplay-crosscheck.txt`); the documented 0-failure return classes are
  treated as CHECK FAILED, never a measurement (named assertion); no
  Set*/Change* verb exists in the tool; ledger population 100 → 101 (ledger
  row + PROVINCE round-61 refinement in the same landing).

- **Record corrections (C1)**: `corpus/lessons/round-60.md` gained
  `## Corrections (round 61)` (the three Census receipt names superseded by
  `landing-counters-r60.txt`'s named sections + `usedby-before-r60.txt`, with
  the `git grep`/`ls` re-derivation) and `corpus/lessons/round-59.md` gained
  `## Corrections (round 61)` (the line-74 "+4/−0 each" figure beside the
  measured +17/−0 and +5/−0, re-derived by the r60 correction block's own
  `git diff-tree -r --numstat 6f2e4115 25294ab3 -- <the two entries>`). Both
  defect sites keep their original bytes (ORIGINAL_PRESERVED reproduced by
  the `git show <base>:… | diff - <(head -n N)` check; r59 lesson 217 lines,
  r60 lesson 181 lines at base).

### Rejected (reasons stay; flip conditions named)

- **Building a screen-capture probe this round** (still): the
  screen-capture-scope L0 question (filed r60) has no ruling. **Flip:**
  unchanged — the operator rules the capture scope; then the probe is
  claimable like any other.
- **Reading the taskbar to close H19's `[UNK]`** (which surface owns the
  48 px band): the taskbar rectangle lives behind Shell surfaces
  (`Shell_TrayWnd`/`ABM_GETTASKBARPOS`), a plane no lane instrument touches;
  pulling it in for one join would widen the lane's live surface beyond the
  documented-getter discipline every Windows entry has held since r57.
  **Flip:** an operator ruling that the Shell appbar plane is in scope.
- **Treating the four dormant-rubric L0 questions as answerable by
  measurement this round** (re-deriving the freshness 28/29, the gate
  selftest, calibration resolved-active, or the screen-capture scope on
  Windows): all four disposals are the operator's (filed r57/r58/r59/r60);
  re-scoring them lane-side would presume the ruling. **Flip:** an operator
  ruling on any of the four.

## Mistakes

- **M61-1 — static selftest assertions written against remembered text
  shapes, not the implementation's actual text; the M60-1 class recurring
  three times in one tally.** Class `measurement` (caught by the selftest's
  own runs, before any green receipt was committed). Evidence: the first
  `--selftest` run printed `9/10`, and the next two runs after partial fixes
  printed `9/10` twice more — all four failures were assertion-authoring
  bugs, not tool-logic bugs: (1) a generic `assertNotIn("registry", …)` ban
  collided with the tool's own legitimate `mode_registry` field name (a
  documented iModeNum shape, not a Registry API read) — the intended pin was
  `microsoft.win32.registry`/`get-itemproperty`; (2) the import+call-site
  occurrences of the three query families were guessed as 1 where the
  implementation text has 2/2/4 (import + call sites −1, −2, index series);
  (3) the fixed-buffer count guessed 2 where the script holds 3
  (`szDevice`, `dmDeviceName`, and the forgotten `dmFormName`). Captured-by:
  reading each failure against the embedded script instead of relaxing the
  assertion; every fixed assertion now names its exact sites in a comment.
  Fix: the committed receipt is the final 10/10 run; the red runs live in
  this lesson's record only, and the rule stands — an assertion that fails
  against committed bytes is read twice (assertion bug vs tool bug) before
  either is edited, and a static count assertion must carry its site list.
- **M61-2 — a source-locator guess (struct's header inferred from a
  neighboring type's home) cost one 404 before any row was written.** Class
  `source-locator` (caught by the fetch itself, inside the sweep). Evidence:
  the first MONITORINFO fetch used the windef.h path
  (`/api/windef/ns-windef-monitorinfo`) — RECT's own header — and returned
  404; the structure lives in winuser.h
  (`/api/winuser/ns-winuser-monitorinfo`), which the GetMonitorInfoW page
  (already opened at that point) links directly. Captured-by: the sweep's
  open-before-write discipline — the 404 happened before any row could cite
  the wrong path, and the search log records the correction event with the
  working URL. Fix: struct pages are located from the function page that
  documents the parameter taking them, never from the header of a type they
  contain; the working URL is recorded in the row (S414) and the sweep log.

## Census

Start (round start, before any edit): tee'd to a committed receipt this
round — `.ufo/waves/round-61/receipts/census-start-r61.txt` (the r59/r60
runs were disclosed as not-tee'd; this round closes that gap): exit 0,
`mado ok`, warning set 36 W04 + 1 W01 (identical to r57-r60), 348 rows by
the registry grep. End: `.ufo/waves/round-61/receipts/census-after-r61.txt`
→ exit 0, 354 rows (S412-S417; no new W04 — none of the six URLs was
previously held). Before-state receipt `before-state-r61.txt` (all base
values for every counting command). Tool and probe receipts committed beside
them: display-probe.ps1 + display-probe-run1/run2.txt (byte-identical),
windisplay-selftest.txt (10/10, the final run), windisplay-live-run1/run2.txt
(byte-identical), windisplay-snapshot.json, windisplay-fromfile.txt,
windisplay-error-path.txt (rc=2), display-crosscheck.py +
windisplay-crosscheck.txt (5/5), harmwatch-selftests-r61.txt (55/55 + 63/63),
landing-counters-r61.txt (the three landing runs, named sections — the r60
lesson's correction is applied by construction this round), navigation and
used-by/ledger runs inside it.

## Considerthese and assimilation

- Mined all nine `considerthese/` files again this round (2026-10-19 through
  2026-10-28; nothing new since the r58 mining): no adoptable proposal. The
  dispositions of r57-r60 stand.
- Assimilation: none — shokuknow unreachable.

## Route to round 62 (intent only; no commitment)

1. The four L0 rulings (omarchy freshness disposal; gate-selftest host gap;
   calibration resolved-active re-derivability; screen-capture scope) — the
   SCORECARD tables follow the ruling, never precede it.
2. The rendered-pixel observation iff the screen-capture-scope L0 question is
   ruled; the candidate shape stays the statistics-only, no-persist capture
   probe.
3. A Win11-labeled DWM model sentence, if one surfaces, still strengthens the
   D01 pin; the taskbar-band owner joins only behind a Shell-plane ruling.

## Corrections (round 62)

The r61 verifier spot-check (§ 7 item 1) routed a number drift in the
round-61 report's "Landed changes" table, corrected here append-only (the
defect lives in the fleet-root report file, which the lane does not edit;
this block names the superseded table rows, and the round-62 report restates
the erratum). The table's per-file counts for three record files are wrong
while the totals are right:

- The rows for `LOG.md` ("+52"), `PROVINCE.md` ("+13") and `SKILL.md`
  ("+50") are superseded by the measured per-file insertions **LOG.md +64/−0,
  PROVINCE.md +19/−0, SKILL.md +55/−0**. The table's totals ("28 files,
  +1416/−0 — zero deleted lines") re-derive exactly, so the three wrong
  per-file figures undercount their files by 12/6/5 lines while the sum of
  all 28 rows stays correct.
- Re-derivation: `git diff-tree -r --numstat cccda4da ad4e8403 -- LOG.md
  PROVINCE.md SKILL.md` → `64 0` / `19 0` / `55 0`; the totals:
  `git diff-tree -r --numstat cccda4da ad4e8403 | awk '{a+=$1; d+=$2; n++}
  END {print n" files "a" added "d" deleted"}'` → `28 files 1416 added 0
  deleted`. Also re-derived at round-62 round start into the committed
  receipt `.ufo/waves/round-62/before-state-r62.txt` (same commands, base
  `4c5435d8`).
- This is the number-shape drift class round 60 corrected in SCORECARD/LOG/
  SKILL and round 61 corrected in the r59 lesson — recurring in a report
  table beside a correction of the same class in the same round's C1. The
  class rule (an asserted number carries its counting command, QUALITY 10)
  is recorded as M62-1's class in `corpus/lessons/round-62.md`.
