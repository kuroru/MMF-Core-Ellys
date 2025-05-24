[Console]::OutputEncoding = [System.Text.Encoding]::UTF8

param(
    [string]$project = "MWF-001"
)

$base = "projects\$project"
$files = @{
    "xp_log.json"        = "[]"
    "error_pool.json"    = "[]"
    "handshake_log.json" = "[]"
    "status.json"        = '{ "status": "active" }'
}

if ($files.Keys.Count -eq 0) {
    Write-Host "[Sentinel] 파일 목록이 비어 있습니다. 스크립트 종료" -ForegroundColor Red
    exit 1
}

if (!(Test-Path $base)) {
    New-Item -ItemType Directory -Path $base -Force | Out-Null
}

foreach ($key in $files.Keys) {
    $target = Join-Path $base $key
    if (!(Test-Path $target)) {
        Write-Host "[Sentinel] $target 파일이 없어 기본값으로 초기화" -ForegroundColor Yellow
        Set-Content $target $files[$key] -Encoding UTF8
    }
    else {
        $content = Get-Content $target -Raw
        if ($content.Length -lt 2 -or $content -match "NUL|�|\s*$|^\s*\]|^\s*\}") {
            Write-Host "[Sentinel] $target 손상 감지 - 기본값으로 복구" -ForegroundColor Red
            Set-Content $target $files[$key] -Encoding UTF8
        }
    }
}

Write-Host "[Sentinel] $base 초기화 완료" -ForegroundColor Green
exit 0
