import pandas as pd

def scoreboard(tables, teams):
    '''html 자료를 스코어 보드로 구성하는 함수
    
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
    '''팀 약자를 가지고 팀 이름을 찾아주는 함수 

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
    ''' 결승타, 도루, 심판 등의 정보를 저장하는 함수

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
    '''html 자료에서 원정팀 타격 기록을 df로 만드는 함수  
    
    Args:
        tables(html): 야구경기 리뷰 테이블이 담긴 html 
        team(html): 경기를 치른 두 팀에 대한 html 
    
    Returns:
        away(pandas DF): 원정팀 타격 기록 df 

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
    '''html 자료에서 홈팀 타격 기록을 df로 만드는 함수  
    
    Args:
        tables(html): 야구경기 리뷰 테이블이 담긴 html 
        team(html): 경기를 치른 두 팀에 대한 html 
    
    Returns:
        home(pandas DF): 홈팀 타격 기록 df 

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
    '''html 자료에서 원정팀 투수 기록을 df로 만드는 함수  
    
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
    '''html 자료에서 홈팀 투수 기록을 df로 만드는 함수  
    
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