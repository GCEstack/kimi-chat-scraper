#!/usr/bin/env python3
"""Consolidate Kimi chat exports into a clean, deduplicated archive."""

from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


def now_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def safe_folder_name(name: str) -> str:
    """Make a string safe for a Windows/Unix folder name."""
    name = re.sub(r'[<>:"/\\|?*\x00-\x1f]', "_", name)
    name = re.sub(r"\s+", " ", name).strip()
    return name[:120] or "untitled"


def parse_timestamp(ts: str | int | float | None) -> datetime | None:
    if ts is None:
        return None
    if isinstance(ts, (int, float)):
        # Seconds or milliseconds since epoch.
        if ts > 1e12:
            ts = ts / 1000
        return datetime.fromtimestamp(ts, tz=timezone.utc)
    try:
        s = str(ts).strip()
        # Normalize a trailing Z to an explicit UTC offset.
        if s.endswith("Z"):
            s = s[:-1] + "+00:00"
        dt = datetime.fromisoformat(s)
        # If the string had no timezone, assume UTC.
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)
        return dt.astimezone(timezone.utc)
    except Exception:
        return None


def message_fingerprint(msg: dict[str, Any]) -> str:
    role = msg.get("role", "unknown")
    content = str(msg.get("content", "")).strip()
    ts = msg.get("timestamp") or ""
    return f"{role}|{ts}|{content[:160]}"


def normalize_conversation(conv: dict[str, Any]) -> dict[str, Any]:
    """Ensure a conversation matches the normalized schema."""
    fallback_id = hash(json.dumps(conv, sort_keys=True, default=str)) & 0xFFFFFFFF
    conv_id = str(conv.get("id") or f"unknown-{fallback_id}")
    title = str(conv.get("title") or "Untitled")
    created = parse_timestamp(conv.get("created_at"))
    updated = parse_timestamp(conv.get("updated_at"))

    raw_messages = conv.get("messages", [])
    if not isinstance(raw_messages, list):
        raw_messages = []

    messages = []
    for m in raw_messages:
        if not isinstance(m, dict):
            continue
        role = str(m.get("role") or "unknown").lower()
        if role in ("bot", "ai", "model"):
            role = "assistant"
        content = str(m.get("content") or "").strip()
        if not content:
            continue
        ts = parse_timestamp(m.get("timestamp"))
        messages.append(
            {
                "role": role,
                "content": content,
                "timestamp": ts.strftime("%Y-%m-%dT%H:%M:%SZ") if ts else None,
            }
        )

    # Sort by timestamp when available; stable otherwise.
    messages.sort(key=lambda m: parse_timestamp(m["timestamp"]) or datetime.min)

    return {
        "id": conv_id,
        "title": title,
        "created_at": created.strftime("%Y-%m-%dT%H:%M:%SZ") if created else None,
        "updated_at": updated.strftime("%Y-%m-%dT%H:%M:%SZ") if updated else None,
        "messages": messages,
        "_sources": conv.get("_sources") or set(),  # preserve sources from wrapper
    }


def load_exports(input_dir: Path) -> list[dict[str, Any]]:
    exports = []
    for path in input_dir.rglob("*.json"):
        if path.name == "index.json":
            continue
        try:
            with path.open("r", encoding="utf-8") as f:
                data = json.load(f)
        except json.JSONDecodeError as e:
            print(f"[warn] skipping invalid JSON {path}: {e}", file=sys.stderr)
            continue

        # Accept both wrapped exports and bare conversation arrays.
        if isinstance(data, list):
            exports.append(
                {
                    "metadata": {"account_tag": "unknown", "source": "unknown", "exported_at": None},
                    "conversations": data,
                    "_file": str(path),
                }
            )
        elif isinstance(data, dict):
            metadata = data.get("metadata", {})
            conversations = data.get("conversations", [])
            if not isinstance(conversations, list):
                continue
            exports.append(
                {
                    "metadata": {
                        "account_tag": str(metadata.get("account_tag") or "unknown"),
                        "source": str(metadata.get("source") or "unknown"),
                        "exported_at": metadata.get("exported_at"),
                    },
                    "conversations": conversations,
                    "_file": str(path),
                }
            )
    return exports


def deduplicate_conversations(conversations: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Merge conversations by id, then by content signature if ids differ."""
    by_id: dict[str, dict[str, Any]] = {}
    by_content_key: dict[str, str] = {}  # fingerprint -> id

    for conv in conversations:
        conv = normalize_conversation(conv)
        cid = conv["id"]

        # Content signature based on first + last user message.
        user_msgs = [m for m in conv["messages"] if m["role"] == "user"]
        sig = ""
        if user_msgs:
            sig = "|".join(
                [user_msgs[0]["content"][:120], user_msgs[-1]["content"][:120]]
            )

        if cid in by_id:
            target = by_id[cid]
        elif sig and sig in by_content_key:
            target = by_id[by_content_key[sig]]
        else:
            by_id[cid] = conv
            if sig:
                by_content_key[sig] = cid
            continue

        # Merge into target.
        seen = {message_fingerprint(m) for m in target["messages"]}
        for m in conv["messages"]:
            fp = message_fingerprint(m)
            if fp not in seen:
                target["messages"].append(m)
                seen.add(fp)
        target["messages"].sort(key=lambda m: parse_timestamp(m["timestamp"]) or datetime.min)
        if not target["created_at"] and conv["created_at"]:
            target["created_at"] = conv["created_at"]
        if conv.get("updated_at") and (not target.get("updated_at") or conv["updated_at"] > target["updated_at"]):
            target["updated_at"] = conv["updated_at"]
        target["_sources"].update(conv["_sources"])

    return list(by_id.values())


def write_markdown(conv: dict[str, Any], folder: Path) -> None:
    lines = [f"# {conv['title']}", ""]
    if conv.get("created_at"):
        lines.append(f"- Created: {conv['created_at']}")
    if conv.get("updated_at"):
        lines.append(f"- Updated: {conv['updated_at']}")
    lines.append("")
    lines.append("---")
    lines.append("")

    for m in conv["messages"]:
        role = "🧑 You" if m["role"] == "user" else "🤖 Kimi"
        ts = f" ({m['timestamp']})" if m.get("timestamp") else ""
        lines.append(f"## {role}{ts}")
        lines.append("")
        lines.append(m["content"])
        lines.append("")
        lines.append("---")
        lines.append("")

    (folder / "chat.md").write_text("\n".join(lines), encoding="utf-8")


def consolidate(input_dir: Path, output_dir: Path) -> dict[str, Any]:
    output_dir.mkdir(parents=True, exist_ok=True)
    exports = load_exports(input_dir)

    if not exports:
        raise ValueError(f"No valid Kimi export JSON files found in {input_dir}")

    # Group by account_tag.
    by_account: dict[str, list[dict[str, Any]]] = {}
    for export in exports:
        account = export["metadata"]["account_tag"]
        for conv in export["conversations"]:
            conv = dict(conv)  # shallow copy
            conv.setdefault("_sources", set()).add(export["metadata"]["source"])
            by_account.setdefault(account, []).append(conv)

    summary = {
        "generated_at": now_iso(),
        "input_files": len(exports),
        "accounts": {},
        "total_conversations": 0,
        "total_messages": 0,
    }

    for account, convs in sorted(by_account.items()):
        account_dir = output_dir / safe_folder_name(account)
        account_dir.mkdir(parents=True, exist_ok=True)

        merged = deduplicate_conversations(convs)
        index_entries = []

        for conv in merged:
            # Determine folder date prefix from created_at or updated_at.
            date_str = "unknown-date"
            for ts_field in (conv.get("updated_at"), conv.get("created_at")):
                dt = parse_timestamp(ts_field)
                if dt:
                    date_str = dt.strftime("%Y-%m-%d")
                    break

            folder_name = safe_folder_name(f"{date_str} - {conv['title']}")
            folder = account_dir / folder_name
            # Disambiguate duplicate folder names.
            counter = 1
            original_folder = folder
            while folder.exists():
                folder = Path(str(original_folder) + f" ({counter})")
                counter += 1
            folder.mkdir(parents=True, exist_ok=True)

            # Remove internal bookkeeping.
            out_conv = {
                "id": conv["id"],
                "title": conv["title"],
                "created_at": conv.get("created_at"),
                "updated_at": conv.get("updated_at"),
                "messages": conv["messages"],
                "sources": sorted(conv.get("_sources", set())),
            }

            (folder / "chat.json").write_text(
                json.dumps(out_conv, indent=2, ensure_ascii=False), encoding="utf-8"
            )
            write_markdown(out_conv, folder)

            index_entries.append(
                {
                    "id": out_conv["id"],
                    "title": out_conv["title"],
                    "folder": str(folder.relative_to(output_dir)),
                    "message_count": len(out_conv["messages"]),
                    "sources": out_conv["sources"],
                }
            )

            summary["total_conversations"] += 1
            summary["total_messages"] += len(out_conv["messages"])

        account_index = {
            "account_tag": account,
            "conversation_count": len(merged),
            "conversations": index_entries,
        }
        summary["accounts"][account] = account_index

        (account_dir / "index.json").write_text(
            json.dumps(account_index, indent=2, ensure_ascii=False), encoding="utf-8"
        )

    (output_dir / "index.json").write_text(
        json.dumps(summary, indent=2, ensure_ascii=False), encoding="utf-8"
    )
    return summary


def main() -> int:
    parser = argparse.ArgumentParser(description="Consolidate Kimi chat exports")
    parser.add_argument(
        "--input",
        "-i",
        type=Path,
        default=Path("exports"),
        help="Directory containing kimi-*.json export files (default: exports)",
    )
    parser.add_argument(
        "--output",
        "-o",
        type=Path,
        default=Path("kimi-chat-archive"),
        help="Output archive directory (default: kimi-chat-archive)",
    )
    args = parser.parse_args()

    if not args.input.exists():
        print(f"[error] input directory not found: {args.input}", file=sys.stderr)
        return 1

    summary = consolidate(args.input, args.output)
    print(f"Archive written to: {args.output.resolve()}")
    print(f"Accounts: {', '.join(summary['accounts'])}")
    print(f"Conversations: {summary['total_conversations']}")
    print(f"Messages: {summary['total_messages']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
