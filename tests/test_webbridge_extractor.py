"""Tests for src/webbridge_extractor.py.

Covers the C6 extractor-completeness fix:

- the embedded extraction JS classifies every miss explicitly (`wrong_path` /
  `empty`) instead of silently returning a bare `null`;
- the assistant-turn delimiter matches the current Kimi K3 UI (`Copy Share`)
  while keeping legacy `Edit Copy Share` support;
- the Python capture wrapper retries an empty pane and never promotes a miss.

Pure JS functions (PURE_START..PURE_END in EXTRACTION_JS) are executed against
node when available; the Pure-JS cases are skipped otherwise.
"""

import json
import shutil
import subprocess
import textwrap

import pytest

import webbridge_extractor
from webbridge_extractor import EXTRACTION_JS, capture_chat_with_retry

PURE_START = "PURE_START"
PURE_END = "PURE_END"

HARNESS_JS = r"""
const fs = require('fs');
const pure = fs.readFileSync(process.argv[2], 'utf8');
const location = { pathname: '' };
(function () {
  eval(pure + '\n' + [
    'globalThis.__classify = classifyCaptureState;',
    'globalThis.__split = splitIntoMessages;',
  ].join('\n'));
})();
const classifyCaptureState = globalThis.__classify;
const splitIntoMessages = globalThis.__split;

const out = {
  routes: [
    classifyCaptureState('/chat/1a055f92-b712-8cca-8000-09b730872ed1'),
    classifyCaptureState('/chat/abc/child'),
    classifyCaptureState('/chat'),
    classifyCaptureState('/'),
    classifyCaptureState('/history'),
    classifyCaptureState('/chat/abc/history'),
  ],
  splitK3: splitIntoMessages('user one\nCopy Share\nassistant one\nCopy Share\nuser two', ''),
  splitLegacy: splitIntoMessages('user one\nEdit Copy Share\nassistant one', ''),
  splitNone: splitIntoMessages('whole blob with no action-button delimiter', ''),
};
process.stdout.write(JSON.stringify(out));
"""


@pytest.fixture
def node_result(tmp_path):
    if not shutil.which("node"):
        pytest.skip("node not available for embedded-JS tests")
    start_marker = EXTRACTION_JS.index(PURE_START)
    start = EXTRACTION_JS.index("\n", start_marker) + 1
    end = EXTRACTION_JS.index(PURE_END)
    pure_path = tmp_path / "pure.js"
    harness_path = tmp_path / "harness.js"
    pure_path.write_text(EXTRACTION_JS[start:end], encoding="utf-8")
    harness_path.write_text(textwrap.dedent(HARNESS_JS), encoding="utf-8")
    proc = subprocess.run(
        ["node", str(harness_path), str(pure_path)],
        capture_output=True,
        text=True,
        timeout=30,
    )
    assert proc.returncode == 0, proc.stderr
    return json.loads(proc.stdout)


def test_classify_accepts_single_segment_chat_route(node_result):
    ok = node_result["routes"][0]
    assert ok["status"] == "ok"
    assert ok["id"] == "chat-1a055f92-b712-8cca-8000-09b730872ed1"


def test_classify_rejects_non_chat_routes_explicitly(node_result):
    assert node_result["routes"][1]["status"] == "wrong_path"
    assert node_result["routes"][1]["reason"] == "not_chat_route"
    assert node_result["routes"][2]["status"] == "wrong_path"
    assert node_result["routes"][3]["status"] == "wrong_path"
    assert node_result["routes"][4]["status"] == "wrong_path"
    assert node_result["routes"][4]["reason"] == "history_page"
    assert node_result["routes"][5]["status"] == "wrong_path"
    assert node_result["routes"][5]["reason"] == "history_page"


def test_split_uses_current_k3_copy_share_delimiter(node_result):
    msgs = node_result["splitK3"]
    assert [m["role"] for m in msgs] == ["user", "assistant", "user"]


def test_split_keeps_legacy_edit_copy_share_support(node_result):
    msgs = node_result["splitLegacy"]
    assert [m["role"] for m in msgs] == ["user", "assistant"]


def test_split_single_blob_when_no_delimiter(node_result):
    msgs = node_result["splitNone"]
    assert len(msgs) == 1


def test_capture_gate_no_longer_silently_returns_null():
    """The demonstrated 2/3 failure must classify, never collapse to `null`."""
    assert "if (!text || text.length < 20) return null;" not in EXTRACTION_JS
    assert "return { status: 'empty'" in EXTRACTION_JS
    assert "status: 'wrong_path'" in EXTRACTION_JS


def _monkeypatch_evaluate(monkeypatch, script):
    calls = []

    def fake(code, session):
        calls.append(code)
        return script(calls)

    monkeypatch.setattr(webbridge_extractor, "evaluate", fake)
    monkeypatch.setattr(webbridge_extractor.time, "sleep", lambda s: None)
    return calls


def test_capture_ok_returns_immediately(monkeypatch):
    calls = _monkeypatch_evaluate(
        monkeypatch, lambda c: {"status": "ok", "id": "chat-x", "title": "T", "messages": []}
    )
    result = capture_chat_with_retry("s")
    assert result["status"] == "ok"
    assert len(calls) == 1


def test_capture_empty_pane_retries_then_succeeds(monkeypatch):
    values = iter(
        [
            {"status": "empty", "id": "chat-x", "title": "T", "textLen": 0},
            {"status": "ok", "id": "chat-x", "title": "T", "messages": []},
        ]
    )
    calls = _monkeypatch_evaluate(monkeypatch, lambda c: next(values))
    result = capture_chat_with_retry("s", retries=3)
    assert result["status"] == "ok"
    assert len(calls) == 2


def test_capture_wrong_path_never_retries(monkeypatch):
    calls = _monkeypatch_evaluate(
        monkeypatch,
        lambda c: {"status": "wrong_path", "reason": "not_chat_route", "pathname": "/"},
    )
    result = capture_chat_with_retry("s", retries=5)
    assert result["status"] == "wrong_path"
    assert len(calls) == 1


def test_capture_empty_pane_times_out_with_explicit_status(monkeypatch):
    calls = _monkeypatch_evaluate(
        monkeypatch,
        lambda c: {"status": "empty", "id": "chat-x", "title": "T", "textLen": 0},
    )
    result = capture_chat_with_retry("s", retries=2)
    assert result["status"] == "empty"
    assert len(calls) == 3


def test_capture_surfaces_evaluate_exception(monkeypatch):
    def boom(code, session):
        raise RuntimeError("JS exception: boom")

    monkeypatch.setattr(webbridge_extractor, "evaluate", boom)
    result = capture_chat_with_retry("s")
    assert result["status"] == "error"
    assert "boom" in result["error"]