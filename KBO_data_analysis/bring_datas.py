'''
데이터를 열어서 분석 함수를 사용하기 전의 상태로 만들어 줍니다. 
'''

import pandas as pd

batter_data = pd.read_csv("./data/sample/KBO_batter_data_full.csv")
pitcher_data = pd.read_csv("./data/sample/KBO_pitcher_data_full.csv")
player_data = pd.read_csv("./data/KBO_player_info_full.csv")

def make_month_column(data):
    '''
    월 관련된 열을 만들어 주는 함수 
    Args:
        data(pandas DF): 선수의 기록 데이터 

    Returns:
        output(pandas DF): 날짜 관련 정보가 생성된 데이터 
    '''
    data["month"] = [i[4:6] for i in data.dateindex]
    return data

batter = batter_data.copy()
pitcher = pitcher_data.copy()

batter = make_month_column(batter)
pitcher = make_month_column(pitcher)