

#Requires -Version 5.1
Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$Root = Split-Path -Parent $PSScriptRoot
Set-Location $Root

function Need-Cmd([string]$Name) {
    if (-not (Get-Command $Name -ErrorAction SilentlyContinue)) {
        throw "Missing command: $Name"
    }
}

Need-Cmd python
Need-Cmd git

$pyVersion = python -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')"
$major, $minor = $pyVersion.Split(".")
if ([int]$major -lt 3 -or ([int]$major -eq 3 -and [int]$minor -lt 11)) {
    throw "Need Python 3.11 or newer (found: $pyVersion)"
}

if (-not (Test-Path ".venv")) {
    python -m venv .venv
}

& .\.venv\Scripts\Activate.ps1
python -m pip install -U pip
pip install -r requirements.txt

$repos = @(
    @{
        Dir = "iotdb"
        Url = "https://anonymous.4open.science/r/iotdb-research-encoding-subcolumns"
    },
    @{
        Dir = "tsfile"
        Url = "https://anonymous.4open.science/r/tsfile-research-encoding-subcolumns"
    },
    @{
        Dir = "elf"
        Url = "https://github.com/Spatio-Temporal-Lab/elf.git"
        Branch = "dev"
    }
)

foreach ($repo in $repos) {
    $path = Join-Path $Root $repo.Dir
    if (Test-Path $path) {
        Write-Host "Directory $($repo.Dir)/ already exists; skip clone."
        continue
    }
    if ($repo.Branch) {
        git clone -b $repo.Branch --single-branch $repo.Url $path
    } else {
        git clone $repo.Url $path
    }
}

Write-Host ""
Write-Host "Python venv ready:  .\.venv\Scripts\Activate.ps1"
Write-Host "Repo root:          $Root"
Write-Host ""
Write-Host "Install JDK 17+ and Maven 3.6+ for Java benchmarks (README section 3.2)."
if (Get-Command java -ErrorAction SilentlyContinue) {
    java -version 2>&1 | Select-Object -First 1
} else {
    Write-Host "  java: not found"
}
if (Get-Command mvn -ErrorAction SilentlyContinue) {
    mvn -version | Select-Object -First 1
} else {
    Write-Host "  mvn:  not found"
}
