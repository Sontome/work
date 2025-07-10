import requests
import json
import urllib.parse
from datetime import datetime, timedelta
import gspread
import time
import subprocess  # Nhớ import nếu chưa có
from oauth2client.service_account import ServiceAccountCredentials



def connect_google_sheet(spreadsheet_id: str):
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
    client = gspread.authorize(creds)
    return client.open_by_key(spreadsheet_id)
def connect_sheet():
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
    client = gspread.authorize(creds)
    # Mở Sheet theo URL
    sheet = client.open_by_url("https://docs.google.com/spreadsheets/d/1KrJoO8kKZ5IYr9qJkMiXuKCHoNF-OnjNz05qYTEjrYI/edit?gid=1010357801")
    # Chọn sheet theo GID (ở đây là sheet có gid = 1010357801)
    worksheet = None
    for ws in sheet.worksheets():
        if str(ws.id) == "1010357801":
            worksheet = ws
            break
    return worksheet
def checkNewContracts():
    ws = connect_sheet()
    # Lấy toàn bộ giá trị cột A & B (giới hạn tới dòng 200 cho nhẹ)
    col_a = ws.col_values(1)[1:200]  # Bỏ dòng tiêu đề
    col_b = ws.col_values(2)[1:200]

    # Nếu B ngắn hơn A thì fill thêm "" để tránh IndexError
    while len(col_b) < len(col_a):
        col_b.append("")

    # So sánh từng dòng: nếu A có mà B trống thì lấy ra
    missing_data = []
    for i in range(len(col_a)):
        hd = col_a[i].strip()
        val_b = col_b[i].strip()
        if hd.isdigit() and val_b == "":
            missing_data.append(int(hd))
    print(missing_data)
    return missing_data
# 🔎 Lấy danh sách cũ A1 → A200
def getListOld():
    ws = connect_sheet()
    values = ws.col_values(1)[:200]
    # Chỉ lấy các giá trị là số
    old_list = [int(v.strip()) for v in values if v.strip().isdigit()]
    return old_list

def updateNewContracts():
    ws = connect_sheet()
    old_list = getListOld()
    new_list = getListHD()  # 🧠 Hàm của đại ca có sẵn

    new_items = [str(hd) for hd in new_list if hd not in old_list]

    if not new_items:
        print("✅ Không có hợp đồng mới cần thêm.")
        return

    print(f"🆕 Thêm {len(new_items)} hợp đồng mới vào dòng đầu.")

    # Chèn dòng trống tương ứng dưới dòng 1
    ws.insert_rows([[""]] * len(new_items), row=2)

    # Ghi hợp đồng mới vào A2, A3,...
    for i, hd in enumerate(new_items):
        ws.update_cell(2 + i, 1, hd)

    print("✅ Đã cập nhật danh sách mới.")


def getListHD( ngay_from: str = None, ngay_to: str = None) -> str:
    try:

        # Nếu không truyền ngày → mặc định today -3 đến today
        if not ngay_to:
            ngay_to = datetime.now().strftime("%d/%m/%Y")
        if not ngay_from:
            ngay_from = ngay_to

        # Encode khoảng thời gian tìm kiếm
        filter_time = f"{ngay_from} - {ngay_to}"
        filter_time_encoded = urllib.parse.quote(filter_time)

        # Load cookies từ file
        with open("tabcookies.json", "r", encoding="utf-8") as f:
            raw_cookies = json.load(f)
        cookie_jar = {cookie["name"]: cookie["value"] for cookie in raw_cookies}

        # Headers
        headers = {
            "accept": "application/json, text/javascript, */*; q=0.01",
            "accept-language": "en-US,en;q=0.9",
            "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
            "priority": "u=1, i",
            "sec-ch-ua": "\"Not)A;Brand\";v=\"8\", \"Chromium\";v=\"138\", \"Google Chrome\";v=\"138\"",
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": "\"Windows\"",
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            "x-requested-with": "XMLHttpRequest",
            "referer": "https://p2p.tima.vn/loanbrief/lender.html"
        }

        # Body post
        data = f"query%5Bsearch%5D=&query%5BtypeSearch%5D=1&query%5BcityId%5D=-1&query%5BdistrictId%5D=&query%5BproductId%5D=-1&query%5Bprice%5D=&query%5BfiltercreateTime%5D={filter_time_encoded}&pagination%5Bpage%5D=1&pagination%5Bpages%5D=1&pagination%5Bperpage%5D=100&pagination%5Btotal%5D=10"

        # Gửi request
        res = requests.post(
            "https://p2p.tima.vn/LoanBrief/LoadDataLender",
            headers=headers,
            cookies=cookie_jar,
            data=data,
            timeout=15
        )

        try:
            res_json = res.json()
        except Exception as err:
            print("❌ Không parse được JSON:")
            print("Status code:", res.status_code)
            print("Res text:", res.text[:500])  # In 500 ký tự đầu thôi cho dễ đọc
            subprocess.Popen(["python", "login.py"])
            time.sleep(20)
            raise err  # ném lại lỗi để block gọi catch bên ngoài
        data_list = res_json.get("data", [])
        listhd = []
        # Dò loanBriefId trùng với sdt
        for item in data_list:
            hd = item.get("loanBriefId")
            listhd.append(hd)

        return  listhd # Không tìm thấy

    except Exception as e:
        print("Lỗi getListHD:", e)
        return []
def getLastPhone(so_hop_dong: str, ngay_from: str = None, ngay_to: str = None) -> str:
    try:

        # Nếu không truyền ngày → mặc định today -3 đến today
        if not ngay_to:
            ngay_to = datetime.now().strftime("%d/%m/%Y")
        if not ngay_from:
            ngay_from = (datetime.now() - timedelta(days=3)).strftime("%d/%m/%Y")

        # Encode khoảng thời gian tìm kiếm
        filter_time = f"{ngay_from} - {ngay_to}"
        filter_time_encoded = urllib.parse.quote(filter_time)

        # Load cookies từ file
        with open("tabcookies.json", "r", encoding="utf-8") as f:
            raw_cookies = json.load(f)
        cookie_jar = {cookie["name"]: cookie["value"] for cookie in raw_cookies}

        # Headers
        headers = {
            "accept": "application/json, text/javascript, */*; q=0.01",
            "accept-language": "en-US,en;q=0.9",
            "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
            "priority": "u=1, i",
            "sec-ch-ua": "\"Not)A;Brand\";v=\"8\", \"Chromium\";v=\"138\", \"Google Chrome\";v=\"138\"",
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": "\"Windows\"",
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            "x-requested-with": "XMLHttpRequest",
            "referer": "https://p2p.tima.vn/loanbrief/lender.html"
        }

        # Body post
        data = f"query%5Bsearch%5D={so_hop_dong}&query%5BtypeSearch%5D=1&query%5BcityId%5D=-1&query%5BdistrictId%5D=&query%5BproductId%5D=-1&query%5Bprice%5D=&query%5BfiltercreateTime%5D={filter_time_encoded}&pagination%5Bpage%5D=1&pagination%5Bpages%5D=1&pagination%5Bperpage%5D=100&pagination%5Btotal%5D=10"

        # Gửi request
        res = requests.post(
            "https://p2p.tima.vn/LoanBrief/LoadDataLender",
            headers=headers,
            cookies=cookie_jar,
            data=data,
            timeout=15
        )

        try:
            res_json = res.json()
        except Exception as err:
            print("❌ Không parse được JSON:")
            print("Status code:", res.status_code)
            print("Res text:", res.text[:500])  # In 500 ký tự đầu thôi cho dễ đọc
            subprocess.Popen(["python", "login.py"])
            time.sleep(20)            
            raise err  # ném lại lỗi để block gọi catch bên ngoài
        data_list = res_json.get("data", [])

        # Dò loanBriefId trùng với sdt
        for item in data_list:
            if str(item.get("loanBriefId")) == str(so_hop_dong):
                phone = item.get("phone", "")
                sdt = phone[-3:] if phone else ""
                dau_so=phone[:2] if phone else ""
                return [dau_so,sdt]

        return ""  # Không tìm thấy

    except Exception as e:
        print("Lỗi getLastPhone:", e)
        return ""
def searchSDT(sdt: str, so_hop_dong: str, ngay_from: str = None, ngay_to: str = None) -> str:
    try:
        # Nếu không truyền ngày → mặc định today -3 đến today
        if not ngay_to:
            ngay_to = datetime.now().strftime("%d/%m/%Y")
        if not ngay_from:
            ngay_from = (datetime.now() - timedelta(days=3)).strftime("%d/%m/%Y")

        # Encode khoảng thời gian tìm kiếm
        filter_time = f"{ngay_from} - {ngay_to}"
        filter_time_encoded = urllib.parse.quote(filter_time)

        # Load cookies từ file
        with open("tabcookies.json", "r", encoding="utf-8") as f:
            raw_cookies = json.load(f)
        cookie_jar = {cookie["name"]: cookie["value"] for cookie in raw_cookies}

        # Headers giả browser
        headers = {
            "accept": "application/json, text/javascript, */*; q=0.01",
            "accept-language": "en-US,en;q=0.9",
            "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
            "priority": "u=1, i",
            "sec-ch-ua": "\"Not)A;Brand\";v=\"8\", \"Chromium\";v=\"138\", \"Google Chrome\";v=\"138\"",
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": "\"Windows\"",
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            "x-requested-with": "XMLHttpRequest",
            "referer": "https://p2p.tima.vn/loanbrief/lender.html"
        }

        # Build body
        data = f"query%5Bsearch%5D={sdt}&query%5BtypeSearch%5D=1&query%5BcityId%5D=-1&query%5BdistrictId%5D=&query%5BproductId%5D=-1&query%5Bprice%5D=&query%5BfiltercreateTime%5D={filter_time_encoded}&pagination%5Bpage%5D=1&pagination%5Bpages%5D=1&pagination%5Bperpage%5D=100&pagination%5Btotal%5D=10"

        # Gửi POST request
        res = requests.post(
            "https://p2p.tima.vn/LoanBrief/LoadDataLender",
            headers=headers,
            cookies=cookie_jar,
            data=data,
            timeout=15
        )

        try:
            res_json = res.json()
        except Exception as err:
            print("❌ Không parse được JSON:")
            print("Status code:", res.status_code)
            print("Res text:", res.text[:500])  # In 500 ký tự đầu thôi cho dễ đọc
            subprocess.Popen(["python", "login.py"])
            time.sleep(20)            
            raise err  # ném lại lỗi để block gọi catch bên ngoài
        data_list = res_json.get("data", [])
        for item in data_list:
            if str(item.get("loanBriefId")) == str(so_hop_dong):
                phone = item.get("phone", "")
                sdt = phone[-3:] if phone else ""
                return 1

        return ""

    except Exception as e:
        print("Lỗi cmnr:", e)
        return ""

def getinfo(so_hop_dong:str,sdt:str) -> []:
    try:

        # Nếu không truyền ngày → mặc định today -3 đến today
        
        ngay_to = datetime.now().strftime("%d/%m/%Y")
        
        ngay_from = (datetime.now() - timedelta(days=3)).strftime("%d/%m/%Y")

        # Encode khoảng thời gian tìm kiếm
        filter_time = f"{ngay_from} - {ngay_to}"
        filter_time_encoded = urllib.parse.quote(filter_time)

        # Load cookies từ file
        with open("tabcookies.json", "r", encoding="utf-8") as f:
            raw_cookies = json.load(f)
        cookie_jar = {cookie["name"]: cookie["value"] for cookie in raw_cookies}

        # Headers
        headers = {
            "accept": "application/json, text/javascript, */*; q=0.01",
            "accept-language": "en-US,en;q=0.9",
            "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
            "priority": "u=1, i",
            "sec-ch-ua": "\"Not)A;Brand\";v=\"8\", \"Chromium\";v=\"138\", \"Google Chrome\";v=\"138\"",
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": "\"Windows\"",
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            "x-requested-with": "XMLHttpRequest",
            "referer": "https://p2p.tima.vn/loanbrief/lender.html"
        }

        # Body post
        data = f"query%5Bsearch%5D={so_hop_dong}&query%5BtypeSearch%5D=1&query%5BcityId%5D=-1&query%5BdistrictId%5D=&query%5BproductId%5D=-1&query%5Bprice%5D=&query%5BfiltercreateTime%5D={filter_time_encoded}&pagination%5Bpage%5D=1&pagination%5Bpages%5D=1&pagination%5Bperpage%5D=100&pagination%5Btotal%5D=10"

        # Gửi request
        res = requests.post(
            "https://p2p.tima.vn/LoanBrief/LoadDataLender",
            headers=headers,
            cookies=cookie_jar,
            data=data,
            timeout=15
        )

        try:
            res_json = res.json()
        except Exception as err:
            print("❌ Không parse được JSON:")
            print("Status code:", res.status_code)
            print("Res text:", res.text[:500])  # In 500 ký tự đầu thôi cho dễ đọc
            subprocess.Popen(["python", "login.py"])
            time.sleep(20)            
            raise err  # ném lại lỗi để block gọi catch bên ngoài
        data_list = res_json.get("data", [])
        
        info={
            "sdt"   :sdt,
            "name"  :"",
            "huyen" :"",
            "tinh"  :"",
            "job"   :"",
            "value" :""

        }

        
        # Dò loanBriefId trùng với sdt
        for item in data_list:
            if str(item.get("loanBriefId")) == str(so_hop_dong):
                info["sdt"] = sdt
                info["name"] = item.get("fullName", "")
                info["job"] = item.get("jobName", "")
                info["tinh"] = item.get("cityName", "")
                info["huyen"] = item.get("districtName", "")
                info["value"] = item.get("loanAmount", "")
                info["value"] = str(info["value"])[:-8]+" tr"
               
                return info

        return ""  # Không tìm thấy

    except Exception as e:
        print("Lỗi getLastPhone:", e)
        return ""
    
def timkiemsdt(so_hop_dong: str) -> list:
    try:
        # Lấy 3 số cuối & 2 số đầu
        sdt_parts = getLastPhone(so_hop_dong)
        if not sdt_parts or not isinstance(sdt_parts, list) or len(sdt_parts) < 2:
            return [so_hop_dong, "Không tìm thấy"]

        dau_so = sdt_parts[0]
        result = sdt_parts[1]  # 3 số cuối

        print(f"DEBUG: Bắt đầu với đuôi: {result}")

        for loop in range(5):  # 6 vòng lặp lớn
            found = False
            for i in range(10):  # vòng lặp nhỏ từ 0 → 9
                so_thu = result + str(i)
                if searchSDT(so_thu, so_hop_dong) == 1:
                    result = so_thu
                    found = True
                    print(f"--> Match khi nối sau: {so_thu}")
                    break

            if not found:
                for i in range(10):
                    so_thu = str(i) + result
                    if searchSDT(so_thu, so_hop_dong) == 1:
                        result = so_thu
                        print(f"--> Match khi thêm trước: {so_thu}")
                        break  # không cần found = True vì không lặp tiếp
        sdt = dau_so + result

        result = getinfo(so_hop_dong,sdt)
        
        return [so_hop_dong, result]

    except Exception as e:
        print("Lỗi hàm timkiemsdt:", e)
        return [so_hop_dong, ["Không tìm thấy"]]
def pushData(hop_dong: str, info: dict):
    try:
        # Lấy tỉnh & huyện
        tinh = info.get("tinh", "").strip()
        huyen = info.get("huyen", "").strip()

        # Dòng dữ liệu cần ghi từ A → G
        row_data = [
            hop_dong,                         # Cột A: Mã HĐ
            info.get("sdt", ""),              # Cột B: SĐT
            info.get("name", ""),             # Cột C: Tên
            huyen,                            # Cột D: Huyện
            tinh,                             # Cột E: Tỉnh
            info.get("job", ""),              # Cột F: Nghề nghiệp
            info.get("value", "")             # Cột G: Số tiền
        ]

        # Kết nối Google Sheet
        sh = connect_google_sheet("1KrJoO8kKZ5IYr9qJkMiXuKCHoNF-OnjNz05qYTEjrYI")

        # Điều kiện sheet
        if tinh == "Hà Nội" and huyen in ["Ba Đình","Đống Đa","Gia Lâm","Hà Đông","Hai Bà Trưng","Hoàn Kiếm","Nam Từ Liêm","Thanh Xuân","Cầu Giấy","Tây Hồ", "Hoàng Mai", "Bắc Từ Liêm", "Long Biên"]:
            ws = sh.get_worksheet_by_id(332142631)  # Sheet HN
            sheet_name = "HN"
        else:
            ws = sh.get_worksheet_by_id(1743801391)  # Sheet Khác
            sheet_name = "Khác"

        # Chèn dòng trống tại dòng 2
        ws.insert_rows([[""]], row=1)

        # Ghi dữ liệu từ A2:G2
        ws.update(values=[row_data], range_name="A2:G2")
        print(f"✅ Ghi vào sheet [{sheet_name}]: {row_data}")

    except Exception as e:
        print(f"💥 Lỗi pushData: {e}")

def loop():
    ws = connect_sheet()
    list_can_check = checkNewContracts()
    col_a = ws.col_values(1)[1:200]  # Bỏ dòng đầu tiêu đề

    for hd in list_can_check:
        try:
            # Gọi hàm lấy thông tin
            result = timkiemsdt(str(hd))
            if not result or not isinstance(result, list):
                print(f"❌ Không lấy được data hợp đồng {hd}")
                continue

            hd_str, info = result
            if not isinstance(info, dict):
                print(f"❌ Sai định dạng trả về của {hd}: {info}")
                continue

            # Tìm đúng dòng chứa hợp đồng
            if str(hd) in col_a:
                row_index = col_a.index(str(hd)) + 2  # +2 vì col_a đã bỏ dòng 1

                # Chuẩn bị dữ liệu ghi vào các cột B→G
                row_data = [
                    info.get("sdt", ""),
                    info.get("name", ""),
                    info.get("huyen", ""),
                    info.get("tinh", ""),
                    info.get("job", ""),
                    info.get("value", "")
                ]

                # Ghi dữ liệu vào B→G
                ws.update(values=[row_data], range_name=f'B{row_index}:G{row_index}')
                pushData(str(hd), info)
                print(f"✅ Ghi xong hợp đồng {hd}")

            else:
                print(f"⚠️ Không tìm thấy dòng chứa hợp đồng {hd}")

        except Exception as e:
            print(f"💥 Lỗi khi xử lý {hd}: {e}")   



print("start")
while True:
    try:
        time.sleep(17)
        updateNewContracts()
        time.sleep(3)
        loop()
    except:
        time.sleep(20)
        pass


