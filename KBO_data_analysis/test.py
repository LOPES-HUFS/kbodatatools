'''
샘플용으로 2019년 7월까지의 경기 자료를 받아오고 자료에서 홈팀과 원정팀의 타자 기록만 뽑아서 다시 저장해줍니다.
'''

import main
import json
import pandas as pd

gameid_2019 = pd.read_csv("./data/KBO_gameid_season2019.csv")

gamedict = main.stack_game_data(gameid_2019)

temp_file_name = "./data/sample/test_data.json"
with open(temp_file_name, 'w') as outfile:  
    json.dump(gamedict, outfile)

with open(temp_file_name, 'r') as outfile:
    playerdata = json.load(outfile)

temp = pd.DataFrame()

for i in range(0,len(playerdata['fulldata'].keys())):
    away = pd.DataFrame(playerdata['fulldata'][list(playerdata['fulldata'].keys())[i]]['away_batter'])
    home = pd.DataFrame(playerdata['fulldata'][list(playerdata['fulldata'].keys())[i]]['home_batter'])
    home['dateindex'] = list(playerdata['fulldata'].keys())[i]
    away['dateindex'] = list(playerdata['fulldata'].keys())[i]
    temp = temp.append(away.append(home))

temp.to_csv("./data/sample/test.csv",index=False)


