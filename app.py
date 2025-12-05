import streamlit as st
from openai import OpenAI
from PIL import Image

st.set_page_config(page_title="1인 가구 AI 해결사", layout="wide")

# ----------------------------
# 🔐 사이드바에서 API KEY 입력
# ----------------------------
st.sidebar.header("🔐 OpenAI API Key 입력")

api_key = st.sidebar.text_input(
    "API Key를 입력하세요",
    type="password",
    placeholder="ex) sk-xxxx..."
)

# API KEY 저장
if api_key:
    st.session_state["openai_client"] = OpenAI(api_key=api_key)
    st.sidebar.success("API Key 설정 완료!")
else:
    st.sidebar.warning("아직 API Key가 입력되지 않았어요.")

# ----------------------------
# API Key 없으면 메인 기능 잠금
# ----------------------------
if "openai_client" not in st.session_state:
    st.title("🏠 1인 가구 AI 해결사")
    st.write("좌측 사이드바에 **OpenAI API Key**를 입력하면 기능이 활성화됩니다.")
    st.stop()

# ----------------------------
# 메인 UI - 원룸 설계도 클릭 이동
# ----------------------------
st.title("🏠 1인 가구 AI 해결사")
st.write("원룸 설계도를 클릭하면 해당 기능의 챗봇으로 이동합니다!")

# 이미지 로드
img = Image.open("assets/oneroom.png")
st.image(img, caption="클릭해서 이동하세요!", use_container_width=True)

# 이미지 클릭 이벤트
click = st.get_image_click("room_map_click")

if click:
    x, y = click["x"], click["y"]
    st.write(f"클릭됨 (x={x}, y={y})")  # 디버깅용

    # ----------------------------
    # 좌표 조건에 따라 페이지 이동
    # ----------------------------

    # 집안 청소
    if 80 < x < 220 and 250 < y < 380:
        st.switch_page("pages/1_🚮_집안 청소 해결사.py")

    # 유지보수 전문가
    elif 220 < x < 350 and 250 < y < 380:
        st.switch_page("pages/2_🔧_유지보수_전문가.py")

    # 고지서 관리사
    elif 350 < x < 480 and 150 < y < 280:
        st.switch_page("pages/3._🧾_고지서_관리사.py")

    # 요리 도우미
    elif 350 < x < 520 and 300 < y < 430:
        st.switch_page("pages/4._🍳_요리_도우미.py")

