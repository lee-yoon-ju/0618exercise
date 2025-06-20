import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# 데이터 불러오기
@st.cache_data
def load_data():
    try:
        df = pd.read_csv("202505_202505_연령별인구현황_월간.csv", encoding="euc-kr")
        df.fillna(0, inplace=True)
        # 숫자 변환 및 쉼표 제거
        for col in df.columns[3:]:
            df[col] = df[col].astype(str).str.replace(",", "", regex=False)
            df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0)
        return df
    except Exception as e:
        st.error(f"❌ 파일 불러오기 오류: {e}")
        return pd.DataFrame()

df = load_data()

st.title("두 지역의 5세 단위 상대도수 인구 분포 비교")
st.markdown("각 지역의 인구를 5세 단위로 묶고, 전체 인구 대비 상대 비율(%)을 선 그래프로 비교합니다.")

if not df.empty:
    region_col = df.columns[0]
    regions = df[region_col].unique()
    selected_regions = st.multiselect("지역 2개 선택", regions, default=regions[:2])

    if len(selected_regions) != 2:
        st.warning("⚠️ 정확히 2개의 지역을 선택해주세요.")
        st.stop()

    # 연령 컬럼 파악
    age_columns = df.columns[3:]
    age_dict = {}

    for col in age_columns:
        try:
            age_token = col.split("_")[-1]
            if "이상" in age_token:
                age = 100
            else:
                age = int(age_token.replace("세", "").strip())
            age_dict[age] = col
        except:
            continue

    # 상대도수 계산
    def get_relative_freq(region_name):
        region_data = df[df[region_col] == region_name]
        grouped = {}

        for age in range(0, 105, 5):
            label = f"{age}~{age+4}세" if age < 100 else "100세 이상"
            cols = [age_dict[a] for a in range(age, age+5) if a in age_dict]
            if age >= 100:
                cols = [v for k, v in age_dict.items() if k >= 100]
            total = region_data[cols].sum(axis=1).values[0] if cols else 0
            grouped[label] = total

        total_population = sum(grouped.values())
        return {k: v / total_population * 100 for k, v in grouped.items()} if total_population > 0 else {k: 0 for k in grouped}

    # 데이터 계산
    rel_freq_1 = get_relative_freq(selected_regions[0])
    rel_freq_2 = get_relative_freq(selected_regions[1])

    # 그래프 시각화
    labels = list(rel_freq_1.keys())
    values1 = list(rel_freq_1.values())
    values2 = list(rel_freq_2.values())

    fig, ax = plt.subplots(figsize=(12, 6))
    ax.plot(labels, values1, marker="o", label=selected_regions[0])
    ax.plot(labels, values2, marker="s", label=selected_regions[1])
    ax.set_title("선택한 지역별 연령대 인구 비율 (상대도수)", fontsize=16)
    ax.set_xlabel("연령대", fontsize=12)
    ax.set_ylabel("인구 비율 (%)", fontsize=12)
    plt.xticks(rotation=45)
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    st.pyplot(fig)
