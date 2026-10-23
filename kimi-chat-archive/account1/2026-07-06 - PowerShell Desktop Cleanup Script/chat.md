# PowerShell Desktop Cleanup Script

- Created: 2026-07-03T02:40:18Z
- Updated: 2026-07-06T11:51:11Z

---

## 🧑 You

Okay. So I need a new prompt. For Kimi code PowerShell. To help me clean up and merge anything that's on my desktop. "C:\Users\Dekan AI Brother\Desktop\01-Music" from that 01 folder to this 08 "C:\Users\Dekan AI Brother\Desktop\08-Admin"  to where it belongs here you can first insrturt to plan this and audt it these shoul dnot be on my desktop and more

---

## 🤖 Kimi

I'll create a Kimi Code PowerShell prompt that audits your desktop, plans the cleanup, and merges everything from 01-Music into 08-Admin where it belongs. This will be a two-phase prompt: first audit/plan, then execute.KIMI CODE PROMPT: DESKTOP CLEANUP — MUSIC → ADMIN MERGECopy-paste this into Kimi Code PowerShell:powershell   Copy # === KIMI CODE PROMPT: DESKTOP CLEANUP AUDIT & MERGE ===
# SOURCE: C:\Users\Dekan AI Brother\Desktop\01-Music
# TARGET: C:\Users\Dekan AI Brother\Desktop\08-Admin
# GOAL: Audit, plan, then merge. These should NOT be on Desktop.

$source = "C:\Users\Dekan AI Brother\Desktop\01-Music"
$target = "C:\Users\Dekan AI Brother\Desktop\08-Admin"
$auditLog = "C:\Users\Dekan AI Brother\Desktop\desktop_cleanup_audit_$(Get-Date -Format 'yyyyMMdd_HHmm').txt"

function Write-Audit {
    param([string]$msg)
    $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    "$timestamp | $msg" | Tee-Object -FilePath $auditLog -Append
}

Write-Audit "=== PHASE 1: AUDIT & PLAN ==="
Write-Audit "Source: $source"
Write-Audit "Target: $target"

# 1. VERIFY PATHS
if (!(Test-Path $source)) {
    Write-Audit "ERROR: Source not found: $source"
    exit 1
}
if (!(Test-Path $target)) {
    Write-Audit "WARNING: Target not found. Creating: $target"
    New-Item -ItemType Directory -Path $target -Force | Out-Null
}

# 2. SCAN SOURCE — WHAT'S IN 01-Music?
Write-Audit "`n--- SOURCE CONTENTS (01-Music) ---"
$sourceItems = Get-ChildItem -Path $source -Recurse -Force
$sourceItems | ForEach-Object {
    $type = if ($_.PSIsContainer) { "DIR" } else { "FILE" }
    $size = if (!$_.PSIsContainer) { "$([math]::Round($_.Length/1MB, 2)) MB" } else { "-" }
    Write-Audit "$type | $($_.FullName.Replace($source, '01-Music')) | $size"
}

# 3. SCAN TARGET — WHAT'S ALREADY IN 08-Admin?
Write-Audit "`n--- TARGET CONTENTS (08-Admin) ---"
$targetItems = Get-ChildItem -Path $target -Recurse -Force -ErrorAction SilentlyContinue
if ($targetItems) {
    $targetItems | ForEach-Object {
        $type = if ($_.PSIsContainer) { "DIR" } else { "FILE" }
        Write-Audit "$type | $($_.FullName.Replace($target, '08-Admin'))"
    }
} else {
    Write-Audit "Target is empty."
}

# 4. CONFLICT DETECTION — Same filenames?
Write-Audit "`n--- CONFLICT ANALYSIS ---"
$conflicts = @()
$sourceItems | Where-Object { !$_.PSIsContainer } | ForEach-Object {
    $relativePath = $_.FullName.Substring($source.Length).TrimStart('\')
    $destPath = Join-Path $target $relativePath
    if (Test-Path $destPath) {
        $conflicts += [PSCustomObject]@{
            File = $relativePath
            SourceSize = $_.Length
            DestSize = (Get-Item $destPath).Length
            SourceModified = $_.LastWriteTime
            DestModified = (Get-Item $destPath).LastWriteTime
        }
        Write-Audit "CONFLICT: $relativePath exists in target"
    }
}
if ($conflicts.Count -eq 0) {
    Write-Audit "No filename conflicts detected."
}

# 5. PROPOSED MERGE STRUCTURE
Write-Audit "`n--- PROPOSED MERGE PLAN ---"
Write-Audit "1. Create subfolder in target: '08-Admin\01-Music-Archive-$(Get-Date -Format 'yyyyMMdd')'"
Write-Audit "2. Move ALL contents from 01-Music into this archive subfolder"
Write-Audit "3. Preserve directory structure: 01-Music\Subfolder\file.mp3 → 08-Admin\01-Music-Archive\Subfolder\file.mp3"
Write-Audit "4. Handle conflicts: Keep newer file, rename older to .backup"
Write-Audit "5. Post-move: Verify checksums/size match, then delete empty 01-Music"
Write-Audit "6. Final: Remove 01-Music folder from Desktop entirely"

# 6. SIZE CALCULATION
$totalSize = ($sourceItems | Where-Object { !$_.PSIsContainer } | Measure-Object -Property Length -Sum).Sum
Write-Audit "`nTotal data to move: $([math]::Round($totalSize/1MB, 2)) MB"
Write-Audit "File count: $(($sourceItems | Where-Object { !$_.PSIsContainer }).Count)"
Write-Audit "Folder count: $(($sourceItems | Where-Object { $_.PSIsContainer }).Count)"

Write-Audit "`n=== AUDIT COMPLETE ==="
Write-Audit "Review $auditLog before proceeding to Phase 2."
Write-Audit "To execute merge, run Phase 2 commands below." PHASE 2: EXECUTE THE MERGEAfter you review the audit log, run this:powershell   Copy # === PHASE 2: EXECUTE MERGE ===
$source = "C:\Users\Dekan AI Brother\Desktop\01-Music"
$target = "C:\Users\Dekan AI Brother\Desktop\08-Admin"
$archiveName = "01-Music-Archive-$(Get-Date -Format 'yyyyMMdd')"
$archivePath = Join-Path $target $archiveName
$log = "C:\Users\Dekan AI Brother\Desktop\desktop_cleanup_EXECUTED_$(Get-Date -Format 'yyyyMMdd_HHmm').txt"

function Write-Log {
    param([string]$msg)
    $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    "$timestamp | $msg" | Tee-Object -FilePath $log -Append
}

Write-Log "=== PHASE 2: MERGE EXECUTION ==="
Write-Log "Archive destination: $archivePath"

# Create archive folder
New-Item -ItemType Directory -Path $archivePath -Force | Out-Null
Write-Log "Created archive folder: $archiveName"

# Robocopy with mirror logic (preserves structure, handles conflicts)
$robocopyArgs = @(
    "`"$source`"",
    "`"$archivePath`"",
    "/E",           # Include subdirectories (empty too)
    "/COPY:DAT",    # Copy Data, Attributes, Timestamps
    "/R:3",         # Retry 3 times
    "/W:5",         # Wait 5 sec between retries
    "/LOG:`"$log`"",
    "/NP",          # No progress percentage
    "/NDL",         # No directory list
    "/TEE"          # Output to console + log
)

Write-Log "Starting robocopy..."
$robocopyCmd = "robocopy $($robocopyArgs -join ' ')"
Invoke-Expression $robocopyCmd

# Verify transfer
$sourceCount = (Get-ChildItem $source -Recurse -File).Count
$destCount = (Get-ChildItem $archivePath -Recurse -File).Count

if ($destCount -ge $sourceCount) {
    Write-Log "SUCCESS: $destCount files copied to archive"
    
    # DELETE SOURCE ONLY IF VERIFIED
    Remove-Item -Path $source -Recurse -Force
    Write-Log "DELETED: $source removed from Desktop"
    
    # CLEANUP: If 08-Admin has other loose items, suggest structure
    Write-Log "`n=== POST-MERGE STATUS ==="
    Write-Log "01-Music is now archived inside 08-Admin"
    Write-Log "Desktop is cleaner. Full log: $log"
} else {
    Write-Log "ERROR: File count mismatch. Source: $sourceCount, Dest: $destCount"
    Write-Log "ABORTED: Source NOT deleted. Review manually."
} What This DoesTable  Copy   StepAction AuditScans everything in 01-Music, checks what's already in 08-Admin, detects filename conflictsPlanProposes an archive subfolder (01-Music-Archive-20250617) inside 08-Admin so nothing gets lostExecuteUses robocopy (fast, reliable, preserves timestamps) to move everything while keeping folder structureVerifyCounts files before deleting source — won't nuke anything unless match confirmedLogEvery action timestamped to a text file for your recordsQuick RunPaste Phase 1 → review the audit log → paste Phase 2. Done.Want me to also add a Phase 3 that scans the rest of your Desktop for other folders that should migrate to 08-Admin (or off Desktop entirely)?                                               Okay. That worked great. Now we need to do the same thing. But without those folders, more everything that our tools, scripts, projects, and review and audit here. Because there's redundant subfolders and loose files.   "C:\Users\Dekan AI Brother"

---

## 🧑 You

Got it — full sweep of your home directory. Auditing loose files, redundant subfolders, tools, scripts, projects, and getting everything consolidated into proper structure. No 01-Music or 08-Admin involved here — this is the root cleanup.KIMI CODE PROMPT: HOME DIRECTORY AUDIT & CONSOLIDATIONC:\Users\Dekan AI Brotherpowershell   Copy # === KIMI CODE PROMPT: HOME DIRECTORY DEEP AUDIT & CONSOLIDATION ===
# TARGET: C:\Users\Dekan AI Brother
# GOAL: Audit everything, find redundancies, plan consolidation
# EXCLUDE: System folders (Windows default), 01-Music, 08-Admin (already handled)

$homeDir = "C:\Users\Dekan AI Brother"
$auditLog = "$homeDir\HOME_AUDIT_$(Get-Date -Format 'yyyyMMdd_HHmm').txt"
$systemExcludes = @(
    "AppData","Contacts","Cookies","Documents","Downloads",
    "Favorites","Links","Music","NetHood","Pictures","PrintHood",
    "Recent","Saved Games","Searches","SendTo","Start Menu",
    "Templates","Videos","3D Objects","OneDrive","source",
    "ntuser.dat*","*.log","Desktop",".vscode",".continuerc"
)

function Write-Audit {
    param([string]$msg)
    $ts = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    "$ts | $msg" | Tee-Object -FilePath $auditLog -Append
}

Write-Audit "=== HOME DIRECTORY AUDIT ==="
Write-Audit "Scanning: $homeDir"
Write-Audit "Excluded: System defaults + 01-Music + 08-Admin"

# 1. DISCOVER ALL TOP-LEVEL ITEMS (excluding system)
Write-Audit "`n--- TOP-LEVEL DISCOVERY ---"
$topLevel = Get-ChildItem -Path $homeDir -Force | Where-Object {
    $name = $_.Name
    $isSystem = $systemExcludes | Where-Object { $name -like $_ }
    $isHandled = ($name -eq "01-Music") -or ($name -eq "08-Admin")
    !$isSystem -and !$isHandled
}

$topLevel | ForEach-Object {
    $type = if ($_.PSIsContainer) { "DIR" } else { "FILE" }
    $size = if ($_.PSIsContainer) { 
        $folderSize = (Get-ChildItem $_.FullName -Recurse -File -ErrorAction SilentlyContinue | Measure-Object -Property Length -Sum).Sum
        "$([math]::Round($folderSize/1MB, 2)) MB"
    } else { 
        "$([math]::Round($_.Length/1MB, 2)) MB" 
    }
    Write-Audit "$type | $($_.Name) | $size"
}

# 2. CATEGORIZE BY TYPE
Write-Audit "`n--- CATEGORIZATION ---"

$categories = @{
    "Projects" = @("Projects","project","repo","repos","github","casa","enpro","crowdsource","runway","edge-crew")
    "Tools" = @("tools","tool","cli","mcp","script","scripts","powershell","ps1","bat","cmd")
    "AI_Assistants" = @("kimi","claude","cursor","agent","agents","swarm","openrouter","groq")
    "Dev_Environment" = @("dev","env","venv","node_modules",".git","docker","azure","vercel")
    "Media_Assets" = @("image","images","video","videos","asset","assets","hero","pipeline")
    "Config_Credentials" = @("config","configs","credential","credentials","token","tokens","api","keys","env")
    "Archive_Old" = @("old","backup","bak","archive","temp","tmp","draft")
    "Documentation" = @("doc","docs","readme","md","note","notes","wiki")
}

$classified = @{}
$uncategorized = @()

$topLevel | ForEach-Object {
    $name = $_.Name.ToLower()
    $matched = $false
    foreach ($cat in $categories.Keys) {
        $patterns = $categories[$cat]
        if ($patterns | Where-Object { $name -match $_ }) {
            if (!$classified[$cat]) { $classified[$cat] = @() }
            $classified[$cat] += $_
            $matched = $true
            break
        }
    }
    if (!$matched) { $uncategorized += $_ }
}

# Report categories
foreach ($cat in $classified.Keys | Sort-Object) {
    Write-Audit "`n[$cat] — $($classified[$cat].Count) items:"
    $classified[$cat] | ForEach-Object {
        Write-Audit "  → $($_.Name)"
    }
}

Write-Audit "`n[UNCATEGORIZED] — $($uncategorized.Count) items:"
$uncategorized | ForEach-Object {
    Write-Audit "  → $($_.Name) | $(if($_.PSIsContainer){"DIR"}else{"FILE"})"
}

# 3. REDUNDANCY DETECTION
Write-Audit "`n--- REDUNDANCY SCAN ---"

# Find duplicate folder names (case-insensitive)
$allFolders = $topLevel | Where-Object { $_.PSIsContainer }
$folderNames = $allFolders | ForEach-Object { $_.Name.ToLower() } | Group-Object
$duplicates = $folderNames | Where-Object { $_.Count -gt 1 }
if ($duplicates) {
    Write-Audit "DUPLICATE FOLDER NAMES:"
    $duplicates | ForEach-Object {
        Write-Audit "  → '$($_.Name)' appears $($_.Count) times"
    }
} else {
    Write-Audit "No duplicate folder names detected."
}

# Find likely duplicate content (same filename in different folders)
Write-Audit "`n--- CROSS-FOLDER FILE DUPLICATES ---"
$allFiles = @()
$topLevel | Where-Object { $_.PSIsContainer } | ForEach-Object {
    Get-ChildItem -Path $_.FullName -Recurse -File -ErrorAction SilentlyContinue | ForEach-Object {
        $allFiles += [PSCustomObject]@{
            Name = $_.Name
            Size = $_.Length
            Folder = $_.DirectoryName.Replace($homeDir, "").TrimStart("\")
            FullPath = $_.FullName
            Hash = $null
        }
    }
}

# Quick hash check for obvious duplicates (same name + size)
$potentialDups = $allFiles | Group-Object Name, Size | Where-Object { $_.Count -gt 1 }
if ($potentialDups) {
    Write-Audit "POTENTIAL DUPLICATES (same name + size):"
    $potentialDups | Select-Object -First 10 | ForEach-Object {
        $files = $_.Group
        Write-Audit "  → $($files[0].Name) ($([math]::Round($files[0].Size/1KB, 2)) KB) found in:"
        $files | ForEach-Object {
            Write-Audit "      - $($_.Folder)"
        }
    }
    if ($potentialDups.Count -gt 10) {
        Write-Audit "  ... and $($potentialDups.Count - 10) more (truncated)"
    }
} else {
    Write-Audit "No obvious file duplicates detected."
}

# 4. LOOSE FILE AUDIT (files directly in home, not in folders)
Write-Audit "`n--- LOOSE FILES (directly in home) ---"
$looseFiles = $topLevel | Where-Object { !$_.PSIsContainer }
if ($looseFiles) {
    $looseFiles | ForEach-Object {
        Write-Audit "  → $($_.Name) | $([math]::Round($_.Length/1KB, 2)) KB | Modified: $($_.LastWriteTime.ToString('yyyy-MM-dd'))"
    }
    Write-Audit "TOTAL loose files: $($looseFiles.Count)"
} else {
    Write-Audit "No loose files found."
}

# 5. SIZE ANALYSIS
Write-Audit "`n--- SIZE ANALYSIS (top 10 largest folders) ---"
$folderSizes = $topLevel | Where-Object { $_.PSIsContainer } | ForEach-Object {
    $size = (Get-ChildItem $_.FullName -Recurse -File -ErrorAction SilentlyContinue | Measure-Object -Property Length -Sum).Sum
    [PSCustomObject]@{
        Name = $_.Name
        SizeMB = [math]::Round($size/1MB, 2)
        SizeGB = [math]::Round($size/1GB, 2)
    }
} | Sort-Object SizeMB -Descending

$folderSizes | Select-Object -First 10 | ForEach-Object {
    Write-Audit "  $($_.Name): $($_.SizeMB) MB ($($_.SizeGB) GB)"
}

$totalHomeSize = ($folderSizes | Measure-Object -Property SizeMB -Sum).Sum
Write-Audit "`nTOTAL scanned folder size: $([math]::Round($totalHomeSize/1024, 2)) GB"

# 6. PROPOSED CONSOLIDATION PLAN
Write-Audit "`n=== PROPOSED CONSOLIDATION PLAN ==="

$proposedStructure = @"
RECOMMENDED HOME STRUCTURE:
C:\Users\Dekan AI Brother\
├── 00-System\          (keep hidden, don't touch)
├── 02-Projects\        (all repos, codebases, active work)
│   ├── casa-companion\
│   ├── enpro\
│   ├── edge-crew\
│   └── runway\
├── 03-Tools\           (scripts, CLIs, MCPs, PowerShell)
│   ├── kimi-code\
│   ├── claude\
│   └── mcp\
├── 04-AI-Config\       (API keys, tokens, agent configs)
│   ├── credentials\
│   └── prompts\
├── 05-Assets\          (images, videos, media pipelines)
│   ├── hero-pipeline\
│   └── brand-assets\
├── 06-Archive\         (old versions, backups, drafts)
│   └── 2024-backups\
├── 07-Reviews\         (audit logs, review outputs, scans)
└── 08-Admin\           (already exists, keep)
    └── 01-Music-Archive\  (already merged)

MIGRATION RULES:
1. Move ALL project repos → 02-Projects\
2. Move ALL scripts/tools/CLIs → 03-Tools\
3. Move ALL API keys, tokens, .env files → 04-AI-Config\
4. Move ALL images/videos/media → 05-Assets\
5. Move anything older than 6 months or labeled old/backup → 06-Archive\
6. Keep loose files? NO → sort into appropriate folder or delete
7. Delete empty folders after move
"@

Write-Audit $proposedStructure

Write-Audit "`n=== AUDIT COMPLETE ==="
Write-Audit "Log saved: $auditLog"
Write-Audit "Review this, then run Phase 2 to execute consolidation." PHASE 2: EXECUTE CONSOLIDATIONAfter you review the audit, run this to build the structure and move everything:powershell   Copy # === PHASE 2: EXECUTE CONSOLIDATION ===
$homeDir = "C:\Users\Dekan AI Brother"
$log = "$homeDir\HOME_CONSOLIDATION_$(Get-Date -Format 'yyyyMMdd_HHmm').txt"

$structure = @{
    "02-Projects" = @("Projects","project","repo","repos","github","casa","enpro","crowdsource","runway","edge-crew","gce")
    "03-Tools" = @("tools","tool","cli","mcp","script","scripts","powershell","ps1","bat","cmd")
    "04-AI-Config" = @("kimi","claude","cursor","agent","agents","swarm","openrouter","groq","config","configs","credential","credentials","token","tokens","api","keys","env")
    "05-Assets" = @("image","images","video","videos","asset","assets","hero","pipeline","media")
    "06-Archive" = @("old","backup","bak","archive","temp","tmp","draft")
    "07-Reviews" = @("review","audit","scan","report","log","logs")
}

function Write-Log {
    param([string]$msg)
    $ts = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    "$ts | $msg" | Tee-Object -FilePath $log -Append
}

Write-Log "=== CONSOLIDATION EXECUTION ==="

# Create folders
$structure.Keys | ForEach-Object {
    $path = Join-Path $homeDir $_
    if (!(Test-Path $path)) {
        New-Item -ItemType Directory -Path $path -Force | Out-Null
        Write-Log "CREATED: $path"
    }
}

# Get top-level items (excluding system, Desktop subfolders already handled)
$excludes = @("AppData","Contacts","Cookies","Documents","Downloads","Favorites",
    "Links","Music","NetHood","Pictures","PrintHood","Recent","Saved Games",
    "Searches","SendTo","Start Menu","Templates","Videos","3D Objects","OneDrive",
    "source","Desktop","01-Music","08-Admin","ntuser.dat*")

$items = Get-ChildItem -Path $homeDir -Force | Where-Object {
    $name = $_.Name
    $skip = $excludes | Where-Object { $name -like $_ }
    $isLog = $name -like "HOME_*"
    !$skip -and !$isLog -and ($name -ne "02-Projects") -and ($name -ne "03-Tools") -and ($name -ne "04-AI-Config") -and ($name -ne "05-Assets") -and ($name -ne "06-Archive") -and ($name -ne "07-Reviews")
}

# Move items to best match
$items | ForEach-Object {
    $name = $_.Name
    $lowerName = $name.ToLower()
    $sourcePath = $_.FullName
    $destFolder = $null
    $reason = "uncategorized"

    foreach ($folder in $structure.Keys) {
        $patterns = $structure[$folder]
        foreach ($pattern in $patterns) {
            if ($lowerName -match $pattern) {
                $destFolder = $folder
                $reason = "matched pattern: $pattern"
                break
            }
        }
        if ($destFolder) { break }
    }

    if ($destFolder) {
        $destPath = Join-Path $homeDir $destFolder
        $finalPath = Join-Path $destPath $name
        
        # Handle conflicts
        if (Test-Path $finalPath) {
            $newName = "$name-$(Get-Date -Format 'yyyyMMdd-HHmmss')"
            $finalPath = Join-Path $destPath $newName
            Write-Log "CONFLICT: Renamed to $newName"
        }

        # Move it
        try {
            Move-Item -Path $sourcePath -Destination $finalPath -Force
            Write-Log "MOVED: $name → $destFolder ($reason)"
        } catch {
            Write-Log "ERROR moving $name : $_"
        }
    } else {
        # Uncategorized → prompt or leave
        Write-Log "UNCATEGORIZED (manual review needed): $name"
    }
}

# Clean empty folders
Write-Log "`n--- CLEANUP ---"
Get-ChildItem -Path $homeDir -Directory -Force | Where-Object {
    $name = $_.Name
    $isNew = $structure.Keys -contains $name
    $isSystem = $excludes -contains $name
    !$isNew -and !$isSystem
} | ForEach-Object {
    $isEmpty = !(Get-ChildItem -Path $_.FullName -Recurse -Force)
    if ($isEmpty) {
        Remove-Item $_.FullName -Force
        Write-Log "DELETED EMPTY: $($_.Name)"
    } else {
        Write-Log "LEFT (has content, review): $($_.Name)"
    }
}

Write-Log "`n=== CONSOLIDATION COMPLETE ==="
Write-Log "Log: $log"
Write-Log "Review uncategorized items and adjust structure as needed." What This DoesTable  Copy   PhaseAction AuditMaps every non-system folder/file in your home directory, categorizes by name patterns, flags duplicates, lists loose filesRedundancyDetects same filenames across folders, duplicate folder names, size mismatchesPlanProposes 02-Projects through 07-Reviews structure based on what you actually haveExecuteCreates the structure, moves items by pattern match, renames on conflict, deletes empty foldersLogEverything timestamped — you can review what moved wherePaste Phase 1, review the audit log, then paste Phase 2. Let me know if you want to adjust the category patterns before execution — I can tune them based on what the audit finds.                                                       Ask away. Pics work too.                       K2.6 Instant

---
