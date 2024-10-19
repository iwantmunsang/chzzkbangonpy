from tkinter import *
import json
import os
import requests

# JSON 파일 경로
json_file_path = 'stremerlist.json'

# API GET 요청 함수
def api_get(chid):
    try:
        url = f'https://api.chzzk.naver.com/service/v1/channels/{chid}'
        # 해더 설정
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Referer': 'https://www.google.com/',
            'Upgrade-Insecure-Requests': '1'
        }
        response = requests.get(url, headers=headers)
        # 응답을 JSON 형태로 변환
        data = response.json()
        # content 안에 있는 openlive 값 추출
        openlive = data.get('content', {}).get('openLive')
        print(f"Open Live: {openlive}")
    except Exception as e:
        print(f"Error: {e}")

# JSON 파일 읽기 함수
def read_json(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return {"users": []}

# 라벨 업데이트 함수
def update_labels():
    data = read_json(json_file_path)
    for widget in tk.winfo_children():
        if isinstance(widget, Label) and widget != header_label:
            widget.destroy()
    for user in data["users"]:
        if user['onlive']:
            label = Label(tk, text=f"{user['name']}", font=("굴림", 15))
            label.pack()
    tk.after(60000, update_labels)  # 1분마다 업데이트


# JSON 데이터 읽기
data = read_json(json_file_path)

tk = Tk()
tk.geometry("500x600")  # 창의 크기를 적절하게 변경
tk.title("치지직 뱅온 알림")

# 각 스트리머의 정보를 라벨로 표시
header_label = Label(tk, text="방송중인 스트리머 목록(창을 끄면 알림을 못 받아요!!!)\n(추가, 삭제는 set파일 사용)", font=("굴림", 15))
header_label.pack()

# 초기 업데이트 및 주기적 업데이트 설정
update_labels()
tk.after(60000, lambda: api_get("9ae7d38b629b78f48e49fb3106218ff5"))  # 1분마다 API 요청
api_get("9ae7d38b629b78f48e49fb3106218ff5")
update_labels()

# 이벤트 루프 시작
tk.mainloop()
