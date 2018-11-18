from bs4 import BeautifulSoup
import re
import requests
import json
from operator import itemgetter

#출처 : 일본 성우 갤러리 유튜브 11월의 성우를 발표합니다! (by 루비루)
url = 'http://gall.dcinside.com/board/view?id=japan_voice&no=398491'
#10월 랭킹으로 해도 가능합니다.

#HTML을 통으로 들여오기
rq = requests.get(url)
source = rq.text

#통 HTML을 파이썬에서 가공하기 쉬운 형태(HTML 객체)로 변환
soup = BeautifulSoup(source, 'html.parser')

#find 함수 이용해서 읽어야 하는 부분 찝어주기
text = soup.find('div',{'style':'overflow:hidden;'})
rank = text.findAll('p')

#정규표현식을 이용해서 글을 어떤 식으로 읽어야 하는지 정해주기
#정규표현식:기호 등을 이용해서 텍스트의 형식을 검사하거나 텍스트의 일부를 뽑아내는 것
re_text = r"\d+위 - (\d+)표 (\w+ \w+)"
re_text2 = r"\d+위[ ]?[(](\d+)표[)]"
r = re.compile(re_text)
r2 = re.compile(re_text2)

#다음 명령어들(for)을 위한 미리 변수 선언
etc = False
ranking_data = []

#각 성우별 득표를 리스트로 정리
#rank에 나온 만큼 각각의 것을 ranking으로 집어넣음
for ranking in rank:
    #ranking 뒤에 .text 는 HTML객체이기 때문에 문자열로 변환해줘야 함.
    match = r.search(ranking.text)
    match2 = r2.search(ranking.text)
    #'n위 - n표 아무개' 로 이루어져 있으면 해당 이름과 표수가 등록됨.
    if match :
        data = match.groups()
        seiyu_vote = {
            'name' : data[1],
            'votes' : int(data[0])
            }
        ranking_data.append(seiyu_vote)
    #'n위 (n표)'로 있는 것의 처리(주로 낮은 순위의 성우)
    elif match2 :
        votes = int(match2.group(1))
        etc = True
    elif ranking.text == "":
        etc = False
    elif etc == True :
        seiyu_vote = {
            'name' : ranking.text,
            'votes' : int(votes)
            }
        #성우 각각의 득표수의 리스트에다가 추가함.
        ranking_data.append(seiyu_vote)


#성우 각각 순위를 정리
result = sorted(ranking_data,key=itemgetter('votes'),reverse=True)
#다음 명령어들(for)을 위한 미리 변수 선언
i = 0
votes_bef = 0

#성우 순위를 콘솔에다가 표시
for row in result :
    i += 1
    if row['votes'] != votes_bef :
        num = i
    line = "%s위 - %s(%s)" % (num, row['name'],row['votes'])
    votes_bef = row['votes']
    print(line)
