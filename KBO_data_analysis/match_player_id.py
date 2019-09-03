'''
타자 데이터와 투수 데이터에 선수 id를 매치하는 코드 
'''

import pandas as pd
import api.make_id

player_id_list = pd.read_csv("./data/KBO_player_info_full.csv")

batter = pd.read_csv("./data/sample/KBO_batter_data_full.csv")
pitcher = pd.read_csv("./data/sample/KBO_pitcher_data_full.csv")
rename_player = pd.read_csv("./data/renamed_player_list.csv")

# 타자 데이터에 선수 아이디 붙이기  

batterdata = batter.copy()
batterdata["year"] = [i[0:4] for i in batterdata.dateindex]
batterdata["id"] = ""
batter_play_info = batterdata[["선수명","팀","year"]].drop_duplicates()
batter_play_info.index = range(0,len(batter_play_info))

for i in range(0,len(batter_play_info)):
    batterdata = api.make_id.match_id(batterdata,batter_play_info.선수명[i],batter_play_info.year[i],batter_play_info.팀[i])

batterdata.to_csv("./data/sample/KBO_batter_data_full.csv",index=False)

# 투수 데이터에 선수 아이디 붙이기 

pitcherdata = pitcher.copy()
pitcherdata["year"] = [i[0:4] for i in pitcherdata.dateindex]
pitcherdata["id"] = ""
pitcher_play_info = pitcherdata[["선수명","팀","year"]].drop_duplicates()
pitcher_play_info.index = range(0,len(pitcher_play_info))

for i in range(0,len(pitcher_play_info)):
    pitcherdata = api.make_id.match_id(pitcherdata,pitcher_play_info.선수명[i],pitcher_play_info.year[i],pitcher_play_info.팀[i])

pitcherdata.to_csv("./data/sample/KBO_pitcher_data_full.csv",index=False)