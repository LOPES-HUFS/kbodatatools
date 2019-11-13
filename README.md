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

### 패키지 인스톨

```bach
pip3 install kbodatatools
```

### 패키지 임포트

```python
import kbodatatools
```

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

### 전체(2010 ~ 2019년 10월까지) 게임 자료를 받아오는 방법

위의 방법을 통해 가상환경이 활성화되면 가상환경에서 아래의 순서대로 파이썬 스크립트 파일을 실행하면 전체 게임 자료를 받아올 수 있습니다. 참고로 전체 자료를 다운 받는 과정에는 약 3시간 이상의 시간이 소요됩니다. 아래의 과정을 끝 마치면 sample 폴더에서 2010~2019년 8월까지의 스코어 보드와 타자와 투수 데이터, 기타 정보가 있는 json 파일과 타자, 투수 데이터 그리고 경기 정보에 대한 데이터가 csv 파일로 생성됩니다.

```python


```

### 분석 모듈 사용 방법

전체 자료가 만들어지면 선수들의 간단한 타격, 투구 기록을 확인해 볼 수 있습니다. 계산 가능한 기록들의 목록은 다음과 같습니다. 타격 기록: 타율, 타점, 득점, 안타, 1루타, 2루타, 3루타, 홈런, 볼넷(4구), 몸에맞는공, 고의4구, 병살, 출루율, 장타율, 희생플라이, 희생번트, 피삼진이 있습니다. 투구 기록: 방어율, 투구수, 타자수, 홀드, 세이브, 피안타, 삼진, 피홈런, 4사구, 자책점, 승률, 이닝, 이닝당투구수, 승리, 패배, 무승부가 있습니다. 이 기록들은 아래와 같은 방식으로 확인할 수 있습니다. 아래에서와 같이 연도별 혹은 월별 기록으로도 확인할 수 있습니다.

```python3
import basic_analysis

basic_analysis.get_player_record(name="이병규",record="타율")
basic_analysis.get_player_record(name="허준혁",record="방어율")
basic_analysis.get_player_record(name="김현수",record="출루율",year=2019)
basic_analysis.get_player_record(name="김광현",record="방어율",year=2019)
basic_analysis.get_player_record(name="김현수",record="출루율",year=2019,month=6)
basic_analysis.get_player_record(name="김광현",record="방어율",year=2019,month=6)
```

참고로 2019년 힌화의 지성준 선수와 장진혁 선수의 경우 KBO의 리뷰 페이지 상으로 3번째 타석의 기록이 나와있지 않기 때문에 타격 기록의 계산이 맞지 않습니다.

### data 폴더의 기초 자료 소개

data 폴더에는 선수 id를 구성하는데 필요한 데이터들과 자료 수집하고 구성하기 위한 데이터들이 있습니다. 그 외에 patch_file이라는 폴더에는 이병규, 허준혁, 이승호 선수의 id 구분을 위한 데이터들이 있습니다. 이 데이터들은 이후 patch.py 파일에서 사용하게 됩니다. record_list.csv 파일은 분석 함수에서 계산할 수 있는 기록들을 모아놓은 데이터 입니다. 이 데이터 파일은 함수 사용시 참고용으로만 사용됩니다. sample 폴더는 이후 경기 자료를 수집하는 코드를 실행시키면 그 결과가 저장되는 폴더입니다. 따라서 이 폴더를 지우게 될 경우 코드 실행시 에러가 발생합니다.

### 스크립트 실행으로 생성되는 자료 소개

전체 게임의 리뷰 데이터는 all_data.json 파일로 저장됩니다. 이 json 파일을 이용해 2010년에서 2019년 8월까지의 타자(KBO_batter_data_full.csv)와 투수(KBO_pitcher_data_full.csv)의 경기 기록 데이터가 생성됩니다. 이렇게 생성된 타자와 투수 데이터는 스크립트를 실행하여 id가 생성됩니다. 이렇게 생성된 데이터를 이용해 선수들의 간단한 기록을 비교 분석해 볼 수 있습니다. 경기 정보 데이터(KBO_game_info_data.csv)는 2010년에서 2019년 8월 까지 승패와 같은 결과와 심판, 구장 등의 경기 정보가 저장됩니다.

### 참고 링크

- [Parsing JavaScript rendered pages in Python with pyppeteer | Tchut-Tchut Blog](https://beenje.github.io/blog/posts/parsing-javascript-rendered-pages-in-python-with-pyppeteer/)
