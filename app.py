import streamlit as st
import datetime

# CSS ကို ချိတ်ဆက်ခြင်း
with open("style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# ၁။ Predictions Title
st.markdown('<div class="title-gradient">Predictions</div>', unsafe_allow_html=True)

# ၂။ Select League & Date
st.markdown('<p style="color:#aaa; margin-left:10px;">Select League</p>', unsafe_allow_html=True)
st.selectbox("L", ["Premier League", "La Liga"], label_visibility="collapsed")

st.markdown('<p style="color:#aaa; margin-left:10px; margin-top:10px;">Select Date</p>', unsafe_allow_html=True)
st.date_input("D", value=datetime.date(2026, 1, 17), label_visibility="collapsed")

# ၃။ Check Matches Button (Glossy Green)
st.button("Check Matches Now")

# ၄။ Select Team Title
st.markdown('<div class="title-gradient" style="font-size:45px;">Select Team</div>', unsafe_allow_html=True)

# ၅။ Purple Match Box (Box အလွတ်မဖြစ်အောင် တိုက်ရိုက် ရေးထားပါတယ်)
# ဤနေရာတွင် st.container(border=True) ကို မသုံးဘဲ HTML div နဲ့ အုပ်လိုက်ပါမယ်
st.markdown('<div class="match-box-container">', unsafe_allow_html=True)

col1, col_vs, col2 = st.columns([2, 1, 2])

with col1:
    st.markdown('<p style="color:white; text-align:center; font-size:12px; font-weight:900;">HOME TEAM</p>', unsafe_allow_html=True)
    st.selectbox("H", ["Arsenal", "Liverpool", "Man City"], key="home_team", label_visibility="collapsed")

with col_vs:
    # VS ကို အလယ်တည့်တည့်ရောက်အောင် margin: auto နဲ့ ထည့်ထားပါတယ်
    st.markdown('<div class="vs-ball-ui" style="margin: 15px auto;">vs</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<p style="color:white; text-align:center; font-size:12px; font-weight:900;">AWAY TEAM</p>', unsafe_allow_html=True)
    st.selectbox("A", ["Chelsea", "Spurs", "Real Madrid"], key="away_team", label_visibility="collapsed")

st.markdown('</div>', unsafe_allow_html=True)

# ၆။ Generate Predictions Button (Glossy Orange)
st.button("Generate Predictions")
