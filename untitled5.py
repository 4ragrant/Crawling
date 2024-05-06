# -*- coding: utf-8 -*-
"""
Created on Wed May  1 23:13:45 2024

@author: PC
"""

import pandas as pd
import requests
from bs4 import BeautifulSoup

# DataFrame에 저장할 데이터를 담을 리스트를 생성합니다.
data = {'Designer': [], 'Product Link': []}

# 디자이너 링크 파일을 열어 디자이너 링크들을 리스트로 읽어옵니다.
with open('designer_links.txt', 'r') as f:
    designer_links = f.read().splitlines()
    
designer_links = designer_links[:designer_links.index('/board/login.php')]

# 각 디자이너 링크를 순회하며 상품 링크를 추출합니다.
for link in designer_links:
    if link.startswith('/designers') : 
        # 디자이너 페이지에 HTTP 요청을 보내고 HTML을 받아옵니다.
        response = requests.get(link, headers={'User-agent': 'your bot 0.1'})
        html = response.text
        soup = BeautifulSoup(html, 'html.parser')

        # 상품 링크를 추출합니다.
        products = soup.find_all('div', class_='cell')
        for product in products:
            link_tag = product.find('a')
            if link_tag:
                product_link = link_tag['href']
                data['Designer'].append(link)
                data['Product Link'].append(product_link)

# DataFrame을 생성합니다.
df = pd.DataFrame(data)

print(df)

# 엑셀 파일로 저장합니다.
df.to_excel('designer_products.xlsx', index=False)

print("엑셀 파일에 데이터 저장 완료")