import streamlit as st
from openai import OpenAI

# 페이지 제목과 설명
st.title("🍽️ 오늘은 뭘 먹을지 물어보세요")
st.write(
    "이 챗봇은 GPT-3.5 모델을 활용해, 오늘 점심이나 저녁 메뉴가 고민되는 분들을 위해 맞춤 추천을 도와드립니다. 🍱🍝🍜\n\n"
    "앱을 사용하려면 OpenAI API 키가 필요하며, [여기에서](https://platform.openai.com/account/api-keys) 발급받을 수 있어요."
)

# API 키 입력 받기
openai_api_key = st.text_input("OpenAI API Key", type="password")
if not openai_api_key:
    st.info("계속하려면 OpenAI API 키를 입력해 주세요.", icon="🗝️")
else:
    # OpenAI 클라이언트 생성
    client = OpenAI(api_key=openai_api_key)

    # 시스템 역할 메시지 추가
    SYSTEM_PROMPT = {
        "role": "system",
        "content": (
            "당신은 사용자의 상황과 기호를 고려해 점심 또는 저녁 메뉴를 추천해주는 챗봇입니다. "
            "메뉴는 한식, 중식, 양식, 일식 등 다양하게 포함하며, 추천 시 이유도 함께 설명해 주세요. "
            "필요 시 식사 장소나 배달 여부도 함께 제안해 주세요."
        )
    }

    # 세션 상태에 메시지 저장
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # 이전 대화 메시지 출력
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # 사용자 입력 받기
    if prompt := st.chat_input("점심이나 저녁 메뉴를 물어보세요!"):
        # 사용자 메시지 저장 및 출력
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # GPT 응답 생성
        stream = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[SYSTEM_PROMPT] + [
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ],
            stream=True,
        )

        # GPT 응답 출력 및 저장
        with st.chat_message("assistant"):
            response = st.write_stream(stream)
        st.session_state.messages.append({"role": "assistant", "content": response})
