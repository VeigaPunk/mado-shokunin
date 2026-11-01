$ErrorActionPreference = 'Stop'
# mado round-61 display-topology probe (read-only; committed receipt artifact).
# Topology half: the MANAGED System.Windows.Forms.Screen layer (independent of
# the round's tool, which enumerates through the native EnumDisplayMonitors
# path). Mode half: one P/Invoke family, EnumDisplaySettingsW, in its three
# documented iModeNum shapes (-1 current, -2 registry, 0..N index series).
Add-Type -AssemblyName System.Windows.Forms | Out-Null
Add-Type -TypeDefinition @"
using System;
using System.Runtime.InteropServices;
namespace MadoDisplayProbe {
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
    [DllImport("user32.dll", CharSet = CharSet.Unicode)]
    public static extern bool EnumDisplaySettingsW(string deviceName, int modeNum, ref DEVMODEW devMode);
    public static DEVMODEW Fresh() {
      DEVMODEW dm = new DEVMODEW();
      dm.dmSize = (ushort)Marshal.SizeOf(typeof(DEVMODEW));
      dm.dmDriverExtra = 0;
      return dm;
    }
  }
}
"@
$screens = @([System.Windows.Forms.Screen]::AllScreens)
$monitors = @()
foreach ($s in $screens) {
  $dmCur = [MadoDisplayProbe.Native]::Fresh()
  $curOk = [MadoDisplayProbe.Native]::EnumDisplaySettingsW($s.DeviceName, -1, [ref]$dmCur)
  $dmReg = [MadoDisplayProbe.Native]::Fresh()
  $regOk = [MadoDisplayProbe.Native]::EnumDisplaySettingsW($s.DeviceName, -2, [ref]$dmReg)
  $count = 0
  for ($i = 0; $i -lt 256; $i++) {
    $dmIdx = [MadoDisplayProbe.Native]::Fresh()
    if (-not [MadoDisplayProbe.Native]::EnumDisplaySettingsW($s.DeviceName, $i, [ref]$dmIdx)) { break }
    $count++
  }
  $cur = $null; $reg = $null
  if ($curOk) {
    $cur = [ordered]@{ ok = $true; w = $dmCur.dmPelsWidth; h = $dmCur.dmPelsHeight;
                       freq = $dmCur.dmDisplayFrequency; bpp = $dmCur.dmBitsPerPel;
                       pos_x = $dmCur.dmPositionX; pos_y = $dmCur.dmPositionY }
  } else { $cur = [ordered]@{ ok = $false } }
  if ($regOk) {
    $reg = [ordered]@{ ok = $true; w = $dmReg.dmPelsWidth; h = $dmReg.dmPelsHeight;
                       freq = $dmReg.dmDisplayFrequency; bpp = $dmReg.dmBitsPerPel }
  } else { $reg = [ordered]@{ ok = $false } }
  $monitors += [ordered]@{
    device  = $s.DeviceName
    primary = [bool]$s.Primary
    bounds  = [ordered]@{ x = $s.Bounds.X; y = $s.Bounds.Y; w = $s.Bounds.Width; h = $s.Bounds.Height }
    work    = [ordered]@{ x = $s.WorkingArea.X; y = $s.WorkingArea.Y; w = $s.WorkingArea.Width; h = $s.WorkingArea.Height }
    mode_current  = $cur
    mode_registry = $reg
    mode_list_count = $count
  }
}
[ordered]@{
  monitor_count = $screens.Count
  monitors = $monitors
} | ConvertTo-Json -Depth 6 -Compress
