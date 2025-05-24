# scripts/error_pool_watcher.ps1
$path = "errors\error_pool.json"

# 파일 미존재, 1KB 미만(비정상), 손상 패턴(NUL, 깨짐 등) 복구
if (
    !(Test-Path $path) -or
    ((Get-Content $path -Raw).Length -lt 2) -or
    ((Get-Content $path -Raw) -match "NUL|�|^\s*$|^\s*\]|^\s*\}")
) {
    Write-Host "[Sentinel] error_pool.json 손상 감지 → 자동 복구" -ForegroundColor Red
    Set-Content $path "[]" -Encoding UTF8
    # ★ 필요시 백업 복구 기능: 주석 해제해서 사용
    # if (Test-Path "$path.bak") { Copy-Item "$path.bak" $path -Force }
}
