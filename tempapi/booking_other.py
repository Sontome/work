
from playwright.sync_api import TimeoutError,sync_playwright


# =========================
# CONFIG
# =========================






STATE_FILE = "statevna.json"

# =========================
# ROUTE
# =========================
def fill_route(page, from_code, to_code):
    print(f"📍 Route: {from_code} -> {to_code}")

    # nơi đi
    page.select_option("#dep0", value=from_code)

    # nơi đến
    select_destination_city(page, to_code)

    print("✅ Hoàn tất route")

def select_destination_city(page, to_code):
    print(f"🎯 Chọn nơi đến: {to_code}")

    page.click("#arr0_text")

    popup_input = page.locator("#strAirCity")
    popup_input.wait_for(state="visible", timeout=5000)

    popup_input.fill("")
    popup_input.fill(to_code)

    page.wait_for_timeout(300)
    popup_input.press("Enter")

    # selector chuẩn: airport code đầu tiên phải là HAN
    result = page.locator(
        f"a[onclick^=\"setAirCity('{to_code}'\"]"
    ).first

    result.wait_for(state="visible", timeout=5000)
    result.click()

    page.wait_for_function(
        f"document.querySelector('#arr0').value === '{to_code}'"
    )

    print("✅ Đã chọn nơi đến")
def fill_depart_date(page, date_text , date_text_dep1 = ""):
    """
    date_text format: YYYY/MM/DD
    ví dụ: 2026/05/21
    """

    print(f"📅 Chọn ngày đi: {date_text}")

    date_input = page.locator("#depdate0_value")

    date_input.wait_for(state="visible", timeout=5000)

    # clear rồi nhập
    date_input.fill("")
    date_input.fill(date_text)

    # trigger change / blur cho web cổ
    #date_input.press("Tab")

    # xác nhận đã set xong
    page.wait_for_function(
        "(el,val)=>el.value===val",
        arg=[date_input.element_handle(), date_text]
    )
    print("✅ Đã nhập ngày đi")
    if date_text_dep1 :
        print(f"📅 Chọn ngày về: {date_text_dep1}")

        date_input = page.locator("#depdate1_value")

        date_input.wait_for(state="visible", timeout=5000)

        # clear rồi nhập
        date_input.fill("")
        date_input.fill(date_text_dep1)

        # trigger change / blur cho web cổ
        #date_input.press("Tab")
        print("✅ Đã nhập ngày về")
    else :
        page.click("#check_OW")
        print("✅ Đã tích OW")
def submit_search(page):
    print("🚀 Bấm tìm chuyến bay...")

    btn = page.locator("a[onclick=\"goSkdFare('L');\"]")

    btn.wait_for(state="visible", timeout=5000)

    btn.click()

    # chờ web load kết quả
    page.wait_for_load_state("networkidle")

    print("✅ Đã submit tìm chuyến")    
# =========================
# MAIN
# =========================
def run():
    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=False,
            slow_mo=500
        )

        context = browser.new_context(
            storage_state=STATE_FILE
        )

        page = context.new_page()

        # vào thẳng trang search luôn
        page.goto("https://wholesale.powercallair.com/b2bIndex.lts")

        page.wait_for_load_state("networkidle")

        print("✅ Đã login bằng state")

        # chạy tiếp luôn
        fill_route(page, "PUS", "HAN")
        fill_depart_date(page,"2026/04/19","2026/04/20")
        submit_search(page)
        # giữ browser mở để test tiếp
        input("Nhấn Enter khi muốn tắt browser...")

        browser.close()


if __name__ == "__main__":
    run()
