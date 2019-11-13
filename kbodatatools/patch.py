'''
선수 id 수동 작업 - 패치내역
'''

import pandas as pd

batter_data=pd.read_csv("data/sample/KBO_batter_data_full.csv")
pitcher_data=pd.read_csv("data/sample/KBO_pitcher_data_full.csv")

batter_data.id[(batter_data["id"]==0) & (batter_data["선수명"] == "이승호")] = 70820
batter_data.id[(batter_data["id"]==0) & (batter_data["선수명"] == "허준혁")] = 74556

batter_data['date'] = ""

for i in batter_data.index[(batter_data["id"]==0) & (batter_data["선수명"] == "이병규")]:
    batter_data.date.loc[i] = str(batter_data.year.loc[i])+"-"+ batter_data.dateindex.loc[i][4:6]+"-"+batter_data.dateindex.loc[i][6:8]

data_97109 = pd.read_csv("data/patch_data_97109.csv")
data_76100 = pd.read_csv("data/patch_data_76100.csv")

date_76100=[i for i in list(batter_data.date[(batter_data["선수명"] == "이병규")& (batter_data.id==0)]) if i not in list(data_97109.date)]
date_97109=[i for i in list(batter_data.date[(batter_data["선수명"] == "이병규")& (batter_data.id==0)]) if i not in list(data_76100.date)]

for i in date_76100:
    batter_data.id[(batter_data.date == i)&(batter_data["선수명"] == "이병규")] = 76100

for i in date_97109:
    batter_data.id[(batter_data.date == i)&(batter_data["선수명"] == "이병규")] = 97109

duplicate_date=batter_data.date[(batter_data["선수명"] == "이병규")& (batter_data.id==0)]
duplicate_date=list(duplicate_date.unique())

data_76100_duplicated = pd.DataFrame()
for i in duplicate_date:
    data_76100_duplicated = data_76100_duplicated.append(data_76100[data_76100.date==i])

data_76100_duplicated.columns = ['date','away','home','doubleheader','name','team',"1","2","3","4","5","6","7","8","9",'ten','eleven','twelve','ab','h','rbi','r','id']

def compare_lee_record(gamedate):
    '''
    이병규의 경기기록을 비교 대조해서 어느 기록이 현역 이병규 선수의 기록인지 찾는 함수

    Args:
        gamedate(str): 경기 날짜
    Returns:
        batter_data(pandas DF): 이병규 id가 붙여진 타자 데이터
    '''
    record_index=batter_data[(batter_data["선수명"] == "이병규")&(batter_data.date==gamedate)].index
    record_76100=data_76100_duplicated[data_76100_duplicated.date==gamedate][["1","2","3","4","5","6","7","8","9"]].values.tolist()[0] 
    for i in record_index:
        if list(batter_data.loc[i][["1","2","3","4","5","6","7","8","9"]]) == record_76100:
            print("y")
            batter_data.id.loc[i] = 76100
        else:
            print("n")
            batter_data.id.loc[i] = 97109
    return batter_data

for i in data_76100_duplicated.date:
    batter_data=compare_lee_record(i)

batter_data_full = batter_data[["dateindex","year","선수명","id","팀","포지션","1","2","3","4","5","6","7","8","9","10","11","12","타수","안타","타율","타점","득점"]]

batter_data_full.to_csv("data/sample/KBO_batter_data_full.csv",index=False)

# 투수 id 패치 - 이승호, 허준혁 

pitcher_data['date'] = ""

for i in pitcher_data.index[(pitcher_data["id"]==0) & (pitcher_data["선수명"] == "이승호")]:
    pitcher_data.date.loc[i] = str(pitcher_data.year.loc[i])+"-"+ pitcher_data.dateindex.loc[i][4:6]+"-"+pitcher_data.dateindex.loc[i][6:8]

data_70820 = pd.read_csv("data/patch_data_70820.csv")
data_99137 = pd.read_csv("data/patch_data_99137.csv")

date_70820=[i for i in list(pitcher_data.date[(pitcher_data["선수명"] == "이승호")& (pitcher_data.id==0)]) if i not in list(data_99137.date)]
date_99137=[i for i in list(pitcher_data.date[(pitcher_data["선수명"] == "이승호")& (pitcher_data.id==0)]) if i not in list(data_70820.date)]

for i in date_70820:
    pitcher_data.id[(pitcher_data.date == i)&(pitcher_data["선수명"] == "이승호")] = 70820

for i in date_99137:
    pitcher_data.id[(pitcher_data.date == i)&(pitcher_data["선수명"] == "이승호")] = 99137

duplicate_date = pitcher_data.date[(pitcher_data["선수명"] == "이승호")& (pitcher_data.id==0)].unique()

data_70820_duplicated = pd.DataFrame()
for i in duplicate_date:
    data_70820_duplicated = data_70820_duplicated.append(data_70820[data_70820.date==i])

def pitcher_compare_record(data,name,gamedate,id1,id2):
    '''
    동명이인 투수의 경기기록을 비교 대조해서 어느 기록 누구의 것인지 찾아 id를 붙여주는 함수

    Args:
        data(pandas DF): 같은 날 같은 팀에서 경기한 동명이인 선수의 기록이 있는 데이터
        name(str): 동명이인 선수의 이름
        gamedate(str): 경기 날짜
        id1(int): 두명의 동명이인 선수 id 중 첫 번째
        id2(int): 두명의 동명이인 선수 id 중 두 번째
    Returns:
        pitcher_data(pandas DF): 동명이인인 선수의 기록에 id가 붙여진 투수 데이터
    '''

    record_index=pitcher_data[(pitcher_data["선수명"] == name)&(pitcher_data.date==gamedate)].index
    record_pitch=data[data.date==gamedate][["mound","ab","h","k"]].values.tolist()[0] 
    for i in record_index:
        if list(pitcher_data.loc[i][["등판","타수","피안타","삼진"]]) == record_pitch:
            print("y")
            pitcher_data.id.loc[i] = id1
        else:
            print("n")
            pitcher_data.id.loc[i] = id2
    return pitcher_data

for i in data_70820_duplicated.date:
    pitcher_data = pitcher_compare_record(data_70820_duplicated,"이승호",i,70820,99137)

#허준혁

for i in pitcher_data.index[(pitcher_data["id"]==0) & (pitcher_data["선수명"] == "허준혁")]:
    pitcher_data.date.loc[i] = str(pitcher_data.year.loc[i])+"-"+ pitcher_data.dateindex.loc[i][4:6]+"-"+pitcher_data.dateindex.loc[i][6:8]

data_74556 = pd.read_csv("data/patch_data_74556.csv")
data_79535 = pd.read_csv("data/patch_data_79535.csv")

date_74556 = [i for i in list(pitcher_data.date[(pitcher_data["선수명"] == "허준혁")& (pitcher_data.id==0)]) if i not in list(data_79535.date)]
date_79535 = [i for i in list(pitcher_data.date[(pitcher_data["선수명"] == "허준혁")& (pitcher_data.id==0)]) if i not in list(data_74556.date)]

for i in date_74556:
    pitcher_data.id[(pitcher_data.date == i)&(pitcher_data["선수명"] == "허준혁")] = 74556

for i in date_79535:
    pitcher_data.id[(pitcher_data.date == i)&(pitcher_data["선수명"] == "허준혁")] = 79535


duplicate_date = pitcher_data.date[(pitcher_data["선수명"] == "허준혁")& (pitcher_data.id==0)].unique()

data_74556_duplicated = pd.DataFrame()
for i in duplicate_date:
    data_74556_duplicated = data_74556_duplicated.append(data_74556[data_74556.date==i])

for i in data_74556_duplicated.date:
    pitcher_data = pitcher_compare_record(data_74556_duplicated,"허준혁",i,74556,79535)

pitcher_data.to_csv("data/sample/KBO_pitcher_data_full.csv",index=False)