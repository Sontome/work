import pychrome
import time
import subprocess
import json
import os
import signal
import psutil  # pip install psutil
from threading import Timer


# ----------- ⚙️ CONFIG ------------ #
USERNAME = "your_username"
PASSWORD = "your_password"
LOGIN_URL = "https://p2p.tima.vn/loanbrief/lender.html"
CHROME_PATH = "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe"
CHROME_DEBUG_PROFILE = "C:\\chrome_debug_profile"
RELOAD_INTERVAL = 300  # mỗi 5 phút = 300 giây
# ---------------------------------- #

# 🚫 Kill all chrome processes
def kill_all_chrome():
    for proc in psutil.process_iter(['pid', 'name']):
        if proc.info['name'] and "chrome" in proc.info['name'].lower():
            try:
                print(f"⚠️ Kill Chrome PID: {proc.pid}")
                proc.kill()
            except Exception as e:
                print(f"Không kill được Chrome PID {proc.pid}: {e}")

# ✅ Hàm reload lại trang mỗi 5 phút
def auto_reload(tab):
    def reload_now():
        try:
            print("🔁 Tự động F5 trang")
            tab.call_method("Page.reload")
        except Exception as e:
            print("Lỗi reload:", e)
        Timer(RELOAD_INTERVAL, reload_now).start()  # Đặt lại timer
    Timer(RELOAD_INTERVAL, reload_now).start()

# 🧠 Chờ tới khi có thể nhập user/pass
def wait_until_input_ready(tab, timeout=10):
    start = time.time()
    while time.time() - start < timeout:
        res = tab.call_method("Runtime.evaluate", expression='''
            !!document.querySelector("input[name='username']")
        ''')
        if res.get("result", {}).get("value"):
            return True
        time.sleep(0.5)
    return False

# 💥 CHẠY MAIN
kill_all_chrome()
time.sleep(1)

# Mở Chrome debug mode
subprocess.Popen([
    CHROME_PATH,
    "--remote-debugging-port=9222",
    f"--user-data-dir={CHROME_DEBUG_PROFILE}"
])

time.sleep(2)  # Đợi Chrome khởi động

# Kết nối vào DevTools
browser = pychrome.Browser(url="http://127.0.0.1:9222")
tab = browser.new_tab()
tab.start()

tab.call_method("Page.enable")
tab.call_method("DOM.enable")
tab.call_method("Runtime.enable")

# Mở trang login
tab.call_method("Page.navigate", url=LOGIN_URL)
time.sleep(10)

if wait_until_input_ready(tab):
    # Điền user/pass và click login
    tab.call_method("Runtime.evaluate", expression=f'''
        document.querySelector("input[name='username']").value = "";
        document.querySelector("input[name='password']").value = "";
    ''')
    time.sleep(2)
    tab.call_method("Runtime.evaluate", expression=f'''
        document.querySelector("input[name='username']").value = "0367507100";
        document.querySelector("input[name='password']").value = "123456";
    ''')
    time.sleep(3)
    # tab.call_method("Page.reload")
    # time.sleep(0.5)
    tab.call_method("Runtime.evaluate", expression='''
        document.querySelector(".btn.btn-primary.font-weight-bold.px-9.py-4.my-3.mx-4").click();
    ''')
    print("✅ Đã click login!")
else:
    print("❌ Không tìm thấy form đăng nhập")

# Tự động reload mỗi 5 phút
auto_reload(tab)

# Chờ tay Enter để dừng (hoặc giữ script chạy hoài để auto reload)
input("⏳ Nhấn Enter để dừng lại...\n")

# Lưu cookies
cookies = tab.call_method("Network.getAllCookies")["cookies"]
with open("tabcookies.json", "w", encoding="utf-8") as f:
    json.dump(cookies, f, indent=2)

print("✅ Cookies đã lưu!")
