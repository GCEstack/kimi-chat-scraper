# Prompt to Find Credential Files

- Created: 2026-07-03T02:40:52Z
- Updated: 2026-07-06T11:51:41Z

---

## 🧑 You

I now need a prompt for kimi coed to go through all repos in my dekan ai user folder and dekstop and everywhere to find any credentials cred files for en vartoiables such as deepgram azure and have it review with me to make one var file

---

## 🤖 Kimi

Memory updated       Here's your Kimi Code prompt — copy-paste ready, no explanations needed:powershell   Copy # === KIMI CODE PROMPT: CREDENTIAL AUDIT & CONSOLIDATION ===
# Task: Scan all repos for scattered credentials/env files, review them with user, and create ONE master .env file

# --- CONFIG ---
$searchPaths = @(
    "$env:USERPROFILE\Desktop",
    "$env:USERPROFILE",
    "$env:USERPROFILE\Documents",
    "$env:USERPROFILE\source",
    "$env:USERPROFILE\repos"
)
$envFileName = ".env"
$masterEnvPath = "$env:USERPROFILE\master-credentials.env"
$reviewLogPath = "$env:USERPROFILE\credential-audit-log.md"

# --- STEP 1: DISCOVERY ---
# Find ALL .env, .env.local, .env.production, credentials.json, config.json, secrets.* files
$credentialFiles = @()
$patterns = @("*.env*", "credentials*", "secrets*", "config.json", "azure.json", "deepgram.json", "api-keys*")

foreach ($path in $searchPaths) {
    if (Test-Path $path) {
        foreach ($pattern in $patterns) {
            $found = Get-ChildItem -Path $path -Recurse -Filter $pattern -ErrorAction SilentlyContinue -Force
            $credentialFiles += $found
        }
    }
}

# Deduplicate and sort
$credentialFiles = $credentialFiles | Select-Object -Property FullName, LastWriteTime, Length -Unique | Sort-Object FullName

# --- STEP 2: EXTRACT & PARSE ---
$allSecrets = @()
foreach ($file in $credentialFiles) {
    $content = Get-Content -Path $file.FullName -Raw -ErrorAction SilentlyContinue
    $lines = $content -split "`n"
    
    foreach ($line in $lines) {
        # Match KEY=VALUE patterns (skip comments and empty lines)
        if ($line -match '^\s*([A-Za-z0-9_]+)\s*=\s*(.+)\s*$') {
            $key = $matches[1].Trim()
            $value = $matches[2].Trim().Trim('"').Trim("'")
            
            # Flag known credential patterns
            $isCredential = $key -match '(?i)(key|token|secret|password|api|azure|deepgram|openai|groq|anthropic|aws|gcp|firebase|supabase|mongo|postgres|db_|auth|jwt|webhook)'
            
            $allSecrets += [PSCustomObject]@{
                SourceFile = $file.FullName
                Key = $key
                Value = $value
                IsCredential = $isCredential
                IsPlaceholder = $value -match '(?i)(your_|placeholder|example|dummy|test|xxx|todo|change)'
                Line = $line.Trim()
            }
        }
    }
}

# --- STEP 3: GROUP BY KEY & DETECT CONFLICTS ---
$grouped = $allSecrets | Group-Object Key
$conflicts = $grouped | Where-Object { $_.Count -gt 1 -and ($_.Group | Select-Object Value -Unique).Count -gt 1 }

# --- STEP 4: GENERATE REVIEW LOG ---
$reviewLog = @"
# Credential Audit Log — $(Get-Date -Format "yyyy-MM-dd HH:mm")
## Files Scanned: $($credentialFiles.Count)
## Total Variables Found: $($allSecrets.Count)
## Conflicts Detected: $($conflicts.Count)

### Files Found:
$($credentialFiles | ForEach-Object { "- $($_.FullName)" } | Out-String)

### All Variables:
$($allSecrets | ForEach-Object { "| $($_.Key) | $($_.SourceFile) | $(if($_.IsCredential){'🔴'}else{'🟢'}) | $(if($_.IsPlaceholder){'⚠️ PLACEHOLDER'}else{'ACTIVE'}) |" } | Out-String)

### CONFLICTS (Same key, different values):
$($conflicts | ForEach-Object { 
    $key = $_.Name
    $vals = $_.Group | Select-Object Value, SourceFile -Unique
    "**$key** found in:`n$($vals | ForEach-Object { "- $($_.SourceFile): $($_.Value.Substring(0,[Math]::Min(20,$_.Value.Length)))..." } | Out-String)"
} | Out-String)

### REVIEW CHECKLIST:
- [ ] Verify each key is still needed
- [ ] Resolve conflicts (pick correct value)
- [ ] Mark placeholders for update
- [ ] Delete old .env files after migration
- [ ] Add .env to .gitignore in all repos
"@

$reviewLog | Out-File -FilePath $reviewLogPath -Encoding utf8

# --- STEP 5: BUILD MASTER ENV (DRY RUN - SHOW ONLY) ---
$masterEnv = @"
# Master Credentials File — Generated $(Get-Date -Format "yyyy-MM-dd")
# REVIEW REQUIRED: This is a DRY RUN. Uncomment Write-Host below to write file.
# Source: Consolidated from $($credentialFiles.Count) files
# 
# === AZURE ===
# DEEPGRAM ===
# OPENAI / ANTHROPIC / GROQ ===
# DATABASE / SUPABASE ===
# OTHER ===

"@

# Build unique keys (prefer non-placeholder values, flag conflicts)
$uniqueKeys = $allSecrets | Where-Object { -not $_.IsPlaceholder } | Group-Object Key | ForEach-Object {
    $best = $_.Group | Sort-Object { $_.IsPlaceholder } | Select-Object -First 1
    $comment = if ($_.Count -gt 1) { " # CONFLICT: $($_.Count) sources" } else { " # From: $(Split-Path $best.SourceFile -Leaf)" }
    "$($best.Key)=$($best.Value)$comment"
}

$masterEnv += ($uniqueKeys | Sort-Object) -join "`n"

# Show everything to user
Write-Host "`n=== FILES FOUND ($($credentialFiles.Count)) ===" -ForegroundColor Cyan
$credentialFiles | Format-Table FullName, LastWriteTime, Length -AutoSize

Write-Host "`n=== CONFLICTS ($($conflicts.Count)) ===" -ForegroundColor Red
$conflicts | ForEach-Object {
    Write-Host "`n$($_.Name) appears in $($_.Count) files with different values:" -ForegroundColor Yellow
    $_.Group | Select-Object SourceFile, Value -Unique | Format-Table -AutoSize
}

Write-Host "`n=== MASTER ENV PREVIEW (DRY RUN) ===" -ForegroundColor Green
Write-Host $masterEnv

Write-Host "`n=== PLACEHOLDERS DETECTED ===" -ForegroundColor Magenta
$allSecrets | Where-Object { $_.IsPlaceholder } | Format-Table Key, SourceFile -AutoSize

Write-Host "`n=== NEXT STEPS ===" -ForegroundColor Cyan
Write-Host "1. Review: $reviewLogPath"
Write-Host "2. Resolve conflicts above"
Write-Host "3. Uncomment the Out-File line below to write master env"
Write-Host "4. After verification, delete old .env files and add .env to .gitignore"

# --- STEP 6: WRITE MASTER ENV (UNCOMMENT AFTER REVIEW) ---
# $masterEnv | Out-File -FilePath $masterEnvPath -Encoding utf8
# Write-Host "Master env written to: $masterEnvPath" -ForegroundColor Green

# --- STEP 7: GITIGNORE CHECK ---
Write-Host "`n=== .GITIGNORE CHECK ===" -ForegroundColor Yellow
$gitignoreFiles = Get-ChildItem -Path $searchPaths -Recurse -Filter ".gitignore" -ErrorAction SilentlyContinue
foreach ($gitignore in $gitignoreFiles) {
    $content = Get-Content $gitignore.FullName -Raw
    if ($content -notmatch '\.env') {
        Write-Host "MISSING .env in: $($gitignore.FullName)" -ForegroundColor Red
    }
} What it does:Scans Desktop, user folder, Documents, source, repos for all .env*, credentials*, secrets*, config.json filesParses KEY=VALUE pairs and flags known credential patterns (Azure, Deepgram, OpenAI, DB, etc.)Detects conflicts — same key with different values across filesGenerates review log (credential-audit-log.md) with markdown table of everything foundShows master env preview (dry run) — doesn't write until you uncomment Step 6Checks .gitignore — flags repos missing .env so you don't leak credentials againAfter you run it:Review the conflicts in redOpen credential-audit-log.md in your editorPick the correct value for each conflicted keyUncomment the Out-File line in Step 6 to write the master fileThen delete the scattered old env files and add .env to .gitignore in every repoBAMMM. One source of truth. No more credential sprawl.                                                       Ask away. Pics work too.                       K2.6 Instant

---
