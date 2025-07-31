import requests, json
import re
import random
from time import sleep
import gspread
import urllib3

from datetime import datetime
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


gs = gspread.service_account('autocheckdonserviceacc.json')
sht = gs.open_by_key('1KrJoO8kKZ5IYr9qJkMiXuKCHoNF-OnjNz05qYTEjrYI')
RawLOS = sht.worksheet('RawLOS')





def getSDT(sohd):
    # Load cookies từ file
    with open("los_cookies.json", "r", encoding="utf-8") as f:
        cookies_raw = json.load(f)

    # Chuyển sang dict cho requests
    cookies = {c["name"]: c["value"] for c in cookies_raw if ".los.tima.vn" in c["domain"] or "los.tima.vn" in c["domain"]}

    # Gửi request tới API Detail
    try:
        res = requests.get(
            f"https://los.tima.vn/LoanBriefV3/Detail?id={str(sohd)}",
            headers={
                "x-requested-with": "XMLHttpRequest",
                "referer": "https://los.tima.vn/loanbrief-search/index.html",
                "user-agent": "Mozilla/5.0 Chrome/138.0.0.0 Safari/537.36",
                "accept": "*/*"
            },
            cookies=cookies,
            verify=False,
            timeout=10
        )
    except Exception as e:
        print("❌ Lỗi khi gửi request:", e)
        return None

    # Decode unicode escape
    try:
        decoded = res.text.encode().decode('unicode_escape')
        match = re.search(r"pbx\.C2c\('(\d{10})'", decoded)
        if match:
            return str(match.group(1))
        else:
            print("❌ Không tìm thấy SĐT trong hồ sơ")
            return None
    except Exception as e:
        print("❌ Lỗi khi xử lý response:", e)
        return None
    
def getThongTinHoSo(sohd):
    # Load cookies từ file
    with open("los_cookies.json", "r", encoding="utf-8") as f:
        cookies_raw = json.load(f)

    cookies = {c["name"]: c["value"] for c in cookies_raw if ".los.tima.vn" in c["domain"] or "los.tima.vn" in c["domain"]}

    # Body của POST request, định dạng form-urlencoded
    body = f"datatable%5Bpagination%5D%5Bpage%5D=1&datatable%5Bpagination%5D%5Bperpage%5D=10&datatable%5Bquery%5D%5BloanBriefId%5D={str(sohd)}&datatable%5Bquery%5D%5Bsearch%5D=&datatable%5Bquery%5D%5BcodeId%5D=&datatable%5Bquery%5D%5Bcif%5D=&datatable%5Bquery%5D%5BcimbLoanId%5D=&pagination%5Bpage%5D=1&pagination%5Bperpage%5D=10&query%5BloanBriefId%5D={str(sohd)}&query%5Bsearch%5D=&query%5BcodeId%5D=&query%5Bcif%5D=&query%5BcimbLoanId%5D="
    sdt = getSDT(str(sohd))
    try:
        res = requests.post(
            "https://los.tima.vn/LoanBriefV3/DataLoanbriefSearch",
            headers={
                "accept": "application/json, text/javascript, */*; q=0.01",
                "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
                "x-requested-with": "XMLHttpRequest",
                "referer": "https://los.tima.vn/loanbrief-search/index.html",
                "user-agent": "Mozilla/5.0 Chrome/138.0.0.0 Safari/537.36"
            },
            cookies=cookies,
            data=body,
            verify=False,
            timeout=10
        )

        data = res.json()
        if data["data"]:
            item = data["data"][0]
            
            created_fmt = ""
            raw_time = item.get("createdTime")
            if raw_time:
                try:
                    dt = datetime.fromisoformat(raw_time.replace("Z", "+00:00"))
                    created_fmt = dt.strftime("%d/%m/%Y")
                except:
                    created_fmt = raw_time
            info = {
                "fullName": item.get("fullName"),
                "sdt" : sdt,
                "provinceName": item.get("provinceName"),
                "districtName": item.get("districtName"),
                "createdTime": created_fmt,
                "loanProductName": item.get("loanProductName"),
                "utmSource": item.get("utmSource"),
                "status": item.get("status")
            }
            return info
        else:
            print("❌ Không tìm thấy hồ sơ")
            return None

    except Exception as e:
        print("❌ Lỗi khi gọi API hoặc xử lý response:", e)
        return None
    

Loan1st = int(RawLOS.acell('A1').value)
i= 0
r = 0
LoanOld=Loan1st
while True:
    try:
        a =random.uniform(2,4)
        sleep(a)
        if LoanOld == Loan1st:
            r = 0
            Loan1st = LoanOld+1
        else :
            r = r+1
            Loan1st = Loan1st+1
        if r > 20 :
            break
        result = getThongTinHoSo(Loan1st)
        Loaninfo = [Loan1st,result["sdt"],result["fullName"],result["districtName"],result["provinceName"],result["createdTime"],result["loanProductName"],result["status"],result["utmSource"]]
        print(Loaninfo)
        LoanOld =Loan1st
        RawLOS.insert_row(Loaninfo,1,1)


    except:
        sleep(a)

print('chay xong don')
input('press any key')