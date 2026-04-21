// ==UserScript==
// @name         GAPO Auto Sync Bearer to Google Sheet (Debug Edition)
// @namespace    http://tampermonkey.net/
// @version      1.3
// @description  Debug bắt Bearer GAPO + log full để soi lỗi nhận diện
// @match        https://www.gapowork.vn/*
// @run-at       document-start
// @grant        GM_xmlhttpRequest
// @grant        unsafeWindow
// ==/UserScript==

(function () {
    'use strict';

    // ====== CONFIG ======
    const WEB_APP_URL = 'https://script.google.com/macros/s/AKfycbyGAGvpmfwdZETnlkMAKHitcjewRMmkooCKqXkh_MH5aDfuCArILOA2__FmMchEz5tk/exec';
    const BEARER_PREFIX = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImp0aSI';
    const STORAGE_KEY = 'GAPO_BEARER_LAST_SYNC_DATE';

    // ====== LOG ======
    const log = (...args) => console.log('%c[DEBUG]', 'color:cyan;font-weight:bold', ...args);
    const warn = (...args) => console.warn('%c[WARN]', 'color:orange;font-weight:bold', ...args);
    const err = (...args) => console.error('%c[ERROR]', 'color:red;font-weight:bold', ...args);

    // ====== UTILS ======
    const todayKey = () => new Date().toISOString().slice(0, 10);

    const canSyncToday = () => {
        const last = localStorage.getItem(STORAGE_KEY);
        const today = todayKey();
        log('Check sync today:', { last, today });
        return last !== today;
    };

    const markSynced = () => {
        localStorage.setItem(STORAGE_KEY, todayKey());
        log('Đã mark synced:', todayKey());
    };

    function sendBearerToWebApp(bearer) {
        log('sendBearerToWebApp() gọi với token:', bearer?.slice(0, 50) + '...');

        if (!bearer) {
            warn('Token rỗng, bỏ qua');
            return;
        }

        if (!canSyncToday()) {
            warn('Hôm nay sync rồi -> skip');
            return;
        }

        warn('🔥 BẮT ĐƯỢC TOKEN -> GỬI WEB APP');

        GM_xmlhttpRequest({
            method: 'POST',
            url: WEB_APP_URL,
            headers: {
                'Content-Type': 'application/json'
            },
            data: JSON.stringify({
                bearer,
                from: 'tampermonkey',
                ts: Date.now()
            }),
            onload: function (res) {
                log('WebApp response:', res.status, res.responseText);
                markSynced();
            },
            onerror: function (e) {
                err('Lỗi gửi WebApp:', e);
            }
        });
    }

    const w = unsafeWindow || window;

    log('Script start...');
    log('unsafeWindow:', !!unsafeWindow);
    log('window.fetch exists:', typeof w.fetch);

    // ====== HOOK FETCH ======
    const _fetch = w.fetch;

    if (typeof _fetch === 'function') {
        w.fetch = function (...args) {
            try {
                log('FETCH CALL:', args);

                const [url, init = {}] = args;
                const headers = init.headers || {};

                let auth = '';

                if (headers instanceof Headers) {
                    auth =
                        headers.get('authorization') ||
                        headers.get('Authorization') ||
                        '';
                } else {
                    auth =
                        headers.authorization ||
                        headers.Authorization ||
                        '';
                }

                log('FETCH URL:', url);
                log('FETCH AUTH HEADER:', auth);

                if (auth) {
                    if (auth.includes(BEARER_PREFIX)) {
                        warn('MATCH PREFIX qua FETCH');
                        const token = auth.replace(/^Bearer\s+/i, '');
                        sendBearerToWebApp(token);
                    } else {
                        warn('Có auth nhưng KHÔNG match prefix');
                    }
                } else {
                    log('Không có Authorization trong fetch');
                }

            } catch (e) {
                err('Lỗi hook fetch:', e);
            }

            return _fetch.apply(this, args);
        };

        log('Đã hook fetch xong');
    } else {
        warn('fetch không tồn tại');
    }

    // ====== HOOK XHR ======
    const open = XMLHttpRequest.prototype.open;
    const setHeader = XMLHttpRequest.prototype.setRequestHeader;

    XMLHttpRequest.prototype.open = function (method, url) {
        this._debug_url = url;
        this._debug_method = method;
        log('XHR OPEN:', method, url);
        return open.apply(this, arguments);
    };

    XMLHttpRequest.prototype.setRequestHeader = function (key, value) {
        try {
            log('XHR HEADER:', key, value);

            if (key.toLowerCase() === 'authorization') {
                if (value.includes(BEARER_PREFIX)) {
                    warn('MATCH PREFIX qua XHR');
                    const token = value.replace(/^Bearer\s+/i, '');
                    sendBearerToWebApp(token);
                } else {
                    warn('Authorization có nhưng không match prefix');
                }
            }
        } catch (e) {
            err('Lỗi hook XHR:', e);
        }

        return setHeader.call(this, key, value);
    };

    log('Đã hook XHR xong');
    console.log('%c🚀 GAPO DEBUG MODE ON', 'color:lime;font-size:16px;font-weight:bold');
})();
