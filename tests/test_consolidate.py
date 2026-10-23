import json
import shutil
from pathlib import Path

import pytest

from consolidate import (
    deduplicate_conversations,
    load_exports,
    message_fingerprint,
    normalize_conversation,
    parse_timestamp,
    safe_folder_name,
    consolidate,
)


@pytest.fixture
def sample_export(tmp_path: Path) -> Path:
    exports_dir = tmp_path / "exports"
    exports_dir.mkdir()
    data = {
        "metadata": {
            "account_tag": "account1",
            "source": "web",
            "exported_at": "2026-07-02T10:00:00Z",
        },
        "conversations": [
            {
                "id": "conv-1",
                "title": "Project Planning",
                "created_at": "2026-07-01T12:00:00Z",
                "updated_at": "2026-07-01T13:00:00Z",
                "messages": [
                    {"role": "user", "content": "Hello", "timestamp": "2026-07-01T12:00:00Z"},
                    {"role": "assistant", "content": "Hi there", "timestamp": "2026-07-01T12:00:05Z"},
                ],
            }
        ],
    }
    (exports_dir / "kimi-web-account1-2026-07-02.json").write_text(json.dumps(data))
    return exports_dir


@pytest.fixture
def duplicate_exports(tmp_path: Path) -> Path:
    exports_dir = tmp_path / "exports"
    exports_dir.mkdir()
    base = {
        "id": "conv-1",
        "title": "Project Planning",
        "created_at": "2026-07-01T12:00:00Z",
        "messages": [
            {"role": "user", "content": "Hello", "timestamp": "2026-07-01T12:00:00Z"},
        ],
    }
    export_a = {
        "metadata": {"account_tag": "account1", "source": "web"},
        "conversations": [base],
    }
    export_b = {
        "metadata": {"account_tag": "account1", "source": "desktop"},
        "conversations": [
            {
                **base,
                "messages": [
                    {"role": "user", "content": "Hello", "timestamp": "2026-07-01T12:00:00Z"},
                    {"role": "assistant", "content": "Hi there", "timestamp": "2026-07-01T12:00:05Z"},
                ],
            }
        ],
    }
    (exports_dir / "a.json").write_text(json.dumps(export_a))
    (exports_dir / "b.json").write_text(json.dumps(export_b))
    return exports_dir


def test_parse_timestamp_iso():
    assert parse_timestamp("2026-07-01T12:00:00Z") == parse_timestamp("2026-07-01T12:00:00+00:00")


def test_parse_timestamp_millis():
    dt = parse_timestamp(1751409600000)
    assert dt is not None
    assert dt.year == 2025


def test_safe_folder_name():
    assert safe_folder_name('A/B Test: Question?') == 'A_B Test_ Question_'
    assert safe_folder_name('   spaced   ') == 'spaced'


def test_normalize_conversation():
    raw = {
        "id": "x",
        "title": "Test",
        "created_at": "2026-07-01T12:00:00Z",
        "messages": [
            {"role": "bot", "content": "Hello", "timestamp": "2026-07-01T12:00:05Z"},
            {"role": "user", "content": "Hi", "timestamp": "2026-07-01T12:00:00Z"},
        ],
    }
    conv = normalize_conversation(raw)
    assert conv["id"] == "x"
    assert conv["messages"][0]["role"] == "user"
    assert conv["messages"][1]["role"] == "assistant"


def test_message_fingerprint():
    a = {"role": "user", "content": "Hello", "timestamp": "2026-07-01T12:00:00Z"}
    b = {"role": "user", "content": "Hello", "timestamp": "2026-07-01T12:00:00Z"}
    assert message_fingerprint(a) == message_fingerprint(b)


def test_load_exports(sample_export: Path):
    exports = load_exports(sample_export)
    assert len(exports) == 1
    assert exports[0]["metadata"]["account_tag"] == "account1"
    assert len(exports[0]["conversations"]) == 1


def test_deduplicate_conversations(duplicate_exports: Path):
    exports = load_exports(duplicate_exports)
    all_convs = []
    for e in exports:
        for c in e["conversations"]:
            c.setdefault("_sources", set()).add(e["metadata"]["source"])
            all_convs.append(c)
    merged = deduplicate_conversations(all_convs)
    assert len(merged) == 1
    assert len(merged[0]["messages"]) == 2


def test_consolidate_creates_files(sample_export: Path, tmp_path: Path):
    output_dir = tmp_path / "archive"
    summary = consolidate(sample_export, output_dir)

    assert summary["total_conversations"] == 1
    assert summary["total_messages"] == 2

    account_dir = output_dir / "account1"
    assert account_dir.exists()

    chat_folders = [d for d in account_dir.iterdir() if d.is_dir()]
    assert len(chat_folders) == 1

    folder = chat_folders[0]
    assert (folder / "chat.json").exists()
    assert (folder / "chat.md").exists()

    chat_json = json.loads((folder / "chat.json").read_text())
    assert chat_json["title"] == "Project Planning"
    assert len(chat_json["messages"]) == 2

    md_text = (folder / "chat.md").read_text()
    assert "Project Planning" in md_text
    assert "Hello" in md_text


def test_consolidate_multiple_accounts(tmp_path: Path):
    exports_dir = tmp_path / "exports"
    exports_dir.mkdir()
    for account in ("work", "personal"):
        data = {
            "metadata": {"account_tag": account, "source": "web"},
            "conversations": [
                {
                    "id": f"{account}-1",
                    "title": f"{account} chat",
                    "created_at": "2026-07-01T12:00:00Z",
                    "messages": [{"role": "user", "content": "hi"}],
                }
            ],
        }
        (exports_dir / f"{account}.json").write_text(json.dumps(data))

    output_dir = tmp_path / "archive"
    summary = consolidate(exports_dir, output_dir)
    assert set(summary["accounts"]) == {"work", "personal"}
    assert summary["total_conversations"] == 2
