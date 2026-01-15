import streamlit as st
import datetime

# ၁။ CSS ချိတ်ဆက်ခြင်း (local_css function မလိုဘဲ တိုက်ရိုက်ဖတ်နည်း)
try:
    with open("style.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
except FileNotFoundError:
    st.error("style.css ဖိုင်ကို ရှာမတွေ့ပါ။ Folder ထဲမှာ style.css ရှိမရှိ စစ်ပေးပါ။")

st.title("Football Predictions")

# ၂။ League ၆ ခု စာရင်း
league_map = {
    "Premier League": 39,
    "Champions League": 2,
    "La Liga": 140,
    "Bundesliga": 78,
    "Serie A": 135,
    "Ligue 1": 61
}

# ၃။ UI Layout (League ရွေးရန်)
st.markdown("<p style='margin-bottom:0;'>Select League</p>", unsafe_allow_html=True)
selected_league_name = st.selectbox(
    "League Selector",
    options=list(league_map.keys()),
    label_visibility="collapsed"
)

# ၄။ Date ရွေးရန်
st.markdown("<p style='margin-bottom:0; margin-top:10px;'>Select Date</p>", unsafe_allow_html=True)
sel_date = st.date_input(
    "Date Selector", 
    value=datetime.date(2026, 1, 17),
    label_visibility="collapsed"
)

# ၅။ Check Match Button
if st.button("Check Match"):
    # ဒီနေရာမှာ API ကနေ ပွဲစဉ်တွေ ဆွဲထုတ်တဲ့ logic လာပါမယ်
    st.info(f"{selected_league_name} ရဲ့ {sel_date} ပွဲစဉ်များကို ရှာဖွေနေပါသည်...")

st.write("---")
st.markdown("<h3>Select Team</h3>", unsafe_allow_html=True)
