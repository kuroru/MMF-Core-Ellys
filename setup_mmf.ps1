# setup_mmf.ps1 (루트 or scripts 폴더에 위치)
$root = $PSScriptRoot  # 스크립트 위치 기준

$folders = @("policies", "errors", "xp", "handshake", "sentinel", "scripts", "docs")
foreach ($f in $folders) {
    $target = Join-Path $root $f
    if (-not (Test-Path $target)) {
        New-Item -ItemType Directory -Path $target | Out-Null
    }
}

# 파일 생성 예시
$files = @{
    "policies\mmf_policy.json" = "{}"
    "errors\error_pool.json" = "{}"
    "xp\xp_table.json" = "{}"
    "handshake\handshake_status.json" = '{ "status": "active" }'
    "sentinel\sentinel_rule.json" = "{}"
    "README.md" = "# MMF Core Ellys Project"
}
foreach ($k in $files.Keys) {
    $targetFile = Join-Path $root $k
    if (-not (Test-Path $targetFile)) {
        $files[$k] | Out-File $targetFile -Encoding UTF8
    }
}
Write-Host "Project folders/files setup complete!" -ForegroundColor Green
