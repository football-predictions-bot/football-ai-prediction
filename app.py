import streamlit as st
import google.generativeai as genai
import requests
import datetime

# --- API SETUP ---
try:
    GEMINI_API_KEY = st.secrets["GEMINI_API_KEY"]
    FOOTBALL_API_KEY = st.secrets["FOOTBALL_DATA_API_KEY"]
    
    genai.configure(api_key=GEMINI_API_KEY)
    model = genai.GenerativeModel('gemini-1.5-flash')
except Exception as e:
    st.error("Secrets ထဲမှာ API Keys များ ထည့်ရန် လိုအပ်ပါသည်။")
    st.stop()

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
    </style>
    """, unsafe_allow_html=True)

st.title("⚽ Football AI Predictions")

league_map = {
    "Premier League": "PL",
    "Champions League": "CL",
    "La Liga": "PD",
    "Serie A": "SA",
    "Bundesliga": "BL1"
}

sel_league = st.selectbox("Select League", list(league_map.keys()))
sel_date = st.date_input("Select Date", datetime.date.today())

# Fetch matches from API
matches = get_matches(league_map[sel_league], sel_date.strftime("%Y-%m-%d"))

st.write("---")

home_team, away_team = "", ""

if matches:
    st.subheader("Select Match from List")
    match_options = [f"{m['homeTeam']['name']} vs {m['awayTeam']['name']}" for m in matches]
    selected_match_str = st.selectbox("ရွေးချယ်ထားသောနေ့တွင် ကန်မည့်ပွဲများ", match_options)
    
    for m in matches:
        if f"{m['homeTeam']['name']} vs {m['awayTeam']['name']}" == selected_match_str:
            home_team = m['homeTeam']['name']
            away_team = m['awayTeam']['name']
            break
else:
    # API က ပွဲရှာမတွေ့ရင် ကိုယ့်ဘာသာ ရိုက်ထည့်ဖို့ ပြပေးမယ်
    st.warning("အဲဒီနေ့အတွက် ပွဲစဉ်များ ရှာမတွေ့ပါ။ အောက်တွင် အသင်းနာမည် တိုက်ရိုက်ရိုက်ထည့်ပါ။")
    col1, col2 = st.columns(2)
    with col1:
        home_team = st.text_input("Home Team Name", placeholder="Eg. Liverpool")
    with col2:
        away_team = st.text_input("Away Team Name", placeholder="Eg. Man City")

# --- PREDICTION ---
if st.button("Get Predictions"):
    if home_team and away_team:
        with st.spinner('AI က ပွဲစဉ်များကို သုံးသပ်နေပါသည်...'):
            prompt = f"""
            Analyze the match: {home_team} vs {away_team} in {sel_league}.
            Provide:
            1. Correct Score Prediction
            2. Over/Under 2.5 Goals
            3. Corner Prediction
            4. Both Teams to Score (Yes/No)
            5. Yellow Cards Prediction
            Language: Burmese with emojis.
            """
            try:
                response = model.generate_content(prompt)
                st.markdown("### 🎯 AI Analysis Result")
                st.write(response.text)
            except:
                st.error("AI တွက်ချက်ရာတွင် အမှားရှိနေပါသည်။")
    else:
        st.error("အသင်းနာမည်များ ထည့်သွင်းပေးပါ။")
