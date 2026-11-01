#!/usr/bin/env python3
"""mado-win-dwm.py — read-only Windows DWM client-attribute observer (mado-shokunin round 62).

WHAT IT OBSERVES (all reads, no writes, no mutations; every P/Invoke is a getter):
  - composition state: DwmIsCompositionEnabled (documented always-on since
    Windows 8; a FALSE binds the querying process's manifest context, so a
    FALSE is CHECK FAILED, never a measurement);
  - the cloaked-window census: EnumWindows + DwmGetWindowAttribute(
    DWMWA_CLOAKED) per top-level window — counts and reason buckets only
    (DWM_CLOAKED_APP 0x1 / DWM_CLOAKED_SHELL 0x2 / DWM_CLOAKED_INHERITED
    0x4), never a handle, title or process name;
  - the frame-bounds join on the probe's own console window (fallback: the
    foreground window): GetWindowRect beside DwmGetWindowAttribute(
    DWMWA_EXTENDED_FRAME_BOUNDS) — the pair whose documented difference has
    two named causes (invisible resize borders; DPI virtualization of the
    Window Rect alone);
  - composition timing: DwmGetCompositionTimingInfo with the documented
    Windows 8.1+ NULL-hwnd shape, plus the documented non-NULL shape whose
    page promises E_INVALIDARG — recorded, never asserted (the pin does not
    reproduce on this host; entry finding D04).

HOW IT RUNS:
  live mode    spawns exactly one child process: the PowerShell interpreter
               named by --powershell (default `powershell.exe`), invoked with
               fixed arguments and an embedded, fixed read-only script. stdin
               is /dev/null. The script spawns no grandchild processes.
  --from-file  parses a previously captured JSON snapshot instead of spawning
               PowerShell, so a committed receipt is re-derivable from its
               committed bytes.
  --selftest   parser and static-safety assertions only; spawns nothing and
               writes nothing except ephemeral fixtures inside a private
               temporary directory it removes on exit.

WHAT IT NEVER DOES (hard boundaries):
  - collects no window titles, no process names, no window handles, no
    registry values; prints no clipboard contents, no environment values,
    no file contents (round-56 M56-17 rule carried: a channel may be
    asserted to exist, its values are never printed);
  - never echoes raw child output — child stdout is parsed as JSON and only
    whitelisted fields are re-printed; on parse failure a verdict line plus
    the raw byte length and sha256 prefix are printed, never the bytes;
  - writes no file, opens no socket, changes no window or composition
    state (no Set*/Move*/Change* verb exists in this tool; cloaking,
    attribute writes and composition changes stay operator-owned).

EXIT MAP:  0 = CLEAN (live or file snapshot parsed and sane)
           1 = CHECK FAILED (parsed, but a sanity check failed)
           2 = ERROR (spawn, parse or schema failure; --selftest failure)
OUTPUT: one `MADO_WINDWM:` verdict line, then one JSON object line.

KNOWN LIMITS (stated, not hidden):
  - every observation is point-in-time; the census counters (top_level,
    visible, cloaked, the rect pair) churn with desktop activity — the
    verdict line is built from structure, not from those numbers, and a
    from-file re-derivation is the determinism receipt;
  - the timing getter's failure mode on this host is itself the entry's
    finding D04: both documented call shapes fail with an HRESULT outside
    the page's S_OK/E_INVALIDARG vocabulary; the tool reports
    `timing=unavailable(hr=0x…)` and never guesses a cause;
  - a timing success with a zero numerator/denominator is CHECK FAILED,
    never a measurement; a per-window attribute failure (attr_failed > 0)
    is CHECK FAILED, never an imputed value;
  - which monitor a NULL-hwnd timing success would describe is not named
    by the page on Windows 8.1+; on this single-display host the join to
    the display entry would be unambiguous (never exercised here — the
    call fails);
  - the tool says nothing about rendered output; it never toggles anything.
"""

from __future__ import annotations

import argparse
import contextlib
import hashlib
import io
import json
import subprocess
import sys
import unittest
from typing import Any

TOOL = "mado-win-dwm"
VERSION = "r62-v1"

# The fixed read-only script handed to PowerShell. It is embedded verbatim so
# the tool's own bytes pin exactly what ran. Counts, rects and HRESULTs are
# desktop facts; no titles, no process names, no handles, no registry reads.
# The static selftest pins that.
PS_SCRIPT = r"""
$ErrorActionPreference = 'Stop'
Add-Type -TypeDefinition @"
using System;
using System.Collections.Generic;
using System.Runtime.InteropServices;
namespace MadoDwm {
  [StructLayout(LayoutKind.Sequential)]
  public struct RECT { public int Left; public int Top; public int Right; public int Bottom; }
  [StructLayout(LayoutKind.Sequential)]
  public struct UNSIGNED_RATIO { public uint uiNumerator; public uint uiDenominator; }
  [StructLayout(LayoutKind.Sequential)]
  public struct DWM_TIMING_INFO {
    public uint cbSize;
    public UNSIGNED_RATIO rateRefresh;
    public ulong qpcRefreshPeriod;
    public UNSIGNED_RATIO rateCompose;
    public ulong qpcVBlank;
    public ulong cRefresh;
    public uint cDXRefresh;
    public ulong qpcCompose;
    public ulong cFrame;
    public uint cDXPresent;
    public ulong cRefreshFrame;
    public ulong cFrameSubmitted;
    public uint cDXPresentSubmitted;
    public ulong cFrameConfirmed;
    public uint cDXPresentConfirmed;
    public ulong cRefreshConfirmed;
    public uint cDXRefreshConfirmed;
    public ulong cFramesLate;
    public uint cFramesOutstanding;
    public ulong cFrameDisplayed;
    public ulong qpcFrameDisplayed;
    public ulong cRefreshFrameDisplayed;
    public ulong cFrameComplete;
    public ulong qpcFrameComplete;
    public ulong cFramePending;
    public ulong qpcFramePending;
    public ulong cFramesDisplayed;
    public ulong cFramesComplete;
    public ulong cFramesPending;
    public ulong cFramesAvailable;
    public ulong cFramesDropped;
    public ulong cFramesMissed;
    public ulong cRefreshNextDisplayed;
    public ulong cRefreshNextPresented;
    public ulong cRefreshesDisplayed;
    public ulong cRefreshesPresented;
    public ulong cRefreshStarted;
    public ulong cPixelsReceived;
    public ulong cPixelsDrawn;
    public ulong cBuffersEmpty;
  }
  public static class Native {
    public delegate bool EnumWindowsProc(IntPtr hWnd, IntPtr lParam);
    [DllImport("dwmapi.dll")] public static extern int DwmIsCompositionEnabled(out bool enabled);
    [DllImport("dwmapi.dll")] public static extern int DwmGetWindowAttribute(IntPtr hwnd, uint attr, out uint value, uint cb);
    [DllImport("dwmapi.dll")] public static extern int DwmGetWindowAttribute(IntPtr hwnd, uint attr, out RECT rect, uint cb);
    [DllImport("dwmapi.dll")] public static extern int DwmGetCompositionTimingInfo(IntPtr hwnd, ref DWM_TIMING_INFO info);
    [DllImport("user32.dll")] public static extern bool EnumWindows(EnumWindowsProc cb, IntPtr lParam);
    [DllImport("user32.dll")] public static extern bool IsWindowVisible(IntPtr hWnd);
    [DllImport("user32.dll")] public static extern bool IsWindow(IntPtr hWnd);
    [DllImport("user32.dll")] public static extern bool GetWindowRect(IntPtr hWnd, out RECT rect);
    [DllImport("kernel32.dll")] public static extern IntPtr GetConsoleWindow();
    [DllImport("user32.dll")] public static extern IntPtr GetForegroundWindow();
    public static object Snapshot() {
      bool composed = false;
      int hrComposed = DwmIsCompositionEnabled(out composed);
      int top = 0, visible = 0, cloaked = 0, cApp = 0, cShell = 0, cInherited = 0, attrFailed = 0;
      EnumWindowsProc cb = (IntPtr h, IntPtr lp) => {
        top++;
        if (IsWindowVisible(h)) { visible++; }
        uint cloak = 0;
        int hr = DwmGetWindowAttribute(h, 14, out cloak, 4);
        if (hr != 0) { attrFailed++; }
        else if (cloak != 0) {
          cloaked++;
          if (cloak == 1) { cApp++; }
          else if (cloak == 2) { cShell++; }
          else if (cloak == 4) { cInherited++; }
        }
        return true;
      };
      EnumWindows(cb, IntPtr.Zero);
      IntPtr own = GetConsoleWindow();
      string src = "console";
      if (own == IntPtr.Zero || !IsWindow(own)) { own = GetForegroundWindow(); src = "foreground"; }
      if (own == IntPtr.Zero || !IsWindow(own)) { src = "none"; }
      object ownObj = new Dictionary<string, object> { { "source", "none" } };
      if (src != "none") {
        RECT wr;
        bool rectOk = GetWindowRect(own, out wr);
        RECT fr;
        int hrFrame = DwmGetWindowAttribute(own, 9, out fr, (uint)Marshal.SizeOf(typeof(RECT)));
        ownObj = new Dictionary<string, object> {
          { "source", src },
          { "rect_ok", rectOk },
          { "rect", new int[] { wr.Left, wr.Top, wr.Right, wr.Bottom } },
          { "frame_hr", hrFrame },
          { "frame_ok", hrFrame == 0 },
          { "frame", hrFrame == 0 ? new int[] { fr.Left, fr.Top, fr.Right, fr.Bottom } : new int[] { 0, 0, 0, 0 } }
        };
      }
      var ti = new DWM_TIMING_INFO();
      ti.cbSize = (uint)Marshal.SizeOf(typeof(DWM_TIMING_INFO));
      int cbSizeVal = (int)ti.cbSize;
      int hrTiming = DwmGetCompositionTimingInfo(IntPtr.Zero, ref ti);
      // documented shape check: a NON-NULL hwnd must return E_INVALIDARG on
      // Windows 8.1+ (the timing function's own page: "If this parameter is
      // not set to NULL" the call "returns E_INVALIDARG"). E_INVALIDARG =
      // 0x80070057. Getter only — no state is touched.
      int hrTimingNonNull = -1;
      if (src != "none") {
        var tj = new DWM_TIMING_INFO();
        tj.cbSize = (uint)Marshal.SizeOf(typeof(DWM_TIMING_INFO));
        hrTimingNonNull = DwmGetCompositionTimingInfo(own, ref tj);
      }
      object timingObj;
      if (hrTiming == 0) {
        timingObj = new Dictionary<string, object> {
          { "ok", true }, { "hr", hrTiming }, { "cb_size", cbSizeVal },
          { "refresh_num", ti.rateRefresh.uiNumerator }, { "refresh_den", ti.rateRefresh.uiDenominator },
          { "compose_num", ti.rateCompose.uiNumerator }, { "compose_den", ti.rateCompose.uiDenominator },
          { "c_refresh", (double)ti.cRefresh }, { "qpc_refresh_period", (double)ti.qpcRefreshPeriod }
        };
      } else {
        timingObj = new Dictionary<string, object> {
          { "ok", false }, { "hr", hrTiming }, { "cb_size", cbSizeVal },
          { "nonnull_hr", hrTimingNonNull }
        };
      }
      var doc = new Dictionary<string, object>();
      doc["composition_enabled"] = composed;
      doc["composition_hr"] = hrComposed;
      doc["windows"] = new Dictionary<string, object> {
        { "top_level", top }, { "visible", visible }, { "cloaked", cloaked },
        { "cloak_app", cApp }, { "cloak_shell", cShell }, { "cloak_inherited", cInherited },
        { "attr_failed", attrFailed }
      };
      doc["own_window"] = ownObj;
      doc["timing"] = timingObj;
      return doc;
    }
  }
}
"@
[MadoDwm.Native]::Snapshot() | ConvertTo-Json -Depth 6 -Compress
"""

# Fields the tool will re-print (whitelist). Anything else in the child JSON
# is dropped silently.
ALLOWED_TOP_KEYS = {"composition_enabled", "composition_hr", "windows", "own_window", "timing"}
ALLOWED_WINDOWS_KEYS = {
    "top_level", "visible", "cloaked",
    "cloak_app", "cloak_shell", "cloak_inherited", "attr_failed",
}
ALLOWED_OWN_KEYS = {"source", "rect_ok", "rect", "frame_hr", "frame_ok", "frame"}
ALLOWED_TIMING_KEYS = {
    "ok", "hr", "cb_size",
    "refresh_num", "refresh_den", "compose_num", "compose_den",
    "c_refresh", "qpc_refresh_period", "nonnull_hr",
}

REASON_NAMES = (("app", "cloak_app", 1), ("shell", "cloak_shell", 2), ("inherited", "cloak_inherited", 4))


def _err(stage: str, detail: str) -> int:
    print(f"MADO_WINDWM: ERROR (stage={stage} detail={_brief(detail)})")
    return 2


def _brief(text: str, limit: int = 120) -> str:
    """One line, bounded, of a message that never carries raw child output."""
    one = " ".join(str(text).split())
    if len(one) > limit:
        one = one[: limit - 3] + "..."
    # belt and braces: no matter the source, never print quote-backed blobs
    return one.replace("`", "'")


def _is_int(value: Any) -> bool:
    """True for real ints (bool is excluded — bool is an int subclass)."""
    return isinstance(value, int) and not isinstance(value, bool)


def _is_rect(value: Any) -> bool:
    return (isinstance(value, list) and len(value) == 4
            and all(_is_int(v) for v in value))


def _rect_extent(rect: list[int]) -> tuple[int, int]:
    return rect[2] - rect[0], rect[3] - rect[1]


def validate(doc: Any) -> tuple[dict[str, Any], list[str]]:
    """Schema-check a parsed snapshot. Returns (clean_doc, problems)."""
    problems: list[str] = []
    if not isinstance(doc, dict):
        return {}, ["top-level JSON is not an object"]
    unknown = sorted(set(doc) - ALLOWED_TOP_KEYS)
    if unknown:
        problems.append(f"unknown top keys dropped: {','.join(unknown)}")
    clean: dict[str, Any] = {}
    for key in ("composition_enabled", "composition_hr"):
        if key in doc:
            clean[key] = doc[key]
    raw_windows = doc.get("windows")
    if isinstance(raw_windows, dict):
        unknown_w = sorted(set(raw_windows) - ALLOWED_WINDOWS_KEYS)
        if unknown_w:
            problems.append(f"windows unknown keys dropped: {','.join(unknown_w)}")
        clean["windows"] = {k: raw_windows[k] for k in ALLOWED_WINDOWS_KEYS if k in raw_windows}
    raw_own = doc.get("own_window")
    if isinstance(raw_own, dict):
        unknown_o = sorted(set(raw_own) - ALLOWED_OWN_KEYS)
        if unknown_o:
            problems.append(f"own_window unknown keys dropped: {','.join(unknown_o)}")
        clean["own_window"] = {k: raw_own[k] for k in ALLOWED_OWN_KEYS if k in raw_own}
    raw_timing = doc.get("timing")
    if isinstance(raw_timing, dict):
        unknown_t = sorted(set(raw_timing) - ALLOWED_TIMING_KEYS)
        if unknown_t:
            problems.append(f"timing unknown keys dropped: {','.join(unknown_t)}")
        clean["timing"] = {k: raw_timing[k] for k in ALLOWED_TIMING_KEYS if k in raw_timing}
    return clean, problems


def sanity(clean: dict[str, Any]) -> list[str]:
    """Post-schema sanity checks (CHECK FAILED class, not ERROR)."""
    problems: list[str] = []
    enabled = clean.get("composition_enabled")
    if enabled is not True:
        # documented always-on since Windows 8; a FALSE binds the querying
        # process's manifest context (S400) — never a host fact
        problems.append(
            "composition_enabled is not TRUE (the documented always-on state; "
            "a FALSE binds the querying process's manifest context, not the host)")
    hr_composed = clean.get("composition_hr")
    if hr_composed != 0:
        problems.append(f"composition_hr is not 0 (got {hr_composed!r})")
    windows = clean.get("windows")
    if not isinstance(windows, dict):
        problems.append("missing/invalid object: windows")
        return problems
    top = windows.get("top_level")
    if not _is_int(top) or top < 1:
        problems.append("windows.top_level is not a positive integer")
        return problems
    visible = windows.get("visible")
    if not _is_int(visible) or visible < 0 or visible > top:
        problems.append("windows.visible is not an integer in [0, top_level]")
    cloaked = windows.get("cloaked")
    if not _is_int(cloaked) or cloaked < 0 or cloaked > top:
        problems.append("windows.cloaked is not an integer in [0, top_level]")
        return problems
    attr_failed = windows.get("attr_failed")
    if attr_failed != 0:
        # a per-window getter failure is not a measurement (the lane's
        # documented-failure rule) — never imputed as "not cloaked"
        problems.append(
            f"windows.attr_failed is not 0 (got {attr_failed!r}; a failed "
            "DWMWA_CLOAKED read is CHECK FAILED, never imputed)")
    reason_sum = 0
    for _short, key, _value in REASON_NAMES:
        bucket = windows.get(key)
        if not _is_int(bucket) or bucket < 0:
            problems.append(f"windows.{key} is not a non-negative integer")
            return problems
        reason_sum += bucket
    if reason_sum != cloaked:
        problems.append(
            f"reason buckets sum to {reason_sum}, not windows.cloaked={cloaked} "
            "(DWMWA_CLOAKED's reason is exactly one of the three values)")
    own = clean.get("own_window")
    if not isinstance(own, dict):
        problems.append("missing/invalid object: own_window")
        return problems
    source = own.get("source")
    if source not in ("console", "foreground", "none"):
        problems.append(f"own_window.source is not console/foreground/none (got {source!r})")
        return problems
    if source == "none":
        return problems
    rect = own.get("rect")
    rect_ok = own.get("rect_ok")
    if rect_ok is not True or not _is_rect(rect) or max(_rect_extent(rect)) <= 0:
        # GetWindowRect's documented failure return is zero: never a measurement
        problems.append(
            "own_window.rect did not report (GetWindowRect's documented "
            "failure return is zero, never a measurement)")
    frame = own.get("frame")
    frame_ok = own.get("frame_ok")
    if frame_ok is not True or not _is_rect(frame) or max(_rect_extent(frame)) <= 0:
        problems.append(
            "own_window.frame did not report (a failed DWMWA_EXTENDED_FRAME_BOUNDS "
            "read is CHECK FAILED, never a measurement)")
    timing = clean.get("timing")
    if not isinstance(timing, dict):
        problems.append("missing/invalid object: timing")
        return problems
    if timing.get("ok") is True:
        for key in ("refresh_num", "refresh_den", "compose_den"):
            value = timing.get(key)
            if not _is_int(value) or value <= 0:
                problems.append(
                    f"timing.{key} is not a positive integer (a zero rate is "
                    "the not-a-measurement shape, never a measurement)")
    else:
        hr = timing.get("hr")
        if hr == 0:
            problems.append("timing.hr is 0 while timing.ok is not true (contradiction)")
    return problems


def _timing_desc(timing: dict[str, Any]) -> str:
    if timing.get("ok") is True:
        num = timing.get("refresh_num")
        den = timing.get("refresh_den")
        return f"{num}/{den}Hz"
    hr = timing.get("hr")
    if isinstance(hr, int) and not isinstance(hr, bool):
        return f"unavailable(hr=0x{hr & 0xFFFFFFFF:08x})"
    return "unavailable(hr=unknown)"


def _reason_pattern(windows: dict[str, Any]) -> str:
    names = [short for short, _key, _value in REASON_NAMES if windows.get(_key)]
    return "+".join(names) if names else "none"


def verdict_line(clean: dict[str, Any]) -> str:
    """Structure-only verdict: no census numbers (they churn with desktop
    activity — the JSON line carries the numbers, the receipts name their
    churn class)."""
    windows = clean.get("windows") or {}
    return (
        f"MADO_WINDWM: CLEAN (composition=on "
        f"reasons={_reason_pattern(windows)} "
        f"timing={_timing_desc(clean.get('timing') or {})})"
    )


def print_json(clean: dict[str, Any]) -> None:
    print(json.dumps(clean, sort_keys=True, ensure_ascii=True))


def run_live(interpreter: str) -> int:
    argv = [interpreter, "-NoProfile", "-NonInteractive", "-NoLogo", "-Command", PS_SCRIPT]
    try:
        proc = subprocess.run(
            argv,
            stdin=subprocess.DEVNULL,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=120,
            check=False,
        )
    except FileNotFoundError:
        return _err("spawn", f"interpreter not found: {interpreter}")
    except subprocess.TimeoutExpired:
        return _err("spawn", "timed out after 120s")
    if proc.returncode != 0:
        return _err(
            "child-exit",
            f"rc={proc.returncode} stderr_len={len(proc.stderr)} (stderr bytes never printed)",
        )
    raw = proc.stdout
    try:
        doc = json.loads(raw.decode("utf-8", errors="strict"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        digest = hashlib.sha256(raw).hexdigest()[:16]
        return _err("parse", f"{type(exc).__name__} raw_len={len(raw)} raw_sha256_16={digest} (bytes never printed)")
    return _emit(doc, source=None)


def run_file(path: str) -> int:
    try:
        with open(path, "rb") as handle:
            raw = handle.read(4 * 1024 * 1024 + 1)
    except OSError as exc:
        return _err("open", str(exc))
    if len(raw) > 4 * 1024 * 1024:
        return _err("open", "snapshot larger than 4 MiB cap")
    try:
        doc = json.loads(raw.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        return _err("parse", f"{type(exc).__name__} in snapshot {path}")
    return _emit(doc, source=path)


def _emit(doc: Any, source: str | None) -> int:
    clean, problems = validate(doc)
    if any(p.startswith("missing/invalid") for p in problems):
        return _err("schema", "; ".join(p for p in problems if p.startswith("missing/invalid")))
    bad = sanity(clean)
    if bad:
        where = f"source=file {source}; " if source else ""
        print(f"MADO_WINDWM: CHECK FAILED ({where}{'; '.join(bad)})")
        print_json(clean)
        return 1
    if source:
        windows = clean.get("windows") or {}
        print(
            f"MADO_WINDWM: CLEAN (source=file {source}) "
            f"reasons={_reason_pattern(windows)} timing={_timing_desc(clean.get('timing') or {})}"
        )
    else:
        print(verdict_line(clean))
    print_json(clean)
    return 0


def selftest() -> int:
    import os
    import tempfile

    def canned(windows_json: str, own_json: str, timing_json: str) -> str:
        return ('{"composition_enabled": true, "composition_hr": 0, "windows": '
                + windows_json + ', "own_window": ' + own_json
                + ', "timing": ' + timing_json + '}')

    LIVE_WINDOWS = ('{"top_level": 170, "visible": 13, "cloaked": 14, "cloak_app": 7, '
                    '"cloak_shell": 7, "cloak_inherited": 0, "attr_failed": 0}')
    LIVE_OWN = ('{"source": "console", "rect_ok": true, "rect": [104, 104, 1097, 623], '
                '"frame_hr": 0, "frame_ok": true, "frame": [111, 104, 1090, 616]}')
    LIVE_TIMING = '{"ok": false, "hr": -2003304304, "cb_size": 320, "nonnull_hr": -2003304304}'
    LIVE_OK = canned(LIVE_WINDOWS, LIVE_OWN, LIVE_TIMING)

    class Tests(unittest.TestCase):
        def test_parses_canned_live_document(self):
            clean, problems = validate(json.loads(LIVE_OK))
            self.assertEqual(problems, [])
            self.assertEqual(sanity(clean), [])
            line = verdict_line(clean)
            self.assertIn("composition=on", line)
            self.assertIn("reasons=app+shell", line)
            self.assertIn("timing=unavailable(hr=0x88980090)", line)
            self.assertNotIn("170", line)  # census numbers never enter the verdict

        def test_unknown_keys_dropped_whitelist(self):
            doc = json.loads(LIVE_OK)
            doc["own_window"]["title"] = "leaked-secret-9d2b"
            doc["timing"]["process_name"] = "leaked-process-4f8a"
            clean, problems = validate(doc)
            self.assertNotIn("title", clean["own_window"])
            self.assertNotIn("process_name", clean["timing"])
            self.assertTrue(any("unknown keys dropped: title" in p for p in problems))
            self.assertTrue(any("unknown keys dropped: process_name" in p for p in problems))
            self.assertEqual(sanity(clean), [])
            flat = verdict_line(clean) + json.dumps(clean, sort_keys=True, ensure_ascii=True)
            self.assertNotIn("leaked-secret-9d2b", flat)
            self.assertNotIn("leaked-process-4f8a", flat)

        def test_reason_sum_mismatch_is_check_failed(self):
            bad_windows = json.loads(LIVE_WINDOWS)
            bad_windows["cloak_app"] = 2
            bad_windows["cloak_shell"] = 2
            doc = json.loads(canned(json.dumps(bad_windows), LIVE_OWN, LIVE_TIMING))
            clean, _ = validate(doc)
            bad = sanity(clean)
            self.assertTrue(any("reason buckets sum to 4" in p for p in bad), bad)

        def test_attr_failed_is_check_failed_never_imputed(self):
            bad_windows = json.loads(LIVE_WINDOWS)
            bad_windows["attr_failed"] = 3
            doc = json.loads(canned(json.dumps(bad_windows), LIVE_OWN, LIVE_TIMING))
            clean, _ = validate(doc)
            bad = sanity(clean)
            self.assertTrue(any("attr_failed is not 0" in p for p in bad), bad)
            self.assertTrue(any("never imputed" in p for p in bad), bad)

        def test_composition_false_is_check_failed_not_a_host_fact(self):
            doc = json.loads(LIVE_OK)
            doc["composition_enabled"] = False
            clean, _ = validate(doc)
            bad = sanity(clean)
            self.assertTrue(any("composition_enabled is not TRUE" in p for p in bad), bad)
            self.assertTrue(any("manifest context" in p for p in bad), bad)

        def test_zero_refresh_rate_is_check_failed(self):
            ok_timing = ('{"ok": true, "hr": 0, "cb_size": 320, "refresh_num": 0, '
                         '"refresh_den": 1000, "compose_num": 60, "compose_den": 1, '
                         '"c_refresh": 1.0, "qpc_refresh_period": 1.0}')
            doc = json.loads(canned(LIVE_WINDOWS, LIVE_OWN, ok_timing))
            clean, _ = validate(doc)
            bad = sanity(clean)
            self.assertTrue(
                any("timing.refresh_num is not a positive integer" in p for p in bad), bad)
            self.assertTrue(any("never a measurement" in p for p in bad), bad)

        def test_rect_failure_is_check_failed(self):
            bad_own = json.loads(LIVE_OWN)
            bad_own["rect_ok"] = False
            doc = json.loads(canned(LIVE_WINDOWS, json.dumps(bad_own), LIVE_TIMING))
            clean, _ = validate(doc)
            bad = sanity(clean)
            self.assertTrue(any("own_window.rect did not report" in p for p in bad), bad)

        def test_from_file_roundtrip(self):
            tmpdir = tempfile.mkdtemp(prefix="mado-windwm-selftest-")
            try:
                path = os.path.join(tmpdir, "snapshot.json")
                with open(path, "w", encoding="utf-8") as handle:
                    handle.write(LIVE_OK)
                buf = io.StringIO()
                with contextlib.redirect_stdout(buf):
                    rc = run_file(path)
                out = buf.getvalue()
                self.assertEqual(rc, 0, out)
                self.assertIn("source=file", out)
                self.assertIn("reasons=app+shell", out)
            finally:
                for name in os.listdir(tmpdir):
                    os.unlink(os.path.join(tmpdir, name))
                os.rmdir(tmpdir)

        def test_malformed_snapshot_is_error_and_bytes_never_echoed(self):
            payload = b'{"timing": NOT_JSON @@@'
            tmpdir = tempfile.mkdtemp(prefix="mado-windwm-selftest-")
            try:
                path = os.path.join(tmpdir, "broken.json")
                with open(path, "wb") as handle:
                    handle.write(payload)
                buf = io.StringIO()
                with contextlib.redirect_stdout(buf):
                    rc = run_file(path)
                out = buf.getvalue()
                self.assertEqual(rc, 2, out)
                self.assertTrue(out.startswith("MADO_WINDWM: ERROR (stage=parse"), out[:80])
                self.assertNotIn("NOT_JSON", out)
            finally:
                for name in os.listdir(tmpdir):
                    os.unlink(os.path.join(tmpdir, name))
                os.rmdir(tmpdir)

        def test_fixed_script_only_getters_never_titles_handles_or_changes(self):
            low = PS_SCRIPT.lower()
            # no write/mutation verb exists (the DwmSetWindowAttribute family,
            # window moves, and state changes stay operator-owned)
            self.assertNotIn("dwmsetwindowattribute", low)
            self.assertNotIn("setwindowpos", low)
            self.assertNotIn("setwindowlong", low)
            self.assertNotIn("movewindow", low)
            self.assertNotIn("setprocessdpiawareness", low)
            self.assertNotIn("changedisplaysettings", low)
            # the WMI/CIM cmdlet ban is pinned to the cmdlet names, not a
            # bare substring: "wmi" occurs inside the legitimate
            # DwmIsCompositionEnabled P/Invoke (the M61-1 collision shape,
            # found by this tool's own first red run)
            self.assertNotIn("get-wmiobject", low)
            self.assertNotIn("get-ciminstance", low)
            self.assertNotIn("clipboard", low)
            self.assertNotIn("windowtitle", low)
            self.assertNotIn("mainwindowhandle", low)
            self.assertNotIn("get-childitem env:", low)
            # no registry API reads
            self.assertNotIn("microsoft.win32.registry", low)
            self.assertNotIn("get-itemproperty", low)
            # the documented query families appear at exactly their declared
            # sites: 2 imports (uint and RECT overloads) + 2 call sites for
            # DwmGetWindowAttribute (cloak per window + frame for own); 1
            # import + 2 call sites for the timing query (NULL + documented
            # non-NULL shape); 1 import + 1 call each for the rest
            self.assertEqual(low.count("dwmgetwindowattribute"), 4, low)
            self.assertEqual(low.count("dwmgetcompositiontiminginfo"), 3, low)
            self.assertEqual(low.count("dwmiscompositionenabled"), 2, low)
            # enumwindows sites (5): the DllImport function name, the
            # EnumWindowsProc parameter type inside that same import
            # signature, the delegate type declaration, the callback
            # variable's type, and the one call
            self.assertEqual(low.count("enumwindows"), 5, low)
            self.assertEqual(low.count("iswindowvisible"), 2, low)
            # iswindow( sites (3): the import signature and the two guards;
            # the bare-substring count is 5 because iswindowvisible's two
            # sites carry "iswindow" as a prefix — the paren form counts
            # the IsWindow getter only
            self.assertEqual(low.count("iswindow("), 3, low)
            self.assertEqual(low.count("getwindowrect"), 2, low)
            self.assertEqual(low.count("getconsolewindow"), 2, low)
            self.assertEqual(low.count("getforegroundwindow"), 2, low)
            # the documented attribute ids at their sites: DWMWA_CLOAKED=14,
            # DWMWA_EXTENDED_FRAME_BOUNDS=9 (enum series anchored by the
            # page's NCRENDERING_ENABLED=1 note; entry K39)
            self.assertIn(", 14, out cloak, 4)", low)
            self.assertIn(", 9, out fr,", low)
            # the callback always returns true (enumeration is never aborted)
            self.assertIn("return true", low)
            self.assertIn("convertto-json", low)

        def test_error_line_is_bounded_and_single_line(self):
            buf = io.StringIO()
            with contextlib.redirect_stdout(buf):
                rc = _err("spawn", "interpreter not found: nope")
            out = buf.getvalue()
            self.assertEqual(rc, 2)
            self.assertEqual(len(out.strip().splitlines()), 1)
            self.assertLessEqual(len(out), 200)
            self.assertTrue(out.startswith("MADO_WINDWM: ERROR (stage=spawn"))

    suite = unittest.defaultTestLoader.loadTestsFromTestCase(Tests)
    runner = unittest.TextTestRunner(stream=sys.stderr, verbosity=0)
    result = runner.run(suite)
    total = result.testsRun
    failures = len(result.failures) + len(result.errors)
    print(f"MADO_WINDWM_SELFTEST: {total - failures}/{total} assertions passed (tool sha256 pinned in the ledger, not in-run)")
    return 0 if failures == 0 else 2


def main() -> int:
    parser = argparse.ArgumentParser(prog=TOOL, description="read-only Windows DWM client-attribute observer")
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--from-file", metavar="SNAPSHOT", help="re-derive the verdict from a captured JSON snapshot")
    group.add_argument("--selftest", action="store_true", help="run parser and static-safety assertions only")
    parser.add_argument("--powershell", default="powershell.exe", help="PowerShell interpreter to spawn in live mode")
    parser.add_argument("--version", action="version", version=f"{TOOL} {VERSION}")
    args = parser.parse_args()
    if args.selftest:
        return selftest()
    if args.from_file:
        return run_file(args.from_file)
    return run_live(args.powershell)


if __name__ == "__main__":
    raise SystemExit(main())
