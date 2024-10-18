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

# JSON 파일 쓰기
def write_json(file_path, data):
    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)

while True:
    print("치지직 뱅온 알람\n")
    print("1. 스트리머 추가")
    print("2. 스트리머 목록")
    print("3. 스트리머 삭제")
    answer = input()
    if answer == "1":
        try:
            print("스트리머의 채널 아이디를 알려주세요")
            id = input()
            print("스트리머의 이름을 알려주세요")
            name = input()
            print("확인해 주세요!")
            print(f"이름 : {name}\nid : {id}")
            data = read_json(json_file_path)
            data["users"].append({"id": len(data["users"]) + 1, "name": name, "chid": id,"onlive":False})
            write_json(json_file_path, data)
            print("스트리머가 추가되었습니다.")
            print("엔터를 입력하시면 초기 화면으로 돌아 갑니다")
            input()
        except Exception as e:
            print(f"에러 발생: {e}")
    elif answer == "2":
        try:
            data = read_json(json_file_path)
            print("스트리머 목록:")
            for user in data["users"]:
                print(f"이름: {user['name']}, ID: {user['chid']}, onlive: {user['onlive']}")
            print("엔터를 입력하시면 초기 화면으로 돌아 갑니다")
            input()
        except Exception as e:
            print(f"에러 발생: {e}")
    elif answer == "3":
        try:
            data = read_json(json_file_path)
            if not data["users"]:
                print("삭제할 스트리머가 없습니다. 엔터 입력시 초기 화면으로 돌아 갑니다.")
                input()
                continue
            print("삭제할 스트리머의 ID를 입력하세요")
            delete_id = int(input())
            data["users"] = [user for user in data["users"] if user["id"] != delete_id]
            write_json(json_file_path, data)
            print("스트리머가 삭제되었습니다.")
            print("엔터를 입력하시면 초기 화면으로 돌아 갑니다")
            input()
        except Exception as e:
            print(f"에러 발생: {e}")
    else:
        print("잘못된 입력입니다. 초기화면으로 이동합니다.")
