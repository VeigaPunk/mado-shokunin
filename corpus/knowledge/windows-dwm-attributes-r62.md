source: corpus/SOURCES.md rows S418-S423 (Microsoft Learn dwmapi/winuser reference, tier A, opened 2026-11-01 in full via fetch before any row was written; every quote below is a verbatim substring of an opened page body)
verified-at: 2026-11-01, Windows 11 Home build 26200 host; probe `.ufo/waves/round-62/receipts/dwm-attributes-probe.ps1` executed twice rc=0 (dwm-run1/run2.txt) and once more inside the crosscheck; observer `tools/mado-win-dwm.py` (VERSION r62-v1) selftest 11/11, live rc=0 twice, crosscheck 5/5 (receipts `.ufo/waves/round-62/receipts/`)
recheck: next Windows-plane round or any operator display/composition change; the timing-query disposition (D04) re-derives from the committed probe bytes alone

# Windows DWM client-attribute plane (round 62)

The compositor-side window attributes Windows exposes to callers: composition
state, cloaking, the extended-frame-bounds pair, and composition timing. This
is the plane *between* the layers already held: r57/r59 observed DWM from the
outside (composition on, service model), r58/r60 observed the DPI
virtualization layer, r61 the display topology; this entry reads the DWM
client API surface itself (`dwmapi.dll` getters). Layers stay separate per
QUALITY 15/16: documentation rows are `[INF-docs]`, host rows carry their
re-derivation command, and every getter failure is CHECK FAILED, never a
measurement.

## Host rows (observed 2026-11-01, each with its re-derivation)

| row | observation | re-derivation |
|---|---|---|
| H21 | `DwmIsCompositionEnabled` → TRUE, hr 0 — the same composition-state pin r59 measured; consistent across both hosts-observed rounds | `powershell.exe -NoProfile -NonInteractive -NoLogo -ExecutionPolicy Bypass -File .ufo/waves/round-62/receipts/dwm-attributes-probe.ps1` → `"composition_enabled":true,"composition_hr":0` (rc=0, runs byte-identical except the census counters; receipt `dwm-run1.txt`) |
| H22 | cloaked-window census: 161-170 top-level windows across five executions (the churn class — the count moves with desktop activity), 13 visible every time, 14 cloaked every time, reasons **7 app + 7 shell + 0 inherited** in every execution, `attr_failed` 0 in every execution; the tool never records which windows, only counts | `python tools/mado-win-dwm.py` → `MADO_WINDWM: CLEAN (composition=on reasons=app+shell timing=unavailable(hr=0x88980090))` rc=0 ×2 (`windwm-live-run1/2.txt`); churn named per field in `windwm-live-churn-diff.txt` (only `windows.top_level` moved: 168→170) |
| H23 | the probe's own console window: `GetWindowRect` [130,130,1123,649] beside `DWMWA_EXTENDED_FRAME_BOUNDS` [137,130,1116,642] — the frame is inset 7 px left/right/bottom, 0 px top (the same 7 px inset in every execution; the rect pair's absolute position moves with each spawn's console placement — spawn-positional, not churn in the delta) | same receipts, `"own_window"` object; the delta re-derives by subtraction on the committed JSON lines |
| H24 | `DwmGetCompositionTimingInfo` **fails on this host in both documented call shapes**: the Windows 8.1+ NULL shape and the non-NULL shape the page promises E_INVALIDARG for both return the same undocumented HRESULT `0x88980090`; `cbSize` 320 per the documented 39-member layout; deterministic across every committed execution (probe ×2 + crosscheck ×1 + tool ×2 + from-file re-derivations); finding **D04**, cause `[UNK]` | `"timing":{"ok":false,"hr":-2003304304,"cb_size":320,"nonnull_hr":-2003304304}` in `dwm-run1.txt` (−2003304304 = 0x88980090 signed); re-derivation identical to H21 |

## Documented rows (`[INF-docs]`, dated, quotes verbatim from the opened pages)

| row | source | fact |
|---|---|---|
| K38 | S418 (ms.date 2019-05-30, git_commit fa53641576e3603fa7b66d3a4ad969d3ce49d6f3, updated 2025-07-01) | DwmGetWindowAttribute: "Retrieves the current value of a specified Desktop Window Manager (DWM) attribute applied to a window."; "If the function succeeds, it returns S_OK. Otherwise, it returns an HRESULT error code." |
| K39 | S419 (ms.date 2024-01-21, git_commit 75d8a6a0145431644157a4dabc09260f0d73118f, updated 2026-03-09) | DWMWA_CLOAKED: "If the window is cloaked, provides one of the following values explaining why. DWM_CLOAKED_APP (value 0x0000001). The window was cloaked by its owner application. DWM_CLOAKED_SHELL (value 0x0000002). The window was cloaked by the Shell. DWM_CLOAKED_INHERITED (value 0x0000004). The cloak value was inherited from its owner window."; set-side DWMWA_CLOAK: "Cloaks the window such that it is not visible to the user. The window is still composed by DWM."; DWMWA_EXTENDED_FRAME_BOUNDS: "Retrieves the extended frame bounds rectangle in screen space."; the enum's numeric anchor is the page's note "The value of DWMWA_NCRENDERING_ENABLED is 1" (so CLOAKED = 14, EXTENDED_FRAME_BOUNDS = 9 in the series; the two explicit values 20 and 33 in the syntax block hold the series open) |
| K40 | S420 (ms.date 2018-12-05, git_commit fa53641576e3603fa7b66d3a4ad969d3ce49d6f3, updated 2025-07-01) | DwmGetCompositionTimingInfo: "Retrieves the current composition timing information for a specified window."; the hwnd pin: "Starting with Windows 8.1, this parameter must be set to NULL. If this parameter is not set to NULL, DwmGetCompositionTimingInfo returns E_INVALIDARG."; "The cbSize member of this structure must be set before this function is called." |
| K41 | S421 (ms.date 2018-12-05, git_commit 9267262487657894a8af112d7165006fed5035a7, updated 2024-02-22) | DWM_TIMING_INFO: 39 members, declaration order read from the page's syntax block (the C# mirror in the committed probe follows it field-for-field); rateRefresh: "The monitor refresh rate."; qpcRefreshPeriod: "The monitor refresh period."; rateCompose: "The composition rate."; cRefresh: "The DWM refresh counter."; Remarks: "Both DWM_FRAME_COUNT and QPC_TIME are defined in Dwmapi.h as ULONGLONG." |
| K42 | S422 (ms.date 2018-12-05, git_commit 9267262487657894a8af112d7165006fed5035a7, updated 2024-02-22) | UNSIGNED_RATIO: `uiNumerator` / `uiDenominator`, UINT32 — "Defines a data type used by the Desktop Window Manager (DWM) APIs. It represents a generic ratio and is used for different purposes and units even within a single API." (the units warning is why the entry never converts rateRefresh to Hz without naming the join) |
| K43 | S423 (ms.date 2018-12-05, git_commit fa53641576e3603fa7b66d3a4ad969d3ce49d6f3, updated 2025-07-01) | GetWindowRect: "Retrieves the dimensions of the bounding rectangle of the specified window."; "GetWindowRect is virtualized for DPI."; "In Windows Vista and later, the Window Rect now may include invisible resize borders."; "To get the visible window bounds, not including the invisible resize borders, use DwmGetWindowAttribute, specifying DWMWA_EXTENDED_FRAME_BOUNDS. Note that unlike the Window Rect, the DWM Extended Frame Bounds are not adjusted for DPI."; "the bottom-right coordinates of the returned rectangle are exclusive" |

## Joins

| row | join |
|---|---|
| J21 | H21 (composition TRUE) beside r59's composition pin (`windows-dwm-service-model-r59.md` H10, S400's manifest caveat): the same documented getter re-measured a second day on the same host; the S400 note (a manifest-less process receives FALSE) stays the reason a TRUE binds the querying context, not a universal host fact — both probes run under powershell.exe, the same context |
| J22 | H22's cloaking is a compositor-side state, documented distinct from user32 visibility: K39's set-side text says a cloaked window "is still composed by DWM"; the measured 13 visible against 14 cloaked never cross-tabulates per window (the tool records counts, never per-window rows), so how many cloaked windows are also IsWindowVisible stays `[UNK]` — the two layers are separate axes, not a partition |
| J23 | H23's 7 px inset is the K43 resize-border cause observed; the second documented cause (DPI virtualization of the Window Rect alone) is vacuous at this host's effective 96 DPI — the r60 J13 shape (caller unaware, metrics at 96 make the virtualization invisible); the two causes stay separated in the record, and one console window grounds no generalization to other windows' frames |
| J24 | D04 beside S420's documented vocabulary: the page documents S_OK and (for non-NULL) E_INVALIDARG; the host returns `0x88980090` for both shapes — a HRESULT outside the page's vocabulary, so the documented non-NULL E_INVALIDARG pin does not reproduce on build 26200. This is the DWM plane's second documented-vs-host divergence (after r57 D01's era mixing); the failure's cause is `[UNK]` and is not guessed at (the struct layout is per K41, cbSize 320, so the record does not blame marshaling it has not disproven) |

## Findings

- **D04** (host behavior beside the documentation): `DwmGetCompositionTimingInfo`
  fails with `0x88980090` on this host in both documented call shapes —
  the required NULL shape and the non-NULL shape the page promises
  E_INVALIDARG for — with `cbSize` 320 per the documented layout,
  deterministic across every committed execution. The compositor refresh
  ratio (`rateRefresh`) that would have joined r61's mode frequency
  (H20, 64 Hz) is therefore **unobserved**: the join never lands on this
  host by this getter, and no other getter is substituted for it this
  round. Residue: which Windows builds fail this way, and whether the
  timing path moved behind another surface, `[UNK]`.

## Limits (restated, not hidden)

- Point-in-time observation; census counters churn with desktop activity
  (named per field in `windwm-live-churn-diff.txt`); the verdict line is
  built from structure, the JSON line carries the numbers.
- No per-window rows exist anywhere in this entry: counts and reason
  buckets only; handles, titles and process names are never collected.
- No Shell surface is read (the r61 J17 taskbar boundary unchanged); no
  rendered-pixel claim (the screen-capture-scope L0 question stays open,
  routed around).
- The timing plane is unobserved on this host (D04); every rateRefresh
  sentence here is documentation-layer (`[INF-docs]`), never a host fact.
- No Set*/Move*/Change* verb exists in the probe or the tool; cloaking and
  attribute writes stay operator-owned.
