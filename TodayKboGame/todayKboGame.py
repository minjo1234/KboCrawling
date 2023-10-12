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
# tb , tb2
# tb와 tb2로 날짜가 하루씩 변경되면 생긴다 .
url = 'https://sports.news.naver.com/kbaseball/schedule/index.nhn'
driver.get(url)
todayGameInfoList = []
a_elements = []
time.sleep(2


           )
try:
    todaykboGame = driver.find_element(By.CSS_SELECTOR, 'div.sch_tb2.selected')
except NoSuchElementException:
    todaykboGame = driver.find_element(By.CSS_SELECTOR, 'div.sch_tb.selected')
today = todaykboGame.find_element(By.CSS_SELECTOR, 'span.td_date')
todayLeftTeams = todaykboGame.find_elements(By.CSS_SELECTOR, 'span.team_lft')
todayRightTeams = todaykboGame.find_elements(By.CSS_SELECTOR, 'span.team_rgt')
todayTeam = []
teamLink = []
for todayLeftTeam in todayLeftTeams:
    todayTeam.append(todayLeftTeam.text)

for todayRightTeam in todayRightTeams:
    todayTeam.append(todayRightTeam.text)
    # 각 tr 태그에서 td 태그를 가져옵니다.


date_parts = today.text.split()
month, day = map(int, date_parts[0].split('.'))

# 형식을 변경하고 출력합니다.
formatted_date = f"{month:02d}{day:02d}"

for i in range((len(todayTeam) // 2)):
    leftTeam = todayTeam[(i)]
    rightTeam = todayTeam[(i + (len(todayTeam) // 2))]

    if (leftTeam == '한화'):
        teamLink.append('HH')
    elif (leftTeam == 'KT'):
        teamLink.append('KT')
    elif (leftTeam == '롯데'):
        teamLink.append('LT')
    elif (leftTeam == '키움'):
        teamLink.append('WO')
    elif (leftTeam == 'SSG'):
        teamLink.append('SK')
    elif (leftTeam == 'LG'):
        teamLink.append('LG')
    elif (leftTeam == '삼성'):
        teamLink.append('SS')
    elif (leftTeam == 'KIA'):
        teamLink.append('HT')
    elif (leftTeam == 'NC'):
        teamLink.append('NC')
    else:
        teamLink.append('OB')

    if (rightTeam == '한화'):
        teamLink.append('HH')
    elif (rightTeam == 'KT'):
        teamLink.append('KT')
    elif (rightTeam == '롯데'):
        teamLink.append('LT')
    elif (rightTeam == '키움'):
        teamLink.append('WO')
    elif (rightTeam == 'SSG'):
        teamLink.append('SK')
    elif (rightTeam == 'LG'):
        teamLink.append('LG')
    elif (rightTeam == '삼성'):
        teamLink.append('SS')
    elif (rightTeam == 'KIA'):
        teamLink.append('HT')
    elif (todayTeam[i] == 'NC'):
        teamLink.append('NC')
    else:
        teamLink.append('OB')

for i in range(len(teamLink) // 2):
    href = formatted_date + teamLink[i * 2] + teamLink[(i*2) + 1]
    url = f'https://m.sports.naver.com/game/2023{href}02023/preview'
    driver.get(url)
    time.sleep(2)

    leftTeam = []
    rightTeam = []
    leftVestPitcher = []
    rightVestPitcher = []
    leftVestHitter = []
    rightVestHitter = []
    leftTeamLineUp = []
    rightTeamLineUp = []

    leftTemaName = driver.find_element(
        By.XPATH, '//*[@id="content"]/div/div/section[2]/div[2]/div/div[1]/div[1]/div[1]/div[1]').text
    rightTeamName = driver.find_element(
        By.XPATH, '//*[@id="content"]/div/div/section[2]/div[2]/div/div[1]/div[1]/div[3]/div[1]').text

    TeamInfo = driver.find_elements(
        By.XPATH, '//*[@id="content"]/div/div/section[2]/div[2]/div/div[1]/div[1]/div')

    leftTeam.append(TeamInfo[0].text)
    rightTeam.append(TeamInfo[2].text)

    leftRecord = driver.find_elements(
        By.XPATH, '//*[@id="content"]/div/div/section[2]/div[2]/div/div[1]/div[2]/table/tbody/tr/td[1]/div')
    rightRecord = driver.find_elements(
        By.XPATH, '//*[@id="content"]/div/div/section[2]/div[2]/div/div[1]/div[2]/table/tbody/tr/td[2]/div')

    for i in range(len(leftRecord)):
        leftTeam.append(leftRecord[i].text)
        rightTeam.append(rightRecord[i].text)

    leftPitcherName = driver.find_element(
        By.XPATH, '//*[@id="content"]/div/div/section[2]/div[2]/div/div[2]/div[1]/a/div[2]')
    leftPitherInfo = driver.find_elements(
        By.XPATH, '//*[@id="content"]/div/div/section[2]/div[2]/div/div[3]/table/tbody/tr/td[1]')
    rightPitcherName = driver.find_element(
        By.XPATH, '//*[@id="content"]/div/div/section[2]/div[2]/div/div[2]/div[3]/a/div[2]')
    rightPitcherInfo = driver.find_elements(
        By.XPATH, '//*[@id="content"]/div/div/section[2]/div[2]/div/div[3]/table/tbody/tr/td[2]')

    leftVestPitcher.append(leftPitcherName.text)
    rightVestPitcher.append(rightPitcherName.text)

    for i in range(len(leftPitherInfo)):
        leftVestPitcher.append(leftPitherInfo[i].text)
        rightVestPitcher.append(rightPitcherInfo[i].text)

    leftHitterName = driver.find_element(
        By.XPATH, '//*[@id="content"]/div/div/section[2]/div[2]/div/div[5]/div[1]/a/div[2]')
    rightHitterName = driver.find_element(
        By.XPATH, '//*[@id="content"]/div/div/section[2]/div[2]/div/div[5]/div[3]/a/div[2]')
    leftHitterInfo = driver.find_elements(
        By.XPATH, '//*[@id="content"]/div/div/section[2]/div[2]/div/div[6]/table/tbody//td[1]')
    rightHitterInfo = driver.find_elements(
        By.XPATH, '//*[@id="content"]/div/div/section[2]/div[2]/div/div[6]/table/tbody/tr/td[2]'
    )

    leftVestHitter.append(leftHitterName.text)
    rightVestHitter.append(rightHitterName.text)

    for i in range(len(leftHitterInfo)):
        leftVestHitter.append(leftHitterInfo[i].text)
        rightVestHitter.append(rightHitterInfo[i].text)

    # 버튼이 나타날 때까지 대기
    button = driver.find_element(
        By.XPATH, '//*[@id="content"]/div/div/section[2]/div[1]/ul/li[2]/button')
    driver.execute_script("arguments[0].click();", button)

    time.sleep(2)
    leftTeamLineUpElements = driver.find_elements(
        By.XPATH, ' //*[@id="content"]/div/div/section[2]/div[2]/div/div/div[1]/div[1]/ol/li')
    rightTeamLineUpElements = driver.find_elements(
        By.XPATH, '//*[@id="content"]/div/div/section[2]/div[2]/div/div/div[1]/div[2]/ol/li')

    for i in range(len(leftTeamLineUpElements)):
        leftTeamLineUp.append(leftTeamLineUpElements[i].text)
        rightTeamLineUp.append(rightTeamLineUpElements[i].text)

    GameStatus = driver.find_element(
        By.XPATH, '//*[@id="content"]/div/div/section[1]/div[2]/div[1]/p[1]').text
    if (GameStatus == '경기전'):
        RemainingStartTime = driver.find_element(
            By.XPATH, '//*[@id="webplayerWrap"]/div/div/div[3]/div/div').text
        GameLeftStartingPlayer = driver.find_element(
            By.XPATH, '//*[@id="content"]/div/div/section[1]/div[2]/div[2]/div').text
        GameRightStartingPlayer = driver.find_element(
            By.XPATH, '//*[@id="content"]/div/div/section[1]/div[2]/div[3]/div').text

        TodayGameInfo = {
            "RemainingStartTime": RemainingStartTime,
            "leftTeamName": leftTemaName,
            "leftTeam": leftTeam,
            "leftVestHitter": leftVestHitter,
            "leftVestPitcher": leftVestPitcher,
            "leftTeamLineUp": leftTeamLineUp,
            "GameLeftStartingPlayer": GameLeftStartingPlayer,
            "rightTeamName": rightTeamName,
            "rightTeam": rightTeam,
            "rightVestHitter": rightVestHitter,
            "rightVestPitcher": rightVestPitcher,
            "rightTeamLineUp": rightTeamLineUp,
            "GameRightStartingPlayer ": GameRightStartingPlayer
        }
    else:
        GameLeftStartingPlayer = driver.find_element(
            By.XPATH, '//*[@id="content"]/div/div/section[1]/div[2]/div[2]/div[1]').text
        LeftTeamScore = driver.find_element(
            By.XPATH, '//*[@id="content"]/div/div/section[1]/div[2]/div[2]/div[2]').text
        GameRightStartingPlayer = driver.find_element(
            By.XPATH, '//*[@id="content"]/div/div/section[1]/div[2]/div[3]/div[1]').text
        RightGameScore = driver.find_element(
            By.XPATH, '//*[@id="content"]/div/div/section[1]/div[2]/div[3]/div[2]').text
        Full_Match_Details = driver.find_element(
            By.XPATH, '//*[@id="content"]/div/div/section[1]/div[3]/div').text

        TodayGameInfo = {
            "GameLeftStartingPlayer": GameLeftStartingPlayer,
            "GameRightStartingPlayer": GameRightStartingPlayer,
            "LeftTeamScore": LeftTeamScore,
            "RightGameScore": RightGameScore,
            "Full_Match_Details": Full_Match_Details,
            "leftTeamName": leftTemaName,
            "leftTeam": leftTeam,
            "leftVestHitter": leftVestHitter,
            "leftVestPitcher": leftVestPitcher,
            "leftTeamLineUp": leftTeamLineUp,
            "rightTeamName": rightTeamName,
            "rightTeam": rightTeam,
            "rightVestHitter": rightVestHitter,
            "rightVestPitcher": rightVestPitcher,
            "rightTeamLineUp": rightTeamLineUp,
        }

    todayGameInfoList.append(TodayGameInfo)

print(todayGameInfoList)
with open("TodayGameInfo.json", "w", encoding="utf-8") as json_file:
    json.dump(todayGameInfoList, json_file, ensure_ascii=False, indent=4)
