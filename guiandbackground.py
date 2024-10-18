from tkinter import *
import json

# JSON 파일 경로
json_file_path = 'stremerlist.json'

# JSON 파일 읽기
def read_json(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        return {"users": []}
    except json.JSONDecodeError:
        return {"users": []}

# JSON 데이터 읽기
data = read_json(json_file_path)

tk = Tk()
tk.geometry("500x600")  # 창의 크기를 적절하게 변경
tk.title("치지직 뱅온 알림")

# 각 스트리머의 정보를 라벨로 표시
labell = Label(tk, text="방송중인 스트리머 목록(창을 끄면 알림을 못 받아요!!!)\n(추가, 삭제는 set파일 사용)",font=("굴림",15) )
labell.pack()
for user in data["users"]:
    if user['onlive']:
        label = Label(tk,text=f"{user['name']}",font=("굴림",15))
    label.pack()

# 이벤트 루프 시작
tk.mainloop()
