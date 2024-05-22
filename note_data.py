# -*- coding: utf-8 -*-
"""
Created on Wed May 22 01:44:14 2024

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

URL = "https://www.fragrantica.com/notes/Bigarade-1083.html"
driver.get(URL)

try:
    # <h1> 태그의 텍스트를 추출하여 note_name에 저장
    note_name_element = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, 'div.cell.text-center h1'))
    )
    note_name = note_name_element.text
    print(f"Note Name: {note_name}")

    # <p> 태그의 텍스트를 추출하여 Other_group에 저장
    other_group_element = driver.find_element(By.CSS_SELECTOR, 'div.cell.text-center p')
    other_group = other_group_element.text.replace('\n', ' ')  # 줄바꿈을 공백으로 변경
    print(f"Other Group: {other_group}")

    # <h3> 태그의 텍스트를 추출하여 group에 저장
    group_element = driver.find_element(By.CSS_SELECTOR, 'div.cell.text-center h3')
    group = group_element.text
    print(f"Group: {group}")

except Exception as e:
    print("페이지 가져오기 실패")
    print(e)

finally:
    driver.quit()
