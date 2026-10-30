$ErrorActionPreference = 'Stop'
$demoRepo = Split-Path -Parent $PSScriptRoot
$demoVenvPython = Join-Path $demoRepo '.venv\Scripts\python.exe'
$demoPython = if (Test-Path -LiteralPath $demoVenvPython) { $demoVenvPython } else { (Get-Command python).Source }
try {
    $demoHealth = Invoke-RestMethod 'http://127.0.0.1:4397/health' -TimeoutSec 2
    if ($demoHealth.app -ne 'nids-demo') { throw 'Cổng 4397 đang được chương trình khác sử dụng.' }
} catch {
    $demoLog = Join-Path $env:TEMP 'tlcn_nids_demo_stdout.log'
    $demoErrorLog = Join-Path $env:TEMP 'tlcn_nids_demo_stderr.log'
    Start-Process -FilePath $demoPython -ArgumentList @('scripts/demo_server.py', '--port', '4397') -WorkingDirectory $demoRepo -WindowStyle Hidden -RedirectStandardOutput $demoLog -RedirectStandardError $demoErrorLog
    $demoReady = $false
    for ($demoAttempt = 0; $demoAttempt -lt 15; $demoAttempt++) {
        Start-Sleep -Milliseconds 500
        try { $demoReady = (Invoke-RestMethod 'http://127.0.0.1:4397/health' -TimeoutSec 1).app -eq 'nids-demo' } catch { }
        if ($demoReady) { break }
    }
    if (-not $demoReady) { throw "Chưa mở được demo. Xem log: $demoErrorLog" }
}
Start-Process 'http://127.0.0.1:4397/lab'
