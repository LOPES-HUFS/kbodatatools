import asyncio
from requests_html import AsyncHTMLSession
from bs4 import BeautifulSoup

from . import pasing_page
from . import modifying_data

def get_games(gameid):
    ''' 
    gameid 20개씩 받아서 다운로드함 
    '''
    souplist = {}

    async def get_game_soup(date, home_team, away_team, double=0):
        '''
        Args:
            date (int): 20190511 과 같이 숫자로 만든 경기 날짜
            home_team (str): 홈팀
            away_team (str): 원정팀
        Returns:
            souplist (list): 20개 경기의 BeautifulSoup의 soup
        '''
        index = str(date)+away_team+home_team+double
        url = (f'https://www.koreabaseball.com/Schedule/GameCenter/Main.aspx?gameDate={date}&gameId={date}{away_team}{home_team}{double}&section=REVIEW')
        asession = AsyncHTMLSession()
        r = await asession.get(url)
        await r.html.arender()
        soup = BeautifulSoup(r.html.html, "lxml")
        souplist.update({index:soup})

    tasks = [get_game_soup(gameid.date[i],gameid.home[i],gameid.away[i]) for i in range(0,len(gameid))]

    asyncio.run(asyncio.wait(tasks))
    return souplist