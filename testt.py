import requests

chids = "9e731707f6524b88436c5b3ede3a9848"

headers = {
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.6326.214 Safari/537.36',
                'Accept-Language': 'ko-KR,ko;q=0.9,en-',
                'Accept-Encoding': 'gzip, deflate, br',
                'Connection': 'keep-alive',
                'Referer': 'https://www.google.com/',
                'Upgrade-Insecure-Requests': '1'
                ,'path':"/polling/v1/channels/9e731707f6524b88436c5b3ede3a9848/live-status"
                ,"cookie":"NID_AUT=I3hV+sO6WBTAnaYbF5rjrKxn2O6ExaHcJa4JEHixnQhKguylPfm64WxChHAkKjOZ; NID_JKL=Rhe4poTMgkwrCO3JuEdoukH9eWZf+tVxfmeZvKY93ZA=; NAC=rAu8BQAyG8dZ; NNB=YKSZCL2TLLFWM; BUC=FUnBiNBqw8djUudesjxuJh5_8mG1C-SDq0zNiSLaIfc=; NID_SES=AAABmhb3rc93wNbtsLPBCgcjow6Y45/i60kNcCdaV3H1Q1aou6mVmqYVcVuVqLC9ozoUTGMo0KYEXZAJ3j97+73rjMBTlblPgEpS4Ku+EIuOCI3nlBAg4UNr3amDWsoLhlw43bCr41FYo5MIeYJwDggfC5VJEaXksobgIcvs00t2LlKbKySTB2H+/sJGw4edCzoe6iRePE9roBqydNjhrwoPTjo//Px6prfpGRmpbpwPyUJMvmYidhlpIboOQi0g2Mtns4JWhyAcKcn0E+HjuFeRCBmfkEByynxx7wKDOPf4qUweE9Kk/TqGckTfbjkAylxeKDB6J8vY3Jx1/pGplh3FD/Mbs3NRTIWkW8e3MWaR6o7weDlguVU7+23px9E0BowBLTJa7H6SPScc2RTG5UXCH7QPrjZBtwjEZJ5RYj/CxxB+SLbt/OYVEaE2NU7nuUClFqXdE2AZ9DuahGbQZ/PMiBxOZeu3H1FVv3BWcD2Wozl5Gp59OjkK60aRonpWMMxwr3ilUgXVAqo29nFqqL371VFxuZMviVmGO6QGlpu+aMh3; ba.uuid=0"
            }

url2 = f"https://api.chzzk.naver.com/polling/v1/channels/9e731707f6524b88436c5b3ede3a9848/live-status"

# 요청 보내기
response = requests.get(url2, headers=headers)

# 응답 데이터 확인
# print(response.status_code)
# print(response.json())  # 전체 응답 데이터를 출력해보기

# apidata에 'content'가 있는지 확인 후 추출
apidata = response.json()
content_data = apidata.get('content')
if content_data :
    print("abcc")

if content_data:
    strimingname = content_data.get("liveTitle")
    print(f"Streaming Name: {strimingname}")
else:
    print("No content data available.")
