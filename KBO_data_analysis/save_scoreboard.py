'''
스코어 보드 전체 돌리는 코드
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

def 

def change_null_to_negative_number(temp):
    '''
    input: 스코어보드의 회 정보가 담긴 열들  
    '''
    return(-1 if temp == '-' else temp)

h5 = tb.open_file("test.h5", 'w')

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
    'R': tb.IntCol(pos=15),
    'H': tb.IntCol(pos=15),
    'E': tb.IntCol(pos=15),
    'B': tb.IntCol(pos=15)
}

filters = tb.Filters(complevel=0)
tab = h5.create_table('/', 'scoreboard', row_des, title='scoreboard', filters=filters)

def insult_data(colname,j):
    '''
     1~12회, 기록 4개 경기 없는 경우 -1로 변경
    input(colname): 스코어보드 1~12회, 기록 4개 열정보
    input(j): 스코어보드의 줄 (for문에서 돌아가는 것)
    '''
    tab.row[colname] = change_null_to_negative_number(j[colname])

'''
TODO: for 문을 뭔가 줄여보기  
'''

for i in key_list:
    for j in data['fulldata'][i]['scoreboard']:
        tab.row['date'] = i[0:8]
        tab.row['team'] = team_list[j['팀']]
        [test(k,j) for k in tab.colnames[2:]]
        tab.row.append()
tab.flush()