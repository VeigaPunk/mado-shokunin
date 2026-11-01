#!/usr/bin/env python3
"""mado-win-displayconfig.py — read-only Windows DisplayConfig path/target observer (mado-shokunin round 63).

WHAT IT OBSERVES (all reads, no writes, no mutations; every P/Invoke is a getter):
  - the CCD (client-side configuration) view of the live display topology:
    GetDisplayConfigBufferSizes beside QueryDisplayConfig, called with
    QDC_ONLY_ACTIVE_PATHS (0x2) and currentTopologyId NULL — the documented
    requirement for any flags value other than QDC_DATABASE_CURRENT;
  - the per-path target refresh rational: DISPLAYCONFIG_PATH_TARGET_INFO.refreshRate
    (the documented query-side refresh the r62 D04 route named as the second
    documented getter);
  - the mode-table join: the path's target modeInfoIdx indexes the
    DISPLAYCONFIG_MODE_INFO array; an entry with infoType ==
    DISPLAYCONFIG_MODE_INFO_TYPE_TARGET (2, per the enumeration page) carries
    DISPLAYCONFIG_TARGET_MODE -> DISPLAYCONFIG_VIDEO_SIGNAL_INFO (vSyncFreq,
    activeSize, totalSize) — recorded, never asserted (this host fills the
    signal's pixelRate/hSyncFreq/vSyncFreq with the undocumented sentinel
    0xFFFFFFFE while activeSize is sane; entry finding D05, cause [UNK]);
  - path/target/source status flags and the documented DPI-virtualization
    non-participation ("This API does not participate in DPI virtualization").

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
    adapter LUID halves, no target/source id integers, no device names, no
    registry values; prints no clipboard contents, no environment values,
    no file contents (round-56 M56-17 rule carried: a channel may be
    asserted to exist, its values are never printed);
  - never echoes raw child output — child stdout is parsed as JSON and only
    whitelisted fields are re-printed; on parse failure a verdict line plus
    the raw byte length and sha256 prefix are printed, never the bytes;
  - writes no file, opens no socket, changes no display configuration
    (no Set*/Change* verb exists in this tool; topology, mode and refresh
    changes stay operator-owned).

EXIT MAP:  0 = CLEAN (live or file snapshot parsed and sane)
           1 = CHECK FAILED (parsed, but a sanity check failed)
           2 = ERROR (spawn, parse or schema failure; --selftest failure)
OUTPUT: one `MADO_WINDISPLAYCONFIG:` verdict line, then one JSON object line.

KNOWN LIMITS (stated, not hidden):
  - every observation is point-in-time; the topology counts and the refresh
    rationals move only when the display configuration changes (unlike the
    r62 window census, not with desktop activity) — two live runs are
    expected byte-identical, and a from-file re-derivation is the
    determinism receipt;
  - the tool emits enum members (outputTechnology, rotation, scaling,
    scanLineOrdering, infoType) as integers only; the member-name mapping
    stays documentation-layer (the enum pages were not opened this round
    beyond DISPLAYCONFIG_MODE_INFO_TYPE, whose SOURCE=1/TARGET=2 values the
    mode-table join needs);
  - the undocumented 0xFFFFFFFE sentinel the host writes into the target
    mode's pixelRate/hSyncFreq/vSyncFreq is recorded, never guessed at
    (finding D05); the path refreshRate side is the measured fact;
  - source-mode entries are counted and indexed only (the union storage is
    mapped to its largest documented member, DISPLAYCONFIG_TARGET_MODE);
    decoding DISPLAYCONFIG_SOURCE_MODE would need a second view of the same
    bytes and no claim needs it;
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

TOOL = "mado-win-displayconfig"
VERSION = "r63-v1"

# The fixed read-only script handed to PowerShell. It is embedded verbatim so
# the tool's own bytes pin exactly what ran. Counts, rationals and flags are
# desktop facts; no adapter LUID halves, no ids, no names, no handles, no
# registry reads. The static selftest pins that.
PS_SCRIPT = r"""
$ErrorActionPreference = 'Stop'
Add-Type -TypeDefinition @"
using System;
using System.Collections.Generic;
using System.Runtime.InteropServices;
namespace MadoDisplayConfig {
  [StructLayout(LayoutKind.Sequential)]
  public struct RATIONAL { public uint Numerator; public uint Denominator; }
  [StructLayout(LayoutKind.Sequential)]
  public struct REGION2D { public uint cx; public uint cy; }
  // DISPLAYCONFIG_VIDEO_SIGNAL_INFO (wingdi.h): pixelRate, hSyncFreq,
  // vSyncFreq, activeSize, totalSize, the DUMMYUNIONNAME 32-bit storage,
  // scanLineOrdering. The union is carried as its 32-bit storage (uint);
  // the tool reads no bitfield of it.
  [StructLayout(LayoutKind.Sequential)]
  public struct VIDEO_SIGNAL_INFO {
    public ulong pixelRate;
    public RATIONAL hSyncFreq;
    public RATIONAL vSyncFreq;
    public REGION2D activeSize;
    public REGION2D totalSize;
    public uint unionBits;
    public int scanLineOrdering;
  }
  [StructLayout(LayoutKind.Sequential)]
  public struct TARGET_MODE { public VIDEO_SIGNAL_INFO targetVideoSignalInfo; }
  // DISPLAYCONFIG_PATH_SOURCE_INFO: LUID adapterId (two 32-bit halves —
  // carried as two uints so the 4-byte alignment of the documented LUID is
  // preserved; the halves are never emitted), id, the DUMMYUNIONNAME
  // 32-bit storage (modeInfoIdx), statusFlags.
  [StructLayout(LayoutKind.Sequential)]
  public struct SOURCE_INFO {
    public uint adapterIdLow;
    public uint adapterIdHigh;
    public uint id;
    public uint modeInfoIdx;
    public uint statusFlags;
  }
  // DISPLAYCONFIG_PATH_TARGET_INFO: LUID adapterId, id, DUMMYUNIONNAME
  // (modeInfoIdx), outputTechnology, rotation, scaling, refreshRate
  // (DISPLAYCONFIG_RATIONAL), scanLineOrdering, targetAvailable (BOOL),
  // statusFlags. Enum members stay integers; names are never emitted.
  [StructLayout(LayoutKind.Sequential)]
  public struct TARGET_INFO {
    public uint adapterIdLow;
    public uint adapterIdHigh;
    public uint id;
    public uint modeInfoIdx;
    public int outputTechnology;
    public int rotation;
    public int scaling;
    public RATIONAL refreshRate;
    public int scanLineOrdering;
    public int targetAvailable;
    public uint statusFlags;
  }
  [StructLayout(LayoutKind.Sequential)]
  public struct PATH_INFO {
    public SOURCE_INFO sourceInfo;
    public TARGET_INFO targetInfo;
    public uint flags;
  }
  // DISPLAYCONFIG_MODE_INFO: infoType (DISPLAYCONFIG_MODE_INFO_TYPE:
  // SOURCE=1, TARGET=2, DESKTOP_IMAGE=3 per the enumeration page), id,
  // LUID adapterId, the union mapped to its largest documented member
  // DISPLAYCONFIG_TARGET_MODE (48 bytes >= source mode 20 bytes);
  // interpreted only when infoType == 2.
  [StructLayout(LayoutKind.Sequential)]
  public struct MODE_INFO {
    public int infoType;
    public uint id;
    public uint adapterIdLow;
    public uint adapterIdHigh;
    public TARGET_MODE targetMode;
  }
  public static class Native {
    [DllImport("user32.dll")] public static extern int GetDisplayConfigBufferSizes(uint flags, out uint numPathArrayElements, out uint numModeInfoArrayElements);
    [DllImport("user32.dll")] public static extern int QueryDisplayConfig(uint flags, ref uint numPathArrayElements, [In, Out] PATH_INFO[] pathArray, ref uint numModeInfoArrayElements, [In, Out] MODE_INFO[] modeInfoArray, IntPtr currentTopologyId);
    public static object Snapshot() {
      // QDC_ONLY_ACTIVE_PATHS = 0x2 (the function page's flag table).
      // currentTopologyId stays NULL: the page requires NULL for any flags
      // value other than QDC_DATABASE_CURRENT (a getter call — no state is
      // touched).
      uint allocFlags = 2;
      uint bufPath = 0, bufMode = 0;
      int hrBuf = GetDisplayConfigBufferSizes(allocFlags, out bufPath, out bufMode);
      var doc = new Dictionary<string, object>();
      doc["buffer_hr"] = hrBuf;
      doc["qdc_flags"] = allocFlags;
      doc["buffer_paths"] = bufPath;
      doc["buffer_modes"] = bufMode;
      if (hrBuf != 0) { return doc; }
      var paths = new PATH_INFO[bufPath];
      var modes = new MODE_INFO[bufMode];
      uint nPath = bufPath, nMode = bufMode;
      int hrQuery = QueryDisplayConfig(allocFlags, ref nPath, paths, ref nMode, modes, IntPtr.Zero);
      doc["query_hr"] = hrQuery;
      doc["paths"] = nPath;
      doc["modes"] = nMode;
      if (hrQuery != 0) { return doc; }
      var pathList = new List<object>();
      for (uint i = 0; i < nPath; i++) {
        var p = paths[i];
        var pj = new Dictionary<string, object>();
        pj["flags"] = p.flags;
        var t = p.targetInfo;
        var tj = new Dictionary<string, object>();
        tj["refresh_num"] = t.refreshRate.Numerator;
        tj["refresh_den"] = t.refreshRate.Denominator;
        tj["output_technology"] = t.outputTechnology;
        tj["rotation"] = t.rotation;
        tj["scaling"] = t.scaling;
        tj["scanline_ordering"] = t.scanLineOrdering;
        tj["target_available"] = t.targetAvailable;
        tj["status_flags"] = t.statusFlags;
        tj["mode_info_idx"] = t.modeInfoIdx;
        pj["target"] = tj;
        var sj = new Dictionary<string, object>();
        sj["status_flags"] = p.sourceInfo.statusFlags;
        sj["mode_info_idx"] = p.sourceInfo.modeInfoIdx;
        pj["source"] = sj;
        uint idx = t.modeInfoIdx;
        if (idx < nMode && modes[idx].infoType == 2) {
          var tm = modes[idx].targetMode.targetVideoSignalInfo;
          var mj = new Dictionary<string, object>();
          mj["vsync_num"] = tm.vSyncFreq.Numerator;
          mj["vsync_den"] = tm.vSyncFreq.Denominator;
          mj["hsync_num"] = tm.hSyncFreq.Numerator;
          mj["hsync_den"] = tm.hSyncFreq.Denominator;
          mj["pixel_rate"] = (double)tm.pixelRate;
          mj["active_cx"] = tm.activeSize.cx;
          mj["active_cy"] = tm.activeSize.cy;
          mj["total_cx"] = tm.totalSize.cx;
          mj["total_cy"] = tm.totalSize.cy;
          mj["scanline_ordering"] = tm.scanLineOrdering;
          mj["join_agree"] = (tm.vSyncFreq.Numerator == t.refreshRate.Numerator && tm.vSyncFreq.Denominator == t.refreshRate.Denominator);
          pj["target_mode"] = mj;
        }
        pathList.Add(pj);
      }
      var modeTypes = new List<int>();
      for (uint i = 0; i < nMode; i++) { modeTypes.Add(modes[i].infoType); }
      doc["mode_info_types"] = modeTypes;
      doc["path_list"] = pathList;
      return doc;
    }
  }
}
"@
[MadoDisplayConfig.Native]::Snapshot() | ConvertTo-Json -Depth 8 -Compress
"""

# Fields the tool will re-print (whitelist). Anything else in the child JSON
# is dropped silently — including the adapter LUID halves and the target and
# source id integers the child script carries for layout only.
ALLOWED_TOP_KEYS = {
    "buffer_hr", "qdc_flags", "buffer_paths", "buffer_modes",
    "query_hr", "paths", "modes", "mode_info_types", "path_list",
}
ALLOWED_PATH_KEYS = {"flags", "target", "source", "target_mode"}
ALLOWED_TARGET_KEYS = {
    "refresh_num", "refresh_den", "output_technology", "rotation",
    "scaling", "scanline_ordering", "target_available", "status_flags",
    "mode_info_idx",
}
ALLOWED_SOURCE_KEYS = {"status_flags", "mode_info_idx"}
ALLOWED_MODE_KEYS = {
    "vsync_num", "vsync_den", "hsync_num", "hsync_den", "pixel_rate",
    "active_cx", "active_cy", "total_cx", "total_cy", "scanline_ordering",
    "join_agree",
}

# The undocumented sentinel this host writes into the target mode's
# pixelRate/hSyncFreq/vSyncFreq (finding D05; recorded, never asserted).
VSYNC_SENTINEL = 0xFFFFFFFE

DISPLAYCONFIG_PATH_ACTIVE = 0x1  # the PATH_INFO page's flag table
MODE_INFO_TYPE_SOURCE = 1        # the DISPLAYCONFIG_MODE_INFO_TYPE page
MODE_INFO_TYPE_TARGET = 2        # the DISPLAYCONFIG_MODE_INFO_TYPE page


def _err(stage: str, detail: str) -> int:
    print(f"MADO_WINDISPLAYCONFIG: ERROR (stage={stage} detail={_brief(detail)})")
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


def _is_num(value: Any) -> bool:
    """True for ints and floats (bool excluded) — pixel_rate arrives as a
    JSON double (the child casts the UINT64 field to double for JSON)."""
    return isinstance(value, (int, float)) and not isinstance(value, bool)


def validate(doc: Any) -> tuple[dict[str, Any], list[str]]:
    """Schema-check a parsed snapshot. Returns (clean_doc, problems)."""
    problems: list[str] = []
    if not isinstance(doc, dict):
        return {}, ["top-level JSON is not an object"]
    unknown = sorted(set(doc) - ALLOWED_TOP_KEYS)
    if unknown:
        problems.append(f"unknown top keys dropped: {','.join(unknown)}")
    clean: dict[str, Any] = {}
    for key in ALLOWED_TOP_KEYS - {"mode_info_types", "path_list"}:
        if key in doc:
            clean[key] = doc[key]
    raw_types = doc.get("mode_info_types")
    if isinstance(raw_types, list):
        clean["mode_info_types"] = [v for v in raw_types if _is_int(v)]
        if len(clean["mode_info_types"]) != len(raw_types):
            problems.append("mode_info_types carried non-integer members (dropped)")
    raw_paths = doc.get("path_list")
    if isinstance(raw_paths, list):
        paths_out: list[dict[str, Any]] = []
        for entry in raw_paths:
            if not isinstance(entry, dict):
                problems.append("path_list carried a non-object member (dropped)")
                continue
            unknown_p = sorted(set(entry) - ALLOWED_PATH_KEYS)
            if unknown_p:
                problems.append(f"path unknown keys dropped: {','.join(unknown_p)}")
            p_clean: dict[str, Any] = {k: entry[k] for k in ALLOWED_PATH_KEYS if k in entry}
            for sub, allowed in (
                ("target", ALLOWED_TARGET_KEYS),
                ("source", ALLOWED_SOURCE_KEYS),
                ("target_mode", ALLOWED_MODE_KEYS),
            ):
                raw_sub = entry.get(sub)
                if isinstance(raw_sub, dict):
                    unknown_s = sorted(set(raw_sub) - allowed)
                    if unknown_s:
                        problems.append(f"path {sub} unknown keys dropped: {','.join(unknown_s)}")
                    p_clean[sub] = {k: raw_sub[k] for k in allowed if k in raw_sub}
            paths_out.append(p_clean)
        clean["path_list"] = paths_out
    return clean, problems


def sanity(clean: dict[str, Any]) -> list[str]:
    """Post-schema sanity checks (CHECK FAILED class, not ERROR)."""
    problems: list[str] = []
    buffer_hr = clean.get("buffer_hr")
    if buffer_hr != 0:
        # GetDisplayConfigBufferSizes' documented return vocabulary is a set
        # of ERROR_ codes; a nonzero return is a documented failure class,
        # never a measurement
        problems.append(
            f"buffer_hr is not 0 (got {buffer_hr!r}; the documented failure "
            "return classes are CHECK FAILED, never a measurement)")
        return problems
    query_hr = clean.get("query_hr")
    if query_hr != 0:
        problems.append(
            f"query_hr is not 0 (got {query_hr!r}; the documented failure "
            "return classes are CHECK FAILED, never a measurement)")
        return problems
    paths = clean.get("paths")
    if not _is_int(paths) or paths < 1:
        # QDC_ONLY_ACTIVE_PATHS returns the active paths of the current
        # session; a session with a visible desktop has at least one
        problems.append("paths is not a positive integer")
        return problems
    modes = clean.get("modes")
    if not _is_int(modes) or modes < 1:
        problems.append("modes is not a positive integer")
        return problems
    path_list = clean.get("path_list")
    if not isinstance(path_list, list) or len(path_list) != paths:
        problems.append("path_list is not a list of paths entries")
        return problems
    mode_types = clean.get("mode_info_types")
    if not isinstance(mode_types, list) or len(mode_types) != modes:
        problems.append("mode_info_types is not a modes-length list")
        return problems
    for i, info_type in enumerate(mode_types):
        if info_type not in (MODE_INFO_TYPE_SOURCE, MODE_INFO_TYPE_TARGET):
            # the MODE_INFO page: the structure contains either source or
            # target mode information — another value is not a measurement
            problems.append(
                f"mode_info_types[{i}] is neither SOURCE(1) nor TARGET(2) "
                f"(got {info_type!r})")
    for i, path in enumerate(path_list):
        flags = path.get("flags")
        if not _is_int(flags) or (flags & DISPLAYCONFIG_PATH_ACTIVE) == 0:
            # the PATH_INFO page: DISPLAYCONFIG_PATH_ACTIVE is "Set by
            # QueryDisplayConfig to indicate that the path is active and
            # part of the desktop" — QDC_ONLY_ACTIVE_PATHS returns active
            # paths only, so a returned path without the bit is not sane
            problems.append(
                f"path_list[{i}].flags does not carry DISPLAYCONFIG_PATH_ACTIVE (0x1)")
        target = path.get("target")
        if not isinstance(target, dict):
            problems.append(f"path_list[{i}].target missing/invalid")
            continue
        refresh_num = target.get("refresh_num")
        refresh_den = target.get("refresh_den")
        if not _is_int(refresh_num) or refresh_num <= 0 or not _is_int(refresh_den) or refresh_den <= 0:
            # a zero refresh rational is the not-a-measurement shape (the
            # all-zero form is documented set-side "does not specify"
            # semantics); never a measurement
            problems.append(
                f"path_list[{i}].target refresh rational is not two positive "
                "integers (a zero rate is the not-a-measurement shape)")
        idx = target.get("mode_info_idx")
        if not _is_int(idx) or idx >= modes:
            problems.append(
                f"path_list[{i}].target mode_info_idx is out of the mode table")
    return problems


def _path_refresh(path: dict[str, Any]) -> str:
    target = path.get("target") or {}
    num = target.get("refresh_num")
    den = target.get("refresh_den")
    return f"{num}/{den}"


def _vsync_status(path: dict[str, Any]) -> str:
    """The recorded-never-asserted vSync disposition of a path's target mode."""
    mode = path.get("target_mode")
    if not isinstance(mode, dict):
        return "absent"
    num = mode.get("vsync_num")
    den = mode.get("vsync_den")
    if num == VSYNC_SENTINEL and den == VSYNC_SENTINEL:
        # the undocumented sentinel this host writes into the signal's
        # frequency fields (finding D05) — recorded, never guessed at
        return f"unavailable(0x{VSYNC_SENTINEL:08x})"
    if not _is_int(num) or not _is_int(den):
        return "unknown"
    if num <= 0 or den <= 0:
        return "not-a-measurement"
    refresh = _path_refresh(path)
    return f"agree({refresh})" if f"{num}/{den}" == refresh else f"differ({num}/{den})"


def verdict_line(clean: dict[str, Any]) -> str:
    """Structure-only verdict: the path count and the refresh/vSync
    dispositions (topology facts that move only on a display change — the
    JSON line carries the full whitelisted detail)."""
    path_list = clean.get("path_list") or []
    refreshes = "+".join(_path_refresh(p) for p in path_list)
    vsync = "+".join(_vsync_status(p) for p in path_list) or "absent"
    return (
        f"MADO_WINDISPLAYCONFIG: CLEAN (paths={len(path_list)} "
        f"refresh={refreshes} vsync={vsync})"
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
    if any("not an object" in p for p in problems):
        return _err("schema", "; ".join(problems))
    bad = sanity(clean)
    if bad:
        where = f"source=file {source}; " if source else ""
        print(f"MADO_WINDISPLAYCONFIG: CHECK FAILED ({where}{'; '.join(bad)})")
        print_json(clean)
        return 1
    if source:
        path_list = clean.get("path_list") or []
        refreshes = "+".join(_path_refresh(p) for p in path_list)
        vsync = "+".join(_vsync_status(p) for p in path_list) or "absent"
        print(
            f"MADO_WINDISPLAYCONFIG: CLEAN (source=file {source}) "
            f"refresh={refreshes} vsync={vsync}"
        )
    else:
        print(verdict_line(clean))
    print_json(clean)
    return 0


def selftest() -> int:
    import os
    import tempfile

    def canned(path_json: str, mode_types: str, path_list: str) -> str:
        return ('{"buffer_hr": 0, "qdc_flags": 2, "buffer_paths": 1, "buffer_modes": 2, '
                '"query_hr": 0, "paths": 1, "modes": 2, "mode_info_types": ' + mode_types
                + ', "path_list": ' + path_list + '}')

    LIVE_PATH = ('{"flags": 1, "target": {"refresh_num": 64, "refresh_den": 1, '
                 '"output_technology": -1, "rotation": 1, "scaling": 1, '
                 '"scanline_ordering": 1, "target_available": 1, "status_flags": 1, '
                 '"mode_info_idx": 0}, "source": {"status_flags": 1, "mode_info_idx": 1}, '
                 '"target_mode": {"vsync_num": 4294967294, "vsync_den": 4294967294, '
                 '"hsync_num": 4294967294, "hsync_den": 4294967294, "pixel_rate": 4294967294, '
                 '"active_cx": 1920, "active_cy": 1080, "total_cx": 1920, "total_cy": 1080, '
                 '"scanline_ordering": 1, "join_agree": false}}')
    LIVE_MODE_TYPES = "[2, 1]"
    LIVE_OK = canned("paths", LIVE_MODE_TYPES, "[" + LIVE_PATH + "]")

    class Tests(unittest.TestCase):
        def test_parses_canned_live_document(self):
            clean, problems = validate(json.loads(LIVE_OK))
            self.assertEqual(problems, [])
            self.assertEqual(sanity(clean), [])
            line = verdict_line(clean)
            self.assertIn("paths=1", line)
            self.assertIn("refresh=64/1", line)
            self.assertIn("vsync=unavailable(0xfffffffe)", line)
            # identity fields never enter any output (the whitelist dropped
            # them before the verdict was built)
            flat = line + json.dumps(clean, sort_keys=True, ensure_ascii=True)
            self.assertNotIn("adapterid", flat.lower().replace("adapter_id", ""))
            self.assertNotIn("output_technology", line)

        def test_unknown_keys_dropped_whitelist(self):
            doc = json.loads(LIVE_OK)
            doc["path_list"][0]["target"]["device_name"] = "leaked-device-9d2b"
            doc["path_list"][0]["adapter_id"] = "leaked-luid-4f8a"
            doc["secret_blob"] = "leaked-secret-1c7e"
            clean, problems = validate(doc)
            self.assertNotIn("device_name", clean["path_list"][0]["target"])
            self.assertNotIn("adapter_id", clean["path_list"][0])
            self.assertNotIn("secret_blob", clean)
            self.assertTrue(any("unknown top keys dropped: secret_blob" in p for p in problems))
            self.assertEqual(sanity(clean), [])
            flat = verdict_line(clean) + json.dumps(clean, sort_keys=True, ensure_ascii=True)
            self.assertNotIn("leaked-device-9d2b", flat)
            self.assertNotIn("leaked-luid-4f8a", flat)
            self.assertNotIn("leaked-secret-1c7e", flat)

        def test_buffer_hr_failure_is_check_failed(self):
            doc = json.loads(LIVE_OK)
            doc["buffer_hr"] = 87
            clean, _ = validate(doc)
            bad = sanity(clean)
            self.assertTrue(any("buffer_hr is not 0" in p for p in bad), bad)
            self.assertTrue(any("never a measurement" in p for p in bad), bad)

        def test_query_hr_failure_is_check_failed(self):
            doc = json.loads(LIVE_OK)
            doc["query_hr"] = 87
            clean, _ = validate(doc)
            bad = sanity(clean)
            self.assertTrue(any("query_hr is not 0" in p for p in bad), bad)

        def test_path_active_bit_missing_is_check_failed(self):
            doc = json.loads(LIVE_OK)
            doc["path_list"][0]["flags"] = 0
            clean, _ = validate(doc)
            bad = sanity(clean)
            self.assertTrue(any("does not carry DISPLAYCONFIG_PATH_ACTIVE" in p for p in bad), bad)

        def test_zero_refresh_rational_is_check_failed(self):
            doc = json.loads(LIVE_OK)
            doc["path_list"][0]["target"]["refresh_num"] = 0
            doc["path_list"][0]["target"]["refresh_den"] = 0
            clean, _ = validate(doc)
            bad = sanity(clean)
            self.assertTrue(any("refresh rational is not two positive integers" in p for p in bad), bad)
            self.assertTrue(any("not-a-measurement shape" in p for p in bad), bad)

        def test_mode_index_out_of_table_is_check_failed(self):
            doc = json.loads(LIVE_OK)
            doc["path_list"][0]["target"]["mode_info_idx"] = 5
            clean, _ = validate(doc)
            bad = sanity(clean)
            self.assertTrue(any("mode_info_idx is out of the mode table" in p for p in bad), bad)

        def test_info_type_neither_source_nor_target_is_check_failed(self):
            doc = json.loads(LIVE_OK)
            doc["mode_info_types"] = [2, 3]
            clean, _ = validate(doc)
            bad = sanity(clean)
            self.assertTrue(any("neither SOURCE(1) nor TARGET(2)" in p for p in bad), bad)

        def test_vsync_decoded_agree_and_differ(self):
            doc = json.loads(LIVE_OK)
            mode = doc["path_list"][0]["target_mode"]
            mode["vsync_num"] = 64
            mode["vsync_den"] = 1
            mode["join_agree"] = True
            clean, _ = validate(doc)
            self.assertEqual(sanity(clean), [])
            self.assertIn("vsync=agree(64/1)", verdict_line(clean))
            mode["vsync_num"] = 59950
            mode["vsync_den"] = 1000
            mode["join_agree"] = False
            clean, _ = validate(doc)
            self.assertEqual(sanity(clean), [])
            self.assertIn("vsync=differ(59950/1000)", verdict_line(clean))

        def test_from_file_roundtrip(self):
            tmpdir = tempfile.mkdtemp(prefix="mado-windisplayconfig-selftest-")
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
                self.assertIn("refresh=64/1", out)
            finally:
                for name in os.listdir(tmpdir):
                    os.unlink(os.path.join(tmpdir, name))
                os.rmdir(tmpdir)

        def test_malformed_snapshot_is_error_and_bytes_never_echoed(self):
            payload = b'{"path_list": NOT_JSON @@@'
            tmpdir = tempfile.mkdtemp(prefix="mado-windisplayconfig-selftest-")
            try:
                path = os.path.join(tmpdir, "broken.json")
                with open(path, "wb") as handle:
                    handle.write(payload)
                buf = io.StringIO()
                with contextlib.redirect_stdout(buf):
                    rc = run_file(path)
                out = buf.getvalue()
                self.assertEqual(rc, 2, out)
                self.assertTrue(out.startswith("MADO_WINDISPLAYCONFIG: ERROR (stage=parse"), out[:80])
                self.assertNotIn("NOT_JSON", out)
            finally:
                for name in os.listdir(tmpdir):
                    os.unlink(os.path.join(tmpdir, name))
                os.rmdir(tmpdir)

        def test_fixed_script_only_getters_never_names_or_changes(self):
            low = PS_SCRIPT.lower()
            # no write/mutation verb exists (SetDisplayConfig and the mode/
            # topology changes stay operator-owned)
            self.assertNotIn("setdisplayconfig", low)
            self.assertNotIn("changedisplaysettings", low)
            self.assertNotIn("deletedisplayconfig", low)
            self.assertNotIn("setwindowpos", low)
            self.assertNotIn("movewindow", low)
            # no registry API, no env, no clipboard, no titles, no handles
            self.assertNotIn("registry", low)
            self.assertNotIn("get-itemproperty", low)
            self.assertNotIn("clipboard", low)
            self.assertNotIn("windowtitle", low)
            self.assertNotIn("mainwindowhandle", low)
            self.assertNotIn("get-childitem env:", low)
            # no name-shaped field is emitted: the adapter LUID halves and
            # the id integers appear as layout fields only, and no device
            # name or friendly-name getter is called
            self.assertNotIn("displayconfiggetdeviceinfo", low)
            self.assertNotIn("friendlyname", low)
            self.assertNotIn("adapterdevicepath", low)
            # the documented query families appear at exactly their declared
            # sites: 1 import + 1 call for GetDisplayConfigBufferSizes;
            # 1 import + 1 call for QueryDisplayConfig
            self.assertEqual(low.count("getdisplayconfigbuffersizes"), 2, low)
            self.assertEqual(low.count("querydisplayconfig"), 2, low)
            # the documented call shapes are pinned: QDC_ONLY_ACTIVE_PATHS
            # (the allocFlags = 2 line) and the NULL currentTopologyId (the
            # IntPtr.Zero argument at the call; the page requires NULL for
            # non-QDC_DATABASE_CURRENT flags)
            self.assertEqual(low.count("allocflags = 2"), 1, low)
            # intptr.zero sites (1): the QueryDisplayConfig call's
            # currentTopologyId argument only — the comment above the call
            # says "stays NULL" and carries no IntPtr.Zero token (the red
            # 12/13 assertion-authoring run counted 2 against a remembered
            # comment shape; fixed to the implementation's actual site list)
            self.assertEqual(low.count("intptr.zero"), 1, low)
            # the LUID is carried as two 32-bit halves at 4-byte alignment
            # (three structs carry the pair: SOURCE_INFO, TARGET_INFO,
            # MODE_INFO)
            self.assertEqual(low.count("public uint adapteridlow;"), 3, low)
            self.assertEqual(low.count("public uint adapteridhigh;"), 3, low)
            # the mode-table join reads infoType == 2 (TARGET per the
            # enumeration page: SOURCE=1, TARGET=2)
            self.assertIn("infotype == 2", low)
            self.assertIn("convertto-json", low)

        def test_error_line_is_bounded_and_single_line(self):
            buf = io.StringIO()
            with contextlib.redirect_stdout(buf):
                rc = _err("spawn", "interpreter not found: nope")
            out = buf.getvalue()
            self.assertEqual(rc, 2)
            self.assertEqual(len(out.strip().splitlines()), 1)
            self.assertLessEqual(len(out), 200)
            self.assertTrue(out.startswith("MADO_WINDISPLAYCONFIG: ERROR (stage=spawn"))

    suite = unittest.defaultTestLoader.loadTestsFromTestCase(Tests)
    runner = unittest.TextTestRunner(stream=sys.stderr, verbosity=0)
    result = runner.run(suite)
    total = result.testsRun
    failures = len(result.failures) + len(result.errors)
    print(f"MADO_WINDISPLAYCONFIG_SELFTEST: {total - failures}/{total} assertions passed (tool sha256 pinned in the ledger, not in-run)")
    return 0 if failures == 0 else 2


def main() -> int:
    parser = argparse.ArgumentParser(prog=TOOL, description="read-only Windows DisplayConfig path/target observer")
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
