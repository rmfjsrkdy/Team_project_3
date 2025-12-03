import streamlit as st
from openai import OpenAI

# OpenAI 클라이언트 초기화 함수
@st.cache_resource
def get_openai_client():
    """
    st.secrets에서 API 키를 읽어 OpenAI 클라이언트를 반환합니다.
    Streamlit의 @st.cache_resource를 사용하여 앱이 실행되는 동안 클라이언트 객체를 재사용합니다.
    """
    
    # st.secrets에 키가 정의되어 있지 않다면 경고 메시지를 출력하고 None을 반환합니다.
    if "OPENAI_API_KEY" not in st.secrets:
        st.error("⚠️ .streamlit/secrets.toml 파일에 'OPENAI_API_KEY'가 설정되지 않았습니다.")
        return None

    try:
        # st.secrets에서 키를 가져와 클라이언트 객체 생성
        client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
        return client
    except Exception as e:
        st.error(f"OpenAI 클라이언트 초기화 중 오류 발생: {e}")
        return None
    

# 각 페이지에서 클라이언트를 사용할 때는 이렇게 호출합니다:
# client = get_openai_client()