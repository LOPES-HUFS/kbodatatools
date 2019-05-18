from requests_html import HTMLSession
from bs4 import BeautifulSoup
session = HTMLSession()
url ="https://www.koreabaseball.com/Schedule/GameCenter/Main.aspx?gameDate=20190511&gameId=20190511OBNC0&section=REVIEW"
r = session.get(url)
r.html.render()
r.html.text
soup = BeautifulSoup(r.html.full_text, "lxml")
print(soup)