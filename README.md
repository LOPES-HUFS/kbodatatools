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
single_game = api.get_data(api.get_game(date=20190511, home_team= 'OB', away_team='NC'))
single_game['scoreboard']
single_game['ETC_info']
single_game['away_batter']
single_game['home_batter']
single_game['away_pitcher']
single_game['home_pitcher']
```

### 참고 링크

- [Parsing JavaScript rendered pages in Python with pyppeteer | Tchut-Tchut Blog](https://beenje.github.io/blog/posts/parsing-javascript-rendered-pages-in-python-with-pyppeteer/)