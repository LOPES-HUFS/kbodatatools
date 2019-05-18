from requests_html import HTMLSession
from bs4 import BeautifulSoup

def get_game(date, home_team, away_team, double=0):
    url = (f'https://www.koreabaseball.com/Schedule/GameCenter/Main.aspx?gameDate={date}&gameId={date}{home_team}{away_team}{double}&section=REVIEW')
    session = HTMLSession()
    r = session.get(url)
    r.html.render()
    soup = BeautifulSoup(r.html.html, "lxml")
    return soup