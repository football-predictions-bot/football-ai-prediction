import streamlit as st
import datetime

# CSS ချိတ်ဆက်ခြင်း
with open("style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Title
st.markdown("<h1 style='text-align: center;'>Football Predictions</h1>", unsafe_allow_html=True)

# ၁။ League & Date (ပုံထဲကအတိုင်း)
sel_league = st.selectbox("Select League", ["Premier League", "Champions League", "La Liga", "Bundesliga", "Serie A", "Ligue 1"], label_visibility="collapsed")
sel_date = st.date_input("Select Date", value=datetime.date(2026, 1, 17), label_visibility="collapsed")

# ၂။ Check Match ခလုတ် (Purple Glossy)
st.button("Check Match")

# ၃။ Select Team Header (အလယ်တည့်တည့်)
st.markdown('<div class="select-team-header">Select Team</div>', unsafe_allow_html=True)

# ၄။ ပုံထဲကအတိုင်း Box တစ်ခုတည်းထဲမှာ အကုန်ထည့်ခြင်း
with st.container():
    st.markdown('<div class="team-container">', unsafe_allow_html=True)
    
    # Home Team
    st.markdown("<div style='color:white; font-weight:bold; margin-bottom:5px;'>HOME TEAM</div>", unsafe_allow_html=True)
    h_team = st.selectbox("H", ["Arsenal", "Man Utd", "Liverpool"], key="h", label_visibility="collapsed")
    
    # VS Ball
    st.markdown('<div class="vs-ball">VS</div>', unsafe_allow_html=True)
    
    # Away Team
    st.markdown("<div style='color:white; font-weight:bold; margin-bottom:5px;'>AWAY TEAM</div>", unsafe_allow_html=True)
    a_team = st.selectbox("A", ["Chelsea", "Man City", "Spurs"], key="a", label_visibility="collapsed")
    
    st.markdown('</div>', unsafe_allow_html=True)

# ၅။ Predictions ခလုတ် (Orange Glossy)
st.button("Predictions")
