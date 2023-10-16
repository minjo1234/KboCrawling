from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
import time
import json
import mysql.connector

options = webdriver.ChromeOptions()
options.add_experimental_option("excludeSwitches", ["enable-logging"])
driver = webdriver.Chrome(options=options)
try:
    url = 'https://www.kleague.com/record/team.do'
    driver.get(url)
    time.sleep(2)
    finalGroupA = tr_elements = driver.find_elements(
        By.XPATH, '//*[@id="ts1"]/tbody/tr/')
    finalGroupB = tr_elements = driver.find_elements(
        By.XPATH, '//*[@id="ts2"]/tbody/tr')
    print(len(finalGroupA))

    # MySQL 데이터베이스 설정
    db_config = {
        "host": "localhost",
        "port": 3306,
        "user": "root",
        "password": "Wlgns3350@",
        "database": "SportInfo"
    }

    # 데이터베이스 연결 생성
    db = mysql.connector.connect(**db_config)

    try:
        # 커서 생성
        cursor = db.cursor()

        # player_data 테이블 생성 (playerId 컬럼은 AUTO_INCREMENT로 설정)
        create_table_sql = """
        CREATE TABLE IF NOT EXISTS kboPlayers (
            K_TeamId BIGINT AUTO_INCREMENT PRIMARY KEY,
            K_Team_Name VARCHAR(20) NOT NULL,
            K_Team_Game VARCHAR(20) NOT NULL,
            K_Team_Win VARCHAR(20) NOT NULL,
            K_Team_Drawn VARCHAR(20) NOT NULL,
            k_Team_Lose VARCHAR(20) NOT NULL,
            K_Team_Score VARCHAR(20) NOT NULL,
            K_Team_Lose_Score VARCHAR(20) NOT NULL,
            K_Team_Recent5_Games VARCHAR(20) NOT NULL, 
        );
        """

        cursor.execute(create_table_sql)
        db.commit()

        # JSON 데이터를 MySQL 데이터베이스에 삽입
        for player in player_list:
            sql = "INSERT INTO kboPlayers (player_Num, player_Name, player_Team, player_Position, player_Birth, player_Physical) VALUES (%s, %s, %s, %s, %s, %s)"
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

except Exception as err:
    print("Error" + err)
