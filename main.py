'''
gameid를 통해 전체 데이터 크롤링
'''

import api
import pandas as pd 
import json

gameid = pd.read_csv("./data/KBO_gameid_season2019.csv")

full_data = {}

for i in range(0,len(gameid)):
    index = str(gameid.date[i])+gameid.gameid[i]
    print(index)
    temp_data = api.get_data(api.get_game(date=gameid.date[i], home_team= gameid.home[i], away_team=gameid.away[i]))
    temp_data = api.modify_data(temp_data)
    full_data.update({index:temp_data})


temp_file_name = "./data/test_data.json"
with open(temp_file_name, 'w') as outfile:  
    json.dump(full_data, outfile)


    

