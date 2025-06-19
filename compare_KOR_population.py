import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# 데이터 불러오기
@st.cache_data
def load_data():
    try:
        df = pd.read_csv("202505_202505_연령별인구현황_월간.csv", encoding="euc-kr")
        df.fillna(0, inplace=True)
        for col in df.columns[3:]:  # D열부터 전부 숫자로 변환
            df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0)
        return df
    except Exception as e:
        st.error(f"❌ 파일을 불러오는 데 문제가 발생했습니다: {e}")
        return pd.DataFrame()

df = load_data()

st.title("두 지역의 5세 단위 상대도수 인구 분포 비교")
st.markdown("엑셀 기준 D열부터 0세 인구가 포함되어 있다고 가정하고, 5세 단위로 그룹화하여 두 지역의 상대도수를 비교합니다.")

if not df.empty:
    region_col = df.columns[0]  # 지역명 열
    regions = df[region_col].unique()
    selected_regions = st.multiselect("지역 2개 선택", regions, default=regions[:2])

    if len(selected_regions) != 2:
        st.warning("⚠️ 정확히 2개의 지역을 선택해주세요.")
        st.stop()

    # 상대도수 계산 함수
    def get_relative_freq(region_name):
        region_data = df[df[region_col] == region_name]
        grouped = {}

        age_start_idx = 3  # D열부터 나이 데이터 시작
        total_age_cols = df.shape[1] - age_start_idx

        for age in range(0, total_age_cols, 5):
            label = f"{age}~{age+4}세" if age + 4 < total_age_cols else f"{age}세 이상"
            col_indices = list(range(age_start_idx + age, min(age_start_idx + age + 5, df.shape[1])))
            cols = df.columns[col_indices]
            total = region_data[cols].sum(axis=1).values[0]
            grouped[label] = total

        total_population = sum(grouped.values())
        if total_population == 0:
            return {k: 0 for k in grouped}
        return {k: v / total_population * 100 for k, v in grouped.items()}

    # 계산
    rel_freq_1 = get_relative_freq(selected_regions[0])
    rel_freq_2 = get_relative_freq(selected_regions[1])

    # 시각화
    labels = list(rel_freq_1.keys())
    values1 = list(rel_freq_1.values())
    values2 = list(rel_freq_2.values())

    fig, ax = plt.subplots(figsize=(12, 6))
    ax.plot(labels, values1, marker="o", label=selected_regions[0])
    ax.plot(labels, values2, marker="s", label=selected_regions[1])
    ax.set_title("선택한 지역별 연령대 인구 비율(상대도수)", fontsize=16)
    ax.set_xlabel("연령대", fontsize=12)
    ax.set_ylabel("인구 비율 (%)", fontsize=12)
    plt.xticks(rotation=45)
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    st.pyplot(fig)
