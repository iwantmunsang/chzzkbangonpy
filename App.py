from tkinter import *
import json
import os
import random
from tkinter import messagebox
import pandas as pd
from tkinter import filedialog
import sys
import webbrowser

# JSON 파일 경로
json_file_path = 'stremerlist.json'
setting_file = 'setting.json'

# JSON 파일 읽기 함수
def read_json(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

# JSON 파일 쓰기 함수
def write_json(file_path, data):
    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)

# 스트리머 추가 함수
def add_streamer():
    id = id_entry.get()
    name = name_entry.get()
    global isteregg
    if isteregg:
        if name == "rickroll" or id == "rickroll" or name == "RICKROLL" or id == "RICKROLL" or name == "릭롤" or id == "릭롤":
            webbrowser.open_new_tab("https://www.youtube.com/watch?v=dQw4w9WgXcQ")
            return
        if name == "케인인님" or name == "케인인" or name == "케인":
            webbrowser.open_new_tab("https://www.youtube.com/watch?v=92volEdYcCQ")
            messagebox.showinfo("무빙맨","얘는! 유튜브 쟁이들은 이런거 몰라! 너무 내수용은 밴이야 밴!! ㅇㅇㄱㄴ1")

    if not id or not name:
        messagebox.showerror("입력 오류", "모든 필드를 입력하세요!")
        return
    #https://chzzk.naver.com/bae2142e03116206963eea4bc15dc402
    if "chzzk.naver.com" in id:
        last_part = id.split('/')[-1]
        id = last_part
        print(id)
    print(id)
    data = read_json(json_file_path)
    if "users" not in data:
        data["users"] = []
    data["users"].append({"id": len(data["users"]) + 1,
                           "name": name,
                            "chid": id,
                            "onlive": False,
                            "bangonallrm": False,
                            "bangoffallrm": False,
                            "livetitle": "제목 없음",
                            "channelImageUrl":None,
                            "channelImagdownload":False,
                            "channelImagename":None})
    write_json(json_file_path, data)
    id_entry.delete(0, END)
    name_entry.delete(0, END)
    refresh_streamer_list()

# 스트리머 목록 갱신 함수
def refresh_streamer_list():
    listbox.delete(0, END)
    data = read_json(json_file_path)
    if "users" in data:
        for user in data["users"]:
            listbox.insert(END, f"이름: {user['name']}, ID: {user['chid']}, onlive: {user['onlive']}")

# 스트리머 삭제 함수
def delete_streamer():
    selected = listbox.curselection()
    if not selected:
        messagebox.showerror("선택 오류", "삭제할 스트리머를 선택하세요!")
        return
    data = read_json(json_file_path)
    selected_index = selected[0]
    user_id = data["users"][selected_index]["id"]
    data["users"] = [user for user in data["users"] if user["id"] != user_id]
    write_json(json_file_path, data)
    messagebox.showinfo("성공", "스트리머가 삭제되었습니다.")
    refresh_streamer_list()

# 스트리머 목록 초기화 함수
def reset_streamer_list():
    if messagebox.askyesno("초기화 확인", "정말로 초기화 하시겠습니까? 초기화가 진행되면 복구가 불가합니다."):
        if messagebox.askyesno("찐막 확인", f"스트리머 목록을 정말 삭제 하시겠습니까?"):
            data = {"users": []}
            write_json(json_file_path, data)
            messagebox.showinfo("성공", "스트리머 목록이 초기화 되었습니다.")
            refresh_streamer_list()

bangoff_set = False

# 방종 알람 설정 파일 업데이트 함수
def update_bangoff_setting():
    data = read_json(setting_file)
    if "setting" not in data:
        data["setting"] = {}
    data["setting"]["bangoff"] = bangoff_set
    write_json(setting_file, data)
    print(f"방종 알람 설정이 {bangoff_set}으로 저장되었습니다.")

def bangoff_setset():
    global bangoff_set
    data = read_json(setting_file)
    bangoff_set = data['setting']["bangoff"]
bangoff_setset

# 방종 알람 버튼 동작 함수
def bangoff_set_button_command():
    global bangoff_set
    bangoff_set = not bangoff_set
    bangoff_set_button.config(text=f"방종 알람 현제 상태 : {bangoff_set}")
    update_bangoff_setting()

bangon_message = None

def bangon_message_btn():
    try:
        global bangon_message
        bangon_message = bangon_message_input.get()
        setting_json = read_json(setting_file)

        # "message" 키가 없는 경우 추가
        if "message" not in setting_json:
            setting_json["message"] = {}

        if bangon_message == "defalt" or bangon_message == None:
            messagebox.showerror("에러 발생", f"사용자 입력 오류\n이 값은 사용할수 없습니다")
            return

        setting_json["message"]["bangon_message"] = bangon_message
        write_json(setting_file, setting_json)
        messagebox.showinfo("뱅온시 메시지 설정", f"뱅온시 메시지가 : {bangon_message}로 설정 되었습니다")
    except Exception as e:
        messagebox.showerror("에러 발생", f"오류가 발생 하였습니다\n{e}")

def bangon_message_btn_deflat_load():
    try:
        setting_json = read_json(setting_file)

        # "message" 키가 없는 경우 추가
        if "message" not in setting_json:
            setting_json["message"] = {}

        setting_json["message"]["bangon_message"] = "defalt"
        write_json(setting_file, setting_json)
        messagebox.showinfo("뱅온시 메시지 설정", f"뱅온시 메시지가 : 기본 값으로 설정 되었습니다")
    except Exception as e:
        messagebox.showerror("에러 발생", f"오류가 발생 하였습니다\n{e}")


def bangoff_message_btn_deflat_load():
    try:
        setting_json = read_json(setting_file)

        # "message" 키가 없는 경우 추가
        if "message" not in setting_json:
            setting_json["message"] = {}

        setting_json["message"]["bangoff_message"] = "defalt"
        write_json(setting_file, setting_json)
        messagebox.showinfo("방종시 메시지 설정", f"방종시 메시지가 : 기본 값으로 설정 되었습니다")
    except Exception as e:
        messagebox.showerror("에러 발생", f"오류가 발생 하였습니다\n{e}")

def bangoff_message_btn():
    try:
        global bangoff_message
        bangoff_message = bangoff_message_input.get()
        setting_json = read_json(setting_file)

        # "message" 키가 없는 경우 추가
        if "message" not in setting_json:
            setting_json["message"] = {}

        if bangoff_message == "defalt" or bangoff_message == None:
            messagebox.showerror("에러 발생", f"사용자 입력 오류\n이 값은 사용할수 없습니다")
            return

        setting_json["message"]["bangoff_message"] = bangoff_message
        write_json(setting_file, setting_json)
        messagebox.showinfo("방종시 메시지 설정", f"방종시 메시지가 : {bangoff_message}로 설정 되었습니다")
    except Exception as e:
        messagebox.showerror("에러 발생", f"오류가 발생 하였습니다\n{e}")

def bunhaun_button_function():
    try:
        # 파일 선택 대화상자를 열고, 선택한 파일을 얻음
        file = filedialog.askopenfile(
            title="불러올 stremerlist.json 파일을 선택하세요",
            filetypes=(('JSON 파일', '*.json'),)
        )
        
        # 파일을 제대로 선택했는지 확인
        if file:
            global json_file_path
            print(file.name)
            
            # 선택한 파일을 열 때 인코딩을 명시적으로 utf-8로 지정
            with open(file.name, 'r', encoding='utf-8') as f:
                data = json.load(f)  # 파일 내용을 JSON으로 불러옴
            
            # JSON 데이터에 새로운 필드 추가
            for user in data.get('users', []):
                # 사용자 객체에 새로운 키 추가하기
                user.update({
                    "channelImageUrl": None,
                    "channelImagdownload": False,
                    "channelImagename": None
                })
            
            # 수정된 데이터를 원래의 json_file_path에 저장
            write_json(json_file_path, data)
            
            messagebox.showinfo("성공", "기존 데이터를 업데이트하였습니다.")
    
    except UnicodeDecodeError as e:
        messagebox.showerror("인코딩 오류", f"파일을 읽는 중 인코딩 오류가 발생했습니다: {e}")
    except json.JSONDecodeError as e:
        messagebox.showerror("JSON 오류", f"JSON 파일을 읽는 중 오류가 발생했습니다: {e}")
    except Exception as e:
        messagebox.showerror("에러 발생", f"예기치 않은 오류가 발생했습니다: {e}")

def all_reset_button_function():
    # 첫 번째 확인 창
    if messagebox.askyesno("리셋 진행", "이 설정은 스트리머 리스트와 설정값 등을 기본 값으로 초기화 합니다.\n진행 하시겠습니까?"):
        # 두 번째 확인 창
        if messagebox.askyesno("리셋 진행", "여기서 예를 클릭하면 진짜로 리셋이 진행됩니다."):

            # 설정 파일을 초기화
            setting_json = {
                "setting": {
                    "bangoff": True,
                    "start_program": False
                },
                "message": {
                    "bangon_message": "default",
                    "bangoff_message": "default"
                }
            }
            write_json(setting_file, setting_json)

            # 스트리머 리스트 파일을 초기화
            streamerlist = {
                "users": []
            }
            write_json(json_file_path, streamerlist)

            # 'images' 폴더 삭제
            images_dir = "images"
            if os.path.exists(images_dir):
                for root, dirs, files in os.walk(images_dir, topdown=False):
                    for name in files:
                        os.remove(os.path.join(root, name))  # 파일 삭제
                    for name in dirs:
                        os.rmdir(os.path.join(root, name))  # 빈 디렉토리 삭제
                os.rmdir(images_dir)  # 최상위 디렉토리 삭제

            # 리셋 완료 메시지 박스
            messagebox.showinfo("리셋 완료", "리셋이 완벽히 진행 되었습니다. 프로그램을 재시작 합니다.")
            sys.exit()  # 프로그램 종료
isteregg = False
def isteregg_onoff_button_function():
    if messagebox.askyesno("🥚is터egg🥚 호ㅏㄹ sungㅎㅏㅗ" , "🥚이🥚s🥚ㅌㅓ🥚달🥚걀🥚을 활성화 할까요????????"):
        global isteregg
        isteregg = True
        messagebox.showinfo("🥚is터egg🥚 호ㅏㄹ sungㅎㅏㅗ","1000000000ㅂㅜㄴ으ㅣ 1ㅇㅢ 확ㅇㅠㄹ을 뚜ㅀ어ㅆ으니 ㅌㅡㄱ벼ㄹ히 허ㄹㅏㄱ해주ㅁ \nㅅㅡㅌㅡㄹㅣ머 ㅊㅜga 카ㄴㅇㅔ rickrollㅇㅣㅂ려ㄱㅎㅐ보셈")



    


# tkinter GUI 설정
tk = Tk()
tk.geometry("600x600")
tk.title("치지직 뱅온 알림 설정기")

# 상단에 스트리머 추가하는 부분
frame_top = Frame(tk)
frame_top.pack(pady=20)

Label(frame_top, text="치지직 뱅온 알람기 설정", font=("굴림", 12)).grid(row=0, columnspan=2)

Label(frame_top, text="채널 아이디", font=("굴림", 12)).grid(row=1, column=0, pady=5)
id_entry = Entry(frame_top)
id_entry.grid(row=1, column=1, pady=5)

Label(frame_top, text="이름", font=("굴림", 12)).grid(row=2, column=0, pady=5)
name_entry = Entry(frame_top)
name_entry.grid(row=2, column=1, pady=5)

add_button = Button(frame_top, text="스트리머 추가", command=add_streamer, font=("굴림", 12))
add_button.grid(row=3, columnspan=2, pady=10)

# 스트리머 리스트를 표시하는 부분
listbox = Listbox(tk, width=80, height=10)
listbox.pack(pady=20)

# 하단에 있는 버튼 부분
frame_bottom = Frame(tk)
frame_bottom.pack(pady=10)

refresh_button = Button(frame_bottom, text="목록 갱신", command=refresh_streamer_list, font=("굴림", 12))
refresh_button.grid(row=0, column=0, padx=10)

delete_button = Button(frame_bottom, text="스트리머 삭제", command=delete_streamer, font=("굴림", 12))
delete_button.grid(row=0, column=1, padx=10)

reset_button = Button(frame_bottom, text="스트리머 목록 초기화", command=reset_streamer_list, font=("굴림", 12))
reset_button.grid(row=0, column=2, padx=10)

# 방종 알람 메시지 설정 부분
frame_bangoff_message = Frame(tk)
frame_bangoff_message.pack(pady=5)

frame_bangon_message = Frame(tk)
frame_bangon_message.pack(pady=5)

frame_3 = Frame(tk)
frame_3.pack(pady=5)

frame_4 = Frame(tk)
frame_4.pack(pady=5)


bangoff_message_label = Label(frame_bangoff_message ,text="방종시 메시지" , font=("굴림",12))
bangoff_message_label.grid(row=0, column=0, padx=5)

bangoff_message_input = Entry(frame_bangoff_message, width=30)
bangoff_message_input.grid(row=0, column=1, padx=5)

bangoff_message_button = Button(frame_bangoff_message, text="설정" , command=bangoff_message_btn)
bangoff_message_button.grid(row=0, column=2, padx=5)

bangoff_message_deflat_load_button = Button(frame_bangoff_message , text="기본값 로드" , command=bangoff_message_btn_deflat_load)
bangoff_message_deflat_load_button.grid(row=0, column=3, padx=5)

# 뱅온 메시지 설정 구역
bangon_message_label = Label(frame_bangon_message ,text="뱅온시 알림 메시지" , font=("굴림",12))
bangon_message_label.grid(row=0, column=0, padx=5)

bangon_message_input = Entry(frame_bangon_message, width=30)
bangon_message_input.grid(row=0, column=1, padx=5)

bangon_message_button = Button(frame_bangon_message, text="설정", command=bangon_message_btn)
bangon_message_button.grid(row=0, column=2, padx=5)

bangon_message_deflat_load_button = Button(frame_bangon_message , text="기본값 로드" , command=bangon_message_btn_deflat_load)
bangon_message_deflat_load_button.grid(row=0, column=3, padx=5)

bangoff_set_button = Button(frame_3 ,text=f"방종 알람 현제 상태 : {bangoff_set}",font=("굴림",12), command=bangoff_set_button_command)
bangoff_set_button.grid(row=0, column=3, padx=5)

bunhaun_button = Button(frame_3 , text="이전 버전 리스트 불러오기" , command=bunhaun_button_function)
bunhaun_button.grid(row=0 , column=4, padx=5)

all_reset_button = Button(frame_4 , text="모든 설정 리셋" , command=all_reset_button_function , bg="red")
all_reset_button.grid(row=0 , column=1, padx=5)

isteregg_button = random.randrange(1 , 1000000000)
if isteregg_button == 123445:
    isteregg_onoff_button = Button(frame_4 , text="🥚이스터에그🥚" , command=isteregg_onoff_button_function)
    isteregg_onoff_button.grid(row=0 , column=2, padx=5)
else:
    print(isteregg_button)

refresh_streamer_list()

tk.mainloop()
