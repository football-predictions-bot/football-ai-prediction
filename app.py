import streamlit as st
import datetime
import requests

# ၁။ Dictionary logic
if 'lang' not in st.session_state:
    st.session_state.lang = 'EN'

if 'team_list' not in st.session_state:
    st.session_state.team_list = ["Select Team"]

def toggle_lang():
    st.session_state.lang = 'MM' if st.session_state.lang == 'EN' else 'EN'

d = {
    'EN': {
        'title1': 'Predictions',
        'sel_league': 'Select League',
        'sel_date': 'Select Date',
        'btn_check': 'Check Matches Now',
        'title2': 'Select Team',
        'home': 'HOME TEAM',
        'away': 'AWAY TEAM',
        'btn_gen': 'Generate Predictions'
    },
    'MM': {
        'title1': 'ပွဲကြိုခန့်မှန်းချက်များ',
        'sel_league': 'လိဂ်ကို ရွေးချယ်ပါ',
        'sel_date': 'ရက်စွဲကို ရွေးချယ်ပါ',
        'btn_check': 'ပွဲစဉ်များကို စစ်ဆေးမည်',
        'title2': 'အသင်းကို ရွေးချယ်ပါ',
        'home': 'အိမ်ရှင်အသင်း',
        'away': 'ဧည့်သည်အသင်း',
        'btn_gen': 'ခန့်မှန်းချက် ထုတ်ယူမည်'
    }
}
lang = st.session_state.lang

league_ids = {
    "Premier League": 39,
    "Champions League": 2,
    "La Liga": 140,
    "Bundesliga": 78,
    "Series A": 135,
    "Ligue 1": 61
}

with open("style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

col_space, col_lang = st.columns([8, 2])
with col_lang:
    st.button("မြန်မာ / EN", on_click=toggle_lang)

st.markdown(f'<div class="title-style">{d[lang]["title1"]}</div>', unsafe_allow_html=True)

# ၂။ Select League & Date
st.markdown(f'<p style="color:#aaa; margin-left:15px;">{d[lang]["sel_league"]}</p>', unsafe_allow_html=True)
league = st.selectbox("L", list(league_ids.keys()), label_visibility="collapsed")

st.markdown(f'<p style="color:#aaa; margin-left:15px; margin-top:15px;">{d[lang]["sel_date"]}</p>', unsafe_allow_html=True)

# စမ်းသပ်ရန်အတွက် min_value ကို ခေတ္တဖြုတ်ထားပါသည် (၂၀၂၄ ရက်စွဲရွေးရန်)
sel_date = st.date_input("D", value=datetime.date.today(), label_visibility="collapsed")

# ၃။ Green Glossy Button
if st.button(d[lang]["btn_check"]):
    with st.spinner('Checking API...'):
        try:
            url = "https://v3.football.api-sports.io/fixtures"
            headers = {
                'x-rapidapi-key': st.secrets["api_keys"]["APISPORTS_KEY_1"],
                'x-rapidapi-host': 'v3.football.api-sports.io'
            }
            
            # Season Logic
            current_season = sel_date.year if sel_date.month >= 8 else sel_date.year - 1
            
            params = {
                'league': league_ids[league],
                'season': current_season,
                'date': sel_date.strftime('%Y-%m-%d')
            }
            
            response = requests.get(url, headers=headers, params=params)
            data = response.json()
            
            # Debug Info ပြရန် (ပွဲထွက်လာလျှင် ဒါကို ပြန်ဖြုတ်ပါ)
            st.write("Debug Info:", data)
            
            fixtures = data.get('response', [])
            if fixtures:
                teams = set()
                for fxt in fixtures:
                    teams.add(fxt['teams']['home']['name'])
                    teams.add(fxt['teams']['away']['name'])
                st.session_state.team_list = sorted(list(teams))
                st.success(f"Found {len(fixtures)} matches!")
            else:
                st.session_state.team_list = ["No matches found"]
                st.warning("No matches found for this date in API.")
        except Exception as e:
            st.error(f"Error: {str(e)}")

st.markdown(f'<div class="title-style" style="font-size:45px; margin-top:20px;">{d[lang]["title2"]}</div>', unsafe_allow_html=True)

# ၅။ Home vs Away Section
c1, cvs, c2 = st.columns([2, 1, 2])
current_teams = st.session_state.team_list

with c1:
    st.markdown(f'<p style="color:white; text-align:center; font-weight:900; font-size:12px;">{d[lang]["home"]}</p>', unsafe_allow_html=True)
    h_options = [t for t in current_teams if t != st.session_state.get('a')]
    st.selectbox("H", h_options, key="h", label_visibility="collapsed")

with cvs:
    st.markdown('<div style="display: flex; justify-content: center; align-items: center; height: 100%;"><div class="vs-ball">vs</div></div>', unsafe_allow_html=True)

with c2:
    st.markdown(f'<p style="color:white; text-align:center; font-weight:900; font-size:12px;">{d[lang]["away"]}</p>', unsafe_allow_html=True)
    a_options = [t for t in current_teams if t != st.session_state.get('h')]
    st.selectbox("A", a_options, key="a", label_visibility="collapsed")

# ၆။ Orange Glossy Button
st.markdown(f'<div class="btn-orange-glossy">{d[lang]["btn_gen"]}</div>', unsafe_allow_html=True)
