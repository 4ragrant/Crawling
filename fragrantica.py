# -*- coding: utf-8 -*-
"""
Created on Fri Apr 26 16:46:39 2024

@author: DS
"""

import requests
from bs4 import BeautifulSoup

def func_height(strr):
    startIndex = strr.find('height')
    endIndex = strr.find(';',startIndex)
    return strr[startIndex+8:endIndex-2]

print("Name, Group, MainNote1, MainNote2, MainNote3, Season, Day/Night, Longevity, sillage")

f = open("url.txt", 'r')
lines = f.readlines()

for line in lines:
    response = requests.get(line[:-1], headers = {'User-agent': 'your bot 0.1'})
    html = response.text

    soup = BeautifulSoup(html, 'html.parser')
    nam = soup.select('span[itemprop=name]')
    gro = soup.select('span[style=float:right;]')
    gru = gro[0].select('span[class=rtg]')
    spr = soup.select('div[id=clsspringD]')
    sum = soup.select('div[id=clssummerD]')
    aut = soup.select('div[id=clsautumnD]')
    win = soup.select('div[id=clswinterD]')
    day = soup.select('div[id=clsdayD]')
    nig = soup.select('div[id=clsnightD]')

    #print(nam[1].text)
    #print(gru[0].text)

    #-------------- SEASON ---------------------------
    strspr = str(spr[0])
    #print("spring : " + func_height(strspr))
    strsum = str(sum[0])
    #print("summer : " + func_height(strsum))
    straut = str(aut[0])
    #print("autumn : " + func_height(straut))
    strwin = str(win[0])
    #print("winter : " + func_height(strwin))
    #-------------- DAY/NIGHT ------------------------
    strday = str(day[0])
    #print("day : " + func_height(strday))
    strnig = str(nig[0])
    #print("night : " + func_height(strnig))
    #-------------- MAIN NOTES -----------------------
    mns = soup.select('div[id=userMainNotes]')
    strmns = str(mns)

    startIndex1 = strmns.find('title')
    endIndex1 = strmns.find(':',startIndex1)
    mn1 = strmns[startIndex1+7:endIndex1]

    startIndex2 = strmns.find(';',endIndex1)+1
    endIndex2 = strmns.find(':',startIndex2)
    mn2 = strmns[startIndex2:endIndex2]

    startIndex3 = strmns.find(';',endIndex2)+1
    endIndex3 = strmns.find(':',startIndex3)
    mn3 = strmns[startIndex3:endIndex3]

    mn11 = "span[title="+ mn1 +"]"
    mnn = soup.select(mn11)
    strmnn = str(mnn[0])
    startIndex1 = strmnn.find('alt')
    endIndex1 = strmnn.find('"',startIndex1+5)
    strmnn[startIndex1+5:endIndex1]
    #print("mainNote1 : " + strmnn[startIndex1+5:endIndex1])

    mn22 = "span[title="+ mn2 +"]"
    mnnn = soup.select(mn22)
    strmnnn = str(mnnn[0])
    startIndex2 = strmnnn.find('alt')
    endIndex2 = strmnnn.find('"',startIndex2+5)
    strmnnn[startIndex2+5:endIndex2]
    #print("mainNote2 : " + strmnnn[startIndex2+5:endIndex2])

    mn33 = "span[title="+ mn3 +"]"
    mnnnn = soup.select(mn33)
    strmnnnn = str(mnnnn[0])
    startIndex3 = strmnnnn.find('alt')
    endIndex3 = strmnnnn.find('"',startIndex3+5)
    strmnnnn[startIndex3+5:endIndex3]
    #print("mainNote3 : " + strmnnnn[startIndex3+5:endIndex3])

    #------ LONGEVITY, SILLAGE --------------------
    cnt = 1
    for num in soup.select('td[class=ndSum]'):
        if cnt == 1:
            #print("poor : " + num.text)
            poo = num.text
            cnt+=1
        elif cnt == 2:
            #print("weak : " + num.text)
            wea = num.text
            cnt+=1
        elif cnt == 3:
            #print("moderate : " + num.text)
            med = num.text
            cnt+=1
        elif cnt == 4:
            #print("long lasting : " + num.text)
            lon = num.text
            cnt+=1
        elif cnt == 5:
            #print("very long lasting : " + num.text)
            ver = num.text
            cnt+=1
        elif cnt == 6:
            #print("soft : " + num.text)
            sof = num.text
            cnt+=1
        elif cnt == 7:
            #print("moderate : " + num.text)
            mode = num.text
            cnt+=1
        elif cnt == 8:
            #print("heavy : " + num.text)
            hea = num.text
            cnt+=1
        elif cnt == 9:
            #print("enormous : " + num.text)
            eno = num.text
            cnt+=1
    print(nam[1].text+" : "+gru[0].text+","+strmnn[startIndex1+5:endIndex1]+","+strmnnn[startIndex2+5:endIndex2]+","+strmnnnn[startIndex3+5:endIndex3]+","+func_height(strspr)+","+func_height(strsum)+","+func_height(straut)+","+func_height(strwin)+","+func_height(strday)+","+func_height(strnig)+","+poo+","+wea+","+med+","+lon+","+ver+","+sof+","+mode+","+hea+","+eno)
f.close()