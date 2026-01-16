import random
import streamlit as st
import matplotlib.pyplot as plt

# =====================
# matplotlib 한글 설정
# =====================
plt.rcParams["font.family"] = "Malgun Gothic"
plt.rcParams["axes.unicode_minus"] = False


# =====================
# 감정 데이터 (10개)
# =====================
emotion_data = {
    "슬픔": {
        "keywords": ["슬퍼", "우울", "힘들어", "눈물", "외로워", "아파", "상처", "허무", "지쳐", "공허"],
        "responses": [
            "많이 힘들었겠다. 그 감정을 혼자서 버텨온 것 같아.",
            "지금 마음이 많이 지쳐 보인다. 그렇게 느껴도 괜찮아."
        ]
    },
    "기쁨": {
        "keywords": ["기뻐", "행복", "좋아", "신나", "즐거워", "웃겨", "설레", "만족", "뿌듯", "재밌어"],
        "responses": [
            "그 말에서 기분 좋은 에너지가 느껴져.",
            "요즘 그런 순간이 있다는 게 참 다행이야."
        ]
    },
    "분노": {
        "keywords": ["화나", "짜증", "열받아", "억울", "분해", "빡쳐", "답답", "불공평"],
        "responses": [
            "그 상황이면 화가 나는 게 너무 당연해.",
            "억울한 마음이 많이 쌓였던 것 같아."
        ]
    },
    "불안": {
        "keywords": ["불안", "걱정", "초조", "긴장", "무서워", "두려워", "떨려", "불확실"],
        "responses": [
            "앞이 안 보여서 더 불안했을 것 같아.",
            "계속 신경 쓰였겠구나."
        ]
    },
    "외로움": {
        "keywords": ["외로워", "혼자", "쓸쓸", "고독", "적적", "허전"],
        "responses": [
            "혼자라고 느끼는 시간이 참 길었을 것 같아.",
            "그 외로움이 마음에 많이 남아 있었구나."
        ]
    },
    "후회": {
        "keywords": ["후회", "미안", "실수", "자책", "돌이켜", "그때"],
        "responses": [
            "이미 충분히 많이 돌아본 것 같아.",
            "너무 자신을 몰아붙이지 않아도 돼."
        ]
    },
    "피로": {
        "keywords": ["피곤", "지쳐", "버거워", "힘겨워", "탈진"],
        "responses": [
            "지금은 쉬라는 신호 같아.",
            "그만큼 열심히 살아왔다는 증거 같아."
        ]
    },
    "기대": {
        "keywords": ["기대", "바라", "희망", "앞으로", "될까"],
        "responses": [
            "그 기대 안에 네 마음이 담겨 있는 것 같아.",
            "잘 되길 바라는 마음이 느껴져."
        ]
    },
    "혼란": {
        "keywords": ["혼란", "헷갈려", "모르겠어", "정리가 안돼"],
        "responses": [
            "생각이 복잡해질 만한 상황이었겠다.",
            "마음이 아직 정리 중인 것 같아."
        ]
    },
    "무기력": {
        "keywords": ["무기력", "의욕없어", "아무것도", "귀찮아"],
        "responses": [
            "아무것도 하기 싫을 때도 있지.",
            "그만큼 에너지가 많이 소진된 것 같아."
        ]
    }
}

# =====================
# 감정 색상 (10개)
# =====================
emotion_colors = {
    "슬픔": "#4A6FA5",
    "기쁨": "#FFD166",
    "분노": "#EF476F",
    "불안": "#6A4C93",
    "외로움": "#577590",
    "후회": "#8D99AE",
    "피로": "#B56576",
    "기대": "#06D6A0",
    "혼란": "#F4A261",
    "무기력": "#ADB5BD"
}


# =====================
# 세션 상태 초기화
# =====================
if "emotion_count" not in st.session_state:
    st.session_state.emotion_count = {e: 0 for e in emotion_data}

if "chat_log" not in st.session_state:
    st.session_state.chat_log = []


# =====================
# 공감 응답 함수
# =====================
def empathic_response(text):
    for emotion, data in emotion_data.items():
        for keyword in data["keywords"]:
            if keyword in text:
                if emotion not in st.session_state.emotion_count:
                    st.session_state.emotion_count[emotion] = 0
                st.session_state.emotion_count[emotion] += 1
                return random.choice(data["responses"])
    return "그런 일이 있었구나. 조금 더 이야기해 줄래?"


# =====================
# UI
# =====================
st.title("공감형 감정 AI")
st.write("감정을 입력해 주세요. `종료`라고 입력하면 분석 결과가 나와요.")

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

        if total > 0:
            stats = [(e, c / total * 100) for e, c in st.session_state.emotion_count.items() if c > 0]
            stats.sort(key=lambda x: x[1], reverse=True)

            emotions = [e for e, _ in stats]
            percents = [round(p, 1) for _, p in stats]
            colors = [emotion_colors.get(e, "#999999") for e in emotions]

            fig, ax = plt.subplots()
            bars = ax.bar(emotions, percents, color=colors)
            ax.set_ylim(0, 100)

            max_idx = percents.index(max(percents))
            ax.text(bars[max_idx].get_x() + bars[max_idx].get_width() / 2,
                    percents[max_idx] + 2, "★", ha="center", fontsize=16)

            st.pyplot(fig)

        st.write("지금까지의 대화에서 드러난 감정 흐름이야.")
        st.write("이야기해 줘서 고마워.")

        # 초기화
        st.session_state.emotion_count = {e: 0 for e in emotion_data}
        st.session_state.chat_log = []

    else:
        ai = empathic_response(user_input)
        st.session_state.chat_log.append(("AI", ai))


# =====================
# 대화 출력
# =====================
for speaker, msg in st.session_state.chat_log:
    st.write(f"**{speaker}:** {msg}")
