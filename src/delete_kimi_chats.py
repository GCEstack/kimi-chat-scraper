#!/usr/bin/env python3
r"""Bulk-delete all Kimi chats via WebBridge UI automation.

Run:
    .venv\Scripts\python src\delete_kimi_chats.py --dry-run
    .venv\Scripts\python src\delete_kimi_chats.py --confirm
"""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
import time
import urllib.request
from pathlib import Path
from typing import Any

if sys.stdout.encoding.lower() not in ("utf-8", "utf8"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
if sys.stderr.encoding.lower() not in ("utf-8", "utf8"):
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")
sys.stdout = os.fdopen(sys.stdout.fileno(), "w", encoding="utf-8", errors="replace", closefd=False, buffering=1)

DAEMON_PORT = 10086
DAEMON_URL = f"http://127.0.0.1:{DAEMON_PORT}/command"
STATUS_URL = f"http://127.0.0.1:{DAEMON_PORT}/status"
CHROME_PATH = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
WEBBRIDGE_BIN = os.path.expandvars(r"%USERPROFILE%\.kimi-webbridge\bin\kimi-webbridge.exe")
KIMI_URL = "https://www.kimi.com/"

DELETE_JS = r"""
(() => {
  const DRY_RUN = __DRY_RUN__;
  const results = [];

  function sleep(ms) { return new Promise(r => setTimeout(r, ms)); }

  function getSidebarRegion() {
    return document.querySelector('[role="region"][aria-label*="Chat" i]') ||
           document.querySelector('aside, [role="complementary"]');
  }

  function getChatItems() {
    const region = getSidebarRegion();
    if (!region) return [];
    // Each chat row usually contains a link /chat/<id>.
    return Array.from(region.querySelectorAll('a[href^="/chat/"]')).map(a => {
      const row = a.closest('div[class*="group"], div[class*="item"], div[role="button"], div') || a.parentElement;
      return { a, row, href: a.getAttribute('href'), title: a.innerText.trim().split(/\n/)[0] };
    }).filter(x => /^\/chat\/[^\/]+$/.test(x.href));
  }

  async function clickDeleteForItem(item) {
    const { a, row, href, title } = item;
    const chatId = href.replace('/chat/', '');

    // Try to open the context menu via right-click on the row.
    const target = row || a;
    const rightClick = new MouseEvent('contextmenu', { bubbles: true, cancelable: true, view: window });
    target.dispatchEvent(rightClick);
    await sleep(300);

    // Look for a delete/trash option in any visible menu.
    let deleteBtn = Array.from(document.querySelectorAll('div, button, a, span')).find(el => {
      const t = el.innerText.trim().toLowerCase();
      return t === 'delete' || t === 'remove' || t.includes('delete chat') || t.includes('trash');
    });

    // Fallback: look for a three-dot menu button within the row and click it.
    if (!deleteBtn) {
      const menuBtn = row.querySelector('button, [role="button"]') ||
                      Array.from(row.querySelectorAll('svg, button, div')).slice(-1)[0];
      if (menuBtn) {
        menuBtn.click();
        await sleep(300);
        deleteBtn = Array.from(document.querySelectorAll('div, button, a, span')).find(el => {
          const t = el.innerText.trim().toLowerCase();
          return t === 'delete' || t === 'remove' || t.includes('delete chat') || t.includes('trash');
        });
      }
    }

    if (!deleteBtn) {
      // Press Escape to close any open menu and report failure.
      document.dispatchEvent(new KeyboardEvent('keydown', { key: 'Escape', bubbles: true }));
      return { chatId, title, deleted: false, reason: 'No delete button found' };
    }

    if (DRY_RUN) {
      document.dispatchEvent(new KeyboardEvent('keydown', { key: 'Escape', bubbles: true }));
      return { chatId, title, deleted: false, reason: 'DRY_RUN' };
    }

    deleteBtn.click();
    await sleep(400);

    // Confirm deletion if a confirmation dialog appears.
    const confirmBtn = Array.from(document.querySelectorAll('button, div[role="button"]')).find(el => {
      const t = el.innerText.trim().toLowerCase();
      return t === 'delete' || t === 'confirm' || t === 'yes' || t === 'ok';
    });
    if (confirmBtn && confirmBtn !== deleteBtn) {
      confirmBtn.click();
      await sleep(400);
    }

    return { chatId, title, deleted: true };
  }

  async function deleteAllChats() {
    // Open "All Chats" if available.
    const allChatsBtn = Array.from(document.querySelectorAll('a, button')).find(el => /all chats/i.test(el.innerText));
    if (allChatsBtn) {
      allChatsBtn.click();
      await sleep(1500);
    }

    let items = getChatItems();
    let lastCount = -1;
    let attempts = 0;

    // Scroll sidebar to load more chats if virtualized.
    while (items.length !== lastCount && attempts < 5) {
      lastCount = items.length;
      const region = getSidebarRegion();
      if (region) {
        region.scrollTop = region.scrollHeight;
        await sleep(800);
      }
      items = getChatItems();
      attempts++;
    }

    // Remove duplicates by href.
    const seen = new Set();
    const unique = [];
    for (const item of items) {
      if (!seen.has(item.href)) {
        seen.add(item.href);
        unique.push(item);
      }
    }

    for (const item of unique) {
      try {
        const res = await clickDeleteForItem(item);
        results.push(res);
        await sleep(600);
      } catch (e) {
        results.push({ chatId: item.href, title: item.title, deleted: false, reason: String(e) });
      }
    }
    return results;
  }

  const res = await deleteAllChats();
  return { count: res.length, results: res };
})();
"""


def daemon_path() -> str:
    candidates = [
        WEBBRIDGE_BIN,
        os.path.expandvars(r"%LOCALAPPDATA%\Programs\kimi-desktop\resources\resources\kimi-webbridge.exe"),
    ]
    for p in candidates:
        if os.path.exists(p):
            return p
    return candidates[0]


def run_webbridge(args: list[str]) -> subprocess.CompletedProcess:
    return subprocess.run([daemon_path(), *args], capture_output=True, text=True, shell=False)


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


def send_command(action: str, payload: dict[str, Any], session: str) -> Any:
    data = json.dumps({"action": action, "payload": payload, "session": session}).encode()
    req = urllib.request.Request(DAEMON_URL, data=data, headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.loads(r.read().decode())


def wait_for_extension(timeout: int = 30) -> bool:
    print("Waiting for WebBridge extension to connect...")
    for _ in range(timeout):
        status = daemon_status()
        if status.get("extension_connected"):
            return True
        time.sleep(1)
    return False


def evaluate(js: str, session: str) -> Any:
    return send_command("evaluate", {"script": js}, session)


def main() -> int:
    parser = argparse.ArgumentParser(description="Bulk-delete all Kimi chats via WebBridge")
    parser.add_argument("--session", "-s", default="kimi-chat-delete", help="WebBridge session name")
    parser.add_argument("--dry-run", action="store_true", help="List chats that would be deleted without deleting")
    parser.add_argument("--confirm", action="store_true", help="Actually delete chats (required)")
    args = parser.parse_args()

    if not args.dry_run and not args.confirm:
        print("ERROR: Use --dry-run to preview or --confirm to actually delete.", file=sys.stderr)
        return 1

    status = daemon_status()
    if not status.get("running"):
        if not start_daemon():
            print("Failed to start WebBridge daemon.", file=sys.stderr)
            return 1
        time.sleep(2)

    if not wait_for_extension():
        print("Extension did not connect. Make sure Chrome is open with Kimi WebBridge enabled.", file=sys.stderr)
        return 1

    print("Navigating to Kimi...")
    send_command("navigate", {"url": KIMI_URL, "newTab": True, "group_title": "Kimi Bulk Delete"}, args.session)
    # wait_for_load equivalent
    for _ in range(20):
        time.sleep(1)
        try:
            res = evaluate("document.readyState", args.session)
            if res == "complete":
                break
        except Exception:
            pass
    time.sleep(2)

    print("Injecting delete script...")
    js_payload = DELETE_JS.replace("__DRY_RUN__", "true" if args.dry_run else "false")
    result = evaluate(js_payload, args.session)

    if not isinstance(result, dict):
        print(f"Unexpected result: {result}", file=sys.stderr)
        return 1

    results = result.get("results", [])
    print(f"\nFound {len(results)} chats:\n")
    for r in results:
        status = "DELETED" if r.get("deleted") else "SKIPPED"
        print(f"  [{status}] {r.get('title', 'Untitled')} ({r.get('chatId', '?')}) {r.get('reason', '')}")

    try:
        send_command("close_session", {}, args.session)
    except Exception:
        pass

    deleted = sum(1 for r in results if r.get("deleted"))
    print(f"\nTotal: {deleted}/{len(results)} deleted.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
