import requests
from bs4 import BeautifulSoup
from tkinter import*
from time import sleep
import os
import subprocess
import sys
from winreg import *

#region AutoRun
keypath = OpenKey(HKEY_CURRENT_USER, "SOFTWARE\Microsoft\Windows\CurrentVersion\Run", 0, KEY_ALL_ACCESS)
SetValueEx(keypath, "급식", 0, REG_SZ, sys.argv[0])
#endregion

Title = "급식 안내" # 메세지박스 제목
msgPath = os.environ["TEMP"]

def scrape_school():
    # url에 사이트 주소를 입력
    url ="https://search.naver.com/search.naver?where=nexearch&sm=tab_etc&mra=blBI&pkid=682&os=24929523&qvt=0&query=%EC%84%9C%EC%9A%B8%EC%95%84%EC%9D%B4%ED%8B%B0%EA%B3%A0%EB%93%B1%ED%95%99%EA%B5%90"
    res = requests.get(url)
    soup = BeautifulSoup(res.text,"lxml")
    date_1 = soup.find("strong", attrs={"class":"cm_date"}).get_text() # 오늘 날짜를 웹스크래핑
    today = soup.find("ul", attrs={"class":"item_list"}).get_text() # 오늘 급식을 웹스크래핑
    
    
    messages = ('{}{}'.format(date_1, today)) # 메세지에 오늘 날짜와 오늘의 급식을 입력
    # print(messages)
    # tkinter.messagebox.showinfo('급식',messages)
    objVBS = open(msgPath + "/msgbox.vbs", "w")
    objVBS.write("MsgBox " + "\"" + messages +  "\", "  + str(4096) + ", " + '\"' + Title + '\"')
    objVBS.close()
    p = subprocess.Popen(["cscript", msgPath + "/msgbox.vbs"], shell=False, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    p.communicate()
    #print(out)
scrape_school()
