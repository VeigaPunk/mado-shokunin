source: S398, S399, S400, S401 (corpus/SOURCES.md; Microsoft Learn, opened 2026-10-31)
verified-at: 2026-10-31
recheck: on-release

# The Windows desktop plane observed read-only (round 57)

**Scope.** The lane's live host changed after round 56. This entry is the first
sourced record of the new host's desktop plane — Windows 11 Home, build 26200 —
observed read-only on 2026-10-31: window-manager state, DPI facts and
compositor (DWM) state. It follows the lane's layers rule (QUALITY 15/16):
every upstream-documentation claim stays a dated `[INF-docs]` claim, every host
sentence cites the command that produced it, and the two are never substituted
for each other. The omarchy plane this entry replaces as the live surface is
recorded absent, with dated probes, in `PROVINCE.md` (round-57 host-change
record) and `SKILL.md` § Round 57.

**Sources.** Rows S398-S401 (opened 2026-10-31, `corpus/SOURCES.md`): the
Microsoft Learn High-DPI development page (S398), the Desktop Window Manager
overview (S399), the `DwmIsCompositionEnabled` function page (S400) and the
`System.Windows.Forms.Screen` class reference (S401). Tier A, `mined`.

## 1. Host claims (H rows, each with its re-derivation command)

| id | proposition | command (read-only) | observed 2026-10-31 |
|---|---|---|---|
| H01 | the live host is Windows 11 Home, build 26200, 64-bit | `powershell Get-CimInstance Win32_OperatingSystem` | `Caption=Microsoft Windows 11 Home Version=10.0.26200 BuildNumber=26200 OSArchitecture=64-bit` |
| H02 | one display: `\\.\DISPLAY1`, primary, 1920x1080, 32 bpp | `Screen.AllScreens` (in the round-57 tool and independently) | `SCREENS 1`; `SCREEN \\.\DISPLAY1 primary=True bounds=0,0,1920x1080 bpp=32` |
| H03 | system DPI is 96 (100% scaling); `LogPixels` is unset | two registry-read layers | `Get-ItemProperty` `AppliedDPI=96`; `Microsoft.Win32.Registry.GetValue` = 96; `reg query` shows `0x60`; `LogPixels` → unset (try/catch empty) |
| H04 | DWM composition reports enabled, call succeeds | `dwmapi!DwmIsCompositionEnabled` | `hr=0 enabled=True` |
| H05 | the window census is a point-in-time set of processes with a main window | `Get-Process | Where MainWindowHandle -ne 0` | 2026-10-31 two samples: 7 then 6 processes; names observed (superset): `1Password, ApplicationFrameHost, chrome, explorer, stremio-service, SystemSettings, ZCode`; foreground at sample 1: `chrome` (pid 22288), at sample 2: `ZCode` (pid 12068) — the foreground process changes between runs and is never bound |

## 2. Documented claims (K rows — dated [INF-docs], never host facts)

| id | proposition (≤25-word quotes verbatim from the named row) | row / anchor | class |
|---|---|---|---|
| K01 | "By default, the system considers desktop applications DPI unaware and bitmap-stretches their windows." | S398 § DPI Awareness Mode | [INF-docs] |
| K02 | "DPI unaware applications render at a fixed DPI value of 96 (100%)." | S398 § DPI Unaware | [INF-docs] |
| K03 | "Desktop composition is performed by the Desktop Window Manager (DWM)." | S399 intro | [INF-docs] |
| K04 | "As of Windows 8, DWM composition is always enabled." | S400 § Parameters (Note) | [INF-docs], with the page's own caveat (below) |
| K05 | "Represents a display device or multiple display devices on a single system." | S401 § Definition | [INF-docs] (the instrument's documented ground) |
| K06 | AllScreens: "Gets an array of all displays on the system." | S401 § Properties | [INF-docs] |
| K07 | System-DPI-aware apps take "the DPI of the primary display at the time the current user session was started". | S398 § awareness table (System row) | [INF-docs] |

## 3. Claim-to-host joins (the only place K and H touch)

| join | documented side | host side | verdict |
|---|---|---|---|
| J01 | K02: an unaware process renders at a fixed 96 DPI | H03: the system DPI **is** 96 here — the condition K02 describes ("greater than 96") does not arise on this host | `agreement*` (vacuous agreement: the stretch path is unexercised at 96 DPI; the value pair matches) |
| J02 | K04: composition always enabled since Windows 8 | H04: `DwmIsCompositionEnabled` → TRUE | `agreement` — with the documented caveat named: the same note says a process **without** a Windows 8 compatibility manifest entry receives FALSE, so the observed TRUE binds the querying process's context, not a machine-global fact; which manifest clause applied here is `[UNK]` |
| J03 | K06: `AllScreens` gets all displays on the system | H02: array length 1 on a single-display host | `agreement` (count 1 = count 1; a multi-display host would test the row harder — named limit) |
| J04 | K05: the Screen object models a display device | H02: device name, bounds and primary flag all populated | `agreement` (instrument ground) |

## 4. Divergence / drift finding

| id | finding | class | recommendation |
|---|---|---|---|
| D01 | S399 (page dated 2018-05-31, refreshed 2025-03-11) also states the DWM "runs as a Windows service" that "can be enabled and disabled through the Administrative Tools Control Panel item, under Services, as Desktop Window Manager Session Manager" — while S400 (same documentation set) states composition is always enabled as of Windows 8, and the observed host (build 26200) reports TRUE. The two pages disagree across eras; which sentence describes the build-26200 service model is not resolvable from these rows. | source-internal drift (era mixing in a refreshed page) | treat the service sentence as Vista/7-era prose, not a build-26200 fact; a future row pinning the Windows 11 service model (e.g. `DwmApi` service documentation for 11) would close it. **Flip:** a sourced row that states the Win11 DWM service model. |

## 5. Verify (re-runnable, read-only)

```bash
# the instrument (round-57 C2 capability): selftest, live, snapshot re-derivation
python tools/mado-win-desk.py --selftest          # MADO_WINDESK_SELFTEST: 9/9 assertions passed, exit 0
python tools/mado-win-desk.py                     # MADO_WINDESK: CLEAN (screens=1 dpi=96 dwm=on windows=<n>), exit 0
python tools/mado-win-desk.py --from-file SNAP    # re-derives the verdict from a captured JSON snapshot
```

Independent probes (2026-10-31, executed separately from the tool):

```text
SCREENS 1 / SCREEN \\.\DISPLAY1 primary=True bounds=0,0,1920x1080 bpp=32   (Screen.AllScreens)
APPLIEDDPI 96; reg query 'HKCU\Control Panel\Desktop\WindowMetrics' /v AppliedDPI → 0x60
DWM_COMPOSITION hr=0 enabled=True                                          (dwmapi P/Invoke)
WINDOWS_WITH_MAIN 6..7; PROCESS_NAMES (point-in-time, see H05)
```

Cross-check receipt (`.ufo/waves/round-57/receipts/crosscheck.txt`, quoted in
the round-57 report):
**5/5 stable fields AGREE** (screens.count, primary.bounds, applied_dpi,
reg_applied_dpi, dwm flag) between one tool run and independently executed
probes; the window census is bound only as a point-in-time observation (H05).
Absence side of the plane: `bash tools/mado-verify.sh --no-live` on this host →
`MADO_VERIFY: DIVERGED (17 fail, 7 unknown, 2 pass)`, first fail
`hypr.file.root` (missing `~/.config/hypr/hyprland.conf`) — the omarchy plane
is gone; that verdict is the absence record, not a regression claim.

## 6. Limits and unknowns

- No rendered pixel is observed: the DWM flag is a composition-state answer,
  not a display-output claim; nothing about animation, glass, or frame pacing
  is measured. `[UNK]`.
- No per-monitor DPI table: `AppliedDPI`/`LogPixels` are system-level values;
  `GetDpiForMonitor`/`GetDpiForWindow` per-display joins are future ground.
- The window census is point-in-time and the foreground process changes between
  runs (H05); only the stable fields are cross-checked.
- K04's manifest caveat leaves which compatibility clause applied `[UNK]`.
- D01 is open: the build-26200 DWM service model is unrowed.

## Errata (round 58)

- § 5's "selftest … 9/9" line records the round-57 observation and stands as
  history; round 58 folded the malformed-snapshot ERROR path into the tally
  (the r57 closure's routed receipt gap), so the current count is **10/10**
  (receipt `.ufo/waves/round-58/receipts/windesk-selftest-10.txt`; committed
  ERROR run `windesk-error-path.txt`). The tool bytes changed with it
  (`VERSION r58-v1`); every other § 5 command reads unchanged.
- The § 6 limit "No per-monitor DPI table" closed the same round:
  [windows-permonitor-dpi-r58.md](windows-permonitor-dpi-r58.md) lands the
  join (rows S402-S404; finding D02 there).
- The lane spawns one read-only PowerShell child per observation; it never
  mutates settings, never reads window titles, clipboard, environment values or
  file contents, and never echoes raw child output (round-56 M56-17 rule).

## Errata (round 59)

- D01 (§ 4) is closed: [windows-dwm-service-model-r59.md](windows-dwm-service-model-r59.md)
  lands the sourced model row (S405, Compatibility Cookbook, opened 2026-10-31) and the
  build-26200 host joins (no DWM service registered; `sc query UxSms` rc 1060; dwm.exe
  hosts no services; composition enabled). The flip D01 named is met; the residue (no
  Win11-labeled model sentence in the bounded sweep) is named in the r59 entry. The
  § 6 line "D01 is open" is history as of the r59 entry.
- The entry's header gained the provenance trio the corpus contract requires (CORPUS.md,
  "a new knowledge entry opens with its provenance trio" — `source:`, `verified-at:`,
  `recheck:` first): a round-59 correction, insertion only, no existing line changed.
  `windows-permonitor-dpi-r58.md` gained its trio the same way.
