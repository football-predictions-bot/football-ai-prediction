import streamlit as st
import datetime

# ၁။ CSS File ကို ချိတ်ဆက်ခြင်း
with open("style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# ၂။ Predictions Title (Gradient Text)
st.markdown('<h1 class="gradient-text" style="font-size: 55px;">Predictions</h1>', unsafe_allow_html=True)

# ၃။ Select League & Date (Labels are plain text, Inputs are neon)
st.markdown('<p style="color: #aaa; margin-left: 5px; margin-bottom: 5px;">Select League</p>', unsafe_allow_html=True)
league = st.selectbox("League", ["Premier League", "La Liga", "Serie A", "Bundesliga", "Ligue 1"], label_visibility="collapsed")

st.markdown('<p style="color: #aaa; margin-left: 5px; margin-top: 15px; margin-bottom: 5px;">Select Date</p>', unsafe_allow_html=True)
match_date = st.date_input("Date", value=datetime.date(2026, 1, 17), label_visibility="collapsed")

# ၄။ Check Matches Now Button (Green Glossy)
# CSS ထဲက div.stButton > button:first-of-type က ဒီခလုတ်ကို အလှပြင်ပေးမှာပါ
st.button("Check Matches Now")

# ၅။ Select Team Title
st.markdown('<h1 class="gradient-text" style="font-size: 45px; margin-top: 30px;">Select Team</h1>', unsafe_allow_html=True)

# ၆။ Home vs Away Box (Purple Neon Container)
# အစ်ကိုဝိုင်းပြထားတဲ့ ဘောင်အပိုတွေ မပါအောင် div တစ်ခုတည်းနဲ့ ထုပ်ထားပါတယ်
st.markdown('<div class="match-box-ui">', unsafe_allow_html=True)

col1, col_vs, col2 = st.columns([2, 1, 2])

with col1:
    st.markdown('<p class="team-label">HOME TEAM</p>', unsafe_allow_html=True)
    home_team = st.selectbox("Home", ["Arsenal", "Liverpool", "Man City", "Man Utd"], key="home", label_visibility="collapsed")

with col_vs:
    # VS Ball Design
    st.markdown('<div style="margin-top: 20px;"><div class="vs-circle-ui">vs</div></div>', unsafe_allow_html=True)

with col2:
    st.markdown('<p class="team-label">AWAY TEAM</p>', unsafe_allow_html=True)
    away_team = st.selectbox("Away", ["Chelsea", "Spurs", "Aston Villa", "Newcastle"], key="away", label_visibility="collapsed")

st.markdown('</div>', unsafe_allow_html=True)

# ၇။ Generate Predictions Button (Orange Glossy)
# CSS ထဲက div.stButton > button:last-of-type က ဒီခလုတ်ကို အလှပြင်ပေးမှာပါ
if st.button("Generate Predictions"):
    st.write(f"Analyzing {home_team} vs {away_team}...")
