import streamlit as st
from openai import OpenAI
import base64

if "openai_client" not in st.session_state:
    st.error("⚠️ OpenAI API Key가 설정되지 않았습니다. 메인 페이지로 돌아가서 Key를 입력해 주세요.")
    st.stop()

client = st.session_state.get('openai_client', None)

if client is None:
    st.error("API 키가 설정되지 않았습니다. 먼저 API 키를 입력하세요.")
    st.stop()

st.title("🧾 고지서 관리 챗봇")
st.write("고지서를 촬영하거나 업로드하거나, 질문을 입력해 보세요!")


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
# 이미지 입력: 촬영 + 업로드 둘 다 가능
# -------------------------------
use_image = st.checkbox("📷 카메라 또는 파일로 고지서 보내기")

image = None
if use_image:
    option = st.radio(
        "입력 방식을 선택하세요:",
        ("카메라 촬영", "파일 업로드"),
        horizontal=True
    )

    if option == "카메라 촬영":
        image = st.camera_input("고지서를 촬영해 주세요")

    elif option == "파일 업로드":
        image = st.file_uploader(
            "고지서를 업로드하세요",
            type=["jpg", "jpeg", "png"]
        )


# -------------------------------
# 채팅 기록 렌더링
# -------------------------------
for msg in st.session_state.bill_messages:
    if msg["role"] != "system":
        show_message(msg)


# -------------------------------
# 텍스트 입력
# -------------------------------
if prompt := st.chat_input("여기에 메시지를 입력하세요..."):

    # 사용자 메시지 추가 및 출력
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
    with st.chat_message("assistant"):
        with st.spinner("고지서 관리사 생각중..."):
            response = client.responses.create(
                model="gpt-4.1",
                input=[
                    *[
                        {"role": msg["role"], "content": msg["content"]}
                        for msg in st.session_state.bill_messages
                        if msg["role"] != "assistant"
                    ],
                    {"role": "user", "content": content_list},
                ]
            )

    assistant_reply = response.output_text

    # assistant 메시지 저장 및 출력
    assistant_msg = {"role": "assistant", "content": assistant_reply}
    show_message(assistant_msg)
    st.session_state.bill_messages.append(assistant_msg)
