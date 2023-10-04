from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
import time
import json
import mysql.connector
from selenium.common.exceptions import NoSuchElementException
import re

options = webdriver.ChromeOptions()
options.add_experimental_option("excludeSwitches", ["enable-logging"])
driver = webdriver.Chrome(options=options)

url = 'https://www.koreabaseball.com/Player/Search.aspx'

driver.get(url)
TeamList = ['LG', 'KT', 'NC', 'OB', 'SK', 'HT', 'LT', 'HH', 'SS', 'WO']
PositionList = ['1', '2', '3,4,5,6', '7,8,9']
players_href = []
i = 0
for p in range(len(TeamList)):

    # 팀 선택하는 select 태그 선택
    team_select = Select(driver.find_element(
        By.ID, 'cphContents_cphContents_cphContents_ddlTeam'))

    # 'LG' 팀 선택

    team_select.select_by_value(TeamList[p])

    driver.implicitly_wait(10)
    for t in range(len(PositionList)):
        position_select = Select(driver.find_element(
            By.ID, 'cphContents_cphContents_cphContents_ddlPosition'))
        position_select.select_by_value(PositionList[t])
        driver.implicitly_wait(10)

        for k in range(1, 4):
            try:
                button_select = driver.find_element(
                    By.ID, f'cphContents_cphContents_cphContents_ucPager_btnNo{k}')
                button_select.click()

            except NoSuchElementException:
                pass
            time.sleep(2)
            players = driver.find_elements(
                By.XPATH, '//*[@id="cphContents_cphContents_cphContents_udpRecord"]/div[2]/table/tbody/tr/td[2]/a')

            for player in players:
                player = player.get_attribute('href')
                href = re.search(r'playerId=(\d+)', player)
                if href:
                    player_href = href.group(1)
                    if (player_href in players_href):
                        continue
                    players_href.append(player_href)


with open("KboPlayers_href.json", "w", encoding="utf-8") as json_file:
    json.dump(players_href, json_file, ensure_ascii=False, indent=4)
# player_detail = player_detail.get_attribute('href')s

# print(player_detail)

# '김기연' 텍스트를 포함하는 요소에서 href 속성 가져오기
