import streamlit as st
import requests
import base64

st.title("AI画像生成（Stable Diffusion Forge ローカルAPI）")

prompt = st.session_state.get("prompt", "")

if not prompt:
    st.write("まだプロンプトが生成されていません。")
    st.stop()

st.subheader("生成プロンプト")
st.code(prompt)

API_URL = "http://127.0.0.1:7860/sdapi/v1/txt2img"

if st.button("画像生成する"):
    with st.spinner("生成中..."):
        payload = {
            "prompt": prompt,
            "steps": 20,
            "width": 512,
            "height": 512
        }

        response = requests.post(API_URL, json=payload)

        if response.status_code != 200:
            st.error(f"エラー: {response.text}")
            st.stop()

        # Base64 画像を取得
        r = response.json()
        image_base64 = r["images"][0]

        # Base64 → バイナリ変換
        image_bytes = base64.b64decode(image_base64)

        st.image(image_bytes, caption="生成画像", use_column_width=True)