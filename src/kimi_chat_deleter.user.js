// ==UserScript==
// @name         Kimi Chat Bulk Deleter
// @namespace    http://tampermonkey.net/
// @version      0.1.0
// @description  Learn Kimi's delete API from one manual delete, then bulk-delete chats via API replay (dry-run first). Safer than DOM right-clicking.
// @match        https://www.kimi.com/*
// @match        https://kimi.com/*
// @match        https://kimi.moonshot.cn/*
// @grant        GM_registerMenuCommand
// @grant        GM_setValue
// @grant        GM_getValue
// ==/UserScript==

(function () {
    'use strict';

    // ── Config / state ─────────────────────────────────────────────────────────

    // Chats whose title matches any of these (case-insensitive) are NEVER deleted.
    const PROTECTED_PATTERNS = [
        // /important/i, /do not delete/i, ...
    ];

    // Collected chat list: id -> { id, title, href? }
    const knownChats = new Map();

    // The captured delete request template, learned from one manual delete.
    // { method, urlTemplate, headers, bodyTemplate, idParam }
    let deleteTemplate = GM_getValue('kimi_delete_template', null); // persisted

    // Hook bookkeeping
    let captureNextDelete = false; // set true by "Learn" command

    // ── Utils ──────────────────────────────────────────────────────────────────

    function isProtected(title) {
        const t = String(title || '').toLowerCase();
        return PROTECTED_PATTERNS.some((re) => re.test(t));
    }

    function logLine(msg, kind = 'info') {
        const panel = document.getElementById('kimi-del-log');
        if (!panel) { console.log('[KimiDeleter]', msg); return; }
        const time = new Date().toLocaleTimeString();
        const line = document.createElement('div');
        line.style.color = kind === 'error' ? '#fca5a5' : kind === 'ok' ? '#86efac' : kind === 'warn' ? '#fcd34d' : '#e5e7eb';
        line.textContent = `[${time}] ${msg}`;
        panel.appendChild(line);
        panel.scrollTop = panel.scrollHeight;
    }

    // ── Network interception (capture chat list + learn delete API) ─────────────

    function extractChatIds(url, text) {
        try {
            const lower = String(url).toLowerCase();
            if (!/kimi/.test(lower)) return;
            const listish = /chat|conversation|message|session|history|list|threads/.test(lower);
            if (!listish) return;
            const json = JSON.parse(text);
            const payloads = Array.isArray(json) ? json : [json];
            for (const p of payloads) {
                if (!p || typeof p !== 'object') continue;
                const candidates = p.conversations || p.chats || p.threads || p.data || p.items || (p.id ? [p] : []);
                if (!Array.isArray(candidates)) continue;
                for (const c of candidates) {
                    if (!c || typeof c !== 'object') continue;
                    const id = c.id || c.conversation_id || c.chat_id || c.session_id || c.object_id;
                    if (!id) continue;
                    const title = c.title || c.name || c.topic || '(untitled)';
                    knownChats.set(String(id), { id: String(id), title: String(title) });
                }
            }
        } catch (e) { /* ignore */ }
    }

    // Try to learn the delete call from a single observed request.
    function maybeLearnDelete(method, url, body, headersSrc) {
        const m = String(method || '').toUpperCase();
        const u = String(url || '');
        const looksLikeDelete =
            m === 'DELETE' ||
            /delete|remove|trash|destroy/i.test(u) ||
            (m === 'POST' && /delete|remove/i.test(u));

        if (!looksLikeDelete) return false;
        if (!captureNextDelete && deleteTemplate) return false;

        // Extract the chat id from the URL or body so we can templatize.
        let idParam = null;
        let urlTemplate = u;
        let bodyTemplate = body;

        // id embedded in path: /api/chat/<id>  or /chat/<id>
        const pathMatch = u.match(/(?:chat|conversation|session)s?\/([^/?#]+)/i);
        if (pathMatch) {
            idParam = pathMatch[1];
            urlTemplate = u.replace(pathMatch[1], '__CHAT_ID__');
        }
        // id in body JSON: {"chat_id":"...","object_id":"...","id":"..."}
        if (!idParam && body) {
            const bm = body.match(/"(?:chat_id|conversation_id|object_id|session_id|id)"\s*:\s*"([^"]+)"/);
            if (bm) {
                idParam = bm[1];
                bodyTemplate = body.replace(bm[1], '__CHAT_ID__');
            }
        }

        if (!idParam) return false; // couldn't isolate an id; skip

        deleteTemplate = {
            method: m,
            urlTemplate,
            bodyTemplate,
            idParam,
            learnedAt: new Date().toISOString(),
        };
        GM_setValue('kimi_delete_template', deleteTemplate);
        captureNextDelete = false;
        logLine(`✅ Learned delete API: ${m} ${urlTemplate}`, 'ok');
        return true;
    }

    // Patch fetch.
    const origFetch = window.fetch;
    window.fetch = async function (input, init) {
        try {
            const url = typeof input === 'string' ? input : (input && input.url) || '';
            const method = (init && init.method) || (input && input.method) || 'GET';
            const body = init && init.body ? String(init.body) : null;
            maybeLearnDelete(method, url, body);
            const res = await origFetch.apply(this, arguments);
            // capture chat list ids
            try {
                const clone = res.clone();
                const text = await clone.text();
                extractChatIds(url, text);
            } catch (e) { /* ignore */ }
            return res;
        } catch (e) {
            throw e;
        }
    };

    // Patch XHR.
    const origOpen = XMLHttpRequest.prototype.open;
    const origSend = XMLHttpRequest.prototype.send;
    XMLHttpRequest.prototype.open = function (method, url, ...rest) {
        this.__kimi_method = method;
        this.__kimi_url = url;
        return origOpen.call(this, method, url, ...rest);
    };
    XMLHttpRequest.prototype.send = function (body) {
        this.addEventListener('load', () => {
            try {
                maybeLearnDelete(this.__kimi_method, this.__kimi_url, body ? String(body) : null);
                extractChatIds(this.__kimi_url, this.responseText);
            } catch (e) { /* ignore */ }
        });
        return origSend.apply(this, arguments);
    };

    // ── Execution: replay the learned delete for a list of ids ──────────────────

    let stopRequested = false;

    async function replayDelete(chatId) {
        if (!deleteTemplate) throw new Error('Delete API not learned yet');
        const t = deleteTemplate;
        const url = t.urlTemplate.replace(/__CHAT_ID__/g, encodeURIComponent(chatId));
        const opts = { method: t.method, credentials: 'include', headers: {} };
        // Let the browser send cookies; add json header if there's a body.
        if (t.bodyTemplate) {
            opts.headers['Content-Type'] = 'application/json';
            opts.body = t.bodyTemplate.replace(/__CHAT_ID__/g, chatId);
        }
        const res = await fetch(url, opts);
        return res.ok;
    }

    async function bulkDelete(dryRun) {
        stopRequested = false;
        if (knownChats.size === 0) {
            logLine('No chats captured yet. Scroll/load the chat list first, or open a chat so the list API fires.', 'warn');
            return;
        }

        const targets = [];
        const protectedHits = [];
        for (const [id, c] of knownChats) {
            if (isProtected(c.title)) { protectedHits.push(c); continue; }
            targets.push(c);
        }

        if (protectedHits.length) {
            logLine(`Protecting ${protectedHits.length} chat(s): ${protectedHits.map((c) => `"${c.title}"`).join(', ')}`, 'warn');
        }

        if (dryRun) {
            logLine(`DRY RUN — would delete ${targets.length} chat(s):`, 'info');
            targets.forEach((c) => logLine(`   • ${c.title}  (${c.id})`));
            return;
        }

        // Confirm gate.
        if (!deleteTemplate) {
            logLine('No delete API learned. Use the menu command to enable "Learn" then delete ONE chat by hand first.', 'error');
            return;
        }
        const really = confirm(
            `Delete ${targets.length} chat(s) via API (${deleteTemplate.method} ${deleteTemplate.urlTemplate})?\n\n` +
            `This cannot be undone. Protected: ${protectedHits.length}.`
        );
        if (!really) { logLine('Cancelled.', 'warn'); return; }

        logLine(`Starting deletion of ${targets.length} chat(s)...`, 'info');
        let ok = 0, fail = 0;
        for (let i = 0; i < targets.length; i++) {
            if (stopRequested) { logLine('STOPPED by user.', 'warn'); break; }
            const c = targets[i];
            try {
                const success = await replayDelete(c.id);
                if (success) { ok++; logLine(`✓ [${i + 1}/${targets.length}] ${c.title}`, 'ok'); }
                else { fail++; logLine(`✗ [${i + 1}/${targets.length}] ${c.title} (HTTP non-OK)`, 'error'); }
            } catch (e) {
                fail++;
                logLine(`✗ [${i + 1}/${targets.length}] ${c.title} — ${e.message}`, 'error');
            }
            await new Promise((r) => setTimeout(r, 500)); // throttle
        }
        logLine(`Done. Deleted: ${ok}, failed: ${fail}.`, 'ok');
    }

    // ── UI ──────────────────────────────────────────────────────────────────────

    function injectPanel() {
        if (document.getElementById('kimi-del-panel')) return;
        const panel = document.createElement('div');
        panel.id = 'kimi-del-panel';
        panel.style.cssText =
            'position:fixed;bottom:80px;right:24px;z-index:2147483647;width:320px;' +
            'background:#1f2937;color:#fff;border-radius:10px;box-shadow:0 8px 24px rgba(0,0,0,0.3);' +
            'font:13px/1.4 -apple-system,Segoe UI,sans-serif;overflow:hidden;';
        panel.innerHTML = `
            <div style="padding:10px 12px;background:#111827;font-weight:bold;display:flex;justify-content:space-between;align-items:center;">
                <span>Kimi Bulk Deleter</span>
                <span id="kimi-del-status" style="font-weight:normal;font-size:11px;color:#9ca3af;">idle</span>
            </div>
            <div style="padding:8px 12px;font-size:11px;color:#9ca3af;border-bottom:1px solid #374151;">
                Known chats: <span id="kimi-del-count">0</span> · API: <span id="kimi-del-api">${deleteTemplate ? 'learned' : 'not learned'}</span>
            </div>
            <div style="padding:8px;display:flex;flex-direction:column;gap:6px;">
                <button id="kimi-del-dryrun" style="padding:8px;border:none;border-radius:6px;background:#3b82f6;color:#fff;cursor:pointer;">🔍 Dry-run (list what would be deleted)</button>
                <button id="kimi-del-learn" style="padding:8px;border:none;border-radius:6px;background:#f59e0b;color:#fff;cursor:pointer;">🧪 Learn: delete ONE chat by hand next</button>
                <button id="kimi-del-confirm" style="padding:8px;border:none;border-radius:6px;background:#ef4444;color:#fff;cursor:pointer;">⚠️ Delete ALL (confirm)</button>
                <button id="kimi-del-stop" style="padding:8px;border:none;border-radius:6px;background:#6b7280;color:#fff;cursor:pointer;">⏹ Stop</button>
            </div>
            <div id="kimi-del-log" style="max-height:200px;overflow-y:auto;padding:8px 12px;font-size:11px;font-family:Consolas,monospace;"></div>
        `;
        document.body.appendChild(panel);

        document.getElementById('kimi-del-dryrun').onclick = () => bulkDelete(true);
        document.getElementById('kimi-del-learn').onclick = () => {
            captureNextDelete = true;
            logLine('Learning enabled. Now delete ONE chat by hand in the UI — I will capture the request.', 'warn');
        };
        document.getElementById('kimi-del-confirm').onclick = () => bulkDelete(false);
        document.getElementById('kimi-del-stop').onclick = () => { stopRequested = true; };
    }

    function refreshStatus() {
        const c = document.getElementById('kimi-del-count');
        if (c) c.textContent = String(knownChats.size);
        const api = document.getElementById('kimi-del-api');
        if (api) api.textContent = deleteTemplate ? 'learned' : 'not learned';
    }

    function injectMenu() {
        GM_registerMenuCommand('🔍 Dry-run (list deletable chats)', () => bulkDelete(true));
        GM_registerMenuCommand('🧪 Learn delete API (delete one chat by hand next)', () => {
            captureNextDelete = true;
            logLine('Learning enabled via menu. Delete ONE chat by hand now.', 'warn');
        });
        GM_registerMenuCommand('⚠️ Delete ALL chats (confirm)', () => bulkDelete(false));
        GM_registerMenuCommand('🗑 Forget learned delete API', () => {
            deleteTemplate = null;
            GM_setValue('kimi_delete_template', null);
            logLine('Forgot learned delete API.', 'warn');
        });
    }

    // ── Init ────────────────────────────────────────────────────────────────────

    function init() {
        injectMenu();
        const tryInject = () => { injectPanel(); refreshStatus(); };
        tryInject();
        setInterval(tryInject, 3000);
    }

    init();
})();
