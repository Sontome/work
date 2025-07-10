from playwright.sync_api import sync_playwright
import json

with sync_playwright() as p:
    browser = p.chromium.connect_over_cdp("http://localhost:9222")
    context = browser.contexts[0]  # lấy context đầu tiên
    cookies = context.cookies("https://p2p.tima.vn")
    
    with open("tabcookies.json", "w") as f:
        json.dump(cookies, f, indent=2)

    print("✅ Đã lưu cookies từ session đang mở!")