import streamlit as st
import os

st.title("메인 페이지")

st.write("청소 기능을 쓰려면 아래 링크를 눌러줘!")

# ✅ 청소 페이지로 이동하는 링크(사이드바 메뉴 클릭과 동일한 효과)
st.page_link("pages/1_cleaning_helper.py", label="🧹 청소 페이지로 이동")

st.write("---")
st.write("디버깅용 정보 (필요 없으면 지워도 됨)")
st.code(os.getcwd())
st.write(os.listdir())
st.write(os.listdir("pages"))
