'''
gameid를 통해 전체 데이터 크롤링
'''

import api 
import pandas as pd 
import json

gameid = pd.read_csv("./data/KBO_gameid_full_season.csv")

def stack_game_data(gameid):
    '''
    input: 날짜, 게임id, 원정팀, 홈팀의 정보가 담긴 데이터 프레임
    output: 여러 날짜의 게임 데이터가 담긴 dict  
    '''
    full_data = {}
    error_list = {}
    for i in range(0,len(gameid)):
        index = str(gameid.date[i])+gameid.gameid[i]
        print(index)
        try:
            temp_data = api.get_data(api.get_game(date=gameid.date[i], home_team= gameid.iloc[i].gameid[2:4], away_team=gameid.iloc[i].gameid[0:2],double=gameid.iloc[i].gameid[4]))
        except:
            #error_list.update({date=gameid.date[i], home_team=gameid.iloc[i].gameid[2:4], away_team=gameid.iloc[i].gameid[0:2],double=gameid.iloc[i].gameid[4]})
            temp_data = api.get_data(api.get_game(date=gameid.date[i], home_team= gameid.iloc[i].gameid[2:4], away_team=gameid.iloc[i].gameid[0:2],double=gameid.iloc[i].gameid[4]))
        finally: 
            temp_data = api.modify_data(temp_data)
            full_data.update({index:temp_data})

    return {'fulldata':full_data,'error':error_list}

def write_json(data):
    '''
    input:data는 경기가 담긴 json
    output: json file 
    '''
    temp_file_name = "./data/sample/all_data.json"
    with open(temp_file_name, 'w') as outfile:  
        json.dump(data, outfile)


if __name__ == "__main__":
    gamedict = stack_game_data(gameid)
    write_json(gamedict)



