import streamlit as st
import datetime

# ၁။ Dictionary logic
if 'lang' not in st.session_state:
    st.session_state.lang = 'EN'

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

with open("style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Language Toggle Button (ညာဘက်အပေါ်မှာ ထည့်ထားသည်)
col_space, col_lang = st.columns([8, 2])
with col_lang:
    st.button("မြန်မာ / EN", on_click=toggle_lang)

# ၁။ Predictions Title
st.markdown(f'<div class="title-style">{d[lang]["title1"]}</div>', unsafe_allow_html=True)

# ၂။ Select League & Date
st.markdown(f'<p style="color:#aaa; margin-left:15px;">{d[lang]["sel_league"]}</p>', unsafe_allow_html=True)
league = st.selectbox("L", [
    "Premier League", 
    "Champions League", 
    "La Liga", 
    "Bundesliga", 
    "Series A", 
    "Ligue 1"
], label_visibility="collapsed")

st.markdown(f'<p style="color:#aaa; margin-left:15px; margin-top:15px;">{d[lang]["sel_date"]}</p>', unsafe_allow_html=True)
st.date_input("D", value=datetime.date.today(), min_value=datetime.date.today(), label_visibility="collapsed")

# ၃။ Green Glossy Button
st.markdown(f'<div class="btn-green-glossy">{d[lang]["btn_check"]}</div>', unsafe_allow_html=True)

# ၄။ Select Team Title
st.markdown(f'<div class="title-style" style="font-size:45px; margin-top:20px;">{d[lang]["title2"]}</div>', unsafe_allow_html=True)

# Teams Data
pl_teams = ["Arsenal", "Aston Villa", "Bournemouth", "Brentford", "Brighton & Hove Albion", "Burnley", "Chelsea", "Crystal Palace", "Everton", "Fulham", "Leeds United", "Liverpool", "Manchester City", "Manchester United", "Newcastle United", "Nottingham Forest", "Sunderland", "Tottenham Hotspur", "West Ham United", "Wolverhampton"]
cl_teams = ["AS Monaco", "Ajax Amsterdam", "Arsenal", "Atalanta", "Athletic Club", "Atlético Madrid", "Barcelona", "Bayer Leverkusen", "Bayern Munich", "Benfica", "Bodo/Glimt", "Borussia Dortmund", "Chelsea", "Club Brugge", "Eintracht Frankfurt", "F.C. København", "FK Qarabag", "Galatasaray", "Internazionale", "Juventus", "Kairat Almaty", "Liverpool", "Manchester City", "Marseille", "Napoli", "Newcastle United", "Olympiacos", "PSV Eindhoven", "Pafos", "Paris Saint-Germain", "Real Madrid", "Slavia Prague", "Sporting CP", "Tottenham Hotspur", "Union St.-Gilloise", "Villarreal"]
la_liga_teams = ["Alavés", "Athletic Club", "Atlético Madrid", "Barcelona", "Celta Vigo", "Elche", "Espanyol", "Getafe", "Girona", "Levante", "Mallorca", "Osasuna", "Rayo Vallecano", "Real Betis", "Real Madrid", "Real Oviedo", "Real Sociedad", "Sevilla", "Valencia", "Villarreal"]
bundesliga_teams = ["1. FC Heidenheim 1846", "1. FC Union Berlin", "Bayer Leverkusen", "Bayern Munich", "Borussia Dortmund", "Borussia Mönchengladbach", "Eintracht Frankfurt", "FC Augsburg", "FC Cologne", "Hamburg SV", "Mainz", "RB Leipzig", "SC Freiburg", "St. Pauli", "TSG Hoffenheim", "VfB Stuttgart", "VfL Wolfsburg", "Werder Bremen"]
series_a_teams = ["AC Milan", "AS Roma", "Atalanta", "Bologna", "Cagliari", "Como", "Cremonese", "Fiorentina", "Genoa", "Hellas Verona", "Internazionale", "Juventus", "Lazio", "Lecce", "Napoli", "Parma", "Pisa", "Sassuolo", "Torino", "Udinese"]
ligue_1_teams = ["AJ Auxerre", "AS Monaco", "Angers", "Brest", "Le Havre AC", "Lens", "Lille", "Lorient", "Lyon", "Marseille", "Metz", "Nantes", "Nice", "Paris FC", "Paris Saint-Germain (PSG)", "Stade Rennais", "Strasbourg", "Toulouse"]

# ၅။ Home vs Away Section (Logic)
c1, cvs, c2 = st.columns([2, 1, 2])

if league == "Premier League": current_teams = pl_teams
elif league == "Champions League": current_teams = cl_teams
elif league == "La Liga": current_teams = la_liga_teams
elif league == "Bundesliga": current_teams = bundesliga_teams
elif league == "Series A": current_teams = series_a_teams
elif league == "Ligue 1": current_teams = ligue_1_teams
else: current_teams = ["Select Team"]

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
