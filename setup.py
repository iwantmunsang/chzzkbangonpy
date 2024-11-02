import subprocess
import platform
import webbrowser
import tkinter as tk
from tkinter import messagebox, ttk

# 전역 변수
python = False
pythonversion = ""

# Python 설치 여부 확인
def check_python_installed():
    global python, pythonversion
    try:
        # Python 버전을 확인하는 명령어 실행
        result = subprocess.run(["python", "--version"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        pythonversion = result.stdout.decode().strip()
        python = True
        log_message(f"Python is installed: {pythonversion}")
    except subprocess.CalledProcessError:
        log_message("Python is not installed.")
        python = False

# 필수 패키지 설치
def install_required_packages():
    required_packages = ["Pillow", "winotify", "requests" , "pandas"]
    for package in required_packages:
        try:
            log_message(f"Installing {package}...")
            subprocess.run(["pip", "install", package], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            log_message(f"{package} installed successfully.")
        except subprocess.CalledProcessError as e:
            log_message(f"Failed to install {package}: {e}")

# Python 미설치 안내 및 다운로드 링크 제공
def notinstallpython():
    architecture = platform.architecture()[0]
    if not python:
        messagebox.showerror("파이썬 설치 오류", "파이썬이 설치 되어 있지 않습니다.\n파이썬을 설치 해 주세요.")
        if architecture == "64bit":
            webbrowser.open("https://www.python.org/ftp/python/3.12.2/python-3.12.2-amd64.exe")
        elif architecture == "32bit":
            webbrowser.open("https://www.python.org/ftp/python/3.12.2/python-3.12.2.exe")
        else:
            webbrowser.open("https://www.python.org/downloads/release/python-3122/")
    log_message(f"System architecture: {architecture}")

# 로그 메시지를 텍스트 위젯에 추가
def log_message(message):
    log_text.insert(tk.END, message + "\n")
    log_text.see(tk.END)
    root.update_idletasks()

# 프로그램 실행
def run_program():
    log_message("Checking if Python is installed...")
    check_python_installed()
    if python:
        log_message("Installing required packages...")
        install_required_packages()
        log_message("모든 설정이 정상화 되었습니다")
    else:
        notinstallpython()

# UI 생성
root = tk.Tk()
root.title("Python 설치 확인 및 패키지 설치")
root.geometry("400x300")

# 진행 상태 UI 구성
label = ttk.Label(root, text="Python 설치 확인 및 필수 패키지 설치", font=("Arial", 12))
label.pack(pady=10)

log_text = tk.Text(root, height=12, width=50)
log_text.pack(pady=5)

start_button = ttk.Button(root, text="실행", command=run_program)
start_button.pack(pady=10)

# Tkinter 윈도우 실행
root.mainloop()
