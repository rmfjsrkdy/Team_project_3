import streamlit as st
from openai import OpenAI

st.set_page_config(page_title="1인 가구 AI 해결사", layout="wide")

# ----------------------------
# 🔐 0) 미리 저장된 KEY 있는지 (선택 사항)
#     - Streamlit Cloud의 Secrets에 OPENAI_API_KEY 넣어두면 여기로 옴
# ----------------------------
pre_saved_key = st.secrets.get("OPENAI_API_KEY", None)

st.sidebar.header("🔐 OpenAI API Key 입력")

# 세션에 클라이언트가 이미 있으면 = 이번 브라우저 세션 동안은 다시 안 물어보기
if "openai_client" not in st.session_state:
    # secrets에 미리 저장해둔 키가 있으면 그걸 기본값으로 사용
    default_value = pre_saved_key if pre_saved_key else ""

    api_key = st.sidebar.text_input(
        "API Key를 입력하세요",
        type="password",
        value=default_value,
        placeholder="ex) sk-xxxx..."
    )

    if api_key:
        st.session_state["openai_client"] = OpenAI(api_key=api_key)
        st.sidebar.success("API Key 설정 완료!")
    else:
        st.sidebar.warning("API Key가 입력될 때까지 기능이 제한됩니다.")
else:
    # 이미 세션에 클라이언트가 있으니 다시 묻지 않음
    st.sidebar.success("API Key 이미 설정됨 ✅")

# 이제부터는 이 플래그로 버튼 활성/비활성 제어
has_key = "openai_client" in st.session_state

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
        disabled=not has_key,
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
    # 혹시 disabled 옵션이 안 먹는 버전 대비
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
