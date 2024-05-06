# -*- coding: utf-8 -*-
"""
Created on Fri Apr 26 18:25:48 2024

@author: DS
"""


import requests
from bs4 import BeautifulSoup


url = "https://www.fragrantica.com/perfume/Chanel/Antaeus-616.html"
headers = ""

response = requests.get(url)

if response.status_code == 200:
    with open('fragrantica.html', 'w', encoding='utf-8') as file:
        file.write(response.text)
else:
    print('실패', response.status_code)