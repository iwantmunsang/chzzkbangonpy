from tkinter import *
import json
import os
import requests
import time
import webbrowser
from plyer import notification
import subprocess
from tkinter import messagebox

falstbagoffallrm = False

# JSON 파일 경로
json_file_path = 'stremerlist.json'
setting_json = 'setting.json'

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
        setting = read_json(setting_json)
        for user in data["users"]:
            chids = user["chid"]
            url = f'https://api.chzzk.naver.com/service/v1/channels/{chids}'
            # 해더 설정
            headers = {
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.6326.214 Safari/537.36',
                'Accept-Language': 'ko-KR,ko;q=0.9,en-',
                'Accept-Encoding': 'gzip, deflate, br',
                'Connection': 'keep-alive',
                'Referer': 'https://www.google.com/',
                'Upgrade-Insecure-Requests': '1','path':"/polling/v1/channels/9e731707f6524b88436c5b3ede3a9848/live-status"
                ,"cookie":"NID_AUT=I3hV+sO6WBTAnaYbF5rjrKxn2O6ExaHcJa4JEHixnQhKguylPfm64WxChHAkKjOZ; NID_JKL=Rhe4poTMgkwrCO3JuEdoukH9eWZf+tVxfmeZvKY93ZA=; NAC=rAu8BQAyG8dZ; NNB=YKSZCL2TLLFWM; BUC=FUnBiNBqw8djUudesjxuJh5_8mG1C-SDq0zNiSLaIfc=; NID_SES=AAABmhb3rc93wNbtsLPBCgcjow6Y45/i60kNcCdaV3H1Q1aou6mVmqYVcVuVqLC9ozoUTGMo0KYEXZAJ3j97+73rjMBTlblPgEpS4Ku+EIuOCI3nlBAg4UNr3amDWsoLhlw43bCr41FYo5MIeYJwDggfC5VJEaXksobgIcvs00t2LlKbKySTB2H+/sJGw4edCzoe6iRePE9roBqydNjhrwoPTjo//Px6prfpGRmpbpwPyUJMvmYidhlpIboOQi0g2Mtns4JWhyAcKcn0E+HjuFeRCBmfkEByynxx7wKDOPf4qUweE9Kk/TqGckTfbjkAylxeKDB6J8vY3Jx1/pGplh3FD/Mbs3NRTIWkW8e3MWaR6o7weDlguVU7+23px9E0BowBLTJa7H6SPScc2RTG5UXCH7QPrjZBtwjEZJ5RYj/CxxB+SLbt/OYVEaE2NU7nuUClFqXdE2AZ9DuahGbQZ/PMiBxOZeu3H1FVv3BWcD2Wozl5Gp59OjkK60aRonpWMMxwr3ilUgXVAqo29nFqqL371VFxuZMviVmGO6QGlpu+aMh3; ba.uuid=0"
            }
            response = requests.get(url, headers=headers)
            # 응답을 JSON 형태로 변환
            api_data = response.json()
            # content 안에 있는 openlive 값 추출
            openlive = api_data.get('content', {}).get('openLive')
            name = api_data.get('content', {}).get('channelName')
            print(f"Open Live: {openlive}")
            # JSON 데이터에 onlive 값 반영
            user['onlive'] = openlive
            # if not user['falst']:
            #     user['falst'] = False
            if openlive:
                url2 = f"https://api.chzzk.naver.com/polling/v1/channels/{chids}/live-status"
                response = requests.get(url2, headers=headers)
                apidata = response.json()
                strimingname = apidata.get('content', {}).get("liveTitle")
                print(strimingname)
                user['livetitle'] = strimingname
                if not user["bangonallrm"] and setting['message']['bangon_message'] == "defalt":
                    notification.notify(
                        title=f"{name}",
                        message=f"{name}님이 방송중 입니다!!\n제목 : {strimingname}",
                        timeout=10
                    )
                    user['bangonallrm'] = True
                    user['bangoffallrm'] = False
                    user['livetitle'] = strimingname
                elif not setting['message']['bangon_message'] == "defalt" and not user["bangonallrm"]:
                    notification.notify(
                        title=f"{name}",
                        message=f"{setting['message']['bangon_message']}\n제목 : {strimingname}",
                        timeout=10
                    )
                    user['bangonallrm'] = True
                    user['bangoffallrm'] = False
                    user['livetitle'] = strimingname
            if not openlive:
                if not user['bangoffallrm']:
                    setting_val = read_json(setting_json)
                    user['bangoffallrm'] = True
                    user['bangonallrm'] = False
                    if falstbagoffallrm:
                        if setting_val['setting']["bangoff"] and setting['message']['bangoff_message'] == "defalt":
                            notification.notify(
                                title=f"{name}님이 방송을 종료 하였습니다",
                                message=f"{name}님이 방송을 종료 하였습니다",
                                timeout=10
                            )
                        elif setting_val['setting']["bangoff"] and not setting['message']['bangoff_message'] == "defalt":
                            notification.notify(
                                title=f"{name}님이 방송을 종료 하였습니다",
                                message=f"{setting['message']['bangoff_message']}",
                                timeout=10
                            )
        time.sleep(0.8)
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

labell = []

# 라벨 업데이트 함수
def update_labels():
    global falstbagoffallrm
    data = read_json(json_file_path)
    for widget in tk.winfo_children():
        if isinstance(widget, Label) and widget != header_label:
            widget.destroy()
    for user in data["users"]:
        if user['onlive']:
            if user['name'] not in labell:
                frame = Frame(tk, bg="white", padx=10, pady=10, bd=1, relief="solid")
                frame.pack(padx=10, pady=5, fill="x")
                label = Label(frame, text=f"{user['name']} | 제목 : {user['livetitle']}", font=("굴림", 15), fg="blue", cursor="hand2", bg="white")
                label.pack()
                label.bind("<Button-1>", lambda e, name=user['name']: open_link(name))
                labell.append(user['name'])
                falstbagoffallrm = True
    tk.after(60000, update_labels)  # 1분마다 업데이트

def reload_button():
    try:
        data = read_json(json_file_path)
        for widget in tk.winfo_children():
            if isinstance(widget, Label) and widget != header_label:
                widget.destroy()
        for user in data["users"]:
            if user['onlive']:
                if user['name'] not in labell:
                    frame = Frame(tk, bg="white", padx=10, pady=10, bd=1, relief="solid")
                    frame.pack(padx=10, pady=5, fill="x")
                    label = Label(frame, text=f"{user['name']} | 제목 : {user['livetitle']}", font=("굴림", 15), fg="blue", cursor="hand2", bg="white")
                    label.pack()
                    label.bind("<Button-1>", lambda e, name=user['name']: open_link(name))
                    labell.append(user['name'])
        api_get()
    except Exception as e:
        print(e)
        messagebox.showerror("에러 발생", f"알수 없는 오류 발생 : {e}")


# 설정 버튼 함수
def setting():
    print("설정")
    subprocess.Popen(['app.exe'], shell=True)

# JSON 데이터 읽기
data = read_json(json_file_path)

tk = Tk()
tk.geometry("600x700")  # 창의 크기를 적절하게 변경
tk.title("치지직 뱅온 알림")
tk.configure(bg="#f0f0f0")

# 각 스트리머의 정보를 라벨로 표시
header_frame = Frame(tk, bg="#0078d4", pady=10)
header_frame.pack(fill="x")
header_label = Label(header_frame, text="방송중인 스트리머 목록\n(창을 끄면 알림을 못 받아요!!!)\n(추가, 삭제는 set파일 사용)", font=("굴림", 15), bg="#0078d4", fg="white")
header_label.pack()

# 설정 버튼 추가
settings_button = Button(tk, text="설정", font=("굴림", 12), command=setting)
settings_button.pack(pady=10)

# 스트리밍 상태 로드 버튼 추가 (오른쪽 아래 배치)
api_get_reload = Button(tk, text="스트리밍 상태 리로드", font=("굴림", 12),bg="yellow", command=reload_button)
api_get_reload.place(relx=1, rely=1, anchor="se")


# 초기 업데이트 및 주기적 업데이트 설정
api_get()
update_labels()
tk.after(60000, lambda: api_get())  # 1분마다 API 요청

# 이벤트 루프 시작
tk.mainloop()
