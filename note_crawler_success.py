# -*- coding: utf-8 -*-
"""
Created on Tue May 28 14:15:44 2024

@author: DS
"""

import time
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

# Loop through all notes_links files
for i in range(1, 17):
    file_name = f'notes_links_{i}.txt'
    data = {'note': [], 'other_group': [], 'group': []}
    
    with open(file_name, 'r') as f:
        note_links = f.read().splitlines()

    for link in note_links:
        try:
            # Ensure Chrome processes are killed and cleanup temp directory
            kill_process("chrome.exe")
            delete_folder(r"c:\chrometemp")
            
            # Check if the port is in use
            if is_port_in_use(9223):
                print("포트 9223이 사용 중입니다. 다른 포트를 사용하거나 사용 중인 프로세스를 종료하세요.")
                continue
            
            # Start Chrome with remote debugging
            subprocess.Popen(r'C:\Program Files\Google\Chrome\Application\chrome.exe --remote-debugging-port=9223 --user-data-dir="C:\chrometemp"')

            # Setup Chrome options for remote debugging
            options = Options()
            options.add_experimental_option("debuggerAddress", "127.0.0.1:9223")

            # Install and setup ChromeDriver
            chrome_ver = chromedriver_autoinstaller.get_chrome_version().split('.')[0]
            chromedriver_autoinstaller.install(True)
            service = Service(f'./{chrome_ver}/chromedriver.exe')

            driver = None
            for _ in range(3):  # 최대 3번 재시도
                try:
                    driver = webdriver.Chrome(service=service, options=options)
                    driver.implicitly_wait(10)
                    driver.get(link)
                    break
                except Exception as e:
                    print(f"드라이버 초기화 실패, 재시도 중... ({e})")
                    if driver:
                        driver.quit()
                    time.sleep(5)
            
            if driver is None:
                raise Exception("Chrome 드라이버를 초기화할 수 없습니다.")

            # Extract data with exception handling
            try:
                note_name_element = driver.find_element(By.CSS_SELECTOR, 'div.cell.text-center h1')
                note_name = note_name_element.text
            except:
                note_name = 'N/A'
            print(note_name)
            data['note'].append(note_name)
            print("note 데이터 프레임 추가 완료")

            other_group_elements = driver.find_elements(By.CSS_SELECTOR, 'div.cell.text-center p')
            if other_group_elements:
                other_group = other_group_elements[0].text.replace('\n', ' ')
            else:
                other_group = 'N/A'
            print(other_group)
            data['other_group'].append(other_group)
            print("other_group 데이터 프레임 추가 완료")

            try:
                group_element = driver.find_element(By.CSS_SELECTOR, 'div.cell.text-center h3')
                group = group_element.text
            except:
                group = 'N/A'
            print(group)
            data['group'].append(group)
            print("group 데이터 프레임 추가 완료")

            driver.quit()

            # Cleanup Chrome processes and temp folder
            kill_process("chrome.exe")
            delete_folder(r"c:\chrometemp")

        except Exception as e:
            print("페이지 가져오기 실패")
            print(e)
            if driver:
                driver.quit()

    # 디버깅: 수집된 데이터를 출력하여 확인
    print(f"수집된 데이터 ({file_name}):", data)

    # 데이터 프레임 생성 및 CSV 저장
    df = pd.DataFrame(data)
    output_csv_file_path = f"note_data_{i}.csv"

    try:
        df.to_csv(output_csv_file_path, index=False, encoding='utf-8')
        print(f"데이터가 CSV 파일에 저장되었습니다: {output_csv_file_path}")
    except Exception as e:
        print(f"CSV 파일 저장 중 오류 발생: {e}")

    # 디버깅: 데이터 프레임을 출력하여 확인
    print(f"데이터 프레임 ({file_name}):\n", df)
