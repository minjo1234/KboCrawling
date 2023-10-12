from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException

import time
import json
import mysql.connector
from datetime import datetime
from bs4 import BeautifulSoup
import requests

options = webdriver.ChromeOptions()
options.add_experimental_option("excludeSwitches", ["enable-logging"])
driver = webdriver.Chrome(options=options)

url = 'https://m.sports.naver.com/game/20231011OBLT02023/preview'
driver.get(url)
time.sleep(2)


TodayLeftGameInfo = driver.find_element(
    By.XPATH, '//*[@id="content"]/div/div/section[1]/div[2]/div[2]/div').text
print(TodayLeftGameInfo)

TodayRightGameInfo = driver.find_element(
    By.XPATH, '//*[@id="content"]/div/div/section[1]/div[2]/div[3]/div').text

print(TodayRightGameInfo)

# 이미지 요소 식별
# 이미지 요소의 XPath 식별
LeftImage_xpath = '//*[@id="content"]/div/div/section[1]/div[2]/div[2]/div/div[1]/img'

# 이미지의 src 속성 가져오기
LeftImage_element = driver.find_element(By.XPATH, LeftImage_xpath)
LeftImage_src = LeftImage_element.get_attribute('src')
# 이미지의 너비와 높이 가져오기
# 결과 출력
RightImage_path = '//*[@id="content"]/div/div/section[1]/div[2]/div[3]/div/div[1]/img'

# 이미지의 src 속성 가져오기
RightImage_element = driver.find_element(By.XPATH, RightImage_path)
Rightimage_src = RightImage_element.get_attribute('src')
# 결과 출력
print(f'이미지의 src 속성:{LeftImage_src}')
print(f'이미지의 src 속성:{Rightimage_src}')


driver.quit()
