# KBO_data_analysis

KBO 자료를 모으고 분석하고자 합니다.

## 사용법

### 가상환경에서 파이썬 실행하는 방법

터미널에서 다음과 같이 입력한다.

```bach
pwd
```

이 때 출력된 결과의 마지막 부분이 `KBO_data_analysis`과 같이 나오면 준비가 다 된 것입니다.

이제 가상 환경으로 터미널을 바꿔봅시다.

```bach
pipenv shell
```

위의 명령어를 터미널이 입력하고 엔터를 치면, 앞 부분이 `(KBO_data_analysis)`과 같이 나오면 가상환경으로 들어간 것입니다. 여기서 `python`이라고 입력하시면 파이썬을 사용할 수 있게 됩니다. 지금 가상환경을 **python3.7**로 만들었기 때문에 앞에 같이 입력해도 파이썬 3.7이 작동하게 됩니다.

### 개별 게임 자료를 받아오는 방법

```python
import api
single_game = api.get_data(api.get_game(date=20190511, home_team= 'NC', away_team='OB'))
single_game['scoreboard']
single_game['ETC_info']
single_game['away_batter']
single_game['home_batter']
single_game['away_pitcher']
single_game['home_pitcher']
```

### 자료 소개

sample 폴더의 KBO_batter_full.csv 파일은 2010년부터 2019년 8월 31일까지의 타자 데이터가 저장되어 있습니다. 해당 데이터는 전체 경기 기록에 대한 정보 데이터(KBO_gameid_full_season.csv)를 사용해 자료를 수집해 만들고 이후 id를 붙여서 완성할 수 있습니다. KBO_pitcher_full.csv 역시 마찬가지 과정으로 만들어집니다. data 폴더의 KBO_player_info_full.csv 파일은 선수이름과 선수 id 연도별 선수의 소속팀에 대한 정보가 있는 데이터 입니다. 참고로 이 데이터에 있는 연도별 팀 정보의 경우에는 해당 년도에 이적을하거나 개명을 하거나 하는 경우로 인해 부정확한 경우가 있을 수도 있습니다. 그외에 타자 기록 데이터의 이병규(2010~2016년 기록), 투수 기록 데이터의 이승호(2010~2011년 기록), 허준혁(2010~2011년 기록)의 경우 제가 직접 경기 기록을 보고 구분한 것이기 때문에 id가 잘 못 입력되는 실수가 있었을 수도 있습니다. 참고로 타자와 투수데이터 그리고, 스코어보드의 데이터는 h5파일에 저장되어 한번에 사용하실 수 있습니다.

### 참고 링크

- [Parsing JavaScript rendered pages in Python with pyppeteer | Tchut-Tchut Blog](https://beenje.github.io/blog/posts/parsing-javascript-rendered-pages-in-python-with-pyppeteer/)
