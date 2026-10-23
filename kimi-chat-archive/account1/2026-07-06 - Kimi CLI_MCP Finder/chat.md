# Kimi CLI/MCP Finder

- Created: 2026-07-03T02:40:57Z
- Updated: 2026-07-06T11:51:46Z

---

## 🧑 You

I need a prmompt foir kimi code to go through and find all CLI and mcp created

---

## 🤖 Kimi

I'll build you a comprehensive Kimi Code prompt to scan your entire project tree for CLI tools, MCP integrations, and any command-line interfaces. Since you work across multiple repos (EnPro, Casa Companion, edge-crew-v3, etc.), this will be a universal scanner.KIMI CODE PROMPT: CLI & MCP AUDIT SCANNERText   Copy # === KIMI CODE PROMPT: UNIVERSAL CLI & MCP DISCOVERY SCAN ===
# Target: Scan entire project tree for all CLI tools, MCP servers, 
#         command-line interfaces, and terminal integrations
# Output: Structured markdown report with file paths, line numbers, 
#         and categorized inventory
# ============================================================

## EXECUTION RULES
- Scan ALL files: .py, .js, .ts, .json, .yaml, .yml, .toml, .sh, .ps1, .md
- Search recursively from project root
- Do NOT skip node_modules, venv, or .git — but flag them as "dependency"
- Report EVERY match with exact file path and line number
- Categorize by: Type (CLI/MCP/Script/Config), Language, Purpose

## SEARCH PATTERNS — FIND ALL OF THESE

### 1. MCP (Model Context Protocol) Indicators
- "mcp" in filenames or content
- "model_context_protocol" 
- "mcp_server", "mcp_client", "mcp-tool"
- "@modelcontextprotocol" (npm packages)
- "stdio" transport references
- "sse" transport references
- Any .json with "mcpServers" or "mcp" key
- Claude Desktop config: claude_desktop_config.json
- Cursor MCP settings
- Files in directories named: mcp/, mcp-servers/, mcp_tools/

### 2. CLI Tool Indicators  
- "argparse", "click", "typer", "fire" (Python CLI libs)
- "commander", "yargs", "minimist", "oclif" (Node CLI libs)
- "#!/usr/bin" or "#!/bin/bash" shebangs
- "bin": entries in package.json
- "console_scripts" in setup.py / pyproject.toml
- "scripts": entries in package.json
- Any file with "cli" in name: *cli*.py, *cli*.js, cli/*.js
- PowerShell functions with [CmdletBinding()] or param blocks
- Any .exe, .bat, .cmd references in code
- "subprocess.run", "os.system", "child_process" calls

### 3. Terminal / Shell Integrations
- .ps1, .sh, .bash, .zsh files
- PowerShell modules (.psm1, .psd1)
- Terminal emulators or PTY references
- "xterm", "node-pty", "pty.js" 
- Shell escape sequences or ANSI codes

### 4. API / SDK Wrappers (CLI-like interfaces)
- Any wrapper around external APIs that exposes commands
- "api_client", "sdk", "wrapper" with command methods
- Azure CLI references ("az ")
- AWS CLI references ("aws ")
- gcloud, kubectl, docker, npm, npx, pip, poetry, uv

## OUTPUT FORMAT — STRICT STRUCTURE

For each discovery, output:

```markdown
### [CATEGORY]: [NAME]
- **File**: `absolute/path/to/file`
- **Line**: [number]
- **Type**: [CLI Tool / MCP Server / MCP Client / Shell Script / Config / Wrapper]
- **Language**: [Python / JavaScript / TypeScript / PowerShell / Bash / JSON / etc]
- **Purpose**: [One-line description of what it does]
- **Dependencies**: [List key imports or external tools]
- **Entry Point**: [How to run it — command name, script path, etc]
- **Context**: [2-3 lines of surrounding code for verification] SUMMARY SECTION — END OF REPORTAfter all discoveries, generate:Markdown  Fullscreen  Download  Fit  Code Preview  ## 📊 AUDIT SUMMARY
- **Total CLI Tools Found**: [N]
- **Total MCP Servers**: [N]  
- **Total MCP Clients**: [N]
- **Total Shell Scripts**: [N]
- **Total Config Files**: [N]
- **Languages Used**: [List]
- **Projects Affected**: [List repo names]

## 🔧 QUICK REFERENCE — ALL COMMANDS
| Command | Source File | Description |
|---------|-------------|-------------|
| `cmd1`  | path/to/file | what it does |

## 🚨 MISSING / INCOMPLETE
[List any files that reference CLI/MCP but appear broken, incomplete, or orphaned]  EXECUTION STEPSStart at project root: [INSERT YOUR ROOT PATH HERE]Run find or Get-ChildItem to enumerate all filesApply search patterns above using grep/Select-StringFor each hit, open file and extract context (±3 lines)Categorize and format per OUTPUT FORMATGenerate SUMMARY SECTIONSave report to: CLI_MCP_AUDIT_REPORT.md in project rootROOT PATHS TO SCAN (your known projects)C:\Users\Dekan AI Brother\Desktop*C:\Claude\Projects*C:\Users\Dekan AI Brother\casa-companion-hero-pipeline\C:\Users\Dekan AI Brother\runway\Any other repo roots you findFINAL INSTRUCTIONDo NOT summarize or explain. Execute the scan, generate the full report,
and save it. If a directory doesn't exist, note it and skip.
If you find nested git repos, scan them too and note the repo name.plain   Copy 
---

## HOW TO USE THIS

1. **Copy the entire block above** into a new Kimi Code chat
2. **Replace the root paths** with your actual directories (or leave the glob patterns — it'll find them)
3. **Add any specific repo names** I missed from your recent work
4. Run it — it'll crawl everything and give you a single master inventory

---

## QUICK CUSTOMIZATION OPTIONS

| If you want... | Add this to the prompt |
|---------------|----------------------|
| Only active/enabled tools | Add: "Skip commented-out code and .bak files" |
| Security audit focus | Add: "Flag any hardcoded tokens, API keys, or credentials in CLI configs" |
| Dependency mapping | Add: "For each CLI tool, trace which other tools call it" |
| Cross-repo linking | Add: "If the same CLI name appears in multiple repos, group them together" |

Want me to also generate a **PowerShell one-liner version** you can run locally without Kimi Code, or a **focused scan for just MCP servers** (since you mentioned Proton Drive and web bridge interests)?                                                        Ask away. Pics work too.                       K2.6 Instant

---
