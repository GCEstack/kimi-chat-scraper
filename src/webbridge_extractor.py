#!/usr/bin/env python3
"""Automated Kimi chat extraction using the Kimi WebBridge."""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
import time
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

# Windows consoles may default to cp1252; force UTF-8 output with safe fallback.
if sys.stdout.encoding.lower() not in ("utf-8", "utf8"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
if sys.stderr.encoding.lower() not in ("utf-8", "utf8"):
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")
sys.stdout = os.fdopen(sys.stdout.fileno(), "w", encoding="utf-8", errors="replace", closefd=False, buffering=1)

DAEMON_PORT = 10086
DAEMON_URL = f"http://127.0.0.1:{DAEMON_PORT}/command"
STATUS_URL = f"http://127.0.0.1:{DAEMON_PORT}/status"
CHROME_PATH = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
WEBBRIDGE_BIN = os.path.expandvars(
    r"%USERPROFILE%\.kimi-webbridge\bin\kimi-webbridge.exe"
)
KIMI_URL = "https://www.kimi.com/"

EXTRACTION_JS = r"""
(() => {
  const ACCOUNT_TAG = __ACCOUNT_TAG__;
  const conversations = new Map();

  function nowISO() { return new Date().toISOString(); }

  function getChatTitle() {
    const docTitle = document.title.replace(/\s*-\s*Kimi$/, '').trim();
    if (docTitle && !/^(kimi|new chat)$/i.test(docTitle)) return docTitle;
    const h1 = document.querySelector('h1');
    if (h1) {
      const t = h1.innerText.trim();
      if (t && !/^(chats|new chat)$/i.test(t)) return t;
    }
    return 'Untitled';
  }

  function extractMainText() {
    const body = document.body.cloneNode(true);
    body.querySelectorAll('script, style, noscript, svg, link[rel="stylesheet"]').forEach(el => el.remove());
    // Remove sidebar by finding an element that contains the chat list links.
    const firstChatLink = body.querySelector('a[href^="/chat/"]');
    const sidebar = firstChatLink ? firstChatLink.closest('aside, [role="complementary"], nav, div') : null;
    if (sidebar && sidebar !== body) sidebar.remove();
    // Fallback removal by role.
    body.querySelectorAll('aside, [role="complementary"]').forEach(el => el.remove());
    // Remove input/textarea areas.
    body.querySelectorAll('textarea, input[type="text"], [contenteditable="true"]').forEach(el => {
      let p = el.closest('div');
      if (p && p !== body) p.remove();
      else el.remove();
    });
    return body.innerText.replace(/\n{3,}/g, '\n\n').trim();
  }

  // PURE_START -- pure logic, unit-tested in tests/test_webbridge_extractor.py
  // The Kimi K3 UI dropped "Edit" from the assistant-turn action buttons; the
  // legacy UI still has "Edit Copy Share". Match both. Evidence: the C6 capture
  // artifact (2026-09-23) contains zero "Edit Copy Share" and 15 "Copy Share".
  const ASSISTANT_TURN_DELIM = /\s*(?:Edit\s+)?Copy\s+Share\s*/gi;

  function splitIntoMessages(fullText, title) {
    // Assistant turns are followed by "Copy Share" (K3) / "Edit Copy Share" (legacy) buttons.
    let parts = fullText.split(ASSISTANT_TURN_DELIM).filter(p => p.trim());
    // Strip title/header from the first part if it starts with the chat title.
    if (title && parts[0]) {
      const first = parts[0].trim();
      const idx = first.indexOf(title);
      if (idx === 0) {
        let rest = first.slice(title.length).trim();
        rest = rest.replace(/^\d+\s+/, '').trim();
        parts[0] = rest;
      }
    }
    const messages = [];
    for (let i = 0; i < parts.length; i++) {
      const part = parts[i].trim();
      if (!part) continue;
      messages.push({ role: i % 2 === 0 ? 'user' : 'assistant', content: part, timestamp: null });
    }
    return messages;
  }

  // Decides, from the URL alone, whether the current page is capturable as a
  // chat. Returns an explicit status so a miss is explainable, never a bare null.
  function classifyCaptureState(pathname) {
    const path = pathname || location.pathname || '';
    if (path.includes('/history')) {
      return { status: 'wrong_path', reason: 'history_page', pathname: path };
    }
    const m = /^\/chat\/([^\/]+)$/.exec(path);
    if (!m) {
      return { status: 'wrong_path', reason: 'not_chat_route', pathname: path };
    }
    return { status: 'ok', id: 'chat-' + m[1] };
  }
  // PURE_END

  function captureCurrentChat() {
    // Only capture actual chat pages, not history/list. Each miss is classified.
    const state = classifyCaptureState();
    if (state.status !== 'ok') return state;
    const title = getChatTitle();
    const id = state.id || `chat-${Date.now()}`;
    const text = extractMainText();
    const textLen = text ? text.length : 0;
    if (!text || textLen < 20) {
      // Empty pane: SPA may still be fetching messages. Report readiness, not silence.
      return { status: 'empty', id, title, textLen, head: text ? text.slice(0, 120) : '' };
    }
    const messages = splitIntoMessages(text, title);
    if (!messages.length) {
      messages.push({ role: 'assistant', content: text, timestamp: null });
    }
    return { status: 'ok', id, title, created_at: nowISO(), updated_at: nowISO(), messages };
  }

  function mergeConversation(conv) {
    const existing = conversations.get(conv.id);
    if (!existing) {
      conversations.set(conv.id, conv);
      return;
    }
    if (conv.messages.length > existing.messages.length) {
      existing.messages = conv.messages;
    }
    if (conv.title && conv.title !== 'Untitled') existing.title = conv.title;
  }

  function saveCurrentChat() {
    const conv = captureCurrentChat();
    if (conv && conv.status === 'ok') mergeConversation(conv);
    return conv;
  }

  function getSidebarChatLinks() {
    const region = document.querySelector('[role="region"][aria-label*="Chat" i]') ||
                   document.querySelector('aside, [role="complementary"]');
    if (!region) return [];
    return Array.from(region.querySelectorAll('a[href^="/chat/"], a[href*="/chat/"]'));
  }

  async function collectChatList() {
    const allChats = Array.from(document.querySelectorAll('a, button')).find(el => /all chats/i.test(el.innerText));
    if (allChats) {
      allChats.click();
      await new Promise(r => setTimeout(r, 1500));
    }
    const links = getSidebarChatLinks();
    return links
      .filter(a => {
        const href = a.getAttribute('href') || '';
        return /^\/chat\/[^\/]+$/.test(href) && !href.includes('/history');
      })
      .map(a => ({ url: a.href, title: a.innerText.trim().split(/\n/)[0] }));
  }

  function getExport() {
    return {
      metadata: { account_tag: ACCOUNT_TAG, source: 'webbridge', exported_at: nowISO() },
      conversations: Array.from(conversations.values()),
    };
  }

  window.__kimiExtractor = { captureCurrentChat, saveCurrentChat, collectChatList, getExport, classifyCaptureState };
  return { initialized: true, chatCount: getSidebarChatLinks().length };
})();
"""


def now_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def daemon_path() -> str:
    candidates = [
        WEBBRIDGE_BIN,
        os.path.expandvars(
            r"%LOCALAPPDATA%\Programs\kimi-desktop\resources\resources\kimi-webbridge.exe"
        ),
    ]
    for p in candidates:
        if os.path.exists(p):
            return p
    return candidates[0]


def run_webbridge(args: list[str]) -> subprocess.CompletedProcess:
    return subprocess.run(
        [daemon_path(), *args],
        capture_output=True,
        text=True,
        shell=False,
    )


def daemon_status() -> dict[str, Any]:
    try:
        with urllib.request.urlopen(STATUS_URL, timeout=3) as r:
            return json.loads(r.read().decode())
    except Exception as e:
        return {"running": False, "error": str(e)}


def start_daemon() -> bool:
    print("Starting Kimi WebBridge daemon...")
    proc = run_webbridge(["start"])
    return proc.returncode == 0


def chrome_is_running() -> bool:
    try:
        output = subprocess.check_output(
            ["tasklist", "/FI", "IMAGENAME eq chrome.exe"],
            text=True,
            shell=False,
        )
        return "chrome.exe" in output
    except Exception:
        return False


def launch_chrome(url: str = KIMI_URL) -> bool:
    print("Launching Chrome...")
    try:
        subprocess.Popen(
            [CHROME_PATH, "--new-window", url],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            shell=False,
        )
        return True
    except Exception as e:
        print(f"Failed to launch Chrome: {e}", file=sys.stderr)
        return False


def wait_for_extension(timeout: int = 60) -> bool:
    print("Waiting for WebBridge extension to connect...")
    for _ in range(timeout):
        status = daemon_status()
        if status.get("extension_connected"):
            return True
        time.sleep(1)
    return False


def send_command(action: str, args: dict[str, Any], session: str) -> dict[str, Any]:
    payload = json.dumps({"action": action, "args": args, "session": session}).encode()
    req = urllib.request.Request(
        DAEMON_URL,
        data=payload,
        headers={"Content-Type": "application/json"},
    )
    with urllib.request.urlopen(req, timeout=180) as r:
        return json.loads(r.read().decode())


def evaluate(code: str, session: str) -> Any:
    resp = send_command("evaluate", {"code": code}, session)
    if not resp.get("ok"):
        raise RuntimeError(f"evaluate failed: {resp}")
    data = resp.get("data", {})
    if data.get("exceptionDetails"):
        raise RuntimeError(f"JS exception: {data['exceptionDetails']}")
    if "value" in data:
        return data["value"]
    return data.get("result", {}).get("value")


def capture_chat_with_retry(session: str, retries: int = 8, gap: float = 1.0) -> dict[str, Any]:
    """Capture the current chat, retrying while the SPA pane is still empty.

    captureCurrentChat() now returns a structured status: 'ok' (captured),
    'wrong_path' (history/list/non-chat route - cannot improve with waiting),
    or 'empty' (page pane has no text yet - SPA may still be fetching messages).
    """
    last: dict[str, Any] = {"status": "none"}
    for _ in range(retries + 1):
        try:
            val = evaluate("window.__kimiExtractor.captureCurrentChat()", session)
        except Exception as e:  # surface explicit failure instead of silent null
            return {"status": "error", "error": str(e)}
        if not isinstance(val, dict):
            last = {"status": "none"} if val is None else {"status": "unexpected", "value": str(val)}
            return last
        last = val
        if val.get("status") == "ok":
            return val
        if str(val.get("status", "")).startswith("wrong_path"):
            return val
        time.sleep(gap)
    return last


def wait_for_load(session: str, timeout: int = 20) -> None:
    """Wait until the page is usable. SPA pages may stay 'interactive'."""
    deadline = time.time() + timeout
    while time.time() < deadline:
        try:
            state = evaluate("document.readyState", session)
            if state == "complete":
                return
            # Accept interactive after a short grace period for SPAs.
            if state == "interactive" and time.time() > deadline - timeout + 1.5:
                return
        except Exception:
            pass
        time.sleep(0.3)


def ensure_ready() -> bool:
    status = daemon_status()
    if not status.get("running"):
        if not start_daemon():
            print("Failed to start daemon", file=sys.stderr)
            return False
        time.sleep(2)
    if not chrome_is_running():
        if not launch_chrome():
            return False
    if not wait_for_extension():
        print(
            "Extension did not connect. Make sure Chrome is open with the Kimi WebBridge extension enabled.",
            file=sys.stderr,
        )
        return False
    return True


def extract(account_tag: str, session: str, walk_delay: int = 800, max_chats: int = 0) -> dict[str, Any] | None:
    if not ensure_ready():
        return None

    print("Navigating to Kimi...", flush=True)
    send_command(
        "navigate",
        {"url": KIMI_URL, "newTab": True, "group_title": f"Kimi Export - {account_tag}"},
        session,
    )
    wait_for_load(session, timeout=20)
    time.sleep(2)

    print("Injecting extraction script...", flush=True)
    js_payload = EXTRACTION_JS.replace("__ACCOUNT_TAG__", json.dumps(account_tag))
    init_result = evaluate(js_payload, session)
    print("Init result:", init_result, flush=True)

    print("Collecting chat list...", flush=True)
    time.sleep(2)
    chats = evaluate("window.__kimiExtractor.collectChatList()", session)
    if not isinstance(chats, list) or not chats:
        print("No chats found. Make sure you are logged into Kimi.", file=sys.stderr)
        return None
    total = len(chats)
    limit = max_chats if max_chats > 0 else total
    print(f"Found {total} chats, extracting {limit}...", flush=True)

    collected_conversations = []
    for i, chat in enumerate(chats[:limit]):
        chat_url = chat.get("url")
        chat_title = chat.get("title", "Untitled")
        if chat_title.lower() in {"all chats", "new chat"}:
            continue
        print(f"[{i+1}/{limit}] {chat_title}", flush=True)
        send_command("navigate", {"url": chat_url}, session)
        wait_for_load(session, timeout=20)
        time.sleep(1)
        # Re-inject extraction script only if the SPA cleared it.
        has_extractor = evaluate("typeof window.__kimiExtractor !== 'undefined'", session)
        if not has_extractor:
            evaluate(js_payload, session)
            time.sleep(0.5)
        conv = capture_chat_with_retry(session)
        status = conv.get("status", "none") if isinstance(conv, dict) else "none"
        if status == "ok":
            print("  capture: ok", flush=True)
            collected_conversations.append(conv)
        elif conv:
            detail = []
            for key in ("reason",):
                if conv.get(key):
                    detail.append(str(conv[key]))
            for key in ("pathname", "textLen"):
                if conv.get(key) is not None:
                    detail.append(f"{key}={conv[key]}")
            print(
                f"  capture: skipped ({status}"
                + (": " + " ".join(detail) if detail else "")
                + ")",
                flush=True,
            )
        else:
            print("  capture: skipped (none)", flush=True)

    print("Retrieving export...", flush=True)
    export = {
        "metadata": {"account_tag": account_tag, "source": "webbridge", "exported_at": now_iso()},
        "conversations": collected_conversations,
    }

    try:
        send_command("close_session", {}, session)
    except Exception:
        pass

    return export


def save_export(export: dict[str, Any], output_dir: Path) -> Path:
    output_dir.mkdir(parents=True, exist_ok=True)
    ts = datetime.now(timezone.utc).strftime("%Y-%m-%d-%H%M%S")
    filename = f"kimi-webbridge-{export['metadata']['account_tag']}-{ts}.json"
    path = output_dir / filename
    path.write_text(json.dumps(export, indent=2, ensure_ascii=False), encoding="utf-8")
    return path


def main() -> int:
    parser = argparse.ArgumentParser(description="Extract Kimi chats via WebBridge")
    parser.add_argument("--account-tag", "-a", default="account1", help="Tag for this account")
    parser.add_argument("--session", "-s", default="kimi-chat-export", help="WebBridge session name")
    parser.add_argument("--output", "-o", type=Path, default=Path("exports"), help="Output directory")
    parser.add_argument("--walk-delay", "-d", type=int, default=800, help="Delay in ms between sidebar clicks")
    parser.add_argument("--max-chats", "-m", type=int, default=0, help="Maximum chats to extract (0 = all)")
    args = parser.parse_args()

    export = extract(args.account_tag, args.session, args.walk_delay, args.max_chats)
    if not export:
        return 1

    conv_count = len(export.get("conversations", []))
    if not conv_count:
        print("No conversations found. Make sure you are logged into Kimi in Chrome.", file=sys.stderr)
        return 1

    path = save_export(export, args.output)
    print(f"Saved {conv_count} conversations to: {path}", flush=True)
    print(f"Run: .venv\\Scripts\\python src\\consolidate.py -i {args.output} -o kimi-chat-archive", flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
