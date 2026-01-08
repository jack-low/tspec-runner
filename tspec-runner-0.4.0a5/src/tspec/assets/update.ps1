param(
  [Parameter(Mandatory=$false)]
  [string]$ZipPath,

  [Parameter(Mandatory=$false)]
  [string]$RepoDir = ".",

  [Parameter(Mandatory=$false)]
  [string]$Branch,

  [Parameter(Mandatory=$false)]
  [string]$Tag,

  [Parameter(Mandatory=$false)]
  [string]$CommitMessage
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

function Fail([string]$msg) {
  Write-Host "ERROR: $msg" -ForegroundColor Red
  exit 1
}

function LatestZipFromDownloads() {
  $dl = Join-Path $HOME "Downloads"
  if (-not (Test-Path $dl)) { return $null }
  $z = Get-ChildItem -Path $dl -Filter "tspec-runner-*.zip" | Sort-Object LastWriteTime -Descending | Select-Object -First 1
  if ($null -eq $z) { return $null }
  return $z.FullName
}

function GuessVersionFromFilename([string]$path) {
  $name = [System.IO.Path]::GetFileName($path)
  if ($name -match "tspec-runner-([0-9A-Za-z\.\-]+)\.zip") { return $Matches[1] }
  return $null
}

# Resolve repo dir
$repo = Resolve-Path -Path $RepoDir
Push-Location $repo

try {
  if (-not (Test-Path ".git")) { Fail "not a git repository: $repo (run git init first)" }

  if ([string]::IsNullOrWhiteSpace($ZipPath)) {
    $ZipPath = LatestZipFromDownloads
    if ([string]::IsNullOrWhiteSpace($ZipPath)) { Fail "ZipPath not specified and no tspec-runner-*.zip found in Downloads" }
  }
  $ZipPath = Resolve-Path -Path $ZipPath

  if (-not (Test-Path $ZipPath)) { Fail "zip not found: $ZipPath" }

  $ver = GuessVersionFromFilename $ZipPath
  if ([string]::IsNullOrWhiteSpace($ver)) { $ver = "unknown" }

  if ([string]::IsNullOrWhiteSpace($Tag)) {
    if ($ver -ne "unknown") { $Tag = "v$ver" } else { $Tag = "vupdate" }
  }
  if ([string]::IsNullOrWhiteSpace($Branch)) {
    $Branch = "upgrade/$Tag"
  }
  if ([string]::IsNullOrWhiteSpace($CommitMessage)) {
    $CommitMessage = "upgrade: apply $Tag"
  }

  Write-Host "Repo:   $repo"
  Write-Host "Zip:    $ZipPath"
  Write-Host "Branch: $Branch"
  Write-Host "Tag:    $Tag"

  git switch -c $Branch

  Expand-Archive -Force -Path $ZipPath -DestinationPath "."

  git add -A
  git commit -m $CommitMessage
  git tag $Tag

  Write-Host "Done. Now run:" -ForegroundColor Green
  Write-Host "  uv pip install -e `".\[dev]`""
}
finally {
  Pop-Location
}
