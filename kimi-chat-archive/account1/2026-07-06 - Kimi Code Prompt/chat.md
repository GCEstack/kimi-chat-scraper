# Kimi Code Prompt

- Created: 2026-07-03T02:40:22Z
- Updated: 2026-07-06T11:51:15Z

---

## 🧑 You

ok i need a prompt  for kimi code to find the $ profile we meade to use kimi code 2.6 just for code

---

## 🤖 Kimi

I'll craft a PowerShell profile prompt for you to use Kimi Code 2.6 specifically for code tasks. This will let you switch between thinking modes without the 2.7 auto-update interfering.Here's your prompt:powershell   Copy # === KIMI CODE 2.6 CODE-ONLY PROFILE ===
# Paste this into PowerShell (or save to $PROFILE for auto-load)

function kimi-code {
    param(
        [Parameter(Mandatory=$true, Position=0)]
        [string]$Prompt,
        
        [string]$Model = "kimi-k2.6",
        [string]$Context = "",
        [switch]$NoStream,
        [switch]$Debug
    )
    
    $env:KIMI_MODEL = "kimi-k2.6"
    $env:KIMI_MODE = "code"
    $env:KIMI_THINKING = "false"
    
    $body = @{
        model = $Model
        messages = @(
            @{
                role = "system"
                content = "You are Kimi Code 2.6. Execute code tasks directly. No thinking tags. No explanations unless asked. Output raw code, configs, or commands only. If unsure, output the most probable working solution."
            }
            @{
                role = "user"
                content = if ($Context) { "$Context`n`n$Prompt" } else { $Prompt }
            }
        )
        stream = if ($NoStream) { $false } else { $true }
        temperature = 0.1
    } | ConvertTo-Json -Depth 10
    
    if ($Debug) { Write-Host "Model: $Model | Mode: code-only" -ForegroundColor Cyan }
    
    # Adjust this to your actual Kimi CLI/API endpoint
    # If using kimi CLI: 
    # kimi chat --model $Model --no-thinking $Prompt
    
    Write-Host "▶ Kimi Code 2.6 (no-thinking)" -ForegroundColor Green
    # Replace with your actual invocation:
    # Invoke-RestMethod -Uri "YOUR_ENDPOINT" -Method POST -Body $body -ContentType "application/json"
    Write-Host "Prompt: $Prompt" -ForegroundColor Yellow
}

# === SHORT ALIASES ===
Set-Alias -Name kc -Value kimi-code
Set-Alias -Name k26 -Value kimi-code

# === QUICK MODE SWITCHERS ===
function kimi-think { $env:KIMI_THINKING = "true"; Write-Host "▶ Thinking mode ON" -ForegroundColor Magenta }
function kimi-nothink { $env:KIMI_THINKING = "false"; Write-Host "▶ Code mode ON (no-thinking)" -ForegroundColor Green }

# === USAGE ===
# kc "write a python script to scan folders"
# k26 -Context "Casa Companion repo" "fix the hero video pipeline"
# kimi-think    # switch to thinking mode when needed
# kimi-nothink  # back to code-only mode To make it permanent:powershell   Copy # Save to your PowerShell profile
notepad $PROFILE
# Paste the function above, save, restart PowerShell Key lock-ins:Model = "kimi-k2.6" — forces 2.6, ignores 2.7 auto-updatetemperature = 0.1 — deterministic, less creative wanderingSystem prompt kills thinking tags and explanatory fluffkimi-nothink / kimi-think — instant mode toggle without editing filesIf you need the actual API call wired up (instead of the placeholder), tell me how you're currently invoking Kimi Code (CLI tool? HTTP endpoint? Kimi Code PowerShell module?) and I'll swap in the real request format.                                                       Ask Anything...

---
