from tkinter import *
from tkinter import messagebox

page = 0

def next():
    print(1)

tk = Tk()

tk.geometry("500x400")
tk.title("치지직 뱅온 알림 설정기")

label = Label(tk , text="치지직 알람기 셋업 마법사를 시작합니다." ,font=("굴림",17))
label.pack()

label2 = Label(tk, text="시작 프로그램 설정 하기")

tk.mainloop()