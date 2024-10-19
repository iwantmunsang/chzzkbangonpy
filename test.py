import sqlite3
import os

# 쿠키 파일 경로 설정
cookie_path = "C:/Users/USER/AppData/Local/Google/Chrome/User Data/Default/Cookies"


# SQLite 데이터베이스 연결
conn = sqlite3.connect(cookie_path)
cursor = conn.cursor()

# 쿠키 테이블에서 데이터 가져오기
cursor.execute("SELECT host_key, name, value FROM cookies")

# 쿠키 출력
for row in cursor.fetchall():
    print(row)

# 연결 닫기
conn.close()
