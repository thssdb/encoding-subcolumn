



param(
    [Parameter(Mandatory = $true)]
    [string]$Test
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$Root = Split-Path -Parent $PSScriptRoot
$IotdbDir = Join-Path $Root "iotdb"

if (-not (Test-Path $IotdbDir)) {
    throw "Missing iotdb checkout at $IotdbDir (run .\scripts\bootstrap_env.ps1 first)."
}

Push-Location $IotdbDir
try {
    mvn test -pl iotdb-core/tsfile `
        "-Dtest=$Test" `
        "-Dcheckstyle.skip=true" `
        "-Dmaven.checkstyle.skip=true" `
        "-Dspotless.check.skip=true"
} finally {
    Pop-Location
}
