# -*- coding: utf-8 -*-
"""
Created on Wed May  1 23:30:58 2024

@author: PC
"""

import pandas as pd
import requests
from bs4 import BeautifulSoup
from time import sleep

# DataFrame에 저장할 데이터를 담을 리스트를 생성합니다.
data = {'Product': [], 'Gender' : [],'Accords' : [], 'Description' : [], 'Additional_Info' : [], 'Pros' : [], 'Cons' : []}

# 디자이너 링크 파일을 열어 디자이너 링크들을 리스트로 읽어옵니다.
with open('search_links.txt', 'r') as f:
    search_links = f.read().splitlines()

    # 각 디자이너 링크를 순회하며 상품 링크를 추출합니다.
    for link in search_links:
        response = requests.get('https://www.fragrantica.com' + link, headers= {'User-agent': 'your bot 0.1'})
        
        if response.status_code == 200 :
            html = response.text
            soup = BeautifulSoup(html, 'html.parser')
            
            # 향수 이름
            product_names = soup.select('h1[itemprop="name"]')
            print(product_names)
            
            for product_name in product_names:
                product = product_name.text.strip()
                
                # 데이터 정제 : 향수 이름 / 성별
                split_index = product.rfind('for')
                product = product[:split_index].strip()
                
                gender = ''
                if split_index != -1:
                    gender = product_name.text[split_index + 4:].strip()
                
                # 향수 이름, 성별 데이터 -> 리스트에 추가
                data['Product'].append(product)
                data['Gender'].append(gender)
                
                # 향수 Main Accords
                accord_bar = soup.select('.accord-bar')
                accords = []
                for accord in accord_bar:
                    accords.append(accord.text.strip())
                
                # 각 향수의 Accords를 쉼표로 구분된 하나의 문자열로 변환하여 리스트에 추가
                accords_string = ', '.join(accords)
                data['Accords'].append(accords_string)
                
                # 향수 설명
                description_element = soup.find('div', itemprop="description")
                
                if description_element:
                    description = description_element.find('p').text
                else:
                    description = "Description not found"


                # 향수 설명 (Detail)
                fragrantica_blockquote = soup.find('div', class_="fragrantica-blockquote")
                if fragrantica_blockquote:
                    paragraphs = fragrantica_blockquote.select('p')
                    additional_info = '\n'.join([p.text.strip() for p in paragraphs])
                    
                else:
                    additional_info = "Additional info not found"
                
                print(description)
                print(additional_info)
            
            
                data['Description'].append(description)
                data['Additional_Info'].append(additional_info)
                
                # 향수 Pros and Cons (사용자 의견)
                print("---- Pros and Cons")
                
                pros_icon = soup.find('img', alt='Pros')
                
                if pros_icon :
                    # 찾은 pros_icon의 부모 요소 찾기
                    pros_section = pros_icon.find_parent('div', class_= 'cell small-6')
                    # pros_section 전체를 찾으면
                    if pros_section :
                        pros_items = pros_section.find_all('div', class_= 'cell small-12 medium-6').find_all('div', class_='cell small-12')
                        print(pros_items)
                        pros_data = []
                
                        for pros in pros_items :
                            text = pros.text.strip() # Pros 항목 텍스트
                            thumbs_up = int(pros.find('div', class_= 'num-votes-sp').text)
                            thumbs_down = int(pros.find('div', class_='num-votes-sp')[1].text)
                            
                            pros_data.append((text, thumbs_up, thumbs_down))
                    
                        print("Pros Data : ")
                        for data in pros_data :
                            print(pros_data)
                            data['Pros'].append(pros_data)
                            
                    else:
                        print("Pros section not found")
                else:
                    print("Pros icon not found")
        else:
            print("상품 페이지를 가져오지 못했습니다.")        
            
        # 대기 시간
        #sleep(100)

# DataFrame을 생성합니다.
df = pd.DataFrame(data)

print(df)

# 엑셀 파일로 저장합니다.
df.to_excel('designer_products.xlsx', index=False)

print("엑셀 파일에 데이터 저장 완료")