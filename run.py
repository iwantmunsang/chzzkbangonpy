# run.py

import subprocess
import datetime
from tkinter import messagebox
import time


def log_to_txt(start_time, end_time, stdout, stderr, is_error=False, error_message=None):
    """기록 내용을 txt 파일에 저장하는 함수"""
    log_content = []
    if is_error:
        log_content.append(f"Start Time: {start_time}")
        log_content.append(f"End Time: {end_time}")
        log_content.append(f"Error: {error_message}")
    else:
        log_content.append(f"Start Time: {start_time}")
        log_content.append(f"End Time: {end_time}")
        log_content.append(f"STDOUT: {stdout if stdout else 'N/A'}")
        log_content.append(f"STDERR: {stderr if stderr else 'N/A'}")
    
    log_content.append("")  # 빈 줄 추가
    with open("debuging/console.txt", "a", encoding="utf-8") as consoletext:  # UTF-8로 수정
        consoletext.write("\n".join(log_content) + "\n")  # 내용 저장



try:
    # 프로세스 실행 시 stdout과 stderr를 UTF-8로 인코딩하여 PIPE로 설정
    process = subprocess.Popen(
        ['python', 'guiandbackground.py'],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        encoding='utf-8',  # 인코딩 지정
        errors='replace',   # 에러 발생 시 대체 문자 사용
        creationflags=0x08000000  # 콘솔 창 숨기기
    )

    # 시작 시간 기록
    start_time = datetime.datetime.today().strftime("%Y/%m/%d %H:%M:%S")

    # 프로세스 종료 대기
    stdout, stderr = process.communicate()

    # 종료 시간 기록
    end_time = datetime.datetime.today().strftime("%Y/%m/%d %H:%M:%S")

    # 기록 파일에 내용 저장
    log_to_txt(start_time, end_time, stdout, stderr)

except Exception as e:
    end_time = datetime.datetime.today().strftime("%Y/%m/%d %H:%M:%S")
    messagebox.showerror('run.py 에러', e)
    
    # 에러 내용을 txt 파일에 기록
    log_to_txt(start_time, end_time, None, None, is_error=True, error_message=str(e))

