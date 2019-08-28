'''
샘플용 데이터를 만드는 코드
2019년 7월까지의 경기 자료를 받아오고 자료에서 홈팀과 원정팀의 타자 또는 투수 기록만 
다시 판다스 객체로 저장하여 샘플용 데이터를 만든다.  
'''

import main
import json
import pandas as pd

gameid_2019 = pd.read_csv("./data/sample/KBO_gameid_season2019.csv")

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

temp = temp.fillna(-1)
temp.to_csv("./data/sample/test.csv",index=False)

# 투수기록 

pitcher_temp = pd.DataFrame()

for i in range(0,len(playerdata['fulldata'].keys())):
    away = pd.DataFrame(playerdata['fulldata'][list(playerdata['fulldata'].keys())[i]]['away_pitcher'])
    home = pd.DataFrame(playerdata['fulldata'][list(playerdata['fulldata'].keys())[i]]['home_pitcher'])
    home['dateindex'] = list(playerdata['fulldata'].keys())[i]
    away['dateindex'] = list(playerdata['fulldata'].keys())[i]
    pitcher_temp = pitcher_temp.append(away.append(home))

pitcher_temp = pitcher_temp.fillna(-1)
pitcher_temp.to_csv("./data/sample/test_pitcher.csv",index=False)