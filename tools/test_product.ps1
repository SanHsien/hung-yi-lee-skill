[CmdletBinding()]
param()

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$repoRoot = Split-Path -Parent $PSScriptRoot
Set-Location -LiteralPath $repoRoot

$venvPython = Join-Path $repoRoot ".venv\Scripts\python.exe"
if (Test-Path -LiteralPath $venvPython) {
    $pythonExe = $venvPython
} else {
    $pythonExe = (Get-Command python -ErrorAction Stop).Source
}

$env:PYTHONUTF8 = "1"
$env:PYTHONIOENCODING = "utf-8"

Write-Host "==> Run hung-yi-lee-skill product verification suite (Windows)"

Write-Host "--> 1. Health check (lint) without PYTHONUTF8"
$env:PYTHONUTF8 = $null
& $pythonExe scripts/hungyi_kb.py lint
if ($LASTEXITCODE -ne 0) {
    throw "scripts/hungyi_kb.py lint failed with exit code $LASTEXITCODE"
}

Write-Host "--> 2. Keyword search test (English)"
& $pythonExe scripts/hungyi_kb.py search "attention" --limit 3
if ($LASTEXITCODE -ne 0) {
    throw "scripts/hungyi_kb.py search failed with exit code $LASTEXITCODE"
}

Write-Host "--> 3. Simplified Chinese search test (Auto S2T alignment)"
& $pythonExe scripts/hungyi_kb.py search "语言模型" --limit 3
if ($LASTEXITCODE -ne 0) {
    throw "scripts/hungyi_kb.py search with Simplified Chinese failed with exit code $LASTEXITCODE"
}

Write-Host "--> 4. Knowledge graph query test (Traditional Chinese)"
& $pythonExe scripts/hungyi_kb.py graph query "什麼是 transformer"
if ($LASTEXITCODE -ne 0) {
    throw "scripts/hungyi_kb.py graph query failed with exit code $LASTEXITCODE"
}

Write-Host "--> 5. Knowledge graph query test (Simplified Chinese)"
& $pythonExe scripts/hungyi_kb.py graph query "什么是 transformer"
if ($LASTEXITCODE -ne 0) {
    throw "scripts/hungyi_kb.py graph query with Simplified Chinese failed with exit code $LASTEXITCODE"
}

Write-Host "PRODUCT TESTS GREEN"
