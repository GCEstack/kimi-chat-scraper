# Third-Party App Scan

- Created: 2026-07-03T02:40:42Z
- Updated: 2026-07-06T11:51:30Z

---

## 🧑 You

ok now i needf a kimi code prompt to have it go through all my repos and scripts and my dekan ai to find mainly all the tyhird party appis we use like vercel groq azure etc

---

## 🤖 Kimi

Memory updated       Here you go — a single, copy-paste-ready PowerShell prompt for Kimi Code to scan your entire machine for every third-party API/service integration.KIMI CODE PROMPT: API & Service Inventory Scanpowershell   Copy # === KIMI CODE PROMPT: THIRD-PARTY API & SERVICE INVENTORY SCAN ===
# Objective: Scan all repos, scripts, and Dekan AI projects to find every 
# third-party API, service, SDK, and platform dependency. Build a master 
# inventory with file paths, line numbers, and usage context.
# ====================================================================

# === CONFIG ===
$scanPaths = @(
    "C:\Users\Dekan AI Brother\",
    "C:\Users\Dekan AI Brother\Desktop\",
    "C:\Claude\Projects\",
    "C:\Users\Dekan AI Brother\Documents\",
    "C:\Users\Dekan AI Brother\Downloads\"
)
$excludeDirs = @("node_modules", ".git", "venv", ".venv", "__pycache__", "dist", "build", ".next", ".vercel", "coverage", ".pytest_cache")
$outputDir = "C:\Users\Dekan AI Brother\api-inventory"
$timestamp = Get-Date -Format "yyyyMMdd_HHmm"
$inventoryFile = "$outputDir\api_inventory_$timestamp.md"

# === TARGET PATTERNS ===
# API Keys / Tokens
$apiKeyPatterns = @(
    "api[_-]?key\s*[:=]\s*['""][a-zA-Z0-9_-]+['""]",
    "apikey\s*[:=]\s*['""][a-zA-Z0-9_-]+['""]",
    "token\s*[:=]\s*['""][a-zA-Z0-9_-]+['""]",
    "auth[_-]?token\s*[:=]\s*['""][a-zA-Z0-9_-]+['""]",
    "bearer\s+['""][a-zA-Z0-9_-]+['""]",
    "sk-[a-zA-Z0-9]{20,}",                    # OpenAI-style keys
    "pk-[a-zA-Z0-9]{20,}",                    # Stripe-style keys
    "AKIA[0-9A-Z]{16}",                       # AWS keys
    "ghp_[a-zA-Z0-9]{36}",                    # GitHub tokens
    "glpat-[a-zA-Z0-9-]{20,}",                # GitLab tokens
    "dapi[a-f0-9]{32}",                       # Databricks
    "r8_[a-zA-Z0-9]{32}",                     # Replicate
    "hf_[a-zA-Z0-9]{30,}",                    # HuggingFace
    "groq[_-]?api[_-]?key",                   # Groq
    "azure[_-]?key",                          # Azure
    "deepgram[_-]?api[_-]?key",               # Deepgram
    "runway[_-]?api[_-]?key",                # Runway
    "vercel[_-]?token",                       # Vercel
    "openrouter[_-]?api[_-]?key",            # OpenRouter
    "cartesia[_-]?api[_-]?key",              # Cartesia
    "elevenlabs[_-]?api[_-]?key",            # ElevenLabs
    "anthropic[_-]?api[_-]?key",             # Anthropic
    "google[_-]?api[_-]?key",                # Google
    "firebase[_-]?api[_-]?key",              # Firebase
    "supabase[_-]?key",                       # Supabase
    "neon[_-]?api[_-]?key",                   # Neon
    "planetscale[_-]?token",                  # PlanetScale
    "mongodb[_-]?uri",                        # MongoDB
    "redis[_-]?url",                          # Redis
    "postgres[_-]?url",                       # PostgreSQL
    "mysql[_-]?url",                          # MySQL
    "docker[_-]?hub[_-]?token",              # Docker Hub
    "npm[_-]?token",                          # NPM
    "pypi[_-]?token"                          # PyPI
)

# Service/Platform Names (import statements, SDK usage, config references)
$servicePatterns = @(
    "vercel", "groq", "azure", "openai", "anthropic", "claude", "deepgram",
    "runway", "replicate", "elevenlabs", "cartesia", "openrouter", "groq",
    "huggingface", "pinecone", "weaviate", "chromadb", "supabase", "firebase",
    "neon", "planetscale", "mongodb", "redis", "postgres", "mysql", "sqlite",
    "docker", "kubernetes", "aws", "gcp", "google.cloud", "cloudflare",
    "stripe", "twilio", "sendgrid", "resend", "mailgun", "postmark",
    "auth0", "clerk", "nextauth", "supabase.auth", "firebase.auth",
    "vercel.ai", "ai-sdk", "langchain", "llamaindex", "crewai", "autogen",
    "semantic-kernel", "haystack", "transformers", "diffusers", "gradio",
    "streamlit", "chainlit", "fastapi", "flask", "django", "express",
    "next.js", "nuxt", "sveltekit", "remix", "astro", "solidjs",
    "tailwind", "shadcn", "radix", "framer-motion", "three.js", "webgl",
    "playwright", "puppeteer", "selenium", "cypress", "jest", "vitest",
    "pytest", "mocha", "github", "gitlab", "bitbucket", "jira", "linear",
    "notion", "slack", "discord", "teams", "zoom", "figma", "linear"
)

# File extensions to scan
$extensions = @("*.js", "*.ts", "*.jsx", "*.tsx", "*.py", "*.json", "*.yaml", "*.yml", "*.toml", "*.ini", "*.cfg", "*.env*", "*.sh", "*.ps1", "*.md", "*.txt", "*.html", "*.css", "*.scss", "*.sql", "*.prisma", "*.graphql", "*.dockerfile", "*.tf", "*.hcl")

# === EXECUTE SCAN ===
New-Item -ItemType Directory -Force -Path $outputDir | Out-Null
$results = [System.Collections.Generic.List[PSObject]]::new()

foreach ($basePath in $scanPaths) {
    if (-not (Test-Path $basePath)) { continue }
    
    Write-Host "🔍 Scanning: $basePath" -ForegroundColor Cyan
    
    foreach ($ext in $extensions) {
        $files = Get-ChildItem -Path $basePath -Filter $ext -Recurse -File -ErrorAction SilentlyContinue | Where-Object {
            $path = $_.FullName
            $skip = $false
            foreach ($ex in $excludeDirs) {
                if ($path -like "*\$ex\*") { $skip = $true; break }
            }
            -not $skip
        }
        
        foreach ($file in $files) {
            $content = Get-Content -Path $file.FullName -Raw -ErrorAction SilentlyContinue
            if (-not $content) { continue }
            
            $lines = $content -split "`n"
            
            # Check for API key patterns
            for ($i = 0; $i -lt $lines.Count; $i++) {
                $line = $lines[$i]
                foreach ($pattern in $apiKeyPatterns) {
                    if ($line -match $pattern) {
                        $results.Add([PSCustomObject]@{
                            Type = "API_KEY"
                            Service = ($pattern -split "[_-]")[0].ToUpper()
                            Pattern = $pattern
                            File = $file.FullName
                            Line = ($i + 1)
                            Snippet = ($line.Trim() -replace "['""][a-zA-Z0-9_-]{10,}['""]", "'***REDACTED***'")
                            Category = "Credential"
                        })
                    }
                }
            }
            
            # Check for service/platform references
            $contentLower = $content.ToLower()
            foreach ($service in $servicePatterns) {
                $matches = [regex]::Matches($contentLower, "\b$service\b")
                if ($matches.Count -gt 0) {
                    $results.Add([PSCustomObject]@{
                        Type = "SERVICE_REF"
                        Service = $service.ToUpper()
                        Pattern = $service
                        File = $file.FullName
                        Line = "N/A (multiple)"
                        Snippet = "Found $($matches.Count) references"
                        Category = "Platform"
                    })
                }
            }
        }
    }
}

# === DEDUPLICATE & ORGANIZE ===
$uniqueResults = $results | Group-Object -Property File, Service | ForEach-Object {
    $first = $_.Group | Select-Object -First 1
    $lines = ($_.Group | Where-Object { $_.Line -ne "N/A (multiple)" } | Select-Object -ExpandProperty Line -Unique) -join ", "
    if (-not $lines) { $lines = "N/A" }
    [PSCustomObject]@{
        Type = $first.Type
        Service = $first.Service
        File = $first.File
        Lines = $lines
        Occurrences = $_.Count
        Category = $first.Category
    }
}

# === GENERATE MARKDOWN INVENTORY ===
$md = @"
# 🔌 Third-Party API & Service Inventory
**Generated:** $(Get-Date -Format "yyyy-MM-dd HH:mm:ss")  
**Scanned Paths:** $($scanPaths -join ", ")  
**Total Findings:** $($uniqueResults.Count)

---

## 📊 Summary by Service

"@

$serviceSummary = $uniqueResults | Group-Object Service | Sort-Object Count -Descending
foreach ($svc in $serviceSummary) {
    $md += "`n### $($svc.Name) ($($svc.Count) files)`n"
    foreach ($item in $svc.Group | Sort-Object File) {
        $md += "- **$($item.File)** | Lines: $($item.Lines) | Type: $($item.Type) | Occurrences: $($item.Occurrences)`n"
    }
}

$md += @"

---

## 📁 Summary by Project/Repo

"@

$repoSummary = $uniqueResults | Group-Object { ($_.File -split "\\")[0..4] -join "\\" }
foreach ($repo in $repoSummary) {
    $md += "`n### $($repo.Name)`n"
    foreach ($item in $repo.Group | Sort-Object Service) {
        $md += "- **$($item.Service)** | File: $(Split-Path $item.File -Leaf) | Lines: $($item.Lines)`n"
    }
}

$md += @"

---

## 🔐 Credential Files Found

"@

$credFiles = $uniqueResults | Where-Object { $_.Category -eq "Credential" } | Select-Object File -Unique
if ($credFiles) {
    foreach ($cf in $credFiles) {
        $md += "- $($cf.File)`n"
    }
} else {
    $md += "_No explicit credential files found._`n"
}

$md += @"

---

## 🎯 Action Items
- [ ] Review each service for active usage vs. dead code
- [ ] Rotate any exposed API keys
- [ ] Consolidate duplicate service integrations
- [ ] Document service-to-project mapping
- [ ] Check for unused services incurring costs

---

*Inventory generated by Kimi Code API Scanner*
"@

# === OUTPUT ===
$md | Out-File -FilePath $inventoryFile -Encoding UTF8
Write-Host "`n✅ Inventory saved to: $inventoryFile" -ForegroundColor Green
Write-Host "📊 Services found: $($serviceSummary.Count)" -ForegroundColor Yellow
Write-Host "🔐 Credential references: $(($uniqueResults | Where-Object Category -eq 'Credential').Count)" -ForegroundColor Red

# Also export CSV for spreadsheet review
$uniqueResults | Export-Csv -Path "$outputDir\api_inventory_$timestamp.csv" -NoTypeInformation -Encoding UTF8
Write-Host "📄 CSV exported to: $outputDir\api_inventory_$timestamp.csv" -ForegroundColor Green

# === OPTIONAL: CREATE CONSOLIDATED .ENV TEMPLATE ===
$envTemplate = @"
# === CONSOLIDATED SERVICE CONFIGURATION ===
# Generated: $(Get-Date -Format "yyyy-MM-dd HH:mm:ss")
# Review each key and uncomment only active services

# AI / LLM
# OPENAI_API_KEY=your_key_here
# ANTHROPIC_API_KEY=your_key_here
# GROQ_API_KEY=your_key_here
# AZURE_OPENAI_KEY=your_key_here
# AZURE_OPENAI_ENDPOINT=your_endpoint_here
# OPENROUTER_API_KEY=your_key_here

# Voice / Audio
# DEEPGRAM_API_KEY=your_key_here
# ELEVENLABS_API_KEY=your_key_here
# CARTESIA_API_KEY=your_key_here

# Image / Video
# RUNWAY_API_KEY=your_key_here
# REPLICATE_API_TOKEN=your_key_here

# Database / Storage
# SUPABASE_URL=your_url_here
# SUPABASE_KEY=your_key_here
# NEON_DATABASE_URL=your_url_here
# MONGODB_URI=your_uri_here
# REDIS_URL=your_url_here

# Deployment / Hosting
# VERCEL_TOKEN=your_token_here
# AZURE_CONTAINER_REGISTRY=your_registry_here

# Auth
# CLERK_SECRET_KEY=your_key_here
# AUTH0_SECRET=your_secret_here

# Other
# HUGGINGFACE_TOKEN=your_token_here
# STRIPE_SECRET_KEY=your_key_here
"@

$envTemplate | Out-File -FilePath "$outputDir\.env.template" -Encoding UTF8
Write-Host "📝 .env template created at: $outputDir\.env.template" -ForegroundColor Cyan What It DoesTable  Copy   PhaseAction ScanRecursively searches all your repos/scripts for API keys, service imports, config referencesDetectMatches 50+ services (Vercel, Groq, Azure, OpenAI, Deepgram, Runway, Supabase, etc.)InventoryBuilds a markdown report with file paths, line numbers, occurrence countsOrganizeGroups by service AND by project so you see both viewsTemplateGenerates a .env.template with all discovered services for consolidationExportSaves CSV for spreadsheet review + Markdown for documentationOutput Filesplain   Copy C:\Users\Dekan AI Brother\api-inventory\
├── api_inventory_20260615_0210.md      # Master markdown report
├── api_inventory_20260615_0210.csv     # Spreadsheet data
└── .env.template                        # Consolidated config template Copy-paste the whole block into Kimi Code. It'll run the scan and give you the full inventory to review. BAM.                                                       Ask away. Pics work too.                       K2.6 Instant

---
