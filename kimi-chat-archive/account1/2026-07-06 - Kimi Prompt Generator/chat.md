# Kimi Prompt Generator

- Created: 2026-07-03T02:41:29Z
- Updated: 2026-07-06T11:52:09Z

---

## 🧑 You

I need a prompt to create the read me for thsi over all and back end front end   https://app-wheat-seven-35.vercel.app/

---

## 🤖 Kimi

I'll check the site first to understand the architecture, then build you a comprehensive README prompt. Fetch URLs   1 pages     Based on the site, here's your Kimi Code PowerShell prompt to generate a full README covering both backend and frontend architecture. Copy-paste this into your Kimi Code terminal:powershell   Copy # === KIMI CODE PROMPT: GENERATE CASA COMPANION README ===
# Run this in Kimi Code to generate a comprehensive README.md

kimi "Read the current project structure at C:\Users\Dekan AI Brother\casa-companion-master\ and generate a README.md that covers:

## PROJECT OVERVIEW
- Casa Companion: AI voice companion app with character selection
- Live at: https://app-wheat-seven-35.vercel.app/
- Tagline: 'Your AI companion. Real voice. Real personality.'

## FRONTEND ARCHITECTURE
- Framework: Next.js / React (inferred from Vercel deployment)
- UI: Character cards with image-to-video pipeline (hero videos in static/images)
- Characters identified: Pietro (The Leader), plus others from the roster
- Styling: Custom CSS with beachfront/ocean Casa Companion brand theme
- Voice integration: Real-time voice chat interface
- Deployment: Vercel (app-wheat-seven-35.vercel.app)

## BACKEND ARCHITECTURE
- API endpoints for character data and voice session management
- Voice processing pipeline (Whisper/Azure/Groq - document whichever is active)
- Character personality engine and response generation
- Database schema for character profiles, user sessions, conversation history

## KEY FEATURES
- Character selection with distinct personalities
- Real-time voice conversation
- Image-to-video hero pipeline (static/images/ → video assets)
- Voice command integration (play/pause/jump-in characters)
- Teen-to-adult character targeting

## FILE STRUCTURE
- Document the actual directory tree from the repo
- Mark sacred files (API keys, database schemas) as DO NOT MODIFY
- Note static asset locations (images, videos, audio)

## DEVELOPMENT WORKFLOW
- Local dev: npm run dev
- Build: npm run build (Vercel optimized)
- Environment variables needed
- How to add new characters (image + voice + personality config)

## VOICE PIPELINE
- Microphone input → transcription → character response → voice output
- Current provider: [document active: Whisper/Groq/Azure]
- Known issues: mic transcript glitch (torque/back-write issue)

## CHARACTER SYSTEM
- Each character has: image, video, voice profile, personality prompt, specialty
- Pietro: The Leader (founder archetype)
- Document all characters found in the codebase
- Character specialties: recipes, DJ help, etc.

## DEPLOYMENT
- Frontend: Vercel (current)
- Backend: [Azure Container Apps / serverless functions - document actual]
- Environment: production + staging

## NEXT STEPS / ROADMAP
- ESP32-S3 firmware integration (browser-only for now)
- Multi-agent orchestration
- Character video generation pipeline
- Voice command expansion

Generate this as a single markdown file at C:\Users\Dekan AI Brother\casa-companion-master\README.md. Do NOT modify any API keys, database connection strings, or sacred code files. Just document what exists." What this prompt does:Scans your actual repo structure at the path you useDocuments frontend (Next.js/Vercel) and backend (voice API + character engine) separatelyCaptures the character system (Pietro + roster), voice pipeline, and image-to-video workflowFlags sacred files so Kimi Code doesn't touch your API/database codeIncludes the known mic glitch and ESP32 roadmap from your recent sessionsRun it, then paste the generated README back if you want me to tighten it up. BAMMMM.                                               ok so i also need a kimi code propt to go throuh my desktop my dekan ai briorther users all folders to find all cas companion fiolders and sub folders so we can a rchive or mere with the atest one locsally'

---

## 🧑 You

Here's your Kimi Code PowerShell prompt to scan your entire Dekan AI Brother user profile, find all Casa Companion related folders, and prepare them for merge/archive:powershell   Copy # === KIMI CODE PROMPT: CASA COMPANION FOLDER AUDIT & MERGE PREP ===
# Paste this into Kimi Code PowerShell

kimi "Scan the entire user directory at C:\Users\Dekan AI Brother\ and perform a comprehensive Casa Companion folder audit.

## TASK 1: DISCOVERY
Recursively search all folders and subfolders under C:\Users\Dekan AI Brother\ for any directory containing:
- 'casa' (case insensitive)
- 'companion' (case insensitive)
- 'casa-companion' (exact)
- 'casa_companion' (underscore variant)
- Any folder with 'cc-' prefix

List EVERY match with:
- Full absolute path
- Folder size (MB/GB)
- Last modified date
- Top-level file count
- Whether it contains: node_modules, .git, static/images, static/videos, README, package.json

## TASK 2: CLASSIFICATION
Tag each found folder by type:
- [MASTER] = primary working repo (most recent, has package.json + .git)
- [PIPELINE] = image/video generation pipeline folders
- [ARCHIVE] = old versions, backups, duplicates
- [STATIC] = asset-only folders (images/videos only)
- [MISC] = anything else

## TASK 3: MERGE RECOMMENDATION
Identify which folders should be:
- MERGED into the master (newer assets, config files, scripts)
- ARCHIVED to a single archive location
- DELETED (empty node_modules, old caches, true duplicates)

Propose a target structure:
C:\Users\Dekan AI Brother\casa-companion-master\          (single source of truth)
C:\Users\Dekan AI Brother\_ARCHIVE\casa-companion\         (dated backups)
C:\Users\Dekan AI Brother\_ASSETS\casa-companion\          (extracted images/videos)

## TASK 4: SAFE EXECUTION SCRIPT
Generate a PowerShell script that:
1. Creates the archive and assets folders
2. Copies (not moves) all non-master folders to _ARCHIVE with date stamps
3. Extracts all images/videos from pipeline folders into _ASSETS
4. Leaves the master untouched
5. Outputs a merge checklist showing what to manually review

## OUTPUT FORMAT
Return:
1. The full audit table (path | size | type | action)
2. The classification summary
3. The generated PowerShell script as a downloadable .ps1 file
4. A manual merge checklist

DO NOT delete or move anything. Only scan, report, and generate scripts." What this does:Crawls your entire C:\Users\Dekan AI Brother\ tree for anything Casa Companion relatedSizes everything so you know what's eating disk spaceClassifies folders so you know what's master vs pipeline vs junkGenerates a safe PowerShell script that copies to archive — nothing gets deletedExtracts all your images/videos into a clean _ASSETS bucket for the mergeAfter you run it, you'll get:A full inventory of every scattered Casa Companion folderA .ps1 script you can review before executingA checklist for manual merge decisionsRun it, paste the results back, and I'll help you decide the merge order. BAMMMM.                                               ```text
     C:\Users\Dekan AI Brother\EPO_CROWDSOURCE_COMMAND_CENTER\
   ```

   What was built

   • 137 directories following the exact 00-99 hierarchy you specified
   • 118 files, including .gitkeep files to preserve empty folders in version control
   • 29 substantive starter files:
       • Master README.md
       • .gitignore for credentials and large data
       • Project charter docs (scope, roles, stakeholders)
       • Legal/ethical docs (GDPR, EPO terms, contributor agreements)
       • OPS API config (api_endpoints.json, rate_limits.yaml, ops_credentials.env.example)
       • Python automation scripts (ops_api_client.py, data_parser.py, batch_processor.py)
       • requirements.txt
       • Workflow docs (ingestion pipeline, QC checklist, escalation)
       • API reference guide and CQL cheatsheet
       • Contributor handbook and troubleshooting guide
       • Naming-standards doc and 4 templates (file naming, folder, report, task)

   Key conventions applied

   • Folder names: [NUMBER]_[CATEGORY]_[SpecificName]
   • File names: YYYY-MM-DD_[TYPE]_[Description]_[VERSION].[ext]
   • ISO 8601 dates, CPC/IPC tagging, raw/processed separation, quota logging, backup isolation

   Next steps you could take

   1. Copy ops_credentials.env.example to ops_credentials.env and add real credentials
   2. Install Python deps: pip install -r 05_COMMAND_CENTER/05b_Scripts/python/requirements.txt
   3. Add contributors and tasks under 02_CROWDSOURCE/
   4. Schedule the first weekly status report in 00d_Reporting/weekly_status_reports/

   No actual API keys, secrets, or sensitive data were committed.
 ╭────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
 │ >

---

## 🤖 Kimi

I see the EPO Crowdsource Command Center structure was built out. But your question was about Casa Companion folder audit — did you run the prompt I gave you, or is this a different output?Let me clarify what you need:Option 1: You want me to adapt that EPO audit prompt for Casa Companion specifically?Option 2: You already ran the Casa Companion scan and this is partial output?Option 3: You want a unified prompt that audits BOTH projects (EPO + Casa Companion) across your Dekan AI Brother profile?If you want the Casa Companion specific scan, here's the refined Kimi Code prompt ready to paste:powershell   Copy # === KIMI CODE PROMPT: CASA COMPANION FOLDER AUDIT ===
# Paste into Kimi Code PowerShell

kimi "Scan C:\Users\Dekan AI Brother\ recursively. Find ALL folders matching:
- *casa* (any case)
- *companion* (any case)
- *cc-*
- *casa-companion*
- *casa_companion*

For each match output:
PATH | SIZE | LAST_MODIFIED | FILE_COUNT | CONTAINS (package.json/.git/static/images/videos/README)

Classify as:
[MASTER] = has package.json + .git + most recent
[PIPELINE] = image/video generation assets
[ARCHIVE] = old/backup versions
[STATIC] = images/videos only
[MISC] = other

Generate a PowerShell script that:
1. Creates C:\Users\Dekan AI Brother\_ARCHIVE\casa-companion\
2. Copies (not moves) all non-master folders there with date stamps
3. Extracts all images/videos to C:\Users\Dekan AI Brother\_ASSETS\casa-companion\
4. Leaves master untouched
5. Outputs a merge checklist

Return the audit table, classification, and the .ps1 script. DO NOT delete anything." Which direction you want? The EPO structure looks solid — 137 dirs deep, proper naming conventions. But Casa Companion is the scattered one we need to wrangle. Let me know if you want me to merge these into one mega-audit prompt for both projects.                                               https://github.com/simplebalance89-ai/casa-companion.git

 Good. Update todo list and provide summary.

 ● Used TodoList

 ● Provide final summary.

 ● Done. READMEs are now in place and pushed.

   READMEs created

   ┌──────────┬─────────────────────────────────┬──────────────────────────────────────────────────────────────┐
   │ README   │ Path                            │ Purpose                                                      │
   ├──────────┼─────────────────────────────────┼──────────────────────────────────────────────────────────────┤
   │ Overall  │ casa-companion-master/README.md │ Repo structure, quick start, consolidation notes             │
   ├──────────┼─────────────────────────────────┼──────────────────────────────────────────────────────────────┤
   │ Backend  │ voice-agent/backend/README.md   │ FastAPI voice server setup, env vars, deploy, endpoints      │
   ├──────────┼─────────────────────────────────┼──────────────────────────────────────────────────────────────┤
   │ Frontend │ voice-agent/dashboard/README.md │ Next.js parent dashboard setup, env vars, deploy, API routes │
   └──────────┴─────────────────────────────────┴──────────────────────────────────────────────────────────────┘

   Also preserved

   • voice-agent/README.md — original detailed voice agent overview
   • README.legacy.md — pre-merge full project documentation
   • pipelines/hero-video/README.md — video pipeline docs

   Latest commit pushed to GitHub: 491239a docs: add backend and frontend READMEs.

 ✨ what is the hgithub repo full path

 ● The user is asking for the GitHub repo full path. From earlier we saw:
   - origin: https://github.com/simplebalance89-ai/casa-companion.git

   So the full path is `https://github.com/simplebalance89-ai/casa-companion.git`.

   I should answer directly.

 ● The GitHub repo full path is:

   ```
     https://github.com/simplebalance89-ai/casa-companion.git
   ```
 ╭────────────────────────────────────────────────────────────────

help me  create a prmot with instructions to use kimi deep research to review solution and add backlog with gap anlyhshysi and full optimization with what is good and bad in the solution

---

## 🧑 You

Here's your Kimi Code prompt to run a full deep research review on the Casa Companion repo, with gap analysis, backlog generation, and optimization recommendations:powershell   Copy # === KIMI CODE PROMPT: DEEP RESEARCH AUDIT — CASA COMPANION ===
# Paste into Kimi Code PowerShell

kimi "Perform a comprehensive deep research review of the Casa Companion project at:
https://github.com/simplebalance89-ai/casa-companion.git

Clone or pull the latest (commit 491239a) and analyze EVERYTHING.

## PHASE 1: ARCHITECTURE REVIEW
Document the full stack:
- Frontend: Next.js version, routing, state management, UI components, deployment config (Vercel)
- Backend: FastAPI structure, voice pipeline, API endpoints, database layer
- Voice: Whisper/Groq/Azure integration, real-time vs batch, latency bottlenecks
- Assets: Image-to-video pipeline, static folder organization, character media
- DevOps: CI/CD, env management, secrets handling, containerization

## PHASE 2: GAP ANALYSIS
Identify what's MISSING or BROKEN:
- [ ] Error handling & logging gaps
- [ ] Security holes (CORS, auth, input validation, API key exposure)
- [ ] Scalability limits (voice concurrency, asset storage, database)
- [ ] Test coverage (unit, integration, e2e)
- [ ] Documentation gaps (API docs, deployment runbooks, character onboarding guide)
- [ ] Performance issues (bundle size, API latency, video load times)
- [ ] Accessibility (WCAG, screen readers, keyboard nav)
- [ ] Mobile responsiveness
- [ ] Monitoring/observability (logs, metrics, alerting)
- [ ] Backup/disaster recovery

## PHASE 3: OPTIMIZATION RECOMMENDATIONS
For each GOOD thing found, explain WHY it's good and how to preserve it.
For each BAD thing found, provide:
- Severity (Critical / High / Medium / Low)
- Impact on users/developers
- Specific fix with code example or config change
- Effort estimate (hours/days)

## PHASE 4: BACKLOG GENERATION
Create a prioritized backlog in this format:

| Priority | Task | Category | Effort | Blockers | Owner |
|----------|------|----------|--------|----------|-------|
| P0 | [Critical fix] | [security/perf/etc] | [time] | [none/dep] | [suggested] |

Backlog categories:
- SECURITY
- PERFORMANCE
- RELIABILITY
- SCALABILITY
- DX (Developer Experience)
- UX (User Experience)
- INFRA
- CONTENT (characters/assets)

## PHASE 5: COMPARATIVE ANALYSIS
Compare against best practices for:
- AI voice apps (ElevenLabs, Bland, Retell patterns)
- Character-based UIs (Character.AI, Replika, AI companion apps)
- Vercel/Next.js production deployments
- FastAPI production patterns

## OUTPUT FORMAT
Generate 3 files in C:\Users\Dekan AI Brother\casa-companion-master\docs\:

1. `deep-research-audit.md` — Full architecture review + gap analysis
2. `optimization-roadmap.md` — Good/bad breakdown + fixes with code
3. `backlog-prioritized.md` — The full prioritized backlog table

DO NOT modify any source code. Only read, analyze, and document. Include specific file paths and line numbers for every issue found." What this gives you:Architecture map — full stack documented so any dev can onboard in 10 minutesSecurity/perf audit — catches the holes before they bite you in productionPrioritized backlog — P0 to P4 so you and Andrew know what to tackle firstCode-level fixes — not vague advice, actual snippets you can pasteBenchmarked against real AI voice apps (ElevenLabs, Retell) so you know if you're competitiveRun it, then paste the audit results back and I'll help you break the P0s into sprints. Bellisima.                                               i need a bteedeeper dive front and back end prompt review we need to move the tidal and spotify mcp to kimie as well with kimi prompts palyliust etc   
 ● Used TodoList

 ● Provide final summary of the audit.

 ● Audit complete. Report saved to:

   ```text
     C:\Users\Dekan AI Brother\RUNWAY_SECURITY_AUDIT.md
   ```

   Summary of runway repo audit

   Project: Runway — Next.js 14 music discovery dashboard with Supabase, Spotify, and Tidal OAuth.

   🔴 Critical (2)

   1. Hardcoded Supabase service-role + anon keys in 8 files (scripts/*.mjs, agents/runway_client.py). The service-role key bypasses RLS and exposes the
   user_tokens table containing Spotify/Tidal tokens.
   2. Command injection in /api/feed/scrape via execSync with interpolated user input.

   🟠 High (3)

   3. Middleware doesn't verify JWT signature — only checks token shape, so auth is bypassable.
   4. Custom /api/auth/login reimplements Supabase auth and sets cookies manually.
   5. Missing authorization checks on playlist delete/sync/edit — any user can mutate any playlist.

   🟡 Medium (5)

   6. agent_runs UPDATE RLS policy allows any authenticated user to update any run.
   7. tracks INSERT policy allows spoofing discovered_by.
   8. .env.local.example tracked in Git.
   9. Python venv/ inside the Node repo.
   10. Verbose logging of partial credentials in Tidal OAuth routes.

   🟢 Low / Info (4)

   11. README is significantly out of date.
   12. Missing input validation on several routes.
   13. Overly broad Tidal image remote pattern.
   14. Hardcoded production URL fallback.

   Top 3 actions you should take right now

   1. Rotate the Supabase service-role key and move all keys to env vars.
   2. Fix the command injection in app/api/feed/scrape/route.ts (use execFile).
   3. Rewrite middleware.ts to use @supabase/ssr and actually validate the session.

   Want me to start fixing any of these issues?

---

## 🤖 Kimi

I see the Runway audit surfaced critical security issues — hardcoded Supabase keys, command injection, auth bypass. But you're asking for a deeper dive on Casa Companion specifically, plus migrating the Tidal/Spotify MCP integration to Kimi with playlist prompts.Here's the refined prompt:powershell   Copy # === KIMI CODE PROMPT: CASA COMPANION DEEP DIVE + MCP MIGRATION ===
# Paste into Kimi Code PowerShell

kimi "Perform an exhaustive deep-dive review of Casa Companion at:
https://github.com/simplebalance89-ai/casa-companion.git

## PART 1: FRONTEND FORENSICS
Analyze the Next.js frontend layer in voice-agent/dashboard/ or equivalent:

- Component hierarchy: map every page, layout, and shared component
- State management: how is voice state, character selection, and session data handled?
- Asset pipeline: how do images load? Lazy loading? Video preloading? WebGL/Three.js usage?
- Voice UI: microphone component, transcript display, character response rendering
- Character cards: how are they rendered? Static or dynamic? Image-to-video transition logic
- Mobile: responsive breakpoints, touch handling, audio autoplay policies
- Performance: bundle analysis, Core Web Vitals, Lighthouse score estimate
- Accessibility: ARIA labels, keyboard navigation, focus management, screen reader support

Identify specific files and line numbers for:
- Memory leaks (event listeners not cleaned up)
- Race conditions (async voice state updates)
- Re-render storms (React.memo missing, context misuse)
- Audio context suspension issues (browser autoplay blocking)

## PART 2: BACKEND FORENSICS
Analyze the FastAPI backend in voice-agent/backend/ or equivalent:

- Endpoint inventory: list every route, method, payload shape, response schema
- Voice pipeline: request flow from mic → transcription → LLM → TTS → playback
- Concurrency: how many simultaneous voice sessions? WebSocket vs HTTP polling?
- Database: schema, migrations, connection pooling, query patterns
- Caching: Redis? In-memory? TTL strategies?
- Error handling: try/catch coverage, fallback behaviors, retry logic
- Rate limiting: per-user, per-endpoint, global?
- Logging: structured? PII scrubbing? Alerting hooks?

Identify specific files and line numbers for:
- Unhandled exceptions (missing try/catch)
- N+1 queries (inefficient DB patterns)
- Blocking I/O in async routes
- Missing input validation (pydantic gaps)
- Secret leakage (hardcoded keys, debug endpoints)

## PART 3: SECURITY AUDIT (Apply Runway lessons learned)
Based on the RUNWAY_SECURITY_AUDIT.md findings, audit Casa Companion for:
- [ ] Hardcoded API keys (OpenAI, Azure, Groq, Whisper, ElevenLabs)
- [ ] Auth implementation: JWT validation, session management, RLS policies
- [ ] Input sanitization: XSS, SQL injection, command injection risks
- [ ] CORS configuration: overly permissive?
- [ ] File upload handling: path traversal, mime type validation
- [ ] Rate limiting: missing or bypassable?
- [ ] Environment variable exposure: .env in git, debug logs leaking secrets

## PART 4: MCP MIGRATION — TIDAL & SPOTIFY
Design a Kimi-native MCP (Model Context Protocol) integration:

### Tidal MCP
- OAuth flow: user connects Tidal → tokens stored securely → Kimi can query
- Capabilities:
  - Search tracks, albums, artists
  - Get user playlists
  - Create/modify playlists
  - Get playback state/recommendations
- Kimi prompts for:
  - 'Find me songs like [character vibe] — e.g., Pietro's morning coffee playlist'
  - 'Create a playlist for [character] based on their personality'
  - 'What's trending in [genre] this week?'

### Spotify MCP
- OAuth flow: parallel to Tidal, shared token storage
- Capabilities:
  - Search, user playlists, recommendations, audio features
  - Cross-reference with Tidal for availability
- Kimi prompts for:
  - 'Build a playlist for Cassita beach vibes'
  - 'Find underground tracks matching [character] energy'
  - 'Sync this Tidal playlist to Spotify'

### Unified Music Agent
- Single interface that queries BOTH Tidal and Spotify
- Fallback logic: if track unavailable on one, check the other
- Playlist generation: Kimi creates based on character personality + user context
- Output: generate .mcp JSON configs and Kimi prompt templates

## PART 5: OPTIMIZATION SCORECARD
Rate each subsystem 1-10 with justification:

| Subsystem | Score | Why | Fix Priority |
|-----------|-------|-----|--------------|
| Frontend Performance | ? | ? | ? |
| Backend Scalability | ? | ? | ? |
| Voice Pipeline Latency | ? | ? | ? |
| Security Posture | ? | ? | ? |
| Developer Experience | ? | ? | ? |
| Asset Pipeline | ? | ? | ? |

## OUTPUT FILES
Generate in C:\Users\Dekan AI Brother\casa-companion-master\docs\:

1. `frontend-forensics.md` — Component map, performance issues, specific line fixes
2. `backend-forensics.md` — Endpoint inventory, DB schema, async issues, line fixes
3. `security-audit.md` — Critical/high/medium/low findings (mirror Runway format)
4. `mcp-migration-plan.md` — Tidal + Spotify MCP architecture + Kimi prompt templates
5. `optimization-scorecard.md` — 1-10 ratings + improvement roadmap

DO NOT modify source code. Read-only audit. Include exact file paths and line numbers." What this covers:Frontend deep dive — catches the React render storms and audio context issues that kill voice appsBackend deep dive — maps every endpoint, finds the N+1s and blocking I/OSecurity audit — applies the Runway hardcoded-key lesson so you don't ship the same CVEsMCP migration — full Tidal + Spotify integration spec with Kimi prompt templates for character-based playlistsScorecard — so you know which subsystem is the bottleneck before you scaleRun it, paste results back, and I'll help you prioritize the P0s across both Casa Companion and Runway. BAMMMM.                                               this was for another repo runway ● Create casa-companion-master/docs directory
   ○ Read frontend files and map components
   ○ Read backend files and map endpoints
   ○ Perform security audit based on Runway findings
   ○ Design MCP migration plan
   … +2 more
 ╭────────────────────────

---

## 🧑 You

Got it — you want the same deep-dive treatment applied to Casa Companion that was done for Runway. Here's the prompt:powershell   Copy # === KIMI CODE PROMPT: CASA COMPANION DEEP-DIVE AUDIT ===
# Paste into Kimi Code PowerShell

kimi "Clone or pull latest from https://github.com/simplebalance89-ai/casa-companion.git
Create directory casa-companion-master/docs/ if not exists.

Perform the following read-only forensic audit:

## FRONTEND FORENSICS
Read all files in the frontend/dashboard/Next.js layer:
- Map every page, layout, component, and hook
- Document state management (React context, Zustand, Redux, or other)
- Identify voice UI components: microphone, transcript, character response, audio player
- Map character card rendering: static vs dynamic, image-to-video transitions
- Find asset loading patterns: lazy loading, preloading, WebGL/Three.js usage
- Check mobile responsiveness, touch handling, audio autoplay policies
- Identify performance issues: bundle bloat, re-render storms, missing React.memo
- Check accessibility: ARIA labels, keyboard nav, focus management, screen readers

For each issue found: provide exact file path, line number, severity (Critical/High/Medium/Low), and fix recommendation.

## BACKEND FORENSICS
Read all files in the backend/FastAPI layer:
- Inventory every API endpoint: route, method, request schema, response schema
- Map voice pipeline flow: mic input → transcription → LLM → TTS → audio output
- Document concurrency model: WebSocket vs HTTP polling, max simultaneous sessions
- Map database schema: tables, relationships, migrations, connection pooling
- Check caching strategy: Redis, in-memory, TTL
- Audit error handling: try/catch coverage, fallback behaviors, retry logic
- Check rate limiting: per-user, per-endpoint, global
- Audit logging: structured vs unstructured, PII scrubbing, alerting hooks

For each issue: exact file path, line number, severity, fix.

## SECURITY AUDIT (Apply Runway lessons)
Check for these specific vulnerabilities:
- [ ] Hardcoded API keys (OpenAI, Azure, Groq, Whisper, ElevenLabs, Supabase)
- [ ] Auth bypass: JWT validation gaps, session management flaws, RLS policy issues
- [ ] Input sanitization: XSS, SQL injection, command injection risks
- [ ] CORS misconfiguration: overly permissive origins
- [ ] File upload handling: path traversal, mime type spoofing, size limits
- [ ] Rate limiting: missing or bypassable
- [ ] Environment exposure: .env files in git, debug logs leaking secrets
- [ ] Dependency vulnerabilities: outdated packages with known CVEs

Output severity matrix: Critical/High/Medium/Low with exact file paths and line numbers.

## MCP MIGRATION — TIDAL & SPOTIFY
Design Kimi-native MCP integration for music:

### Tidal MCP
- OAuth flow: user auth → secure token storage → Kimi query capability
- Endpoints: search, playlists, recommendations, playback state
- Kimi prompts:
  - 'Create a [character] playlist based on their personality'
  - 'Find tracks matching [vibe/mood] for [character]'
  - 'What's trending in [genre] this week?'

### Spotify MCP
- OAuth flow: parallel to Tidal, shared token storage
- Endpoints: search, user playlists, recommendations, audio features
- Kimi prompts:
  - 'Build a beach vibes playlist for Cassita'
  - 'Find underground tracks matching [character] energy'
  - 'Cross-reference this Tidal playlist on Spotify'

### Unified Music Agent
- Single interface querying both Tidal and Spotify
- Fallback: track unavailable on one → check the other
- Character-aware playlist generation: personality + context + music taste
- Output: .mcp JSON configs + Kimi prompt templates

## OPTIMIZATION SCORECARD
Rate each subsystem 1-10:

| Subsystem | Score | Justification | Priority Fix |
|-----------|-------|---------------|--------------|
| Frontend Performance | ? | ? | ? |
| Backend Scalability | ? | ? | ? |
| Voice Pipeline Latency | ? | ? | ? |
| Security Posture | ? | ? | ? |
| Developer Experience | ? | ? | ? |
| Asset Pipeline | ? | ? | ? |
| MCP Integration | ? | ? | ? |

## OUTPUT FILES
Write to casa-companion-master/docs/:

1. `frontend-forensics.md` — Component map + performance issues + line fixes
2. `backend-forensics.md` — Endpoint inventory + DB schema + async issues
3. `security-audit.md` — Severity matrix (mirror RUNWAY_SECURITY_AUDIT.md format)
4. `mcp-migration-plan.md` — Tidal + Spotify architecture + Kimi prompts
5. `optimization-scorecard.md` — 1-10 ratings + improvement roadmap

DO NOT modify any source code. Read-only audit. Include exact file paths and line numbers for every finding." This mirrors the Runway audit format but applied to Casa Companion's specific architecture (voice pipeline, character system, image-to-video assets). Run it and paste the security findings back first — those are the ones that'll bite you before launch. BAMMMM.                                              README.md md 5.36 kb

---

## 🤖 Kimi

I see the uploaded README is for Runway, not Casa Companion. But your request is clear — you want the same deep-dive audit structure applied to Casa Companion, plus the Tidal/Spotify MCP migration plan with Kimi prompts.Here's the prompt ready to paste:powershell   Copy # === KIMI CODE PROMPT: CASA COMPANION DEEP-DIVE AUDIT ===
# Paste into Kimi Code PowerShell

kimi "Clone or pull latest from https://github.com/simplebalance89-ai/casa-companion.git
Create directory casa-companion-master/docs/ if not exists.

Perform the following read-only forensic audit:

## FRONTEND FORENSICS
Read all files in the frontend/dashboard/Next.js layer:
- Map every page, layout, component, and hook
- Document state management (React context, Zustand, Redux, or other)
- Identify voice UI components: microphone, transcript, character response, audio player
- Map character card rendering: static vs dynamic, image-to-video transitions
- Find asset loading patterns: lazy loading, preloading, WebGL/Three.js usage
- Check mobile responsiveness, touch handling, audio autoplay policies
- Identify performance issues: bundle bloat, re-render storms, missing React.memo
- Check accessibility: ARIA labels, keyboard nav, focus management, screen readers

For each issue found: provide exact file path, line number, severity (Critical/High/Medium/Low), and fix recommendation.

## BACKEND FORENSICS
Read all files in the backend/FastAPI layer:
- Inventory every API endpoint: route, method, request schema, response schema
- Map voice pipeline flow: mic input → transcription → LLM → TTS → audio output
- Document concurrency model: WebSocket vs HTTP polling, max simultaneous sessions
- Map database schema: tables, relationships, migrations, connection pooling
- Check caching strategy: Redis, in-memory, TTL
- Audit error handling: try/catch coverage, fallback behaviors, retry logic
- Check rate limiting: per-user, per-endpoint, global
- Audit logging: structured vs unstructured, PII scrubbing, alerting hooks

For each issue: exact file path, line number, severity, fix.

## SECURITY AUDIT (Apply Runway lessons)
Check for these specific vulnerabilities:
- [ ] Hardcoded API keys (OpenAI, Azure, Groq, Whisper, ElevenLabs, Supabase)
- [ ] Auth bypass: JWT validation gaps, session management flaws, RLS policy issues
- [ ] Input sanitization: XSS, SQL injection, command injection risks
- [ ] CORS misconfiguration: overly permissive origins
- [ ] File upload handling: path traversal, mime type spoofing, size limits
- [ ] Rate limiting: missing or bypassable
- [ ] Environment exposure: .env files in git, debug logs leaking secrets
- [ ] Dependency vulnerabilities: outdated packages with known CVEs

Output severity matrix: Critical/High/Medium/Low with exact file paths and line numbers.

## MCP MIGRATION — TIDAL & SPOTIFY
Design Kimi-native MCP integration for music:

### Tidal MCP
- OAuth flow: user auth → secure token storage → Kimi query capability
- Endpoints: search, playlists, recommendations, playback state
- Kimi prompts:
  - 'Create a [character] playlist based on their personality'
  - 'Find tracks matching [vibe/mood] for [character]'
  - 'What's trending in [genre] this week?'

### Spotify MCP
- OAuth flow: parallel to Tidal, shared token storage
- Endpoints: search, user playlists, recommendations, audio features
- Kimi prompts:
  - 'Build a beach vibes playlist for Cassita'
  - 'Find underground tracks matching [character] energy'
  - 'Cross-reference this Tidal playlist on Spotify'

### Unified Music Agent
- Single interface querying both Tidal and Spotify
- Fallback: track unavailable on one → check the other
- Character-aware playlist generation: personality + context + music taste
- Output: .mcp JSON configs + Kimi prompt templates

## OPTIMIZATION SCORECARD
Rate each subsystem 1-10:

| Subsystem | Score | Justification | Priority Fix |
|-----------|-------|---------------|--------------|
| Frontend Performance | ? | ? | ? |
| Backend Scalability | ? | ? | ? |
| Voice Pipeline Latency | ? | ? | ? |
| Security Posture | ? | ? | ? |
| Developer Experience | ? | ? | ? |
| Asset Pipeline | ? | ? | ? |
| MCP Integration | ? | ? | ? |

## OUTPUT FILES
Write to casa-companion-master/docs/:

1. `frontend-forensics.md` — Component map + performance issues + line fixes
2. `backend-forensics.md` — Endpoint inventory + DB schema + async issues
3. `security-audit.md` — Severity matrix (mirror RUNWAY_SECURITY_AUDIT.md format)
4. `mcp-migration-plan.md` — Tidal + Spotify architecture + Kimi prompts
5. `optimization-scorecard.md` — 1-10 ratings + improvement roadmap

DO NOT modify any source code. Read-only audit. Include exact file paths and line numbers for every finding." Key differences from Runway audit:Voice pipeline forensics (not just music discovery)Character system analysis (image-to-video, personality engine)MCP migration designed for Kimi-native prompts (not Claude Code)Asset pipeline scoring (your hero video pipeline is unique to Casa Companion)Run it and paste the security findings back first — those are the P0s that'll block launch. BAMMMM.                                               this prompt si s wrong its runway  local director i  "C:\Users\Dekan AI Brother\runway"

---

## 🧑 You

Got it — you want the Runway repo audited at your local path C:\Users\Dekan AI Brother\runway, not Casa Companion. Here's the corrected prompt:powershell   Copy # === KIMI CODE PROMPT: RUNWAY LOCAL DEEP-DIVE AUDIT ===
# Paste into Kimi Code PowerShell

kimi "Read the entire Runway project at C:\Users\Dekan AI Brother\runway\
Create directory C:\Users\Dekan AI Brother\runway\docs\ if not exists.

Perform the following read-only forensic audit:

## FRONTEND FORENSICS
Read all files in app/ and components/:
- Map every page, layout, component, and hook
- Document state management (React context, Zustand, Redux, or other)
- Map music discovery UI: dashboard, playlists, prompts, ratings, feed pages
- Check Supabase client integration: browser vs server, auth handling
- Identify data fetching patterns: Server Components, Client Components, caching
- Check mobile responsiveness, dark mode implementation, Tailwind config
- Identify performance issues: bundle bloat, re-render storms, missing React.memo
- Check accessibility: ARIA labels, keyboard nav, focus management

For each issue: exact file path, line number, severity (Critical/High/Medium/Low), fix recommendation.

## BACKEND FORENSICS
Read all files in app/api/:
- Inventory every API endpoint: route, method, request schema, response schema
- Map MCP agent integration: /api/discover, playlist creation, feed ingestion
- Document database operations: Supabase queries, RLS bypass with service role key
- Check error handling: try/catch coverage, fallback behaviors
- Audit logging: structured vs unstructured, PII scrubbing
- Check rate limiting: missing or bypassable

For each issue: exact file path, line number, severity, fix.

## SECURITY AUDIT (Deep dive based on prior findings)
Verify these specific vulnerabilities from RUNWAY_SECURITY_AUDIT.md:
- [ ] Hardcoded Supabase keys in scripts/*.mjs and agents/runway_client.py
- [ ] Command injection in /api/feed/scrape via execSync
- [ ] Middleware JWT validation gaps — only checks token shape
- [ ] Custom /api/auth/login reimplementing Supabase auth
- [ ] Missing authorization on playlist delete/sync/edit
- [ ] agent_runs UPDATE RLS policy allowing any user to update any run
- [ ] tracks INSERT policy allowing spoofing discovered_by
- [ ] .env.local.example tracked in Git
- [ ] Python venv/ inside Node repo
- [ ] Verbose credential logging in Tidal OAuth routes

Check for ADDITIONAL vulnerabilities:
- [ ] SQL injection via raw Supabase queries
- [ ] XSS in feed item rendering
- [ ] CSRF protection missing
- [ ] Session fixation risks
- [ ] Dependency vulnerabilities (npm audit)

Output severity matrix: Critical/High/Medium/Low with exact file paths and line numbers.

## MCP MIGRATION — TIDAL & SPOTIFY TO KIMI
Design Kimi-native MCP integration replacing current Claude-centric setup:

### Tidal MCP
- OAuth flow: user auth → secure token storage → Kimi query capability
- Endpoints: search, playlists, recommendations, playback state
- Kimi prompts:
  - 'Discover tracks for Dekan vs Jim taste profiles'
  - 'Find peak time techno matching [prompt_name] energy'
  - 'What's trending on Beatport this week?'

### Spotify MCP
- OAuth flow: parallel to Tidal, shared token storage
- Endpoints: search, user playlists, recommendations, audio features
- Kimi prompts:
  - 'Build a KIMI_ playlist for [genre] with [bpm_min]-[bpm_max] range'
  - 'Cross-reference Tidal discoveries on Spotify'
  - 'Find underground tracks matching [agent] style'

### Unified Music Agent
- Single interface querying both Tidal and Spotify
- Fallback: track unavailable on one → check the other
- Agent-aware: KIMI vs CLAUDE discovery styles, prompt templates
- Rekordbox export integration
- Output: .mcp JSON configs + Kimi prompt templates

## OPTIMIZATION SCORECARD
Rate each subsystem 1-10:

| Subsystem | Score | Justification | Priority Fix |
|-----------|-------|---------------|--------------|
| Frontend Performance | ? | ? | ? |
| Backend Scalability | ? | ? | ? |
| MCP Integration | ? | ? | ? |
| Security Posture | ? | ? | ? |
| Developer Experience | ? | ? | ? |
| Database Design | ? | ? | ? |
| Music Discovery Pipeline | ? | ? | ? |

## OUTPUT FILES
Write to C:\Users\Dekan AI Brother\runway\docs\:

1. `frontend-forensics.md` — Component map + performance issues + line fixes
2. `backend-forensics.md` — Endpoint inventory + DB issues + async problems
3. `security-audit.md` — Severity matrix (all findings, mirror prior format)
4. `mcp-migration-plan.md` — Tidal + Spotify Kimi architecture + prompt templates
5. `optimization-scorecard.md` — 1-10 ratings + improvement roadmap

DO NOT modify any source code. Read-only audit. Include exact file paths and line numbers for every finding." This targets your local Runway folder at C:\Users\Dekan AI Brother\runway\ and builds on the prior security audit. Run it and paste the security findings back — those hardcoded Supabase keys need rotation ASAP. BAMMMM.                                              Files created.txt txt 4.38 kb

---

## 🤖 Kimi

I see the audit ran and generated all 5 docs at C:\Users\Dekan AI Brother\runway\docs\. Here's the Kimi Code prompt to read those files and produce a consolidated action plan with the Tidal/Spotify MCP migration to Kimi:powershell   Copy # === KIMI CODE PROMPT: CONSOLIDATED RUNWAY ACTION PLAN + MCP MIGRATION ===
# Paste into Kimi Code PowerShell

kimi "Read all 5 audit files from C:\Users\Dekan AI Brother\runway\docs\:
1. frontend-forensics.md
2. backend-forensics.md
3. security-audit.md
4. mcp-migration-plan.md
5. optimization-scorecard.md

## TASK 1: CRITICAL PATH FIXES
From security-audit.md, extract the 2 Critical + top 5 High findings.
For each, generate:
- Exact file path and line number (already in audit)
- One-sentence impact: what breaks if not fixed
- Fix code snippet (ready to paste)
- Estimated time to fix

Priority order:
1. Rotate hardcoded Supabase service-role keys (affects all agent scripts)
2. Fix middleware.ts JWT validation bypass (affects all auth)
3. Fix custom /api/auth/login cookie security (affects session hijacking)
4. Add authorization checks to playlist mutations (affects data integrity)
5. Tighten RLS policies on agent_runs, tracks, playlists (affects row-level security)

## TASK 2: MCP MIGRATION — EXECUTABLE PLAN
From mcp-migration-plan.md, generate the ACTUAL implementation files:

### Kimi Tidal MCP Server
Create: C:\Users\Dekan AI Brother\runway\kimi-mcp\tidal\
- `server.json` — MCP server config with OAuth endpoints
- `prompts/discover.md` — Kimi prompt for track discovery
- `prompts/playlist.md` — Kimi prompt for playlist creation
- `prompts/trending.md` — Kimi prompt for trending tracks

### Kimi Spotify MCP Server
Create: C:\Users\Dekan AI Brother\runway\kimi-mcp\spotify\
- `server.json` — MCP server config with OAuth endpoints
- `prompts/discover.md` — Kimi prompt for track discovery
- `prompts/playlist.md` — Kimi prompt for playlist creation
- `prompts/crossref.md` — Kimi prompt for Tidal→Spotify cross-reference

### Unified Music Agent
Create: C:\Users\Dekan AI Brother\runway\kimi-mcp\agent\
- `config.json` — Unified agent routing Tidal vs Spotify
- `prompts/orchestrator.md` — Kimi prompt that decides which service to query
- `fallback.md` — Fallback logic when track unavailable on primary service

### Prompt Templates (Kimi-native)
Each prompt must include:
- Context: Dekan vs Jim taste profiles, agent identity (KIMI vs CLAUDE)
- Parameters: genre, bpm_min, bpm_max, energy, timeframe, limit
- Output format: JSON matching the tracks table schema
- Example: 'KIMI, discover peak time techno 130-140 BPM, high energy, last 30 days, limit 20'

## TASK 3: OPTIMIZATION ROADMAP
From optimization-scorecard.md, extract the lowest-scoring subsystem.
Generate a 5-phase improvement plan:
- Phase 1: Security hardening (week 1)
- Phase 2: MCP migration + auth fix (week 2)
- Phase 3: Performance optimization (week 3)
- Phase 4: Database tuning + caching (week 4)
- Phase 5: Monitoring + alerting (week 5)

Each phase: specific files to touch, expected outcome, success metric.

## TASK 4: MERGE CHECKLIST
Generate a single markdown file: C:\Users\Dekan AI Brother\runway\MERGE_CHECKLIST.md
Sections:
- [ ] Pre-merge: rotate all secrets, backup DB
- [ ] Security fixes: checklist of 5 critical/high fixes
- [ ] MCP migration: Tidal + Spotify server setup steps
- [ ] Testing: verify playlist CRUD, feed scrape, auth flow
- [ ] Deploy: Vercel env vars update, smoke test
- [ ] Post-merge: monitor logs, verify agent runs

## OUTPUT
Write all generated files to disk. Do NOT modify existing source code.
Only create new files in kimi-mcp/ and MERGE_CHECKLIST.md." What this gives you:Critical fixes with copy-pasteable code snippets for the 2 Critical + 5 High security issuesActual MCP server configs — .json + .md prompt files ready to wire into KimiUnified agent that routes between Tidal/Spotify with fallback logic5-phase roadmap so you and Andrew can sprint this week-by-weekMerge checklist so nothing gets forgotten when you push to VercelRun it, then paste the MERGE_CHECKLIST back if you want me to tighten the deploy steps. BAMMMM.                                               New files created

   Critical path fixes
   • CRITICAL_PATH_FIXES.md — 288 lines with ready-to-paste snippets for the 2 critical + 5 high-severity issues

   Merge checklist
   • MERGE_CHECKLIST.md — 120-line pre-merge / security / MCP / testing / deploy / post-merge checklist

   Kimi MCP servers

   ```
     kimi-mcp/
     ├── tidal/
     │   ├── server.json
     │   └── prompts/
     │       ├── discover.md
     │       ├── playlist.md
     │       └── trending.md
     ├── spotify/
     │   ├── server.json
     │   └── prompts/
     │       ├── discover.md
     │       ├── playlist.md
     │       └── crossref.md
     └── agent/
         ├── config.json
         ├── fallback.md
         └── prompts/
             └── orchestrator.md
   ```

   What each file contains

   • Tidal/Spotify server.json — MCP server configs with OAuth endpoints, tool schemas, and env-var placeholders
   • Prompts — Kimi-native prompts for discover, playlist creation, trending, and cross-reference
   • agent/config.json — Unified agent routing, Dekan/Jim taste profiles, KIMI/CLAUDE styles, fallback rules
   • agent/fallback.md — Cross-service fallback logic with ISRC → title+artist matching
   • agent/prompts/orchestrator.md — Master prompt that decides which service to query and merges results

   Critical fixes covered

   1. Rotate hardcoded Supabase/Tidal/Spotify keys
   2. Rewrite middleware.ts to validate JWT via @supabase/ssr
   3. Replace custom /api/auth/login with secure SSR cookies
   4. Add user_id ownership checks to all playlist mutations
   5. Tighten RLS policies on playlists, tracks, agent_runs

   No existing source code was modified.
 ╭─────────────────────────────────────────────

---

## 🧑 You

All files generated. Here's your next-step prompt to execute the critical fixes safely:powershell   Copy # === KIMI CODE PROMPT: EXECUTE CRITICAL FIXES — RUNWAY ===
# Paste into Kimi Code PowerShell

kimi "Read C:\Users\Dekan AI Brother\runway\docs\CRITICAL_PATH_FIXES.md
Execute ONLY the 2 Critical fixes first. Do NOT touch High/Medium/Low yet.

## FIX 1: ROTATE HARDCODED KEYS
- Identify every file with hardcoded Supabase service-role, Tidal, or Spotify keys
- Replace with process.env.VAR_NAME references
- Add the new env var names to .env.local.example
- Generate a key-rotation script that outputs:
  - Old key location (file:line)
  - New env var name
  - Whether rotation is needed (Supabase dashboard, Tidal dev portal, Spotify dev portal)

## FIX 2: REWRITE MIDDLEWARE JWT VALIDATION
- Read current middleware.ts
- Replace token-shape check with @supabase/ssr createMiddlewareClient validation
- Ensure session is verified against Supabase auth server
- Add redirect to /login on invalid session
- Preserve existing route protection logic

## SAFETY RULES
- Create .bak files for every modified file
- Write changes to a new branch or timestamped backup folder
- Do NOT commit or push
- Output a diff showing before/after for each fix

After both fixes, run a syntax check:
- npm run build (catch TypeScript errors)
- node -c on any modified .js/.mjs files

If build fails, revert to .bak and report the error.

DO NOT proceed to High fixes until Critical fixes pass build." Why this order:Key rotation first — because every other fix is meaningless if keys are still exposed in git historyMiddleware fix second — because auth bypass affects all routes, including the playlist mutationsBuild check — catches the TypeScript breakage before you touch 16 High-severity filesAfter this passes, paste the diff back and I'll give you the prompt for the 5 High fixes. BAMMMM.                                                       Ask away. Pics work too.                       K2.6 Instant

---
