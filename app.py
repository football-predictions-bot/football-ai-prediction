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
    st.error("Secrets ထဲမှာ API Keys များ ထည့်သွင်းရန် လိုအပ်ပါသည်။")
    st.stop()

# --- FUNCTION: API ကနေ ပွဲစဉ်များ ဆွဲယူရန် ---
def get_matches(league_code, date_str):
    # API URL - သတ်မှတ်ထားတဲ့ ရက်စွဲနဲ့ လိဂ်အလိုက် ပွဲစဉ်ရှာခြင်း
    url = f"https://api.football-data.org/v4/matches?dateFrom={date_str}&dateTo={date_str}&competitions={league_code}"
    headers = {"X-Auth-Token": FOOTBALL_API_KEY}
    try:
        response = requests.get(url, headers=headers)
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
        color: white; border-radius: 15px; height: 3.5em; width: 100%; font-weight: bold; border: none;
    }
    div[data-baseweb="select"] > div, div[data-baseweb="input"] > div {
        border: 2px solid #39FF14 !important; background-color: #1e1e1e !important;
    }
    h1, h3 { text-align: center; }
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

# Background မှာ ပွဲစဉ်တွေကို ကြိုရှာမယ်
matches = get_matches(league_map[sel_league], sel_date.strftime("%Y-%m-%d"))

st.markdown("<h3>Select Match</h3>", unsafe_allow_html=True)

home_team, away_team = None, None

if matches:
    # ပွဲစဉ်စာရင်းကို Dropdown ထဲမှာ ပြမယ်
    match_options = [f"{m['homeTeam']['name']} vs {m['awayTeam']['name']}" for m in matches]
    selected_match_str = st.selectbox("ရွေးချယ်ထားသောနေ့တွင် ကန်မည့်ပွဲများ", match_options)
    
    # ရွေးလိုက်တဲ့ အသင်းနာမည်တွေကို သိမ်းမယ်
    for m in matches:
        if f"{m['homeTeam']['name']} vs {m['awayTeam']['name']}" == selected_match_str:
            home_team = m['homeTeam']['name']
            away_team = m['awayTeam']['name']
            break
else:
    st.warning("အဲဒီနေ့မှာ ရွေးချယ်ထားတဲ့ လိဂ်အတွက် ပွဲစဉ်များ မရှိသေးပါ။")

# --- PREDICTION ---
if st.button("Predictions") and home_team:
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
            st.markdown("---")
            st.markdown("### 🎯 AI Analysis Result")
            st.write(response.text)
        except Exception as e:
            st.error("AI တွက်ချက်ရာတွင် အမှားတစ်ခုရှိနေပါသည်။")
