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
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
gs = gspread.service_account('autocheckdonserviceacc.json')
sht = gs.open_by_key('1MBtOQ4iWD-wSkn3IJKQVU-6JkGzvtPRIAINBISkKnNE')
Input = sht.worksheet('ChatBot')
Name = sht.worksheet('Ten Khach Hang')
OnOff = sht.worksheet('OnOff')
# loanInfoSheet = sht.worksheet('TES CHAT ')
print ('nhập số phút giãn cách giữa các khách : (ví dụ 5 phút nhập 5)')
phut = input()
giay = int(phut)*60
print (giay)
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
        browser.save_screenshot("chatbotsc.png")
        print("Đã chụp màn hình thành công")
        
        # Thông tin Telegram Bot của bạn
        bot_token = '5737041469:AAG5XdXVwATvldvDpXmnlQT0dmh2-sZ70gE'
        chat_id = '-4747949924'
        
        # Gửi ảnh lên Telegram
        send_telegram_image("chatbotsc.png", bot_token, chat_id,content)
    except Exception as e:
        print(f"Lỗi khi chụp và gửi ảnh: {e}")




def TestOnFB(content):
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
    a = random.randint(1,4)
    file = str(a)+'.json'
    # Tải cookie từ file đã chọn
    with open(file, "r") as f:  # Đọc dữ liệu từ file đã chọn
        cookie_data = json.load(f)  # Đọc dữ liệu từ file
        for cookie in cookie_data:
            browser.add_cookie(cookie)  # Thêm cookie vào trình duyệt
    browser.refresh()        
    print("Thông báo", "Đã đăng nhập thành công")


    
    print('Đăng nhập thành công')
    browser.get('https://www.facebook.com/messages/t/166007636835093')
    sleep(5)
    browser.switch_to.window(original_window)
    print("Test chat bot trên fb với content : "+ content)
    sleep(5)

    try:
        # Tìm và click vào phần tử <div> theo thuộc tính aria-label
        message_box = WebDriverWait(browser, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//div[@aria-label="Tin nhắn"]'))
        )
        message_box.click()  # Click vào phần tử
        # Điền nội dung vào phần tử
        if content != "No":
            message_box.send_keys("nhân viên")
            message_box.send_keys(Keys.RETURN)
            sleep(10)
            message_boxes = WebDriverWait(browser, 10).until(
                EC.presence_of_all_elements_located((By.XPATH, '//div[@aria-label="Liên hệ tư vấn viên"]'))
            )
            if message_boxes:
                message_boxes[-1].click()  # Click vào phần tử cuối cùng trong danh sách
            
            sleep(5)
            message_box.send_keys(content)  # Gửi nội dung vào phần tử
            message_box.send_keys(Keys.RETURN) 

    except Exception as e:
        print(f'Đã xảy ra lỗi khi cố gắng click vào phần tử: {e}')
    print("Chờ kết quả " + str(giay))
    sleep(int(giay))
    capture_and_send_screenshot(content)

    browser.close()
    return "đã hỏi xong"
def TestOnWeb(content,ten):
    if ten :
        str(ten)
    else :
        ten = 'Suzin'
    print(ten)
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
    print("Test chat bot trên web mobifone.vn với content : "+ content)
    browser.get('https://www.mobifone.vn/')
    sleep(5)
    webdriver.ActionChains(browser).send_keys(Keys.ESCAPE).perform()
    sleep(5)
    webdriver.ActionChains(browser).send_keys(Keys.ESCAPE).perform()
    sleep(2)
    Chatbot_box = WebDriverWait(browser, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//div[@class="social-kiem-dinh"]'))
        )
    Chatbot_box.click()
    sleep(2)
    Chatbot_box = WebDriverWait(browser, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//span[@class="message-icon"]'))
        )
    Chatbot_box.click()
    sleep(2)
    
    try:
        print("Đang chuyển sang iframe của chat popup...")
        # Đợi và chuyển sang iframe của chat popup
        chat_iframe = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.XPATH, "//iframe[contains(@id, 'iframeChat')]"))
        )
        browser.switch_to.frame(chat_iframe)
        
        Chatbot_box = WebDriverWait(browser, 10).until(
                EC.element_to_be_clickable((By.XPATH, '//input[@class="input-name"]'))
            )
        
        Chatbot_box.click()
        
        Chatbot_box.send_keys(ten)
        print('dien ten ' + ten)
        Chatbot_box.send_keys(Keys.RETURN)
        
        sleep(5)
        Chatbot_box = WebDriverWait(browser, 10).until(
                EC.element_to_be_clickable((By.XPATH, '//input[@id="txt_input_message"]'))
            )
        
        Chatbot_box.click()
        Chatbot_box.send_keys('nhân viên')
        Chatbot_box.send_keys(Keys.RETURN)
        sleep(10)
        gap_nhan_vien = WebDriverWait(browser, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Liên hệ tư vấn viên')]"))
            )
        gap_nhan_vien.click()
        sleep(10)
        Chatbot_box.send_keys(content)
        print(content)
        sleep(10)
        Chatbot_box.send_keys(Keys.RETURN)
        sleep(int(giay))
        print("Chờ kết quả " + str(giay))
        capture_and_send_screenshot(content)
        browser.close()
        return "đã hỏi xong"
    except Exception as e:
        print(f"Có lỗi xảy ra khi nhập tên: {str(e)}")
        print("HTML của trang hiện tại:", browser.page_source)
    
def get_random_name():
    try:
        namelist = Name.get_all_values()
        # Bỏ qua hàng đầu tiên nếu nó là tiêu đề
        if len(namelist) > 1:
            namelist = namelist[1:]
        # Lấy ngẫu nhiên một tên từ danh sách
        random_name = random.choice([name[0] for name in namelist if name[0].strip()])
        return random_name
    except Exception as e:
        print(f"Lỗi khi lấy tên ngẫu nhiên: {e}")
        return "Unknown"
while True:
    try :
        data = Input.get_all_values()
        
        for i, row in enumerate(data):
            sleep(10)
            question = row[0]  # Cột A
            answer = row[1]    # Cột B
            source = row[2]    # Cột C
            ten =get_random_name()
            status = OnOff.acell('A2').value
            # Kiểm tra điều kiện
            if status == 'ON':
                if question and source == "FB" and not answer:
                    # Gọi hàm TestOnFB với nội dung từ cột A
                    response = TestOnFB(question)

                    # Lưu kết quả vào ô tương ứng của cột B
                    Input.update_cell(i + 1, 2, response)
                if question and source == "WEB" and not answer:
                    # Gọi hàm TestOnFB với nội dung từ cột A
                    response = TestOnWeb(question,ten)

                    # Lưu kết quả vào ô tương ứng của cột B
                    Input.update_cell(i + 1, 2, response)
            else:
                print('status : OFF')
        sleep(int(giay))
        requests.get(
                    'https://api.telegram.org/bot5737041469:AAG5XdXVwATvldvDpXmnlQT0dmh2-sZ70gE/sendMessage?chat_id=-4747949924&text=Đã hỏi xong hết, để tiếp tục vui lòng ấn clear trên sheet OnOff')
    except:
        print ("chưa điền câu hỏi")
        sleep(int(giay))



















                #huy













   

    
    






