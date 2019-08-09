'''
선수 이름으로 선수 id를 만들고, 선수 id를 이용해 생년 월일을 찾아 동명이인 구분을 해준다.
만들어진 선수 id 정보 데이터로 동명이인이 아닌 선수들과 id를 매치시킨다.
만약 동명이인인 선수가 있다면 데이터에 있는 정보를 가지고 선수의 기록과 비교하여 id를 매치한다.
TODO: 동명이인과 은퇴한 선수들의 경기기록일 경우 어떻게 id 붙일지 고민 - 전체 데이터를 가지고 해볼 것 
일단 현역 동명이인 애들부터 처리하는거 고민 ! 
'''

import pandas as pd
import requests
from bs4 import BeautifulSoup
import lxml

test_name = pd.read_csv("./data/new_player_list.csv")

def get_id(name):
    '''
    input(string): 선수 이름
    output(list): 입력된 선수 이름의 모든 선수 id (동명이인 포함)
    '''
    return list(test_name.ID[test_name['이름']==name])

def find_id(name):
'''
선수이름을 통해 id를 찾는 함수로 선수 이름이 고유하면 해당 선수의 id 바로 출력
만약 선수 이름이 고유하지 않으면 현재 은퇴 경우를 따져서 현역 선수 중 고유한 이름이면 선수 id 출력
현역 선수들 중에도 이름이 중복될 경우 check player status를 출력 
주의: 이 함수는 현재 시즌 데이터에만 사용 가능 

input(string): name은 선수이름으로 한글 문자열 형식
output(int): 선수의 id, 선수 이름이 동명이인이면 동명이인 선수의 id까지 모두 출력
'''
if len(get_id(name))== 1:
    return get_id(name)[0]
elif len(get_id(name)) > 1:
    samename = test_name[test_name['이름']==name]
    if len(samename.ID[samename['현재 상태']=="KBO"]) ==1:
        return list(samename.ID[samename['현재 상태']=="KBO"])[0]
    else:
        return("check player status")
    

def check_player_position(id):
    '''
    TODO: 현역 투수와 현역 타자 선수 간 동명이인 구분용 함수 여기에 은퇴한 선수와 투수 간 구분도 필요 
    '''
    url = f"https://www.koreabaseball.com/Record/Player/HitterDetail/Daily.aspx?playerId={id}"
    r = requests.post(url)
    soup = BeautifulSoup(r.text, "lxml")
    
    if soup.find_all("td")[0].text == '기록이 없습니다.':
        return "투수 id이거나 은퇴한 선수입니다"
    else:
        return "현역 타자 id 입니다"


def make_player_data(id):
    '''
    현재 선수 id가 투수나 은퇴한 선수의 id일 경우 에러 발생
    동명이인 선수의 시즌 경기 기록을 조회하기 위한 함수 
    input(string): 선수의 id 
    output(dataframe): 선수의 시즌 월별 경기기록 데이터 프레임
    TODO: 동명이인 선수들 id 이름 있는 dict 활용해서 현역 타자 선수들 id 넣기해야함 
    '''

    url = f"https://www.koreabaseball.com/Record/Player/HitterDetail/Daily.aspx?playerId={id}"
    r = requests.post(url)
    soup = BeautifulSoup(r.text, "lxml")
    th = soup.find_all('th')
    tr = soup.find_all('tr') 
    col = [i.find("a").text for i in th if i.find("a") != None]
    col = list(dict.fromkeys(col))
    col.insert(0,"월")
    col.insert(1,"상대")
    temp = [i.text.split("\n")[1:-1] for i in tr if not i.text.find("\n")]
    data = [i for i in temp if "상대"  not in i]
    return pd.DataFrame(data,columns=col)


sample = pd.read_csv("./data/sample/test.csv")
sampledata = sample.copy()
samenamelist = []

for i in sample['선수명']:
    if find_id(i) == "check player status":
        samenamelist.append(i)
        sampledata.id[sampledata['선수명']==i] = 0
    else:
        sampledata.id[sampledata['선수명']==i] = find_id(i)

samename_dict={}
for i in samenamelist:
    for j in get_id(i):
        samename_dict.update({j:{i:check_player_position(j)}})

for i,j in samename_dict.items():
    if list(j.values())[0]=="현역 타자 id 입니다":
        print(i,list(j.keys())[0])