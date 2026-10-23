# Kimi Chat Scraper

Export and consolidate your Kimi chat history from the **web app** and the **Windows desktop app** into a clean, organized archive.

- **WebBridge automation (recommended):** drives your real Chrome browser through the already-installed Kimi WebBridge and extracts every chat automatically.
- **Tampermonkey web exporter:** manual one-click export if you prefer not to use the WebBridge.
- **Desktop DevTools snippet:** for the desktop app, where local IndexedDB data is encrypted.
- **Consolidate:** Python script that merges exports from all sources, removes duplicates, and writes one folder per chat.
- **Profile builder:** groups consolidated chats into self-contained project profiles you can paste into new Kimi chats as one-off context.

> ⚠️ The Kimi desktop app encrypts local chat data in its WebView IndexedDB, so we cannot read it directly from disk. The desktop extractor works while the app is running and decrypting data in memory.

---

## Project Layout

```
kimi-chat-scraper/
├── src/
│   ├── webbridge_extractor.py         # Automated Chrome extraction via Kimi WebBridge
│   ├── kimi_web_exporter.user.js      # Tampermonkey script for the web app
│   ├── kimi_desktop_extractor.js      # DevTools snippet for the desktop app
│   ├── consolidate.py                 # Python merger / deduplicator
│   └── build_profiles.py              # Group chats into project-profile Markdown files
├── tests/
│   └── test_consolidate.py            # Unit tests for the consolidator
├── pyproject.toml
└── README.md
```

---

## Quick Start

### 1. Install Python dependencies

```powershell
cd "C:\Users\Dekan AI Brother\Projects\ACTIVE\kimi-chat-scraper"
python -m venv .venv
.venv\Scripts\python -m pip install -e ".[dev]"
```

### 2. Automated extraction with Kimi WebBridge (recommended)

Prerequisites:
- Google Chrome is installed.
- The Kimi WebBridge browser extension is installed and enabled in Chrome.
- You are already logged into https://www.kimi.com/ in Chrome.

Run the extractor for your first account:

```powershell
.venv\Scripts\python src\webbridge_extractor.py --account-tag personal --max-chats 0
```

- `--account-tag` labels the export so you can tell accounts apart later.
- `--max-chats 0` exports every chat found. Use a number like `10` for a quick test.
- `--walk-delay 1500` waits 1.5s between chats; increase if your connection is slow.

To export a second login, switch Chrome profiles (or log out and into the other account), then run again with a different tag:

```powershell
.venv\Scripts\python src\webbridge_extractor.py --account-tag work --max-chats 0
```

Exports are saved to `exports/` as `kimi-webbridge-<account_tag>-<timestamp>.json`.

### 3. Alternative: export from the Kimi web app manually

1. Install the [Tampermonkey extension](https://www.tampermonkey.net/) in your browser.
2. Import `src/kimi_web_exporter.user.js` into Tampermonkey.
3. Open https://www.kimi.com/.
4. Click the 📥 **Export Kimi Chats** button and download the JSON.

### 4. Alternative: export from the Kimi desktop app

1. Open the Kimi desktop app.
2. Open DevTools (`Ctrl + Shift + I` or `F12`).
3. Paste the contents of `src/kimi_desktop_extractor.js` into the Console and press Enter.
4. Click the 📥 button or run `kimiAutoWalk()` to export.

### 5. Consolidate everything

```powershell
.venv\Scripts\python src\consolidate.py -i exports -o kimi-chat-archive
```

Output structure:

```
kimi-chat-archive/
├── index.json
├── personal/
│   ├── index.json
│   ├── 2026-07-02 - Project Planning/
│   │   ├── chat.json
│   │   └── chat.md
│   └── ...
└── work/
    └── ...
```

### 6. Build project profiles for one-off ingestion

```powershell
.venv\Scripts\python src\build_profiles.py -a kimi-chat-archive -o profiles
```

This creates self-contained Markdown files like `profiles\EC8 Edge Crew.md` that you can paste into a fresh Kimi chat to give it focused project context without dumping your whole archive.

---

## Running Tests

```powershell
.venv\Scripts\python -m pytest tests/ -v
```

---

## How It Works

- `webbridge_extractor.py` uses the Kimi WebBridge HTTP API to control Chrome, opens each chat, and extracts the conversation text from the rendered page. Messages are split into user/assistant turns using the "Edit Copy Share" action buttons as delimiters.
- The Tampermonkey userscript intercepts `fetch`/`XMLHttpRequest` and has a DOM-scraping fallback.
- The desktop extractor runs the same extraction logic inside the desktop app's WebView via DevTools.
- `consolidate.py` reads every export JSON, groups by `account_tag`, deduplicates by conversation ID (and by first/last user message content as a fallback), then writes one folder per chat containing both structured JSON and a human-readable Markdown transcript.

---

## Troubleshooting

| Problem | Likely Cause | Fix |
|---------|--------------|-----|
| "Extension did not connect" | Chrome is closed or the WebBridge extension is disabled | Open Chrome and enable the extension. |
| "No chats found" | Not logged into Kimi in Chrome | Log in at https://www.kimi.com/ first. |
| WebBridge command times out | Page is slow to load | Increase `--walk-delay`. |
| Only some chats export | Sidebar needs "All Chats" expansion | The script clicks it automatically; if it fails, click All Chats manually before running. |
| A chat exports as a single blob | The chat rendered after the assistant-turn delimiter check | A genuinely long single reply can be one message. Re-run after messages finish loading (the extractor retries empty panes and logs `capture: skipped (empty)`); if it stays a blob, that chat has no `Copy Share` markers. |
| `capture: skipped (...)` in the log | Per-chat miss is now classified on purpose | `wrong_path` = URL was not a `/chat/<uuid>` page (e.g. SPA redirect); `empty` = messages not rendered yet (retried). Both mean the chat was intentionally not exported, not silently lost. |
| Duplicate chats across sources | Web and desktop give different IDs | The consolidator merges by content signature too; make sure account tags match. |

---

## Design Documents

- `../docs/superpowers/specs/2026-07-02-kimi-chat-scraper-design.md`
- `../docs/superpowers/specs/2026-07-02-kimi-chat-scraper-webbridge-design.md`

# Purpose

Kimi Chat Scraper — Active.

# Status

Active

# Family Pod

- Lead: Sintonia
- Members: Costruito, Corvo

# Stack
- Languages: Python
- Apis: Kimi WebBridge

# Quick Commands

- `open kimi chat scraper`
- `audit kimi chat scraper`

# Backlog

See [BACKLOG.md](BACKLOG.md).

# Risks

- TBD
