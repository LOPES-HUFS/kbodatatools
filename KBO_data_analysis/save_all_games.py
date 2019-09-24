'''
전체 경기 데이터 저장하는 코드 파일 샘플용 파일이 아닌 2010년부터 2019년 8월까지의 
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

temp = pd.DataFrame()

for i in range(0,len(playerdata['fulldata'].keys())):
    away = pd.DataFrame(playerdata['fulldata'][list(playerdata['fulldata'].keys())[i]]['away_batter'])
    home = pd.DataFrame(playerdata['fulldata'][list(playerdata['fulldata'].keys())[i]]['home_batter'])
    home['dateindex'] = list(playerdata['fulldata'].keys())[i]
    away['dateindex'] = list(playerdata['fulldata'].keys())[i]
    temp = temp.append(away.append(home))

temp = temp.fillna(0)
temp['선수명'][temp['선수명']=="페르난데"] = "페르난데스"
temp['선수명'][temp['선수명']=="해즐베이"] = "해즐베이커"
temp['선수명'][temp['선수명']=="스몰린스"] = "스몰린스키"
temp['선수명'][temp['선수명']=="반슬라이"] = "반슬라이크"
temp.to_csv("./data/sample/KBO_batter_data_full.csv",index=False)

# 투수 기록을 CSV파일로 저장

pitcher_temp = pd.DataFrame()

for i in range(0,len(playerdata['fulldata'].keys())):
    away = pd.DataFrame(playerdata['fulldata'][list(playerdata['fulldata'].keys())[i]]['away_pitcher'])
    home = pd.DataFrame(playerdata['fulldata'][list(playerdata['fulldata'].keys())[i]]['home_pitcher'])
    home['dateindex'] = list(playerdata['fulldata'].keys())[i]
    away['dateindex'] = list(playerdata['fulldata'].keys())[i]
    pitcher_temp = pitcher_temp.append(away.append(home))

pitcher_temp = pitcher_temp.fillna(0)
pitcher_temp.to_csv("./data/sample/KBO_pitcher_data_full.csv",index=False)