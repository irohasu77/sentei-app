import streamlit as st
import os
import json
from PIL import Image

st.set_page_config(layout="wide")

IMAGE_DIR = "characters"
FEATURE_FILE = "character_features.json"

# ============================
# 髪色分類体系（大分類→中分類）
# ============================
HAIR_COLOR_MAP = {
    "black": ["jet black", "soft black"],
    "brown": ["dark brown", "light brown", "chestnut"],
    "blonde": ["golden blonde", "ash blonde", "platinum blonde"],
    "blue": ["dark blue", "light blue", "sky blue"],
    "red": ["dark red", "light red"],
    "pink": ["vivid pink", "pastel pink"],
    "green": ["dark green", "mint green"],
    "purple": ["dark purple", "lavender"],
    "white": ["pure white", "off white"],
    "silver": ["silver", "metallic silver"]
}

# ============================
# 髪型分類体系（大分類→中分類→細分類）
# ============================
HAIRSTYLE_MAP = {
    "straight": {
        "type": ["long straight", "medium straight", "short straight", "pigtails", "one-length"],
        "detail": ["center parted", "side parted", "see-through bangs", "straight bangs", "himecut"]
    },
    "wavy": {
        "type": ["loose wave", "medium wave", "strong wave"],
        "detail": ["fluffy wave", "beach wave"]
    },
    "curly": {
        "type": ["loose curls", "tight curls", "perm curls"],
        "detail": ["ringlet curls", "afro curls"]
    },
    "ponytail": {
        "type": ["high ponytail", "low ponytail", "side ponytail"],
        "detail": ["straight ponytail","messy ponytail", "ribbon ponytail"]
    },
    "twintail": {
        "type": ["high twintails", "low twintails", "side twintails", "half-up twintails"],
        "detail": ["straight twintail","drill twintails", "curly twintails"]
    },
    "bob": {
        "type": ["short bob", "medium bob", "layered bob", "inner curl bob"],
        "detail": ["straight bob", "wavy bob"]
    },
    "braid": {
        "type": ["single braid", "double braids", "side braid", "half braid", "french braid"],
        "detail": ["braided ponytail", "braided bun"]
    },
    "bun": {
        "type": ["single bun", "twin buns"],
        "detail": ["messy bun", "braided bun"]
    }
}

st.title("キャラ検索(フィルタ)")

# JSON読み込み
if os.path.exists(FEATURE_FILE):
    with open(FEATURE_FILE, "r", encoding="utf-8") as f:
        features = json.load(f)
else:
    features = {}

# ============================
# キャラ名・作品名
# ============================
name_options = [""] + sorted({data.get("name", "") for data in features.values() if data.get("name")})
work_options = [""] + sorted({data.get("work", "") for data in features.values() if data.get("work")})

# ============================
# サイドバー
# ============================
st.sidebar.header("検索条件")

sel_name = st.sidebar.selectbox("キャラ名", name_options)
sel_work = st.sidebar.selectbox("作品名", work_options)

# ============================
# 髪色（大分類→中分類）
# ============================
hair_color_main_options = [""] + list(HAIR_COLOR_MAP.keys())
sel_hair_color_main = st.sidebar.selectbox("髪色（大分類）", hair_color_main_options)

# 中分類は大分類に応じて変化
if sel_hair_color_main:
    hair_color_sub_options = [""] + HAIR_COLOR_MAP[sel_hair_color_main]
else:
    # 全サブカラーを集める
    all_sub = []
    for subs in HAIR_COLOR_MAP.values():
        all_sub.extend(subs)
    hair_color_sub_options = [""] + sorted(all_sub)

sel_hair_color_sub = st.sidebar.selectbox("髪色（中分類）", hair_color_sub_options)

# ============================
# 髪の長さ
# ============================
hair_length_options = ["", "short hair", "medium hair", "long hair"]
sel_length = st.sidebar.selectbox("髪の長さ", hair_length_options)

# ============================
# 髪型（大分類→中分類→細分類）
# ============================
hairstyle_main_options = [""] + list(HAIRSTYLE_MAP.keys())
sel_hairstyle_main = st.sidebar.selectbox("髪型（大分類）", hairstyle_main_options)

# 中分類
if sel_hairstyle_main:
    hairstyle_type_options = [""] + HAIRSTYLE_MAP[sel_hairstyle_main]["type"]
else:
    # 全タイプ
    all_types = []
    for v in HAIRSTYLE_MAP.values():
        all_types.extend(v["type"])
    hairstyle_type_options = [""] + sorted(all_types)

sel_hairstyle_type = st.sidebar.selectbox("髪型（中分類）", hairstyle_type_options)

# 細分類
if sel_hairstyle_main:
    hairstyle_detail_options = [""] + HAIRSTYLE_MAP[sel_hairstyle_main]["detail"]
else:
    # 全細分類
    all_details = []
    for v in HAIRSTYLE_MAP.values():
        all_details.extend(v["detail"])
    hairstyle_detail_options = [""] + sorted(all_details)

sel_hairstyle_detail = st.sidebar.selectbox("髪型（細分類）", hairstyle_detail_options)

# ============================
# その他の特徴
# ============================
eye_color_options = [
    "", "black eyes", "brown eyes", "blue eyes", "green eyes",
    "red eyes", "yellow eyes", "purple eyes", "pink eyes", "grey eyes"
]
sel_eye = st.sidebar.selectbox("目の色", eye_color_options)

eye_shape_options = ["", "big eyes", "sharp eyes", "round eyes", "narrow eyes", "droopy eyes"]
sel_eye_shape = st.sidebar.selectbox("目の形", eye_shape_options)

expression_options = ["", "smiling", "serious expression", "angry", "shy", "sad", "surprised"]
sel_expression = st.sidebar.selectbox("表情", expression_options)

vibe_options = ["", "cute girl", "cool girl", "elegant girl", "energetic girl", "mysterious girl"]
sel_vibe = st.sidebar.selectbox("雰囲気", vibe_options)

# ============================
# フィルタ処理
# ============================
results = []
for filename, data in features.items():

    if sel_name and data.get("name") != sel_name:
        continue
    if sel_work and data.get("work") != sel_work:
        continue

    # 髪色（大分類＋中分類）
    if sel_hair_color_main and data.get("hair_color_main") != sel_hair_color_main:
        continue
    if sel_hair_color_sub and data.get("hair_color_sub") != sel_hair_color_sub:
        continue

    # 髪の長さ
    if sel_length and data.get("hair_length") != sel_length:
        continue

    # 髪型（大分類＋中分類＋細分類）
    if sel_hairstyle_main and data.get("hairstyle_main") != sel_hairstyle_main:
        continue
    if sel_hairstyle_type and data.get("hairstyle_type") != sel_hairstyle_type:
        continue
    if sel_hairstyle_detail and data.get("hairstyle_detail") != sel_hairstyle_detail:
        continue

    # その他
    if sel_eye and data.get("eye_color") != sel_eye:
        continue
    if sel_eye_shape and data.get("eye_shape") != sel_eye_shape:
        continue
    if sel_expression and data.get("expression") != sel_expression:
        continue
    if sel_vibe and data.get("vibe") != sel_vibe:
        continue

    results.append(filename)

st.write(f"検索結果：{len(results)}件")

# ============================
# 結果表示
# ============================
TARGET_HEIGHT = 200
CANVAS_SIZE = 200  # キャンバスの縦横（好きに調整できる）

cols = st.columns(3)

for idx, r in enumerate(results):
    with cols[idx % 3]:
        img = Image.open(os.path.join(IMAGE_DIR, r)).convert("RGB")

        # 元サイズ
        w, h = img.size

        # 高さを揃えて比率維持でリサイズ
        new_w = int(w * (TARGET_HEIGHT / h))
        img = img.resize((new_w, TARGET_HEIGHT))

        # ★ 正方形キャンバスを作成（白背景）
        canvas = Image.new("RGB", (CANVAS_SIZE, CANVAS_SIZE), (255, 255, 255))

        # 中央に貼り付ける位置を計算
        x = (CANVAS_SIZE - new_w) // 2
        y = (CANVAS_SIZE - TARGET_HEIGHT) // 2

        canvas.paste(img, (x, y))

        caption = features[r].get("name", r)
        st.image(canvas, caption=caption)
