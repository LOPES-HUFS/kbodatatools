'''
선수 이름
'''
import pandas as pd
import requests
from bs4 import BeautifulSoup
import lxml

def finding_player(name):
    '''
    input
    '''
    error_list= []
    url =f'https://www.koreabaseball.com/Player/Search.aspx?searchWord={name}'
    r = requests.post(url)
    try:
        soup = BeautifulSoup(r.text, "lxml")
        table = soup.find('table')
        table_rows = table.find_all('a')
        temp = [parsing_player(table_row) for table_row in table_rows]
        res = [{item['ID']:item} for item in temp]
        return res
    except:
        error_list.append(name)

def parsing_player(table_row):
    if str(table_row).split('/')[1] == 'Futures':
        status = 'Futures'
    elif str(table_row).split('/')[2] == 'Retire':
        status = '은퇴'
    else:
        status = 'KBO'
    player_id = str(table_row).split('playerId=')[1].split('">')[0]
    name = table_row.get_text()
    return{"ID":player_id, "이름":name, "현재 상태":status}

def request_birth(id):
    '''
    input(int): id는 선수 id로  
    '''
    url = f"https://www.koreabaseball.com/Record/Player/HitterDetail/Total.aspx?playerId={id}"
    response = requests.get(url) 
    print(response.status_code)
    soup = BeautifulSoup(response.text, 'lxml')
    return soup.find_all("span")[9].text

namelist = pd.read_csv("./data/player_name_list.csv",index_col=[0])

player_dict_list = [finding_player(i) for i in namelist['이름']]
player_list=[i[0] for i in player_dict_list]
player_id_df = pd.DataFrame() 

for i in player_list:
    player_id_df=player_id_df.append(pd.DataFrame(i).transpose())
    
player_id_df = player_id_df.drop_duplicates()
player_id_df = player_id_df.sort_values(by=['이름'])
player_id_df.index = range(0,len(player_id_df))

birth=[request_test(i) for i in player_id_df.ID]

player_id_df['생년월일'] = birth

player_id_df.to_csv("./data/new_player_list.csv",index=False)


