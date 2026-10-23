# PowerShell Repo Scan

- Created: 2026-07-03T02:42:28Z
- Updated: 2026-07-03T02:42:28Z

---

## 🧑 You

can u create a kimi code powershell prompt to search my whole computer for all repos local and any folders that are named the same or simliar and give a full audit on how many there are if they have reme and how many can et archived vs combined an dupdated as of 1 month

---

## 🤖 Kimi

I can create a comprehensive Kimi Code PowerShell prompt for you. This will audit all local repositories, detect duplicates/similar names, check remotes, and categorize them by action (archive, combine, update).Here's the complete prompt:KIMI CODE POWERSHELL — FULL REPO AUDIT & DEDUPLICATION ENGINECopy-paste this into Kimi Code:powershell   Copy # ============================================
# KIMI CODE: FULL REPO AUDIT & DEDUPLICATION ENGINE
# ============================================
# Run: kimi-code powershell -f repo-audit.ps1
# Or paste into Kimi Code terminal

# CONFIGURATION
$AuditDate = Get-Date -Format "yyyy-MM-dd_HH-mm"
$OutputPath = "$env:USERPROFILE\Desktop\RepoAudit_$AuditDate"
$OneMonthAgo = (Get-Date).AddMonths(-1)

# Create output directory
New-Item -ItemType Directory -Path $OutputPath -Force | Out-Null

# ============================================
# PHASE 1: DISCOVER ALL REPOS
# ============================================
Write-Host "`n🔍 PHASE 1: Scanning entire system for Git repositories..." -ForegroundColor Cyan

$RepoLocations = @(
    "$env:USERPROFILE\Desktop",
    "$env:USERPROFILE\Documents",
    "$env:USERPROFILE\Projects",
    "$env:USERPROFILE\source",
    "$env:USERPROFILE\repos",
    "$env:USERPROFILE\github",
    "$env:USERPROFILE\git",
    "C:\Projects",
    "C:\Repos",
    "C:\Dev",
    "C:\Code"
)

$AllRepos = @()
foreach ($location in $RepoLocations) {
    if (Test-Path $location) {
        $repos = Get-ChildItem -Path $location -Recurse -Depth 3 -Filter ".git" -Directory -ErrorAction SilentlyContinue
        foreach ($repo in $repos) {
            $repoPath = $repo.Parent.FullName
            $repoName = $repo.Parent.Name
            
            # Get last modified date
            $lastModified = (Get-Item $repoPath).LastWriteTime
            
            # Check for remote
            $remote = $null
            try {
                $remote = git -C $repoPath remote -v 2>$null | Select-Object -First 1
                if ($remote) {
                    $remote = ($remote -split '\s+')[1]
                }
            } catch {}
            
            # Check if dirty/uncommitted
            $status = "clean"
            try {
                $gitStatus = git -C $repoPath status --porcelain 2>$null
                if ($gitStatus) { $status = "dirty" }
            } catch {}
            
            # Get branch count
            $branches = 0
            try {
                $branches = (git -C $repoPath branch -a 2>$null).Count
            } catch {}
            
            $AllRepos += [PSCustomObject]@{
                Name = $repoName
                FullPath = $repoPath
                ParentFolder = $repo.Parent.Parent.FullName
                LastModified = $lastModified
                IsRecent = $lastModified -gt $OneMonthAgo
                HasRemote = [bool]$remote
                RemoteUrl = $remote
                GitStatus = $status
                BranchCount = $branches
                SizeMB = [math]::Round((Get-ChildItem $repoPath -Recurse -ErrorAction SilentlyContinue | Measure-Object -Property Length -Sum).Sum / 1MB, 2)
            }
        }
    }
}

# Also scan entire C: drive for .git folders (deep scan)
Write-Host "🌐 Running deep scan of C: drive for any missed repos..." -ForegroundColor Yellow
$DeepRepos = Get-ChildItem -Path C:\ -Recurse -Depth 4 -Filter ".git" -Directory -ErrorAction SilentlyContinue | 
    Where-Object { $_.FullName -notlike "*node_modules*" -and $_.FullName -notlike "*/.*" } |
    ForEach-Object {
        $repoPath = $_.Parent.FullName
        $repoName = $_.Parent.Name
        $lastModified = (Get-Item $repoPath).LastWriteTime
        
        $remote = $null
        try {
            $remote = git -C $repoPath remote -v 2>$null | Select-Object -First 1
            if ($remote) { $remote = ($remote -split '\s+')[1] }
        } catch {}
        
        [PSCustomObject]@{
            Name = $repoName
            FullPath = $repoPath
            ParentFolder = $_.Parent.Parent.FullName
            LastModified = $lastModified
            IsRecent = $lastModified -gt $OneMonthAgo
            HasRemote = [bool]$remote
            RemoteUrl = $remote
            GitStatus = "unknown"
            BranchCount = 0
            SizeMB = [math]::Round((Get-ChildItem $repoPath -Recurse -ErrorAction SilentlyContinue | Measure-Object -Property Length -Sum).Sum / 1MB, 2)
        }
    }

$AllRepos = ($AllRepos + $DeepRepos) | Sort-Object FullPath -Unique

# Export full inventory
$AllRepos | Export-Csv "$OutputPath\1-FULL-INVENTORY.csv" -NoTypeInformation
Write-Host "✅ Found $($AllRepos.Count) total repositories" -ForegroundColor Green

# ============================================
# PHASE 2: SIMILARITY & DUPLICATION DETECTION
# ============================================
Write-Host "`n🔍 PHASE 2: Analyzing similar names and duplicates..." -ForegroundColor Cyan

# Group by exact name
$ExactDuplicates = $AllRepos | Group-Object Name | Where-Object { $_.Count -gt 1 }

# Fuzzy similarity detection (Levenshtein-style simple matching)
function Get-SimilarityScore {
    param([string]$s1, [string]$s2)
    $s1 = $s1.ToLower().Replace("-","").Replace("_","").Replace(" ","")
    $s2 = $s2.ToLower().Replace("-","").Replace("_","").Replace(" ","")
    
    if ($s1 -eq $s2) { return 100 }
    if ($s1.Contains($s2) -or $s2.Contains($s1)) { return 85 }
    
    # Simple character overlap
    $set1 = $s1.ToCharArray() | Sort-Object -Unique
    $set2 = $s2.ToCharArray() | Sort-Object -Unique
    $intersection = ($set1 | Where-Object { $set2 -contains $_ }).Count
    $union = ($set1 + $set2 | Sort-Object -Unique).Count
    return [math]::Round(($intersection / $union) * 100)
}

$SimilarGroups = @()
$processed = @()

for ($i = 0; $i -lt $AllRepos.Count; $i++) {
    if ($processed -contains $i) { continue }
    
    $group = @($AllRepos[$i])
    $processed += $i
    
    for ($j = $i + 1; $j -lt $AllRepos.Count; $j++) {
        if ($processed -contains $j) { continue }
        
        $score = Get-SimilarityScore $AllRepos[$i].Name $AllRepos[$j].Name
        if ($score -ge 70) {
            $group += $AllRepos[$j]
            $processed += $j
        }
    }
    
    if ($group.Count -gt 1) {
        $SimilarGroups += [PSCustomObject]@{
            GroupID = $SimilarGroups.Count + 1
            PrimaryName = $group[0].Name
            MatchCount = $group.Count
            Similarity = "High"
            Paths = ($group.FullPath -join "`n")
            TotalSizeMB = ($group | Measure-Object -Property SizeMB -Sum).Sum
            HasRemotes = ($group | Where-Object { $_.HasRemote }).Count
            AllRemotes = ($group | Where-Object { $_.RemoteUrl } | Select-Object -ExpandProperty RemoteUrl -Unique) -join "`n"
        }
    }
}

# Export duplicates
$ExactDuplicates | Select-Object Name, Count, @{N='Paths';E={($_.Group.FullPath -join "`n")}} | 
    Export-Csv "$OutputPath\2-EXACT-DUPLICATES.csv" -NoTypeInformation

$SimilarGroups | Export-Csv "$OutputPath\3-SIMILAR-NAMES.csv" -NoTypeInformation
Write-Host "✅ Found $($ExactDuplicates.Count) exact duplicates, $($SimilarGroups.Count) similar groups" -ForegroundColor Green

# ============================================
# PHASE 3: ACTION CATEGORIZATION
# ============================================
Write-Host "`n🔍 PHASE 3: Categorizing actions..." -ForegroundColor Cyan

$ArchiveCandidates = @()
$CombineCandidates = @()
$UpdateCandidates = @()
$KeepAsIs = @()

foreach ($repo in $AllRepos) {
    # Archive: No remote, old, clean, single branch
    if (-not $repo.HasRemote -and -not $repo.IsRecent -and $repo.GitStatus -eq "clean" -and $repo.BranchCount -le 1 -and $repo.SizeMB -lt 50) {
        $ArchiveCandidates += $repo
    }
    # Combine: Part of a duplicate/similar group
    elseif (($ExactDuplicates | Where-Object { $_.Name -eq $repo.Name }) -or 
            ($SimilarGroups | Where-Object { $_.Paths -contains $repo.FullPath })) {
        $CombineCandidates += $repo
    }
    # Update: Has remote but not recent, or dirty
    elseif ($repo.HasRemote -and (-not $repo.IsRecent -or $repo.GitStatus -eq "dirty")) {
        $UpdateCandidates += $repo
    }
    else {
        $KeepAsIs += $repo
    }
}

# Export categorized lists
$ArchiveCandidates | Export-Csv "$OutputPath\4-ARCHIVE-CANDIDATES.csv" -NoTypeInformation
$CombineCandidates | Export-Csv "$OutputPath\5-COMBINE-CANDIDATES.csv" -NoTypeInformation
$UpdateCandidates | Export-Csv "$OutputPath\6-UPDATE-CANDIDATES.csv" -NoTypeInformation
$KeepAsIs | Export-Csv "$OutputPath\7-KEEP-AS-IS.csv" -NoTypeInformation

# ============================================
# PHASE 4: GENERATE EXECUTIVE SUMMARY
# ============================================
Write-Host "`n📊 PHASE 4: Generating executive summary..." -ForegroundColor Cyan

$TotalSize = ($AllRepos | Measure-Object -Property SizeMB -Sum).Sum
$RemoteCount = ($AllRepos | Where-Object { $_.HasRemote }).Count
$RecentCount = ($AllRepos | Where-Object { $_.IsRecent }).Count
$DirtyCount = ($AllRepos | Where-Object { $_.GitStatus -eq "dirty" }).Count

$Summary = @"
# REPOSITORY AUDIT REPORT
**Generated:** $(Get-Date)
**Auditor:** Kimi Code PowerShell Engine
**Cutoff Date:** $OneMonthAgo

## 📊 HIGH-LEVEL METRICS
| Metric | Count |
|--------|-------|
| **Total Repositories** | $($AllRepos.Count) |
| **Total Size** | $([math]::Round($TotalSize, 2)) MB |
| **With Remotes** | $RemoteCount |
| **Updated (Last 30 Days)** | $RecentCount |
| **Uncommitted Changes** | $DirtyCount |
| **Exact Duplicates** | $($ExactDuplicates.Count) |
| **Similar Names** | $($SimilarGroups.Count) groups |

## 🎯 ACTION BREAKDOWN
| Action | Count | Est. Space Saved |
|--------|-------|------------------|
| **🗑️ ARCHIVE** | $($ArchiveCandidates.Count) | $([math]::Round(($ArchiveCandidates | Measure-Object -Property SizeMB -Sum).Sum, 2)) MB |
| **🔗 COMBINE** | $($CombineCandidates.Count) | $([math]::Round(($CombineCandidates | Measure-Object -Property SizeMB -Sum).Sum / 2, 2)) MB |
| **⬆️ UPDATE** | $($UpdateCandidates.Count) | - |
| **✅ KEEP** | $($KeepAsIs.Count) | - |

## 🔗 REMOTE REPOSITORIES
$($AllRepos | Where-Object { $_.HasRemote } | ForEach-Object { "- [$($_.Name)]($($_.RemoteUrl)) - $($_.FullPath)" } | Out-String)

## 🗑️ ARCHIVE CANDIDATES (Safe to Zip/Delete)
$($ArchiveCandidates | ForEach-Object { "- **$($_.Name)** | $($_.FullPath) | Last: $($_.LastModified.ToString('yyyy-MM-dd')) | $($_.SizeMB)MB" } | Out-String)

## 🔗 COMBINE CANDIDATES (Merge These)
$($SimilarGroups | ForEach-Object { 
    "### Group $($_.GroupID): $($_.PrimaryName) ($($_.MatchCount) matches)`n$($_.Paths -split "`n" | ForEach-Object { "- $_" } | Out-String)`n**Suggested:** Keep one with remote, archive others`n" 
} | Out-String)

## ⬆️ UPDATE CANDIDATES (Git Pull/Push Needed)
$($UpdateCandidates | ForEach-Object { "- **$($_.Name)** | $($_.GitStatus) | $($_.FullPath)" } | Out-String)

## 📁 OUTPUT FILES
All detailed CSVs saved to: $OutputPath

---
**Next Steps:**
1. Review `4-ARCHIVE-CANDIDATES.csv` → Zip and delete
2. Review `5-COMBINE-CANDIDATES.csv` → Merge repos
3. Run `git pull` on `6-UPDATE-CANDIDATES.csv`
"@

$Summary | Out-File "$OutputPath\0-EXECUTIVE-SUMMARY.md" -Encoding utf8

# ============================================
# PHASE 5: GENERATE ACTION SCRIPTS
# ============================================
Write-Host "`n⚡ PHASE 5: Generating action scripts..." -ForegroundColor Cyan

# Archive script
$ArchiveScript = @"
# AUTO-GENERATED ARCHIVE SCRIPT
# Run with: .\archive-repos.ps1
# BACKUP BEFORE RUNNING!

`$ArchiveDate = Get-Date -Format "yyyy-MM-dd"
`$ArchiveDir = "`$env:USERPROFILE\ArchivedRepos_`$ArchiveDate"
New-Item -ItemType Directory -Path `$ArchiveDir -Force

"@ + ($ArchiveCandidates | ForEach-Object { 
    "`$source = '$($_.FullPath -replace "'", "''")'`n`$name = '$($_.Name -replace "'", "''")'`nCompress-Archive -Path `$source -DestinationPath `"`$ArchiveDir\`$name.zip`" -Force`nWrite-Host `"Archived: `$name`"`n# Remove-Item `$source -Recurse -Force # UNCOMMENT TO DELETE`n" 
} | Out-String)

$ArchiveScript | Out-File "$OutputPath\ACTION-archive-repos.ps1" -Encoding utf8

# Update script
$UpdateScript = @"
# AUTO-GENERATED UPDATE SCRIPT
# Run with: .\update-repos.ps1

"@ + ($UpdateCandidates | Where-Object { $_.HasRemote } | ForEach-Object { 
    "`$path = '$($_.FullPath -replace "'", "''")'`nWrite-Host `"Updating: $($_.Name)`" -ForegroundColor Cyan`ngit -C `$path fetch --all`ngit -C `$path pull --all`n" 
} | Out-String)

$UpdateScript | Out-File "$OutputPath\ACTION-update-repos.ps1" -Encoding utf8

# ============================================
# FINAL OUTPUT
# ============================================
Write-Host "`n✅ AUDIT COMPLETE!" -ForegroundColor Green
Write-Host "📁 All reports saved to: $OutputPath" -ForegroundColor Yellow
Write-Host "`n📊 SUMMARY:" -ForegroundColor Cyan
Write-Host "   Total Repos: $($AllRepos.Count)" -ForegroundColor White
Write-Host "   🗑️ Archive: $($ArchiveCandidates.Count)" -ForegroundColor Red
Write-Host "   🔗 Combine: $($CombineCandidates.Count)" -ForegroundColor Yellow
Write-Host "   ⬆️ Update: $($UpdateCandidates.Count)" -ForegroundColor Blue
Write-Host "   ✅ Keep: $($KeepAsIs.Count)" -ForegroundColor Green

# Open folder
Invoke-Item $OutputPath WHAT THIS DOES:Table  Copy   PhaseAction 1Scans common dev folders + deep C: drive scan for .git folders2Detects exact duplicates and fuzzy similar names (70%+ match)3Categorizes: Archive (no remote, old, clean), Combine (duplicates), Update (has remote, dirty/old), Keep4Generates EXECUTIVE-SUMMARY.md with full markdown report5Auto-generates ready-to-run PowerShell scripts for archiving and updatingOUTPUT FILES:0-EXECUTIVE-SUMMARY.md — Full markdown report1-FULL-INVENTORY.csv — Every repo found2-EXACT-DUPLICATES.csv — Same name, different paths3-SIMILAR-NAMES.csv — Fuzzy matches (e.g., casa-companion vs casa_companion)4-ARCHIVE-CANDIDATES.csv — Safe to zip/delete5-COMBINE-CANDIDATES.csv — Merge these6-UPDATE-CANDIDATES.csv — Run git pull7-KEEP-AS-IS.csv — Active projectsACTION-archive-repos.ps1 — One-click archive scriptACTION-update-repos.ps1 — One-click update scriptTo run in Kimi Code:Save as repo-audit.ps1Run: kimi-code powershell -f repo-audit.ps1Or paste directly into Kimi Code terminalWant me to add GitHub API integration to check if remotes are ahead/behind, or add a "merge repos" script for the combine candidates?                                                       Ask away. Pics work too.                       K2.6 Instant

---
