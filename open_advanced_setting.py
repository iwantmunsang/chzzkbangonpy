from tkinter import *
import tkinter.font as tkFont
from tkinter import ttk
import json
from tkinter import messagebox
import datetime

def printt(message:str):
    print(f"[{datetime.datetime.today().strftime("%Y/%m/%d %H:%M:%S")}]  :  {message}")

def printterror(message:str):
    printt(f"\n\n\n 오류가 발생 하였지만 프로그램을 종류하지 않고 계속 실행합니다. \n {message}\n\n\n")


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

def check_setting_json():
    try:
        data = read_json('setting.json')
        
        # 'setting' 키가 없으면 'setting'을 딕셔너리로 초기화
        if "setting" not in data:
            data["setting"] = {}
            
        # 'api_get_time' 키가 없으면 추가
        if "api_get_time" not in data["setting"]:
            data["setting"]["api_get_time"] = 60

        # 'debugingmod' 키가 없으면 추가
        if "debugingmod" not in data["setting"]:
            data["setting"]["debugingmod"] = False

        # 'font' 키가 없으면 기본값 설정
        if "font" not in data["setting"]:
            data["setting"]["font"] = "굴림"

        # 'font_size' 키가 없으면 기본값 설정
        if "font_size" not in data["setting"]:
            data["setting"]["font_size"] = "none"

        write_json('setting.json', data)  # 수정된 데이터를 다시 저장합니다
    except Exception as e:
        messagebox.showerror("에러 check_setting_json", f"check_setting_json 함수에서 오류가 발생했습니다.\n{e}")

check_setting_json()

# 설정 파일이 존재하지 않거나 "setting" 키가 없을 경우에 대비한 초기값 설정
setting_data = read_json("setting.json")
debug_mod = setting_data.get("setting", {}).get("debugingmod", False)
selected_font = setting_data.get("setting", {}).get("font", "굴림")
font_size = setting_data.get("setting", {}).get("font_size", "none")  # 기본값 추가

def button_debuging_mod_function():
    try:
        data = read_json('setting.json')
        global debug_mod
        debug_mod = not data["setting"].get("debugingmod", False)
        data["setting"]["debugingmod"] = debug_mod
        write_json('setting.json', data)  # 파일 경로를 올바르게 지정
        button_debuging_mod.config(text=f"{debug_mod}")  # 버튼 텍스트 업데이트
    except Exception as e:
        messagebox.showerror("에러 button_debuging_mod_function", f"button_debuging_mod_function 함수에서 오류가 발생했습니다.\n{e}")

def applybutton_api_get_function():
    try:
        data = read_json('setting.json')
        value = input_api_get.get()
        
        # 입력 값이 정수인지 확인하고 변환
        try:
            value = int(value)
        except ValueError:
            messagebox.showwarning("api 간격 사용자 인풋 오류", "API 요청 간격은 정수 타입으로만 설정 가능합니다")
            return
        
        # 최소값 5 확인
        if value <= 5:
            messagebox.showwarning("api 간격 사용자 인풋 오류", "API 요청 간격은 5초 이상으로 설정 가능합니다")
            return
        
        # 데이터 저장
        data["setting"]["api_get_time"] = value
        write_json('setting.json', data)
        
    except Exception as e:
        messagebox.showerror("오류 applybutton_api_get_function", f"applybutton_api_get_function 함수에서 오류가 발생했습니다.\n{e}")

# 폰트를 설정하는 함수
def apply_font():
    try:
        global selected_font
        selected_font = font_combobox.get()
        data = read_json('setting.json')
        data["setting"]["font"] = selected_font
        write_json('setting.json', data)


        try:
            label.config(font=(selected_font, 12, "bold"))
            label_api_get.config(font=(selected_font, 15, "bold"))
            label_debuging_mod.config(font=(selected_font, 13, "bold"))
            applybutton_api_get.config(font=(selected_font, 13, "bold"))
            button_debuging_mod.config(font=(selected_font, 13, "bold"))
        except ValueError:
            messagebox.showwarning("폰트 사이즈 오류", "폰트 사이즈는 정수여야 합니다.")
            return

        messagebox.showinfo("폰트 적용 완료", "폰트가 적용 되었습니다\n일부 텍스트는 다시 시작 시 적용 됩니다")

        printt(f"open_advanced_setting.py  apply_font  {selected_font}")
    except Exception as e:
        messagebox.showerror("오류 apply_font", f"apply_font 함수에서 오류가 발생했습니다.\n{e}")

window_size = {"main" : "600x700" , "setting" : "600x600" , "this":"600x600"}

def window_size_apply_button_function():
    if "x" in input_main_window_size.get():
        window_size["main"] = input_main_window_size.get() or "600x700"
    else:
        window_size["main"] = "600x700"
        
    if "x" in input_setting_window_size.get():  # Corrected here
        window_size["setting"] = input_setting_window_size.get() or "600x600"
    else:
        window_size["setting"] = "600x600"
        
    if "x" in input_this_window_size.get():
        window_size["this"] = input_this_window_size.get() or "600x600"
    else:
        window_size["this"] = "600x600"

    data = read_json('setting.json')
    data['setting']['window_size'] = window_size

    write_json('setting.json' , data)

    printt(f"open_advanced_setting.py  window_size_apply_button_function  {window_size}")


    

tk = Tk()
tk.title("치지직 뱅온 알람기 고급 설정")
tk.geometry(f"{read_json('setting.json')["setting"]["window_size"]["this"]}")

label = Label(text="빨간색 라벨이 있는 값을 수정하면 프로그램에 오류가 생길 수 있습니다", font=(selected_font, 12, "bold"))
label.pack()

frame_1 = Frame(tk)
frame_1.pack(pady=5)

label_api_get = Label(frame_1, text="api 요청 간격 (초)", bg="red", font=(selected_font, 15, "bold"))
label_api_get.grid(row=0, column=0, padx=5)

input_api_get = Entry(frame_1, width=10)
input_api_get.grid(row=0, column=1, padx=5)

applybutton_api_get = Button(frame_1, text="적용", font=(selected_font, 13, "bold"), command=applybutton_api_get_function)
applybutton_api_get.grid(row=0, column=2, padx=5)

frame_2 = Frame(tk)
frame_2.pack(pady=5)

label_debuging_mod = Label(frame_2, text="디버깅 모드를 활성화 / 비활성화 합니다", font=(selected_font, 13, "bold"))
label_debuging_mod.grid(row=0, column=0, padx=5)

# button_debuging_mod의 텍스트 값은 버튼을 누르면 업데이트하기
button_debuging_mod = Button(frame_2, text=f"{debug_mod}", command=button_debuging_mod_function, font=(selected_font, 13, "bold"))
button_debuging_mod.grid(row=0, column=1, padx=5)

frame_3 = Frame(tk)
frame_3.pack(pady=5)

# 폰트 선택 콤보박스 (Combobox)
font_var = StringVar(value=selected_font)
available_fonts = list(tkFont.families())
font_combobox = ttk.Combobox(frame_3, textvariable=font_var, values=available_fonts)
font_combobox.set(selected_font)  # 초기값 설정
font_combobox.grid(row=0, column=0, padx=5)

# 폰트 적용 버튼
apply_font_button = Button(frame_3, text="폰트 적용", command=apply_font, font=(selected_font, 12, "bold"))
apply_font_button.grid(row=0, column=3, padx=5)

frame_4 = Frame(tk)
frame_4.pack(pady=5)
label1 = Label(frame_4,text="창 크기는 (가로)x(세로)로 입력 해주세요(곱하기 아님)", font=(selected_font, 12, "bold"))
label1.grid(row=0, column=0, padx=5)

# 창 크기
frame_5 = Frame(tk)
frame_5.pack(pady=5)

label_this_window_size = Label(frame_5, text="이 창의 크기 : ", font=(selected_font, 12, "bold"))
label_this_window_size.grid(row=0, column=0, padx=5)

input_this_window_size = Entry(frame_5 ,width=10)
input_this_window_size.grid(row=0, column=1, padx=5)

label_setting_window_size = Label(frame_5, text="설정창의 크기 : ", font=(selected_font, 12, "bold"))
label_setting_window_size.grid(row=0, column=2, padx=5)

input_setting_window_size = Entry(frame_5 ,width=10)
input_setting_window_size.grid(row=0, column=3, padx=5)

label_main_window_size = Label(frame_5, text="메인창의 크기 : ", font=(selected_font, 12, "bold"))
label_main_window_size.grid(row=0, column=4, padx=5)

input_main_window_size = Entry(frame_5 ,width=10)
input_main_window_size.grid(row=0, column=5, padx=5)

frame_6 = Frame(tk)
frame_6.pack(pady=5)

window_size_apply_button = Button(frame_6 , text="창 크기 적용", font=(selected_font, 12, "bold"), command=window_size_apply_button_function)
window_size_apply_button.grid(row=0, column=0, padx=5)




tk.mainloop()
