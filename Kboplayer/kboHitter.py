import json
import requests
from bs4 import BeautifulSoup
import mysql.connector

file_path = 'kboPlayers_href2.json'
kbo_hitters = []
count = 0
try:
    with open(file_path, 'r', encoding='utf-8') as json_file:
        # JSON 파일을 파싱
        players_href = json.load(json_file)
# https://www.koreabaseball.com/Futures/Player/HitterDetail.aspx?playerId=53103
        for i in range(len(players_href)):
            # https://www.koreabaseball.com/Record/Player/PitcherDetail/Basic.aspx?playerId=67119
            url = f'https://www.koreabaseball.com/Futures/Player/HitterDetail.aspx?playerId={players_href[i]}'
            response = requests.get(url)
            soup = BeautifulSoup(response.text, 'html.parser')
            # player_position
            players_position_elements = soup.find(
                'span', id='cphContents_cphContents_cphContents_ucPlayerProfile_lblPosition').text
            player_Name = soup.find(
                'span', id='cphContents_cphContents_cphContents_ucPlayerProfile_lblName').text
            count += 1
            if '투수' not in players_position_elements:
                # player_data
                table = soup.find('table')
                tbody = table.find('tbody')
                td_elements = tbody.find_all('td')
                player_href = players_href[i]
                player_Team = td_elements[0].text if td_elements and len(
                    td_elements) > 0 else ""
                player_AVG = td_elements[1].text if td_elements and len(
                    td_elements) > 1 else ""
                player_Game = td_elements[2].text if td_elements and len(
                    td_elements) > 2 else ""
                player_AB = td_elements[3].text if td_elements and len(
                    td_elements) > 3 else ""
                player_R = td_elements[4].text if td_elements and len(
                    td_elements) > 4 else ""
                player_H = td_elements[5].text if td_elements and len(
                    td_elements) > 5 else ""
                player_2B = td_elements[6].text if td_elements and len(
                    td_elements) > 6 else ""
                player_3B = td_elements[7].text if td_elements and len(
                    td_elements) > 7 else ""
                player_HR = td_elements[8].text if td_elements and len(
                    td_elements) > 8 else ""
                kbo_hittersData = {
                    'player_Id': count,
                    'player_Name': player_Name,
                    'player_href': player_href,
                    'player_Team': player_Team,
                    'player_AVG': player_AVG,
                    'player_Game': player_Game,
                    'player_AB': player_AB,
                    'player_R': player_R,
                    'player_H': player_H,
                    'player_2B': player_2B,
                    'player_3B': player_3B,
                    'player_HR': player_HR,
                }
                kbo_hitters.append(kbo_hittersData)
                # JSON 데이터를 MySQL 데이  터베이스에 삽입
    db_config = {
        "host": "localhost",
        "port": 3306,  # 포트 번호를 별도로 지정
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
        CREATE TABLE IF NOT EXISTS kboHitter (
            player_Id BIGINT PRIMARY KEY,
            player_Name VARCHAR(255) NOT NULL,
            player_href VARCHAR(255) NOT Null, 
            player_Team VARCHAR(255),
            player_AVG VARCHAR(255),
            player_Game VARCHAR(255),
            player_AB VARCHAR(255),
            player_R VARCHAR(255),
            player_H VARCHAR(255),
            player_2B VARCHAR(255),
            player_3B VARCHAR(255),
            player_HR VARCHAR(255)
        );
        """
        cursor.execute(create_table_sql)
        db.commit()
        for kbo_hitter in kbo_hitters:
            print(kbo_hitter)
            sql = """
            INSERT INTO kboHitter(player_Id , player_Name , player_href, player_Team, player_AVG, player_Game,  player_AB, player_R, player_H, player_2B, player_3B, player_HR)
            VALUES (%s , %s ,%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            val = (kbo_hitter["player_Id"],
                   kbo_hitter["player_Name"],
                   kbo_hitter["player_href"],
                   kbo_hitter["player_Team"],
                   kbo_hitter["player_AVG"],
                   kbo_hitter["player_Game"],
                   kbo_hitter["player_AB"],
                   kbo_hitter["player_R"],
                   kbo_hitter["player_H"],
                   kbo_hitter["player_2B"],
                   kbo_hitter["player_3B"],
                   kbo_hitter["player_HR"])

            cursor.execute(sql, val)
            db.commit()
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        # 변경 내용을 저장
        db.commit()

    finally:
        # 커넥션 닫기
        if db.is_connected():
            cursor.close()
            db.close()
        # sql 구문에 val를 넣겠다 .

except Exception as err:
    print(err)
    # JSON 파일 경로
