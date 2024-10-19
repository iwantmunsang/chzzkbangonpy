from tkinter import *
import json
import os
import random
from tkinter import messagebox

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
    if not id or not name:
        messagebox.showerror("입력 오류", "모든 필드를 입력하세요!")
        return
    data = read_json(json_file_path)
    if "users" not in data:
        data["users"] = []
    data["users"].append({"id": len(data["users"]) + 1, "name": name, "chid": id, "onlive": False, "bangonallrm": False, "bangoffallrm": False, "livetitle": "제목 없음"})
    write_json(json_file_path, data)
    messagebox.showinfo("성공", "스트리머가 추가되었습니다.")
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
        monjang = [
            "망겜이야 어쩌라고 나가",
            "너이 게이씨 뒷부분은 금지야 금지!",
            "계약서 깟다구!!",
            "한탕탕이님 한판 해요",
            "지리야 가서 코코아좀 타와라",
            "뿌웅 뭉탱이 월드에 오신걸 환영 합니다",
            "안녕하세요 저는 트위치에서 방송을 하고 있는 스트리머 케인입니다",
            "지금부터는"
        ]
        random_monjang = random.choice(monjang)
        if messagebox.askyesno("문장 확인", f"스트리머 목록을 정말 삭제 하시겠습니까?"):
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
    bangoff_set_button.config(text=f"방종 알람 {bangoff_set}")
    update_bangoff_setting()

# tkinter GUI 설정
tk = Tk()
tk.geometry("600x600")
tk.title("치지직 뱅온 알림 설정기")

frame = Frame(tk)
frame.pack(pady=20)

Label(frame, text="스트리머 추가", font=("굴림", 14)).grid(row=0, columnspan=2)

Label(frame, text="채널 아이디", font=("굴림", 12)).grid(row=1, column=0, pady=5)
id_entry = Entry(frame)
id_entry.grid(row=1, column=1, pady=5)

Label(frame, text="이름", font=("굴림", 12)).grid(row=2, column=0, pady=5)
name_entry = Entry(frame)
name_entry.grid(row=2, column=1, pady=5)

add_button = Button(frame, text="스트리머 추가", command=add_streamer, font=("굴림", 12))
add_button.grid(row=3, columnspan=2, pady=10)

listbox = Listbox(tk, width=80, height=10)
listbox.pack(pady=20)

refresh_button = Button(tk, text="목록 갱신", command=refresh_streamer_list, font=("굴림", 12))
refresh_button.pack(pady=5)

delete_button = Button(tk, text="스트리머 삭제", command=delete_streamer, font=("굴림", 12))
delete_button.pack(pady=5)

reset_button = Button(tk, text="스트리머 목록 초기화", command=reset_streamer_list, font=("굴림", 12))
reset_button.pack(pady=5)



# 방종 알람 버튼 추가
bangoff_set_button = Button(tk, text=f"방종 알람 현제 상태 : {bangoff_set}", command=bangoff_set_button_command, font=("굴림", 12))
bangoff_set_button.pack(pady=5)

refresh_streamer_list()

tk.mainloop()
