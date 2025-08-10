// ==UserScript==
// @name         updateTokenBearer
// @namespace    https://gapowork.vn
// @version      1.3
// @description  Hook token Gapo và chỉ update khi thật sự thay đổi
// @match        https://www.gapowork.vn/*
// @grant        none
// ==/UserScript==

(function() {
    'use strict';

    const sheetAPI = "https://script.google.com/macros/s/AKfycbxppPhpPyyWzzSDodrxZcy8_SaZVyk40ij5q2McMbXTMaYVKZAmFU9f8JNMA4R4qX5E/exec";
    let lastToken = localStorage.getItem("_lastGapoToken") || "";

    let debounceTimer = null;
    function updateA2(newValue) {
        clearTimeout(debounceTimer);
        debounceTimer = setTimeout(() => {
            fetch(`${sheetAPI}?token=${encodeURIComponent(newValue)}`)
                .then(r => r.text())
                .then(t => console.log("✅ Cập nhật A2:", t))
                .catch(e => console.error(e));
        }, 500); // đợi 0.5s để gom call
    }

    function handleToken(token) {
        if (token && token.startsWith("Bearer ") && token !== lastToken) {
            lastToken = token;
            localStorage.setItem("_lastGapoToken", token);
            console.log("🆕 Token mới:", token);
            updateA2(token);
        }
    }

    // Hook fetch
    const origFetch = window.fetch;
    window.fetch = function(...args) {
        const token = args[1]?.headers?.Authorization || args[1]?.headers?.authorization;
        handleToken(token);
        return origFetch.apply(this, args);
    };

    // Hook XMLHttpRequest
    const origSetRequestHeader = XMLHttpRequest.prototype.setRequestHeader;
    XMLHttpRequest.prototype.setRequestHeader = function(header, value) {
        if (header.toLowerCase() === 'authorization') {
            handleToken(value);
        }
        return origSetRequestHeader.call(this, header, value);
    };
})();