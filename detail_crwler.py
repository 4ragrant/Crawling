import time
import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import chromedriver_autoinstaller
import subprocess
import pandas as pd
import shutil

# 디버깅 모드에서 Chrome 시작
subprocess.Popen(r'C:\Program Files\Google\Chrome\Application\chrome.exe --remote-debugging-port=9222 --user-data-dir="C:\chrometemp"')
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

csv_file_path = "2024.csv"
urls = pd.read_csv(csv_file_path)["URL"].tolist()
# review_urls = [url + "#all-reviews" for url in urls]

# DataFrame에 저장할 데이터 리스트
data = {'Product': [], 'Gender' : [], 'Accords' : [], 'Description' : [], 'Additional_Info' : [],
         'Top_Notes': [], 'Middle_Notes': [], 'Base_Notes': [], 'love': [], 'like': [], 'ok': [], 'dislike': [], 'hate': [],
         'winter': [], 'spring': [], 'summer': [], 'fall': [], 'day': [], 'night': [],
         'cons': [], 'props': [], 'longevity_veryweak': [], 'longevity_weak': [], 'longevity_moderate': [], 'longevity_longlasting': [], 'longevity_eternal': [],
         'sillage_intimate': [], 'sillage_moderate': [], 'sillage_strong': [], 'sillage_enormous': []}

for url in urls:
    try:    
        driver.get(url)
        time.sleep(2)
        
        # 향수 이름, 성별
        print("---이름, 성별---")
        elements = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'h1[itemprop="name"]')))
        print(elements.text)
            
        product = elements.text.strip()
            
        # 데이터 정제 : 향수 이름 / 성별
        split_index = product.rfind('for')
        product = product[:split_index].strip()
            
        gender = ''
        if split_index != -1:
            gender = elements.text[split_index + 4:].strip()
            
        # 향수 이름, 성별 데이터 -> 리스트에 추가
        data['Product'].append(product)
        data['Gender'].append(gender)
        
        # Main Accords
        print("---Main accords---")
            
        accord_elements = driver.find_elements(By.CSS_SELECTOR, '.accord-box .accord-bar')
        accords = [f"{elem.text} ({elem.get_attribute('style').split('width: ')[-1].split('%')[0].strip()}%)" for elem in accord_elements]
        accords_string = ', '.join(accords)
        print(accords_string)
        data['Accords'].append(accords_string)
        
        # 전체 설명
        print("---전체 설명---")
        description_element = driver.find_element(By.XPATH, '//div[@itemprop="description"]/p')
        print(description_element.text)
        data['Description'].append(description_element.text)
            
        # 추가 설명 (Detail)
        print("---추가 설명---")
        try:
            detail_description = driver.find_element(By.CSS_SELECTOR, '.fragrantica-blockquote')
            paragraphs = detail_description.find_elements(By.TAG_NAME, 'p')
            additional_info = '\n'.join([p.text.strip() for p in paragraphs if p.text.strip()])
        except:
            additional_info = "Additional info not found"
            
        print(additional_info)
        data['Additional_Info'].append(additional_info)
        
        # 피라미드
        print("---피라미드---")
            
        def extract_notes(section_name):
            try:
                section_header = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, f'//h4/b[text()="{section_name}"]/parent::h4/following-sibling::div'))
                )
                note_divs = section_header.find_elements(By.XPATH, './/div[contains(@style, "margin: 0.2rem")]')
                notes = [div.text.split('\n')[-1] for div in note_divs if div.text.strip()]
                notes_string = ', '.join(notes)
                return notes_string
            except Exception as e:
                print(f"{section_name} section not found")
                return ""
        
        # Top notes
        print("---Top note---")
        top_notes_string = extract_notes("Top Notes")
        print(top_notes_string)
        data['Top_Notes'].append(top_notes_string)       
        # Middle notes
        print("---Middle note---")
        middle_notes_string = extract_notes("Middle Notes")
        print(middle_notes_string)
        data['Middle_Notes'].append(middle_notes_string)  
        # Base notes
        print("---Base note---")
        base_notes_string = extract_notes("Base Notes")
        print(base_notes_string)
        data['Base_Notes'].append(base_notes_string)        
                    
        # 선호도(5), 계절감(6): 총 11건
        print("---선호도, 계절감---")
        love, like, ok, dislike, hate, winter, spring, summer, fall, day, night = [0] * 11  # 초기값 설정
        preference_and_season_elements = driver.find_elements(By.XPATH, "//div[@class='cell small-6']/..//div[@class='voting-small-chart-size']/div/div")
        
        for i, element in preference_and_season_elements:
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
        
        # 장점(8), 단점(8): 총 16건
        print("---장점, 단점---")
        props, cons = [], []
        props_and_cons_elements = driver.find_elements(By.XPATH, "//div[@class='cell small-12 medium-6']/div[@class='cell small-12']/span")
        for i, element in props_and_cons_elements:
            if i<8:
                cons.append(element.text)
            else:
                props.append(element.text)
        data['cons'].append(', '.join(cons))
        data['props'].append(', '.join(props))
        
        # 지속력(5), 잔향(4)
        print("---지속력, 잔향---")
        longevity_and_sillage_elements = driver.find_elements(By.XPATH, "//div[@class='cell small-12 medium-6']//progress")
        longevity_values = [0] * 5
        sillage_values = [0] * 4
        
        # 지속력
        for i, element in enumerate(longevity_and_sillage_elements[:5]):
            value = float(element.get_attribute("value"))
            max_value = float(element.get_attribute("max"))
            # 비율 구해서 퍼센트로 변환
            if max_value != 0:
                result = (value / max_value) * 100
                longevity_values[i] = result
                
        # 잔향
        for i, element in enumerate(longevity_and_sillage_elements[5:]):
            value = float(element.get_attribute("value"))
            max_value = float(element.get_attribute("max"))
            # 비율 구해서 퍼센트로 변환
            if max_value != 0:
                result = (value / max_value) * 100
                sillage_values[i] = result
    
        data.update({
            'longevity_veryweak': longevity_values[0],
            'longevity_weak': longevity_values[1],
            'longevity_moderate': longevity_values[2],
            'longevity_longlasting': longevity_values[3],
            'longevity_eternal': longevity_values[4],
            'sillage_intimate': sillage_values[0],
            'sillage_moderate': sillage_values[1],
            'sillage_strong': sillage_values[2],
            'sillage_enormous': sillage_values[3]
        })
        # 리뷰: 210건
        # review_elements = driver.find_elements(By.XPATH, "//div[@itemprop='reviewBody']/p")
        # print(len(review_elements))
              
    except Exception as e:
        print(f"에러 발생: {e}")
        
df = pd.DataFrame(data)
output_csv_file_path = "output_data.csv"
df.to_csv(output_csv_file_path, index=False, encoding='utf-8')                

driver.quit()