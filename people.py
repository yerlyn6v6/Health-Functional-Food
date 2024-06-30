

import pandas as pd

# 파일명 확인 및 수정
base_df = pd.read_csv("건강기능식품_원재료매핑_초성처리_240109.csv", encoding='utf-8-sig')


# 사람 구분 함수
def getPeople(text):
    kid = "영유아"
    pregnant = "임산부"
    allergy = "알러지"
    result = []
    if isinstance(text, str):
        if any(keyword in text for keyword in ["영유아", "영아", "유아", "어린이"]):
            result.append(kid)
        if any(keyword in text for keyword in ["임산부", "임부", "수유", "임신"]):
            result.append(pregnant)
        if any(keyword in text for keyword in ["알레르기", "알러지"]):
            result.append(allergy)
    return ' '.join(result)


# 주의 인물 저장용
base_df['attention_person_type'] = base_df['user_attention'].apply(getPeople)

# `=-`, `=+` 제거
#result = result.applymap(lambda x: x.replace('=-', '').replace('=+', '') if isinstance(x, str) else x)

# CSV 저장
base_df.to_csv("건강기능식품_원재료매핑_주의인물추가_240109.csv", index=False, encoding="utf-8-sig")
