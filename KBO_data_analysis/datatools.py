'''
함수들 몰아서 정리 파일 단순화시키기 
'''

def data2dataframe(data:dict,datatype:str):
    '''
    경기 자료가 담긴 json 데이터를 가지고 pandas Dataframe으로 만드는 함수 
    Args:
        data(dict): 선수들의 경기 자료가 담긴 딕트 또는 json 파일  
        datatype(str): 타자 기록인지 투수 기록인지를 확인하는 인자로 
        타자면 batter 투수면 pitcher를 입력하여 각각 기록을 데이터프레임에 저장할 수 있다
    Returns:
        temp(Pandas DF): 타자기록 또는 투수기록이 일자별로 쌓인 데이터 프레임 
    '''
    temp = pd.DataFrame()

    for i in range(0,len(data['fulldata'].keys())):
        away = pd.DataFrame(data['fulldata'][list(data['fulldata'].keys())[i]][f'away_{datatype}'])
        home = pd.DataFrame(data['fulldata'][list(data['fulldata'].keys())[i]][f'home_{datatype}'])
        home['dateindex'] = list(data['fulldata'].keys())[i]
        away['dateindex'] = list(data['fulldata'].keys())[i]
        temp = temp.append(away.append(home))

    temp = temp.fillna(0)
    return temp
