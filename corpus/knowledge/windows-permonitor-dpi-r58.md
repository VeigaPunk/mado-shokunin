source: S402, S403, S404 (corpus/SOURCES.md; Microsoft Learn, opened 2026-10-31; S403 is an
  archived previous-versions page, status carried in the row)
verified-at: 2026-10-31
recheck: on-release

# The per-monitor DPI join on the Windows host (round 58)

**Scope.** Round 57 recorded the lane's live Windows host (Windows 11 Home,
build 26200) at the system-DPI layer only: `AppliedDPI`/`LogPixels` are
system-level values, and the r57 entry named the per-monitor join as future
ground (`windows-desktop-plane-r57.md` § 6: "`GetDpiForMonitor`/
`GetDpiForWindow` per-display joins are future ground"). This entry closes
that gap with a read-only probe on 2026-10-31: one `HMONITOR` queried through
`GetDpiForMonitor` in all three documented `MONITOR_DPI_TYPE` modes, plus the
foreground window through `GetDpiForWindow`. The lane's layers rule (QUALITY
15/16) holds throughout: every documentation sentence stays a dated
`[INF-docs]` claim, every host sentence cites the command that produced it.

**Sources.** Rows S402-S404 (opened 2026-10-31, `corpus/SOURCES.md`): the
`MONITOR_DPI_TYPE` enumeration reference (S402), the `GetDpiForMonitor`
function page — an archived previous-versions page, status noted (S403) — and
the `GetDpiForWindow` function page (S404). Tier A, `mined`.

**Source discipline note (this round's own mistake, kept visible).** The
first probe draft labeled `dpiType` 1 as raw and 2 as angular — an ordering
taken from an unopened search snippet. Opening S402/S403 before writing any
row caught it: both pages state `MDT_ANGULAR_DPI = 1` and `MDT_RAW_DPI = 2`.
The probe was corrected and re-run; the committed receipts carry the corrected
labels. Lesson `corpus/lessons/round-58.md` (M58-2).

## 1. Host claims (H rows, each with its re-derivation command)

| id | proposition | command (read-only) | observed 2026-10-31 |
|---|---|---|---|
| H06 | the primary monitor's three documented DPI modes are distinct values: effective 96, angular 91, raw 92, queried through one `HMONITOR` | `.ufo/waves/round-58/receipts/dpi-probe.ps1` (P/Invoke `MonitorFromPoint` → `GetDpiForMonitor` types 0/1/2) | two runs, both rc=0: `mdt_effective.dpi=96 hr=0`; `mdt_angular.dpi=91 hr=0`; `mdt_raw.dpi=92 hr=0`; `hmonitor=65537` (0x10001) — receipts `dpi-probe-run1.txt`, `dpi-probe-run2.txt` |
| H07 | the foreground window reports a DPI of 96 through `GetDpiForWindow` (point-in-time foreground, never bound) | same probe (`GetForegroundWindow` → `GetDpiForWindow`) | `fg_window.present=true fg_window.dpi=96`, both runs |
| H08 | the display topology the probe joins against is one display, 1920x1080 at 32 bpp, primary | `Screen.AllScreens` inside the same probe | `\\.\DISPLAY1 primary=True bounds={X=0,Y=0,Width=1920,Height=1080} bpp=32` — agrees with the r57 entry H02 |

## 2. Documented claims (K rows — dated [INF-docs], never host facts)

| id | proposition (≤25-word quotes verbatim from the named row) | row / anchor | class |
|---|---|---|---|
| K08 | MDT_RAW_DPI: "This value is the linear DPI of the screen as measured on the screen itself." | S402 § Constants (MDT_RAW_DPI) | [INF-docs] |
| K09 | MDT_ANGULAR_DPI: "This DPI ensures rendering at a compliant angular resolution on the screen." | S402 § Constants (MDT_ANGULAR_DPI) | [INF-docs] |
| K10 | the enumeration's documented values are `MDT_EFFECTIVE_DPI = 0`, `MDT_ANGULAR_DPI = 1`, `MDT_RAW_DPI = 2` | S402 § Syntax | [INF-docs] (structural) |
| K11 | `GetDpiForMonitor` "Queries the specified monitor for the dots per inch (dpi) horizontal and vertical values." | S403 intro (archived page; DLL `Shcore.dll`, min client Windows 8.1) | [INF-docs] |
| K12 | for MDT_Effective_DPI, "the returned dpi value includes any changes that the user made to the dpi" | S403 § Remarks | [INF-docs] |
| K13 | `GetDpiForWindow` "Returns the dots per inch (dpi) value for the specified window." | S404 intro | [INF-docs] |
| K14 | the returned DPI "depends on the DPI_AWARENESS" of the provided hwnd: UNAWARE → 96 (`USER_DEFAULT_SCREEN_DPI`), SYSTEM_AWARE → "The system DPI.", PER_MONITOR_AWARE → "The DPI of the monitor where the window is located." | S404 § Return value + § Remarks table | [INF-docs] |

## 3. Claim-to-host joins (the only place K and H touch)

| join | documented side | host side | verdict |
|---|---|---|---|
| J05 | K12 + K10: the effective mode incorporates the user's scale factor for the display | H06: effective 96 on a host whose system scale is 100% (r57 H03: `AppliedDPI=96`) — the user-scale component is the identity here | `agreement*` (vacuous at 100% scaling, the same shape as the r57 entry's J01); which PROCESS_DPI_AWARENESS the probe child carried is `[UNK]` — the probe never queries its own awareness, and S402's own remark says all three settings are affected by it |
| J06 | K10 + K11: types 0/1/2 are documented, Shcore.dll exports the function since Windows 8.1 | H06: all three calls return `hr=0` (S_OK) on build 26200 | `agreement` (the archived page's own dpiType table carries the same 0/1/2 mapping as the current enum page — two pages, one mapping) |
| J07 | K13 + K14: the returned DPI depends on the window's awareness; both the UNAWARE branch (base 96) and the SYSTEM_AWARE branch (system DPI) yield 96 on this host | H07: foreground window reports 96 | `agreement` — with the branch ambiguity named: which awareness the foreground window holds is `[UNK]`, and both documented branches produce the observed value here |
| J08 | K08: raw DPI is "the linear DPI of the screen as measured on the screen itself" | H06: raw 92 for a 1920x1080 display — the linear-density identity `sqrt(1920²+1080²)/92 ≈ 23.9"` is panel-size arithmetic, and the panel diagonal is unobserved | `agreement` on the row's class (raw is panel-linear, not scale-adjusted); the physical diagonal stays `[UNK]` — the arithmetic is consistency context, not a claim |

## 4. Divergence / drift finding

| id | finding | class | recommendation |
|---|---|---|---|
| D02 | the three documented modes do not collapse on this host: effective 96 vs angular 91 vs raw 92 (H06). The per-monitor layer is therefore not a copy of the system value — contrast the r57 entry's J01, where the system-layer agreement at 96 was vacuous. The pages predict the direction of the gap (raw/angular exclude the user's scale factor; only effective includes it), and the observed gap matches: scale is 100%, so effective sits at the 96 base while the panel-derived values sit below it. | documented divergence, observed | any UI-scale decision must read MDT_EFFECTIVE_DPI only; MDT_RAW_DPI/MDT_ANGULAR_DPI values must never be fed to scale factors (they are panel facts, not scaling settings). **Flip:** a host where effective ≠ 96 with matching raw/angular would test the row harder; a multi-display host would test the per-monitor table (named limit below) |

## 5. Verify (re-runnable, read-only)

```bash
# the probe (committed receipt artifact; spawns one read-only PowerShell child)
powershell -NoProfile -NonInteractive -NoLogo -ExecutionPolicy Bypass \
  -File .ufo/waves/round-58/receipts/dpi-probe.ps1
# expect: rc=0; mdt_effective.dpi=96; mdt_angular.dpi=91; mdt_raw.dpi=92;
#         fg_window.dpi=96 (foreground is point-in-time; only its presence is stable)
# committed receipts: dpi-probe-run1.txt, dpi-probe-run2.txt (two stable runs)
```

## 6. Limits and unknowns

- Single-display host: the join covers one `HMONITOR` (count 1 = count 1,
  the same limit shape as the r57 entry's J03); a multi-display host would
  test the per-monitor table.
- The probe child's own PROCESS_DPI_AWARENESS is `[UNK]` (never queried);
  S402's remark states all three returned settings are affected by it.
- The foreground window is point-in-time; only `fg_window.dpi` is recorded
  and never bound to a process name.
- S403 is an archived previous-versions page (ms.date 2014-01-13): its
  dpiType table agrees with the current S402 enum on values 0/1/2, but its
  angular-DPI wording mentions accessibility overrides where S402 mentions
  the user scale factor — wording-era difference noted, both exclude user
  scaling from raw/angular.
- The panel diagonal behind H08/J08 is unobserved (no EDID read; none is
  planned — the lane reads documented API surfaces, not driver tables).
