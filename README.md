# 치지직 뱅온 알림기

치지직 api를 이용해서 스트리밍 시작시 알람을 보내드려요!!

다른 파일 말고 "치지직 알람기" 바로가기 파일로 열어서 사용해주세요. (바로가기 파일은 위치를 옮기셔도 정상 작동합니다.)
⚠️ app.exe, guiandbackground.exe, stremerlist.json 파일들은 건들지 마세요! 작동에 문제가 생깁니다. ⚠️
목록과 알림 기능은 1분마다 실행되기 때문에 딜레이가 있을 수 있습니다.

채널 추가 방법

	1.설정 버튼을 클릭합니다.
	2.설정창에서 채널 아이디(치지직 채널 아이디 = https://chzzk.naver.com/4325b1d5bbc321fad3042306646e2e50 링크에서 마지막 / 다음 부분 "4325b1d5bbc321fad3042306646e2e50" 이 부분을 말합니다.) 입력
	3.스트리머의 이름을 입력하고 추가 버튼을 누릅니다.
방종 알람 끄기
	설정 => 방종 알람 버튼을 눌러 현재 상태를 false로 만들면 방종 알람이 오지 않습니다.
	반대로 다시 켜려면 버튼을 다시 한번 눌러 주세요.

방종 시, 뱅온 시 메시지
	방종, 뱅온 시 메시지는 알림의 내용을 설정할 수 있는 메시지입니다.
	예시: {name}님이 방송 중입니다!! 제목: {방송 이름} => 방송 중
	현재는 {name} 같은 태그는 사용할 수 없습니다. (1.0.2버전 이하)
	기본값 로드를 눌러 기본값으로 돌릴 수 있습니다.

스트리머 목록 리로드
	치지직 뱅온 알림 창의 오른쪽 아래에 노란 버튼을 눌러 목록을 리로드할 수 있습니다.
	⚠️ 너무 많이 누르면 네이버 측에서 IP를 차단하거나 제재할 수 있으니 너무 많이 누르지 마세요. ⚠️


업데이트 로그

1.0.0BETA
  뭐 한거 없음
1.0.1
  제목이 none으로 뜨던 버그 수정
1.0.2
  뱅종 , 뱅온시 메시지 수정 기능 추가
  스트리머 목록 리로드 기능 추가
  방종 알람 끄기 추가
  프로그램 처음 시작시 방종 알림 안오게 픽스
  각종 버그 픽스
