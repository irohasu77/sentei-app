import streamlit as st
import os
import json
from PIL import Image
import torch
from transformers import CLIPProcessor, CLIPModel

st.set_page_config(layout="wide")

# ============================
# 設定
# ============================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
IMAGE_DIR = os.path.join(BASE_DIR, "characters")
FEATURE_FILE = os.path.join(BASE_DIR, "character_features.json")

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
# JSON保存
# ============================
def save_json():
    with open(FEATURE_FILE, "w", encoding="utf-8") as f:
        json.dump(features, f, ensure_ascii=False, indent=4)

def save_if_changed(key, new_value):
    if key not in st.session_state:
        st.session_state[key] = new_value
        return
    if st.session_state[key] != new_value:
        st.session_state[key] = new_value
        save_json()

'''
# ============================
# CLIPモデル読み込み
# ============================

clip_model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32")
clip_processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")


# ============================
# 推定関数（髪色は大分類のみ）
# ============================
def predict_hair_color_main(image_path):
    image = Image.open(image_path).convert("RGB")
    texts = list(HAIR_COLOR_MAP.keys())
    inputs = clip_processor(text=texts, images=image, return_tensors="pt", padding=True)
    with torch.no_grad():
        outputs = clip_model(**inputs)
    idx = outputs.logits_per_image.softmax(dim=1).argmax().item()
    return texts[idx]

def predict_hair_length(image_path):
    image = Image.open(image_path).convert("RGB")
    texts = ["short hair", "medium hair", "long hair"]
    inputs = clip_processor(text=texts, images=image, return_tensors="pt", padding=True)
    with torch.no_grad():
        outputs = clip_model(**inputs)
    return texts[outputs.logits_per_image.softmax(dim=1).argmax().item()]

def predict_eye_color(image_path):
    image = Image.open(image_path).convert("RGB")
    texts = [
        "black eyes", "brown eyes", "blue eyes", "green eyes",
        "red eyes", "yellow eyes", "purple eyes", "pink eyes", "grey eyes"
    ]
    inputs = clip_processor(text=texts, images=image, return_tensors="pt", padding=True)
    with torch.no_grad():
        outputs = clip_model(**inputs)
    return texts[outputs.logits_per_image.softmax(dim=1).argmax().item()]

def predict_eye_shape(image_path):
    image = Image.open(image_path).convert("RGB")
    texts = ["big eyes", "sharp eyes", "round eyes", "narrow eyes", "droopy eyes"]
    inputs = clip_processor(text=texts, images=image, return_tensors="pt", padding=True)
    with torch.no_grad():
        outputs = clip_model(**inputs)
    return texts[outputs.logits_per_image.softmax(dim=1).argmax().item()]

def predict_expression(image_path):
    image = Image.open(image_path).convert("RGB")
    texts = ["smiling", "serious expression", "angry", "shy", "sad", "surprised"]
    inputs = clip_processor(text=texts, images=image, return_tensors="pt", padding=True)
    with torch.no_grad():
        outputs = clip_model(**inputs)
    return texts[outputs.logits_per_image.softmax(dim=1).argmax().item()]

def predict_vibe(image_path):
    image = Image.open(image_path).convert("RGB")
    texts = ["cute girl", "cool girl", "elegant girl", "energetic girl", "mysterious girl"]
    inputs = clip_processor(text=texts, images=image, return_tensors="pt", padding=True)
    with torch.no_grad():
        outputs = clip_model(**inputs)
    return texts[outputs.logits_per_image.softmax(dim=1).argmax().item()]

# ============================
# AI推定まとめ
# ============================
def analyze_character(image_path):
    hair_color_main = predict_hair_color_main(image_path)

    return {
        "name": "",
        "work": "",
        "hair_length": predict_hair_length(image_path),

        # 髪色（大分類＋中分類）
        "hair_color_main": hair_color_main,
        "hair_color_sub": "",

        # 髪型（大分類・中分類・細分類）
        "hairstyle_main": "",
        "hairstyle_type": "",
        "hairstyle_detail": "",

        "eye_color": predict_eye_color(image_path),
        "eye_shape": predict_eye_shape(image_path),
        "expression": predict_expression(image_path),
        "vibe": predict_vibe(image_path),
        "other": ""
    }
'''

# ============================
# JSON読み込み
# ============================
if os.path.exists(FEATURE_FILE):
    try:
        with open(FEATURE_FILE, "r", encoding="utf-8") as f:
            features = json.load(f)
    except:
        features = {}
else:
    features = {}

# ============================
# UI
# ============================
st.title("キャラ管理アプリ（編集＋保存）")

files = os.listdir(IMAGE_DIR)
image_files = [f for f in files if f.lower().endswith((".png", ".jpg", ".jpeg"))]
image_files.sort()

col1, col2 = st.columns([1, 3])

# ============================
# 左：画像一覧
# ============================
with col1:
    st.header("画像一覧")

    # ============================
    # 名前検索欄（追加部分）
    # ============================
    if "selected_image" not in st.session_state:
        st.session_state["selected_image"] = image_files[0]

    all_names = []
    name_to_img = {}

    for img in image_files:
        data = features.get(img, {})
        name = data.get("name", "")
        if name:
            all_names.append(name)
            name_to_img[name] = img

    search_name = st.selectbox("名前で検索", [""] + all_names)

    # 検索されたら選択中キャラを書き換え（rerunしない）
    if search_name:
        st.session_state["selected_image"] = name_to_img[search_name]

    # ============================
    # 画像一覧（radio）
    # ============================
    display_labels = []
    for img in image_files:
        data = features.get(img, {})
        name = data.get("name", "")
        label = f"{name}_{img}" if name else img
        display_labels.append(label)

    # ★ radio の index を「必ず selected_image から決める」
    current_index = image_files.index(st.session_state["selected_image"])

    selected_index = st.radio(
        "キャラを選択",
        list(range(len(image_files))),
        format_func=lambda i: display_labels[i],
        index=current_index,   # ← これが常に最新になる
        key=f"radio_{st.session_state['selected_image']}"
    )

    selected_radio = image_files[selected_index]

    if selected_radio != st.session_state["selected_image"]:
        st.session_state["selected_image"] = selected_radio

selected = st.session_state["selected_image"]

# ============================
# 右：画像プレビュー + 特徴編集
# ============================
with col2:
    if selected:

        col_img, col_form = st.columns([1, 1])

        # ----------------------------
        # 左：画像プレビュー
        # ----------------------------
        with col_img:
            st.header("画像プレビュー")
            st.markdown("<div style='margin-top:200px;'></div>", unsafe_allow_html=True)
            img_path = os.path.join(IMAGE_DIR, selected)
            img = Image.open(img_path)
            st.image(img, width=1500)

            # ============================
            # ◀ 前へ / 次へ ▶ ボタン
            # ============================

            prev_col, next_col = st.columns(2)

            current_idx = image_files.index(st.session_state["selected_image"])

            with prev_col:
                if st.button("◀ 前のキャラ"):
                    if current_idx > 0:
                        st.session_state["selected_image"] = image_files[current_idx - 1]

            with next_col:
                if st.button("次のキャラ ▶"):
                    if current_idx < len(image_files) - 1:
                        st.session_state["selected_image"] = image_files[current_idx + 1]

        # ----------------------------
        # 右：特徴編集フォーム
        # ----------------------------
        with col_form:
            st.header("特徴データ（編集可能）")

            data = features.get(selected, {
                "name": "",
                "work": "",
                "hair_length": "",
                "hair_color_main": "",
                "hair_color_sub": "",
                "hairstyle_main": "",
                "hairstyle_type": "",
                "hairstyle_detail": "",
                "eye_color": "",
                "eye_shape": "",
                "expression": "",
                "vibe": "",
                "other": ""
            })

            # 名前
            char_name = st.text_input("名前", data["name"], key=f"widget_name_{selected}")
            save_if_changed(f"data_name_{selected}", char_name)

            # 作品名
            work = st.text_input("作品名", data.get("work", ""), key=f"widget_work_{selected}")
            save_if_changed(f"data_work_{selected}", work)

            # 髪色（大分類）
            hair_color_main_options = [""] + list(HAIR_COLOR_MAP.keys())
            current_color_main = data.get("hair_color_main", "")
            hair_color_main = st.selectbox(
                "髪色（大分類）",
                hair_color_main_options,
                index=hair_color_main_options.index(current_color_main) if current_color_main in hair_color_main_options else 0,
                key=f"widget_hair_color_main_{selected}"
            )
            save_if_changed(f"data_hair_color_main_{selected}", hair_color_main)

            # 髪色（中分類）
            sub_options = [""] if hair_color_main == "" else [""] + HAIR_COLOR_MAP[hair_color_main]
            current_color_sub = data.get("hair_color_sub", "")
            hair_color_sub = st.selectbox(
                "髪色（中分類）",
                sub_options,
                index=sub_options.index(current_color_sub) if current_color_sub in sub_options else 0,
                key=f"widget_hair_color_sub_{selected}"
            )
            save_if_changed(f"data_hair_color_sub_{selected}", hair_color_sub)

            # 髪の長さ
            hair_length_options = ["", "short hair", "medium hair", "long hair"]
            hair_length = st.selectbox(
                "髪の長さ",
                hair_length_options,
                index=hair_length_options.index(data["hair_length"]) if data["hair_length"] in hair_length_options else 0,
                key=f"widget_hair_length_{selected}"
            )
            save_if_changed(f"data_hair_length_{selected}", hair_length)

            # 髪型（大分類）
            hairstyle_main_options = [""] + list(HAIRSTYLE_MAP.keys())
            current_main = data.get("hairstyle_main", "")
            hairstyle_main = st.selectbox(
                "髪型（大分類）",
                hairstyle_main_options,
                index=hairstyle_main_options.index(current_main) if current_main in hairstyle_main_options else 0,
                key=f"widget_hairstyle_main_{selected}"
            )
            save_if_changed(f"data_hairstyle_main_{selected}", hairstyle_main)

            # 髪型（中分類）
            type_options = [""] if hairstyle_main == "" else [""] + HAIRSTYLE_MAP[hairstyle_main]["type"]
            current_type = data.get("hairstyle_type", "")
            hairstyle_type = st.selectbox(
                "髪型（中分類）",
                type_options,
                index=type_options.index(current_type) if current_type in type_options else 0,
                key=f"widget_hairstyle_type_{selected}"
            )
            save_if_changed(f"data_hairstyle_type_{selected}", hairstyle_type)

            # 髪型（細分類）
            detail_options = [""] if hairstyle_main == "" else [""] + HAIRSTYLE_MAP[hairstyle_main]["detail"]
            current_detail = data.get("hairstyle_detail", "")
            hairstyle_detail = st.selectbox(
                "髪型（細分類）",
                detail_options,
                index=detail_options.index(current_detail) if current_detail in detail_options else 0,
                key=f"widget_hairstyle_detail_{selected}"
            )
            save_if_changed(f"data_hairstyle_detail_{selected}", hairstyle_detail)

            # 目の色
            eye_color_options = [
                "", "black eyes", "brown eyes", "blue eyes", "green eyes",
                "red eyes", "yellow eyes", "purple eyes", "pink eyes", "grey eyes"
            ]
            eye_color = st.selectbox(
                "目の色",
                eye_color_options,
                index=eye_color_options.index(data["eye_color"]) if data["eye_color"] in eye_color_options else 0,
                key=f"widget_eye_color_{selected}"
            )
            save_if_changed(f"data_eye_color_{selected}", eye_color)

            # 目の形
            eye_shape_options = ["", "big eyes", "sharp eyes", "round eyes", "narrow eyes", "droopy eyes"]
            eye_shape = st.selectbox(
                "目の形",
                eye_shape_options,
                index=eye_shape_options.index(data["eye_shape"]) if data["eye_shape"] in eye_shape_options else 0,
                key=f"widget_eye_shape_{selected}"
            )
            save_if_changed(f"data_eye_shape_{selected}", eye_shape)

            # 表情
            expression_options = ["", "smiling", "serious expression", "angry", "shy", "sad", "surprised"]
            expression = st.selectbox(
                "表情",
                expression_options,
                index=expression_options.index(data["expression"]) if data["expression"] in expression_options else 0,
                key=f"widget_expression_{selected}"
            )
            save_if_changed(f"data_expression_{selected}", expression)

            # 雰囲気
            vibe_options = ["", "cute girl", "cool girl", "elegant girl", "energetic girl", "mysterious girl"]
            vibe = st.selectbox(
                "雰囲気",
                vibe_options,
                index=vibe_options.index(data["vibe"]) if data["vibe"] in vibe_options else 0,
                key=f"widget_vibe_{selected}"
            )
            save_if_changed(f"data_vibe_{selected}", vibe)

            # その他
            other = st.text_input("その他", data["other"], key=f"widget_other_{selected}")
            save_if_changed(f"data_other_{selected}", other)

                        # ============================
            # JSON保存
            # ============================
            features[selected] = {
                "name": st.session_state.get(f"data_name_{selected}", ""),
                "work": st.session_state.get(f"data_work_{selected}", ""),

                # 髪色（大分類＋中分類）
                "hair_color_main": st.session_state.get(f"data_hair_color_main_{selected}", ""),
                "hair_color_sub": st.session_state.get(f"data_hair_color_sub_{selected}", ""),

                # 髪の長さ
                "hair_length": st.session_state.get(f"data_hair_length_{selected}", ""),

                # 髪型（大分類・中分類・細分類）
                "hairstyle_main": st.session_state.get(f"data_hairstyle_main_{selected}", ""),
                "hairstyle_type": st.session_state.get(f"data_hairstyle_type_{selected}", ""),
                "hairstyle_detail": st.session_state.get(f"data_hairstyle_detail_{selected}", ""),

                # 目
                "eye_color": st.session_state.get(f"data_eye_color_{selected}", ""),
                "eye_shape": st.session_state.get(f"data_eye_shape_{selected}", ""),

                # 表情・雰囲気
                "expression": st.session_state.get(f"data_expression_{selected}", ""),
                "vibe": st.session_state.get(f"data_vibe_{selected}", ""),

                # その他
                "other": st.session_state.get(f"data_other_{selected}", "")
            }

            save_json()
            st.success("保存しました！")
