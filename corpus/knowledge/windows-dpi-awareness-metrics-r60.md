source: S406, S407, S408, S409, S410, S411 (corpus/SOURCES.md; Microsoft Learn,
  opened 2026-10-31) plus re-used S404 for the J14 join
verified-at: 2026-10-31
recheck: on-release

# The DPI-awareness and system-metrics join on the Windows host (round 60)

**Scope.** The r58 entry recorded two named residues on the per-monitor DPI
layer: the probe caller's `PROCESS_DPI_AWARENESS` was `[UNK]` (J05), and the
awareness-branch ambiguity was named (J07) — without the caller's branch, the
documented virtualization behavior of `GetSystemMetrics` cannot be read
against a host measurement. This entry closes that gap with a read-only probe
on 2026-10-31: the caller's branch measured through the documented getter
chain (`GetThreadDpiAwarenessContext` → `GetAwarenessFromDpiAwarenessContext`),
`GetSystemMetrics(SM_CXSCREEN/SM_CYSCREEN)` read beside
`GetSystemMetricsForDpi(…, 96)`, a main-window awareness histogram, and the
foreground window's `GetDpiForWindow` with its own window awareness. The lane's
layers rule (QUALITY 15/16) holds throughout: every documentation sentence
stays a dated `[INF-docs]` claim, every host sentence cites the command that
produced it. The r58 D02 rule is restated and unchanged: raw/angular per-panel
facts never feed UI scale factors — nothing in this entry re-opens it.

**Sources.** Rows S406-S411 (opened 2026-10-31, `corpus/SOURCES.md`): the
`GetSystemMetrics` page (S406), the `GetSystemMetricsForDpi` page (S407), the
`GetThreadDpiAwarenessContext` page (S408), the
`GetAwarenessFromDpiAwarenessContext` page (S409), the `DPI_AWARENESS`
enumeration (S410), and the `GetWindowDpiAwarenessContext` page (S411). Row
S404 is re-used for J14 (the awareness-dependent `GetDpiForWindow` return
table). All tier A, `mined`, opened in full before any row was written.

## 1. Host claims (H rows, each with its re-derivation command)

| id | proposition | command (read-only) | observed 2026-10-31 |
|---|---|---|---|
| H13 | the r58 probe's launch shape — a `powershell.exe -NoProfile -NonInteractive` child — measures its calling thread as `DPI_AWARENESS_UNAWARE` (0) on this host | `.ufo/waves/round-60/receipts/dpi-awareness-probe.ps1` (P/Invoke `GetThreadDpiAwarenessContext` → `GetAwarenessFromDpiAwarenessContext`) | two runs, both rc=0, byte-identical: `thread.awareness=0` — receipts `dpi-awareness-run1.txt`, `dpi-awareness-run2.txt` |
| H14 | `GetSystemMetrics(SM_CXSCREEN/SM_CYSCREEN)` returns 1920x1080 and equals `GetSystemMetricsForDpi(SM_CXSCREEN/SM_CYSCREEN, 96)` on this host | same probe (`GetSystemMetrics(0/1)` beside `GetSystemMetricsForDpi(0/1, 96)`) | `metrics.cxscreen=1920 metrics.cyscreen=1080 metrics.cxscreen_dpi96=1920 metrics.cyscreen_dpi96=1080`, both runs byte-identical |
| H15 | the main-window census reads 6 windows with a main window, all 6 `PER_MONITOR_AWARE` (2), none unaware, system-aware or invalid (point-in-time histogram; no titles, no names, no handles collected) | same probe (`Get-Process` census where `MainWindowHandle -ne 0`, then `GetWindowDpiAwarenessContext` → awareness per handle) | `windows.with_main=6 windows.aware0=0 windows.aware1=0 windows.aware2=6 windows.awareness_invalid=0`, both runs |
| H16 | the foreground window reports `GetDpiForWindow` = 96 and its own window awareness = 2 (point-in-time foreground, never bound) | same probe (`GetForegroundWindow` → `GetDpiForWindow`, `GetWindowDpiAwarenessContext` → awareness) | `fg_window.present=True fg_window.dpi=96 fg_window.awareness=2`, both runs |

## 2. Documented claims (K rows — dated [INF-docs], never host facts)

| id | proposition (≤25-word quotes verbatim from the named row) | row / anchor | class |
|---|---|---|---|
| K21 | the awareness vocabulary is `DPI_AWARENESS_INVALID = −1`, `UNAWARE = 0`, `SYSTEM_AWARE = 1`, `PER_MONITOR_AWARE = 2`; UNAWARE is "always assumed to have a scale factor of 100% (96 DPI)" | S410 § Syntax + § Constants (UNAWARE) | [INF-docs] |
| K22 | "Note that all dimensions retrieved by GetSystemMetrics are in pixels."; SM_CXSCREEN is "The width of the screen of the primary display monitor, in pixels." | S406 § Description + § Parameters (SM_CXSCREEN) | [INF-docs] |
| K23 | GetSystemMetrics "is not DPI aware, and should not be used if the calling thread is per-monitor DPI aware"; its documented failure return is 0 | S406 § Remarks + § Return value | [INF-docs] |
| K24 | GetSystemMetricsForDpi "returns the same result as GetSystemMetrics but scales it according to an arbitrary DPI you provide if appropriate"; minimum client Windows 10 1607 | S407 § Remarks + Requirements | [INF-docs] |
| K25 | "Gets the DPI_AWARENESS_CONTEXT for the current thread."; without a prior `SetThreadDpiAwarenessContext` the value equals the process default | S408 § Description + § Remarks | [INF-docs] |
| K26 | "Retrieves the DPI_AWARENESS value from a DPI_AWARENESS_CONTEXT."; a null or invalid context decodes to `DPI_AWARENESS_INVALID` | S409 § Description + § Return value | [INF-docs] |
| K27 | "Returns the DPI_AWARENESS_CONTEXT associated with a window."; the value "is not affected by the DPI_AWARENESS of the current thread" | S411 § Description + § Remarks | [INF-docs] |

## 3. Joins (J rows — documentation read against the host, limits named)

| id | join | verdict | caveat carried |
|---|---|---|---|
| J13 | H13's UNAWARE caller (0) read against K21's unaware semantics ("assumed … 100% (96 DPI)") and K22's pixels rule, joined to H14's equality with the ForDpi-96 values | agreement — the unaware caller reads physical pixels on this host, consistent with the documented model | vacuous shape (the r58 J05 class): at effective 96 an aware and an unaware caller read the same numbers, so the metrics join alone cannot identify the branch; the branch is identified by the measured awareness value (H13), never by the metrics equality |
| J14 | H16's foreground reading (dpi 96, window awareness 2) read against S404's awareness-dependent return table (PER_MONITOR_AWARE → "The DPI of the monitor where the window is located") and the r58 entry's H06 effective-96 measurement | agreement | point-in-time foreground; the r58 probe's own caller context stays `[UNK]` as a point-in-time fact — H13 pins the branch of the launch SHAPE, not the r58 process (disclosed, not overwritten) |
| J15 | H15's histogram (6 × PER_MONITOR_AWARE) read against K27's independence remark: the per-window values are window facts, unaffected by the querying thread's UNAWARE branch | agreement | point-in-time census; the histogram's stability across the two runs is a property of this desktop's current window set, not a law |
| J16 | K23's documented 0-failure return read against the r60 tool's sanity rule: any metric ≤ 0 is CHECK FAILED, never a measurement (the failure return is indistinguishable from a zero metric) | boundary join | the tool cannot distinguish "metric is 0" from "call failed"; it refuses to interpret instead (selftest assertion `test_zero_metrics_is_check_failed`) |

## 4. The r58 residues close, limits stay named

The r58 entry's two named residues close here, scoped exactly:

- **J05's caller `[UNK]`** closes for the launch SHAPE: every probe this lane
  has run on this host (r58 `dpi-probe.ps1`, r60 `dpi-awareness-probe.ps1`,
  the r60 tool `tools/mado-win-dpi.py`) is the same launch shape, and that
  shape measures `DPI_AWARENESS_UNAWARE` (H13). The r58 probe's own process
  context remains a point-in-time `[UNK]` — same-shape measurement, disclosed
  as such in J14; the r58 entry's bytes are untouched.
- **J07's awareness-branch ambiguity** closes: the branch is now a measured
  fact (H13), and the metrics join's vacuous shape at effective 96 is named
  (J13) rather than read as an identification.

Limits that stay open, stated: the **rendered pixel** remains unobserved (the
r57/r58 entries' named limit); screen-capture scope is now an L0 question
filed this round (`mado | round-60`), routed around, never treated as
answered. The census and foreground rows are point-in-time. No Win11-labeled
model sentence was sought or claimed here — the D01 residue of the r59 entry
is untouched.

## 5. Verify (re-derivation commands, all read-only)

```
powershell.exe -NoProfile -NonInteractive -NoLogo -ExecutionPolicy Bypass -File \
  .ufo/waves/round-60/receipts/dpi-awareness-probe.ps1     # H13-H16; two runs, diff clean
python tools/mado-win-dpi.py --selftest                    # 10/10 assertions, rc 0
python tools/mado-win-dpi.py                               # MADO_WINDPI: CLEAN (awareness=unaware …)
python tools/mado-win-dpi.py --from-file \
  .ufo/waves/round-60/receipts/windpi-snapshot.json        # re-derives from committed bytes
```

Cross-check: `windpi-crosscheck.txt` — 5/5 stable fields (thread awareness,
the four metric values) agree between the independent probe child and the
tool's JSON. The window histogram and foreground values are point-in-time and
are bound by the receipts, not asserted live.
