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

### 전체(2010 ~ 2019년 8월까지) 게임 자료를 받아오는 방법

위의 방법을 통해 가상환경이 활성화되면 가상환경에서 아래의 순서대로 파이썬 스크립트 파일을 실행하면 전체 게임 자료를 받아올 수 있습니다. 참고로 전체 자료를 다운 받는 과정에는 약 3시간 이상의 시간이 소요됩니다. 전체 게임의 결과 데이터는 patch.py 파일까지 실행한 이후 make_game_info.py 스크립트의 실행으로 만들 수 있습니다.

```bash
cd KBO_data_analysis

python3 save_all_games.py

python3 match_player_id.py

python3 patch.py

python3 make_game_info.py
```

### data 폴더의 자료 소개

data 폴더에는 선수 id를 구성하는데 필요한 데이터들과 자료 수집하고 구성하기 위한 데이터들이 있습니다. 그 외에 patch_file이라는 폴더에는 이병규, 허준혁, 이승호 선수의 id 구분을 위한 데이터들이 있습니다. 이 데이터들은 이후 patch.py 파일에서 사용하게 됩니다. record_list.csv 파일은 분석 함수에서 계산할 수 있는 기록들을 모아놓은 데이터 입니다. 이 데이터 파일은 함수 사용시 참고용으로만 사용됩니다. sample 폴더는 이후 경기 자료를 수집하는 코드를 실행시키면 그 결과가 저장되는 폴더입니다. 따라서 이 폴더를 지우게 될 경우 코드 실행시 에러가 발생합니다.

### 스크립트 실행으로 생성되는 자료 소개

전체 게임의 리뷰 데이터는 all_data.json 파일로 저장됩니다. 이 json 파일을 이용해 2010~2019년 8월까지의 타자(KBO_batter_data_full.csv)와 투수(KBO_pitcher_data_full.csv)의 경기 기록 데이터가 생성됩니다. 이렇게 생성된 타자와 투수 데이터는 스크립트를 실행하여 id가 생성됩니다. 이렇게 생성된 데이터를 이용해 선수들의 간단한 기록을 비교 분석해 볼 수 있습니다. 경기 정보 데이터(KBO_game_info_data.csv)는 2010~2019년 8월 까지 승패와 같은 결과와 심판, 구장 등의 경기 정보가 저장됩니다.

### 참고 링크

- [Parsing JavaScript rendered pages in Python with pyppeteer | Tchut-Tchut Blog](https://beenje.github.io/blog/posts/parsing-javascript-rendered-pages-in-python-with-pyppeteer/)
