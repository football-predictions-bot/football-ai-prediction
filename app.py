import streamlit as st

# CSS ချိတ်ဆက်ခြင်း
with open("style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

st.markdown("<h1 style='text-align: center;'>Football Predictions</h1>", unsafe_allow_html=True)

# ... (League & Date Selection အပိုင်း) ...

st.markdown("<h3>Select Team</h3>", unsafe_allow_html=True)

# ခရမ်းရောင် Box (ဒီတစ်ခုတည်းပဲ ရှိရပါမယ်)
st.markdown('<div class="team-container">', unsafe_allow_html=True)

# အထဲမှာ Home Team ရွေးတာ၊ VS၊ Away Team ရွေးတာကို အစဉ်လိုက် ထည့်မယ်
st.markdown("<div style='color:white; font-weight:bold; margin-top:10px;'>HOME TEAM</div>", unsafe_allow_html=True)
h_team = st.selectbox("Home", ["Arsenal", "Man Utd", "Liverpool"], key="h", label_visibility="collapsed")

st.markdown('<div class="vs-ball">VS</div>', unsafe_allow_html=True)

st.markdown("<div style='color:white; font-weight:bold;'>AWAY TEAM</div>", unsafe_allow_html=True)
a_team = st.selectbox("Away", ["Chelsea", "Man City", "Spurs"], key="a", label_visibility="collapsed")

st.markdown('</div>', unsafe_allow_html=True)

# Predictions ခလုတ်
if st.button("Predictions"):
    st.info("Analyzing match...")
