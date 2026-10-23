# Kimi Work Scheduler Integration

- Created: 2026-07-03T02:41:15Z
- Updated: 2026-07-06T11:52:00Z

---

## 🧑 You

Is there a way I could schedule tasks from Kimi app on my phone or the Kimi desktop to when we create things power show will pick up those task in the work session and run them

---

## 🤖 Kimi

Search Kimi AI schedule tasks PowerShell automation Kimi Code PowerShell integration task scheduling Kimi AI agent scheduled execution workflow  22 results    Yes, absolutely. The bridge between Kimi (app/desktop) and PowerShell execution is Kimi Work — the desktop local agent — which has a built-in Cron scheduler and can execute shell/Python tasks on your machine. Here's how to wire it up:The ArchitectureKimi Work (Desktop) → Cron Scheduler → PowerShell Script → Your Work SessionKimi Work runs locally, mounts your folders, and has a Cron engine that can trigger LLM agent calls, Python executions, or shell commands at scheduled intervals. It also supports "Keep Computer Awake" for overnight tasks. Two Ways to Set This UpOption 1: Kimi Work Native Cron (Recommended)Kimi Work has a built-in scheduler that supports:LLM Agent Calls — Trigger a Kimi agent to run a specific taskPython/Shell executions — Run PowerShell scripts directlyConditional triggers — Daily, hourly, or custom intervalsHow to configure:Open Kimi Work desktop appCreate a Skill (reusable instruction package) that defines what PowerShell should doUse the Cron scheduler to set when it runs (e.g., daily at 8 AM, or every 4 hours)Toggle "Keep Computer Awake" if you need overnight executionThe agent executes quietly in the background and writes outputs to your local foldersExample Skill prompt for PowerShell execution:plain   Copy Run PowerShell script at C:\Users\Dekan AI Brother\scripts\daily-sync.ps1
Capture output to C:\Users\Dekan AI Brother\logs\sync-$(Get-Date -Format yyyyMMdd).log
If errors occur, summarize them and save to error-log.txt Option 2: Windows Task Scheduler + Kimi Work BridgeIf you want more granular Windows-native control, use Task Scheduler to kick off PowerShell, but have Kimi Work generate/maintain the scripts:powershell   Copy # === KIMI WORK → POWERSHELL SCHEDULER ===
# Save this as: C:\Users\Dekan AI Brother\scripts\kimi-task-runner.ps1

param(
    [string]$TaskName = "default",
    [string]$WorkingDir = "C:\Users\Dekan AI Brother\",
    [string]$LogDir = "C:\Users\Dekan AI Brother\logs\"
)

$timestamp = Get-Date -Format "yyyy-MM-dd_HH-mm"
$logFile = Join-Path $LogDir "kimi-task-$TaskName-$timestamp.log"

# Create log directory if missing
New-Item -ItemType Directory -Force -Path $LogDir | Out-Null

# Write header
"=== KIMI TASK: $TaskName | $(Get-Date) ===" | Out-File $logFile -Append

# Your task logic here - this is what Kimi Work would generate/update
switch ($TaskName) {
    "repo-scan" {
        # Example: scan your repos
        "Running repo scan..." | Out-File $logFile -Append
        # Add your actual commands
    }
    "casa-companion-deploy" {
        "Deploying Casa Companion updates..." | Out-File $logFile -Append
    }
    "epo-crowdsource-sync" {
        "Syncing EPO Crowdsource..." | Out-File $logFile -Append
    }
    default {
        "No task handler for: $TaskName" | Out-File $logFile -Append
    }
}

"=== COMPLETED: $(Get-Date) ===" | Out-File $logFile -Append Then register it with Windows Task Scheduler:powershell   Copy # === REGISTER SCHEDULED TASK ===
$action = New-ScheduledTaskAction `
    -Execute "powershell.exe" `
    -Argument "-NoProfile -ExecutionPolicy Bypass -File `"C:\Users\Dekan AI Brother\scripts\kimi-task-runner.ps1`" -TaskName `"repo-scan`""

$trigger = New-ScheduledTaskTrigger -Daily -At 8am

$principal = New-ScheduledTaskPrincipal `
    -UserId "$env:USERDOMAIN\$env:USERNAME" `
    -LogonType Interactive `
    -RunLevel Highest

$settings = New-ScheduledTaskSettingsSet `
    -AllowStartIfOnBatteries `
    -DontStopIfGoingOnBatteries `
    -StartWhenAvailable

Register-ScheduledTask `
    -TaskName "KimiWork-RepoScan" `
    -Action $action `
    -Trigger $trigger `
    -Principal $principal `
    -Settings $settings `
    -Description "Kimi Work scheduled task - runs PowerShell script for repo scanning" The Workflow LoopYou create/schedule tasks in Kimi (app or desktop) — describe what you want doneKimi Work generates the PowerShell script and saves it to your scripts folderKimi Work Cron or Windows Task Scheduler picks it up at the scheduled timePowerShell runs it — writes logs, modifies files, deploys to Azure, etc.Next Kimi session — you or the AI reads the logs and continues from where it left offKimi Code IntegrationSince you use Kimi Code in PowerShell already, you can have the scheduled task invoke Kimi Code directly:powershell   Copy # In your scheduled script, call Kimi Code for autonomous execution
kimi --session "nightly-tasks" --yolo "Review C:\Users\Dekan AI Brother\runway\ for any new images, generate videos using the hero pipeline, and save to the videos folder. Log all actions." This uses Kimi Code's session persistence (--session) and auto-approval (--yolo) for fully hands-off execution. Bottom LineKimi Work desktop is the missing link. It has the scheduler, it runs locally, it can execute PowerShell, and it maintains context across sessions. You schedule tasks in natural language, Kimi Work translates that to PowerShell, and your Windows machine runs them on autopilot.Want me to build out the full PowerShell scaffold for your specific projects (Casa Companion, EPO, edge-crew) with the task definitions and scheduler registration?                                       Reference             Yes, please

---

## 🧑 You

Execute Python code      Here's your complete scaffold. Download it, run -Setup once, and you're fully automated.Download: kimi-work-scheduler.ps1What It DoesTable  Copy   ProjectTaskScheduleAction casa-companionhero-pipelineDaily 2 AMGenerate hero videos from new images via Runway pipelinechar-syncEvery 6 hoursSync character assets and voice commandsdeploy-checkDaily 8 AMCheck Azure container health, redeploy if deadepo-crowdsourcerepo-scanDaily 9 AMScan repo, update README, archive old branchesvendor-syncMondays 12 PMWeekly vendor search optimizationcommand-centerDaily 10 AMUpdate dashboard and logsedge-crew-v3swarm-reviewEvery 4 hoursSwarm review on latest commitsagent-healthDaily 7 AMCheck agent orchestration healthrunwayimage-to-videoDaily 1 AMProcess new images through Runway MLasset-cleanupSundays 3 AMWeekly temp asset and log cleanupHow to Use1. First-time setup (run once)powershell   Copy cd C:\Users\Dekan AI Brother\scripts\
.\kimi-work-scheduler.ps1 -Setup This creates:Individual .ps1 files for every task in C:\Users\Dekan AI Brother\scripts\Windows Scheduled Tasks for each (view in taskschd.msc)Log folder at C:\Users\Dekan AI Brother\logs\2. Run a task manuallypowershell   Copy .\kimi-work-scheduler.ps1 -RunNow -TaskName "KimiWork-casa-companion-hero-pipeline" 3. Run all tasks for a projectpowershell   Copy .\kimi-work-scheduler.ps1 -Project "epo-crowdsource" 4. Check statuspowershell   Copy .\kimi-work-scheduler.ps1 The Kimi Code BridgeEach generated task script calls Kimi Code like this:powershell   Copy kimi --session "scheduled-work" --yolo "You are in scheduled work mode for project casa-companion. Task: Generate hero videos from new images. Working directory: C:\Users\Dekan AI Brother\casa-companion-master\. Read the current state, execute the task, log all actions, and save outputs. Do NOT ask for confirmation. Execute immediately." What this means:--session "scheduled-work" — Maintains context across all scheduled runs--yolo — Auto-approves all actions (no human confirmation needed)The prompt includes the project context and working directory so Kimi Code knows exactly where it is and what to doQuick CustomizationOpen the script and edit the $Config hashtable at the top. Add new projects, change schedules, or modify task descriptions. Re-run -Setup to regenerate everything.Cron format used: minute hour day month weekday0 2 * * * = Daily at 2:00 AM0 */6 * * * = Every 6 hours0 12 * * 1 = Mondays at 12:00 PMLogsEvery task writes to:plain   Copy C:\Users\Dekan AI Brother\logs\kimi-work-{project}-{task}-{date}.log When you open a new Kimi session, point it at the logs folder and say "pick up where the scheduled tasks left off" — it'll read the latest logs and continue the work.BAM. Fully autonomous.                                                       Ask Anything...

---
