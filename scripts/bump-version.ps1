param([string]$Notes = "update")
# Sync version.json / sw.js BUILD_VERSION / index.html APP_VERSION (write UTF-8 no BOM)
$ErrorActionPreference = "Stop"
$root = Split-Path -Parent $PSScriptRoot
$enc  = New-Object System.Text.UTF8Encoding($false)
$today = Get-Date -Format "yyyy.MM.dd"
$vp = Join-Path $root "version.json"; $seq = 1
if (Test-Path $vp) {
  $raw = [System.IO.File]::ReadAllText($vp, [System.Text.Encoding]::UTF8)  # 必用 UTF-8 讀，否則中文 notes 讀壞 JSON
  $old = ($raw | ConvertFrom-Json).version
  if ($old -match "^$([regex]::Escape($today))-(\d+)$") { $seq=[int]$Matches[1]+1 }
}
$ver = "$today-$seq"
[System.IO.File]::WriteAllText($vp, ([ordered]@{version=$ver;notes=$Notes}|ConvertTo-Json), $enc)
foreach ($f in @(@("sw.js","const BUILD_VERSION = '[^']*';","const BUILD_VERSION = '$ver';"),
                 @("index.html","var APP_VERSION='[^']*';","var APP_VERSION='$ver';"))) {
  $p = Join-Path $root $f[0]; $t = [System.IO.File]::ReadAllText($p,[System.Text.Encoding]::UTF8)
  [System.IO.File]::WriteAllText($p, [regex]::Replace($t,$f[1],$f[2]), $enc)
}
Write-Host "bumped -> $ver  (next: git add -A; git commit; git push)"
