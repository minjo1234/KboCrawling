import json
import requests
from bs4 import BeautifulSoup
import mysql.connector

file_path = 'kboPlayers_href2.json'
kbo_pitchers = []
count = 0
try:
    with open(file_path, 'r', encoding='utf-8') as json_file:
        # JSON 파일을 파싱
        players_href = json.load(json_file)

        for i in range(len(players_href)):
            # https://www.koreabaseball.com/Record/Player/PitcherDetail/Basic.aspx?playerId=67119
            url = f'https://www.koreabaseball.com/Record/Player/PitcherDetail/Basic.aspx?playerId={players_href[i]}'
            response = requests.get(url)
            soup = BeautifulSoup(response.text, 'html.parser')
            # player_position
            players_position_elements = soup.find(
                'span', id='cphContents_cphContents_cphContents_playerProfile_lblPosition').text
            # cphContents_cphContents_cphContents_playerProfile_lblPosition
            player_Name = soup.find(
                'span', id='cphContents_cphContents_cphContents_playerProfile_lblName').text
            count += 1
            print(count)
            if '투수' in players_position_elements:
                # player_data
                table = soup.find('table')
                tbody = table.find('tbody')
                td_elements = tbody.find_all('td')

                player_href = players_href[i]
                player_Team = td_elements[0].text if td_elements and len(
                    td_elements) > 0 else ""
                player_ERA = td_elements[1].text if td_elements and len(
                    td_elements) > 1 else ""
                player_Game = td_elements[2].text if td_elements and len(
                    td_elements) > 2 else ""
                player_Win = td_elements[5].text if td_elements and len(
                    td_elements) > 5 else ""
                player_Lose = td_elements[6].text if td_elements and len(
                    td_elements) > 6 else ""
                player_Save = td_elements[7].text if td_elements and len(
                    td_elements) > 7 else ""
                player_HLD = td_elements[8].text if td_elements and len(
                    td_elements) > 8 else ""
                player_WPCT = td_elements[9].text if td_elements and len(
                    td_elements) > 9 else ""
                kbo_pitcherData = {
                    'player_Id': count,
                    'player_Name': player_Name,
                    'player_href': player_href,
                    'player_Team': player_Team,
                    'player_ERA': player_ERA,
                    'player_Game': player_Game,
                    'player_Win': player_Win,
                    'player_Lose': player_Lose,
                    'player_Save': player_Save,
                    'player_HLD': player_HLD,
                    'player_WPCT': player_WPCT
                }

                kbo_pitchers.append(kbo_pitcherData)
                # JSON 데이터를 MySQL 데이터베이스에 삽입

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
        CREATE TABLE IF NOT EXISTS kboPitcher (
            player_Id BIGINT PRIMARY KEY,
            player_Name VARCHAR(255) NOT NULL,
            player_href VARCHAR(255), 
            player_Team VARCHAR(255),
            player_ERA VARCHAR(255),
            player_Game VARCHAR(255),
            player_Win VARCHAR(255),
            player_Lose VARCHAR(255),
            player_Save VARCHAR(255),
            player_HLD VARCHAR(255),
            player_WPCT VARCHAR(255)
        );
        """
        cursor.execute(create_table_sql)
        db.commit()

        for kbo_pitcher in kbo_pitchers:
            sql = """
            INSERT INTO kboPitcher(player_Id, player_Name , player_href, player_Team, player_ERA, player_Game, player_Win, player_Lose, player_Save, player_HLD, player_WPCT)
            VALUES (%s, %s , %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            val = (kbo_pitcher["player_Id"],
                   kbo_pitcher["player_Name"],
                   kbo_pitcher["player_href"],
                   kbo_pitcher["player_Team"],
                   kbo_pitcher["player_ERA"],
                   kbo_pitcher["player_Game"],
                   kbo_pitcher["player_Win"],
                   kbo_pitcher["player_Lose"],
                   kbo_pitcher["player_Save"],
                   kbo_pitcher["player_HLD"],
                   kbo_pitcher["player_WPCT"])
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
    print()
    # JSON 파일 경로
