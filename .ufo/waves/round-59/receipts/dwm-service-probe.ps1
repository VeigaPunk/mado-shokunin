# Round-59 D01 probe: the DWM service model on the live host, read-only.
# Queries only: registered services (WMI), one sc query of the Vista/7-era
# service name, the dwm.exe process census point-in-time, the services hosted
# by dwm.exe, and the composition flag. Starts nothing, changes nothing,
# prints no window titles, environment values or file contents.
$ErrorActionPreference = "Continue"

Write-Output ("OS " + (Get-CimInstance Win32_OperatingSystem | ForEach-Object { "$($_.Caption) $($_.Version) build $($_.BuildNumber)" }))

Write-Output "-- registered services matching name dwm/uxsms or display name 'Desktop Window' --"
$svc = Get-CimInstance Win32_Service | Where-Object { $_.Name -match 'dwm|uxsms' -or $_.DisplayName -match 'Desktop Window' }
if ($null -eq $svc) { Write-Output "SERVICES 0" }
else { $svc | ForEach-Object { Write-Output ("SERVICE name=" + $_.Name + " display=" + $_.DisplayName + " state=" + $_.State) } }

Write-Output "-- sc query UxSms (the Vista/7-era DWM session manager service name) --"
sc.exe query UxSms 2>&1 | ForEach-Object { Write-Output $_ }
Write-Output ("SC_UXSMS_RC=" + $LASTEXITCODE)

Write-Output "-- dwm.exe processes, point in time --"
$dwm = Get-Process dwm -ErrorAction SilentlyContinue
if ($null -eq $dwm) { Write-Output "DWMPROCS 0" }
else { $dwm | ForEach-Object { Write-Output ("DWMPROC name=" + $_.Name + " pid=" + $_.Id + " session=" + $_.SessionId) } }

Write-Output "-- services hosted by dwm.exe (tasklist /svc) --"
tasklist.exe /svc /fi "IMAGENAME eq dwm.exe" 2>&1 | ForEach-Object { Write-Output $_ }

Write-Output "-- composition flag (dwmapi!DwmIsCompositionEnabled) --"
Add-Type -TypeDefinition 'using System; using System.Runtime.InteropServices; public static class DwmQ59 { [DllImport("dwmapi.dll")] public static extern int DwmIsCompositionEnabled(out bool enabled); }' -ErrorAction SilentlyContinue
$enabled = $false
$hr = [DwmQ59]::DwmIsCompositionEnabled([ref]$enabled)
Write-Output ("DWM_COMPOSITION hr=" + $hr + " enabled=" + $enabled)
