import random
from time import sleep
import gspread
import requests
import time
import pywinauto
import pyautogui
from pywinauto.keyboard import send_keys
import pyperclip

gs = gspread.service_account('autocheckdonserviceacc.json')
sht = gs.open_by_key('1KrJoO8kKZ5IYr9qJkMiXuKCHoNF-OnjNz05qYTEjrYI')
listchecklos = sht.worksheet('listchecklos')
RawLOSSDT = sht.worksheet('RawLOSSDT')

















i= 0
r = 0

while i <20:
    try:
        a = random.uniform(1, 2)
        r = r+1
        if r>20 :
            r=0
            pywinauto.mouse.click(button='left', coords=(91, 59))
            sleep(2)
        pywinauto.mouse.click(button='left', coords=(63, 1117))
        sleep(a)
        Loan1st = str(listchecklos.acell('A1').value)

        pywinauto.mouse.double_click(button='left', coords=(453, 383))
        pyautogui.write(Loan1st)

        send_keys("{ENTER}")
        time.sleep(a)
        x, y = pyautogui.locateCenterOnScreen('1.png', confidence=0.9, minSearchTime=2,
                                              region=(289, 544,342, 549))
        pywinauto.mouse.click(button='left', coords=(x+500, y-10))
        time.sleep(a)
        x,y = pyautogui.locateCenterOnScreen('phone.png', confidence=0.9, minSearchTime=2, region=(1229, 306, 800, 1000))
        pywinauto.mouse.click(button='right', coords=(x, y))
        time.sleep(0.2)
        pywinauto.mouse.click(button='left', coords=(x+30, y+438))
        time.sleep(0.2)
        pywinauto.mouse.click(button='right', coords=(x, y))
        time.sleep(0.2)
        pywinauto.mouse.click(button='left', coords=(x + 30, y + 470))
        x, y = pyautogui.locateCenterOnScreen('pbx.png', confidence=0.9, minSearchTime=2,
                                              region=(3077, 123, 800, 1800))

        pywinauto.mouse.double_click(button='left', coords=(x+90, y))
        time.sleep(0.2)
        pywinauto.mouse.double_click(button='left', coords=(x+90, y))
        send_keys('^c')

        time.sleep(0.2)
        sdt = str(pyperclip.paste())
        print(sdt)
        pyperclip.copy("")
        kq = [int(Loan1st),sdt]
        print(kq)
        listchecklos.delete_rows(1, 1)
        RawLOSSDT.insert_row(kq,1,1)
        sleep(a)





        

    except:
        i = i + 1
        sleep(5)
print('chay xong don')
input('press any key')
sleep(30)