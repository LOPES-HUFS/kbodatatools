'''
타자 데이터와 투수 데이터를 h5파일로 저장하는 코드
'''
import tables as tb
import pandas as pd

# 타자 데이터를 h5파일에 저장 

batter_data = pd.read_csv("./data/sample/KBO_batter_data_full.csv")

kbo_batter_record = batter_data[["1","2","3","4","5","6","7","8","9","10","11","12","dateindex","타수","안타","타점","득점","타율","id"]]

kbo_batter_copy = kbo_batter_record.copy()
kbo_batter_copy['당일타율'] = kbo_batter_copy['안타']/kbo_batter_copy['타수']
kbo_batter_copy['당일타율'] = kbo_batter_copy['당일타율'].fillna(0)

h5 = tb.open_file("./data/sample/kbo_data_full.h5", 'w')

filters = tb.Filters(complevel=0)

batter_des = {
    'gameinfo': tb.StringCol(13, pos=1),
    'id': tb.IntCol(pos=2),
    'inning_1': tb.IntCol(pos=3),
    'inning_2': tb.IntCol(pos=4),
    'inning_3': tb.IntCol(pos=5),
    'inning_4': tb.IntCol(pos=6),
    'inning_5': tb.IntCol(pos=7),
    'inning_6': tb.IntCol(pos=8),
    'inning_7': tb.IntCol(pos=9),
    'inning_8': tb.IntCol(pos=10),
    'inning_9': tb.IntCol(pos=11),
    'inning_10': tb.IntCol(pos=12),
    'inning_11': tb.IntCol(pos=13),
    'inning_12': tb.IntCol(pos=14),
    "AB": tb.IntCol(pos=15),
    'H': tb.IntCol(pos=16),
    'RBI': tb.IntCol(pos=17),
    'R': tb.IntCol(pos=18),
    'Today_AVG': tb.IntCol(pos=19),
    'AVG': tb.IntCol(pos=20), 
}

tab = h5.create_table('/', 'batter_record', batter_des, title='batter_record', filters=filters)

for i in range(0,len(kbo_batter_copy)):
    tab.row['gameinfo'] = kbo_batter_copy.loc[i]['dateindex']
    tab.row['id'] = kbo_batter_copy.loc[i]['id']
    tab.row['inning_1'] = kbo_batter_copy.loc[i]['1']
    tab.row['inning_2'] = kbo_batter_copy.loc[i]['2']
    tab.row['inning_3'] = kbo_batter_copy.loc[i]['3']
    tab.row['inning_4'] = kbo_batter_copy.loc[i]['4']
    tab.row['inning_5'] = kbo_batter_copy.loc[i]['5']
    tab.row['inning_6'] = kbo_batter_copy.loc[i]['6']
    tab.row['inning_7'] = kbo_batter_copy.loc[i]['7']
    tab.row['inning_8'] = kbo_batter_copy.loc[i]['8']
    tab.row['inning_9'] = kbo_batter_copy.loc[i]['9']
    tab.row['inning_10'] = kbo_batter_copy.loc[i]['10']
    tab.row['inning_11'] = kbo_batter_copy.loc[i]['11']
    tab.row['inning_12'] = kbo_batter_copy.loc[i]['12']
    tab.row['AB'] = kbo_batter_copy.loc[i]['타수']
    tab.row['H'] = kbo_batter_copy.loc[i]['안타']
    tab.row['RBI'] = kbo_batter_copy.loc[i]['타점']
    tab.row['R'] = kbo_batter_copy.loc[i]['득점']
    tab.row['Today_AVG'] = kbo_batter_copy.loc[i]['당일타율']
    tab.row['AVG'] = kbo_batter_copy.loc[i]['타율']
    tab.row.append()
tab.flush()

# 투수 데이터를 h5 파일에 저장 

pitcher_data = pd.read_csv("./data/sample/KBO_pitcher_data_full.csv") 

kbo_pitcher_record = pitcher_data[["dateindex","id","등판","inning","restinning","승리","패배","무승부","삼진","4사구","실점",'자책',"타수","타자","투구수","피안타","홈런","세이브","홀드"]]

pitcher_des = {
    'gameinfo': tb.StringCol(13, pos=1),
    'id': tb.IntCol(pos=2),
    'Mound': tb.IntCol(pos=3),
    'Inning': tb.IntCol(pos=4),
    'Restinning': tb.IntCol(pos=5),
    'Win': tb.IntCol(pos=6),
    'Lose': tb.IntCol(pos=7),
    'Draw': tb.IntCol(pos=8),
    'K': tb.IntCol(pos=9),
    'DeadballAndFourball': tb.IntCol(pos=10),
    'R': tb.IntCol(pos=11),
    'ER': tb.IntCol(pos=12),
    'AB': tb.IntCol(pos=13),
    'NumberofBatter': tb.IntCol(pos=14),
    "PIT": tb.IntCol(pos=15),
    'H': tb.IntCol(pos=16),
    'HR': tb.IntCol(pos=17),
    'Save': tb.IntCol(pos=18),
    'Hold': tb.IntCol(pos=19),
}

tab = h5.create_table('/', 'pitcher_record', pitcher_des, title='pitcher_record', filters=filters)

for i in range(0,len(kbo_pitcher_copy)):
    tab.row['gameinfo'] = kbo_pitcher_copy.loc[i]['dateindex']
    tab.row['id'] = kbo_pitcher_copy.loc[i]['id']
    tab.row['Mound'] = kbo_pitcher_copy.loc[i]['등판']
    tab.row['Inning'] = kbo_pitcher_copy.loc[i]['inning']
    tab.row['Restinning'] = kbo_pitcher_copy.loc[i]['restinning']
    tab.row['Win'] = kbo_pitcher_copy.loc[i]['승리']
    tab.row['Lose'] = kbo_pitcher_copy.loc[i]['패배']
    tab.row['Draw'] = kbo_pitcher_copy.loc[i]['무승부']
    tab.row['K'] = kbo_pitcher_copy.loc[i]['삼진']
    tab.row['DeadballAndFourball'] = kbo_pitcher_copy.loc[i]['4사구']
    tab.row['R'] = kbo_pitcher_copy.loc[i]['실점']
    tab.row['ER'] = kbo_pitcher_copy.loc[i]['자책']
    tab.row['AB'] = kbo_pitcher_copy.loc[i]['타수']
    tab.row['NumberofBatter'] = kbo_pitcher_copy.loc[i]['타자']
    tab.row['PIT'] = kbo_pitcher_copy.loc[i]['투구수']
    tab.row['H'] = kbo_pitcher_copy.loc[i]['피안타']
    tab.row['HR'] = kbo_pitcher_copy.loc[i]['홈런']
    tab.row['Save'] = kbo_pitcher_copy.loc[i]['세이브']
    tab.row['Hold'] = kbo_pitcher_copy.loc[i]['홀드']
    tab.row.append()
tab.flush()