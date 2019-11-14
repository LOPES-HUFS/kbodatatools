'''
함수들 몰아서 정리 파일 단순화시키기 
'''

import pandas as pd
from .api import (get_game, get_data, modify_data)
from .make_id import match_id 
import json

def stack_game_data(data):
    '''
    게임 아이디와 날짜를 가지고 전체 게임 데이터를 모아서 저장하는 함수 

    Args:
        data(pandas DF): 날짜와 경기 정보가 담긴 데이터 프레임 
    Returns:
        full_data(dict): 전체 게임 데이터가 담긴 딕트 
    '''
    full_data = {}
    error_list = {}
    for i in range(0,len(data)):
        index = str(data.date[i])+data.gameid[i]
        print(i/len(data))
        try:
            temp_data = get_data(get_game(date=data.date[i], home_team= data.iloc[i].gameid[2:4], away_team=data.iloc[i].gameid[0:2],double=data.iloc[i].gameid[4]))
        except:
            temp_data = get_data(get_game(date=data.date[i], home_team= data.iloc[i].gameid[2:4], away_team=data.iloc[i].gameid[0:2],double=data.iloc[i].gameid[4]))
        finally: 
            temp_data = modify_data(temp_data)
            full_data.update({index:temp_data})
    return full_data
def write_json(data):
    '''
    딕트 데이터를 json 파일로 쓰는 함수 

    Args:
        data(dict): 전체 경기 데이터가 담긴 dict 파일  
    Returns:
        json 파일 
    '''
    temp_file_name = "data/sample/all_data.json"
    with open(temp_file_name, 'w') as outfile:  
        json.dump(data, outfile)


def data2dataframe(data:dict,datatype:str):
    '''
    경기 자료가 담긴 json 데이터를 가지고 pandas Dataframe으로 만드는 함수 
    Args:
        data(dict): 선수들의 경기 자료가 담긴 딕트 또는 json 파일  
        datatype(str): 타자 기록인지 투수 기록인지를 확인하는 인자로 
        타자면 batter 투수면 pitcher를 입력하여 각각 기록을 데이터프레임에 저장할 수 있다
    Returns:
        temp(Pandas DF): 타자기록 또는 투수기록이 일자별로 쌓인 데이터 프레임 
    '''
    temp = pd.DataFrame()

    for i in range(0,len(data.keys())):
        away = pd.DataFrame(data[list(data.keys())[i]][f'away_{datatype}'])
        home = pd.DataFrame(data[list(data.keys())[i]][f'home_{datatype}'])
        home['dateindex'] = list(data.keys())[i]
        away['dateindex'] = list(data.keys())[i]
        temp = temp.append(away.append(home))

    temp = temp.fillna(0)
    return temp

def make_player_id(data):
    '''
    타자나 투수 데이터에 선수 아이디 열을 만들어주는 함수
    Args:
        data(pandas DF): 타자나 투수 선수들의 경기 자료가 담긴 데이터프레임
    Returns:
        tempdata(Pandas DF): 같은 팀에서 활약한 동명이인 선수의 id를 제외한 선수 id가 만들어진 경기 데이터
    '''
    tempdata = data.copy()
    tempdata["year"] = [i[0:4] for i in data.dateindex]
    tempdata["id"] = ""
    player_info = tempdata[["선수명","팀","year"]].drop_duplicates()
    player_info.index = range(0,len(player_info))
    for i in range(0,len(player_info)):
        tempdata = match_id(tempdata,player_info.선수명[i],player_info.year[i],player_info.팀[i])
        
        if player_info.선수명[i] == "페르난데":
            tempdata['선수명'][tempdata['선수명']=="페르난데"] = "페르난데스"
        if player_info.선수명[i] == "해즐베이":
            tempdata['선수명'][tempdata['선수명']=="해즐베이"] = "해즐베이커"
        if player_info.선수명[i] == "스몰린스":
            tempdata['선수명'][tempdata['선수명']=="스몰린스"] = "스몰린스키"
        if player_info.선수명[i] == "반슬라이":
            tempdata['선수명'][tempdata['선수명']=="반슬라이"] = "반슬라이크"
    
    return tempdata

def make_game_info(playerdata,gameid):
    '''
    ETC_info의 정보로 경기 정보 관련 데이터 만드는 함수 

    Args:
        playerdata(json): 전체 시즌(2010-2019) 경기 데이터가 들어있는 json
        gameid(str): 날짜와 원정팀,홈팀 더블헤더 여부로 이루어진 문자열
    Returns:
        output(pandas DF): 구장, 심판, 관중 수, 경기 시작, 진행, 끝 시간이 포함된 경기 정보 데이터프레임
    '''
    date = gameid[0:8]
    away = playerdata['fulldata'][gameid]['scoreboard'][0]['팀']
    home = playerdata['fulldata'][gameid]['scoreboard'][1]['팀']
    doubleheader = gameid[12]
    away_score = playerdata['fulldata'][gameid]['scoreboard'][0]['R']
    home_score = playerdata['fulldata'][gameid]['scoreboard'][1]['R']
    away_result = playerdata['fulldata'][gameid]['scoreboard'][0]['승패']
    home_result = playerdata['fulldata'][gameid]['scoreboard'][1]['승패']
    stadium = playerdata['fulldata'][gameid]["ETC_info"]["구장"]
    spactator = playerdata['fulldata'][gameid]["ETC_info"]["관중"]
    start_time =  playerdata['fulldata'][gameid]["ETC_info"]["개시"]
    end_time = playerdata['fulldata'][gameid]["ETC_info"]["종료"]
    match_time = playerdata['fulldata'][gameid]["ETC_info"]["경기시간"]
    try:
        referee = "_".join(playerdata['fulldata'][gameid]["ETC_info"]["심판"])
    except:
        referee = ""
    temp = pd.DataFrame({"경기날짜":date,"더블헤더":doubleheader,"원정팀":away,"원정팀점수":away_score,"홈팀점수":home_score,"홈팀":home,"원정팀결과":away_result,"홈팀결과":home_result,"구장":stadium,"관중":spactator,"개시":start_time,"종료":end_time,"경기시간":match_time,"심판":referee},index=[0])
    return temp