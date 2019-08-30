'''
hdf5 파일을 읽어와 원하는 선수를 찾고 선수의 기록을 확인하는 함수들 
'''

import pandas as pd
import tables as tb
import make_id

tables = tb.open_file("./data/sample/kbo_data_full.h5","r")

player_data = pd.read_csv("./data/KBO_player_info_full.csv")

def make_date_column(data):
    '''
    날짜 관련된 열을 만들어 주는 함수 
    Args:
        data(pandas DF): 선수의 기록 데이터 

    Returns:
        output(pandas DF): 날짜 관련 정보가 생성된 데이터 
    '''
    data["year"] = ""
    data["month"] = ""
    for i in range(0,len(data['gameinfo'])):
        data["year"][i] = int(data['gameinfo'][i][0:4])
        data["month"][i] = int(data['gameinfo'][i][4:6])
    return data

# 아래의 함수에서 선수의 id를 확인하고 원하는 선수를 선택할 수 있다. 
def find_player_info(name):
    '''
    기록을 확인하고 싶은 선수의 이름을 입력하여 자신이 원하는 선수의 id를 확인하는 함수 
    단 동명이인일 경우 출력된 데이터의 연도별 팀 정보를 보고 id를 스스로 찾아야함 
    예를 들면 큰 이병규(97109)는 2016년 이후에 은퇴로 소속팀이 없고 
    작은이병규(76100)은 16년 이후에도 소속팀이 있다. 는 정보로 원하는 선수의 id를 찾을 수 있다.

    Args:
        name(str): 선수 이름

    Returns:
        output(pandas DF): 선수의 id와 연도별 팀 정보가 담긴 데이터 프레임 
    '''
    return player_data[player_data['선수명']==name]

def get_player_data(data,player_id):
    '''
    id를 토대로 해당 선수의 데이터를 읽어오는 함수 
    
    Args:
        data(HDF5 table data): hdf5 파일에 저장된 타자나 투수 데이터가 담긴 테이블 
        player_id(int): 선수의 고유 id
    
    Returns:
        player_data(pandas DF): 특정한 선수의 경기 기록 전체
    '''
    rows = data.read_where(f'id=={player_id}')
    player_data = pd.DataFrame(rows)
    return player_data

def get_player_data(data,player_id,the_year="all",the_month=None):
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
    rows = data.read_where(f'id=={player_id}')
    player_data = pd.DataFrame(rows)
    player_data = make_date_column(player_data)

    if year != "all" and month != None:
        return player_data[(player_data.year==the_year) & (player_data.month==the_month)]
    if year != "all" and month == None:
        return player_data[player_data.year==the_year]
    if year == "all" and month == None:
        return player_data
    if year == "all" and month != None:
        return player_data[player_data.month==the_month]

def check_record(data,num1,num2,num3):
    '''
    내부 함수로 코드로 변경된 기록을 보고 개수를 계산하는 함수  
    '''
    data = data[data.columns[2:14]]
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
    if sum(data.AB)!= 0:
        return round(sum(data.H)/sum(data.AB),3)
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
    obp_temp = sum(data.AB)+bb+hbp+sf

    if obp_temp != 0:
        return round((sum(data.H)+bb+hbp)/obp_temp,3)
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
    hormrun = check_record(data,1300,1305,13)

    if sum(data.AB)!= 0:
        return round((one_b+2*two_b+3*three_b+4*hormrun)/sum(data.AB),3)
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
        return round(sum(data.ER)*9 /temp_era)
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
        return round(sum(data.PIT) /temp_era)
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
    temp_wpct = sum(data.Win)+sum(data.Lose)
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
    if recordname == "삼진":
        return check_record(data,2000,2100,20)+check_record(data,2000,2100,21)
    if recordname == "몸에맞는 공":
        return check_record(data,3100,3200,31)
    if recordname == "고의4구" or "고의사구":
        return check_record(data,3200,3300,32)
    if recordname == "병살" or "병살타":
        return check_record(data,7200,7227,72)
    if recordname == "희번" or "희생번트":
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
        return sum(data.RBI)
    if recordname == "득점":
        return sum(data.R)

def get_pitcher_record(data,recordname):
    if recordname == "방어율":
        return get_ERA(data)
    if recordname == "투구수":
        return sum(data.PIT)
    if recordname == "타자수":
        return sum(data.NumberofBatter)
    if recordname == "홀드":
        return sum(data.Hold)
    if recordname == "세이브":
        return sum(data.Save)
    if recordname == "피안타":
        return sum(data.H)
    if recordname == "삼진":
        return sum(data.K)
    if recordname == "사사구" or "4사구":
        return sum(data.DeadballAndFourball)
    if recordname == "자책점":
        return sum(data.ER)
    if recordname == "피홈런":
        return sum(data.HR)
    if recordname == "이닝":
        return round(sum(data.inning)+sum(data.restinning)/3,2)
    if recordname == "이닝당투구수":
        return get_P_IP(data)
    if recordname == "승률":
        return get_WPCT(data)
    if recordname == "승":
        return sum(data.Win)
    if recordname == "패":
        return sum(data.Lose)
    if recordname == "무":
        return sum(data.Draw)
    


        