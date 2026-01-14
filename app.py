import streamlit as st
import google.generativeai as genai
import requests
import datetime

# --- API SETUP ---
# Streamlit Secrets ထဲက Key တွေကို လှမ်းယူမယ်
try:
    GEMINI_API_KEY = st.secrets["GEMINI_API_KEY"]
    FOOTBALL_API_KEY = st.secrets["FOOTBALL_DATA_API_KEY"]
    
    genai.configure(api_key=GEMINI_API_KEY)
    model = genai.GenerativeModel('gemini-1.5-flash')
except Exception as e:
    st.error("Secrets ထဲမှာ API Keys များ ထည့်သွင်းရန် လိုအပ်ပါသည်။ (Settings > Secrets ထဲမှာ သွားထည့်ပေးပါ)")
    st.stop()

# --- FUNCTION: ပွဲစဉ်များ ဆွဲယူရန် ---
def get_matches(league_code, date_str):
    url = f"https://api.football-data.org/v4/matches?dateFrom={date_str}&dateTo={date_str}&competitions={league_code}"
    headers = {"X-Auth-Token": FOOTBALL_API_KEY}
    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            return response.json().get("matches", [])
        return []
    except:
        return []

# --- UI DESIGN ---
st.set_page_config(page_title="Football AI Pro", layout="centered")

st.markdown("""
    <style>
    .stApp { background-color: #121212; color: white; }
    .stButton>button {
        background: linear-gradient(90deg, #FF5F1F 0%, #FF8C00 100%);
        color: white; border-radius: 12px; height: 3.5em; width: 100%; font-weight: bold; border: none;
    }
    div[data-baseweb="select"] > div, div[data-baseweb="input"] > div {
        border: 2px solid #39FF14 !important; background-color: #1e1e1e !important;
    }
    h1, h3 { text-align: center; color: white; }
    </style>
    """, unsafe_allow_html=True)

st.title("⚽ Football AI Predictions")

# --- SELECTION ---
league_map = {
    "Premier League": "PL",
    "Champions League": "CL",
    "La Liga": "PD",
    "Serie A": "SA",
    "Bundesliga": "BL1"
}

sel_league = st.selectbox("Select League", list(league_map.keys()))
sel_date = st.date_input("Select Date", datetime.date.today())

# ပွဲစဉ်ရှာခြင်း
matches = get_matches(league_map[sel_league], sel_date.strftime("%Y-%m-%d"))

st.write("---")

home_team, away_team = "", ""

if matches:
    st.subheader("Select Match")
    match_options = [f"{m['homeTeam']['name']} vs {m['awayTeam']['name']}" for m in matches]
    selected_match_str = st.selectbox("ကန်မည့်ပွဲများ", match_options)
    
    for m in matches:
        if f"{m['homeTeam']['name']} vs {m['awayTeam']['name']}" == selected_match_str:
            home_team = m['homeTeam']['name']
            away_team = m['awayTeam']['name']
            break
else:
    st.warning("အဲဒီနေ့အတွက် ပွဲစဉ်များ ရှာမတွေ့ပါ။ အောက်တွင် အသင်းနာမည် တိုက်ရိုက်ရိုက်ထည့်ပါ။")
    col1, col2 = st.columns(2)
    with col1:
        home_team = st.text_input("Home Team Name", placeholder="Eg. Liverpool")
    with col2:
        away_team = st.text_input("Away Team Name", placeholder="Eg. Man City")

# --- PREDICTION LOG
