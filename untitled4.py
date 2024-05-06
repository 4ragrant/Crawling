# -*- coding: utf-8 -*-
"""
Created on Wed May  1 22:45:52 2024

@author: PC
"""

import requests
from bs4 import BeautifulSoup

with open('designer_links.txt', 'r') as f:
    designer_links = f.read().splitlines()

# 모든 상품 링크를 저장할 리스트를 생성합니다.
all_product_links = []

# 각 디자이너 링크를 순회하면서 상품 링크를 수집합니다.
for link in designer_links:
    response = requests.get(link, headers={'User-agent': 'your bot 0.1'})
    html = response.text
    soup = BeautifulSoup(html, 'html.parser')

    # 제품 정보가 포함된 div 요소를 선택합니다.
    products = soup.find_all('div', class_='cell')

    # 각 제품의 링크를 저장할 리스트를 생성합니다.
    product_links = []

    # 제품 정보를 추출하고 링크를 리스트에 추가합니다.
    for product in products:
        # 각 제품의 링크는 'a' 태그 안에 있습니다.
        link_tag = product.find('a')
        if link_tag:  # 'a' 태그가 존재하는 경우에만 링크를 추출합니다.
            link = link_tag['href']
            product_links.append(link)

    # 모든 상품 링크를 all_product_links에 추가합니다.
    all_product_links.extend(product_links)

# 모든 상품 링크를 한꺼번에 파일에 저장합니다.
with open('designer_product.txt', 'w') as f:
    for link in all_product_links:
        f.write(link + '\n')

print("상품 링크 텍스트 파일 저장 완료")