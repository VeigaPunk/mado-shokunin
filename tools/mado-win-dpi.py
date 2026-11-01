#!/usr/bin/env python3
"""mado-win-dpi.py — read-only Windows DPI-virtualization observer (mado-shokunin round 60).

WHAT IT OBSERVES (all reads, no writes, no mutations; every P/Invoke is a getter):
  - calling-thread DPI awareness (GetThreadDpiAwarenessContext ->
    GetAwarenessFromDpiAwarenessContext; reported as the documented
    DPI_AWARENESS value 0/1/2, -1 invalid);
  - system metrics under DPI virtualization: GetSystemMetrics(SM_CXSCREEN /
    SM_CYSCREEN) beside GetSystemMetricsForDpi(SM_CXSCREEN / SM_CYSCREEN, 96);
  - main-window awareness histogram (Get-Process census where MainWindowHandle
    -ne 0, then GetWindowDpiAwarenessContext -> GetAwarenessFromDpiAwareness-
    Context per handle; histogram counts only);
  - foreground window: GetDpiForWindow and the window's own awareness
    (point-in-time foreground, never bound).

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
  - collects no window titles, no process names, no window handles in its
    output; prints no clipboard contents, no environment values, no file
    contents (round-56 M56-17 rule carried: a channel may be asserted to
    exist, its values are never printed);
  - never echoes raw child output — child stdout is parsed as JSON and only
    whitelisted fields are re-printed; on parse failure a verdict line plus
    the raw byte length and sha256 prefix are printed, never the bytes;
  - writes no file, opens no socket, changes no setting (no Set* verb exists
    in this tool; setting thread DPI awareness stays operator-owned).

EXIT MAP:  0 = CLEAN (live or file snapshot parsed and sane)
           1 = CHECK FAILED (parsed, but a sanity check failed)
           2 = ERROR (spawn, parse or schema failure; --selftest failure)
OUTPUT: one `MADO_WINDPI:` verdict line, then one JSON object line.

KNOWN LIMITS (stated, not hidden):
  - the awareness join is vacuous at an effective DPI of 96: aware and
    unaware callers read the same numbers on a 100%-scaled host, so an
    agreement between GetSystemMetrics and GetSystemMetricsForDpi(..., 96)
    does not by itself identify the caller's branch (the r58 entry's J05
    vacuous shape; the branch is identified by the measured awareness value,
    not by the metrics join);
  - the window histogram and the foreground window are point-in-time
    observations; cross-checks bind only the stable fields (thread
    awareness, the four metric values);
  - GetSystemMetrics is documented "not DPI aware" and its failure return is
    0, indistinguishable from a zero metric; the tool treats any metric <= 0
    as CHECK FAILED rather than as a measurement;
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

TOOL = "mado-win-dpi"
VERSION = "r60-v1"

# The fixed read-only script handed to PowerShell. It is embedded verbatim so
# the tool's own bytes pin exactly what ran. It collects no titles, no process
# names and no handles into its output; the static selftest asserts that.
PS_SCRIPT = r"""
$ErrorActionPreference = 'Stop'
$sig = @'
[DllImport("user32.dll")] public static extern System.IntPtr GetThreadDpiAwarenessContext();
[DllImport("user32.dll")] public static extern int GetAwarenessFromDpiAwarenessContext(System.IntPtr value);
[DllImport("user32.dll")] public static extern System.IntPtr GetWindowDpiAwarenessContext(System.IntPtr hwnd);
[DllImport("user32.dll")] public static extern System.IntPtr GetForegroundWindow();
[DllImport("user32.dll")] public static extern int GetDpiForWindow(System.IntPtr hwnd);
[DllImport("user32.dll")] public static extern int GetSystemMetrics(int nIndex);
[DllImport("user32.dll")] public static extern int GetSystemMetricsForDpi(int nIndex, uint dpi);
'@
Add-Type -MemberDefinition $sig -Name MadoDpi -Namespace Win32 | Out-Null
$awareness = [Win32.MadoDpi]::GetAwarenessFromDpiAwarenessContext([Win32.MadoDpi]::GetThreadDpiAwarenessContext())
$cx   = [Win32.MadoDpi]::GetSystemMetrics(0)
$cy   = [Win32.MadoDpi]::GetSystemMetrics(1)
$cx96 = [Win32.MadoDpi]::GetSystemMetricsForDpi(0, 96)
$cy96 = [Win32.MadoDpi]::GetSystemMetricsForDpi(1, 96)
$hist = @{ a0 = 0; a1 = 0; a2 = 0; invalid = 0 }
$wins = @(Get-Process | Where-Object { $_.MainWindowHandle -ne 0 })
foreach ($w in $wins) {
  try {
    $a = [Win32.MadoDpi]::GetAwarenessFromDpiAwarenessContext([Win32.MadoDpi]::GetWindowDpiAwarenessContext($w.MainWindowHandle))
    switch ($a) { 0 { $hist.a0++ } 1 { $hist.a1++ } 2 { $hist.a2++ } default { $hist.invalid++ } }
  } catch { $hist.invalid++ }
}
$fg = [Win32.MadoDpi]::GetForegroundWindow()
$fgPresent = $false; $fgDpi = -1; $fgAware = -1
if ($fg -ne [System.IntPtr]::Zero) {
  $fgPresent = $true
  $fgDpi = [Win32.MadoDpi]::GetDpiForWindow($fg)
  $fgAware = [Win32.MadoDpi]::GetAwarenessFromDpiAwarenessContext([Win32.MadoDpi]::GetWindowDpiAwarenessContext($fg))
}
[ordered]@{
  thread  = [ordered]@{ awareness = $awareness }
  metrics = [ordered]@{ cxscreen = $cx; cyscreen = $cy; cxscreen_dpi96 = $cx96; cyscreen_dpi96 = $cy96 }
  windows = [ordered]@{ with_main = $wins.Count; aware0 = $hist.a0; aware1 = $hist.a1;
                        aware2 = $hist.a2; awareness_invalid = $hist.invalid;
                        foreground_present = [bool]$fgPresent; foreground_dpi = $fgDpi;
                        foreground_awareness = $fgAware }
} | ConvertTo-Json -Depth 5 -Compress
"""

# Fields the tool will re-print (whitelist). Anything else in the child JSON
# is dropped silently.
ALLOWED_TOP_KEYS = {"thread", "metrics", "windows"}
DOCUMENTED_AWARENESS = {-1, 0, 1, 2}
AWARENESS_NAMES = {-1: "invalid", 0: "unaware", 1: "system", 2: "per-monitor"}


def _err(stage: str, detail: str) -> int:
    print(f"MADO_WINDPI: ERROR (stage={stage} detail={_brief(detail)})")
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
    for key in ("thread", "metrics", "windows"):
        sub = doc.get(key)
        if not isinstance(sub, dict):
            problems.append(f"missing/invalid object: {key}")
        else:
            clean[key] = dict(sub)
    return clean, problems


def sanity(clean: dict[str, Any]) -> list[str]:
    """Post-schema sanity checks (CHECK FAILED class, not ERROR)."""
    problems: list[str] = []
    thread = clean.get("thread") or {}
    awareness = thread.get("awareness")
    if not _is_int(awareness) or awareness not in DOCUMENTED_AWARENESS:
        problems.append("thread.awareness is not a documented DPI_AWARENESS value")
    elif awareness == -1:
        problems.append("thread.awareness is DPI_AWARENESS_INVALID")
    metrics = clean.get("metrics") or {}
    for key in ("cxscreen", "cyscreen", "cxscreen_dpi96", "cyscreen_dpi96"):
        value = metrics.get(key)
        if not _is_int(value) or value <= 0:
            problems.append(f"metrics.{key} is not a positive integer "
                            f"(GetSystemMetrics's documented failure return is 0)")
    windows = clean.get("windows") or {}
    with_main = windows.get("with_main")
    buckets = [windows.get(k) for k in ("aware0", "aware1", "aware2", "awareness_invalid")]
    if not _is_int(with_main) or with_main < 0:
        problems.append("windows.with_main is not a non-negative integer")
    for name, value in zip(("aware0", "aware1", "aware2", "awareness_invalid"), buckets):
        if not _is_int(value) or value < 0:
            problems.append(f"windows.{name} is not a non-negative integer")
    if _is_int(with_main) and all(_is_int(b) and b >= 0 for b in buckets):
        if with_main != sum(buckets):
            problems.append("window histogram does not sum to windows.with_main")
    fg_present = windows.get("foreground_present")
    if not isinstance(fg_present, bool):
        problems.append("windows.foreground_present is not a boolean")
    elif fg_present:
        fg_dpi = windows.get("foreground_dpi")
        if not _is_int(fg_dpi) or fg_dpi <= 0:
            problems.append("foreground window present but windows.foreground_dpi is not positive")
        fg_aware = windows.get("foreground_awareness")
        if not _is_int(fg_aware) or fg_aware not in DOCUMENTED_AWARENESS or fg_aware == -1:
            problems.append("windows.foreground_awareness is not a documented DPI_AWARENESS value")
    return problems


def verdict_line(clean: dict[str, Any]) -> str:
    metrics = clean.get("metrics") or {}
    windows = clean.get("windows") or {}
    awareness = (clean.get("thread") or {}).get("awareness")
    name = AWARENESS_NAMES.get(awareness, "?") if _is_int(awareness) else "?"
    cx, cy = metrics.get("cxscreen"), metrics.get("cyscreen")
    cx96, cy96 = metrics.get("cxscreen_dpi96"), metrics.get("cyscreen_dpi96")
    if windows.get("foreground_present") is True:
        fg = f"fg_dpi={windows.get('foreground_dpi')}"
    else:
        fg = "fg_dpi=absent"
    return (
        f"MADO_WINDPI: CLEAN (awareness={name} metrics={cx}x{cy} "
        f"dpi96={cx96}x{cy96} windows={windows.get('with_main')} {fg})"
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
    if any("missing/invalid" in p for p in problems):
        return _err("schema", "; ".join(p for p in problems if "missing/invalid" in p))
    bad = sanity(clean)
    if bad:
        where = f"source=file {source}; " if source else ""
        print(f"MADO_WINDPI: CHECK FAILED ({where}{'; '.join(bad)})")
        print_json(clean)
        return 1
    if source:
        metrics = clean.get("metrics") or {}
        windows = clean.get("windows") or {}
        awareness = (clean.get("thread") or {}).get("awareness")
        name = AWARENESS_NAMES.get(awareness, "?") if _is_int(awareness) else "?"
        print(
            f"MADO_WINDPI: CLEAN (source=file {source}) awareness={name} "
            f"metrics={metrics.get('cxscreen')}x{metrics.get('cyscreen')} "
            f"windows={windows.get('with_main')}"
        )
    else:
        print(verdict_line(clean))
    print_json(clean)
    return 0


def selftest() -> int:
    import os
    import tempfile

    class Tests(unittest.TestCase):
        def test_parses_canned_live_document(self):
            canned = (
                '{"thread":{"awareness":0},'
                '"metrics":{"cxscreen":1920,"cyscreen":1080,"cxscreen_dpi96":1920,"cyscreen_dpi96":1080},'
                '"windows":{"with_main":6,"aware0":0,"aware1":0,"aware2":6,"awareness_invalid":0,'
                '"foreground_present":true,"foreground_dpi":96,"foreground_awareness":2}}'
            )
            clean, problems = validate(json.loads(canned))
            self.assertEqual(problems, [])
            self.assertEqual(sanity(clean), [])
            self.assertEqual(clean["thread"]["awareness"], 0)
            self.assertIn("awareness=unaware", verdict_line(clean))
            self.assertIn("metrics=1920x1080", verdict_line(clean))
            self.assertIn("fg_dpi=96", verdict_line(clean))

        def test_unknown_keys_dropped_whitelist(self):
            doc = json.loads(
                '{"thread":{"awareness":1},"metrics":{"cxscreen":1920,"cyscreen":1080,'
                '"cxscreen_dpi96":1920,"cyscreen_dpi96":1080},"windows":{"with_main":0,'
                '"aware0":0,"aware1":0,"aware2":0,"awareness_invalid":0,'
                '"foreground_present":false,"foreground_dpi":-1,"foreground_awareness":-1},'
                '"secret":{"value":"leaked-secret-7f3a"}}'
            )
            clean, problems = validate(doc)
            self.assertNotIn("secret", clean)
            self.assertTrue(any("unknown top keys dropped: secret" in p for p in problems))
            self.assertEqual(sanity(clean), [])
            self.assertNotIn("leaked-secret-7f3a", verdict_line(clean))
            self.assertNotIn("leaked-secret-7f3a", json.dumps(clean, sort_keys=True, ensure_ascii=True))

        def test_thread_awareness_invalid_is_check_failed(self):
            doc = json.loads(
                '{"thread":{"awareness":-1},'
                '"metrics":{"cxscreen":1920,"cyscreen":1080,"cxscreen_dpi96":1920,"cyscreen_dpi96":1080},'
                '"windows":{"with_main":0,"aware0":0,"aware1":0,"aware2":0,"awareness_invalid":0,'
                '"foreground_present":false,"foreground_dpi":-1,"foreground_awareness":-1}}'
            )
            clean, _ = validate(doc)
            bad = sanity(clean)
            self.assertTrue(any("DPI_AWARENESS_INVALID" in p for p in bad), bad)

        def test_zero_metrics_is_check_failed(self):
            doc = json.loads(
                '{"thread":{"awareness":0},'
                '"metrics":{"cxscreen":0,"cyscreen":1080,"cxscreen_dpi96":1920,"cyscreen_dpi96":1080},'
                '"windows":{"with_main":0,"aware0":0,"aware1":0,"aware2":0,"awareness_invalid":0,'
                '"foreground_present":false,"foreground_dpi":-1,"foreground_awareness":-1}}'
            )
            clean, _ = validate(doc)
            bad = sanity(clean)
            self.assertTrue(any("cxscreen is not a positive integer" in p for p in bad), bad)

        def test_metrics_dpi96_disagreement_is_not_a_failure(self):
            # A non-96 effective DPI legitimately splits the two metric
            # families; the tool must report it CLEAN, not CHECK FAILED —
            # the branch is identified by the awareness value, never by the
            # metrics join.
            doc = json.loads(
                '{"thread":{"awareness":0},'
                '"metrics":{"cxscreen":1536,"cyscreen":864,"cxscreen_dpi96":1920,"cyscreen_dpi96":1080},'
                '"windows":{"with_main":0,"aware0":0,"aware1":0,"aware2":0,"awareness_invalid":0,'
                '"foreground_present":false,"foreground_dpi":-1,"foreground_awareness":-1}}'
            )
            clean, problems = validate(doc)
            self.assertEqual(problems, [])
            self.assertEqual(sanity(clean), [])
            self.assertIn("metrics=1536x864", verdict_line(clean))
            self.assertIn("dpi96=1920x1080", verdict_line(clean))

        def test_histogram_mismatch_is_check_failed(self):
            doc = json.loads(
                '{"thread":{"awareness":0},'
                '"metrics":{"cxscreen":1920,"cyscreen":1080,"cxscreen_dpi96":1920,"cyscreen_dpi96":1080},'
                '"windows":{"with_main":6,"aware0":0,"aware1":0,"aware2":5,"awareness_invalid":0,'
                '"foreground_present":false,"foreground_dpi":-1,"foreground_awareness":-1}}'
            )
            clean, _ = validate(doc)
            bad = sanity(clean)
            self.assertTrue(any("does not sum to" in p for p in bad), bad)

        def test_from_file_roundtrip(self):
            canned = (
                '{"thread":{"awareness":2},'
                '"metrics":{"cxscreen":1920,"cyscreen":1080,"cxscreen_dpi96":1920,"cyscreen_dpi96":1080},'
                '"windows":{"with_main":1,"aware0":0,"aware1":0,"aware2":1,"awareness_invalid":0,'
                '"foreground_present":false,"foreground_dpi":-1,"foreground_awareness":-1}}'
            )
            tmpdir = tempfile.mkdtemp(prefix="mado-windpi-selftest-")
            try:
                path = os.path.join(tmpdir, "snapshot.json")
                with open(path, "w", encoding="utf-8") as handle:
                    handle.write(canned)
                buf = io.StringIO()
                with contextlib.redirect_stdout(buf):
                    rc = run_file(path)
                out = buf.getvalue()
                self.assertEqual(rc, 0, out)
                self.assertIn("awareness=per-monitor", out)
                self.assertIn("source=file", out)
            finally:
                for name in os.listdir(tmpdir):
                    os.unlink(os.path.join(tmpdir, name))
                os.rmdir(tmpdir)

        def test_malformed_snapshot_is_error_and_bytes_never_echoed(self):
            payload = b'{"thread":{"awareness":0}, "metrics": NOT_JSON @@@'
            tmpdir = tempfile.mkdtemp(prefix="mado-windpi-selftest-")
            try:
                path = os.path.join(tmpdir, "broken.json")
                with open(path, "wb") as handle:
                    handle.write(payload)
                buf = io.StringIO()
                with contextlib.redirect_stdout(buf):
                    rc = run_file(path)
                out = buf.getvalue()
                self.assertEqual(rc, 2, out)
                self.assertTrue(out.startswith("MADO_WINDPI: ERROR (stage=parse"), out[:80])
                self.assertNotIn("NOT_JSON", out)
            finally:
                for name in os.listdir(tmpdir):
                    os.unlink(os.path.join(tmpdir, name))
                os.rmdir(tmpdir)

        def test_fixed_script_never_collects_titles_names_handles_or_env(self):
            low = PS_SCRIPT.lower()
            self.assertNotIn("windowtitle", low)
            self.assertNotIn("processname", low)
            self.assertNotIn("clipboard", low)
            self.assertNotIn("get-childitem env:", low)
            self.assertNotIn("microsoft.win32.registry", low)
            # MainWindowHandle appears exactly twice, both reads: the census
            # filter and the per-window awareness query. The handle value
            # itself is never emitted into the output object below.
            self.assertEqual(low.count("mainwindowhandle"), 2, low)
            out_block = low[low.index("[ordered]@{"):]
            self.assertNotIn("mainwindowhandle", out_block)
            self.assertIn("convertto-json", low)
            # every P/Invoke in the script is a getter: no Set* verb exists
            for banned in ("setthreaddpiawareness", "setprocessdpiawareness", "shcore"):
                self.assertNotIn(banned, low)

        def test_error_line_is_bounded_and_single_line(self):
            buf = io.StringIO()
            with contextlib.redirect_stdout(buf):
                rc = _err("spawn", "interpreter not found: nope")
            out = buf.getvalue()
            self.assertEqual(rc, 2)
            self.assertEqual(len(out.strip().splitlines()), 1)
            self.assertLessEqual(len(out), 200)
            self.assertTrue(out.startswith("MADO_WINDPI: ERROR (stage=spawn"))

    suite = unittest.defaultTestLoader.loadTestsFromTestCase(Tests)
    runner = unittest.TextTestRunner(stream=sys.stderr, verbosity=0)
    result = runner.run(suite)
    total = result.testsRun
    failures = len(result.failures) + len(result.errors)
    print(f"MADO_WINDPI_SELFTEST: {total - failures}/{total} assertions passed (tool sha256 pinned in the ledger, not in-run)")
    return 0 if failures == 0 else 2


def main() -> int:
    parser = argparse.ArgumentParser(prog=TOOL, description="read-only Windows DPI-virtualization observer")
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
