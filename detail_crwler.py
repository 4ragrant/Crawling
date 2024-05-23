import time
import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import chromedriver_autoinstaller
import subprocess
import pandas as pd
import shutil

#쿠키/캐시파일 삭제
try:
    shutil.rmtree(r"c:\chrometemp")
except FileNotFoundError:
    pass

# 디버깅 모드에서 Chrome 시작
subprocess.Popen(r'C:\Program Files (x86)\Google\Chrome\Application\chrome.exe --remote-debugging-port=9222 --user-data-dir="C:\chrometemp"')
# 옵션 설정
options = Options()
options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
# Chrome 버전 가져오기
chrome_ver = chromedriver_autoinstaller.get_chrome_version().split('.')[0]
# 크롬 드라이버 설정
chromedriver_autoinstaller.install(True)  # 자동 설치
service = Service(f'./{chrome_ver}/chromedriver.exe')

try:
    driver = webdriver.Chrome(service=service, options=options)
except Exception as e:
    print(f"Error: {e}")

driver.implicitly_wait(10)

csv_file_path = "item_links.csv"
urls = pd.read_csv(csv_file_path)["URL"].tolist()

data = []

for url in urls:
    try:    
        driver.get(url)
        time.sleep(2)
                    
    # 선호도(5), 계절감(6): 총 11건
    # preference = ["love", "like", "ok", "dislike", "hate"]
    # season = ["winter", "spring", "summer", "fall", "day", "night"]
        
        preference_and_season_elements = driver.find_elements(By.XPATH, "//div[@class='cell small-6']/..//div[@class='voting-small-chart-size']/div/div")
        for element in preference_and_season_elements:
            style_attribute = element.get_attribute("style")
            width_value = re.search(r'width:\s*([\d.]+%)', style_attribute).group(1)
            print(width_value)
            
        # 장점(8), 단점(8): 총 16건
        props_and_cons_elements = driver.find_elements(By.XPATH, "//div[@class='cell small-12 medium-6']/div[@class='cell small-12']/span")
        for element in props_and_cons_elements:
            print(element.text)
    
        # 지속력(5), 잔향(4), 성별(5), 가성비(5): 총 19건
        longevity_and_sillage_elements = driver.find_elements(By.XPATH, "//div[@class='cell small-12 medium-6']//progress")
        for element in longevity_and_sillage_elements:
            value = float(element.get_attribute("value"))
            max_value = float(element.get_attribute("max"))
            # 비율 구해서 퍼센트로 변환
            if max_value != 0:
                result = (value/max_value) * 100
                print(result)
    
        # 리뷰: 210건
        review_elements = driver.find_elements(By.XPATH, "//div[@itemprop='reviewBody']/p")
        print(len(review_elements))
        
        
    except Exception as e:
        print(f"에러 발생: {e}")
        
df = pd.DataFrame(data)
output_csv_file_path = "output_data.csv"
df.to_csv(output_csv_file_path, index=False, encoding='utf-8-sig')                

driver.quit()