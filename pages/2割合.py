import streamlit as st
import os
import json
import pandas as pd
import altair as alt

FEATURE_FILE = "character_features.json"

st.title("特徴の割合を可視化")

# JSON読み込み
if os.path.exists(FEATURE_FILE):
    with open(FEATURE_FILE, "r", encoding="utf-8") as f:
        features = json.load(f)
else:
    st.write("特徴データがありません")
    st.stop()

# DataFrame化
df = pd.DataFrame.from_dict(features, orient="index")

# 欠損値を空文字に統一
df = df.fillna("")

# ============================
# ★ 作品名フィルタ
# ============================
st.subheader("作品で絞り込み")

work_list = sorted([w for w in df["work"].unique() if w != ""])
work_options = ["全作品"] + work_list

selected_work = st.selectbox("作品を選択", work_options)

# ============================
# ★ DataFrame を絞り込み
# ============================
if selected_work != "全作品":
    df_filtered = df[df["work"] == selected_work]
else:
    df_filtered = df

# ============================
# ★ 割合計算関数
# ============================
def make_ratio_df(column_name, target_df):
    counts = target_df[column_name].value_counts()
    if counts.sum() == 0:
        return pd.DataFrame({column_name: [], "count": [], "ratio (%)": []})
    ratio = (counts / counts.sum() * 100).round(1)
    return pd.DataFrame({
        column_name: counts.index,
        "count": counts.values,
        "ratio (%)": ratio.values
    })

# ============================
# ★ グラフ生成関数
# ============================
def show_ratio_chart(title, column_name):
    st.subheader(title)
    ratio_df = make_ratio_df(column_name, df_filtered)

    if len(ratio_df) == 0:
        st.write("データがありません")
        return

    chart = alt.Chart(ratio_df).mark_bar().encode(
        x=alt.X(f"{column_name}:N", title=title),
        y=alt.Y("ratio (%):Q", title="割合 (%)"),
        tooltip=[column_name, "count", "ratio (%)"]
    )
    st.altair_chart(chart, use_container_width=True)

# ============================
# ★ 各特徴の割合グラフ（新仕様対応）
# ============================

# 髪の長さ
show_ratio_chart("髪の長さ", "hair_length")

# 髪色（大分類・中分類・細分類）
show_ratio_chart("髪色（大分類）", "hair_color_main")
show_ratio_chart("髪色（中分類）", "hair_color_sub")

# 髪型（大分類・中分類・細分類）
show_ratio_chart("髪型（大分類）", "hairstyle_main")
show_ratio_chart("髪型（中分類）", "hairstyle_type")
show_ratio_chart("髪型（細分類）", "hairstyle_detail")

# その他の特徴
show_ratio_chart("目の色", "eye_color")
show_ratio_chart("目の形", "eye_shape")
show_ratio_chart("表情", "expression")
show_ratio_chart("雰囲気", "vibe")