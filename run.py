import subprocess

# Popen을 사용하여 프로세스를 실행합니다.
process = subprocess.Popen(['python', 'guiandbackground.py'])

# 필요한 경우, 프로세스가 종료될 때까지 기다릴 수 있습니다.
process.wait()
