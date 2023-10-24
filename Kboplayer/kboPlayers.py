from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
import time
import json
import mysql.connector

options = webdriver.ChromeOptions()
options.add_experimental_option("excludeSwitches", ["enable-logging"])
driver = webdriver.Chrome(options=options)

url = 'https://www.koreabaseball.com/Player/Search.aspx'
driver.get(url)

TeamList = ['LG', 'KT', 'NC', 'OB', 'SK', 'HT', 'LT', 'HH', 'SS', 'WO']
player_list = []

for p in range(0, 10):
    # 팀 선택하는 select 태그 선택
    team_select = Select(driver.find_element(
        By.ID, 'cphContents_cphContents_cphContents_ddlTeam'))
    team_select.select_by_value(TeamList[p])
    time.sleep(6)
    print(TeamList[p])

    for i in range(1, 6):
        button_select = driver.find_element(
            By.ID, f'cphContents_cphContents_cphContents_ucPager_btnNo{i}')
        button_select.click()
        time.sleep(3)

        tr_elements = driver.find_elements(
            By.XPATH, '//*[@id="cphContents_cphContents_cphContents_udpRecord"]/div[2]/table/tbody/tr')
        print(len(tr_elements))

        for k in range(len(tr_elements)):
            td_elements = tr_elements[k].find_elements(By.TAG_NAME, 'td')
            player_Num = td_elements[0].text if td_elements and len(
                td_elements) > 1 else ""
            player_Name = td_elements[1].text if td_elements and len(
                td_elements) > 2 else ""
            player_Team = td_elements[2].text if td_elements and len(
                td_elements) > 3 else ""
            player_Position = td_elements[3].text if td_elements and len(
                td_elements) > 4 else ""
            player_Birth = td_elements[4].text if td_elements and len(
                td_elements) > 5 else ""
            player_Physical = td_elements[5].text if td_elements and len(
                td_elements) > 6 else ""

            player_dict = {
                'player_Num': player_Num,
                'player_Name': player_Name,
                'player_Team': player_Team,
                'player_Position': player_Position,
                'player_Birth': player_Birth,
                'player_Physical': player_Physical,
            }
            player_list.append(player_dict)

# JSON 파일에 데이터 저장
# with open("player_data.json", "w", encoding="utf-8") as json_file:
#     json.dump(player_list, json_file, ensure_ascii=False, indent=4)

# MySQL 데이터베이스 설정
db_config = {
    "host": "localhost",
    "port": 3306,
    "user": "root",
    "password": "1234",
    "database": "sportinfo"
}

# db_config = {
#     "host": "localhost",
#     "port": 3306,
#     "user": "root",
#     "password": "1234",
#     "database": "lee"
# }

# 데이터베이스 연결 생성
db = mysql.connector.connect(**db_config)

try:
    # 커서 생성
    cursor = db.cursor()

    # player_data 테이블 생성 (playerId 컬럼은 AUTO_INCREMENT로 설정)
    create_table_sql = """
    CREATE TABLE IF NOT EXISTS kbo_Players (
        player_id BIGINT AUTO_INCREMENT PRIMARY KEY,
        player_num VARCHAR(255),
        player_name VARCHAR(255),
        player_team VARCHAR(255),
        player_position VARCHAR(255),
        player_birth DATE,
        player_physical VARCHAR(255)
    );
    """

    cursor.execute(create_table_sql)
    db.commit()

    # JSON 데이터를 MySQL 데이터베이스에 삽입
    for player in player_list:
        sql = "INSERT INTO kbo_Players (player_num, player_name, player_team, player_position, player_birth, player_physical) VALUES (%s, %s, %s, %s, %s, %s)"
        val = (player["player_Num"],
               player["player_Name"],
               player["player_Team"],
               player["player_Position"],
               player["player_Birth"],
               player["player_Physical"])
        cursor.execute(sql, val)
        db.commit()

except mysql.connector.Error as err:
    print(f"Error: {err}")

finally:
    # 커넥션 닫기
    if db.is_connected():
        cursor.close()
        db.close()

# 브라우저 닫기
driver.quit()
