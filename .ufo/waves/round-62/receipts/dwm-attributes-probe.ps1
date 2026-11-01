$ErrorActionPreference = 'Stop'
# mado round-62 read-only probe: DWM client-attribute plane.
# Getters only: DwmIsCompositionEnabled, DwmGetWindowAttribute (CLOAKED=14,
# EXTENDED_FRAME_BOUNDS=9), DwmGetCompositionTimingInfo (hwnd NULL — the
# documented Windows 8.1+ requirement), EnumWindows + IsWindowVisible +
# IsWindow, GetWindowRect, GetConsoleWindow, GetForegroundWindow (fallback).
# Counts only: no titles, no handles emitted, no process names, no registry.
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
      // Windows 8.1+ ("If this parameter is not set to NULL,
      // DwmGetCompositionTimingInfo returns E_INVALIDARG"). E_INVALIDARG =
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
