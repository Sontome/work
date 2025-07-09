
import cv2
import pyperclip
import time
import pywinauto
import pyautogui
import requests
#                                     175% chrome
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
newestnhaptay = sht.worksheet('newestnhaptay')
listold= sht.worksheet('Listold')
rawhcm= sht.worksheet('So HCM+HN ngoai thanh')
rawhn = sht.worksheet('RawHN')
app = application.Application(backend="uia")
urlhcm = 'https://api.telegram.org/bot5737041469:AAG5XdXVwATvldvDpXmnlQT0dmh2-sZ70gE/sendMessage?chat_id=-634512779&text=HĐ '



#đăng nhập ------------------- -------------------------------
web = app.start(r'"C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Default"')

input("an phim bat ki de tiep tuc")
time.sleep(4)
time.sleep(2)
send_keys("p2p.tima.vn{ENTER}")
time.sleep(3)
send_keys("{TAB}{TAB}0367507100{TAB}123456{ENTER}")
time.sleep(3)


#-----------mở tab info----------------------------------

send_keys('^t')
pyautogui.write("https://docs.google.com/spreadsheets/d/1KrJoO8kKZ5IYr9qJkMiXuKCHoNF-OnjNz05qYTEjrYI/edit#gid=803076381")
send_keys("{ENTER}")
time.sleep(3)
send_keys('^{TAB}')
time.sleep(3)
# send_keys('^{VK_ADD}')
# send_keys('^{VK_ADD}')


# -------------------------------------------------------------
# clipboard = send_keys('^a^c')
# df = pd.read_clipboard()
# print(df)



def checkhd(hd):
    job ='null'
    value = 'null'
    district = 'null'
    province = 'null'
    tenkh='null'
    sdt = 'đã bán'
    url='null'
    time.sleep(1)
    pywinauto.mouse.click(button='left', coords=(428, 581))
    time.sleep(1)
    pywinauto.mouse.click(button='left', coords=(355, 720))
    time.sleep(1)
    pywinauto.mouse.click(button='left', coords=(934, 924))
    time.sleep(1)
    pywinauto.mouse.click(button='left', coords=(924, 1008))
    time.sleep(1)
    pywinauto.mouse.double_click(button='left', coords=(493, 502))
    pyautogui.write(str(hd))
    send_keys("{ENTER}")
    time.sleep(2)
    try:
        so1 =  pyautogui.locateOnScreen('so1.png',confidence=0.9,minSearchTime=2,region=(264, 683,444, 904))
        print("co thay hd")

        pywinauto.mouse.click(button='left', coords=(635, 694))
        time.sleep(1)
        pywinauto.mouse.click(button='left', coords=(638, 726))
        time.sleep(2)
        pywinauto.mouse.click(button='left', coords=(636, 751))
        time.sleep(1)
        pywinauto.mouse.click(button='left', coords=(910, 390))

        send_keys('^a^c')


        time.sleep(0.2)
        tenkh = str(pyperclip.paste())
        pyperclip.copy("")


        pywinauto.mouse.click(button='left', coords=(1365, 386))
        send_keys('^a^c')

        sdt = str(pyperclip.paste())
        pyperclip.copy("")

        time.sleep(0.2)

        pywinauto.mouse.click(button='left', coords=(896, 598))

        send_keys('^a^c')


        time.sleep(0.2)
        job = str(pyperclip.paste())
        pyperclip.copy("")
        pywinauto.mouse.click(button='left', coords=(891, 710))

        send_keys('^a^c')


        time.sleep(0.2)
        value = str(pyperclip.paste())
        pyperclip.copy("")
        pywinauto.mouse.click(button='left', coords=(1404, 928))
        send_keys('^a^c')


        time.sleep(0.2)
        district = str(pyperclip.paste())
        pyperclip.copy("")
        pywinauto.mouse.click(button='left', coords=(913, 931))
        send_keys('^a^c')
        time.sleep(0.2)
        province = str(pyperclip.paste())
        pyperclip.copy("")
        pywinauto.mouse.click(button='left', coords=(93, 1000))

        static = 1
    except :
        static = 0
    urlhn = 'https://api.telegram.org/bot5737041469:AAG5XdXVwATvldvDpXmnlQT0dmh2-sZ70gE/sendMessage?chat_id=-775255924&text=HĐ '
    urlhcm = 'https://api.telegram.org/bot5737041469:AAG5XdXVwATvldvDpXmnlQT0dmh2-sZ70gE/sendMessage?chat_id=-634512779&text=HĐ '

    if district== "Sóc Sơn":
        url=urlhcm
    elif  district== "Mê Linh":
        url=urlhcm
    elif  district== "Sơn Tây":
        url=urlhcm
    elif  district== "Ba Vì":
        url=urlhcm
    elif  district== "Chương Mỹ":
        url=urlhcm
    elif  district== "Đan Phượng":
        url=urlhcm
    elif  district== "Hoài Đức":
        url=urlhcm
    elif  district== "Mỹ Đức":
        url=urlhcm
    elif  district== "Phú Xuyên":
        url=urlhcm
    elif  district== "Phúc Thọ":
        url=urlhcm
    elif  district== "Quốc Oai":
        url=urlhcm
    elif  district== "Sơn Tây":
        url=urlhcm
    elif  district== "Thạch Thất":
        url=urlhcm
    elif  district== "Thanh Oai":
        url=urlhcm
    elif  district== "Thanh Trì":
        url=urlhcm
    elif  district== "Thường Tín":
        url=urlhcm
    elif  district== "Ứng Hòa":
        url=urlhcm
    elif  district== "Đông Anh":
        url=urlhcm
    elif  province== "Hà Nội":
        url=urlhn
    else:
        url=urlhcm
    ketquacheck= (hd, sdt, static,tenkh,district,province,job,value,url)
    print(ketquacheck)
    return ketquacheck


def searbox(x) :
    pywinauto.mouse.double_click(button='left', coords=(493, 502))
    pyautogui.write(str(x))
    send_keys("{ENTER}")
    time.sleep(1)




# chon ngay thang-------------------------------------------------------------

# chon ngay thang------------------------------------------------------

# hd= '390790'
#searbox(sdt)

# ==================

# print(ketquacheck)
def loopsear(hd):


    global final
    pywinauto.mouse.double_click(button='left', coords=(493, 502))
    pyautogui.write(str(hd))
    send_keys("{ENTER}")
    time.sleep(1.5)
    locationX, locationY = pyautogui.locateCenterOnScreen('so1.png', confidence=0.9, minSearchTime=2,
                                                          region=(264, 683,444, 904))

    toadox = int(locationX + 280)
    toadoy = 590
    toadox2 = int(locationX + 770)
    toadoy2 = int(2 * locationY - 1366)

    anhhdsear = pyautogui.screenshot(region=(toadox, 683,700, toadoy2))
    anhhdsear.save('anhhdsear.png')
    time.sleep(0.3)

    sdt = str(final[1])



    numsear = str(final[1])[-3:]




    for a in range(0, 8):
        b = 0
        for i in range(0, 10):
            x = numsear +str(i)
            print(x)
            searbox(x)

            try:
                location = pyautogui.locateOnScreen('anhhdsear.png',confidence=0.8)
                print(f"Vị trí tọa độ của hình ảnh: {location}")
                numsear=x
                break
            except pyautogui.ImageNotFoundException:
                if i== 9:
                    b = 1

        if b==1 :
            if a >5:
                a=5
            solan = 5-a
            break





    for a in range(0, solan):

        for i in range(0, 10):
            x = str(i) + numsear
            print(x)
            searbox(x)

            try:
                location = pyautogui.locateOnScreen('anhhdsear.png', confidence=0.8)
                print(f"Vị trí tọa độ của hình ảnh: {location}")
                numsear = x
                break
            except pyautogui.ImageNotFoundException:
                pass
                # print("Không tìm thấy hình ảnh trên màn hình.")



                # print("Không tìm thấy hình ảnh trên màn hình.")

    if len(numsear)==8:

        sdt = str(final[1][0:2])+numsear
        searbox(sdt)
    elif len(numsear) == 9 :
        sdt = str(final[1][0:1]) + numsear
        searbox(sdt)
    elif len(numsear) == 10:
        sdt =  numsear
        searbox(sdt)
    try:
        location = pyautogui.locateOnScreen('anhhdsear.png', confidence=0.8)
        print(f"đã đúng sdt")


        print(sdt)
        url= final[8]

        urll = url + \
              final[0] + '\t\t SĐT : ' + sdt + '\t\t Tên :' + final[3] + '\t\t , ' + final[4] + '\t\t , ' + final[5] + '\t\t , ' + final[6] + '\t\t , cần vay ' + final[7]
        ketquacheckpush = (final[0], sdt, final[3], final[4], final[5], final[6], final[7])
        if url==urlhcm:
            rawhcm.insert_row(ketquacheckpush, 2)
        else:
            rawhn.insert_row(ketquacheckpush, 1)
        #requests.get(urll)

        listold.insert_row([hd,sdt],2)
    except :
        print(sdt+" sai")
    time.sleep(5)
    return sdt
hdcu1 = 2
hdcu2 = 3
while True :
    try:

        pywinauto.mouse.click(button='left', coords=(93, 1000))
        send_keys("{F5}")

        time.sleep(3)

        getloan = newestnhaptay.acell('A1').value

        if getloan == None:
            time.sleep(20)
            print('đã chạy hết > đi check đơn mới lên')
            pywinauto.mouse.click(button='left', coords=(93, 1000))
            send_keys('^a')
            time.sleep(0.5)
            send_keys('^c')
            time.sleep(0.5)
            send_keys('^{TAB}')
            time.sleep(2)
            send_keys('^v')
            time.sleep(3)
            send_keys('^{TAB}')



        else:
            if int(getloan) == 1:
                requests.get(
                    'https://api.telegram.org/bot5737041469:AAG5XdXVwATvldvDpXmnlQT0dmh2-sZ70gE/sendMessage?chat_id=-4153385107&text=Bot Check Sdt Online')
                time.sleep(3)
            elif getloan == hdcu2:
                listold.insert_row([getloan,'Da Ban'],2)

            else:
                hdcu2 = hdcu1
                hdcu1 = getloan

                queue = len(newestnhaptay.col_values(1))
                print('Hang cho con ' + str(queue))
                print(getloan)
                final= checkhd(getloan)





    #chuyển đơn xuống cuối chạy lại nếu sdt lỗi -------------------------
                if final[1] != "đã bán":
                    sdtcheck = loopsear(getloan)
                    if len(str(sdtcheck)) != 10:




                        print('check lỗi')
                else :
                    print('đơn đã bán không tìm thấy')
                    listold.insert_row([getloan], 2)
    #----------------------------------------------------------





                time.sleep(3)

    except:
        time.sleep(3)