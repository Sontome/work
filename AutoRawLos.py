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
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
gs = gspread.service_account('autocheckdonserviceacc.json')
sht = gs.open_by_key('1KrJoO8kKZ5IYr9qJkMiXuKCHoNF-OnjNz05qYTEjrYI')
RawLOS = sht.worksheet('RawLOS')
# loanInfoSheet = sht.worksheet('Info')





idLos='spt_sontx'
passLos='Aa@554772'










opt = webdriver.ChromeOptions()
opt.add_argument("--window-size=1920,1080")
opt.add_experimental_option("excludeSwitches", ["ignore-certificate-errors"])
opt.add_argument('headless')
browser = webdriver.Chrome(options=opt)

browser.get('https://sso.tima.vn/')
original_window = browser.current_window_handle
sleep(3)
browser.find_element(By.ID, 'Username').send_keys(idLos)
browser.find_element(By.ID, 'Password').send_keys(passLos)
browser.find_element(By.ID, 'Password').send_keys(Keys.ENTER)
sleep(2)
browser.find_element(By.XPATH, '/html/body/div[1]/div/div[3]/div/div/a[1]').click()

sleep(1)
try:
    browser.find_element(By.ID, 'Otp').click()
    otp = input('Nhập OTP mail vào LOS:')
    browser.find_element(By.ID, 'Otp').send_keys(otp)
    browser.find_element(By.XPATH,'//*[@id="modal_otp"]/div/div/form/div[2]/button[2]').click()
except:
    pass
sleep(3)
print('Đăng nhập thành công')

browser.switch_to.window(original_window)
sleep(2)
browser.get('https://los.tima.vn/loanbrief-search/index.html')
sleep(2)
Loan1st = int(RawLOS.acell('A1').value)
i= 0
r = 0
LoanOld=Loan1st
while True:
    try:
        if LoanOld == Loan1st:
            r = 0
            Loan1st = LoanOld+1
        else :
            r = r+1
            Loan1st = Loan1st+1
        if r > 20 :
            break
        browser.get('https://los.tima.vn/loanbrief-search/index.html')
          
        a =random.uniform(1,2)
        sleep(a)
        
        browser.find_element(By.XPATH, '//*[@id="filterLoanId"]').clear()
        browser.find_element(By.XPATH, '//*[@id="filterLoanId"]').send_keys(Loan1st)

        browser.find_element(By.XPATH,'//*[@id="filterLoanId"]').send_keys(Keys.ENTER)
        sleep(a)
        name = browser.find_element(By.CLASS_NAME,'fullname').text
        date = browser.find_element(By.CLASS_NAME, 'date').text
        try:
            source = browser.find_element(By.XPATH, '//*[@id="dtLoanSeach"]/tbody/tr/td[2]/div/p').text
        except:
            source = 'null'
        try:
            district = browser.find_element(By.CLASS_NAME, 'district').text
        except:
            district = 'null'
        try:
            province = browser.find_element(By.CLASS_NAME, 'province').text
        except:
            province = 'null'
        try:
            browser.find_element(By.CLASS_NAME,'fullname').click()
            sleep(a)
            # Chờ phần tử có mặt trước khi cố gắng tìm nó
            elementsdt =browser.find_element(By.XPATH, '//a[contains(@onclick, "pbx.C2c")]')
            onclick_value = elementsdt.get_attribute('onclick')
            
            # Sử dụng biểu thức chính quy để tìm số điện thoại
            match = re.search(r"'(\d+)'", onclick_value)
            if match:
                sdt = match.group(1)
            else:
                print('Không tìm thấy số điện thoại.')
        except Exception as e:  # Bắt các ngoại lệ cụ thể
            print(f'Đã xảy ra lỗi: {e}')  # Ghi lại thông báo lỗi
            sdt = 'null'
        desciption = browser.find_element(By.CLASS_NAME, 'item-desciption').text
        status = browser.find_element(By.XPATH,'//*[@id="dtLoanSeach"]/tbody/tr/td[7]/div/span/span').text

        Loaninfo = [Loan1st,sdt,name,district,province,date,desciption,status,source]
        print(Loaninfo)
        LoanOld =Loan1st
        RawLOS.insert_row(Loaninfo,1,1)
    except:
        sleep(a)


print('chay xong don')
input('press any key')
browser.close()




















                #huy













   

    
    






