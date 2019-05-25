import ast
import json

from requests_html import HTMLSession
from bs4 import BeautifulSoup

import api.pasing_page

def get_game(date, home_team, away_team, double=0):
    ''' 개별 게임을 가져오는 함수
    쉽게 분석할 수 있도록 soup 으로 내보낸다.

    Args:
        date (int): 20190511 과 같이 숫자로 만든 경기 날짜
        home_team (str): 홈팀
    
    Returns:
        soup (soup): BeautifulSoup의 soup
    '''
    url = (f'https://www.koreabaseball.com/Schedule/GameCenter/Main.aspx?gameDate={date}&gameId={date}{home_team}{away_team}{double}&section=REVIEW')
    session = HTMLSession()
    r = session.get(url)
    r.html.render()
    soup = BeautifulSoup(r.html.html, "lxml")
    return soup

def get_data(soup):
    '''가져온 개별 게임들을 스코어보드 ,타자, 투수 별로 정리 합니다.
    단순하게 사용하는 방법은 다음 링클를 참고합니다.

    https://github.com/LOPES-HUFS/KBO_data_analysis/blob/master/README.md#개별-게임-자료를-받아오는-방법

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
    temp_scoreboard = api.pasing_page.scoreboard(tables, teams)

    temp_all = {'scoreboard':ast.literal_eval(temp_scoreboard.to_json(orient='records'))}
    temp_all.update({"ETC_info":api.pasing_page.ETC_info(tables,record_etc)})
    temp_all.update({'away_batter':ast.literal_eval(api.pasing_page.away_batter(tables,teams).to_json(orient='records'))})
    temp_all.update({'home_batter':ast.literal_eval(api.pasing_page.home_batter(tables,teams).to_json(orient='records'))})
    temp_all.update({'away_pitcher':ast.literal_eval(api.pasing_page.away_pitcher(tables,teams).to_json(orient='records'))})
    temp_all.update({'home_pitcher':ast.literal_eval(api.pasing_page.home_pitcher(tables,teams).to_json(orient='records'))})

    return temp_all 
  