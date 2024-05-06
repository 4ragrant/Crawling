# -*- coding: utf-8 -*-
"""
Created on Thu May  2 15:02:14 2024

@author: PC
"""

import pandas as pd
import requests
from bs4 import BeautifulSoup
from time import sleep

# DataFrame에 저장할 데이터를 담을 리스트를 생성합니다.
data = {'Product': []}

# 디자이너 링크 파일을 열어 디자이너 링크들을 리스트로 읽어옵니다.
with open('search_links.txt', 'r') as f:
    search_links = f.read().splitlines()

# 세 번째 링크를 선택합니다.
target_link = search_links[2]

try : 
    response = requests.get('https://www.fragrantica.com' + target_link, headers={'User-agent': 'your bot 0.1'})
    html = response.text
    soup = BeautifulSoup(html, 'html.parser')
    with open('html.txt', 'w', encoding='utf-8') as file:
        file.write(html)
    
    product_name = soup.find('h1', itemprop='name').text.strip()
    
    data['Product'].append(product_name)
    #data['Main Accords'].append(main_accords)
    
except:
    pass


# DataFrame을 생성합니다.
df = pd.DataFrame(data)

print(df)

# 엑셀 파일로 저장합니다.
df.to_excel('designer_products.xlsx', index=False)

print("엑셀 파일에 데이터 저장 완료")