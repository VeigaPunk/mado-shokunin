# The Windows DisplayConfig plane — the CCD path/target view beside the GDI mode layer (round 63)

Host: Windows 11 Home, build 26200, single active display (the r57-r62
host). This entry reads the CCD (client-side configuration display)
plane — `GetDisplayConfigBufferSizes` + `QueryDisplayConfig` with
`QDC_ONLY_ACTIVE_PATHS` — the documented path/target view of the live
topology that no committed entry held. It lands beside the layers already
measured: r57 the managed `Screen` plane, r58 per-monitor DPI, r60 the
metrics/awareness join, r61 the GDI topology (`EnumDisplayMonitors` +
`EnumDisplaySettingsW`), r62 the DWM client-attribute plane. Every host
row carries its re-derivation command; probe and tool are committed
receipt artifacts. Rows S424-S434 were opened in full BEFORE any row was
written (the M58-2 discipline; the lesson's Gate records the sweep).

## Host rows (re-derivable on this host)

| row | claim (this host, 2026-11-01) | re-derivation |
|---|---|---|
| H25 | The active-path query answers on this host: `GetDisplayConfigBufferSizes(QDC_ONLY_ACTIVE_PATHS=0x2)` returns rc 0 with buffer paths=1, modes=2; `QueryDisplayConfig` with the same flag and `currentTopologyId = NULL` (the documented requirement for any non-`QDC_DATABASE_CURRENT` call) returns rc 0 with paths=1, modes=2 — byte-identical JSON in two formal probe runs and two formal tool runs (the CCD topology moves only on a display change, unlike the r62 window census; the churn class here is display-configuration change, not desktop activity) | `powershell.exe -NoProfile -NonInteractive -NoLogo -ExecutionPolicy Bypass -File .ufo/waves/round-63/receipts/displayconfig-probe.ps1` → rc 0 (`dwdc-run1.json`, `dwdc-run2.json`, byte-identical by `cmp`); `python tools/mado-win-displayconfig.py` → `MADO_WINDISPLAYCONFIG: CLEAN (paths=1 refresh=64/1 vsync=unavailable(0xfffffffe))` rc 0 ×2 (`windisplayconfig-live-run1/2.txt`, full outputs byte-identical by `cmp`) |
| H26 | The single active path is documented-shaped end to end: `flags` bit 0x1 (`DISPLAYCONFIG_PATH_ACTIVE`) set; `targetInfo.refreshRate` = **64/1**; `targetInfo.modeInfoIdx` = 0 and `sourceInfo.modeInfoIdx` = 1; the mode table holds exactly 2 entries with `infoType` values [2, 1] — TARGET at the index the path names, SOURCE at the index the source names (the documented SOURCE=1/TARGET=2 values, S431); the target's `outputTechnology` = −1, `rotation` = 1, `scaling` = 1, `scanLineOrdering` = 1, `targetAvailable` = 1 (BOOL TRUE), `statusFlags` = 1 — **emitted as integers only**; the enum member-name mapping stays documentation-layer (those enum pages were not opened this round, except S431 whose values the join needs) | same receipts as H25; the JSON `path_list[0]` block in `dwdc-run1.json` (the tool's whitelisted re-print is the committed snapshot `windisplayconfig-snapshot.json`) |
| H27 | The indexed target mode (`modes[0].targetMode.targetVideoSignalInfo`) reads: `activeSize` 1920x1080, `totalSize` 1920x1080, `scanLineOrdering` 1 — and **`pixelRate`, `hSyncFreq` and `vSyncFreq` all read the undocumented sentinel 0xFFFFFFFE (4294967294)**, deterministic across every committed execution (probe ×2, tool ×2, crosscheck, raw-byte dump). This is finding **D05** (below): documented fields, documented call shape, undocumented value — recorded, never guessed at | same receipts as H25, plus the raw-byte receipt: `powershell.exe … -File .ufo/waves/round-63/receipts/displayconfig-rawdump.ps1` → struct sizes PATH_INFO=72 SOURCE=20 TARGET=48 VIDEO=48 TMODE=48 MODEINFO=64, rc 0/0, and the mode[0] byte dump showing `FE-FF-FF-FF` at the documented offsets 16-39 and `80-07`/`38-04` (1920/1080) at offsets 40-55 (`displayconfig-rawdump.txt`) |
| H28 | Cross-layer refresh agreement: the CCD path refresh (64/1, this entry) equals the GDI mode frequency r61 measured independently (`EnumDisplaySettingsW` `dmDisplayFrequency` = 64 Hz, `windows-display-topology-r61.md` H20) — two documented OS planes measured in two rounds agree on the refresh fact. The DWM timing side stays unobserved: `mado-win-dwm.py` re-run this round still prints `timing=unavailable(hr=0x88980090)` (D04 unchanged, its cause still `[UNK]`), so the compositor-refresh join that D04 left open now has a second documented getter's agreement on the *mode* refresh — while the *compositor* rate itself remains unobserved on this host | `python tools/mado-win-displayconfig.py` (refresh=64/1) beside `git show cb442f66:corpus/knowledge/windows-display-topology-r61.md \| grep -o "64 Hz"`; `python tools/mado-win-dwm.py` → verdict line unchanged (receipt `dwm-recheck-r63.txt` in the round-63 wave) |

## Documented rows (`[INF-docs]`, dated; all opened in full 2026-11-01)

| row | source | teaches (verbatim-anchored) |
|---|---|---|
| K44 | S424 | `QueryDisplayConfig` — "retrieves information about all possible display paths for all display devices, or views, in the current setting"; the flags table (QDC_ALL_PATHS 0x1, **QDC_ONLY_ACTIVE_PATHS 0x2**, QDC_DATABASE_CURRENT 0x4, QDC_VIRTUAL_MODE_AWARE 0x10, QDC_INCLUDE_HMD 0x20, **QDC_VIRTUAL_REFRESH_RATE_AWARE 0x40, Windows 11**); "If the flags parameter value is not set to QDC_DATABASE_CURRENT, the currentTopologyId parameter value must be NULL"; the six-code return vocabulary (ERROR_SUCCESS / INVALID_PARAMETER / NOT_SUPPORTED / ACCESS_DENIED / GEN_FAILURE / INSUFFICIENT_BUFFER); the ERROR_INSUFFICIENT_BUFFER retry shape; "This API does not participate in DPI virtualization"; ms.date 2018-12-05, git_commit 39f250c30f4e46de1ef92f2ef07161753ba36e35, updated_at 2026-05-15 |
| K45 | S425 | `GetDisplayConfigBufferSizes` — "retrieves the size of the buffers that are required to call the QueryDisplayConfig function"; "can return values that are slightly larger than are actually required"; the same six-code return vocabulary minus INSUFFICIENT_BUFFER; ms.date 2018-12-05, git_commit 9267262487657894a8af112d7165006fed5035a7, updated_at 2024-02-22 |
| K46 | S426 | `DISPLAYCONFIG_PATH_INFO` — "used to describe a single path from a target to a source"; members sourceInfo/targetInfo/flags; flag values DISPLAYCONFIG_PATH_ACTIVE 0x1 ("Set by QueryDisplayConfig to indicate that the path is active and part of the desktop"), DISPLAYCONFIG_PATH_SUPPORT_VIRTUAL_MODE 0x8, DISPLAYCONFIG_PATH_BOOST_REFRESH_RATE 0x10 ("Dynamic refresh rate", Windows 11); ms.date 2018-12-05, git_commit a315d8e18e82a977e0cbbef37649b1d35f1785d9, updated_at 2025-09-21 |
| K47 | S427 | `DISPLAYCONFIG_PATH_TARGET_INFO` — member list adapterId/id/modeInfoIdx-union/outputTechnology/rotation/scaling/**refreshRate**/scanLineOrdering/targetAvailable/statusFlags; refreshRate: "A DISPLAYCONFIG_RATIONAL structure that specifies the refresh rate of the target"; the set-side zero-zero semantics ("A refresh rate with both the numerator and denominator set to zero indicates that the caller does not specify a refresh rate") — set-side only, never observed query-side here (J25); statusFlags vocabulary IN_USE 0x1 … IS_HMD 0x20; ms.date 2018-12-05, git_commit 9267262487657894a8af112d7165006fed5035a7, updated_at 2024-02-22 |
| K48 | S428 | `DISPLAYCONFIG_VIDEO_SIGNAL_INFO` — member list pixelRate/hSyncFreq/vSyncFreq/activeSize/totalSize/union/scanLineOrdering (no pixelFormat member on the page); vSyncFreq "a DISPLAYCONFIG_RATIONAL structure that represents vertical sync"; activeSize "the width and height (in pixels) of the active portion of the video signal"; ms.date 2018-12-05, git_commit 9267262487657894a8af112d7165006fed5035a7, updated_at 2024-02-22 |
| K49 | S429 | `DISPLAYCONFIG_PATH_SOURCE_INFO` — member list adapterId/id/modeInfoIdx-union (cloneGroupId:16 + sourceModeInfoIdx:16 under virtual mode)/statusFlags; "A source corresponds to a surface on which the display adapter can render pixels"; ms.date 2018-12-05, git_commit 9267262487657894a8af112d7165006fed5035a7, updated_at 2024-02-22 |
| K50 | S430 | `DISPLAYCONFIG_MODE_INFO` — "contains either source mode or target mode information"; member list infoType/id/adapterId/union(targetMode|sourceMode|desktopImageInfo); ms.date 2018-12-05, git_commit 9267262487657894a8af112d7165006fed5035a7, updated_at 2024-02-22 |
| K51 | S431 | `DISPLAYCONFIG_MODE_INFO_TYPE` — the values the join decodes: **DISPLAYCONFIG_MODE_INFO_TYPE_SOURCE = 1, DISPLAYCONFIG_MODE_INFO_TYPE_TARGET = 2**, DESKTOP_IMAGE = 3, FORCE_UINT32 = 0xFFFFFFFF (the locator event: the remembered order was TARGET=1 — the opened page decided, before any code was written; mined M63-3); ms.date 2018-12-05, git_commit 9267262487657894a8af112d7165006fed5035a7, updated_at 2024-02-22 |
| K52 | S432 | `DISPLAYCONFIG_TARGET_MODE` — "describes a display path target mode"; the single member `targetVideoSignalInfo` (a DISPLAYCONFIG_VIDEO_SIGNAL_INFO); ms.date 2018-12-05, git_commit 9267262487657894a8af112d7165006fed5035a7, updated_at 2024-02-22 |
| K53 | S433 | `DISPLAYCONFIG_RATIONAL` — "a fractional value that represents vertical and horizontal frequencies of a video mode"; members Numerator/Denominator (UINT32 pair); specified in members of PATH_TARGET_INFO and VIDEO_SIGNAL_INFO; ms.date 2018-12-05, git_commit 9267262487657894a8af112d7165006fed5035a7, updated_at 2024-02-22 |
| K54 | S434 | `DISPLAYCONFIG_2DREGION` — "represents a point or an offset in a two-dimensional space"; members cx/cy (UINT32 pair); ms.date 2018-12-05, git_commit 9267262487657894a8af112d7165006fed5035a7, updated_at 2024-02-22 |

## Joins

| row | join |
|---|---|
| J25 | H26 ↔ K47: the query-side `refreshRate` is the documented target refresh and this host answers 64/1; K47's all-zero "caller does not specify" sentence is documented **set-side** semantics and never appears query-side here — the tool treats a non-positive rational as CHECK FAILED (the not-a-measurement shape), the same rule the r62 tool applied to a zero timing rate |
| J26 | H26/H27 ↔ K48/K52: the vSyncFreq the page describes ("represents vertical sync") does not reach this host's mode table — the sentinel D05 fills it — so the refreshRate↔vSyncFreq join lands `unavailable(0xfffffffe)`, not `agree`: the D04 shape repeated at the CCD layer (documented call shape, undocumented field value, cause `[UNK]`). The refresh fact of this entry therefore rests on the **path side alone** (J25), and the tool prints `vsync=unavailable(0xfffffffe)` in its verdict line, recorded never asserted |
| J27 | H28 ↔ r61 H20/J17: the CCD path/target plane and the GDI mode layer agree on the refresh fact (64) across two rounds and two independent artifacts — dual-sourcing the r61 mode frequency that D03 had single-sourced; the compositor-rate side stays unobserved (D04 unchanged on this round's recheck, its `0x88980090` failure not re-litigated here) |
| J28 | K44 ↔ r58/r60/r61: "This API does not participate in DPI virtualization" makes the CCD sizes physical pixels regardless of caller awareness — the r60 caller-awareness `[UNK]` (J13's vacuous branch at effective 96) and r61's physical-pixel pins carry over unchanged; the measured activeSize 1920x1080 equals the r61 monitor rectangle exactly |

## Finding

- **D05** (host behavior beside the documentation): the active target
  mode's `DISPLAYCONFIG_VIDEO_SIGNAL_INFO` frequency fields — `pixelRate`,
  `hSyncFreq` and `vSyncFreq` — read the undocumented sentinel 0xFFFFFFFE
  (−2 signed) in every field on this host, deterministic across every
  committed execution, while the same structure's `activeSize` reads sane
  (1920x1080) and the path-side `refreshRate` reads 64/1. The call shape is
  fully documented (K44/K45); the value appears nowhere in the opened
  pages. Cause **`[UNK]`** — not guessed at. Residue named: whether the
  sentinel is a driver-class behavior (the host's adapter reports no
  name here — the name getter `DisplayConfigGetDeviceInfo` is deliberately
  not called), a host-specific state, or a Windows-11 virtual-refresh
  artifact (K44's QDC_VIRTUAL_REFRESH_RATE_AWARE exists on this OS
  version's API set but was not invoked), and whether a
  `QDC_VIRTUAL_MODE_AWARE` query fills the fields differently — all
  testable on a later round with its own rows, or on a different host.
  **Flip:** a documented sentinel value, or a query shape that returns
  decoded frequencies, moves D05 from `[UNK]` to measured.

## Limits (restated, not hidden)

- Point-in-time observation; the topology facts move only on a display
  configuration change (a different churn class than the r62 window
  census); two live runs are expected byte-identical and the from-file
  re-derivation is the determinism receipt.
- No adapter LUID halves, no target/source id integers, no device names,
  no monitor friendly names, no handles: the documented name getter
  (`DisplayConfigGetDeviceInfo`) is deliberately not called — the join
  needs only indexes, and names can carry identifying strings. The
  whitelisted output carries counts, rationals, flags and enum integers.
- Source-mode entries are counted and indexed only (the mode union is
  mapped to its largest documented member, DISPLAYCONFIG_TARGET_MODE);
  decoding DISPLAYCONFIG_SOURCE_MODE would need a second view of the same
  bytes and no claim here needs it.
- Enum members (outputTechnology, rotation, scaling, scanLineOrdering) are
  emitted as integers; the member-name mapping stays documentation-layer
  (those enum pages were not opened this round beyond S431).
- No rendered-pixel claim (the screen-capture-scope L0 question stays
  open, routed around); no Shell surface is read.
- No Set*/Change* verb exists in the probe or the tool (`SetDisplayConfig`
  is the documented mutator of this plane and its name appears in neither
  artifact; topology, mode and refresh changes stay operator-owned).

## Verify (re-derivation, read-only)

```bash
# probe twice, byte-identical
powershell.exe -NoProfile -NonInteractive -NoLogo -ExecutionPolicy Bypass \
  -File .ufo/waves/round-63/receipts/displayconfig-probe.ps1
# tool: selftest, live twice, from-file, error path
python tools/mado-win-displayconfig.py --selftest
python tools/mado-win-displayconfig.py
python tools/mado-win-displayconfig.py --from-file .ufo/waves/round-63/receipts/windisplayconfig-snapshot.json
# crosscheck: independently executed probe vs tool, 5 stable fields
python .ufo/waves/round-63/receipts/displayconfig-crosscheck.py .
```

## Update (round 64) — the D05 flip-condition probe: the QDC flag matrix

Appended 2026-11-01 (round 64, append-only; every row above keeps its original bytes).
Finding D05 named its flip condition: "whether a `QDC_VIRTUAL_MODE_AWARE` query fills
the fields differently". S424 was re-opened this round (page unchanged since the r63
open: ms.date 2018-12-05, git_commit 39f250c30f4e46de1ef92f2ef07161753ba36e35,
updated_at 2026-05-15) and its flags table pins the two virtual flags:
`QDC_VIRTUAL_MODE_AWARE` 0x10 (Windows 10+) and `QDC_VIRTUAL_REFRESH_RATE_AWARE` 0x40
(Windows 11+); the page's own example code is the
`QDC_ONLY_ACTIVE_PATHS | QDC_VIRTUAL_MODE_AWARE` shape. One bounded read-only probe
(`.ufo/waves/round-64/receipts/qdc-flagmatrix-probe.ps1`, getters only, whitelist
unchanged: counts, rationals, flags, enum integers — no ids, no LUID halves, no names)
ran the four documented shapes — 0x02 (the r63 baseline), 0x12, 0x42, 0x52 — twice,
byte-identical runs (`qdc-matrix-run1.json` / `qdc-matrix-run2.json`); the 0x02 leg
crosschecks 19/19 stable fields AGREE against the r63 committed snapshot
(`qdc-matrix-crosscheck.py` + `qdc-matrix-crosscheck.txt`). The r63 baseline still
holds at r64 (`tools/mado-win-displayconfig.py` live re-run CLEAN,
`windisplayconfig-recheck-r64.txt`).

| row | claim (this host, 2026-11-01) | re-derivation |
|---|---|---|
| H29 | The virtual-refresh-aware shape does not change the answer: 0x42 returns the identical table to the r63 baseline (buffer 1/2, rc 0/0, modes [2, 1], path_flags 0x1, target idx 0, refresh 64/1, pixelRate/hSyncFreq/vSyncFreq all the 0xFFFFFFFE sentinel, active/total 1920x1080) — D05's "Windows-11 virtual-refresh artifact" residue branch is now measured on this host, and it is not the cause | `powershell.exe -NoProfile -NonInteractive -NoLogo -ExecutionPolicy Bypass -File .ufo/waves/round-64/receipts/qdc-flagmatrix-probe.ps1` → rc 0 twice, byte-identical by `cmp`; the `qdc_flags=66` (0x42) block of `qdc-matrix-run1.json` |
| H30 | The virtual-mode-aware shapes change the table structure instead: under 0x12 and 0x52 the buffer answers 1 path / 3 modes, the mode table gains a third entry with `infoType` 3 (the documented DESKTOP_IMAGE value, S431/K51), the path's `flags` gain 0x8 (the documented `DISPLAYCONFIG_PATH_SUPPORT_VIRTUAL_MODE`, S426/K46), and the path's `targetInfo.modeInfoIdx` moves 0 → 2 — naming the new DESKTOP_IMAGE entry, not the TARGET entry. The probe's decode guard (decodes only `infoType == 2`, the r63 tool's rule) therefore emits `target_mode = null` for these shapes: at the index the path names, the union storage is a non-TARGET member and is deliberately not decoded (the r63 rejected-row discipline kept) | same receipts; the `qdc_flags=18` (0x12) and `qdc_flags=82` (0x52) blocks of `qdc-matrix-run1.json` |
| H31 | D05 disposition after the probe: **narrowed, not flipped**. No documented query shape returns decoded frequencies: the virtual-refresh flag returns the identical sentinel (H29); the virtual-mode flag re-indexes the path's target entry to a non-TARGET union member (H30). The sentinel's cause stays `[UNK]`; D05's own Flip sentence ("a query shape that returns decoded frequencies") did not fire. The residue that remains named is the driver-class / second-host reading, operator-scoped | this Update section; D05's original text above stands byte-untouched (append-only) |
| J29 | H29/H30 ↔ K44/K46/K51: the flag table's two virtual flags each answer a distinct D05 residue branch on this host — the refresh flag (0x40, Windows 11) changes nothing in the mode data, the mode flag (0x10, Windows 10) adds the documented SUPPORT_VIRTUAL_MODE path flag and a DESKTOP_IMAGE mode entry and re-points the target index — the documented vocabulary (SOURCE=1 / TARGET=2 / DESKTOP_IMAGE=3) decides the third entry's class with no new page opened | rows above; K44/K46/K51 (S424 re-opened 2026-11-01; S426/S431 held from the r63 sweep) |

Limits of this Update: the DESKTOP_IMAGE union member stays undecoded (same rejected
row class as SOURCE_MODE); no rendered-pixel claim (the screen-capture-scope L0 stays
open, routed around); point-in-time; the probe emits no target/source ids, no LUID
halves, no names; no Set*/Change* verb exists in it (topology, mode and refresh
changes stay operator-owned).

## Update (round 64) — the r63 receipt's fixture citation repaired (carry-in)

The r63 closure routed: the error-path receipt
`.ufo/waves/round-63/receipts/windisplayconfig-error-path.txt` cites its input fixture
`…receipts/broken-fixture.json`, which never landed. Round 64 commits a fixture at the
cited path and re-derives the verdict against the committed bytes. Disclosure: the
committed fixture is the round-64 re-creation (a truncated JSON snapshot whose
`JSONDecodeError` the parse stage refuses) — the r63 original's bytes were ephemeral
and are not recoverable; the r63 receipt remains the record of the r63 run, and the
round-64 receipt (`windisplayconfig-errorpath-r64.txt`) records the re-derivation:
`MADO_WINDISPLAYCONFIG: ERROR (stage=parse detail=JSONDecodeError in snapshot
.ufo/waves/round-63/receipts/broken-fixture.json)`, rc=2 — the same verdict class and
the same whitelisted detail line as the r63 receipt, raw bytes never echoed. The
citation now resolves to committed bytes; the class is mechanized as
`tools/mado-receipt-citecheck.py` (its red run at the r63 base rev names exactly this
citation MISSING — `citecheck-red-base-rev.txt`).
