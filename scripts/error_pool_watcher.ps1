# scripts/error_pool_watcher.ps1
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8

$paths = @(
    "projects\MWF-001\error_pool.json",
    "projects\MWF-002\error_pool.json"
)

foreach ($path in $paths) {
    $dir = Split-Path $path
    if (!(Test-Path $dir)) {
        New-Item -ItemType Directory -Force -Path $dir | Out-Null
    }
    if (
        !(Test-Path $path) -or
        ((Get-Content $path -Raw).Length -lt 2) -or
        ((Get-Content $path -Raw) -match "NUL|�|^\s*$|^\s*\]|^\s*\}")
    ) {
        Write-Host "[Sentinel] $path 손상 감지 → 자동 복구" -ForegroundColor Yellow
        Set-Content $path "[]" -Encoding UTF8
    } else {
        Write-Host "[Sentinel] $path 정상" -ForegroundColor Green
    }
}

Write-Host "[Sentinel] 전체 error_pool.json 점검 완료" -ForegroundColor Cyan
exit 0
