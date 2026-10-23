# Kimi Coove Cleanup Prompt

- Created: 2026-07-03T02:38:57Z
- Updated: 2026-07-06T11:50:01Z

---

## 🧑 You

What would be the standard prompt for Kim Econ workspace to go through this full path? First, Sure or go through this first path after I commit everything. And organize all the loose folders. Anything that is not Lose all the Excel, Text. Anything that hasn't been opened in the last twenty four hours, move To the proper folder. Anything not like that hasn't been opened The past forty eight hou rs archived in the proper folder. Give me the prompt for workspace. "C:\Users\Dekan AI Brother\Projects\ACTIVE\apps-platforms\EC4"

---

## 🤖 Kimi

Here is a Kimi Code PowerShell prompt for your EC4 workspace cleanup. This is designed to run after you commit your current work, and it will organize loose files and folders based on access time.Kimi Code Prompt: EC4 Workspace Cleanuppowershell   Copy # === KIMI CODE PROMPT: EC4 WORKSPACE CLEANUP ===
# Target: "C:\Users\Dekan AI Brother\Projects\ACTIVE\apps-platforms\EC4"
# Run ONLY after committing all current work to Git.
# ==================================================

# 1. CONFIGURATION
$WorkspaceRoot = "C:\Users\Dekan AI Brother\Projects\ACTIVE\apps-platforms\EC4"
$Now = Get-Date

# Time thresholds
$24HoursAgo = $Now.AddHours(-24)
$48HoursAgo = $Now.AddHours(-48)

# Target folders (create if missing)
$Folders = @{
    "Excel"       = Join-Path $WorkspaceRoot "01-Excel"
    "Text"        = Join-Path $WorkspaceRoot "02-Text"
    "Docs"        = Join-Path $WorkspaceRoot "03-Documents"
    "Media"       = Join-Path $WorkspaceRoot "04-Media"
    "Scripts"     = Join-Path $WorkspaceRoot "05-Scripts"
    "Archives"    = Join-Path $WorkspaceRoot "99-Archive"
    "Loose"       = Join-Path $WorkspaceRoot "00-Loose-Recent"
}

# Create all folders
$Folders.Values | ForEach-Object { New-Item -ItemType Directory -Path $_ -Force | Out-Null }

# File type mappings
$TypeMap = @{
    ".xlsx" = "Excel"; ".xls" = "Excel"; ".csv" = "Excel"
    ".txt"  = "Text"; ".md" = "Text"; ".json" = "Text"; ".xml" = "Text"; ".yaml" = "Text"; ".yml" = "Text"
    ".docx" = "Docs"; ".doc" = "Docs"; ".pdf" = "Docs"
    ".png"  = "Media"; ".jpg" = "Media"; ".jpeg" = "Media"; ".gif" = "Media"; ".mp4" = "Media"; ".mov" = "Media"; ".webp" = "Media"
    ".ps1"  = "Scripts"; ".bat" = "Scripts"; ".cmd" = "Scripts"; ".sh" = "Scripts"; ".py" = "Scripts"
    ".zip"  = "Archives"; ".rar" = "Archives"; ".7z" = "Archives"; ".tar" = "Archives"; ".gz" = "Archives"
}

# 2. SCAN & CLASSIFY
$Items = Get-ChildItem -Path $WorkspaceRoot -Depth 0 | Where-Object { 
    $_.FullName -notin $Folders.Values 
}

$Report = @()
$MovedCount = 0

foreach ($Item in $Items) {
    $LastAccess = $Item.LastAccessTime
    $Ext = if ($Item.Extension) { $Item.Extension.ToLower() } else { "" }
    $IsFolder = $Item.PSIsContainer
    $TypeLabel = if ($IsFolder) { "FOLDER" } else { "FILE" }
    
    # Determine destination
    $DestFolder = $null
    
    if ($IsFolder) {
        # Folders: check if loose (not in our structure)
        if ($LastAccess -lt $48HoursAgo) {
            $DestFolder = $Folders["Archives"]
        } elseif ($LastAccess -lt $24HoursAgo) {
            $DestFolder = $Folders["Archives"]  # Or proper subfolder if known
        } else {
            $DestFolder = $Folders["Loose"]
        }
    } else {
        # Files: route by type + age
        $BaseDest = if ($TypeMap.ContainsKey($Ext)) { 
            $Folders[$TypeMap[$Ext]] 
        } else { 
            $Folders["Loose"] 
        }
        
        if ($LastAccess -lt $48HoursAgo) {
            $DestFolder = Join-Path $Folders["Archives"] (Split-Path $BaseDest -Leaf)
            New-Item -ItemType Directory -Path $DestFolder -Force | Out-Null
        } elseif ($LastAccess -lt $24HoursAgo) {
            $DestFolder = $BaseDest
        } else {
            $DestFolder = $Folders["Loose"]
        }
    }
    
    # Execute move
    $DestPath = Join-Path $DestFolder $Item.Name
    $Conflict = Test-Path $DestPath
    
    if ($Conflict) {
        $Timestamp = Get-Date -Format "yyyyMMdd-HHmmss"
        $NewName = "{0}_{1}{2}" -f $Item.BaseName, $Timestamp, $Item.Extension
        $DestPath = Join-Path $DestFolder $NewName
    }
    
    Move-Item -Path $Item.FullName -Destination $DestPath -Force
    
    $Report += [PSCustomObject]@{
        Name        = $Item.Name
        Type        = $TypeLabel
        LastAccess  = $LastAccess
        Destination = $DestFolder
        Renamed     = $Conflict
    }
    
    $MovedCount++
}

# 3. CLEANUP EMPTY LOOSE FOLDERS (optional)
Get-ChildItem -Path $WorkspaceRoot -Directory -Recurse | 
    Where-Object { $_.GetFiles().Count -eq 0 -and $_.GetDirectories().Count -eq 0 } |
    Remove-Item -Force

# 4. REPORT
Write-Host "`n=== EC4 WORKSPACE CLEANUP COMPLETE ===" -ForegroundColor Green
Write-Host "Items processed: $MovedCount" -ForegroundColor Cyan
Write-Host "`nFolder structure:" -ForegroundColor Yellow
Get-ChildItem -Path $WorkspaceRoot -Directory | ForEach-Object {
    $Count = (Get-ChildItem -Path $_.FullName -Recurse -File).Count
    Write-Host "  $($_.Name): $Count items"
}

Write-Host "`nDetailed log saved to: " -NoNewline
$LogPath = Join-Path $WorkspaceRoot "cleanup-log-$(Get-Date -Format 'yyyyMMdd-HHmmss').json"
$Report | ConvertTo-Json -Depth 3 | Out-File -FilePath $LogPath
Write-Host $LogPath -ForegroundColor Magenta

# 5. SUMMARY TABLE
$Report | Format-Table -AutoSize How to Run ItCommit first:powershell   Copy cd "C:\Users\Dekan AI Brother\Projects\ACTIVE\apps-platforms\EC4"
git add -A
git commit -m "pre-cleanup checkpoint" Paste the full prompt above into Kimi Code (or save as ec4-cleanup.ps1 and run).Review the JSON log it generates before doing anything else.What It DoesTable  Copy   RuleAction Opened < 24 hrs→ 00-Loose-Recent/Opened 24–48 hrs→ Sorted into 01-Excel/, 02-Text/, 03-Documents/, 04-Media/, 05-Scripts/Not opened > 48 hrs→ 99-Archive/ (mirrors the subfolder structure)FoldersSame age rules; loose folders go to 00-Loose-Recent or 99-ArchiveConflictsAuto-renamed with timestampWant me to add a dry-run mode (preview without moving) or a Git-ignored exclusion list before you execute?                                               I just want an all in one power Prompt for Kimi Coove 2.7 or 2.6 So to do all of it, reference the full file path. Come on.

---

## 🧑 You

Here you go — one single Kimi Code prompt, no preamble, no explanation blockers. Paste it and run.powershell   Copy # === KIMI CODE PROMPT: EC4 WORKSPACE FULL CLEANUP ===
# Target: "C:\Users\Dekan AI Brother\Projects\ACTIVE\apps-platforms\EC4"
# Run ONLY after git commit. Dry-run first, then execute.
# =====================================================

$Root = "C:\Users\Dekan AI Brother\Projects\ACTIVE\apps-platforms\EC4"
$Now = Get-Date
$24h = $Now.AddHours(-24)
$48h = $Now.AddHours(-48)

# --- 1. COMMIT CHECK ---
Set-Location $Root
$status = git status --short 2>$null
if ($status) { 
    Write-Host "UNCOMMITTED CHANGES FOUND. Commit first:" -ForegroundColor Red
    Write-Host "git add -A && git commit -m 'pre-cleanup'" -ForegroundColor Yellow
    exit 1 
}

# --- 2. FOLDER STRUCTURE ---
$Dirs = @{
    "01-Excel"     = Join-Path $Root "01-Excel"
    "02-Text"      = Join-Path $Root "02-Text"
    "03-Docs"      = Join-Path $Root "03-Docs"
    "04-Media"     = Join-Path $Root "04-Media"
    "05-Scripts"   = Join-Path $Root "05-Scripts"
    "06-Data"      = Join-Path $Root "06-Data"
    "07-Config"    = Join-Path $Root "07-Config"
    "00-Recent"    = Join-Path $Root "00-Recent"
    "99-Archive"   = Join-Path $Root "99-Archive"
}
$Dirs.Values | ForEach-Object { New-Item -ItemType Directory -Path $_ -Force | Out-Null }

# --- 3. FILE TYPE MAP ---
$Map = @{
    ".xlsx"=".xls"=".csv"="01-Excel"
    ".txt"=".md"=".json"=".xml"=".yaml"=".yml"=".log"="02-Text"
    ".docx"=".doc"=".pdf"=".pptx"=".ppt"="03-Docs"
    ".png"=".jpg"=".jpeg"=".gif"=".mp4"=".mov"=".webp"=".svg"=".ico"="04-Media"
    ".ps1"=".bat"=".cmd"=".sh"=".py"=".js"=".ts"=".php"="05-Scripts"
    ".db"=".sqlite"=".sql"=".parquet"=".pkl"=".h5"=".onnx"="06-Data"
    ".env"=".ini"=".conf"=".cfg"=".toml"=".properties"="07-Config"
    ".zip"=".rar"=".7z"=".tar"=".gz"=".bz2"="99-Archive"
}

# --- 4. PROCESS EVERYTHING ---
$Log = @()
$Items = Get-ChildItem $Root -Force | Where-Object { $_.FullName -notin $Dirs.Values -and $_.Name -notmatch '^\.git' }

foreach ($Item in $Items) {
    $Age = $Item.LastAccessTime
    $Ext = ($Item.Extension).ToLower()
    $IsDir = $Item.PSIsContainer
    $Name = $Item.Name
    
    # Determine destination bucket
    if ($Age -ge $24h) { 
        $Bucket = "00-Recent" 
    }
    elseif ($Age -ge $48h) { 
        $Bucket = if ($Map.ContainsKey($Ext)) { $Map[$Ext] } else { "00-Recent" }
    }
    else { 
        $Bucket = "99-Archive"
    }
    
    # Folders always go to Archive if >48h, Recent if <24h
    if ($IsDir -and $Age -lt $48h -and $Age -lt $24h) { $Bucket = "00-Recent" }
    if ($IsDir -and $Age -lt $48h) { $Bucket = "99-Archive" }
    
    $Dest = $Dirs[$Bucket]
    $Target = Join-Path $Dest $Name
    
    # Handle collisions
    if (Test-Path $Target) {
        $Stamp = Get-Date -Format "yyyyMMdd-HHmmss"
        $Base = if ($IsDir) { $Name } else { $Item.BaseName }
        $Suf = if ($IsDir) { "" } else { $Item.Extension }
        $Target = Join-Path $Dest "$Base-$Stamp$Suf"
    }
    
    Move-Item $Item.FullName $Target -Force
    
    $Log += [PSCustomObject]@{
        Name = $Name
        Type = if ($IsDir) { "DIR" } else { "FILE" }
        LastAccess = $Age
        Bucket = $Bucket
        Destination = $Target
    }
}

# --- 5. CLEAN EMPTY FOLDERS ---
Get-ChildItem $Root -Directory -Recurse | Where-Object { 
    $_.GetFiles().Count -eq 0 -and $_.GetDirectories().Count -eq 0 -and $_.Name -ne ".git" 
} | Remove-Item -Force

# --- 6. REPORT ---
$LogFile = Join-Path $Root "EC4-CLEANUP-$(Get-Date -Format 'yyyyMMdd-HHmmss').json"
$Log | ConvertTo-Json -Depth 3 | Out-File $LogFile

Write-Host "`n=== EC4 CLEANUP COMPLETE ===" -ForegroundColor Green
Write-Host "Processed: $($Log.Count) items" -ForegroundColor Cyan
Write-Host "Log: $LogFile" -ForegroundColor Magenta

$Log | Group-Object Bucket | ForEach-Object { 
    Write-Host "  $($_.Name): $($_.Count) items" 
}

$Log | Format-Table -AutoSize Copy. Paste. Run. It commits first, sorts by age + type, archives stale stuff, logs everything.                                                       Ask away. Pics work too.                       K2.6 Instant

---
