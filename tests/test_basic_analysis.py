'''
기초 분석 함수 테스트 - 이병규(76100,97109(17년은퇴)), 정근우, 이용찬, 허준혁 선수를 예시로 기록이 옳게 계산되는지 테스트한다.
각각 4명의 (년도 기록, 년도와 특정 월 기록) , (통산 기록과 월별 통산 기록은 따로 계산해야함 10년부터 있기 때문)
'''
TODO: "4가지 경우에 대한 4명의 선수 테스트 케이스 작성"

import kbodatatools
from kbodatatools.basic_analysis import (find_player_info,get_player_data,get_record_data)
import pytest
import requests
from bs4 import BeautifulSoup
import lxml


def request_stat(name,birth,opt_num,date_year,date_month):
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
        opt_num(int): 1(연도별),4(상황별)
        date_year(int): 년도
        date_month(str): 월
    Returns:
            output(dict): 스탯티즈의 선수 기록 자료 

    '''
    if opt_num == 1:
        url = f"http://www.statiz.co.kr/player.php?opt=1&name={name}&birth={birth}"
        contents = requests.get(url)
        soup = BeautifulSoup(contents.text, 'lxml')
        colnames = [i.text for i in soup.findAll('th')]
        key = [i for i in list(dict.fromkeys(colnames)) if i not in ['','비율','WAR*','WAR','WPA']]
        if len(key) == 29:
            index=[i for i in range(0,len(soup.findAll('td')[25:-30])) if date_year==soup.findAll('td')[25:-30][i].text]
            value = [i.text for i in soup.findAll('td')[25:-30][index[0]:-2]]
        if len(key) == 30:
            index=[i for i in range(0,len(soup.findAll('td')[25:-31])) if date_year==soup.findAll('td')[25:-31][i].text]
            value = [i.text for i in soup.findAll('td')[25:-31][index[0]:-2]]
    else:
        url = f"http://www.statiz.co.kr/player.php?opt=4&name={name}&birth={birth}&year={date_year}&cv="
        contents = requests.get(url)
        soup = BeautifulSoup(contents.text, 'lxml')
        colnames = [i.text for i in soup.findAll('th')]
        key =  list(dict.fromkeys(colnames))
        if len(key) == 26:
            index = [i for i in range(0,len(soup.findAll('td')[25:])) if str(date_month)+"월"==soup.findAll('td')[25:][i].text]
            value = [i.text for i in soup.findAll('td')[25:][index[0]:index[0]+26]]
        if len(key) == 31:
            index = [i for i in range(0,len(soup.findAll('td')[25:])) if str(date_month)+"월"==soup.findAll('td')[25:][i].text]
            value = [i.text for i in soup.findAll('td')[25:][index[0]:index[0]+31]]
    return dict(zip(key,value))

@pytest.mark.ok
def test_find_player_info():
    idlists = []
    for i in ["정근우","이병규","이용찬","허준혁"]:
        for j in find_player_info(i):
            idlists.append(j["ID"])

    assert idlists == [75808,76100,97109,77211,74556,79535]

@pytest.mark.ok
'''
최근 출전 데이터 출력 테스트
'''
def test_get_player_data_typeone():
    len_list = []
    for i in ["정근우","이병규"]:
        if type(get_player_data(i,"타자")) == dict:
            len_list.extend([len(j)for j in get_player_data(i,"타자").values()])
        else:
            len_list.append(len(get_player_data(i,"타자")))
    for i in ["이용찬","허준혁"]:
        if type(get_player_data(i,"투수")) == dict:
            len_list.extend([len(j)for j in get_player_data(i,"투수").values()])
        else:
            len_list.append(len(get_player_data(i,"투수")))

    assert len_list[0] == int(request_stat("정근우","1982-10-02",1,2019,None)["G"])
    assert len_list[1] == int(request_stat("이병규","1983-10-09",1,2019,None)["G"])
    assert len_list[2] == int(request_stat("이병규","1974-10-25",1,2016,None)["G"])
    assert len_list[3] == int(request_stat("이용찬","1989-01-02",1,2019,None)['출장'])
    assert len_list[4] == int(request_stat("허준혁","1985-12-15",1,2015,None)['출장'])
    assert len_list[5] == int(request_stat("허준혁","1990-09-30",1,2018,None)['출장'])


@pytest.mark.ok
def test_get_player_data_typetwo():
    '''
    특정 날짜의 출전 데이터 출력 테스트
    '''
    len_list = []
    for i in ["정근우","이병규"]:
        if type(get_player_data(i,"타자")) == dict:
            len_list.extend([sum(j["타수"])for j in get_player_data(i,"타자",2015,"05").values()])
        else:
            len_list.append(len(get_player_data(i,"타자",2019,"06")))
    for i in ["이용찬","허준혁"]:
        if type(get_player_data(i,"투수")) == dict:
            len_list.extend([len(j)for j in get_player_data(i,"투수",2014,"05").values()])
        else:
            len_list.append(len(get_player_data(i,"투수",2019,"06")))
    
    assert len_list[0] == int(request_stat("정근우","1982-10-02",4,2019,"06")["타수"])
    assert len_list[1] == int(request_stat("이병규","1983-10-09",4,2015,"05")["타수"])
    assert len_list[2] == int(request_stat("이병규","1974-10-25",4,2015,"05")["타수"])
    assert len_list[3] == int(request_stat("이용찬","1989-01-02",4,2019,"06")['출장'])
    assert len_list[4] == int(request_stat("허준혁","1985-12-15",4,2014,"05")['출장'])
    assert len_list[5] == int(request_stat("허준혁","1990-09-30",4,2014,"05")['출장'])



@pytest.mark.ok
def test_get_record_type1():
    '''
    최근 시즌 기록 출력확인 및 특정년도
    대표적으로 타율이나 방어율을 통해 테스트 
    '''
    record_list = [get_record_data(name=i,record="타율").to_dict("series") for i in ["정근우","이병규"]]
    record_list_p = [get_record_data(name=i,record="방어율").to_dict("series") for i in ["이용찬","허준혁"]]    
    
    assert request_stat("정근우","1982-10-02",1,2019,None)["타율"] in record_list[0]['타율'].values
    assert request_stat("이병규","1983-10-09",1,2019,None)["타율"] in record_list[1]['타율'].values
    assert request_stat("이병규","1974-10-25",1,2016,None)["타율"] in record_list[1]['타율'].values
    assert request_stat("이용찬","1989-01-02",1,2019,None)['ERA'] in record_list_p[0]['방어율'].values
    assert request_stat("허준혁","1985-12-15",1,2015,None)['ERA'] in record_list_p[1]['방어율'].values
    assert request_stat("허준혁","1990-09-30",1,2018,None)['ERA'] in record_list_p[1]['방어율'].values

@pytest.mark.ok
def test_get_record_type2():
    '''
    특정년도의 월 기록 출력 테스트
    대표적으로 타율이나 방어율을 통해 테스트 
    '''
    record_list = [get_record_data(name=i,record="타율",year=2015,month="05").to_dict("series") for i in ["정근우","이병규"]]
    record_list_p = [get_record_data(name=i,record="방어율",,year=2014,month="05").to_dict("series") for i in ["이용찬","허준혁"]]    
    
    assert request_stat("정근우","1982-10-02",4,2015,"05")["타율"] in record_list[0]['타율'].values
    assert request_stat("이병규","1983-10-09",4,2015,"05")["타율"] in record_list[1]['타율'].values
    assert request_stat("이병규","1974-10-25",4,2015,"05")["타율"] in record_list[1]['타율'].values
    assert request_stat("이용찬","1989-01-02",1,2014,"05")['ERA'] in record_list_p[0]['방어율'].values
    assert request_stat("허준혁","1985-12-15",1,2014,"05")['ERA'] in record_list_p[1]['방어율'].values
    assert request_stat("허준혁","1990-09-30",1,2014,"05")['ERA'] in record_list_p[1]['방어율'].values