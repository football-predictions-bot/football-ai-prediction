import streamlit as st
import datetime
import requests
import google.generativeai as genai

# ၁။ Dictionary & Session State
if 'lang' not in st.session_state:
    st.session_state.lang = 'EN'
if 'team_list' not in st.session_state:
    st.session_state.team_list = ["Select Team"]

def toggle_lang():
    st.session_state.lang = 'MM' if st.session_state.lang == 'EN' else 'EN'

d = {
    'EN': {
        'title1': 'Predictions', 'sel_league': 'Select League', 'sel_date': 'Select Date',
        'btn_check': 'Check Matches Now', 'title2': 'Select Team',
        'home': 'HOME TEAM', 'away': 'AWAY TEAM', 'btn_gen': 'Generate Predictions'
    },
    'MM': {
        'title1': 'ပွဲကြိုခန့်မှန်းချက်များ', 'sel_league': 'လိဂ်ကို ရွေးချယ်ပါ', 'sel_date': 'ရက်စွဲကို ရွေးချယ်ပါ',
        'btn_check': 'ပွဲစဉ်များကို စစ်ဆေးမည်', 'title2': 'အသင်းကို ရွေးချယ်ပါ',
        'home': 'အိမ်ရှင်အသင်း', 'away': 'ဧည့်သည်အသင်း', 'btn_gen': 'ခန့်မှန်းချက် ထုတ်ယူမည်'
    }
}
lang = st.session_state.lang

# Football-Data.org League Codes
league_codes = {
    "Premier League": "PL",
    "Champions League": "CL",
    "La Liga": "PD",
    "Bundesliga": "BL1",
    "Series A": "SA",
    "Ligue 1": "FL1"
}

with open("style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# CSS for hidden buttons overlay
st.markdown("""
    <style>
    div[key="check_btn_hidden"] button, div[key="gen_btn_hidden"] button {
        background-color: transparent !important;
        border: none !important;
        color: transparent !important;
        height: 55px !important;
        margin-top: -55px !important;
        z-index: 10 !important;
    }
    div[key="check_btn_hidden"] button:hover, div[key="gen_btn_hidden"] button:hover {
        background-color: rgba(255, 255, 255, 0.1) !important;
    }
    </style>
""", unsafe_allow_html=True)

col_space, col_lang = st.columns([8, 2])
with col_lang:
    st.button("မြန်မာ / EN", on_click=toggle_lang)

st.markdown(f'<div class="title-style">{d[lang]["title1"]}</div>', unsafe_allow_html=True)

# ၂။ Select League & Date
st.markdown(f'<p style="color:#aaa; margin-left:15px;">{d[lang]["sel_league"]}</p>', unsafe_allow_html=True)
league = st.selectbox("L", list(league_codes.keys()), label_visibility="collapsed")

st.markdown(f'<p style="
