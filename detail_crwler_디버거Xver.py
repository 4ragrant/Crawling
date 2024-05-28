import time
import re
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By

PAUSE_TIME = 2
CLICK_COUNT = 0

driverPath = "D:\chromedriver-win64\chromedriver.exe"

csv_file_path = "2024.csv"
urls = pd.read_csv(csv_file_path)["URL"].tolist()
review_urls = [url + "#all-reviews" for url in urls]

data = {'Product': [], 'Gender': [], 'Accords': [], 'Description': [], 'AdditionalInfo': [],
        'TopNotes': [], 'MiddleNotes': [], 'BaseNotes': [], 'love': [], 'like': [], 'ok': [], 'dislike': [], 'hate': [],
        'winter': [], 'spring': [], 'summer': [], 'fall': [], 'day': [], 'night': [],
        'Cons': [], 'Props': [], 'longevity_veryweak': [], 'longevity_weak': [], 'longevity_moderate': [], 'longevity_longlasting': [], 'longevity_eternal': [],
        'sillage_intimate': [], 'sillage_moderate': [], 'sillage_strong': [], 'sillage_enormous': [], 'Reviews': []}

for url in review_urls:
    try:
        
        driver = webdriver.Chrome()
        driver.get(url)
        time.sleep(2)
        
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
        print("Main accords: ", accords_string)
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
        top_notes = driver.find_elements(By.XPATH, "//*[@id='pyramid']/div[1]/div/div[2]/div[3]/div")
        middle_notes = driver.find_elements(By.XPATH, "//*[@id='pyramid']/div[1]/div/div[2]/div[4]/div")
        base_notes = driver.find_elements(By.XPATH, "//*[@id='pyramid']/div[1]/div/div[2]/div[5]/div")
        
        for element in top_notes:
            text = element.text.replace('\n', ', ').strip()
            print("Top notes:", text)
            top.append(text)

        for element in middle_notes:
            text = element.text.replace('\n', ', ').strip()
            print("Middle notes:", text)
            middle.append(text)

        for element in base_notes:
            text = element.text.replace('\n', ', ').strip()
            print("Base notes:", text)
            base.append(text)
            
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
        
        # 장점과 단점
        print("---Props and Cons---")
        props, cons = [], []
        props_and_cons_elements = driver.find_elements(By.XPATH, "//div[@class='cell small-12 medium-6']/div[@class='cell small-12']/span")
        
        if props_and_cons_elements:
            for i, element in enumerate(props_and_cons_elements):
                print(element.text)
                if i < 8:
                    cons.append(element.text)
                else:
                    props.append(element.text)
        else:
            print("Not Found")
            cons.append("Not Found")
            props.append("Not Found")     
            
        data['Cons'].append(', '.join(cons))
        data['Props'].append(', '.join(props))
        
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
                    print("longevity_veryweak:", result, "%")
                    longevity_veryweak = result
                elif i == 1:
                    print("longevity_weak:", result, "%")
                    longevity_weak = result
                elif i == 2:
                    print("longevity_moderate:", result, "%")
                    longevity_moderate = result
                elif i == 3:
                    print("longevity_longlasting:", result, "%")
                    longevity_longlasting = result
                elif i == 4:
                    print("longevity_eternal:", result, "%")
                    longevity_eternal = result
                elif i == 5:
                    print("sillage_intimate:", result, "%")
                    sillage_intimate = result
                elif i == 6:
                    print("sillage_moderate:", result, "%")
                    sillage_moderate = result
                elif i == 7:
                    print("sillage_strong:", result, "%")
                    sillage_strong = result
                elif i == 8:
                    print("sillage_enormous:", result, "%")
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
        
        # 리뷰: 210건
        print("---Reivews---")
        reviews = []
        review_elements = driver.find_elements(By.XPATH, "//div[@itemprop='reviewBody']/p")
        if review_elements:
            print(len(review_elements), "건")
            for element in review_elements:
                reviews.append(element.text)
        else:
            print("Not Found")
            reviews.append("Not Found")
        data['Reviews'].append(', '.join(reviews))
        
        # 드라이버 종료
        driver.quit()
        
    except Exception as e:
        print(f"에러 발생: {e}")

df = pd.DataFrame(data)
output_csv_file_path = "2024_output_data.csv"
df.to_csv(output_csv_file_path, index=False, encoding='utf-8')