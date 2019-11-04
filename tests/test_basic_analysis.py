from kbodatatools import basic_analysis
import pytest
import requests
from bs4 import BeautifulSoup
import lxml

def request_stat(name,birth):
    url = f"http://www.statiz.co.kr/player.php?name={name}&birth={birth}"
    contents = requests.get(url)
    soup = BeautifulSoup(contents.text, 'lxml')
    colnames = [i.text for i in soup.findAll('th')]
    key = [i for i in list(dict.fromkeys(colnames)) if i not in ['','비율','WAR*','WAR','WPA']]
    if len(key) == 29:
        value = [i.text for i in soup.findAll('td')[58:87]]
    if len(key) == 30:
        value = [i.text for i in soup.findAll('td')[59:89]]
    
    return dict(zip(key,value))
        

@pytest.mark.ok
def test_get_record():
    for i in 
