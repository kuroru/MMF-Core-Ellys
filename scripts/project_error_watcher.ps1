$proj = "projects/MMF-001/error_pool.json"
while ($true) {
  if (!(Test-Path $proj) -or ((Get-Content $proj -Raw).Length -lt 2)) {
    Write-Host "[Sentinel] 프로젝트 에러풀 손상 감지→자동 복구" -ForegroundColor Yellow
    Set-Content $proj "[]" -Encoding UTF8
  }
  Start-Sleep -Seconds 15
}
