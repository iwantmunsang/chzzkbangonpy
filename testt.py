import tkinter as tk
from PIL import Image, ImageTk

# 루트 윈도우 생성
root = tk.Tk()
root.title("이미지 표시 예제")

# Frame 생성
frame = tk.Frame(root, width=300, height=300, bg="white")
frame.pack(padx=10, pady=10)

# 이미지 로드 (PIL 사용)
image = Image.open("MDAxNzA1MTY2NzAxMDM0.jxRoo4V4TdOptYggL80STQpPI-gHlzL43jzAaStOnsAg.3xenvZbIgK6vdP82zXdEG3w5X0rrKphOGY0HhTlM_58g.PNG")  # 이미지 경로를 실제 파일 경로로 바꾸세요.
image = image.resize((100, 100))  # 이미지 크기 조절 (선택 사항)
photo = ImageTk.PhotoImage(image)

# Label에 이미지 설정
label = tk.Label(frame, image=photo)
label.image = photo  # 이미지가 가비지 컬렉션 되지 않도록 참조 유지
label.pack()

# 메인 루프 실행
root.mainloop()
