# Round 63 — mado lesson (hyaku run 12)

Base `cb442f663ca616c0825ed10beccece26bf920b35` (the r62 verifier
spot-check). Host: Windows 11 Home, build 26200, as in rounds 57-62. Three
claims: **C1 calibration** (the r62 carry-in corrections — the closure's
six routed number-shape drifts, all M62-1 class, in the round's own report
records: the total-range mislabel, the "+441" wave-receipts figure, the
"18 receipt files" count, the "four commits" prose, the census-range
endpoint 161-170 vs committed run 2's 160, and the declaration's S418-S422
spread — all dispositioned in ONE append-only `## Corrections (round 63)`
block in `corpus/lessons/round-62.md`, each beside its re-derivation
command, plus the in-file erratum on entry row H22; defect bytes
untouched), **C2 coverage** (sourced entry
`knowledge/windows-displayconfig-r63.md` — rows S424-S434 opened in full
before any row was written; the CCD path/target plane: the active-path
query, the path refresh rational 64/1 agreeing with r61's GDI 64 Hz across
two documented OS planes, and finding D05, the mode table's undocumented
0xFFFFFFFE frequency sentinel beside a sane 1920x1080), **C3 operability**
(capability acquisition `tools/mado-win-displayconfig.py` — the durable
DisplayConfig observer: selftest 13/13 after two disclosed red runs, live
byte-identical x2, from-file, ERROR rc=2, crosscheck 5/5, ledger
102 → 103). L1-only round again: the MISSION ≥8-L2 dispatch floor has no
surface on this host (disclosed since r57, L0 open; unchanged). The
security boundary held throughout: no r56-era credential material was
opened or surfaced; the round touched only the files named in the report.

## Gate

### Admitted

- **Rows S424-S434** (tier A, `mined`, opened 2026-11-01 on the Windows
  host; every page opened in full via fetch BEFORE any row was written;
  every quote below is a verbatim substring of the opened body):

  | row | URL | located quote (≤25 words) |
  |---|---|---|
  | S424 | `https://learn.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-querydisplayconfig` | "The QueryDisplayConfig function retrieves information about all possible display paths for all display devices, or views, in the current setting." (ms.date 2018-12-05, git_commit 39f250c30f4e46de1ef92f2ef07161753ba36e35, updated_at 2026-05-15) |
  | S425 | `https://learn.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-getdisplayconfigbuffersizes` | "retrieves the size of the buffers that are required to call the QueryDisplayConfig function" (ms.date 2018-12-05, git_commit 9267262487657894a8af112d7165006fed5035a7, updated_at 2024-02-22) |
  | S426 | `https://learn.microsoft.com/en-us/windows/win32/api/wingdi/ns-wingdi-displayconfig_path_info` | "The DISPLAYCONFIG_PATH_INFO structure is used to describe a single path from a target to a source." (ms.date 2018-12-05, git_commit a315d8e18e82a977e0cbbef37649b1d35f1785d9, updated_at 2025-09-21) |
  | S427 | `https://learn.microsoft.com/en-us/windows/win32/api/wingdi/ns-wingdi-displayconfig_path_target_info` | "A DISPLAYCONFIG_RATIONAL structure that specifies the refresh rate of the target." (ms.date 2018-12-05, git_commit 9267262487657894a8af112d7165006fed5035a7, updated_at 2024-02-22) |
  | S428 | `https://learn.microsoft.com/en-us/windows/win32/api/wingdi/ns-wingdi-displayconfig_video_signal_info` | "A DISPLAYCONFIG_RATIONAL structure that represents vertical sync." (same ms.date/commit as S427) |
  | S429 | `https://learn.microsoft.com/en-us/windows/win32/api/wingdi/ns-wingdi-displayconfig_path_source_info` | "The DISPLAYCONFIG_PATH_SOURCE_INFO structure contains source information for a single path." (same ms.date/commit as S427) |
  | S430 | `https://learn.microsoft.com/en-us/windows/win32/api/wingdi/ns-wingdi-displayconfig_mode_info` | "The DISPLAYCONFIG_MODE_INFO structure contains either source mode or target mode information." (same ms.date/commit as S427) |
  | S431 | `https://learn.microsoft.com/en-us/windows/win32/api/wingdi/ne-wingdi-displayconfig_mode_info_type` | "DISPLAYCONFIG_MODE_INFO_TYPE_SOURCEValue: 1Indicates that the DISPLAYCONFIG_MODE_INFO structure contains source mode information." (SOURCE=1, TARGET=2; same ms.date/commit as S427) |
  | S432 | `https://learn.microsoft.com/en-us/windows/win32/api/wingdi/ns-wingdi-displayconfig_target_mode` | "The DISPLAYCONFIG_TARGET_MODE structure describes a display path target mode." (same ms.date/commit as S427) |
  | S433 | `https://learn.microsoft.com/en-us/windows/win32/api/wingdi/ns-wingdi-displayconfig_rational` | "The DISPLAYCONFIG_RATIONAL structure describes a fractional value that represents vertical and horizontal frequencies of a video mode" (same ms.date/commit as S427) |
  | S434 | `https://learn.microsoft.com/en-us/windows/win32/api/wingdi/ns-wingdi-displayconfig_2dregion` | "The DISPLAYCONFIG_2DREGION structure represents a point or an offset in a two-dimensional space." (same ms.date/commit as S427) |

  One search sweep, bounded to the eleven documented functions/structures
  the round's probe and tool call and marshal (search log § Round 63); no
  rejected-row event — all eleven opened pages were included. No 404
  event: every struct slug was derived as the type name's lowercase
  underscored form (the M62-2 rule) and every first fetch landed. One
  locator event before any row or code was written: the
  DISPLAYCONFIG_MODE_INFO_TYPE values were remembered in the wrong order
  (TARGET=1); the opened page documents SOURCE=1, TARGET=2 — the
  open-before-write discipline caught it (mined M63-3). The enum pages for
  outputTechnology/rotation/scaling/scanLineOrdering were deliberately not
  opened (the tool emits those members as integers; the sweep opens what
  the join decodes). No reused rows: none of the eleven URLs was
  previously held.

- **Entry** `knowledge/windows-displayconfig-r63.md`: 4 host rows (H25-H28,
  each with its re-derivation command; probe, tool, raw-byte dump and
  crosscheck are committed receipt artifacts), 11 documented rows
  (K44-K54, `[INF-docs]`, dated), 4 joins (J25: the query-side refreshRate
  is the measured fact and the set-side zero-zero semantics never appears
  query-side; J26: the refreshRate↔vSyncFreq join lands `unavailable` —
  the D04 shape at the CCD layer; J27: CCD 64/1 vs GDI 64 Hz cross-layer
  agreement, dual-sourcing r61's mode fact; J28: the documented
  DPI-virtualization non-participation carries r60/r61's physical-pixel
  boundary over), and finding **D05** (the mode table's `pixelRate`/
  `hSyncFreq`/`vSyncFreq` read the undocumented sentinel 0xFFFFFFFE in
  every committed execution while `activeSize` reads sane 1920x1080 and
  the path-side refreshRate reads 64/1; call shape documented, value
  undocumented, cause `[UNK]`, residue and flip condition named). Limits
  restated: no rendered pixel (screen-capture scope stays an open L0),
  point-in-time, no adapter LUID halves/ids/names/handles in any output,
  the documented name getter deliberately not called, enum members as
  integers, source-mode union not decoded, no Set*/Change* verb. Layers
  stay separate per QUALITY 15/16.

- **Capability (C3)**: `tools/mado-win-displayconfig.py` (`VERSION
  r63-v1`): selftest 13/13 rc=0 (after two disclosed red runs — M63-1 and
  M63-2); live `MADO_WINDISPLAYCONFIG: CLEAN (paths=1 refresh=64/1
  vsync=unavailable(0xfffffffe))` rc=0 twice, full outputs byte-identical;
  `--from-file` re-derives from the committed snapshot rc=0; malformed
  snapshot → `MADO_WINDISPLAYCONFIG: ERROR (stage=parse …)` rc=2, raw
  bytes never echoed; crosscheck 5/5 stable fields AGREE against the
  independently executed probe (+ verdict structure); named sanity
  assertions (documented failure return classes as CHECK FAILED,
  DISPLAYCONFIG_PATH_ACTIVE required, positive refresh rational required,
  mode-index bounds, SOURCE=1/TARGET=2 vocabulary, the sentinel recorded
  never asserted); no Set*/Change* verb exists in the tool; ledger
  population 102 → 103 (ledger row + PROVINCE round-63 refinement in the
  same landing).

- **Record corrections (C1)**: `corpus/lessons/round-62.md` gained
  `## Corrections (round 63)` — ONE block, six items, each beside its
  re-derivation command (numstat ranges re-derived at three tips; the
  receipts/wave numstats; the receipt-file count; the first-parent commit
  count; the committed census endpoints; the declaration spread) — and
  `corpus/knowledge/windows-dwm-attributes-r62.md` gained `## Errata
  (round 63)` naming row H22's superseded range endpoint in place (defect
  row untouched). The defect sites in the round-62 records (README index
  row + frontier bullet, SKILL § Round 62 item 1, SCORECARD round-62 C2
  cell and its § Corrections (round 62) total, the LOG round-62 amendment
  bullet) keep their original bytes; the round-63 report restates the
  erratum (the fleet-root report file is not lane-edited). Original-
  preserved checks: r62 lesson 254 lines at base, r62 entry 72 lines at
  base, `git show <base>:<file> | diff - <(head -n <lines> <file>)` empty.

### Rejected (reasons stay; flip conditions named)

- **Building a screen-capture probe this round** (still): the
  screen-capture-scope L0 question (filed r60) has no ruling. **Flip:**
  unchanged — the operator rules the capture scope; then the probe is
  claimable like any other.
- **Decoding the mode union's SOURCE_MODE view** (a second struct view of
  the same bytes): the mode table's source entry carries width/height/
  position facts, but no claim this round needs them and a second view
  would double the marshaling surface for zero claim value; the limit is
  named in the entry. **Flip:** a claim that joins source-mode geometry
  (e.g. against r61's monitor rectangle at the CCD layer) brings it in
  with its own rows.
- **Calling `DisplayConfigGetDeviceInfo` for target/adapter names** (the
  documented name getter the S424 example code uses): names are
  identifying strings and the join needs only indexes — the lane's
  titles-excluded rule (r57) applied to device names; the residue is that
  D05's adapter-class reading stays `[UNK]` without the adapter name.
  **Flip:** an operator ruling that adapter identity is lane-scoped, or a
  claim that needs it, brings the getter in behind the same
  no-raw-values whitelist.
- **Treating the five dormant L0/rubric questions as answerable by
  measurement this round** (omarchy freshness disposal; gate-selftest
  host gap; calibration resolved-active re-derivability; screen-capture
  scope; the L2 floor): all disposals are the operator's (filed
  r57/r58/r59/r60 + the standing L2 line); re-scoring them lane-side
  would presume the ruling. **Flip:** an operator ruling on any of them.

## Mistakes

- **M63-1 — the first on-disk write of the tool lost the two-line tail of
  the embedded PowerShell script** (the `[MadoDisplayConfig.Native]::
  Snapshot() | ConvertTo-Json …` invocation line and the closing `"""`),
  and the tokenizer reported the damage 190 lines away as `SyntaxError:
  invalid character '—' (U+2014)` inside an ordinary docstring. Class
  `measurement` (caught by the selftest's first run, before any green
  receipt or live run). Evidence: the first `--selftest` rc=2 with a
  traceback pointing at `_is_int`'s docstring; reading the traceback
  against the file instead of the reported line found `PS_SCRIPT`'s raw
  string swallowing everything after line 92 (the triple-quote count was
  17 — odd; the ConvertTo-Json line absent from the file). Captured-by:
  the selftest is the first reader of every new tool byte — it caught a
  write defect no review of the intended content would see. Fix: the tail
  restored and the rule carried — a write that ends inside an embedded
  heredoc is re-read at the heredoc terminator, never trusted from the
  write's echo; a SyntaxError's reported line is a symptom, the odd
  string-delimiter count is the diagnosis.
- **M63-2 — the M62-3 class recurred a fourth round running: a static
  count assertion written against a remembered shape.** The assertion
  `low.count("intptr.zero") == 2` expected "comment + call argument";
  the actual script has exactly one site (the call argument — the comment
  says "stays NULL" and carries no token). Class `measurement` (caught by
  the selftest's red 12/13 run, before any green receipt). Evidence:
  selftest-iter2 stderr, `AssertionError: 1 != 2`. Captured-by: the same
  red-run discipline as r60-r62; the fix was read against the
  implementation and the assertion now names its single site in a
  comment. Fix: the standing rule restated with its fourth recurrence —
  a static count assertion is written FROM the implementation's bytes,
  never from the author's memory of them; every count assertion carries
  its site list.
- **M63-3 — an enum's values were remembered in the wrong order, and the
  open-before-write sweep caught it before any code or row was written.**
  The DISPLAYCONFIG_MODE_INFO_TYPE values were remembered as
  TARGET=1/SOURCE=2; the opened page (S431) documents SOURCE=1,
  TARGET=2, DESKTOP_IMAGE=3. Had the decode branch been written from
  memory, the tool would have interpreted source modes as target modes
  and printed nonsense as vSync facts. Class `source-locator` (the
  M61-2/M62-2 class one level up: not the slug, the payload). Evidence:
  the fetched page body vs the pre-fetch plan; the locator event is
  recorded in the search log § Round 63. Captured-by: the M58-2
  open-before-write discipline — the fetch precedes the branch. Fix:
  enumerated values are copied from the opened enumeration page, never
  from memory; the K51 row and the tool's MODE_INFO_TYPE constants pin
  the page's values.

## Census

Start (round start, before any edit): exit 0, `mado ok`, warning set
36 W04 + 1 W01 (identical to r57-r62), 360 rows by the registry grep;
tee'd to `.ufo/waves/round-63/receipts/census-start-r63.txt` (the r61/r62
committed-receipt shape kept). End: `.ufo/waves/round-63/census-after-r63.txt`
→ exit 0, 371 rows (S424-S434; no new W04 — none of the eleven URLs was
previously held). Before-state receipt `before-state-r63.txt` (all base
values for every counting command, measured before any edit, including
the six carry-in re-derivations; one receipt defect caught and fixed in
the work window before commit: the first draft ran the two harmwatch
selftests without the caller-declared `--scratch-root` the M57-1 policy
requires and mis-grepped the live-run JSON spacing — both re-derived,
disclosed in the receipt header, QUALITY 26). Tool and probe receipts
committed beside them: displayconfig-probe.ps1 + dwdc-run1/run2.json
(byte-identical, rc=0 ×2) + stderr, displayconfig-rawdump.ps1 +
rawdump.txt (the D05 byte-level receipt), windisplayconfig-selftest.txt
(13/13, the final run) + the two disclosed red-run stderr files,
windisplayconfig-live-run1/run2.txt (byte-identical) + stderr,
windisplayconfig-snapshot.json, windisplayconfig-fromfile.txt (rc=0),
windisplayconfig-error-path.txt (rc=2), displayconfig-crosscheck.py +
windisplayconfig-crosscheck.txt (5/5), dwm-recheck (the r62 tool re-run
verbatim), harmwatch-selftests-r63.txt (55/55 + 63/63),
landing-counters-r63.txt (navigation/used-by/ledger at the landing,
named sections).

## Considerthese and assimilation

- Mined all nine `considerthese/` files again this round (2026-10-19
  through 2026-10-28; directory listing re-run 2026-11-01 — no new files
  since the r58 mining, mtimes unchanged): no adoptable proposal. The
  dispositions of r57-r62 stand.
- Assimilation: none — shokuknow unreachable.

## Route to round 64 (intent only; no commitment)

1. The five L0 rulings (omarchy freshness disposal; gate-selftest host
   gap; calibration resolved-active re-derivability; screen-capture
   scope; the L2 floor) — the SCORECARD tables follow the ruling, never
   precede it.
2. The rendered-pixel observation iff the screen-capture-scope L0
   question is ruled; the candidate shape stays the statistics-only,
   no-persist capture probe.
3. D05's residue: a `QDC_VIRTUAL_MODE_AWARE` query shape (one bounded
   query, S424's flag table) to test whether the sentinel is
   virtual-mode-path-specific — the flip condition D05 names; and a
   second-host or driver-side reading only if the operator scopes one.

## Addendum (used-by setup gate fired red at the landing; repaired in-round, before closure)

The landing counters receipt records a red state this round's harm-watch
sentences did not predict: at the landing `c9a70974` the used-by counter
failed in setup — registry row S430's `teaches` cell carried two unescaped
pipe characters (`targetMode|sourceMode|desktopImageInfo`), breaking the
registry's 11-cell row shape (the counter read 13 cells and refused).
Class: the report-table number-drift class one level down again — a cell
written from the entry's prose (where `|` is table syntax) instead of from
the registry's row grammar; caught by the counter's own setup gate, before
any verdict ran. Repaired as the round's own consistency move, keyed on
the row id (`| S430 |` asserted on the edited line): the pipe set replaced
with slashes, proposition text otherwise untouched. The final counters
receipt records the red run at `c9a70974` and the green run at the repair
`cdacf215` (`missing=0 extra=0 … TARGET_MET`, `entries=78 rows=371`); the
M59-4 proactivity rule held — every named row's used-by cell was already
correct, and the M59-4 row-id rule held on the repair (no extra, no
mis-aimed neighbor this time).
