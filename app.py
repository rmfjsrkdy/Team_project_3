import streamlit as st
from openai import OpenAI

#API키 설정
api_key=""
st.session_state["API_KEY"] = api_key
client = OpenAI(api_key=api_key) 
st.session_state["openai_client"]=client