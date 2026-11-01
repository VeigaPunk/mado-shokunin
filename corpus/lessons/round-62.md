# Round 62 — mado lesson (hyaku run 12)

Base `4c5435d8bb3dd108f1dba4998de73c514609d885` (the r61 verifier
spot-check). Host: Windows 11 Home, build 26200, as in rounds 57-61. Three
claims: **C1 calibration** (the r61 carry-in corrections — the round-61
report's Landed-changes table under-counted LOG/PROVINCE/SKILL (+52/+13/+50
against measured +64/+19/+55, totals correct; the same-correction family's
section-name nit: the receipt header is the parenthetical form) — both
corrected append-only as `## Corrections (round 62)` blocks with
re-derivation commands, defect bytes untouched), **C2 coverage** (sourced
entry `knowledge/windows-dwm-attributes-r62.md` — rows S418-S423 opened in
full before any row was written; the DWM client-attribute plane: composition
state, the cloaked-window census, the frame-bounds join, and finding D04,
the timing getter's undocumented failure in both documented call shapes),
**C3 operability** (capability acquisition `tools/mado-win-dwm.py` — the
durable DWM attribute observer: selftest 11/11 after three red
assertion-authoring runs, live verdict lines byte-identical ×2 beside a
named-field churn receipt, from-file, ERROR rc=2, crosscheck 5/5, ledger
101 → 102). L1-only round again: the MISSION ≥8-L2 dispatch floor has no
surface on this host (disclosed since r57, L0 open; unchanged). The security
boundary held throughout: no r56-era credential material was opened or
surfaced; the round touched only the files named in the report.

## Gate

### Admitted

- **Rows S418-S423** (tier A, `mined`, opened 2026-11-01 on the Windows
  host; every page opened in full via fetch BEFORE any row was written;
  every quote below is a verbatim substring of the opened body):

  | row | URL | located quote (≤25 words) |
  |---|---|---|
  | S418 | `https://learn.microsoft.com/en-us/windows/win32/api/dwmapi/nf-dwmapi-dwmgetwindowattribute` | "Retrieves the current value of a specified Desktop Window Manager (DWM) attribute applied to a window." (ms.date 2019-05-30, git_commit fa53641576e3603fa7b66d3a4ad969d3ce49d6f3, updated_at 2025-07-01) |
  | S419 | `https://learn.microsoft.com/en-us/windows/win32/api/dwmapi/ne-dwmapi-dwmwindowattribute` | "If the window is cloaked, provides one of the following values explaining why." (ms.date 2024-01-21, git_commit 75d8a6a0145431644157a4dabc09260f0d73118f, updated_at 2026-03-09) |
  | S420 | `https://learn.microsoft.com/en-us/windows/win32/api/dwmapi/nf-dwmapi-dwmgetcompositiontiminginfo` | "Starting with Windows 8.1, this parameter must be set to NULL." (ms.date 2018-12-05, git_commit fa53641576e3603fa7b66d3a4ad969d3ce49d6f3, updated_at 2025-07-01) |
  | S421 | `https://learn.microsoft.com/en-us/windows/win32/api/dwmapi/ns-dwmapi-dwm_timing_info` | rateRefresh: "The monitor refresh rate." (ms.date 2018-12-05, git_commit 9267262487657894a8af112d7165006fed5035a7, updated_at 2024-02-22) |
  | S422 | `https://learn.microsoft.com/en-us/windows/win32/api/dwmapi/ns-dwmapi-unsigned_ratio` | "It represents a generic ratio and is used for different purposes and units even within a single API." (same ms.date/commit as S421) |
  | S423 | `https://learn.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-getwindowrect` | "GetWindowRect is virtualized for DPI." (ms.date 2018-12-05, git_commit fa53641576e3603fa7b66d3a4ad969d3ce49d6f3, updated_at 2025-07-01) |

  One search sweep, bounded to the six documented functions/structures the
  round's probe and tool actually call (search log § Round 62); no
  rejected-row event — all six opened pages were included. One
  URL-correction event before any row was written (the first DWM_TIMING_INFO
  fetch used the hyphen slug and 404'd; the struct slug keeps the type
  name's underscore — recorded in the search log, mined as M62-2). No
  reused rows this round: none of the six URLs was previously held;
  S399/S400 (composition state) are quoted from their held pages, not
  re-fetched.

- **Entry** `knowledge/windows-dwm-attributes-r62.md`: 4 host rows (H21-H24,
  each with its re-derivation command; probe and tool are committed receipt
  artifacts), 6 documented rows (K38-K43, `[INF-docs]`, dated), 4 joins
  (J21-J24; J22 names the cross-layer visibility/cloaking `[UNK]` the
  counts-only tool cannot tabulate; J23 keeps the two documented rect/frame
  causes separate — the resize-border cause observed at a stable 7 px, the
  DPI-virtualization cause vacuous at effective 96, the r60 J13 shape; J24
  reads D04 against S420's documented S_OK/E_INVALIDARG vocabulary), and
  finding D04 (the timing getter fails with undocumented `0x88980090` in
  both documented call shapes, cbSize 320 per the documented layout,
  deterministic across every committed execution; the rateRefresh→r61's
  64 Hz join never lands on this host and stays documentation-layer).
  Limits restated: no rendered pixel (screen-capture scope stays an open L0
  question, routed around), point-in-time, counts never per-window rows, no
  Shell surface read. Layers stay separate per QUALITY 15/16.

- **Capability (C3)**: `tools/mado-win-dwm.py` (`VERSION r62-v1`): selftest
  11/11 rc=0 (after three red assertion-authoring runs — M62-mined); live
  `MADO_WINDWM: CLEAN (composition=on reasons=app+shell
  timing=unavailable(hr=0x88980090))` rc=0 twice, verdict lines
  byte-identical, the JSON census churning on exactly the named field
  (`windows.top_level` 168→170; receipt `windwm-live-churn-diff.txt` — the
  declared amendment narrowed this receipt shape before the formal runs);
  `--from-file` re-derives from the committed snapshot rc=0; malformed
  snapshot → `MADO_WINDWM: ERROR (stage=parse …)` rc=2, raw bytes never
  echoed; crosscheck 5/5 stable fields AGREE against the independently
  executed probe (+ census structure, no equality claim on churn-prone
  counters); the documented 0-failure return classes and a nonzero
  `attr_failed` are treated as CHECK FAILED, never a measurement (named
  assertions); no Set*/Move*/Change* verb exists in the tool; ledger
  population 101 → 102 (ledger row + PROVINCE round-62 refinement in the
  same landing).

- **Record corrections (C1)**: `corpus/lessons/round-61.md` gained
  `## Corrections (round 62)` (the r61 report's Landed-changes rows for
  LOG/PROVINCE/SKILL superseded by the measured +64/+19/+55, re-derivation
  `git diff-tree -r --numstat cccda4da ad4e8403 -- LOG.md PROVINCE.md
  SKILL.md` → `64 0` / `19 0` / `55 0`, totals re-derived 28 files +1416/−0;
  the fleet-root report file is not lane-edited — the round-62 report
  restates the erratum) and `corpus/lessons/round-60.md` gained
  `## Corrections (round 62)` (the exact section header named beside the
  `git show <base>:… | grep -n '^--'` re-derivation; the LOG round-62
  correction bullet names the short form's second site in LOG's own round-61
  bullet). Both defect sites keep their original bytes (ORIGINAL_PRESERVED
  reproduced by the `git show <base>:… | diff - <(head -n N)` check; r60
  lesson 208 lines, r61 lesson 175 lines at base).

### Rejected (reasons stay; flip conditions named)

- **Building a screen-capture probe this round** (still): the
  screen-capture-scope L0 question (filed r60) has no ruling. **Flip:**
  unchanged — the operator rules the capture scope; then the probe is
  claimable like any other.
- **Treating D04 as an operator question or an L0 line**: the timing
  getter's failure is a host observation with a documented call shape and
  an undocumented result — it is recorded as a finding with cause `[UNK]`,
  not routed to the operator (nothing in the lane's scope changes either
  way). **Flip:** an operator ruling that DWM timing behavior is
  operator-relevant would move it into the L0 set.
- **Substituting another surface for the failed rateRefresh join** (e.g.
  calling `DwmFlush`-adjacent or Graphics-Capture/IDXGI-out-of-documented-
  vocabulary surfaces): the documented-vocabulary discipline every Windows
  entry has held since r57 keeps the round from pulling a new API family in
  through a side door in the same round its first surface failed; the
  residue is named (planned-63 item 3). **Flip:** a documented getter whose
  page the sweep actually opens, in a later round with its own rows.
- **Treating the four dormant-rubric L0 questions as answerable by
  measurement this round**: all four disposals are the operator's (filed
  r57/r58/r59/r60); re-scoring them lane-side would presume the ruling.
  **Flip:** an operator ruling on any of the four.

## Mistakes

- **M62-1 — the number-shape drift class recurred in the previous round's
  own report table, beside a C1 that corrected the same class.** Class
  `measurement` (caught by the r61 non-author closure's numstat
  re-derivation). Evidence: the round-61 report's Landed-changes table
  printed LOG "+52", PROVINCE "+13", SKILL "+50" against measured
  +64/+19/+55 — the totals (28 files, +1416/−0) were correct, so three
  per-file figures were wrong by 12/6/5 while their sum was right; the
  re-derivation is `git diff-tree -r --numstat cccda4da ad4e8403 -- LOG.md
  PROVINCE.md SKILL.md`. Captured-by: the closure's own landing-shape check
  (the same `diff-tree --numstat` the report could have run). Fix: every
  table number this round carries its counting command in the same cell
  (SCORECARD C1), and the carried rule is now written in SKILL § Round 62
  rule 3: a number asserted without its command is the defect, whatever
  surface it sits on — report tables included.
- **M62-2 — a struct-slug guess (hyphen where the docs keep the type
  name's underscore) cost one 404 before any row was written.** Class
  `source-locator` (the M61-2 class recurring; caught by the fetch itself,
  inside the sweep). Evidence: the first DWM_TIMING_INFO fetch used
  `/api/dwmapi/ns-dwmapi-dwm-timing-info` and returned 404; the working URL
  is `/api/dwmapi/ns-dwmapi-dwm_timing_info` — the underscore of the type
  name survives into the slug, while the function page's markdown link
  renders the anchor hyphenated. The M61-2 rule (locate the struct from the
  function page that documents the parameter taking it) was applied and
  still produced the wrong slug form. Captured-by: the sweep's
  open-before-write discipline — the 404 happened before any row could
  cite the wrong path, and the search log records the correction event with
  the working URL. Fix: struct slugs are copied from the working URL the
  fetch lands on, never re-derived from the display form of a link; the
  working URL is recorded in the row (S421) and the sweep log.
- **M62-3 — three selftest assertion-authoring runs failed red before the
  green receipt: static pins written against remembered shapes, not the
  implementation's actual text (the M61-1/M60-1 class, third round
  running).** Class `measurement` (caught by the selftest's own runs,
  before any green receipt was committed). Evidence: run 1 printed 8/11 —
  a generic `assertNotIn("wmi", …)` ban collided with the legitimate
  `DwmIsCompositionEnabled` P/Invoke (the substring sits inside dw-m-i-s;
  the intended pin is the WMI/CIM cmdlets `get-wmiobject`/`get-ciminstance`
  — the exact M61-1 shape), and the reason-pattern assertion expected
  short names the implementation spelled as its keys; run 2 printed 10/11 —
  `enumwindows` counted 5 sites, not the asserted 2 (the import signature
  names both the function and its delegate parameter type); run 3 printed
  10/11 — `iswindow` counted 5, not 3 (`iswindowvisible`'s two sites carry
  it as a prefix; the paren form `iswindow(` counts the getter's 3 true
  sites). Captured-by: reading each failure against the embedded script
  before either the assertion or the implementation was edited; every
  fixed count assertion now names its exact site list in a comment. Fix:
  the committed receipt is the final 11/11 run; the red runs live in this
  lesson's record only, and the standing rule is restated with its third
  recurrence — a static count assertion must carry its site list, and a
  substring ban must name its intended tokens.

## Census

Start (round start, before any edit): tee'd to a committed receipt —
.ufo/waves/round-62/receipts/census-start-r62.txt` (the r61 committed-receipt shape
kept): exit 0, `mado ok`, warning set 36 W04 + 1 W01 (identical to
r57-r61), 354 rows by the registry grep. End:
`.ufo/waves/round-62/census-after-r62.txt` → exit 0, 360 rows (S418-S423;
no new W04 — none of the six URLs was previously held). Before-state
receipt `before-state-r62.txt` (all base values for every counting command,
measured before any edit, including the carry-in numstat re-derivations and
the header re-derivation; one receipt defect caught and fixed in the work
window: the first entry-absence check captured the pipe's status instead of
the producer's — re-run with the producer's own rc, QUALITY 26). Tool and
probe receipts committed beside them: dwm-attributes-probe.ps1 +
dwm-run1/run2.txt (byte-identical except the census counters, rc=0 ×2),
windwm-selftest.txt (11/11, the final run) + stderr,
windwm-live-run1/run2.txt (verdict-identical) + windwm-live-churn-diff.txt
(the named-field churn receipt), windwm-snapshot.json, windwm-fromfile.txt,
windwm-error-path.txt (rc=2), dwm-crosscheck.py + windwm-crosscheck.txt
(5/5), harmwatch-selftests-r62.txt (55/55 + 63/63),
landing-counters-r62.txt (the three landing runs in named sections — the
file shape the r61 correction carried, with the exact parenthetical header
this round's correction names).

## Considerthese and assimilation

- Mined all nine `considerthese/` files again this round (2026-10-19 through
  2026-10-28; nothing new since the r58 mining): no adoptable proposal. The
  dispositions of r57-r61 stand.
- Assimilation: none — shokuknow unreachable.

## Route to round 63 (intent only; no commitment)

1. The four L0 rulings (omarchy freshness disposal; gate-selftest host gap;
   calibration resolved-active re-derivability; screen-capture scope) — the
   SCORECARD tables follow the ruling, never precede it.
2. The rendered-pixel observation iff the screen-capture-scope L0 question
   is ruled; the candidate shape stays the statistics-only, no-persist
   capture probe.
3. D04's residue: a documented-getter surface for the compositor refresh,
   iff one exists in the documented vocabulary the sweep opens, lands the
   rateRefresh→64 Hz join D04 left open; a Win11-labeled DWM model
   sentence, if one surfaces, still strengthens the D01 pin.
