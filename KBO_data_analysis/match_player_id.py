'''
플레이어 데이터와 선수 id정보를 일치 시키는 코드
'''

import pandas as pd

player_id_list=pd.read_csv("./data/KBO_player_info_full.csv")

batter = pd.read_csv("./data/sample/KBO_batter_data_full.csv")
pitcher = pd.read_csv("./data/sample/KBO_pitcher_data_full.csv")
rename_player = pd.read_csv("./data/renamed_player_list.csv")

test['선수명'][test['선수명']=="페르난데"] = "페르난데스"
test['선수명'][test['선수명']=="해즐베이"] = "해즐베이커"
test['선수명'][test['선수명']=="스몰린스"] = "스몰린스키"
test['선수명'][test['선수명']=="반슬라이"] = "반슬라이크"

def get_id(name):
    '''
    Args:
        name(str): 선수 이름
    Returns:
        output(list): 입력된 선수 이름의 모든 선수 id (동명이인 포함)
    '''
    return list(player_id_list.ID[player_id_list['선수명']==name])

def find_id(name,year,team):
    '''
    Args:
        name(str): 선수 이름
        year(numeric): 선수가 출장한 경기 연도
        team(str): 선수의 소속팀 
    Returns:
        output(list): 입력된 선수 이름과 연도 팀으로 찾은 선수 id 
    '''
    temp = player_id_list[player_id_list['선수명']==name]
    return [temp.ID[temp["season_"+year]==i].values for i in list(temp["season_"+year]) if team in i]

error = []
def match_id(data,name,year,team):
    '''
    Args:
        name(str): 선수 이름
        year(numeric): 선수가 출장한 경기 연도
        team(str): 선수의 소속팀 
    Returns:
        sampledata(pandas DF): id가 입력된 선수 기록 데이터
    '''
    year = str(year)
    id_list = get_id(name)
    if len(id_list)==1:
        data.id[data["선수명"]==name] = id_list[0]
    elif len(id_list)==0:
        newname = check_rename(name)
        id_list = get_id(newname)
        data.id[data["선수명"]==name] = id_list[0]
    else:
        id_list = list(find_id(name,year,team)[0])
        if len(id_list)>=2:
            print("check_record")
            error.append([name,year,team])
        else:
            data.id[(data["선수명"]==name) & (data.팀.isin([team])) & (data.year.isin([year]))] = id_list[0]
    return(data)

def check_rename(name):
    '''
    Args:
        name(str): 선수 이름
    Returns:
        output(str): 선수의 개명한 이름 또는 "not_rename_player"
    '''
    rename_tmp=rename_player.where(name == rename_player.before_name).dropna()
    if len(rename_tmp) !=0:
        return rename_tmp["rename"].values[0]
    else:
        return "not_rename_player" 

# 타자 데이터에 선수 아이디 붙이기  

batterdata = batter.copy()
batterdata["year"] = [i[0:4] for i in batterdata.dateindex]
batterdata["id"] = ""
batter_play_info = batterdata[["선수명","팀","year"]].drop_duplicates()
batter_play_info.index = range(0,len(batter_play_info))

for i in range(0,len(batter_play_info)):
    batterdata = match_id(batterdata,batter_play_info.선수명[i],batter_play_info.year[i],batter_play_info.팀[i])

# 투수 데이터에 선수 아이디 붙이기 

pitcherdata = pitcher.copy()
pitcherdata["year"] = [i[0:4] for i in pitcherdata.dateindex]
pitcherdata["id"] = ""
pitcher_play_info = pitcherdata[["선수명","팀","year"]].drop_duplicates()
pitcher_play_info.index = range(0,len(pitcher_play_info))

for i in range(0,len(pitcher_play_info)):
    pitcherdata = match_id(pitcherdata,pitcher_play_info.선수명[i],pitcher_play_info.year[i],pitcher_play_info.팀[i])
