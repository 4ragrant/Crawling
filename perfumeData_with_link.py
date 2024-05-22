# -*- coding: utf-8 -*-
"""
Created on Wed May 22 01:04:03 2024

@author: PC
"""

import time
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

driverPath = "D:\chromedriver-win64\chromedriver.exe"
driver = webdriver.Chrome()

options = Options()
options.add_argument("--start-maximized")
options.add_experimental_option("detach", True)
options.add_argument("--disable-blink-features=AutomationControlled")

# DataFrame에 저장할 데이터 리스트 생성
data = {'Product': [], 'Gender' : [], 'Accords' : [], 'Description' : [], 'Additional_Info' : [],
         'Top_Notes': [], 'Middle_Notes': [], 'Base_Notes': []}

# URL = "https://www.fragrantica.com/perfume/Givenchy/Amarige-3.html"
# driver.get(URL)

with open('search_links.txt', 'r') as f:
    search_links = f.read().splitlines()

    # 링크 순회 -> 상품 링크 추출
    for link in search_links:
        driver.get('https://www.fragrantica.com' + link)

        try:
            
            # 향수 이름 + 성별
            print("향수 이름 + 성별")
            elements = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'h1[itemprop="name"]')))
            print(elements.text)
            
            product = elements.text.strip()
            
            # 데이터 정제 : 향수 이름 / 성별
            split_index = product.rfind('for')
            product = product[:split_index].strip()
            
            gender = ''
            if split_index != -1:
                gender = elements.text[split_index + 4:].strip()
            
            # 향수 이름, 성별 데이터 -> 리스트에 추가
            data['Product'].append(product)
            data['Gender'].append(gender)
        
            # 향수 Main Accords
            print("\n")
            print("향수 Main accords")
            
            accord_elements = driver.find_elements(By.CSS_SELECTOR, '.accord-box .accord-bar')
            accords = [f"{elem.text} ({elem.get_attribute('style').split('width: ')[-1].split('%')[0].strip()}%)" for elem in accord_elements]
            accords_string = ', '.join(accords)
            print(accords_string)
            data['Accords'].append(accords_string)
        
            # 향수 전체 설명
            print("\n")
            print("향수 전체 설명")
            description_element = driver.find_element(By.XPATH, '//div[@itemprop="description"]/p')
            print(description_element.text)
            data['Description'].append(description_element.text)
            
            # 향수 추가 설명 (Detail)
            print("\n'")
            print("향수 추가 설명")
            
            try:
                detail_description = driver.find_element(By.CSS_SELECTOR, '.fragrantica-blockquote')
                paragraphs = detail_description.find_elements(By.TAG_NAME, 'p')
                additional_info = '\n'.join([p.text.strip() for p in paragraphs if p.text.strip()])
            
            except:
                additional_info = "Additional info not found"
            
            print(additional_info)
            data['Additional_Info'].append(additional_info)
        
            
            # 향수 피라미드
            print("\n")
            print("향수 피라미드")
            
            def extract_notes(section_name):
                try:
                    section_header = WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.XPATH, f'//h4/b[text()="{section_name}"]/parent::h4/following-sibling::div'))
                    )
                    note_divs = section_header.find_elements(By.XPATH, './/div[contains(@style, "margin: 0.2rem")]')
                    notes = [div.text.split('\n')[-1] for div in note_divs if div.text.strip()]
                    notes_string = ', '.join(notes)
                    return notes_string
                except Exception as e:
                    print(f"{section_name} section not found")
                    return ""
        
            # Top notes
            print("\n")
            print("---Top note---")
            top_notes_string = extract_notes("Top Notes")
            print(top_notes_string)
            data['Top_Notes'].append(top_notes_string)
        
            # Middle notes
            print("\n")
            print("---Middle note---")
            middle_notes_string = extract_notes("Middle Notes")
            print(middle_notes_string)
            data['Middle_Notes'].append(middle_notes_string)
        
            # Base notes
            print("\n")
            print("---Base note---")
            base_notes_string = extract_notes("Base Notes")
            print(base_notes_string)
            data['Base_Notes'].append(base_notes_string)
            
            
        except Exception as e:
            print("페이지 가져오기 실패")
            print(e)
    
# DataFrame을 생성합니다.
df = pd.DataFrame(data)

# DataFrame을 CSV 파일로 저장합니다.
csv_file_path = 'Real_data.csv'
df.to_csv(csv_file_path, index=False, encoding='utf-8')
print(f"Data saved to {csv_file_path} 저장")