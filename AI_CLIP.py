'''
import os
import json
from PIL import Image
import torch
from transformers import CLIPProcessor, CLIPModel

# ============================
# 設定
# ============================
IMAGE_DIR = r"characters"
FEATURE_FILE = r"character_features.json"

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
# CLIPモデル読み込み
# ============================
clip_model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32")
clip_processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")

# ============================
# 髪型大分類の推定
# ============================
def predict_hairstyle_main(image_path):
    image = Image.open(image_path).convert("RGB")

    texts = [
        "straight hair",
        "wavy hair",
        "curly hair",
        "ponytail",
        "twin tails",
        "bob cut",
        "braid hair",
        "bun hair"
    ]

    inputs = clip_processor(text=texts, images=image, return_tensors="pt", padding=True)

    with torch.no_grad():
        outputs = clip_model(**inputs)

    idx = outputs.logits_per_image.softmax(dim=1).argmax().item()
    return texts[idx]

# ============================
# CLIP → hairstyle_main の変換
# ============================
def map_clip_hairstyle_to_main(text):
    mapping = {
        "straight hair": "straight",
        "wavy hair": "wavy",
        "curly hair": "curly",
        "ponytail": "ponytail",
        "twin tails": "twintail",
        "bob cut": "bob",
        "braid hair": "braid",
        "bun hair": "bun"
    }
    return mapping.get(text, "")

# ============================
# 髪色（大分類）の推定
# ============================
def predict_hair_color_main(image_path):
    image = Image.open(image_path).convert("RGB")
    texts = list(HAIR_COLOR_MAP.keys())  # 大分類だけ
    inputs = clip_processor(text=texts, images=image, return_tensors="pt", padding=True)

    with torch.no_grad():
        outputs = clip_model(**inputs)

    idx = outputs.logits_per_image.softmax(dim=1).argmax().item()
    return texts[idx]

# ============================
# その他の推定関数
# ============================
def predict_eye_color(image_path):
    image = Image.open(image_path).convert("RGB")
    eye_texts = [
        "black eyes", "brown eyes", "blue eyes", "green eyes",
        "red eyes", "yellow eyes", "purple eyes", "pink eyes", "grey eyes"
    ]
    inputs = clip_processor(text=eye_texts, images=image, return_tensors="pt", padding=True)
    with torch.no_grad():
        outputs = clip_model(**inputs)
    idx = outputs.logits_per_image.softmax(dim=1).argmax().item()
    return eye_texts[idx]

def predict_hair_length(image_path):
    image = Image.open(image_path).convert("RGB")
    length_texts = ["short hair", "medium hair", "long hair"]
    inputs = clip_processor(text=length_texts, images=image, return_tensors="pt", padding=True)
    with torch.no_grad():
        outputs = clip_model(**inputs)
    idx = outputs.logits_per_image.softmax(dim=1).argmax().item()
    return length_texts[idx]

def predict_expression(image_path):
    image = Image.open(image_path).convert("RGB")
    texts = ["smiling", "serious expression", "angry", "shy", "sad", "surprised"]
    inputs = clip_processor(text=texts, images=image, return_tensors="pt", padding=True)
    with torch.no_grad():
        outputs = clip_model(**inputs)
    idx = outputs.logits_per_image.softmax(dim=1).argmax().item()
    return texts[idx]

def predict_vibe(image_path):
    image = Image.open(image_path).convert("RGB")
    texts = ["cute girl", "cool girl", "elegant girl", "energetic girl", "mysterious girl"]
    inputs = clip_processor(text=texts, images=image, return_tensors="pt", padding=True)
    with torch.no_grad():
        outputs = clip_model(**inputs)
    idx = outputs.logits_per_image.softmax(dim=1).argmax().item()
    return texts[idx]

def predict_eye_shape(image_path):
    image = Image.open(image_path).convert("RGB")
    texts = ["big eyes", "sharp eyes", "round eyes", "narrow eyes", "droopy eyes"]
    inputs = clip_processor(text=texts, images=image, return_tensors="pt", padding=True)
    with torch.no_grad():
        outputs = clip_model(**inputs)
    idx = outputs.logits_per_image.softmax(dim=1).argmax().item()
    return texts[idx]

# ============================
# 特徴推定まとめ（髪色は大分類のみ）
# ============================
def analyze_character(image_path):
    hair_color_main = predict_hair_color_main(image_path)
    clip_main = predict_hairstyle_main(image_path)
    hairstyle_main = map_clip_hairstyle_to_main(clip_main)

    return {
        "name": "",
        "work": "",
        "hair_length": predict_hair_length(image_path),

        # 髪色（大分類＋中分類）
        "hair_color_main": hair_color_main,
        "hair_color_sub": "",  # 中分類は空欄

        #髪型（大分類のみ推定）
        "hairstyle_main": hairstyle_main,
        "hairstyle_type": "",
        "hairstyle_detail": "",

        "eye_color": predict_eye_color(image_path),
        "eye_shape": predict_eye_shape(image_path),
        "expression": predict_expression(image_path),
        "vibe": predict_vibe(image_path),
        "other": ""
    }

# ============================
# 1. 画像一覧取得
# ============================
files = os.listdir(IMAGE_DIR)
image_files = [f for f in files if f.lower().endswith((".png", ".jpg", ".jpeg"))]
image_files.sort()

# ============================
# 2. JSON読み込み
# ============================
if os.path.exists(FEATURE_FILE):
    try:
        with open(FEATURE_FILE, "r", encoding="utf-8") as f:
            features = json.load(f)
    except json.JSONDecodeError:
        print("⚠ JSONが壊れていたため、新しく作成します")
        features = {}
else:
    features = {}

# ============================
# 3. 画像を 001 から順にリネーム
# ============================
rename_map = {}
for i, old_name in enumerate(image_files, start=1):
    ext = os.path.splitext(old_name)[1]
    new_name = f"{i:03d}{ext}"
    old_path = os.path.join(IMAGE_DIR, old_name)
    new_path = os.path.join(IMAGE_DIR, new_name)

    if old_name != new_name:
        os.rename(old_path, new_path)

    rename_map[old_name] = new_name

# ============================
# 4. 特徴データ更新（髪色新仕様）
# ============================
new_features = {}

for old_name, new_name in rename_map.items():
    img_path = os.path.join(IMAGE_DIR, new_name)

    print(f"特徴推定中: {new_name}")

    ai = analyze_character(img_path)
    old_data = features.get(old_name, {})

    merged = {
        "name": old_data.get("name") or "",
        "work": old_data.get("work") or "",

        "hair_length": old_data.get("hair_length") or ai["hair_length"],

        "hair_color_main": old_data.get("hair_color_main") or ai["hair_color_main"],
        "hair_color_sub": old_data.get("hair_color_sub") or "",

        "hairstyle_main": old_data.get("hairstyle_main") or ai["hairstyle_main"],
        "hairstyle_type": old_data.get("hairstyle_type") or "",
        "hairstyle_detail": old_data.get("hairstyle_detail") or "",

        "eye_color": old_data.get("eye_color") or ai["eye_color"],
        "eye_shape": old_data.get("eye_shape") or ai["eye_shape"],
        "expression": old_data.get("expression") or ai["expression"],
        "vibe": old_data.get("vibe") or ai["vibe"],

        "other": old_data.get("other") or ai["other"]
    }

    new_features[new_name] = merged

# ============================
# 5. JSON保存
# ============================
with open(FEATURE_FILE, "w", encoding="utf-8") as f:
    json.dump(new_features, f, ensure_ascii=False, indent=4)

print("\n=== 完了 ===")
print("・画像を 001 から順にリネーム")
print("・旧データ保持")
print("・空欄だけAI推定で補完")
print("・髪色は大分類のみ自動推定（中分類は空欄）")
print("・髪型は大分類のみ自動推定")
'''
