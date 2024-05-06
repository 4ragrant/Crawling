# -*- coding: utf-8 -*-
"""
Created on Thu May  2 00:52:23 2024

@author: PC
"""

import pandas as pd
import requests
from bs4 import BeautifulSoup
from time import sleep

# DataFrame에 저장할 데이터를 담을 리스트를 생성합니다.
data = {'Product': [], 'Designer': [], 'Main Accords' : []}

# 디자이너 링크 파일을 열어 디자이너 링크들을 리스트로 읽어옵니다.
with open('search_links.txt', 'r') as f:
    search_links = f.read().splitlines()

# 각 디자이너 링크를 순회하며 상품 링크를 추출합니다.
for link in search_links:
    print(link)
    # 디자이너 페이지에 HTTP 요청을 보내고 HTML을 받아옵니다.
    response = requests.get('https://www.fragrantica.com' + link, headers={'User-agent': 'your bot 0.1'})
    html = response.text
    soup = BeautifulSoup(html, 'html.parser')

    # 상품 링크를 추출합니다.
    products = soup.find_all('div', class_='cell')
    
    for product in products:
        link_tag = product.find('a')
        if link_tag:
            product_link = link_tag['href']
            
            product_response = requests.get('https://www.fragrantica.com' + product_link, headers={'User-agent': 'your bot 0.1'})
            product_html = product_response.text
            product_soup = BeautifulSoup(product_html, 'html.parser')


            #product_name_tag = product_soup.find('h1', itemprop='name').text.strip()
            #if product_name_tag :
            #    product_name = product_name_tag.text.strip()
            #else :
            #    product_name = "Unknown"
                
            designer = product_soup.find('span', class_='vote-button-name').text.strip()

            #main_accords = [accord.text.strip() for accord in product_soup.find_all('div', class_='accord-bar')]
            
            #data['Product'].append(product_name)
            data['Designer'].append(designer)
            #data['Main Accords'].append(main_accords)
            
    sleep(100)

# DataFrame을 생성합니다.
df = pd.DataFrame(data)

print(df)

# 엑셀 파일로 저장합니다.
df.to_excel('designer_products.xlsx', index=False)

print("엑셀 파일에 데이터 저장 완료")