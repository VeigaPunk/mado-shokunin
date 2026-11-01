source: S412, S413, S414, S415, S416, S417 (corpus/SOURCES.md; Microsoft Learn, opened
  2026-11-01 in full before any row was written)
verified-at: 2026-11-01
recheck: on-release

# The native display-topology plane on the Windows host (round 61)

**Scope.** Rounds 57-60 hold the managed Screen layer (r57: device name, bounds,
primary flag, bpp), the per-monitor DPI modes (r58), the DWM service model (r59)
and the metrics/awareness join (r60). No committed entry holds the *native*
enumeration surface or the display-mode layer: `EnumDisplayMonitors` +
`GetMonitorInfo`/MONITORINFOEX (device name, monitor rectangle, **work area**,
primary flag) and `EnumDisplaySettings` + `DEVMODE` (current/registry settings,
**refresh rate**, the graphics-mode index series). This entry closes that gap
with a read-only probe on 2026-11-01 (one `powershell.exe` child, two
byte-identical runs) and the round's durable observer
`tools/mado-win-display.py`. The lane's layers rule (QUALITY 15/16) holds
throughout: every documentation sentence stays a dated `[INF-docs]` claim,
every host sentence cites the command that produced it.

**Sources.** Rows S412-S417 (opened 2026-11-01, `corpus/SOURCES.md`): the
`EnumDisplayMonitors` function page (S412), the `GetMonitorInfoW` function page
(S413), the `MONITORINFO` and `MONITORINFOEXW` structure pages (S414, S415),
the `EnumDisplaySettingsA` function page (S416 — the page documents the
`EnumDisplaySettings` family, `EnumDisplaySettingsW (Unicode) and
EnumDisplaySettingsA (ANSI)`, and the probe calls the W entry point) and the
`DEVMODEW` structure page (S417). Tier A, `mined`.

## 1. Host claims (H rows, each with its re-derivation command)

| id | proposition | command (read-only) | observed 2026-11-01 |
|---|---|---|---|
| H17 | exactly one display monitor enumerates through the native path (the `EnumDisplayMonitors` callback fires once), equal to the managed count (`Screen.AllScreens` length 1; r57 H02's count) | `.ufo/waves/round-61/receipts/display-probe.ps1` (managed half) and `tools/mado-win-display.py` (native half) | probe `monitor_count=1`; tool `monitors=1` — two runs each, all rc=0, all byte-identical (receipts `display-probe-run1/2.txt`, `windisplay-live-run1/2.txt`) |
| H18 | the primary monitor's MONITORINFOEXW reads: szDevice `\\.\DISPLAY1`, rcMonitor (0,0,1920,1080), dwFlags carries MONITORINFOF_PRIMARY — field-for-field agreement with the managed layer (r57 H02: device name, bounds, primary) and with this round's probe | the tool (native `EnumDisplayMonitors` → `GetMonitorInfoW`) vs the probe (managed `Screen.PrimaryScreen`) | tool: `primary=\\.\DISPLAY1`, `monitor=[0,0,1920,1080]`, `primary=true`; probe: `device=\\.\DISPLAY1`, `bounds={0,0,1920,1080}`, `primary=true`; crosscheck 5/5 AGREE (`windisplay-crosscheck.txt`) |
| H19 | the primary's work-area rectangle rcWork is (0,0,1920,1032): same origin and width as the monitor rectangle, 48 px shorter (1032 vs 1080) — the documented work-area shape observed; which appbar surface occupies the subtracted band is `[UNK]` (the taskbar is never read) | same probe and tool (`Screen.WorkingArea` vs native rcWork) | both read `work h=1032`; `1080 − 1032 = 48` — probe and tool byte-identical across runs |
| H20 | the current display mode (ENUM_CURRENT_SETTINGS) is 1920x1080 @ 64 Hz, 32 bpp at desktop position (0,0); the registry settings (ENUM_REGISTRY_SETTINGS) are identical on this host; the graphics-mode index series returns exactly **1** mode before the documented zero return (series bounded at 256) | `EnumDisplaySettingsW(device, -1 / -2 / i)` in the probe and the tool | `mode_current={1920,1080,64,32,pos(0,0)}`; `mode_registry={1920,1080,64,32}`; `mode_list_count=1` — both artifacts, byte-identical runs |

## 2. Documented claims (K rows — dated [INF-docs], never host facts)

| id | proposition (≤25-word quotes verbatim from the named row) | row / anchor | class |
|---|---|---|---|
| K28 | EnumDisplayMonitors "enumerates display monitors (including invisible pseudo-monitors associated with the mirroring drivers)" | S412 § Description | [INF-docs] |
| K29 | with hdc NULL and lprcClip NULL the documented behavior is "Enumerates all display monitors. The callback function receives a NULL HDC." | S412 § Remarks (behavior table, NULL/NULL row) | [INF-docs] |
| K30 | GetMonitorInfo "retrieves information about a display monitor"; "You must set the cbSize member of the structure to sizeof(MONITORINFO) or sizeof(MONITORINFOEX) before calling" | S413 § Description + § Parameters (lpmi) | [INF-docs] |
| K31 | rcWork: "A RECT structure that specifies the work area rectangle of the display monitor, expressed in virtual-screen coordinates." | S414 § Members (rcWork) | [INF-docs] |
| K32 | MONITORINFOF_PRIMARY: "This is the primary display monitor." | S414 § Members (dwFlags table) | [INF-docs] |
| K33 | szDevice: "A string that specifies the device name of the monitor being used." | S415 § Members (szDevice) | [INF-docs] |
| K34 | EnumDisplaySettings "retrieves information about one of the graphics modes for a display device"; "Graphics mode indexes start at zero"; the series continues "until the return value is zero"; ENUM_CURRENT_SETTINGS "Retrieve the current settings", ENUM_REGISTRY_SETTINGS "Retrieve the settings … stored in the registry" | S416 § Description + § Parameters (iModeNum) | [INF-docs] |
| K35 | dmDisplayFrequency: "the frequency, in hertz, of a display device in its current mode"; dmPelsWidth/dmPelsHeight: "the width/height, in pixels, of the visible device surface"; dmBitsPerPel: "the color resolution, in bits per pixel" | S417 § Members | [INF-docs] |
| K36 | "Apps that you design to target Windows 8 and later can no longer query or set display modes that are less than 32 bits per pixel (bpp)" | S416 § Description (Note) | [INF-docs] |
| K37 | "This API does not participate in DPI virtualization. The output given is always in terms of physical pixels, and is not related to the calling context." | S416 § Remarks (DPI Virtualization) | [INF-docs] |

## 3. Claim-to-host joins (the only place K and H touch)

| join | documented side | host side | verdict |
|---|---|---|---|
| J17 | K31 + K32: the work area is a documented sub-rectangle of the display monitor; the primary monitor is flagged | H18 + H19: rcWork (0,0,1920,1032) is a strict sub-rectangle of rcMonitor (0,0,1920,1080) on the flagged primary | `agreement*` — directional agreement on the documented shape; *which* surface owns the subtracted 48 px band is `[UNK]` (the probe and the tool never read the taskbar — Shell surfaces stay outside; named limit) |
| J18 | K33 + K32: the primary monitor carries a device name | H18: szDevice `\\.\DISPLAY1` equals the managed layer's primary DeviceName (this round's probe; r57 H02's device name) — cross-layer agreement, native vs managed | `agreement` |
| J19 | K34 + K35: the function documents the five DEVMODE members it sets (dmBitsPerPel, dmPelsWidth, dmPelsHeight, dmDisplayFlags, dmDisplayFrequency); each member's display meaning is dated | H20: the queried members are populated in the reported current mode — 1920x1080, 64 Hz, 32 bpp | `agreement` (dmDisplayFlags was not read by the probe — a named omission, not an `[UNK]` in a claim: no row asserts its value) |
| J20 | K37 + K36: the mode layer reports physical pixels regardless of calling context, and Win8+-manifested apps see only ≥32 bpp modes | H20 + H17: the mode rectangle (1920x1080) equals the DPI-affected layers' rectangle at effective 96 (r60's H14) with no virtualization caveat needed — the equality is documented-shape, not a vacuous scale accident; the observed 32 bpp is the only class the note leaves | `agreement` (the caller-awareness `[UNK]` the r58/r60 entries carried does not arise here: S416 states the API ignores the calling context) |

## 4. Divergence / drift finding

| id | finding | class | recommendation |
|---|---|---|---|
| D03 | the graphics-mode index series returns exactly **one** mode before the documented zero return, and ENUM_REGISTRY_SETTINGS equals ENUM_CURRENT_SETTINGS on this host (H20). The display reports a single documented mode while the DPI layer splits three ways (r58 D02: effective 96, angular 91, raw 92). The two layers answer different questions: the mode list is a per-display-device driver surface; the DPI modes are per-monitor Shcore queries. | documented-shape observation, not a defect | no mode-switch reasoning is possible from the documented enumeration on this host: it offers no alternative mode. Display-mode changes stay operator-owned in any case (the round's tool contains no Set*/Change* verb). **Flip:** a driver update or display change that grows the index series past 1. |

## 5. Verify (re-runnable, read-only)

```bash
# the probe (committed receipt artifact; managed topology + one mode P/Invoke)
powershell -NoProfile -NonInteractive -NoLogo -ExecutionPolicy Bypass \
  -File .ufo/waves/round-61/receipts/display-probe.ps1
# expect: rc=0; monitor_count=1; work h=1032; mode_current 1920x1080@64 bpp32;
#         mode_list_count=1
# committed receipts: display-probe-run1.txt, display-probe-run2.txt (byte-identical)
# the durable observer (round-61 C3):
python tools/mado-win-display.py --selftest      # 10/10, exit 0
python tools/mado-win-display.py                 # MADO_WINDISPLAY: CLEAN (monitors=1 …)
python tools/mado-win-display.py --from-file \
  .ufo/waves/round-61/receipts/windisplay-snapshot.json
python .ufo/waves/round-61/receipts/display-crosscheck.py   # 5/5 AGREE
```

## 6. Limits and unknowns

- Point-in-time: topology and mode facts are stable while no display change
  occurs; the crosscheck binds stable fields only.
- The subtracted work-area band's owner (taskbar vs another appbar) is
  `[UNK]` — neither artifact reads the taskbar; no Shell surface is queried.
- Pseudo-monitors: S412 says mirroring pseudo-monitors are enumerated while
  SM_CMONITORS "counts only the display monitors" — on this single-display
  host the native and managed counts agree at 1, and the join that would
  separate them is unexercised (named limit, J20/K28).
- The mode index series is bounded at 256 in both artifacts (documented
  series shape: increment until the zero return); the documented caching note
  (iModeNum 0 initializes the cache) applies to the series order — the count
  is taken after the -1/-2 queries in both artifacts.
- No EDID/driver tables are read (the r58 entry's limit carried): the panel's
  physical diagonal stays `[UNK]`.
- EnumDisplaySettings's documented failure return is 0: the tool treats a
  zero frequency/dimension/bpp in a reported mode as CHECK FAILED, never a
  measurement (r60's GetSystemMetrics 0 rule, same class).
