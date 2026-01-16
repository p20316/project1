import random
import streamlit as st
import matplotlib.pyplot as plt

# =====================
# 감정별 키워드 & 공감 응답
# =====================
emotion_data = {
    "SAD": {
        "keywords": ["슬퍼", "우울", "힘들어", "눈물", "외로워", "상처", "아파", "허무", "공허", "서러워"],
        "responses": [
            "많이 힘들었겠다. 그 감정을 혼자서 버텨온 것 같아.",
            "지금 마음이 많이 아파 보인다. 그렇게 느껴도 괜찮아."
        ]
    },
    "JOY": {
        "keywords": ["기뻐", "행복", "좋아", "신나", "즐거워", "설레", "뿌듯", "재밌어"],
        "responses": [
            "그 말에서 기분 좋은 에너지가 느껴져.",
            "요즘 그런 순간이 있다는 게 참 다행이야."
        ]
    },
    "ANGRY": {
        "keywords": ["화나", "짜증", "열받아", "억울", "분노", "빡쳐"],
        "responses": [
            "그 상황이면 화날 수밖에 없었을 것 같아.",
            "참고 넘기기엔 마음이 너무 상했을 것 같아."
        ]
    },
    "ANXIETY": {
        "keywords": ["불안", "걱정", "초조", "무서워", "긴장", "조마조마"],
        "responses": [
            "불안할 때는 모든 게 확실하지 않게 느껴지지.",
            "지금 많이 긴장하고 있는 것 같아."
        ]
    },
    "LONELY": {
        "keywords": ["외로워", "혼자", "쓸쓸", "고독", "허전"],
        "responses": [
            "혼자라고 느껴질 때 마음이 더 무거워지지.",
            "누군가 곁에 있었으면 좋겠다는 마음이 느껴져."
        ]
    },
    "TIRED": {
        "keywords": ["피곤", "지쳐", "번아웃", "녹초", "탈진"],
        "responses": [
            "정말 오래 버텨온 것 같아.",
            "몸도 마음도 쉬고 싶다고 말하는 것 같아."
        ]
    },
    "REGRETFUL": {
        "keywords": ["후회", "실수", "잘못", "미련", "아쉽다"],
        "responses": [
            "이미 충분히 스스로를 돌아보고 있는 것 같아.",
            "그 일 때문에 아직 마음이 많이 남아 있구나."
        ]
    },
    "FECKLESS": {
        "keywords": ["무기력", "의욕없어", "귀찮아", "하기싫어", "멍해"],
        "responses": [
            "아무것도 하고 싶지 않을 만큼 지친 것 같아.",
            "에너지가 바닥난 느낌이 드는 것 같아."
        ]
    },
    "EXPECTATION": {
        "keywords": ["기대", "설렘", "두근", "희망", "앞으로"],
        "responses": [
            "마음 한편에서 뭔가를 기대하고 있는 것 같아.",
            "그 설렘이 조심스럽게 느껴져."
        ]
    },
    "CONFUSED": {
        "keywords": ["혼란", "헷갈려", "모르겠어", "복잡해", "갈등"],
        "responses": [
            "머릿속이 정리되지 않은 느낌이네.",
            "지금은 방향이 잘 안 보일 수도 있을 것 같아."
        ]
    }
}

# =====================
# 감정별 색상 (10개)
# =====================
emotion_colors = {
    "SAD": "#4A6FA5",
    "JOY": "#FFD166",
    "ANGRY": "#EF476F",
    "ANXIETY": "#8E7DBE",
    "LONELY": "#6C757D",
    "TIRED": "#495057",
    "REGRETFUL": "#A44A3F",
    "FECKLESS": "#ADB5BD",
    "EXPECTATION": "#06D6A0",
    "CONFUSED": "#B565A7"
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
# 공감 응답 함수 (KeyError 방지)
# =====================
def empathic_response(text):
    for emotion, data in emotion_data.items():
        for keyword in data["keywords"]:
            if keyword in text:
                st.session_state.emotion_count[emotion] = (
                    st.session_state.emotion_count.get(emotion, 0) + 1
                )
                return random.choice(data["responses"])
    return "그런 일이 있었구나. 조금 더 이야기해 줄래?"

# =====================
# UI
# =====================
st.title("공감형 감정 AI")
st.write("감정을 적고 **전송 버튼**을 눌러 주세요. `종료`라고 입력하면 분석 결과를 보여줘요.")

st.text_input("나:", key="user_input")
send = st.button("전송")

# =====================
# 입력 처리 (버튼 기반)
# =====================
if send and st.session_state.user_input:
    text = st.session_state.user_input.strip()
    st.session_state.chat_log.append(("나", text))

    # 종료 처리
    if text == "종료":
        total = sum(st.session_state.emotion_count.values())

        st.subheader("📊 감정 분석 결과")

        if total > 0:
            stats = [
                (e, round(c / total * 100, 1))
                for e, c in st.session_state.emotion_count.items()
                if c > 0
            ]
            stats.sort(key=lambda x: x[1], reverse=True)

            emotions = [e for e, _ in stats]
            percentages = [p for _, p in stats]
            colors = [emotion_colors.get(e, "#999999") for e in emotions]

            fig, ax = plt.subplots()
            bars = ax.bar(emotions, percentages, color=colors)
            ax.set_ylim(0, 100)
            ax.set_xlabel("EMOTION")
            ax.set_ylabel("PERCENT (%)")
            ax.set_title("CURRENT EMOTIONAL STATE")

            max_idx = percentages.index(max(percentages))
            ax.text(
                bars[max_idx].get_x() + bars[max_idx].get_width() / 2,
                percentages[max_idx] + 2,
                "★",
                ha="center",
                fontsize=16
            )

            st.pyplot(fig)

        st.write("이건 판단이 아니라, 네가 표현해 온 감정의 흐름이야.")
        st.write("이야기해 줘서 고마워.")

        # 🔄 종료 후 완전 초기화
        st.session_state.emotion_count = {e: 0 for e in emotion_data}
        st.session_state.chat_log = []
        st.session_state.user_input = ""

    else:
        ai_response = empathic_response(text)
        st.session_state.chat_log.append(("AI", ai_response))
        st.session_state.user_input = ""

# =====================
# 대화 로그 출력
# =====================
for speaker, msg in st.session_state.chat_log:
    st.write(f"**{speaker}:** {msg}")
