from tkinter import *
import json
import os
import requests
import time
import webbrowser
from plyer import notification
import subprocess
from tkinter import messagebox
import shutil
import imge
from PIL import Image, ImageTk
import sys
import datetime

falstbagoffallrm = False


def printt(message:str):
    print(f"[{datetime.datetime.today().strftime("%Y/%m/%d %H:%M:%S")}]  :  {message}")

def printterror(message:str):
    printt(f"\n\n\n 오류가 발생 하였지만 프로그램을 종류하지 않고 계속 실행합니다. \n {message}\n\n\n")


def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)


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
        global channelImageUrlname
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
                'Upgrade-Insecure-Requests': '1',
                'Cookie': "NID_AUT=I3hV+sO6WBTAnaYbF5rjrKxn2O6ExaHcJa4JEHixnQhKguylPfm64WxChHAkKjOZ; NID_JKL=Rhe4poTMgkwrCO3JuEdoukH9eWZf+tVxfmeZvKY93ZA=; NAC=rAu8BQAyG8dZ; NNB=YKSZCL2TLLFWM; BUC=FUnBiNBqw8djUudesjxuJh5_8mG1C-SDq0zNiSLaIfc=; NID_SES=AAABmhb3rc93wNbtsLPBCgcjow6Y45/i60kNcCdaV3H1Q1aou6mVmqYVcVuVqLC9ozoUTGMo0KYEXZAJ3j97+73rjMBTlblPgEpS4Ku+EIuOCI3nlBAg4UNr3amDWsoLhlw43bCr41FYo5MIeYJwDggfC5VJEaXksobgIcvs00t2LlKbKySTB2H+/sJGw4edCzoe6iRePE9roBqydNjhrwoPTjo//Px6prfpGRmpbpwPyUJMvmYidhlpIboOQi0g2Mtns4JWhyAcKcn0E+HjuFeRCBmfkEByynxx7wKDOPf4qUweE9Kk/TqGckTfbjkAylxeKDB6J8vY3Jx1/pGplh3FD/Mbs3NRTIWkW8e3MWaR6o7weDlguVU7+23px9E0BowBLTJa7H6SPScc2RTG5UXCH7QPrjZBtwjEZJ5RYj/CxxB+SLbt/OYVEaE2NU7nuUClFqXdE2AZ9DuahGbQZ/PMiBxOZeu3H1FVv3BWcD2Wozl5Gp59OjkK60aRonpWMMxwr3ilUgXVAqo29nFqqL371VFxuZMviVmGO6QGlpu+aMh3; ba.uuid=0"  # 쿠키 사용
            }
            response = requests.get(url, headers=headers)
            # 응답을 JSON 형태로 변환
            api_data = response.json()
            # content 안에 있는 openlive 값 추출
            openlive = api_data.get('content', {}).get('openLive')
            name = api_data.get('content', {}).get('channelName')
            url = f"https://api.chzzk.naver.com/polling/v1/channels/{chids}/live-status"
            response = requests.get(url , headers=headers)
            channelImageUrl = api_data.get('content',{}).get('channelImageUrl')
            printt(f"api get  Open Live: {openlive}")
            printt(f"api get  channelImageUrl : {channelImageUrl}")
            user['onlive'] = openlive
            user['channelImageUrl'] = channelImageUrl
            last_part = channelImageUrl.split('/')[-2]
            channelImageUrlname = last_part
            if not user['channelImagdownload']:
                user['channelImagename'] = channelImageUrlname
            elif user['channelImagdownload'] and not user['channelImagename'] == channelImageUrlname:
                printt(f"api get  채널 이미지 url의 변경을 감지 하였습니다 재 다운로드를 시도합니다  다운로드하는 스트리머의 channelImageUrlname : {channelImageUrlname}")
                imge.imge(channelImageUrl, channelImageUrlname , "images")
                user['channelImagdownload'] = True

            ############################################ 이미지 다운
            if not user['channelImagdownload']:
                try:
                    printt(f"api get  {channelImageUrlname}의 다운로드를 시도합니다")
                    imge.imge(channelImageUrl, channelImageUrlname , "images")
                    user['channelImagdownload'] = True
                except Exception as e:
                    printterror(f"api get  초기 이미지 다운로드중 오류가 발생 하였습니다 {e}")
            ############################################################################################################################################
            if openlive:
                url2 = f"https://api.chzzk.naver.com/polling/v1/channels/{chids}/live-status"
                response = requests.get(url2, headers=headers)
                apidata = response.json()
                strimingname = apidata.get('content', {}).get("liveTitle")
                printt(f"api get  방송중인 스트리머의 스트리밍 제목 : {strimingname}")
                user['livetitle'] = strimingname
                if not user["bangonallrm"] and setting['message']['bangon_message'] == "default":
                    notification.notify(
                        title=f"{name}",
                        message=f"{name}님이 방송중 입니다!!\n제목 : {strimingname}",
                        timeout=10
                    )
                    user['bangonallrm'] = True
                    user['bangoffallrm'] = False
                    user['livetitle'] = strimingname
                elif not setting['message']['bangon_message'] == "default" and not user["bangonallrm"]:
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
                        if setting_val['setting']["bangoff"] and setting['message']['bangoff_message'] == "default":
                            notification.notify(
                                title=f"{name}님이 방송을 종료 하였습니다",
                                message=f"{name}님이 방송을 종료 하였습니다",
                                timeout=10
                            )
                        elif setting_val['setting']["bangoff"] and not setting['message']['bangoff_message'] == "default":
                            notification.notify(
                                title=f"{name}님이 방송을 종료 하였습니다",
                                message=f"{setting['message']['bangoff_message']}",
                                timeout=10
                            )
        time.sleep(0.8)
        # JSON 파일에 업데이트된 데이터 쓰기
        write_json(json_file_path, data)
    except Exception as e:
        printterror(f"Error api_get: {e}")

# 이름으로 URL 열기 함수
def open_link(name):
    data = read_json(json_file_path)
    for user in data["users"]:
        if user["name"] == name:
            printt(f"open_link  제목을 클릭하여 링크를 엽니다 chid = {user["chid"]}")
            webbrowser.open(f"https://chzzk.naver.com/{user['chid']}")

labell = []

# 프레임을 저장할 딕셔너리
frames = {}

def update_labels():
    global falstbagoffallrm
    data = read_json(json_file_path)

    # 현재 활성화된 사용자 ID 목록
    active_user_ids = {user['id'] for user in data["users"] if user['onlive']}

    # 프레임을 유지할 사용자 ID 목록
    current_user_ids = set(frames.keys())

    # 프레임 삭제: JSON에 없는 사용자 ID에 대한 프레임 제거
    for user_id in current_user_ids - active_user_ids:
        frame = frames.pop(user_id, None)
        if frame:
            frame.destroy()  # 프레임 삭제
            labell.remove(user_id)  # 라벨에서 ID 제거

    for user in data["users"]:
        if user['onlive']:
            if user['id'] not in labell:
                # 새로운 프레임과 라벨 생성
                frame = Frame(main, bg="white", padx=10, pady=10, bd=1, relief="solid")
                frame.pack(padx=10, pady=5, fill="x")

                # 36글자 넘으면 자르기
                title = f"{user['name']} | 제목 : {user['livetitle']}"
                if len(title) >= 36:
                    setting = read_json(setting_json)
                    if setting["setting"]["showimage"]:
                        title = title[0:31] + "..."
                    else:
                        title = title[0:36] + "..."

                # 텍스트 라벨 생성
                label = Label(frame, text=f"{title}", font=("굴림", 15), fg="blue", cursor="hand2", bg="white")

                # 이미지 처리
                try:
                    if setting["setting"]["showimage"]:
                        if os.path.exists(f"images/{channelImageUrlname}"):
                            image = Image.open(f"images/{channelImageUrlname}")  # 이미지 경로를 실제 파일 경로로 바꾸세요.
                        else:
                            printt("update_labels  이미지 파일을 찾을수 없습니다")
                            image = Image.open(f"images/ERROR.png")
                            user["channelImagdownload"] = False
                            write_json(json_file_path , data)
                            reload_button()

                        image = image.resize((50, 50))  # 이미지 크기 조절 (선택 사항)
                        photo = ImageTk.PhotoImage(image)

                        # Label에 이미지 설정
                        image_label = Label(frame, image=photo, bg="white")
                        image_label.image = photo  # 이미지가 가비지 컬렉션 되지 않도록 참조 유지
                        image_label.pack(side="left")
                except Exception as e:
                    printterror(f"update_labels  이미지 로드 오류: {e}")
                label.pack(side="left", padx=10)

                label.bind("<Button-1>", lambda e, name=user['name']: open_link(name))
                labell.append(user['id'])  # 라벨에 이름 추가
                frames[user['id']] = frame  # 프레임을 딕셔너리에 저장
                falstbagoffallrm = True
        elif user['id'] in labell:
            # 해당 프레임 제거
            frame = frames.pop(user['id'], None)
            if frame:
                frame.destroy()  # 프레임 삭제
                labell.remove(user['id'])  # 라벨에서 ID 제거

    printt(f"update_labels  현재 목록 라벨에 올라가있는 스트리머의 id {labell}")
    main.after(60000, update_labels)  # 1분마다 업데이트


def reload_button():
    try:
        update_labels()
        api_get()
        update_labels()
    except Exception as e:
        printterror(f"리로드 버튼 에러 \n{e}")
        messagebox.showerror("에러 발생", f"알수 없는 오류 발생 : {e}")


# 설정 버튼 함수
def setting():
    try:
        printt("설정버튼 클릭을 감지 하였습니다 app.py실행")
        subprocess.run(['python','App.py'])
    except Exception as e:
        printterror(f"설정 버튼 함수 오류 : \n{e}")

def start_program_function():
    data = read_json(setting_json)
    start_program = data["setting"]["start_program"]
    
    # start_program이 False일 때만 실행
    if not start_program:
        if messagebox.askyesno("시작 프로그램으로 등록 할까요?", "컴퓨터가 실행 되면 같이 실행 할까요?"):
            abc = os.getcwd()  # 현재 작업 디렉토리 가져오기
            wichi = os.path.join(abc, "치지직뱅온알람기.lnk")  # 경로 설정 (os.path.join 사용)
            
            # 복사할 대상 경로 설정
            target_path = r"C:\Users\USER\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup\치지직뱅온알람기.lnk"
            
            # 파일 복사
            if os.path.exists(wichi):
                try:
                    shutil.copyfile(wichi, target_path)  # 원본 파일과 대상 파일 경로 제공
                    printt("파일이 성공적으로 복사되었습니다.")
                    
                    # JSON 설정 업데이트
                    data["setting"]["start_program"] = True
                    write_json(setting_json, data)  # 설정 업데이트
                except Exception as e:
                    printterror(f"파일 복사 중 오류 발생: \n{e}")
            else:
                printt("원본 파일을 찾을 수 없습니다.")
        else:
            data["setting"]["start_program"] = True
            write_json(setting_json, data)
    else:
        printt("이미 파일이 존재합니다.")


start_program_function()

# JSON 데이터 읽기
data = read_json(json_file_path)

main = Tk()
main.geometry("600x700")  # 창의 크기를 적절하게 변경
main.title("치지직 뱅온 알림")
main.configure(bg="#f0f0f0")

def on_closing():
    main.destroy()  # maininter 창 종료
    sys.exit()    # 프로세스 종료

def closing():
    main.destroy()
    sys.exit()

main.protocol("WM_DELETE_WINDOW", on_closing)  # 창 닫기 이벤트에 on_closing 함수 등록

# 각 스트리머의 정보를 라벨로 표시
header_frame = Frame(main, bg="#0078d4", pady=10)
header_frame.pack(fill="x")
header_label = Label(header_frame, text="방송중인 스트리머 목록\n(창을 끄면 알림을 못 받아요!!!)\n(추가, 삭제는 set파일 사용)", font=("굴림", 15), bg="#0078d4", fg="white")
header_label.pack()

# 설정 버튼 추가
settings_button = Button(main, text="설정", font=("굴림", 12), command=setting)
settings_button.pack(pady=10)

# 스트리밍 상태 로드 버튼 추가 (오른쪽 아래 배치)
api_get_reload = Button(main, text="스트리밍 상태 리로드", font=("굴림", 12), bg="yellow", command=reload_button)
api_get_reload.place(relx=1, rely=1, anchor="se")

# 초기 업데이트 및 주기적 업데이트 설정
api_get()
update_labels()
main.after(60000, lambda: api_get())  # 1분마다 API 요청

# 이벤트 루프 시작
main.mainloop()
