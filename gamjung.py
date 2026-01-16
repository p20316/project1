import random
import streamlit as st
import matplotlib.pyplot as plt

# =====================
# 감정 데이터 및 색상 설정
# =====================
emotion_data = {
    "SAD": {"keywords": ["슬퍼", "우울", "힘들어", "눈물", "외로워"], "responses": ["많이 힘들었겠다. 그 감정을 혼자서 버텨온 것 같아.", "지금 마음이 많이 아파 보인다."]},
    "JOY": {"keywords": ["기뻐", "행복", "좋아", "신나", "즐거워"], "responses": ["그 말에서 기분 좋은 에너지가 느껴져.", "요즘 그런 순간이 있다는 게 참 다행이야."]},
    "ANGRY": {"keywords": ["화나", "짜증", "열받아", "억울", "분노"], "responses": ["그 상황이면 화날 수밖에 없었을 것 같아.", "참고 넘기기엔 마음이 너무 상했을 것 같아."]},
    "ANXIETY": {"keywords": ["불안", "걱정", "초조", "무서워", "긴장"], "responses": ["불안할 때는 모든 게 확실하지 않게 느껴지지.", "지금 많이 긴장하고 있는 것 같아."]},
    "LONELY": {"keywords": ["외로워", "혼자", "쓸쓸", "고독", "허전"], "responses": ["혼자라고 느껴질 때 마음이 더 무거워지지.", "누군가 곁에 있었으면 좋겠다는 마음이 느껴져."]},
    "TIRED": {"keywords": ["피곤", "지쳐", "번아웃", "녹초", "탈진"], "responses": ["정말 오래 버텨온 것 같아.", "몸도 마음도 쉬고 싶다고 말하는 것 같아."]},
    "REGRETFUL": {"keywords": ["후회", "실수", "잘못", "미련", "아쉽다"], "responses": ["이미 충분히 스스로를 돌아보고 있는 것 같아.", "그 일 때문에 아직 마음이 많이 남아 있구나."]},
    "FECKLESS": {"keywords": ["무기력", "의욕없어", "귀찮아", "하기싫어"], "responses": ["아무것도 하고 싶지 않을 만큼 지친 것 같아.", "에너지가 바닥난 느낌이 드는 것 같아."]},
    "EXPECTATION": {"keywords": ["기대", "설렘", "두근", "희망", "앞으로"], "responses": ["마음 한편에서 뭔가를 기대하고 있는 것 같아.", "그 설렘이 조심스럽게 느껴져."]},
    "CONFUSED": {"keywords": ["혼란", "헷갈려", "모르겠어", "복잡해", "갈등"], "responses": ["머릿속이 정리되지 않은 느낌이네.", "지금은 방향이 잘 안 보일 수도 있을 것 같아."]}
}

emotion_colors = {
    "SAD": "#4A6FA5", "JOY": "#FFD166", "ANGRY": "#EF476F", "ANXIETY": "#8E7DBE",
    "LONELY": "#6C757D", "TIRED": "#495057", "REGRETFUL": "#A44A3F",
    "FECKLESS": "#ADB5BD", "EXPECTATION": "#06D6A0", "CONFUSED": "#B565A7"
}

# =====================
# 세션 상태 초기화
# =====================
if "emotion_count" not in st.session_state:
    st.session_state.emotion_count = {e: 0 for e in emotion_data}
if "chat_log" not in st.session_state:
    st.session_state.chat_log = []
if "show_analysis" not in st.session_state:
    st.session_state.show_analysis = False

# =====================
# 로직 함수
# =====================
def empathic_response(text):
    for emotion, data in emotion_data.items():
        for keyword in data["keywords"]:
            if keyword in text:
                st.session_state.emotion_count[emotion] = st.session_state.emotion_count.get(emotion, 0) + 1
                return random.choice(data["responses"])
    return "그런 일이 있었구나. 조금 더 이야기해 줄래?"

# =====================
# UI 레이아웃
# =====================
st.title("🍀 공감형 감정 AI")
st.write("감정을 적고 **전송**을 누르세요. `종료`라고 입력하면 분석 결과를 보여드려요.")

# 입력창 (st.form 사용으로 KeyError 및 새로고침 이슈 해결)
with st.form(key="chat_input_form", clear_on_submit=True):
    user_input = st.text_input("나의 이야기:")
    submitted = st.form_submit_button("전송")

if submitted and user_input:
    text = user_input.strip()
    
    if text == "종료":
        st.session_state.show_analysis = True
    else:
        # 대화 기록 저장
        response = empathic_response(text)
        st.session_state.chat_log.append(("나", text))
        st.session_state.chat_log.append(("AI", response))

# =====================
# 📊 감정 분석 결과 그래프 출력
# =====================
if st.session_state.show_analysis:
    total = sum(st.session_state.emotion_count.values())
    
    if total > 0:
        st.divider()
        st.subheader("📊 오늘의 감정 분석 보고서")
        
        # 데이터 정리 (비율 계산 및 정렬)
        stats = [(e, (c / total * 100)) for e, c in st.session_state.emotion_count.items() if c > 0]
        stats.sort(key=lambda x: x[1], reverse=True)

        emotions = [s[0] for s in stats]
        percentages = [s[1] for s in stats]
        colors = [emotion_colors.get(e, "#999999") for e in emotions]

        # Matplotlib 그래프 생성
        fig, ax = plt.subplots(figsize=(10, 5))
        bars = ax.bar(emotions, percentages, color=colors)
        
        ax.set_ylim(0, 100)
        ax.set_ylabel("Percentage (%)")
        ax.set_title("Your Emotional Flow Today", fontsize=15)
        
        # 막대 위에 숫자 표시
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height + 1,
                    f'{height:.1f}%', ha='center', va='bottom')

        st.pyplot(fig)
        st.write("위 차트는 네가 오늘 나눈 대화 속에서 느껴진 감정들의 비율이야.")
    else:
        st.warning("분석할 감정 데이터가 부족해요. 대화를 조금 더 나눠볼까요?")
    
    if st.button("새로운 대화 시작하기"):
        st.session_state.emotion_count = {e: 0 for e in emotion_data}
        st.session_state.chat_log = []
        st.session_state.show_analysis = False
        st.rerun()

# =====================
# 대화 로그 출력
# =====================
st.divider()
for speaker, msg in reversed(st.session_state.chat_log):
    if speaker == "나":
        st.info(f"**{speaker}**: {msg}")
    else:
        st.success(f"**{speaker}**: {msg}")
