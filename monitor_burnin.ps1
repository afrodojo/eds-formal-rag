# ==============================================================================
#   48-HOUR BURN-IN WATCHDOG & METRIC LOGGER
#   Principal Investigator: Asaad Morman (Bowie State University)
#   Target Script: run_48hr_burnin.py
# ==============================================================================

$TargetScript = "run_48hr_burnin.py"
$LogDir       = "test_results"
$WatchdogLog  = "$LogDir/watchdog_telemetry.log"

if (-not (Test-Path $LogDir)) {
    New-Item -ItemType Directory -Path $LogDir -Force | Out-Null
}

function Write-WatchdogLog {
    param ([string]$Message, [string]$Level = "INFO")
    $Timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    $Formatted = "$Timestamp [$Level] $Message"
    Write-Host $Formatted -ForegroundColor $(if ($Level -eq "ERROR") { "Red" } elseif ($Level -eq "WARN") { "Yellow" } else { "Green" })
    Add-Content -Path $WatchdogLog -Value $Formatted -Encoding UTF8
}

Write-WatchdogLog "Starting 48-Hour Burn-In Watchdog Service..." "INFO"

# Hourly loop (3600 seconds interval, checking process state every 30 seconds)
$CheckIntervalSeconds = 30
$HourlyCounter = 0

while ($true) {
    # 1. Check if run_48hr_burnin.py is currently running
    $PythonProc = Get-CimInstance Win32_Process -Filter "Name = 'python.exe' or Name = 'pythonw.exe'" | 
                  Where-Object { $_.CommandLine -like "*$TargetScript*" }

    if (-not $PythonProc) {
        Write-WatchdogLog "Target process '$TargetScript' not detected! Attempting auto-restart..." "WARN"
        
        # Auto-restart the background process
        Start-Process python -ArgumentList $TargetScript -WindowStyle Hidden
        Start-Sleep -Seconds 5

        # Re-check process after restart attempt
        $PythonProc = Get-CimInstance Win32_Process -Filter "Name = 'python.exe' or Name = 'pythonw.exe'" | 
                      Where-Object { $_.CommandLine -like "*$TargetScript*" }

        if ($PythonProc) {
            Write-WatchdogLog "Successfully restarted '$TargetScript' (PID: $($PythonProc.ProcessId))." "INFO"
        } else {
            Write-WatchdogLog "CRITICAL: Failed to restart '$TargetScript'." "ERROR"
        }
    }

    # 2. Hourly Metrics Log (every 120 iterations * 30 seconds = 3600 seconds)
    if ($HourlyCounter % 120 -eq 0 -and $PythonProc) {
        $PidVal     = $PythonProc.ProcessId
        $ProcObj    = Get-Process -Id $PidVal -ErrorAction SilentlyContinue
        
        if ($ProcObj) {
            $RamMB      = [math]::Round($ProcObj.WorkingSet64 / 1MB, 2)
            $SysRamPct  = [math]::Round((Get-CimInstance Win32_OperatingSystem | ForEach-Object { ($_.TotalVisibleMemorySize - $_.FreePhysicalMemory) / $_.TotalVisibleMemorySize * 100 }), 2)
            $CpuTotal   = [math]::Round((Get-Counter '\Processor(_Total)\% Processor Time').CounterSamples.CookedValue, 2)

            $MetricMsg = "HOURLY METRICS | PID: $PidVal | Process RAM: $RamMB MB | System RAM: $SysRamPct% | Overall CPU: $CpuTotal%"
            Write-WatchdogLog $MetricMsg "INFO"
        }
    }

    Start-Sleep -Seconds $CheckIntervalSeconds
    $HourlyCounter++
}
