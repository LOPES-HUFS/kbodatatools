'''
ETC_info에 있는 경기 관련 정보만 뽑아 정리하는 코드 
구장,관중,개시,종료,경기시간,심판 등의 정보와 경기날짜와 원정,홈 구분 
'''

import pandas as pd
import json

temp_file_name = "./data/sample/all_data.json"
with open(temp_file_name, 'r') as outfile:
    playerdata = json.load(outfile)

def make_game_info(gameid):
    '''
    ETC_info의 정보로 경기 정보 관련 데이터 만드는 함수 

    Args:
        gameid(str): 날짜와 원정팀,홈팀 더블헤더 여부로 이루어진 문자열
    Returns:
        output(pandas DF): 구장, 심판, 관중 수, 경기 시작, 진행, 끝 시간이 포함된 경기 정보 데이터프레임
    '''
    ate = gameid[0:8]
    away = gameid[8:10]
    home = gameid[10:12]
    doubleheader = gameid[12]
    stadium = playerdata['fulldata'][gameid]["ETC_info"]["구장"]
    spactator = playerdata['fulldata'][gameid]["ETC_info"]["관중"]
    start_time =  playerdata['fulldata'][gameid]["ETC_info"]["개시"]
    end_time = playerdata['fulldata'][gameid]["ETC_info"]["종료"]
    match_time = playerdata['fulldata'][gameid]["ETC_info"]["경기시간"]
    try:
        referee = "_".join(playerdata['fulldata'][gameid]["ETC_info"]["심판"])
    except:
        referee = ""
    temp = pd.DataFrame({"경기날짜":date,"더블헤더":doubleheader,"원정팀":away,"홈팀":home,"구장":stadium,"관중":spactator,"개시":start_time,"종료":end_time,"경기시간":match_time,"심판":referee},index=[0])
    return temp


game_info_df=pd.DataFrame()
for i in playerdata['fulldata'].keys():
    game_info_df = game_info_df.append(make_game_info(i))
    
game_info_df.index = range(0,len(game_info_df))

game_info_df.to_csv("/data/sample/KBO_game_info_data.csv",index=False)