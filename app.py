import streamlit as st
from openai import OpenAI
import os
import toml

st.set_page_config(page_title="1인 가구 AI 해결사", layout="wide")


# ----------------------------
# 🔐 1) 기존에 저장된 API Key 자동 로딩
# ----------------------------
saved_key = None

# Streamlit Cloud / 로컬 모두 지원됨
if "OPENAI_API_KEY" in st.secrets:
    saved_key = st.secrets["OPENAI_API_KEY"]


# ----------------------------
# 🔐 2) 사이드바에 입력창
# ----------------------------
st.sidebar.header("🔐 OpenAI API Key 입력")

api_key = st.sidebar.text_input(
    "API Key를 입력하세요",
    type="password",
    value=saved_key if saved_key else "",
    placeholder="ex) sk-xxxx...",
)


# ----------------------------
# 🔐 3) API Key 저장하기 (최초 1회)
# ----------------------------
def save_key_to_secrets(key):
    """로컬 + Streamlit Cloud 모두 지원되는 방식"""

    secrets_path = ".streamlit/secrets.toml"
    os.makedirs(".streamlit", exist_ok=True)

    data = {"OPENAI_API_KEY": key}

    with open(secrets_path, "w") as f:
        toml.dump(data, f)

    st.success("API Key가 저장되었습니다! 앱을 다시 실행하면 자동으로 적용돼요 ✨")


# 저장 버튼
if api_key and api_key != saved_key:
    if st.sidebar.button("🔒 API Key 저장하기"):
        save_key_to_secrets(api_key)


# ----------------------------
# 4) 실제로 사용할 키 결정
# ----------------------------
final_key = api_key or saved_key or None

if final_key:
    st.session_state["openai_client"] = OpenAI(api_key=final_key)
    st.sidebar.success("API Key 설정 완료!")
else:
    st.sidebar.warning("API Key가 입력될 때까지 기능이 일부 제한됩니다.")


# ----------------------------
# 메인 화면
# ----------------------------
st.title("🏠 1인 가구 AI 해결사")
st.write("원하는 AI 도우미를 선택하세요!")

col1, col2 = st.columns(2)
has_key = bool(final_key)

with col1:
    btn_clean = st.button("🧹 집안 청소 해결사", use_container_width=True, disabled=not has_key)
    btn_bill = st.button("🧾 고지서 관리사", use_container_width=True, disabled=not has_key)

with col2:
    btn_maint = st.button("🔧 유지보수 전문가", use_container_width=True, disabled=not has_key)
    btn_cook = st.button("🍳 요리 도우미", use_container_width=True, disabled=not has_key)


# ----------------------------
# 버튼 처리
# ----------------------------
if not has_key:
    if btn_clean or btn_bill or btn_maint or btn_cook:
        st.warning("먼저 OpenAI API Key를 입력해 주세요!")
else:
    if btn_clean:
        st.switch_page("pages/1_집안 청소_해결사.py")
    if btn_bill:
        st.switch_page("pages/3_🧾_고지서_관리사.py")
    if btn_maint:
        st.switch_page("pages/2_🔧_유지 보수_전문가.py")
    if btn_cook:
        st.switch_page("pages/4_🍳_요리_도우미.py")
