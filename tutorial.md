# 패키지 사용 설명서

## 튜토리얼

### 패키지 임포트

```python
import kbodatatools as kd
```

### KBO 경기 자료를 다운 받는 법

```python
import pandas as pd

full_season = pd.read_csv("./data/KBO_gameid_full_season.csv")
kd.datatools.write_json(kd.datatools.stack_game_data(full_season))
```

이제 KBO의 정규시즌 데이터를 수집해보겠습니다. 여기서 전체 데이터가 아닌 일부 데이터를 받고 싶다면 stack_game_data 함수의 year과 month인자에 특정 년도와 월을 입력하면 됩니다.

아래부터는 다운 받은 파일을 분리하고 전처리하여 저장하는 방법에 대해 설명합니다. 이 부분은 개별적으로 선수들의 경기 기록 데이터를 가지고 추가 분석이나 개인적인 작업을 하실 분들을 위한 것입니다. 따라서 패키지에 들어있는 기본적인 분석이나 패키지 내부의 데이터를 사용하실 분들은 아래의 내용들을 생략하여도 괜찮습니다.

### 타자 데이터와 투수 데이터로 분리하기

```python
game_dict = kd.datatools.read_json("all_data.json")

batter_temp = kd.datatools.data2dataframe(game_dict,"batter")
kd.datatools.save_csv(batter_temp,"batter")

pitcher_temp = kd.datatools.data2dataframe(game_dict,"pitcher")

kd.datatools.save_csv(pitcher_temp,"pitcher")
```

위에서 저장한 json 파일을 읽어와 줍니다. 읽은 json 파일에서 data2dataframe() 함수를 사용해 타자와 투수 데이터로 나누어 줍니다. 데이터를 구분하는 방법은 함수 안의 인자로 타자면 "batter" 투수면 "pitcher"를 사용해서 구분할 수 있습니다. 구분한 데이터를 csv 파일로 저장해 줍니다.

### 선수 기록 데이터에 개별 id 붙이기

```python
batter_id_data = kd.datatools.make_player_id(batter_temp)
pitcher_id_data = kd.datatools.make_player_id(pitcher_temp)
```

다음에는 선수들의 자료에 동명이인 선수를 구분할 id를 생성해줍니다. id를 만드는 방법은 make_player_id 함수를 통해 가능합니다. 이 과정에서 같은 팀에서 같은 년도에 경기한 동명이인 선수들의 경우 (이병규, 이승호, 허준혁 선수)는 이후 patch.py 파일의 코드를 실행시켜 줌으로써 경기 기록에서 해당 선수들의 기록을 구분할 수 있습니다. 코드를 직접 타이핑할 필요 없이 터미널이나 cmd에서 py 파일을 실행시켜도 적용됩니다. 단 이 파일은 선수들의 id가 기본적으로 적용된 이후에 실행시켜야합니다.

패치 파일 실행으로 동명이인 선수들의 id까지 생성이 완료되면, 이제 선수들의 기록 데이터를 개별적으로 분석에 사용하실 수 있습니다. 패키지의 기본적인 분석 함수의 사용법에 대해서는 ReadME 파일을 참고해주시면 감사하겠습니다.
