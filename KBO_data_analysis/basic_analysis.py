'''
타자 데이터와 투수 데이터 파일을 읽어와 원하는 선수를 찾고 선수의 기록을 확인하는 함수들 
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
    data["month"] = ""
    for i in range(0,len(data['dateindex'])):
        data["month"][i] = int(data['dateindex'][i][4:6])
    return data

# 아래의 함수에서 선수의 id를 확인하고 원하는 선수를 선택할 수 있다. 
def find_player_info(name):
    '''
    기록을 확인하고 싶은 선수의 이름을 입력하여 자신이 원하는 선수의 id를 확인하는 함수 

    Args:
        name(str): 선수 이름

    Returns:
        output(dict): 선수의 id와 연도별 팀 정보가 담긴 딕트 
    '''
    id_list=[]
    data=player_data[player_data['선수명']==name][player_data.columns[0:12]]
    data.index = range(0,len(data))
    for j in range(0,len(data)):
        temp ={}
        id_list.append({"ID":data['ID'].loc[j]})
        for i in range(2010,2020):
            temp.update({i:list(data[data.ID==data['ID'].loc[j]]["season_"+str(i)])[0]})
        id_list[j].update({"seasons":temp})
    
    return id_list

def get_player_data(data,player_id,the_year=None,the_month=None):
    '''
    id와 연도 혹은 월 정보를 가지고 해당 정보의 선수의 데이터를 읽어오는 함수 
    
    Args:
        data(HDF5 table data): hdf5 파일에 저장된 타자나 투수 데이터가 담긴 테이블 
        player_id(int): 선수의 고유 id
        the_year(int): 기본 값은 all로 선수가 경기를 한 전체 연도이며 특정 연도 입력시 해당 연도
        the_month(int): 기본 값은 None으로 전체 월이지만 특정한 월을 지정하면 해당 월
    
    Returns:
        player_data(pandas DF): 조건에 맞는 선수의 경기 기록
    '''
    player_data = data[data.id == player_id]
    player_data = make_date_column(player_data)

    if the_year != None and the_month != None:
        return player_data[(player_data.year==the_year) & (player_data.month==the_month)]
    if the_year != None and the_month == None:
        return player_data[player_data.year==the_year]
    if the_year == None and the_month == None:
        return player_data
    if the_year == None and the_month != None:
        return player_data[player_data.month==the_month]

def what_record(record):
    b_fun=['타율','스탯','타점','득점','안타','1루타','2루타','3루타','홈런','볼넷','4구','몸에맞는공','고의4구','병살','출루율','장타율','희생플라이','희생번트','피삼진']
    p_fun=['방어율','투구수','상대타자수','홀드','세이브','피안타','삼진','피홈런','4사구','자책점','승률','이닝','이닝당투구수','승리','패배','무승부']
    if record in b_fun:
        return "kbo_batter_data"
    elif record in p_fun:
        return "kbo_pitcher_data"
    else:
        return "찾는 기록을 계산할 수 없습니다"

def check_record(data,num1,num2,num3):
    '''
    내부 함수로 코드로 변경된 기록을 보고 개수를 계산하는 함수  
    '''
    data = data[data.columns[0:12]]
    count1 = ['있다' if num1 <= x < num2 else '없다' for x in pd.to_numeric(pd.melt(data)['value'])].count("있다")
    count2 = ['있다' if len(str(x))==8 and str(x)[0:2] == str(num3) else '없다' for x in pd.melt(data)['value']].count("있다")
    count3 = ['있다' if len(str(x))==8 and str(x)[4:6] == str(num3) else '없다' for x in pd.melt(data)['value']].count("있다")
    return count1+count2+count3

def get_AVG(data):
    '''
    타율을 계산하는 함수 기존의 당일 타율과 누적 타율이 있지만 월별,연도별 계산을 위해 함수 작성
    
    Args:
        data(pandas DF): 특정 선수의 타자 데이터 
    
    Returns:
        output(numeric): 선수의 타율 
    '''
    if sum(data['타수'])!= 0:
        return round(sum(data['안타'])/sum(data['타수']),3)
    else:
        return 0

def get_OBP(data):
    '''
    출루을 계산하는 함수 기존의 당일 타율과 누적 타율이 있지만 월별,연도별 계산을 위해 함수 작성
    
    Args:
        data(pandas DF): 특정 선수의 타자 데이터 
    
    Returns:
        output(numeric): 선수의 출루율
    '''
    bb = check_record(data,3200,3300,32)+check_record(data,3000,3100,30)
    hbp = check_record(data,3100,3200,31)
    sf = check_record(data,5000,5006,50)
    obp_temp = sum(data['타수'])+bb+hbp+sf

    if obp_temp != 0:
        return round((sum(data['안타'])+bb+hbp)/obp_temp,3)
    else:
        return 0

def get_SLG(data):
    '''
    장타율 계산하는 함수 기존의 당일 타율과 누적 타율이 있지만 월별,연도별 계산을 위해 함수 작성
    
    Args:
        data(pandas DF): 특정 선수의 타자 데이터 
    
    Returns:
        output(numeric): 선수의 장타율
    '''
    one_b = check_record(data,1000,1029,10)
    two_b = check_record(data,1100,1123,11)
    three_b = check_record(data,1200,1222,12)
    homerun = check_record(data,1300,1305,13)

    if sum(data['타수'])!= 0:
        return round((one_b+2*two_b+3*three_b+4*homerun)/sum(data['타수']),3)
    else:
        return 0

def get_ERA(data):
    '''
    방어율 계산하는 함수 기존의 당일 타율과 누적 타율이 있지만 월별,연도별 계산을 위해 함수 작성
    
    Args:
        data(pandas DF): 특정 선수의 투수 데이터 
    
    Returns:
        output(numeric): 선수의 방어율
    '''
    temp_era = sum(data.inning)+sum(data.restinning)
    if temp_era != 0:
        return round(sum(data['자책'])*9 /temp_era)
    else:
        return 99.99

def get_P_IP(data):
    '''
    이닝당 투구수 계산하는 함수 기존의 당일 타율과 누적 타율이 있지만 월별,연도별 계산을 위해 함수 작성
    
    Args:
        data(pandas DF): 특정 선수의 투수 데이터 
    
    Returns:
        output(numeric): 선수의 이닝당 투구수
    '''
    temp_era = sum(data.inning)+sum(data.restinning)
    if temp_era != 0:
        return round(sum(data['투구수']) /temp_era)
    else:
        return 99.99

def get_WPCT(data):
    '''
    승률 계산하는 함수 기존의 당일 타율과 누적 타율이 있지만 월별,연도별 계산을 위해 함수 작성
    
    Args:
        data(pandas DF): 특정 선수의 투수 데이터 
    
    Returns:
        output(numeric): 선수의 이닝당 투구수
    '''
    temp_wpct = sum(data['승리'])+sum(data['패배'])
    if temp_wpct != 0:
        return round(sum(data.Win) /temp_wpct)
    else:
        return 0

def get_batter_record(data,recordname):
    if recordname == "1루타":
        return check_record(data,1000,1029,10)
    if recordname == "2루타":
        return check_record(data,1100,1123,11)
    if recordname == "3루타":
        return check_record(data,1200,1222,12)
    if recordname == "홈런":
        return check_record(data,1300,1305,13)
    if recordname == "볼넷":
        return check_record(data,3000,3100,30)+check_record(data,3200,3300,32)
    if recordname == "피삼진":
        return check_record(data,2000,2100,20)+check_record(data,2000,2100,21)
    if recordname == "몸에맞는 공":
        return check_record(data,3100,3200,31)
    if recordname == "고의사구":
        return check_record(data,3200,3300,32)
    if recordname == "병살":
        return check_record(data,7200,7227,72)
    if recordname == "희생번트":
        return check_record(data,4100,4106,41)+check_record(data,6100,6108,61)
    if recordname == "희생플라이":
        return check_record(data,5000,5006,50)
    if recordname == "타율":
        return get_AVG(data)
    if recordname == "출루율":
        return get_OBP(data)
    if recordname == "장타율":
        return get_SLG(data)
    if recordname == "타점":
        return sum(data['타점'])
    if recordname == "득점":
        return sum(data['득점'])

def get_pitcher_record(data,recordname):
    if recordname == "방어율":
        return get_ERA(data)
    if recordname == "투구수":
        return sum(data['투구수'])
    if recordname == "타자수":
        return sum(data["타자"])
    if recordname == "홀드":
        return sum(data["홀드"])
    if recordname == "세이브":
        return sum(data['세이브'])
    if recordname == "피안타":
        return sum(data["피안타"])
    if recordname == "삼진":
        return sum(data["삼진"])
    if recordname == "4사구":
        return sum(data["4사구"])
    if recordname == "자책점":
        return sum(data["자책"])
    if recordname == "피홈런":
        return sum(data["홈런"])
    if recordname == "이닝":
        return round(sum(data.inning)+sum(data.restinning)/3,2)
    if recordname == "이닝당투구수":
        return get_P_IP(data)
    if recordname == "승률":
        return get_WPCT(data)
    if recordname == "승":
        return sum(data["승리"])
    if recordname == "패":
        return sum(data['패배'])
    if recordname == "무":
        return sum(data['무승부'])

def get_player_record(**kwargs):
    '''
    사용법: name = "이병규", record="장타율" 등등 이런식으로 인자를 입력하면 사용 가능 

    Args:
        keyword_Args: 
            name(str): 선수이름
            record(str): 타격 혹은 투구 기록
            year(int): 기본값은 None이지만 2010~2019년도 중 하나를 입력하면 해당 년도의 기록 볼 수 있음
            month(int): 기본값은 None이지만 3~10 월 중 하나를 입력하면 해당 월의 기록 볼 수 있음
            id(int): 기본값은 None이지만 특정 선수의 id 입력하면 해당 선수의 기록이 나옴 
    Returns:
        output(pandas DF): 선수의 id와 기록이 있는 데이터 프레임

    '''
    
    if "name" not in kwargs:
        return "선수 이름이 누락되었습니다"
    if "record" not in kwargs:
        return "찾는 기록이 누락되었습니다"
    if kwargs['name'] not in list(player_data['선수명'].unique()):
        return "해당 선수는 2010년에서 2019년 시즌에 경기 기록이 없습니다."
    if "id" in kwargs:
        if  kwargs["id"] not in list(player_data["ID"].unique()):
            return "id가 올바르지 않습니다"
        else:
            if what_record(kwargs['record'])=="kbo_batter_data":
                if 'year' and 'month' not in kwargs:
                     return pd.DataFrame({"id":kwargs["id"],"기록":get_batter_record(get_player_data(batter_data,kwargs['id']),kwargs['record'])},index=[0])
                if 'year' and 'month' in kwargs:
                    player_df = get_player_data(batter_data,kwargs['id'],kwargs['year'],kwargs['month'])
                    if len(player_df) != 0:
                        temp = get_batter_record(player_df,kwargs['record'])
                        return pd.DataFrame({"id":kwargs["id"],"기록":temp,"연도":kwargs['year'],"월":kwargs['month']},index=[0])
                    else:
                        return pd.DataFrame({"id":kwargs["id"],"기록":"출장 기록이 없습니다.","연도":kwargs['year'],"월":kwargs['month']},index=[0])
                if 'year' in kwargs:
                    player_df = get_player_data(batter_data,kwargs['id'],kwargs['year'])
                    if len(player_df) != 0:
                        temp = get_batter_record(player_df,kwargs['record'])
                        return pd.DataFrame({"id":kwargs["id"],"기록":temp,"연도":kwargs['year']},index=[0])
                    else:
                        return pd.DataFrame({"id":kwargs["id"],"기록":"출장 기록이 없습니다.","연도":kwargs['year']},index=[0])
                if 'month' in kwargs:
                    player_df = get_player_data(batter_data,kwargs['id'],None,kwargs['month'])
                    if len(player_df) != 0:
                        temp = get_batter_record(player_df,kwargs['record'])
                        return pd.DataFrame({"id":kwargs["id"],"기록":temp,"월":kwargs['month']},index=[0])
                    else:
                        return pd.DataFrame({"id":kwargs["id"],"기록":"출장 기록이 없습니다.","월":kwargs['month']},index=[0])
            elif what_record(kwargs['record'])=="kbo_pitcher_data":
                if 'year' and 'month' not in kwargs:
                     return pd.DataFrame({"id":kwargs["id"],"기록":get_pitcher_record(get_player_data(pitcher_data,kwargs['id']),kwargs['record'])},index=[0])
                if 'year' and 'month' in kwargs:
                    player_df = get_player_data(pitcher_data,kwargs['id'],kwargs['year'],kwargs['month'])
                    if len(player_df) != 0:
                        temp = get_pitcher_record(player_df,kwargs['record'])
                        return pd.DataFrame({"id":kwargs["id"],"기록":temp,"연도":kwargs['year'],"월":kwargs['month']},index=[0])
                    else:
                        return pd.DataFrame({"id":kwargs["id"],"기록":"출장 기록이 없습니다.","연도":kwargs['year'],"월":kwargs['month']},index=[0])                            
                if 'year' in kwargs:
                    player_df = get_player_data(pitcher_data,kwargs['id'],kwargs['year'])
                    if len(player_df) != 0:
                        temp = get_pitcher_record(player_df,kwargs['record'])
                        return pd.DataFrame({"id":kwargs["id"],"기록":temp,"연도":kwargs['year']},index=[0])
                    else:
                        return pd.DataFrame({"id":kwargs["id"],"기록":"출장 기록이 없습니다.","연도":kwargs['year']},index=[0])      
                if 'month' in kwargs:
                    player_df = get_player_data(pitcher_data,kwargs['id'],None,kwargs['month'])
                    if len(player_df) != 0:
                        temp = get_pitcher_record(player_df,kwargs['record'])
                        return pd.DataFrame({"id":kwargs["id"],"기록":temp,"월":kwargs['month']},index=[0])
                    else:
                        return pd.DataFrame({"id":kwargs["id"],"기록":"출장 기록이 없습니다.","월":kwargs['month']},index=[0])
            else:
                return "이 기록은 현재 데이터로 계산할 수 없습니다"
    if "id" not in kwargs:
        idlists =[i["ID"] for i in find_player_info(kwargs['name'])]
        player_record_df = pd.DataFrame()
        for i in idlists:
            if what_record(kwargs['record'])=="kbo_batter_data":
                if 'year' and 'month' not in kwargs:
                    player_df = get_player_data(batter_data,i)
                    player_record = get_batter_record(player_df,kwargs['record'])
                    temp = pd.DataFrame({"id":i,"기록":player_record},index=[0])
                if 'year' and 'month' in kwargs:
                    player_df = get_player_data(batter_data,i,kwargs['year'],kwargs['month'])
                    if len(player_df) != 0:
                        player_record = get_batter_record(player_df,kwargs['record'])
                        temp = pd.DataFrame({"id":i,"기록":player_record,"연도":kwargs['year'],"월":kwargs['month']},index=[0])
                    else:
                        temp = pd.DataFrame({"id":i,"기록":"출장 기록이 없습니다.","연도":kwargs['year'],"월":kwargs['month']},index=[0])
                if 'year' in kwargs:
                    player_df = get_player_data(batter_data,i,kwargs['year'])
                    if len(player_df) != 0:
                        player_record = get_batter_record(player_df,kwargs['record'])
                        temp = pd.DataFrame({"id":i,"기록":player_record,"연도":kwargs['year']},index=[0])
                    else:
                        temp = pd.DataFrame({"id":i,"기록":"출장 기록이 없습니다.","연도":kwargs['year']},index=[0])
                if 'month' in kwargs:
                    player_df = get_player_data(batter_data,i,None,kwargs['month'])
                    if len(player_df) != 0:
                        player_record = get_batter_record(player_df,kwargs['record'])
                        temp = pd.DataFrame({"id":i,"기록":player_record,"월":kwargs['month']},index=[0])
                    else:
                        temp = pd.DataFrame({"id":i,"기록":"출장 기록이 없습니다.","월":kwargs['month']},index=[0])
            elif what_record(kwargs['record'])=="kbo_pitcher_data":
                if 'year' and 'month' not in kwargs:
                    player_df = get_player_data(pitcher_data,i)
                    player_record = get_pitcher_record(player_df,kwargs['record'])
                    temp = pd.DataFrame({"id":i,"기록":player_record},index=[0])
                if 'year' and 'month' in kwargs:
                    player_df = get_player_data(pitcher_data,i,kwargs['year'],kwargs['month'])
                    if len(player_df) != 0:
                        player_record = get_pitcher_record(player_df,kwargs['record'])
                        temp = pd.DataFrame({"id":i,"기록":player_record,"연도":kwargs['year'],"월":kwargs['month']},index=[0])
                    else:
                        temp = pd.DataFrame({"id":i,"기록":"출장 기록이 없습니다.","연도":kwargs['year'],"월":kwargs['month']},index=[0])
                if 'year' in kwargs:
                    player_df = get_player_data(pitcher_data,i,kwargs['year'])
                    if len(player_df) != 0:
                        player_record = get_pitcher_record(player_df,kwargs['record'])
                        temp = pd.DataFrame({"id":i,"기록":player_record,"연도":kwargs['year']},index=[0])
                    else:
                        temp = pd.DataFrame({"id":i,"기록":"출장 기록이 없습니다.","연도":kwargs['year']},index=[0])
                if 'month' in kwargs:
                    player_df = get_player_data(pitcher_data,i,None,kwargs['month'])
                    if len(player_df) != 0:
                        player_record = get_pitcher_record(player_df,kwargs['record'])
                        temp = pd.DataFrame({"id":i,"기록":player_record,"월":kwargs['month']},index=[0])
                    else:
                        temp = pd.DataFrame({"id":i,"기록":"출장 기록이 없습니다.","월":kwargs['month']},index=[0])
            else:
                return "이 기록은 현재 데이터로 계산할 수 없습니다"
            
            player_record_df = player_record_df.append(temp)
            
        return player_record_df
    

        