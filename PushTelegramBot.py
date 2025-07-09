import cv2
import pyperclip
import time
import pywinauto
import pyautogui
import requests

import pandas as pd
# pyautogui.useImageNotFoundException()
from pywinauto import application
from pywinauto import Desktop
# Get the PID of your running process (replace 'yourExeName' with the actual executable name)
from pywinauto.keyboard import send_keys
import gspread
import requests

# Use the PID to connect
gs = gspread.service_account('sontome-de382811160d.json')
sht = gs.open_by_key('1KrJoO8kKZ5IYr9qJkMiXuKCHoNF-OnjNz05qYTEjrYI')
rawhn = sht.worksheet('RawHN')



while True:
    try:
        getloan = rawhn.acell('A1').value

        print('ket noi thanh cong den ggsheet')
        time.sleep(40)
        if getloan == None:

            print('chưa có đơn cần push')
        else :
            getloan = rawhn.row_values(1)

            urlgoc = 'https://api.telegram.org/bot5737041469:AAG5XdXVwATvldvDpXmnlQT0dmh2-sZ70gE/sendMessage?chat_id=-775255924&text=   '


            url = urlgoc + \
                   str('HD ') + '\t\t SĐT : ' + str(getloan[1]) + '\t\t Tên :' + str(getloan[2]) + '\t\t , ' + str(getloan[3]) + '\t\t , ' + str(getloan[4]) + '\t\t , ' + str(getloan[5]) + '\t\t , cần vay ' + str(getloan[6])

            requests.get(url)
            rawhn.delete_rows(1, 1)
    except:
        print('ko ket noi duoc den telegram')


