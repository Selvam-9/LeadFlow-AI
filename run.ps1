$ErrorActionPreference = "Stop"

$venvPython = Join-Path $PSScriptRoot ".venv\Scripts\python.exe"
if (-not (Test-Path -LiteralPath $venvPython)) {
    throw "Project environment not found. Run .\setup.ps1 first."
}

Push-Location $PSScriptRoot
try {
    & $venvPython -m uvicorn app.main:app --reload --reload-dir app @args
    if ($LASTEXITCODE -ne 0) {
        throw "Uvicorn exited with code $LASTEXITCODE."
    }
}
finally {
    Pop-Location
}
