import streamlit as st
import datetime

with open("style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# ၁။ Predictions Title
st.markdown('<div class="title-style">Predictions</div>', unsafe_allow_html=True)

# ၂။ Select League & Date
st.markdown('<p style="color:#aaa; margin-left:15px;">Select League</p>', unsafe_allow_html=True)
league = st.selectbox("L", [
    "Premier League", 
    "Champions League", 
    "La Liga", 
    "Bundesliga", 
    "Series A", 
    "Ligue 1"
], label_visibility="collapsed")

st.markdown('<p style="color:#aaa; margin-left:15px; margin-top:15px;">Select Date</p>', unsafe_allow_html=True)
st.date_input("D", value=datetime.date.today(), label_visibility="collapsed")

# ၃။ Green Glossy Button
st.markdown('<div class="btn-green-glossy">Check Matches Now</div>', unsafe_allow_html=True)

# ၄။ Select Team Title
st.markdown('<div class="title-style" style="font-size:45px; margin-top:20px;">Select Team</div>', unsafe_allow_html=True)

# Premier League အသင်း ၂၀ စာရင်း
pl_teams = [
    "Arsenal", "Aston Villa", "Bournemouth", "Brentford", "Brighton & Hove Albion",
    "Burnley", "Chelsea", "Crystal Palace", "Everton", "Fulham",
    "Leeds United", "Liverpool", "Manchester City", "Manchester United", "Newcastle United",
    "Nottingham Forest", "Sunderland", "Tottenham Hotspur", "West Ham United", "Wolverhampton"
]

# Champions League အသင်း ၃၆ သင်းစာရင်း
cl_teams = [
    "AS Monaco", "Ajax Amsterdam", "Arsenal", "Atalanta", "Athletic Club",
    "Atlético Madrid", "Barcelona", "Bayer Leverkusen", "Bayern Munich", "Benfica",
    "Bodo/Glimt", "Borussia Dortmund", "Chelsea", "Club Brugge", "Eintracht Frankfurt",
    "F.C. København", "FK Qarabag", "Galatasaray", "Internazionale", "Juventus",
    "Kairat Almaty", "Liverpool", "Manchester City", "Marseille", "Napoli",
    "Newcastle United", "Olympiacos", "PSV Eindhoven", "Pafos", "Paris Saint-Germain",
    "Real Madrid", "Slavia Prague", "Sporting CP", "Tottenham Hotspur", "Union St.-Gilloise", "Villarreal"
]

# La Liga အသင်း ၂၀ စာရင်း
la_liga_teams = [
    "Alavés", "Athletic Club", "Atlético Madrid", "Barcelona", "Celta Vigo",
    "Elche", "Espanyol", "Getafe", "Girona", "Levante",
    "Mallorca", "Osasuna", "Rayo Vallecano", "Real Betis", "Real Madrid",
    "Real Oviedo", "Real Sociedad", "Sevilla", "Valencia", "Villarreal"
]

# ၅။ Home vs Away Section
c1, cvs, c2 = st.columns([2, 1, 2])

# League အလိုက် အသင်းစာရင်း ပြောင်းလဲခြင်း Logic
if league == "Premier League":
    current_teams = pl_teams
elif league == "Champions League":
    current_teams = cl_teams
elif league == "La Liga":
    current_teams = la_liga_teams
else:
    current_teams = ["Select Team"]

with c1:
    st.markdown('<p style="color:white; text-align:center; font-weight:900; font-size:12px;">HOME TEAM</p>', unsafe_allow_html=True)
    st.selectbox("H", current_teams, key="h", label_visibility="collapsed")

with cvs:
    st.markdown('<div style="display: flex; justify-content: center; align-items: center; height: 100%;"><div class="vs-ball">vs</div></div>', unsafe_allow_html=True)

with c2:
    st.markdown('<p style="color:white; text-align:center; font-weight:900; font-size:12px;">AWAY TEAM</p>', unsafe_allow_html=True)
    st.selectbox("A", current_teams, key="a", label_visibility="collapsed")

# ၆။ Orange Glossy Button
st.markdown('<div class="btn-orange-glossy">Generate Predictions</div>', unsafe_allow_html=True)
