# publish.ps1
# Publishes the github/ folder as a public repository on GitHub.
# Requires git, optionally the GitHub CLI (gh).
#
# Reads forbidden terms from a local-only file `.publish-blocklist`.
# That file is in .gitignore and never reaches GitHub.
#
# Usage:
#   .\publish.ps1                  # full publish
#   .\publish.ps1 -CheckOnly       # run only the blocklist scan, no commit/push

[CmdletBinding()]
param(
    [switch]$CheckOnly
)

$ErrorActionPreference = "Stop"
$repoName = "godstruegospel"
$description = "A concordant Bible-study skill grounded in Hebrew, Aramaic and Greek source text. Sola scriptura."

Write-Host "==> Verifying we are in the github/ folder..." -ForegroundColor Cyan
if (-not (Test-Path "README.md") -or -not (Test-Path "LICENSE") -or -not (Test-Path "claude-skill/Kennis")) {
    Write-Error "This script must be run from the github/ folder. Required files (README.md, LICENSE, claude-skill/Kennis/) are missing."
    exit 1
}

Write-Host "==> Loading blocklist from .publish-blocklist..." -ForegroundColor Cyan
if (-not (Test-Path ".publish-blocklist")) {
    Write-Warning "No .publish-blocklist file found. Skipping blocklist scan."
    Write-Host "   To enable the scan, create .publish-blocklist with one forbidden term per line."
    $patterns = @()
} else {
    $patterns = Get-Content ".publish-blocklist" |
                Where-Object { $_ -and -not $_.Trim().StartsWith('#') } |
                ForEach-Object { $_.Trim() } |
                Where-Object { $_ }
}

if ($patterns.Count -gt 0) {
    Write-Host "==> Scanning $($patterns.Count) blocklist term(s) across all text files..." -ForegroundColor Cyan
    $failed = $false
    $exclude = @(".publish-blocklist", "publish.ps1", "PUBLISH-TO-GITHUB.md")
    foreach ($p in $patterns) {
        $hits = Get-ChildItem -Recurse -Include *.md, *.py, *.json, *.jsonl, *.txt -ErrorAction SilentlyContinue |
                Where-Object { $exclude -notcontains $_.Name } |
                Select-String -Pattern ([regex]::Escape($p)) -CaseSensitive:$false -ErrorAction SilentlyContinue
        $count = ($hits | Measure-Object).Count
        $line = "{0,-40} {1}" -f $p, $count
        if ($count -gt 0) {
            Write-Host "   $line" -ForegroundColor Red
            $failed = $true
            $hits | Select-Object -First 3 | ForEach-Object {
                Write-Host "     -> $($_.Path):$($_.LineNumber)" -ForegroundColor DarkRed
            }
        } else {
            Write-Host "   $line" -ForegroundColor Green
        }
    }
    if ($failed) {
        Write-Error "Blocklist scan failed. One or more forbidden terms were found. Aborting."
        exit 1
    }
    Write-Host "==> Blocklist scan passed." -ForegroundColor Green
}

if ($CheckOnly) {
    Write-Host "==> CheckOnly mode: skipping commit and push." -ForegroundColor Yellow
    exit 0
}

Write-Host "==> Initializing git..." -ForegroundColor Cyan
if (-not (Test-Path ".git")) {
    git init -b main | Out-Null
}

Write-Host "==> Staging files..." -ForegroundColor Cyan
git add .

Write-Host "==> Creating commit..." -ForegroundColor Cyan
$status = git status --porcelain
if ($status) {
    git commit -m "Initial public release: godstruegospel concordant Bible-study skill" | Out-Null
} else {
    Write-Host "   Nothing to commit."
}

$useGhCli = $false
try {
    & gh --version 2>&1 | Out-Null
    if ($LASTEXITCODE -eq 0) { $useGhCli = $true }
} catch {
    $useGhCli = $false
}

if ($useGhCli) {
    Write-Host "==> Using GitHub CLI to create repository and push..." -ForegroundColor Cyan
    gh repo create $repoName --public --source=. --remote=origin --push --description $description
    Write-Host "==> Done. Repository created and pushed." -ForegroundColor Green
} else {
    Write-Host "==> GitHub CLI not found. Manual steps follow." -ForegroundColor Yellow
    Write-Host ""
    Write-Host "   Create an empty repository at https://github.com/new"
    Write-Host "     Repository name: $repoName"
    Write-Host "     Visibility:      Public"
    Write-Host "     Do NOT initialize with README, LICENSE, or .gitignore."
    Write-Host ""
    Write-Host "   Then run:"
    Write-Host "     git remote add origin https://github.com/<your-username>/$repoName.git"
    Write-Host "     git push -u origin main"
    Write-Host ""
    Write-Host "   For SSH instead of HTTPS:"
    Write-Host "     git remote add origin git@github.com:<your-username>/$repoName.git"
    Write-Host "     git push -u origin main"
}
