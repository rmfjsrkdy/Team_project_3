import streamlit as st
from openai import OpenAI

st.set_page_config(page_title="1인 가구 AI 해결사", layout="wide")

# ----------------------------
# 🔐 API Key 입력
# ----------------------------
st.sidebar.header("🔐 OpenAI API Key 입력")

api_key = st.sidebar.text_input(
    "API Key를 입력하세요",
    type="password",
    placeholder="ex) sk-xxxx..."
)

if api_key:
    st.session_state["openai_client"] = OpenAI(api_key=api_key)
    st.sidebar.success("API Key 설정 완료!")
else:
    st.sidebar.warning("API Key가 입력될 때까지 기능이 비활성화됩니다.")
    st.stop()

# ----------------------------
# 메인 화면
# ----------------------------
st.title("🏠 1인 가구 AI 해결사")
st.write("원하는 AI 도우미를 선택하세요!")

col1, col2 = st.columns(2)

with col1:
    if st.button("🧹 집안 청소 해결사", use_container_width=True):
        st.switch_page("pages/1_🚮_집안 청소 해결사.py")

    if st.button("🧾 고지서 관리사", use_container_width=True):
        st.switch_page("pages/3._🧾_고지서_관리사.py")

with col2:
    if st.button("🔧 유지보수 전문가", use_container_width=True):
        st.switch_page("pages/2_🔧_유지보수_전문가.py")

    if st.button("🍳 요리 도우미", use_container_width=True):
        st.switch_page("pages/4._🍳_요리_도우미.py")
