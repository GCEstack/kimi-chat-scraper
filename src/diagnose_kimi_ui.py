#!/usr/bin/env python3
"""Inspect the Kimi web UI for automation hooks (New Chat button, title editing, tags)."""

from __future__ import annotations

import json
import os
import subprocess
import sys
import time
import urllib.request
from pathlib import Path
from typing import Any

DAEMON_PORT = 10086
DAEMON_URL = f"http://127.0.0.1:{DAEMON_PORT}/command"
STATUS_URL = f"http://127.0.0.1:{DAEMON_PORT}/status"
CHROME_PATH = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
WEBBRIDGE_BIN = os.path.expandvars(r"%USERPROFILE%\.kimi-webbridge\bin\kimi-webbridge.exe")
KIMI_URL = "https://www.kimi.com/"


def daemon_status() -> dict[str, Any]:
    try:
        with urllib.request.urlopen(STATUS_URL, timeout=3) as r:
            return json.loads(r.read().decode())
    except Exception as e:
        return {"running": False, "error": str(e)}


def start_daemon() -> bool:
    print("Starting Kimi WebBridge daemon...")
    proc = subprocess.run([WEBBRIDGE_BIN, "start"], capture_output=True, text=True, shell=False)
    return proc.returncode == 0


def chrome_is_running() -> bool:
    try:
        output = subprocess.check_output(
            ["tasklist", "/FI", "IMAGENAME eq chrome.exe"], text=True, shell=False
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


PROBE_JS = r"""
(() => {
  function describe(el) {
    if (!el) return null;
    return {
      tag: el.tagName,
      text: el.innerText?.slice(0, 120) || null,
      ariaLabel: el.getAttribute('aria-label'),
      title: el.getAttribute('title'),
      role: el.getAttribute('role'),
      className: el.className?.slice(0, 200) || null,
      href: el.getAttribute('href'),
      id: el.id || null,
    };
  }

  // Look for New Chat triggers.
  const newChatCandidates = Array.from(document.querySelectorAll('button, a, div[role="button"], div'))
    .filter(el => /new chat|新建对话|开始新对话|new conversation/i.test(el.innerText || el.getAttribute('aria-label') || ''))
    .slice(0, 5)
    .map(describe);

  // Look for sidebar top controls.
  const sidebar = document.querySelector('aside, [role="complementary"], nav');
  const sidebarTop = sidebar
    ? Array.from(sidebar.querySelectorAll('button, a, div[role="button"]')).slice(0, 8).map(describe)
    : [];

  // Look for tag-related UI.
  const tagCandidates = Array.from(document.querySelectorAll('*'))
    .filter(el => /tag|标签|folder|文件夹/i.test(el.innerText || el.getAttribute('aria-label') || ''))
    .slice(0, 8)
    .map(describe);

  // Current chat title if any.
  const titleEl = document.querySelector('h1, [class*="title" i], [class*="chat-title" i]');

  return {
    url: location.href,
    pathname: location.pathname,
    newChatCandidates,
    sidebarTop,
    tagCandidates,
    currentTitle: titleEl ? describe(titleEl) : null,
  };
})();
"""


def find_kimi_tab() -> Any | None:
    tabs_resp = send_command("list_tabs", {}, "diagnose-tabs")
    print("Raw list_tabs response:")
    print(json.dumps(tabs_resp, indent=2, ensure_ascii=False))
    tabs = tabs_resp.get("data") if isinstance(tabs_resp, dict) else tabs_resp
    if not isinstance(tabs, list):
        return None
    for tab in tabs:
        url = tab.get("url") if isinstance(tab, dict) else str(tab)
        if url and "kimi.com" in url:
            return tab
    return None


def main() -> int:
    session = "kimi-ui-diagnose"
    if not ensure_ready():
        return 1

    print("Looking for an existing Kimi tab...")
    existing = find_kimi_tab()
    if existing:
        if isinstance(existing, dict):
            print(f"Using existing tab: {existing.get('id')} — {existing.get('url')}")
            send_command("navigate", {"url": existing.get("url")}, session)
        else:
            print(f"Using existing tab string: {existing}")
            send_command("navigate", {"url": str(existing)}, session)
    else:
        print("No existing Kimi tab found; opening a new one...")
        send_command("navigate", {"url": KIMI_URL, "newTab": True, "group_title": "Kimi UI Diagnose"}, session)
    time.sleep(4)

    print("Probing DOM...")
    result = evaluate(PROBE_JS, session)
    print(json.dumps(result, indent=2, ensure_ascii=False))

    try:
        send_command("close_session", {}, session)
    except Exception:
        pass
    return 0


if __name__ == "__main__":
    sys.exit(main())
