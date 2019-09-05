'''
선수 id 수동 작업 - 패치내역
'''

import pandas as pd

batter_data=pd.read_csv("./data/sample/KBO_batter_data_full.csv")
pitcher_data=pd.read_csv("./data/sample/KBO_pitcher_data_full.csv")

batter_data.id[(batter_data["id"]==0) & (batter_data["선수명"] == "이승호")] = 70820
batter_data.id[(batter_data["id"]==0) & (batter_data["선수명"] == "허준혁")] = 74556

batter_data['date'] = ""

for i in batter_data.index[(batter_data["id"]==0) & (batter_data["선수명"] == "이병규")]:
    batter_data.date.loc[i] = str(batter_data.year.loc[i])+"-"+ batter_data.dateindex.loc[i][4:6]+"-"+batter_data.dateindex.loc[i][6:8]


data_97109 = pd.read_csv("./data/patch_file/data_97109.csv")
data_76100 = pd.read_csv("./data/patch_file/data_76100.csv")

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
    batter_data=compare_record(i)

# 이승호 허준혁 도 마찬가지로 진행 ㄱ 

