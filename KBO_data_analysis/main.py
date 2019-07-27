'''
gameid를 통해 전체 데이터 크롤링
'''

import .init from get_game, get_data, modify_data
import pandas as pd 
import json

gameid = pd.read_csv("./data/KBO_gameid_season2019.csv")

def stack_game_data(gameid):
    '''
    input: 날짜, 게임id, 원정팀, 홈팀의 정보가 담긴 데이터 프레임
    output: 여러 날짜의 게임 데이터가 담긴 dict  
    '''
    full_data = {}

    for i in range(0,len(gameid)):
        index = str(gameid.date[i])+gameid.gameid[i]
        print(index)
        temp_data = get_data(get_game(date=gameid.date[i], home_team= gameid.home[i], away_team=gameid.away[i]))
        temp_data = modify_data(temp_data)
        full_data.update({index:temp_data})

    return full_data

def write_json(data):
    '''
    input:data는 경기가 담긴 json
    output: json file 
    '''
    temp_file_name = "./data/test_data.json"
    with open(temp_file_name, 'w') as outfile:  
        json.dump(data, outfile)


if __name__ == "__main__":
    gamedict = stack_game_data(gameid)
    write_json(gamedict)



