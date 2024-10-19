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
    print("치지직 뱅온 알람 설정기\n")
    print("1. 스트리머 추가")
    print("2. 스트리머 목록")
    print("3. 스트리머 삭제")
    print("4. 스트리머 목록 초기화")
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
            data["users"].append({"id": len(data["users"]) + 1, "name": name, "chid": id,"onlive":False,"bangonallrm":False,"bangoffallrm":False})
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
    elif answer == "4":
        import random
        try:
            print("정말로 초기화를 하시겠습니까? 초기화가 진행 돼면 복구가 불가합니다. Y/N")
            a = input()

            if a.lower() == "y":
                monjang = [
                    "망겜이야 어쩌라고 나가",
                    "너이 게이씨 뒷부분은 금지야 금지!",
                    "계약서 깟다구!!",
                    "한탕탕이님 한판 해요",
                    "지리야 가서 코코아좀 타와라",
                    "뿌웅 뭉탱이 월드에 오신걸 환영 합니다",
                    "안녕하세요 저는 트위치에서 방송을 하고 있는 스트리머 케인입니다",
                    "지금부터는"
                ]
                radomm = monjang[random.randrange(0, len(monjang))]
                print(f"이 문장을 따라 입력해주세요 : {radomm}")
                a = input()
                if a == radomm:
                    dataa = data = {
    "users": []
}
                    write_json(json_file_path, dataa)
                    print("스트리머 목록이 초기화 되었습니다.")
                else:
                    print("입력한 문장이 일치하지 않습니다.")
            else:
                print("초기화가 취소되었습니다.")
        except Exception as e:
            print(f"오류 발생 : {e}")

                
    else:
        print("잘못된 입력입니다. 초기화면으로 이동합니다.")
