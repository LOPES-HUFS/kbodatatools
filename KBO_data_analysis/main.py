""" KBO 자료를 받아서 JSON 형식으로 바꾸는 메인 모듈
api에 들어 있는 코드을 사용하여 KBO자료를 받아서 저장합니다.


TODO: 함수 설명 인자에 (str) 같은 형식으로 통일
"""

import api 
import pandas as pd 
import json

gameid = pd.read_csv("./data/KBO_gameid_full_season.csv")

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
            temp_data = api.get_data(api.get_game(date=data.date[i], home_team= data.iloc[i].gameid[2:4], away_team=data.iloc[i].gameid[0:2],double=data.iloc[i].gameid[4]))
        except:
            temp_data = api.get_data(api.get_game(date=data.date[i], home_team= data.iloc[i].gameid[2:4], away_team=data.iloc[i].gameid[0:2],double=data.iloc[i].gameid[4]))
        finally: 
            temp_data = api.modify_data(temp_data)
            full_data.update({index:temp_data})

    return {'fulldata':full_data}

def write_json(data):
    '''
    딕트 데이터를 json 파일로 쓰는 함수 

    Args:
        data(dict): 전체 경기 데이터가 담긴 dict 파일  
    Returns:
        json 파일 
    '''
    temp_file_name = "./data/sample/all_data.json"
    with open(temp_file_name, 'w') as outfile:  
        json.dump(data, outfile)


if __name__ == "__main__":
    gamedict = stack_game_data(gameid)
    write_json(gamedict)



