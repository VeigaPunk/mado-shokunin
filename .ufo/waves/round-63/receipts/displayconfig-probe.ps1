$ErrorActionPreference = 'Stop'
# mado round-63 read-only probe: DisplayConfig path/target plane (CCD view).
# Getters only: GetDisplayConfigBufferSizes + QueryDisplayConfig with
# QDC_ONLY_ACTIVE_PATHS (0x2) and currentTopologyId NULL (the documented
# requirement for non-QDC_DATABASE_CURRENT calls). Counts and rationals
# only: no adapter ids, no target ids, no device names, no handles emitted.
Add-Type -TypeDefinition @"
using System;
using System.Collections.Generic;
using System.Runtime.InteropServices;
namespace MadoDisplayConfig {
  [StructLayout(LayoutKind.Sequential)]
  public struct RATIONAL { public uint Numerator; public uint Denominator; }
  [StructLayout(LayoutKind.Sequential)]
  public struct REGION2D { public uint cx; public uint cy; }
  [StructLayout(LayoutKind.Sequential)]
  public struct VIDEO_SIGNAL_INFO {
    public ulong pixelRate;
    public RATIONAL hSyncFreq;
    public RATIONAL vSyncFreq;
    public REGION2D activeSize;
    public REGION2D totalSize;
    public uint unionBits;        // the documented DUMMYUNIONNAME storage (videoStandard / AdditionalSignalInfo)
    public int scanLineOrdering;  // DISPLAYCONFIG_SCANLINE_ORDERING, emitted as integer
  }
  [StructLayout(LayoutKind.Sequential)]
  public struct TARGET_MODE { public VIDEO_SIGNAL_INFO targetVideoSignalInfo; }
  [StructLayout(LayoutKind.Sequential)]
  public struct SOURCE_INFO {
    public uint adapterIdLow;   // the documented LUID (two 32-bit halves), carried for layout, never emitted
    public uint adapterIdHigh;
    public uint id;
    public uint modeInfoIdx;    // the documented DUMMYUNIONNAME as its 32-bit storage
    public uint statusFlags;
  }
  [StructLayout(LayoutKind.Sequential)]
  public struct TARGET_INFO {
    public uint adapterIdLow;
    public uint adapterIdHigh;
    public uint id;
    public uint modeInfoIdx;
    public int outputTechnology; // enum integer, never a name
    public int rotation;
    public int scaling;
    public RATIONAL refreshRate;
    public int scanLineOrdering;
    public int targetAvailable;  // BOOL
    public uint statusFlags;
  }
  [StructLayout(LayoutKind.Sequential)]
  public struct PATH_INFO {
    public SOURCE_INFO sourceInfo;
    public TARGET_INFO targetInfo;
    public uint flags;
  }
  [StructLayout(LayoutKind.Sequential)]
  public struct MODE_INFO {
    public int infoType;         // DISPLAYCONFIG_MODE_INFO_TYPE: SOURCE=1, TARGET=2, DESKTOP_IMAGE=3
    public uint id;
    public uint adapterIdLow;
    public uint adapterIdHigh;
    public TARGET_MODE targetMode; // the union storage mapped to its largest documented member; interpreted only when infoType==2
  }
  public static class Native {
    [DllImport("user32.dll")] public static extern int GetDisplayConfigBufferSizes(uint flags, out uint numPathArrayElements, out uint numModeInfoArrayElements);
    [DllImport("user32.dll")] public static extern int QueryDisplayConfig(uint flags, ref uint numPathArrayElements, [In, Out] PATH_INFO[] pathArray, ref uint numModeInfoArrayElements, [In, Out] MODE_INFO[] modeInfoArray, IntPtr currentTopologyId);
    public static object Snapshot() {
      uint allocFlags = 2; // QDC_ONLY_ACTIVE_PATHS (the function page's flag table)
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
      // currentTopologyId must be NULL when flags is not QDC_DATABASE_CURRENT (the function page)
      int hrQuery = QueryDisplayConfig(allocFlags, ref nPath, paths, ref nMode, modes, IntPtr.Zero);
      doc["query_hr"] = hrQuery;
      doc["paths"] = nPath;
      doc["modes"] = nMode;
      if (hrQuery != 0) { return doc; }
      var modeByIndex = new Dictionary<uint, MODE_INFO>();
      for (uint i = 0; i < nMode; i++) { modeByIndex[i] = modes[i]; }
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
        // the join: path refresh rational vs the indexed target mode's vSync rational
        uint idx = t.modeInfoIdx;
        object joinObj;
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
          joinObj = mj;
        } else { joinObj = null; }
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
