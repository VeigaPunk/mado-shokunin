$ErrorActionPreference = 'Stop'
# mado round-64 read-only probe: the D05 flip-condition flag matrix (CCD view).
# Getters only: GetDisplayConfigBufferSizes + QueryDisplayConfig, four documented
# flag shapes off the opened S424 page (QDC_ONLY_ACTIVE_PATHS 0x2 baseline;
# | QDC_VIRTUAL_MODE_AWARE 0x10, Windows 10+; | QDC_VIRTUAL_REFRESH_RATE_AWARE 0x40,
# Windows 11+; both). currentTopologyId NULL for every non-QDC_DATABASE_CURRENT call
# (the documented requirement). Counts and rationals only: no adapter ids, no target
# ids, no device names, no handles emitted. No Set* verb; nothing is written.
Add-Type -TypeDefinition @"
using System;
using System.Collections.Generic;
using System.Runtime.InteropServices;
namespace MadoQdcMatrix {
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
    public uint unionBits;        // the documented DUMMYUNIONNAME storage
    public int scanLineOrdering;  // DISPLAYCONFIG_SCANLINE_ORDERING, integer
  }
  [StructLayout(LayoutKind.Sequential)]
  public struct TARGET_MODE { public VIDEO_SIGNAL_INFO targetVideoSignalInfo; }
  [StructLayout(LayoutKind.Sequential)]
  public struct SOURCE_INFO {
    public uint adapterIdLow;   // documented LUID halves, carried for layout, never emitted
    public uint adapterIdHigh;
    public uint id;
    public uint modeInfoIdx;    // documented DUMMYUNIONNAME as its 32-bit storage
    public uint statusFlags;
  }
  [StructLayout(LayoutKind.Sequential)]
  public struct TARGET_INFO {
    public uint adapterIdLow;
    public uint adapterIdHigh;
    public uint id;
    public uint modeInfoIdx;
    public int outputTechnology; // enum integers only, never a name
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
  [StructLayout(LayoutKind.Sequential)]
  public struct MODE_INFO {
    public int infoType;         // SOURCE=1, TARGET=2, DESKTOP_IMAGE=3 (the opened S431 page)
    public uint id;
    public uint adapterIdLow;
    public uint adapterIdHigh;
    public TARGET_MODE targetMode; // union storage mapped to its largest documented member; read only when infoType==2
  }
  public static class Native {
    [DllImport("user32.dll")] public static extern int GetDisplayConfigBufferSizes(uint flags, out uint numPathArrayElements, out uint numModeInfoArrayElements);
    [DllImport("user32.dll")] public static extern int QueryDisplayConfig(uint flags, ref uint numPathArrayElements, [In, Out] PATH_INFO[] pathArray, ref uint numModeInfoArrayElements, [In, Out] MODE_INFO[] modeInfoArray, IntPtr currentTopologyId);
    static object Shape(uint allocFlags) {
      var doc = new Dictionary<string, object>();
      doc["qdc_flags"] = allocFlags;
      uint bufPath = 0, bufMode = 0;
      int hrBuf = GetDisplayConfigBufferSizes(allocFlags, out bufPath, out bufMode);
      doc["buffer_hr"] = hrBuf;
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
        pj["path_flags"] = p.flags;
        var t = p.targetInfo;
        var tj = new Dictionary<string, object>();
        tj["refresh_num"] = t.refreshRate.Numerator;
        tj["refresh_den"] = t.refreshRate.Denominator;
        tj["status_flags"] = t.statusFlags;
        tj["mode_info_idx"] = t.modeInfoIdx;
        pj["target"] = tj;
        uint idx = t.modeInfoIdx;
        if (idx < nMode && modes[idx].infoType == 2) {
          var tm = modes[idx].targetMode.targetVideoSignalInfo;
          var mj = new Dictionary<string, object>();
          mj["pixel_rate"] = (double)tm.pixelRate;
          mj["hsync_num"] = tm.hSyncFreq.Numerator;
          mj["hsync_den"] = tm.hSyncFreq.Denominator;
          mj["vsync_num"] = tm.vSyncFreq.Numerator;
          mj["vsync_den"] = tm.vSyncFreq.Denominator;
          mj["active_cx"] = tm.activeSize.cx;
          mj["active_cy"] = tm.activeSize.cy;
          mj["total_cx"] = tm.totalSize.cx;
          mj["total_cy"] = tm.totalSize.cy;
          mj["scanline_ordering"] = tm.scanLineOrdering;
          mj["join_agree"] = (tm.vSyncFreq.Numerator == t.refreshRate.Numerator && tm.vSyncFreq.Denominator == t.refreshRate.Denominator);
          pj["target_mode"] = mj;
        } else {
          pj["target_mode"] = null;
        }
        pathList.Add(pj);
      }
      var modeTypes = new List<int>();
      for (uint i = 0; i < nMode; i++) { modeTypes.Add(modes[i].infoType); }
      doc["mode_info_types"] = modeTypes;
      doc["path_list"] = pathList;
      return doc;
    }
    public static List<object> Matrix() {
      // the four documented shapes: baseline QDC_ONLY_ACTIVE_PATHS (0x2), then the
      // two virtual flags the opened S424 page documents (0x10 Windows 10+,
      // 0x40 Windows 11+), alone and together.
      uint[] shapes = new uint[] { 0x2u, 0x12u, 0x42u, 0x52u };
      var outList = new List<object>();
      foreach (var f in shapes) { outList.Add(Shape(f)); }
      return outList;
    }
  }
}
"@
[MadoQdcMatrix.Native]::Matrix() | ConvertTo-Json -Depth 8 -Compress
