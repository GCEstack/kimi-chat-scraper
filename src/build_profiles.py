#!/usr/bin/env python3
"""Build self-contained project profiles from a consolidated Kimi archive.

Each profile is a single Markdown file you can drop into a new Kimi chat as
context.  Profiles are grouped by keyword rules; unmatched chats go into
misc.md.
"""

from __future__ import annotations

import argparse
import json
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


DEFAULT_PROFILE_RULES: dict[str, list[str]] = {
    "EC8 Edge Crew": [
        "edge", "bet", "betting", "mlb", "wnba", "soccer", "corner", "handicap",
        "nrfi", "yrfi", "spread", "moneyline", "parlay", "odds", "book", "line",
        "lock", "dial", "croatia", "portugal", "sweden", "switzerland", "mls",
        "slots", "rtp", "casino",
    ],
    "Casa Companion": [
        "casa companion", "casa", "companion", "repo audit", "bug fix", "ui revamp",
    ],
    "Kimi Code Ops": [
        "kimi code", "kimi cli", "kimi prompt", "kimi webbridge", "kimi work",
        "agent credit", "secret audit", "credential", "mcp", "thinking mode",
        "powershell", "desktop cleanup", "repo scan", "git worktree",
    ],
    "Voice & Audio": [
        "voice", "tts", "deepgram", "openrouter", "gemini audio", "mic transcript",
        "voice agent",
    ],
    "AI Models & APIs": [
        "groq", "qwen", "gemini", "openrouter", "model", "api key", "api management",
        "best model",
    ],
    "Media & Video": [
        "hulu", "drm", "embedding", "chunking", "family video", "video",
    ],
    "Creative & Brand": [
        "logo", "flyer", "brand", "fusion menu", "dj flyer", "gianelli",
        "south florida",
    ],
    "Desktop & File Org": [
        "desktop folder", "folder merge", "file org", "epo folder", "large repo",
        "proton drive",
    ],
    "Heartbeat Family System": [
        "heartbeat", "family creed", "mafia", "animal", "orchestra", "traffik",
        "lares", "leone", "lupo", "falco", "vesta",
    ],
}


def now_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def load_archive(archive_dir: Path) -> list[dict[str, Any]]:
    """Load all conversations from a consolidated archive directory."""
    conversations: list[dict[str, Any]] = []
    root_index = archive_dir / "index.json"
    if not root_index.exists():
        raise FileNotFoundError(f"No archive index found at {root_index}")

    with root_index.open("r", encoding="utf-8") as f:
        summary = json.load(f)

    for account, account_info in summary.get("accounts", {}).items():
        account_dir = archive_dir / account
        account_index_path = account_dir / "index.json"
        if not account_index_path.exists():
            continue
        with account_index_path.open("r", encoding="utf-8") as f:
            account_index = json.load(f)

        for entry in account_index.get("conversations", []):
            folder = archive_dir / entry["folder"]
            chat_file = folder / "chat.json"
            if not chat_file.exists():
                continue
            with chat_file.open("r", encoding="utf-8") as f:
                conv = json.load(f)
            conv["_account"] = account
            conv["_folder"] = str(folder)
            conversations.append(conv)

    return conversations


def tag_conversation(conv: dict[str, Any], rules: dict[str, list[str]]) -> list[str]:
    """Return all profile tags that match a conversation."""
    title = str(conv.get("title", "")).lower()
    text = title
    for m in conv.get("messages", [])[:3]:
        text += " " + str(m.get("content", "")).lower()[:500]

    tags: list[str] = []
    for profile, keywords in rules.items():
        if any(kw in text for kw in keywords):
            tags.append(profile)
    return tags or ["Misc"]


def safe_file_name(name: str) -> str:
    name = re.sub(r'[<>:"/\\|?*\x00-\x1f]', "-", name)
    return name.strip("-") or "untitled"


def build_profile_md(profile: str, convs: list[dict[str, Any]]) -> str:
    lines = [
        f"# Profile: {profile}",
        "",
        f"Generated: {now_iso()}",
        f"Conversations: {len(convs)}",
        "",
        "## Summary",
        "",
    ]

    for conv in convs:
        title = conv.get("title", "Untitled")
        msg_count = len(conv.get("messages", []))
        account = conv.get("_account", "unknown")
        lines.append(f"- **{title}** ({account}, {msg_count} messages)")

    lines.extend(["", "---", ""])

    for conv in convs:
        title = conv.get("title", "Untitled")
        created = conv.get("created_at", "")
        account = conv.get("_account", "unknown")
        lines.extend([
            f"## {title}",
            f"- Account: {account}",
            f"- Created: {created}",
            "",
        ])
        for m in conv.get("messages", []):
            role = m.get("role", "unknown").capitalize()
            content = str(m.get("content", "")).strip()
            if not content:
                continue
            lines.append(f"**{role}:** {content}")
            lines.append("")
        lines.extend(["---", ""])

    return "\n".join(lines)


def build_profiles(archive_dir: Path, output_dir: Path, rules: dict[str, list[str]]) -> dict[str, Any]:
    output_dir.mkdir(parents=True, exist_ok=True)
    conversations = load_archive(archive_dir)

    # Group by tag; a conversation can appear in multiple profiles.
    by_profile: dict[str, list[dict[str, Any]]] = {}
    for conv in conversations:
        for tag in tag_conversation(conv, rules):
            by_profile.setdefault(tag, []).append(conv)

    # Sort conversations by title for stable output.
    for tag in by_profile:
        by_profile[tag].sort(key=lambda c: str(c.get("title", "")).lower())

    # Write each profile.
    written: list[dict[str, str]] = []
    for tag in sorted(by_profile):
        filename = safe_file_name(tag) + ".md"
        path = output_dir / filename
        path.write_text(build_profile_md(tag, by_profile[tag]), encoding="utf-8")
        written.append({"profile": tag, "file": filename, "conversations": str(len(by_profile[tag]))})

    # Write index.
    index = {
        "generated_at": now_iso(),
        "archive": str(archive_dir),
        "profiles": written,
    }
    (output_dir / "index.json").write_text(
        json.dumps(index, indent=2, ensure_ascii=False), encoding="utf-8"
    )

    # Write human-readable index.
    index_lines = ["# Project Profiles", "", f"Generated: {now_iso()}", ""]
    for item in written:
        index_lines.append(f"- [{item['profile']}]({item['file']}) — {item['conversations']} chats")
    (output_dir / "index.md").write_text("\n".join(index_lines), encoding="utf-8")

    return index


def main() -> int:
    parser = argparse.ArgumentParser(description="Build project profiles from a Kimi archive")
    parser.add_argument("--archive", "-a", type=Path, default=Path("kimi-chat-archive"))
    parser.add_argument("--output", "-o", type=Path, default=Path("profiles"))
    parser.add_argument("--rules", "-r", type=Path, help="Optional JSON file with profile keyword rules")
    args = parser.parse_args()

    rules = DEFAULT_PROFILE_RULES
    if args.rules and args.rules.exists():
        with args.rules.open("r", encoding="utf-8") as f:
            rules = json.load(f)

    try:
        index = build_profiles(args.archive, args.output, rules)
        print(f"Profiles written to: {args.output.resolve()}")
        for p in index["profiles"]:
            print(f"  {p['profile']}: {p['conversations']} chats -> {p['file']}")
        return 0
    except Exception as e:
        print(f"[error] {e}", file=__import__("sys").stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
