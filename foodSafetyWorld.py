import pandas as pd
import numpy as np
import requests, xmltodict, json, time
from requests.exceptions import ConnectionError


# 크롤링 후 csv파일 다운로드 함수
def trans_csv(df, name):
    df.to_csv(name + '.csv', encoding='utf-8-sig', index=False)


# ## 테스트
# startIdx = 1
# endIdx =  3
# key = '6781689f75474c368fce'
# service_name = 'I0030'
# url = f'http://openapi.foodsafetykorea.go.kr/api/{key}/{service_name}/xml/{startIdx}/{endIdx}'


# response = requests.get(url)
# print(response.text)

## 1. 자동화 함수
def auto_req():
    # page_no = 1
    startIdx = 1
    endIdx = 1000

    # endIdx = 2
    df_list = []
    key = '6781689f75474c368fce'
    service_name = 'C003'  # 다른 항목 할 때 바꿔주기

    # 값 저장할 리스트 변수 만들기

    while True:
        url = f'http://openapi.foodsafetykorea.go.kr/api/{key}/{service_name}/xml/{startIdx}/{endIdx}'

        response = requests.get(url)

        xml_data = response.text

        xml_parse = xmltodict.parse(xml_data)

        if json.loads(json.dumps(xml_parse[service_name]['RESULT']['MSG'])) == '해당하는 데이터가 없습니다.':
            break
        if json.loads(json.dumps(xml_parse[service_name]['RESULT']['MSG'])) == '유효 호출건수를 이미 초과하셨습니다.':
            print("유효 호출건수 초과")
            break
        else:
            xml_dict = json.loads(json.dumps(xml_parse[service_name]['row']))
            item_list = xml_dict
            df = pd.json_normalize(item_list)
            # df = np.array(df)
            # df = np.array(df).reshape(100, 18)
            # df = pd.DataFrame(df)
            df_list.append(df)
            # print(df.head())

            # print(type(df))

        print(str(startIdx) + ',' + str(endIdx))
        # page_no += 1 #페이지 증가
        startIdx += 1000
        endIdx += 1000

    return (df_list)

## 2. API 호출
df_list = auto_req()  # 실행 전 함수에서 해당파라미터 주석 풀기

# print(df_list)

base_df = df_list[0]  # concat 할 가장 첫번째 df

# --호출한 df 모두 concat
for i in range(1, len(df_list)):
    con_df = df_list[i]
    base_df = pd.concat([base_df, con_df])

print(base_df)

# 유효 호출 횟수가 정해져 있어서 중간저장 꼭 해주기
trans_csv(base_df, '중간_건강기능식품_품목제조신고(원재료)2_202401')