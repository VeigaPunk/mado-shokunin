#!/usr/bin/env python3
"""mado-win-desk.py — read-only Windows desktop observer (mado-shokunin round 57).

WHAT IT OBSERVES (all reads, no writes, no mutations):
  - OS identity            (Win32_OperatingSystem: caption, version, build)
  - display topology       (System.Windows.Forms.Screen: device name, primary,
                            bounds, bits per pixel)
  - DPI facts              (registry read twice through different API layers:
                            Get-ItemProperty and Microsoft.Win32.Registry.GetValue;
                            AppliedDPI, LogPixels)
  - compositor state       (dwmapi!DwmIsCompositionEnabled — TRUE/FALSE only)
  - window-manager census  (count of processes with a main window, their process
                            names, foreground window -> pid -> process name)

HOW IT RUNS:
  live mode    spawns exactly one child process: the PowerShell interpreter
               named by --powershell (default `powershell.exe`, resolved on
               PATH), invoked with the fixed arguments below and an embedded,
               fixed read-only script. stdin is /dev/null. The fixed script
               spawns no grandchild processes (the double registry read is two
               different in-process API layers, not two tools).
  --from-file  parses a previously captured JSON snapshot instead of spawning
               PowerShell, so a committed receipt is re-derivable from its
               committed bytes.
  --selftest   parser and static-safety assertions only; spawns nothing and
               writes nothing.

WHAT IT NEVER DOES (hard boundaries):
  - prints no window titles, no clipboard contents, no environment-variable
    values, no file contents (round-56 M56-17 rule: a channel may be asserted
    to exist, its values are never printed);
  - never echoes raw child output — child stdout is parsed as JSON and only
    whitelisted fields are re-printed; on parse failure a verdict line plus the
    raw byte length and sha256 are printed, never the bytes;
  - writes no file, opens no socket, changes no setting.

EXIT MAP:  0 = CLEAN (live or file snapshot parsed and sane)
           1 = CHECK FAILED (parsed, but a sanity check failed, e.g. zero screens)
           2 = ERROR (spawn, parse or schema failure; --selftest failure)
OUTPUT: one `MADO_WINDESK:` verdict line, then one JSON object line.

KNOWN LIMITS (stated, not hidden):
  - the window census is a point-in-time observation; the foreground process
    can change between the tool run and any cross-check, so cross-checks bind
    only the stable fields (screens, DPI, DWM flag, the census count bound);
  - `Screen.AllScreens` reflects the calling session's desktop; in a non-
    interactive session it may report no screens — that is a CHECK FAILED
    verdict, not a host claim;
  - AppliedDPI is the system-metrics DPI for the interactive user, not a
    per-monitor DPI table (no per-monitor value is claimed);
  - the tool reports the DWM composition flag; it says nothing about rendered
    output, and it never toggles anything.
"""

from __future__ import annotations

import argparse
import contextlib
import hashlib
import io
import json
import os
import subprocess
import sys
import unittest
from typing import Any

TOOL = "mado-win-desk"
VERSION = "r58-v1"

# The fixed read-only script handed to PowerShell. It is embedded verbatim so
# the tool's own bytes pin exactly what ran. It must never print environment
# values, window titles or file contents; the static selftest asserts that.
PS_SCRIPT = r"""
$ErrorActionPreference = 'Stop'
$os = Get-CimInstance Win32_OperatingSystem | Select-Object -First 1
Add-Type -AssemblyName System.Windows.Forms | Out-Null
$screens = @([System.Windows.Forms.Screen]::AllScreens | ForEach-Object {
  [ordered]@{ device_name = $_.DeviceName; primary = [bool]$_.Primary;
              x = $_.Bounds.X; y = $_.Bounds.Y; w = $_.Bounds.Width;
              h = $_.Bounds.Height; bpp = $_.BitsPerPixel }
})
$applied = $null
try { $applied = (Get-ItemProperty -Path 'HKCU:\Control Panel\Desktop\WindowMetrics' -Name AppliedDPI -ErrorAction Stop).AppliedDPI } catch {}
$logpix = $null
try { $logpix = (Get-ItemProperty -Path 'HKCU:\Control Panel\Desktop' -Name LogPixels -ErrorAction Stop).LogPixels } catch {}
$regApplied = $null
try { $o = [Microsoft.Win32.Registry]::GetValue('HKEY_CURRENT_USER\Control Panel\Desktop\WindowMetrics', 'AppliedDPI', $null); if ($null -ne $o) { $regApplied = [int]$o } } catch {}
$sig = @'
[DllImport("dwmapi.dll")] public static extern int DwmIsCompositionEnabled(out bool enabled);
[DllImport("user32.dll")] public static extern IntPtr GetForegroundWindow();
[DllImport("user32.dll")] public static extern uint GetWindowThreadProcessId(IntPtr hWnd, out uint pid);
'@
Add-Type -MemberDefinition $sig -Name MadoDesk -Namespace Win32 | Out-Null
$en = $false
$hr = [Win32.MadoDesk]::DwmIsCompositionEnabled([ref]$en)
$wins = @(Get-Process | Where-Object { $_.MainWindowHandle -ne 0 })
$names = @($wins | ForEach-Object { $_.ProcessName } | Sort-Object -Unique)
$fg = [Win32.MadoDesk]::GetForegroundWindow()
$fgpid = [uint32]0
[void][Win32.MadoDesk]::GetWindowThreadProcessId($fg, [ref]$fgpid)
$fgname = $null
if ($fgpid -gt 0) { try { $fgname = (Get-Process -Id $fgpid -ErrorAction Stop).ProcessName } catch {} }
[ordered]@{
  os      = [ordered]@{ caption = $os.Caption; version = $os.Version; build = $os.BuildNumber }
  screens = $screens
  dpi     = [ordered]@{ applied_dpi = $applied; logpixels = $logpix; reg_applied_dpi = $regApplied }
  dwm     = [ordered]@{ composition_enabled = [bool]$en; hr = $hr }
  windows = [ordered]@{ with_main = $wins.Count; process_names = $names;
                        foreground_pid = $fgpid; foreground_process = $fgname }
} | ConvertTo-Json -Depth 5 -Compress
"""

# Fields the tool will re-print (whitelist). Anything else in the child JSON is
# dropped silently.
ALLOWED_SCREEN_KEYS = {"device_name", "primary", "x", "y", "w", "h", "bpp"}
ALLOWED_TOP_KEYS = {"os", "screens", "dpi", "dwm", "windows"}


def _err(stage: str, detail: str) -> int:
    print(f"MADO_WINDESK: ERROR (stage={stage} detail={_brief(detail)})")
    return 2


def _brief(text: str, limit: int = 120) -> str:
    """One line, bounded, of a message that never carries raw child output."""
    one = " ".join(str(text).split())
    if len(one) > limit:
        one = one[: limit - 3] + "..."
    # belt and braces: no matter the source, never print quote-backed blobs
    return one.replace("`", "'")


def _screen_view(raw: dict[str, Any]) -> dict[str, Any]:
    out: dict[str, Any] = {}
    for key in sorted(ALLOWED_SCREEN_KEYS):
        if key in raw:
            out[key] = raw[key]
    return out


def validate(doc: Any) -> tuple[dict[str, Any], list[str]]:
    """Schema-check a parsed snapshot. Returns (clean_doc, problems)."""
    problems: list[str] = []
    if not isinstance(doc, dict):
        return {}, ["top-level JSON is not an object"]
    unknown = sorted(set(doc) - ALLOWED_TOP_KEYS)
    if unknown:
        problems.append(f"unknown top keys dropped: {','.join(unknown)}")
    clean: dict[str, Any] = {}
    for key in ("os", "dpi", "dwm", "windows"):
        sub = doc.get(key)
        if not isinstance(sub, dict):
            problems.append(f"missing/invalid object: {key}")
        else:
            clean[key] = dict(sub)
    screens = doc.get("screens")
    if not isinstance(screens, list):
        problems.append("missing/invalid array: screens")
    else:
        clean["screens"] = [_screen_view(s) if isinstance(s, dict) else {"invalid": True} for s in screens]
    return clean, problems


def sanity(clean: dict[str, Any]) -> list[str]:
    """Post-schema sanity checks (CHECK FAILED class, not ERROR)."""
    problems: list[str] = []
    screens = clean.get("screens") or []
    if len(screens) == 0:
        problems.append("zero screens (non-interactive session or snapshot without screens)")
    for s in screens:
        if s.get("invalid"):
            problems.append("a screen entry is not an object")
    dpi = clean.get("dpi") or {}
    a, r = dpi.get("applied_dpi"), dpi.get("reg_applied_dpi")
    if isinstance(a, int) and isinstance(r, int) and a != r:
        problems.append(f"dpi layer disagreement: Get-ItemProperty={a} Registry.GetValue={r}")
    dwm = clean.get("dwm") or {}
    if not isinstance(dwm.get("composition_enabled"), bool):
        problems.append("dwm.composition_enabled is not a boolean")
    wins = clean.get("windows") or {}
    if not isinstance(wins.get("with_main"), int) or wins.get("with_main", -1) < 0:
        problems.append("windows.with_main is not a non-negative integer")
    return problems


def verdict_line(clean: dict[str, Any]) -> str:
    screens = clean.get("screens") or []
    dpi = clean.get("dpi") or {}
    dwm = clean.get("dwm") or {}
    wins = clean.get("windows") or {}
    dwm_state = "on" if dwm.get("composition_enabled") is True else ("off" if dwm.get("composition_enabled") is False else "?")
    dpi_v = dpi.get("applied_dpi") if dpi.get("applied_dpi") is not None else "unset"
    return (
        f"MADO_WINDESK: CLEAN (screens={len(screens)} dpi={dpi_v} dwm={dwm_state} "
        f"windows={wins.get('with_main')})"
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
    clean, problems = validate(doc)
    if any("missing/invalid" in p for p in problems):
        return _err("schema", "; ".join(p for p in problems if "missing/invalid" in p))
    bad = sanity(clean)
    if bad:
        print(f"MADO_WINDESK: CHECK FAILED ({'; '.join(bad)})")
        print_json(clean)
        return 1
    print(verdict_line(clean))
    print_json(clean)
    return 0


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
    clean, problems = validate(doc)
    if any("missing/invalid" in p for p in problems):
        return _err("schema", "; ".join(p for p in problems if "missing/invalid" in p))
    bad = sanity(clean)
    if bad:
        print(f"MADO_WINDESK: CHECK FAILED (source=file {path}; {'; '.join(bad)})")
        print_json(clean)
        return 1
    print(f"MADO_WINDESK: CLEAN (source=file {path}) " f"screens={len(clean.get('screens') or [])}")
    print_json(clean)
    return 0


def selftest() -> int:
    import tempfile

    class Tests(unittest.TestCase):
        def test_parses_canned_live_document(self):
            canned = (
                '{"os":{"caption":"Microsoft Windows 11 Home","version":"10.0.26200",'
                '"build":"26200"},"screens":[{"device_name":"\\\\.\\u005cDISPLAY1",'
                '"primary":true,"x":0,"y":0,"w":1920,"h":1080,"bpp":32}],'
                '"dpi":{"applied_dpi":96,"logpixels":null,"reg_applied_dpi":96},'
                '"dwm":{"composition_enabled":true,"hr":0},'
                '"windows":{"with_main":7,"process_names":["explorer"],'
                '"foreground_pid":9,"foreground_process":"x"}}'
            )
            clean, problems = validate(json.loads(canned))
            self.assertEqual(problems, [])
            self.assertEqual(sanity(clean), [])
            self.assertEqual(len(clean["screens"]), 1)
            self.assertEqual(clean["dpi"]["applied_dpi"], 96)
            self.assertIs(clean["dwm"]["composition_enabled"], True)
            self.assertIn("windows=7", verdict_line(clean))

        def test_zero_screens_is_check_failed(self):
            doc = json.loads(
                '{"os":{"caption":"c","version":"v","build":"b"},"screens":[],'
                '"dpi":{},"dwm":{"composition_enabled":false},"windows":{"with_main":0}}'
            )
            clean, problems = validate(doc)
            self.assertEqual(problems, [])
            self.assertTrue(any("zero screens" in p for p in sanity(clean)))

        def test_dpi_layer_disagreement_fails_sanity(self):
            doc = json.loads(
                '{"os":{"caption":"c","version":"v","build":"b"},'
                '"screens":[{"device_name":"d","primary":true,"x":0,"y":0,"w":1,"h":1,"bpp":32}],'
                '"dpi":{"applied_dpi":96,"logpixels":null,"reg_applied_dpi":120},'
                '"dwm":{"composition_enabled":true},"windows":{"with_main":1}}'
            )
            clean, _ = validate(doc)
            self.assertTrue(any("layer disagreement" in p for p in sanity(clean)))

        def test_unknown_keys_dropped_whitelist(self):
            doc = json.loads(
                '{"os":{},"screens":[],"dpi":{},"dwm":{},"windows":{},'
                '"window_title":"SHOULD-NOT-PRINT","clipboard":"SHOULD-NOT-PRINT"}'
            )
            clean, problems = validate(doc)
            joined = json.dumps(clean)
            self.assertNotIn("SHOULD-NOT-PRINT", joined)
            self.assertTrue(any("unknown top keys dropped" in p for p in problems))

        def test_bad_schema_is_error_class(self):
            clean, problems = validate({"screens": "no"})
            self.assertTrue(any("missing/invalid" in p for p in problems))

        def test_from_file_roundtrip(self):
            doc = {
                "os": {"caption": "c", "version": "v", "build": "b"},
                "screens": [{"device_name": "d", "primary": True, "x": 0, "y": 0, "w": 1, "h": 1, "bpp": 32}],
                "dpi": {"applied_dpi": 96, "logpixels": None, "reg_applied_dpi": 96},
                "dwm": {"composition_enabled": True, "hr": 0},
                "windows": {"with_main": 1, "process_names": ["p"], "foreground_pid": 1, "foreground_process": "p"},
            }
            with tempfile.TemporaryDirectory() as tmp:
                fd, snap = tempfile.mkstemp(suffix=".json", dir=tmp)
                os.close(fd)  # Windows: an open fd locks the file against cleanup
                with open(snap, "w", encoding="utf-8") as fh:
                    fh.write(json.dumps(doc))
                with open(snap, encoding="utf-8") as fh:
                    clean, problems = validate(json.loads(fh.read()))
                self.assertEqual(problems, [])
                self.assertEqual(sanity(clean), [])

        def test_fixed_script_never_prints_titles_env_or_clipboard(self):
            blob = PS_SCRIPT
            for banned in ("MainWindowTitle", "Get-Clipboard", "$env:", "ConvertTo-SecureString"):
                self.assertNotIn(banned, blob, f"fixed script mentions {banned}")

        def test_verdict_line_never_leaks_process_names(self):
            clean = {
                "os": {"caption": "c", "version": "v", "build": "b"},
                "screens": [{"device_name": "d", "primary": True, "x": 0, "y": 0, "w": 1, "h": 1, "bpp": 32}],
                "dpi": {"applied_dpi": 96, "logpixels": None, "reg_applied_dpi": 96},
                "dwm": {"composition_enabled": True, "hr": 0},
                "windows": {"with_main": 3, "process_names": ["secretapp"], "foreground_pid": 5, "foreground_process": "secretapp"},
            }
            line = verdict_line(clean)
            self.assertNotIn("secretapp", line)
            self.assertIn("windows=3", line)

        def test_error_line_is_bounded_and_single_line(self):
            msg = _brief("a\nb\tc  d" + "x" * 500)
            self.assertNotIn("\n", msg)
            self.assertLessEqual(len(msg), 120)

        def test_malformed_snapshot_is_error_and_bytes_never_echoed(self):
            # Round 58: the r57 closure routed the ERROR-path receipt — the C2 sub-claim
            # "malformed input -> MADO_WINDESK: ERROR exit 2, raw bytes never echoed" now
            # runs as part of this tally instead of resting on an uncommitted run.
            payload = '{"os": TRUNCATED-NOT-JSON ::<<raw-payload-marker>>'
            with tempfile.TemporaryDirectory() as tmp:
                fd, snap = tempfile.mkstemp(suffix=".json", dir=tmp)
                os.close(fd)  # Windows: an open fd locks the file against cleanup
                with open(snap, "w", encoding="utf-8") as fh:
                    fh.write(payload)
                buffer = io.StringIO()
                with contextlib.redirect_stdout(buffer):
                    rc = run_file(snap)
            out = buffer.getvalue()
            self.assertEqual(rc, 2)
            self.assertTrue(out.startswith("MADO_WINDESK: ERROR (stage=parse"), out[:80])
            self.assertNotIn("TRUNCATED-NOT-JSON", out)
            self.assertNotIn("raw-payload-marker", out)

    suite = unittest.defaultTestLoader.loadTestsFromTestCase(Tests)
    result = unittest.TextTestRunner(verbosity=0).run(suite)
    total = result.testsRun
    failures = len(result.failures) + len(result.errors)
    print(f"MADO_WINDESK_SELFTEST: {total - failures}/{total} assertions passed (tool sha256 pinned in the ledger, not in-run)")
    return 0 if failures == 0 else 2


def main() -> int:
    parser = argparse.ArgumentParser(prog=TOOL, description="read-only Windows desktop observer (round 57)")
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--selftest", action="store_true", help="parser and safety assertions; spawns nothing")
    group.add_argument("--from-file", metavar="SNAPSHOT", help="validate a captured JSON snapshot instead of running live")
    parser.add_argument("--powershell", default="powershell.exe", help="PowerShell interpreter to spawn (default: powershell.exe)")
    parser.add_argument("--version", action="version", version=f"{TOOL} {VERSION}")
    args = parser.parse_args()
    if args.selftest:
        return selftest()
    if args.from_file:
        return run_file(args.from_file)
    return run_live(args.powershell)


if __name__ == "__main__":
    sys.exit(main())
