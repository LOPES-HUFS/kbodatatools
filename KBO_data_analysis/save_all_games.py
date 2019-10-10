'''
전체 경기 데이터 저장하는 코드 파일 샘플용 파일이 아닌 2010년부터 2019년 9월까지의 
경기 데이터를 타자와 투수 데이터로 나누어서 저장하는 코드 
'''

import main
import json
import pandas as pd

gameid = pd.read_csv("./data/KBO_gameid_full_season.csv")

gamedict = main.stack_game_data(gameid)

main.write_json(gamedict)

with open("./data/sample/all_data.json", 'r') as outfile:
    playerdata = json.load(outfile)

# 타자 기록을 CSV파일로 저장

def data2dataframe(data:json,datatype:str):
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

    for i in range(0,len(data['fulldata'].keys())):
        away = pd.DataFrame(data['fulldata'][list(data['fulldata'].keys())[i]][f'away_{datatype}'])
        home = pd.DataFrame(data['fulldata'][list(data['fulldata'].keys())[i]][f'home_{datatype}'])
        home['dateindex'] = list(data['fulldata'].keys())[i]
        away['dateindex'] = list(data['fulldata'].keys())[i]
        temp = temp.append(away.append(home))

    temp = temp.fillna(0)
    return temp

batter_temp = data2dataframe(playerdata,batter)

batter_temp['선수명'][batter_temp['선수명']=="페르난데"] = "페르난데스"
batter_temp['선수명'][batter_temp['선수명']=="해즐베이"] = "해즐베이커"
batter_temp['선수명'][batter_temp['선수명']=="스몰린스"] = "스몰린스키"
batter_temp['선수명'][batter_temp['선수명']=="반슬라이"] = "반슬라이크"
batter_temp.to_csv("./data/sample/KBO_batter_data_full.csv",index=False)

# 투수 기록을 CSV파일로 저장

pitcher_temp = data2dataframe(playerdata,pitcher)

pitcher_temp.to_csv("./data/sample/KBO_pitcher_data_full.csv",index=False)