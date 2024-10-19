import json

# JSON 파일 경로
json_file_path = 'stremerlist.json'

# JSON 파일 읽기 함수
def read_json(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return {"users": []}

# 모든 chid 값을 가져오는 함수
def get_all_chids(data):
    chids = None
    for user in data["users"]:
        chids = user["chid"]
        print (chids)
    return chids

# JSON 데이터 읽기
data = read_json(json_file_path)

# 모든 chid 값 출력
chids = get_all_chids(data)
