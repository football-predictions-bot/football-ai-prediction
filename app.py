import streamlit as st
import datetime

# CSS ချိတ်ဆက်ခြင်း
with open("style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# ၁။ Predictions Header
st.markdown("<h1 class='main-title'>Predictions</h1>", unsafe_allow_html=True)

# ၂။ Select League & Date
st.markdown("<p style='margin-bottom:5px; color:#aaa;'>Select League</p>", unsafe_allow_html=True)
st.selectbox("League", ["Premier League", "La Liga", "Serie A"], label_visibility="collapsed")

st.markdown("<p style='margin-top:10px; margin-bottom:5px; color:#aaa;'>Select Date</p>", unsafe_allow_html=True)
st.date_input("Date", value=datetime.date(2026, 1, 17), label_visibility="collapsed")

# ၃။ Check Matches Now Button
st.button("Check Matches Now")

# ၄။ Select Team Header
st.markdown("<h1 class='select-team-title'>Select Team</h1>", unsafe_allow_html=True)

# ၅။ Purple Container (Home - VS - Away)
st.markdown('<div class="match-box">', unsafe_allow_html=True)
c1, cvs, c2 = st.columns([2, 1, 2])
with c1:
    st.selectbox("Home", ["Home Team", "Arsenal", "Man Utd"], key="h", label_visibility="collapsed")
with cvs:
    st.markdown('<div class="vs-circle">vs</div>', unsafe_allow_html=True)
with c2:
    st.selectbox("Away", ["Away Team", "Man City", "Chelsea"], key="a", label_visibility="collapsed")
st.markdown('</div>', unsafe_allow_html=True)

# ၆။ Generate Predictions Button
st.button("Generate Predictions")
