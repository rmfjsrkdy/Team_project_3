import streamlit as st
from openai import OpenAI
# 이미지 클릭 이벤트 활성화
click = st.get_image_click("room_map_click")

if click:
    x, y = click["x"], click["y"]
    st.write(f"클릭됨 (x={x}, y={y})")  # 디버깅용

    # 청소 영역
    if 80 < x < 220 and 250 < y < 380:
        st.switch_page("pages/1_🚮_집안 청소 해결사.py")

    # 유지보수 영역
    elif 220 < x < 350 and 250 < y < 380:
        st.switch_page("pages/2_🔧_유지보수_전문가.py")

    # 고지서 영역
    elif 350 < x < 480 and 150 < y < 280:
        st.switch_page("pages/3._🧾_고지서_관리사.py")

    # 요리 도우미 영역
    elif 350 < x < 520 and 300 < y < 430:
        st.switch_page("pages/4._🍳_요리_도우미.py")
