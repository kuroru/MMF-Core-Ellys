# MMF Core Ellys - 오류 없는 설정 스크립트
# MMF Core Ellys - 오류 없는 설정 스크립트
# 한글 깨짐 방지 인코딩 설정
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
$OutputEncoding = [System.Text.Encoding]::UTF8
chcp 65001 | Out-Null

Write-Host "=== MMF Core Ellys 프로젝트 초기화 ===" -ForegroundColor Cyan

# 기본 파일 초기화 함수
function Initialize-MMFFile {
    param(
        [string]$FilePath,
        [string]$Content
    )
    
    try {
        if (!(Test-Path $FilePath)) {
            New-Item -ItemType File -Path $FilePath -Force | Out-Null
            Set-Content -Path $FilePath -Value $Content -Encoding UTF8
            Write-Host "✅ 생성: $FilePath" -ForegroundColor Green
        } else {
            Write-Host "⚠️  이미 존재: $FilePath" -ForegroundColor Yellow
        }
    } catch {
        Write-Host "❌ 오류: $FilePath - $($_.Exception.Message)" -ForegroundColor Red
    }
}

# 디렉토리 생성 함수
function New-MMFDirectory {
    param([string]$Path)
    
    if (!(Test-Path $Path)) {
        New-Item -ItemType Directory -Path $Path -Force | Out-Null
        Write-Host "📁 디렉토리 생성: $Path" -ForegroundColor Blue
    }
}

Write-Host "디렉토리 구조 생성 중..." -ForegroundColor Yellow

# 디렉토리들 생성
$directories = @(
    "policies",
    "errors", 
    "xp",
    "handshake",
    "sentinel", 
    "scripts",
    "docs",
    "docs\patch_notes",
    ".github",
    ".github\workflows"
)

foreach ($dir in $directories) {
    New-MMFDirectory -Path $dir
}

Write-Host "파일 초기화 중..." -ForegroundColor Yellow

# 파일들 초기화
Initialize-MMFFile -FilePath "README.md" -Content "# MMF Core Ellys Project"
Initialize-MMFFile -FilePath "policies\mmf_policy.json" -Content "{}"
Initialize-MMFFile -FilePath "errors\error_pool.json" -Content "[]"
Initialize-MMFFile -FilePath "errors\fail-log.md" -Content "# Fail Logs"
Initialize-MMFFile -FilePath "xp\xp_table.json" -Content "{}"
Initialize-MMFFile -FilePath "xp\rewards_catalog.yaml" -Content "---"
Initialize-MMFFile -FilePath "handshake\handshake_status.json" -Content '{"status": "active"}'
Initialize-MMFFile -FilePath "sentinel\sentinel_rule.json" -Content "{}"
Initialize-MMFFile -FilePath "sentinel\verify_block.md" -Content "# Verification Block"
Initialize-MMFFile -FilePath "scripts\mmf_auto_sync.py" -Content "# MMF Auto Sync Script"
Initialize-MMFFile -FilePath "docs\MMF_Ellys_MVF_Whitepaper.md" -Content "# MMF Ellys MVF Whitepaper"
Initialize-MMFFile -FilePath ".github\workflows\mmf_auto_ci.yml" -Content "# MMF Auto CI"

Write-Host "" 
Write-Host "🎉 MMF Core Ellys 프로젝트 초기화 완료!" -ForegroundColor Green
Write-Host "tree /f 명령으로 구조를 확인하세요." -ForegroundColor Cyan