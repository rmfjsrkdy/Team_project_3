import streamlit as st
from openai import OpenAI
import base64

st.title("🧾 고지서 관리 챗봇")
st.write("고지서를 촬영하거나 질문을 입력해 보세요!")

client = st.session_state.get('openai_client', None)


# -------------------------------
# 메시지 렌더링 함수
# -------------------------------
def show_message(msg):
    st.chat_message(msg["role"]).write(msg["content"])


# -------------------------------
# 세션 초기화
# -------------------------------
if "bill_messages" not in st.session_state:
    st.session_state.bill_messages = [
        {
            "role": "system",
            "content": (
                "너는 1인 가구 고지서 분석 전문가야. "
                "사진 속 고지서를 읽고 OCR을 수행한 뒤, "
                "항목별 요금표를 요약하고, 증가/감소 원인을 분석하고, "
                "1인 가구에게 맞는 절약 팁을 제공해."
                "또는 사용자의 질문에 맞는 팁을 제공해."
            )
        }
    ]


# -------------------------------
# 고지서 이미지 입력
# -------------------------------
image = st.camera_input("📸 고지서를 업로드하거나 촬영하세요")


# -------------------------------
# 채팅 기록 렌더링
# -------------------------------
for msg in st.session_state.bill_messages:
    # system 메시지는 출력하지 않음
    if msg["role"] != "system":
        show_message(msg)


# -------------------------------
# 사용자의 텍스트 입력
# -------------------------------
if prompt := st.chat_input("여기에 메시지를 입력하세요..."):
    # 사용자 메시지 추가
    user_msg = {"role": "user", "content": prompt}
    show_message(user_msg)
    st.session_state.bill_messages.append(user_msg)

    # 이미지가 있으면 base64 변환 후 input에 포함
    content_list = [{"type": "input_text", "text": prompt}]

    if image:
        img_b64 = base64.b64encode(image.getvalue()).decode()
        content_list.append({
            "type": "input_image",
            "image_url": f"data:image/jpeg;base64,{img_b64}"
        })

    # -------------------------------
    # Responses API 호출
    # -------------------------------
    response = client.responses.create(
        model="gpt-4.1",
        input=[
            *[
                # 기존 메시지 반영
                {"role": msg["role"], "content": msg["content"]}
                for msg in st.session_state.bill_messages
                if msg["role"] != "assistant"  # assistant 중복 프롬프트 방지
            ],
            {"role": "user", "content": content_list},
        ]
    )

    assistant_reply = response.output_text

    # assistant 메시지 표시 및 저장
    assistant_msg = {"role": "assistant", "content": assistant_reply}
    show_message(assistant_msg)
    st.session_state.bill_messages.append(assistant_msg)