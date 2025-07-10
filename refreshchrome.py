import pychrome
import time
from threading import Timer

RELOAD_INTERVAL = 30 * 60  # 30 phút = 1800 giây

def auto_reload(tab):
    def reload_tab():
        try:
            print("🔁 F5 trang giữ sống session...")
            tab.call_method("Page.reload")
        except Exception as e:
            print("❌ Reload lỗi:", e)
        Timer(RELOAD_INTERVAL, reload_tab).start()
    
    Timer(RELOAD_INTERVAL, reload_tab).start()
# Giữ script chạy

# ----- Kết nối tới tab Chrome đang chạy -----
browser = pychrome.Browser(url="http://127.0.0.1:9222")
tabs = browser.list_tab()

# Tìm tab đang mở đúng trang tima (đại ca login thủ công trước nhé)
for tab in tabs:
    try:
        tab.start()
        tab.call_method("Page.enable")
        tab_url = tab.call_method("Runtime.evaluate", expression="window.location.href")["result"]["value"]
        if "p2p.tima.vn" in tab_url:
            print("✅ Tìm thấy tab tima:", tab_url)
            auto_reload(tab)
            break
        tab.stop()
    except Exception as e:
        print("❌ Lỗi khi kiểm tra tab:", e)

while True:
    time.sleep(15)