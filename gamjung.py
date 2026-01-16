import random
import streamlit as st
import matplotlib.pyplot as plt

# 1. 데이터 정의 (오타 방지를 위해 대문자 유지)
emotion_data = {
    "SAD": {"keywords": ["슬퍼", "우울", "힘들어"], "responses": ["마음이 많이 힘들었구나."]},
    "JOY": {"keywords": ["기뻐", "행복", "좋아"], "responses": ["나도 같이 기분이 좋아져!"]},
    "ANGRY": {"keywords": ["화나", "짜증", "열받아"], "responses": ["정말 화날만한 상황이네."]},
    "ANXIETY": {"keywords": ["불안", "걱정", "초조"], "responses": ["불안해하지 않아도 괜찮아."]},
    "LONELY": {"keywords": ["외로워", "혼자", "쓸쓸"], "responses": ["내가 네 옆에 있어줄게."]},
    "TIRED": {"keywords": ["피곤", "지쳐", "번아웃"], "responses": ["오늘은 푹 쉬는 게 어때?"]},
    "REGRETFUL": {"keywords": ["후회", "실수", "잘못"], "responses": ["누구나 실수할 수 있어."]},
    "FECKLESS": {"keywords": ["무기력", "의욕없어"], "responses": ["잠시 멈춰가도 괜찮아."]},
    "EXPECTATION": {"keywords": ["기대", "설렘", "두근"], "responses": ["좋은 일이 생길 것 같아!"]},
    "CONFUSED": {"keywords": ["혼란", "복잡해"], "responses": ["천천히 정리해보자."]}
}

# 2. 세션 초기화 (최상단 위치)
if "emotion_count" not in st.session_state:
    st.session_state.emotion_count = {e: 0 for e in emotion_data}
if "chat_log" not in st.session_state:
    st.session_state.chat_log = []

def empathic_response(text):
    # KeyError 방지를 위한 안전한 접근
    for emotion, data in emotion_data.items():
        for keyword in data["keywords"]:
            if keyword in text:
                # 안전하게 값을 가져오고 업데이트
                st.session_state.emotion_count[emotion] = st.session_state.emotion_count.get(emotion, 0) + 1
                return random.choice(data["responses"])
    return "그랬구나. 조금 더 자세히 말해줄 수 있니?"

st.title("🍀 감정 상담소")

# 입력 폼
with st.form(key="my_form", clear_on_submit=True):
    user_input = st.text_input("지금 기분이 어때?")
    submitted = st.form_submit_button("전송")

if submitted and user_input:
    if user_input == "종료":
        st.write("분석 결과를 확인하세요!")
        # (여기에 그래프 코드 추가)
    else:
        res = empathic_response(user_input)
        st.session_state.chat_log.append(("나", user_input))
        st.session_state.chat_log.append(("AI", res))

# 대화 출력
for name, msg in reversed(st.session_state.chat_log):
    st.write(f"**{name}**: {msg}")
