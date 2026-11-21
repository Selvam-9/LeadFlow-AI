$ErrorActionPreference = "Stop"

$projectRoot = $PSScriptRoot
$venvPython = Join-Path $projectRoot ".venv\Scripts\python.exe"
$requirements = Join-Path $projectRoot "requirements.txt"
$uv = Get-Command uv -ErrorAction SilentlyContinue

if ($uv) {
    & uv --system-certs python install 3.12
    if ($LASTEXITCODE -ne 0) {
        throw "Failed to install Python 3.12 with uv."
    }

    if (-not (Test-Path -LiteralPath $venvPython)) {
        & uv --system-certs venv (Join-Path $projectRoot ".venv") --python 3.12
        if ($LASTEXITCODE -ne 0) {
            throw "Failed to create the project virtual environment."
        }
    }

    & uv --system-certs pip install --python $venvPython -r $requirements
    if ($LASTEXITCODE -ne 0) {
        throw "Failed to install project dependencies."
    }

    Write-Host "Dependencies installed. Start the API with .\run.ps1"
    return
}

$python = Get-Command py, python -ErrorAction SilentlyContinue |
    Where-Object { $_.Source -notlike "*\Microsoft\WindowsApps\*" } |
    Select-Object -First 1

if (-not $python) {
    throw "Python and uv were not found. Install Python from python.org or install uv, then run this script again."
}

& $python.Source -m venv (Join-Path $projectRoot ".venv")
if ($LASTEXITCODE -ne 0) {
    throw "Failed to create the project virtual environment."
}

& $venvPython -m pip install -r $requirements
if ($LASTEXITCODE -ne 0) {
    throw "Failed to install project dependencies."
}

Write-Host "Dependencies installed. Start the API with .\run.ps1"
