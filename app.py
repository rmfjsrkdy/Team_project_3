# app.py (임시 디버깅 버전)

import streamlit as st
import os

st.title("디버깅 모드")

st.write("### 현재 작업 디렉토리 (cwd)")
st.code(os.getcwd())

st.write("### 현재 디렉토리 안의 파일/폴더 목록")
st.write(os.listdir())

# pages 폴더 내용 확인
if "pages" in os.listdir():
    st.write("### pages 폴더 안의 파일 목록")
    st.write(os.listdir("pages"))
else:
    st.error("'pages' 폴더를 현재 디렉토리에서 찾을 수 없습니다.")

st.write("---")

go = st.button("청소 페이지로 이동 시도")

if go:
    st.switch_page("pages/1_cleaning_helper.py")
