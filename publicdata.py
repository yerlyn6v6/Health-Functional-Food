import pandas as pd
import numpy as np
import requests, xmltodict, json,  time
from requests.exceptions import ConnectionError

pd.set_option('mode.chained_assignment',  None) #경고무시

#크롤링 후 csv파일 다운로드 함수
def trans_csv(df, name):

    df.to_csv(name + '.csv', encoding='utf-8-sig', index=False)



## 0. API 기본 정보
key = 'x4N+cgBxTUXXIVNkNmkDLAPQtVutbbVH7QQNMQ2Tm8cmGkX69RyzQPRNk2Rpd7/YinVJnK/iYPlOsyKNk6+VmQ=='
url = 'http://apis.data.go.kr/1471000/HtfsTrgetInfoService02/getHtfsInfoList02'


## 1. 자동화 함수
def auto_req( numOfRows ):
    page_no = 1
    df_list = []

    #값 저장할 리스트 변수 만들기

    while True:
        try:
            params = {'serviceKey': key, 'pageNo': page_no, 'numOfRows': numOfRows, 'type' : 'xml' } # 대상별 정보 파라미터
            #params = {'serviceKey' : key, 'returnType' : 'xml', 'numOfRows' : numOfRows, 'pageNo' : page_no}  # 대상별 정보 파라미터

            response = requests.get(url, params=params)
            xml_data = response.text
            xml_parse = xmltodict.parse(xml_data)
            xml_dict = json.loads(json.dumps(xml_parse))

            if xml_dict['response']['body']['items'] == None:
                break
            else:
                item_list = xml_dict['response']['body']['items']['item']
                df = pd.json_normalize(item_list)
                df_list.append(df)

            print(page_no)
            page_no += 1 #페이지 증가
        except:
            print('error')
            time.sleep(10)
    return(df_list)



## 2. API 호출
df_list = auto_req(100)  #실행 전 함수에서 해당파라미터 주석 풀기
base_df = df_list[0]  #concat 할 가장 첫번째 df

#--호출한 df 모두 concat
for i in range(1, len(df_list)):
    con_df = df_list[i]
    base_df = pd.concat([base_df, con_df])

## 3. 형식 정리
# columns 이름 변경
Healthfood_df = base_df[['GU_PRDLST_MNF_MANAGE_NO', 'PRDLST_NM', 'BSSH_NM', 'DISPOS', 'CSTDY_MTHD', 'PRIMARY_FNCLTY', 'IFTKN_ATNT_MATR_CN', 'NTK_MTHD']]

# 회사양식과 동일하게 이름 변경
Healthfood_df.columns = ['medicine_seq_no', 'medicine_name', 'company_name', 'unit',
       'expiration_date', 'effect', 'user_attention', 'usage_volume']

# 기존 데이터에 없는 열 생성 (회사 양식과 통일화)
Healthfood_df['medicine_category_cd'] = None
Healthfood_df['medicine_eng_name'] = None
Healthfood_df['company_seq_no'] = None
Healthfood_df['store_method'] = None

# 순서정리
Healthfood_df = Healthfood_df[['medicine_seq_no', 'medicine_category_cd', 'medicine_name',
       'medicine_eng_name', 'company_seq_no', 'company_name', 'unit',
       'expiration_date', 'effect', 'store_method', 'user_attention',
       'usage_volume']]


Healthfood_df['medicine_seq_no'].astype('str')
Healthfood_df.dtypes



# csv 저장
trans_csv(Healthfood_df, '건강기능식품_대상별_240108')