import os
import requests
from PIL import Image
import time

# 이미지를 다운로드하고 저장하는 함수
def imge(link: str, name: str, save_path: str = "."):
    """
    link: 다운로드할 이미지 URL
    name: 저장할 이미지 파일 이름
    save_path: 저장할 경로 (기본값은 현재 디렉토리)
    """
    url = f"{link}"
    
    # 경로에 디렉토리가 없다면 생성
    if not os.path.exists(save_path):
        os.makedirs(save_path)
    
    # 파일 경로 설정
    file_path = os.path.join(save_path, name)
    
    # 시간 체크 시작
    start = time.time()

    # 이미지 다운로드
    response = requests.get(url)
    with open(file_path, "wb") as f:
        f.write(response.content)

    # 이미지 다운로드 시간 체크
    print("다운로드 시간:", time.time() - start)


    print(f"이미지가 {save_path}에 저장되었습니다.")

# 예시 호출
# image_url = "https://dispatch.cdnser.be/cms-content/uploads/2020/04/09/a26f4b7b-9769-49dd-aed3-b7067fbc5a8c.jpg"
# image_name = "downloaded_image.jpg"
# save_directory = "images"  # 저장할 폴더 경로

# # 이미지를 다운로드하고 저장
# saved_image_path = imge(image_url, image_name, save_directory)
