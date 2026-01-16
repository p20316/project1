import random
import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm

# =====================
# matplotlib 한글 폰트 설정 (환경 안전)
# =====================
plt.rcParams["font.family"] = "Malgun Gothic"
plt.rcParams["axes.unicode_minus"] = False


# =====================
# 감정 데이터
# =====================
emotion_data = {
    "SAD": {
        "keywords": ["슬퍼", "우울", "힘들어", "눈물", "외로워", "상처", "아파", "허무", "공허", "서러워", "눈물나"],
        "responses": [
            "많이 힘들었겠다. 그 감정을 혼자서 버텨온 것 같아.",
            "지금 마음이 많이 아파 보인다. 그렇게 느껴도 괜찮아."
        ]
    },
    "JOY": {
        "keywords": ["기뻐", "행복", "좋아", "신나", "즐거워", "만족", "웃겨", "뿌듯", "기분좋아", "설레", "재밌어"],
        "responses": [
            "그 말에서 기분 좋은 에너지가 느껴져.",
            "요즘 그런 순간이 있다는 게 참 다행이야."
        ]
    },
    "ANGRY": {
        "keywords": ["화나", "짜증", "열받아", "분해", "빡쳐", "억울", "분노"],
        "responses": [
            "그 상황이면 화날 수밖에 없었을 것 같아.",
            "참고 넘기기엔 마음이 너무 상했을 것 같아."
        ]
    }
}

emotion_colors = {
    "SAD": "#4A6FA5",
    "JOY": "#FFD166",
    "ANGRY": "#EF476F"
}


# =====================
# 세션 상태 초기화
# =====================
if "emotion_count" not in st.session_state:
    st.session_state.emotion_count = {e: 0 for e in emotion_data}

if "chat_log" not in st.session_state:
    st.session_state.chat_log = []

if "user_input" not in st.session_state:
    st.session_state.user_input = ""


# =====================
# 공감 응답 함수
# =====================
def empathic_response(text):
    for emotion, data in emotion_data.items():
        for keyword in data["keywords"]:
            if keyword in text:
                st.session_state.emotion_count[emotion] += 1
                return random.choice(data["responses"])

    return "그런 일이 있었구나. 조금 더 이야기해 줄래?"


# =====================
# UI
# =====================
st.title("공감형 감정 AI")

user_input = st.text_input("나:", key="user_input")
send = st.button("전송")


# =====================
# 입력 처리
# =====================
if send and user_input:
    st.session_state.chat_log.append(("나", user_input))

    if "종료" in user_input:
        total = sum(st.session_state.emotion_count.values())

        st.subheader("📊 감정 분석 결과")

        if total == 0:
            st.write("분석할 만큼의 감정 표현이 없었어.")
        else:
            stats = [
                (e, round((c / total) * 100, 1))
                for e, c in st.session_state.emotion_count.items()
                if c > 0
            ]
            stats.sort(key=lambda x: x[1], reverse=True)

            emotions = [e for e, _ in stats]
            percents = [p for _, p in stats]
            colors = [emotion_colors[e] for e in emotions]

            fig, ax = plt.subplots()
            bars = ax.bar(emotions, percents, color=colors)
            ax.set_ylim(0, 100)
            ax.set_ylabel("퍼센트 (%)")
            ax.set_title("현재 감정 상태")

            max_idx = percents.index(max(percents))
            ax.text(
                bars[max_idx].get_x() + 0.4,
                percents[max_idx] + 2,
                "★",
                ha="center",
                fontsize=16
            )

            st.pyplot(fig)

        # === 종료 후 초기화 ===
        st.session_state.emotion_count = {e: 0 for e in emotion_data}
        st.session_state.chat_log = []
        st.session_state.user_input = ""

    else:
        ai = empathic_response(user_input)
        st.session_state.chat_log.append(("AI", ai))
        st.session_state.user_input = ""


# =====================
# 대화 로그 출력
# =====================
for speaker, msg in st.session_state.chat_log:
    st.write(f"**{speaker}:** {msg}")
