// ==UserScript==
// @name         Kimi Chat Web Exporter
// @namespace    http://tampermonkey.net/
// @version      1.0.0
// @description  Export Kimi chat conversations from the web app to normalized JSON.
// @match        https://www.kimi.com/*
// @match        https://kimi.com/*
// @match        https://kimi.moonshot.cn/*
// @grant        GM_registerMenuCommand
// @grant        GM_setValue
// @grant        GM_getValue
// ==/UserScript==

(function () {
    'use strict';

    const CONFIG = {
        // Tag this export so you can tell accounts apart later.
        accountTag: GM_getValue('kimi_account_tag', 'account1'),
        // Delay (ms) between opening chats in auto-walk mode.
        autoWalkDelay: 1200,
        // Max chats to export in auto-walk mode (0 = unlimited).
        maxChats: 0,
    };

    // In-memory store of captured conversations.
    const conversations = new Map();

    // ── Utils ────────────────────────────────────────────────────────────────

    function nowISO() {
        return new Date().toISOString();
    }

    function safeFilename(name) {
        return String(name || 'untitled')
            .replace(/[<>:"/\\|?*\x00-\x1f]/g, '_')
            .replace(/\s+/g, ' ')
            .trim()
            .slice(0, 120);
    }

    function downloadJSON(obj, filename) {
        const blob = new Blob([JSON.stringify(obj, null, 2)], { type: 'application/json' });
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = filename;
        document.body.appendChild(a);
        a.click();
        a.remove();
        URL.revokeObjectURL(url);
    }

    function normalizeMessage(msg) {
        // Accept a wide range of shapes from API or DOM scraping.
        const role =
            msg.role ||
            msg.sender ||
            (msg.type === 'user' ? 'user' : msg.type === 'bot' ? 'assistant' : 'unknown');
        const content =
            typeof msg.content === 'string'
                ? msg.content
                : Array.isArray(msg.content)
                  ? msg.content.map((c) => (typeof c === 'string' ? c : c.text || '')).join('\n')
                  : msg.text || msg.message || msg.value || JSON.stringify(msg);
        const ts = msg.created_at || msg.timestamp || msg.time || msg.createTime || null;
        return {
            role: role === 'bot' || role === 'ai' || role === 'model' ? 'assistant' : 'user',
            content: String(content || ''),
            timestamp: ts ? new Date(ts).toISOString() : null,
        };
    }

    function mergeConversation(conv) {
        const existing = conversations.get(conv.id);
        if (!existing) {
            conversations.set(conv.id, conv);
            return;
        }
        // Merge messages by timestamp + content hash to avoid duplicates.
        const seen = new Set(existing.messages.map((m) => `${m.timestamp}|${m.content.slice(0, 80)}`));
        for (const m of conv.messages) {
            const key = `${m.timestamp}|${m.content.slice(0, 80)}`;
            if (!seen.has(key)) {
                existing.messages.push(m);
                seen.add(key);
            }
        }
        existing.messages.sort((a, b) => {
            const ta = a.timestamp ? new Date(a.timestamp) : new Date(0);
            const tb = b.timestamp ? new Date(b.timestamp) : new Date(0);
            return ta - tb;
        });
        if (conv.title) existing.title = conv.title;
        if (conv.updated_at) existing.updated_at = conv.updated_at;
    }

    // ── API interception ─────────────────────────────────────────────────────

    function parseAPIResponse(url, data) {
        try {
            const text = typeof data === 'string' ? data : JSON.stringify(data);
            if (!text || text.length < 2) return;

            const lower = url.toLowerCase();
            const isChatEndpoint =
                /kimi/.test(lower) &&
                (/chat|conversation|message|session|history|list|threads/.test(lower) ||
                    /api/.test(lower));
            if (!isChatEndpoint) return;

            const json = typeof data === 'string' ? JSON.parse(data) : data;
            const payloads = Array.isArray(json) ? json : [json];

            for (const payload of payloads) {
                if (!payload || typeof payload !== 'object') continue;

                // Heuristic: look for conversation/list shapes.
                const candidates =
                    payload.conversations ||
                    payload.chats ||
                    payload.threads ||
                    payload.data ||
                    payload.items ||
                    payload.messages ||
                    (payload.id && payload.messages ? [payload] : []);

                if (!Array.isArray(candidates)) continue;

                for (const item of candidates) {
                    if (!item || typeof item !== 'object') continue;
                    const messages = Array.isArray(item.messages)
                        ? item.messages.map(normalizeMessage)
                        : [];
                    if (!messages.length && !item.id) continue;

                    const id = item.id || item.conversation_id || item.chat_id || item.session_id;
                    const title =
                        item.title ||
                        item.name ||
                        item.topic ||
                        (messages[0] ? messages[0].content.slice(0, 60) : 'Untitled');
                    mergeConversation({
                        id: String(id || `unknown-${Date.now()}-${Math.random().toString(36).slice(2, 7)}`),
                        title: String(title),
                        created_at: item.created_at ? new Date(item.created_at).toISOString() : null,
                        updated_at: item.updated_at ? new Date(item.updated_at).toISOString() : null,
                        messages,
                    });
                }
            }
        } catch (e) {
            // Silently ignore parse failures so we don't break the app.
        }
    }

    // Patch fetch.
    const origFetch = window.fetch;
    window.fetch = async function (...args) {
        const response = await origFetch.apply(this, args);
        try {
            const url = typeof args[0] === 'string' ? args[0] : args[0].url;
            const clone = response.clone();
            const text = await clone.text();
            parseAPIResponse(url, text);
        } catch (e) {
            /* ignore */ }
        return response;
    };

    // Patch XHR.
    const origOpen = XMLHttpRequest.prototype.open;
    const origSend = XMLHttpRequest.prototype.send;
    XMLHttpRequest.prototype.open = function (method, url, ...rest) {
        this._kimi_url = url;
        return origOpen.call(this, method, url, ...rest);
    };
    XMLHttpRequest.prototype.send = function (...args) {
        this.addEventListener('load', function () {
            try {
                parseAPIResponse(this._kimi_url, this.responseText);
            } catch (e) {
                /* ignore */ }
        });
        return origSend.apply(this, args);
    };

    // ── DOM scraping fallback ────────────────────────────────────────────────

    function scrapeVisibleChat() {
        // These selectors are best-guess. Update them if Kimi changes its layout.
        const titleEl =
            document.querySelector('h1, .chat-title, [class*="title" i]') ||
            document.querySelector('[class*="conversation" i] [class*="name" i]');
        const title = titleEl ? titleEl.innerText.trim() : 'Untitled';

        const messageEls = document.querySelectorAll(
            '[class*="message" i], [class*="bubble" i], [class*="chat-item" i], .message'
        );
        const messages = [];
        messageEls.forEach((el) => {
            const isUser =
                /user|me|right|human/.test(el.className + ' ' + (el.getAttribute('data-role') || ''));
            const textEl = el.querySelector('p, [class*="content" i], [class*="text" i]') || el;
            const text = textEl.innerText.trim();
            if (!text) return;
            messages.push({
                role: isUser ? 'user' : 'assistant',
                content: text,
                timestamp: null,
            });
        });

        if (!messages.length) return null;
        return {
            id: `dom-${location.pathname.replace(/\//g, '-')}-${Date.now()}`,
            title,
            created_at: nowISO(),
            updated_at: nowISO(),
            messages,
        };
    }

    // ── Auto-walk sidebar ────────────────────────────────────────────────────

    function findSidebarItems() {
        return document.querySelectorAll(
            'nav [class*="chat" i], nav [class*="conversation" i], nav [class*="session" i], nav [class*="item" i], nav a, [class*="sidebar" i] [class*="item" i]'
        );
    }

    async function autoWalkAndExport() {
        const items = findSidebarItems();
        if (!items.length) {
            alert('Kimi Exporter: Could not find chat list items. Try scrolling the sidebar first, then export again.');
            return;
        }
        const limit = CONFIG.maxChats > 0 ? Math.min(CONFIG.maxChats, items.length) : items.length;
        for (let i = 0; i < limit; i++) {
            items[i].click();
            await new Promise((r) => setTimeout(r, CONFIG.autoWalkDelay));
            const scraped = scrapeVisibleChat();
            if (scraped) mergeConversation(scraped);
        }
        exportToFile();
    }

    // ── Export ───────────────────────────────────────────────────────────────

    function exportToFile() {
        if (!conversations.size) {
            alert('Kimi Exporter: No conversations captured yet. Open some chats or wait for API responses.');
            return;
        }
        const payload = {
            metadata: {
                account_tag: CONFIG.accountTag,
                source: 'web',
                exported_at: nowISO(),
            },
            conversations: Array.from(conversations.values()),
        };
        const date = new Date().toISOString().replace(/[:T]/g, '-').slice(0, 19);
        const filename = `kimi-web-${CONFIG.accountTag}-${date}.json`;
        downloadJSON(payload, filename);
    }

    function setAccountTag() {
        const tag = prompt('Account tag for this export (e.g., account1, work, personal):', CONFIG.accountTag);
        if (tag) {
            CONFIG.accountTag = tag.trim();
            GM_setValue('kimi_account_tag', CONFIG.accountTag);
        }
    }

    // ── UI ───────────────────────────────────────────────────────────────────

    function injectButton() {
        if (document.getElementById('kimi-export-btn')) return;

        const btn = document.createElement('button');
        btn.id = 'kimi-export-btn';
        btn.innerText = '📥 Export Kimi Chats';
        btn.style.cssText =
            'position:fixed;bottom:24px;right:24px;z-index:2147483647;' +
            'padding:12px 18px;background:#4f46e5;color:#fff;border:none;border-radius:8px;' +
            'cursor:pointer;font-weight:bold;box-shadow:0 4px 12px rgba(0,0,0,0.15);';
        btn.onclick = exportToFile;
        document.body.appendChild(btn);
    }

    function injectMenu() {
        GM_registerMenuCommand('📥 Export captured chats now', exportToFile);
        GM_registerMenuCommand('🚶 Auto-walk sidebar and export', autoWalkAndExport);
        GM_registerMenuCommand('🏷️ Set account tag', setAccountTag);
    }

    // ── Init ─────────────────────────────────────────────────────────────────

    function init() {
        injectMenu();
        if (document.readyState === 'loading') {
            document.addEventListener('DOMContentLoaded', injectButton);
        } else {
            injectButton();
        }
        // Also try to re-inject button if the SPA re-renders.
        setInterval(injectButton, 3000);
    }

    init();
})();
