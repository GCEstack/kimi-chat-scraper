# Agent Credit Usage

- Created: 2026-07-03T02:41:09Z
- Updated: 2026-07-06T11:51:56Z

---

## 🧑 You

OK, is there a way to check how many credits are used on what agent for what like chemical code versus this on my $99 plan?

---

## 🤖 Kimi

I don't have access to your Kimi account's billing dashboard or usage metrics, so I can't directly check your credit consumption per agent. But I can tell you how to verify this yourself and what the typical breakdown looks like.Where to check your usage:Kimi Web App → Settings → Account → Usage/BillingKimi Code (if that's where you're running agents) → Check the CLI output or .kimi/logs/ for token counts per sessionKimi Claw (if using the agent framework) → Usually logs token usage in the agent execution summaryTypical credit burn patterns on the $99 plan:Kimi Code (Chemical Code / coding agents): Heavy burn. Code generation, especially with long context windows or multiple file edits, consumes significantly more tokens than chat. If you're running automated repo scans, batch refactors, or ESP-IDF builds, this is likely your biggest consumer.Deep Researcher / Web Agents: Moderate-to-high. These do web searches, page scraping, and synthesis. Each search + read operation is a separate API call.Websites / Frontend Agents: Variable. Image generation (Runway, image-to-video) and WebGL/Three.js code generation are expensive. Static HTML/CSS review is cheap.Standard Chat (this conversation): Lowest burn. Standard Q&A is the most credit-efficient mode.Quick diagnostic you can run:If you're using Kimi Code with PowerShell automation, check your recent sessions:powershell   Copy # If you have Kimi Code CLI logs
Get-ChildItem "$env:USERPROFILE\.kimi\logs" | Sort-Object LastWriteTime -Descending | Select-Object -First 5 | ForEach-Object {
    $content = Get-Content $_.FullName -Raw
    # Look for token usage summaries or credit deductions
    [regex]::Matches($content, '(?i)(tokens used|credits?|cost|usage).*') | ForEach-Object { $_.Value }
} My guess based on your recent sessions: Your "chemical code" (Kimi Code / repo automation) and image/video generation for Casa Companion are likely eating 60-70% of your credits. The deep-researcher agent audits and website rebuilds are secondary.Want me to help you build a PowerShell script to parse your local Kimi logs and estimate per-agent costs?                                               Sure

---

## 🧑 You

Execute Python code      Done. Here's your PowerShell credit auditor:Download: kimi-credit-audit.ps1What it does:Scans your Kimi Code logs (~\.kimi\logs and common alternates)Classifies every session by agent (chemical-code, deep-researcher, websites, ok-computer, etc.)Estimates token counts and credit burn per sessionGives you a ranked breakdown of which agent is eating your creditsShows daily burn rate and projects if you'll hit your $99 capHow to run it:powershell   Copy # Basic run (last 30 days)
.\kimi-credit-audit.ps1

# Weekly view
.\kimi-credit-audit.ps1 -DaysBack 7

# Custom log path if yours is elsewhere
.\kimi-credit-audit.ps1 -LogPath "C:\Your\Custom\Path" The output looks like this:plain   Copy chemical-code      ████████████████ 12.4 credits (45%) | 23 sessions | 41,333 tokens
image-video        ████████ 6.8 credits (25%) | 8 sessions | 13,600 tokens
deep-researcher    ████ 3.2 credits (12%) | 5 sessions | 16,000 tokens
websites           ██ 1.9 credits (7%) | 12 sessions | 6,333 tokens
ok-computer        █ 0.8 credits (3%) | 4 sessions | 2,666 tokens Important: The credit rates are estimates based on typical API pricing. If you know your exact Kimi plan rates, edit the $CREDIT_RATES hash at the top of the script before running.If the script can't find your logs, check where Kimi Code actually stores them—sometimes it's in %LOCALAPPDATA%\Kimi\logs instead of ~\.kimi\logs.                                                       Ask away. Pics work too.                       K2.6 Instant

---
