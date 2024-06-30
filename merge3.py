import pandas as pd

# 파일명 확인 및 수정
base_df = pd.read_csv("건강기능식품_대상별_240108.csv", encoding='utf-8-sig')
add_df = pd.read_csv("중간_건강기능식품_품목제조신고(원재료)_202401.csv", encoding='utf-8-sig')

# 추가할 데이터의 columns 이름 변경
Healthfood_df = add_df[['PRDLST_REPORT_NO', 'PRDLST_NM', 'BSSH_NM', 'DISPOS',
                        'POG_DAYCNT', 'PRIMARY_FNCLTY', 'IFTKN_ATNT_MATR_CN', 'NTK_MTHD']]
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

Healthfood_df['medicine_seq_no'] = Healthfood_df['medicine_seq_no'].astype('str')

# 기존 데이터와 추가 데이터의 중복 제거
base_df['medicine_seq_no'] = base_df['medicine_seq_no'].astype('str')
Healthfood_df = Healthfood_df.drop_duplicates()
base_df = base_df.drop_duplicates()

# 병합 전에 중복 확인
print(f"Base DataFrame shape: {base_df.shape}")
print(f"Additional DataFrame shape: {Healthfood_df.shape}")

# 병합
result = pd.concat([base_df, Healthfood_df], ignore_index=True)

# 병합 후 중복 제거
result = result.drop_duplicates(subset=['medicine_seq_no'])

# 병합 후 중복 확인
print(f"Result DataFrame shape: {result.shape}")


# 한글 초성 추출 함수
def extract_initials(text):
    # 초성 리스트
    CHOSUNG_LIST = [
        'ㄱ', 'ㄲ', 'ㄴ', 'ㄷ', 'ㄸ', 'ㄹ', 'ㅁ', 'ㅂ', 'ㅃ', 'ㅅ', 'ㅆ',
        'ㅇ', 'ㅈ', 'ㅉ', 'ㅊ', 'ㅋ', 'ㅌ', 'ㅍ', 'ㅎ'
    ]

    result = []

    for char in text:
        if '가' <= char <= '힣':  # 한글 음절의 범위
            # 유니코드에서 해당 한글의 값
            char_code = ord(char) - ord('가')
            # 초성 인덱스
            chosung_index = char_code // 588
            result.append(CHOSUNG_LIST[chosung_index])
        else:
            result.append(char)

    return ''.join(result)


# 초성 저장용 열 추가
result['medicine_initials'] = result['medicine_name'].apply(extract_initials)

# 데이터에 `=-` 또는 `=+` 패턴이 있는지 확인
#before_replace_count = result.stack().apply(lambda x: '=-' in str(x) or '=+' in str(x)).sum()
#print(f"Before replace: {before_replace_count} cells contain the pattern.")

# `=-`, `=+` 제거
#result = result.applymap(lambda x: str(x).replace('=-', ' ').replace('=+', '') if isinstance(x, str) else x)

# 데이터에 `=-` 또는 `=+` 패턴이 제거되었는지 확인
#after_replace_count = result.stack().apply(lambda x: '=-' in str(x) or '=+' in str(x)).sum()
#print(f"After replace: {after_replace_count} cells contain the pattern.")

# CSV 저장
result.to_csv("건강기능식품_원재료매핑_초성처리_240109.csv", index=False, encoding="utf-8-sig")
