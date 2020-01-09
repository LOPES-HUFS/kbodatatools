'''
타자 데이터와 투수 데이터 파일을 읽어와 원하는 선수를 찾고 선수의 기록을 확인하는 함수들 
'''

import pandas as pd
import tables as tb 
import os 

def check_rawdata():
    '''
    데이터 다운 코드 실행 여부 검사하는 함수 
    '''
    if 'KBO_batter_data_full.csv' and 'KBO_pitcher_data_full.csv' in os.listdir("./data"):
        batterdata = pd.read_csv("./data/KBO_batter_data_full.csv")
        pitcherdata = pd.read_csv("./data/KBO_pitcher_data_full.csv")
        return {"batter":batterdata,"pitcher":pitcherdata}
    else:
        fulldata = tb.open_file("./data/KBO_full_data.h5","r")
        batterdata = pd.DataFrame(fulldata.get_node('/')['batter_data'][:])
        pitcherdata = pd.DataFrame(fulldata.get_node('/')['pitcherdata'][:])
        return {"batter":batterdata,"pitcher":pitcherdata}


def get_data():
    base_data = check_rawdata
    player_data = pd.read_csv("./data/KBO_player_info_full.csv")
    base_data.update({"player_data":player_data})
    return base_data

# 아래의 함수에서 선수의 id를 확인하고 원하는 선수를 선택할 수 있다. 
def find_player_info(name):
    '''
    기록을 확인하고 싶은 선수의 이름을 입력하여 자신이 원하는 선수의 id를 확인하는 함수 

    Args:
        name(str): 선수 이름

    Returns:
        idlist(list): 선수의 id와 연도별 팀 정보가 담긴 리스트로 리스트 안의 값은 딕트로 구성
    '''
    id_list=[]
    data = get_data()
    player_data = data['player_data']
    data = player_data[player_data['선수명']==name][player_data.columns[0:12]]
    data.index = range(0,len(data))
    for j in range(0,len(data)):
        temp ={}
        id_list.append({"ID":data['ID'].loc[j]})
        for i in range(2010,2020):
            temp.update({i:list(data[data.ID==data['ID'].loc[j]]["season_"+str(i)])[0]})
        id_list[j].update({"seasons":temp})
    return id_list

def check_position(data,record):
    '''
    들어온 데이터가 타격 기록 데이터인지 투구 기록 데이터인지 구분하는 함수
    '''
    if len(data) != 0 and hasattr(data, '등판')==False:
        return get_batter_record(data,record)
    if len(data) != 0 and hasattr(data, '등판')==True:
        return get_pitcher_record(data,record)
    if len(data) == 0:
        return "출장 기록이 없습니다."
    
def what_record(record):
    '''
    입력된 기록이 타격 관련 기록인지 투구 관련 기록인지 구분하는 함수 
    '''
    b_fun=['타율','타점','득점','안타','1루타','2루타','3루타','홈런','볼넷','4구','몸에맞는공','고의4구','병살','출루율','장타율','희생플라이','희생번트','피삼진']
    p_fun=['방어율','투구수','타자수','홀드','세이브','피안타','삼진','피홈런','4사구','자책점','승률','이닝','이닝당투구수','승리','패배','무승부']
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
    data = data[['1','2','3','4','5','6','7','8','9','10','11','12']]
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
    temp_era = sum(data.inning)+sum(data.restinning)/3
    if temp_era != 0:
        return round(sum(data['자책'])*9 /temp_era,3)
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
    temp_era = sum(data.inning)+sum(data.restinning)/3
    if temp_era != 0:
        return round(sum(data['투구수']) /temp_era,3)
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
        return round(sum(data['승리']) /temp_wpct,3)
    else:
        return 0

def get_batter_record(data,recordname):
    '''
    타자의 타격 기록을 찾고 계산하는 함수
    Args:
        data(pandas DF): 특정한 어떤 타자 선수의 타격 데이터 
        recordname(str): 타격기록  

    Returns:
        예를 들어 타율이면 입력한 데이터를 기반으로 해당 선수의 타율을 계산
        output(numeric): 선수의 입력한 타격 기록 
    '''
    if recordname == "1루타":
        return check_record(data,1000,1029,10)
    if recordname == "2루타":
        return check_record(data,1100,1123,11)
    if recordname == "3루타":
        return check_record(data,1200,1222,12)
    if recordname == "홈런":
        return check_record(data,1300,1305,13)
    if recordname in ["볼넷","4구"]:
        return check_record(data,3000,3100,30)+check_record(data,3200,3300,32)
    if recordname == "피삼진":
        return check_record(data,2000,2100,20)+check_record(data,2000,2100,21)
    if recordname == "몸에맞는공":
        return check_record(data,3100,3200,31)
    if recordname == "고의4구":
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
    if recordname == "안타":
        return sum(data['안타'])

def get_pitcher_record(data,recordname):
    '''
    투수의 투구 기록을 찾고 계산하는 함수
    Args:
        data(pandas DF): 특정한 어떤 투수 선수의 투구 데이터 
        recordname(str): 투구기록  

    Returns:
        예를 들어 방어율이면 입력한 데이터를 기반으로 해당 선수의 방어율을 계산
        output(numeric): 선수의 입력한 투구 기록 
    '''
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
        return round(sum(data.inning)+sum(data.restinning)/3,3)
    if recordname == "이닝당투구수":
        return get_P_IP(data)
    if recordname == "승률":
        return get_WPCT(data)
    if recordname in ["승리","승"]:
        return sum(data["승리"])
    if recordname in ["패배","패"]:
        return sum(data['패배'])
    if recordname in ["무","무승부"]:
        return sum(data['무승부'])

def check_date(data,theyear=None,themonth=None,full=False):
    '''
    년도와 월 인자를 검사하는 함수이다.
    Args:
        data(pandas DF): 타자 또는 투수 데이터 
        year(int): 찾는 년도로 없는 경우 최근 년도로 지정
        month(str): 입력은 06과 같은 스트링 타입 찾는 월로 없는 경우 년도별 정규시즌의 모든 월로 지정
        full(boolean): False가 기본 값으로 True 입력시 전체 데이터 반환 
    Returns:
       output(pandas DF): 입력받은 년도하고 월에 따라 추출된 타자 또는 투수 데이터 
    '''

    if full == True:
        return data
    else:
        if theyear is None and themonth is None:
            return data[data.year == max(data.year)]
        if theyear is not None and themonth is None:
            return data[data.year == theyear]
        if theyear is None and themonth is not None:
            return data[data.month == themonth]
        if theyear is not None and themonth is not None:
            return data[(data.year==theyear)&(data.month == themonth)]

def get_player_data(data,name,year=None,month=None,full=False):
    '''
    선수의 이름과 타자인지 투수인지 정보를 입력하면 해당 선수의 전체 출전 데이터를 출력하는 함수
    기본적으로 선수가 경기를 출전한 가장 최근 시즌의 데이터가 나옵니다. 
    선수가 출전한 모든 기록을 보고 싶다면 년도와 월을 입력하지 않고 full 인자를 True로 설정하면
    모든 출전 데이터가 나옵니다.
    단 년도와 월을 입력하면 입력된 정보의 선수 출전 데이터를 출력합니다. 
    만약 년도만 입력하면 해당 년도의 모든 출전 데이터가 나오고
    월만 입력하면 2010년부터 2019년까지 해당 월의 모든 출전 데이터가 나옵니다.
    년도와 월을 동시에 입력할 경우 예를 들면 인자가 2019, 5인 경우에는 2019시즌 5월의 일자별 데이터가 나옵니다.  
    Args:
        data(pandas DF): 타자 또는 투수 데이터
        name(str): 찾는 선수의 이름 
        year(int): 찾는 년도로 없는 경우 기본값은 None으로 2010~2019년도 전체로 지정
        month(str): 찾는 월로 입력 형태는 06과 같은 형태 입력이 없는 경우 기본값은 None으로 년도별 정규시즌의 모든 월로 지정 
        full(boolean): True 면 모든 출전 기록 False가 기본 값
    Returns:
        output(dict or pandas DF):입력받은 년도하고 월에 따라 추출된 타자 또는 투수 데이터
                                단 동명이인 있는 선수일 경우 dict 형식으로 출력 
    '''
    idlists =[i["ID"] for i in find_player_info(name)]
    if len(idlists) == 1:
        data = data[data.id == idlists[0]]
        return check_date(data,year,month,full) 
    elif len(idlists) > 1:
        save_dict = {}
        for i in idlists:
            playdata = data[data.id == i]
            save_dict.update({i:check_date(playdata,year,month,full)})
        return save_dict
    else:
        return "에러:찾는 선수의 이름이 잘못되었거나 해당 날짜에 출전 기록이 없습니다."


        
def arg_test(temp_dict):
    '''
    연도와 월이 인자로 입력되어 있는지 검사하는 함수 
    
    Args:
        data(pandas DF): 특정 선수의 기록 데이터
        temp_dict(dict): kwargs에서 받은 인자가 담긴 딕트  
    Returns:
        output(pandas DF): 선수의 id와 기록이 있는 데이터 프레임
    '''
    keylist = list(temp_dict.keys())
    data = temp_dict['data']
    selected_player_data = data[data.id == temp_dict['id']]
    if len(selected_player_data) == 0:
        return "출장 기록이 없습니다."
    if 'year' not in keylist and 'month' not in keylist:
        player_df = selected_player_data[(selected_player_data.year==max(selected_player_data.year))]
        return pd.DataFrame({"name":temp_dict['name'],"id":temp_dict["id"],temp_dict['record']:check_position(player_df,temp_dict['record']),"최근시즌":max(selected_player_data.year)},index=[0])
    if 'year' in keylist and 'month' in keylist:
        player_df = selected_player_data[(selected_player_data.year==temp_dict['year']) & (selected_player_data.month==temp_dict['month'])]
        return pd.DataFrame({"name":temp_dict['name'],"id":temp_dict["id"],temp_dict['record']:check_position(player_df,temp_dict['record']),"년도":temp_dict['year'],"월":temp_dict['month']},index=[0])
    if 'year' in keylist:
        player_df = selected_player_data[selected_player_data.year==temp_dict['year']]
        return pd.DataFrame({"name":temp_dict['name'],"id":temp_dict["id"],temp_dict['record']:check_position(player_df,temp_dict['record']),"년도":temp_dict['year']},index=[0])
    if 'year' not in keylist and 'month' in keylist:
        player_df = selected_player_data[selected_player_data.month==temp_dict['month']]   
        return pd.DataFrame({"name":temp_dict['name'],"id":temp_dict["id"],temp_dict['record']:check_position(player_df,temp_dict['record']),"월":temp_dict['month']},index=[0])
    
def get_record_data(**kwargs):
    '''
    사용법: data = batter,name = "이병규", record="장타율" 등등 이런식으로 인자를 입력하면 사용 가능 

    Args:
        keyword_Args:
            data(pandas): 타자 또는 투수 데이터가 있는 데이터 프레임 
            name(str): 선수이름
            record(str): 타격 혹은 투구 기록
            year(int): 기본값은 None이지만 2010~2019년도 중 하나를 입력하면 해당 년도의 기록 볼 수 있음
            month(str): 기본값은 None이지만 3~10 월 중 하나를 입력하면 해당 월의 기록 볼 수 있음
            id(int): 기본값은 None이지만 특정 선수의 id 입력하면 해당 선수의 기록이 나옴 
    
    Returns:
        output(pandas DF): 선수의 id와 기록이 있는 데이터 프레임 혹은 에러메세지

    '''
    data = get_data()
    player_data = data['player_data']
    if "name" not in kwargs:
        return "에러:선수 이름이 누락되었습니다."
    if "record" not in kwargs:
        return "에러:찾을 타격기록 혹은 투구기록이 누락되었습니다."
    if "data" not in kwargs:
        return "에러:분석에 필요한 타자 또는 투수 데이터가 누락되었습니다."
    if kwargs['name'] not in list(player_data['선수명'].unique()):
        return "에러:해당 선수는 2010년에서 2019년 시즌에 경기 출장 기록이 없습니다."
    if "id" in kwargs:
        if  kwargs["id"] not in list(player_data["ID"].unique()):
            return "에러: 입력된 id가 올바르지 않습니다. \nfind_player_info 함수를 사용해 id를 다시 찾을 수 있습니다."
        else:
            if what_record(kwargs['record']) != "찾는 기록을 계산할 수 없습니다":
                return arg_test(kwargs)
            else:
                return "에러:죄송합니다. 찾는 기록은 현재 데이터로 계산할 수 없습니다."
    if "id" not in kwargs:
        idlists =[i["ID"] for i in find_player_info(kwargs['name'])]
        if len(idlists)==1:
            kwargs.update({"id":idlists[0]})
            if what_record(kwargs['record']) != "찾는 기록을 계산할 수 없습니다":
                return arg_test(kwargs)
            else:
                return "에러:죄송합니다. 찾는 기록은 현재 데이터로 계산할 수 없습니다."
        else:
            player_record_df = pd.DataFrame()
            for i in idlists:
                kwargs.update({"id":i})
                if what_record(kwargs['record']) != "찾는 기록을 계산할 수 없습니다":
                    temp = arg_test(kwargs)
                else:
                    return "에러:죄송합니다. 찾는 기록은 현재 데이터로 계산할 수 없습니다."

                player_record_df = player_record_df.append(temp)
            return player_record_df




        
            
   
            
        
    

        