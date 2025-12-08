import streamlit as st
from openai import OpenAI
import base64

# -------------------------------
# OpenAI 클라이언트 체크
# -------------------------------
if "openai_client" not in st.session_state:
    st.error("⚠️ OpenAI API Key가 설정되지 않았습니다. 메인 페이지로 돌아가서 Key를 입력해 주세요.")
    st.stop()

client = st.session_state.get("openai_client", None)

if client is None:
    st.error("API 키가 설정되지 않았습니다. 먼저 API 키를 입력하세요.")
    st.stop()

# -------------------------------
# 화면 제목
# -------------------------------
st.title("🧹 집안 청소 해결사")
st.write("집안 청소가 고민되면 사진을 촬영하거나 파일을 첨부하거나, 질문을 입력해 보세요!")


# -------------------------------
# 메시지 렌더링 함수
# -------------------------------
def show_message(msg):
    st.chat_message(msg["role"]).write(msg["content"])


# -------------------------------
# 세션 초기화
# -------------------------------
if "clean_messages" not in st.session_state:
    st.session_state.clean_messages = [
        {
            "role": "system",
            "content": (
                "너는 1인 가구 청소 전문가 AI야. "
                "사용자가 보내는 사진(에어컨 필터, 화장실, 보일러, 곰팡이, 싱크대, 창틀, 베란다, 세탁기, 가스레인지 등)을 기반으로 "
                "현재 상태를 분석하고, 청소 난이도와 위험 요소(곰팡이, 세제 혼합 금지, 환기 필요 등)를 설명한 뒤, "
                "1) 지금 해야 할 우선 조치 "
                "2) 필요한 준비물(최대한 집에 있을 만한 것 위주, 예: 베이킹소다, 식초, 락스, 행주, 칫솔, 고무장갑 등) "
                "3) 단계별 청소 방법 "
                "4) 주의사항 "
                "5) 전문가나 관리실, AS센터를 불러야 하는 상황인지 여부 "
                "를 간단하고 차분하게 설명해. "
                "사진이 없으면 텍스트만으로도 최대한 구체적으로 도와줘."
            ),
        }
    ]


# -------------------------------
# 이미지 / 파일 입력 (촬영 + 업로드)
# -------------------------------
use_media = st.checkbox("📷 카메라 또는 파일로 청소가 필요한 곳 보내기")

uploaded_doc = None  # 카메라/이미지/PDF 모두 이 변수로 처리

if use_media:
    option = st.radio(
        "입력 방식을 선택하세요:",
        ("카메라 촬영", "파일 업로드"),
        horizontal=True,
    )

    if option == "카메라 촬영":
        uploaded_doc = st.camera_input("청소가 필요한 부분을 촬영해 주세요")

    elif option == "파일 업로드":
        uploaded_doc = st.file_uploader(
            "청소가 필요한 부분의 사진 또는 관련 PDF를 업로드하세요",
            type=["jpg", "jpeg", "png", "pdf"],
        )

# -------------------------------
# 기존 채팅 기록 렌더링
# -------------------------------
for msg in st.session_state.clean_messages:
    if msg["role"] != "system":
        show_message(msg)


# -------------------------------
# 텍스트 입력
# -------------------------------
prompt = st.chat_input("어떤 청소가 고민이신가요? (예: 화장실 곰팡이, 에어컨 필터, 가스레인지 기름때 등)")

if prompt:
    # 사용자 메시지 추가 및 출력
    user_msg = {"role": "user", "content": prompt}
    st.session_state.clean_messages.append(user_msg)
    show_message(user_msg)

    # 기본 텍스트 블록
    content_list = [{"type": "input_text", "text": prompt}]

    # ---------------------------
    # 첨부된 이미지/PDF 처리
    # ---------------------------
    if uploaded_doc is not None:
        # Streamlit의 UploadedFile/camera_input 둘 다 getvalue() 지원
        file_bytes = uploaded_doc.getvalue()
        mime_type = getattr(uploaded_doc, "type", None)  # ex) image/jpeg, application/pdf

        # 1) PDF 고지서/메뉴얼/점검표 → input_file 로 첨부
        if mime_type == "application/pdf":
            file_b64 = base64.b64encode(file_bytes).decode()
            content_list.append(
                {
                    "type": "input_file",
                    "filename": getattr(uploaded_doc, "name", "document.pdf"),
                    "file_data": f"data:application/pdf;base64,{file_b64}",
                }
            )

        # 2) 그 외(카메라, jpg, png 등) → input_image
        else:
            img_b64 = base64.b64encode(file_bytes).decode()
            content_list.append(
                {
                    "type": "input_image",
                    "image_url": f"data:{mime_type or 'image/jpeg'};base64,{img_b64}",
                }
            )

    # -------------------------------
    # Responses API 호출
    # -------------------------------
    with st.chat_message("assistant"):
        placeholder = st.empty()

        with placeholder.container():
            with st.spinner("청소 방법을 고민 중이에요..."):
                # 이전 system + user 메시지들을 그대로 넣고,
                # 이번 턴에는 content_list(텍스트 + 파일)를 함께 보냄
                response = client.responses.create(
                    model="gpt-4.1-mini",  # 필요하면 gpt-4.1 으로 변경 가능
                    input=[
                        *[
                            {"role": msg["role"], "content": msg["content"]}
                            for msg in st.session_state.clean_messages
                            if msg["role"] != "assistant"
                        ],
                        {"role": "user", "content": content_list},
                    ],
                )

        placeholder.empty()

        assistant_reply = response.output_text

        # assistant 메시지 저장 및 출력
        st.write(assistant_reply)
        assistant_msg = {"role": "assistant", "content": assistant_reply}
        st.session_state.clean_messages.append(assistant_msg)
