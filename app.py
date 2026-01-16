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

# Language Toggle
col_space, col_lang = st.columns([8, 2])
with col_lang:
    st.button("မြန်မာ / EN", on_click=toggle_lang)

st.markdown(f'<div class="title-style">{d[lang]["title1"]}</div>', unsafe_allow_html=True)

# ၂။ Select League & Date
st.markdown(f'<p style="color:#aaa; margin-left:15px;">{d[lang]["sel_league"]}</p>', unsafe_allow_html=True)
league = st.selectbox("L", list(league_codes.keys()), label_visibility="collapsed")

st.markdown(f'<p style="color:#aaa; margin-left:15px; margin-top:15px;">{d[lang]["sel_date"]}</p>', unsafe_allow_html=True)
# ယနေ့ထက် စောသောရက်များ ရွေးမရအောင် min_value ထည့်သွင်းထားသည်
sel_date = st.date_input("D", value=datetime.date.today(), min_value=datetime.date.today(), label_visibility="collapsed")

# ၃။ Check Matches Now (Green Glossy)
st.markdown(f'<div class="btn-green-glossy">{d[lang]["btn_check"]}</div>', unsafe_allow_html=True)
if st.button(" ", key="check_btn_hidden", use_container_width=True):
    with st.spinner('Checking Matches...'):
        try:
            token = st.secrets["api_keys"]["FOOTBALL_DATA_KEY"]
            date_str = sel_date.strftime('%Y-%m-%d')
            url = f"https://api.football-data.org/v4/competitions/{league_codes[league]}/matches?dateFrom={date_str}&dateTo={date_str}"
            headers = {'X-Auth-Token': token}
            response = requests.get(url, headers=headers)
            data = response.json()
            matches = data.get('matches', [])
            if matches:
                teams = set()
                for m in matches:
                    teams.add(m['homeTeam']['name'])
                    teams.add(m['awayTeam']['name'])
                st.session_state.team_list = sorted(list(teams))
                st.success(f"Found {len(matches)} matches!")
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

# ၆။ Orange Glossy Button (Generate Predictions)
st.markdown(f'<div class="btn-orange-glossy">{d[lang]["btn_gen"]}</div>', unsafe_allow_html=True)
if st.button(" ", key="gen_btn_hidden", use_container_width=True):
    if h_team and a_team and h_team != "Select Team" and h_team != "No matches found":
        with st.spinner('AI is thinking...'):
            try:
                genai.configure(api_key=st.secrets["gemini_keys"]["GEMINI_KEY_1"])
                model = genai.GenerativeModel('gemini-3-flash-preview')
                prompt = f"Analyze {h_team} vs {a_team} in {league}. Predict winner and score. Respond in {lang} language."
                response = model.generate_content(prompt)
                st.info(response.text)
            except Exception as e:
                st.error(f"AI Error: {str(e)}")
    else:
        st.warning("Please select teams first!")
        
