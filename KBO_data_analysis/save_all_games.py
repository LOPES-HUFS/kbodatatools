'''
전체 데이터 저장하는 코드  
'''

import main
import json
import pandas as pd


#gameid = pd.read_csv("./data/KBO_gameid_full_season.csv")

#gamedict = main.stack_game_data(gameid)

temp_file_name = "./data/sample/all_data.json"
#with open(temp_file_name, 'w') as outfile:  
#    json.dump(gamedict, outfile)

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
temp.to_csv("./data/sample/KBO_normal_season_data_full.csv",index=False)


