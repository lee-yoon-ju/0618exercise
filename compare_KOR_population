import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# 데이터 불러오기
@st.cache_data
def load_data():
    df = pd.read_csv("202505_202505_연령별인구현황_월간.csv", encoding="euc-kr")
    return df

df = load_data()

st.title("두 지역의 5세 단위 상대도수 인구 분포 비교")
st.markdown("두 지역을 선택하면 각 지역의 인구를 5세 단위로 묶고, 해당 지역 내 비율(상대도수)로 선 그래프를 그립니다.")

# 지역 선택
region_col = df.columns[0]
regions = df[region_col].unique()
selected_regions = st.multiselect("지역 2개 선택", regions, default=regions[:2])

if len(selected_regions) != 2:
    st.warning("⚠️ 정확히 2개의 지역을 선택해주세요.")
    st.stop()

# 연령 컬럼 숫자 추출
def get_age_labels(columns):
    agedict = {}
    for col in columns:
        cleaned = col.replace(" ", "")
        if cleaned.endswith("세"):
            try:
                age = int(cleaned.replace("세", ""))
                agedict[age] = col
            except ValueError:
                pass
        elif "이상" in cleaned:
            agedict[100] = col  # 100세 이상 등
    return agedict

age_columns = df.columns[1:]
age_dict = get_age_labels(age_columns)

# 5세 단위 구간 생성
age_bins = list(range(0, 105, 5))
age_labels = [f"{a}~{a+4}세" if a < 100 else "100세 이상" for a in age_bins]

def get_relative_freq(region_name):
    # 입력 지역 데이터 (assume 1 row)
    region_row = df[df[region_col] == region_name]
    grouped = {}
    for a in age_bins:
        label = f"{a}~{a+4}세" if a < 100 else "100세 이상"
        cols = [age_dict[x] for x in range(a, a+5) if x in age_dict]
        if a >= 100:
            # 100세 이상 모든 값 합산
            cols = [col for key, col in age_dict.items() if key >= 100]
        value = region_row[cols].sum(axis=1).values[0] if cols else 0
        grouped[label] = value
    total = sum(grouped.values())
    if total == 0:
        # 비정상 데이터
        return {k:0 for k in grouped.keys()}
    rel_freq = {k:v/total*100 for k,v in grouped.items()}
    return rel_freq

rel1 = get_relative_freq(selected_regions[0])
rel2 = get_relative_freq(selected_regions[1])

fig, ax = plt.subplots(figsize=(12,6))
ax.plot(age_labels, [rel1[k] for k in age_labels], marker='o', label=selected_regions[0])
ax.plot(age_labels, [rel2[k] for k in age_labels], marker='s', label=selected_regions[1])
ax.set_title("선택한 지역별 연령대 인구 비율(상대도수)", fontsize=16)
ax.set_xlabel("연령대", fontsize=12)
ax.set_ylabel("인구 비율 (%)", fontsize=12)
ax.set_xticklabels(age_labels, rotation=45)
ax.grid(True)
ax.legend()
plt.tight_layout()
st.pyplot(fig)
