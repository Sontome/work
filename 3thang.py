import requests, json
import random
from time import sleep
import gspread
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# ====== GOOGLE SHEET ======
gs = gspread.service_account('cre.json')
sht = gs.open_by_key('1S0Qd-SvgWI3p17Xpd2r71_zTgTzwXqoYU8VQZKbAP2s')
SHD = sht.worksheet('Trang tính2')


# ====== API ======
def get_status_fetch_style(sohd):
    with open("los_cookies.json", "r", encoding="utf-8") as f:
        cookies_raw = json.load(f)

    cookies = {
        c["name"]: c["value"]
        for c in cookies_raw
        if "los.tima.vn" in c["domain"]
    }

    url = "https://los.tima.vn/LoanBriefV3/DataLoanbriefSearch"

    headers = {
        "accept": "application/json, text/javascript, */*; q=0.01",
        "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
        "x-requested-with": "XMLHttpRequest",
        "referer": "https://los.tima.vn/loanbrief-search/index.html",
        "user-agent": "Mozilla/5.0 Chrome/142.0.0.0 Safari/537.36",
    }

    body = (
        "datatable%5Bpagination%5D%5Bpage%5D=1"
        "&datatable%5Bpagination%5D%5Bperpage%5D=10"
        f"&datatable%5Bquery%5D%5BloanBriefId%5D={sohd}"
        "&pagination%5Bpage%5D=1"
        "&pagination%5Bperpage%5D=10"
        f"&query%5BloanBriefId%5D={sohd}"
    )

    try:
        res = requests.post(
            url,
            headers=headers,
            cookies=cookies,
            data=body,
            verify=False,
            timeout=10
        )
        data = res.json()
        if data.get("data"):
            return data["data"][0].get("status")
    except Exception as e:
        print("❌ Lỗi sohd", sohd, e)

    return None


# ====== MAIN LOOP ======
rows = SHD.get_all_values()

for idx, row in enumerate(rows[1:], start=2):  # bắt đầu từ A2
    sohd = row[0].strip() if len(row) > 0 else ""
    status_cell = row[1].strip() if len(row) > 1 else ""

    if not sohd:
        continue

    if status_cell == "":
        print(f"🔄 Đang check SHD {sohd} (row {idx})")
        status = get_status_fetch_style(sohd)

        if status:
            SHD.update_cell(idx, 2, status)  # cột B
            print(f"✅ {sohd} → {status}")
        else:
            SHD.update_cell(idx, 2, "NOT_FOUND")
            print(f"⚠️ {sohd} → NOT_FOUND")

        sleep(random.uniform(1, 1))

print("🔥 Chạy xong đơn rồi đại ca")