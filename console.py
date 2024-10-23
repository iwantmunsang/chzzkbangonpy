# console.py

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
    with open("debuging/console.txt", "a", encoding="UTF-8-sig") as consoletext:
        consoletext.write("\n".join(log_content) + "\n")  # 내용 저장