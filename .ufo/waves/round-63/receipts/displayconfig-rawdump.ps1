$ErrorActionPreference = 'Stop'
Add-Type -TypeDefinition @"
using System;
using System.Runtime.InteropServices;
namespace MadoDbg {
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
    public uint unionBits;
    public int scanLineOrdering;
  }
  [StructLayout(LayoutKind.Sequential)]
  public struct TARGET_MODE { public VIDEO_SIGNAL_INFO targetVideoSignalInfo; }
  [StructLayout(LayoutKind.Sequential)]
  public struct SOURCE_INFO { public uint a0; public uint a1; public uint id; public uint idx; public uint st; }
  [StructLayout(LayoutKind.Sequential)]
  public struct TARGET_INFO {
    public uint a0; public uint a1; public uint id; public uint idx;
    public int ot; public int rot; public int scal;
    public RATIONAL rr; public int slo; public int ta; public uint st;
  }
  [StructLayout(LayoutKind.Sequential)]
  public struct PATH_INFO { public SOURCE_INFO s; public TARGET_INFO t; public uint flags; }
  [StructLayout(LayoutKind.Sequential)]
  public struct MODE_INFO {
    public int infoType; public uint id; public uint a0; public uint a1;
    public TARGET_MODE targetMode;
  }
  public static class Native {
    [DllImport("user32.dll")] public static extern int GetDisplayConfigBufferSizes(uint flags, out uint nPath, out uint nMode);
    [DllImport("user32.dll")] public static extern int QueryDisplayConfig(uint flags, ref uint nPath, [In, Out] PATH_INFO[] pathArray, ref uint nMode, [In, Out] MODE_INFO[] modeInfoArray, IntPtr topology);
    public static string Raw() {
      uint f = 2, bp = 0, bm = 0;
      int hr = GetDisplayConfigBufferSizes(f, out bp, out bm);
      var sizes = "sizes: PATH_INFO=" + Marshal.SizeOf(typeof(PATH_INFO)) + " SOURCE=" + Marshal.SizeOf(typeof(SOURCE_INFO)) + " TARGET=" + Marshal.SizeOf(typeof(TARGET_INFO)) + " VIDEO=" + Marshal.SizeOf(typeof(VIDEO_SIGNAL_INFO)) + " TMODE=" + Marshal.SizeOf(typeof(TARGET_MODE)) + " MODEINFO=" + Marshal.SizeOf(typeof(MODE_INFO));
      var paths = new PATH_INFO[bp]; var modes = new MODE_INFO[bm];
      uint np = bp, nm = bm;
      int hr2 = QueryDisplayConfig(f, ref np, paths, ref nm, modes, IntPtr.Zero);
      var mi = modes[0];
      var bytes = new byte[Marshal.SizeOf(typeof(MODE_INFO))];
      IntPtr ptr = Marshal.AllocHGlobal(bytes.Length);
      Marshal.StructureToPtr(mi, ptr, false);
      Marshal.Copy(ptr, bytes, 0, bytes.Length);
      Marshal.FreeHGlobal(ptr);
      var hex = BitConverter.ToString(bytes);
      return sizes + "\nhr=" + hr + " hr2=" + hr2 + " np=" + np + " nm=" + nm + "\nmode0.infoType=" + mi.infoType + " id=" + mi.id + "\n" + hex;
    }
  }
}
"@
[MadoDbg.Native]::Raw()
