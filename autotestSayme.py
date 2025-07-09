import random
from time import sleep
import gspread
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import pandas as pd
from selenium.webdriver.support.ui import Select
import re
import json
from datetime import datetime
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
gs = gspread.service_account('autocheckdonserviceacc.json')
sht = gs.open_by_key('1MBtOQ4iWD-wSkn3IJKQVU-6JkGzvtPRIAINBISkKnNE')
Input = sht.worksheet('Sayme')
# loanInfoSheet = sht.worksheet('Info')
OnOff = sht.worksheet('OnOff')

global browser



       










opt = webdriver.ChromeOptions()
opt.add_argument("--window-size=1920,1080")
opt.add_experimental_option("excludeSwitches", ["ignore-certificate-errors"])
prefs = {
    "profile.default_content_setting_values.notifications": 1  # 1 để cho phép, 2 để chặn
}
opt.add_experimental_option("prefs", prefs)
opt.add_argument('headless')
browser = webdriver.Chrome(options=opt)

browser.get("https://facebook.com")  # Truy cập vào Facebook
original_window = browser.current_window_handle
sleep(3)
WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.ID, "pass")))
sleep(1)  # Chờ cho đến khi trường email xuất hiện

# Tải cookie từ file đã chọn
with open("1.json", "r") as f:  # Đọc dữ liệu từ file đã chọn
    cookie_data = json.load(f)  # Đọc dữ liệu từ file
    for cookie in cookie_data:
        browser.add_cookie(cookie)  # Thêm cookie vào trình duyệt
browser.refresh()        
print("Thông báo", "Đã đăng nhập thành công")



print('Đăng nhập thành công')
browser.get('https://www.facebook.com/messages/t/103529715943028')
sleep(5)
browser.switch_to.window(original_window)

def send_telegram_image(image_path, bot_token, chat_id, content):
    try:
        url = f"https://api.telegram.org/bot{bot_token}/sendPhoto"
        with open(image_path, 'rb') as photo:
            files = {'photo': ('screenshot.png', photo, 'image/png')}  # Thêm thông tin về file
            data = {
                'chat_id': str(chat_id),
                'caption': content  # Thêm caption cho ảnh
            }  
            response = requests.post(url, files=files, data=data)
        if response.status_code == 200:
            print("Đã gửi ảnh lên Telegram thành công")
        else:
            print(f"Lỗi khi gửi ảnh: {response.status_code}")
            print(f"Response: {response.text}")  # In ra thông tin lỗi chi tiết
    except Exception as e:
        print(f"Lỗi khi gửi ảnh lên Telegram: {e}")

def capture_and_send_screenshot(content):
    try:
        global browser
        # Chụp màn hình
        browser.save_screenshot("saymesc.png")
        print("Đã chụp màn hình thành công")
        
        # Thông tin Telegram Bot của bạn
        bot_token = '5737041469:AAG5XdXVwATvldvDpXmnlQT0dmh2-sZ70gE'
        chat_id = '-4720627885'
        
        # Gửi ảnh lên Telegram
        send_telegram_image("saymesc.png", bot_token, chat_id,content)
    except Exception as e:
        print(f"Lỗi khi chụp và gửi ảnh: {e}")

def TestOnFB(content):
    global browser
    print("Test bot Sayme with content : "+ content)
    browser.get('https://www.facebook.com/messages/t/103529715943028')
    try:
        # Tìm và click vào phần tử <div> theo thuộc tính aria-label
        message_box = WebDriverWait(browser, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//div[@aria-label="Tin nhắn"]'))
        )
        message_box.click()  # Click vào phần tử
        # Điền nội dung vào phần tử
        if content != "No":
            message_box.send_keys(content)  # Gửi nội dung vào phần tử
            message_box.send_keys(Keys.RETURN) 

    except Exception as e:
        print(f'Đã xảy ra lỗi khi cố gắng click vào phần tử: {e}')
    print("Chờ kết quả 30s ...")
    sleep(30)
    #capture_and_send_screenshot(content)
    all_text = browser.find_element(By.TAG_NAME, "body").text
    last_index = all_text.rfind("Umee AI from Saymee")
    last_index2 = all_text.rfind("- 𝑈𝑚𝑒𝑒 𝐴𝐼 -")
    if last_index != -1:
        # Cắt văn bản từ vị trí cuối cùng đến hết
        all_text = all_text[last_index:last_index2]

    # Sử dụng biểu thức chính quy để tìm câu cần thiết
    matches = all_text

    if matches:
        # Lấy câu trả lời từ đoạn cuối cùng
        remove_text = "Umee AI from Saymee"
        remove_text2 = "Tớ là Umee AI trợ lý của Saymee. Cậu cần tớ giúp gì hôm nay? (Tớ là AI nên thông tin chỉ mang tính tham khảo cậu nhé)"
        remove_text3 = "đã gửi,"
        # Loại bỏ câu
        cleaned_text = matches.replace(remove_text, "").strip()
        cleaned_text = cleaned_text.replace(remove_text2, "").strip()
        cleaned_text = cleaned_text.replace(remove_text3, "").strip()
        cleaned_text = "\n".join(line for line in cleaned_text.splitlines() if line.strip())
        response = cleaned_text
        
        
        # Loại bỏ chuỗi "-𝑈𝑚𝑒𝑒 𝐴𝐼-" và "Umee AI" nếu có
        response = response.replace("-𝑈𝑚𝑒𝑒 𝐴𝐼-", "").strip()
        response = response.replace("Umee AI", "").strip()
        try:
            vi_tri = response.find("2022 - Bản quyền thuộc về Tổng công ty Viễn thông MobiFone")

            # Cắt từ sau đoạn đó
            
            response = response[vi_tri + len("2022 - Bản quyền thuộc về Tổng công ty Viễn thông MobiFone"):].strip()
        except:
            pass
        print("Câu Trả lời bot : "+response)
        
        return response
    else:
        print("Không tìm thấy câu trả lời.")
        response = "Null"
        return response
def TestOnWeb(content):
    global browser
    print("Test bot Sayme with content : "+ content)
    browser.get('https://saymee.vn/')
    Chatbot_box = WebDriverWait(browser, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//div[@class="chatbot"]'))
        )
    Chatbot_box.click()
    
    
     

    try:
        # Tìm và click vào phần tử <div> theo thuộc tính aria-label
        
        try:
            Chatlun = WebDriverWait(browser, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Chat lun!')]"))
            )
            Chatlun.click()
            
        except:
            pass
        # Điền nội dung vào phần tử
        message_box = WebDriverWait(browser, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//textarea[@class="chatbot_chatting_input_text"]'))
        )
        message_box.click()
        if content != "No":
            message_box.send_keys(content)  # Gửi nội dung vào phần tử
            message_box.send_keys(Keys.RETURN) 

    except Exception as e:
        print(f'Đã xảy ra lỗi khi cố gắng click vào phần tử: {e}')
    print("Chờ kết quả 30s ...")
    sleep(30)
    #capture_and_send_screenshot(content)

    all_text = browser.find_element(By.TAG_NAME, "body").text
    # print (all_text)
    
    last_index = all_text.rfind(content)
    if last_index != -1:
        # Cắt văn bản từ vị trí cuối cùng đến hết
        all_text = all_text[last_index:]

    # Sử dụng biểu thức chính quy để tìm câu cần thiết
    
    matches = all_text

    if matches:
        # Lấy câu trả lời từ đoạn cuối cùng
        remove_text = "Tớ là Umee AI trợ lý của Saymee. Cậu cần tớ giúp gì hôm nay? (Tớ là AI nên thông tin chỉ mang tính tham khảo cậu nhé)"

        # Loại bỏ câu
        cleaned_text = matches.replace(remove_text, "").strip()
        cleaned_text = cleaned_text.replace(content, "").strip()
        cleaned_text = "\n".join(line for line in cleaned_text.splitlines() if line.strip())
        response = cleaned_text
        response = response.replace("-𝑈𝑚𝑒𝑒 𝐴𝐼-", "").strip()
        response = response.replace("Umee AI", "").strip()
        try:
            vi_tri = response.find("2022 - Bản quyền thuộc về Tổng công ty Viễn thông MobiFone")

            # Cắt từ sau đoạn đó
            response = response[vi_tri + len("2022 - Bản quyền thuộc về Tổng công ty Viễn thông MobiFone"):].strip()
        except:
            pass
        print("Câu Trả lời bot : "+response)
        return response
    else:
        print("Không tìm thấy câu trả lời.")
        response = "Null"
        return response
while True:
    try :
        data = Input.get_all_values()
        sleep(20)
        for i, row in enumerate(data):
            sleep(20)
            question = row[0]  # Cột A
            answer = row[1]    # Cột B
            source = row[2]    # Cột C
            status = OnOff.acell('A9').value
            # Kiểm tra điều kiện
            if status == 'ON':
                if question and source == "Facebook" and not answer:
                    # Gọi hàm TestOnFB với nội dung từ cột A
                    response = TestOnFB(question)

                    # Lưu kết quả vào ô tương ứng của cột B
                    Input.update_cell(i + 1, 2, response)
                if question and source == "Web" and not answer:
                    # Gọi hàm TestOnFB với nội dung từ cột A
                    response = TestOnWeb(question)

                    # Lưu kết quả vào ô tương ứng của cột B
                    Input.update_cell(i + 1, 2, response)
            else:
                print('status :OFF')
        
        requests.get(
                    'https://api.telegram.org/bot5737041469:AAG5XdXVwATvldvDpXmnlQT0dmh2-sZ70gE/sendMessage?chat_id=-4720627885&text=Đã hỏi xong hết, để tiếp tục vui lòng ấn clear trên sheet OnOff')
    except:
        print ("chưa điền câu hỏi")
        sleep(20)



















                #huy













   

    
    






