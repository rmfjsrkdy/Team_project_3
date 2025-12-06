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

has_key = bool(api_key)

if has_key:
    # 키가 바뀌었을 수도 있으니 필요하면 새로 생성
    if (
        "openai_client" not in st.session_state
        or st.session_state.get("api_key") != api_key
    ):
        st.session_state["openai_client"] = OpenAI(api_key=api_key)
        st.session_state["api_key"] = api_key

    st.sidebar.success("API Key 설정 완료!")
else:
    st.sidebar.info("기능을 사용하려면 API Key를 입력해 주세요.")

# ----------------------------
# 메인 화면
# ----------------------------
st.title("🏠 1인 가구 AI 해결사")
st.write("원하는 AI 도우미를 선택하세요!")

col1, col2 = st.columns(2)

with col1:
    btn_clean = st.button(
        "🧹 집안 청소 해결사",
        use_container_width=True,
        disabled=not has_key,  # 키 없으면 버튼 비활성화
    )

    btn_bill = st.button(
        "🧾 고지서 관리사",
        use_container_width=True,
        disabled=not has_key,
    )

with col2:
    btn_maint = st.button(
        "🔧 유지보수 전문가",
        use_container_width=True,
        disabled=not has_key,
    )

    btn_cook = st.button(
        "🍳 요리 도우미",
        use_container_width=True,
        disabled=not has_key,
    )

# ----------------------------
# 버튼 클릭 처리
# ----------------------------
if not has_key:
    # 혹시 disabled 옵션 없는 버전 대비, 클릭 시 경고만 보여주기
    if btn_clean or btn_bill or btn_maint or btn_cook:
        st.warning("먼저 왼쪽에서 OpenAI API Key를 입력해 주세요.")
else:
    if btn_clean:
        st.switch_page("pages/1_집안 청소_해결사.py")

    if btn_bill:
        st.switch_page("pages/3_🧾_고지서_관리사.py")

    if btn_maint:
        st.switch_page("pages/2_🔧_유지 보수_전문가.py")

    if btn_cook:
        st.switch_page("pages/4_🍳_요리_도우미.py")
