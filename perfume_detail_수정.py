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

# 기존 CSV 파일 경로 및 데이터 로드
csv_file_path = "2024.csv"
urls = pd.read_csv(csv_file_path)["URL"].tolist()
review_urls = [url + "#all-reviews" for url in urls]

data = {'Product': [], 'Gender': [], 'Accords': [], 'Description': [], 'Additional_Info': [],
        'Top_Notes': [], 'Middle_Notes': [], 'Base_Notes': [], 'love': [], 'like': [], 'ok': [], 'dislike': [], 'hate': [],
        'winter': [], 'spring': [], 'summer': [], 'fall': [], 'day': [], 'night': [],
        'cons': [], 'props': [], 'longevity_veryweak': [], 'longevity_weak': [], 'longevity_moderate': [], 'longevity_longlasting': [], 'longevity_eternal': [],
        'sillage_intimate': [], 'sillage_moderate': [], 'sillage_strong': [], 'sillage_enormous': []}

# 모든 URL에 대해 웹 스크래핑 실행
for url in review_urls:
    try:
        # 크롬 디버깅 포트 설정 및 크롬 드라이버 자동 설치
        subprocess.Popen(r'C:\Program Files (x86)\Google\Chrome\Application\chrome.exe --remote-debugging-port=9223 --user-data-dir="C:\chrometemp"')

        options = Options()
        options.add_experimental_option("debuggerAddress", "127.0.0.1:9223")

        chrome_ver = chromedriver_autoinstaller.get_chrome_version().split('.')[0]
        chromedriver_autoinstaller.install(True)  # 자동 설치
        service = Service(f'./{chrome_ver}/chromedriver.exe')
        
        driver = webdriver.Chrome(service=service, options=options)
        driver.implicitly_wait(10)
        driver.get(url)
        time.sleep(2)
        
        # 향수 이름, 성별
        element = driver.find_element(By.CSS_SELECTOR, 'h1[itemprop="name"]')
        full_text = element.text
        split_index =full_text.rfind('for')
        
        product = full_text[:split_index].strip()
        gender = full_text[split_index + 4:].strip()
        
        print("Product: ", product)
        print("Gender: ", gender)
        
        data['Product'].append(product)
        data['Gender'].append(gender)
        
        # Main Accords
        accord_elements = driver.find_elements(By.CSS_SELECTOR, '.accord-box .accord-bar')
        accords = [f"{elem.text} ({elem.get_attribute('style').split('width: ')[-1].split('%')[0].strip()}%)" for elem in accord_elements]
        accords_string = ', '.join(accords)
        print("Main accords: ", accords_string)
        data['Accords'].append(accords_string)
        
        # 전체 설명
        description_element = driver.find_element(By.XPATH, '//div[@itemprop="description"]/p')
        print("전체 설명:", description_element.text)
        data['Description'].append(description_element.text)
        
        # 추가 설명 (Detail)
        try:
            detail_description = driver.find_element(By.CSS_SELECTOR, '.fragrantica-blockquote')
            paragraphs = detail_description.find_elements(By.TAG_NAME, 'p')
            additional_info = '\n'.join([p.text.strip() for p in paragraphs if p.text.strip()])
        except:
            additional_info = "Additional info not found"
            
        print("추가 설명:", additional_info)
        data['Additional_Info'].append(additional_info)
        
        # 피라미드 노트
        def extract_notes(section_name):
            try:
                section_header = driver.find_element(By.XPATH, f'//h4/b[text()="{section_name}"]/parent::h4/following-sibling::div')
                note_divs = section_header.find_elements(By.XPATH, './/div[contains(@style, "margin: 0.2rem")]')
                notes = [div.text.split('\n')[-1] for div in note_divs if div.text.strip()]
                notes_string = ', '.join(notes)
                return notes_string
            except Exception as e:
                print(f"{section_name} section not found")
                return ""
        
        data['Top_Notes'].append(extract_notes("Top Notes"))
        data['Middle_Notes'].append(extract_notes("Middle Notes"))
        data['Base_Notes'].append(extract_notes("Base Notes"))
        
        # 선호도와 계절감
        love, like, ok, dislike, hate, winter, spring, summer, fall, day, night = [0] * 11  # 초기값 설정
        preference_and_season_elements = driver.find_elements(By.XPATH, "//div[@class='cell small-6']/..//div[@class='voting-small-chart-size']/div/div")
        
        for i, element in enumerate(preference_and_season_elements):
            style_attribute = element.get_attribute("style")
            width_value = re.search(r'width:\s*([\d.]+%)', style_attribute).group(1)
            print(width_value)
            
            if i == 0:
                love = float(width_value[:-1])
            elif i == 1:
                like = float(width_value[:-1])
            elif i == 2:
                ok = float(width_value[:-1])
            elif i == 3:
                dislike = float(width_value[:-1])
            elif i == 4:
                hate = float(width_value[:-1])
            elif i == 5:
                winter = float(width_value[:-1])
            elif i == 6:
                spring = float(width_value[:-1])
            elif i == 7:
                summer = float(width_value[:-1])
            elif i == 8:
                fall = float(width_value[:-1])
            elif i == 9:
                day = float(width_value[:-1])
            elif i == 10:
                night = float(width_value[:-1])
                   
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
        
        # 장점과 단점
        print("---장점, 단점---")
        props, cons = [], []
        props_and_cons_elements = driver.find_elements(By.XPATH, "//div[@class='cell small-12 medium-6']/div[@class='cell small-12']/span")
        for i, element in enumerate(props_and_cons_elements):
            print(element)
            if i < 8:
                cons.append(element.text)
            else:
                props.append(element.text)
        data['cons'].append(', '.join(cons))
        data['props'].append(', '.join(props))
        
        # 지속력과 잔향
        print("---지속력, 잔향---")
        longevity_veryweak, longevity_weak, longevity_moderate, longevity_longlasting, longevity_eternal = [0]*5
        sillage_intimate, sillage_moderate, sillage_strong, sillage_enormous = [0]*4
        longevity_and_sillage_elements = driver.find_elements(By.XPATH, "//div[@class='cell small-12 medium-6']//progress")
    
        for i, element in enumerate(longevity_and_sillage_elements):
            value = float(element.get_attribute("value"))
            max_value = float(element.get_attribute("max"))
    
            if max_value != 0:
                result = (value / max_value) * 100
                
                if i == 0:
                    longevity_veryweak = result
                elif i == 1:
                    longevity_weak = result
                elif i == 2:
                    longevity_moderate = result
                elif i == 3:
                    longevity_longlasting = result
                elif i == 4:
                    longevity_eternal = result
                elif i == 5:
                    sillage_intimate = result
                elif i == 6:
                    sillage_moderate = result
                elif i == 7:
                    sillage_strong = result
                elif i == 8:
                    sillage_enormous = result
                
        data['longevity_veryweak'].append(longevity_veryweak)
        data['longevity_weak'].append(longevity_weak)
        data['longevity_moderate'].append(longevity_moderate)
        data['longevity_longlasting'].append(longevity_longlasting)
        data['longevity_eternal'].append(longevity_eternal)
        data['sillage_intimate'].append(sillage_intimate)
        data['sillage_moderate'].append(sillage_moderate)
        data['sillage_strong'].append(sillage_strong)
        data['sillage_enormous'].append(sillage_enormous)

        driver.quit()
        
        # Chrome 프로세스 종료 및 폴더 삭제
        def kill_process(name):
            for proc in psutil.process_iter():
                if proc.name() == name:
                    proc.kill()

        kill_process("chrome.exe")
        
        # 파일 잠금을 해제하고 폴더를 삭제하는 함수
        def delete_folder(folder):
            for root, dirs, files in os.walk(folder):
                for file in files:
                    file_path = os.path.join(root, file)
                    try:
                        os.unlink(file_path)
                    except PermissionError:
                        kill_process("chrome.exe")
                        os.unlink(file_path)
            shutil.rmtree(folder, ignore_errors=True)

        try:
            delete_folder(r"c:\chrometemp")
        except PermissionError as e:
            print(f"폴더 삭제 중 오류 발생: {e}")
        
    except Exception as e:
        print(f"에러 발생: {e}")
        driver.quit()


df = pd.DataFrame(data)
output_csv_file_path = "output_data.csv"
df.to_csv(output_csv_file_path, index=False, encoding='utf-8')