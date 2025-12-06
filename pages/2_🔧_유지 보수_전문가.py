import streamlit as st
from openai import OpenAI

st.title("🔧 집수리 해결사 챗봇")
st.text("수리 및 유지보수가 필요하다면 언제든지 물어보세요!")

if "openai_client" not in st.session_state:
    st.error("⚠️ OpenAI API Key가 설정되지 않았습니다. 메인 페이지로 돌아가서 Key를 입력해 주세요.")
    st.stop()

client = st.session_state.get('openai_client', None)

if "chatbot_messages" not in st.session_state:
    st.session_state.chatbot_messages = [
        {"role":"system","content":f"""당신은 생활 고장 수리 및 유지보수를 잘하는 AI 해결사 입니다. 사용자의 문제를 응답받으면 해결방안을 간단하게 답변 하시오.
"""}
    ]

def show_message(msg):
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if st.button("Clear"):
    del st.session_state["messages"]

for msg in st.session_state.chatbot_messages[1:]:
    show_message(msg)

if prompt := st.chat_input("수리가 필요한 상황 입력하기"):
    msg = {"role":"user", "content":prompt}
    show_message(msg)
    st.session_state.chatbot_messages.append(msg)

    response = client.chat.completions.create(
        model="gpt-4o-mini", 
        messages=st.session_state.chatbot_messages
    )
    assistant_msg = {"role":"assistant", "content":response.choices[0].message.content}
    show_message(assistant_msg)
    st.session_state.chatbot_messages.append(assistant_msg)
