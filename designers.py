# -*- coding: utf-8 -*-
"""
Created on Fri Apr 26 16:45:04 2024

@author: DS
"""

import requests
from bs4 import BeautifulSoup

response = requests.get('https://www.fragrantica.com/designers/', headers = {'User-agent': 'your bot 0.1'})
html = response.text
soup = BeautifulSoup(html, 'html.parser')
ndu = soup.select('div[class=nduList]')
for nduu in ndu:
    nduuu = nduu.select('a')
    strn = str(nduuu[0])
    startIndex = strn.find('"')
    endIndex = strn.find('"',startIndex+1)
    print("https://www.fragrantica.com" + strn[startIndex+1:endIndex])