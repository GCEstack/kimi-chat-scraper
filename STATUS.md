# Kimi Chat Scraper — Live Status

Generated: 2026-07-11 (refreshed after clean rebuild)

## Accounts (login mapping — NOT stored in export data)

| Tag | Login | Role (family model) |
| --- | --- | --- |
| **account1** | simplebalance89@gmail.com | ibis — work/run chat |
| **account2** | brother's phone number | squalo — outside-brain talk chat |

## Raw exports (`exports/`)

| File | Chats |
| --- | --- |
| account1 — 2026-07-03 | 55 |
| account1 — 2026-07-06 | 53 |
| account1 — 2026-07-10 | 16 |
| account2 — 2026-07-06 | 5 |
| account2 — 2026-07-10 | 16 |

## ✅ Clean archive (`kimi-chat-archive/`) — rebuilt 2026-07-11

Consolidated from all 5 exports, deduplicated by id + content signature:

- **account1:** 73 conversations
- **account2:** 20 conversations
- **Combined:** 93 conversations / 1,668 messages
- Each chat as `chat.json` + `chat.md`; `index.json` at root + per account.

> Old bloated archive (271 duplicate folders, accumulated `(1)`/`(2)` copies from
> re-runs) preserved at `kimi-chat-archive.old-bloated-20260710/`. Safe to delete
> once verified.

## ✅ Profiles (`profiles/`) — rebuilt 2026-07-11 (now includes 07-10 chats)

Built with `src/build_profiles.py` from the clean archive.

| Profile | Chats |
| ------- | ----- |
| EC8 Edge Crew | 57 |
| Kimi Code Ops | 36 |
| AI Models & APIs | 25 |
| Voice & Audio | 23 |
| Casa Companion | 18 |
| Heartbeat Family System | 12 |
| Media & Video | 6 |
| Creative & Brand | 5 |
| Desktop & File Org | 5 |
| Misc | 3 |

Self-contained Markdown — paste into a new Kimi chat for one-off context.

## To refresh again

```powershell
cd "C:\Users\Dekan AI Brother\Projects\ACTIVE\kimi-chat-scraper"
# 1. Scrape (per account). NOTE: output dir accumulates if not cleared first.
.venv\Scripts\python src\webbridge_extractor.py --account-tag <tag> --max-chats 0
# 2. Clean rebuild — wipe the archive dir first to avoid (N) duplicate folders:
rmdir /s /q kimi-chat-archive
.venv\Scripts\python src\consolidate.py -i exports -o kimi-chat-archive
# 3. Rebuild profiles
.venv\Scripts\python src\build_profiles.py -a kimi-chat-archive -o profiles
```

## Session 2026-07-11 (late-night) — progress log

- ✅ Diagnosed & fixed the `consolidate.py` duplicate-folder bug (it never overwrote/cleaned → accumulated `(1)`/`(2)` copies). Clean rebuild = 93 convos / 1668 msgs. Old bloated archive backed up at `kimi-chat-archive.old-bloated-20260710/`.
- ✅ Profiles rebuilt to include the 07-10 chats.
- ✅ Account→login mapping saved to Claude memory (not stored in export data): account1=ibis=simplebalance89@gmail.com; account2=squalo=Moonwalker5830=brother's phone.
- ✅ **Wrote `src/kimi_chat_deleter.user.js`** — Tampermonkey bulk-deleter that *learns* the delete API from one manual delete, then replays it. Dry-run by default, confirm gate, STOP button, live log. NOT YET INSTALLED.
- ✅ **account2 (Moonwalker5830) freshly pulled 07-11** → `exports/kimi-webbridge-account2-2026-07-11-065811.json` (16 chats). **NOT yet consolidated** — waiting so we do one clean rebuild after account1 too.
- ⏳ **account1 (simplebalance89, work) — last two days NOT pulled yet.** It lives in Edge (WebBridge is Chrome-only). Peter's pending decision: (a) install exporter in Edge, or (b) log simplebalance89 into a Chrome profile (his own Gmail — does NOT touch brother's phone). He leaned (b) then paused for the night.
- ⚠️ account1/account2 content overlaps (account2 has Casa/EC8/ROOKSWARM work chats). Not clean work-vs-talk. Consolidation dedups by content so harmless; just don't trust the ibis/squalo split as clean.

### Resume here tomorrow
1. Get account1's last-two-days export into `exports/` (Edge exporter OR Chrome profile + `webbridge_extractor.py --account-tag account1 --max-chats 0`). Safety check: extractor's init `chatCount` ≈ 73 = account1, ≈16 = account2 (wrong).
2. Clean re-consolidate: wipe `kimi-chat-archive`, run `consolidate.py`, then `build_profiles.py`. Report new counts.
3. Then bulk-delete (dry-run first) — install `kimi_chat_deleter.user.js`, learn on one manual delete, dry-run, confirm.

## Known follow-ups

- [ ] **Bulk-delete Kimi chats** from the live web/desktop app (P1, due 2026-07-11) — run `delete_kimi_chats.py --dry-run` first, then `--confirm`. Requires Chrome + WebBridge + logged-in target account.
- [ ] **Verify account separation:** account1 and account2 07-10 exports share near-identical chat titles — confirm the two scrapes didn't both grab the same sidebar.
- [ ] Delete `kimi-chat-archive.old-bloated-20260710/` after final verification.
- [ ] Rotate exposed GLM API key (P0 security).
