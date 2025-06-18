import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

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

# 연령대 컬럼 파악
age_columns = df.columns[1:]
age_dict = {}
for col in age_columns:
    try:
        if '이상' in col:
            age = 100
        else:
            age = int(col.replace("세", ""))
        age_dict[age] = col
    except:
        continue

# 5세 단위 상대도수 계산 함수
def get_relative_freq(region_name):
    region_data = df[df[region_col] == region_name]
    grouped = {}

    for age in range(0, 105, 5):
        label = f"{age}~{age+4}세" if age < 100 else "100세 이상"
        cols = [age_dict[a] for a in range(age, age+5) if a in age_dict]
        if age >= 100:
            cols = [v for k, v in age_dict.items() if k >= 100]
        total = region_data[cols].sum(axis=1).values[0]
        grouped[label] = total

    # 각 연령대 인구 / 해당 지역 전체 인구 × 100
    total_population = sum(grouped.values())
    relative_freq = {k: v / total_population * 100 for k, v in grouped.items()}
    return relative_freq

# 데이터 가져오기
rel_freq_1 = get_relative_freq(selected_regions[0])
rel_freq_2 = get_relative_freq(selected_regions[1])

# 시각화
labels = list(rel_freq_1.keys())
values1 = list(rel_freq_1.values())
values2 = list(rel_freq_2.values())

fig, ax = plt.subplots(figsize=(12, 6))
ax.plot(labels, values1, marker='o', label=selected_regions[0])
ax.plot(labels, values2, marker='s', label=selected_regions[1])
ax.set_title("선택한 지역별 연령대 인구 비율(상대도수)", fontsize=16)
ax.set_xlabel("연령대", fontsize=12)
ax.set_ylabel("인구 비율 (%)", fontsize=12)
plt.xticks(rotation=45)
plt.grid(True)
plt.legend()
plt.tight_layout()
st.pyplot(fig)
