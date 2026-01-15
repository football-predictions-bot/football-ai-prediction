import streamlit as st
import datetime

# CSS ချိတ်မယ်
with open("style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# ၁။ Predictions Title
st.markdown('<div class="title-style">Predictions</div>', unsafe_allow_html=True)

# ၂။ Select League & Date
st.markdown('<p style="color:#aaa; margin-left:15px;">Select League</p>', unsafe_allow_html=True)
st.selectbox("L", ["Premier League", "La Liga", "Serie A"], key="league", label_visibility="collapsed")

st.markdown('<p style="color:#aaa; margin-left:15px; margin-top:15px;">Select Date</p>', unsafe_allow_html=True)
st.date_input("D", value=datetime.date(2026, 1, 17), label_visibility="collapsed")

# ၃။ Green Glossy Button
st.button("Check Matches Now")

# ၄။ Select Team Title
st.markdown('<div class="title-style" style="font-size:45px; margin-top:20px;">Select Team</div>', unsafe_allow_html=True)

# ၅။ Purple Match Box (အတွင်းထဲမှာ Home vs Away ကို စုထည့်ထားတယ်)
st.markdown('<div class="match-section">', unsafe_allow_html=True)
col1, col_vs, col2 = st.columns([2, 1, 2])

with col1:
    st.markdown('<p style="color:white; text-align:center; font-weight:900; font-size:12px;">HOME TEAM</p>', unsafe_allow_html=True)
    st.selectbox("H", ["Arsenal", "Liverpool", "Man City"], key="home", label_visibility="collapsed")

with col_vs:
    # VS ကို အလယ်တည့်တည့်ရောက်အောင် Div နဲ့ ထုပ်ထားတယ်
    st.markdown('<div class="vs-ball-center">vs</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<p style="color:white; text-align:center; font-weight:900; font-size:12px;">AWAY TEAM</p>', unsafe_allow_html=True)
    st.selectbox("A", ["Chelsea", "Spurs", "Real Madrid"], key="away", label_visibility="collapsed")
st.markdown('</div>', unsafe_allow_html=True)

# ၆။ Orange Glossy Button
st.button("Generate Predictions")
