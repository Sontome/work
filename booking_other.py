
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

    korea_airport_codes = {
        "ICN", "PUS", "GMP", "CJU", "CJJ", "TAE", "KWJ",
        "MWX", "RSU", "USN", "KPO", "YNY", "WJU", "HIN"
    }

    # Nếu nơi đi không thuộc Hàn Quốc, chuyển qua chế độ overseas.
    if from_code not in korea_airport_codes:
        page.check("#areasoto")

        # nơi đi chọn bằng popup city picker
        select_destination_city(
            page,
            from_code,
            trigger_selector="#dep0_text",
            value_selector="#dep0"
        )

        # nơi đến chọn bằng select thường
        page.select_option("#arr0", value=to_code)
    else:
        # nơi đi
        page.select_option("#dep0", value=from_code)

        # nơi đến
        select_destination_city(page, to_code)

    print("✅ Hoàn tất route")

def select_destination_city(page, city_code, trigger_selector="#arr0_text", value_selector="#arr0"):
    print(f"🎯 Chọn điểm: {city_code}")

    page.click(trigger_selector)

    popup_input = page.locator("#strAirCity")
    popup_input.wait_for(state="visible", timeout=5000)

    popup_input.fill("")
    popup_input.fill(city_code)

    page.wait_for_timeout(300)
    popup_input.press("Enter")

    # selector chuẩn: airport code đầu tiên phải là HAN
    result = page.locator(
        f"a[onclick^=\"setAirCity('{city_code}'\"]"
    ).first

    result.wait_for(state="visible", timeout=5000)
    result.click()

    page.wait_for_function(
        f"document.querySelector('{value_selector}').value === '{city_code}'"
    )

    print("✅ Đã chọn điểm")
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
def fill_passenger_count(page, adt, chd, inf):
    print(f"👥 Chọn số khách - ADT:{adt}, CHD:{chd}, INF:{inf}")

    page.select_option("#adt_value", value=str(adt))
    page.select_option("#chd_value", value=str(chd))
    page.select_option("#inf_value", value=str(inf))

    page.wait_for_function(
        """([adt, chd, inf]) => {
            return document.querySelector('#adt_value')?.value === adt
                && document.querySelector('#chd_value')?.value === chd
                && document.querySelector('#inf_value')?.value === inf;
        }""",
        arg=[str(adt), str(chd), str(inf)]
    )
    print("✅ Đã chọn số khách")
def submit_search(page):
    print("🚀 Bấm tìm chuyến bay...")

    btn = page.locator("a[onclick=\"goSkdFare('L');\"]")

    btn.wait_for(state="visible", timeout=5000)

    btn.click()

    # chờ web load kết quả
    

    print("✅ Đã submit tìm chuyến") 
    wait_loading_finish(page)  
def wait_loading_finish(page):
    print("⏳ Chờ loading xong...")

    # đợi network trước
    page.wait_for_load_state("networkidle")

    # đợi mấy popup/banner/loading hay gặp biến mất
    selectors = [
        ".loading",
        ".layerPop",
        ".banner",
        ".dimmed",
        ".overlay",
        ".ui-widget-overlay"
    ]

    for css in selectors:
        try:
            page.locator(css).wait_for(state="hidden", timeout=2000)
        except:
            pass

    print("✅ Hết loading")

def select_airline(page, airline_code="KE"):
    print(f"✈️ Chọn hãng bay: {airline_code}")
    #wait_loading_finish(page)
    # mở tab filter hãng bay
    filter_box = page.locator("#carFilter")
    filter_box.wait_for(state="visible", timeout=5000)
    filter_box.click()

    # đợi checkbox hãng hiện ra
    checkbox = page.locator(
        f'#carFilter input[type="checkbox"][value="{airline_code}"]'
    )

    checkbox.wait_for(state="visible", timeout=5000)

    # nếu chưa tick thì tick
    if not checkbox.is_checked():
        checkbox.check(force=True)
    page.wait_for_load_state("networkidle")
    print("✅ Đã chọn hãng bay") 
def select_fare(page, fare_id:str):
    wait_loading_finish(page) 
    print(f"🎯 Chọn fare ID: {fare_id}")

    page.evaluate(f"faresSelect('{fare_id}')")

    page.wait_for_load_state("networkidle")

    print("✅ Đã chọn fare")
def reserve_selected_fare(page, fareindex: str,adt=1,chd=0,inf=0):
    wait_loading_finish(page)

    print(f"🛒 Tiến hành đặt chỗ fare index: {fareindex}")

    # đợi function tồn tại
    page.wait_for_function(
        "typeof reserveFare === 'function'"
    )

    # đợi nút reserve xuất hiện
    reserve_btn = page.locator('a[href^="javascript:reserveFare"]')
    reserve_btn.first.wait_for(state="visible", timeout=10000)

    # nghỉ nhẹ cho DOM ổn định
    page.wait_for_timeout(500)

    # chạy script
    current_url = page.url
    page.evaluate(
        """
        ({idx, adt, chd, inf}) => {
            reserveFare(idx, '0', 9, adt, chd, inf, '', '');
        }
        """,
        {
            "idx": fareindex,
            "adt": adt,
            "chd": chd,
            "inf": inf
        }
    )

    # reserveFare xử lý async, cần đợi điều hướng thật sự diễn ra.
    try:
        page.wait_for_function(
            "(oldUrl) => window.location.href !== oldUrl",
            arg=current_url,
            timeout=20000
        )
        page.wait_for_load_state("domcontentloaded")
        page.wait_for_load_state("networkidle")
    except TimeoutError:
        # Fallback: có thể web không đổi URL nhưng form khách đã render.
        page.locator("#paxLastNameEn1").wait_for(state="visible", timeout=15000)

    wait_loading_finish(page) 
    print("✅ Đã chạy reserveFare")
def fill_customer(page, customers):
    """
    customers: list[dict]
    Mỗi khách gồm: type, gender, firstname, lastname
    Ví dụ:
    [
        {"type": "ADT", "gender": "M", "firstname": "AN", "lastname": "NGUYEN"},
        {"type": "CHD", "gender": "F", "firstname": "BINH", "lastname": "TRAN"}
    ]
    """
    print(f"🧾 Bắt đầu điền thông tin {len(customers)} khách")

    for idx, customer in enumerate(customers, start=1):
        raw_gender = str(customer.get("gender", "NAM")).strip().upper()
        gender_map = {
            "NAM": "M",
            "MALE": "M",
            "M": "M",
            "NU": "F",
            "NỮ": "F",
            "FEMALE": "F",
            "F": "F"
        }
        gender = gender_map.get(raw_gender, "M")

        first_name = str(customer.get("firstname", "")).strip().upper()
        last_name = str(customer.get("lastname", "")).strip().upper()
        pax_type = str(customer.get("type", "")).strip().upper()

        print(
            f"👤 Khách {idx} - TYPE:{pax_type or 'N/A'}, "
            f"GENDER:{gender}, LAST:{last_name}, FIRST:{first_name}"
        )

        gender_selector = f"#paxGenderRadio{gender}{idx}"
        last_name_selector = f"#paxLastNameEn{idx}"
        first_name_selector = f"#paxFirstNameEn{idx}"
        hidden_gender_selector = f"#paxGender{idx}"

        page.locator(gender_selector).wait_for(state="visible", timeout=10000)
        page.evaluate("""
            (selector) => {
                const el = document.querySelector(selector);
                if (el) el.click();
            }
            """, gender_selector)

        # page.wait_for_function(
        #     "(selector, val) => document.querySelector(selector)?.value === val",
        #     arg=[hidden_gender_selector, gender]
        # )
        print("đã tích chọn gender")
        page.click(last_name_selector)
        # page.keyboard.press("Control+A")
        # page.keyboard.press("Backspace")
        page.type(last_name_selector, last_name, delay=1)

        page.click(first_name_selector)
        # page.keyboard.press("Control+A")
        # page.keyboard.press("Backspace")
        page.type(first_name_selector, first_name, delay=1)

    print("✅ Đã điền xong thông tin khách")
def fill_phone(page, phone="010-2451-1790"):
    print(f"📞 Điền số điện thoại: {phone}")

    parts = str(phone).strip().split("-")
    if len(parts) != 3:
        parts = ["010", "2451", "1790"]

    mid = parts[1]
    last = parts[2]

    page.locator('input[name="revMobile02"]').wait_for(state="visible", timeout=10000)
    page.fill('input[name="revMobile02"]', "")
    page.fill('input[name="revMobile02"]', mid)

    page.locator('input[name="revMobile03"]').wait_for(state="visible", timeout=10000)
    page.fill('input[name="revMobile03"]', "")
    page.fill('input[name="revMobile03"]', last)

    for checkbox_id in ("#ruleAgree1", "#ruleAgree2", "#ruleAgree3"):
        checkbox = page.locator(checkbox_id)
        checkbox.wait_for(state="visible", timeout=10000)
        if not checkbox.is_checked():
            checkbox.check(force=True)

    print("✅ Đã điền phone và tick 3 điều khoản")
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
        fill_route(page, "HAN", "ICN")
        fill_passenger_count(page, adt=2, chd=1, inf=1)
        fill_depart_date(page,"2026/06/18","2026/06/20")
        submit_search(page)
        select_airline(page=page,airline_code="KE")
        #input("enter")
        select_fare(page=page,fare_id="8")
        #input("enter")
        reserve_selected_fare(page=page,fareindex="8",adt=2,chd=1,inf=1)
        # Ví dụ gọi hàm điền khách sau khi màn hình passenger đã hiển thị:
        fill_customer(page, [
            {"type": "ADT", "gender": "NAM", "firstname": "VAN A", "lastname": "NGUYEN"},
            {"type": "ADT", "gender": "NAM", "firstname": "THI B", "lastname": "TRAN"},
            {"type": "CHD", "gender": "NAM", "firstname": "BE C", "lastname": "LE"},
            {"type": "INF", "gender": "NU", "firstname": "BABY D", "lastname": "PHAM"}
        ])
        fill_phone(page)
        # giữ browser mở để test tiếp
        input("Nhấn Enter khi muốn tắt browser...")

        browser.close()


if __name__ == "__main__":
    run()