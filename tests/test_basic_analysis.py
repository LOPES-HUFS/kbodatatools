'''
기초 분석 함수 테스트 - 이병규(76100,97109(17년은퇴)), 정근우, 이용찬, 허준혁 선수를 예시로 기록이 옳게 계산되는지 테스트한다.
각각 4명의 4가지 경우(통산기록,년도 기록, 년도와 특정 월 기록)
'''
TODO: "4가지 경우에 대한 4명의 선수 테스트 케이스 작성"

import kbodatatools
from kbodatatools.basic_analysis import (find_player_info,get_player_data,get_record_data)
import pytest
import requests
from bs4 import BeautifulSoup
import lxml


def request_stat(name,birth,opt_num,date_year):
    '''
    스탯티즈에서 선수들의 기록을 찾는 함수
    연도별의 경우 통산 기록과 특정 년도 입력시 나오는 것과 비교 가능 
    상황별의 경우 특정 년도의 특정 월 나오는 것과 비교 가능 
    정근우-75808(1982-10-02)
    이병규-76100(1983-10-09) 이병규-97109(1974-10-25) 
    이용찬-77211(1989-01-02)
    허준혁-74556(1985-12-15) 허준혁-79535(1990-09-30)
    Args:
        name(str): 선수의 이름
        birth(str): ex) 1982-05-11 같은 형식의 스트링
        number(int): 1(연도별),4(상황별)
    Returns:


    '''
    if opt_num == 1:
        url = f"http://www.statiz.co.kr/player.php?opt=1&name={name}&birth={birth}"
    elif opt_num == 3:
        url = f"http://www.statiz.co.kr/player.php?opt=3&name={name}&birth={birth}&re=0&se=&da=&year={date_year}&cv="
    else:
        url = f"http://www.statiz.co.kr/player.php?opt=4&name={name}&birth={birth}&re=0&se=&da=&year={date_year}&cv="
    contents = requests.get(url)
    soup = BeautifulSoup(contents.text, 'lxml')
    colnames = [i.text for i in soup.findAll('th')]
    key = [i for i in list(dict.fromkeys(colnames)) if i not in ['','비율','WAR*','WAR','WPA']]
    if len(key) == 29:
        value = [i.text for i in soup.findAll('td')[58:87]]
    if len(key) == 30:
        value = [i.text for i in soup.findAll('td')[59:89]]
    
    return dict(zip(key,value))
        

@pytest.mark.ok
def test_find_player_info():
    idlists = []
    for i in ["정근우","이병규","이용찬","허준혁"]:
        for j in find_player_info(i):
            idlists.append(j["ID"])

    assert idlists == [75808,76100,97109,77211,74556,79535]

@pytest.mark.ok
def test_get_player_data():
    #
    for i in ["정근우","이병규","이용찬","허준혁"]:


@pytest.mark.ok
def test_get_record():
    pass
