import streamlit as st
import datetime

with open("style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# ၁။ Predictions Title
st.markdown('<div class="title-style">Predictions</div>', unsafe_allow_html=True)

# ၂။ Select League & Date
st.markdown('<p style="color:#aaa; margin-left:15px;">Select League</p>', unsafe_allow_html=True)
st.selectbox("L", ["Premier League", "La Liga"], label_visibility="collapsed")

st.markdown('<p style="color:#aaa; margin-left:15px; margin-top:15px;">Select Date</p>', unsafe_allow_html=True)
st.date_input("D", value=datetime.date(2026, 1, 1), label_visibility="collapsed")

# ၃။ Green Glossy Button
st.markdown('<div class="btn-green-glossy">Check Matches Now</div>', unsafe_allow_html=True)

# ၄။ Select Team Title
st.markdown('<div class="title-style" style="font-size:45px; margin-top:20px;">Select Team</div>', unsafe_allow_html=True)

# ၅။ ခရမ်းရောင် Box နဲ့ ပတ်သက်တာတွေ အကုန်ဖျက်ပြီး VS ကို အလယ်ပို့လိုက်ပြီ
c1, cvs, c2 = st.columns([2, 1, 2])

with c1:
    st.markdown('<p style="color:white; text-align:center; font-weight:900; font-size:12px;">HOME TEAM</p>', unsafe_allow_html=True)
    st.selectbox("H", ["Arsenal", "Man Utd"], key="h", label_visibility="collapsed")

with cvs:
    # VS ဘောလုံးကို အလယ်တည့်တည့်ရောက်အောင် div နဲ့ အုပ်ပြီး flex နဲ့ ညှိထားပါတယ်
    st.markdown('<div style="display: flex; justify-content: center; align-items: center; height: 100%;"><div class="vs-ball">vs</div></div>', unsafe_allow_html=True)

with c2:
    st.markdown('<p style="color:white; text-align:center; font-weight:900; font-size:12px;">AWAY TEAM</p>', unsafe_allow_html=True)
    st.selectbox("A", ["Chelsea", "Man City"], key="a", label_visibility="collapsed")

# ၆။ Orange Glossy Button
st.markdown('<div class="btn-orange-glossy">Generate Predictions</div>', unsafe_allow_html=True)
