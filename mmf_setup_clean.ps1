# MMF Core Ellys Simple Setup Script
# No complex syntax - just basic commands

Write-Host "MMF Core Ellys Setup Starting..." -ForegroundColor Green

# Create directories one by one
if (!(Test-Path "policies")) { New-Item -ItemType Directory -Name "policies" | Out-Null }
if (!(Test-Path "errors")) { New-Item -ItemType Directory -Name "errors" | Out-Null }
if (!(Test-Path "xp")) { New-Item -ItemType Directory -Name "xp" | Out-Null }
if (!(Test-Path "handshake")) { New-Item -ItemType Directory -Name "handshake" | Out-Null }
if (!(Test-Path "sentinel")) { New-Item -ItemType Directory -Name "sentinel" | Out-Null }
if (!(Test-Path "scripts")) { New-Item -ItemType Directory -Name "scripts" | Out-Null }
if (!(Test-Path "docs")) { New-Item -ItemType Directory -Name "docs" | Out-Null }

Write-Host "Directories created successfully" -ForegroundColor Yellow

# Create files one by one with simple content
if (!(Test-Path "README.md")) { 
    "# MMF Core Ellys" | Out-File "README.md" -Encoding UTF8 
}

if (!(Test-Path "policies\mmf_policy.json")) { 
    "{}" | Out-File "policies\mmf_policy.json" -Encoding UTF8 
}

if (!(Test-Path "errors\error_pool.json")) { 
    "[]" | Out-File "errors\error_pool.json" -Encoding UTF8 
}

if (!(Test-Path "xp\xp_table.json")) { 
    "{}" | Out-File "xp\xp_table.json" -Encoding UTF8 
}

if (!(Test-Path "handshake\handshake_status.json")) { 
    '{"status": "active"}' | Out-File "handshake\handshake_status.json" -Encoding UTF8 
}

if (!(Test-Path "sentinel\sentinel_rule.json")) { 
    "{}" | Out-File "sentinel\sentinel_rule.json" -Encoding UTF8 
}

Write-Host "Files created successfully" -ForegroundColor Cyan
Write-Host "MMF Core Ellys setup completed!" -ForegroundColor Green

# Show structure
Write-Host "Project structure:" -ForegroundColor Yellow
Get-ChildItem -Recurse -Name | Sort-Object