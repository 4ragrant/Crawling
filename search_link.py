# -*- coding: utf-8 -*-
"""
Created on Tue Apr 30 18:09:39 2024

@author: PC
"""

import requests
from bs4 import BeautifulSoup

response = requests.get('https://www.fragrantica.com/search/', headers={'User-agent': 'your bot 0.1'})
html = response.text
soup = BeautifulSoup(html, 'html.parser')

# 제품 정보가 포함된 div 요소를 선택합니다.
products = soup.find_all('div', class_='card-section')

# 각 제품의 링크를 저장할 리스트를 생성합니다.
product_links = []

# 제품 정보를 추출하고 링크를 리스트에 추가합니다.
for product in products:
    # 각 제품의 링크는 'a' 태그 안에 있습니다.
    link_tag = product.find('a')
    if link_tag:  # 'a' 태그가 존재하는 경우에만 링크를 추출합니다.
        link = link_tag['href']
        product_links.append(link)

with open('search_links.txt', 'w') as f:
    for link in product_links :
        f.write(link + '\n')
        
print("search 링크 텍스트 파일 저장 완료")