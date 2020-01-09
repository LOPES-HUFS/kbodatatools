import pandas as pd
import ast 
from requests_html import HTMLSession
from bs4 import BeautifulSoup

'''
parsing_page 함수들
'''

def scoreboard(tables, teams):
    '''
    html 자료를 스코어 보드로 구성하는 함수
    
    Args:
        tables(html): 야구경기 리뷰 테이블이 담긴 html 
        teams(html): 경기를 치른 두 팀에 대한 html 
    
    Returns:
        temp_total(pandas DF): 두 팀의 경기 기록에 대한 스코어 보드가 pandas df 으로 나옴

    '''

    temp_df_0 = pd.read_html(str(tables[0]))[0]
    temp_df_0 = temp_df_0.rename(columns={"Unnamed: 0":"승패"})
    temp_df_1 = pd.read_html(str(tables[1]))[0]
    temp_df_2 = pd.read_html(str(tables[2]))[0]
    temp_teams = looking_for_teams_name(teams)
    temp_teams_df = pd.DataFrame({'팀':temp_teams})
    temp_total = pd.concat([temp_teams_df, temp_df_0['승패'], temp_df_1, temp_df_2] , axis= 1)
    return(temp_total)

def looking_for_team_name(string):
    '''
    팀 약자를 가지고 팀 이름을 찾아주는 함수 

    Args:
        string(str): 팀 이름 정보가 담긴 html 스트링
    
    Returns:
        temp[1](str): 팀 이름 
    '''
    # 과거 넥센 팀은 현재 키움 히어로즈로 바뀌었기 때문에 2010 ~ 2018년 데이터에서도 키움으로 표시됩니다. 
    team_list={'HT':'기아','OB':'두산','LT':'롯데','NC':'NC','SK':'SK','LG':'LG','WO':'키움','HH':'한화','SS':'삼성','KT':'KT'}
    temp = [string.find(team) for team in team_list.keys()]
    temp[:] = [0 if ele != -1 else ele for ele in temp]
    # -1: 없다 이고 나머지 숫자는 그것이 있는 자리다!
    temp=temp.index(0)
    temp=list(team_list.items())[temp]
    return(temp[1])

def looking_for_teams_name(teams):
    temp_0 = looking_for_team_name(str(teams[0]))
    temp_1 = looking_for_team_name(str(teams[1]))
    return(temp_0, temp_1)

def ETC_info(tables,record_etc):
    ''' 
    결승타, 도루, 심판 등의 정보를 저장하는 함수

    Args:
        tables(html): 야구경기 리뷰 테이블이 담긴 html 자료
        record_etc(html): 결승타, 도루, 심판 등의 정보가 담긴 html 자료
    Returns:
        record(dict): 결승타, 도루자, 심판 등의 정보가 담신 dict 
    '''
    record = {}
    header_list = tables[3].find_all("th")
    if len(header_list)!=0:
        header = [h.get_text(strip=True) for h in header_list]
        data = tables[3].find_all("td")
        etc_data = [d.get_text(strip=True) for d in data]
        record = {header[i]:etc_data[i] for i in range(0,len(header))}
        record.update({key: record[key].split(') ') for key in record.keys() if len(record[key].split(') ')) >=2})
        record['심판'] = record['심판'].split(" ")
    etc={i.split(" : ")[0]:i.split(" : ")[1] for i in record_etc[0].get_text().split("\n") if len(i)!=0 }
    record.update(etc)
    return record

def away_batter(tables, team):
    '''
    html 자료에서 원정팀 타자 기록을 df로 만드는 함수  
    
    Args:
        tables(html): 야구경기 리뷰 테이블이 담긴 html 
        team(html): 경기를 치른 두 팀에 대한 html 
    
    Returns:
        away(pandas DF): 원정팀 타자 기록 df 

    '''
    temp1 = pd.read_html(str(tables[4]))[0].dropna()
    temp1 = temp1.rename(columns={'Unnamed: 1':"포지션"})
    del temp1['Unnamed: 0']
    temp2 = pd.read_html(str(tables[5]))[0][:-1]
    temp3 = pd.read_html(str(tables[6]))[0][:-1]
    away = pd.concat([temp1, temp2, temp3],axis=1)
    away['팀'] = looking_for_team_name(str(team[0]))
    away = away.fillna(0)
    return away

def home_batter(tables, team):
    '''
    html 자료에서 홈팀 타자 기록을 df로 만드는 함수  
    
    Args:
        tables(html): 야구경기 리뷰 테이블이 담긴 html 
        team(html): 경기를 치른 두 팀에 대한 html 
    
    Returns:
        home(pandas DF): 홈팀 타자 기록 df 

    '''

    temp1 = pd.read_html(str(tables[7]))[0].dropna()
    temp1 = temp1.rename(columns={'Unnamed: 1':"포지션"})
    del temp1['Unnamed: 0']
    temp2 = pd.read_html(str(tables[8]))[0][:-1]
    temp3 = pd.read_html(str(tables[9]))[0][:-1]
    home = pd.concat([temp1, temp2, temp3],axis=1)
    home['팀'] = looking_for_team_name(str(team[1]))
    home = home.fillna(0)
    return home

def away_pitcher(tables, team):
    '''
    html 자료에서 원정팀 투수 기록을 df로 만드는 함수  
    
    Args:
        tables(html): 야구경기 리뷰 테이블이 담긴 html 
        team(html): 경기를 치른 두 팀에 대한 html 
    
    Returns:
        away(pandas DF): 원정팀 투수 기록 df 

    '''

    away = pd.read_html(str(tables[10]))[0][:-1]
    away['팀'] = looking_for_team_name(str(team[0]))
    away = away.fillna(0)
    return away

def home_pitcher(tables, team):
    '''
    html 자료에서 홈팀 투수 기록을 df로 만드는 함수  
    
    Args:
        tables(html): 야구경기 리뷰 테이블이 담긴 html 
        team(html): 경기를 치른 두 팀에 대한 html 
    
    Returns:
        home(pandas DF): 홈팀 투수 기록 df 

    '''

    home = pd.read_html(str(tables[11]))[0][:-1]
    home['팀'] = looking_for_team_name(str(team[1]))
    home = home.fillna(0)
    return home

'''
modifying_data 함수들
'''

def change_record(temp,column,factorlist):
    '''
    타자의 이닝별 기록을 숫자 코드로 변경하는 함수 

    Args:
        temp(pandas DF): 타자기록이 저장된 데이터 프레임  
        column(str): 열이름들 중 이닝
        factorlist(pandas DF): 타격 기록에 해당하는 숫자코드

    Returns:
        temp(pandas DF): 타자기록이 숫자코드로 변경된 데이터 프레임
    '''
    for i in range(0,len(temp[[str(column)]])):
        if "/" in list(str(temp[str(column)].tolist()[i])):
            temp1=factorlist.code[factorlist.factor_list==str(temp[str(column)].tolist()[i].split("/ ")[0].split("\\")[0])]
            temp2=factorlist.code[factorlist.factor_list==str(temp[str(column)].tolist()[i].split("/ ")[1])]
            temp.loc[i,str(column)]=str(list(temp1)[0])+str(list(temp2)[0])
    return temp

def batter_clean(data,section):
    '''
    딕트 안에 있는 타자 기록 데이터 프레임을 정리하여 다시 json으로 넣어주는 함수

    Args:
        data(dict): 타자기록이 저장된 딕트  
        section(str): 어떤 타자 기록인지를 지칭 예를 들면 원정팀 타자기록이면 'away_batter'
    
    Returns:
        data(dict): 기존에 입력된 data 중 타자 기록이 보기 좋게 변경되어 저장된 dict

    '''
    temp_b=pd.DataFrame(data[section])
    factorlist = pd.read_csv("/data/KBO_factor_list.csv")
    for i in factorlist.factor_list:
        temp_b=temp_b.replace(i,factorlist.code[factorlist.factor_list==i].tolist()[0])
        
    columns=[x for x in temp_b.columns if x in ['1', '2', '3', '4', '5', '6', '7', '8', '9',"10","11","12"]]
    for j in columns:
        temp_b=change_record(temp_b,j,factorlist)

    data[section]=ast.literal_eval(temp_b.to_json(orient='records'))
    return data

def change_inning(item):
    '''
    투수 데이터의 던진 이닝 수를 분리하는 함수
    '''

    if ('/' and " ") in list(str(item)):
        inning=list(item)[0]
        rest_inning=list(item)[2]
    elif '/' in list(str(item)):
        inning=0
        rest_inning=item.split('\/')[0]
    else:
        inning=item
        rest_inning=0
    
    return [inning,rest_inning]

def pitcher_clean(data,section):
    '''
    투수 기록 df를 보기 좋게 정리하는 함수
    
    Args:
        data(dict): 투수 기록이 저장된 딕트  
        section(str): 어떤 투수 기록인지를 지칭 예를 들면 원정팀 타자기록이면 'away_pitcher'
    
    Returns:
        data(dict): 기존에 입력된 data 중 투수 기록이 보기 좋게 변경되어 저장된 dict

    '''
    temp_p=pd.DataFrame(data[section])
    temp1 = temp_p['등판'] == '선발'
    temp1 = temp1.replace(True,"선발투수")
    temp1 = temp1.replace(False,"불펜투수")
    temp_p['포지션'] = temp1
    temp_p['등판'] = temp_p['등판'].replace('선발',1.1)
    temp_p['결과']= temp_p['결과'].astype(str)
    temp2=temp_p['결과']=='승'
    temp_p['승리'] = temp2.astype(int)
    temp3 = temp_p['결과']=='패'
    temp_p['패배'] = temp3.astype(int)
    temp4 = temp_p['결과']=='무'
    temp_p['무승부'] = temp4.astype(int)
    temp5 = temp_p['결과']=='홀드'
    temp_p['홀드'] = temp5.astype(int)
    temp6 = temp_p['결과']=='세'
    temp_p['세이브'] = temp6.astype(int)
    temp7= temp_p['이닝'].map(lambda x :change_inning(x))
    temp_p['inning'] = temp7.map(lambda x :x[0])
    temp_p['restinning'] = temp7.map(lambda x :x[1])
    temp_p = temp_p[['선수명','포지션','등판','팀','승리', '패배', '무승부', '홀드', '세이브', 'inning', 
            'restinning','4사구','삼진','실점', '자책','투구수','피안타','홈런','타수', '타자']]
    data[section]=ast.literal_eval(temp_p.to_json(orient='records'))
    return data


def get_game(date, home_team, away_team, double=0):
    ''' 
    개별 게임을 가져오는 함수 쉽게 분석할 수 있도록 soup 으로 내보낸다.

    Args:
        date (int): 20190511 과 같이 숫자로 만든 경기 날짜
        home_team (str): 홈팀
        away_team (str): 원정팀
    Returns:
        soup (soup): BeautifulSoup의 soup
    '''
    url = (f'https://www.koreabaseball.com/Schedule/GameCenter/Main.aspx?gameDate={date}&gameId={date}{away_team}{home_team}{double}&section=REVIEW')
    session = HTMLSession()
    r = session.get(url)
    r.html.render()
    soup = BeautifulSoup(r.html.html, "lxml")
    session.close()
    return soup

def get_data(soup):
    '''
    가져온 개별 게임들을 스코어보드 ,타자, 투수 별로 정리 합니다.
    단순하게 사용하는 방법은 다음 링클를 참고합니다.

    https://github.com/LOPES-HUFS/kbodatatools/blob/master/README.md

    Args:
        soup (soup): get_game()으로 받아온 한 경기 자료
    
    Returns:
        temp_all (dict): JSON 형식으로 되어 있는 값이 
        아래와 같은 키로 저장되어 있다.

        scoreboard (스코어 보드)
        ETC_info 
        away_batter (원정팀 타자 정보)
        home_batter (홈팀 타자 정보)
        away_pitcher (원정팀 투수 정보)
        home_pitcher (홈팀 투수 정보) 
    '''

    tables = soup.find_all('table')
    record_etc = soup.findAll('div',{'class':'record-etc'})
    box_score = soup.findAll('div',{'class':'box-score-wrap'})
    teams = box_score[0].findAll('span',{'class':'logo'})
    temp_scoreboard = scoreboard(tables, teams)

    temp_all = {'scoreboard':ast.literal_eval(temp_scoreboard.to_json(orient='records'))}
    temp_all.update({"ETC_info":ETC_info(tables,record_etc)})
    temp_all.update({'away_batter':ast.literal_eval(away_batter(tables,teams).to_json(orient='records'))})
    temp_all.update({'home_batter':ast.literal_eval(home_batter(tables,teams).to_json(orient='records'))})
    temp_all.update({'away_pitcher':ast.literal_eval(away_pitcher(tables,teams).to_json(orient='records'))})
    temp_all.update({'home_pitcher':ast.literal_eval(home_pitcher(tables,teams).to_json(orient='records'))})

    return temp_all 

def modify_data(data):
    '''
    투수와 타자 기록을 보기 좋게 정리합니다. 
    
    Args:
        data: get_data 함수의 return 값 
    
    Returns:
        data: 타자 기록과 투수 기록이 보기 좋게 정리된 dict

    '''  
    data = batter_clean(data,'away_batter')
    data = batter_clean(data,'home_batter')
    data = pitcher_clean(data,'away_pitcher')
    data = pitcher_clean(data,'home_pitcher')

    return(data)