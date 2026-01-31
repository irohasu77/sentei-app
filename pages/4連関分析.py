import streamlit as st
import os
import json
import pandas as pd
from mlxtend.frequent_patterns import apriori, association_rules
import base64
import requests

import altair as alt
# Altair の巨大データ埋め込みを防ぐ
alt.data_transformers.disable_max_rows()
alt.data_transformers.enable('json')

FEATURE_FILE = "character_features.json"
SELECTED_FILE = "selected.json"

st.title("連関分析（好みの特徴を抽出）")

# ---------------------------------------------------
# データ読み込み
# ---------------------------------------------------

with open(FEATURE_FILE, "r", encoding="utf-8") as f:
    features = json.load(f)

if not os.path.exists(SELECTED_FILE):
    st.write("まだ選択データがありません")
    st.stop()

with open(SELECTED_FILE, "r", encoding="utf-8") as f:
    selected = json.load(f)

# 選択されたキャラの特徴をまとめる
selected_features = [features[img] for img in selected]

# DataFrame 化
df = pd.DataFrame(selected_features)

# name, work, other を元データから削除
df = df.drop(columns=["name", "work", "other"], errors="ignore")

# ★ 行番号を 1 始まりにする
df.index = df.index + 1
df.index.name = "No."

# ---------------------------------------------------
# 表示
# ---------------------------------------------------

st.subheader("選ばれた特徴一覧")
st.dataframe(df)

# ---------------------------------------------------
# アソシエーション分析
# ---------------------------------------------------
# One-hot 化
df_hot = pd.get_dummies(df)

# name_〇〇, other_〇〇 を完全に除去
df_hot = df_hot[[c for c in df_hot.columns
                 if not c.startswith("name_")
                 and not c.startswith("other_")
                 and not c.startswith("work_")]]

# 重み付け（専用最適化）
for col in df_hot.columns:

    # 髪型（最重要）
    if "hairstyle_detail" in col:
        df_hot[col] *= 3.0
    elif "hairstyle_type" in col:
        df_hot[col] *= 2.5
    elif "hairstyle_main" in col:
        df_hot[col] *= 2.0

    # 髪の長さ
    elif "hair_length" in col:
        df_hot[col] *= 2.0

    # 髪色（大分類・中分類）
    elif "hair_color_main" in col:
        df_hot[col] *= 1.8
    elif "hair_color_sub" in col:
        df_hot[col] *= 1.5

    # 目の色・形（中間）
    elif "eye_color" in col:
        df_hot[col] *= 1.0
    elif "eye_shape" in col:
        df_hot[col] *= 0.8

    # 表情・雰囲気（弱め）
    elif "expression" in col:
        df_hot[col] *= 0.5
    elif "vibe" in col:
        df_hot[col] *= 0.5

# 正規化（重みの暴れを抑える）
df_hot = df_hot / df_hot.max()

# apriori（精度向上版）
frequent = apriori(df_hot, min_support=0.25, use_colnames=True)
rules = association_rules(frequent, metric="lift", min_threshold=1.1)
rules = rules.sort_values("lift", ascending=False)

st.subheader("連関分析結果")
st.dataframe(rules.head(50))

# ---------------------------------------------------
# 好みの特徴抽出
# ---------------------------------------------------

top_features = set()
for _, row in rules.iterrows():
    top_features |= row["antecedents"]
    top_features |= row["consequents"]

top_features = list(top_features)

st.subheader("好みの特徴（抽出）")
st.write(top_features)

# ---------------------------------------------------
# プロンプト生成
# ---------------------------------------------------
BASE_PROMPT = "masterpiece, best quality, amazing quality, 4k, very aesthetic, high resolution, ultra-detailed, absurdres, newest, anime, anime coloring, 1girl, solo, wearing clothes,eyes that feel natural, pupil, cute eyes"
NEGATIVE_PROMPT = "photorealistic, realistic, 3d, Two-toned hair, multiple views, multiple angle, split view, grid view, two shot, outside border, picture frame, framed, border, letterboxed, pillarboxed, 2koma, old, oldest, cartoon, graphic, text, painting, crayon, graphite, abstract, glitch, deformed, mutated, ugly, disfigured, long body, lowres, bad anatomy, bad hands, missing fingers, extra fingers, extra digits, fewer digits, cropped, very displeasing, (worst quality, bad quality:1.2), sketch, jpeg artifacts, signature, watermark, username, (censored, bar_censor, mosaic_censor:1.2), conjoined, bad ai-generated, Steps: 20, Sampler: Euler a, CFG scale: 4.5, Global Seed: 428649103, Seed: 3282307999, Size: 768x1344,Clip skip: 2, Model hash: 6a2e0c8dd7, Model: NovaAnimeILV15, Hires steps: 40, Hires upscale: 1.5, DPM++ 2M, Schedule type: Karras, CFG scale: 7, Seed: 2147104563, Size: 512x640, Model hash: 6a2e0c8dd7, Model: novaAnimeXL_ilV150, Denoising strength: 0.7, Hires Module 1: Use same choices, Hires CFG Scale: 7, Hires upscale: 2, Hires upscaler: Latent, Version: f2.0.1v1.10.1-1.10.1, nsfw, sheer clothing"
prompt = BASE_PROMPT + ", " + ", ".join(top_features)

payload = {
    "prompt": prompt,
    "negative_prompt": NEGATIVE_PROMPT,
    "steps": 20,
    "sampler_name": "DPM++ 2M Karras",
    "override_settings": {"sd_model_checkpoint": "AnythingXL_inkBase.safetensors"},
    "width": 832,
    "height": 1216
}

st.subheader("生成プロンプト")
st.code(prompt)

st.session_state["prompt"] = prompt

# ---------------------------------------------------
# 画像生成
# ---------------------------------------------------

API_URL = "http://127.0.0.1:7860/sdapi/v1/txt2img"

st.subheader("画像生成")

if st.button("このプロンプトで画像生成する"):
    with st.spinner("生成中..."):

        response = requests.post(API_URL, json=payload)

        if response.status_code != 200:
            st.error(f"エラー: {response.text}")
            st.stop()

        r = response.json()
        image_base64 = r["images"][0]
        image_bytes = base64.b64decode(image_base64)

        st.image(image_bytes, caption="生成画像", use_column_width=True)
        st.session_state["generated_image"] = image_bytes

# 保存ボタン
import time

if "generated_image" in st.session_state:
    if st.button("画像を保存する"):
        save_path = r"C:\AI\stable-diffusion-webui-forge-main\outputs\AI-images"
        os.makedirs(save_path, exist_ok=True)

        filename = f"generated_{int(time.time())}.png"
        file_path = os.path.join(save_path, filename)

        with open(file_path, "wb") as f:
            f.write(st.session_state["generated_image"])

        st.success(f"保存しました: {file_path}")
