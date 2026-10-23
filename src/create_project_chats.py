#!/usr/bin/env python3
"""Create new Kimi chats titled after projects via the Kimi WebBridge."""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
import time
import urllib.request
from typing import Any

DAEMON_PORT = 10086
DAEMON_URL = f"http://127.0.0.1:{DAEMON_PORT}/command"
STATUS_URL = f"http://127.0.0.1:{DAEMON_PORT}/status"
CHROME_PATH = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
WEBBRIDGE_BIN = os.path.expandvars(r"%USERPROFILE%\.kimi-webbridge\bin\kimi-webbridge.exe")
NEW_CHAT_URL = "https://www.kimi.com/?chat_enter_method=new_chat"


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


def launch_chrome(url: str = "https://www.kimi.com/") -> bool:
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


INPUT_PROBE_JS = r"""
(() => {
  function describe(el) {
    if (!el) return null;
    return {
      tag: el.tagName,
      className: el.className?.slice(0, 200) || null,
      ariaLabel: el.getAttribute('aria-label'),
      role: el.getAttribute('role'),
      contenteditable: el.getAttribute('contenteditable'),
      placeholder: el.getAttribute('placeholder'),
    };
  }

  const candidates = [];
  // Textarea inputs.
  document.querySelectorAll('textarea').forEach((el, i) => {
    if (i < 3) candidates.push({type: 'textarea', ...describe(el)});
  });
  // Contenteditable.
  document.querySelectorAll('[contenteditable="true"]').forEach((el, i) => {
    if (i < 3) candidates.push({type: 'contenteditable', ...describe(el)});
  });
  // Send buttons.
  document.querySelectorAll('button').forEach((el, i) => {
    if (i < 3 && /send|submit/i.test(el.innerText + ' ' + el.getAttribute('aria-label'))) {
      candidates.push({type: 'send-button', text: el.innerText?.slice(0, 40), ...describe(el)});
    }
  });
  return {url: location.href, pathname: location.pathname, candidates};
})();
"""


def find_input_selector(session: str) -> str:
    """Probe the new-chat page to find the best input selector."""
    probe = evaluate(INPUT_PROBE_JS, session)
    print("Input probe:", json.dumps(probe, indent=2, ensure_ascii=False))

    candidates = probe.get("candidates", [])
    for c in candidates:
        if c.get("type") == "textarea" and c.get("className"):
            return f"textarea.{'.'.join(c['className'].split())}"
        if c.get("type") == "contenteditable" and c.get("className"):
            return f"[contenteditable='true'].{'.'.join(c['className'].split())}"

    # Fallbacks.
    if any(c.get("type") == "textarea" for c in candidates):
        return "textarea"
    if any(c.get("type") == "contenteditable" for c in candidates):
        return "[contenteditable='true']"
    raise RuntimeError("Could not locate a chat input box on the new-chat page.")


def create_chat(title: str, session: str, input_selector: str, delay: int = 2000) -> dict[str, Any]:
    print(f"\nCreating chat: {title}")
    send_command("navigate", {"url": NEW_CHAT_URL, "newTab": True}, session)
    time.sleep(2)

    # Wait for input.
    deadline = time.time() + 10
    while time.time() < deadline:
        present = evaluate(f"!!document.querySelector({json.dumps(input_selector)})", session)
        if present:
            break
        time.sleep(0.5)

    # Focus and inject text via InputEvent so React/TipTap registers it.
    type_js = f"""
    (() => {{
      const el = document.querySelector({json.dumps(input_selector)});
      if (!el) return {{error: 'input not found'}};
      el.focus();
      el.click();
      const ev = new InputEvent('beforeinput', {{
        bubbles: true,
        cancelable: true,
        inputType: 'insertText',
        data: {json.dumps(title)},
      }});
      el.dispatchEvent(ev);
      return {{ok: true, defaultPrevented: ev.defaultPrevented}};
    }})();
    """
    result = evaluate(type_js, session)
    print("  type result:", result)
    time.sleep(1)

    # Click the send button that appears after text is entered.
    submit_js = """
    (() => {
      const btn = document.querySelector('.send-button-container');
      if (!btn) return {error: 'send button not found'};
      btn.click();
      return {ok: true};
    })();
    """
    result = evaluate(submit_js, session)
    print("  submit result:", result)

    # Wait for navigation to a real chat URL.
    nav_deadline = time.time() + 10
    while time.time() < nav_deadline:
        pathname = evaluate("location.pathname", session)
        if pathname and pathname.startswith("/chat/"):
            break
        time.sleep(0.5)
    time.sleep(delay / 1000)

    return {
        "title": title,
        "url": evaluate("location.href", session),
        "pathname": evaluate("location.pathname", session),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Create blank Kimi project chats via WebBridge")
    parser.add_argument("titles", nargs="+", help="Chat titles to create")
    parser.add_argument("--session", default="kimi-create-chats", help="WebBridge session name")
    parser.add_argument("--delay", type=int, default=2500, help="Ms to wait after submitting each chat")
    args = parser.parse_args()

    if not ensure_ready():
        return 1

    session = args.session
    try:
        print("Opening a probe new-chat tab to locate the input box...")
        send_command("navigate", {"url": NEW_CHAT_URL, "newTab": True, "group_title": "Project Chats"}, session)
        time.sleep(3)
        input_selector = find_input_selector(session)
        print(f"Using input selector: {input_selector}")

        created = []
        for title in args.titles:
            info = create_chat(title, session, input_selector, delay=args.delay)
            created.append(info)
            print(f"  -> {info['url']}")

        print("\nCreated chats:")
        for c in created:
            print(f"  {c['title']}: {c['url']}")

    finally:
        try:
            send_command("close_session", {}, session)
        except Exception:
            pass

    return 0


if __name__ == "__main__":
    sys.exit(main())
