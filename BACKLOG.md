# Backlog

## Done this session
- [x] Fix voice dictation HTTP 402 infinite loop in `capture.py` + `voice_access.py`
- [x] Create clean Desktop launchers: `Voice Dictation.bat` + `Voice Access.lnk`
- [x] Upgrade Kimi WebBridge `v1.10.1 -> v1.11.1`
- [x] Scrape missing Kimi chats (account1 + account2), consolidate 93 conversations, build profiles
- [x] Delete 3 original chat `.md` files from `Desktop Archive 2026-07-09`
- [x] Create `delete-kimi-chats` skill + `src/delete_kimi_chats.py`
- [x] Configure/test `the-guardian` GLM connection, then park the project
- [x] Fix `the-guardian` wire parser for current Kimi CLI format
- [x] Clarify family model split: `ibis` (work/run chat, Kimi) vs `squalo` (outside-brain talk chat, GLM)

## P0 — Blocked / Security
- [ ] Rotate exposed GLM API key (printed in session tool output) | owner:Costruito | due:2026-07-10

## P1 — This Week
- [ ] Bulk-delete Kimi chats from web/desktop app after final scrape/consolidation | owner:Costruito | due:2026-07-11
- [ ] Set up two-account scrape archive: `ibis` (work/run chat, Kimi) and `squalo` (outside-brain talk chat, GLM) | owner:Costruito | due:2026-07-11

## P2 — Next
- [ ] Add tests for `webbridge_extractor.py`, `build_profiles.py`, `delete_kimi_chats.py`
- [ ] Decide whether to archive or keep `the-guardian` project

## Icebox
- [ ] Refactor `the-guardian` into a true Squalo/Egress review tool if needed later
