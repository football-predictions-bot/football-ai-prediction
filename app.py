import streamlit as st
import datetime
import requests
import google.generativeai as genai
import time


# UI အမှိုက်များ (Menu, Toolbar, Badge) ကို လုံးဝပျောက်သွားစေရန် configuration သတ်မှတ်ခြင်း
st.set_page_config(
    page_title="Football AI",
    layout="wide",
    initial_sidebar_state="collapsed",
    menu_items=None
)

# မြန်မာစံတော်ချိန် (UTC + 6:30) ကိုတွက်ချက်ခြင်း
now_mm = datetime.datetime.utcnow() + datetime.timedelta(hours=6, minutes=30)
today_mm = now_mm.date()

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
        'home': 'HOME TEAM', 'away': 'AWAY TEAM', 'btn_gen': 'Generate Predictions',
        'trans_btn': 'မြန်မာဘာသာသို့ ပြောင်းရန်',
        'date_opts': ["Manual Date", "Within 24 Hours", "Within 48 Hours"],
        'ai_lang': 'English'
    },
    'MM': {
        'title1': 'ပွဲကြိုခန့်မှန်းချက်များ', 'sel_league': 'လိဂ်ကို ရွေးချယ်ပါ', 'sel_date': 'ရက်စွဲကို ရွေးချယ်ပါ',
        'btn_check': 'ပွဲစဉ်များကို စစ်ဆေးမည်', 'title2': 'အသင်းကို ရွေးချယ်ပါ',
        'home': 'အိမ်ရှင်အသင်း', 'away': 'ဧည့်သည်အသင်း', 'btn_gen': 'ခန့်မှန်းချက် ထုတ်ယူမည်',
        'trans_btn': 'Switch to English',
        'date_opts': ["ရက်စွဲတပ်၍ရှာမည်", "၂၄ နာရီအတွင်း", "၄၈ နာရီအတွင်း"],
        'ai_lang': 'Burmese'
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

# Language Toggle
col_space, col_lang = st.columns([7, 3])
with col_lang:
    st.markdown('<div class="lang-wrapper">', unsafe_allow_html=True)
    st.button(d[lang]["trans_btn"], key="lang_btn", on_click=toggle_lang, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown(f'<div class="title-style">{d[lang]["title1"]}</div>', unsafe_allow_html=True)

# ၂။ Select League & Date
st.markdown(f'<p style="color:#aaa; margin-left:15px;">{d[lang]["sel_league"]}</p>', unsafe_allow_html=True)
league = st.selectbox("L", list(league_codes.keys()), label_visibility="collapsed")

st.markdown(f'<p style="color:#aaa; margin-left:15px; margin-top:15px;">{d[lang]["sel_date"]}</p>', unsafe_allow_html=True)
date_option = st.radio("Date Option", d[lang]['date_opts'], horizontal=True, label_visibility="collapsed")
sel_date = st.date_input("D", value=today_mm, min_value=today_mm, label_visibility="collapsed")

# ၃။ Check Matches Now
st.markdown('<div class="check-btn-wrapper">', unsafe_allow_html=True)
check_click = st.button(d[lang]["btn_check"], key="check_btn", use_container_width=True)
st.markdown('</div>', unsafe_allow_html=True)

if check_click:
    # Loading Animation
    progress_bar = st.progress(0)
    for percent_complete in range(100):
        time.sleep(0.01)
        progress_bar.progress(percent_complete + 1)
    
    with st.spinner('Checking Matches...'):
        try:
            token = st.secrets["api_keys"]["FOOTBALL_DATA_KEY"]
            if date_option == d[lang]['date_opts'][1]: # 24 Hours
                d_from = today_mm
                d_to = today_mm + datetime.timedelta(days=1)
            elif date_option == d[lang]['date_opts'][2]: # 48 Hours
                d_from = today_mm
                d_to = today_mm + datetime.timedelta(days=2)
            else:
                d_from = d_to = sel_date

            url = f"https://api.football-data.org/v4/competitions/{league_codes[league]}/matches?dateFrom={d_from}&dateTo={d_to}"
            headers = {'X-Auth-Token': token}
            response = requests.get(url, headers=headers)
            data = response.json()
            matches = data.get('matches', [])
            if matches:
                teams = set()
                match_display_data = []
                for m in matches:
                    h = m['homeTeam']['name']
                    a = m['awayTeam']['name']
                    teams.add(h)
                    teams.add(a)
                    match_display_data.append({"Home Team": h, "Away Team": a, "Time (UTC)": m['utcDate'][11:16]})
                
                st.session_state.team_list = sorted(list(teams))
                st.success(f"Found {len(matches)} matches!")
                st.table(match_display_data)
            else:
                st.session_state.team_list = ["No matches found"]
                st.warning("No matches found.")
        except Exception as e:
            st.error(f"Error: {str(e)}")

# ၄။ Select Team Title
st.markdown(f'<div class="title-style" style="font-size:45px; margin-top:20px;">{d[lang]["title2"]}</div>', unsafe_allow_html=True)
# ၅။ Home vs Away Section
c1, cvs, c2 = st.columns([2, 1, 2])
current_teams = st.session_state.team_list

with c1:
    st.markdown(f'<p style="color:white; text-align:center; font-weight:900; font-size:12px;">{d[lang]["home"]}</p>', unsafe_allow_html=True)
    h_team = st.selectbox("H", current_teams, key="h", label_visibility="collapsed")

with cvs:
    st.markdown('<div style="display: flex; justify-content: center; align-items: center; height: 100%;"><div class="vs-ball">vs</div></div>', unsafe_allow_html=True)

with c2:
    st.markdown(f'<p style="color:white; text-align:center; font-weight:900; font-size:12px;">{d[lang]["away"]}</p>', unsafe_allow_html=True)
    a_team = st.selectbox("A", [t for t in current_teams if t != h_team], key="a", label_visibility="collapsed")

# ၆။ Orange Glossy Button
st.markdown('<div class="gen-btn-wrapper">', unsafe_allow_html=True)
gen_click = st.button(d[lang]["btn_gen"], key="gen_btn", use_container_width=True)
st.markdown('</div>', unsafe_allow_html=True)

if gen_click:
    if h_team and a_team and h_team != "Select Team" and h_team != "No matches found":
        # Loading Animation
        progress_bar = st.progress(0)
        for percent_complete in range(100):
            time.sleep(0.01)
            progress_bar.progress(percent_complete + 1)
            
        with st.spinner('AI is thinking...'):
            try:
                genai.configure(api_key=st.secrets["gemini_keys"]["GEMINI_KEY_1"])
                model = genai.GenerativeModel('gemini-flash-latest') 
                prompt = f"Analyze {h_team} vs {a_team} in {league}. Predict winner and score. Respond in {d[lang]['ai_lang']} language."
                response = model.generate_content(prompt)
                st.info(response.text)
            except Exception as e:
                st.error(f"AI Error: {str(e)}")
    else:
        st.warning("Please select teams first!")
