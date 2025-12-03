import streamlit as st
from openai import OpenAI

# OpenAI API 키 입력 함수.
@st.cache_resource
def get_openai_client():
    API_KEY="sk-"
    client = OpenAI(api_key=API_KEY)
    return client
    

# 각 페이지에서 클라이언트를 사용할 때는 이렇게 호출합니다:
# from utils import get_openai_client
# client = get_openai_client()