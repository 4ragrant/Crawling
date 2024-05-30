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
import psutil
import os
import socket
import random

data = {'Product': [], 'Gender': [], 'Accords': [], 'Description': [], 'AdditionalInfo': [],
        'TopNotes': [], 'MiddleNotes': [], 'BaseNotes': [], 'love': [], 'like': [], 'ok': [], 'dislike': [], 'hate': [],
        'winter': [], 'spring': [], 'summer': [], 'fall': [], 'day': [], 'night': []}

#with open('2024_1.txt', 'r') as f:
#    urls = f.read().splitlines()

csv_file_path = "2023.csv"
urls = pd.read_csv(csv_file_path)["URL"].tolist()
# urls = ["https://www.fragrantica.com/perfume/Gritti/Mango-Aoud-86927.html"]
# review_urls = [url + "#all-reviews" for url in urls]

COUNT = 0

def kill_process(name):
    for proc in psutil.process_iter():
        if proc.name() == name:
            proc.kill()

def delete_folder(folder):
    if os.path.exists(folder):
        try:
            shutil.rmtree(folder)
        except Exception as e:
            print(f"폴더 삭제 중 오류 발생: {e}")

def is_port_in_use(port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(('localhost', port)) == 0

def random_sleep(min_seconds=5, max_seconds=10):
    time.sleep(random.uniform(min_seconds, max_seconds))

def get_random_user_agent():
    user_agents = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Safari/605.1.15",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0",
        "Mozilla/5.0 (iPhone; CPU iPhone OS 14_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1"
    ]
    return random.choice(user_agents)

def get_available_port(start_port=9223, end_port=9300):
    for port in range(start_port, end_port):
        if not is_port_in_use(port):
            return port
    raise Exception("사용 가능한 포트를 찾을 수 없습니다.")

for url in urls:
    try:
        # Ensure Chrome processes are killed and cleanup temp directory
        kill_process("chrome.exe")
        delete_folder(r"c:\chrometemp")

        if is_port_in_use(9223):
            print("포트 9223이 사용 중입니다. 다른 포트를 사용하거나 사용 중인 프로세스를 종료하세요.")
            continue
        
        # Start Chrome with remote debugging
        subprocess.Popen(r'C:\Program Files (x86)\Google\Chrome\Application\chrome.exe --remote-debugging-port=9223 --user-data-dir="C:\chrometemp"')

        # Setup Chrome options for remote debugging
        options = Options()
        options.add_experimental_option("debuggerAddress", "127.0.0.1:9223")
        options.add_argument(f"user-agent={get_random_user_agent()}")
        options.add_argument("disable-gpu")   # GPU가속 끄기
        options.add_argument("lang=ko_KR")    # 가짜 플러그인 탑재
        options.add_argument("--incognito")  # 시크릿 모드로 브라우저 열기
        
        # Install and setup ChromeDriver
        chrome_ver = chromedriver_autoinstaller.get_chrome_version().split('.')[0]
        chromedriver_autoinstaller.install(True)
        service = Service(f'./{chrome_ver}/chromedriver.exe')

        driver = None
        for _ in range(3):  # 최대 3번 재시도
            try:
                driver = webdriver.Chrome(service=service, options=options)
                driver.implicitly_wait(10)
                driver.get(url)
                time.sleep(2)
                break
            except Exception as e:
                print(f"드라이버 초기화 실패, 재시도 중... ({e})")
                if driver:
                    driver.quit()
                time.sleep(5)
        
        if driver is None:
            raise Exception("Chrome 드라이버를 초기화할 수 없습니다.")
            
        COUNT += 1    
        print("반복횟수:", COUNT)
        
        # 향수 이름, 성별
        element = driver.find_element(By.CSS_SELECTOR, 'h1[itemprop="name"]')
        full_text = element.text
        split_index =full_text.rfind('for')
        
        product = full_text[:split_index].strip()
        gender = full_text[split_index + 4:].strip()
        
        print("Product:", product)
        print("Gender:", gender)
        
        data['Product'].append(product)
        data['Gender'].append(gender)
        
        # Main Accords
        accord_elements = driver.find_elements(By.CSS_SELECTOR, '.accord-box .accord-bar')
        accords = [f"{elem.text} ({elem.get_attribute('style').split('width: ')[-1].split('%')[0].strip()}%)" for elem in accord_elements]
        accords_string = ', '.join(accords)
        print("Main accords:", accords_string)
        data['Accords'].append(accords_string)
        
        # 전체 설명
        print("---Description---")
        description_element = driver.find_element(By.XPATH, '//div[@itemprop="description"]/p')
        print(description_element.text)
        data['Description'].append(description_element.text)
        
        # 추가 설명 (Detail)
        print("---Additional info---")
        try:
            detail_description = driver.find_element(By.CSS_SELECTOR, '.fragrantica-blockquote')
            paragraphs = detail_description.find_elements(By.TAG_NAME, 'p')
            additional_info = '\n'.join([p.text.strip() for p in paragraphs if p.text.strip()])
        except:
            additional_info = "Not Found"
            
        print(additional_info)
        data['AdditionalInfo'].append(additional_info)
        
        # 피라미드 노트
        print("---Perfume Pyramid---")
        top, middle, base = [], [], []
        
        try:
            top_notes = driver.find_elements(By.XPATH, "//*[@id='pyramid']/div[1]/div/div[2]/div[3]/div")
            for element in top_notes:
                text = element.text.replace('\n', ', ').strip()
                print("Top notes:", text)
                top.append(text)
        except:
            top.append("Not Found")
            
        try:
            middle_notes = driver.find_elements(By.XPATH, "//*[@id='pyramid']/div[1]/div/div[2]/div[4]/div")
            for element in middle_notes:
                text = element.text.replace('\n', ', ').strip()
                print("Middle notes:", text)
                middle.append(text)
        except:
            middle.append("Not Found")
            
        try:
            base_notes = driver.find_elements(By.XPATH, "//*[@id='pyramid']/div[1]/div/div[2]/div[5]/div")
            for element in base_notes:
                text = element.text.replace('\n', ', ').strip()
                print("Base notes:", text)
                base.append(text)
        except:
            base.append("Not Found")
            
        data['TopNotes'].append(', '.join(top))
        data['MiddleNotes'].append(', '.join(middle))
        data['BaseNotes'].append(', '.join(base))
        
        # 선호도와 계절감
        print("---preference and seasons---")
        love, like, ok, dislike, hate, winter, spring, summer, fall, day, night = [0] * 11  # 초기값 설정
        preference_and_season_elements = driver.find_elements(By.XPATH, "//div[@class='cell small-6']/..//div[@class='voting-small-chart-size']/div/div")
        
        for i, element in enumerate(preference_and_season_elements):
            style_attribute = element.get_attribute("style")
            width_value = re.search(r'width:\s*([\d.]+%)', style_attribute).group(1)

            if i == 0:
                love = float(width_value[:-1])
                print("love:", love, "%")
            elif i == 1:
                like = float(width_value[:-1])
                print("like:", like, "%")
            elif i == 2:
                ok = float(width_value[:-1])
                print("ok:", ok, "%")
            elif i == 3:
                dislike = float(width_value[:-1])
                print("dislike:", dislike, "%")
            elif i == 4:
                hate = float(width_value[:-1])
                print("hate:", hate, "%")
            elif i == 5:
                winter = float(width_value[:-1])
                print("winter:", winter, "%")
            elif i == 6:
                spring = float(width_value[:-1])
                print("spring:", spring, "%")
            elif i == 7:
                summer = float(width_value[:-1])
                print("summer:", summer, "%")
            elif i == 8:
                fall = float(width_value[:-1])
                print("fall:", fall, "%")
            elif i == 9:
                day = float(width_value[:-1])
                print("day:", day, "%")
            elif i == 10:
                night = float(width_value[:-1])
                print("night:", night, "%")
                   
        data['love'].append(love)
        data['like'].append(like)
        data['ok'].append(ok)
        data['dislike'].append(dislike)
        data['hate'].append(hate)
        data['winter'].append(winter)
        data['spring'].append(spring)
        data['summer'].append(summer)
        data['fall'].append(fall)
        data['day'].append(day)
        data['night'].append(night)

        driver.quit()

        # Cleanup Chrome processes and temp folder
        kill_process("chrome.exe")
        delete_folder(r"c:\chrometemp")
        
        print("5분간 대기합니다.")
        time.sleep(300)
        
        # 10개의 요청마다 6분 대기
        # if COUNT != 0 and COUNT % 10 == 0:
        #    print("10개의 요청이 완료되어 6분간 대기합니다.")
        #    time.sleep(360)
        
        if COUNT != 0 and COUNT % 100 == 0:
            df = pd.DataFrame(data)
            output_csv_file_path = f"결과데이터_2023_{COUNT}.csv"

            try:
                df.to_csv(output_csv_file_path, index=False, encoding='utf-8')
                print(f"데이터가 CSV 파일에 저장되었습니다: {output_csv_file_path}")
            except Exception as e:
                print(f"CSV 파일 저장 중 오류 발생: {e}")

    except Exception as e:
        print("페이지 가져오기 실패")
        print(e)
        if driver:
            driver.quit()



# 디버깅: 데이터 프레임을 출력하여 확인
print("데이터 프레임:\n", df)