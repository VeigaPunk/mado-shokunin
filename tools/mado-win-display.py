#!/usr/bin/env python3
"""mado-win-display.py — read-only Windows display-topology observer (mado-shokunin round 61).

WHAT IT OBSERVES (all reads, no writes, no mutations; every P/Invoke is a getter):
  - native monitor enumeration: EnumDisplayMonitors(NULL, NULL, cb, 0) with
    GetMonitorInfoW per handle into a MONITORINFOEXW — device name (szDevice),
    the display monitor rectangle (rcMonitor), the work-area rectangle
    (rcWork) and the MONITORINFOF_PRIMARY flag;
  - the display-mode layer per enumerated device: EnumDisplaySettingsW in the
    three documented iModeNum shapes — ENUM_CURRENT_SETTINGS (-1),
    ENUM_REGISTRY_SETTINGS (-2), and the graphics-mode index series 0..N
    (bounded at 256, stopping at the documented zero return).

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
  - collects no window titles, no process names, no handles, no registry
    values, no EDID/driver tables; prints no clipboard contents, no
    environment values, no file contents (round-56 M56-17 rule carried: a
    channel may be asserted to exist, its values are never printed);
  - never echoes raw child output — child stdout is parsed as JSON and only
    whitelisted fields are re-printed; on parse failure a verdict line plus
    the raw byte length and sha256 prefix are printed, never the bytes;
  - writes no file, opens no socket, changes no mode (no Set*/Change* verb
    exists in this tool; display-mode changes stay operator-owned).

EXIT MAP:  0 = CLEAN (live or file snapshot parsed and sane)
           1 = CHECK FAILED (parsed, but a sanity check failed)
           2 = ERROR (spawn, parse or schema failure; --selftest failure)
OUTPUT: one `MADO_WINDISPLAY:` verdict line, then one JSON object line.

KNOWN LIMITS (stated, not hidden):
  - topology and mode facts are point-in-time: they are stable while no
    display change occurs, and the crosscheck binds only stable fields;
  - the work-area subtraction's cause (which appbar occupies the band the
    monitor rectangle loses) is NOT observed — the tool reads the work-area
    rectangle, never the taskbar itself (Shell surfaces stay outside);
  - a mirroring pseudo-monitor would change the native count relative to the
    managed count (the pages say pseudo-monitors are enumerated); the
    count agreement on a single-display host is a named-limit join;
  - EnumDisplaySettings's documented failure return is 0: a current mode
    that fails to report, or a zero frequency/dimension in a reported mode,
    is CHECK FAILED, never a measurement;
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

TOOL = "mado-win-display"
VERSION = "r61-v1"

# The fixed read-only script handed to PowerShell. It is embedded verbatim so
# the tool's own bytes pin exactly what ran. Device names are desktop facts
# (the r57 observer already printed them); no titles, no process names, no
# handles, no registry reads. The static selftest pins that.
PS_SCRIPT = r"""
$ErrorActionPreference = 'Stop'
Add-Type -TypeDefinition @"
using System;
using System.Collections.Generic;
using System.Runtime.InteropServices;
namespace MadoDisplay {
  [StructLayout(LayoutKind.Sequential)]
  public struct RECT { public int Left; public int Top; public int Right; public int Bottom; }
  [StructLayout(LayoutKind.Sequential, CharSet = CharSet.Unicode)]
  public struct MONITORINFOEXW {
    public uint cbSize;
    public RECT rcMonitor;
    public RECT rcWork;
    public uint dwFlags;
    [MarshalAs(UnmanagedType.ByValTStr, SizeConst = 32)] public string szDevice;
  }
  [StructLayout(LayoutKind.Sequential, CharSet = CharSet.Unicode)]
  public struct DEVMODEW {
    [MarshalAs(UnmanagedType.ByValTStr, SizeConst = 32)] public string dmDeviceName;
    public ushort dmSpecVersion; public ushort dmDriverVersion; public ushort dmSize; public ushort dmDriverExtra;
    public uint dmFields;
    public int dmPositionX; public int dmPositionY; public uint dmDisplayOrientation; public uint dmDisplayFixedOutput;
    public short dmColor; public short dmDuplex; public short dmYResolution; public short dmTTOption; public short dmCollate;
    [MarshalAs(UnmanagedType.ByValTStr, SizeConst = 32)] public string dmFormName;
    public ushort dmLogPixels; public uint dmBitsPerPel; public uint dmPelsWidth; public uint dmPelsHeight;
    public uint dmDisplayFlags; public uint dmDisplayFrequency;
    public uint dmICMMethod; public uint dmICMIntent; public uint dmMediaType; public uint dmDitherType;
    public uint dmReserved1; public uint dmReserved2; public uint dmPanningWidth; public uint dmPanningHeight;
  }
  public static class Native {
    public delegate bool MonitorEnumProc(IntPtr hMonitor, IntPtr hdcMonitor, ref RECT rect, IntPtr data);
    [DllImport("user32.dll")] public static extern bool EnumDisplayMonitors(IntPtr hdc, IntPtr clip, MonitorEnumProc cb, IntPtr data);
    [DllImport("user32.dll", CharSet = CharSet.Unicode)] public static extern bool GetMonitorInfoW(IntPtr hMonitor, ref MONITORINFOEXW info);
    [DllImport("user32.dll", CharSet = CharSet.Unicode)] public static extern bool EnumDisplaySettingsW(string deviceName, int modeNum, ref DEVMODEW devMode);
    public static DEVMODEW Fresh() {
      DEVMODEW dm = new DEVMODEW();
      dm.dmSize = (ushort)Marshal.SizeOf(typeof(DEVMODEW));
      dm.dmDriverExtra = 0;
      return dm;
    }
    public static object Snapshot() {
      var monitors = new List<object>();
      MonitorEnumProc cb = (IntPtr hMon, IntPtr hdc, ref RECT rect, IntPtr data) => {
        var mi = new MONITORINFOEXW();
        mi.cbSize = (uint)Marshal.SizeOf(typeof(MONITORINFOEXW));
        if (!GetMonitorInfoW(hMon, ref mi)) {
          monitors.Add(new Dictionary<string, object> { { "getmonitorinfo_failed", true } });
          return true;
        }
        string device = mi.szDevice;
        var mc = new Dictionary<string, object>();
        DEVMODEW cur = Fresh();
        mc["ok"] = EnumDisplaySettingsW(device, -1, ref cur);
        if ((bool)mc["ok"]) {
          mc["w"] = cur.dmPelsWidth; mc["h"] = cur.dmPelsHeight;
          mc["freq"] = cur.dmDisplayFrequency; mc["bpp"] = cur.dmBitsPerPel;
          mc["pos"] = new int[] { cur.dmPositionX, cur.dmPositionY };
        }
        DEVMODEW reg = Fresh();
        bool regOk = EnumDisplaySettingsW(device, -2, ref reg);
        object regObj;
        if (regOk) {
          regObj = new Dictionary<string, object> {
            { "ok", true }, { "w", reg.dmPelsWidth }, { "h", reg.dmPelsHeight },
            { "freq", reg.dmDisplayFrequency }, { "bpp", reg.dmBitsPerPel } };
        } else {
          regObj = new Dictionary<string, object> { { "ok", false } };
        }
        int count = 0;
        for (int i = 0; i < 256; i++) {
          DEVMODEW idx = Fresh();
          if (!EnumDisplaySettingsW(device, i, ref idx)) { break; }
          count++;
        }
        var m = new Dictionary<string, object>();
        m["device"] = device;
        m["primary"] = (mi.dwFlags & 1u) != 0u;
        m["monitor"] = new int[] { mi.rcMonitor.Left, mi.rcMonitor.Top, mi.rcMonitor.Right, mi.rcMonitor.Bottom };
        m["work"] = new int[] { mi.rcWork.Left, mi.rcWork.Top, mi.rcWork.Right, mi.rcWork.Bottom };
        m["mode_current"] = mc;
        m["mode_registry"] = regObj;
        m["mode_list_count"] = count;
        monitors.Add(m);
        return true;
      };
      EnumDisplayMonitors(IntPtr.Zero, IntPtr.Zero, cb, IntPtr.Zero);
      var doc = new Dictionary<string, object>();
      doc["monitors"] = monitors;
      return doc;
    }
  }
}
"@
[MadoDisplay.Native]::Snapshot() | ConvertTo-Json -Depth 6 -Compress
"""

# Fields the tool will re-print (whitelist). Anything else in the child JSON
# is dropped silently.
ALLOWED_TOP_KEYS = {"monitors"}
ALLOWED_MONITOR_KEYS = {
    "device", "primary", "monitor", "work",
    "mode_current", "mode_registry", "mode_list_count",
}


def _err(stage: str, detail: str) -> int:
    print(f"MADO_WINDISPLAY: ERROR (stage={stage} detail={_brief(detail)})")
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


def validate(doc: Any) -> tuple[dict[str, Any], list[str]]:
    """Schema-check a parsed snapshot. Returns (clean_doc, problems)."""
    problems: list[str] = []
    if not isinstance(doc, dict):
        return {}, ["top-level JSON is not an object"]
    unknown = sorted(set(doc) - ALLOWED_TOP_KEYS)
    if unknown:
        problems.append(f"unknown top keys dropped: {','.join(unknown)}")
    clean: dict[str, Any] = {}
    raw_monitors = doc.get("monitors")
    if not isinstance(raw_monitors, list):
        problems.append("missing/invalid object: monitors")
        return clean, problems
    monitors: list[Any] = []
    for index, mon in enumerate(raw_monitors):
        if not isinstance(mon, dict):
            problems.append(f"monitor {index} is not an object")
            continue
        unknown_mon = sorted(set(mon) - ALLOWED_MONITOR_KEYS)
        if unknown_mon:
            problems.append(f"monitor {index} unknown keys dropped: {','.join(unknown_mon)}")
        monitors.append({k: mon[k] for k in ALLOWED_MONITOR_KEYS if k in mon})
    clean["monitors"] = monitors
    return clean, problems


def sanity(clean: dict[str, Any]) -> list[str]:
    """Post-schema sanity checks (CHECK FAILED class, not ERROR)."""
    problems: list[str] = []
    monitors = clean.get("monitors") or []
    if not monitors:
        problems.append("no monitor was enumerated")
        return problems
    primaries = 0
    for index, mon in enumerate(monitors):
        tag = f"monitor[{index}]"
        device = mon.get("device")
        if not isinstance(device, str) or not device:
            problems.append(f"{tag}.device is not a non-empty string")
        if mon.get("primary") is True:
            primaries += 1
        elif mon.get("primary") is not False:
            problems.append(f"{tag}.primary is not a boolean")
        rect = mon.get("monitor")
        work = mon.get("work")
        if not _is_rect(rect) or not _rect_positive(rect):
            problems.append(f"{tag}.monitor rect is not four ints with positive extent")
            rect = None
        if not _is_rect(work):
            problems.append(f"{tag}.work rect is not four ints")
            work = None
        if rect is not None and work is not None:
            if not (_rect_contains(rect, work)):
                problems.append(f"{tag}.work rect is not inside the monitor rect")
        mode = mon.get("mode_current")
        if not isinstance(mode, dict) or mode.get("ok") is not True:
            problems.append(
                f"{tag}.mode_current did not report "
                f"(EnumDisplaySettings's documented failure return is 0)")
        else:
            for key in ("w", "h", "freq", "bpp"):
                value = mode.get(key)
                if not _is_int(value) or value <= 0:
                    problems.append(
                        f"{tag}.mode_current.{key} is not a positive integer "
                        f"(a 0 return is the not-reported shape, never a measurement)")
        registry = mon.get("mode_registry")
        if not isinstance(registry, dict):
            problems.append(f"{tag}.mode_registry is not an object")
        count = mon.get("mode_list_count")
        if not _is_int(count) or count < 1:
            problems.append(f"{tag}.mode_list_count is not a positive integer")
    if primaries != 1:
        problems.append(
            f"exactly one monitor must carry MONITORINFOF_PRIMARY; found {primaries}")
    return problems


def _is_rect(value: Any) -> bool:
    return (isinstance(value, list) and len(value) == 4
            and all(_is_int(v) for v in value))


def _rect_positive(rect: list[int]) -> bool:
    left, top, right, bottom = rect
    return right > left and bottom > top


def _rect_contains(outer: list[int], inner: list[int]) -> bool:
    return (inner[0] >= outer[0] and inner[1] >= outer[1]
            and inner[2] <= outer[2] and inner[3] <= outer[3])


def _primary(monitors: list[Any]) -> dict[str, Any] | None:
    for mon in monitors:
        if mon.get("primary") is True:
            return mon
    return None


def verdict_line(clean: dict[str, Any]) -> str:
    monitors = clean.get("monitors") or []
    primary = _primary(monitors) or {}
    rect = primary.get("monitor") or [0, 0, 0, 0]
    work = primary.get("work") or [0, 0, 0, 0]
    mode = primary.get("mode_current") or {}
    if mode.get("ok") is True:
        mode_txt = f"mode={mode.get('w')}x{mode.get('h')}@{mode.get('freq')}"
    else:
        mode_txt = "mode=unreported"
    return (
        f"MADO_WINDISPLAY: CLEAN (monitors={len(monitors)} "
        f"primary={primary.get('device')} {mode_txt} "
        f"work={work[2] - work[0]}x{work[3] - work[1]})".replace("  ", " ")
        if rect is not None else "MADO_WINDISPLAY: CLEAN"
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
        print(f"MADO_WINDISPLAY: CHECK FAILED ({where}{'; '.join(bad)})")
        print_json(clean)
        return 1
    if source:
        monitors = clean.get("monitors") or []
        primary = _primary(monitors) or {}
        mode = primary.get("mode_current") or {}
        print(
            f"MADO_WINDISPLAY: CLEAN (source=file {source}) monitors={len(monitors)} "
            f"primary={primary.get('device')}"
        )
    else:
        print(verdict_line(clean))
    print_json(clean)
    return 0


def selftest() -> int:
    import os
    import tempfile

    def canned(monitors_json: str) -> str:
        return '{"monitors": ' + monitors_json + '}'

    SINGLE = ('[{"device":"\\\\\\\\.\\\\DISPLAY1","primary":true,'
              '"monitor":[0,0,1920,1080],"work":[0,0,1920,1032],'
              '"mode_current":{"ok":true,"w":1920,"h":1080,"freq":64,"bpp":32,"pos":[0,0]},'
              '"mode_registry":{"ok":true,"w":1920,"h":1080,"freq":64,"bpp":32},'
              '"mode_list_count":1}]')

    class Tests(unittest.TestCase):
        def test_parses_canned_live_document(self):
            clean, problems = validate(json.loads(canned(SINGLE)))
            self.assertEqual(problems, [])
            self.assertEqual(sanity(clean), [])
            self.assertEqual(len(clean["monitors"]), 1)
            line = verdict_line(clean)
            self.assertIn("monitors=1", line)
            self.assertIn("primary=\\\\.\\DISPLAY1", line)
            self.assertIn("mode=1920x1080@64", line)
            self.assertIn("work=1920x1032", line)

        def test_unknown_keys_dropped_whitelist(self):
            doc = json.loads(canned(
                '[{"device":"\\\\\\\\.\\\\DISPLAY1","primary":true,'
                '"monitor":[0,0,1920,1080],"work":[0,0,1920,1032],'
                '"mode_current":{"ok":true,"w":1920,"h":1080,"freq":64,"bpp":32},'
                '"mode_registry":{"ok":true,"w":1920,"h":1080,"freq":64,"bpp":32},'
                '"mode_list_count":1,"secret":{"value":"leaked-secret-9d2b"}}]'))
            clean, problems = validate(doc)
            self.assertNotIn("secret", clean["monitors"][0])
            self.assertTrue(any("unknown keys dropped: secret" in p for p in problems))
            self.assertEqual(sanity(clean), [])
            self.assertNotIn("leaked-secret-9d2b", verdict_line(clean))
            self.assertNotIn("leaked-secret-9d2b", json.dumps(clean, sort_keys=True, ensure_ascii=True))

        def test_two_primaries_is_check_failed(self):
            two = json.loads(canned(SINGLE)[:-2] + ", " + SINGLE[1:-1] + "]}")
            two_doc = json.loads(canned(
                '[' + SINGLE[1:-1] + ', ' + SINGLE[1:-1] + ']'))
            clean, problems = validate(two_doc)
            self.assertEqual(problems, [])
            bad = sanity(clean)
            self.assertTrue(any("exactly one monitor must carry MONITORINFOF_PRIMARY" in p for p in bad), bad)
            self.assertEqual(two, two_doc)  # the two-primary fixture really has two entries

        def test_work_rect_outside_monitor_is_check_failed(self):
            doc = json.loads(canned(
                '[{"device":"\\\\\\\\.\\\\DISPLAY1","primary":true,'
                '"monitor":[0,0,1920,1080],"work":[0,0,1921,2000],'
                '"mode_current":{"ok":true,"w":1920,"h":1080,"freq":64,"bpp":32},'
                '"mode_registry":{"ok":true,"w":1920,"h":1080,"freq":64,"bpp":32},'
                '"mode_list_count":1}]'))
            clean, _ = validate(doc)
            bad = sanity(clean)
            self.assertTrue(any("work rect is not inside the monitor rect" in p for p in bad), bad)

        def test_zero_frequency_is_check_failed_not_a_measurement(self):
            doc = json.loads(canned(
                '[{"device":"\\\\\\\\.\\\\DISPLAY1","primary":true,'
                '"monitor":[0,0,1920,1080],"work":[0,0,1920,1032],'
                '"mode_current":{"ok":true,"w":1920,"h":1080,"freq":0,"bpp":32},'
                '"mode_registry":{"ok":true,"w":1920,"h":1080,"freq":64,"bpp":32},'
                '"mode_list_count":1}]'))
            clean, _ = validate(doc)
            bad = sanity(clean)
            self.assertTrue(
                any("mode_current.freq is not a positive integer" in p for p in bad), bad)
            self.assertTrue(any("never a measurement" in p for p in bad), bad)

        def test_empty_mode_list_is_check_failed(self):
            doc = json.loads(canned(
                '[{"device":"\\\\\\\\.\\\\DISPLAY1","primary":true,'
                '"monitor":[0,0,1920,1080],"work":[0,0,1920,1032],'
                '"mode_current":{"ok":true,"w":1920,"h":1080,"freq":64,"bpp":32},'
                '"mode_registry":{"ok":true,"w":1920,"h":1080,"freq":64,"bpp":32},'
                '"mode_list_count":0}]'))
            clean, _ = validate(doc)
            bad = sanity(clean)
            self.assertTrue(any("mode_list_count is not a positive integer" in p for p in bad), bad)

        def test_from_file_roundtrip(self):
            tmpdir = tempfile.mkdtemp(prefix="mado-windisplay-selftest-")
            try:
                path = os.path.join(tmpdir, "snapshot.json")
                with open(path, "w", encoding="utf-8") as handle:
                    handle.write(canned(SINGLE))
                buf = io.StringIO()
                with contextlib.redirect_stdout(buf):
                    rc = run_file(path)
                out = buf.getvalue()
                self.assertEqual(rc, 0, out)
                self.assertIn("source=file", out)
                self.assertIn("primary=", out)
            finally:
                for name in os.listdir(tmpdir):
                    os.unlink(os.path.join(tmpdir, name))
                os.rmdir(tmpdir)

        def test_malformed_snapshot_is_error_and_bytes_never_echoed(self):
            payload = b'{"monitors": NOT_JSON @@@'
            tmpdir = tempfile.mkdtemp(prefix="mado-windisplay-selftest-")
            try:
                path = os.path.join(tmpdir, "broken.json")
                with open(path, "wb") as handle:
                    handle.write(payload)
                buf = io.StringIO()
                with contextlib.redirect_stdout(buf):
                    rc = run_file(path)
                out = buf.getvalue()
                self.assertEqual(rc, 2, out)
                self.assertTrue(out.startswith("MADO_WINDISPLAY: ERROR (stage=parse"), out[:80])
                self.assertNotIn("NOT_JSON", out)
            finally:
                for name in os.listdir(tmpdir):
                    os.unlink(os.path.join(tmpdir, name))
                os.rmdir(tmpdir)

        def test_fixed_script_only_getters_never_titles_handles_or_changes(self):
            low = PS_SCRIPT.lower()
            # every import is a documented getter; no mode-change verb exists
            self.assertNotIn("changedisplaysettings", low)
            self.assertNotIn("setdisplaysettings", low)
            self.assertNotIn("changethread", low)
            self.assertNotIn("wmi", low)
            self.assertNotIn("clipboard", low)
            self.assertNotIn("windowtitle", low)
            self.assertNotIn("mainwindowhandle", low)
            self.assertNotIn("get-childitem env:", low)
            # no registry API reads (the mode_registry FIELD is a documented
            # iModeNum shape, not a Registry read — named for the next reader)
            self.assertNotIn("microsoft.win32.registry", low)
            self.assertNotIn("get-itemproperty", low)
            # the three documented query families appear at exactly their
            # declared sites: 1 import + 1 call for the enumeration pair;
            # 1 import + 3 call sites for the mode query (-1 current,
            # -2 registry, index series)
            self.assertEqual(low.count("enumdisplaymonitors"), 2, low)
            self.assertEqual(low.count("getmonitorinfow"), 2, low)
            self.assertEqual(low.count("enumdisplaysettingsw"), 4, low)
            # the callback always returns true (enumeration is never aborted)
            self.assertIn("return true", low)
            # fixed-size buffers exactly as documented: szDevice,
            # dmDeviceName and dmFormName are each CCHDEVICENAME/CCHFORMNAME
            self.assertEqual(low.count("sizeconst = 32"), 3, low)
            self.assertIn("convertto-json", low)

        def test_error_line_is_bounded_and_single_line(self):
            buf = io.StringIO()
            with contextlib.redirect_stdout(buf):
                rc = _err("spawn", "interpreter not found: nope")
            out = buf.getvalue()
            self.assertEqual(rc, 2)
            self.assertEqual(len(out.strip().splitlines()), 1)
            self.assertLessEqual(len(out), 200)
            self.assertTrue(out.startswith("MADO_WINDISPLAY: ERROR (stage=spawn"))

    suite = unittest.defaultTestLoader.loadTestsFromTestCase(Tests)
    runner = unittest.TextTestRunner(stream=sys.stderr, verbosity=0)
    result = runner.run(suite)
    total = result.testsRun
    failures = len(result.failures) + len(result.errors)
    print(f"MADO_WINDISPLAY_SELFTEST: {total - failures}/{total} assertions passed (tool sha256 pinned in the ledger, not in-run)")
    return 0 if failures == 0 else 2


def main() -> int:
    parser = argparse.ArgumentParser(prog=TOOL, description="read-only Windows display-topology observer")
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
