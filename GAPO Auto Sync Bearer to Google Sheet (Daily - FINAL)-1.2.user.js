// ==UserScript==
// @name         GAPO Auto Sync Bearer to Google Sheet (Daily - FINAL)
// @namespace    http://tampermonkey.net/
// @version      1.2
// @description  Tự động bắt Bearer GAPO và update Google Sheet mỗi ngày 1 lần (bypass CORS)
// @match        https://www.gapowork.vn/*
// @run-at       document-start
// @grant        GM_xmlhttpRequest
// @grant        unsafeWindow
// ==/UserScript==

(function () {
    'use strict';

    // ====== CONFIG ======
    const WEB_APP_URL = 'https://script.google.com/macros/s/AKfycbyGAGvpmfwdZETnlkMAKHitcjewRMmkooCKqXkh_MH5aDfuCArILOA2__FmMchEz5tk/exec';
    const BEARER_PREFIX = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImp0aSI'; // prefix để nhận diện
    const STORAGE_KEY = 'GAPO_BEARER_LAST_SYNC_DATE';

    // ====== UTILS ======
    const todayKey = () => new Date().toISOString().slice(0, 10);
    const canSyncToday = () => localStorage.getItem(STORAGE_KEY) !== todayKey();
    const markSynced = () => localStorage.setItem(STORAGE_KEY, todayKey());

    function sendBearerToWebApp(bearer) {
        if (!canSyncToday()) {
            console.log('😴 Hôm nay sync rồi, skip cho đỡ xàm lol');
            return;
        }

        console.warn('🔥 BẮT ĐƯỢC BEARER → GỬI LÊN WEB APP');

        GM_xmlhttpRequest({
            method: 'POST',
            url: WEB_APP_URL,
            headers: {
                'Content-Type': 'application/json'
            },
            data: JSON.stringify({
                bearer: bearer,
                from: 'tampermonkey',
                ts: Date.now()
            }),
            onload: function (res) {
                console.log('✅ WebApp phản hồi:', res.responseText);
                markSynced();
            },
            onerror: function (err) {
                console.error('❌ Gửi bearer lỗi vl:', err);
            }
        });
    }

    const w = unsafeWindow || window;

    // ====== HOOK FETCH ======
    const _fetch = w.fetch;
    if (typeof _fetch === 'function') {
        w.fetch = function (...args) {
            try {
                const [, init = {}] = args;
                const headers = init.headers || {};

                let auth = '';
                if (headers instanceof Headers) {
                    auth = headers.get('authorization') || headers.get('Authorization') || '';
                } else {
                    auth = headers.authorization || headers.Authorization || '';
                }

                if (auth && auth.includes(BEARER_PREFIX)) {
                    const token = auth.replace(/^Bearer\s+/i, '');
                    sendBearerToWebApp(token);
                }
            } catch (e) {
                // ignore
            }
            return _fetch.apply(this, args);
        };
    }

    // ====== HOOK XHR ======
    const setHeader = XMLHttpRequest.prototype.setRequestHeader;
    XMLHttpRequest.prototype.setRequestHeader = function (key, value) {
        try {
            if (key.toLowerCase() === 'authorization' && value.includes(BEARER_PREFIX)) {
                const token = value.replace(/^Bearer\s+/i, '');
                sendBearerToWebApp(token);
            }
        } catch (e) {
            // ignore
        }
        return setHeader.call(this, key, value);
    };

    console.log('%c🚀 GAPO Auto Bearer Sync ON – mỗi ngày 1 phát, mượt vl', 'color:lime;font-weight:bold');
})();