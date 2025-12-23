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
sht = gs.open_by_key('1KrJoO8kKZ5IYr9qJkMiXuKCHoNF-OnjNz05qYTEjrYI')
RawLOS = sht.worksheet('RawLOS')
# loanInfoSheet = sht.worksheet('Info')





idLos='spt_sontx'
passLos='Aa@554772'










opt = webdriver.ChromeOptions()
opt.add_argument("--window-size=1920,1080")
opt.add_experimental_option("excludeSwitches", ["ignore-certificate-errors"])
#opt.add_argument('headless')
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

with open("los_cookies.json", "w", encoding="utf-8") as f:
    json.dump(browser.get_cookies(), f, indent=2, ensure_ascii=False)
print("✅ Đã lưu cookies LOS dạng JSON")
print("✅ Đã lưu cookies LOS")