import requests, json
import random
from time import sleep
import gspread
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# ====== GOOGLE SHEET ======
gs = gspread.service_account('cre.json')
sht = gs.open_by_key('1x8_hB0liRywpaj2HIixg8bmaGPanTaIN1a99VoyoG4w')
SHD = sht.worksheet('Trang tính2')

def checkCIF(sohd):
    import requests, json, re

    # load cookies
    with open("los_cookies.json", "r", encoding="utf-8") as f:
        cookies_raw = json.load(f)

    cookies = {
        c["name"]: c["value"]
        for c in cookies_raw
        if "los.tima.vn" in c["domain"]
    }

    url = f"https://los.tima.vn/LoanBriefV3/Detail?id={sohd}"

    headers = {
        "accept": "*/*",
        "accept-language": "vi-VN,vi;q=0.9,en-US;q=0.8,en;q=0.7",
        "x-requested-with": "XMLHttpRequest",
        "sec-ch-ua": "\"Chromium\";v=\"142\", \"Google Chrome\";v=\"142\", \"Not_A Brand\";v=\"99\"",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "\"Windows\"",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "referer": "https://los.tima.vn/loanbrief-search/index.html",
        "user-agent": "Mozilla/5.0 Chrome/142.0.0.0 Safari/537.36",
    }

    try:
        res = requests.get(
            url,
            headers=headers,
            cookies=cookies,
            verify=False,
            timeout=10
        )

        data = res.json()
        html = data.get("html", "")

        # regex tìm CIF
        match = re.search(r"CIF:\s*<span[^>]*>(\d+)</span>", html)
        if match:
            return match.group(1)

    except Exception as e:
        print("❌ Lỗi checkCIF", sohd, e)

    return None
# ====== API ======
def get_status_by_codeid_exact(code_id):
    import requests, json

    # load cookies
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
        "accept-language": "vi-VN,vi;q=0.9,en-US;q=0.8,en;q=0.7",
        "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
        "sec-ch-ua": "\"Chromium\";v=\"142\", \"Google Chrome\";v=\"142\", \"Not_A Brand\";v=\"99\"",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "\"Windows\"",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "x-requested-with": "XMLHttpRequest",
        "referer": "https://los.tima.vn/loanbrief-search/index.html",
        "user-agent": "Mozilla/5.0 Chrome/142.0.0.0 Safari/537.36",
    }

    body = (
        "datatable%5Bpagination%5D%5Bpage%5D=1"
        "&datatable%5Bpagination%5D%5Bpages%5D=1"
        "&datatable%5Bpagination%5D%5Bperpage%5D=10"
        "&datatable%5Bpagination%5D%5Btotal%5D=1"
        "&datatable%5Bquery%5D%5BloanBriefId%5D="
        "&datatable%5Bquery%5D%5Bsearch%5D="
        f"&datatable%5Bquery%5D%5BcodeId%5D={code_id}"
        "&datatable%5Bquery%5D%5Bcif%5D="
        "&datatable%5Bquery%5D%5BcimbLoanId%5D="
        "&pagination%5Bpage%5D=1"
        "&pagination%5Bpages%5D=1"
        "&pagination%5Bperpage%5D=10"
        "&pagination%5Btotal%5D=1"
        "&query%5BloanBriefId%5D="
        "&query%5Bsearch%5D="
        f"&query%5BcodeId%5D={code_id}"
        "&query%5Bcif%5D="
        "&query%5BcimbLoanId%5D="
    )

    res = requests.post(
        url,
        headers=headers,
        cookies=cookies,
        data=body,
        verify=False,
        timeout=10
    )

    data = res.json()

    if data.get("data") and len(data["data"]) > 0:
        return data["data"][0]["loanBriefId"]

    return None


# ====== MAIN LOOP ======

shd = get_status_by_codeid_exact(132798)
cif = checkCIF(shd)
print(shd)
if cif:
   
    print(f"✅ {shd} → {cif}")
else:
    
    print(f"⚠️ {shd} → NOT_FOUND")

sleep(random.uniform(1, 1))

