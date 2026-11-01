# dpi-awareness-probe.ps1 - mado-shokunin round 60 receipt artifact (read-only).
#
# Measures, inside this one powershell.exe child process:
#   - the calling thread's DPI_AWARENESS via the documented getter chain
#     (GetThreadDpiAwarenessContext -> GetAwarenessFromDpiAwarenessContext);
#   - GetSystemMetrics(SM_CXSCREEN / SM_CYSCREEN) beside
#     GetSystemMetricsForDpi(SM_CXSCREEN / SM_CYSCREEN, 96);
#   - a main-window awareness histogram (Get-Process census where
#     MainWindowHandle -ne 0, then GetWindowDpiAwarenessContext ->
#     GetAwarenessFromDpiAwarenessContext per handle; histogram counts only);
#   - the foreground window's GetDpiForWindow and window awareness
#     (point-in-time foreground, never bound).
#
# Hard boundaries: prints key=value lines only; collects and prints no window
# titles, no process names, no window handles, no environment values, no file
# contents; writes no file; opens no socket; mutates nothing (every P/Invoke
# is a getter). Launched by the caller as:
#   powershell.exe -NoProfile -NonInteractive -NoLogo -ExecutionPolicy Bypass -File <this file>

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

"PROBE windpi-r60"
"thread.awareness=$awareness"
"metrics.cxscreen=$cx"
"metrics.cyscreen=$cy"
"metrics.cxscreen_dpi96=$cx96"
"metrics.cyscreen_dpi96=$cy96"
"windows.with_main=$($wins.Count)"
"windows.aware0=$($hist.a0)"
"windows.aware1=$($hist.a1)"
"windows.aware2=$($hist.a2)"
"windows.awareness_invalid=$($hist.invalid)"
"fg_window.present=$fgPresent"
"fg_window.dpi=$fgDpi"
"fg_window.awareness=$fgAware"
"WINDPI_PROBE: DONE"
