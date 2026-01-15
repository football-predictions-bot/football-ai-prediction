import streamlit as st
import datetime

# CSS ချိတ်ဆက်ခြင်း
with open("style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

st.title("Football Predictions")

# ၁။ League & Date
sel_league = st.selectbox("Select League", ["Premier League", "Champions League", "La Liga", "Bundesliga", "Serie A", "Ligue 1"], label_visibility="collapsed")
sel_date = st.date_input("Select Date", value=datetime.date(2026, 1, 17), label_visibility="collapsed")

# ၂။ Check Match ခလုတ်
st.button("Check Match")

st.markdown("<h3>Select Team</h3>", unsafe_allow_html=True)

# ၃။ Home Team နဲ့ Away Team ကို Box တစ်ခုတည်းထဲ ထည့်ခြင်း
with st.container():
    # HTML/CSS နဲ့ Box ပုံစံဆောက်ခြင်း
    st.markdown('<div class="team-container">', unsafe_allow_html=True)
    
    col1, col_vs, col2 = st.columns([2, 1, 2])
    
    with col1:
        st.markdown("<div style='text-align:center; font-weight:bold; margin-bottom:5px;'>HOME TEAM</div>", unsafe_allow_html=True)
        h_team = st.selectbox("Home", ["Arsenal", "Liverpool", "Man Utd"], key="h", label_visibility="collapsed")
        
    with col_vs:
        # အလယ်က VS Ball
        st.markdown('<div class="vs-ball">VS</div>', unsafe_allow_html=True)
        
    with col2:
        st.markdown("<div style='text-align:center; font-weight:bold; margin-bottom:5px;'>AWAY TEAM</div>", unsafe_allow_html=True)
        a_team = st.selectbox("Away", ["Man City", "Chelsea", "Spurs"], index=1, key="a", label_visibility="collapsed")
        
    st.markdown('</div>', unsafe_allow_html=True)

# ၄။ Predictions ခလုတ်
st.button("Predictions")
