import streamlit as st
from openai import OpenAI

client = OpenAI(api_key="sk_xxxx")

st.set_page_config(page_title="주방 문제 해결 챗봇", page_icon="🍳")

st.title("🍳 주방 문제 해결 챗봇")
st.write("요리 • 음식 보관 • 음식물쓰레기 처리 등 어떤 고민이든 말해보세요!")

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": 
         "너는 요리, 주방 청결, 식재료 보관, 음식물쓰레기 관리 전문가야. "
         "사용자가 주방 관련 문제를 말하면 간단하고 실용적인 해결책을 알려줘."}
    ]

for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.chat_message("user").write(msg["content"])
    elif msg["role"] == "assistant" and msg["content"]:
        st.chat_message("assistant").write(msg["content"])

user_input = st.chat_input("주방 관련 고민을 말해보세요!")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    st.chat_message("user").write(user_input)

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=st.session_state.messages
    )
    bot_reply = response.choices[0].message.content

    st.session_state.messages.append({"role": "assistant", "content": bot_reply})

    st.chat_message("assistant").write(bot_reply)