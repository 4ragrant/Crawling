# -*- coding: utf-8 -*-
"""
Created on Wed May 22 01:57:54 2024

@author: PC
"""

import time
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

driverPath = "D:\chromedriver-win64\chromedriver.exe"
driver = webdriver.Chrome()

URL = "https://www.fragrantica.com/notes/"
driver.get(URL)

try:
    # 링크들을 저장할 리스트 생성
    links = []

    # 모든 노트 링크가 포함된 div를 찾음
    note_boxes = WebDriverWait(driver, 20).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'div.notebox a'))
    )

    # 각 링크의 href 속성을 추출
    for note_box in note_boxes:
        link = note_box.get_attribute('href')
        links.append(link)

    # 링크들을 txt 파일에 저장
    with open("notes_links.txt", "w") as file:
        for link in links:
            file.write(link + "\n")
    print("Links have been saved to notes_links.txt")

except Exception as e:
    print("페이지에서 데이터를 가져오는 데 실패했습니다.")
    print(e)

finally:
    driver.quit()