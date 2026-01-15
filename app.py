import streamlit as st
import datetime

# CSS ချိတ်ဆက်ခြင်း
with open("style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

st.title("Football Predictions")

# ၁။ Input Section
st.markdown("<p style='margin-bottom:5px;'>Select League</p>", unsafe_allow_html=True)
st.selectbox("League", ["Premier League", "Champions League", "La Liga", "Bundesliga", "Serie A", "Ligue 1"], label_visibility="collapsed")

st.markdown("<p style='margin-bottom:5px; margin-top:10px;'>Select Date</p>", unsafe_allow_html=True)
st.date_input("Date", value=datetime.date(2026, 1, 17), label_visibility="collapsed")

# ၂။ Check Match ခလုတ် (Purple Glossy)
st.button("Check Match")

# ၃။ Select Team Header
st.markdown("<h3>Select Team</h3>", unsafe_allow_html=True)

# ၄။ Team Selection UI (VS ပုံစံ)
st.markdown("""
    <div class="team-container">
        <div style="text-align:center; font-weight:bold;">HOME TEAM</div>
        <div class="vs-ball">VS</div>
        <div style="text-align:center; font-weight:bold;">AWAY TEAM</div>
    </div>
    """, unsafe_allow_html=True)

# Dropdowns (Home/Away အသင်းရွေးရန်)
c1, c2 = st.columns(2)
with c1:
    st.selectbox("H", ["Man Utd", "Arsenal", "Liverpool"], key="h", label_visibility="collapsed")
with c2:
    st.selectbox("A", ["Man City", "Chelsea", "Spurs"], key="a", label_visibility="collapsed")

# ၅။ Predictions ခလုတ် (Orange Glossy)
st.button("Predictions")
