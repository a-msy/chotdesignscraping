import math
import sys
import re
import glob
import os
import json
import time
import chromedriver_binary

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from urllib import request

def PrintSetUp():
    #印刷としてPDF保存する設定
    chopt=webdriver.ChromeOptions()
    appState = {
        "recentDestinations": [
            {
                "id": "Save as PDF",
                "origin": "local",
                "account":""
            }
        ],
        "selectedDestinationId": "Save as PDF",
        "version": 2,
        "isLandscapeEnabled": True, #印刷の向きを指定 tureで横向き、falseで縦向き。
        "pageSize": 'A4', #用紙タイプ(A3、A4、A5、Legal、 Letter、Tabloidなど)
        #"mediaSize": {"height_microns": 355600, "width_microns": 215900}, #紙のサイズ　（10000マイクロメートル = １cm）
        #"marginsType": 0, #余白タイプ #0:デフォルト 1:余白なし 2:最小
        #"scalingType": 3 , #0：デフォルト 1：ページに合わせる 2：用紙に合わせる 3：カスタム
        #"scaling": "141" ,#倍率
        #"profile.managed_default_content_settings.images": 2,  #画像を読み込ませない
        "isHeaderFooterEnabled": False, #ヘッダーとフッター
        "isCssBackgroundEnabled": True, #背景のグラフィック
        #"isDuplexEnabled": False, #両面印刷 tureで両面印刷、falseで片面印刷
        #"isColorEnabled": True, #カラー印刷 trueでカラー、falseで白黒
        "isCollateEnabled": True #部単位で印刷
    }
    
    prefs = {'printing.print_preview_sticky_settings.appState':
             json.dumps(appState),
             "download.default_directory": "./downloads"
             } #appState --> pref
    chopt.add_experimental_option('prefs', prefs) #prefs --> chopt
    chopt.add_argument("--headless")
    chopt.add_argument('--kiosk-printing') #印刷ダイアログが開くと、印刷ボタンを無条件に押す。
    return chopt

def main_WebToPDF(BlogURL):
    #Web ページもしくはhtmlファイルをPDFにSeleniumを使って変換する
    chopt = PrintSetUp()
    driver_path = "/opt/chrome/chromedriver" #webdriverのパス
    driver = webdriver.Chrome(executable_path=driver_path, options=chopt)
    driver.implicitly_wait(10) # 秒 暗示的待機 
    driver.get(BlogURL) #ブログのURL 読み込み
    WebDriverWait(driver, 15).until(EC.presence_of_all_elements_located)  # ページ上のすべての要素が読み込まれるまで待機（15秒でタイムアウト判定）
    driver.execute_script('return window.print()') #Print as PDF
    time.sleep(10) #ファイルのダウンロードのために10秒待機
    driver.quit() #Close Screen

url = "https://chot.design"
files = os.listdir("./links")
for file in files:
    f = open("./links/"+file)
    links = f.read().split()
    prefix = file.replace(".txt","")
    for index,link in enumerate(links):
        filename = prefix+"-"+str(index)+".pdf"
        print(url+link)
        main_WebToPDF(url+link)