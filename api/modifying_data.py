import pandas as pd
from api.pasing_page import looking_for_team_name
import ast 

def change_record(temp,column,factorlist):
    for i in range(0,len(temp[[str(column)]])):
        if "/" in list(str(temp[str(column)].tolist()[i])):
            temp1=factorlist.code[factorlist.factor_list==str(temp[str(column)].tolist()[i].split("/ ")[0].split("\\")[0])]
            temp2=factorlist.code[factorlist.factor_list==str(temp[str(column)].tolist()[i].split("/ ")[1])]
            temp.loc[i,str(column)]=str(list(temp1)[0])+str(list(temp2)[0])
    return temp

def batter_clean(data,section):
    temp_b=pd.DataFrame(data[section])
    factorlist = pd.read_csv("./api/data/KBO_factor_list.csv")
    for i in factorlist.factor_list:
        temp_b=temp_b.replace(i,factorlist.code[factorlist.factor_list==i].tolist()[0])
        
    columns=[x for x in temp_b.columns if x in ['1', '2', '3', '4', '5', '6', '7', '8', '9',"10","11","12"]]
    for j in columns:
        temp_b=change_record(temp_b,j,factorlist)

    data[section]=ast.literal_eval(temp_b.to_json(orient='records'))
    return data

def change_inning(item):
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

#section은 away_pitcher,home_pitcher 구분
def pitcher_clean(data,section):
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


