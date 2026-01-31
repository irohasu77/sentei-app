import streamlit as st
import os
import json
import random
from PIL import Image
from io import BytesIO
import base64

IMAGE_DIR = "characters"
FEATURE_FILE = "character_features.json"
SELECTED_FILE = "selected.json"

st.title("キャラ選択（ランダム2枚から選ぶ）")

# ---------------------------------------------------
# 初期化
# ---------------------------------------------------

if "started" not in st.session_state:
    st.session_state["started"] = False

if "finished" not in st.session_state:
    st.session_state["finished"] = False

# ---------------------------------------------------
# スタート / リセット
# ---------------------------------------------------

col_start, col_reset = st.columns(2)

if col_start.button("スタート"):
    if os.path.exists(SELECTED_FILE):
        os.remove(SELECTED_FILE)

    st.session_state["selected"] = []
    st.session_state["count"] = 0
    st.session_state["pair"] = None
    st.session_state["started"] = True
    st.session_state["finished"] = False

    st.success("新しい選択を開始します！")
    st.rerun()

if col_reset.button("リセット"):
    if os.path.exists(SELECTED_FILE):
        os.remove(SELECTED_FILE)

    st.session_state.clear()
    st.session_state["started"] = False
    st.session_state["finished"] = False
    st.success("データをリセットしました")
    st.rerun()

# ---------------------------------------------------
# スタート前
# ---------------------------------------------------

if not st.session_state["started"]:
    st.info("スタートを押して選択を開始してください")
    st.stop()

# ---------------------------------------------------
# JSON読み込み
# ---------------------------------------------------

with open(FEATURE_FILE, "r", encoding="utf-8") as f:
    features = json.load(f)

images = list(features.keys())

if "selected" not in st.session_state:
    if os.path.exists(SELECTED_FILE):
        with open(SELECTED_FILE, "r", encoding="utf-8") as f:
            st.session_state["selected"] = json.load(f)
    else:
        st.session_state["selected"] = []

if "count" not in st.session_state:
    st.session_state["count"] = len(st.session_state["selected"])

st.write(f"現在の選択数：{st.session_state['count']} / 10")

# ---------------------------------------------------
# 10回で自動遷移
# ---------------------------------------------------

if st.session_state["count"] >= 10 and not st.session_state["finished"]:

    with open(SELECTED_FILE, "w", encoding="utf-8") as f:
        json.dump(st.session_state["selected"], f, ensure_ascii=False, indent=4)

    st.session_state["finished"] = True
    st.success("10回の選択が完了しました！次のページへ移動します。")
    st.switch_page("pages/4連関分析.py")
    st.stop()

if st.session_state["finished"]:
    st.info("選択は完了しています。リセットして再開できます。")
    st.stop()

# ---------------------------------------------------
# ランダム2枚
# ---------------------------------------------------
if "used" not in st.session_state:
    st.session_state["used"] = []

if "pair" not in st.session_state or st.session_state["pair"] is None:

    used = st.session_state["used"]

    remaining = [img for img in images if img not in used]

    if len(remaining) < 2:
        st.warning("選べる画像がもうありません")
        st.stop()

    st.session_state["pair"] = random.sample(remaining, 2)

img1, img2 = st.session_state["pair"]

col1, col2 = st.columns(2)

# ---------------------------------------------------
# 正方形サムネイル生成
# ---------------------------------------------------

TARGET_HEIGHT = 300
CANVAS_SIZE = 320

def make_square_thumbnail(path):
    img = Image.open(path).convert("RGB")
    w, h = img.size

    new_w = int(w * (TARGET_HEIGHT / h))
    img = img.resize((new_w, TARGET_HEIGHT))

    canvas = Image.new("RGB", (CANVAS_SIZE, CANVAS_SIZE), (255, 255, 255))
    x = (CANVAS_SIZE - new_w) // 2
    y = (CANVAS_SIZE - TARGET_HEIGHT) // 2
    canvas.paste(img, (x, y))

    buffer = BytesIO()
    canvas.save(buffer, format="PNG")
    return base64.b64encode(buffer.getvalue()).decode()

def show_square_thumbnail(path):
    img_base64 = make_square_thumbnail(path)

    html = f"""
        <style>
        .thumb {{
            border: 4px solid #888;
            border-radius: 10px;
            padding: 5px;
            margin-bottom: 10px;
        }}
        .thumb img {{
            width: 100%;
            border-radius: 6px;
        }}
        </style>

        <div class="thumb">
            <img src="data:image/png;base64,{img_base64}">
        </div>
    """
    st.markdown(html, unsafe_allow_html=True)

# ---------------------------------------------------
# ボタン（キャラ名）＋ サムネイル
# ---------------------------------------------------
with col1:
    label1 = features[img1]["name"]
    if st.button(label1, use_container_width=True):
        st.session_state["selected"].append(img1)
        st.session_state["used"].extend([img1, img2])
        st.session_state["pair"] = None
        st.session_state["count"] += 1
        st.rerun()

    show_square_thumbnail(os.path.join(IMAGE_DIR, img1))

with col2:
    label2 = features[img2]["name"]
    if st.button(label2, use_container_width=True):
        st.session_state["selected"].append(img2)
        st.session_state["used"].extend([img1, img2])
        st.session_state["pair"] = None
        st.session_state["count"] += 1
        st.rerun()

    show_square_thumbnail(os.path.join(IMAGE_DIR, img2))

# ---------------------------------------------------
# 保存
# ---------------------------------------------------

with open(SELECTED_FILE, "w", encoding="utf-8") as f:
    json.dump(st.session_state["selected"], f, ensure_ascii=False, indent=4)