import os
import random
import json
import pandas as pd
from mlxtend.frequent_patterns import apriori, association_rules
from PIL import Image

# ============================
# 1. 画像フォルダと特徴データ
# ============================
IMAGE_DIR = "sentei/characters/"
FEATURE_FILE = "sentei/character_features.json"

with open(FEATURE_FILE, "r", encoding="utf-8") as f:
    features = json.load(f)

images = list(features.keys())  # 特徴がある画像のみ対象


# ============================
# 2. ランダムに2枚提示して選択
# ============================
def show_image(path):
    img = Image.open(path)
    img.show()  # OS標準ビューアで開く


def pick_two_images():
    return random.sample(images, 2)


selected = []

print("=== キャラ選択を10回行います ===")

for i in range(10):
    img1, img2 = pick_two_images()

    print(f"\n【第 {i+1} 回】")
    print(f"1: {img1}")
    print(f"2: {img2}")

    # 画像表示
    show_image(os.path.join(IMAGE_DIR, img1))
    show_image(os.path.join(IMAGE_DIR, img2))

    choice = input("どちらを選ぶ？ (1/2): ")

    if choice == "1":
        selected.append(img1)
    else:
        selected.append(img2)


# ============================
# 3. 選ばれた特徴を集計
# ============================
selected_features = [features[img] for img in selected]
df = pd.DataFrame(selected_features)

print("\n=== 選ばれた特徴一覧 ===")
print(df)


# ============================
# 4. 連関分析（アソシエーション分析）
# ============================
df_hot = pd.get_dummies(df)

frequent = apriori(df_hot, min_support=0.2, use_colnames=True)
rules = association_rules(frequent, metric="confidence", min_threshold=0.5)

rules = rules.sort_values("confidence", ascending=False)

print("\n=== 連関分析の結果（confidence順） ===")
print(rules)


# ============================
# 5. 好みの特徴を抽出
# ============================
# confidence が高い特徴を抽出
top_features = []

for _, row in rules.iterrows():
    for item in row["antecedents"]:
        top_features.append(item)
    for item in row["consequents"]:
        top_features.append(item)

top_features = list(set(top_features))  # 重複削除

print("\n=== 好みの特徴（抽出） ===")
print(top_features)


# ============================
# 6. AI画像生成用プロンプトを作成
# ============================
prompt = ", ".join(top_features) + ", anime style, high quality"

print("\n=== AI画像生成プロンプト ===")
print(prompt)