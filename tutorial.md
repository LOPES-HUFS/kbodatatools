# 패키지 사용 설명서

## 튜토리얼

먼저 패키지를 임포트합니다.

'''python
import kbodatatools as kd
import pandas as pd
'''

이제 KBO의 정규시즌 데이터를 수집해보겠습니다. 여기서 전체 데이터가 아닌 일부 데이터를 받고 싶다면 stack_game_data 함수의 year과 month인자에 특정 년도와 월을 입력하면 됩니다.
'''python
full_season = pd.read_csv("data/KBO_gameid_full_season.csv")
kd.datatools.write_json(kd.datatools.stack_game_data(full_season))
'''

이제 선수들의 기록 데이터를 타자와 투수 데이터로 나누어 csv 파일로 저장해볼 차례입니다. 먼저 생성한 json 파일을 읽어와 줍니다. 읽어온 json 데이터를 data2dataframe 함수와 save csv함수를 사용해 csv 파일로 만들어줍니다.

'''python
game_dict = kd.datatools.read_json("all_data.json")

batter_temp = kd.datatools.data2dataframe(game_dict,"batter")
kd.datatools.save_csv(batter_temp,"batter")

pitcher_temp = kd.datatools.data2dataframe(game_dict,"pitcher")

kd.datatools.save_csv(pitcher_temp,"pitcher")
'''

다음에는 선수들의 자료에 동명이인 선수를 구분할 id를 생성해줍니다. id를 만드는 방법은 make_player_id 함수를 통해 가능합니다.

'''python
batter_id_data = kd.datatools.make_player_id(batter_temp)
pitcher_id_data = kd.datatools.make_player_id(pitcher_temp)

'''
