from tkinter import *
import json
import os
import requests
import time
import webbrowser

# JSON 파일 경로
json_file_path = 'stremerlist.json'

# JSON 파일 읽기 함수
def read_json(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return {"users": []}

# JSON 파일 쓰기 함수
def write_json(file_path, data):
    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)

# API GET 요청 함수
def api_get():
    try:
        data = read_json(json_file_path)
        for user in data["users"]:
            chids = user["chid"]
            url = f'https://api.chzzk.naver.com/service/v1/channels/{chids}'
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
            api_data = response.json()
            # content 안에 있는 openlive 값 추출
            openlive = api_data.get('content', {}).get('openLive')
            print(f"Open Live: {openlive}")
            # JSON 데이터에 onlive 값 반영
            user['onlive'] = openlive
            time.sleep(1)
        
        # JSON 파일에 업데이트된 데이터 쓰기
        write_json(json_file_path, data)
        
    except Exception as e:
        print(f"Error: {e}")

# 이름으로 URL 열기 함수
def open_link(name):
    data = read_json(json_file_path)
    for user in data["users"]:
        if user["name"] == name:
            print(user["chid"])
            webbrowser.open(f"https://chzzk.naver.com/{user['chid']}")

# 라벨 업데이트 함수
def update_labels():
    data = read_json(json_file_path)
    for widget in tk.winfo_children():
        if isinstance(widget, Label) and widget != header_label:
            widget.destroy()
    for user in data["users"]:
        if user['onlive']:
            label = Label(tk, text=f"{user['name']}", font=("굴림", 15), fg="blue", cursor="hand2")
            label.pack()
            label.bind("<Button-1>", lambda e, name=user['name']: open_link(name))
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
api_get()
update_labels()
tk.after(60000, api_get)  # 1분마다 API 요청

# 이벤트 루프 시작
tk.mainloop()
