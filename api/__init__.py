from requests_html import HTMLSession
from bs4 import BeautifulSoup

def get_game(date, home_team, away_team, double=0):
    url = f'https://www.koreabaseball.com/Schedule/GameCenter/Main.aspx?gameDate={date}&gameId={date}{home_team}{away_team}{double}&section=REVIEW'
    gameld = f'{date}{home_team}{away_team}{double}'
    session = HTMLSession()
    r = session.get(url)
    r.html.render()
    soup = BeautifulSoup(r.html.html, "lxml")
    tables = soup.find_all('table')
    record_etc = soup.findAll('div',{'class':'record-etc'})
    box_score = soup.findAll('div',{'class':'box-score-wrap'})
    teams = box_score[0].findAll('span',{'class':'logo'})
    return{'tables':tables, 'record_etc':record_etc, 'teams':teams, 'date':date, 'id':gameld}
    