# mado round-58 probe: per-monitor DPI join (read-only)
# Read-only API surface: MonitorFromPoint (user32), GetDpiForMonitor (Shcore, three
# MDT types), GetForegroundWindow + GetDpiForWindow (user32). No setting is changed;
# the only process affected is this throwaway PowerShell child itself.
$ErrorActionPreference = 'Stop'
$src = @'
using System;
using System.Runtime.InteropServices;
public static class DpiProbe {
  [StructLayout(LayoutKind.Sequential)]
  public struct POINT { public int X; public int Y; }
  [DllImport("user32.dll")]
  public static extern IntPtr MonitorFromPoint(POINT pt, uint dwFlags);
  [DllImport("Shcore.dll")]
  public static extern int GetDpiForMonitor(IntPtr hmonitor, int dpiType, ref uint dpiX, ref uint dpiY);
  [DllImport("user32.dll")]
  public static extern uint GetDpiForWindow(IntPtr hwnd);
  [DllImport("user32.dll")]
  public static extern IntPtr GetForegroundWindow();
}
'@
Add-Type -TypeDefinition $src
Add-Type -AssemblyName System.Windows.Forms
$screens = [System.Windows.Forms.Screen]::AllScreens | ForEach-Object {
  [pscustomobject]@{ device_name = $_.DeviceName; primary = $_.Primary;
                     bounds = $_.Bounds.ToString(); bpp = $_.BitsPerPixel }
}
# MONITOR_DEFAULTTONEAREST = 2 against point (0,0)
$pt = New-Object DpiProbe+POINT
$pt.X = 0; $pt.Y = 0
$hmon = [DpiProbe]::MonitorFromPoint($pt, 2)
$ex=0;$ey=0;$rx=0;$ry=0;$ax=0;$ay=0
$he=[DpiProbe]::GetDpiForMonitor($hmon,0,[ref]$ex,[ref]$ey)   # MDT_EFFECTIVE_DPI (0)
$ha=[DpiProbe]::GetDpiForMonitor($hmon,1,[ref]$ax,[ref]$ay)   # MDT_ANGULAR_DPI  (1)
$hr=[DpiProbe]::GetDpiForMonitor($hmon,2,[ref]$rx,[ref]$ry)   # MDT_RAW_DPI      (2)
$fg = [DpiProbe]::GetForegroundWindow()
$fdpi = 0
$have_fg = ($fg -ne [IntPtr]::Zero)
if ($have_fg) { $fdpi = [DpiProbe]::GetDpiForWindow($fg) }
[pscustomobject]@{
  screens       = $screens
  hmonitor      = $hmon.ToString()
  mdt_effective = [pscustomobject]@{ dpi = $ex; hr = $he }
  mdt_angular   = [pscustomobject]@{ dpi = $ax; hr = $ha }
  mdt_raw       = [pscustomobject]@{ dpi = $rx; hr = $hr }
  fg_window     = [pscustomobject]@{ present = $have_fg; dpi = $fdpi }
} | ConvertTo-Json -Depth 4
