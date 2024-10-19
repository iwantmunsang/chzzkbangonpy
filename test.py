import requests

url = 'https://api.chzzk.naver.com/service/v1/channels/9ae7d38b629b78f48e49fb3106218ff5'

# 해더 설정
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
    'Accept-Language': 'en-US,en;q=0.9',
    'Accept-Encoding': 'gzip, deflate, br',
    'Connection': 'keep-alive',
    'Referer': 'https://www.google.com/',
    'Upgrade-Insecure-Requests': '1'
}

response = requests.get(url, headers=headers)

# 응답을 JSON 형태로 변환
data = response.json()

# content 안에 있는 openlive 값 추출
openlive = data.get('content', {}).get('openLive')

print(f"Open Live: {openlive}")
