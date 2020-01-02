'''
전체 경기의 스코어 보드를 저장하는 코드
'''
import tables as tb
import datetime as dt
import pandas as pd
import json

temp_file_name = "./data/sample/all_data.json"
with open(temp_file_name, 'r') as outfile:
    playerdata = json.load(outfile)

key_list=list(playerdata['fulldata'].keys())

team_list={'기아':'HT','두산':'OB','롯데':'LT','NC':'NC','SK':'SK','LG':'LG','키움':'WO','한화':'HH','삼성':'SS','KT':'KT'}

def change_null_to_negative_number(temp):
    '''
    input
    temp: 스코어보드의 회 정보가 담긴 열들  
    '''
    return(-1 if temp == '-' else temp)

def insult_data(colname,data):
    '''
    input:
    colname(str): 스코어보드 1~12회, 기록 4개 열정보
    data(dict value): 스코어보드의 줄 (for문에서 돌아가는 것)
    '''
    tab.row[colname] = change_null_to_negative_number(data[colname])

def append_table(keys):
    '''
    input:
    keys(str): 전체게임 딕트의 게임정보(날짜와 상대팀이 합쳐진 문자열)와 관련된 데이터
    return: 
    tab(table): 하나의 경기의 스코어보드가 붙여진 테이블
    '''
    for i in playerdata['fulldata'][keys]['scoreboard']:
        tab.row['date'] = keys[0:8]
        tab.row['team'] = team_list[i['팀']]
        [insult_data(j,i) for j in tab.colnames[2:]]
        tab.row.append()
    return tab

h5 = tb.open_file("./data/sample/KBO_scoreboard_full.h5", 'w')

row_des = {
    'date': tb.StringCol(10, pos=1),
    'team': tb.StringCol(2, pos=2),
    '1': tb.IntCol(pos=4),
    '2': tb.IntCol(pos=5),
    '3': tb.IntCol(pos=6),
    '4': tb.IntCol(pos=7),
    '5': tb.IntCol(pos=8),
    '6': tb.IntCol(pos=9),
    '7': tb.IntCol(pos=10),
    '8': tb.IntCol(pos=11),
    '9': tb.IntCol(pos=12),
    '10': tb.IntCol(pos=13),
    '11': tb.IntCol(pos=14),
    '12': tb.IntCol(pos=15),
    'R': tb.IntCol(pos=16),
    'H': tb.IntCol(pos=17),
    'E': tb.IntCol(pos=18),
    'B': tb.IntCol(pos=19)
}

filters = tb.Filters(complevel=0)
tab = h5.create_table('/', 'scoreboard', row_des, title='scoreboard', filters=filters)

for item in key_list:
    tab=append_table(item)
tab.flush()