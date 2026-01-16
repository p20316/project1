import random
import streamlit as st
import matplotlib.pyplot as plt

# =====================
# matplotlib 한글 설정
# =====================
plt.rcParams["font.family"] = "Malgun Gothic"
plt.rcParams["axes.unicode_minus"] = False


# =====================
# 감정 데이터
# =====================
emotion_data = {
    "슬픔": {
        "keywords": ["슬퍼", "우울", "힘들어", "눈물", "외로워", "상처", "아파"],
        "responses": [
            "많이 힘들었겠다. 그 감정을 혼자서 버텨온 것 같아.",
            "지금 마음이 많이 아파 보인다. 그렇게 느껴도 괜찮아."
        ]
    },
    "기쁨": {
        "keywords": ["기뻐", "행복", "좋아", "신나", "즐거워"],
        "responses": [
            "그 말에서 기분 좋은 에너지가 느껴져.",
            "요즘 그런 순간이 있다는 게 참 다행이야."
        ]
    },
    "분노": {
        "keywords": ["화나", "짜증", "열받아", "억울"],
        "responses": [
            "그 상황이면 화날 수밖에 없었을 것 같아.",
            "참고 넘기기엔 마음이 너무 상했을 것 같아."
        ]
    }
}

emotion_colors = {
    "슬픔": "#4A6FA5",
    "기쁨": "#FFD166",
    "분노": "#EF476F"
}


# =====================
# 세션 상태 초기화
# =====================
if "emotion_count" not in st.session_state:
    st.session_state.emotion_count = {e: 0 for e in emotion_data}

if "chat_log" not in st.session_state:
    st.session_state.chat_log = []


# =====================
# 공감 응답 함수 (안전 버전)
# =====================
def empathic_response(text):
    for emotion, data in emotion_data.items():
        for keyword in data["keywords"]:
            if keyword in text:
                # 🔒 KeyError 완전 차단
                if emotion not in st.session_state.emotion_count:
                    st.session_state.emotion_count[emotion] = 0
                st.session_state.emotion_count[emotion] += 1

                return random.choice(data["responses"])

    return "그런 일이 있었구나. 조금 더 이야기해 줄래?"


# =====================
# UI
# =====================
st.title("공감형 감정 AI")
st.write("감정을 자유롭게 적어 주세요. `종료`라고 입력하면 분석 결과를 보여줘요.")

user_input = st.text_input("나:")
send = st.button("전송")


# =====================
# 입력 처리
# =====================
if send and user_input:
    st.session_state.chat_log.append(("나", user_input))

    if user_input.strip() == "종료":
        total = sum(st.session_state.emotion_count.values())

        st.subheader("📊 감정 분석 결과")

        if total == 0:
            st.write("아직 분석할 만큼의 감정 표현이 없었어.")
        else:
            stats = []
            for e, c in st.session_state.emotion_count.items():
                if c > 0:
                    stats.append((e, round((c / total) * 100, 1)))

            stats.sort(key=lambda x: x[1], reverse=True)

            emotions = [e for e, _ in stats]
            percents = [p for _, p in stats]
            colors = [emotion_colors[e] for e in emotions]

            fig, ax = plt.subplots()
            bars = ax.bar(emotions, percents, color=colors)
            ax.set_ylim(0, 100)

            max_idx = percents.index(max(percents))
            ax.text(
                bars[max_idx].get_x() + bars[max_idx].get_width() / 2,
                percents[max_idx] + 2,
                "★",
                ha="center",
                fontsize=16
            )

            st.pyplot(fig)

        st.write("이건 판단이 아니라, 네가 표현해 온 감정의 흐름이야.")
        st.write("이야기해 줘서 고마워.")

        # 상태 초기화
        st.session_state.emotion_count = {e: 0 for e in emotion_data}
        st.session_state.chat_log = []

    else:
        ai = empathic_response(user_input)
        st.session_state.chat_log.append(("AI", ai))


# =====================
# 대화 로그 출력
# =====================
for speaker, msg in st.session_state.chat_log:
    st.write(f"**{speaker}:** {msg}")
